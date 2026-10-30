def _t(S):
    if 'x' in S and 'y' in S and 'delta' in S and S.get('_line') != 8:
        return f"第 `{S['x']}` 颗给第 `{S['y']}` 颗：转移 `gem[{S['x']}] // 2` = =={S['delta']}=="
    return ''


CONFIG = dict(
    num='LCP 50', title='宝石补给', difficulty='Easy', category='模拟',
    author='yiduobo', technique='直接模拟 · 最大减最小',
    tags=[],
    code='''
class Solution(object):
    def giveGem(self, gem, operations):

        for x, y in operations:
            delta = gem[x] // 2
            gem[x] -= delta
            gem[y] += delta

        ma = mi = gem[0]
        for g in gem[1:]:
            ma = max(ma, g)
            mi = min(mi, g)
        
        return ma - mi
''',
    call='Solution().giveGem([8,3,5,6], [[0,1],[2,3],[1,2]])',
    expect=4,
    views=[
        dict(type='array', var='gem', label='gem（每位勇者的宝石数）', pointers={'x': 'pink', 'y': 'blue'},
             color=lambda S, i, v: 'pink' if 'x' in S and i == S['x'] else 'blue' if 'y' in S and i == S['y'] else None, h=260),
        dict(type='array', var=lambda S: [f'{a}→{b}' for a, b in S['operations']], label='operations（x 给 y 一半）', h=200,
             color=lambda S, i, v: 'yellow' if 'x' in S and [S['x'], S['y']] == S['operations'][i] else None),
        dict(type='text', fn=lambda S: f"当前最大 `{S['ma']}`，最小 `{S['mi']}`，差 `{S['ma'] - S['mi']}`" if 'ma' in S else '', size=30, h=110),
    ],
    watch=[('x', 'x', 'pink'), ('y', 'y', 'blue'), 'delta', ('ma', 'ma', 'orange'), ('mi', 'mi', 'cyan')],
    captions={
        'for x, y in operations': lambda S, B, r: ('所有转移都做完，循环结束' if 'x' in B and B.x == S.x and B.y == S.y
                                          else f'下一次转移：`{S.x}` 号把一半宝石给 `{S.y}` 号'),
        'delta = gem': '`{x}` 号有 `{B.gem[x]}` 颗，一半（向下取整）= =={delta}==',
        'gem[x] -= delta': '`gem[{x}]` 减少 `{delta}` → =={gem[x]}==',
        'gem[y] += delta': '`gem[{y}]` 增加 `{delta}` → =={gem[y]}==',
        'ma = mi = gem[0]': '最大值、最小值都先取 `gem[0]` = `{ma}`',
        'for g in gem[1:]': '看下一个数 `g = {g}`',
        'ma = max': '`ma = max({B.ma}, {g})` = =={ma}==',
        'mi = min': '`mi = min({B.mi}, {g})` = =={mi}==',
        'return ma - mi': '最大 `{ma}` − 最小 `{mi}` = =={ma - mi}==',
    },
    cards=dict(
        one_liner='照着规则模拟转移，最后拿最大值减最小值',
        complexity='时间 `O(n + m)`，空间 `O(1)`',
        problem=['`gem[i]` 是第 `i` 位勇者的宝石数，`operations[j] = [x, y]`',
                 '每次 `x` 把自己宝石的一半（向下取整）给 `y`',
                 '全部操作后，返回宝石最多与最少的差',
                 '本视频：`[8,3,5,6]` → `4`'],
        quote='直接模拟宝石转移的过程，最后一趟遍历，找出当前宝石数组中的最大值和最小值，二者之差即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['每次操作 `delta = gem[x] // 2`，`x` 减 `delta`，`y` 加 `delta`',
              '操作按顺序做，前一次的结果会影响下一次',
              '最后线性扫描求最大、最小'],
        summary=['时间 `O(n + m)`，空间 `O(1)`',
                 '易错：`delta` 要先算好再加减，不能边减边用新的 `gem[x]`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '宝石总数不变，只是在重新分配'],
    ),
)
