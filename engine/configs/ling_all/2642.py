import math as _m


def _graph(cv, T, box, pos, edges, ncol, nsub, ecol, title, directed=True):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    R = 30
    L, Rr, Tp, Bt = x0 + 70, x1 - 70, y0 + 70 + R, y1 - R - 34
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
    for u, (px, py) in pos.items():
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

POS = {3: (0.02, 0.62), 0: (0.34, 0.24), 1: (0.68, 0.04), 2: (0.68, 0.96)}


def _edges_of(S):
    g = S.get('self.g')
    out = set()
    if g is None:
        return out
    for x, row in enumerate(g):
        if isinstance(row, list) and row and isinstance(row[0], tuple):
            for y, w in row:
                out.add((x, y, w))
        elif isinstance(row, list):
            for y, w in enumerate(row):
                if w not in (-1, float('inf')) and x != y and not isinstance(w, tuple):
                    out.add((x, y, w))
    return out

def _fmt(v):
    return '∞' if v == _m.inf else v


def _draw(cv, S, B, box, T):
    es = sorted(_edges_of(S))
    old = _edges_of(B)
    dis = S.get('dis')
    line = S.get('_line')
    cur = S.get('x') if 'h' in S and 'd' in S else None
    y = S.get('y') if line in (REL, REL + 1, REL + 2) else None
    start, end = S.get('start'), S.get('end')
    new = {e for e in es if B.get('self.g') is not None and e not in old and 'start' not in S}

    def ncol(u):
        if u == cur:
            return T['blue']
        if dis is not None and dis[u] != _m.inf:
            return T['orange'] if u != start else T['green']
        return T['panel2']

    def nsub(u):
        if dis is None:
            return None
        return f'dis={_fmt(dis[u])}'

    def ecol(u, v):
        if y is not None and (u, v) == (cur, y):
            return T['yellow'], 6
        if any(e[0] == u and e[1] == v for e in new):
            return T['green'], 6
        return T['dim'], 3

    _graph(cv, T, box, POS, es, ncol, nsub, ecol, '有向图（蓝 = 刚出堆，橙 = 已有最短路，黄边 = 正在松弛，绿边 = 新加的边）')
    if start is not None:
        cv.text((box[0] + 18, box[3] - 8), f'查询：{start} → {end}', 22, T['yellow'], bold=True, anchor='lb')


def _text(S, B):
    line = S.get('_line')
    if 'd' in S and 'start' in S and 'x' in S and 'h' in S:
        return f"出堆 `({S['d']}, {S['x']})`，起点 `{S['start']}` 到终点 `{S['end']}`"
    if 'start' in S:
        return f"求 `{S['start']}` 到 `{S['end']}` 的最短路"
    return '邻接表 `self.g[x]` 存 `(y, w)`'


def _rel(S, B, r):
    if S.d + S.w < S.dis[S.y]:
        return f'`{S.d} + {S.w} = {S.d + S.w} < dis[{S.y}] = {_fmt(S.dis[S.y])}`：==更短=='
    return f'`{S.d} + {S.w} = {S.d + S.w} >= dis[{S.y}] = {S.dis[S.y]}`：不更短'


CODE = '''
class Graph:
    def __init__(self, n: int, edges: List[List[int]]):
        self.g = [[] for _ in range(n)]  # 邻接表
        for x, y, w in edges:
            self.g[x].append((y, w))

    def addEdge(self, e: List[int]) -> None:
        self.g[e[0]].append((e[1], e[2]))

    def shortestPath(self, start: int, end: int) -> int:
        dis = [inf] * len(self.g)  # dis[i] 表示从起点 start 出发，到节点 i 的最短路长度
        dis[start] = 0
        h = [(0, start)]
        while h:
            d, x = heappop(h)
            if x == end:  # 计算出从起点到终点的最短路长度
                return d
            if d > dis[x]:  # x 之前出堆过，无需更新邻居的最短路
                continue
            for y, w in self.g[x]:
                if d + w < dis[y]:
                    dis[y] = d + w  # 更新最短路长度
                    heappush(h, (dis[y], y))
        return -1  # 无法到达终点
'''
_L = CODE.strip('\n').split('\n')
REL = next(i + 1 for i, l in enumerate(_L) if 'for y, w in self.g[x]' in l)

