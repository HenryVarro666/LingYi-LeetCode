def _col(S, i, j, v):
    vis = S.get('vis')
    if vis is None:
        return None
    return 'green' if vis[i][j] else None


def _inn(S, k):
    return S['_inner'].get(k)


def _chk(S, B, ret):
    i, j, x, y, px, py = S.i, S.j, S.x, S.y, S.px, S.py
    m, n = S.m, S.n
    if (i, j) == (px, py):
        return f'`({i},{j})` 就是上一步的格子 → ==不能立刻回头=='
    if not (0 <= i < m and 0 <= j < n):
        return f'`({i},{j})` ==出界=='
    if S.grid[i][j] != S.grid[x][y]:
        return f'`({i},{j})` 是 `{S.grid[i][j]}`，和 `{S.grid[x][y]}` 不同 → 不能走'
    if S.vis[i][j]:
        return f'`({i},{j})` 同值、不是回头、==之前访问过== → 找到环！'
    return f'`({i},{j})` 同值、没访问过 → ==递归 dfs({i},{j})== 继续找'


CONFIG = dict(
    num=1559, title='二维网格图中探测环', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='网格 DFS · 记录上一步位置',
    tags=['灵神题单', '网格图', '难度分 1838'],
    code='''
class Solution:
    def containsCycle(self, grid: List[List[str]]) -> bool:
        m, n = len(grid), len(grid[0])
        vis = [[False] * n for _ in range(m)]

        def dfs(x: int, y: int, px: int, py: int) -> bool:
            vis[x][y] = True
            for i, j in (x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y):  # 枚举移动方向
                if ((i != px or j != py) and  # (i, j) 不是上一步的格子 (px, py)
                    0 <= i < m and 0 <= j < n and  # (i, j) 没有出界
                    grid[i][j] == grid[x][y] and  # (i, j) 和 (x, y) 的格子值相同
                    (vis[i][j] or dfs(i, j, x, y))):  # 如果之前访问过 (i, j)，那么找到了环，否则继续递归找
                    return True
            return False

        for i in range(m):
            for j in range(n):
                if not vis[i][j] and dfs(i, j, -1, -1):
                    return True
        return False
''',
    call="Solution().containsCycle([['b','a','a','c'],['b','a','a','c']])",
    expect=True,
    skip=['m, n = len', 'vis = [[', 10, 11],
    views=[
        dict(type='grid', var='grid', label='grid（绿 = 已访问；蓝框 = dfs 当前格）', cell=96, h=250,
             color=_col, cursors=[(lambda S: _inn(S, 'x'), lambda S: _inn(S, 'y'), 'blue', '')]),
        dict(type='calls', h=230),
        dict(type='text', h=60, fn=lambda S: (f"从 `({S['x']},{S['y']})` 来，上一步 `({S['px']},{S['py']})`" if 'px' in S['_inner'] else '')),
    ],
    watch=[('x', "_inner.get('x')", 'blue'), ('y', "_inner.get('y')", 'blue'), ('px,py', "(_inner.get('px'), _inner.get('py'))", 'pink')],
    captions={
        'vis[x][y] = True': '标记 `({x},{y})` 访问过',
        'for i, j in (x, y - 1)': lambda S, B, r: (f'`({S.x},{S.y})` 的四个方向枚举完了，没找到环' if B.get('i') == S.i and B.get('j') == S.j and 'i' in B
                                                   else f'依次枚举 `({S.x},{S.y})` 的左、右、上、下，现在是 `({S.i},{S.j})`'),
        'if ((i != px': _chk,
        '(vis[i][j] or dfs': lambda S, B, r: (f'`vis[{B.i}][{B.j}]` 为真 → `or` 短路，条件成立' if B.vis[B.i][B.j]
                                              else f'`({B.i},{B.j})` 没访问过 → `dfs({B.i},{B.j},{B.x},{B.y})`，上一步记为 `({B.x},{B.y})`'),
        'return True': '==找到环==，一路返回 True',
        'return False': '从 `({x},{y})` 出发没找到环 → 返回 False，回到上一层',
        'for i in range(m)': '外层枚举每个格子作为 DFS 起点：`i = {i}`',
        'for j in range(n)': '枚举 `j = {j}`',
        'if not vis[i][j] and dfs': lambda S, B, r: (f'`({S.i},{S.j})` 已访问过（属于已搜过的连通块）→ 跳过' if S.vis[S.i][S.j]
                                                     else f'`({S.i},{S.j})` 没访问过 → 以它为起点 `dfs({S.i},{S.j},-1,-1)`，没有上一步用 -1'),
    },
    cards=dict(
        one_liner='DFS 时不许立刻回头；碰到访问过的同值格子，就是环',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['字符网格里，同值格子沿四邻移动，找长度 `>= 4` 的环',
                 '不能回到上一步所在的格子',
                 '示例：`[[b,a,a,c],[b,a,a,c]]` → `true`（中间 2×2 的 a）'],
        quote='所以我们规定，不能立刻回头。在 DFS 的过程中，额外传入上一步的位置 (px,py)，并禁止从当前位置移动到上一步的位置。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(x, y, px, py)` 多带一个上一步位置，禁止走回头路',
              '遇到同值、非回头、且已访问的格子 → 环',
              '网格是二分图（棋盘染色），环长必为偶数，不回头就至少是 4'],
        summary=['时间 `O(mn)`，每格只访问一次',
                 '易错：不能只判断「访问过」，要排除刚走过来的上一步格子',
                 '长度 3 的环在四连通网格里不存在，所以不用单独判长度',
                 '同值判断：只能在值相同的格子间移动'],
    ),
)
