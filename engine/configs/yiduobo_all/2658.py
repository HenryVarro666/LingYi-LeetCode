G0 = [[2, 1, 0, 0], [4, 0, 0, 3], [0, 0, 3, 4]]


def _col(S, i, j, v):
    if 'vis' not in S:
        return None
    if v == 0:
        return None
    return 'green' if S['vis'][i][j] else None


def _nb(S, B, r):
    x, y = S.x, S.y
    m, n = B.m, B.n
    if not (0 <= x < m and 0 <= y < n):
        return f'邻居 `({x},{y})` 越界 → 跳过'
    if B.grid[x][y] == 0:
        return f'邻居 `({x},{y})` 是陆地 → 跳过'
    if B.vis[x][y]:
        return f'邻居 `({x},{y})` 已访问过 → 跳过'
    return f'邻居 `({x},{y})` 是没访问过的水域 → ==入队=='


CONFIG = dict(
    num=2658, title='网格图中鱼的最大数目', difficulty='Medium', category='网格图',
    author='yiduobo', technique='floodfill（BFS 数组队列）',
    tags=['灵神核心路线', '灵神题单·网格图', '难度分 1490'],
    code='''
class Solution(object):
    def findMaxFish(self, grid):

        m = len(grid)
        n = len(grid[0])

        vis = [[False] * n for _ in range(m)]

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        res = 0
        for i in range(m):
            for j in range(n):
                if not vis[i][j] and grid[i][j] > 0:
                    vis[i][j] = True
                    q = [[i, j]]
                    s = grid[i][j]
                    head, tail = 0, 1
                    while head < tail:
                        nowx, nowy = q[head]
                        head += 1
                        for index in range(4):
                            x = nowx + dx[index]
                            y = nowy + dy[index]
                            if x >= 0 and x < m and y >= 0 and y < n and not vis[x][y] and grid[x][y] > 0:
                                vis[x][y] = True
                                q.append([x, y])
                                tail += 1
                                s += grid[x][y]
                    
                    res = max(res, s)
        
        return res
''',
    call=f'Solution().findMaxFish({G0})',
    expect=10,
    skip=['m = len', 'n = len', 'vis = [[', 'dx = [', 'dy = [', 'res = 0', 'head += 1', 'for index in range(4)',
          'x = nowx', 'y = nowy', 'q.append', 'tail += 1', 'for j in range', 'for i in range', 'head, tail = 0, 1'],
    max_steps=80,
    views=[
        dict(type='grid', var='grid', label='grid（绿 = 已访问；黄框 = 起点；蓝框 = 出队；粉框 = 邻居）', cell=84, h=300,
             color=_col, cursors=[('i', 'j', 'yellow'), ('nowx', 'nowy', 'blue'),
                                  ('x if _line == 26 else None', 'y', 'pink')]),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']] if 'q' in S else None,
             label='q（暗 = 已出队，head 指向下一个出队的）', cell=64, pointers={'head': 'blue'},
             dim=lambda S, i, v: i < S.get('head', 0), h=170),
    ],
    watch=[('head', 'head', 'blue'), ('tail', 'tail'), ('s', 's', 'green'), ('res', 'res', 'green')],
    captions={
        'if not vis[i][j]': lambda S, B, r: (
            f'`({S.i},{S.j})` 是没访问过的水域 → 找到新连通块，从这里开始 BFS'
            if (not B.vis[S.i][S.j] and B.grid[S.i][S.j] > 0) else f'`({S.i},{S.j})` 是陆地或已访问过 → 跳过'),
        'vis[i][j] = True': '起点标记已访问',
        'q = [[i, j]]': '起点入队',
        's = grid[i][j]': '这块的鱼数先记起点的 `s = {s}`',
        'while head < tail': lambda S, B, r: (f'`head = {B.head} < tail = {B.tail}`：队列不空，继续扩展' if B.head < B.tail
                                              else f'`head == tail`：这个连通块扩展完了，`s = {S.s}`'),
        'nowx, nowy = q[head]': '出队 `({nowx},{nowy})`，看它的上下左右四个邻居',
        'if x >= 0': _nb,
        'vis[x][y] = True': '入队前就标记，避免被别的格子重复入队',
        's += grid[x][y]': '这格的鱼加进总数：`s = {s}`',
        'res = max': '`res = max({B.res}, {s}) = {res}`：用这个连通块的鱼数更新答案',
        'return res': '所有格子都遍历完，最大连通块的鱼数 =={res}==',
    },
    cards=dict(
        one_liner='遍历格子，遇到新水域就 floodfill 求这一块的鱼数',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`grid[r][c] = 0` 是陆地，`> 0` 是水域，数值是鱼数',
                 '渔夫可从任一水域出发，捕鱼并走到相邻水域',
                 '求最多捞多少鱼；示例 `[[2,1,0,0],[4,0,0,3],[0,0,3,4]]` → `10`'],
        quote='经典的网格图找连通块的问题，常规做法是使用floodfill来处理。',
        quote_src='—— yiduobo 题解原文',
        idea=['从左上角到右下角扫描，遇到没访问过的水域就 BFS',
              'BFS 用数组 `q` + `head`/`tail` 模拟队列',
              '一块 BFS 完，用这块的数值之和更新 `res`'],
        summary=['时间 `O(mn)`：每个格子最多入队一次',
                 '易错：入队时就要标记 `vis`，不能等出队再标',
                 '用单独的 `vis` 数组，不修改输入 `grid`',
                 '原文已是 Python 3 可运行写法，代码未改'],
    ),
)
