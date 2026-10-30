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
EDGES = [[0, 2, 2], [1, 2, 3], [2, 3, 1], [3, 4, 2], [0, 3, 5], [1, 4, 6]]
POS = [(0.0, 0.1), (0.0, 0.9), (0.33, 0.5), (0.66, 0.5), (1.0, 0.5)]
ARR = {(u, v) for u, v, _ in EDGES}

CODE = '''
class Solution(object):
    def minimumWeight(self, n, edges, src1, src2, dest):

        dis_s1 = [None] * n
        dis_s2 = [None] * n
        dis_d = [None] * n

        g = {}
        reverse_g = {}
        for x, y, w in edges:
            if x not in g:
                g[x] = {}
            if y not in g[x]:
                g[x][y] = w
            else:
                g[x][y] = min(g[x][y], w)
            
            if y not in reverse_g:
                reverse_g[y] = {}
            if x not in reverse_g[y]:
                reverse_g[y][x] = w
            else:
                reverse_g[y][x] = min(reverse_g[y][x], w)

        def dijkstra(s, g, dis):
            dis[s] = 0
            heap = []
            for next in g.get(s, {}):
                heapq.heappush(heap, [g[s][next], next])
            
            while heap:
                d, now = heapq.heappop(heap)
                if dis[now] is None:
                    dis[now] = d
                    for next in g.get(now, {}):
                        heapq.heappush(heap, [d + g[now][next], next])
            
        dijkstra(src1, g, dis_s1)
        dijkstra(src2, g, dis_s2)
        dijkstra(dest, reverse_g, dis_d)

        res = -1
        for t in range(n):
            if dis_s1[t] is not None and dis_s2[t] is not None and dis_d[t] is not None:
                if res == -1 or res > dis_s1[t] + dis_s2[t] + dis_d[t]:
                    res = dis_s1[t] + dis_s2[t] + dis_d[t]
        
        return res
'''
_L = CODE.split('\n')
PUSH = [i for i, l in enumerate(_L) if 'heapq.heappush' in l]


def _fm(v):
    return '?' if v is None else str(v)


def _arrs(S):
    return [S.get('dis_s1'), S.get('dis_s2'), S.get('dis_d')], 'heap' in (S.get('_inner') or {}), (S.get('_inner') or {})


def _ncol(S, T):
    d, run, inner = _arrs(S)
    res = S.get('res')
    best = None
    if not run and res is not None and res != -1 and all(a is not None for a in d):
        best = [t for t in range(N) if all(a[t] is not None for a in d) and sum(a[t] for a in d) == res]

    def f(i):
        if best and i in best and S.get('_line', 0) > PUSH[-1] + 3:
            return T['green']
        if run and inner.get('now') == i:
            return T['pink']
        if run and S.get('_line') in PUSH and inner.get('next') == i:
            return T['blue']
        return None
    return f


def _draw(cv, S, B, box, T):
    d, run, inner = _arrs(S)
    now, nx = inner.get('now'), inner.get('next')
    useg = run and S.get('_line') in PUSH and now is not None and nx is not None

    def ecol(k):
        u, v, w = EDGES[k]
        if useg and {u, v} == {now, nx}:
            return (T['yellow'], 6)
        return None

    def nlab(i):
        out = []
        for k, (nm, c) in enumerate((('s1', T['cyan']), ('s2', T['orange']), ('d', T['purple']))):
            if d[k] is not None:
                out.append((f'{nm}={_fm(d[k][i])}', c))
        return out
    _gdraw(cv, box, T, POS, EDGES, ncol=_ncol(S, T), nlab=nlab, ecol=ecol, arrows=ARR, r=30,
           title='s1 = dis_s1　s2 = dis_s2　d = dis_d（反向图上从 dest 出发）　? = 还没确定')


def _sumtxt(S):
    d, run, inner = _arrs(S)
    if run or any(a is None for a in d) or 'res' not in S:
        return ''
    t = S.get('t')
    parts = []
    for i in range(N):
        if all(a[i] is not None for a in d):
            parts.append(f'{i}:{d[0][i]}+{d[1][i]}+{d[2][i]}={sum(a[i] for a in d)}')
        else:
            parts.append(f'{i}:到不了')
    return '枚举中继点 t：`dis_s1[t]+dis_s2[t]+dis_d[t]`　' + '　'.join(parts)


