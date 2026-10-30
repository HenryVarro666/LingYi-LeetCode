import math


def _ln(code, sub):
    """1-based line number of the first code line containing sub (leading blank line stripped)"""
    for k, s in enumerate(code.strip('\n').split('\n')):
        if sub in s:
            return k + 1
    return -1


def _gdraw(cv, box, T, pos, E, node_fn, edge_fn, label_fn=None, title='', directed=True, R=30, base=0, above=None, elabel=None, left=None):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    w = x1 - x0 - 140
    h = y1 - y0 - 195
    P = [(x0 + 70 + fx * w, y0 + 100 + fy * h) for fx, fy in pos]
    es = set(E)
    for (a, b) in E:
        col, wd = edge_fn(a, b)
        (ax, ay), (bx, by) = P[a], P[b]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        off = 10 if (b, a) in es else 0
        nx, ny = -uy * off, ux * off
        p0 = (ax + ux * R + nx, ay + uy * R + ny)
        p1 = (bx - ux * (R + 2) + nx, by - uy * (R + 2) + ny)
        if elabel:
            t = elabel(a, b)
            if t:
                mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
                cv.text((mx + nx * 2.2 + 6, my + ny * 2.2 - 4), t, 20, col, anchor='lb', bold=True)
        if directed:
            cv.arrow(p0, p1, col, wd, head=16)
        else:
            cv.line([p0, p1], col, wd)
    for i, (x, y) in enumerate(P):
        fill, tc, ring = node_fn(i)
        cv.rect((x - R, y - R, x + R, y + R), fill=fill, r=R, outline=ring or T['border'], width=5 if ring else 1)
        cv.text((x, y), i + base, 26, tc, anchor='mm', bold=True)
        if label_fn:
            lab = label_fn(i)
            if lab:
                if left and left(i):
                    cv.text((x - R - 8, y), lab[0], 21, lab[1], anchor='rm', bold=True)
                elif above and above(i):
                    cv.text((x, y - R - 6), lab[0], 21, lab[1], anchor='mb', bold=True)
                else:
                    cv.text((x, y + R + 8), lab[0], 21, lab[1], anchor='mt', bold=True)


G = [1, 2, 0, 0, 3, 4, 7, 6]
POS = [(0.3, 0.4), (0.5, 0.05), (0.7, 0.4), (0.3, 0.9), (0.15, 0.9), (0.0, 0.9), (0.93, 0.1), (0.93, 0.8)]
CODE = '''
class Solution:
    def countVisitedNodes(self, g: List[int]) -> List[int]:
        n = len(g)
        rg = [[] for _ in range(n)]  # 反图
        deg = [0] * n
        for x, y in enumerate(g):
            rg[y].append(x)
            deg[y] += 1

        # 拓扑排序，剪掉 g 上的所有树枝
        # 拓扑排序后，deg 值为 1 的点必定在基环上，为 0 的点必定在树枝上
        q = deque(i for i, d in enumerate(deg) if d == 0)
        while q:
            x = q.popleft()
            y = g[x]
            deg[y] -= 1
            if deg[y] == 0:
                q.append(y)

        ans = [0] * n
        # 在反图上遍历树枝
        def rdfs(x: int, depth: int) -> None:
            ans[x] = depth
            for y in rg[x]:
                if deg[y] == 0:  # 树枝上的点在拓扑排序后，入度均为 0
                    rdfs(y, depth + 1)
        for i, d in enumerate(deg):
            if d <= 0:
                continue
            ring = []
            x = i
            while True:
                deg[x] = -1  # 将基环上的点的入度标记为 -1，避免重复访问
                ring.append(x)  # 收集在基环上的点
                x = g[x]
                if x == i:
                    break
            for x in ring:
                rdfs(x, len(ring))  # 为方便计算，以 len(ring) 作为初始深度
        return ans
'''


_LS = [k + 1 for k, t in enumerate(CODE.strip('\n').split('\n')) if 'if deg[y] == 0' in t]
L_TOPO, L_RDFS = _LS


def _draw(cv, S, B, box, T):
    g = S.get('g') or G
    deg = S.get('deg')
    ans = S.get('ans')
    inner = S.get('_inner') or {}
    cur = inner.get('x')
    if cur is None:
        cur = S.get('x')
    ring = set(S.get('ring') or [])
    started = ans is not None
    topo = deg is not None and 'q' in S

    def node(i):
        ring_c = T['yellow'] if (cur == i and topo) else None
        if started and ans[i] > 0:
            return (T['green'] if i in ring else T['cyan']), T['bg'], ring_c
        if topo and deg[i] == -1:
            return T['green'], T['bg'], ring_c
        if topo and deg[i] == 0:
            return T['orange'], T['bg'], ring_c
        if i in ring:
            return T['green'], T['bg'], ring_c
        return T['panel2'], T['text'], ring_c

    def edge(a, b):
        if started and ans[a] > 0 and ans[b] > 0:
            return T['cyan'], 4
        if topo and deg[a] == 0:
            return T['orange'], 4
        return (120, 128, 140), 3

    def lab(i):
        if started and ans[i] > 0:
            return (f'ans={ans[i]}', T['green'] if i in ring else T['cyan'])
        if deg is not None and 'q' in S:
            return (f'deg={deg[i]}', T['muted'])
        return None
    E = [(i, e) for i, e in enumerate(g)]
    _gdraw(cv, box, T, POS, E, node, edge, lab, '橙 = 树枝（入度 0），绿 = 基环，青 = 已算出答案，deg = 入度，黄圈 = 当前点', above=lambda i: i in (1, 6), left=lambda i: i == 0)


