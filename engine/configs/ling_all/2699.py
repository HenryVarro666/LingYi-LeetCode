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

N = 5
ORIG = [[0, 1, -1], [1, 4, 2], [0, 2, 3], [2, 4, -1], [0, 3, -1], [3, 4, 4]]
POS = [(0.0, 0.5), (0.4, 0.0), (0.4, 0.5), (0.4, 1.0), (1.0, 0.5)]
SRC, DST, TARGET = 0, 4, 6

CODE = '''
class Solution:
    def modifiedGraphEdges(self, n: int, edges: List[List[int]], source: int, destination: int, target: int) -> List[List[int]]:
        g = [[] for _ in range(n)]
        for i, (x, y, _) in enumerate(edges):
            g[x].append((y, i))
            g[y].append((x, i))  # 建图，额外保存边的编号

        dis = [[1 << 30] * 2 for _ in range(n)]
        dis[source] = [0] * 2

        def dijkstra(k: int) -> None:  # 这里 k 表示第一次/第二次
            vis = [False] * n
            while True:
                # 找到当前最短路，去更新它的邻居的最短路
                # 根据数学归纳法，dis[x][k] 一定是最短路长度
                x = -1
                for y, (b, d) in enumerate(zip(vis, dis)):
                    if not b and (x < 0 or d[k] < dis[x][k]):
                        x = y
                if x == destination:  # 起点 source 到终点 destination 的最短路已确定
                    return
                vis[x] = True  # 标记，在后续的循环中无需反复更新 x 到其余点的最短路长度
                for y, eid in g[x]:
                    wt = edges[eid][2]
                    if wt == -1:
                        wt = 1  # -1 改成 1
                    if k == 1 and edges[eid][2] == -1:
                        # 第二次 Dijkstra，改成 w
                        w = delta + dis[y][0] - dis[x][1]
                        if w > wt:
                            edges[eid][2] = wt = w  # 直接在 edges 上修改
                    # 更新最短路
                    dis[y][k] = min(dis[y][k], dis[x][k] + wt)

        dijkstra(0)
        delta = target - dis[destination][0]
        if delta < 0:  # -1 全改为 1 时，最短路比 target 还大
            return []

        dijkstra(1)
        if dis[destination][1] < target:  # 最短路无法再变大，无法达到 target
            return []

        for e in edges:
            if e[2] == -1:  # 剩余没修改的边全部改成 1
                e[2] = 1
        return edges
'''
_L = CODE.split('\n')
_A = next(i for i, l in enumerate(_L) if 'for y, eid in g[x]' in l)
_B = next(i for i, l in enumerate(_L) if 'dis[y][k] = min' in l)
EDGE_LINES = range(_A, _B + 1)


def _fm(v):
    return '∞' if v is None or v >= (1 << 30) else str(v)


def _cur(S):
    inner = S.get('_inner') or {}
    return inner, 'vis' in inner


def _ncol(S, T):
    inner, run = _cur(S)

    def f(i):
        if run and inner.get('x') == i and inner.get('x', -1) >= 0:
            return T['pink']
        if run and 'eid' in inner and S.get('_line') in EDGE_LINES and inner.get('y') == i:
            return T['blue']
        if run and inner['vis'][i]:
            return T['green']
        return None
    return f


def _draw(cv, S, B, box, T):
    inner, run = _cur(S)
    E = S.get('edges') or ORIG
    dis = S.get('dis')
    x, y = inner.get('x'), inner.get('y')
    act = run and S.get('_line') in EDGE_LINES and x is not None and y is not None and 'eid' in inner
    k = inner.get('k')
    two = 'delta' in S

    def ecol(i):
        u, v, w = ORIG[i]
        if act and inner.get('eid') == i:
            return (T['pink'], 7)
        if w == -1:
            return (T['yellow'], 5) if E[i][2] != -1 else (T['orange'], 5)
        return None

    def elab(i):
        w = E[i][2]
        return '?' if w == -1 else str(w)

    def nlab(i):
        if dis is None:
            return []
        out = [(f'd0={_fm(dis[i][0])}', T['cyan'])]
        if two:
            out.append((f'd1={_fm(dis[i][1])}', T['purple']))
        return out
    _gdraw(cv, box, T, POS, ORIG, ncol=_ncol(S, T), nlab=nlab, ecol=ecol, elab=elab, r=30,
           title='橙 = 待定 -1 边　黄 = 已改的权　d0 = 全按 1　d1 = 边走边改')


def _fx(S):
    if 'delta' not in S:
        return '第一遍：把所有 -1 当成 1，求 d0，看看最短路最少是多少'
    d = S['delta']
    return f'`delta = target − d0[dest] = {TARGET} − {TARGET - d} = {d}`　第二遍：改 -1 边　`w = delta + d0[y] − d1[x]`'


