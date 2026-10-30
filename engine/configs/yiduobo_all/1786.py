import math as _m


def _fnum(v):
    if v is None:
        return '?'
    if isinstance(v, float) and _m.isinf(v):
        return '∞'
    return str(v)


def _gdraw(cv, box, T, pos, edges, ncol=None, nlab=None, ecol=None, elab=None, arrows=None, r=28, title=None, pad=70):
    """pos: [(fx,fy)]; edges: [(u,v,w)]; ncol(i)->(r,g,b)|None; nlab(i)->[str..] 画在节点下方;
    ecol(k)->((r,g,b), width)|None; elab(k)->str|None; arrows: set of (u,v) 有向画箭头"""
    x0, y0, x1, y1 = box
    if title:
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    ax0, ay0, ax1, ay1 = x0 + pad, y0 + 84, x1 - pad, y1 - 100
    P = [(ax0 + fx * (ax1 - ax0), ay0 + fy * (ay1 - ay0)) for fx, fy in pos]
    for k, (u, v, w) in enumerate(edges):
        c, wd = (ecol(k) if ecol else None) or (T['border'], 3)
        (xa, ya), (xb, yb) = P[u], P[v]
        L = _m.hypot(xb - xa, yb - ya) or 1
        ux, uy = (xb - xa) / L, (yb - ya) / L
        if arrows and (u, v) in arrows:
            cv.arrow((xa + ux * r, ya + uy * r), (xb - ux * (r + 4), yb - uy * (r + 4)), c, wd, head=16)
        elif arrows and (v, u) in arrows:
            cv.arrow((xb - ux * r, yb - uy * r), (xa + ux * (r + 4), ya + uy * (r + 4)), c, wd, head=16)
        else:
            cv.line([(xa, ya), (xb, yb)], c, wd)
    for k, (u, v, w) in enumerate(edges):
        t = elab(k) if elab else str(w)
        if t is None:
            continue
        c, wd = (ecol(k) if ecol else None) or (T['border'], 3)
        mx, my = (P[u][0] + P[v][0]) / 2, (P[u][1] + P[v][1]) / 2
        tw = cv.tlen(t, 22, bold=True) + 14
        cv.rect((mx - tw / 2, my - 15, mx + tw / 2, my + 15), fill=T['panel'], r=8)
        cv.text((mx, my), t, 22, c if c != T['border'] else T['muted'], anchor='mm', bold=True)
    for i, (X, Y) in enumerate(P):
        c = ncol(i) if ncol else None
        cv.d.ellipse((X - r, Y - r, X + r, Y + r), fill=c or T['panel2'], outline=T['border'] if not c else c, width=3)
        cv.text((X, Y), i if not isinstance(i, str) else i, 28, T['bg'] if c else T['text'], anchor='mm', bold=True, mono=True)
        for j, s in enumerate((nlab(i) if nlab else []) or []):
            if isinstance(s, tuple):
                s, sc = s
            else:
                sc = T['muted']
            cv.text((X, Y + r + 6 + j * 24), s, 20, sc, anchor='mt', bold=True, mono=True)

N = 4
EDGES1 = [[1, 2, 1], [1, 3, 3], [2, 3, 1], [2, 4, 2], [3, 4, 1]]      # 题目输入（节点从 1 开始）
EDGES = [(a - 1, b - 1, w) for a, b, w in EDGES1]                      # 代码里减 1 后的 0-based 边
POS = [(0.0, 0.5), (0.25, 0.0), (0.75, 1.0), (1.0, 0.5)]


