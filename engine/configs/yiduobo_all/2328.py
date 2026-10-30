GRID = [[1, 2, 4], [3, 5, 2]]


def _I(S):
    return S['_inner']


def _fcell(S, i, j, v):
    I = S['_inner']
    x, y = I.get('x'), I.get('y')
    if x is None:
        return None
    if (i, j) == (I.get('next_x'), I.get('next_y')) and 'next_x' in I and 0 <= I['next_x'] < len(GRID) and 0 <= I['next_y'] < len(GRID[0]):
        return 'pink' if GRID[i][j] > GRID[x][y] else None
    if v > 0:
        return 'green'
    return None


def _txt(S):
    I = S['_inner']
    if 'x' not in I:
        return '`f[i][j]` = 从 `(i,j)` 出发的递增路径数；0 表示还没算过'
    return f"正在算 `f[{I['x']}][{I['y']}]`（当前值 {S['f'][I['x']][I['y']]}）：先累加更大邻居的 `f`，最后 `+1`（原地不动也算一条）"


CONFIG = dict(
    num=2328, title='网格图中递增路径的数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='记忆化搜索（f 数组兼作访问标记）',
    tags=['二、网格图 DP', '难度分 2001'],
    code='''
class Solution(object):
    def countPaths(self, grid):

        mod = 10 ** 9 + 7
        m = len(grid)
        n = len(grid[0])
        
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        def dfs(x, y, f):
            if f[x][y] == 0:
                for index in range(4):
                    next_x = x + dx[index]
                    next_y = y + dy[index]
                    if next_x >= 0 and next_x < m and next_y >= 0 and next_y < n and grid[next_x][next_y] > grid[x][y]:
                        f[x][y] += dfs(next_x, next_y, f)
                        if f[x][y] >= mod:
                            f[x][y] -= mod
                
                f[x][y] += 1
                if f[x][y] >= mod:
                    f[x][y] -= mod
            
            return f[x][y]

        f = [[0] * n for _ in range(m)]
        res = 0
        for i in range(m):
            for j in range(n):
                res += dfs(i, j, f)
                if res >= mod:
                    res -= mod
        
        return res
''',
    call=f'Solution().countPaths({GRID})',
    expect=16,
    max_steps=64,
    skip=['mod = 10', 'm = len', 'n = len', 'dx = [', 'dy = [', 'for index in range(4)', 'next_x = x', 'next_y = y',
          'if f[x][y] >= mod', 'if res >= mod', 'f[x][y] -= mod', 'res -= mod', 'for i in range(m)', 'for j in range(n)'],
    views=[
        dict(type='grid', var='grid', label='grid', cell=84, h=200,
             cursors=[(lambda S: S['_inner'].get('x'), lambda S: S['_inner'].get('y'), 'blue')]),
        dict(type='grid', var='f', label='f（0 = 还没算；绿 = 已算出；蓝框 = 当前格；粉 = 更大的邻居）', cell=84, h=220, color=_fcell,
             cursors=[(lambda S: S['_inner'].get('x'), lambda S: S['_inner'].get('y'), 'blue')]),
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='calls', h=200, hide=('countPaths',)),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'blue'), ('res', 'res', 'green')],
    captions={
        'f = [[0] * n': '`f[i][j]` 全部初始为 0，==0 表示还没算过==',
        'res = 0': '`res` 累计所有起点的路径数',
        'if f[x][y] == 0': lambda S, B, r: (f'`f[{S.x}][{S.y}] = 0`：没算过 → 开始递归求解' if S.f[S.x][S.y] == 0
                                             else f'`f[{S.x}][{S.y}] = {S.f[S.x][S.y]}` ≠ 0：已经算过 → ==直接返回，不再展开=='),
        'if next_x >= 0': lambda S, B, r: (f'邻居 `({S.next_x},{S.next_y})` 越界 → 跳过' if not (0 <= S.next_x < S.m and 0 <= S.next_y < S.n)
                                           else (f'`grid[{S.next_x}][{S.next_y}] = {S.grid[S.next_x][S.next_y]} > grid[{S.x}][{S.y}] = {S.grid[S.x][S.y]}` → ==更大，可以走=='
                                                 if S.grid[S.next_x][S.next_y] > S.grid[S.x][S.y]
                                                 else f'`grid[{S.next_x}][{S.next_y}] = {S.grid[S.next_x][S.next_y]}` 不比 {S.grid[S.x][S.y]} 大 → 跳过')),
        'f[x][y] += dfs(next_x': lambda S, B, r: (f'`f[{S.x}][{S.y}] += dfs({S.next_x}, {S.next_y}, f)`：先去求邻居的路径数' if S.f[S.x][S.y] == B.f[S.x][S.y]
                                                  else f'拿到邻居的值，`f[{S.x}][{S.y}]` 从 {B.f[S.x][S.y]} 变成 =={S.f[S.x][S.y]}=='),
        'f[x][y] += 1': '遍历完四个邻居，再 `+1`：==原地不动也是一条路径== → `f[{x}][{y}] = {f[x][y]}`',
        'return f[x][y]': '`dfs({x}, {y})` 返回 `{f[x][y]}`',
        'res += dfs(i, j, f)': lambda S, B, r: (f'从 `({S.i},{S.j})` 开始求解' if S.res == B.res else f'`res += f[{S.i}][{S.j}]`，累计 res = =={S.res}=='),
        'return res': '所有起点累加完成，答案 `{res}`',
    },
    cards=dict(
        one_liner='f 数组记录每格出发的路径数，没算过才递归',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`m x n` 网格，四个方向移动，路径中的数字==严格递增==',
                 '求任意起点、任意终点的路径数，对 `10^9+7` 取余',
                 '本视频：`[[1,2,4],[3,5,2]]` → `16`'],
        quote='对于记忆化搜索的启动，通常是在最外部遍历所有可能的状态，若当前遍历到状态还没有被求解过，即对应的f还是初始值，那么就递归求解当前状态。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]` 表示从 `(i,j)` 出发的递增路径数',
              '枚举四个邻居，比当前格大的就 `f[i][j] += f[邻居]`',
              '最后加 1：原地不动也是一条合法路径；`f == 0` 当作还没算过'],
        summary=['时间 `O(mn)`：每个格子只算一次，四个方向转移',
                 '用 `f[x][y] == 0` 判断是否算过：每格算完至少为 1，所以不会混淆',
                 '取余用「大于等于 mod 就减 mod」代替 `%`',
                 '原文是 Python 3 兼容写法，代码未改',
                 '对比灵神：灵神用 `@cache`，yiduobo 手动维护 `f` 数组'],
    ),
)