CONFIG = dict(
    num=2699, title='修改图中的边权', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='两遍 Dijkstra · 边走边改权',
    tags=['难度分 2874'],
    code=CODE,
    call=f'Solution().modifiedGraphEdges({N}, {ORIG}, {SRC}, {DST}, {TARGET})',
    expect=[[0, 1, 4], [1, 4, 2], [0, 2, 3], [2, 4, 3], [0, 3, 4], [3, 4, 4]],
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', fn=_fx, size=24),
    ],
    watch=[('k', lambda S: (S.get('_inner') or {}).get('k'), 'cyan'), ('x', lambda S: (S.get('_inner') or {}).get('x'), 'pink'),
           ('y', lambda S: (S.get('_inner') or {}).get('y'), 'blue'),
           ('wt', lambda S: (S.get('_inner') or {}).get('wt'), 'orange'), ('delta', 'delta', 'purple')],
    skip=['g = [[]', 'for i, (x, y, _) in enumerate', 'g[x].append', 'g[y].append', 'dis[source] = [0]', 'vis = [False]',
          'while True', 'x = -1', 'for y, (b, d) in enumerate', 'if not b and', 'x = y', 'vis[x] = True', 'for y, eid in g[x]',
          'wt = edges[eid][2]', 'if wt == -1', 'wt = 1', 'if k == 1 and', 'for e in edges', 'if e[2] == -1'],
    captions={
        'dis = [[1 << 30]': '`dis[i][k]`：第 k 遍 Dijkstra 里 source 到 i 的最短路；k=0 是第一遍，k=1 是第二遍',
        'dijkstra(0)': '第一遍：-1 边都当作 1，求出每个点的最短路 `dis[i][0]`',
        'if x == destination': lambda S, B, r: (f'取出还没处理、最短路最小的点 `x = {S.x}`' + (
            '，正是终点 → 终点最短路已确定，本遍结束' if S.x == S.destination else f'（`dis[{S.x}][{S.k}] = {S.dis[S.x][S.k]}`），用它去更新邻居')),
        'delta = target': lambda S, B, r: (f'`delta = {S.target} − {S.dis[S.destination][0]}` = =={S.delta}==：全按 1 时最短路是 {S.dis[S.destination][0]}，还差 delta 才到 target'),
        'if delta < 0': lambda S, B, r: ('`delta < 0`：-1 全改成最小的 1，最短路都已经超过 target，只会更大 → 无解' if S.delta < 0
                                         else '`delta ≥ 0`：全按 1 时最短路不超过 target，有希望，继续'),
        'dijkstra(1)': '第二遍：按 Dijkstra 的顺序，一边走一边把 -1 边改成合适的 w。已确定的最短路不会被后面的改动影响',
        'w = delta': lambda S, B, r: (f'经 `{S.x}→{S.y}` 的路径 = `d1[{S.x}] + w + (d0[dest] − d0[{S.y}])` 要等于 target，'
                                      f'解得 `w = delta + d0[{S.y}] − d1[{S.x}]` = `{S.delta} + {S.dis[S.y][0]} − {S.dis[S.x][1]}` = =={S.w}=='),
        'if w > wt': lambda S, B, r: (f'`w = {S.w}` 比 1 大 → 把这条边改成 w' if S.w > S.wt
                                      else f'`w = {S.w}` 不比 1 大 → 保持 1，这里不用补'),
        'edges[eid][2] = wt = w': '直接把这条边改成 =={wt}==',
        'dis[y][k] = min': lambda S, B, r: (f'`dis[{S.y}][{S.k}] = min({_fm(B["dis"][S.y][S.k])}, {S.dis[S.x][S.k]} + {S.wt})` = =={S.dis[S.y][S.k]}=='),
        'if dis[destination][1] < target': lambda S, B, r: (f'`d1[dest] = {S.dis[S.destination][1]}`，' + (
            '< target：即使改完最短路仍太小 → 无解' if S.dis[S.destination][1] < S.target else '等于 target：改完恰好是 target ✓')),
        21: '终点最短路已确定，这一遍结束，函数返回',
        'return edges': '剩下没改到的 -1 边统一改成 1，返回改好的 `edges`',
    },
    max_steps=120,
    cards=dict(
        one_liner='先全按 1 求最短路，再按 Dijkstra 的顺序边走边改，把最短路抬到 target',
        complexity='时间 `O(n²)`（稠密图朴素 Dijkstra），空间 `O(m)`',
        problem=['无向带权连通图，部分边权是 `-1`，其余为正',
                 '把 `-1` 改成 `[1, 2×10^9]` 的正整数，使 source 到 destination 的最短距离恰为 `target`',
                 '本视频：`n=5`，`0→4`，`target=6`，有 4 条 -1 边'],
        quote='按照 Dijkstra 算法遍历点/边的顺序去修改，就不会对已确定的最短路产生影响。……w = target − d[destination][0] + d[y][0] − d[x][1]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['无解：全改成 1 仍然比 target 长；或全改成无穷大仍比 target 短',
              '只改一两条边不行：最短路会绕到别的边上',
              '第二遍 Dijkstra：改边 x-y 时，前面 source→x 已定，后面 y→dest 还没改，用第一遍的 d0 代替'],
        summary=['时间 `O(n²)`：输入最坏是稠密图，朴素 Dijkstra 比堆更合适',
                 '要记录边的编号，才能在邻接表里直接改 `edges`',
                 '只有 `w > 1` 才需要改；剩下仍是 -1 的边统一改成 1',
                 '两种无解判断：第一遍后 `delta < 0`；第二遍后 `d1[dest] < target`',
                 '同类：Dijkstra 中途改边 / 不变式推导'],
    ),
)
