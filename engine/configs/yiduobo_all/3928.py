N0 = 3
PRICES = [9, 4, 6]
ROADS = [[0, 1, 1, 3], [1, 2, 4, 2]]
POS = {0: (0.1, 0.5), 1: (0.5, 0.5), 2: (0.9, 0.5)}


def _inn(S):
    I = S.get('_inner') or {}
    return I if ('heap' in I and 'start' in I) else None


def _wts(S):
    I = _inn(S)
    w = {}
    if I is not None and 'f' in I:
        for u, lst in enumerate(I['f']):
            for v, wt in lst:
                w[(min(u, v), max(u, v))] = wt
        return w, I
    for u, v, c, t in ROADS:
        w[(u, v)] = c
    return w, None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    w, I = _wts(S)
    L, R = x0 + 90, x1 - 90
    cy = y0 + (y1 - y0) / 2 + 10
    P = {u: (L + fx * (R - L), cy) for u, (fx, fy) in POS.items()}
    which = ''
    if I is not None:
        which = '（去程图：cost）' if all(w.get((u, v)) == c for u, v, c, t in ROADS) else '（返程图：cost × tax）'
    cv.text((x0 + 18, y0 + 4), '商店与道路' + which + '　蓝 = 起点，黄 = 刚出堆，绿 = 距离已确定', 20, T['muted'], bold=True)
    R_ = 36
    dis = I.get('dis') if I else None
    x = I.get('x') if I and 'd' in I else None
    y = I.get('y') if I and 'w' in I else None
    for (u, v), wt in w.items():
        a, b = P[u], P[v]
        col, wd = T['dim'], 4
        if x is not None and y is not None and {u, v} == {x, y}:
            col, wd = T['yellow'], 6
        cv.line([(a[0] + R_, a[1]), (b[0] - R_, b[1])], col, wd)
        mxp = (a[0] + b[0]) / 2
        cv.rect((mxp - 30, cy - 52, mxp + 30, cy - 22), fill=T['bg'], r=6)
        cv.text((mxp, cy - 37), wt, 26, T['yellow'] if col == T['yellow'] else T['muted'], anchor='mm', bold=True, mono=True)
    for u, (px, py) in P.items():
        if I is not None and u == I['start']:
            fill = T['blue']
        elif x is not None and u == x:
            fill = T['yellow']
        elif dis is not None and dis[u] is not None:
            fill = T['green']
        else:
            fill = T['panel2']
        cv.d.ellipse((px - R_, py - R_, px + R_, py + R_), fill=fill, outline=T['border'], width=2)
        cv.text((px, py), u, 32, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)
        cv.text((px, py - R_ - 30), f'苹果价 {PRICES[u]}', 22, T['orange'], anchor='mm', bold=True)
        if dis is not None:
            cv.text((px, py + R_ + 26), f'dis = {"?" if dis[u] is None else dis[u]}', 22, T['green'], anchor='mm', bold=True, mono=True)


def _txt(S, B):
    I = _inn(S)
    if I is None:
        if 'to' in S and 'back' in S:
            return f"出发店 `{S['start']}`：去程 `{S['to']}`，返程 `{S['back']}`（None = 超过就地买的价 `{PRICES[S['start']]}`，不考虑）"
        return '每个商店：就地买，或去别的店买再回来（去程 cost，返程 cost × tax）'
    return f"Dijkstra 起点 `{I['start']}`：只让路长 `< prices[start] = {PRICES[I['start']]}` 的点入堆"


def _dis1(S):
    I = _inn(S)
    if I is not None:
        return I['dis']
    return S.get('to')


