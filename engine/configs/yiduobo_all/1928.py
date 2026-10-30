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

N = 6
MAXT = 30
EDGES = [[0, 1, 10], [1, 2, 10], [2, 5, 10], [0, 3, 1], [3, 4, 10], [4, 5, 15]]
FEES = [5, 1, 2, 20, 20, 3]
POS = [(0.0, 0.5), (0.25, 0.0), (0.65, 0.0), (0.25, 1.0), (0.65, 1.0), (1.0, 0.5)]

CODE = '''
class Solution(object):
    def minCost(self, maxTime, edges, passingFees):

        n = len(passingFees)
        cost = [-1] * n
        heap = [[0, 0, passingFees[0]]]
        g = {x : {} for x in range(n)}
        for x, y, t in edges:
            if t <= maxTime:
                if y not in g[x]:
                    g[x][y] = g[y][x] = t
                else:
                    g[x][y] = min(g[x][y], t)
                    g[y][x] = min(g[y][x], t)

        while heap:
            t, now, c = heapq.heappop(heap)
            if cost[now] != -1 and c >= cost[now]:
                continue
            
            cost[now] = c

            for next in g[now]:
                if t + g[now][next] <= maxTime and ((cost[next] == -1) or (c + passingFees[next] < cost[next])):
                    heapq.heappush(heap, [t + g[now][next], next, c + passingFees[next]])

        return cost[-1]
'''
_L = CODE.split('\n')
_IF = next(i for i, l in enumerate(_L) if 'if t + g[now][next]' in l)
_PUSH = next(i for i, l in enumerate(_L) if 'heapq.heappush' in l)


def _ncol(S, T):
    cost = S.get('cost')
    ln = S.get('_line', 0)
    now, nx = S.get('now'), S.get('next')
    popped = 'now' in S and ln >= _IF - 8

    def f(i):
        if popped and now == i and ln < _IF + 5 and ln > 15:
            return T['pink']
        if popped and nx == i and ln in (_IF, _PUSH):
            return T['blue']
        if cost is not None and cost[i] != -1:
            return T['green'] if i == N - 1 and ln > _PUSH + 1 else None
        return None
    return f


def _draw(cv, S, B, box, T):
    cost = S.get('cost')
    ln = S.get('_line', 0)
    now, nx = S.get('now'), S.get('next')
    act = ln in (_IF, _PUSH) and now is not None and nx is not None

    def ecol(k):
        u, v, w = EDGES[k]
        if act and {u, v} == {now, nx}:
            return (T['yellow'], 7)
        return None

    def elab(k):
        return str(EDGES[k][2])

    def nlab(i):
        out = [(f'费{FEES[i]}', T['muted'])]
        if cost is not None:
            out.append((f'cost={"?" if cost[i] == -1 else cost[i]}', T['green']))
        return out
    _gdraw(cv, box, T, POS, EDGES, ncol=_ncol(S, T), nlab=nlab, ecol=ecol, elab=elab, r=30,
           title=f'边上数字 = 通行分钟，费 = 经过该城市的费用　maxTime = {MAXT}')


def _fx(S):
    if 'now' not in S or 't' not in S:
        return '堆里的元素是 `[用时 t, 城市, 花费 c]`，每次取用时最少的'
    return f"当前：用时 `{S['t']}` / {MAXT}，花费 `{S['c']}`，在城市 `{S['now']}`"


