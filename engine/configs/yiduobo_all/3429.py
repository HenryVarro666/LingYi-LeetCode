STATES = [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]


def _cc(S, r, c, v):
    if 'index' not in S:
        return None
    n = S['n']
    if r == S['index']:
        return ('blue', 'pink')[0] if 'st' not in S else ('yellow' if c == S['states'][S['st']][0] else 'blue')
    if r == n - S['index'] - 1:
        return 'yellow' if 'st' in S and c == S['states'][S['st']][1] else 'pink'
    return None


def _fcol(S, i, v):
    if 'st' in S and i == S['st']:
        return 'yellow'
    if 'pre' in S and i == S['pre'] and 'g' in S:
        return 'cyan'
    return None


def _cond(S, B, ret):
    a, b = S.states[S.st], S.states[S.pre]
    if a[0] == b[0] or a[1] == b[1]:
        return f'`{a}` 和上一列 `{b}`：' + ('左边同色' if a[0] == b[0] else '右边同色') + ' → ==冲突==，不能转移'
    return f'`{a}` 和上一列 `{b}`：上下都不同色 → 可以从 `g[{S.pre}]` 转移'


def _cand(S, B, ret):
    first, second = S.states[S.st]
    return (f'`c = g[{S.pre}] + cost[{S.index}][{first}] + cost[{S.n - S.index - 1}][{second}]` '
            f'= {S.g[S.pre]} + {S.cost[S.index][first]} + {S.cost[S.n - S.index - 1][second]} = =={S.c}==')


CONFIG = dict(
    num=3429, title='粉刷房子 IV', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='对折成两行 · 列状态 DP',
    tags=['灵神题单·动态规划', '难度分 2166'],
    code='''
class Solution(object):
    def minCost(self, n, cost):
        
        states = {0: (0, 1),
                  1: (0, 2),
                  2: (1, 0),
                  3: (1, 2),
                  4: (2, 0),
                  5: (2, 1)
        }
        f = [0] * 6
        for st in states:
            first, second = states[st]
            f[st] = cost[0][first] + cost[-1][second]
        
        for index in range(1, n // 2):
            g = f[:]
            f = [None] * 6
            for st in states:
                for pre in states:
                    if states[st][0] == states[pre][0] or states[st][1] == states[pre][1]:
                        continue
                    first, second = states[st]
                    c = g[pre] + cost[index][first] + cost[n - index - 1][second]
                    if f[st] is None or f[st] > c:
                        f[st] = c
        
        return min(f)
''',
    call='Solution().minCost(4, [[3,5,7],[6,2,9],[4,8,1],[7,3,5]])',
    expect=9,
    views=[
        dict(type='grid', var='cost', label='cost（对折：蓝 = 上行房子 index，粉 = 下行对称房子，黄 = 当前列选的颜色）', cell=60, h=270,
             color=_cc, cols=['色0', '色1', '色2']),
        dict(type='array', var=lambda S: [x if x is not None else '·' for x in S.get('f', [])],
             label='f[state]（state 0~5 = (0,1) (0,2) (1,0) (1,2) (2,0) (2,1)；黄 = 正在算）', cell=80, h=170,
             color=_fcol),
        dict(type='array', var='g', label='g（上一列的 f，青 = 当前考察的 pre）', cell=80, h=170,
             color=lambda S, i, v: 'cyan' if S.get('pre') == i else None),
    ],
    watch=['index', 'st', 'pre', ('c', 'c', 'yellow')],
    captions={
        'states = {0': lambda S, B, r: ('一列有上下两个房子，颜色必须不同：==共 6 种组合==，编号 0~5' if 'states' not in B else '编号 → (上格颜色, 下格颜色)，已建好'),
        'f = [0] * 6': '`f[st]`：粉刷完前若干列，最后一列组合为 `st` 的最低成本',
        'f[st] = cost[0]': '第 0 列 `{states[st]}`：`cost[0][{first}] + cost[-1][{second}]` = `{f[st]}`',
        'for index in range': lambda S, B, r: ('所有列都算完' if 'index' in B and B.index == S.index else f'开始第 `{S.index}` 列：房子 `{S.index}` 和房子 `{S.n - S.index - 1}` 同一列'),
        'g = f[:]': '把上一列的结果存进 `g`，`f` 重新开始算（滚动数组，省掉 index 维）',
        'f = [None] * 6': '`f` 清空，等下面逐个状态填',
        'if states[st][0]': _cond,
        'c = g[pre]': _cand,
        'if f[st] is None': lambda S, B, r: (f'`f[{S.st}]` 还没有值 → 直接取 `c = {S.c}`' if B.f[S.st] is None
                                              else (f'`{B.f[S.st]} > {S.c}` → 更小，更新为 {S.c}' if B.f[S.st] > S.c else f'`{B.f[S.st]} ≤ {S.c}` → 保持不变')),
        'f[st] = c': '`f[{st}] = {f[st]}`',
        'return min': '最后一列所有组合里取最小 → =={ret}==',
    },
    skip=['}', '1: (0, 2)', '2: (1, 0)', '3: (1, 2)', '4: (2, 0)', '5: (2, 1)', 'continue', 'for st in states', 'for pre in states', 'first, second = states[st]'],
    max_steps=54,
    cards=dict(
        one_liner='把一排房子从正中间对折，变成两行的矩阵',
        complexity='时间 `O(n)`，空间 `O(1)`（颜色组合固定 6 种）',
        problem=['`n` 栋房子（偶数）排成一排，`cost[i][j]` 是涂颜色 `j` 的成本',
                 '相邻不同色，==两端等距的两栋也不同色==，求最低总成本',
                 '示例：`n=4`，`cost=[[3,5,7],[6,2,9],[4,8,1],[7,3,5]]` → `9`'],
        quote='对于这类单行等距的问题，可以在正中间对折一下，变为两行，n // 2列的矩阵，那么问题就变成了保证矩阵所有单元格的颜色在水平和竖直方向下都不相同时的最低成本。',
        quote_src='—— yiduobo 题解',
        idea=['对折后每一列 = 一对等距房子，列内两格不同色 → 6 种组合',
              '相邻两列：上格不同、下格也不同才能转移',
              '`f[index][state]` 只依赖上一列，滚动成 `f` 和 `g`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '下行房子下标是 `n - index - 1`，别写成 `n - index`',
                 '转移条件是「上下两格都和上一列不同」，只要有一边同色就跳过',
                 '同类：等距、对称约束的题都可以先对折'],
    ),
)
