GRID = [[5, 3], [4, 0], [2, 1]]
MC = [[9, 8], [1, 5], [10, 12], [18, 6], [2, 4], [14, 3]]


def _ft(S):
    f = S.get('f')
    if f is None:
        return None
    return [['∞' if x == float('inf') else x for x in r] for r in f]


def _fc(S, i, j, v):
    a, b, k = S.get('i'), S.get('j'), S.get('k')
    if a is None or b is None:
        return None
    if (i, j) == (a, b):
        return 'yellow'
    if k is not None and (i, j) == (a + 1, k) and S.get('_line') in (11, 12):
        return 'blue'
    return None


def _kcap(S, B, ret):
    i, j, k, c, g = S.i, S.j, S.k, S.c, S.g
    old = B.f[i][j]
    cand = S.f[i + 1][k] + c
    o = '∞' if old == float('inf') else old
    tail = '更小，更新' if cand < old else '不更小，保留'
    return f'走到下一行第 `{k}` 列：`f[{i+1}][{k}] + moveCost[{g}][{k}] = {S.f[i+1][k]} + {c} = {cand}`，与旧值 `{o}` 比 → {tail}：`f[{i}][{j}]` = =={S.f[i][j]}=='


CONFIG = dict(
    num=2304, title='网格中的最小路径代价', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='倒序递推 · 枚举下一步选哪列',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1658'],
    code='''
class Solution:
    def minPathCost(self, grid: List[List[int]], moveCost: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        f = [[inf] * n for _ in range(m)]
        f[-1] = grid[-1]
        for i in range(m - 2, -1, -1):
            for j, g in enumerate(grid[i]):
                for k, c in enumerate(moveCost[g]):  # 移动到下一行的第 k 列
                    f[i][j] = min(f[i][j], f[i + 1][k] + c)
                f[i][j] += g
        return min(f[0])
''',
    call=f'Solution().minPathCost({GRID}, {MC})',
    expect=17,
    skip=['for j, g in', 'for _ in range'],
    views=[
        dict(type='grid', var='grid', label='grid（黄 = 当前格 (i,j)，值 g 决定 moveCost 的哪一行）', cell=84, h=290,
             cursors=[('i', 'j', 'yellow')]),
        dict(type='table', var=_ft, label='f[i][j]：从 (i,j) 出发到最后一行的最小代价（黄 = 正在算，蓝 = 下一行目标）',
             cell=84, h=290, color=_fc),
        dict(type='text', fn=lambda S: (f"`moveCost[{S['g']}] = {MC[S['g']]}`：从值 {S['g']} 的格子移到下一行各列的代价"
                                         if 'g' in S else ''), size=24, h=50),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), 'g', 'k', 'c'],
    captions={
        'm, n = len': '`m = {m}` 行，`n = {n}` 列',
        'f = [[inf]': '`f[i][j]` 先全设为 `inf`，等着取最小值',
        'f[-1] = grid[-1]': '边界：最后一行不用再移动，`f[m-1][j] = grid[m-1][j]` = {f[-1]}',
        'for i in range': lambda S, B, r: ('`i` 从倒数第二行往上：算 `f[i]` 需要先有 `f[i+1]` → ==i 倒序==' if 'i' in S and S.i == S.m - 2
                                           else '所有行都算完了，答案在第一行' if S.i == B.get('i') else f'`i = {S.i}`：上一行已经算好了，继续往上'),
        'f[i][j] = min': _kcap,
        'f[i][j] += g': '加上当前格自己的值 `{g}`：`f[{i}][{j}]` = =={f[i][j]}==',
        'return min(f[0])': '起点可以是第一行任意格，取 `min(f[0])` = =={ret}==',
    },
    cards=dict(
        one_liner='枚举下一步去哪一列，倒着从最后一行往上递推',
        complexity='时间 `O(mn^2)`，空间 `O(mn)`',
        problem=['`grid` 每个格子的值互不相同；从第一行任意格出发，每步可移到下一行任意格',
                 '移动代价由 `moveCost[格子值][目标列]` 给出',
                 '路径代价 = 经过格子的值之和 + 移动代价之和，求到最后一行的最小值',
                 '示例：`grid=[[5,3],[4,0],[2,1]]` → `17`'],
        quote='定义 dfs(i,j) 表示从 grid[i][j] 出发，到达最后一行任意单元格的最小路径代价。枚举下一步的位置……',
        quote_src='—— 灵茶山艾府题解',
        idea=['「枚举选哪个」：下一步去 `grid[i+1][k]`，代价 `moveCost[g][k]`',
              '`f[i][j] = g + min(f[i+1][k] + moveCost[g][k])`',
              '算 `f[i]` 前必须先有 `f[i+1]`，所以 `i` 倒序'],
        summary=['时间 `O(mn^2)`，空间 `O(mn)`',
                 '易错：`moveCost` 的行下标是格子的==值== `g`，不是坐标',
                 '易错：最后一行初值是 `grid[-1]`，不加移动代价',
                 '灵神还给了朴素递归、`@cache` 记忆化、原地修改 `grid` 的写法'],
    ),
)
