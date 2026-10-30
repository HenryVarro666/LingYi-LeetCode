def _graph(cv, box, T, title, POS, EDGES, fill, label=None, ecol=None, elab=None, directed=False, ring=None):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 21, T['muted'], bold=True)
    Wd, Hd = x1 - x0 - 120, y1 - y0 - 110
    P = {k: (x0 + 60 + Wd * a, y0 + 66 + Hd * b) for k, (a, b) in POS.items()}
    R = 30
    for e in EDGES:
        a, b = e[0], e[1]
        col, wd = ecol(e) if ecol else (T['border'], 4)
        (ax, ay), (bx, by) = P[a], P[b]
        if directed:
            d = max(1.0, ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5)
            ux, uy = (bx - ax) / d, (by - ay) / d
            cv.arrow((ax + ux * R, ay + uy * R), (bx - ux * (R + 3), by - uy * (R + 3)), col, wd, head=16)
        else:
            cv.line([P[a], P[b]], col, wd)
        if elab:
            mx, my = (ax + bx) / 2, (ay + by) / 2
            s = elab(e)
            cv.rect((mx - 22, my - 16, mx + 22, my + 16), fill=T['bg'], r=8)
            cv.text((mx, my), s, 22, col, anchor='mm', bold=True)
    for k, (px, py) in P.items():
        f = fill(k)
        cv.rect((px - R, py - R, px + R, py + R), fill=f or T['panel2'], outline=T['border'], r=R)
        cv.text((px, py), k if label is None else label(k), 32, T['bg'] if f else T['muted'], anchor='mm', bold=True)
        if ring is not None and ring == k:
            cv.rect((px - R - 10, py - R - 10, px + R + 10, py + R + 10), outline=T['text'], width=5, r=R + 10)


PAL = ['blue', 'orange', 'purple', 'cyan', 'pink', 'green']
POS = {1: (0.05, 0.15), 4: (0.05, 0.90), 2: (0.40, 0.15), 3: (0.72, 0.02), 5: (0.80, 0.75)}
EDGES = [(1, 2, 9), (2, 3, 3), (2, 5, 6), (1, 4, 7)]


def _root(fa, x):
    while fa[x] != x:
        x = fa[x]
    return x


def _draw(cv, S, B, box, T):
    fa = S.get('fa')
    if not isinstance(fa, list):
        fa = list(range(6))
    roots = {k: _root(fa, k) for k in POS}
    size = {}
    for r in roots.values():
        size[r] = size.get(r, 0) + 1

    def fill(k):
        return T[PAL[roots[k] % 6]] if size[roots[k]] > 1 else None

    def ecol(e):
        if roots[e[0]] == roots[e[1]] and size[roots[e[0]]] > 1:
            return T[PAL[roots[e[0]] % 6]], 6
        return T['border'], 4
    _graph(cv, box, T, '无向图（同色 = 并查集里同一个集合；灰 = 还没被合并；边上数字 = distance）', POS, EDGES, fill, ecol=ecol,
           elab=lambda e: e[2])


