G0 = [[5, 2, 4], [3, 0, 5]]
K0 = 3
M0, N0 = len(G0), len(G0[0])


def _flat(S):
    f = S.get('f')
    if f is None:
        return None
    return [f[i][j] for i in range(M0) for j in range(N0)]


def _fc(S, r, c, v):
    i, j, rr = S.get('i'), S.get('j'), S.get('r')
    if i is None or rr is None or S.get('_line', 0) < 14:
        return None
    if (r, c) == (i * N0 + j, rr):
        return 'yellow'
    if S.get('_line') in (17, 16) and i + 1 < M0 and (r, c) == ((i + 1) * N0 + j, (rr + G0[i + 1][j]) % K0):
        return 'blue'
    if S.get('_line') in (19, 18) and j + 1 < N0 and (r, c) == (i * N0 + j + 1, (rr + G0[i][j + 1]) % K0):
        return 'green'
    return None


def _text(S):
    i, j, r = S.get('i'), S.get('j'), S.get('r')
    if i is None or r is None:
        return '`f[i][j][r]`：从左上走到 `(i,j)`、路径和模 `k` 为 `r` 的路径数；向前「推」给右/下'
    return f'当前 `(i,j) = ({i},{j})`，余数 `r = {r}`，方案数 `f = {S["f"][i][j][r]}`：新余数 = `(r + 目标格值) % {K0}`'


CONFIG = dict(
    num=2435, title='矩阵中和能被 K 整除的路径', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='三维 DP（向前推送）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1952'],
    code='''
class Solution(object):
    def numberOfPaths(self, grid, k):

        m = len(grid)
        n = len(grid[0])

        f = [[[0] * k for j in range(n)] for i in range(m)]

        f[0][0][grid[0][0] % k] = 1
        mod = 10 ** 9 + 7
        for i in range(m):
            for j in range(n):
                for r in range(k):
                    if f[i][j][r] > 0:
                        f[i][j][r] %= mod
                        if i + 1 < m:
                            f[i + 1][j][(r + grid[i + 1][j]) % k] += f[i][j][r]
                        if j + 1 < n:
                            f[i][j + 1][(r + grid[i][j + 1]) % k] += f[i][j][r]
        
        return f[-1][-1][0]
''',
    call=f'Solution().numberOfPaths({G0}, {K0})',
    expect=1,
    max_steps=80,
    skip=['m = len', 'n = len', 'mod = ', 'for i in range', 'for j in range', 'for r in range', 'f[i][j][r] %= mod'],
    views=[
        dict(type='grid', var='grid', label='grid（黄框 = 当前格子）', h=150, cell=60,
             cursors=[('i', 'j', 'yellow', '')]),
        dict(type='text', fn=_text, size=21, h=55),
        dict(type='table', var=_flat, label='f[i][j][r]（行 = 格子 i,j，列 = 余数 r）：黄 = 当前，蓝 = 推给下边，绿 = 推给右边', h=330, cell=46,
             rows=lambda S: [f'{i},{j}' for i in range(M0) for j in range(N0)],
             cols=lambda S: [f'r={c}' for c in range(K0)], color=_fc),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('r', 'r', 'purple'), ('f[i][j][r]', 'f[i][j][r]', 'green')],
    captions={
        'f = [[[0]': '`f[i][j][r]`：走到 `(i,j)`、路径和模 `k` 余 `r` 的路径数，初始全 0',
        'f[0][0][grid[0][0] % k] = 1': '起点：路径只含 `grid[0][0] = {grid[0][0]}`，余数 `{grid[0][0] % k}` 的方案数为 `1`',
        'if f[i][j][r] > 0': lambda S, B, r: (f'`f[{S.i}][{S.j}][{S.r}] = {S.f[S.i][S.j][S.r]}` > 0：有路径到这，向右/下推送' if S.f[S.i][S.j][S.r] > 0 else f'`f[{S.i}][{S.j}][{S.r}] = 0`：没有这种余数的路径，不用推'),
        'if i + 1 < m': lambda S, B, r: (f'`i + 1 = {S.i+1} < m`：可以向下' if S.i + 1 < S.m else '已在最后一行，不能向下'),
        'f[i + 1][j]': '向下推：新余数 `({r} + {grid[i+1][j]}) % {k} = {(r + grid[i+1][j]) % k}`，`f[{i+1}][{j}][·] += {f[i][j][r]}`',
        'if j + 1 < n': lambda S, B, r: (f'`j + 1 = {S.j+1} < n`：可以向右' if S.j + 1 < S.n else '已在最后一列，不能向右'),
        'f[i][j + 1]': '向右推：新余数 `({r} + {grid[i][j+1]}) % {k} = {(r + grid[i][j+1]) % k}`，`f[{i}][{j+1}][·] += {f[i][j][r]}`',
        'return f[-1][-1][0]': '终点余数 `0` 的方案数：`f[-1][-1][0]` = =={ret}==',
    },
    cards=dict(
        one_liner='经典路径数 DP 加一维余数，向右、向下「推送」',
        complexity='时间 `O(mnk)`，空间 `O(mnk)`',
        problem=['`m×n` 矩阵，从左上走到右下，每步向右或向下',
                 '统计路径和能被 `k` 整除的路径数，对 `10^9+7` 取余',
                 '示例：`[[5,2,4],[3,0,5],[0,7,2]], k=3` → `2`'],
        quote='令 f[i][j][r] 表示从左上角走到第 i 行第 j 列这个单元格，且当前路径上的数字之和模 k 余 r 时可行的路径数量。',
        quote_src='—— yiduobo 题解',
        idea=['经典版只有 `f[i][j]`；这里把余数 `r` 加进状态',
              '从 `f[i][j][r]` 向右、向下推：新余数 `(r + 目标格值) % k`',
              '只处理 `f > 0` 的状态，推送前先取模避免溢出'],
        summary=['时间/空间 `O(mnk)`',
                 '易错：推送到的新余数要加上==目标格==的值，而不是当前格的值',
                 '数值累加后只在处理该状态时取模，Python 不会溢出',
                 '起点要把 `grid[0][0] % k` 的那一格设为 1，不是 `r = 0`'],
    ),
)