def _draw(cv, S, B, box, T):
    dis, ind, f = S.get('dis'), S.get('ind'), S.get('f')
    heap = S.get('heap') or []
    inheap = {p[1] for p in heap}
    ph2 = 'q' in S
    line = S.get('_line', 0)
    now, prev, nxt = S.get('now'), S.get('prev'), S.get('next')
    if ph2:
        hot = {now, nxt} if line >= 33 and nxt is not None else None
    else:
        hot = {now, prev} if now is not None and prev is not None and 20 <= line <= 27 else None
        if now is not None and nxt is not None and 28 <= line <= 30:
            hot = {now, nxt}
    arrows = set()
    if ph2 and dis is not None:
        for u, v, w in EDGES:
            if dis[u] is not None and dis[v] is not None and dis[u] != dis[v]:
                arrows.add((u, v) if dis[u] < dis[v] else (v, u))

    def ncol(i):
        if dis is None:
            return None
        if i == now and now is not None and line >= 20:
            return T['pink']
        if ph2 and nxt is not None and i == nxt and line >= 33:
            return T['blue']
        if (not ph2) and 28 <= line <= 30 and nxt is not None and i == nxt:
            return T['blue']
        if dis[i] is not None:
            return T['green']
        return T['yellow'] if i in inheap else None

    def ecol(k):
        u, v, w = EDGES[k]
        if hot and {u, v} == hot:
            return (T['yellow'], 6)
        if ph2 and (u, v) in arrows or (v, u) in arrows and ph2:
            return (T['blue'], 4)
        return None

    def nlab(i):
        if dis is None:
            return []
        out = [(f'd={_fnum(dis[i])}', T['cyan']), (f'入度={ind[i]}', T['orange'])]
        if ph2:
            out.append((f'f={f[i]}', T['green']))
        return out
    _gdraw(cv, box, T, POS, EDGES, ncol=ncol, nlab=nlab, ecol=ecol, arrows=arrows, r=30,
           title='节点编号已减 1（0 ~ n-1）　蓝箭头 = 拓扑图的边' if ph2 else '节点编号已减 1（0 ~ n-1）　粉 = 刚弹出　黄 = 在堆里　绿 = 已确定')