CONFIG = dict(
    num=3928, title='购买苹果的最低成本 II', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='暴力枚举起点 · 两张图 Dijkstra',
    tags=['灵神题单·图论算法', '难度分 2187'],
    code='''
class Solution(object):
    def minCost(self, n, prices, roads):
        
        g = [[] for _ in range(n)]
        t = [[] for _ in range(n)]
        for x, y, cost, tax in roads:
            g[x].append((y, cost))
            t[x].append((y, cost * tax))
            g[y].append((x, cost))
            t[y].append((x, cost * tax))
        
        def dijkstra(start, f, dis):
            heap = [(0, start)]
            while heap:
                d, x = heapq.heappop(heap)
                if dis[x] is None:
                    dis[x] = d
                    for y, w in f[x]:
                        if dis[y] is None and d + w < prices[start]:
                            heapq.heappush(heap, (d + w, y))

        res = []
        for start in range(n):
            to = [None] * n
            dijkstra(start, g, to)
            back = [None] * n
            dijkstra(start, t, back)

            cost = prices[start]
            for index in range(n):
                if to[index] is not None and back[index] is not None:
                    cost = min(cost, to[index] + back[index] + prices[index])
            res.append(cost)
        
        return res
''',
    call=f'Solution().minCost({N0}, {PRICES}, {ROADS})',
    expect=[8, 4, 6],
    max_steps=66,
    skip=['g = [[] for', 't = [[] for', 'g[x].append', 't[x].append', 'g[y].append', 't[y].append', 'for x, y, cost, tax',
          'def dijkstra', 'res = []', 'for index in range'],
    views=[
        dict(type='text', fn=_txt, h=44, size=22),
        dict(type='custom', draw=_draw, h=210),
        dict(type='array', var=_dis1, label='dis / to（起点到各店，• = None 未确定）', h=140, cell=80, fmt=lambda v: '-' if v is None else str(v)),
        dict(type='array', var='res', label='res（每个商店的最小总花费）', h=140, cell=80),
        dict(type='heap', var=lambda S: (_inn(S) or {}).get('heap'), label='heap（最小堆，元素 = (路长, 商店)）', h=100, fmt=lambda t: f'({t[0]},{t[1]})'),
    ],
    watch=[('start', 'start', 'blue'), ('d', "_inner.get('d', '')", 'blue'), ('x', "_inner.get('x', '') if 'heap' in _inner else ''", 'yellow'), ('y', "_inner.get('y', '') if 'heap' in _inner else ''"), ('w', "_inner.get('w', '')"), ('cost', "_inner.get('cost', '-') if 'heap' not in _inner else '-'", 'green')],
    captions={
        'heap = [(0, start)]': '起点 `{start}` 入堆：`(0, {start})`',
        'd, x = heapq.heappop': '弹出路最短的 `x = {x}`，距离 `{d}`',
        'if dis[x] is None': lambda S, B, r: f'`dis[{S.x}]` 还没确定 → ==首次出堆==，距离就是 `{S.d}`' if S.dis[S.x] is None else f'`dis[{S.x}] = {S.dis[S.x]}` 已确定，这是旧记录，跳过',
        'dis[x] = d': '确定 `dis[{x}] = {d}`',
        'for y, w in f[x]': lambda S, B, r: f'`{S.x}` 的出边都看完了' if ('y' in B and 'w' in B and (B.y, B.w) == (S.y, S.w) and B.x == S.x and B.d == S.d) else f'看边 `{S.x} → {S.y}`，边权 `{S.w}`',
        'if dis[y] is None and d + w': lambda S, B, r: (f'`{S.y}` 已确定，不用再入堆' if S.dis[S.y] is not None else (f'`{S.d} + {S.w} = {S.d + S.w}`，对比 `prices[{S.start}] = {PRICES[S.start]}`：' + ('==更小，入堆==' if S.d + S.w < PRICES[S.start] else '不小于就地买的价，剪掉'))),
        'heapq.heappush': '`({d + w}, {y})` 入堆',
        'to = [None] * n': '`to[i]`：空手从 `{start}` 到 `i` 的最短路，None 表示还没算出',
        'dijkstra(start, g, to)': '去程：在图 `g`（边权 cost）上求最短路',
        'back = [None] * n': '`back[i]`：带着苹果从 `i` 回 `{start}`',
        'dijkstra(start, t, back)': '返程：在图 `t`（边权 cost×tax）上求；==无向图==，从 start 出发算即可',
        'cost = prices[start]': '先假设就地买：`cost = {cost}`',
        'if to[index] is not None': lambda S, B, r: f'去程 `{S.to[S.index]}`，返程 `{S.back[S.index]}`：' + ('两个方向都到得了 → 比较' if (S.to[S.index] is not None and S.back[S.index] is not None) else '有一个方向到不了 → 跳过'),
        'cost = min(cost': '`min(cost, 去程 + 返程 + prices[{index}])` → `cost = {cost}`',
        'res.append(cost)': '商店 `{start}` 的答案：`{cost}`',
        'return res': '全部商店算完，返回 `{ret}`',
    },
    cards=dict(
        one_liner='枚举出发点，在去程图和返程图上各跑一次堆 Dijkstra',
        complexity='时间 `O(n(n + m log m))`，空间 `O(n + m)`',
        problem=['`n` 个商店，`prices[i]` 是苹果价；`roads` 是双向路 `[u, v, cost, tax]`',
                 '空手走一条路花 `cost`，带着苹果走花 `cost × tax`',
                 '每个商店可以就地买，也可以去别处买完再回来，求最小总花费',
                 '示例：`prices=[9,4,6]`，`roads=[[0,1,1,3],[1,2,4,2]]` → `[8,4,6]`'],
        quote='题目中点和边的数量都比较小，因此在这里可以直接暴力枚举每个商店，然后在两张图上分别执行带堆dijkstra计算最短路即可。',
        quote_src='—— yiduobo 题解',
        idea=['去程是「起点到任意店」，返程是「任意店到起点」：==无向图，所以返程也是从起点出发==',
              '建两张图：`g` 边权 `cost`，`t` 边权 `cost*tax`',
              '路长已经 `≥ prices[start]` 的点没必要入堆（反正不如就地买）'],
        summary=['时间 `O(n(n + m log m))`，`n ≤ 1000`、`m ≤ 2000` 可以暴力',
                 '易错：去程用 `cost`，返程用 `cost * tax`；就地买是 `cost` 的初值',
                 '`dis[y] is None` 当作「未确定」，堆里可能有旧记录，出堆时判断',
                 '代码原文已是 Python 3 可运行写法，无需修改',
                 '对比灵神：他把 `dis` 初始化成 `price`；这里用 `d + w < prices[start]` 在入堆时剪枝'],
    ),
)
