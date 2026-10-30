import math as _m

START, TARGET = [1, 1], [4, 5]
ROADS = [[1, 2, 3, 3, 2], [3, 4, 4, 5, 1]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nl = S.get('node_list') or []
    sp = S.get('sp_dict') or {}
    dis = S.get('dis')
    vis = S.get('vis') or set()
    mi, i = S.get('mi'), S.get('i')
    line = S.get('_line', 0)
    cv.text((x0 + 18, y0 + 4), '粉 = mi　蓝 = i　黄 = 有距离　绿 = 已确定', 21, T['muted'], bold=True)
    ax0, ax1, ay0, ay1 = x0 + 90, x1 - 90, y0 + 110, y1 - 70

    def P(p):
        return (ax0 + (p[0] - 0.5) / 4 * (ax1 - ax0), ay1 - (p[1] - 0.5) / 5 * (ay1 - ay0))
    for gx in range(1, 5):
        X, _ = P((gx, 1))
        cv.line([(X, ay0), (X, ay1)], (34, 40, 50), 1)
        cv.text((X, ay1 + 8), gx, 18, T['dim'], anchor='mt', mono=True)
    for gy in range(1, 6):
        _, Y = P((1, gy))
        cv.line([(ax0, Y), (ax1, Y)], (34, 40, 50), 1)
        cv.text((ax0 - 12, Y), gy, 18, T['dim'], anchor='rm', mono=True)

    def arrow(a, b, c, w, lab=None, frac=0.5):
        pa, pb = P(a), P(b)
        L = _m.hypot(pb[0] - pa[0], pb[1] - pa[1]) or 1
        ux, uy = (pb[0] - pa[0]) / L, (pb[1] - pa[1]) / L
        cv.arrow((pa[0] + ux * 22, pa[1] + uy * 22), (pb[0] - ux * 26, pb[1] - uy * 26), c, w, head=16)
        if lab is not None:
            mx, my = pa[0] + (pb[0] - pa[0]) * frac, pa[1] + (pb[1] - pa[1]) * frac
            cv.rect((mx - 20, my - 15, mx + 20, my + 15), fill=T['panel'], r=8)
            cv.text((mx, my), lab, 22, c, anchor='mm', bold=True)
    # 题目给的特殊路（暗）
    for a1, b1, a2, b2, cost in ROADS:
        pa, pb = P((a1, b1)), P((a2, b2))
        cv.dashed(pa, pb, (60, 68, 80), 2)
    # 已存进 sp_dict 的特殊路（亮）
    for (u, v), c in sp.items():
        arrow(nl[u], nl[v], T['blue'], 5, f'车{c}', 0.5)
    # 正在尝试的 i
    if mi is not None and i is not None and 40 <= line <= 47 and i < len(nl):
        pa, pb = P(nl[mi]), P(nl[i])
        cv.dashed(pa, (pb[0], pa[1]), T['yellow'], 3)
        cv.dashed((pb[0], pa[1]), pb, T['yellow'], 3)
    for k, p in enumerate(nl):
        X, Y = P(p)
        col = T['panel2']
        if dis is not None and k < len(dis):
            if k == mi and 39 <= line <= 47:
                col = T['pink']
            elif k in vis:
                col = T['green']
            elif 40 <= line <= 47 and k == i:
                col = T['blue']
            elif dis[k] is not None:
                col = T['yellow']
        cv.d.ellipse((X - 20, Y - 20, X + 20, Y + 20), fill=col, outline=T['border'], width=3)
        cv.text((X, Y), k, 24, T['bg'] if col != T['panel2'] else T['text'], anchor='mm', bold=True, mono=True)
        t1 = f'({p[0]},{p[1]})'
        if dis is not None and k < len(dis) and dis[k] is not None:
            cv.text((X + 28, Y - 14), f'dis={dis[k]}', 20, T['cyan'], anchor='lm', bold=True, mono=True)
            cv.text((X + 28, Y + 10), t1, 16, T['dim'], anchor='lm', mono=True)
        else:
            cv.text((X + 28, Y), t1, 18, T['dim'], anchor='lm', mono=True)
    if not nl:
        cv.text(((x0 + x1) / 2, (y0 + y1) / 2), '点还没有建好', 28, T['dim'], anchor='mm')


CONFIG = dict(
    num=2662, title='前往目标的最小代价', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='关键点建图 · 朴素 Dijkstra',
    tags=['难度分 2154'],
    code='''
class Solution(object):
    def minimumCost(self, start, target, specialRoads):

        if start == target:
            return 0

        node_list = [start, target]
        node_dict = {}
        node_dict[(start[0], start[1])] = 0
        node_dict[(target[0], target[1])] = 1

        sp_dict = {}

        for x1, y1, x2, y2, cost in specialRoads:
            if (x1, y1) not in node_dict:
                node_dict[(x1, y1)] = len(node_list)
                node_list.append([x1, y1])
            
            if (x2, y2) not in node_dict:
                node_dict[(x2, y2)] = len(node_list)
                node_list.append([x2, y2])
            
            id1 = node_dict[(x1, y1)]
            id2 = node_dict[(x2, y2)]
            if abs(x1 - x2) + abs(y1 - y2) > cost:
                if (id1, id2) not in sp_dict or sp_dict[(id1, id2)] > cost:
                    sp_dict[(id1, id2)] = cost
            
        n = len(node_list)
        dis = [None] * n
        dis[0] = 0
        vis = set()
        for _ in range(n):
            mi = None
            for i in range(n):
                if i not in vis and dis[i] is not None and (mi is None or dis[mi] > dis[i]):
                    mi = i
            
            vis.add(mi)
            for i in range(n):
                if i not in vis:
                    cost = abs(node_list[i][0] - node_list[mi][0]) + abs(node_list[i][1] - node_list[mi][1])
                    if (mi, i) in sp_dict and cost > sp_dict[(mi, i)]:
                        cost = sp_dict[(mi, i)]

                    if dis[i] is None or dis[i] > dis[mi] + cost:
                        dis[i] = dis[mi] + cost

        return dis[1]
''',
    call=f'Solution().minimumCost({START}, {TARGET}, {ROADS})',
    expect=5,
    views=[
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=[('mi', 'mi', 'pink'), ('i', 'i', 'blue'), ('cost', 'cost', 'orange'),
           ('dis', lambda S: S.get('dis'), 'cyan')],
    skip=['node_dict = {}', 'node_dict[(start', 'node_dict[(target', 'sp_dict = {}', 'for x1, y1, x2, y2, cost in',
          'if (x1, y1) not in node_dict', 'node_dict[(x1, y1)] = len', 'if (x2, y2) not in node_dict',
          'node_dict[(x2, y2)] = len', 'id1 =', 'id2 =', 'if (id1, id2) not in sp_dict', 'dis = [None]', 'vis = set()',
          'dis[0] = 0', 'mi = None', 'for i in range(n)', 'if i not in vis', 'mi = i', 'n = len(node_list)'],
    captions={
        'if start == target': '起点就是终点：代价 0。否则继续建图',
        'node_list = [start, target]': '关键点只有：起点、终点、特殊路的两端。`node_list` 先放起点（编号 0）和终点（编号 1）',
        'node_list.append': '新的关键点 `{node_list[-1]}`，编号 =={len(node_list) - 1}==',
        'if abs(x1 - x2)': lambda S, B, r: (f'特殊路 `({S.x1},{S.y1}) → ({S.x2},{S.y2})`：走过去要 `{abs(S.x1 - S.x2) + abs(S.y1 - S.y2)}`，坐车 `{S.cost}`，==车更便宜==，记下' if abs(S.x1 - S.x2) + abs(S.y1 - S.y2) > S.cost
                                            else f'特殊路 `({S.x1},{S.y1}) → ({S.x2},{S.y2})`：车 `{S.cost}` 不比走路便宜，没用，忽略'),
        'sp_dict[(id1, id2)] = cost': '`sp_dict[({id1}, {id2})] = {cost}`：有向边，只能从 {id1} 号点坐到 {id2} 号点',
        'for _ in range(n)': lambda S, B, r: (f'所有 {S.n} 个点都确定了，结束' if len(S.vis) == S.n
                                              else f'第 {len(S.vis) + 1} 轮：先找“没确定、距离最小”的点'),
        'vis.add(mi)': lambda S, B, r: f'==稠密图不用堆==：在没确定的点里扫一遍，`dis` 最小的是 `mi = {S.mi}`（`dis = {S.dis[S.mi]}`），确定它',
        'cost = abs': '从 `{mi}` 号点直接走到 `{i}` 号点：曼哈顿距离 `cost` = =={cost}==',
        'if (mi, i) in sp_dict': lambda S, B, r: ((f'`({S.mi}, {S.i})` 有特殊路，车费 `{S.sp_dict[(S.mi, S.i)]}` 比走路 `{B.cost}` 便宜 → 改用车费' if (S.mi, S.i) in S.sp_dict and B.cost > S.sp_dict[(S.mi, S.i)]
                                                    else (f'有特殊路但不比走路便宜，仍走路 `{S.cost}`' if (S.mi, S.i) in S.sp_dict else f'没有 `{S.mi} → {S.i}` 的特殊路，按走路 `{S.cost}` 算'))),
        'cost = sp_dict[(mi, i)]': '换成车费 `cost` = =={cost}==',
        'if dis[i] is None or': lambda S, B, r: (lambda new: (f'`dis[{S.mi}] + cost = {S.dis[S.mi]} + {S.cost}` = {new}；`dis[{S.i}]` 目前 `{S.dis[S.i] if S.dis[S.i] is not None else "∞"}` → ' + ('==更小，更新==' if S.dis[S.i] is None or S.dis[S.i] > new else '不更小，保持')))(S.dis[S.mi] + S.cost),
        'dis[i] = dis[mi] + cost': '`dis[{i}]` = =={dis[i]}==',
        'return dis[1]': '终点（1 号点）的最短代价 `dis[1]` = =={ret}==',
    },
    max_steps=110,
    cards=dict(
        one_liner='曼哈顿距离下只有关键点有用：起点、终点、特殊路两端，建图后稠密图 Dijkstra',
        complexity='时间 `O(k²)`，空间 `O(k)`（`k ≤ 2·路数 + 2`）',
        problem=['平面上走一格代价为曼哈顿距离；另有若干条==单向特殊路==，代价 `cost`',
                 '求 `start` 到 `target` 的最小代价',
                 '本视频：`start=[1,1]`，`target=[4,5]`，两条特殊路 `(1,2)→(3,3)`、`(3,4)→(4,5)` → `5`'],
        quote='由于路径长度的计算方式是曼哈顿距离，因此除了起点、终点以及特殊路径中位置点之外，是没有必要走到其他无关点位上的……问题就变成了最多只有两百零二个点的最短路径问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['点只保留：起点、终点、特殊路两端，编号存进 `node_list`',
              '任意两点之间都能走，边权 = 曼哈顿距离；特殊路是有向边，只在==更便宜==时才记',
              '点数最多 202、边是全连接 → 稠密图，用朴素 Dijkstra：每轮线性扫描找最小的点'],
        summary=['时间 `O(k²)`，`k` 为关键点数（最多 202）；空间 `O(k)`',
                 '特殊路是==有向==的，且不一定比走路便宜，所以建边前要判断 `> cost`',
                 '起点终点相同要先单独返回 0',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '对比灵神：灵神用坐标元组当键、只存终点，不显式编号；这里先给每个关键点编号再建图'],
    ),
)
