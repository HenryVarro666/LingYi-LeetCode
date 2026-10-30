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


def _arrs(S):
    inner = S.get('_inner') or {}
    run = 'h' in inner
    d = [S.get('d1'), S.get('d2'), S.get('d3')]
    if run:
        d[sum(1 for v in d if v is not None)] = inner.get('dis')
    return d, run, inner


def _fm(v):
    return '∞' if v is None or (isinstance(v, (int, float)) and v >= 10 ** 9) else str(v)


def _ncol(S, T):
    d, run, inner = _arrs(S)
    done = S.get('ans') is not None

    def f(i):
        if done and all(d[k] is not None and d[k][i] + 0 == d[k][i] for k in range(3)):
            tot = sum(d[k][i] for k in range(3))
            if tot == S['ans']:
                return T['green']
        if run and inner.get('x') == i:
            return T['pink']
        if run and inner.get('y') == i and S.get('_line') in (13, 14, 15, 16):
            return T['blue']
        return None
    return f


def _draw(cv, S, B, box, T):
    d, run, inner = _arrs(S)
    x, y = inner.get('x'), inner.get('y')
    useg = run and x is not None and y is not None and S.get('_line') in (13, 14, 15, 16)

    def ecol(k):
        u, v, w = EDGES[k]
        if useg and {u, v} == {x, y}:
            return (T['yellow'], 6)
        return None

    def nlab(i):
        out = []
        for k, (nm, c) in enumerate((('d1', T['cyan']), ('d2', T['orange']), ('d3', T['purple']))):
            if d[k] is not None:
                out.append((f'{nm}={_fm(d[k][i])}', c))
        return out
    _gdraw(cv, box, T, POS, EDGES, ncol=_ncol(S, T), nlab=nlab, ecol=ecol, arrows=ARR, r=30,
           title='d1 = 从 src1 出发　d2 = 从 src2 出发　d3 = 反图上从 dest 出发')


def _sumtxt(S):
    d1, d2, d3 = S.get('d1'), S.get('d2'), S.get('d3')
    if d1 is None or d3 is None or d2 is None or 'h' in (S.get('_inner') or {}):
        return ''
    parts = []
    for i in range(N):
        s = d1[i] + d2[i] + d3[i]
        parts.append(f'{i}:' + ('∞' if s >= 10 ** 9 else str(s)))
    return '相遇点 x 的 `d1+d2+d3`　' + '　'.join(parts)


