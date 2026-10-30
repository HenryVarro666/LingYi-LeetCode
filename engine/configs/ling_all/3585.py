def _tidy(children, root=0):
    pos = {}
    cnt = [0]
    md = [0]

    def go(u, d):
        md[0] = max(md[0], d)
        ks = children[u]
        if not ks:
            x = cnt[0]
            cnt[0] += 1
        else:
            for k in ks:
                go(k, d + 1)
            x = (pos[ks[0]][0] + pos[ks[-1]][0]) / 2
        pos[u] = (x, d)
    go(root, 0)
    return pos, max(cnt[0], 1), md[0] + 1


def _children(n, edges):
    g = [[] for _ in range(n)]
    for e in edges:
        g[e[0]].append(e[1])
        g[e[1]].append(e[0])
    ch = [[] for _ in range(n)]
    seen = {0}
    st = [0]
    while st:
        u = st.pop()
        for v in g[u]:
            if v not in seen:
                seen.add(v)
                ch[u].append(v)
                st.append(v)
    for c in ch:
        c.sort()
    return ch


def _draw_tree(cv, box, T, children, edges, node_fn, edge_fn=None, under_fn=None, title=None, rad=23):
    """node_fn(u)->颜色名或None；edge_fn(a,b)->颜色名或None；under_fn(u)->节点下方小字"""
    x0, y0, x1, y1 = box
    if title:
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
        y0 += 44
    pos, w, dep = _tidy(children)
    gx = (x1 - x0 - 80) / max(w - 1, 1) if w > 1 else 0
    gx = min(gx, 170)
    gy = min((y1 - y0 - 90) / max(dep - 1, 1), 120)
    ox = x0 + (x1 - x0 - gx * (w - 1)) / 2
    oy = y0 + 40

    def P(u):
        return (ox + pos[u][0] * gx, oy + pos[u][1] * gy)
    for e in edges:
        a, b = e[0], e[1]
        pa_, pb = P(a), P(b)
        c = edge_fn(a, b) if edge_fn else None
        cv.line([pa_, pb], T[c] if c else T['border'], 7 if c else 3)
        if len(e) > 2:
            mx, my = (pa_[0] + pb[0]) / 2, (pa_[1] + pb[1]) / 2
            lab = str(e[2])
            tw = cv.tlen(lab, 20, True) + 12
            cv.rect((mx - tw / 2, my - 13, mx + tw / 2, my + 13), fill=T['bg'], r=8)
            cv.text((mx, my), lab, 20, T[c] if c else T['muted'], anchor='mm', bold=True, mono=True)
    for u in range(len(children)):
        X, Y = P(u)
        c = node_fn(u)
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=T[c] if c else T['panel2'],
                     outline=T[c] if c else T['border'], width=3)
        cv.text((X, Y), u, 26, T['bg'] if c else T['text'], anchor='mm', bold=True)
        if under_fn:
            s = under_fn(u)
            if s:
                cv.text((X + rad + 8, Y), s, 20, T['cyan'], anchor='lm', bold=True, mono=True)

CODE = '''
class LcaBinaryLifting:
    def __init__(self, edges: List[List[int]]):
        n = len(edges) + 1
        self.m = m = n.bit_length()
        g = [[] for _ in range(n)]
        for x, y, w in edges:
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
            if k >> i & 1:
                node = self.pa[node][i]
        return node

    # 返回 x 和 y 的最近公共祖先
    def get_lca(self, x: int, y: int) -> int:
        if self.depth[x] > self.depth[y]:
            x, y = y, x
        # 使 y 和 x 在同一深度
        y = self.get_kth_ancestor(y, self.depth[y] - self.depth[x])
        if y == x:
            return x
        for i in range(self.m - 1, -1, -1):
            px, py = self.pa[x][i], self.pa[y][i]
            if px != py:
                x, y = px, py  # 同时往上跳 2**i 步
        return self.pa[x][0]

    # 返回 x 到 y 的距离（最短路长度）
    def get_dis(self, x: int, y: int) -> int:
        return self.dis[x] + self.dis[y] - self.dis[self.get_lca(x, y)] * 2

    # 从 x 往上跳【至多】d 距离，返回最远能到达的节点
    def upto_dis(self, x: int, d: int) -> int:
        dx = self.dis[x]
        for i in range(self.m - 1, -1, -1):
            p = self.pa[x][i]
            if p != -1 and dx - self.dis[p] <= d:  # 可以跳至多 d
                x = p
        return x

class Solution:
    def findMedian(self, n: int, edges: List[List[int]], queries: List[List[int]]) -> List[int]:
        g = LcaBinaryLifting(edges)
        ans = []
        for x, y in queries:
            if x == y:
                ans.append(x)
                continue
            lca = g.get_lca(x, y)
            dis_xy = g.dis[x] + g.dis[y] - g.dis[lca] * 2
            half = (dis_xy + 1) // 2
            if g.dis[x] - g.dis[lca] >= half:  # 答案在 x-lca 路径中
                # 先往上跳至多 half-1，然后再跳一步，就是至少 half
                to = g.upto_dis(x, half - 1)
                res = g.pa[to][0]  # 再跳一步
            else:  # 答案在 y-lca 路径中
                # 从 y 出发至多 dis_xy-half，就是从 x 出发至少 half
                res = g.upto_dis(y, dis_xy - half)
            ans.append(res)
        return ans
'''
LINE_TXT = {i: l for i, l in enumerate(CODE.strip('\n').split('\n'), 1)}