CONFIG = dict(
    num=1786, title='从第一个节点出发到最后一个节点的受限路径数', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='Dijkstra 建拓扑图 · 拓扑排序 DP',
    tags=['动态规划'],
    code='''
class Solution(object):
    def countRestrictedPaths(self, n, edges):

        g = {}
        for x, y, w in edges:
            x -= 1
            y -= 1
            if x not in g:
                g[x] = {}
            if y not in g:
                g[y] = {}
            g[x][y] = g[y][x] = w

        heap = [[0, n - 1, None]]
        dis = [None] * n
        ind = [0] * n
        f = [0] * n
        mod = 10 ** 9 + 7
        while heap:
            d, now, prev = heapq.heappop(heap)
            if dis[now] is not None:
                if prev is not None and dis[now] > dis[prev]:
                    ind[now] += 1
            else:
                dis[now] = d
                if prev is not None:
                    ind[now] += 1
                for next, w in g.get(now, {}).items():
                    if dis[next] is None or dis[next] >= d + w:
                        heapq.heappush(heap, [d + w, next, now])

        
        q = [n - 1]
        f[n - 1] = 1
        l = 0
        r = 1
        while l < r:
            now = q[l]
            l += 1
            for next in g.get(now, {}):
                if dis[next] > dis[now]:
                    f[next] += f[now]
                    if f[next] >= mod:
                        f[next] -= mod
                    
                    ind[next] -= 1
                    if ind[next] == 0:
                        q.append(next)
                        r += 1
        
        return f[0]
''',
    call=f'Solution().countRestrictedPaths({N}, {EDGES1})',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=410),
        dict(type='heap', var='heap', fmt=lambda p: f'{p[1]}:{p[0]}', label='堆（点:距离）', top_color='purple', h=100),
        dict(type='queue', var='q', label='拓扑队列 q', h=100),
    ],
    watch=[('now', 'now', 'pink'), ('prev', 'prev', 'orange'), ('next', 'next', 'blue'),
           ('f[0]', lambda S: S['f'][0] if 'f' in S else None, 'green')],
    skip=['g = {}', 'for x, y, w in edges', 'x -= 1', 'y -= 1', 'if x not in g', 'g[x] = {}', 'if y not in g', 'g[y] = {}',
          'g[x][y] = g[y][x]', 'dis = [None]', 'ind = [0]', 'f = [0]', 'mod = 10', 'l += 1', 'r = 1', 'l = 0', 'while heap',
          'for next in g.get', 'for next, w in g.get', 'if f[next] >= mod', 'f[next] -= mod', 'r += 1', 'while l < r'],
    captions={
        'heap = [[0, n - 1, None]]': '==从终点 n-1 出发==跑 Dijkstra：堆里放 `[距离, 点, 前驱]`，`ind` 记入度',
        'heapq.heappop': '弹出 `[{d}, {now}, 前驱 {prev}]`',
        'if dis[now] is not None': lambda S, B, r: (f'`dis[{S.now}]` 已有值：第二次到达，看是不是拓扑边' if S.dis[S.now] is not None
                                                    else f'`dis[{S.now}]` 还没值：第一次到达，`{S.d}` 就是最短距离'),
        'if prev is not None and dis[now] > dis[prev]': lambda S, B, r: (f'前驱距离 `{S.dis[S.prev]}` < `{S.dis[S.now]}` → ==从近指向远==，是拓扑边' if S.prev is not None and S.dis[S.now] > S.dis[S.prev]
                                                                         else '不比前驱远：不是拓扑边'),
        'ind[now] += 1': '多一条指向 `{now}` 的拓扑边：`ind[{now}]` = =={ind[now]}==',
        'dis[now] = d': '`dis[{now}] = {d}`',
        'if prev is not None': lambda S, B, r: ('终点没有前驱，入度为 0' if S.prev is None else f'前驱 `{S.prev}` 更近 → 拓扑边'),
        'if dis[next] is None or dis[next] >= d + w': lambda S, B, r: (f'邻居 `{S.next}`：`{S.d} + {S.w} = {S.d + S.w}`，`dis` 为 `{_fnum(S.dis[S.next])}` → 入堆' if S.dis[S.next] is None or S.dis[S.next] >= S.d + S.w
                                                                       else f'邻居 `{S.next}` 已有更短的 `{S.dis[S.next]}`，不入堆'),
        'heapq.heappush': '`[{d + w}, {next}, {now}]` 入堆，前驱记为 `{now}`',
        'q = [n - 1]': '==Dijkstra 结束==。从终点拓扑排序，`f[i]` = 从 i 到终点的受限路径数',
        'f[n - 1] = 1': '终点本身算 1 条路径：`f[n-1] = 1`',
        'now = q[l]': '取队首 `{now}`（入度已为 0）',
        'if dis[next] > dis[now]': lambda S, B, r: (f'邻居 `{S.next}`：`dis` {S.dis[S.next]} > {S.dis[S.now]} → 拓扑边，可走' if S.dis[S.next] > S.dis[S.now]
                                                    else f'邻居 `{S.next}`：`dis` {S.dis[S.next]} ≤ {S.dis[S.now]} → 不能走'),
        'f[next] += f[now]': '`f[{next}]` += `f[{now}]`：`{B.f[next]} + {f[now]}` = =={f[next]}==',
        'ind[next] -= 1': '`ind[{next}]` 减 1 → =={ind[next]}==',
        'if ind[next] == 0': lambda S, B, r: (f'`ind[{S.next}]` 变 0：前驱都算完 → 入队' if S.ind[S.next] == 0
                                              else f'`ind[{S.next}] = {S.ind[S.next]}`：还有前驱，先不入队'),
        'q.append(next)': '`{next}` 入队',
        'return f[0]': '起点的受限路径数 `f[0]` = =={ret}==',
    },
    max_steps=130,
    cards=dict(
        one_liner='先从终点跑 Dijkstra 顺手建拓扑图，再沿拓扑序做 DP',
        complexity='时间 `O((n + m) log m)`，空间 `O(n + m)`',
        problem=['无向带权图，节点 `1 ~ n`。受限路径：每走一步，到终点 `n` 的最短距离==严格变小==',
                 '求从 `1` 到 `n` 的受限路径数，对 `10^9+7` 取模',
                 '本视频：`n=4`，边 `[1,2,1] [1,3,3] [2,3,1] [2,4,2] [3,4,1]` → `3`'],
        quote='拓扑图的建图需要在dijkstra算法中完成……若边两侧的节点满足当前节点与n的距离大于前置节点与n的距离，……那么这条边是拓扑图中的一条边，且边的方向是从前置节点指向当前节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['先以 `n` 为起点跑 Dijkstra，得到每个点到 `n` 的距离 `dis`',
              '距离更小的点指向距离更大的点，这些边构成一张==有向无环图==；入度在 Dijkstra 里就数好',
              '从 `n` 开始拓扑排序，`f[next] += f[now]`：到终点的受限路径数沿 DAG 累加，答案是 `f[0]`'],
        summary=['时间 `O((n + m) log m)`，空间 `O(n + m)`',
                 '==严格==变近：距离相等的边不属于拓扑图，所以判断用 `>` 而不是 `>=`',
                 '入堆条件包含 `>=`：为的是让“一样长的路”也能把入度数对',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '同类：最短路 + 拓扑 DP（灵神题单图论算法、动态规划）'],
    ),
)
