def _rooted(edges, root=0):
    adj = {}
    for a, b in edges:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    kids, seen, qq = {}, {root}, [root]
    for x in qq:
        for y in adj.get(x, []):
            if y not in seen:
                seen.add(y)
                kids.setdefault(x, []).append(y)
                qq.append(y)
    return kids


def _layout(kids, root=0):
    pos, slot = {}, [0]

    def go(x, d):
        ks = kids.get(x, [])
        if not ks:
            pos[x] = (slot[0], d)
            slot[0] += 1
        else:
            for k in ks:
                go(k, d + 1)
            pos[x] = ((pos[ks[0]][0] + pos[ks[-1]][0]) / 2, d)
    go(root, 0)
    return pos, slot[0], max(d for _, d in pos.values()) + 1


def _pre(kids, root=0):
    order, end = [], {}

    def go(x):
        order.append(x)
        for k in kids.get(x, []):
            go(k)
        end[x] = len(order) - 1
    go(root)
    return order, end


def _draw_tree(cv, box, T, kids, pos, nl, nd, node_fn, edge_fn=None, title='', rad=28):
    import math
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    top, bot = y0 + 76, y1 - 66
    dy = min(120, (bot - top) / max(nd - 1, 1))
    dx = min(150, (x1 - x0 - 160) / max(nl - 1, 1))
    cx = (x0 + x1) / 2 - dx * (nl - 1) / 2
    P = lambda n: (cx + pos[n][0] * dx, top + pos[n][1] * dy)
    for a, ks in kids.items():
        for b in ks:
            (ax, ay), (bx, by) = P(a), P(b)
            e = edge_fn(a, b) if edge_fn else {}
            col = e.get('color', T['border'])
            w = e.get('width', 3)
            L = math.hypot(bx - ax, by - ay)
            ux, uy = (bx - ax) / L, (by - ay) / L
            p0, p1 = (ax + ux * rad, ay + uy * rad), (bx - ux * rad, by - uy * rad)
            ar = e.get('arrow')
            if ar == 'down':
                cv.arrow(p0, p1, col, w, 14)
            elif ar == 'up':
                cv.arrow(p1, p0, col, w, 14)
            elif e.get('dashed'):
                cv.dashed(p0, p1, col, w)
            else:
                cv.line([p0, p1], col, w)
            if e.get('label') is not None:
                mx, my = (ax + bx) / 2, (ay + by) / 2
                lx, ly = mx + (18 if bx >= ax else -18) + (-uy * 0), my - 4
                cv.text((lx + (10 if bx >= ax else -10), ly), e['label'], 22, e.get('lcolor', T['yellow']), anchor='mm', bold=True)
    for n in pos:
        X, Y = P(n)
        s = node_fn(n)
        fill = s.get('fill', T['panel2'])
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=s.get('outline', T['border']), width=s.get('ow', 2))
        cv.text((X, Y), n, 26, s.get('tc', T['text']), anchor='mm', bold=True)
        if s.get('sub'):
            cv.text((X, Y + rad + 6), s['sub'], 20, s.get('subc', T['muted']), anchor='mt', bold=True)
        if s.get('tag'):
            cv.text((X + rad + 4, Y - rad - 2), s['tag'], 19, s.get('tagc', T['yellow']), anchor='lb', bold=True)

_CODE = '''
class Solution:
    def reachableNodes(self, n: int, edges: List[List[int]], restricted: List[int]) -> int:
        r = set(restricted)
        g = [[] for _ in range(n)]
        for x, y in edges:
            if x not in r and y not in r:
                g[x].append(y)  # 都不受限才连边
                g[y].append(x)
        def dfs(x: int, fa: int) -> int:
            cnt = 1
            for y in g[x]:
                if y != fa:
                    cnt += dfs(y, x)
            return cnt
        return dfs(0, -1)
'''
_LINES = _CODE.strip('\n').split('\n')
_EDGES = [[0, 1], [1, 2], [3, 1], [4, 0], [0, 5], [5, 6]]
_KIDS = _rooted(_EDGES)
_POS, _NL, _ND = _layout(_KIDS)


def _pre_g(g):
    order, end, km = [], {}, {}

    def go(x, fa):
        order.append(x)
        km[x] = [y for y in g[x] if y != fa]
        for y in km[x]:
            go(y, x)
        end[x] = len(order) - 1
    go(0, -1)
    return order, end


def _vis(S, B):
    """已经走到过的节点（先序前缀）"""
    g, inner = S.get('g'), S['_inner']
    if g is None or 'fa' not in inner:
        return set(), None
    x, fa = inner['x'], inner['fa']
    order, end = _pre_g(g)
    src = _LINES[S['_line'] - 1]
    e = order.index(x)
    y = inner.get('y')
    if 'return cnt' in src:
        e = end[x]
    elif y is not None:
        if 'for y in g[x]' in src and B['_inner'].get('y') == y:
            e = end[x]  # 循环结束
        else:
            prior = [k for k in g[x][:g[x].index(y)] if k != fa]
            e = end[prior[-1]] if prior else e
    return set(order[:e + 1]), x


