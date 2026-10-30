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


def _dtree(cv, T, box, n, edges, title, fills=None, rings=None, notes=None, hot=None, root=0, maxR=28, labels=None, side=False):
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
            if side:
                cv.text((X + R + 8, Y), t, 20, c, anchor='lm', bold=True, mono=True)
            else:
                cv.text((X, Y + R + 6), t, 20, c, anchor='mt', bold=True, mono=True)
    return pos

EDGES = [[0, 1], [1, 2], [1, 3]]
G = [[] for _ in range(4)]
for _a, _b in EDGES:
    G[_a].append(_b)
    G[_b].append(_a)
PRICE = [2, 2, 10, 6]


def _order():
    out, par = [], {}

    def go(x, fa):
        out.append(x)
        par[x] = fa
        for y in G[x]:
            if y != fa:
                go(y, x)
    go(0, -1)
    return out, par


def _dp(cnt):
    res = {}

    def go(x, fa):
        a = PRICE[x] * cnt[x]
        b = a // 2
        for y in G[x]:
            if y != fa:
                nh, h = go(y, x)
                a += min(nh, h)
                b += nh
        res[x] = (a, b)
        return a, b
    go(0, -1)
    return res


def _done(S):
    cur = S['_inner'].get('x')
    if cur is None:
        return set()
    order, par = _order()
    path, v = set(), cur
    while v != -1:
        path.add(v)
        v = par[v]
    d = {v for v in order[:order.index(cur)] if v not in path}
    if S['_line'] == 30:
        d.add(cur)
    return d


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = 4
    cnt = S.get('cnt') or [0] * n
    price = S.get('price') or [2, 2, 10, 6]
    inner = S['_inner']
    in_dp = 'not_halve' in S
    cur = inner.get('x')
    fills, rings, notes = {}, {}, {}
    done = _done(S) if in_dp else set()
    dp = _dp(cnt) if in_dp else {}
    start, end = S.get('start'), S.get('end')
    for v in range(n):
        if cnt[v] > 0:
            fills[v] = (28, 84, 52)
        if in_dp and v in done:
            a, b = dp[v]
            notes[v] = (f'({a},{b})', T['orange'])
        elif cnt[v] > 0:
            notes[v] = (f'×{cnt[v]}', T['green'])
    if not in_dp and start is not None and 'end' in S and S['_line'] <= 15:
        rings[start] = T['blue']
        rings[end] = T['pink']
    if cur is not None and cur < n:
        rings[cur] = T['yellow']
    _dtree(cv, T, (x0 + 10, y0, x1 - 10, y1), n, EDGES, '树（×次数 = cnt；橙 = 子树 (不变, 减半) 最小和）',
           fills, rings, notes, side=False, labels={v: f'{v}' for v in range(n)})


def _cap_trip(S, B, ret):
    return f'旅行 `{S.start} → {S.end}`：以 `{S.start}` 为根 dfs，找到 `{S.end}`'


def _cap_found(S, B, ret):
    if S.x == S.end:
        return f'`{S.x}` 就是终点 `end` → 路径的末端，`cnt[{S.x}]` +1，返回 True'
    return f'`{S.x}` 不是终点，继续往下找'


