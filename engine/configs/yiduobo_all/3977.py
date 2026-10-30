import math as _m


def _graph(cv, T, box, pos, edges, ncol, nsub, ecol, title, directed=True, R=30):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    L, Rr, Tp, Bt = x0 + 70, x1 - 70, y0 + 60 + R, y1 - R - 34
    P = {u: (L + fx * (Rr - L), Tp + fy * (Bt - Tp)) for u, (fx, fy) in pos.items()}
    for u, v, w in edges:
        c, wd = ecol(u, v)
        (ax, ay), (bx, by) = P[u], P[v]
        dd = _m.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / dd, (by - ay) / dd
        if directed:
            cv.arrow((ax + ux * R, ay + uy * R), (bx - ux * (R + 2), by - uy * (R + 2)), c, wd, 16)
        else:
            cv.line([(ax + ux * R, ay + uy * R), (bx - ux * R, by - uy * R)], c, wd)
        mx, my = (ax + bx) / 2 - uy * 20, (ay + by) / 2 + ux * 20
        cv.rect((mx - 17, my - 15, mx + 17, my + 15), fill=T['bg'], r=6)
        cv.text((mx, my), w, 22, c if c != T['dim'] else T['muted'], anchor='mm', bold=True, mono=True)
    for u in pos:
        px, py = P[u]
        fc = ncol(u)
        cv.d.ellipse((px - R, py - R, px + R, py + R), fill=fc, outline=T['border'], width=2)
        cv.text((px, py), u, 28, T['bg'] if fc != T['panel2'] else T['text'], anchor='mm', bold=True)
        s = nsub(u)
        if s is not None:
            if py < (Tp + Bt) / 2 - 5:
                cv.text((px, py - R - 4), s, 20, T['yellow'], anchor='mb', bold=True, mono=True)
            else:
                cv.text((px, py + R + 4), s, 20, T['yellow'], anchor='mt', bold=True, mono=True)

N = 4
EDGES = [(0, 1, 1), (0, 2, 2), (1, 3, 2), (2, 3, 1)]
POWER = 5
COST = [1, 2, 1, 1]
POS = {0: (0.0, 0.5), 1: (0.5, 0.0), 2: (0.5, 1.0), 3: (1.0, 0.5)}

CODE = '''
class Solution(object):
    def minTimeMaxPower(self, n, edges, power, cost, source, target):

        g = [[] for _ in range(n)]
        for x, y, w in edges:
            g[x].append((y, w))

        dis = [[None] * (power + 1) for _ in range(n)]
        heap = [(0, source, power)]

        best_dis = -1
        best_power = -1

        while heap:
            d, x, p = heapq.heappop(heap)
            if best_dis != -1 and d > best_dis or (d == best_dis and p <= best_power):
                continue

            if dis[x][p] is None:
                dis[x][p] = d
                if x == target:
                    best_dis = d
                    best_power = p
                    continue

                if p < cost[x]:
                    continue

                p -= cost[x]

                for y, w in g[x]:
                    if dis[y][p] is None:
                        heapq.heappush(heap, (d + w, y, p))

        return [best_dis, best_power]
'''
_L = CODE.strip('\n').split('\n')
WHILE_LINE = next(i + 1 for i, l in enumerate(_L) if 'while heap' in l)
FOR_LINE = next(i + 1 for i, l in enumerate(_L) if 'for y, w in g[x]' in l)
POP_LINE = next(i + 1 for i, l in enumerate(_L) if 'heappop' in l)
RET_LINE = next(i + 1 for i, l in enumerate(_L) if 'return [best' in l)


def _live(S):
    return (S.get('_line') or 0) > POP_LINE - 0 and 'p' in S and 'd' in S and 'x' in S


