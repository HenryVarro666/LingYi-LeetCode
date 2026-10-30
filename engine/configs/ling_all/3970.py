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
    author='灵茶山艾府', technique='分层图 Dijkstra（状态 = 节点 + 末尾连续个数）',
    tags=['难度分 1840'],
    code='''
class Solution:
    def shortestPath(self, n: int, edges: list[list[int]], labels: str, k: int) -> int:
        g = [[] for _ in range(n)]
        for x, y, w in edges:
            g[x].append((y, w))

        dis = [[inf] * (k + 1) for _ in range(n)]
        h = [(0, 0, 1)]  # (最短路长度, 节点编号, 最后连续相同字母个数)

        while h:
            d, x, cnt = heappop(h)
            if x == n - 1:
                return d
            if d > dis[x][cnt]:
                continue
            for y, w in g[x]:
                new_cnt = 1 if labels[y] != labels[x] else cnt + 1
                new_dis = d + w
                if new_cnt <= k and new_dis < dis[y][new_cnt]:
                    dis[y][new_cnt] = new_dis
                    heappush(h, (new_dis, y, new_cnt))

        return -1
''',
    call='Solution().shortestPath(5, [[0,1,1],[1,2,1],[2,4,1],[0,3,2],[3,4,5]], "aaabb", 2)',
    expect=7,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='table', var='dis', label='dis[节点][末尾连续个数 cnt]', h=270, cell=90,
             rows=lambda S: [f"{i}'{S['labels'][i]}'" for i in range(len(S['dis']))],
             cols=lambda S: [str(j) for j in range(len(S['dis'][0]))],
             cursors=[('x', 'cnt', 'yellow', '')],
             color=lambda S, i, j, v: 'green' if v != float('inf') else None),
        dict(type='heap', var='h', label='堆：(距离, 节点, cnt)', h=140, fmt=lambda t: f'{t[0]},{t[1]},{t[2]}'),
    ],
    skip=['heappush(h, (new_dis', 'g[x].append'],
    max_steps=60,
    watch=[('d', 'd', 'blue'), ('x', 'x', 'yellow'), ('cnt', 'cnt', 'pink'), 'k'],
    captions={
        'g = [[]': '邻接表，`g[x]` 存 `(y, w)`',
        'dis = [[inf]': '`dis[x][cnt]`：到 x、且末尾恰有 `cnt` 个连续相同字母的最短路。==cnt 就是分层图的层号==',
        'h = [(0, 0, 1)]': '起点：节点 0，距离 0，末尾连续个数 `1`（它自己）',
        'while h': '堆里还有状态 → 取距离最小的',
        'heappop': '弹出 `(距离 {d}, 节点 {x}, cnt={cnt})`',
        'if x == n - 1': lambda S, B, r: (f'到达终点 {S.x}：首次出堆即最短，答案 =={S.d}==' if S.x == S.n - 1 else f'节点 {S.x} 不是终点 {S.n - 1}，继续'),
        'if d > dis[x][cnt]': lambda S, B, r: (f'`{S.d} > dis[{S.x}][{S.cnt}] = {S.dis[S.x][S.cnt]}`：这是过期的旧元素（懒更新堆）→ 跳过' if S.d > S.dis[S.x][S.cnt]
                                               else f'`{S.d} > {S.dis[S.x][S.cnt]}` 不成立：状态有效，往后扩展'),
        'for y, w in g[x]': '走边 `{x} → {y}`，权重 `{w}`',
        'new_cnt = 1 if': lambda S, B, r: (f"标签 `{S.labels[S.y]}` ≠ `{S.labels[S.x]}`：断开，重新计数 → `new_cnt = 1`" if S.labels[S.y] != S.labels[S.x]
                                           else f"标签都是 `{S.labels[S.x]}`：连续 +1 → `new_cnt = {S.cnt} + 1 = {S.new_cnt}`"),
        'new_dis = d + w': '走到 y 的距离 `{d} + {w} = {new_dis}`',
        'if new_cnt <= k': lambda S, B, r: (f'`new_cnt = {S.new_cnt} > k = {S.k}`：连续字母超限 → 这条路不合法，丢弃' if S.new_cnt > S.k
                                            else (f'`{S.new_dis} < dis[{S.y}][{S.new_cnt}] = {S.dis[S.y][S.new_cnt]}` → 更短，更新并入堆' if S.new_dis < S.dis[S.y][S.new_cnt]
                                                  else f'`{S.new_dis}` 不比 `dis[{S.y}][{S.new_cnt}] = {S.dis[S.y][S.new_cnt]}` 小 → 不更新')),
        'dis[y][new_cnt] = new_dis': '`dis[{y}][{new_cnt}] = {new_dis}`',
        'return -1': '堆空仍没到终点 → 没有合法路径，返回 `-1`',
    },
    cards=dict(
        one_liner='状态 = (节点, 末尾连续相同字母个数)，在分层图上跑 Dijkstra',
        complexity='时间 `O(nk + mk·log(mk))`，空间 `O(nk + mk)`',
        problem=['有向带权图，每个节点有一个字母标签，路径的标签按序拼接成字符串',
                 '求节点 0 到 n−1 的最小边权和，要求拼接串里最多 `k` 个连续相同字符；不存在返回 `-1`',
                 '示例：标签 `aaabb`，`k=2` → `7`（走 0→3→4，拼出 `abb`）'],
        quote='定义 dis[x][cnt] 表示从节点 0 到节点 x 的最短路长度，满足路径中的最后连续相同字母个数为 cnt。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只看节点不够：同样到 x，末尾连续个数不同，后面能走的路不同 → ==cnt 也要进状态==',
              '走边 `x→y`：标签不同，cnt 重置为 1；相同，cnt+1，超过 `k` 就不能走',
              '边权为正 → Dijkstra；节点 `n-1` 首次出堆就是答案，直接返回'],
        summary=['时间 `O(nk + mk·log(mk))`，空间 `O(nk + mk)`',
                 '易错：起点 cnt 是 1，不是 0；`dis` 第二维开 `k + 1`',
                 '易错：用的是懒更新堆，弹出时要用 `d > dis[x][cnt]` 跳过过期元素',
                 '终点不管 cnt 是多少，只要首次出堆就是最短，不必遍历各层',
                 '同类：灵神题单「单源最短路 Dijkstra」中状态多一维的题'],
    ),
)
