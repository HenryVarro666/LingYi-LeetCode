import math


def _layout(n):
    if n == 4:
        return [(0.1, 0.5), (0.5, 0.12), (0.5, 0.88), (0.9, 0.5)]
    if n == 5:
        return [(0.08, 0.5), (0.5, 0.12), (0.33, 0.88), (0.67, 0.88), (0.92, 0.5)]
    return [(0.1 + 0.8 * i / max(1, n - 1), 0.5 + (0.3 if i % 2 else -0.3)) for i in range(n)]


def _make_draw(low_key, node_cur, node_nb, node_text):
    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        edges, online = S['edges'], S['online']
        n = len(online)
        low = S.get(low_key)
        lay = _layout(n)
        W, H = x1 - x0 - 160, y1 - y0 - 150
        pos = [(x0 + 80 + a * W, y0 + 70 + b * H) for a, b in lay]
        cv.text((x0 + 18, y0 + 4), '图（箭头旁的数 = 恢复成本；绿 = 当前下界下可用的边，灰 = 成本太小被排除，红 = 离线节点）', 20, T['muted'], bold=True)
        cur, nb = node_cur(S), node_nb(S)
        R = 30
        for u, v, w in edges:
            a, b = pos[u], pos[v]
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy)
            p0 = (a[0] + dx / L * R, a[1] + dy / L * R)
            p1 = (b[0] - dx / L * (R + 4), b[1] - dy / L * (R + 4))
            dead = not (online[u] and online[v])
            ok = (low is not None) and w >= low and not dead
            hot = cur == u and nb == v
            col = T['yellow'] if hot else T['red'] if dead else T['green'] if ok else T['dim']
            cv.arrow(p0, p1, col, 6 if hot else 4 if ok else 2)
            mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
            nx, ny = -dy / L * 18, dx / L * 18
            cv.text((mx + nx, my + ny), w, 22, col if (ok or hot or dead) else T['muted'], anchor='mm', bold=True)
        for i in range(n):
            X, Y = pos[i]
            fill = T['panel2'] if online[i] else (90, 40, 46)
            ring = T['yellow'] if cur == i else (T['red'] if not online[i] else T['border'])
            cv.rect((X - R, Y - R, X + R, Y + R), fill=fill, outline=ring, width=5 if cur == i else 2, r=R)
            cv.text((X, Y), i, 28, T['text'], anchor='mm', bold=True)
            t = node_text(S, i)
            if t:
                cv.text((X, Y + R + 8), t, 20, T['cyan'], anchor='mt', bold=True)
            if i == 0:
                cv.text((X, Y - R - 6), '起点', 18, T['muted'], anchor='mb')
            if i == n - 1:
                cv.text((X, Y - R - 6), '终点', 18, T['muted'], anchor='mb')
    return draw


def _ntext(S, i):
    dis, k = S.get('dis'), S.get('k')
    if dis is None or len(dis) != len(S['online']) or 'mid' not in S:
        return ''
    return f'dis={dis[i]}' if dis[i] <= k else 'dis=∞'


_draw = _make_draw('mid', lambda S: S.get('now') if 'dis' in S else None, lambda S: S.get('nxt') if 'dis' in S else None, _ntext)


