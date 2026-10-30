GRID = [[1, 2, 4], [3, 5, 2]]


def _cur(S):
    return S['_inner'].get('i')


def _cell(S, i, j, v):
    I = S['_inner']
    ci, cj = I.get('i'), I.get('j')
    if ci is None:
        return None
    x, y = I.get('x'), I.get('y')
    if x is not None and S['_line'] in (9, 10) and 0 <= x < len(GRID) and 0 <= y < len(GRID[0]) and (i, j) == (x, y):
        return 'pink' if GRID[x][y] > GRID[ci][cj] else 'dim'
    return None


def _txt(S):
    I = S['_inner']
    if 'res' not in I or 'i' not in I:
        return '`dfs(i, j)` = 以 `(i,j)` 为起点的递增路径数（含只有自己的 1 条）'
    return f"`dfs({I['i']}, {I['j']})`：`res = {I['res']}`（先算上自己这 1 条，再累加每个更大邻居的路径数）"


CONFIG = dict(
    num=2328, title='网格图中递增路径的数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='记忆化搜索（以每格为起点）',
    tags=['二、网格图 DP', '难度分 2001'],
    code='''
class Solution:
    def countPaths(self, grid: List[List[int]]) -> int:
        MOD = 1_000_000_007
        m, n = len(grid), len(grid[0])
        @cache
        def dfs(i: int, j: int) -> int:
            res = 1
            for x, y in (i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1):
                if 0 <= x < m and 0 <= y < n and grid[x][y] > grid[i][j]:
                    res += dfs(x, y)
            return res % MOD
        return sum(dfs(i, j) for i in range(m) for j in range(n)) % MOD
''',
    call=f'Solution().countPaths({GRID})',
    expect=16,
    skip=['for x, y in'],
    views=[
        dict(type='grid', var='grid', label='grid（蓝 = 当前格 (i,j)；粉 = 更大的邻居，会递归；暗 = 不能走）', cell=100, h=250,
             cursors=[(lambda S: S['_inner'].get('i'), lambda S: S['_inner'].get('j'), 'blue')], color=_cell),
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='calls', h=250),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'blue'), ('res', 'res', 'green')],
    captions={
        'MOD = 1_000_000_007': '路径数可能很大，要对 `10^9 + 7` 取余',
        'm, n = len(grid)': '网格 `{m} × {n}`',
        '@cache': '`@cache`：同一个 `(i, j)` 只算一次，==记忆化==',
        'res = 1': '`dfs({i}, {j})`：先记上只含 `({i},{j})` 自己的 ==1 条路径==',
        'if 0 <= x < m': lambda S, B, r: (f'邻居 `({S.x},{S.y})` 越界 → 跳过' if not (0 <= S.x < S.m and 0 <= S.y < S.n)
                                          else (f'`grid[{S.x}][{S.y}] = {S.grid[S.x][S.y]} > grid[{S.i}][{S.j}] = {S.grid[S.i][S.j]}` → ==严格递增，可以走过去=='
                                                if S.grid[S.x][S.y] > S.grid[S.i][S.j]
                                                else f'`grid[{S.x}][{S.y}] = {S.grid[S.x][S.y]} ≤ {S.grid[S.i][S.j]}` → 不是递增，跳过')),
        'res += dfs(x, y)': lambda S, B, r: (f'`res += dfs({S.x}, {S.y})`：要拿到从 `({S.x},{S.y})` 出发的路径数，先递归（若已缓存则直接取）' if S.res == B.res else f'拿到 `dfs({S.x}, {S.y})`（刚算完，或直接命中缓存），`res` 从 {B.res} 变成 =={S.res}=='),
        'return res % MOD': '`dfs({i}, {j}) = {res}`：以 `({i},{j})` 为起点共 =={res}== 条递增路径',
        'return sum(': lambda S, B, r: ('每个格子都当一次起点调用 `dfs`，把所有结果加起来' if r is None else f'每个格子的路径数累加，对 MOD 取余，答案 =={r}=='),
    },
    cards=dict(
        one_liner='以每个格子为起点，路径数 = 1 + 所有更大邻居的路径数之和',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`m x n` 网格，可以向上下左右四个方向走，路径中的数字==严格递增==',
                 '求从任意格子出发、到任意格子结束的路径数，对 `10^9+7` 取余',
                 '示例：`[[1,1],[3,4]]` → `8`；本视频用 `[[1,2,4],[3,5,2]]`'],
        quote='由于路径中的数字严格递增，状态无后效性，可以用动态规划解决。我们把四个方向可以走的格子所对应的状态 f[i\'][j\'] 累加起来，再加上 1，即当前格子组成的长度为 1 的路径，即为 f[i][j]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i][j]` = 以 `(i,j)` 为起点的路径数',
              '只能走向更大的格子，所以不会走回头路，没有环',
              '代码用 `@cache` 记忆化搜索实现，答案是所有格子的 `f` 之和'],
        summary=['时间 `O(mn)`：状态 `O(mn)` 个，每个状态 4 个转移',
                 '易错：`res` 初始为 1（单个格子也算一条路径）',
                 '易错：必须是严格大于，相等的不能走',
                 '递归深度最多 `O(mn)`，网格很大时 Python 要注意递归栈',
                 '同类题：329. 矩阵中的最长递增路径'],
    ),
)