def _draw(cv, S, B, box, T):
    g, r = S.get('g'), S.get('r')
    vis, cur = _vis(S, B)

    def node(n):
        if r is not None and n in r:
            return dict(fill=T['red'], tc=T['bg'], tag='受限', tagc=T['red'])
        if n == cur:
            return dict(fill=T['green'], tc=T['bg'], outline=T['yellow'], ow=5)
        if n in vis:
            return dict(fill=T['green'], tc=T['bg'])
        return {}

    def edge(a, b):
        if g is not None and b in g[a]:
            return dict(color=T['blue'], width=4)
        return dict(color=T['dim'], dashed=True, width=3)
    _draw_tree(cv, box, T, _KIDS, _POS, _NL, _ND, node, edge, '树（蓝实线 = 已连边，灰虚线 = 没连；红 = 受限，绿 = DFS 已到达）')


CONFIG = dict(
    num=2368, title='受限条件下可到达节点的数目', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='受限点不连边 + DFS 计数',
    tags=['链表树与回溯', '难度分 1477'],
    code=_CODE,
    call='Solution().reachableNodes(7, [[0,1],[1,2],[3,1],[4,0],[0,5],[5,6]], [4,5])',
    expect=4,
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='set', var='r', label='受限集合 r', h=90),
        dict(type='calls', h=180),
    ],
    watch=[('x', lambda S: S['_inner'].get('x') if 'fa' in S['_inner'] else None, 'blue'), ('cnt', lambda S: S['_inner'].get('cnt') if 'fa' in S['_inner'] else None, 'green')],
    max_steps=90,
    captions={
        'r = set': '受限点放进集合：`r = {r}`，判断是否受限只要 `O(1)`',
        'g = [[]': '`g[i]` 存节点 `i` 的邻居，先全空',
        'for x, y in edges': lambda S, B, ret: (f'取一条边 `({S.x}, {S.y})`' if B.get('x') != S.x or B.get('y') != S.y
                                                else '所有边都处理完了，树建好了'),
        'if x not in r': lambda S, B, ret: (f'边 `({S.x}, {S.y})`：两端都不受限 → ==连边==' if S.x not in S.r and S.y not in S.r
                                             else f'边 `({S.x}, {S.y})`：`{S.x if S.x in S.r else S.y}` 受限 → ==不连边==，这条路被封死'),
        'g[x].append': '`g[{x}]` 加上 `{y}`：{x} 能走到 {y}',
        'g[y].append': '无向边，反过来 `g[{y}]` 加上 `{x}`',
        'cnt = 1': '进入节点 `{x}`：它自己算 1 个，`cnt = 1`',
        'for y in g[x]': lambda S, B, ret: (f'枚举 `{S.x}` 的邻居 `y = {S.y}`' if S.get('y') is not None and B.get('y') != S.y
                                            else f'`{S.x}` 的邻居都走完了'),
        'if y != fa': lambda S, B, ret: (f'`y = {S.y}` 就是父节点 `{S.fa}` → 跳过，不走回头路' if S.y == S.fa
                                         else f'`y = {S.y}` 不是父节点 `{S.fa}` → 往下走'),
        'cnt += dfs': '递归进入 `{B.y}`，把它子树里能到的点数加到 `cnt`',
        'return cnt': '`{x}` 这棵子树共 ==`{ret}`== 个可达节点，返回给父节点',
        'return dfs(0, -1)': '受限点没连边，所以 DFS 自然走不到；从 `0` 出发，`fa = -1` 表示没有父节点',
    },
    cards=dict(
        one_liner='受限的点不连边，从 0 出发 DFS 数一数能走到几个点',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树，从节点 `0` 出发，==不能经过受限节点==，最多能到几个点',
                 '示例：`n = 7`，`restricted = [4, 5]` → 只有 `0, 1, 2, 3` 能到，答案 `4`',
                 '注意：`6` 虽然不受限，但只能经过受限的 `5` 到达'],
        quote='然后建树，只有当两个节点都不是受限的（都不在哈希集合中）才连边。从 0 出发 DFS 这棵树，统计能访问到的节点个数，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['用集合 `r` 记录受限点，建树时==有一端受限的边直接不要==',
              '这样受限点成了孤岛，DFS 根本到不了，不用在搜索里判断',
              '树里往下走只要不回头：传入父节点 `fa`，`y != fa` 才递归'],
        summary=['时间 `O(n)`：建图和 DFS 都是线性；空间 `O(n)`（邻接表 + 递归栈）',
                 '==两个端点都不受限才连边==，只判一端会漏掉被封住的子树',
                 '树没有环，用 `fa` 防回头就够了，不需要 visited 数组',
                 '节点 `0` 不会受限；同类题：二叉树 / 一般树的 DFS 遍历'],
    ),
)
