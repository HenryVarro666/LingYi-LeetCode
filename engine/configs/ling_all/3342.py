M0 = [[0, 4, 2], [3, 0, 5]]

CONFIG = dict(
    num=3342, title='到达最后一个房间的最少时间 II', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='网格 Dijkstra + 按 (i+j) 奇偶定步长',
    tags=['灵神题单·图论算法', '难度分 1862'],
    code='''
class Solution:
    def minTimeToReach(self, moveTime: List[List[int]]) -> int:
        n, m = len(moveTime), len(moveTime[0])
        dis = [[inf] * m for _ in range(n)]
        dis[0][0] = 0
        h = [(0, 0, 0)]
        while True:
            d, i, j = heappop(h)
            if i == n - 1 and j == m - 1:
                return d
            if d > dis[i][j]:
                continue
            time = (i + j) % 2 + 1
            for x, y in (i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1):  # 枚举周围四个格子
                if 0 <= x < n and 0 <= y < m:
                    new_dis = max(d, moveTime[x][y]) + time
                    if new_dis < dis[x][y]:
                        dis[x][y] = new_dis
                        heappush(h, (new_dis, x, y))
''',
    call=f'Solution().minTimeToReach({M0})',
    expect=7,
    skip=['n, m = len', 'dis = [[inf]', 'dis[0][0] = 0', 'for x, y in', 'while True', 'if 0 <= x < n'],
    max_steps=90,
    views=[
        dict(type='grid', var='moveTime', label='moveTime（每格 = 最早能开始移动进入的时刻）', cursors=[('i', 'j', 'yellow'), ('x', 'y', 'pink')], h=200, cell=76),
        dict(type='table', var='dis', label='dis[i][j]：到达该房间的最少时间（inf = 还没到过）', cursors=[('x', 'y', 'pink')], h=200, cell=76,
             color=lambda S, i, j, v: 'green' if v != float('inf') else None),
        dict(type='heap', var='h', fmt=lambda t: f'{t[0]}@({t[1]},{t[2]})', label='h 最小堆（时间@房间）', top_color='blue', h=130),
    ],
    watch=[('d', 'd', 'blue'), ('i', 'i'), ('j', 'j'), ('time', 'time', 'orange'), ('new_dis', 'new_dis', 'green')],
    captions={
        'h = [(0, 0, 0)]': '堆里放 `(时间, 行, 列)`：`t = 0` 从 `(0,0)` 出发',
        'd, i, j = heappop': '取出时间最小的房间：`d = {d}`，`({i},{j})`',
        'if i == n - 1 and j == m - 1': lambda S, B, r: (f'`({S.i},{S.j})` 是终点：==堆顶最小，d 就是最少时间==' if (S.i == S.n - 1 and S.j == S.m - 1) else f'`({S.i},{S.j})` 还不是终点'),
        'return d': '到达右下角，最少时间 `{d}`',
        'if d > dis[i][j]': lambda S, B, r: (f'`{S.d} > dis[{S.i}][{S.j}] = {S.dis[S.i][S.j]}`：==旧记录==，跳过' if S.d > S.dis[S.i][S.j] else f'`{S.d} == dis[{S.i}][{S.j}]`：最新记录，继续'),
        'continue': '这个房间早有更小的时间，邻居已更新过 → 跳过',
        'time = (i + j) % 2 + 1': '`(i+j) % 2 + 1` = `{time}`：从 `(i+j)` 为 ==偶数== 的格子出发花 1 秒，==奇数== 的花 2 秒（相邻格子奇偶交替）',
        'if 0 <= x < n': lambda S, B, r: f'邻居 `({S.x},{S.y})` ' + ('在网格内' if (0 <= S.x < S.n and 0 <= S.y < S.m) else '越界，跳过'),
        'new_dis = max': '到 `({x},{y})`：先等到 `moveTime = {moveTime[x][y]}` 才能出发，所以 `max({d}, {moveTime[x][y]}) + {time}` = =={new_dis}==',
        'if new_dis < dis[x][y]': lambda S, B, r: (f'`{S.new_dis} < dis[{S.x}][{S.y}] = {S.dis[S.x][S.y]}` → 更早，更新' if S.new_dis < S.dis[S.x][S.y] else f'`{S.new_dis} >= dis[{S.x}][{S.y}] = {S.dis[S.x][S.y]}` → 不更早，不更新'),
        'dis[x][y] = new_dis': '更新：`dis[{x}][{y}] = {new_dis}`',
        'heappush': '`({new_dis}, {x}, {y})` 入堆',
    },
    cards=dict(
        one_liner='网格最短路：等房间开放再走，步长由 (i+j) 的奇偶决定',
        complexity='时间 `O(nm log nm)`，空间 `O(nm)`',
        problem=['`moveTime[i][j]` 是这个时刻==以后==才能开始往该房间移动；从 `(0,0)` 在 `t=0` 出发',
                 '每次走相邻房间，第 1、3、5… 次花 1 秒，第 2、4、6… 次花 2 秒',
                 '求到达右下角的最少时间；本视频：`[[0,4,2],[3,0,5]]`'],
        quote='本题由于每走一步 time 都会在 1,2 之间变化，类似国际象棋棋盘，(i+j) 的奇偶性就决定了 time，即 time = (i+j) mod 2 + 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['到 `(x,y)` 的时间 = `max(dis[i][j], moveTime[x][y]) + time`',
              '步长只看出发格子：`(i+j) % 2 + 1`，不用记步数',
              '剩下就是网格上的堆优化 Dijkstra，出堆是终点就返回'],
        summary=['时间 `O(nm log nm)`，空间 `O(nm)`',
                 '易错：先取 `max(d, moveTime)` 再加 `time`，不是反过来',
                 '`d > dis[i][j]` 的 `continue` 对 4 邻居图可有可无，但一般图必须写',
                 '上一题 3341 步长恒为 1，只把 `time` 改成常数即可'],
    ),
)