CONFIG = dict(
    num=2876, title='有向图访问计数', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='拓扑排序剪树枝 + 反图 DFS',
    tags=['灵神题单·图论算法', '难度分 2210'],
    code=CODE,
    call=f'Solution().countVisitedNodes({G})',
    expect=[3, 3, 3, 4, 5, 6, 2, 2],
    skip=['n = len(g)', 'deg = [0] * n', 'def rdfs', 'ring = []', 'ans = [0] * n', 'for x, y in enumerate(g)', 'for y in rg[x]', 'for i, d in enumerate(deg)', 'for x in ring', 'while True', 'continue', 'break', 'y = g[x]', 'deg[x] = -1'],
    max_steps=110,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='queue', var='q', label='q（拓扑排序队列）', h=90),
        dict(type='array', var='ans', label='ans', h=125, cell=60),
        dict(type='calls', h=110),
    ],
    watch=[('x', 'x', 'yellow'), ('i', 'i', 'blue')],
    captions={
        'rg = [[] for': '`rg` 是反图：`rg[y]` 存所有指向 y 的点',
        'rg[y].append(x)': '边 `{x} → {y}`：反图里 `rg[{y}]` 加上 `{x}`',
        'deg[y] += 1': '`{y}` 的入度 +1：`deg[{y}] = {deg[y]}`',
        'q = deque': '入度为 0 的点就是树枝的叶子，它们先入队：`q = {list(q)}`',
        'while q': lambda S, B, r: ('队列空了，所有树枝都剪掉了：剩下 `deg` 为 1 的点都在基环上' if not S.q else f'队列非空，继续剪（队首 `{S.q[0]}`）'),
        'x = q.popleft()': '取出叶子 `{x}`，它指向 `{g[x]}`',
        'y = g[x]': '`y = g[{x}] = {y}`',
        'deg[y] -= 1': '剪掉 `{x}` 这条树枝：`{y}` 的入度 −1 → `deg[{y}] = {deg[y]}`',
        L_TOPO: lambda S, B, r: (f'`deg[{S.y}] = 0`：`{S.y}` 也变成树枝，入队' if S.deg[S.y] == 0
                                            else f'`deg[{S.y}] = {S.deg[S.y]}` > 0：还有别的点指向它，==它在基环上==，不入队'),
        'q.append(y)': '`{y}` 入队：`q = {list(q)}`',
        'if d <= 0': lambda S, B, r: (f'枚举 `i = {S.i}`：`d = {S.d} <= 0`：树枝上的点或已处理的基环点，跳过' if S.d <= 0
                                      else f'枚举 `i = {S.i}`：`d = {S.d}` > 0：==基环上的点==，从它开始收集整个基环'),
        'x = i': '从 `{i}` 出发沿 `g` 绕基环一圈',
        'deg[x] = -1': '标记 `{x}` 已访问：`deg[{x}] = -1`',
        'ring.append(x)': '`deg[{x}] = -1` 标记已访问，并收集到基环：`ring = {ring}`',
        'x = g[x]': '走到下一个点 `{x}`',
        'if x == i': lambda S, B, r: (f'走回起点 `{S.i}`：基环收集完毕 `{S.ring}`' if S.x == S.i else f'`x = {S.x}` ≠ 起点 `{S.i}`，继续'),
        'rdfs(x, len(ring))': '基环点 `{x}`：它能访问的节点数就是环长 `{len(ring)}`；以环长作初始深度，去反图找树枝',
        'ans[x] = depth': '`ans[{x}] = {depth}`：环长 + 它在树枝上的深度',
        L_RDFS: lambda S, B, r: (f'`deg[{S.y}] = 0`：`{S.y}` 是树枝上的点 → 深度 +1 递归' if S.deg[S.y] == 0
                                            else f'`deg[{S.y}] = {S.deg[S.y]}`：基环上的点，不往里走'),
        'return ans': '每个点的访问数：基环点 = 环长，树枝点 = 环长 + 深度；答案 =={ret}==',
    },
    cards=dict(
        one_liner='基环点答案是环长，树枝点再加上到环的深度',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 个点 `n` 条边，`edges[i]` 是 i 的出边终点，从每个点出发一直走，直到再次走到访问过的点',
                 '`answer[i]` = 从 i 出发能访问到的==不同节点数==',
                 '示例：`[1,2,0,0]` → `[3,3,3,4]`；本视频用 8 个点、两个连通块'],
        quote='对于不在基环上的点 x，其可以访问到的节点数，是基环的大小，再加上点 x 的深度。',
        quote_src='—— 灵茶山艾府题解',
        idea=['这是内向基环树：先==拓扑排序剪掉所有树枝==，剩下 `deg = 1` 的点就是基环',
              '基环上的点：答案 = 基环大小',
              '树枝上的点：从环上点出发在==反图==上 DFS，以环长为初始深度，深度逐层 +1'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`deg` 剪完树枝后：1 = 基环、0 = 树枝；收集基环时置 -1 避免重复访问',
                 '图可能有多棵基环树，所以外层要枚举每个点',
                 '反图 DFS 只往 `deg == 0` 的点走，不会误入基环',
                 '同类题：2360 图中的最长环；一般有向图要学 SCC'],
    ),
)
