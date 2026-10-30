import math as _m

START, TARGET = (1, 1), (10, 4)
ROADS = [[1, 2, 4, 2, 1], [4, 3, 7, 4, 1], [7, 4, 9, 4, 1], [2, 4, 6, 1, 5]]


def _fn(v):
    return '∞' if (isinstance(v, float) and _m.isinf(v)) else str(v)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    dis = S.get('dis') or {}
    vis = S.get('vis') or set()
    v = S.get('v')
    line = S.get('_line', 0)
    cv.text((x0 + 18, y0 + 4), '粉 = 当前点 v　黄 = 已有距离　绿 = 已确定　方块 = 特殊路起点', 22, T['muted'], bold=True)
    ax0, ax1, ay0, ay1 = x0 + 70, x1 - 70, y0 + 90, y1 - 70

    def P(p):
        return (ax0 + (p[0] - 0.5) / 10 * (ax1 - ax0), ay1 - (p[1] - 0.5) / 4 * (ay1 - ay0))
    for gx in range(1, 11):
        X, _ = P((gx, 1))
        cv.line([(X, ay0), (X, ay1)], (34, 40, 50), 1)
        cv.text((X, ay1 + 8), gx, 18, T['dim'], anchor='mt', mono=True)
    for gy in range(1, 5):
        _, Y = P((1, gy))
        cv.line([(ax0, Y), (ax1, Y)], (34, 40, 50), 1)
        cv.text((ax0 - 12, Y), gy, 18, T['dim'], anchor='rm', mono=True)
    cur = None
    if 'x1' in S and line in (17, 18):
        cur = (S['x1'], S['y1'], S['x2'], S['y2'])
    # 曼哈顿走法（虚线）
    if v is not None and line in (15, 17, 18):
        tgt = TARGET if line == 15 else (cur[0], cur[1]) if cur else None
        if tgt:
            a, b = P(v), P(tgt)
            c = T['yellow']
            cv.dashed(a, (b[0], a[1]), c, 3)
            cv.dashed((b[0], a[1]), b, c, 3)
    for k, (a1, b1, a2, b2, cost) in enumerate(ROADS):
        pa, pb = P((a1, b1)), P((a2, b2))
        hot = cur == (a1, b1, a2, b2)
        c = T['yellow'] if hot else T['muted']
        L = _m.hypot(pb[0] - pa[0], pb[1] - pa[1]) or 1
        ux, uy = (pb[0] - pa[0]) / L, (pb[1] - pa[1]) / L
        cv.arrow((pa[0] + ux * 16, pa[1] + uy * 16), (pb[0] - ux * 22, pb[1] - uy * 22), c, 6 if hot else 3, head=16)
        mx, my = pa[0] + (pb[0] - pa[0]) * 0.3, pa[1] + (pb[1] - pa[1]) * 0.3
        cv.rect((mx - 20, my - 15, mx + 20, my + 15), fill=T['panel'], r=8)
        cv.text((mx, my), cost, 22, c, anchor='mm', bold=True)
    pts = {tuple(START), tuple(TARGET)} | {(r[2], r[3]) for r in ROADS}
    for r in ROADS:
        if (r[0], r[1]) not in pts:
            X, Y = P((r[0], r[1]))
            cv.rect((X - 9, Y - 9, X + 9, Y + 9), fill=T['panel2'], outline=T['muted'], width=2)
            cv.text((X + 14, Y + 4), f'({r[0]},{r[1]})', 18, T['dim'], anchor='lt', mono=True)
    for p in sorted(pts):
        X, Y = P(p)
        col = T['panel2']
        if p == v:
            col = T['pink']
        elif p in vis:
            col = T['green']
        elif p in dis and not (isinstance(dis[p], float) and _m.isinf(dis[p])):
            col = T['yellow']
        cv.d.ellipse((X - 17, Y - 17, X + 17, Y + 17), fill=col, outline=T['border'], width=3)
        nm = 'S' if p == tuple(START) else 'T' if p == tuple(TARGET) else ''
        if nm:
            cv.text((X, Y), nm, 22, T['bg'] if col != T['panel2'] else T['text'], anchor='mm', bold=True)
        d = dis.get(p) if p in dis else None
        if d is not None:
            cv.text((X, Y - 24), f'dis={_fn(d)}', 20, T['cyan'], anchor='mb', bold=True, mono=True)
            cv.text((X, Y - 44), f'({p[0]},{p[1]})', 17, T['dim'], anchor='mb', mono=True)
        else:
            cv.text((X, Y - 24), f'({p[0]},{p[1]})', 17, T['dim'], anchor='mb', mono=True)


