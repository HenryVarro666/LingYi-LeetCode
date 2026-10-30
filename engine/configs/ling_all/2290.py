G = [[0, 1, 0], [1, 1, 0]]

CONFIG = dict(
    num=2290, title='到达角落需要移除障碍物的最小数目', difficulty='Hard', category='网格图',
    author='灵茶山艾府', technique='0-1 BFS（双端队列）',
    tags=['灵神题单', '网格图', '难度分 2138'],
    code='''
class Solution:
    def minimumObstacles(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dis = [[inf] * n for _ in range(m)]
        dis[0][0] = 0
        q = deque([(0, 0)])
        while q:
            i, j = q.popleft()
            for x, y in (i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j):
                if 0 <= x < m and 0 <= y < n:
                    g = grid[x][y]
                    if dis[i][j] + g < dis[x][y]:
                        dis[x][y] = dis[i][j] + g
                        if g == 0:
                            q.appendleft((x, y))
                        else:
                            q.append((x, y))
        return dis[-1][-1]
''',
    call=f'Solution().minimumObstacles({G})',
    expect=1,
    skip=['m, n = len', 'q = deque', 'for x, y in', 'g = grid'],
    views=[
        dict(type='grid', var='dis', label='dis（到该格最少要移除的障碍数；红 = 障碍物；蓝框 = 出队，粉框 = 邻居）', cell=100, h=300,
             color=lambda S, i, j, v: ('green' if v == 0 else 'orange' if v == 1 else 'yellow') if v != float('inf') else ('red' if G[i][j] else None),
             cursors=[('i', 'j', 'blue'), ('x if _line in (9, 10, 11, 12, 13, 14, 15) else None', 'y', 'pink')]),
        dict(type='queue', var='q', fmt=lambda p: f'({p[0]},{p[1]})', label='q（空格走队首，障碍物走队尾）', h=150),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'blue'), ('x', 'x', 'pink'), ('y', 'y', 'pink'), ('g', 'g', 'orange'), ('终点 dis', 'dis[-1][-1]', 'green')],
    captions={
        'dis = [[inf]': '`dis[i][j]`：到 `(i,j)` 最少要移除几个障碍物，初始 ==∞==',
        'dis[0][0] = 0': '起点本身是空格，不用移除：`dis[0][0] = 0`',
        'while q': lambda S, B, r: (f'队列里还有 `{len(B.q)}` 个格子，继续' if B.q else '队列空了，所有格子的最少移除数都算好了'),
        'i, j = q.popleft()': '取队首 `({i},{j})`：==队首的 dis 最小==，它的值已经定下来了',
        'if 0 <= x < m': lambda S, B, r: (f'`({B.x},{B.y})` 在界内' if 0 <= B.x < B.m and 0 <= B.y < B.n else f'`({B.x},{B.y})` 越界，跳过'),
        'if dis[i][j] + g < dis[x][y]': lambda S, B, r: (f'`g = {S.g}`（1 = 要拆障碍物）：`{S.dis[S.i][S.j]} + {S.g} < {B.dis[S.x][S.y]}` → 成立，路更优' if S.dis[S.i][S.j] + S.g < B.dis[S.x][S.y] else f'`g = {S.g}`：`{S.dis[S.i][S.j]} + {S.g}` 不比 `dis[{S.x}][{S.y}]` = {S.dis[S.x][S.y]} 更小 → 不更新'),
        'dis[x][y] = dis[i][j] + g': '更新 `dis[{x}][{y}] = {dis[x][y]}`',
        'if g == 0': lambda S, B, r: ('走空格不花代价 → 它和当前格同层，该最先处理' if S.g == 0 else '要拆障碍物，代价多 1 → 该放到后面处理'),
        'q.appendleft': '边权 0 → ==加入队首==，下一个就处理它',
        'q.append((x, y))': '边权 1 → 加入队尾',
        'return dis[-1][-1]': '右下角最少移除 `{ret}` 个障碍物',
    },
    max_steps=110,
    cards=dict(
        one_liner='走进障碍物算 1 步代价，走空格算 0：求最短路，0-1 BFS',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['网格里 `0` 是空格，`1` 是可以移除的障碍物，四方向移动',
                 '从左上角走到右下角，最少要移除多少个障碍物',
                 '示例：`[[0,1,1],[1,1,0],[1,1,0]]` → `2`',
                 '本视频：`[[0,1,0],[1,1,0]]` → `1`'],
        quote='从 (i,j) 移动到与其相邻的格子 (i\',j\')，视作一条从 (i,j) 到 (i\',j\') 的有向边，边权为 grid[i\'][j\']。问题变成计算从起点到终点的最短路。',
        quote_src='—— 灵茶山艾府题解',
        idea=['走进格子 `(x,y)` 的代价 = `grid[x][y]`：障碍物 1，空格 0',
              '边权只有 0/1：不用堆，0 边权放队首、1 边权放队尾',
              '`dis[i][j] + g < dis[x][y]` 才更新，所以每个点至多入队两次'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '`dis` 记录的是「最少移除数」，起点终点都是空格，所以起点为 0',
                 '用 `appendleft` 而不是 `append` 处理 0 边权，是 0-1 BFS 正确的关键',
                 '同类题：3286、3552、1368'],
    ),
)
