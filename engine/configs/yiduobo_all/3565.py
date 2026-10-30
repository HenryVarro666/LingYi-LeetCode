GRID = [[0, 0, 0], [0, 1, 2]]
_I = lambda S: S['_inner']


def _color(S, i, j, v):
    I = S['_inner']
    if 'vis' not in I and 'vis' not in S:
        return None
    vis = I.get('vis') or S['vis']
    if vis[i][j]:
        return 'green'
    return None


def _try(S, B, r):
    I = S['_inner']
    x, y, nv = I['nxt_x'], I['nxt_y'], I['nxt_v']
    m, n = S['m'], S['n']
    if not (0 <= x < m and 0 <= y < n):
        return f'邻居 `({x},{y})` ==出界== → 换方向'
    if I['vis'][x][y]:
        return f'邻居 `({x},{y})` 已在路径里 → 换方向'
    g = S['grid'][x][y]
    if g == 0:
        return f'邻居 `({x},{y})` 是 `0`（普通格）且没走过 → ==可以走=='
    if g == nv:
        return f'邻居 `({x},{y})` 是 `{g}`，正好是下一个要访问的编号 `{nv}` → ==可以走=='
    return f'邻居 `({x},{y})` 是 `{g}`，但下一个编号是 `{nv}`，==不能跳序== → 换方向'


