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
EDGES = [[2, 0, 1], [0, 1, 1], [0, 3, 4], [3, 2, 2]]
POS = [(0.0, 0.4), (0.25, 1.0), (0.5, 0.0), (1.0, 0.4)]
EXPECT = [True, False, False, True]


def _arrs(S):
    """(d0, dn, 正在运行的那一个)"""
    dis = S.get('dis') if 'start' in S else None
    d0, dn = S.get('dis_start'), S.get('dis_end')
    if dis is not None and S.get('start') == 0:
        d0 = dis
    if dis is not None and S.get('start') == N - 1:
        dn = dis
    return d0, dn, dis


def _draw(cv, S, B, box, T):
    d0, dn, run = _arrs(S)
    line = S.get('_line', 0)
    res = S.get('res')
    heap = S.get('heap') or []
    inheap = {p[1] for p in heap}
    in_dij = 'start' in S and run is not None
    in_chk = 'index' in S and 'x' in S and 'y' in S and 'start' not in S and 25 <= line <= 29
    x, y = S.get('x'), S.get('y')
    yy = S.get('y') if in_dij and 'w' in S and line in (16, 17) else None
    idx = S.get('index')

    def ncol(i):
        if in_chk:
            return T['pink'] if i == x else T['blue'] if i == y else None
        if in_dij:
            if i == x and 12 <= line <= 17:
                return T['pink']
            if yy is not None and i == yy:
                return T['blue']
            if run[i] != -1:
                return T['green']
            return T['yellow'] if i in inheap else None
        return None

    def ecol(k):
        u, v, w = EDGES[k]
        if in_chk and idx == k:
            return (T['yellow'], 7)
        if res and k < len(res) and res[k]:
            return (T['green'], 7)
        if in_dij and yy is not None and {u, v} == {x, yy}:
            return (T['yellow'], 6)
        return None

    def nlab(i):
        out = []
        if d0 is not None:
            out.append((f'0→: {"?" if d0[i] == -1 else d0[i]}', T['cyan']))
        if dn is not None:
            out.append((f'→{N - 1}: {"?" if dn[i] == -1 else dn[i]}', T['orange']))
        return out
    _gdraw(cv, box, T, POS, [tuple(e) for e in EDGES], ncol=ncol, nlab=nlab, ecol=ecol, r=30,
           title='青 = 离 0 的距离　橙 = 离 n-1 的距离　绿边 = 在最短路上')


def _check(S):
    if 'index' not in S or 'start' in S or 'x' not in S or 'y' not in S or not (26 <= S.get('_line', 0) <= 29):
        return ''
    ds, de, x, y, w = S['dis_start'], S['dis_end'], S['x'], S['y'], S['w']
    t = ds[-1]
    a = f'{ds[x]} + {w} + {de[y]} = {ds[x] + w + de[y]}'
    b = f'{ds[y]} + {w} + {de[x]} = {ds[y] + w + de[x]}'
    return f'总长 `{t}`：正走 `{a}`；反走 `{b}`'