N = 5
EDGES = [[0, 1, 2], [0, 2, 5], [1, 3, 1], [2, 4, 3]]
QUERIES = [[3, 4], [4, 3]]
CH = _children(N, EDGES)


def _dis(S):
    d = S.get('dis')
    if d is None and S.get('g') is not None:
        d = S['g'].dis
    return d


def _pa(S):
    d = S.get('pa')
    if d is None and S.get('g') is not None:
        d = S['g'].pa
    return d


def _q(S):
    """当前询问 (x, y)"""
    ans = S.get('ans')
    if ans is None:
        return None
    k = len(ans) - (1 if 'ans.append' in LINE_TXT.get(S.get('_line'), '') else 0)
    return QUERIES[k] if 0 <= k < len(QUERIES) else None


def _node(S):
    inner = S.get('_inner', {})
    q = _q(S)
    roles = {}
    if 'fa' in inner and 'y' in inner and 'x' in inner:
        roles[inner['x']] = 'yellow'
        return lambda u: roles.get(u)
    if q and S.get('g') is not None:
        roles[q[0]] = 'blue'
        roles[q[1]] = 'pink'
        if S.get('lca') is not None and 'lca' in inner:
            roles[S['lca']] = 'yellow'
        if 'd' in inner:
            roles[inner['x']] = 'cyan'
        if 'to' in inner and 'res' in inner:
            roles[inner['res']] = 'green'
        elif 'res' in inner and inner['res'] is not None and not inner.get('d'):
            roles[inner['res']] = 'green'
    return lambda u: roles.get(u)


def _draw(cv, S, B, box, T):
    nf = _node(S)
    d = _dis(S)
    _draw_tree(cv, box, T, CH, EDGES, nf,
               under_fn=(lambda u: f'dis={d[u]}' if d and u < len(d) and (d[u] or u == 0) else None),
               title='树（蓝 = x，粉 = y，黄 = lca，青 = 正在往上跳的点，绿 = 答案）')


def _cap_half(S, B, ret):
    g = S.g
    x, y, lca = S.x, S.y, S.lca
    return f'`dis_xy = {g.dis[x]} + {g.dis[y]} − 2×{g.dis[lca]} = {S.dis_xy}`，`half = ceil({S.dis_xy}/2) = {S.half}`'


def _cap_jump(S, B, ret):
    p = S.p
    if p == -1:
        return f'`pa[{S.x}][{S.i}] = -1`：没有 2^{S.i} 级祖先，不能跳'
    c = S.dx - S.self.dis[p]
    ok = c <= S.d
    return f'跳到 {p} 要走 `{S.dx} − {S.self.dis[p]} = {c}`，`{c} {"<=" if ok else ">"} d = {S.d}` → ' + ('==能跳==' if ok else '太远，不跳')


def _cap_branch(S, B, ret):
    g = S.g
    a = g.dis[S.x] - g.dis[S.lca]
    if a >= S.half:
        return f'`dis[x]−dis[lca] = {a} >= half = {S.half}` → 答案在 ==x 到 lca== 这一段'
    return f'`dis[x]−dis[lca] = {a} < half = {S.half}` → 答案在 ==y 到 lca== 这一段'


