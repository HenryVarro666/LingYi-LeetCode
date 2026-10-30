def _graph(cv, S, box, T, names, pos, edges, directed=False, wfmt=None, done=None, cur=None, sub=None, title=''):
    """names: 节点名列表；pos: 名字->(0..1,0..1)；edges: [(u,v,label)]；done: 已定节点集合；sub: 名字->节点下方小字"""
    x0, y0, x1, y1 = box
    W, H = x1 - x0 - 80, y1 - y0 - 110
    P = {k: (x0 + 40 + pos[k][0] * W, y0 + 50 + pos[k][1] * H) for k in names}
    R = 30
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    for u, v, lab in edges:
        (ax, ay), (bx, by) = P[u], P[v]
        d = max(1.0, ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5)
        ux, uy = (bx - ax) / d, (by - ay) / d
        if directed:
            cv.arrow((ax + ux * R, ay + uy * R), (bx - ux * (R + 4), by - uy * (R + 4)), T['border'], width=3, head=14)
        else:
            cv.line([(ax + ux * R, ay + uy * R), (bx - ux * R, by - uy * R)], T['border'], 3)
        mx, my = (ax + bx) / 2 - uy * 16, (ay + by) / 2 + ux * 16
        cv.text((mx, my), str(lab), 22, T['yellow'], anchor='mm', bold=True)
    for k in names:
        x, y = P[k]
        isdone = done is not None and k in done
        fill = T['green'] if isdone else T['panel2']
        cv.rect((x - R, y - R, x + R, y + R), fill=fill, r=R, outline=T['yellow'] if k == cur else T['border'], width=5 if k == cur else 2)
        cv.text((x, y), str(k), 28, T['bg'] if isdone else T['text'], anchor='mm', bold=True)
        if sub and sub.get(k) is not None:
            cv.text((x, y + R + 6), str(sub[k]), 20, T['cyan'], anchor='mt', bold=True)


def _draw(cv, S, B, box, T):
    if 'roads' not in S or 'k' not in S:
        return
    n = S['n']
    names = list(range(1, n + 1))
    pos = {1: (0.05, 0.5), 2: (0.4, 0.1), 3: (0.4, 0.9), 4: (0.85, 0.5)}
    edges = [(x, y, f"{v}×{S['k'] + 1}={v * (S['k'] + 1)}") for x, y, v in S['roads']]
    dis = S.get('dis') or [None] * (n + 1)
    done = {i for i in names if dis[i] is not None}
    sub = {i: (f"最低 {dis[i]}" if dis[i] is not None else f"自买 {S['appleCost'][i - 1]}") for i in names}
    _graph(cv, S, box, T, names, pos, edges, done=done, cur=S.get('now'), sub=sub,
           title='城市图（边上 = 往返路费，绿 = 最低成本已定，下方 = 最低成本 / 自己买的价）')