CONFIG = dict(
    num=2646, title='最小化旅行的价格总和', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='统计经过次数 + 树形 DP（打家劫舍 III）',
    tags=['灵神题单·动态规划', '灵神题单·链表树与回溯', '难度分 2238'],
    code='''
class Solution:
    def minimumTotalPrice(self, n: int, edges: List[List[int]], price: List[int], trips: List[List[int]]) -> int:
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        cnt = [0] * n
        for start, end in trips:
            def dfs(x: int, fa: int) -> bool:
                if x == end:
                    cnt[x] += 1
                    return True  # 找到 end
                for y in g[x]:
                    if y != fa and dfs(y, x):
                        cnt[x] += 1  # x 是 end 的祖先节点，也就在路径上
                        return True
                return False  # 未找到 end
            dfs(start, -1)

        # 类似 337. 打家劫舍 III
        def dfs(x: int, fa: int) -> (int, int):
            not_halve = price[x] * cnt[x]  # x 不变
            halve = not_halve // 2  # x 减半
            for y in g[x]:
                if y != fa:
                    nh, h = dfs(y, x)  # 计算 y 不变/减半的最小价值总和
                    not_halve += min(nh, h)  # x 不变，那么 y 可以不变或者减半，取这两种情况的最小值
                    halve += nh  # x 减半，那么 y 只能不变
            return not_halve, halve
        return min(dfs(0, -1))
''',
    call='Solution().minimumTotalPrice(4, [[0,1],[1,2],[1,3]], [2,2,10,6], [[0,3],[2,1]])',
    expect=13,
    views=[
        dict(type='array', var='price', label='price', cell=70, h=135),
        dict(type='array', var='cnt', label='cnt（每个点被经过的次数）', cell=70, h=135),
        dict(type='custom', draw=_draw, h=290),
        dict(type='calls', h=140),
    ],
    watch=[('start', 'start', 'blue'), ('end', 'end', 'pink'), ('x', lambda S: S['_inner'].get('x'), 'yellow'),
           ('not_halve', lambda S: S['_inner'].get('not_halve')), ('halve', lambda S: S['_inner'].get('halve'), 'green')],
    skip=['for x, y in edges', 'g[x].append(y)', 'g[y].append(x)', 14, 25, 26],
    captions={
        'g = [[] for': '建邻接表 `g`',
        'cnt = [0] * n': '`cnt[x]`：所有旅行一共经过 x 几次',
        'for start, end in trips': lambda S, B, r: (_cap_trip(S, B, r) if ('start' not in B or (S.start, S.end) != (B.start, B.end)) else '所有旅行都数完了，`cnt` 就绪'),
        19: '从 `start` 出发 dfs，找 `end`',
        12: '`{x}` 就是终点 → `cnt[{x}]` 变成 `{cnt[x]}`',
        16: '`{x}` 在路径上（终点的祖先）→ `cnt[{x}]` 变成 `{cnt[x]}`',
        'not_halve = price[x]': '`{x}` 不变的价值 = `price × cnt` = `{price[x]} × {cnt[x]}` = `{not_halve}`',
        'halve = not_halve': '`{x}` 减半 → 一半：`{halve}`',
        'nh, h = dfs(y, x)': '先算儿子 `{y}` 的子树：返回它「不变 / 减半」的最小和',
        'not_halve += min': '`x` 不变 → 儿子随意，取 `min({nh}, {h})` → `not_halve = {not_halve}`',
        'halve += nh': '`x` 减半 → 儿子只能不变，加 `nh = {nh}` → `halve = {halve}`',
        'return not_halve, halve': lambda S, B, r: f"`{S['_inner']['x']}` 的子树：不变 ==`{r[0]}`==，减半 ==`{r[1]}`==",
        'return min(dfs': lambda S, B, ret: ('答案取根「不变 / 减半」中较小的' if ret is None else f'`min` 后得到答案 `{ret}`'),
        'if x == end': _cap_found,
    },
    max_steps=80,
    cards=dict(
        one_liner='先数每个点被经过几次，再当「打家劫舍」做',
        complexity='时间 `O(nm)`，空间 `O(n)`',
        problem=['无根树，每个点有价格；一次旅行的价格 = 路径上点的价格之和',
                 '开始前可以把一些==互不相邻==的点价格减半，求所有旅行的最小总价',
                 '示例：`price = [2,2,10,6]`，两次旅行 `0→3`、`2→1` → `13`'],
        quote='把 price[i] 更新成 price[i]·cnt[i]，问题就转换成计算减半后的 price[i] 之和的最小值。……做法和 337. 打家劫舍 III 是类似的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['对每次旅行 dfs 找路径，路径上的点 `cnt` +1',
              '点权变成 `price × cnt`，选不相邻的点减半 → 树上最大独立集的变形',
              '`dfs(x)` 返回两个值：x 不变 / x 减半时子树的最小和'],
        summary=['时间 `O(nm)`：每次旅行一次 dfs；空间 `O(n)`',
                 'x 不变：儿子取 `min(不变, 减半)`；x 减半：儿子只能不变',
                 '`cnt[x] += 1` 写在「归」的时候：从 end 往回走，沿途祖先都加 1',
                 '方法二用 Tarjan 离线 LCA + 树上差分，复杂度 `O(n+m)`，本视频选方法一'],
    ),
)