CONFIG = dict(
    num=2642, title='设计可以求最短路径的图类', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='邻接表 + 堆优化 Dijkstra（写法二）',
    tags=['灵神题单·图论算法', '难度分 1811'],
    code=CODE,
    call='''g = Graph(4, [[0, 2, 5], [0, 1, 2], [1, 2, 1], [3, 0, 3]])
out = [g.shortestPath(0, 3)]
g.addEdge([1, 3, 4])
out.append(g.shortestPath(0, 3))
out''',
    expect=[-1, 6],
    skip=['for x, y, w in edges', 'dis[start] = 0', 'h = [(0, start)]'],
    max_steps=90,
    views=[
        dict(type='text', fn=_text, h=56, size=24),
        dict(type='custom', draw=_draw, h=340),
        dict(type='array', var=lambda S: [_fmt(v) for v in S['dis']] if 'dis' in S else None, label='dis[i]：起点到 i 的最短路（∞ = 未到过）', h=150, cell=90,
             color=lambda S, i, v: 'blue' if 'x' in S and 'h' in S and i == S['x'] else None),
        dict(type='heap', var='h', label='h（最小堆，元素 = (最短路, 节点)）', h=120, fmt=lambda t: f'({t[0]},{t[1]})'),
    ],
    watch=[('start', 'start', 'green'), ('end', 'end', 'pink'), ('d', 'd', 'blue'), ('x', 'x', 'blue'), ('y', 'y', 'yellow'), ('w', 'w')],
    captions={
        'self.g = [[] for': '建邻接表：`g[x]` 存从 x 出发的边 `(y, w)`',
        'self.g[x].append': '加边 `{x} → {y}`，权 `{w}`',
        'self.g[e[0]].append': '`addEdge`：直接把新边挂进邻接表，==O(1)==：`{e[0]} → {e[1]}`，权 `{e[2]}`',
        'dis = [inf] * len': '每次查询都重新跑一遍：`dis` 全设 ∞',
        'while h': lambda S, B, r: '堆非空，继续' if S.h else '堆空了，终点没出过堆',
        'd, x = heappop': '弹出堆顶 `({d}, {x})`：==最短路最小==的节点',
        'if x == end': lambda S, B, r: (f'`x = {S.x}` 就是终点：==出堆即最短路==，提前返回' if S.x == S.end else f'`x = {S.x}` 不是终点 `{S.end}`'),
        'return d': '返回最短路长度 `{d}`',
        'if d > dis[x]': lambda S, B, r: (f'`{S.d} > dis[{S.x}] = {S.dis[S.x]}`：x 之前出堆过，旧记录' if S.d > S.dis[S.x] else f'`{S.d} == dis[{S.x}]`：首次出堆，去更新邻居'),
        'continue': '旧记录，跳过',
        'for y, w in self.g[x]': lambda S, B, r: (f'`{S.x}` 的出边看完了' if 'y' in B and (B.x, B.y, B.w) == (S.x, S.y, S.w) else f'看出边 `{S.x} → {S.y}`，权 `{S.w}`'),
        'if d + w < dis[y]': _rel,
        'dis[y] = d + w': '更新最短路：`dis[{y}]` = =={dis[y]}==',
        'heappush': '`({dis[y]}, {y})` 入堆',
        'return -1': '堆空了仍没出过终点 → ==无法到达==，返回 `-1`',
    },
    cards=dict(
        one_liner='加边只改邻接表，每次查询现跑一遍 Dijkstra',
        complexity='`addEdge` `O(1)`，`shortestPath` `O(n + m log m)`',
        problem=['有向带权图，支持 `addEdge` 加边、`shortestPath(a, b)` 查最短路，不通返回 `-1`',
                 '示例：`n=4`，边 `[[0,2,5],[0,1,2],[1,2,1],[3,0,3]]`',
                 '本视频：先查 `0→3` 得 `-1`（没有路），加边 `1→3` 后再查 `0→3` 得 `6`'],
        quote='对于 addEdge，直接把边加入图中即可。对于 shortestPath，用 Dijkstra 算法计算从起点 start 到终点 end 的最短路长度。',
        quote_src='—— 灵茶山艾府题解 · 方法一',
        idea=['邻接表建图：`addEdge` 一步到位',
              '`shortestPath` 用堆优化 Dijkstra，出堆是终点就提前返回',
              '没出过终点堆就空了 → `-1`'],
        summary=['写法二：邻接表 + 堆，`shortestPath` `O(n + m log m)`；稠密图可用写法一邻接矩阵朴素 Dijkstra `O(n^2)`',
                 '方法二 Floyd：查询 `O(1)`，加边 `O(n^2)`，适合查询特别多的场景',
                 '`addEdge` 调用多时选方法一，`shortestPath` 调用多时选 Floyd',
                 '易错：堆里会有重复节点，出堆要判 `d > dis[x]`'],
    ),
)