CONFIG = dict(
    num=2662, title='前往目标的最小代价', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='朴素 Dijkstra（稠密图）',
    tags=['难度分 2154'],
    code='''
class Solution:
    def minimumCost(self, start: List[int], target: List[int], specialRoads: List[List[int]]) -> int:
        t = tuple(target)
        dis = defaultdict(lambda: inf)
        dis[tuple(start)] = 0
        vis = set()
        while True:
            v, dv = None, -1
            for p, d in dis.items():
                if p not in vis and (dv < 0 or d < dv):
                    v, dv = p, d
            if v == t: return dv  # 到终点的最短路已确定
            vis.add(v)
            vx, vy = v
            dis[t] = min(dis[t], dv + t[0] - vx + t[1] - vy)  # 更新到终点的最短路
            for x1, y1, x2, y2, cost in specialRoads:
                w = (x2, y2)
                dis[w] = min(dis[w], dv + abs(x1 - vx) + abs(y1 - vy) + cost)
''',
    call=f'Solution().minimumCost({list(START)}, {list(TARGET)}, {ROADS})',
    expect=6,
    views=[
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=[('v', 'v', 'pink'), ('dv', 'dv', 'cyan'), ('dis[t]', lambda S: S['dis'][S['t']] if 'dis' in S and S['t'] in S['dis'] else None, 'green')],
    skip=['t = tuple(target)', 'dis[tuple(start)] = 0', 'vis = set()', 'while True', 'v, dv = None, -1', 'for p, d in dis.items()',
          'if p not in vis', 'v, dv = p, d', 'vx, vy = v', 'for x1, y1, x2, y2, cost', 'w = (x2, y2)'],
    captions={
        'dis = defaultdict': '`dis[点]`：从起点到该点的最短代价，默认 ∞。图上的点 = 起点、终点、所有特殊路的终点',
        'if v == t': lambda S, B, r: (f'在没确定的点里取 `dis` 最小的：`v = {S.v}`，代价 =={S.dv}==' + ('。它就是终点 → ==最短路确定，直接返回==' if S.v == S.t else '，它的最短路已经定了')),
        'vis.add(v)': '标记 `{v}` 已确定，不再重复处理',
        'dis[t] = min': lambda S, B, r: (lambda old, new: f'从 `{S.v}` 直接走曼哈顿到终点：`{S.dv} + {S.t[0] - S.vx} + {S.t[1] - S.vy}` = {new}，`dis[t]` 取 min({_fn(old)}, {new}) = =={S.dis[S.t]}==')(B.dis.get(S.t, float('inf')), S.dv + S.t[0] - S.vx + S.t[1] - S.vy),
        'dis[w] = min': lambda S, B, r: (lambda old, new: f'先走到特殊路起点 `({S.x1},{S.y1})` 花 `{abs(S.x1 - S.vx) + abs(S.y1 - S.vy)}`，再坐车 `{S.cost}`：到 `{S.w}` = {new}；`dis` 取 min({_fn(old)}, {new}) = =={S.dis[S.w]}==')(B.dis.get(S.w, float('inf')), S.dv + abs(S.x1 - S.vx) + abs(S.y1 - S.vy) + S.cost),
        'return dv': '到终点的最小代价 =={ret}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='只有起点、终点和特殊路终点值得走：把它们当点跑朴素 Dijkstra',
        complexity='时间 `O(n²)`，空间 `O(n)`（`n` 为特殊路数量）',
        problem=['二维平面上，普通移动的代价是曼哈顿距离 `|x2−x1| + |y2−y1|`',
                 '另有若干条==单向特殊路==，可以从 `(x1,y1)` 以代价 `cost` 直达 `(x2,y2)`，可用任意次',
                 '求 `start` 到 `target` 的最小代价；本视频：连用三条特殊路，答案 `6`'],
        quote='把起点、终点和所有特殊路径的终点看成是图上的点。……由于图是稠密图，所以用朴素 Dijkstra 求最短路。',
        quote_src='—— 灵茶山艾府题解',
        idea=['点只有三类：起点、终点、特殊路终点；到特殊路终点只需考虑“走到起点再坐车”',
              '连续的曼哈顿走法可以合并成一次，所以每次只要更新终点和各特殊路终点',
              '每轮取未确定的 `dis` 最小的点 `v`：此时 `dis[v]` 已是最短路（边权非负）'],
        summary=['时间 `O(n²)`，空间 `O(n)`；任意两点都能走，是稠密图，不用堆',
                 '更新时只考虑“先走到特殊路起点再坐车”，直接走过去的情况已被合并',
                 '特殊路是==单向==的，且可能比直接走更贵，用 `min` 兜底',
                 '`dis` 用 `defaultdict(lambda: inf)`，坐标元组当键',
                 '同类：稠密图朴素 Dijkstra，参考 743、1631'],
    ),
)
