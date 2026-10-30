# ---------- 一般树的自绘（custom 视图）：按 children 布局，状态完全由当前步的变量推出 ----------
import math as _m


def _tree_pos(children, root, box, top=56, bottom=40):
    x0, y0, x1, y1 = box
    depth, leaf_x, pos = {}, [0], {}

    def go(u, d):
        depth[u] = d
        ks = children.get(u, [])
        if not ks:
            pos[u] = leaf_x[0]
            leaf_x[0] += 1
        else:
            for k in ks:
                go(k, d + 1)
            pos[u] = sum(pos[k] for k in ks) / len(ks)
    go(root, 0)
    nl, md = max(1, leaf_x[0]), max(depth.values()) + 1
    sp = min(110, (x1 - x0 - 60) / nl)
    dy = min(100, (y1 - y0 - top - bottom) / max(1, md))
    rad = max(16, min(26, sp * 0.36, dy * 0.3))
    sx = x0 + 30 + ((x1 - x0 - 60) - sp * (nl - 1)) / 2
    P = {u: (sx + pos[u] * sp, y0 + top + depth[u] * dy + rad) for u in depth}
    return P, rad


def _preorder(children, root):
    out = []

    def go(u):
        out.append(u)
        for k in children.get(u, []):
            go(k)
    go(root)
    return out


def _ancestors(parent, u):
    out = []
    while u is not None and u in parent:
        u = parent[u]
        if u is not None:
            out.append(u)
    return out


def draw_gtree(cv, T, box, children, root, parent, cur, hot=None, finished=(), badge=None, bad_edges=(),
               label_fn=None, color_fn=None, title=None, node_color=None):
    """cur: 当前递归节点；hot: 当前正在考察的子节点；finished: 已返回的节点集合；badge: {节点: 文字}"""
    P, rad = _tree_pos(children, root, box)
    if title:
        cv.text((box[0] + 18, box[1] + 4), title, 22, T['muted'], bold=True)
    for u, ks in children.items():
        for k in ks:
            bad = (u, k) in bad_edges
            isc = hot is not None and u == cur and k == hot
            c = T['pink'] if isc else (T['red'] if bad else T['border'])
            if bad and not isc:
                cv.dashed(P[u], P[k], c, 3, 10, 7)
            else:
                cv.line([P[u], P[k]], c, 6 if isc else 3)
    anc = set(_ancestors(parent, cur)) if cur is not None else set()
    for u, (X, Y) in P.items():
        fill, outl, w, tc = T['panel2'], T['border'], 2, T['text']
        if u in finished:
            fill, tc = T['green'], T['bg']
        if node_color and node_color(u):
            fill, tc = T[node_color(u)], T['bg']
        if u in anc:
            outl, w = T['yellow'], 4
        if u == hot:
            outl, w = T['pink'], 5
        if u == cur:
            outl, w = T['blue'], 5
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=outl, width=w)
        cv.text((X, Y), label_fn(u) if label_fn else u, int(rad * 0.95), tc, anchor='mm', bold=True)
        if badge and u in badge:
            s = badge[u]
            bw = cv.tlen(s, 19, bold=True) + 14
            cv.rect((X - bw / 2, Y + rad + 4, X + bw / 2, Y + rad + 28), fill=T['panel'], outline=T['green'], width=2, r=8)
            cv.text((X, Y + rad + 16), s, 19, T['green'], anchor='mm', bold=True)


def _subtree(children, u):
    out = [u]
    for k in children.get(u, []):
        out += _subtree(children, k)
    return out


def fin_set(CH, ORDER, PAR, x, y, line, call_line, for_line, ret_line, yb):
    """已返回的节点：x 之前先序出现且不在栈上的、x 已处理完的孩子子树、（return 行上的）x 自己"""
    if x is None:
        return set()
    anc = set(_ancestors(PAR, x))
    fin = {u for u in ORDER[:ORDER.index(x)] if u not in anc}
    ks = CH[x]
    ended = (y is not None and yb == y and line == for_line) or line == ret_line
    if ended:
        for k in ks:
            fin |= set(_subtree(CH, k))
    elif y in ks:
        for k in ks:
            if ks.index(k) < ks.index(y) or (k == y and line > call_line):
                fin |= set(_subtree(CH, k))
    if line == ret_line:
        fin.add(x)
    return fin

E1 = [[0, 1], [1, 2]]
E2 = [[0, 1]]


def _rooted(edges):
    n = len(edges) + 1
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)
    ch, par, order = {i: [] for i in range(n)}, {0: None}, []

    def go(u, f):
        order.append(u)
        for v in g[u]:
            if v != f:
                ch[u].append(v)
                par[v] = u
                go(v, u)
    go(0, -1)
    return ch, par, order


TREES = [_rooted(E1), _rooted(E2)]


