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
    return '-' if v == -1 else v


def _draw(cv, S, B, box, T):
    es = sorted(_edges_of(S))
    old = _edges_of(B)
    dis = S.get('dis')
    vis = S.get('vis')
    line = S.get('_line')
    p = S.get('p') if dis is not None and S.get('p', -1) != -1 and line is not None and line >= SEL_P else None
    i = S.get('i') if line in (REL, REL + 1) else None
    n1, n2 = S.get('node1'), S.get('node2')
    new = {e for e in es if B.get('self.g') is not None and e not in old and 'node1' not in S}

    def ncol(u):
        if p is not None and u == p and line >= REL - 1:
            return T['blue']
        if vis is not None and vis[u]:
            return T['green']
        if dis is not None and dis[u] != -1:
            return T['orange']
        return T['panel2']

    def nsub(u):
        return None if dis is None else f'dis={_fmt(dis[u])}'

    def ecol(u, v):
        if p is not None and i is not None and (u, v) == (p, i):
            return T['yellow'], 6
        if any(e[0] == u and e[1] == v for e in new):
            return T['green'], 6
        return T['dim'], 3

    _graph(cv, T, box, POS, es, ncol, nsub, ecol, '有向图（绿 = 已定最短路，橙 = 有暂定值，蓝 = 本轮选中的点，黄边 = 正在松弛）')
    if n1 is not None:
        cv.text((box[0] + 18, box[3] - 8), f'查询：{n1} → {n2}', 22, T['yellow'], bold=True, anchor='lb')


def _text(S, B):
    if 'node1' in S and 'dis' in S:
        return f"求 `{S['node1']}` 到 `{S['node2']}`，`-1` 表示还没有路 / 没有边"
    if 'node1' in S:
        return f"求 `{S['node1']}` 到 `{S['node2']}` 的最短路"
    return '邻接矩阵 `g[x][y]`：边权，`-1` 表示没有边'


CODE = '''
class Graph(object):

    def __init__(self, n, edges):
        self.n = n
        self.g = [[-1] * n for _ in range(n)]
        for x, y, v in edges:
            self.g[x][y] = v

    def addEdge(self, edge):
        x, y, v = edge
        self.g[x][y] = v

    def shortestPath(self, node1, node2):

        dis = self.g[node1][:]
        dis[node1] = 0
        vis = [False] * self.n
        vis[node1] = True

        while True:
            p = -1
            mi = -1
            for i in range(self.n):
                if not vis[i] and dis[i] != -1 and (mi == -1 or mi > dis[i]):
                    p = i
                    mi = dis[i]
            
            if p == -1:
                break
            
            vis[p] = True
            for i in range(self.n):
                if self.g[p][i] != -1 and (dis[i] == -1 or dis[i] > dis[p] + self.g[p][i]):
                    dis[i] = dis[p] + self.g[p][i]

        return dis[node2]
'''
_L = CODE.strip('\n').split('\n')
SEL_P = next(i + 1 for i, l in enumerate(_L) if 'if p == -1' in l)
REL = next(i + 1 for i, l in enumerate(_L) if 'if self.g[p][i] != -1' in l)


def _sel(S, B, r):
    i = S.i
    if S.vis[i]:
        return f'`{i}` 已经定过最短路 → 不选'
    if S.dis[i] == -1:
        return f'`dis[{i}] = -1`：还没有路到它 → 不选'
    if S.mi == -1 or B.mi == -1 or B.mi > S.dis[i]:
        return f'`dis[{i}] = {S.dis[i]}`：未定且是目前最小 → 选它做候选 `p = {i}`'
    return f'`dis[{i}] = {S.dis[i]}` 不比 `mi = {B.mi}` 小 → 不换'


def _relax(S, B, r):
    p, i = S.p, S.i
    w = S['self.g'][p][i]
    if w == -1:
        return f'`{p} → {i}` 没有边（`-1`），跳过'
    head = f'`{p} → {i}` 有边，权 `{w}`；'
    if S.dis[i] == -1:
        return head + f'`dis[{i}] = -1` 还没有路 → ==更新=='
    if S.dis[i] > S.dis[p] + w:
        return head + f'`{S.dis[i]} > {S.dis[p]} + {w}`，经 `{p}` 更短 → ==更新=='
    return head + f'`dis[{i}] = {S.dis[i]}` 不比经 `{p}` 的 `{S.dis[p] + w}` 长 → 不更新'