def _draw(cv, S, B, box, T):
    line = S.get('_line') or 0
    live = line >= POP_LINE and 'p' in S and 'x' in S and 'd' in S
    x = S['x'] if live else None
    y = S['y'] if live and line >= FOR_LINE else None
    dis = S.get('dis')
    bp = S.get('best_power', -1)

    def ncol(u):
        if u == x:
            return T['blue']
        if u == TARGET_NODE and bp >= 0:
            return T['green']
        if dis is not None and any(v is not None for v in dis[u]):
            return T['orange']
        return T['panel2']

    def nsub(u):
        if dis is None:
            return None
        s = ' '.join(f'{v}@{r}' for r, v in enumerate(dis[u]) if v is not None)
        return s or None

    def ecol(u, v):
        if y is not None and (u, v) == (x, y):
            return T['yellow'], 6
        return T['dim'], 3

    _graph(cv, T, box, POS, EDGES, ncol, nsub, ecol,
           '黄字 = 已确定的 (最短时间@剩余电量)；蓝 = 当前出堆；绿 = 终点已有答案', directed=True)


TARGET_NODE = 3


def _text(S, B):
    line = S.get('_line') or 0
    if line <= WHILE_LINE or 'p' not in S or 'x' not in S or 'd' not in S:
        return '把 `p`（剩余电量）塞进状态，不真的建图：堆里存 `(时间, 节点, 电量)`'
    bd, bp = S.get('best_dis', -1), S.get('best_power', -1)
    base = f"当前状态：节点 `{S['x']}`，电量 `{S['p']}`，用时 `{S['d']}`"
    if bd != -1:
        base += f'；已有答案 ==({bd}, 电量 {bp})=='
    return base


def _filter(S, B, r):
    bd, bp = S.best_dis, S.best_power
    if bd != -1 and S.d > bd:
        return f'已有答案时间 `{bd}`，而 `d = {S.d}` 更久 → ==不可能更优，丢弃=='
    if S.d == bd and S.p <= bp:
        return f'时间同为 `{bd}`，但电量 `{S.p} <= {bp}` 没有更多 → ==丢弃=='
    if bd == -1:
        return '还没有答案（`best_dis = -1`）→ 继续处理这个状态'
    return f'时间 `{S.d} == {bd}` 且电量 `{S.p} > {bp}` → ==同样快、电量更大==，继续处理'


def _first(S, B, r):
    if S.dis[S.x][S.p] is None:
        return f'`dis[{S.x}][{S.p}]` 还是空 → ==这个状态第一次出堆，时间 {S.d} 就是它的最短路=='
    return f'`dis[{S.x}][{S.p}] = {S.dis[S.x][S.p]}` 已经定下来了 → 旧记录，跳过'


def _edge(S, B, r):
    if S.dis[S.y][S.p] is None:
        return f'`dis[{S.y}][{S.p}]` 还没确定 → 值得入堆'
    return f'`dis[{S.y}][{S.p}] = {S.dis[S.y][S.p]}` 已确定 → 不再入堆'


