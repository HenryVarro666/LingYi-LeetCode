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
class Solution(object):
    def modifiedGraphEdges(self, n, edges, source, destination, target):

        global g
        g = [[None] * n for _ in range(n)]
        for x, y, v in edges:
            g[x][y] = g[y][x] = v

        def dijkstra(start):
            dis = [None] * n
            dis[start] = 0
            vis = [False] * n
            global g

            for _ in range(n):
                mi = None
                for i in range(n):
                    if dis[i] is not None and not vis[i] and (mi is None or dis[mi] > dis[i]):
                        mi = i
                
                if mi is None:
                    break
                
                vis[mi] = True

                for i in range(n):
                    if g[mi][i] is not None:
                        d = abs(g[mi][i])
                        if start == source and g[mi][i] == -1:
                            if dis[mi] + pre_dis[i] + 1 < target:
                                g[mi][i] = g[i][mi] = target - dis[mi] - pre_dis[i]
                            else:
                                g[mi][i] = g[i][mi] = 1

                            d = g[mi][i]

                        if dis[i] is None or dis[i] > dis[mi] + d:
                            dis[i] = dis[mi] + d
            
            return dis
        

        pre_dis = dijkstra(destination)
        if pre_dis[source] > target:
            return []

        dis = dijkstra(source)
        if dis[destination] < target:
            return []
        
        res = []
        for x, y, v in edges:
            if v == -1:
                res.append([x, y, g[x][y]])
            else:
                res.append([x, y, v])

        return res
