PAL = ['blue', 'orange', 'purple']
COMP = {0: 0, 2: 0, 4: 0, 5: 0, 1: 1, 6: 1, 3: 2}
POS = {0: (0.08, 0.22), 2: (0.30, 0.22), 5: (0.08, 0.80), 4: (0.30, 0.80), 1: (0.55, 0.22), 6: (0.55, 0.80), 3: (0.82, 0.50)}
EDGES = [(0, 2), (0, 5), (2, 4), (5, 4), (1, 6)]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '无向图（染色 = 已访问，同色 = 同一个连通块，白环 = 当前正在访问的点）', 21, T['muted'], bold=True)
    W, H = x1 - x0 - 80, y1 - y0 - 100
    P = {k: (x0 + 40 + W * a, y0 + 64 + H * b) for k, (a, b) in POS.items()}
    for a, b in EDGES:
        cv.line([P[a], P[b]], T['border'], 4)
    seen = {i for i, v in enumerate(S.get('vis') or []) if v}
    cur = (S.get('_inner') or {}).get('x') if 10 <= S.get('_line', 0) <= 15 else None
    for k, (px, py) in P.items():
        on = k in seen
        fill = T[PAL[COMP[k]]] if on else T['panel2']
        cv.rect((px - 34, py - 34, px + 34, py + 34), fill=fill, outline=T['border'], r=34)
        cv.text((px, py), k, 34, T['bg'] if on else T['muted'], anchor='mm', bold=True)
        if k == cur:
            cv.rect((px - 44, py - 44, px + 44, py + 44), outline=T['text'], width=5, r=44)


CONFIG = dict(
    num=2316, title='统计无向图中无法互相到达点对数', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='DFS 求连通块大小 + 乘法原理', tags=['灵神题单·图论算法', '灵神题单·数学算法', '难度分 1604'],
    code='''
class Solution:
    def countPairs(self, n: int, edges: List[List[int]]) -> int:
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)  # 建图

        vis = [False] * n
        def dfs(x: int) -> int:
            vis[x] = True  # 避免重复访问同一个点
            size = 1
            for y in g[x]:
                if not vis[y]:
                    size += dfs(y)
            return size

        ans = total = 0
        for i in range(n):
            if not vis[i]:  # 未访问的点：说明找到了一个新的连通块
                size = dfs(i)
                ans += size * total
                total += size
        return ans
''',
    call='Solution().countPairs(7, [[0,2],[0,5],[2,4],[1,6],[5,4]])',
    expect=14,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='text', h=60, fn=lambda S: (f"已有连通块共 `total = {S['total']}` 个点，累计无法互通的点对 `ans = {S['ans']}`" if 'total' in S else '')),
        dict(type='calls', h=220),
    ],
    watch=['i', 'size', ('total', 'total', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'g[y].append(x)': '无向边 `{x}—{y}`：两个方向都记进邻接表',
        'vis = [False]': '`vis` 标记哪些点已经访问过',
        'ans = total = 0': '`total` 是前面连通块的点数之和，`ans` 是答案',
        'if not vis[i]': lambda S, B, r: (f'点 `{S.i}` 还没访问 → 说明找到了==新的连通块==' if not S.vis[S.i] else f'点 `{S.i}` 已经属于某个连通块，跳过'),
        'size = dfs(i)': '从点 `{i}` 出发 DFS，把它所在连通块走一遍，数出大小',
        'vis[x] = True': '访问点 `{x}`，标记已访问，避免重复',
        'size += dfs(y)': '邻居 `{y}` 没访问过，递归进去，把它那一片的大小加进来 → `size = {size}`',
        'ans += size * total': '新块的每个点 × 前面所有点都无法互通：`{size} × {total} = {size * total}` → `ans = {ans}`',
        'total += size': '把这个块并入「前面的点」：`total = {total}`',
        'return size': lambda S, B, r: f'`dfs({S.x})` 返回 `size = {r}`',
        'return ans': '所有连通块处理完，无法互相到达的点对共 =={ans}==',
    },
    skip=['size = 1'],
    max_steps=120,
    cards=dict(
        one_liner='每找到一个连通块，它和前面所有点两两不通',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['`n` 个点的无向图，`edges` 是边，问有多少对点互相无法到达',
                 '同一连通块内能互通，不同连通块之间不能',
                 '示例：`n=7, edges=[[0,2],[0,5],[2,4],[1,6],[5,4]]` → `14`'],
        quote='设当前连通块的大小为 size，那么这个连通块中的每个点，与前面遍历过的连通块的每个点，都是无法互相到达的，根据乘法原理，这有 size·total 个，加到答案中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['DFS 遍历，每次从未访问的点出发，就找到一个新的连通块',
              '`total` 维护已处理连通块的点数之和',
              '新块大小 `size`，贡献 `size * total` 对，再并入 `total`'],
        summary=['时间 `O(n + m)`，空间 `O(n + m)`（建图 + 递归栈）',
                 '本例：块大小依次 4、2、1 → `2×4 + 1×6 = 14`',
                 '易错：先 `ans += size * total`，再 `total += size`，顺序不能反',
                 'n 很大时递归可能很深，Python 要注意递归深度',
                 '同类题：547 朋友圈（数连通块）'],
    ),
)