CONFIG = dict(
    num=3123, title='最短路径中的边', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='两次 Dijkstra · 枚举边判断',
    tags=['难度分 2093'],
    code='''
class Solution(object):
    def findAnswer(self, n, edges):

        g = {index : {} for index in range(n)}
        for x, y, w in edges:
            g[x][y] = g[y][x] = w

        def dijkstra(start):
            dis = [-1] * n
            heap = [[0, start]]
            while heap:
                d, x = heapq.heappop(heap)
                if dis[x] == -1:
                    dis[x] = d
                    for y, w in g[x].items():
                        if dis[y] == -1:
                            heapq.heappush(heap, [d + w, y])
            
            return dis
        
        dis_start = dijkstra(0)
        dis_end = dijkstra(n - 1)

        res = [False] * len(edges)
        for index, (x, y, w) in enumerate(edges):
            if dis_start[x] != -1 and dis_end[y] != -1 and dis_start[x] + dis_end[y] + w == dis_start[-1]:
                res[index] = True
            if dis_start[y] != -1 and dis_end[x] != -1 and dis_start[y] + dis_end[x] + w == dis_start[-1]:
                res[index] = True
    
        return res
''',
    call=f'Solution().findAnswer({N}, {EDGES})',
    expect=EXPECT,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='heap', var='heap', fmt=lambda p: f'{p[1]}:{p[0]}', label='堆（点:距离）', top_color='purple', h=110),
        dict(type='text', fn=_check, h=50, size=26),
    ],
    watch=[('start', 'start', 'purple'), ('d', 'd', 'cyan'), ('x', 'x', 'pink'), ('y', 'y', 'blue'), ('w', 'w', 'orange')],
    skip=['g = {index', 'for x, y, w in edges:', 'g[x][y] = g[y][x]', 'dis = [-1]', 'def dijkstra', 'return dis', 'for y, w in g[x].items()', 'while heap'],
    captions={
        'heap = [[0, start]]': '从 `start = {start}` 出发：堆里放 `[距离, 点]`，起点距离 0。`dis[i] = -1` 表示还没到过',
        'heapq.heappop': '弹出堆里最近的 `[{d}, {x}]`',
        'if dis[x] == -1': lambda S, B, r: (f'`dis[{S.x}]` 还是 -1：==第一次到达==，`{S.d}` 就是最短距离' if S.dis[S.x] == -1
                                            else f'`dis[{S.x}]` 已经有值，这条是旧记录，跳过'),
        'dis[x] = d': '`dis[{x}] = {d}`',
        'if dis[y] == -1': lambda S, B, r: (f'邻居 `{S.y}`（边权 {S.w}）还没到过 → 值得入堆' if S.dis[S.y] == -1
                                            else f'邻居 `{S.y}`（边权 {S.w}）已定型，不用再入堆'),
        'heapq.heappush': '`{d} + {w}` = {d + w}，`[{d + w}, {y}]` 入堆',
        'dis_start = dijkstra(0)': lambda S, B, r: f'第一次 Dijkstra：从 0 出发的最短距离 `dis_start = {S.dis_start}`',
        'dis_end = dijkstra(n - 1)': lambda S, B, r: f'第二次 Dijkstra：从 `n-1` 出发（无向图，反过来也一样）`dis_end = {S.dis_end}`',
        'res = [False]': '准备结果 `res`，每条边先当作不在最短路上。接下来枚举每条边，用两个距离拼出经过它的最短路长度',
        'for index, (x, y, w) in enumerate(edges)': lambda S, B, r: ('所有边都检查完了' if B.get('index') == S.index and B.get('x') == S.x
                                                                      else f'检查边 `{S.index}`：`({S.x}, {S.y}, 权 {S.w})`，最短路总长是 `dis_start[-1] = {S.dis_start[-1]}`'),
        'if dis_start[x] != -1 and dis_end[y]': lambda S, B, r: (lambda v: f'==正走== `{S.x} → {S.y}`：`{S.dis_start[S.x]} + {S.w} + {S.dis_end[S.y]} = {v}`，总长 `{S.dis_start[-1]}` → ' + ('==相等==' if v == S.dis_start[-1] else '不相等'))(S.dis_start[S.x] + S.w + S.dis_end[S.y]),
        'if dis_start[y] != -1 and dis_end[x]': lambda S, B, r: (lambda v: f'==反走== `{S.y} → {S.x}`：`{S.dis_start[S.y]} + {S.w} + {S.dis_end[S.x]} = {v}`，总长 `{S.dis_start[-1]}` → ' + ('==相等==' if v == S.dis_start[-1] else '不相等'))(S.dis_start[S.y] + S.w + S.dis_end[S.x]),
        'res[index] = True': '拼出来正好等于总长 → 边 `{index}` 在某条最短路上，`res[{index}] = True`',
        'return res': '返回 `{ret}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='从两端各跑一次 Dijkstra，拼起来恰好等于最短路长的边就是答案',
        complexity='时间 `O(n + m log m)`，空间 `O(n + m)`',
        problem=['无向带权图，求从 `0` 到 `n-1` 的所有最短路',
                 '返回 `res`：第 `i` 条边在==至少一条==最短路上就是 `True`',
                 '本视频：`n=4`，4 条边，只有 `0 → 2 → 3` 一条最短路'],
        quote='对于图中的某条边(x, y, w)，如果其处于某条最短路径上，那么这条最短路径的构成必然是……从0到x，经过(x, y, w)，然后从y到n - 1……',
        quote_src='—— yiduobo 题解原文',
        idea=['最短路总长固定：`dis_start[n-1]`',
              '一条边在最短路上，必然是 “0 到 x，走边，y 到 n-1” 或者反过来',
              '所以只要两次 Dijkstra：一次从 0 出发，一次从 `n-1` 出发，再逐条边检查两种拼法的总长'],
        summary=['时间 `O(n + m log m)`，空间 `O(n + m)`',
                 '两个方向都要检查：边是无向的，`x → y` 和 `y → x` 都可能在最短路上',
                 '图不连通时距离是 `-1`，所以拼之前要先判断 `!= -1`',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '对比灵神：灵神只跑一次 Dijkstra，再从终点倒着搜；这里跑两次，不用搜索'],
    ),
)