CONFIG = dict(
    num=1928, title='规定时间内到达终点的最小花费', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='按时间出堆的 Dijkstra · 记录最小花费',
    tags=['动态规划'],
    code=CODE,
    call=f'Solution().minCost({MAXT}, {EDGES}, {FEES})',
    expect=11,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='heap', var='heap', fmt=lambda p: f'城{p[1]} t{p[0]} 费{p[2]}', label='heap（城市 用时 花费）', top_color='purple', h=100),
        dict(type='text', fn=_fx, size=24),
    ],
    watch=[('t', 't', 'purple'), ('now', 'now', 'pink'), ('c', 'c', 'orange'), ('next', 'next', 'blue'),
           ('cost[-1]', lambda S: S['cost'][-1] if 'cost' in S else None, 'green')],
    skip=['n = len(passingFees)', 'g = {x', 'for x, y, t in edges', 'if t <= maxTime', 'if y not in g[x]', 'g[x][y] = g[y][x] = t',
          'g[x][y] = min', 'g[y][x] = min', 'while heap', 'for next in g[now]', 'continue'],
    captions={
        'cost = [-1] * n': '`cost[i]`：到达城市 i 目前已知的最小花费，`-1` 表示还没到过（花费 = 路过的每个城市费用之和，包括起点和终点）',
        'heap = [[0, 0, passingFees[0]]]': '起点：用时 0，在城市 0，花费就是起点的费 `{passingFees[0]}`',
        't, now, c = heapq.heappop(heap)': '弹出==用时最少==的状态：用时 `{t}`，城市 `{now}`，花费 `{c}`（时间只会增加，所以按时间从小到大处理）',
        'if cost[now] != -1 and c >= cost[now]': lambda S, B, r: (
            f'城市 `{S.now}` 以前到过，花费 `{S.cost[S.now]}`；这次花费 `{S.c}` 不比它少 → 更慢又更贵，==丢弃==' if S.cost[S.now] != -1 and S.c >= S.cost[S.now]
            else (f'城市 `{S.now}` 第一次到' if S.cost[S.now] == -1 else f'城市 `{S.now}` 以前花费 `{S.cost[S.now]}`，这次 `{S.c}` 更少 → 虽然更晚到，但更便宜，值得保留')),
        'cost[now] = c': '记下：到城市 `{now}` 的最小花费 `cost[{now}] = {c}`',
        'if t + g[now][next] <= maxTime': lambda S, B, r: (
            f'去邻居 `{S.next}`：用时 `{S.t} + {S.g[S.now][S.next]} = {S.t + S.g[S.now][S.next]}`，' + (
                '超过 maxTime → 不能走' if S.t + S.g[S.now][S.next] > S.maxTime else (
                    f'没超时；花费 `{S.c} + {S.passingFees[S.next]} = {S.c + S.passingFees[S.next]}`，' + (
                        '这个城市还没到过 → 值得入堆' if S.cost[S.next] == -1 else (
                            f'比已知的 `{S.cost[S.next]}` 少 → 值得入堆' if S.c + S.passingFees[S.next] < S.cost[S.next]
                            else f'不比已知的 `{S.cost[S.next]}` 少 → 更晚又更贵，不入堆'))))),
        'heapq.heappush': '入堆：`[用时 {t + g[now][next]}, 城市 {next}, 花费 {c + passingFees[next]}]`',
        'return cost[-1]': '终点（最后一个城市）的最小花费 =={ret}==',
    },
    max_steps=120,
    cards=dict(
        one_liner='用时间当“距离”出堆，同一城市只保留更便宜的到达方式',
        complexity='时间 `O(m log m)`（状态数受剪枝限制），空间 `O(n + m)`',
        problem=['无向图，边有通行时间；每经过一个城市要付该城市的费用（起点终点也算）',
                 '从 0 出发，在 `maxTime` 分钟内到达 `n-1`，求最小总花费，到不了返回 `-1`',
                 '本视频：`maxTime=30`，6 个城市 → ==11=='],
        quote='为了保证时间是从小到大计算的，那么可以使用类似dijkstra + SPFA的做法来进行状态转移：每次都对距离最近的点计算f，为了满足最近这个需求，自然是使用一个堆来维护当前可计算的节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想 DP：`f[i][j]` = 在时刻 i 恰好到城市 j 的最小花费，按时间 i 从小到大算',
              '边权为正 → 转移只会从更小的时间来 → 可以省掉时间这一维',
              '用堆按时间取点；堆顶花费比 `cost` 更少才更新邻居，再入堆'],
        summary=['堆里存 `[用时, 城市, 花费]`，用时小的先出',
                 '==时间和花费两个因素==：更晚到达的状态只有花费更少才有价值',
                 '重边取最小时间；`t > maxTime` 的边直接不要',
                 '花费包含起点，所以初始就是 `passingFees[0]`',
                 '原文是 Python 2 风格，但无需改动即可运行（用到的 heapq 已预置）'],
    ),
)
