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


POS = {1: (0.05, 0.15), 4: (0.05, 0.90), 2: (0.40, 0.15), 3: (0.72, 0.02), 5: (0.80, 0.75)}
EDGES = [(1, 2, 9), (2, 3, 3), (2, 5, 6), (1, 4, 7)]


def _draw(cv, S, B, box, T):
    vis = S.get('vis') or []
    seen = {i for i, b in enumerate(vis) if b}
    ans = S.get('ans')
    inner = S.get('_inner') or {}
    cur = inner.get('x') if 13 <= S.get('_line', 0) <= 17 else None
    best = ans if isinstance(ans, int) else None

    def ecol(e):
        if best is not None and e[2] == best and (e[0] in seen or e[1] in seen):
            return T['orange'], 7
        if e[0] in seen or e[1] in seen:
            return T['blue'], 5
        return T['border'], 4
    _graph(cv, box, T, '无向图（边上数字 = distance；绿 = 已访问，白环 = 当前点，橙边 = 目前最小的边）', POS, EDGES,
           lambda k: T['green'] if k in seen else None, ecol=ecol, elab=lambda e: e[2], ring=cur)


CONFIG = dict(
    num=2492, title='两个城市间路径的最小分数', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='DFS 遍历 1 所在连通块，取最小边', tags=['灵神题单·图论算法', '难度分 1680'],
    code='''
class Solution:
    def minScore(self, n: int, roads: List[List[int]]) -> int:
        g = [[] for _ in range(n + 1)]
        for x, y, dis in roads:
            g[x].append((y, dis))
            g[y].append((x, dis))

        vis = [False] * (n + 1)
        ans = inf

        def dfs(x: int) -> None:
            nonlocal ans
            vis[x] = True  # 避免重复访问
            for y, dis in g[x]:
                ans = min(ans, dis)
                if not vis[y]:
                    dfs(y)

        # 遍历节点 1 所在连通块
        dfs(1)
        return ans
''',
    call='Solution().minScore(5, [[1,2,9],[2,3,3],[2,5,6],[1,4,7]])',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', h=60, fn=lambda S: (f"连通块里目前见过的最小边：`ans = {S['ans']}`" if isinstance(S.get('ans'), int) else '')),
        dict(type='calls', h=210),
    ],
    watch=['x', 'y', 'dis', ('ans', 'ans', 'green')],
    captions={
        'g[y].append': '无向边 `{x}—{y}`，距离 `{dis}`：两个方向都记进邻接表',
        'vis = [False]': '`vis` 标记哪些城市已访问',
        'ans = inf': '`ans` 取连通块里最小的边，初值无穷大',
        'vis[x] = True': '访问城市 `{x}`，先标记，避免环上重复访问',
        'ans = min(ans, dis)': '`min({B.ans}, {dis}) = {ans}`：这条边在连通块里，==不管 y 访问过没有都要参与取最小==',
        'if not vis[y]': lambda S, B, r: (f'`{S.y}` 没访问过 → 递归进去' if not S.vis[S.y] else f'`{S.y}` 已访问过 → 不再递归（但上一行已经算过这条边）'),
        'dfs(y)': '递归到城市 `{y}`',
        'dfs(1)': '从城市 1 出发，把它所在连通块的所有边都扫一遍',
        'return ans': '1 所在连通块里最小的边就是答案 =={ans}==',
    },
    skip=['nonlocal ans'],
    max_steps=120,
    cards=dict(
        one_liner='路径能折返，1 所在连通块的每条边都能走到',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['`n` 个城市、双向道路 `roads[i] = [a, b, distance]`',
                 '路径的分数 = 路径上最小的道路距离，路径可重复走边',
                 '求城市 1 到城市 `n` 所有路径的最小分数',
                 '本例：`n=5` → `3`'],
        quote='由于路径可以折返，节点 1 所在连通块的每条边都可以在路径上，所以答案为节点 1 所在连通块中的最小的 distance_i。',
        quote_src='—— 灵茶山艾府题解',
        idea=['能折返：先走到某条边，绕一圈再回来，这条边就==进了路径==',
              '题目保证 1 与 `n` 连通，所以 `n` 也在同一个连通块',
              '问题变成：DFS 1 所在连通块，取边权最小值'],
        summary=['时间 `O(n + m)`，空间 `O(n + m)`',
                 '`ans = min(ans, dis)` 放在 `if not vis[y]` 之前：已访问点的边也要算',
                 '本例最小边 3 在支路 2—3 上，走过去再折返即可',
                 '思考题：每条边至多访问一次时，就不能折返了，是另一类问题'],
    ),
)