CONFIG = dict(
    num=2492, title='两个城市间路径的最小分数', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='并查集 + 每个集合记录最小边', tags=['灵神题单·图论算法', '难度分 1680'],
    code='''
class Solution(object):
    def minScore(self, n, roads):

        fa = list(range(n + 1))
        score = {}

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        for x, y, v in roads:
            fa_x = find(x)
            fa_y = find(y)
            if fa_x != fa_y:
                fa[fa_x] = fa_y
                if fa_x in score:
                    v = min(v, score[fa_x])
            if fa_y in score:
                v = min(v, score[fa_y])
            score[fa_y] = v
        
        return score[find(1)]
''',
    call='Solution().minScore(5, [[1,2,9],[2,3,3],[2,5,6],[1,4,7]])',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=270),
        dict(type='array', var='fa', label='fa（父节点，fa[i] = i 表示是根）', h=170, pointers={}),
        dict(type='map', var='score', label='score（集合的根 → 该集合里最小的边）', fmt=lambda k, v: f'根 {k}：最小边 {v}', h=110),
        dict(type='calls', h=120),
    ],
    watch=['x', 'y', 'v', ('fa_x', 'fa_x', 'blue'), ('fa_y', 'fa_y', 'pink')],
    captions={
        'fa = list(range': '`fa[i]` 是 i 的父节点：一开始每个城市自成一个集合',
        'score = {}': '`score[根]` 记录这个集合里最小的边',
        'if fa[x] != x': lambda S, B, r: (f'`fa[{S.x}] = {S.fa[S.x]}` 不是自己 → 还不是根，继续往上找' if S.fa[S.x] != S.x else f'`fa[{S.x}] = {S.x}` 是自己 → ==找到根=='),
        'fa[x] = find(fa[x])': '递归找到根，顺便路径压缩：`fa[{x}]` 直接指向根 `{fa[x]}`',
        'return fa[x]': '`{x}` 所在集合的根是 `{ret}`',
        'fa_x = find(x)': '处理道路 `{x}—{y}`（距离 `{v}`）：先找 `{x}` 所在集合的根',
        'fa_y = find(y)': '`{x}` 的根是 `fa_x = {fa_x}`；再找 `{y}` 所在集合的根',
        'if fa_x != fa_y': lambda S, B, r: (f'根不同（`{S.fa_x}` ≠ `{S.fa_y}`）→ 两个集合要合并' if S.fa_x != S.fa_y else f'根相同（都是 `{S.fa_x}`）→ 已在同一集合，不用合并'),
        'fa[fa_x] = fa_y': '合并：`{fa_x}` 挂到 `{fa_y}` 下',
        'if fa_x in score': lambda S, B, r: (f'被合并的集合记过最小边 `{S.score[S.fa_x]}` → 要带过来' if S.fa_x in S.score else '被合并的集合还没有记录'),
        'v = min(v, score[fa_x])': '`v` 取新边与旧集合最小边的较小者 → ==`{v}`==',
        'if fa_y in score': lambda S, B, r: (f'目标集合已有最小边 `{S.score[S.fa_y]}` → 再比较' if S.fa_y in S.score else '目标集合还没有记录，新边就是最小'),
        'v = min(v, score[fa_y])': '`v` 取较小者 → ==`{v}`==',
        'score[fa_y] = v': '`score[{fa_y}] = {v}`：合并后这个集合里最小的边',
        'return score[find(1)]': '所有边处理完：先 `find(1)` 找到 1 的根，再取这个集合的最小边（路径可折返，整个集合的边都走得到）',
    },
    result='城市 1 所在集合的最小边 `score[find(1)] = 3`，即答案 ==3==',
    max_steps=120,
    cards=dict(
        one_liner='路径可重复走边：1 所在集合的最小边就是答案',
        complexity='时间 `O(m α(n))`，空间 `O(n)`',
        problem=['`n` 个城市，双向道路 `[a, b, distance]`，路径的分数 = 路上最小的距离',
                 '路径可以重复经过同一条边，求城市 1 到 `n` 的最小分数',
                 '本例：`n=5` → `3`'],
        quote='两个城市间的路径实际上包含了其所在连通块中的所有边，那么在这里只需要遍历所有的边，使用并查集求出图中所有的连通块，并在求解过程中记录每个连通块中值最小的边。',
        quote_src='—— yiduobo 题解原文',
        idea=['能重复走边 → 连通块里每条边都能纳入路径',
              '不建图，直接用并查集边读边合并',
              '每个集合的根上记一个 `score`：合并时取两边和新边的最小值'],
        summary=['时间近似 `O(m)`（路径压缩），空间 `O(n)`',
                 '合并前要先把被挂走的根 `fa_x` 的 `score` 带上',
                 '最后用 `find(1)` 取根再查 `score`，别直接 `score[1]`',
                 '原文为 Python 2 写法，`fa = range(n + 1)` 已改为 `list(range(n + 1))`（Python 3 的 range 不能赋值）',
                 '对比灵神：灵神用 DFS 扫 1 所在连通块，yiduobo 用并查集一次遍历所有边'],
    ),
)
