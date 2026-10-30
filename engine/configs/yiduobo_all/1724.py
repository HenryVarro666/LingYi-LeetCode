_POS = {6: (0.5, 0.0), 0: (0.3, 0.33), 5: (0.8, 0.33), 1: (0.17, 0.66), 2: (0.45, 0.66), 3: (0.17, 1.0), 4: (0.45, 1.0)}
_TREE = [(6, 0), (6, 5), (0, 1), (0, 2), (1, 3), (2, 4)]
_W = {(6, 0): '∞', (6, 5): '∞', (0, 1): 2, (0, 2): 4, (1, 3): 5, (2, 4): 3}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '最小生成树（边上数字 = 权重，∞ = 超级树根的边）', 24, T['muted'], bold=True)
    W, H = x1 - x0 - 80, y1 - y0 - 150
    P = {k: (x0 + 40 + W * a, y0 + 70 + H * b) for k, (a, b) in _POS.items()}
    g = S.get('g')
    for a, b in _TREE:
        if g is not None and b not in g.get(a, {}):
            continue
        cv.line([P[a], P[b]], T['border'], 3)
        mx, my = (P[a][0] + P[b][0]) / 2, (P[a][1] + P[b][1]) / 2
        cv.text((mx + 14, my - 4), _W[(a, b)], 22, T['yellow'], anchor='lm', bold=True)
    pq = {}
    if 'p' in S and 'q' in S and 'limit' in S:
        pq = {S['p']: T['blue'], S['q']: T['pink']}
    for k, (x, y) in P.items():
        if g is not None and not g.get(k) and not any(k in v for v in g.values()):
            col = T['border']
        else:
            col = pq.get(k, T['dim'])
        cv.circle((x, y), 26, fill=col) if hasattr(cv, 'circle') else cv.rect((x - 26, y - 26, x + 26, y + 26), fill=col, r=26)
        cv.text((x, y), 'root' if k == 6 else k, 22 if k == 6 else 26, T['bg'], anchor='mm', bold=True)
    if pq:
        cv.text((x1 - 18, y1 - 6), f"limit = {S['limit']}：路径最大边权必须 < limit", 24, T['text'], anchor='rb', bold=True)


def _ftab(S):
    f = S.get('self.f')
    lv = S.get('self.level')
    if not f:
        return {}
    return {i: (lv[i], [(a, '∞' if d > 10 ** 9 else d) for a, d in row]) for i, row in enumerate(f)}


