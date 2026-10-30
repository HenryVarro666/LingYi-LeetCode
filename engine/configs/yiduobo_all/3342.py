M0 = [[0, 4, 2], [3, 0, 5]]


def _dis(S):
    d = S.get('dis')
    return None if d is None else [['·' if v is None else v for v in row] for row in d]


CONFIG = dict(
    num=3342, title='到达最后一个房间的最少时间 II', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='堆优化 Dijkstra，目的格 (x+y) 奇偶定代价',
    tags=['灵神题单·图论算法', '难度分 1862'],
    code='''
class Solution(object):
    def minTimeToReach(self, moveTime):
        
        n = len(moveTime)
        m = len(moveTime[0])
        dis = [[None] * m for _ in range(n)]

        q = [(0, 0, 0)]
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        while q:
            now_t, now_x, now_y = heapq.heappop(q)
            if dis[now_x][now_y] is None:
                dis[now_x][now_y] = now_t
            else:
                continue

            if now_x == n - 1 and now_y == m - 1:
                return now_t

            for d in range(4):
                nxt_x = now_x + dx[d]
                nxt_y = now_y + dy[d]
                if 0 <= nxt_x < n and 0 <= nxt_y < m and dis[nxt_x][nxt_y] is None:
                    nxt_t = max(now_t, moveTime[nxt_x][nxt_y]) + 2 - (nxt_x + nxt_y) % 2
                    heapq.heappush(q, (nxt_t, nxt_x, nxt_y))

        return dis[n - 1][m - 1]
''',
    call=f'Solution().minTimeToReach({M0})',
    expect=7,
    skip=['n = len(moveTime)', 'm = len(moveTime[0])', 'dis = [[None]', 'q = [(0, 0, 0)]', 'dx = [', 'dy = [', 'for d in range(4)', 'nxt_x = now_x', 'nxt_y = now_y', 'else:'],
    max_steps=90,
    views=[
        dict(type='grid', var='moveTime', label='moveTime（每格 = 最早能开始移动进入的时刻）', cursors=[('now_x', 'now_y', 'yellow'), ('nxt_x', 'nxt_y', 'pink')], h=200, cell=76),
        dict(type='table', var=_dis, label='dis[x][y]：定下的最少时间（· = None，还没定）', cursors=[('nxt_x', 'nxt_y', 'pink')], h=200, cell=76,
             color=lambda S, i, j, v: 'green' if v != '·' else None),
        dict(type='heap', var='q', fmt=lambda t: f'{t[0]}@({t[1]},{t[2]})', label='q 最小堆（时间@房间）', top_color='blue', h=130),
    ],
    watch=[('now_t', 'now_t', 'blue'), ('now_x', 'now_x'), ('now_y', 'now_y'), ('nxt_t', 'nxt_t', 'green')],
    captions={
        'while q': lambda S, B, r: '堆非空，继续' if S.q else '堆空了',
        'now_t, now_x, now_y = heapq.heappop': '弹出时间最小的记录：`t = {now_t}`，房间 `({now_x},{now_y})`',
        'if dis[now_x][now_y] is None': lambda S, B, r: (f'`dis[{S.now_x}][{S.now_y}]` 还是 None：==第一次弹出，这个时间就是最短时间==' if S.dis[S.now_x][S.now_y] is None else f'`dis[{S.now_x}][{S.now_y}] = {S.dis[S.now_x][S.now_y]}` 已有值 → ==重复记录，丢掉=='),
        'dis[now_x][now_y] = now_t': '定下 `dis[{now_x}][{now_y}] = {now_t}`',
        'continue': '这个房间已经定过了，跳过',
        'if now_x == n - 1': lambda S, B, r: (f'`({S.now_x},{S.now_y})` 是终点 → 直接返回' if (S.now_x == S.n - 1 and S.now_y == S.m - 1) else f'`({S.now_x},{S.now_y})` 不是终点，继续扩展'),
        'return now_t': '到达终点，最少时间 `{now_t}`',
        'if 0 <= nxt_x < n': lambda S, B, r: (f'邻居 `({S.nxt_x},{S.nxt_y})` 在网格内且没定过 → 可以考虑' if (0 <= S.nxt_x < S.n and 0 <= S.nxt_y < S.m and S.dis[S.nxt_x][S.nxt_y] is None) else f'邻居 `({S.nxt_x},{S.nxt_y})` 越界或已定好 → 跳过'),
        'nxt_t = max': '到 `({nxt_x},{nxt_y})`：先等到 `moveTime = {moveTime[nxt_x][nxt_y]}`，再走 `2 - (x+y)%2 = {2 - (nxt_x + nxt_y) % 2}` 秒：`max({now_t}, {moveTime[nxt_x][nxt_y]}) + {2 - (nxt_x + nxt_y) % 2}` = =={nxt_t}==',
        'heapq.heappush': '`({nxt_t}, {nxt_x}, {nxt_y})` 入堆',
        'return dis[n - 1]': '堆空返回（实际上不会走到）',
    },
    cards=dict(
        one_liner='稀疏图最短路：目的格的 (x+y) 奇偶就是这一步的代价',
        complexity='时间 `O(nm log nm)`，空间 `O(nm)`',
        problem=['`n × m` 个房间，`moveTime[i][j]` 之后才能开始往该房间移动，`t = 0` 从 `(0,0)` 出发',
                 '相邻移动：奇数次花 1 秒，偶数次花 2 秒，求到 `(n-1, m-1)` 的最少时间',
                 '本视频：`[[0,4,2],[3,0,5]]`'],
        quote='奇数次的移动一定是从行列和为偶数的单元格移动到行列和为奇数的单元格，而偶数次的移动则相反，因此可以通过目的地单元格的行列和来判断当前这次移动的代价。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个房间最多连 4 个邻居，是稀疏无向图 → 堆优化 Dijkstra',
              '更新时除了常规的距离，还要把 `moveTime` 也考虑进去：`max(now_t, moveTime)`',
              '代价看目的格：`(x+y)` 为奇 → 1 秒，为偶 → 2 秒，即 `2 - (x+y) % 2`'],
        summary=['时间 `O(nm log nm)`，空间 `O(nm)`',
                 '`dis` 初值是 `None`：第一次弹出才写入，之后的重复记录用 `else: continue` 丢弃',
                 '入堆前就检查 `dis[nxt] is None`，省掉一些无用记录',
                 '对比灵神：灵神按出发格 `(i+j)%2+1` 取步长，本文按目的格 `2-(x+y)%2`，两者等价'],
    ),
)
