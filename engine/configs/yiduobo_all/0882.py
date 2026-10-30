import math as _m

EDGES0 = [[0, 1, 10], [0, 2, 1], [1, 2, 2]]
MM, N0 = 6, 3
POS = {0: (0.08, 0.5), 1: (0.86, 0.12), 2: (0.86, 0.9)}
EDGE_FOR = 28    # for u, v, w in edges
EDGE_ADD = (30, 32)   # res += w / res += min(...)


def _phase1(S):
    return 'heap' in S and 'res' not in S


def _fd(v):
    return f'>{MM}' if v > MM else v


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    dis = S.get('dis')
    line = S.get('_line')
    p1 = _phase1(S)
    inloop = 'res' in S and 'u' in S and line is not None and line >= EDGE_FOR
    cur = None
    if inloop:
        for k, (a, b, c) in enumerate(EDGES0):
            if (a, b) == (S['u'], S['v']):
                cur = k
    done = line == 34
    cv.text((x0 + 18, y0 + 4), '细分图：边上的点 = 细分点（绿 = 走得到）；圆 = 原节点，旁边是 dis', 20, T['muted'], bold=True)
    R = 32
    Lx, Rx, Tp, Bt = x0 + 70, x1 - 90, y0 + 80, y1 - 70
    P = {u: (Lx + fx * (Rx - Lx), Tp + fy * (Bt - Tp)) for u, (fx, fy) in POS.items()}
    for k, (u, v, cnt) in enumerate(EDGES0):
        a, b = P[u], P[v]
        d = _m.hypot(b[0] - a[0], b[1] - a[1])
        ux, uy = (b[0] - a[0]) / d, (b[1] - a[1]) / d
        shaded = done or (cur is not None and (k < cur or (k == cur and line in EDGE_ADD)))
        hot = inloop and cur == k and line not in EDGE_ADD and line != 34
        cv.line([(a[0] + ux * R, a[1] + uy * R), (b[0] - ux * R, b[1] - uy * R)], T['yellow'] if hot else T['border'], 5 if hot else 3)
        off = 26 + 44 * abs(uy)
        mx, my = (a[0] + b[0]) / 2 - uy * off, (a[1] + b[1]) / 2 + ux * off
        cv.text((mx, my), f'w={cnt}', 22, T['yellow'] if hot else T['muted'], anchor='mm', bold=True, mono=True)
        for i in range(1, cnt + 1):
            f = i / (cnt + 1)
            px, py = a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
            ok = False
            if dis is not None:
                ra = max(MM - dis[u], 0)
                rb = max(MM - dis[v], 0)
                ok = i <= ra or (cnt + 1 - i) <= rb
            col = T['green'] if (shaded and ok) else (T['dim'] if shaded else T['panel2'])
            cv.d.ellipse((px - 8, py - 8, px + 8, py + 8), fill=col, outline=T['border'])
    for u, (px, py) in P.items():
        du = dis[u] if dis is not None else None
        if p1 and S.get('now') == u and 'now_dis' in S:
            fill = T['blue']
        elif du is not None and du <= MM and (not p1 or u in (S.get('used') or ())):
            fill = T['green']
        else:
            fill = T['panel2']
        cv.d.ellipse((px - R, py - R, px + R, py + R), fill=fill, outline=T['border'], width=2)
        cv.text((px, py), u, 28, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)
        if du is not None:
            if u == 0:
                cv.text((px, py + R + 22), f'dis={_fd(du)}', 20, T['yellow'], anchor='mm', bold=True, mono=True)
            else:
                cv.text((px + R + 10, py), f'dis={_fd(du)}', 20, T['yellow'], anchor='lm', bold=True, mono=True)