CONFIG = dict(
    num=1724, title='检查边长度限制的路径是否存在 II', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='最小生成树 + 倍增 LCA',
    tags=['灵神题单·图论算法'],
    code='''
class DistanceLimitedPathsExist(object):

    def __init__(self, n, edgeList):

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        fa = list(range(n + 1))
        g = {u : {} for u in range(n + 1)}
        for u, v, d in sorted(edgeList, key=lambda d:d[-1]):
            fa_u = find(u)
            fa_v = find(v)
            if fa_u != fa_v:
                if fa_u < fa_v:
                    fa[fa_u] = fa_v
                else:
                    fa[fa_v] = fa_u
        
                g[u][v] = g[v][u] = d

        max_dis = 10 ** 9 + 1
        for u in range(n):
            fa_u = find(u)
            if fa_u != n:
                g[n][u] = max_dis
                fa[fa_u] = n
        
        self.f = [[] for _ in range(n + 1)]
        self.level = [0] * (n + 1)
        q = [n]
        self.level[n] = 0
        head, tail = 0, 1
        while head < tail:
            for u in q[head : tail]:
                for v in g[u]:
                    if self.level[v] != 0:
                        continue
                    d = g[u][v]
                    self.f[v].append([u, d])
                    q.append(v)
                    self.level[v] = self.level[u] + 1
            
            head, tail = tail, len(q)

        p = 1
        while True:
            flag = True
            for u in range(n):
                if len(self.f[u]) >= p:
                    v = self.f[u][p - 1][0]
                    if len(self.f[v]) >= p:
                        t = self.f[v][p - 1][0]
                        d = max(self.f[u][p - 1][1], self.f[v][p - 1][1])
                        self.f[u].append([t, d])
                        flag = False
            
            if flag:
                break

            p += 1

    def query(self, p, q, limit):

        if self.level[p] < self.level[q]:
            p, q = q, p

        now = 0
        while self.level[p] != self.level[q]:
            i = len(self.f[p]) - 1
            while self.level[self.f[p][i][0]] < self.level[q]:
                i -= 1

            if self.f[p][i][1] >= limit:
                return False
            p = self.f[p][i][0]

        i = len(self.f[p]) - 1
        while p != q:
            while i >= len(self.f[p]) or (i > 0 and self.f[p][i][0] == self.f[q][i][0]):
                i -= 1
            
            if self.f[p][i][1] >= limit or self.f[q][i][1] >= limit:
                return False
            p = self.f[p][i][0]
            q = self.f[q][i][0]
        
        return True
''',
    call="""obj = DistanceLimitedPathsExist(6, [[0,1,2],[0,2,4],[1,3,5],[2,4,3]])
[obj.query(3, 2, 6), obj.query(3, 2, 5)]""",
    expect=[True, False],
    skip=['fa_u = find(u)', 'fa_v = find(v)', 'if fa_u != fa_v', 'if fa_u < fa_v', 'fa[fa_u] = fa_v', 'fa[fa_v] = fa_u',
          'if fa[x] != x', 'fa[x] = find(fa[x])', 'return fa[x]', 'for u in range(n):', 'if len(self.f[u]) >= p',
          'v = self.f[u][p - 1][0]', 'if len(self.f[v]) >= p', 't = self.f[v][p - 1][0]', 'd = max(', 'flag = False',
          'flag = True', 'if flag:', 'break', 'p += 1', 'for u in q[head : tail]', 'for v in g[u]',
          'if self.level[v] != 0', 'continue', 'd = g[u][v]', 'q.append(v)', 'head, tail = tail', 'if fa_u != n',
          'fa[fa_u] = n', 'def find', 'def __init__', 'now = 0', 'if self.level[p] < self.level[q]', 'max_dis = ', 'self.f = [[]',
          'self.level = [0]', 'q = [n]', 'self.level[n] = 0', 'head, tail = 0, 1', 'fa = list', 'g = {u'],
    views=[
        dict(type='custom', draw=_draw, h=380),
        dict(type='map', var=_ftab, fmt=lambda k, v: f'{k} 层{v[0]}: {v[1]}', h=270, label='f[u] = [(向上 2^level 步的节点, 路径最大边权)]', font=22),
    ],
    max_steps=110,
    watch=['u', 'v', 'p', 'q', 'limit'],
    captions={
        'for u, v, d in sorted': lambda S, B, r: ('4 条边都处理完，最小生成树建好了' if sum(len(x) for x in S.g.values()) == 8 else f'按边权从小到大取边 `({S.u}, {S.v})` 权重 `{S.d}`，并查集判断两端是否已连通'),
        'g[n][u] = max_dis': '`{u}` 所在的块还没挂到根上 → 加一条权重 `10^9+1` 的边连到超级树根 `{n}`，这样不连通的点也在同一棵树里',
        'g[u][v] = g[v][u] = d': '两端不连通 → 这条边进最小生成树：`g[{u}][{v}] = {d}`',
        'while head < tail': lambda S, B, r: ('从超级树根出发，按层 bfs，求每个点的父亲和层数' if S.head == 0 else ('bfs 结束，所有点都有了层数' if S.head >= S.tail else f'处理下一层：`q[{S.head}:{S.tail}]`')),
        'self.f[v].append([u, d])': '`f[{v}][0] = [{u}, {d}]`：`{v}` 往上走 `2^0` 步到父亲 `{u}`，边权 `{d}`',
        'self.level[v] =': '`level[{v}] = {self.level[v]}`：比父亲深一层',
        'p = 1': '开始倍增：`f[u][p]` 表示向上走 `2^p` 步，从 `p = 1` 开始',
        'while True': '`p = {p}`：用两个 `2^(p-1)` 步拼出 `2^p` 步',
        'self.f[u].append([t, d])': '`f[{u}][{p}]`：先走到 `{v}`，再走到 `{t}`，最大边权取两段的 `max` → `{d}`',
        'if self.level[p] < self.level[q]': '保证 `p` 是较深的一个：`level[p] = {self.level[p]}`，`level[q] = {self.level[q]}`',
        'while self.level[p] != self.level[q]': lambda S, B, r: (f'`level[{S.p}] = {S.self.level[S.p]}`，`level[{S.q}] = {S.self.level[S.q]}`：' + ('还没在同一层，先把 p 往上提' if S.self.level[S.p] != S.self.level[S.q] else '已在同一层')),
        71: '从最大的 `i = {i}` 开始，尝试一次跳 `2^i` 步',
        'while self.level[self.f[p][i][0]] < self.level[q]': lambda S, B, r: (f'跳 `2^{S.i}` 步会到 `{S.self.f[S.p][S.i][0]}`（层 {S.self.level[S.self.f[S.p][S.i][0]]}），比 `q` 的层 {S.self.level[S.q]} 还浅 → 跳太多了，`i` 减小' if S.self.level[S.self.f[S.p][S.i][0]] < S.self.level[S.q] else f'跳 `2^{S.i}` 步到 `{S.self.f[S.p][S.i][0]}`，不比 `q` 浅 → 这一步可以跳'),
        'i -= 1': '`i` → {i}',
        'if self.f[p][i][1] >= limit:': lambda S, B, r: f'这一跳路径上最大边权 `{S.self.f[S.p][S.i][1]}`，`limit = {S.limit}`：' + ('不小于 limit → 路径不满足，返回 False' if S.self.f[S.p][S.i][1] >= S.limit else '小于 limit，可以跳'),
        77: '`p` 跳到 `{p}`，深度和 `q` 一致',
        79: '深度对齐后，一起往上找最近公共祖先：从 `i = {i}` 开始',
        'while p != q': lambda S, B, r: ('`p == q`：已经走到同一个点（LCA）' if S.p == S.q else f'`p = {S.p}`，`q = {S.q}` 还不是同一个点'),
        'while i >= len(self.f[p])': lambda S, B, r: (f'`i = {S.i}`：两边跳 `2^{S.i}` 步都落在 `{S.self.f[S.p][S.i][0]}`，同一个点 → 可能越过 LCA，不能跳，`i` 减小' if (S.i >= len(S.self.f[S.p]) or (S.i > 0 and S.self.f[S.p][S.i][0] == S.self.f[S.q][S.i][0])) else f'`i = {S.i}`：跳 `2^{S.i}` 步后两边落点不同 → 可以跳'),
        'or self.f[q][i][1] >= limit': '两边这一跳的最大边权：`{f[p][i][1] if False else self.f[p][i][1]}` 和 `{self.f[q][i][1]}`，与 `limit = {limit}` 比较',
        86: '`p` 跳到 `{p}`',
        87: '`q` 跳到 `{q}`，两边落在同一个点：LCA 到了',
        'return False': '路径上有一条边 `>= limit` → ==返回 False==',
        'return True': '一路上所有边权都 `< limit` → ==返回 True==',
    },
    cards=dict(
        one_liner='先建最小生成树，再用倍增求路径最大边权',
        complexity='建树 `O(n log n)`，每次查询 `O(log n)`',
        problem=['无向图 n 个点，调用 `query(p, q, limit)`：是否存在 p 到 q 的路径，==所有边权都严格小于 limit==',
                 '必须在线回答（不能离线排序询问）',
                 '本视频：n = 6，边 `[0,1,2] [0,2,4] [1,3,5] [2,4,3]`，查询 `(3,2,6)` 与 `(3,2,5)`'],
        quote='对于本题，则需要提前将这颗最小生成树构造出来，然后对于每个询问，需要查询的就是这两个节点间的路径中权重最大的边是否小于limit。',
        quote_src='—— yiduobo 题解原文',
        idea=['最小生成树上两点路径的最大边权，是所有路径里最小的 → 它 `< limit` 就有解',
              '`f[u][i] = [向上 2^i 步的节点, 路径最大边权]`，用两段 `2^(i-1)` 拼出来',
              '查询：先把深的点提到同层，再两边一起跳，直到落点相同前一步',
              '不连通的点：加超级树根，边权 `10^9+1`'],
        summary=['时间：建树 `O(n log n)`，查询 `O(log n)`，空间 `O(n log n)`',
                 '`limit` 是严格小于：边权 `>= limit` 就返回 False（视频里 5 >= 5）',
                 '两边一起跳时，落点相同就不能跳，否则越过 LCA',
                 '原文为 Python 2 写法，`fa = range(n + 1)` 已改为 `list(range(n + 1))`（Python 3 的 range 不能赋值）'],
    ),
)