CONFIG = dict(
    num=3565, title='顺序网格路径覆盖', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='DFS 回溯（哈密尔顿路径 + 编号按序）',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def findPath(self, grid, k):
        
        m = len(grid)
        n = len(grid[0])
        vis = [[False] * n for _ in range(m)]
        path = []

        global found
        found = False
        
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        def dfs(level, now_x, now_y, vis, path, nxt_v):
            global found
            if level == m * n:
                found = True
                return
            
            for d in range(4):
                nxt_x = now_x + dx[d]
                nxt_y = now_y + dy[d]
                if 0 <= nxt_x < m and 0 <= nxt_y < n and not vis[nxt_x][nxt_y] and (grid[nxt_x][nxt_y] == 0 or grid[nxt_x][nxt_y] == nxt_v):
                    vis[nxt_x][nxt_y] = True
                    path.append([nxt_x, nxt_y])
                    if grid[nxt_x][nxt_y] == nxt_v:
                        dfs(level + 1, nxt_x, nxt_y, vis, path, nxt_v + 1)
                    else:
                        dfs(level + 1, nxt_x, nxt_y, vis, path, nxt_v)
                    if found:
                        return
                    path.pop()
                    vis[nxt_x][nxt_y] = False
        
        for i in range(m):
            for j in range(n):
                if grid[i][j] <= 1:
                    vis[i][j] = True
                    path.append([i, j])
                    dfs(1, i, j, vis, path, grid[i][j] + 1)
                    if found:
                        return path
                    path.pop()
                    vis[i][j] = False

        return path
''',
    call=f'Solution().findPath({GRID}, 2)',
    expect=[[0, 0], [1, 0], [1, 1], [1, 2], [0, 2], [0, 1]],
    skip=['m = len', 'n = len', 'dx = [', 'dy = [', 'nxt_x = now_x', 'nxt_y = now_y', 'for d in range(4)',
          'for i in range(m)', 'for j in range(n)', 'global found', 'path.append', 31],
    max_steps=66,
    views=[
        dict(type='grid', var='grid', label='grid（绿 = 已在路径里；蓝框 = 当前格，粉框 = 正在试的邻居）', cell=110, h=300,
             color=_color,
             cursors=[(lambda S: S['_inner'].get('now_x', S.get('i')), lambda S: S['_inner'].get('now_y', S.get('j')), 'blue'),
                      (lambda S: S['_inner'].get('nxt_x') if S['_line'] == 23 else None, lambda S: S['_inner'].get('nxt_y'), 'pink')]),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['path']] if 'path' in S else None,
             label='path（走过的格子 行,列，按顺序）', cell=84, h=140),
        dict(type='calls', h=170, hide=('vis', 'path')),
    ],
    watch=[('level', lambda S: S['_inner'].get('level'), 'blue'), ('nxt_v', lambda S: S['_inner'].get('nxt_v'), 'pink'),
           ('len(path)', lambda S: len(S['path']), 'green')],
    captions={
        'vis = [[False]': '`vis[i][j]` 记录格子是否已在路径里',
        'found = False': '`found` 是全局标志：一旦找到完整路径，所有层都立刻返回',
        'if level == m * n': lambda S, B, r: (f'`level = {S._inner["level"]} == {S.m * S.n}`：==每个格子都走过一次== → `found = True`'
                                              if S._inner['level'] == S.m * S.n
                                              else f'`level = {S._inner["level"]} < {S.m * S.n}`：还没走满，继续找邻居（下一个要访问的编号是 `{S._inner["nxt_v"]}`）'),
        'found = True': '找到了：置 `found = True`，并返回',
        'if 0 <= nxt_x < m': _try,
        'vis[nxt_x][nxt_y] = True': '这个格子加入路径，`vis` 标记为 True',
        'if grid[nxt_x][nxt_y] == nxt_v': lambda S, B, r: (f'`grid = {S.grid[S._inner["nxt_x"]][S._inner["nxt_y"]]}` == 下一个编号 `{S._inner["nxt_v"]}` → 递归时==编号加一=='
                                                           if S.grid[S._inner["nxt_x"]][S._inner["nxt_y"]] == S._inner["nxt_v"]
                                                           else f'`grid = 0` ≠ 编号 `{S._inner["nxt_v"]}` → 编号不变，继续走'),
        'dfs(level + 1, nxt_x, nxt_y, vis, path, nxt_v + 1)': '走到了编号格：==期待的编号加一==，进入下一层',
        'dfs(level + 1, nxt_x, nxt_y, vis, path, nxt_v)': '走的是 0 格：期待的编号不变，进入下一层',
        'if found': lambda S, B, r: ('`found` 为 True（路径已走满 `{}` 格）→ ==不撤销，直接返回=='.format(len(S.path)) if len(S.path) == S.m * S.n
                                     else f'`found` 还是 False（路径只有 `{len(S.path)}` 格）→ 这条路没走通，准备==撤销=='),
        'path.pop()': lambda S, B, r: '撤销：把刚走的格子从 `path` 弹出',
        'vis[nxt_x][nxt_y] = False': '`vis` 还原为 False，换下一个方向',
        'if grid[i][j] <= 1': lambda S, B, r: (f'起点 `({S.i},{S.j})` 的值是 `{S.grid[S.i][S.j]}` ≤ 1 → ==可以当起点=='
                                               if S.grid[S.i][S.j] <= 1 else f'起点 `({S.i},{S.j})` 的值是 `{S.grid[S.i][S.j]}` > 1，不能当起点'),
        'vis[i][j] = True': '枚举起点：==起点不一定是 1==，可以是任意 0 或 1 的格子',
        'dfs(1, i, j, vis, path, grid[i][j] + 1)': '从起点出发 DFS；起点若是 `1`，下一个要访问的编号就是 `2`',
        'return path': '`found` 为 True，返回路径',
    },
    cards=dict(
        one_liner='枚举起点，DFS 走满全部格子，编号格必须按序',
        complexity='时间指数级（`m,n ≤ 6`），空间 `O(mn)`',
        problem=['`m × n` 的网格，`k` 个格子分别含 `1..k`，其余为 `0`',
                 '找一条经过==每个格子恰好一次==、且按 `1..k` 顺序经过编号格的路径',
                 '起点任意，无解返回空数组',
                 '本视频：`[[0,0,0],[0,1,2]]` → 路径从 `(0,0)` 出发'],
        quote='题目要求从找出一条哈密尔顿路径，同时这条路径还需要满足按顺序访问1到k的值。……到了最后还是只好使用dfs来处理。需要注意本题中路径的起点不一定是1所在的单元格。',
        quote_src='—— yiduobo 题解原文',
        idea=['状压 DP 状态太多，插头 DP 又不好处理顺序，直接 DFS',
              '`nxt_v` 表示下一个要访问的编号；邻居是 0 或正好是 `nxt_v` 才能走',
              '走到 `nxt_v` 时编号加一；走满 `m*n` 个格子即找到'],
        summary=['时间指数级，`m,n ≤ 6`，最基本的 DFS 就能过',
                 '起点必须枚举所有 `grid[i][j] <= 1` 的格子，不能只从 1 出发',
                 '`found` 是全局变量，找到后各层直接返回，不撤销',
                 '原文为 Python 2 风格，代码未改（`global found` 在 Python 3 同样可用）'],
    ),
)