CONFIG = dict(
    num=3585, title='树中找到带权中位节点', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='LCA 倍增 · 往上跳至多 d',
    tags=['难度分 2429'],
    code=CODE,
    call='Solution().findMedian(5, [[0,1,2],[0,2,5],[1,3,1],[2,4,3]], [[3,4],[4,3]])',
    expect=[2, 0],
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var=_dis, label='dis（根到各点的距离）', cell=60, h=150),
        dict(type='table', var=_pa, label='pa[x][i]：x 的 2^i 级祖先（-1 = 没有）', cell=48, h=240),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), 'lca', 'half', ('ans', 'ans', 'green')],
    skip=['self.depth = depth', 'self.dis = dis', 'self.pa = pa', 'g = [[] for', 'depth = [0]', 'dis = [0]', 'pa = [[-1]',
          'self.m = m', 'n = len(edges) + 1', 'for x, y, w in edges', 'g[x].append', 'g[y].append', 'depth[y] = depth[x] + 1',
          'for x in range(n):', 'for y, w in g[x]', 'pa[x][0] = fa', 'if y != fa', 'if (p := pa[x][i]) != -1',
          'p = self.pa[x][i]', 'for i in range(self.m - 1, -1, -1)'] + list(range(31, 52)) + ['ans = []'],
    max_steps=110,
    captions={
        'g = LcaBinaryLifting(edges)': '先建 ==LCA 倍增模板==：预处理每个点的 2^i 级祖先，以及到根的距离 `dis`',
        'dfs(0, -1)': '从根 0 开始 DFS，记下父节点、深度、到根的距离 `dis`',
        'pa[x][0] = fa': '`pa[{x}][0] = {fa}`：先记下直接父节点',
        'if y != fa': '`{y} != 父节点 {fa}`？不走回头路 → {"==继续往下==" if y != fa else "是父节点，跳过"}',
        'dis[y] = dis[x] + w': '`dis[{y}] = dis[{x}] + {w} = {dis[y]}`：到根距离 = 父亲的距离 + 边权',
        'for i in range(m - 1)': '倍增：先填 2^i 级祖先，再用它们推 2^(i+1) 级',
        'pa[x][i + 1] = pa[p][i]': '`pa[{x}][{i+1}] = pa[{p}][{i}] = {pa[x][i+1]}`：先跳 2^{i} 步到 {p}，再从 {p} 跳 2^{i} 步',
        'lca = g.get_lca(x, y)': '求 x、y 的最近公共祖先 `lca`（先拉到同一深度，再一起往上跳）',
        'dis_xy = g.dis': '`lca = {lca}`，`dis_xy = dis[x] + dis[y] − 2·dis[lca] = {g.dis[x]} + {g.dis[y]} − 2×{g.dis[lca]} = {dis_xy}`',
        'half = (dis_xy': '`half = ceil({dis_xy}/2) = {half}`：答案是离 x ==至少 half== 的第一个点',
        'if g.dis[x] - g.dis[lca] >= half': _cap_branch,
        'to = g.upto_dis(x, half - 1)': '先从 x 往上跳==至多== `half−1 = {half-1}`，得到 `to`；再多跳一步就刚好 ≥ half',
        'res = g.pa[to][0]': '再跳一步：`res = pa[{to}][0] = {res}`，就是离 x 至少 half 的第一个点',
        'res = g.upto_dis(y, dis_xy - half)': '从 y 往上跳至多 `dis_xy − half = {dis_xy - half}`，等价于从 x 出发至少 half',
        'dx = self.dis[x]': '记下起点到根的距离 `dx = {dx}`，往上跳了多远 = `dx − dis[p]`',
        'for i in range(self.m - 1, -1, -1)': lambda S, B, r: f'从大到小试 `i`：先试 2^{S.i} 级祖先（大步优先）',
        'p = self.pa[x][i]': '`p` = x 的 2^{i} 级祖先 = {p}',
        'if p != -1 and dx - self.dis[p] <= d': _cap_jump,
        'x = p': '能跳就跳：`x` → {x}',
        'return x': '返回最远能到的节点 `{x}`',
        'ans.append(x)': '起点终点相同，答案就是 x',
        'ans.append(res)': '第 {len(ans)} 个询问的答案：`{res}`',
    },
    cards=dict(
        one_liner='LCA 倍增：往上跳至多 d，再补一步就是至少',
        complexity='时间 `O((n+q) log n)`，空间 `O(n log n)`',
        problem=['无向带权树，根为 0；询问 `(x, y)`：求 x 到 y 路径上第一个“离 x 的边权和 ≥ 总权值一半”的节点',
                 '示例：`edges=[[0,1,2],[0,2,5],[1,3,1],[2,4,3]]`，询问 `[3,4]` → `2`',
                 '本视频：询问 `[3,4]` 与 `[4,3]`，答案 `[2,0]`'],
        quote='往上跳至少 half 可以转化成：往上跳至多 half-1，然后再往上跳一个节点。',
        quote_src='—— 灵茶山艾府题解',
        idea=['记 `lca`、`dis_xy`、`half = ceil(dis_xy/2)`，按 x 到 lca 的距离是否 ≥ half 分两种情况',
              '答案在 x 一侧：x 往上跳至多 half−1，再跳一步；在 y 一侧：y 往上跳至多 dis_xy−half',
              '两种情况统一成“从某点往上跳至多 d 的最远点”，用倍增从大到小试：`upto_dis`'],
        summary=['时间 `O((n+q) log n)`，空间 `O(n log n)`，`pa[x][i]` 是 x 的 2^i 级祖先',
                 '==half 要向上取整==：`(dis_xy + 1) // 2`；“至少”和“至多”差一步，别写反',
                 '`upto_dis` 里要判 `p != -1`；边权 ≥ 1，所以 dis 沿路径严格递增，贪心跳才成立',
                 'x == y 时路径长 0，直接把 x 当答案'],
    ),
)
