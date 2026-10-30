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
    if 'edges' not in S or 'dis' not in S:
        return
    n = S['n']
    names = list(range(n))
    pos = {0: (0.05, 0.5), 1: (0.35, 0.15), 2: (0.7, 0.15), 3: (0.35, 0.85), 4: (0.8, 0.85)}
    lab = {}
    for x, y, v in S['edges']:
        lab.setdefault((x, y), []).append(str(v))
    edges = [(x, y, ' / '.join(vs) + ('（重边）' if len(vs) > 1 else '')) for (x, y), vs in lab.items()]
    dis = S['dis']
    done = {i for i in names if dis[i] is not None}
    sub = {i: (('标记 ' if i in S['marked'] else '') + (f'距离 {dis[i]}' if dis[i] is not None else '')).strip() or None for i in names}
    _graph(cv, S, box, T, names, pos, edges, directed=True, done=done, cur=S.get('now'), sub=sub,
           title=f"有向图（起点 {S['s']}，绿 = 最短距离已定，标记 = marked 里的点）")


CONFIG = dict(
    num=2737, title='找到最近的标记节点', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='Dijkstra + 取标记点最小值',
    tags=[],
    code='''
class Solution(object):
    def minimumDistance(self, n, edges, s, marked):

        dis = [None] * n
        heap = [[0, s]]
        g = {x : {} for x in range(n)}
        for x, y, v in edges:
            if y not in g[x]:
                g[x][y] = v
            else:
                g[x][y] = min(g[x][y], v)
        
        while heap:
            d, now = heapq.heappop(heap)
            if dis[now] is None:
                dis[now] = d
                for nxt in g[now]:
                    if dis[nxt] is None:
                        heapq.heappush(heap, [g[now][nxt] + d, nxt])
        
        res = -1
        for x in marked:
            if dis[x] is not None and (res == -1 or res > dis[x]):
                res = dis[x]
        
        return res
''',
    call='Solution().minimumDistance(5, [[0,1,3],[0,1,1],[1,2,2],[0,3,6],[3,4,1]], 0, [2, 4])',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=340),
        dict(type='array', var='dis', label='dis[点]（None = 还没算出来）', h=190, pointers={'now': 'yellow'}),
        dict(type='heap', var='heap', label='堆：[距离, 点]', h=170, fmt=lambda x: f'{x[0]}@{x[1]}'),
    ],
    skip=['heapq.heappush', 'g[x : {}', 'g = {x'],
    max_steps=60,
    watch=[('d', 'd', 'blue'), ('now', 'now', 'yellow'), ('res', 'res', 'green')],
    captions={
        'dis = [None]': '`dis[i]`：起点到点 i 的最短距离，None 表示还没定',
        'heap = [[0, s]]': '堆里先放起点：距离 0',
        'for x, y, v in edges': '建图：逐条读边 `{x} → {y}`，权重 `{v}`',
        'if y not in g[x]': lambda S, B, r: (f'`{S.x} → {S.y}` 第一次出现 → 直接记权重' if S.y not in S.g[S.x] else f'`{S.x} → {S.y}` 是重边 → 只保留较小的'),
        'g[x][y] = v': '记下边权：`g[{x}][{y}] = {v}`',
        'g[x][y] = min': '重边取小：`min` 之后 `g[{x}][{y}] = {g[x][y]}`（题目有重边，必须这样）',
        'while heap': '堆里还有候选 → 继续',
        'heapq.heappop': '弹出距离最小的 `[{d}, 点{now}]`',
        'if dis[now] is None': lambda S, B, r: (f'点 {S.now} 还没定 → 第一次出堆，距离 {S.d} 就是最短（边权非负）' if S.dis[S.now] is None
                                                else f'点 {S.now} 已定，这是旧候选 → 忽略'),
        'dis[now] = d': '定下来：`dis[{now}] = {d}`',
        'for nxt in g[now]': '看 `{now}` 的出边指向 `{nxt}`，权重 `{g[now][nxt]}`',
        'if dis[nxt] is None': lambda S, B, r: (f'`{S.nxt}` 未定 → 候选距离 `{S.g[S.now][S.nxt]} + {S.d} = {S.g[S.now][S.nxt] + S.d}` 入堆' if S.dis[S.nxt] is None
                                                 else f'`{S.nxt}` 已定 → 不用入堆'),
        'res = -1': '`res = -1` 表示没有可达的标记点',
        'for x in marked': '逐个看标记点 `{x}`',
        'if dis[x] is not None': lambda S, B, r: (f'标记点 {S.x} 可达，距离 {S.dis[S.x]}' + ('，比当前 res 小（或 res 还是 -1）→ 更新' if (S.res == -1 or S.res > S.dis[S.x]) else '，不比 res 小 → 不更新')
                                                   if S.dis[S.x] is not None else f'标记点 {S.x} 不可达 → 跳过'),
        'res = dis[x]': '`res = {res}`',
        'return res': '最近的标记点距离是 `{res}`',
    },
    cards=dict(
        one_liner='先 Dijkstra 求出起点到所有点的距离，再在标记点里挑最小',
        complexity='时间 `O((n+m)·log(n+m))`，空间 `O(n+m)`',
        problem=['有向带权图，边权为正，给定起点 `s` 和一组标记点 `marked`',
                 '求从 `s` 到任意标记点的最短距离，到不了返回 `-1`',
                 '示例：`n=5`，`s=0`，`marked=[2,4]` → `3`（有重边 `0→1` 权 3 和 1）'],
        quote='题目中边的权重非负，因此可以直接使用dijkstra算法，计算从s出发到图中所有点的最短距离。接下来遍历marked中的点，找出其中离s距离最近的点即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['权重非负 → Dijkstra，一趟得到 `s` 到所有点的最短距离',
              '再扫一遍 `marked`，取可达点里距离最小的',
              '注意重边：建图时同一对点只留权重较小的那条'],
        summary=['时间 `O((n+m)·log(n+m))`，空间 `O(n+m)`',
                 '易错：有重边，用 `min` 保留小边权',
                 '易错：`dis[x]` 可能是 None（不可达），要先判断',
                 '原文用 `res == -1` 代表还没找到，所以别和距离为 -1 混淆（距离不会是负数）',
                 '同类：灵神题单「单源最短路 Dijkstra」'],
    ),
)