CONFIG = dict(
    num=2203, title='包含要求路径的最小带权子图', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='正反图 Dijkstra · 枚举中继点',
    tags=['难度分 2364'],
    code=CODE,
    call=f'Solution().minimumWeight({N}, {EDGES}, 0, 1, 4)',
    expect=8,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='heap', var='heap', fmt=lambda p: f'{p[1]}:{p[0]}', label='heap（点:距离）', top_color='purple', h=100),
        dict(type='text', fn=_sumtxt, size=22),
    ],
    watch=[('s', lambda S: (S.get('_inner') or {}).get('s'), 'cyan'), ('d', lambda S: (S.get('_inner') or {}).get('d'), 'purple'),
           ('now', lambda S: (S.get('_inner') or {}).get('now'), 'pink'),
           ('next', lambda S: (S.get('_inner') or {}).get('next'), 'blue'), ('res', 'res', 'green')],
    skip=['dis_s2 = [None]', 'dis_d = [None]', 'g = {}', 'reverse_g = {}', 'for x, y, w in edges', 'if x not in g', 'g[x] = {}',
          'if y not in g[x]', 'g[x][y] = w', 'g[x][y] = min', 'if y not in reverse_g', 'reverse_g[y] = {}', 'if x not in reverse_g[y]',
          'reverse_g[y][x] = w', 'reverse_g[y][x] = min', 'heap = []', 'for next in g.get', 'while heap', 'for t in range(n)', 'dis[s] = 0', 'dis[now] = d'],
    captions={
        'dis_s1 = [None] * n': '三张距离表（`None` = 还没确定）：`dis_s1` 从 src1 出发，`dis_s2` 从 src2 出发，`dis_d` 到 dest',
        'heapq.heappush(heap, [g[s][next]': '`dis[{s}] = 0`；起点的邻居 `{next}` 入堆，距离 `{g[s][next]}`',
        'd, now = heapq.heappop(heap)': '弹出堆里距离最小的 `[{d}, {now}]`',
        'if dis[now] is None': lambda S, B, r: (f'`dis[{S.now}]` 还是 None：第一次弹出的就是最短路，==确定 dis[{S.now}] = {S.d}==' if S.dis[S.now] is None
                                                else f'`dis[{S.now}]` 已经是 {S.dis[S.now]}：这是更长的旧记录，跳过'),
        'heapq.heappush(heap, [d + g[now][next], next])': '经 `{now}` 到邻居 `{next}`：`{d} + {g[now][next]}` = =={d + g[now][next]}==，入堆（不判断大小，靠“只认第一次弹出”去重）',
        'dijkstra(src1, g, dis_s1)': '第一次：在正向图 `g` 上以 `src1 = {src1}` 为源',
        'dijkstra(src2, g, dis_s2)': '第二次：在正向图 `g` 上以 `src2 = {src2}` 为源',
        'dijkstra(dest, reverse_g, dis_d)': '第三次：在==反向图==上以 `dest = {dest}` 为源，`dis_d[t]` 就是 t 走到 dest 的最短路',
        'res = -1': '`res = -1` 表示还没找到可行的中继点；下面逐个枚举 t',
        'if dis_s1[t] is not None and': lambda S, B, r: (f'中继点 `t = {S.t}`：三条路都存在吗？' + (
            f'都存在（`{S.dis_s1[S.t]} + {S.dis_s2[S.t]} + {S.dis_d[S.t]}`）' if None not in (S.dis_s1[S.t], S.dis_s2[S.t], S.dis_d[S.t])
            else '有一条是 None（到不了）→ 这个 t 不行')),
        'if res == -1 or res > ': lambda S, B, r: (f'`t = {S.t}`：总和 {S.dis_s1[S.t] + S.dis_s2[S.t] + S.dis_d[S.t]}，' + (
            '还没有答案（res = -1）→ 先记下' if S.res == -1 else f'`res = {S.res}`，' + ('更小 → 更新' if S.res > S.dis_s1[S.t] + S.dis_s2[S.t] + S.dis_d[S.t] else '不更小 → 不动'))),
        'res = dis_s1[t] + dis_s2[t] + dis_d[t]': '`res` 更新为 =={res}==',
        'return res': '最小的 `dis_s1[t]+dis_s2[t]+dis_d[t]` = =={ret}==（t 就是图上的绿点）',
    },
    max_steps=120,
    cards=dict(
        one_liner='设两条路最早重合在 t：答案拆成 src1→t、src2→t、t→dest 三段',
        complexity='时间 `O(n + m log m)`，空间 `O(n + m)`',
        problem=['有向带权图，找 src1→dest 和 src2→dest 各一条路径',
                 '两条路径上所有边的权重和最小，==重复出现的边只算一次==',
                 '本视频：`n=5`，`src1=0, src2=1, dest=4` → ==8=='],
        quote='不妨设这两条路径上最早重复的点为t，那么最终答案就可以拆分成三个部分，分别为src1到t的最短路，src2到t的最短路，以及从t到dest的最短路。',
        quote_src='—— yiduobo 题解原文',
        idea=['麻烦在“重复边只算一次”→ 想办法去重：枚举最早重合的点 `t`',
              'src1→t、src2→t：分别以 src1、src2 为源跑 Dijkstra',
              't→dest：把所有边反向，在反向图上以 dest 为源跑一次'],
        summary=['三次 Dijkstra + 一次枚举，`O(n + m log m)`',
                 '原文用 `None` 表示不可达，枚举时三个距离都不是 None 才算',
                 '堆里入堆时不比较大小，靠“`dis[now]` 为 None 才记录”保证第一次弹出即最短',
                 '重边取最小权重：`g[x][y] = min(...)`',
                 '原文是 Python 2 风格，但无需改动即可运行（用到的 heapq 已预置）'],
    ),
)
