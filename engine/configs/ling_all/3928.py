import math as _m

N0 = 3
PRICES = [9, 4, 6]
ROADS = [[0, 1, 1, 3], [1, 2, 4, 2]]
POS = {0: (0.1, 0.5), 1: (0.5, 0.5), 2: (0.9, 0.5)}


def _inn(S):
    I = S.get('_inner') or {}
    return I if 'start' in I else None


def _wts(S):
    """当前图的边权：Dijkstra 帧里读 g，否则显示 cost"""
    I = _inn(S)
    w = {}
    if I is not None and 'g' in I:
        for u, lst in enumerate(I['g']):
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
        which = '（去程图：边权 = cost）' if all(w.get((u, v)) == c for u, v, c, t in ROADS) else '（返程图：边权 = cost × tax）'
    cv.text((x0 + 18, y0 + 4), '商店与道路' + which + '　蓝 = 起点，黄 = 刚出堆的 x，绿 = 最短路已确定', 20, T['muted'], bold=True)
    R_ = 36
    dis = I.get('dis') if I else None
    x = I.get('x') if I and 'dis_x' in I else None
    y = I.get('y') if I and 'wt' in I else None
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
        elif dis is not None and I and 'dis_x' in I and dis[u] <= I['dis_x']:
            fill = T['green']
        else:
            fill = T['panel2']
        cv.d.ellipse((px - R_, py - R_, px + R_, py + R_), fill=fill, outline=T['border'], width=2)
        cv.text((px, py), u, 32, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)
        cv.text((px, py - R_ - 30), f'苹果价 {PRICES[u]}', 22, T['orange'], anchor='mm', bold=True)
        if dis is not None:
            cv.text((px, py + R_ + 26), f'dis = {dis[u]}', 22, T['green'], anchor='mm', bold=True, mono=True)


def _txt(S, B):
    I = _inn(S)
    if I is None:
        i = S.get('i')
        if 'dis1' in S and 'dis2' in S and i is not None:
            return f'从商店 `{i}` 出发：去程最短 `{S["dis1"]}`，返程最短 `{S["dis2"]}`，再加各店苹果价取最小'
        return '每个商店 i：枚举去 j 买苹果 = 去程 + 价格 + 返程；也可以就地买'
    return f"Dijkstra 起点 `{I['start']}`，价格上限 `price = {I['price']}`：路超过它就不如就地买"


def _dis1(S):
    I = _inn(S)
    if I is not None:
        return I['dis']
    return S.get('dis1')