CONFIG = dict(
    num=2473, title='购买苹果的最低成本', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='多源 Dijkstra（点权当起点距离）',
    tags=[],
    code='''
class Solution(object):
    def minCost(self, n, roads, appleCost, k):

        g = [[] for _ in range(n + 1)]
        for x, y, v in roads:
            g[x].append([y, v * (k + 1)])
            g[y].append([x, v * (k + 1)])
        
        heap = []
        for index in range(n):
            heapq.heappush(heap, [appleCost[index], index + 1])
        
        dis = [None] * (n + 1)
        while heap:
            nowd, now = heapq.heappop(heap)
            if dis[now] is not None:
                continue
            
            dis[now] = nowd
            for next, v in g[now]:
                if dis[next] is None:
                    heapq.heappush(heap, [nowd + v, next])
        
        return dis[1:]
''',
    call='Solution().minCost(4, [[1,2,4],[2,3,2],[2,4,5],[3,4,1],[1,3,4]], [56,42,102,301], 2)',
    expect=[54, 42, 48, 51],

    views=[
        dict(type='custom', draw=_draw, h=340),
        dict(type='array', var='dis', label='dis[城市]（下标 0 不用，None = 还没定）', h=200, pointers={'now': 'yellow'}),
        dict(type='heap', var='heap', label='堆：[成本, 城市]', h=170, fmt=lambda x: f'{x[0]}@{x[1]}'),
    ],
    skip=['for index in range(n)', 'g[y].append', 'heapq.heappush(heap, [appleCost', 'heapq.heappush(heap, [nowd'],
    max_steps=60,
    watch=[('nowd', 'nowd', 'blue'), ('now', 'now', 'yellow'), 'k'],
    captions={
        'g = [[]': '邻接表 `g`，城市编号 1～n',
        'g[x].append': '边权先乘 `k + 1`：往返都走最短路，==来回的路费一次算完==：`{v} × {k + 1} = {v * (k + 1)}`',
        'heap = []': '先把每个城市「就地买」的 [成本, 城市] 放进堆，==初始成本就是该城市的苹果价==，相当于把所有城市当起点',
        'dis = [None]': '`dis[i]`：从城市 i 出发买到苹果的最低总成本',
        'while heap': '堆里还有候选 → 取成本最小的',
        'heapq.heappop': '弹出成本最小的 `[{nowd}, 城市{now}]`',
        'if dis[now] is not None': lambda S, B, r: (f'城市 {S.now} 已经定过（更便宜的先出堆），这条是旧的 → `continue` 跳过' if S.dis[S.now] is not None
                                                    else f'城市 {S.now} 还没定 → 这就是它的最低成本'),
        'dis[now] = nowd': '定下来：`dis[{now}] = {nowd}`（第一次出堆即最小）',
        'for next, v in g[now]': '成本 `{nowd}` 往邻居 `{next}` 传：到邻居买这个城市的苹果再运回来，要加上往返路费 `{v}`',
        'if dis[next] is None': lambda S, B, r: (f'邻居 {S.next} 还没定 → 入堆候选 `{S.nowd} + {S.v} = {S.nowd + S.v}`' if S.dis[S.next] is None
                                                  else f'邻居 {S.next} 已定 → 不用再算'),
        'return dis[1:]': '去掉下标 0，得到每个城市的最低成本 `{dis[1:]}`',
    },
    cards=dict(
        one_liner='往返路费一次乘好，所有城市的买苹果价当作多个起点，跑一趟 Dijkstra',
        complexity='时间 `O((n+m)·log(n+m))`，空间 `O(n+m)`',
        problem=['n 个城市，每个城市有苹果价 `appleCost[i]`；每条路有路费，返程时路费要乘 `k + 1`',
                 '从每个城市出发，去某个城市买 1 个苹果（也可原地买）再回来，求最小总成本',
                 '示例：`k=2`，`appleCost=[56,42,102,301]` → `[54,42,48,51]`'],
        quote='来回必然都是走的最短路，在这里就可以直接将图中的所有边先乘以(k + 1)，来代替返回路径的计算。',
        quote_src='—— yiduobo 题解原文',
        idea=['路费乘 `k+1`：去一次 + 回来带着 k 倍的价格，等价于单程 `k+1` 倍',
              '无向图，最短路对称：不用对每个城市跑一遍，反过来从「买苹果」那端出发',
              '每个城市的苹果价直接作为初始堆元素（点权 = 虚拟起点到该点的边），一趟 Dijkstra 搞定'],
        summary=['时间 `O((n+m)·log(n+m))`，空间 `O(n+m)`',
                 '不用真的拆点：把 `[appleCost, 城市]` 全放进初始堆即可',
                 '易错：城市编号从 1 开始，所以 `dis` 开 `n + 1`，返回 `dis[1:]`',
                 '易错：边权乘的是 `k + 1`，不是 `k`',
                 '同类：多源最短路（超级源点）'],
    ),
)
