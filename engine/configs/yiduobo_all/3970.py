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
    pos = {0: (0.05, 0.5), 1: (0.3, 0.1), 2: (0.62, 0.1), 3: (0.42, 0.9), 4: (0.92, 0.5)}
    edges = [(x, y, w) for x, y, w in S['edges']]
    fin = lambda v: v is not None and v != float('inf')
    best = {}
    for i in names:
        vs = [v for v in S['dis'][i] if fin(v)]
        best[i] = min(vs) if vs else None
    done = {i for i in names if best[i] is not None}
    sub = {i: f"'{S['labels'][i]}'" + (f"  最短 {best[i]}" if best[i] is not None else '') for i in names}
    _graph(cv, S, box, T, names, pos, edges, directed=True, done=done, cur=S.get('x'), sub=sub,
           title='有向图（节点下方 = 标签 / 当前已知最短，绿 = 已有最短路）')


CONFIG = dict(
    num=3970, title='最多 K 个连续相同字符的最短路径', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='分层图 Dijkstra（k 层）',
    tags=['难度分 1840'],
    code='''
class Solution(object):
    def shortestPath(self, n, edges, labels, k):
        
        g = [[] for _ in range(n)]
        for x, y, w in edges:
            g[x].append((y, w))
        
        heap = [(0, 0, 1)]
        dis = [[None] * (k + 1) for _ in range(n)]

        while heap:
            d, x, cnt = heapq.heappop(heap)
            if dis[x][cnt] is None:
                dis[x][cnt] = d
                for y, w in g[x]:
                    nxt_cnt = cnt
                    if labels[x] == labels[y]:
                        nxt_cnt += 1
                    else:
                        nxt_cnt = 1
                    
                    if nxt_cnt <= k and dis[y][nxt_cnt] is None:
                        heapq.heappush(heap, (d + w, y, nxt_cnt))
        
        res = -1
        for cnt in range(1, k + 1):
            if dis[-1][cnt] is not None and (res == -1 or res > dis[-1][cnt]):
                res = dis[-1][cnt]
        return res
''',
    call='Solution().shortestPath(5, [[0,1,1],[1,2,1],[2,4,1],[0,3,2],[3,4,5]], "aaabb", 2)',
    expect=7,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='table', var='dis', label='dis[节点][所在层 cnt]（None = 还没定）', h=270, cell=90,
             rows=lambda S: [f"{i}'{S['labels'][i]}'" for i in range(len(S['dis']))],
             cols=lambda S: [str(j) for j in range(len(S['dis'][0]))],
             cursors=[('x', 'cnt', 'yellow', '')],
             color=lambda S, i, j, v: 'green' if v is not None else None),
        dict(type='heap', var='heap', label='堆：(距离, 节点, 层)', h=140, fmt=lambda t: f'{t[0]},{t[1]},{t[2]}'),
    ],
    skip=['heapq.heappush', 'g[x].append', 'nxt_cnt = cnt'],
    max_steps=60,
    watch=[('d', 'd', 'blue'), ('x', 'x', 'yellow'), ('cnt', 'cnt', 'pink'), 'k'],
    captions={
        'g = [[]': '邻接表，`g[x]` 存 `(y, w)`',
        'heap = [(0, 0, 1)]': '从第 1 层的 0 号点出发：`(距离 0, 节点 0, 第 1 层)`',
        'dis = [[None]': '`dis[x][cnt]`：到达==第 cnt 层==的节点 x 的最短路，None 表示这个状态还没被确定',
        'while heap': '堆里还有状态 → 取距离最小的',
        'heapq.heappop': '弹出 `(距离 {d}, 节点 {x}, 第 {cnt} 层)`',
        'if dis[x][cnt] is None': lambda S, B, r: (f'`dis[{S.x}][{S.cnt}]` 还没定 → 第一次出堆，距离 {S.d} 就是它的最短路' if S.dis[S.x][S.cnt] is None
                                                  else f'`dis[{S.x}][{S.cnt}]` 已有值 → 旧状态，跳过'),
        'dis[x][cnt] = d': '定下来：`dis[{x}][{cnt}] = {d}`',
        'for y, w in g[x]': lambda S, B, r: (f'枚举 `{S.x}` 指向的 `{S.y}`，权重 `{S.w}`' if S.g[S.x] and B.get('x') != S.x or B.get('y') != S.y else f'节点 {S.x} 没有出边（或边已枚举完）'),
        'if labels[x] == labels[y]': lambda S, B, r: (f"`{S.labels[S.x]}` == `{S.labels[S.y]}` → 标签相同，走到下一层（连续个数 +1）" if S.labels[S.x] == S.labels[S.y]
                                                    else f"`{S.labels[S.x]}` != `{S.labels[S.y]}` → 标签不同，回到第 1 层"),
        'nxt_cnt += 1': '同字符：`nxt_cnt = {nxt_cnt}`',
        'nxt_cnt = 1': '字符断开：`nxt_cnt = 1`',
        'if nxt_cnt <= k': lambda S, B, r: (f'`nxt_cnt = {S.nxt_cnt} > k = {S.k}`：层数超限 → 这条边不连，丢弃' if S.nxt_cnt > S.k
                                            else (f'第 {S.nxt_cnt} 层的 `{S.y}` 还没定 → `({S.d} + {S.w})` = {S.d + S.w} 入堆' if S.dis[S.y][S.nxt_cnt] is None
                                                  else f'第 {S.nxt_cnt} 层的 `{S.y}` 已定 → 不用入堆')),
        'res = -1': '终点可能停在任意一层 → 汇总各层取最小，`-1` 表示没有合法路径',
        'for cnt in range(1, k + 1)': '检查终点第 `{cnt}` 层',
        'if dis[-1][cnt] is not None': lambda S, B, r: (f'终点第 {S.cnt} 层距离 {S.dis[-1][S.cnt]}' + ('，更小 → 更新答案' if (S.res == -1 or S.res > S.dis[-1][S.cnt]) else '，不更小 → 保留')
                                                       if S.dis[-1][S.cnt] is not None else f'终点第 {S.cnt} 层没到过 → 跳过'),
        'res = dis[-1][cnt]': '`res = {res}`',
        'return res': '最短路径 `{res}`',
    },
    cards=dict(
        one_liner='把「连续相同字符个数」做成 k 层图，从第 1 层的 0 号点跑 Dijkstra',
        complexity='时间 `O(nk + mk·log(mk))`，空间 `O(nk + mk)`',
        problem=['有向带权图，每个点有字符标签；路径经过的点按序拼接标签',
                 '拼接串最多包含 `k` 个连续相同字符，求 0 到 n−1 的最短路，没有返回 `-1`',
                 '示例：标签 `aaabb`，`k=2` → `7`'],
        quote='非常标准的分层图最短路问题。对于本题最多连续k个相同字符的限制，可以通过构造一张k层的图来解决。',
        quote_src='—— yiduobo 题解原文',
        idea=['同标签：`u` 连向下一层的 `v`；第 k 层不再往下连',
              '不同标签：`u` 连向第一层的 `v`，计数清零',
              '路径只能是「第 1 层爬到某层，再回到第 1 层」的循环，最高到 k 层 → 连续字符不会超过 k',
              '不真建图：用 `dis[x][cnt]` 表示第 cnt 层的 x'],
        summary=['时间 `O(nk + mk·log(mk))`，空间 `O(nk + mk)`',
                 '易错：起点在第 1 层，`dis` 第二维开 `k + 1`',
                 '这份写法入堆前只判断「状态没定过」，出堆时才记录，所以可能有重复入堆',
                 '终点可能在任意层，最后要遍历 `1..k` 取最小（灵神是首次出堆即返回）',
                 '对比灵神：他用 `d > dis[x][cnt]` 懒删除，这里用「None 才处理」'],
    ),
)