CONFIG = dict(
    num=3977, title='有限电量到达目标节点的最少时间', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='分层图 Dijkstra',
    tags=['灵神题单·图论算法', '灵神题单·动态规划', '难度分 2103'],
    code=CODE,
    call=f'Solution().minTimeMaxPower({N}, {[list(e) for e in EDGES]}, {POWER}, {COST}, 0, 3)',
    expect=[3, 3],
    skip=['for x, y, w in edges', 'g[x].append', 'best_dis = -1', 'best_power = -1'],
    max_steps=90,
    views=[
        dict(type='text', fn=_text, h=56, size=24),
        dict(type='custom', draw=_draw, h=340),
        dict(type='grid', var='dis', rows=list(range(N)), cols=list(range(POWER + 1)), h=260, cell=64,
             label='dis[节点][剩余电量]（行 = 节点，列 = 电量）',
             color=lambda S, i, j, v: 'blue' if S.get('_line', 0) >= POP_LINE and 'x' in S and 'p' in S and 'd' in S and v is not None and (i, j) == (S['x'], S['p']) and S.get('_line') < FOR_LINE else None),
        dict(type='heap', var='heap', label='heap：(时间, 节点, 电量)', h=110, fmt=lambda t: f'({t[0]},{t[1]},{t[2]})'),
    ],
    watch=[('d', 'd', 'blue'), ('x', 'x', 'blue'), ('p', 'p', 'cyan'), ('best_dis', 'best_dis', 'green'), ('best_power', 'best_power', 'green')],
    captions={
        'g = [[] for': '有向图：邻接表 `g[x]` 存 `(终点, 耗时)`',
        'dis = [[None]': '`dis[x][p]`：第 p 层（剩余电量 p）里节点 x 的最短时间，`None` = 还没确定',
        'heap = [(0, source, power)]': '从第 `{power}` 层的起点出发：`(时间 0, 节点 {source}, 电量 {power})`',
        'while heap': lambda S, B, r: '堆非空，继续取最小的状态' if S.heap else '堆空了：答案就是 `best_*`（没找到就是 -1）',
        'heapq.heappop': '弹出时间最小的状态：节点 `{x}`，电量 `{p}`，时间 `{d}`',
        'if best_dis != -1 and': _filter,
        'continue': lambda S, B, r: ('终点已记录，不再往后扩展' if S.x == S.target and S.best_power == S.p and S.dis[S.x][S.p] == S.d else (f'电量 `{S.p}` 不够从 `{S.x}` 出发（需要 `{S.cost[S.x]}`）→ 这条路走不下去' if S.p < S.cost[S.x] else '丢弃这个状态')),
        'if dis[x][p] is None': _first,
        'dis[x][p] = d': '记下 `dis[{x}][{p}]` = =={d}==',
        'if x == target': lambda S, B, r: f'`x = {S.x}`，终点是 `{S.target}`：' + ('==到终点了==' if S.x == S.target else '还没到'),
        'best_dis = d': '终点记录：最短时间 `best_dis` = =={best_dis}==',
        'best_power = p': '同时记下此刻电量 `best_power` = =={best_power}==（同样快时取电量更大的）',
        'if p < cost[x]': lambda S, B, r: (f'`{S.p} < cost[{S.x}] = {S.cost[S.x]}` → 成立：==电量不够转发==' if S.p < S.cost[S.x] else f'`{S.p} < cost[{S.x}] = {S.cost[S.x]}` → 不成立：电量够转发，继续'),
        'p -= cost[x]': '离开节点 `{x}`：电量 `{B.p} - {cost[x]}` = =={p}==（下一层）',
        'for y, w in g[x]': lambda S, B, r: (f'`{S.x}` 的出边都看完了' if 'y' in B and (B.x, B.y, B.w) == (S.x, S.y, S.w) else f'看出边 `{S.x}→{S.y}`，耗时 `{S.w}`'),
        'if dis[y][p] is None': _edge,
        'heapq.heappush': '`({d} + {w}, {y}, {p})` 入堆：到 `{y}` 的新状态，时间 =={d + w}==',
        'return [best_dis': '返回 `[{best_dis}, {best_power}]`：==最短时间，以及这个时间下最大的剩余电量==',
    },
    cards=dict(
        one_liner='原图复制 power+1 层，第 p 层表示剩余电量 p，跑 Dijkstra',
        complexity='时间 `O(nk + mk log(mk))`，空间 `O(nk)`，`k = power`',
        problem=['有向带权图，带 `power` 电量出发，离开节点 `u` 要花 `cost[u]` 电量',
                 '求到 `target` 的最短时间，以及最短时间下可能剩余的最大电量',
                 '本视频：4 个点，`power = 5`，两条路都用 3 分钟，电量一条剩 2、一条剩 3'],
        quote='从题目的数据规模来看，分层图的dijkstra是非常适合的。具体来说，将原图复制power + 1份，第p层表示当前剩余电量为p。',
        quote_src='—— yiduobo 题解原文',
        idea=['边 `u→v`：第 `p` 层的 u 连到第 `p - cost[u]` 层的 v',
              '不真建图：把电量 `p` 放进堆元素就行',
              '终点可能在不同层出堆：同样快时，==选层数最高（电量最大）的=='],
        summary=['时间 `O(nk + mk log(mk))`，状态数 `n × (power+1)`',
                 '和灵神不同：这里堆不管电量大小，用 `best_dis / best_power` 在终点上取舍',
                 '时间相同的终点状态要继续看：电量更大的才更新答案',
                 '易错：`p -= cost[x]` 要先判断 `p < cost[x]`，再扣电量'],
    ),
)
