G = [[1, 2, 1], [3, 0, 2]]


def _ftab(S):
    f = S.get('f')
    if f is None:
        return None
    return [[''.join(map(str, f[i + 1][j + 1])) for j in range(len(f[0]) - 1)] for i in range(len(f) - 1)]


def _fcol(S, i, j, v):
    a, b, x = S.get('i'), S.get('j'), S.get('x')
    if a is None or 'val' not in S or S.get('_line') not in (13, 14):
        return None
    if (i, j) == (a, b):
        return 'yellow'
    if (i, j) == (a, b - 1) or (i, j) == (a - 1, b):
        return 'blue'
    return None


def _xcap(S, B, ret):
    i, j, x, val = S.i, S.j, S.x, S.val
    y = x ^ val
    return (f'`f[{i+1}][{j+1}][{x}] = f[{i+1}][{j}][{y}] + f[{i}][{j+1}][{y}]` = '
            f'`{S.f[i+1][j][y]} + {S.f[i][j+1][y]}` = =={S.f[i+1][j+1][x]}==（前一格异或值必须是 `{x}^{val}={y}`）')


CONFIG = dict(
    num=3393, title='统计异或值为给定值的路径数目', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='网格 DP + 异或值作第三维（递推）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1573'],
    code='''
class Solution:
    def countPathsWithXorValue(self, grid: List[List[int]], k: int) -> int:
        MOD = 1_000_000_007
        u = 1 << max(map(max, grid)).bit_length()
        if k >= u:
            return 0

        m, n = len(grid), len(grid[0])
        f = [[[0] * u for _ in range(n + 1)] for _ in range(m + 1)]
        f[0][1][0] = 1
        for i, row in enumerate(grid):
            for j, val in enumerate(row):
                for x in range(u):
                    f[i + 1][j + 1][x] = (f[i + 1][j][x ^ val] + f[i][j + 1][x ^ val]) % MOD
        return f[m][n][k]
''',
    call=f'Solution().countPathsWithXorValue({G}, 0)',
    expect=2,
    skip=['MOD = ', 'for x in range', 'for _ in range', 'for i, row', 'for j, val'],
    views=[
        dict(type='grid', var='grid', label='grid（黄 = 当前格 (i,j)）', cell=84, h=210,
             cursors=[('i', 'j', 'yellow')]),
        dict(type='table', var=_ftab, label='f（四位 = x 为 0,1,2,3 的方案数；黄 = 正在算，蓝 = 来源）',
             cell=120, h=260, color=_fcol),
        dict(type='text', fn=lambda S: (f"枚举 `x = {S['x']}`，当前格值 `val = {S['val']}`，需要来源异或值 `{S['x']} ^ {S['val']} = {S['x'] ^ S['val']}`"
                                         if 'x' in S and 'val' in S else '`f[i+1][j+1][x]` = 到 `(i,j)` 且路径异或值为 `x` 的方案数'), size=24, h=50),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), 'val', 'x', ('k', 'k', 'green')],
    captions={
        'u = 1 <<': '`u = {u}`：最大值 `{max(map(max, grid))}` 的二进制长度是 `{max(map(max, grid)).bit_length()}`，异或值不会超过 `{u-1}`',
        'if k >= u': lambda S, B, r: (f'`k = {S.k} >= u = {S.u}`：异或值根本凑不出来，直接返回 0' if S.k >= S.u
                                      else f'`k = {S.k} < u = {S.u}`，目标值凑得出来，继续'),
        'm, n = len': '`m = {m}`，`n = {n}`',
        'f = [[[0]': '`f` 多开一圈（下标 +1）：`f[0][*]`、`f[*][0]` 是出界，方案数为 0',
        'f[0][1][0] = 1': '把起点放进去：`f[0][1][0] = 1`（空路径异或值为 0），这样算 `(0,0)` 时无需特判',
        'f[i + 1][j + 1][x] =': _xcap,
        'return f[m][n][k]': '终点 `f[{m}][{n}][{k}]` = =={ret}== 条路径异或值等于 `k`',
    },
    cards=dict(
        one_liner='把路径异或值当作第三维：异或可移项，来源值 = x ^ 当前格',
        complexity='时间 `O(mnU)`，空间 `O(mnU)`',
        problem=['`m x n` 的 `grid`，从左上走到右下，每步向右或向下',
                 '统计路径上所有数的 ==XOR 等于 k== 的路径条数（对 `1e9+7` 取余）',
                 '示例：`grid=[[2,1,5],[7,10,0],[12,6,4]]`，`k=11` → `3`',
                 '本视频：`grid=[[1,2,1],[3,0,2]]`，`k=0` → `2`'],
        quote='异或运算和加减法是一样的，可以移项，得 y = x ⊕ grid[i][j]',
        quote_src='—— 灵茶山艾府题解（方法一）',
        idea=['`dfs(i,j,x)`：到 `(i,j)` 且异或值为 `x` 的方案数',
              '从左或从上来，来源异或值 `y = x ^ grid[i][j]`，两边相加',
              '把记忆化搜索 1:1 翻译成递推 `f`，多开一圈当出界哨兵'],
        summary=['时间/空间 `O(mnU)`，`U` 是格子最大值',
                 '易错：`k >= u` 时一定无解，先返回 0，避免下标越界',
                 '易错：`f[0][1][0] = 1` 才能让起点算对，否则全是 0',
                 '灵神还给了方法一：`@cache` 记忆化搜索，倒序递归，思路相同'],
    ),
)
