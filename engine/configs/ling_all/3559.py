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
EDGES = [[1, 2], [1, 3], [3, 4], [3, 5]]
CH = {0: [1, 2], 2: [3, 4]}      # 0 下标：节点 1..5 -> 0..4


def _colors(S):
    c = {}
    for nm, col in (('x', 'blue'), ('y', 'pink')):
        v = S.get(nm)
        if isinstance(v, int) and 0 <= v < 5:
            c[v] = col
    v = S.get('node')
    if isinstance(v, int) and 0 <= v < 5 and 'k' in S:
        c[v] = 'yellow'
    return c


def _tags(S):
    d = S.get('depth')
    if d is None:
        return {}
    return {i: f'd={d[i]}' for i in range(5)}


def _formula(S):
    if 'k' in S and 'i' in S and 'node' in S:
        return f"`k = {S['k']}` = `{S['k']:b}`₂：为 1 的那些位，各往上跳 `2^i` 步"
    return '路径有 `d` 条边：每条边设 1 或 2，代价为奇数的方案数 = `2^(d-1)`；`x == y` 时没有边，答案 `0`'


CONFIG = dict(
    num=3559, title='给边赋权值的方案数 II', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='倍增 LCA 求距离 + 2^(d-1)',
    tags=['链表树与回溯', '难度分 2146'],
    code='''
class LcaBinaryLifting:
    def __init__(self, edges: List[List[int]]):
        n = len(edges) + 1
        m = n.bit_length()
        g = [[] for _ in range(n)]
        for x, y in edges:
            x -= 1  # 节点编号从 0 开始
            y -= 1
            g[x].append(y)
            g[y].append(x)

        depth = [0] * n
        pa = [[-1] * m for _ in range(n)]

        def dfs(x: int, fa: int) -> None:
            pa[x][0] = fa
            for y in g[x]:
                if y != fa:
                    depth[y] = depth[x] + 1
                    dfs(y, x)

        dfs(0, -1)

        for i in range(m - 1):
            for x in range(n):
                if (p := pa[x][i]) != -1:
                    pa[x][i + 1] = pa[p][i]
        self.depth = depth
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
        return self.depth[x] + self.depth[y] - self.depth[self.get_lca(x, y)] * 2

# 预处理 2 的幂
MOD = 1_000_000_007
POW2 = [0] * 10 ** 5
POW2[0] = 1
for i in range(1, len(POW2)):
    POW2[i] = POW2[i - 1] * 2 % MOD

class Solution:
    def assignEdgeWeights(self, edges: List[List[int]], queries: List[List[int]]) -> List[int]:
        g = LcaBinaryLifting(edges)
        return [POW2[g.get_dis(x - 1, y - 1) - 1] if x != y else 0 for x, y in queries]
''',
    call='Solution().assignEdgeWeights([[1, 2], [1, 3], [3, 4], [3, 5]], [[1, 4], [3, 4], [2, 5]])',
    expect=[2, 1, 4],
    views=[
        dict(type='text', fn=_formula, size=24, h=60),
        dict(_tree_view(CH, 0, _colors, '树（编号已减 1，对应代码里的下标；蓝 = x，粉 = y）', tags=_tags, lab=lambda u: u), h=330),
        dict(type='table', var=lambda S: S.get('pa') or S.get('self.pa'), label='pa[x][i]（行 = 节点，列 = i）', rows=list(range(5)), cols=[0, 1, 2],
             cell=60, h=300),
    ],
    watch=['x', 'y', 'i', 'k', 'node'],
    max_steps=100,
    skip=['for x, y in edges', 'x -= 1', 'y -= 1', 'g[x].append', 'g[y].append', 'for y in g[x]', 'for i in range(k.bit_length())', 'for i in range(len(self.pa[x]) - 1', 'if (p := pa[x][i]) != -1', 'for x in range(n)', 'if y != fa'],
    captions={
        'g = LcaBinaryLifting': '建 LCA 工具：先建图，再 DFS 记深度和父节点，最后做倍增表',
        'n = len(edges) + 1': '`n = {n}` 个节点',
        'm = n.bit_length()': '`m = {m}`：每个节点存 `m` 个祖先（第 2^0 … 2^{m - 1} 个）',
        'g = [[] for': '邻接表 `g`：边已按「节点编号 - 1」建好',
        'depth = [0] * n': '`depth[x]`：根到 `x` 的边数',
        'pa = [[-1] * m': '`pa[x][i]` 先全填 `-1`（不存在）',
        'dfs(0, -1)': '从根 `0` 出发 DFS：记下父节点和深度',
        'pa[x][0] = fa': '`pa[{x}][0] = {fa}`：第 1 个祖先就是父节点',
        'depth[y] = depth[x] + 1': '孩子 `{y}` 的深度 = `{depth[x]} + 1` = =={depth[y]}==',
        'for i in range(m - 1)': '按列填：先算完所有 2^i 级，再算 2^(i+1) 级（`i = {i}`）',
        'if (p := pa[x][i]) != -1': lambda S, B, ret: (f'`pa[{S.x}][{S.i}] = {S.p}`：存在，可以拼下一档' if S.p != -1
                                                      else f'`pa[{S.x}][{S.i}] = -1`：已经出树了，下一档也是 `-1`'),
        'pa[x][i + 1] = pa[p][i]': '`pa[{x}][{i + 1}] = pa[{p}][{i}]` = =={pa[x][i + 1]}==：走 2^i 步，再走 2^i 步',
        'self.depth = depth': '预处理结束，开始回答询问',
        'if self.depth[x] > self.depth[y]': lambda S, B, ret: f'`depth[{S.x}] = {S.depth[S.x]}`，`depth[{S.y}] = {S.depth[S.y]}`：让 `x` 是较浅的那个',
        'x, y = y, x': '`x` 比 `y` 深，交换',
        'y = self.get_kth_ancestor': '把更深的 `y` 往上提 `depth[y] - depth[x]` 步，和 `x` 同一深度',
        'for i in range(k.bit_length())': '`k` 的每个二进制 1 对应一次跳跃',
        'if k >> i & 1': lambda S, B, ret: (f'第 {S.i} 位是 1：跳 `2^{S.i}` 步' if S.k >> S.i & 1 else f'第 {S.i} 位是 0：不跳'),
        'node = self.pa[node][i]': '查表：跳到 ==`{node}`==',
        'return node': '同一深度了：`y` = ==`{ret}`==',
        'if y == x': lambda S, B, ret: ('`y == x`：`x` 本身就是最近公共祖先' if S.y == S.x else '`y != x`：LCA 还在更上面，两个一起往上跳'),
        'for i in range(len(self.pa[x]) - 1': '从大步到小步试：能跳（跳完还不相遇）就跳，否则缩小步长',
        'px, py =': '从大步到小步试跳 `2^{i}` 步：`px = {px}`，`py = {py}`',
        'if px != py': lambda S, B, ret: (f'`{S.px} != {S.py}`：还没汇合 → 这一步可以跳' if S.px != S.py
                                          else (f'两边都是 `-1`：步子迈大了（祖先不存在）→ 不跳，换小步' if S.px == -1
                                                else f'`{S.px} == {S.py}`：汇合了，LCA 可能在它下面 → 不跳，换小步')),
        'x, y = px, py': '一起跳：`x = {x}`，`y = {y}`',
        'return self.pa[x][0]': '`x`、`y` 离 LCA 只差一步：LCA = `pa[x][0]` = ==`{ret}`==',
        'return x': 'LCA 就是 ==`{ret}`==',
        'return self.depth[x] + self.depth[y]': '两点距离 = `depth[x] + depth[y] - 2 * depth[lca]`，先去求 `lca`',
        'return [POW2': lambda S, B, ret: ('逐个询问：先求距离 `d`，`x == y` 答案 0，否则 `2^(d-1)`' if ret is None else '三个询问的答案：==`{}`=='.format(ret)),
    },
    cards=dict(
        one_liner='两点距离 d 条边，奇数代价的方案数 = 2^(d-1)',
        complexity='预处理 `O(n log n)`，每次询问 `O(log n)`',
        problem=['树有 `n` 个节点，根是 `1`；每条边权值设为 `1` 或 `2`',
                 '每个询问 `[u, v]`：路径总代价为==奇数==的赋值方案数，对 `10^9+7` 取模',
                 '示例：`edges=[[1,2],[1,3],[3,4],[3,5]]`，`queries=[[1,4],[3,4],[2,5]]` → `[2,1,4]`'],
        quote='**定理**：从 k 个不同元素中，选奇数个数（选奇数条边设置边权为 1），有 2^(k-1) 种选法。……本题需要快速计算两点之间的距离（边数），套 LCA 模板即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['路径上有 `d` 条边：权值为 1 的边数是奇数，总和才是奇数',
              '从 `d` 条边里选奇数条，共 `2^(d-1)` 种',
              '距离 = `depth[x] + depth[y] - 2 * depth[lca]`，LCA 用倍增求',
              '`POW2` 提前预处理好 2 的幂（取模）'],
        summary=['预处理 `O(n log n)`，每次询问 `O(log n)`',
                 '易错：`x == y` 时没有边，答案是 `0`，不能算 `2^(-1)`',
                 '节点编号从 1 开始，模板里统一减 1 变成下标',
                 '求 LCA：先对齐深度，再从大步到小步一起往上跳',
                 '代码里的 `POW2` 预处理是模块级代码，视频不单独演示'],
    ),
)