def _ecc(edges):
    n = len(edges) + 1
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)

    def far(s):
        dist, q = {s: 0}, [s]
        for u in q:
            for v in g[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    q.append(v)
        return q[-1], dist[q[-1]]
    p, _ = far(0)
    return far(p)[1]


D = [_ecc(E1), _ecc(E2)]


def _g(S, k):
    return S['_inner'].get(k)


def _q(S):
    q = _g(S, 'q')
    return q if isinstance(q, list) else []


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    inner = S.get('_inner', {})
    d1, d2 = S.get('d1'), S.get('d2')
    active = 0 if d1 is None else (1 if d2 is None else -1)
    if S.get('_line', 0) >= MERGE_LINE:
        active = -1
    mid = (x0 + x1) / 2
    vis = inner.get('vis') if isinstance(inner.get('vis'), set) else set()
    q = inner.get('q') if isinstance(inner.get('q'), list) else []
    head, tail = inner.get('head'), inner.get('tail')
    layer = set(q[head:tail]) if (head is not None and tail is not None) else set()
    x, y = inner.get('x'), inner.get('y')
    p = S.get('p')
    qend = inner.get('q') if isinstance(inner.get('q'), int) else None
    for k in range(2):
        ch, par, order = TREES[k]
        bx = (x0, y0, mid - 6, y1) if k == 0 else (mid + 6, y0, x1, y1)
        done = (k == 0 and d1 is not None) or (k == 1 and d2 is not None)
        if k == active:
            def nc(u):
                if u == p and p is not None or (qend is not None and u == qend):
                    return 'orange'
                if u in layer and u != x:
                    return 'yellow'
                return None
            hot = y if (y is not None and x is not None and line_ok(S)) else None
            draw_gtree(cv, T, bx, ch, 0, {}, x if _g(S, 'vis') is not None else None, hot, vis, None, (),
                       node_color=nc, title=f'第 {k + 1} 棵树（绿 = vis，黄 = 本轮，橙 = 直径端点）')
        else:
            draw_gtree(cv, T, bx, ch, 0, {}, None, None, set(), None, (),
                       title=f'第 {k + 1} 棵树' + (f'：直径 d{k + 1} = {D[k]}' if done else '（还没算）'))


def line_ok(S):
    return S.get('_line', 0) in (HOT_LINES)
CODE = '''
class Solution(object):
    def minimumDiameterAfterMerge(self, edges1, edges2):

        def calc(edges):

            def bfs(x):
                q = [x]
                head, tail = 0, 1
                vis = set([x])
                rnd = 0
                while head < tail:
                    rnd += 1
                    for x in q[head : tail]:
                        for y in g.get(x, set()):
                            if y not in vis:
                                vis.add(y)
                                q.append(y)
                    
                    head, tail = tail, len(q)
                
                return q[-1], rnd

            g = {}
            for x, y in edges:
                if x not in g:
                    g[x] = set()
                if y not in g:
                    g[y] = set()
                g[x].add(y)
                g[y].add(x)
            
            p, _ = bfs(0)
            q, d = bfs(p)

            return d - 1

        d1 = calc(edges1)
        d2 = calc(edges2)
        return max(d1, d2, (d1 + 1) // 2 + (d2 + 1) // 2 + 1)
'''
_CL = CODE.strip('\n').split('\n')


def _ln(sub):
    return [i + 1 for i, t in enumerate(_CL) if sub in t][0]


MERGE_LINE = _ln('return max(d1')
HOT_LINES = (_ln('if y not in vis'), _ln('vis.add(y)'), _ln('q.append(y)'))


def _cap_for_y(S, B, r):
    return f"看 `{_g(S, 'x')}` 的邻居 `{_g(S, 'y')}`"


def _cap_if(S, B, r):
    y = _g(S, 'y')
    return f"`{y}` " + ('还没访问过 → 新节点，下一轮要扩展它' if y not in _g(S, 'vis') else '已经在 `vis` 里 → 跳过，避免走回头路')


CONFIG = dict(
    num=3203, title='合并两棵树后的最小直径', difficulty='Hard',
    category='链表、二叉树与回溯',
    author='yiduobo', technique='双 BFS 求直径 · 连直径中点',
    tags=['动态规划', '链表树与回溯', '难度分 2266'],
    code=CODE,
    call='Solution().minimumDiameterAfterMerge([[0,1],[1,2]], [[0,1]])',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=280),
        dict(type='array', var=lambda S: _q(S), pointers={'head': 'blue', 'tail': 'pink'}, label='队列 q（蓝 = head，粉 = tail）', cell=70, h=160),
        dict(type='text', fn=lambda S: (f"`d1 = {S.get('d1')}`　`d2 = {S.get('d2')}`" if S.get('d1') is not None else '先对每棵树 BFS 两次求直径 `d1`、`d2`'), size=26, h=50),
    ],
    watch=[('rnd', lambda S: _g(S, 'rnd'), 'yellow'), ('x', lambda S: _g(S, 'x'), 'blue'), ('y', lambda S: _g(S, 'y'), 'pink'),
           ('p', lambda S: S.get('p') if isinstance(S.get('p'), int) else None, 'orange'),
           ('d1', lambda S: S.get('d1')), ('d2', lambda S: S.get('d2'))],
    captions={
        'g = {}': '先建图：`g[x]` 是 x 的邻居集合',
        'q = [x]': lambda S, B, r: f"从 `{_g(S, 'x')}` 出发 BFS：队列里先放起点",
        'head, tail = 0, 1': '`q[head:tail]` 是当前这一轮要扩展的节点',
        'vis = set([x])': '`vis` 记录访问过的节点',
        'rnd = 0': '`rnd` 数 BFS 的轮数 = 离起点最远点的距离 + 1',
        'while head < tail': lambda S, B, r: (f"这一轮还有节点 `q[{S.head}:{S.tail}]` 要扩展" if S.head < S.tail else '本轮没有新节点了，BFS 结束'),
        'rnd += 1': '新开一轮：`rnd = {rnd}`',
        'for x in q[head : tail]': lambda S, B, r: (f"扩展 `{_g(S, 'x')}`" if _g(S, 'x') != B['_inner'].get('x') or B['_inner'].get('y') is None else '这一轮的节点都扩展完了'),
        'for y in g.get': lambda S, B, r: (_cap_for_y(S, B, r) if _g(S, 'y') != B['_inner'].get('y') else f"`{_g(S, 'x')}` 的邻居都看完了"),
        'if y not in vis': _cap_if,
                'q.append(y)': '`{y}` 标记已访问并入队：`q = {q}`',
        'head, tail = tail': '这一轮扩展完，下一轮的范围 = 新入队的节点：`q[{head}:{tail}]`',
        'return q[-1], rnd': lambda S, B, ret: f"BFS 结束：最后入队的 `{ret[0]}` 就是离起点最远的点（==直径的一个端点==），一共 `{ret[1]}` 轮",
        'p, _ = bfs(0)': '第 1 次 BFS：从任意点 `0` 出发，最后入队的 `p = {p}` 是最远点，==它必是直径的一个端点==',
        'q, d = bfs(p)': '第 2 次 BFS：从 `p = {p}` 出发，最远点 `q = {q}`，一共 `d = {d}` 轮',
        'return d - 1': '轮数比距离多 1 → 直径 = `d - 1 = {d - 1}`（边数）',
        'd1 = calc': '先算第一棵树的直径',
        'd2 = calc': '`d1 = {d1}`；再算第二棵树',
        'return max(d1': ('分两种情况：不经过新边 → `max(d1, d2) = {max(d1, d2)}`；经过新边（连直径中点）'
                         '→ `({d1}+1)//2 + ({d2}+1)//2 + 1 = {(d1 + 1) // 2 + (d2 + 1) // 2 + 1}`；取较大者 ==`{ret}`=='),
    },
    skip=['if x not in g', 'g[x] = set()', 'if y not in g', 'g[y] = set()', 'g[x].add(y)', 'g[y].add(x)', 'for x, y in edges', 'rnd = 0', 'vis = set', 'head, tail = 0, 1', 'rnd += 1', 'vis.add(y)', 'while head < tail'],
    max_steps=110,
    cards=dict(
        one_liner='两次 BFS 找直径；两棵树各连「直径中点」，再取最大',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['给两棵无向树 `edges1`、`edges2`，各选一个点连一条边',
                 '要使合并后的树==直径最小==，返回这个最小直径',
                 '本视频：`edges1 = [[0,1],[1,2]]`，`edges2 = [[0,1]]` → `3`'],
        quote='分别选择两颗树中距离其他节点最大距离最小的点，也就是原始两颗树中最长路径的中点，而最长的距离则是原始两颗树的直径除以2向上取整。',
        quote_src='—— yiduobo 知乎题解',
        idea=['新树里的最长路径，要么不经过新边：`max(d1, d2)`',
              '要么经过新边：两侧都连直径中点，半径各为 `ceil(d/2)`，再加新边的 `1`',
              '直径用「双 BFS」求：任选点 BFS 找最远点 `p`，再从 `p` 出发 BFS，轮数 − 1 就是直径'],
        result='运行结束，返回 `3`：`d1 = 2`、`d2 = 1`，经过新边 `1 + 1 + 1 = 3`，比 `d1` 大',
        summary=['时间 `O(n+m)`，空间 `O(n+m)`',
                 '易错：`bfs` 返回的是==轮数==（点数），直径 = 轮数 − 1',
                 '易错：`ceil(d/2)` 要写成 `(d + 1) // 2`',
                 '原文是 Python 2 风格但无需改动；对比灵神：灵神用树形 DP 求直径，yiduobo 用两次 BFS'],
    ),
)
