def _cd(S, B, ret):
    return f'数位 `{S.num}` 的成本 `{S.c}`'


def _tcolor(S, i, j, v):
    if S.get('i') is None:
        return None
    if i == S['i'] and j == 0:
        return 'yellow'
    if S.get('c') is not None and i == S['i'] - S['c'] and S['i'] >= S['c'] and j == 0:
        return 'blue'
    if S.get('num') is not None and i == S['i'] and j == S['num'] and S.get('_line', 0) >= 17:
        return 'green'
    return None


CONFIG = dict(
    num=1449, title='数位成本和为目标值的最大数字', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='背包 · 记录各数位个数 · 比较集合',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1927'],
    code='''
class Solution(object):
    def largestNumber(self, cost, target):

        cost_dict = {}
        for num in range(9, 0, -1):
            c = cost[num - 1]
            if c not in cost_dict:
                cost_dict[c] = num
        
        f = [[0] * 10 for _ in range(target + 1)]
        for i in range(1, target + 1):
            for c, num in cost_dict.items():
                if i == c or (i > c and f[i - c][0] > 0):
                    if f[i][0] < f[i - c][0] + 1:
                        f[i] = f[i - c][:]
                        f[i][0] += 1
                        f[i][num] += 1
                    elif f[i][0] == f[i - c][0] + 1:
                        flag = False
                        tmp = f[i - c][:]
                        tmp[num] += 1
                        for compare_num in range(9, 0, -1):
                            if f[i][compare_num] < tmp[compare_num]:
                                flag = True
                                break
                            elif f[i][compare_num] > tmp[compare_num]:
                                break
                        
                        if flag:
                            f[i] = f[i - c][:]
                            f[i][0] += 1
                            f[i][num] += 1
        
        if f[target][0] == 0:
            return '0'
        return ''.join([str(num) * f[target][num] for num in range(9, 0, -1)])
''',
    call='Solution().largestNumber([2,3,2,3,2,3,2,3,2], 5)',
    expect='98',
    skip=['c = cost[num - 1]', 'for num in range(9', 'if c not in cost_dict', 'for c, num in', 'for compare_num', 'flag = False', 'tmp = ', 'tmp['],
    max_steps=90,
    views=[
        dict(type='map', var='cost_dict', label='cost_dict：成本 → 该成本下最大的数位（同成本小数位无用）', h=130,
             fmt=lambda k, v: f'成本{k} → 数位{v}'),
        dict(type='table', var='f', label='f[i]：[总个数, 数位1 的个数 … 数位9 的个数]（黄 = 正在算，蓝 = 来源）', h=400, cell=62,
             rows=lambda S: [f'成本{k}' for k in range(len(S['f']))], cols=['总数', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
             color=_tcolor),
    ],
    watch=[('i', 'i', 'yellow'), ('c', 'c', 'blue'), ('num', 'num', 'green')],
    captions={
        'cost_dict[c] = num': '成本 `{c}` 第一次出现：留下数位 `{num}`（从 9 往 1 遍历，所以留下的是最大的）',
        'for i in range(1': '算成本恰好为 `{i}` 的最优方案 `f[{i}]`',
        'f = [[0]': '`f[i][0]` = 成本 i 时最多几位；`f[i][k]` = 数位 k 用了几个',
        'if i == c or': lambda S, B, r: (f'数位 `{S.num}`（成本 `{S.c}`），目标成本 `{S.i}`：'
                                         + ('==恰好一个就够==' if S.i == S.c else
                                            (f'`f[{S.i - S.c}]` 可达，能在它后面再加一个' if S.i > S.c and S.f[S.i - S.c][0] > 0 else '凑不出 → 跳过'))),
        'if f[i][0] < f[i - c][0] + 1': lambda S, B, r: (
            f'`f[{S.i}][0] = {S.f[S.i][0]}` < `f[{S.i - S.c}][0] + 1 = {S.f[S.i - S.c][0] + 1}`：位数更多 → ==直接替换=='
            if S.f[S.i][0] < S.f[S.i - S.c][0] + 1 else f'`f[{S.i}][0] = {S.f[S.i][0]}` 不比 `{S.f[S.i - S.c][0] + 1}` 小 → 看是否同位数'),
        'f[i] = f[i - c][:]': '复制 `f[{i - c}]`',
        'f[i][0] += 1': '总位数 +1：`f[{i}][0] = {f[i][0]}`',
        'f[i][num] += 1': '数位 `{num}` 个数 +1：`f[{i}][{num}] = {f[i][num]}`',
        'elif f[i][0] ==': lambda S, B, r: ('位数相同（`%d`）：要比较哪个数字集合更大' % S.f[S.i][0] if S.f[S.i][0] == S.f[S.i - S.c][0] + 1
                                            else '现有位数更多 → 不用换'),
        'if flag': lambda S, B, r: ('从 9 往 1 比较，新集合在某个数位上更多 → ==换成新的==' if S.flag else '旧集合不比新集合差 → 保持不变'),
        'return \'0\'': '`f[target][0] = 0`：凑不出，返回 "0"',
        'return \'\'.join': '从 9 到 1 依次拼：每个数位重复它的个数 → `{ret}`',
    },
    cards=dict(
        one_liner='不存数字本身，只存「每个数位用了几个」',
        complexity='时间 `O(9·target)`，空间 `O(10·target)`',
        problem=['数位 `k` 的成本是 `cost[k-1]`，总成本恰好等于 `target`，不含数位 0',
                 '返回能得到的最大整数（字符串），做不到返回 `"0"`',
                 '示例：`cost=[4,3,2,5,6,7,2,5,5], target=9` → `"7772"`；视频用 `cost=[2,3,2,3,2,3,2,3,2], target=5` → `"98"`'],
        quote='直接保存数字显然是不行的，因为在极限情况下，这个数字可能长达5000位。……只需要储存选择了哪些数字集合。',
        quote_src='—— yiduobo 题解原文',
        idea=['位数越多数字越大；位数相同，高位放大数字 → 集合可以不存顺序',
              '`f[i]` 记录总位数和每个数位的个数；比较两个集合：先比位数，再从 9 到 1 比个数',
              '同成本的数位只留最大的，小的永远用不上'],
        summary=['时间 `O(9·target)`，空间 `O(10·target)`',
                 '`f[i - c][0] > 0` 保证前一状态可达，避免从不可行状态转移',
                 '位数相同的时候必须从 9 往 1 比较个数，才能决定字典序',
                 '原文即 Python 3 可运行写法，未作修改',
                 '对比灵神：灵神只存长度，再用 f 倒推；yiduobo 每个状态存下完整的个数向量'],
    ),
)
