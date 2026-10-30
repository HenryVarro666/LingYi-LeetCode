G = [[0, 1, 0], [0, 0, 1]]

CONFIG = dict(
    num=3286, title='穿越网格图的安全路径', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='0-1 BFS（双端队列）',
    tags=['灵神题单', '网格图'],
    code='''
class Solution:
    def findSafeWalk(self, grid: List[List[int]], health: int) -> bool:
        m, n = len(grid), len(grid[0])
        dis = [[inf] * n for _ in range(m)]
        dis[0][0] = grid[0][0]
        q = deque([(0, 0)])
        while q:
            i, j = q.popleft()
            for x, y in (i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j):
                if 0 <= x < m and 0 <= y < n:
                    cost = grid[x][y]
                    if dis[i][j] + cost < dis[x][y]:
                        dis[x][y] = dis[i][j] + cost
                        if cost == 0:
                            q.appendleft((x, y))
                        else:
                            q.append((x, y))
        return dis[-1][-1] < health
''',
    call=f'Solution().findSafeWalk({G}, 2)',
    expect=True,
    skip=['m, n = len', 'q = deque', 'for x, y in', 'cost = grid'],
    views=[
        dict(type='grid', var='dis', label='dis（到该格的最少扣血；红底 = 不安全格；蓝框 = 出队，粉框 = 邻居）', cell=100, h=330,
             color=lambda S, i, j, v: ('green' if v == 0 else 'orange' if v == 1 else 'yellow' if v == 2 else None) if v != float('inf') else (('red' if G[i][j] else None)),
             cursors=[('i', 'j', 'blue'), ('x if _line in (9, 10, 11, 12, 13, 14) else None', 'y', 'pink')]),
        dict(type='queue', var='q', fmt=lambda p: f'({p[0]},{p[1]})', label='q（队首最小：0 边权放队首，1 边权放队尾）', h=150),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'blue'), ('x', 'x', 'pink'), ('y', 'y', 'pink'), ('cost', 'cost', 'orange'), ('health', 'health', 'green')],
    captions={
        'dis = [[inf]': '`dis[i][j]`：到 `(i,j)` 的最少扣血，初始都是 ==∞==',
        'dis[0][0] = grid[0][0]': '起点自己也可能是不安全格：`dis[0][0] = {dis[0][0]}`',
        'while q': lambda S, B, r: (f'队列里还有 `{len(B.q)}` 个格子，继续' if B.q else '队列空了，最短路算完'),
        'i, j = q.popleft()': '从队首取出 `({i},{j})`，==队首永远是当前扣血最少的==',
        'for x, y in': '枚举四个方向的邻居（边权 = 邻居格子的值）',
        'if 0 <= x < m': lambda S, B, r: (f'`({B.x},{B.y})` 在界内' if 0 <= B.x < B.m and 0 <= B.y < B.n else f'`({B.x},{B.y})` 越界，跳过'),
        'cost = grid[x][y]': '走进 `({x},{y})` 的代价 `cost = {cost}`（1 = 不安全格，扣 1 点血）',
        'if dis[i][j] + cost < dis[x][y]': lambda S, B, r: (f'走进格子 cost = {S.cost}：`{S.dis[S.i][S.j]} + {S.cost} < {B.dis[S.x][S.y]}` → 成立，找到更省血的路' if r is None and S.dis[S.i][S.j] + S.cost < B.dis[S.x][S.y] else f'走进格子 cost = {S.cost}：`{S.dis[S.i][S.j]} + {S.cost}` 不比 `dis[{S.x}][{S.y}]` 的 {S.dis[S.x][S.y]} 更小 → 不更新'),
        'dis[x][y] = dis[i][j] + cost': '松弛：`dis[{x}][{y}] = {dis[x][y]}`',
        'if cost == 0': lambda S, B, r: ('边权 0：扣血没变，应排在队首' if S.cost == 0 else '边权 1：扣血多 1，应排在队尾'),
        'q.appendleft': '边权 0 → ==加入队首==，保证队首最小，不需要最小堆',
        'q.append((x, y))': '边权 1 → 加入队尾',
        'return dis[-1][-1] < health': '终点最少扣血 `{dis[-1][-1]}`，健康值 `{health}`：==扣血 < health== 才能保持正数 → `{ret}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='扣血越少越好，本质是最短路；边权只有 0/1，用双端队列代替堆',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`grid[i][j] = 1` 是不安全格，走进去扣 1 点血，血量必须始终为正',
                 '从左上角走到右下角，问能否到达',
                 '示例：`[[0,1,0,0,0],[0,1,0,1,0],[0,0,0,1,0]]`，`health = 1` → `true`',
                 '本视频：`[[0,1,0],[0,0,1]]`，`health = 2` → `true`（终点是不安全格，最少扣 1）'],
        quote='0-1 BFS 本质是对 Dijkstra 算法的优化。因为边权只有 0 和 1，我们可以把最小堆换成双端队列，遇到 0 边权就加入队首，遇到 1 边权就加入队尾，这样可以保证队首总是最小的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从 `(i,j)` 走到邻居 `(x,y)` 是一条有向边，边权 = `grid[x][y]`',
              '最少扣血 = 起点到终点的最短路，只要 ==最短路 < health==',
              '0 边权入队首、1 边权入队尾，队列始终从小到大'],
        summary=['时间 `O(mn)`：每个格子至多入队两次',
                 '起点也要算：`dis[0][0] = grid[0][0]`',
                 '判断是 `dis < health`，不是 `<=`：到终点血量也要为正',
                 '写法二：出队时发现血扣完或已到终点就提前返回',
                 '同类题：2290、1368、3552（0-1 BFS）'],
    ),
)