CONFIG = dict(
    num=3928, title='购买苹果的最低成本 II', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='每点两次 Dijkstra',
    tags=['灵神题单·图论算法', '难度分 2187'],
    code='''
def dijkstra(g: list[list[tuple[int, int]]], start: int, price: int) -> list[int]:
    dis = [price] * len(g)
    dis[start] = 0  # 起点到自己的距离是 0
    h = [(0, start)]  # 堆中保存 (起点到节点 x 的最短路长度，节点 x)

    while h:
        dis_x, x = heappop(h)
        if dis_x > dis[x]:  # x 之前出堆过
            continue
        for y, wt in g[x]:
            new_dis_y = dis_x + wt
            if new_dis_y < dis[y]:
                dis[y] = new_dis_y  # 更新 x 的邻居的最短路
                # 懒更新堆：只插入数据，不更新堆中数据
                # 相同节点可能有多个不同的 new_dis_y，除了最小的 new_dis_y，其余值都会触发上面的 continue
                heappush(h, (new_dis_y, y))

    return dis

class Solution:
    def minCost(self, n: int, prices: list[int], roads: list[list[int]]) -> list[int]:
        g1 = [[] for _ in range(n)]
        g2 = [[] for _ in range(n)]
        for x, y, cost, tax in roads:
            g1[x].append((y, cost))
            g1[y].append((x, cost))
            g2[x].append((y, cost * tax))
            g2[y].append((x, cost * tax))

        ans = [0] * n
        for i, price in enumerate(prices):
            dis1 = dijkstra(g1, i, price)
            dis2 = dijkstra(g2, i, price)
            ans[i] = min(p + d1 + d2 for p, d1, d2 in zip(prices, dis1, dis2))
        return ans
''',
    call=f'Solution().minCost({N0}, {PRICES}, {ROADS})',
    expect=[8, 4, 6],
    max_steps=66,
    skip=['g1 = [[] for', 'g2 = [[] for', 'g1[x].append', 'g1[y].append', 'g2[x].append', 'g2[y].append', 'for x, y, cost, tax',
          'return dis', 'dis[start] = 0'],
    views=[
        dict(type='text', fn=_txt, h=44, size=22),
        dict(type='custom', draw=_draw, h=210),
        dict(type='array', var=_dis1, label='dis（当前这一轮 Dijkstra：起点到各店）', h=140, cell=80),
        dict(type='array', var='ans', label='ans（每个商店的最小总花费）', h=140, cell=80),
        dict(type='heap', var=lambda S: (_inn(S) or {}).get('h'), label='h（最小堆，元素 = (路长, 商店)）', h=100, fmt=lambda t: f'({t[0]},{t[1]})'),
    ],
    watch=[('i', 'i', 'blue'), ('dis_x', 'dis_x', 'blue'), ('x', 'x', 'yellow'), ('y', 'y'), ('wt', 'wt'), ('new_dis_y', 'new_dis_y', 'orange')],
    captions={
        'dis = [price]': '`dis` 不用 ∞，直接初始化成 `price = {price}`：路长 ==≥ 就地买的价格== 就没必要入堆',
        'h = [(0, start)]': '起点 `{start}` 入堆：`(0, {start})`',
        'dis_x, x = heappop': '弹出路最短的 `x = {x}`，到它的距离是 `{dis_x}`',
        'if dis_x > dis[x]': lambda S, B, r: f'`{S.dis_x} > dis[{S.x}] = {S.dis[S.x]}`：==x 之前出堆过==，跳过' if S.dis_x > S.dis[S.x] else f'`{S.dis_x} == dis[{S.x}]`：首次出堆，去更新邻居',
        'for y, wt in g[x]': lambda S, B, r: f'`{S.x}` 的出边都看完了' if ('y' in B and 'wt' in B and (B.y, B.wt) == (S.y, S.wt) and B.dis_x == S.dis_x and B.x == S.x) else f'看边 `{S.x} → {S.y}`，边权 `{S.wt}`',
        'new_dis_y = dis_x + wt': '走这条边：`{dis_x} + {wt}` = =={new_dis_y}==',
        'if new_dis_y < dis[y]': lambda S, B, r: f'`{S.new_dis_y} < dis[{S.y}] = {S.dis[S.y]}` → ==更短，更新==' if S.new_dis_y < S.dis[S.y] else f'`{S.new_dis_y} ≥ dis[{S.y}] = {S.dis[S.y]}` → 不更短（或不如就地买），不更新',
        'dis[y] = new_dis_y': '更新邻居：`dis[{y}] = {new_dis_y}`',
        'heappush': '`({new_dis_y}, {y})` 入堆（懒更新：旧记录之后会被 `continue` 跳过）',
        'ans = [0] * n': '`ans[i]`：从商店 `i` 出发买到苹果的最小总花费',
        'dis1 = dijkstra': '去程：空手走，边权 `cost`，求 `i` 到每个商店的最短路',
        'dis2 = dijkstra': '返程：带着苹果，边权 `cost*tax`；==无向图==，所以也可以从 `i` 出发算',
        'ans[i] = min': lambda S, B, r: f'枚举买苹果的商店 j：`价格 + 去程 + 返程` = `{[p + a + b for p, a, b in zip(S.prices, S.dis1, S.dis2)]}` → 取最小 `ans[{S.i}] = {S.ans[S.i]}`',
        'return ans': '全部商店算完，返回 `{ret}`',
    },
    cards=dict(
        one_liner='每个商店跑两次 Dijkstra：去程 cost，返程 cost×tax',
        complexity='时间 `O(n(n+m log m))`，空间 `O(n+m)`',
        problem=['`n` 个商店，`prices[i]` 是苹果价；`roads` 是双向道路 `[u, v, cost, tax]`',
                 '空手走道路花 `cost`，带着苹果走花 `cost × tax`',
                 '从每个商店 `i` 出发：可以就地买，也可以==去 j 买再回来==，求最小总花费',
                 '示例：`prices=[9,4,6]`，`roads=[[0,1,1,3],[1,2,4,2]]` → `[8,4,6]`'],
        quote='对于每个 i，枚举在商店 j 购买苹果。从 j 到 i 的最短路长度，由于图是无向图，等于从 i 到 j 的最短路长度。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`n ≤ 1000`，可以暴力：每个 `i` 在两张图（cost / cost×tax）上各跑一次 Dijkstra',
              '总花费 = 去程 + `prices[j]` + 返程，对所有 `j` 取最小',
              '==优化==：`ans[i] ≤ prices[i]`，所以 `dis` 直接初始化成 `price`，更长的路不入堆'],
        summary=['时间 `O(n(n+m log m))`，用懒更新堆',
                 '易错：返程边权是 `cost * tax`，去程是 `cost`；就地买 = `j = i`，距离 0',
                 '`dis` 初始化成 `price` 同时保证了 `ans[i] ≤ prices[i]`',
                 '`list[int]` 这类写法需要 Python 3.9+',
                 '为让视频短，示例用 3 个商店；本题 `n` 最大 1000'],
    ),
)