CONFIG = dict(
    num=2203, title='包含要求路径的最小带权子图', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='三次 Dijkstra · 枚举相遇点',
    tags=['难度分 2364'],
    code='''
class Solution:
    def minimumWeight(self, n: int, edges: List[List[int]], src1: int, src2: int, dest: int) -> int:
        def dijkstra(g: List[List[Tuple[int, int]]], start: int) -> List[int]:
            dis = [inf] * n
            dis[start] = 0
            h = [(0, start)]

            while h:
                dis_x, x = heappop(h)
                if dis_x > dis[x]:
                    continue
                for y, wt in g[x]:
                    new_dis_y = dis_x + wt
                    if new_dis_y < dis[y]:
                        dis[y] = new_dis_y
                        heappush(h, (new_dis_y, y))
            return dis

        g = [[] for _ in range(n)]
        rg = [[] for _ in range(n)]  # 反图，用于计算从 dest 出发的最短路
        for x, y, wt in edges:
            g[x].append((y, wt))
            rg[y].append((x, wt))

        d1 = dijkstra(g, src1)
        d2 = dijkstra(g, src2)
        d3 = dijkstra(rg, dest)

        ans = min(map(sum, zip(d1, d2, d3)))  # 计算 d1[i]+d2[i]+d3[i] 的最小值
        return ans if ans < inf else -1
''',
    call=f'Solution().minimumWeight({N}, {EDGES}, 0, 1, 4)',
    expect=8,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='heap', var='h', fmt=lambda p: f'{p[1]}:{p[0]}', label='堆 h（点:距离）', top_color='purple', h=100),
        dict(type='text', fn=_sumtxt, size=24),
    ],
    watch=[('dis_x', 'dis_x', 'purple'), ('x', lambda S: (S.get('_inner') or {}).get('x'), 'pink'),
           ('y', lambda S: (S.get('_inner') or {}).get('y'), 'blue'),
           ('new_dis_y', lambda S: (S.get('_inner') or {}).get('new_dis_y'), 'orange'), ('ans', 'ans', 'green')],
    skip=['g[x].append', 'rg[y].append', 'for x, y, wt in edges', 'new_dis_y = dis_x + wt', 'g = [[]', 'dis[start] = 0',
          'for y, wt in g[x]', 'while h', 'dis[y] = new_dis_y', 'heappush', 'dis = [inf] * n', 'continue'],
    captions={
        'h = [(0, start)]': '`dis[i]` = 从 {start} 到 i 的最短路，初始全 ∞；堆里放 `(距离, 点)`，先放起点 `(0, {start})`',
        'rg = [[]': '再建一张==反图== `rg`：所有边反向，这样从 dest 出发就能算出“每个点到 dest”的最短路',
        'dis_x, x = heappop(h)': '弹出离起点最近的点 `{x}`，它的最短路已经确定 =={dis_x}==',
        'if dis_x > dis[x]': lambda S, B, r: (f'`{S.dis_x} > dis[{S.x}] = {S.dis[S.x]}`：旧的重复项，`continue` 跳过' if S.dis_x > S.dis[S.x]
                                              else f'`{S.dis_x} > {S.dis[S.x]}` 不成立：`{S.x}` 第一次出堆，用它更新邻居'),
        'for y, wt in g[x]': lambda S, B, r: (f'`{S.x}` 的邻居都看完了，回到堆里取下一个' if B.get('x') == S.x and B.get('y') == S.y
                                              else f'看 `{S.x}` 的邻居 `{S.y}`，边权 `{S.wt}`'),
        'if new_dis_y < dis[y]': lambda S, B, r: (f'经 `{S.x}` 到 `{S.y}`：`{S.dis_x} + {S.wt}` = =={S.new_dis_y}==，`< {_fm(S.dis[S.y])}` → ==更短==：更新 `dis[{S.y}]`，并把 `({S.new_dis_y}, {S.y})` 入堆' if S.new_dis_y < S.dis[S.y]
                                                  else f'经 `{S.x}` 到 `{S.y}`：`{S.dis_x} + {S.wt}` = =={S.new_dis_y}==，不比 `{_fm(S.dis[S.y])}` 短，不更新'),
        'return dis': '最短路表算完：`{dis}`（∞ 表示到不了）',
        'd1 = dijkstra': '第一次：从 `src1 = {src1}` 出发，得到 `d1`',
        'd2 = dijkstra': '第二次：从 `src2 = {src2}` 出发，得到 `d2`',
        'd3 = dijkstra': '第三次：在==反图==上从 `dest = {dest}` 出发，`d3[i]` = 从 i 走到 dest 的最短路',
        'ans = min': lambda S, B, r: ('枚举相遇点 x：`d1[x] + d2[x] + d3[x]`，两人在 x 相遇后合走到 dest（公共边只算一次）。最小值 =={0}==，绿色点就是最佳相遇点'.format(S.ans)),
        'return ans if': '`ans = {ans}` 不是 ∞，返回 =={ret}==；若是 ∞ 说明有人到不了，返回 -1',
    },
    max_steps=120,
    cards=dict(
        one_liner='最优子图是 Y 形：两人先各走各的，在某点相遇后合走到终点',
        complexity='时间 `O(n + m log m)`，空间 `O(n + m)`',
        problem=['有向带权图，选一个边权和最小的子图，使 `src1` 和 `src2` 都能到达 `dest`',
                 '公共边只算一次；不存在就返回 `-1`',
                 '本视频：`n=5`，`src1=0, src2=1, dest=4` → ==8=='],
        quote='如果两人相遇后又分开，各走各的，分别到达 dest，那么删除其中一条从相遇点到 dest 的路径，两人仍然可以到达 dest，……所以两人相遇后一定不会分开。',
        quote_src='—— 灵茶山艾府题解',
        idea=['反证得到子图是 Y 形：src1、src2 各走一段，在 `x` 汇合，再一起走到 `dest`',
              '枚举相遇点 `x`，答案 = `d1[x] + d2[x] + d3[x]`',
              '`d3` 要“每个点到 dest”，把边反向，从 dest 跑一次 Dijkstra 即可'],
        summary=['时间 `O(n + m log m)`：三次 Dijkstra，懒更新堆里有 `O(m)` 个元素',
                 '==要建反图==：d3 是“x 到 dest”，不是“dest 到 x”',
                 '`x = dest` 时对应两条路不重叠的链形情况，不用单独讨论',
                 '不可达是 ∞，三项相加仍是 ∞，最后判断 `ans < inf`',
                 '同类：单源最短路 + 枚举中转点'],
    ),
)