def _txt(S, B):
    line = S.get('_line')
    if _phase1(S):
        return f'Dijkstra：边长 = 细分点数 + 1；堆顶距离 `> maxMoves = {MM}` 就停（`dis` 初值 `maxMoves + 1` = 没到）'
    if 'res' in S and 'u' in S and line is not None and line >= EDGE_FOR and line != 34:
        return f"边 `({S['u']}, {S['v']}, w={S['w']})`：两端 `dis` 分别是 `{S['dis'][S['u']]}`、`{S['dis'][S['v']]}`，能从两头走进多少个细分点？"
    return f'从 0 出发，最多走 `maxMoves = {MM}` 步；先数原节点，再数每条边上走得到的细分点'


def _edge_cap(S, B, r):
    u, v, w = S.u, S.v, S.w
    lo = min(S.dis[u], S.dis[v])
    if MM - lo >= w:
        return f'`maxMoves - min(dis[u], dis[v]) = {MM - lo} >= w = {w}`：一端能走完整条边 → 细分点全到，`res += {w}`'
    return f'`maxMoves - min(dis) = {MM - lo} < w = {w}`：走不完整条边 → 两头各走一段：`{MM - S.dis[u]} + {MM - S.dis[v]}` 与 `{w}` 取小'


CONFIG = dict(
    num=882, title='细分图中的可到达结点', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='Dijkstra + 分情况数细分点',
    tags=['灵神题单·图论算法', '难度分 2328'],
    code='''
class Solution(object):
    def reachableNodes(self, edges, maxMoves, n):
        
        g = {index : {} for index in range(n)}
        for u, v, w in edges:
            g[u][v] = w + 1
            g[v][u] = w + 1
        
        dis = [maxMoves + 1] * n
        heap = [[0, 0]]
        used = set()
        while heap and heap[0][0] <= maxMoves:
            now_dis, now = heapq.heappop(heap)
            if now not in used:
                used.add(now)
                dis[now] = now_dis
                for next in g[now]:
                    if next not in used:
                        heapq.heappush(heap, [g[now][next] + now_dis, next])
        
        res = 0
        for index in range(n):
            if dis[index] <= maxMoves:
               res += 1
            else:
                dis[index] = maxMoves

        for u, v, w in edges:
            if maxMoves - min(dis[u], dis[v]) >= w:
                res += w
            else:
                res += min(maxMoves - dis[u] + maxMoves - dis[v], w)
        
        return res
''',
    call=f'Solution().reachableNodes({EDGES0}, {MM}, {N0})',
    expect=13,
    max_steps=66,
    skip=[4, 5, 6, 7],
    views=[
        dict(type='text', fn=_txt, h=44, size=22),
        dict(type='custom', draw=_draw, h=360),
        dict(type='array', var='dis', label='dis[i]：0 到原节点 i 的最短路（maxMoves+1 = 还没到）', h=140, cell=80),
        dict(type='heap', var=lambda S: S.get('heap'), label='heap（最小堆，元素 = [距离, 节点]）', h=100, fmt=lambda t: f'({t[0]},{t[1]})'),
    ],
    watch=[('now_dis', 'now_dis', 'blue'), ('now', 'now', 'blue'), ('next', 'next', 'yellow'), ('res', 'res', 'green'), ('index', 'index'), ('w', 'w', 'orange')],
    captions={
        'dis = [maxMoves + 1]': '`dis` 初值 `maxMoves + 1`：表示「在 maxMoves 内到不了」',
        'heap = [[0, 0]]': '起点 `[0, 0]` 入堆',
        'used = set()': '`used`：已经确定最短路的节点',
        'while heap and': lambda S, B, r: f'堆顶距离 `{S.heap[0][0]} <= maxMoves = {S.maxMoves}`，继续' if (S.heap and S.heap[0][0] <= S.maxMoves) else '堆空，或堆顶距离已经 `> maxMoves`：再远也走不到，停',
        'heappop': '弹出最近的 `now = {now}`，距离 `{now_dis}`',
        'if now not in used': lambda S, B, r: f'`{S.now}` 第一次出堆' if S.now not in S.used else f'`{S.now}` 已确定过，旧记录，跳过',
        'used.add': '`{now}` 的最短路确定了',
        'dis[now] = now_dis': '`dis[{now}] = {now_dis}`',
        'for next in g[now]': lambda S, B, r: f'`{S.now}` 的邻居都看完了' if ('next' in B and B.next == S.next and B.now == S.now) else f'看邻居 `{S.next}`，边长 `{S.g[S.now][S.next]}`',
        'if next not in used': lambda S, B, r: f'`{S.next}` 已确定，不再入堆' if S.next in S.used else f'`{S.next}` 还没确定 → 入堆候选',
        'heapq.heappush': '`[{g[now][next]} + {now_dis}, {next}]` = `[{g[now][next] + now_dis}, {next}]` 入堆',
        'res = 0': '原节点算完最短路。下面先数原节点，再数每条边上的细分点',
        'for index in range(n)': lambda S, B, r: '原节点都检查完了' if ('index' in B and B.index == S.index) else f'检查原节点 `{S.index}`：`dis = {S.dis[S.index]}`',
        'if dis[index] <= maxMoves': lambda S, B, r: f'`dis[{S.index}] = {S.dis[S.index]} <= {S.maxMoves}` → ==到得了==' if S.dis[S.index] <= S.maxMoves else f'`dis[{S.index}] = {S.dis[S.index]} > {S.maxMoves}` → 到不了',
        'res += 1': '到得了的原节点计 1 个：`res = {res}`',
        'dis[index] = maxMoves': '到不了的把 `dis` 改成 `maxMoves`：后面算「剩余步数」就是 0',
        EDGE_FOR: lambda S, B, r: '所有边都数完了' if ('u' in B and 'res' in B and B.u == S.u and B.v == S.v and B.res == S.res) else f'取边 `({S.u}, {S.v}, w={S.w})`',
        'if maxMoves - min(dis[u], dis[v]) >= w': _edge_cap,
        'res += w': '这条边的 `{w}` 个细分点全都走得到：`res = {res}`',
        'res += min': lambda S, B, r: f'两头各走一段：`{S.maxMoves - S.dis[S.u]} + {S.maxMoves - S.dis[S.v]}`，可能重叠，不会超过 `w = {S.w}` → 加 `min(…, {S.w})`，`res = {S.res}`',
        'return res': '可到达结点总数 =={ret}==',
    },
    cards=dict(
        one_liner='原节点的最短路 + 按两端剩余步数讨论每条边',
        complexity='时间 `O(n + m log m)`，空间 `O(n + m)`',
        problem=['无向图 `n` 个节点；边 `[u, v, w]` 被细分成 `w` 个新节点',
                 '从 0 出发走不超过 `maxMoves` 步能到的结点（含细分点）有几个',
                 '示例：`edges=[[0,1,10],[0,2,1],[1,2,2]]`，`maxMoves=6`，`n=3` → `13`'],
        quote='可以将细分边的细分节点数量视为边长，那么此时执行一次单源最短路就可以得到从0出发到达图中原始节点的移动次数。……细分点要么是从0开始走到u，然后再走到细分点，要么就是从0开始走到v。',
        quote_src='—— yiduobo 题解',
        idea=['先把「细分点数 + 1」当边长，原节点跑一遍带堆 Dijkstra',
              '边 `[u, v, w]` 上的细分点只能从 `u` 或 `v` 走进来，按 `maxMoves` 与 `dis` 的大小关系讨论',
              '一端走得完整条边 → 全加 `w`；否则两头各走一段，之和不超过 `w`'],
        summary=['时间 `O(n + m log m)`，堆里用 `[距离, 节点]`',
                 '易错：`dis` 超过 `maxMoves` 的要改成 `maxMoves`，否则剩余步数会算成负数',
                 '两头各走一段可能重叠，所以最后还要和 `w` 取小',
                 '代码原文已是 Python 3 可运行写法，无需修改',
                 '对比灵神：他用 `max(maxMoves - dist, 0)` 统一处理，这里分情况讨论'],
    ),
)
