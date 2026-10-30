import math as _m

EDGES0 = [[0, 1, 10], [0, 2, 1], [1, 2, 2]]
MM, N0 = 6, 3
POS = {0: (0.08, 0.5), 1: (0.86, 0.12), 2: (0.86, 0.9)}
LOOP_LINE = 11   # for u, v, cnt in edges
SUM_LINE = 14    # ans += min(a + b, cnt)


def _fd(v):
    return '∞' if (isinstance(v, float) and v == _m.inf) else v


def _cur(S):
    I = S.get('_inner') or {}
    return I if 'h' in I and 'start' in I else None


def _dist(S):
    I = _cur(S)
    if I is not None:
        return I['dist']
    return S.get('dist')


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    I = _cur(S)
    dist = _dist(S)
    line = S.get('_line')
    inloop = I is None and 'ans' in S and 'u' in S
    cur = None
    if inloop:
        for k, (a, b, c) in enumerate(EDGES0):
            if (a, b) == (S['u'], S['v']):
                cur = k
    done = len(EDGES0) if (I is None and line == LOOP_LINE + 4) else None
    cv.text((x0 + 18, y0 + 4), '细分图：边上的点 = 新节点（绿 = 在 maxMoves 内到得了）；圆 = 原节点，旁边是 dist', 20, T['muted'], bold=True)
    R = 32
    Lx, Rx, Tp, Bt = x0 + 70, x1 - 90, y0 + 80, y1 - 70
    P = {u: (Lx + fx * (Rx - Lx), Tp + fy * (Bt - Tp)) for u, (fx, fy) in POS.items()}
    for k, (u, v, cnt) in enumerate(EDGES0):
        a, b = P[u], P[v]
        d = _m.hypot(b[0] - a[0], b[1] - a[1])
        ux, uy = (b[0] - a[0]) / d, (b[1] - a[1]) / d
        shaded = done is not None or (cur is not None and (k < cur or (k == cur and line == SUM_LINE)))
        hot = (inloop and cur == k and line in (LOOP_LINE, LOOP_LINE + 1, LOOP_LINE + 2)) or (I is not None and 'wt' in I and {I['x'], I['y']} == {u, v})
        cv.line([(a[0] + ux * R, a[1] + uy * R), (b[0] - ux * R, b[1] - uy * R)], T['yellow'] if hot else T['border'], 5 if hot else 3)
        off = 26 + 44 * abs(uy)
        mx, my = (a[0] + b[0]) / 2 - uy * off, (a[1] + b[1]) / 2 + ux * off
        cv.text((mx, my), f'cnt={cnt}', 22, T['yellow'] if hot else T['muted'], anchor='mm', bold=True, mono=True)
        for i in range(1, cnt + 1):
            f = i / (cnt + 1)
            px, py = a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
            ok = False
            if dist is not None:
                ra = max(MM - dist[u], 0) if dist[u] != _m.inf else 0
                rb = max(MM - dist[v], 0) if dist[v] != _m.inf else 0
                ok = i <= ra or (cnt + 1 - i) <= rb
            col = T['green'] if (shaded and ok) else (T['dim'] if shaded else T['panel2'])
            cv.d.ellipse((px - 8, py - 8, px + 8, py + 8), fill=col, outline=T['border'])
    for u, (px, py) in P.items():
        du = dist[u] if dist is not None else None
        x = I.get('x') if I and 'd' in I else None
        if x == u:
            fill = T['blue']
        elif du is not None and du <= MM:
            fill = T['green']
        else:
            fill = T['panel2']
        cv.d.ellipse((px - R, py - R, px + R, py + R), fill=fill, outline=T['border'], width=2)
        cv.text((px, py), u, 28, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)
        if du is not None:
            if u == 0:
                cv.text((px, py + R + 22), f'dist={_fd(du)}', 20, T['yellow'], anchor='mm', bold=True, mono=True)
            else:
                cv.text((px + R + 10, py), f'dist={_fd(du)}', 20, T['yellow'], anchor='lm', bold=True, mono=True)


