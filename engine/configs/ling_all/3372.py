def _tlay(n, edges, root=0):
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)
    depth, par, order = {root: 0}, {root: -1}, [root]
    for x in order:
        for y in g[x]:
            if y not in depth:
                depth[y], par[y] = depth[x] + 1, x
                order.append(y)
    kids = [[y for y in g[x] if par.get(y) == x] for x in range(n)]
    xs, cnt = {}, [0]

    def go(x):
        if not kids[x]:
            xs[x] = cnt[0]
            cnt[0] += 1
        else:
            for y in kids[x]:
                go(y)
            xs[x] = (xs[kids[x][0]] + xs[kids[x][-1]]) / 2
    go(root)
    return xs, depth, par, cnt[0], max(depth.values()) + 1


def _dtree(cv, T, box, n, edges, title, fills=None, rings=None, notes=None, hot=None, root=0, maxR=28, labels=None):
    """画一棵一般树。fills: 点->颜色；rings: 点->描边色；notes: 点->(文字,颜色)（点下方）；hot: {(a,b):颜色}；labels: 点->显示文字"""
    x0, y0, x1, y1 = box
    fills, rings, notes, hot, labels = fills or {}, rings or {}, notes or {}, hot or {}, labels or {}
    cv.text((x0 + 8, y0), title, 22, T['muted'], bold=True)
    xs, depth, par, leaves, levels = _tlay(n, edges, root)
    w = x1 - x0 - 50
    top = y0 + 44
    R = max(16, min(maxR, w / leaves / 2.3))
    dy = min(110, (y1 - top - 2 * R - 34) / max(1, levels - 1)) if levels > 1 else 0
    pos = {v: (x0 + 25 + (xs[v] + 0.5) * w / leaves, top + depth[v] * dy + R) for v in range(n)}
    for a, b in edges:
        (ax, ay), (bx, by) = pos[a], pos[b]
        c = hot.get((a, b)) or hot.get((b, a))
        cv.line([(ax, ay), (bx, by)], c or T['border'], 6 if c else 3)
    for v in range(n):
        X, Y = pos[v]
        ring = rings.get(v)
        cv.rect((X - R, Y - R, X + R, Y + R), fill=fills.get(v, T['panel2']), outline=ring or T['border'],
                width=5 if ring else 2, r=R)
        cv.text((X, Y), labels.get(v, v), int(R * 0.95), T['text'], anchor='mm', bold=True)
        if v in notes:
            t, c = notes[v]
            cv.text((X, Y + R + 6), t, 20, c, anchor='mt', bold=True, mono=True)
    return pos

E1 = [[0, 1], [1, 2], [2, 3], [2, 4]]
E2 = [[0, 1]]
K = 2


def _dist(n, edges, s):
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)
    d, q = {s: 0}, [s]
    for x in q:
        for y in g[x]:
            if y not in d:
                d[y] = d[x] + 1
                q.append(y)
    return d


def _path(n, edges, root, x):
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)
    par, q = {root: None}, [root]
    for u in q:
        for y in g[u]:
            if y not in par:
                par[y] = u
                q.append(y)
    out = []
    while x is not None:
        out.append(x)
        x = par.get(x)
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    mid = (x0 + x1) / 2
    g = S.get('g')
    act = 0 if not g else (1 if len(g) == 5 else 2)
    cur = S['_inner'].get('x') if act else None
    in_diam = act and 'd' not in S['_inner']
    start = S.get('i') if (act and not in_diam and 'i' in S) else None
    for ti, (n, E, ox, title) in enumerate([(5, E1, x0, '第一棵树：每个点算一个答案'),
                                              (2, E2, mid, '第二棵树：找最佳连接点')]):
        mine = act == ti + 1
        fills, rings, notes = {}, {}, {}
        if mine and start is not None and start < n:
            lim = K if ti == 0 else K - 1
            dd = _dist(n, E, start)
            for v, dv in dd.items():
                notes[v] = (f'd={dv}', T['green'] if dv <= lim else T['dim'])
                if dv <= lim:
                    fills[v] = (28, 84, 52)
            fills[start] = (40, 84, 140)
        if mine and cur is not None and cur < n:
            root = start if (start is not None and start < n) else 0
            for v in _path(n, E, root, cur):
                rings[v] = (150, 120, 40)
            rings[cur] = T['yellow']
        _dtree(cv, T, (ox + 10, y0, ox + (x1 - x0) / 2 - 10, y1 - 66), n, E, title, fills, rings, notes)
    if 'max2' in S:
        cv.text((x0 + 10, y1 - 34), f"max2 = {S['max2']}（第二棵树连接点最多带来的目标节点数）", 22, T['orange'], anchor='lb', bold=True)
    cv.text((x0 + 10, y1 - 6), '蓝 = 起点  绿 = 距起点在限制内  黄圈 = 当前 dfs 的点', 20, T['muted'], anchor='lb')