CONFIG = dict(
    num=2642, title='设计可以求最短路径的图类', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='邻接矩阵 + 朴素 Dijkstra（不用堆）',
    tags=['灵神题单·图论算法', '难度分 1811'],
    code=CODE,
    call='''g = Graph(4, [[0, 2, 5], [0, 1, 2], [1, 2, 1], [3, 0, 3]])
out = [g.shortestPath(1, 3)]
g.addEdge([2, 3, 1])
out.append(g.shortestPath(1, 3))
out''',
    expect=[-1, 2],
    skip=['self.n = n', 'for x, y, v in edges', 'p = -1', 'mi = -1', 'for i in range(self.n)', 'p = i', 'mi = dis[i]', 'x, y, v = edge'],
    max_steps=110,
    views=[
        dict(type='text', fn=_text, h=56, size=24),
        dict(type='custom', draw=_draw, h=340),
        dict(type='array', var=lambda S: [_fmt(v) for v in S['dis']] if 'dis' in S else None, label='dis[i]：起点到 i 的当前最短路（- = 没有路）', h=150, cell=90,
             color=lambda S, i, v: 'green' if 'vis' in S and S['vis'][i] else None),
    ],
    watch=[('node1', 'node1', 'green'), ('node2', 'node2', 'pink'), ('p', 'p', 'blue'), ('mi', 'mi', 'orange'), ('i', 'i', 'yellow')],
    captions={
        'self.g = [[-1]': '邻接矩阵：`g[x][y]` 是边权，`-1` 表示没有这条边',
        'self.g[x][y] = v': lambda S, B, r: f'`g[{S.x}][{S.y}] = {S.v}`：{"加边" if "node1" not in S else ""}',
        'dis = self.g[node1][:]': '起点那一行当初始距离：`dis = g[{node1}]` = `{dis}`，能直达的点有暂定值',
        'dis[node1] = 0': '起点到自己 `0`',
        'vis = [False]': '`vis[i]`：是否已定下最短路',
        'vis[node1] = True': '起点已定',
        'while True': '开始一轮：选一个==未定且 dis 最小==的点',
        'if not vis[i]': _sel,
        'if p == -1': lambda S, B, r: ('没有可选的点了：能到的点都定完 → 结束' if S.p == -1 else f'这轮选中 `p = {S.p}`，`dis[{S.p}] = {S.mi}` 是未定点里最小'),
        'break': '循环结束',
        'vis[p] = True': '`p = {p}` 的最短路就此确定：==dis 最小的未定点不可能被别的点再缩短==（边权为正）',
        'if self.g[p][i] != -1': _relax,
        'dis[i] = dis[p] + self.g[p][i]': '更新 `dis[{i}]` = =={dis[i]}==',
        'return dis[node2]': '返回 `dis[{node2}]` = `{dis[node2]}`：==-1 就是没有路==',
    },
    cards=dict(
        one_liner='边数接近 n 的平方，不用堆：用矩阵直接选最小的点',
        complexity='`addEdge` `O(1)`，`shortestPath` `O(n^2)`',
        problem=['有向带权图，`addEdge` 加边，`shortestPath(a, b)` 查最短路，没有路返回 `-1`',
                 '示例：`n=4`，边 `[[0,2,5],[0,1,2],[1,2,1],[3,0,3]]`',
                 '本视频：先查 `1→3` 得 `-1`（3 只有出边），加边 `2→3` 后再查得 `2`'],
        quote='由于本题的图中边的规模达到了点规模的平方，因此在这里可以直接使用临接矩阵来储存这张图，同时不应该使用二叉堆优化，而是应该使用最原始的dijkstra算法来求最短路。',
        quote_src='—— yiduobo 题解原文',
        idea=['新增边后很难增量维护所有点对距离，但 `n` 很小',
              '每次询问对一个点跑一遍 Dijkstra，边权为正',
              '邻接矩阵 + 每轮线性扫描找 dis 最小的未定点，不需要堆'],
        summary=['`addEdge` `O(1)`，`shortestPath` `O(n^2)`，空间 `O(n^2)`',
                 '`-1` 同时表示「没有边」和「还没有路」，比较时要先判 `-1`',
                 '起点那一行 `dis = g[node1][:]` 是浅拷贝，别改到矩阵本身',
                 '对比灵神：灵神用邻接表 + 堆，并且在出堆是终点时提前返回；这里不提前返回，跑完全部点'],
    ),
)
