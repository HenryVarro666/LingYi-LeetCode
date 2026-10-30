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
EDGES = [[0, 1, 2], [0, 2, 1], [1, 3, 1], [2, 3, 2], [1, 2, 5]]
POS = [(0.0, 0.5), (0.5, 0.0), (0.5, 1.0), (1.0, 0.5)]
EXPECT = [True, True, True, True, False]


def _phase2(S):
    return 'ans' in S


def _draw(cv, S, B, box, T):
    dis = S.get('dis')
    ph2 = _phase2(S)
    line = S.get('_line', 0)
    ans = S.get('ans') or []
    vis = S.get('vis')
    q = list(S.get('q') or [])
    h = S.get('h') or []
    inheap = {p[1] for p in h}
    x, y = S.get('x'), S.get('y')
    ei = S.get('i') if ph2 else None
    # 第一阶段：x 是刚弹出的点，y 是正在更新的邻居；第二阶段：y 是刚出队的点，x 是它的邻居
    inloop = 33 <= line <= 39 and ph2 and x is not None and y is not None
    inrelax = (not ph2) and 16 <= line <= 20 and x is not None and y is not None and 'new_dis' in S

    def ncol(i):
        if dis is None:
            return None
        if ph2:
            if inloop and i == y:
                return T['pink']
            if inloop and i == x:
                return T['blue']
            if vis and vis[i]:
                return T['yellow'] if i in q else T['green']
            return None
        if x is not None and i == x and 13 <= line <= 20:
            return T['pink']
        if inrelax and i == y:
            return T['blue']
        if isinstance(dis[i], float):
            return None
        return T['yellow'] if i in inheap else T['green']

    def ecol(k):
        u, v, w = EDGES[k]
        if ph2:
            if inloop and ei == k:
                return (T['yellow'], 7)
            if k < len(ans) and ans[k]:
                return (T['green'], 7)
            return None
        if inrelax and {u, v} == {x, y}:
            return (T['yellow'], 6)
        return None

    def nlab(i):
        if dis is None:
            return []
        return [(f'dis={_fnum(dis[i])}', T['cyan'])]
    _gdraw(cv, box, T, POS, [tuple(e) for e in EDGES], ncol=ncol, nlab=nlab, ecol=ecol, r=30,
           title='绿边 = 已确认在最短路上的边' if ph2 else '粉 = 刚弹出的 x　蓝 = 在更新的 y　黄 = 在堆里　绿 = 已确定')


def _check(S):
    if 'ans' not in S or not (34 <= S.get('_line', 0) <= 36) or 'w' not in S or S.get('x') is None:
        return ''
    x, y, w, dis = S['x'], S['y'], S['w'], S['dis']
    lhs = dis[x] + w
    if lhs == dis[y]:
        return f"`dis[{x}] + {w} = {lhs}` ==等于== `dis[{y}] = {dis[y]}` → 边 {x}-{y} 在最短路上"
    return f"`dis[{x}] + {w} = {lhs}` ≠ `dis[{y}] = {dis[y]}` → 边 {x}-{y} 不在最短路上"


