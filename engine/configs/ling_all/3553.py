def _layout_tree(ch, root):
    pos, cnt = {}, [0]

    def go(u, d):
        kids = ch.get(u, [])
        if not kids:
            x = cnt[0]
            cnt[0] += 1
        else:
            xs = [go(v, d + 1) for v in kids]
            x = (xs[0] + xs[-1]) / 2
        pos[u] = (x, d)
        return x
    go(root, 0)
    return pos, cnt[0]


def _tree_view(ch, root, colors, title, tags=None, wt=None, lab=None):
    """ch: {父: [子...]}；colors(S) -> {节点: 颜色名}；tags(S) -> {节点: 小字}；wt: {子: 边权}"""
    pos, W = _layout_tree(ch, root)
    D = max(d for _, d in pos.values()) + 1

    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
        cell = min(120, (x1 - x0 - 60) / max(W, 1))
        rowh = min(110, (y1 - y0 - 165) / max(D - 1, 1))
        sx = x0 + 30 + ((x1 - x0 - 60) - cell * W) / 2
        r = min(28, cell * 0.36, rowh * 0.42)
        P = {u: (sx + (x + 0.5) * cell, y0 + 80 + d * rowh) for u, (x, d) in pos.items()}
        for u, kids in ch.items():
            for v in kids:
                cv.line([P[u], P[v]], T['border'], 3)
                if wt:
                    left = P[v][0] <= P[u][0] + 1
                    cv.text(((P[u][0] + P[v][0]) / 2 + (-10 if left else 10), (P[u][1] + P[v][1]) / 2 - 6), wt[v], 22, T['orange'],
                            anchor='rm' if left else 'lm', bold=True)
        cm = colors(S) or {}
        tg = (tags(S) if tags else None) or {}
        for u, (X, Y) in P.items():
            c = cm.get(u)
            cv.rect((X - r, Y - r, X + r, Y + r), fill=T[c] if c else T['panel2'], outline=T['border'], width=2, r=r)
            cv.text((X, Y), lab(u) if lab else u, 26, T['bg'] if c else T['text'], anchor='mm', bold=True)
            if u in tg:
                cv.text((X + r + 6, Y + r * 0.5), tg[u], 20, T['muted'], anchor='lm', bold=True)
    return dict(type='custom', draw=draw, h=0)
CH = {0: [1], 1: [2, 3, 4], 2: [5]}
WT = {1: 2, 2: 3, 3: 5, 4: 4, 5: 6}


def _colors(S):
    c = {}
    for nm, col in (('x', 'blue'), ('y', 'pink'), ('node', 'yellow')):
        v = S.get(nm)
        if isinstance(v, int) and 0 <= v < 6:
            c[v] = col
    return c


def _tags(S):
    d = S.get('dis')
    if d is None:
        return {}
    return {i: f'dis={d[i]}' for i in range(6)}


def _formula(S):
    q = S.get('queries')
    if q and S.get('g') is not None and hasattr(S['g'], 'dis'):
        a, b, c = q[0]
        g = S['g']
        return f'`a={a}, b={b}, c={c}`：三条两两距离之和除以 2（回路里每条边出现两次）'
    return '`a`、`b`、`c` 三点两两距离之和 ÷ 2 = 最小子树的总权重（每条边恰好被算两次）'


def _final(S, B, ret):
    g, (a, b, c) = S['g'], S['queries'][0]
    d1, d2, d3 = g.get_dis(a, b), g.get_dis(b, c), g.get_dis(a, c)
    return f'`d(a,b) = {d1}`，`d(b,c) = {d2}`，`d(a,c) = {d3}`：`({d1} + {d2} + {d3}) // 2` = =={(d1 + d2 + d3) // 2}=='