def _txt(S, B):
    I = _cur(S)
    if I is not None:
        return f'Dijkstra：只在原节点上跑，边权 = `cnt + 1`；`dist >= maxMoves = {MM}` 就不用再扩展'
    if 'u' in S and 'a' in S and 'b' in S and S.get('_line') in (LOOP_LINE + 2, LOOP_LINE + 3):
        return f"边 `({S['u']}, {S['v']}, cnt={S['cnt']})`：从 `{S['u']}` 能走进 `a = {S['a']}` 个，从 `{S['v']}` 能走进 `b = {S['b']}` 个"
    return f'从 0 出发，最多走 `maxMoves = {MM}` 步；数原节点 + 每条边上够得着的新节点'


CONFIG = dict(
    num=882, title='细分图中的可到达节点', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='Dijkstra + 边上两头数点',
    tags=['灵神题单·图论算法', '难度分 2328'],
    code='''
class Solution:
    def reachableNodes(self, edges: List[List[int]], maxMoves: int, n: int) -> int:
        g = [[] for _ in range(n)]
        for u, v, cnt in edges:
            g[u].append((v, cnt + 1))
            g[v].append((u, cnt + 1))  # 建图

        dist = self.dijkstra(g, 0, maxMoves)  # 从 0 出发的最短路

        ans = sum(d <= maxMoves for d in dist)  # 可以在 maxMoves 步内到达的点的个数
        for u, v, cnt in edges:
            a = max(maxMoves - dist[u], 0)
            b = max(maxMoves - dist[v], 0)
            ans += min(a + b, cnt)  # 这条边上可以到达的节点数
        return ans

    # Dijkstra 算法模板
    # 返回从 start 到每个点的最短路
    def dijkstra(self, g: List[List[Tuple[int]]], start: int, maxMoves: int) -> List[int]:
        dist = [inf] * len(g)
        dist[start] = 0
        h = [(0, start)]

        # 优化：最短路 >= maxMoves 就不用再算了（注意本题边权 > 0）
        while h and h[0][0] < maxMoves:
            d, x = heappop(h)
            if d > dist[x]:
                continue
            for y, wt in g[x]:
                new_d = d + wt
                if new_d < dist[y]:
                    dist[y] = new_d
                    heappush(h, (new_d, y))
        return dist
''',
    call=f'Solution().reachableNodes({EDGES0}, {MM}, {N0})',
    expect=13,
    max_steps=66,
    skip=[3, 4, 5, 6],
    views=[
        dict(type='text', fn=_txt, h=44, size=22),
        dict(type='custom', draw=_draw, h=360),
        dict(type='array', var=lambda S: [_fd(v) for v in _dist(S)] if _dist(S) is not None else None,
             label='dist[i]：0 到原节点 i 的最短路', h=140, cell=80),
        dict(type='heap', var=lambda S: (_cur(S) or {}).get('h'), label='h（最小堆，元素 = (距离, 节点)）', h=100, fmt=lambda t: f'({t[0]},{t[1]})'),
    ],
    watch=[('d', 'd', 'blue'), ('x', 'x', 'blue'), ('y', 'y', 'yellow'), ('new_d', 'new_d', 'orange'), ('a', 'a', 'green'), ('b', 'b', 'green'), ('ans', 'ans', 'green')],
    captions={
        'dist = self.dijkstra': '先只在==原节点==上求最短路：边长 = `cnt + 1`（走过 `cnt` 个新节点要 `cnt + 1` 步）',
        'dist = [inf]': '`dist[i]`：0 到原节点 `i` 的最短路，先设 ∞',
        'dist[start] = 0': '起点到自己是 `0`',
        'h = [(0, start)]': '起点 `(0, {start})` 入堆',
        'while h': lambda S, B, r: f'堆非空且堆顶距离 `{S.h[0][0]} < maxMoves = {S.maxMoves}`，继续' if (S.h and S.h[0][0] < S.maxMoves) else f'堆空或堆顶 `>= {S.maxMoves}`：==再远也到不了==，不用再算',
        'd, x = heappop': '弹出最近的 `x = {x}`，距离 `{d}`',
        'if d > dist[x]': lambda S, B, r: f'`{S.d} > dist[{S.x}] = {S.dist[S.x]}`：==旧记录==，跳过' if S.d > S.dist[S.x] else f'`{S.d} == dist[{S.x}]`：首次出堆，去更新邻居',
        'for y, wt in g[x]': lambda S, B, r: f'`{S.x}` 的邻居都看完了' if ('y' in B and 'wt' in B and (B.y, B.wt) == (S.y, S.wt) and B.x == S.x and B.d == S.d) else f'看边 `{S.x} → {S.y}`，边长 `{S.wt}`',
        'new_d = d + wt': '走这条边：`{d} + {wt}` = =={new_d}==',
        'if new_d < dist[y]': lambda S, B, r: f'`{S.new_d} < dist[{S.y}] = {_fd(S.dist[S.y])}` → ==更近，更新==' if S.new_d < S.dist[S.y] else f'`{S.new_d} ≥ dist[{S.y}] = {S.dist[S.y]}` → 不更新',
        'dist[y] = new_d': '`dist[{y}] = {new_d}`',
        'heappush': '`({new_d}, {y})` 入堆',
        'return dist': '最短路算完：`dist = {ret}`',
        'ans = sum': lambda S, B, r: f'原节点中 `dist <= maxMoves = {S.maxMoves}` 的有 `{S.ans}` 个，先记进答案',
        'a = max(maxMoves - dist[u], 0)': lambda S, B, r: f'站在 `{S.u}` 出发走，还剩 `{S.maxMoves} - {_fd(S.dist[S.u])}`，能走进这条边 `a = {S.a}` 个新节点',
        'b = max(maxMoves - dist[v], 0)': lambda S, B, r: f'站在 `{S.v}` 出发走，还剩 `{S.maxMoves} - {_fd(S.dist[S.v])}`，能走进这条边 `b = {S.b}` 个新节点',
        'ans += min': lambda S, B, r: f'两头合起来 `a + b = {S.a + S.b}`，但边上只有 `cnt = {S.cnt}` 个点（可能重叠）→ 加 `min({S.a + S.b}, {S.cnt})` = =={min(S.a + S.b, S.cnt)}==，`ans = {S.ans}`',
        11: lambda S, B, r: '所有边都数完了' if ('u' in B and (B.u, B.v) == (S.u, S.v)) else f'取边 `({S.u}, {S.v}, cnt={S.cnt})`',
        'return ans': '可到达节点总数 =={ret}==',
    },
    cards=dict(
        one_liner='原节点跑 Dijkstra，每条边从两头各数能走进几个点',
        complexity='时间 `O(n + m log m)`，空间 `O(n + m)`',
        problem=['无向图 `n` 个节点；第 `i` 条边 `[u, v, cnt]` 被细分成 `cnt` 个新节点',
                 '从节点 0 出发，==距离不超过 `maxMoves`== 的节点（含新节点）算可到达',
                 '示例：`edges=[[0,1,10],[0,2,1],[1,2,2]]`，`maxMoves=6`，`n=3` → `13`'],
        quote='先只在原节点上求最短路（边权 cnt + 1）。每条边上可以到达的节点数：a = max(maxMoves - dist[u], 0)，b = max(maxMoves - dist[v], 0)，ans += min(a + b, cnt)。',
        quote_src='—— 灵茶山艾府题解（据代码与注释）',
        idea=['新节点不用真建：边长设成 `cnt + 1`，只对原节点跑 Dijkstra',
              '边上的新节点只能从 `u` 或 `v` 走进来：`u` 侧最多 `a` 个，`v` 侧最多 `b` 个',
              '两侧可能覆盖同一批点，所以取 `min(a + b, cnt)`'],
        summary=['时间 `O(n + m log m)`，空间 `O(n + m)`',
                 '优化：堆顶距离 `>= maxMoves` 就停，再远的点走不进来',
                 '易错：边长是 `cnt + 1` 不是 `cnt`；`dist` 为 ∞ 时 `a`、`b` 取 0（靠 `max(..., 0)`）',
                 '原节点（`dist <= maxMoves`）和边上的新节点分开数，不要重复',
                 '同类：Dijkstra 加「每条边怎么数」的后处理'],
    ),
)
