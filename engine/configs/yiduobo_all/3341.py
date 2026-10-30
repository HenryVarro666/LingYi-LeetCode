import math as _math


def _gdraw(cv, T, box, title, pos, edges, color_of, sub_of=None, ecolor_of=None, R=26):
    """有向图：pos = [(fx, fy)]（0~1 的相对位置），edges = [(a, b)]"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    Wd, Hd = x1 - x0 - 100, y1 - y0 - 110
    P = [(x0 + 50 + fx * Wd, y0 + 60 + fy * Hd) for fx, fy in pos]
    es = set(edges)
    for a, b in edges:
        ec = (ecolor_of(a, b) if ecolor_of else None) or 'dim'
        col = T[ec] if isinstance(ec, str) else ec
        (xa, ya), (xb, yb) = P[a], P[b]
        if a == b:
            cv.arc_arrow((xa - 12, ya - R + 2), (xa + 12, ya - R + 2), 46, col, 3, 11)
            continue
        dx, dy = xb - xa, yb - ya
        L = _math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        off = 9 if (b, a) in es else 0
        nx, ny = -uy * off, ux * off
        cv.arrow((xa + ux * (R + 3) + nx, ya + uy * (R + 3) + ny), (xb - ux * (R + 6) + nx, yb - uy * (R + 6) + ny), col, 3, 12)
    for i, (x, y) in enumerate(P):
        c = color_of(i)
        fill = T[c] if isinstance(c, str) else (c or T['panel2'])
        cv.rect((x - R, y - R, x + R, y + R), fill=fill, outline=T['border'], r=R)
        cv.text((x, y), i, 26, T['bg'] if c else T['muted'], anchor='mm', bold=True)
        if sub_of:
            s = sub_of(i)
            if s:
                cv.text((x, y + R + 6), s, 19, T['text'], anchor='mt', mono=True)
    return P


MT = [[0, 3, 1], [2, 0, 5]]


def _gcol(S, i, j, v):
    if 'dis' in S and S['dis'][i][j] is not None:
        return 'green'
    return None


def _dcol(S, i, j, v):
    if v is not None:
        return 'green'
    return None


def _cap_pop(S, B, r):
    return f'弹出堆里时间最小的：`({S.now_x},{S.now_y})`，时刻 `{S.now_t}`'


def _cap_first(S, B, r):
    if B.dis[S.now_x][S.now_y] is None:
        return f'`dis[{S.now_x}][{S.now_y}]` 还没定 → 第一次弹出该格，时刻 `{S.now_t}` 就是==最短时间==，记入 `dis`'
    return f'`dis[{S.now_x}][{S.now_y}]` 已经定了 → 这是堆里残留的更慢记录，丢掉'


def _cap_in(S, B, r):
    if not (0 <= S.nxt_x < S.n and 0 <= S.nxt_y < S.m):
        return f'邻居 `({S.nxt_x},{S.nxt_y})` 出界，不能走'
    if S.dis[S.nxt_x][S.nxt_y] is not None:
        return f'邻居 `({S.nxt_x},{S.nxt_y})` 最短时间已确定，不用再入堆'
    return f'邻居 `({S.nxt_x},{S.nxt_y})` 在界内且未确定 → 计算到它的时间并入堆'


CONFIG = dict(
    num=3341, title='到达最后一个房间的最少时间 I', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='堆优化 Dijkstra · 网格最短路',
    tags=['灵神题单·图论算法', '难度分 1721'],
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
                    nxt_t = max(now_t, moveTime[nxt_x][nxt_y]) + 1
                    heapq.heappush(q, (nxt_t, nxt_x, nxt_y))

        return dis[n - 1][m - 1]
''',
    call=f'Solution().minTimeToReach({MT})',
    expect=6,
    views=[
        dict(type='grid', var='moveTime', label='moveTime（绿 = 最短时间已定，蓝框 = 当前房间，粉框 = 邻居）', cell=100, h=280,
             color=_gcol, cursors=[('now_x', 'now_y', 'blue'), ('nxt_x if _line in (21, 22, 23, 24) else None', 'nxt_y', 'pink')]),
        dict(type='grid', var='dis', label='dis（到每个房间的最短时间）', cell=80, h=220, color=_dcol),
        dict(type='heap', var='q', label='q（小根堆：时刻, x, y）', fmt=lambda t: f'{t[0]}:({t[1]},{t[2]})', h=150),
    ],
    watch=[('now_t', 'now_t', 'blue'), ('now_x', 'now_x'), ('now_y', 'now_y'), 'nxt_t'],
    skip=['n = len(moveTime)', 'm = len(moveTime[0])', 'dx = [', 'dy = [', 'for d in range(4)', 'nxt_x = now_x', 'nxt_y = now_y', 'continue', 'while q', 'dis[now_x][now_y] = now_t', 'heapq.heappush', 'if now_x == n - 1'],
    max_steps=70,
    captions={
        'dis = [[None]': '`dis[i][j]` 记录到房间 `(i, j)` 的最短时间，`None` = 还没确定',
        'q = [(0, 0, 0)]': '堆里放 `(时刻, x, y)`，起点 `(0,0)` 时刻 0；堆顶永远是时刻最小的',
        'heapq.heappop': _cap_pop,
        'if dis[now_x][now_y] is None': _cap_first,
        'dis[now_x][now_y] = now_t': '`dis[{now_x}][{now_y}] = {now_t}`：Dijkstra 第一次弹出的时刻就是最短时间',
        'if now_x == n - 1': lambda S, B, r: ('到达右下角 `({0},{1})`'.format(S.now_x, S.now_y) if (S.now_x == S.n - 1 and S.now_y == S.m - 1) else f'`({S.now_x},{S.now_y})` 还不是终点，继续扩展邻居'),
        'if 0 <= nxt_x < n': _cap_in,
        'nxt_t = max': '先等房间开启再走 1 秒：`max({now_t}, {moveTime[nxt_x][nxt_y]}) + 1` = =={nxt_t}==，`({nxt_t}, {nxt_x}, {nxt_y})` 入堆',
        'return now_t': '终点最先被弹出的时刻就是答案 =={ret}==',
        'return dis[n - 1][m - 1]': '堆空了也没到终点（本题一定可达，不会走到这里）',
    },
    cards=dict(
        one_liner='网格当稀疏图，堆优化 Dijkstra；更新时间要和房间开启时刻取 max',
        complexity='时间 `O(nm log(nm))`，空间 `O(nm)`',
        problem=['`n × m` 个房间，`moveTime[i][j]` 是房间开启的最早时刻，时刻 0 从 `(0,0)` 出发',
                 '每次移动到相邻房间要 1 秒，到达时房间必须已开启',
                 '求到达 `(n-1, m-1)` 的最少时间',
                 '本视频：`[[0,3,1],[2,0,5]]` → `6`'],
        quote='将这n * m个单元格都视为图中的点，那么每个点最多只会和相邻的四个点连上边，问题就变成了稀疏无向图中的最短路径问题，使用堆优化的dijkstra算法直接跑一遍就行了。另外需要注意的是在更新到达每个单元格的最短路径时，除了常规的距离迭代，还需要将单元格对应的moveTime也考虑进去。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个房间是一个点，相邻房间连边，边权 1：标准堆优化 Dijkstra',
              '特殊点：到邻居的时刻 = `max(当前时刻, 邻居开启时刻) + 1`（可以在门口等）',
              '堆里允许有同一房间的多条记录：`dis` 已确定就丢弃，晚到的是旧记录'],
        summary=['时间 `O(nm log(nm))`，空间 `O(nm)`',
                 '`max(now_t, moveTime[..])`：房间没开就得等，等到开启再走 1 秒',
                 '同一格可能多次入堆，弹出时用 `dis` 判重，只处理第一次',
                 '原文给的是 3342（奇偶步 +1/+2）的代码；本题 3341 每步固定 1 秒，已把 `+ 2 - (nxt_x + nxt_y) % 2` 改为 `+ 1`，其余未改'],
    ),
)
