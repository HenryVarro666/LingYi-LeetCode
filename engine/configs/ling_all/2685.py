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


POS = {0: (0.05, 0.12), 1: (0.30, 0.12), 2: (0.17, 0.88), 3: (0.60, 0.12), 4: (0.52, 0.88), 5: (0.92, 0.88)}
EDGES = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5)]
COMP = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1}
PAL = ['green', 'orange', 'cyan']


def _draw(cv, S, B, box, T):
    vis = S.get('vis') or []
    seen = {i for i, b in enumerate(vis) if b}
    ln = S.get('_line', 0)
    inner = S.get('_inner') or {}
    cur = inner.get('x') if 'x' in inner and 10 <= ln <= 18 else None
    _graph(cv, box, T, '无向图（染色 = 已访问，同色 = 同一连通块，白环 = DFS 正在访问的点）', POS, EDGES,
           lambda k: T[PAL[COMP[k]]] if k in seen else None, ring=cur,
           ecol=lambda e: ((T[PAL[COMP[e[0]]]], 5) if e[0] in seen and e[1] in seen else (T['border'], 4)))


CONFIG = dict(
    num=2685, title='统计完全连通分量的数量', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='DFS 数点数与边数：e == v(v-1)', tags=['灵神题单·图论算法', '难度分 1769'],
    code='''
class Solution:
    def countCompleteComponents(self, n: int, edges: List[List[int]]) -> int:
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        vis = [False] * n

        def dfs(x: int) -> None:
            nonlocal v, e
            v += 1
            e += len(g[x])

            vis[x] = True
            for y in g[x]:
                if not vis[y]:
                    dfs(y)

        ans = 0
        for i, b in enumerate(vis):
            if not b:
                v = e = 0
                dfs(i)
                ans += e == v * (v - 1)
        return ans
''',
    call='Solution().countCompleteComponents(6, [[0,1],[0,2],[1,2],[3,4],[3,5]])',
    expect=1,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='text', h=80, fn=lambda S: (f"当前连通块：点数 `v = {S['v']}`，度数之和 `e = {S['e']}`；完全图要求 `e == v×(v−1) = {S['v'] * (S['v'] - 1)}`" if isinstance(S.get('v'), int) and isinstance(S.get('e'), int) else '')),
        dict(type='calls', h=200),
    ],
    watch=['i', ('v', 'v', 'blue'), ('e', 'e', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'g[y].append(x)': '无向边 `{x}—{y}`：两个方向都记进邻接表',
        'vis = [False]': '`vis` 标记哪些点已访问',
        'v += 1': '访问点 `{x}`：连通块点数 `v = {v}`',
        'e += len(g[x])': '`{x}` 有 `{len(g[x])}` 个邻居 → `e` 加 `{len(g[x])}`，`e = {e}`（==一条边被两端各数一次==）',
        'vis[x] = True': '标记 `{x}` 已访问',
        'if not vis[y]': lambda S, B, r: (f'邻居 `{S.y}` 没访问过 → 递归' if not S.vis[S.y] else f'邻居 `{S.y}` 已访问，跳过'),
        'dfs(y)': '递归进入 `{y}`',
        'ans = 0': '`ans` 统计完全连通分量个数',
        'v = e = 0': '点 `{i}` 没访问过 → 新连通块，`v`、`e` 清零',
        'dfs(i)': '从点 `{i}` DFS，把整个连通块走一遍，数点数和度数之和',
        'ans += e == v * (v - 1)': lambda S, B, r: (f'`e = {S.e}`，`v(v-1) = {S.v * (S.v - 1)}`：' +
                                                    ('==相等 → 完全图==，`ans = %d`' % S.ans if S.e == S.v * (S.v - 1) else '不相等 → 有点对之间缺边，不计入')),
        'return ans': '共 =={ans}== 个完全连通分量',
    },
    skip=['nonlocal v, e'],
    max_steps=140,
    cards=dict(
        one_liner='DFS 数出点数 v 和边数，完全图的边数必为 v(v-1)/2',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['无向图，`n` 个点，`edges` 是边',
                 '连通分量里每对点之间都有边，就是==完全连通分量==',
                 '求完全连通分量的个数',
                 '本例：`n=6` → `1`（只有 `{0,1,2}`）'],
        quote='每访问一个点 x，就把 v 加一，把 e 加上点 x 的邻居个数（注意同一条边会被计入两次）。……所以实际代码中的判断条件是 e 是否等于 v(v-1)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['DFS 每个连通块，累计点数 `v` 和各点邻居数之和 `e`',
              '`v` 个点的完全图有 `v(v-1)/2` 条边',
              '`e` 把每条边算了两次，所以直接比较 `e == v*(v-1)`'],
        summary=['时间 `O(n + m)`，空间 `O(n + m)`',
                 '`e` 是度数之和 = 边数 × 2，别拿它直接和 `v(v-1)/2` 比',
                 '孤立点：`v=1, e=0`，`0 == 1×0`，也算完全连通分量',
                 '`ans += e == v * (v - 1)` 利用了布尔值加到整数上',
                 '本例 `{3,4,5}` 缺边 `4—5`：`e = 4 ≠ 6`，不计入'],
    ),
)
