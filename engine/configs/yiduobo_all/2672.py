def _col(S, i, v):
    if 'index' not in S or '_inner' not in S or 'c' not in S['_inner']:
        return None
    k = S['index']
    if i == k:
        return 'yellow'
    if i in (k - 1, k + 1) and v and v == S['color'][k]:
        return 'green'
    return None


CONFIG = dict(
    num=2672, title='有相同颜色的相邻元素数目', difficulty='Medium', category='模拟',
    author='yiduobo', technique='一趟遍历 · 分情况加减',
    tags=[],
    code='''
class Solution(object):
    def colorTheArray(self, n, queries):

        color = [0] * n
        res = []
        now = 0
        for index, c in queries:
            if color[index] > 0:
                if index > 0 and color[index] == color[index - 1]:
                    now -= 1
                if index < n - 1 and color[index] == color[index + 1]:
                    now -= 1
            
            color[index] = c
            if index > 0 and color[index] == color[index - 1]:
                now += 1
            if index < n - 1 and color[index] == color[index + 1]:
                now += 1
            
            res.append(now)
        
        return res
''',
    call='Solution().colorTheArray(4, [[0,2],[1,2],[3,1],[1,1],[2,1]])',
    expect=[0, 1, 1, 0, 2],
    views=[
        dict(type='array', var='color', pointers={'index': 'blue'}, color=_col, h=200, label='color（黄 = 被染的格子，绿 = 与它同色的邻居）'),
        dict(type='array', var='res', h=130, label='res'),
    ],
    watch=[('index', 'index', 'blue'), ('c', 'c', 'pink'), ('now', 'now', 'green')],
    captions={
        'color = [0]': '`color` 记录每个位置的颜色，0 表示未染色',
        'now = 0': '`now` = 当前相邻同色对数，只在每次修改时增量更新',
        'for index, c in queries': lambda S, B, r: ('查询都处理完了，退出循环' if len(S.res) == len(S.queries)
                                                     else f'这次把位置 `{S.index}` 染成 `{S.c}`'),
        'if color[index] > 0': lambda S, B, r: (f'位置 {S.index} 原来颜色是 `{S.color[S.index]}`，有颜色 → 先检查旧的配对要不要扣掉'
                                                 if S.color[S.index] > 0 else f'位置 {S.index} 原来没有颜色 → 没有旧配对，不用扣'),
        'if index > 0 and color[index] == color[index - 1]': lambda S, B, r: (
            f'和左边比：左边 `{S.color[S.index-1] if S.index > 0 else "无"}`，自己 `{S.color[S.index]}`，'
            + ('相同 → 配对数变化 1' if S.index > 0 and S.color[S.index] == S.color[S.index-1] else '不同 → 不变')),
        'if index < n - 1 and color[index] == color[index + 1]': lambda S, B, r: (
            f'右边 `{S.color[S.index+1] if S.index < S.n-1 else "无"}`，自己 `{S.color[S.index]}`，'
            + ('相同 → 配对数变化 1' if S.index < S.n-1 and S.color[S.index] == S.color[S.index+1] else '不同 → 不变')),
        'now -= 1': '旧颜色的配对作废，`now` 减 1 → =={now}==',
        'color[index] = c': '改色：`color[{index}]` = =={c}==',
        'now += 1': '新颜色形成了新配对，`now` 加 1 → =={now}==',
        'res.append': '记下这次修改后的配对数 =={now}==',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='每次改色只影响左右两对，在上一次答案上增量修改',
        complexity='时间 `O(n+q)`，空间 `O(n)`',
        problem=['长度为 `n` 的数组初始全 0（未染色），依次执行 `[index, color]` 染色',
                 '每次染色后，统计颜色相同的相邻对数',
                 '示例：`n=4`，`[[0,2],[1,2],[3,1],[1,1],[2,1]]` → `[0,1,1,0,2]`'],
        quote='每次修改颜色的操作实际上只会影响到修改的位置以及与该位置相邻位置的配对。',
        quote_src='—— yiduobo 题解原文',
        idea=['修改前：旧颜色若和左（右）邻居相同，说明有一对要作废，各减 1',
              '修改后：新颜色若和左（右）邻居相同，形成新的一对，各加 1',
              '边界用 `index > 0`、`index < n - 1` 单独判断'],
        summary=['时间 `O(n+q)`，空间 `O(n)`',
                 '易错点：未染色（0）的位置不参与扣减，要先判断 `color[index] > 0`',
                 '先减旧后加新，顺序不能反',
                 '对比灵神：灵神用哨兵避免边界判断，yiduobo 显式写边界条件'],
    ),
)