def _if_d(S, B, ret):
    if S.d > S.k:
        return f'`d = {S.d} > k = {S.k}`：太远了，整棵子树都不算 → ==剪枝==返回 0'
    return f'`d = {S.d} ≤ k = {S.k}`：还在范围内，继续数'


def _diam_if(S, B, ret):
    if S.diameter < S.k:
        return f'`直径 {S.diameter} < k = {S.k}`：每个点都够得着'
    return f'`直径 {S.diameter} ≥ k = {S.k}`：只能暴力数'


def _diam1(S, B, ret):
    if S.diameter <= S.k:
        return f'`直径 {S.diameter} ≤ k = {S.k}`：每点答案都是 `n + max2`'
    return f'`直径 {S.diameter} > k = {S.k}`：不能走捷径，逐点暴力数'


CONFIG = dict(
    num=3372, title='连接两棵树后最大目标节点数目 I', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='贪心拆分 + 暴力 DFS · 直径剪枝',
    tags=['灵神题单·动态规划', '灵神题单·链表树与回溯', '难度分 1927'],
    code='''
class Solution:
    def calc_tree(self, edges: List[List[int]], k: int) -> Tuple[int, 'Callable[[int, int, int], int]']:
        g = [[] for _ in range(len(edges) + 1)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        diameter = 0
        def dfs_diameter(x: int, fa: int) -> int:
            nonlocal diameter
            max_len = 0
            for y in g[x]:
                if y != fa:
                    sub_len = dfs_diameter(y, x) + 1
                    diameter = max(diameter, max_len + sub_len)
                    max_len = max(max_len, sub_len)
            return max_len
        dfs_diameter(0, -1)

        def dfs(x: int, fa: int, d: int) -> int:
            if d > k:
                return 0
            cnt = 1
            for y in g[x]:
                if y != fa:
                    cnt += dfs(y, x, d + 1)
            return cnt

        return diameter, dfs

    def maxTargetNodes(self, edges1: List[List[int]], edges2: List[List[int]], k: int) -> List[int]:
        n, m = len(edges1) + 1, len(edges2) + 1

        max2 = 0
        if k:
            diameter, dfs = self.calc_tree(edges2, k - 1)
            if diameter < k:
                max2 = m  # 第二棵树的每个节点都是目标节点
            else:
                max2 = max(dfs(i, -1, 0) for i in range(m))

        diameter, dfs = self.calc_tree(edges1, k)
        if diameter <= k:
            return [n + max2] * n  # 第一棵树的每个节点都是目标节点
        return [dfs(i, -1, 0) + max2 for i in range(n)]
''',
    call='Solution().maxTargetNodes([[0,1],[1,2],[2,3],[2,4]], [[0,1]], 2)',
    expect=[5, 7, 7, 6, 6],
    views=[
        dict(type='custom', draw=_draw, h=440),
        dict(type='calls', h=170, hide=('edges', 'edges1', 'edges2')),
    ],
    watch=[('start i', lambda S: S.get('i')), ('x', lambda S: S['_inner'].get('x'), 'yellow'),
           ('d', lambda S: S['_inner'].get('d')), ('cnt', lambda S: S['_inner'].get('cnt')),
           ('diameter', 'diameter', 'purple'), ('max2', 'max2', 'orange')],
    captions={
        'n, m = len': '`n = {n}`、`m = {m}`：两棵树的点数',
        'max2 = 0': '`max2`：第二棵树最多能带来的目标点数',
        'if k:': lambda S, B, r: ('`k = %d`：新边占 1 步，第二棵树只剩 `k − 1` 步' % S.k if S.k else '`k = 0`：第二棵树帮不上忙，`max2 = 0`'),
        'self.calc_tree(edges2': '第二棵树：限制 `k - 1 = {B.k - 1}`（新边占一步）',
        'self.calc_tree(edges1': '第一棵树：限制就是 `k = {B.k}`',
        'g = [[] for': '建邻接表 `g`',
        'dfs_diameter(0, -1)': '从 0 出发求直径（最长路径的边数）',
        'sub_len = dfs_diameter': '递归儿子，儿子最长链 + 1 条边',
        'diameter = max(diameter, max_len + sub_len)': '过 `{x}` 的最长路径 = `{max_len}` + `{sub_len}` → 直径 `{diameter}`',
        'max_len = max': '`{x}` 向下最长链 `{max_len}`',
        'return diameter, dfs': '返回直径和计数函数 `dfs`',
        'if d > k': _if_d,
        'cnt = 1': '节点 `{x}` 自己算 1 个',
        'cnt += dfs(y, x, d + 1)': '走向儿子 `{y}`（不回头），累加它子树的点数',
        'return cnt': '`{x}` 这一块共 `{cnt}` 个目标节点',
        'if diameter < k': _diam_if,
        'max2 = m  #': '任意两点都够得着 → 全是目标：`max2 = {max2}`',
        'max2 = max(dfs(i': '每个点当连接点，数 `≤ k−1` 的点，取最大',
        'if diameter <= k': _diam1,
        'return [n + max2]': '每个点答案都是 `n + max2`',
        'return [dfs(i': lambda S, B, ret: ('每个点 `i` 当起点：数 `≤ k` 的点，再加 `max2`' if ret is None else f'`answer[i] = dfs(i) + max2` → `{ret}`'),
    },
    max_steps=62,
    skip=['for x, y in edges', 'g[x].append(y)', 'g[y].append(x)', 'for y in g[x]', 'if y != fa', 'max_len = 0', 'return max_len'],
    cards=dict(
        one_liner='新边的一端必是 i，两棵树各算各的再相加',
        complexity='时间 `O(n²+m²)`（随机树期望接近 `O(n+m)`），空间 `O(n+m)`',
        problem=['两棵无向树，各连一条边把它们接起来；`u` 到 `v` 路径边数 `≤ k` 就算目标节点',
                 '对第一棵树每个点 `i`，求连边后 `i` 的目标节点数的最大值（每次询问独立）',
                 '示例：`k = 2` 的第一棵树 5 点、第二棵树 2 点 → `[5,7,7,6,6]`'],
        quote='新添加的边的一个端点必然是 i。为什么？因为用其他节点当作端点，只会让第二棵树的节点到 i 距离变得更远，答案更小。',
        quote_src='—— 灵茶山艾府题解',
        idea=['新边一端是 `i`，另一端 `j` 在第二棵树上：==两棵树的计数互相独立==',
              '第二棵树：新边占 1 步，数每个 `j` 周围 `≤ k−1` 的点，取最大 `max2`',
              '第一棵树：数每个 `i` 周围 `≤ k` 的点，加上 `max2` 就是答案'],
        result='运行结束，返回 `[5, 7, 7, 6, 6]`：每个点的 `cnt + max2`（`max2 = 2`）',
        summary=['时间 `O(n²+m²)`：每个点 DFS 一次；空间 `O(n+m)`',
                 '易错：第二棵树限制是 `k − 1`；`k = 0` 时 `max2 = 0`',
                 '直径剪枝：直径 `≤ k`（第二棵树是 `< k`）时每个点都是目标，不用暴力',
                 '优化前的写法没有直径判断，其余相同；本视频选「直径优化」写法',
                 '为在引擎里运行，类型注解  加了引号，逻辑未改'],
    ),
)