CONFIG = dict(
    num=3620, title='恢复网络路径', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='二分答案 + Dijkstra', tags=['灵神题单·二分算法', '难度分 1998'],
    code='''
class Solution(object):
    def findMaxPathScore(self, edges, online, k):
        
        left = -1
        right = k
        n = len(online)
        g = [[] for _ in range(n)]
        for x, y, w in edges:
            g[x].append((y, w))

        while left < right:
            mid = (left + right + 1) // 2
            dis = [k + 1] * n

            heap = [(0, 0)]
            dis[0] = 0
            while heap:
                now, d = heapq.heappop(heap)
                if d > dis[now]:
                    continue
                for nxt, w in g[now]:
                    if online[nxt] and w >= mid and dis[nxt] > dis[now] + w:
                        dis[nxt] = dis[now] + w
                        heapq.heappush(heap, (nxt, dis[nxt]))

            if dis[-1] <= k:
                left = mid
            else:
                right = mid - 1
        
        return left
''',
    call='Solution().findMaxPathScore([[0,1,5],[1,3,10],[0,2,3],[2,3,4]], [True,True,True,True], 10)',
    expect=3, max_steps=110,
    skip=['left = -1', 'n = len(online)', 'g = [[]', 'for x, y, w in edges', 'g[x].append', 'dis = [k + 1]', 'heap = [(0, 0)]', 'while heap', 'if d > dis[now]', 'continue', 'for nxt, w in g[now]', 'heapq.heappush'],
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var='dis', h=200, label='dis[i]：只用 cost ≥ mid 的边时 0 到 i 的最短路（k+1 = 超过 k）', pointers={'now': 'yellow'}),
        dict(type='heap', var='heap', h=140, label='heap：(节点, 距离)', fmt=lambda t: f'{t[0]}:{t[1]}'),
        dict(type='text', h=60, fn=lambda S: (f"二分范围 `[{S['left']}, {S['right']}]`（闭区间）" + (f"，试 `mid = {S['mid']}`：只用 `cost ≥ {S['mid']}` 的边" if 'mid' in S else '')) if 'left' in S and 'right' in S else ''),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('k', 'k', 'orange')],
    captions={
        'right = k': '二分最小边成本：范围 `[-1, {right}]`，`-1` 表示无解，上界取 `k`',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`：继续二分' if S.left < S.right else f'`left = right = {S.left}`：夹到答案'),
        'mid = (': '取偏大中点 `mid = ({left} + {right} + 1) // 2 = {mid}`：只用 `cost ≥ {mid}` 的边跑 Dijkstra',
        'dis[0] = 0': '`dis` 初值 `k+1`（超过 k = 走不到），起点 `dis[0] = 0`',
        'heapq.heappop': '弹出堆顶：节点 `{now}`，记录的距离 `{d}`',
        'if online[nxt]': lambda S, B, r: (f'边 `{B.now} → {B.nxt}`（cost {B.w}）：在线，`{B.w} ≥ {B.mid}`，且 `{B.dis[B.now] + B.w} < dis[{B.nxt}] = {B.dis[B.nxt]}` → ==松弛=='
                                           if (B.online[B.nxt] and B.w >= B.mid and B.dis[B.nxt] > B.dis[B.now] + B.w)
                                           else f'边 `{B.now} → {B.nxt}`（cost {B.w}）：' + ('离线节点' if not B.online[B.nxt] else (f'`cost {B.w} < {B.mid}`，边太便宜，不能用' if B.w < B.mid else f'走过来 `{B.dis[B.now] + B.w}` 不比 `dis[{B.nxt}] = {B.dis[B.nxt]}` 更短'))
                                           + '，跳过'),
        'dis[nxt] = dis[now] + w': '`dis[{nxt}]` 更新为 `{dis[nxt]}`，`({nxt}, {dis[nxt]})` 入堆',
        'if dis[-1] <= k': lambda S, B, r: (f'`dis[终点] = {S.dis[-1]} ≤ k = {S.k}`：最小边成本 ≥ {S.mid} 的有效路径存在' if S.dis[-1] <= S.k
                                            else f'`dis[终点] = {S.dis[-1]}`（> k，或到不了）：下界 {S.mid} 太高，没有有效路径'),
        'left = mid': '可行 → 答案 ≥ {mid}：`left = {left}`',
        'right = mid - 1': '不可行 → 答案 ≤ {mid} − 1：`right = {right}`',
        'return left': '二分夹出的最大可行下界：==返回 {left}==',
    },
    cards=dict(
        one_liner='最小边成本越小越容易有路：二分它，再 Dijkstra 判最短路是否 ≤ k',
        complexity='时间 `O(m log m log k)`，空间 `O(n+m)`',
        problem=['DAG 上走 0 → n-1，中间点在线，总成本 ≤ k；路径分数 = 最小边成本',
                 '求最大分数，没有有效路径返回 -1',
                 '示例：`edges=[[0,1,5],[1,3,10],[0,2,3],[2,3,4]]`，`k=10` → `3`'],
        quote='如果最大的最小边成本越小，那么可用的边就越多，存在有效路径的可能性就越大，因此在这里可以二分这个最大的最小边成本mid，然后检测如果只使用cost大于等于mid的边时是否存在有效路径。',
        quote_src='—— yiduobo 题解原文',
        idea=['先按 `mid` 过滤边：只用 `cost ≥ mid` 且终点在线的边',
              '问题变成：0 到 n-1 的最短路 ≤ k 吗？从 0 跑一趟 Dijkstra',
              '不真的删边，松弛时才判断；`dis` 初值 `k+1`，超过 k 的都视作走不到'],
        summary=['时间 `O(m log m · log k)`，空间 `O(n+m)`',
                 '原文已是 Python 3 可运行写法，未改动',
                 '闭区间二分：`left` 初值 `-1` 表示无解，`mid` 取偏大防死循环',
                 '堆里元组是 `(节点, 距离)`，按节点编号排序；靠 `d > dis[now]` 过滤旧记录，结果仍正确',
                 '对比灵神：灵神利用 DAG 做记忆化 DP，少一个 `log m`；这里不依赖无环'],
    ),
)