CONFIG = dict(
    num=3553, title='包含要求路径的最小带权子图 II', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='倍增 LCA + 三点距离和的一半',
    tags=['链表树与回溯', '难度分 2411'],
    code='''
class LcaBinaryLifting:
    def __init__(self, edges: List[List[int]]):
        n = len(edges) + 1
        m = n.bit_length()
        g = [[] for _ in range(n)]
        for x, y, w in edges:  # 节点编号从 0 开始
            g[x].append((y, w))
            g[y].append((x, w))

        depth = [0] * n
        dis = [0] * n
        pa = [[-1] * m for _ in range(n)]

        def dfs(x: int, fa: int) -> None:
            pa[x][0] = fa
            for y, w in g[x]:
                if y != fa:
                    depth[y] = depth[x] + 1
                    dis[y] = dis[x] + w
                    dfs(y, x)

        dfs(0, -1)

        for i in range(m - 1):
            for x in range(n):
                if (p := pa[x][i]) != -1:
                    pa[x][i + 1] = pa[p][i]
        self.depth = depth
        self.dis = dis
        self.pa = pa

    def get_kth_ancestor(self, node: int, k: int) -> int:
        for i in range(k.bit_length()):
            if k >> i & 1:  # k 二进制从低到高第 i 位是 1
                node = self.pa[node][i]
        return node

    # 返回 x 和 y 的最近公共祖先（节点编号从 0 开始）
    def get_lca(self, x: int, y: int) -> int:
        if self.depth[x] > self.depth[y]:
            x, y = y, x
        # 使 y 和 x 在同一深度
        y = self.get_kth_ancestor(y, self.depth[y] - self.depth[x])
        if y == x:
            return x
        for i in range(len(self.pa[x]) - 1, -1, -1):
            px, py = self.pa[x][i], self.pa[y][i]
            if px != py:
                x, y = px, py  # 同时往上跳 2**i 步
        return self.pa[x][0]

    # 返回 x 到 y 的距离（最短路长度）
    def get_dis(self, x: int, y: int) -> int:
        return self.dis[x] + self.dis[y] - self.dis[self.get_lca(x, y)] * 2

class Solution:
    def minimumWeight(self, edges: List[List[int]], queries: List[List[int]]) -> List[int]:
        g = LcaBinaryLifting(edges)
        return [(g.get_dis(a, b) + g.get_dis(b, c) + g.get_dis(a, c)) // 2 for a, b, c in queries]
''',
    call='Solution().minimumWeight([[0,1,2],[1,2,3],[1,3,5],[1,4,4],[2,5,6]], [[2,3,4]])',
    expect=[12],
    views=[
        dict(type='text', fn=_formula, size=24, h=60),
        dict(_tree_view(CH, 0, _colors, '树（边上是权重，节点下方是到根的距离 dis；蓝 = x，粉 = y）', tags=_tags, wt=WT), h=520),
        dict(type='table', var=lambda S: S.get('pa') or S.get('self.pa'), label='pa[x][i]（行 = 节点，列 = i）', rows=list(range(6)),
             cols=[0, 1, 2], cell=44, h=290),
    ],
    watch=['x', 'y', 'i', 'k', 'node'],
    max_steps=84,
    skip=['for x, y, w in edges', 'g[x].append', 'g[y].append', 'for y, w in g[x]', 'for i in range(k.bit_length())',
          'for i in range(len(self.pa[x]) - 1', 'if (p := pa[x][i]) != -1', 'for x in range(n)', 'if y != fa',
          'depth[y] = depth[x] + 1', 'self.depth = depth', 'self.dis = dis', 'if px != py'],
    captions={
        'g = LcaBinaryLifting': '建 LCA 工具：建图、DFS 记深度和到根距离、倍增表',
        'n = len(edges) + 1': '`n = {n}` 个节点',
        'm = n.bit_length()': '`m = {m}`：每个节点存 `m` 个祖先',
        'g = [[] for': '邻接表 `g`：每条边带权重 `w`，两头都存',
        'depth = [0] * n': '`depth[x]` 是边数，`dis[x]` 是带权距离，都是相对根 `0`',
        'pa = [[-1] * m': '`pa[x][i]` 先全填 `-1`',
        'dfs(0, -1)': '从根 `0` 出发 DFS',
        'pa[x][0] = fa': '`pa[{x}][0] = {fa}`：父节点',
        'dis[y] = dis[x] + w': '`dis[{y}] = {dis[x]} + {w}` = =={dis[y]}==：到根的带权距离',
        'for i in range(m - 1)': '倍增表：按列填（`i = {i}`）',
        'pa[x][i + 1] = pa[p][i]': '`pa[{x}][{i + 1}] = pa[{p}][{i}]` = =={pa[x][i + 1]}==：先走 2^i 步，再走 2^i 步',
        'self.pa = pa': '预处理完成',
        'return [(g.get_dis': lambda S, B, ret: ('对每个询问 `(a, b, c)`：求三对点的距离' if ret is None else _final(S, B, ret)),
        'return self.dis[x] + self.dis[y]': '距离 = `dis[x] + dis[y] - 2 * dis[lca]`，先去求 `lca`',
        'if self.depth[x] > self.depth[y]': lambda S, B, ret: f'`depth[{S.x}] = {S.depth[S.x]}`，`depth[{S.y}] = {S.depth[S.y]}`：保证 `x` 不比 `y` 深',
        'x, y = y, x': '`x` 更深，交换：`x = {x}`，`y = {y}`',
        'y = self.get_kth_ancestor': '把更深的 `y` 提到和 `x` 同一深度：上跳 `depth[y] - depth[x]` 步',
        'if k >> i & 1': lambda S, B, ret: (f'第 {S.i} 位是 1：跳 `2^{S.i}` 步' if S.k >> S.i & 1 else f'第 {S.i} 位是 0：不跳'),
        'node = self.pa[node][i]': '查表跳到 ==`{node}`==',
        'return node': '已在同一深度：`y` = ==`{ret}`==',
        'if y == x': lambda S, B, ret: ('`y == x`：`x` 本身就是最近公共祖先' if S.y == S.x else '`y != x`：LCA 还在更上面，两个一起往上跳'),
        'px, py =': lambda S, B, ret: (f'试跳 `2^{S.i}` 步：`px = {S.px}`，`py = {S.py}`，' + (f'不同 → 还没汇合，==可以跳==' if S.px != S.py
                                       else ('都是 `-1` → 步子太大，换小步' if S.px == -1 else '相同 → 已汇合，LCA 可能在下面，换小步'))),
        'x, y = px, py': '一起跳：`x = {x}`，`y = {y}`',
        'return self.pa[x][0]': '只差一步：LCA = `pa[x][0]` = ==`{ret}`==',
        'return x': 'LCA 就是 ==`{ret}`==',
    },
    cards=dict(
        one_liner='三点两两距离相加再除以 2，每条边恰好被数两次',
        complexity='预处理 `O(n log n)`，每个询问 `O(log n)`',
        problem=['无向带权树，节点 `0..n-1`；每个询问 `[src1, src2, dest]`',
                 '求一棵子树的==最小总权重==，使 `src1`、`src2` 都能到达 `dest`',
                 '示例：`edges=[[0,1,2],[1,2,3],[1,3,5],[1,4,4],[2,5,6]]`，查 `[2,3,4]` → `12`'],
        quote='这三条路径，恰好形成了一个回路（从 a 到 b 到 c 再回到 a），所以回路中的每条边都恰好出现在两条路径中。因此，把这三个距离相加，再除以 2，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['最小子树 = 三个点两两连起来的那棵「Y 形」树',
              '两两距离之和里，Y 形的每条边恰好出现两次 → 除以 2',
              '距离 = `dis[x] + dis[y] - 2 * dis[lca]`，LCA 用倍增求'],
        summary=['预处理 `O(n log n)`，每个询问 `O(log n)`',
                 '易错：距离用==带权== `dis`，不是 `depth`；除以 2 用 `//`',
                 'LCA：先对齐深度，再从大步到小步一起上跳',
                 '思考题：4 个点或 k 个点，见题解视频（按 DFS 序排序后相邻点距离之和 ÷ 2）',
                 '视频只演示一个询问 `[2,3,4]`'],
    ),
)
