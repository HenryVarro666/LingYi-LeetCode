GRID = [[1, 1, 1, 1, 1],
        [0, 0, 1, 0, 1],
        [1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1]]


def _color(S, i, j, v):
    if v == 0:
        return 'yellow'
    if GRID[i][j] == 0:
        return 'green' if (i, j) in ((1, 3), (2, 3)) and 'ans' in S else 'cyan'
    return None


def _nb(S, B, ret):
    i, j = B.i, B.j
    m, n = B.m, B.n
    if not (0 <= i < m and 0 <= j < n):
        return f'邻居 `({i},{j})` 出界'
    v = B.grid[i][j]
    if v == 0:
        return f'邻居 `({i},{j})` 是没访问过的 `0` → ==继续 DFS=='
    if GRID[i][j] == 0:
        return f'邻居 `({i},{j})` 已经被改成 `1`（访问过）→ 跳过'
    return f'邻居 `({i},{j})` 是水 `1` → 跳过'


def _edge_if(S, B, ret):
    i, j = S.i, S.j
    if S.grid[i][j] == 0:
        return f'边界格子 `({i},{j})` 是 `0` → 它所在的岛==碰到边界，一定不封闭==，DFS 把整座岛标记掉'
    return f'边界格子 `({i},{j})` 是 `1`，跳过'


def _in_if(S, B, ret):
    i, j = S.i, S.j
    if S.grid[i][j] == 0:
        return f'内部格子 `({i},{j})` 还是 `0` → 边界岛已经全被标记，它==一定在封闭岛上=='
    return f'`({i},{j})` 是 `1`（水或已访问），跳过'


CONFIG = dict(
    num=1254, title='统计封闭岛屿的数目', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='网格图 DFS · 先外后内',
    tags=['labuladong', '灵神核心路线', '难度分 1659'],
    code='''
class Solution:
    def closedIsland(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        if m < 3 or n < 3: return 0

        def dfs(x: int, y: int) -> None:
            grid[x][y] = 1  # 标记 (x,y) 被访问，避免重复访问
            # 访问四方向的 0
            for i, j in (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1):
                if 0 <= i < m and 0 <= j < n and grid[i][j] == 0:
                    dfs(i, j)

        for i in range(m):
            # 如果是第一行和最后一行，访问所有格子
            # 如果不是，只访问第一列和最后一列的格子
            step = 1 if i == 0 or i == m - 1 else n - 1
            for j in range(0, n, step):
                if grid[i][j] == 0:  # 从没有访问过的 0 出发
                    dfs(i, j)

        ans = 0
        for i in range(1, m - 1):
            for j in range(1, n - 1):
                if grid[i][j] == 0:  # 从没有访问过的 0 出发
                    ans += 1  # 一定是封闭岛屿
                    dfs(i, j)
        return ans
''',
    call=f'Solution().closedIsland({GRID})',
    expect=1,
    views=[
        dict(type='text', fn=lambda S: '黄 = 还没访问的 `0`（陆地）　青 = 边界岛（已标记）　绿 = 封闭岛（已标记）　深色 = 水 `1`', size=22, h=56),
        dict(type='grid', var='grid', cell=96, h=420, color=_color,
             cursors=[(lambda S: S['_inner'].get('x'), lambda S: S['_inner'].get('y'), 'blue', '(x,y)'),
                      (lambda S: S['_inner'].get('i') if 'x' not in S['_inner'] else None,
                       lambda S: S['_inner'].get('j'), 'pink')]),
        dict(type='calls', h=200),
    ],
    watch=[('i', lambda S: S['_inner'].get('i'), 'pink'), ('j', lambda S: S['_inner'].get('j'), 'pink'),
           ('step', 'step'), ('ans', 'ans', 'green')],
    skip=['for i, j in (x - 1', 'for j in range(0, n, step)', 'for j in range(1, n - 1)'],
    captions={
        'm, n = len': '网格 `{m}` 行 `{n}` 列：`0` 是陆地，`1` 是水',
        'if m < 3 or n < 3': '行列都 ≥ 3，可能有封闭岛（否则每个格子都在边界上）',
        'grid[x][y] = 1': '标记 `({x},{y})`：直接把 `0` 改成 `1`，==避免重复访问==',
        'if 0 <= i < m and': _nb,
        11: lambda S, B, ret: f'从 `({B.x},{B.y})` 递归到邻居 `({B.i},{B.j})`',
        19: lambda S, B, ret: f'从边界的 `({B.i},{B.j})` 出发，DFS 标记整座==非封闭岛==',
        26: lambda S, B, ret: f'从 `({B.i},{B.j})` 出发 DFS，标记这座封闭岛',
        'for i in range(m)': lambda S, B, ret: (f'第一阶段：扫描第 `{S.i}` 行的边界格子' if S.i != B.get('i') or 'step' not in B
                                                 else '边界扫描完毕'),
        'step = 1 if': lambda S, B, ret: ('第一行 / 最后一行：`step = 1`，每个格子都是边界' if S.step == 1
                                          else f'中间行：`step = n - 1 = {S.step}`，只看第一列和最后一列'),
        18: _edge_if,
        24: _in_if,
        'ans = 0': '第二阶段：边界岛都被标记了，剩下的 `0` ==一定在封闭岛上==',
        'for i in range(1, m - 1)': lambda S, B, ret: (f'扫描内部第 `{S.i}` 行' if S.i != B.get('i') else '内部扫描完毕'),
        'ans += 1': '封闭岛 +1：`ans` = =={ans}==，再 DFS 把这座岛标记掉',
        'return ans': '共 =={ret}== 座封闭岛',
    },
    max_steps=75,
    cards=dict(
        one_liner='先从边界出发标记非封闭岛，剩下的 0 都在封闭岛上',
        complexity='时间 `O(mn)`，空间 `O(mn)`（递归栈）',
        problem=['`0` 是陆地，`1` 是水；四方向相连的 `0` 组成岛',
                 '封闭岛：上下左右==完全被 1 包围==，求封闭岛的个数',
                 '本视频：4×5 网格，左边那座岛碰到边界，右边那座封闭 → `1`'],
        quote='既然关键是「边界」，那么不妨==从边界出发，先标记所有非封闭岛屿==。标记完后，网格图内部的 0 就一定在封闭岛屿上。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从一个 `0` 出发能走到边界 → 它的岛不封闭',
              '第一阶段：从四条边上的 `0` DFS，把它们的岛全改成 `1`',
              '第二阶段：内部每遇到一个新的 `0`，`ans += 1`，再 DFS 标记整座岛'],
        summary=['时间 `O(mn)`；蛇形岛递归最深 `O(mn)`',
                 '`step = n - 1` 的写法让中间行只访问第一列和最后一列',
                 '行数或列数不足 3 时没有封闭岛，直接返回 0',
                 '题解的算法二：只从内部 DFS，碰到边界就把 `closed` 置为 False，==不能中途退出 DFS==',
                 '同类题：1020. 飞地的数量、130. 被围绕的区域'],
    ),
)