'''
_L = CODE.split('\n')
_A = next(i for i, l in enumerate(_L) if 'if g[mi][i] is not None' in l)
_B = next(i for i, l in enumerate(_L) if 'dis[i] = dis[mi] + d' in l)
REL = range(_A, _B + 1)
_C2 = next(i for i, l in enumerate(_L) if 'g[mi][i] = g[i][mi] = 1' in l)


def _fm(v):
    return '?' if v is None else str(v)


def _cur(S):
    inner = S.get('_inner') or {}
    return inner, 'vis' in inner


def _orig(u, v):
    for a, b, w in ORIG:
        if {a, b} == {u, v}:
            return w
    return None


def _weights(S):
    """当前每条边的权（g 是全局变量，快照里没有，只能从状态推出来）"""
    inner, run = _cur(S)
    W = [w for _, _, w in ORIG]
    res = S.get('res')
    if isinstance(res, list) and len(res) == len(ORIG) and all(isinstance(r, list) for r in res):
        return [r[2] for r in res]
    pre = S.get('pre_dis')
    if run and inner.get('start') == SRC:
        dis, vis = inner['dis'], inner['vis']
    elif not run and S.get('dis') is not None and pre is not None and 'vis' not in inner:
        dis, vis = S['dis'], [True] * N
    else:
        return W
    mi, i, line = inner.get('mi'), inner.get('i'), S.get('_line', 0)
    for k, (u, v, w) in enumerate(ORIG):
        if w != -1 or dis[u] is None or dis[v] is None and not (vis[u] or vis[v]):
            continue
        cand = [x for x in (u, v) if vis[x] and dis[x] is not None]
        if not cand:
            continue
        a = min(cand, key=lambda x: (dis[x], x))
        b = v if a == u else u
        if run and a == mi and mi is not None and i is not None:
            if not (b < i or (b == i and line > _C2)):
                continue
        W[k] = (TARGET - dis[a] - pre[b]) if dis[a] + pre[b] + 1 < TARGET else 1
    return W


def _ncol(S, T):
    inner, run = _cur(S)

    def f(i):
        if run and inner.get('mi') == i and S.get('_line') in REL:
            return T['pink']
        if run and inner.get('mi') == i:
            return T['pink']
        if run and S.get('_line') in REL and inner.get('i') == i:
            return T['blue']
        return None
    return f


def _draw(cv, S, B, box, T):
    inner, run = _cur(S)
    WS = _weights(S)
    mi, i = inner.get('mi'), inner.get('i')
    act = run and S.get('_line') in REL and mi is not None and i is not None
    pre = S.get('pre_dis')
    dis = S.get('dis') if run is False else None
    if run:
        if inner.get('start') == DST:
            pre = inner['dis']
        else:
            dis = inner['dis']

    def ecol(k):
        u, v, w = ORIG[k]
        if act and {u, v} == {mi, i}:
            return (T['pink'], 7)
        if w == -1:
            return (T['yellow'], 5) if WS[k] != -1 else (T['orange'], 5)
        return None

    def elab(k):
        cur = WS[k]
        return '?' if cur == -1 else str(cur)

    def nlab(j):
        out = []
        if pre is not None:
            out.append((f'p={_fm(pre[j])}', T['cyan']))
        if dis is not None and inner.get('start', SRC) == SRC:
            out.append((f'd={_fm(dis[j])}', T['purple']))
        return out
    _gdraw(cv, box, T, POS, ORIG, ncol=_ncol(S, T), nlab=nlab, ecol=ecol, elab=elab, r=30,
           title='橙 = 待定 -1 边　黄 = 已改的权　p = pre_dis（dest 出发）　d = dis（source 出发）')


def _fx(S):
    inner, run = _cur(S)
    if S.get('pre_dis') is None and not (run and inner.get('start') == DST):
        return '先把 -1 当成 1，从 destination 出发求 pre_dis：每个点到 destination 的最短路'
    if run and inner.get('start') == DST:
        return '第一遍：-1 边当成 1（`abs`），从 destination 出发，得到 `pre_dis`'
    return f'第二遍：从 source 出发，遇到 -1 边：`w = target − dis[x] − pre_dis[y]`（target = {TARGET}）'


CONFIG = dict(
    num=2699, title='修改图中的边权', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='两次 Dijkstra · 走到哪改到哪',
    tags=['难度分 2874'],
    code=CODE,
    call=f'Solution().modifiedGraphEdges({N}, {ORIG}, {SRC}, {DST}, {TARGET})',
    expect=[[0, 1, 4], [1, 4, 2], [0, 2, 3], [2, 4, 3], [0, 3, 2], [3, 4, 4]],
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', fn=_fx, size=24),
    ],
    watch=[('start', lambda S: (S.get('_inner') or {}).get('start'), 'cyan'), ('mi', lambda S: (S.get('_inner') or {}).get('mi'), 'pink'),
           ('i', lambda S: (S.get('_inner') or {}).get('i'), 'blue'), ('d', lambda S: (S.get('_inner') or {}).get('d'), 'orange')],
    skip=['global g', 'g = [[None]', 'for x, y, v in edges:', 'g[x][y] = g[y][x] = v', 'dis[start] = 0', 'vis = [False]', 'for _ in range(n)',
          'mi = None', 'for i in range(n)', 'if dis[i] is not None and not vis', 'mi = i', 'if mi is None', 'break', 'vis[mi] = True',
          'if g[mi][i] is not None', 'd = abs(', 'if start == source and', 'dis[i] = dis[mi] + d', 'd = g[mi][i]', 'res = []', 'if v == -1', 'res.append'],
    captions={
        'dis = [None] * n': '`dis[i]`：start 到 i 的最短路，`None` 表示还没算到；`g` 是邻接矩阵，`-1` 表示可改的边',
        'pre_dis = dijkstra': '第一遍：从 `destination` 出发。-1 边按 1 算（`abs`），因为图是无向的，所以也是“每个点到 destination”',
        'if pre_dis[source] > target': lambda S, B, r: (f'`pre_dis[source] = {S.pre_dis[S.source]}`，' + (
            '> target：-1 全取最小的 1 仍然太长 → 无解' if S.pre_dis[S.source] > S.target else '≤ target：有希望，继续')),
        'dis = dijkstra': '第二遍：从 `source` 出发，==边算边改==：弹出 mi 的时候，它到 source 的 `dis[mi]` 已经定了',
        'if dis[mi] + pre_dis[i] + 1 < target': lambda S, B, r: (
            f'边 `{S.mi}→{S.i}` 是 -1：走它（权取最小 1）到 destination 要 `dis[{S.mi}] + 1 + pre_dis[{S.i}] = {S.dis[S.mi] + 1 + S.pre_dis[S.i]}`，' + (
                '比 target 小 → 要把它加大' if S.dis[S.mi] + S.pre_dis[S.i] + 1 < S.target else '已经 ≥ target → 取 1 就行')),
        'g[mi][i] = g[i][mi] = target': '`w = target − dis[mi] − pre_dis[i]` = `{target} − {dis[mi]} − {pre_dis[i]}` = =={target - dis[mi] - pre_dis[i]}==：这样经过它到 destination 恰好 = target',
        'g[mi][i] = g[i][mi] = 1': '用不着加大：权取 ==1==',
        'if dis[i] is None or dis[i] > dis[mi] + d': lambda S, B, r: (
            f'经 `{S.mi}` 到 `{S.i}` = `{S.dis[S.mi]} + {S.d}` = {S.dis[S.mi] + S.d}；' + (
                '`dis[i]` 还是 None → 更新' if S.dis[S.i] is None else (
                    f'比 `dis[{S.i}] = {S.dis[S.i]}` ' + ('更短 → 更新' if S.dis[S.i] > S.dis[S.mi] + S.d else '不更短 → 不动')))),
        'return dis': '这一遍的最短路表：`{dis}`',
        'if dis[destination] < target': lambda S, B, r: (f'`dis[destination] = {S.dis[S.destination]}`，' + (
            '< target：存在一条不含 -1 的更短路，改不了 → 无解' if S.dis[S.destination] < S.target else '等于 target ✓ 有解')),
        'return res': '按原顺序收集每条边现在的权，返回 `res`',
    },
    max_steps=130,
    cards=dict(
        one_liner='先求每点到终点的距离，再边走边改：把经过 -1 边的路径恰好调成 target',
        complexity='时间 `O(n²)`，空间 `O(n²)`（邻接矩阵）',
        problem=['无向带权连通图，部分边权为 `-1`，其余为正',
                 '把 `-1` 改成正整数，使 source 到 destination 的最短路恰为 `target`；无解返回空数组',
                 '本视频：`n=5`，`0→4`，`target=6`'],
        quote='边(x, y)的新权重就应该是target - dis[x] - pre_dis[y]，其中dis[x]表示本轮dijkstra算法计算的在边权调整后从source到x的最短路长度，而pre_dis[y]则表示在边权还未调整之前，从destination出发到y的最短路径长度。',
        quote_src='—— yiduobo 题解原文',
        idea=['无解两种：-1 全取 1 仍然 > target；或不用 -1 边就有路径 < target',
              '第一遍：-1 当 1，从 destination 出发得 `pre_dis`（无向图，等价于 y 到 destination）',
              '第二遍：source 出发，弹出 x 时对 x 的 -1 边立刻定权，不会影响已定的最短路'],
        summary=['时间 `O(n²)`：邻接矩阵 + 朴素 Dijkstra，不用堆',
                 '`-1` 既是“待改”标记也是权，计算距离时用 `abs`',
                 '第二遍只在 `start == source` 时改权；`pre_dis` 要在改动之前算好',
                 '最后检查 `dis[destination] < target`，对应“无 -1 边的短路”那种无解',
                 '原文是 Python 2 风格，但无需改动即可运行（用到 `global g`）'],
    ),
)