CONFIG = dict(
    num=3123, title='最短路径中的边', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='Dijkstra + 从终点倒着 BFS',
    tags=['难度分 2093'],
    code='''
class Solution:
    def findAnswer(self, n: int, edges: List[List[int]]) -> List[bool]:
        g = [[] for _ in range(n)]
        for i, (x, y, w) in enumerate(edges):
            g[x].append((y, w, i))
            g[y].append((x, w, i))

        # Dijkstra 算法模板
        dis = [inf] * n
        dis[0] = 0
        h = [(0, 0)]
        while h:
            dx, x = heappop(h)
            if dx > dis[x]:
                continue
            for y, w, _ in g[x]:
                new_dis = dx + w
                if new_dis < dis[y]:
                    dis[y] = new_dis
                    heappush(h, (new_dis, y))

        ans = [False] * len(edges)
        # 图不连通
        if dis[-1] == inf:
            return ans

        # 从终点出发 BFS
        vis = [False] * n
        vis[-1] = True
        q = deque([n - 1])
        while q:
            y = q.popleft()
            for x, w, i in g[y]:
                if dis[x] + w != dis[y]:
                    continue
                ans[i] = True
                if not vis[x]:
                    vis[x] = True
                    q.append(x)
        return ans
''',
    call=f'Solution().findAnswer({N}, {EDGES})',
    expect=EXPECT,
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='heap', var='h', fmt=lambda p: f'{p[1]}:{p[0]}', label='堆 h（点:距离）', top_color='purple', h=110),
        dict(type='queue', var='q', label='队列 q', h=110),
        dict(type='text', fn=_check, h=50, size=26),
    ],
    watch=[('x', 'x', 'pink'), ('y', 'y', 'blue'), ('w', 'w', 'orange')],
    skip=['g = [[]', 'g[x].append', 'g[y].append', 'for i, (x, y, w) in enumerate', 'new_dis = dx + w', 'dis[0] = 0',
          'vis = [False]', 'continue', 'vis[x] = True', 'for y, w, _ in g[x]', 'for x, w, i in g[y]'],
    captions={
        'dis = [inf] * n': '第一步：Dijkstra 求 0 到每个点的最短路 `dis`，起点 `dis[0] = 0`',
        'h = [(0, 0)]': '最小堆放 `(距离, 点)`，先放起点',
        'while h': lambda S, B, r: ('堆里还有记录，继续取最近的点' if S.h else '堆空了：所有点的最短路都定下来了'),
        'while q': lambda S, B, r: ('队列里还有点，取出一个检查它的边' if S.q else '队列空了：所有通向终点的最短路边都标记完'),
        'dx, x = heappop(h)': '弹出堆顶：当前离起点最近的点 `{x}`，`dis = {dx}`',
        'if dx > dis[x]': lambda S, B, r: (f'`{S.dx} > dis[{S.x}] = {S.dis[S.x]}`：旧记录，跳过' if S.dx > S.dis[S.x]
                                           else f'`dx = {S.dx}` 等于 `dis[{S.x}]`：有效，用 `{S.x}` 更新它的邻居'),
        'for y, w, _ in g[x]': lambda S, B, r: (f'`{S.x}` 的邻居都看完了' if B.get('x') == S.x and B.get('y') == S.y
                                                else f'邻居 `{S.y}`，边权 `{S.w}`'),
        'if new_dis < dis[y]': lambda S, B, r: (f'经 `{S.x}` 走到 `{S.y}`：`{S.dx} + {S.w}` = =={S.new_dis}==，比 `{_fnum(S.dis[S.y])}` 小 → 更新' if S.new_dis < S.dis[S.y]
                                                else f'经 `{S.x}` 走到 `{S.y}`：`{S.dx} + {S.w}` = {S.new_dis}，不比 `{S.dis[S.y]}` 小 → 不更新'),
        'dis[y] = new_dis': '`dis[{y}]` 更新为 =={dis[y]}=='
        ,
        'heappush': '`({new_dis}, {y})` 入堆',
        'ans = [False]': 'Dijkstra 完成。准备 `ans`，每条边先假设不在最短路上',
        'if dis[-1] == inf': lambda S, B, r: ('终点到不了 → 全 False' if S.dis[-1] == float('inf')
                                              else f'`dis[-1] = {S.dis[-1]}`，终点可达，继续'),
        'vis[-1] = True': '==从终点倒着找==：起点出发找的边不一定通向终点，终点出发找到的才一定在 0 到 n-1 的最短路上',
        'q = deque': '从终点 `{n - 1}` 开始 BFS',
        'y = q.popleft()': '取出点 `{y}`，检查它的每条边',
        'for x, w, i in g[y]': lambda S, B, r: (f'`{S.y}` 的边都检查完了' if B.get('y') == S.y and B.get('x') == S.x and B.get('i') == S.i
                                                else f'看边 `{S.i}`：邻居 `{S.x}`，边权 `{S.w}`'),
        'if dis[x] + w != dis[y]': lambda S, B, r: (f'`dis[{S.x}] + {S.w} = {S.dis[S.x] + S.w}` ≠ `dis[{S.y}] = {S.dis[S.y]}` → 这条边走不出最短路，跳过' if S.dis[S.x] + S.w != S.dis[S.y]
                                                    else f'`dis[{S.x}] + {S.w} = {S.dis[S.x] + S.w}` == `dis[{S.y}] = {S.dis[S.y]}` → 边在最短路上'),
        'ans[i] = True': '等式成立：边 `{i}`（{x}-{y}）在某条最短路上 → `ans[{i}] = True`',
        'if not vis[x]': lambda S, B, r: (f'`{S.x}` 还没访问过，加入队列' if not S.vis[S.x] else f'`{S.x}` 已访问过，但边已经标记好了'),
        'q.append(x)': '标记 `vis[{x}]` 并让 `{x}` 入队，之后继续往起点方向倒推',
        'return ans': '返回 `{ret}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='先 Dijkstra 求最短路，再从终点倒着找满足 `dis[x] + w = dis[y]` 的边',
        complexity='时间 `O(n + m log m)`，空间 `O(n + m)`',
        problem=['无向带权图，求起点 `0` 到终点 `n-1` 的所有最短路',
                 '返回 `ans`：第 `i` 条边只要在==至少一条==最短路上就为 `true`',
                 '图可能不连通；本视频：`n=4`，5 条边，有两条等长最短路、一条多余的边'],
        quote='从终点 n-1 出发，倒着 DFS 或 BFS，设当前在点 y，邻居为 x，边权为 w，如果满足 dis[x] + w = dis[y]，则说明 x-y 这条边在从 0 到 n-1 的最短路上。',
        quote_src='—— 灵茶山艾府题解',
        idea=['Dijkstra 得到起点到所有点的最短路 `dis`',
              '为什么从终点出发：从起点满足等式的边==不一定通向终点==，比如一棵树的分支',
              '终点倒着走，每条满足等式的边都能接到终点，一定在最短路上'],
        after=[dict(heading='另一种写法', lines=['写法一：把 BFS 换成递归 DFS', '同样从终点出发、同样判断等式', '只是用 `vis` + 递归代替队列'])],
        summary=['时间 `O(n + m log m)`，空间 `O(n + m)`',
                 '==必须从终点往回找==，从起点找会把不通向终点的边也标成 true',
                 '先判断终点是否可达：`dis[-1] == inf` 时全为 False',
                 '边已标记后，点只入队一次（`vis`），否则会重复',
                 '同类：最短路上的点/边计数'],
    ),
)
