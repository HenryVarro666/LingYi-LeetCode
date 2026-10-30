DIRS = (
    (),
    ((0, -1), (0, 1)), ((-1, 0), (1, 0)), ((0, -1), (1, 0)),
    ((0, 1), (1, 0)), ((0, -1), (-1, 0)), ((0, 1), (-1, 0)),
)  # 与题解里的 DIRS 相同，仅供字幕/视图使用


def _vis(S, i, j, v):
    vis = S.get('vis')
    if vis is None:
        return None
    if 'x' in S['_inner'] and (i, j) == (S['_inner']['x'], S['_inner']['y']):
        return 'yellow'
    return 'green' if vis[i][j] else None


def _chk(S, B, ret):
    i, j, dx, dy = S.i, S.j, S.dx, S.dy
    m, n = S.m, S.n
    if not (0 <= i < m and 0 <= j < n):
        return f'邻居 `({i},{j})` ==出界== → 这个方向走不了'
    if S.vis[i][j]:
        return f'邻居 `({i},{j})` ==已访问过== → 不再走'
    back = (-dx, -dy) in DIRS[S.grid[i][j]]
    if not back:
        return f'邻居 `({i},{j})` 是街道 {S.grid[i][j]}，没有反方向 `({-dx},{-dy})` → ==不连通=='
    return f'邻居 `({i},{j})` 是街道 {S.grid[i][j]}，含反方向 `({-dx},{-dy})` → 连通，==递归 dfs({i},{j})=='


CONFIG = dict(
    num=1391, title='检查网格中是否存在有效路径', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='网格 DFS · 反方向互通',
    tags=['灵神题单', '网格图', '难度分 1746'],
    code='''
DIRS = (
    (),
    ((0, -1), (0, 1)),  # 站在街道 1，可以往左或者往右
    ((-1, 0), (1, 0)),  # 站在街道 2，可以往上或者往下
    ((0, -1), (1, 0)),  # 站在街道 3，可以往左或者往下
    ((0, 1), (1, 0)),   # 站在街道 4，可以往右或者往下
    ((0, -1), (-1, 0)), # 站在街道 5，可以往左或者往上
    ((0, 1), (-1, 0)),  # 站在街道 6，可以往右或者往上
)

class Solution:
    def hasValidPath(self, grid: list[list[int]]) -> bool:
        m, n = len(grid), len(grid[0])
        vis = [[False] * n for _ in range(m)]

        def dfs(x: int, y: int) -> bool:
            if x == m - 1 and y == n - 1:
                return True
            vis[x][y] = True  # 标记 (x, y) 访问过，从而避免重复访问
            for dx, dy in DIRS[grid[x][y]]:  # 枚举下一步往哪走
                i, j = x + dx, y + dy
                if 0 <= i < m and 0 <= j < n and not vis[i][j] and \\
                   (-dx, -dy) in DIRS[grid[i][j]] and dfs(i, j):
                    return True
            return False

        return dfs(0, 0)
''',
    call='Solution().hasValidPath([[2,4,3],[6,5,2]])',
    expect=True,
    skip=['m, n = len', 'vis = [['],
    views=[
        dict(type='grid', var='grid', label='grid（街道编号；绿 = 已访问，黄 = 当前所在格）', cell=96, h=330,
             color=_vis, cursors=[(lambda S: S['_inner'].get('x'), lambda S: S['_inner'].get('y'), 'blue', '(x,y)')]),
        dict(type='calls', h=200),
        dict(type='text', h=70, fn=lambda S: (f"街道 `{S['grid'][S['_inner']['x']][S['_inner']['y']]}` 可走方向：`{DIRS[S['grid'][S['_inner']['x']][S['_inner']['y']]]}`" if 'x' in S['_inner'] else '')),
    ],
    watch=[('x', "_inner.get('x')", 'blue'), ('y', "_inner.get('y')", 'blue'), ('dx,dy', "(_inner.get('dx'), _inner.get('dy'))", 'pink')],
    captions={
        'if x == m - 1 and y == n - 1': lambda S, B, r: (f'`({S.x},{S.y})` 就是右下角终点 → ==找到有效路径=='
                                                         if (S.x, S.y) == (S.m - 1, S.n - 1) else
                                                         f'`({S.x},{S.y})` 还不是终点 `({S.m-1},{S.n-1})` → 继续走'),
        'vis[x][y] = True': '标记 `({x},{y})` 访问过：格子之间互通，不标记会来回走成死循环',
        'for dx, dy in DIRS': '站在街道 `{grid[x][y]}`，只能沿它自带的方向 `{DIRS[grid[x][y]]}` 走',
        'i, j = x + dx': '往 `({dx},{dy})` 走一步：邻居是 `({i},{j})`',
        'if 0 <= i < m': _chk,
        'return True': '一路返回 True：路径存在',
        'return False': '这个格子往哪都走不通 → ==返回 False，回到上一层试别的方向==',
    },
    cards=dict(
        one_liner='站在格子上只能沿街道方向走，且邻居必须能反向走回来',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['网格每格是一条街道（1~6），连接上下左右中的两个方向',
                 '从 `(0,0)` 出发，只能沿街道走，能否到 `(m-1,n-1)`',
                 '示例：`[[2,4,3],[6,5,2]]` → `true`'],
        quote='如果从当前位置往 (dx,dy) 方向移动到相邻街道，那么相邻街道必须包含相反的方向向量 (-dx,-dy)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先用 `DIRS` 记下每种街道能往哪走（问题一）',
              '往 `(dx,dy)` 走，邻居必须含 `(-dx,-dy)` 才算连通（问题二）',
              '连通性确定后就是普通的网格 DFS，`vis` 防重复'],
        summary=['时间 `O(mn)`，每格最多访问一次；递归深度最多 `mn`',
                 '易错：只看自己的方向不够，==邻居也要能走回来==',
                 '起点就是终点时，进 dfs 直接返回 True',
                 '同类：网格图 DFS 题单里的岛屿问题'],
    ),
)
