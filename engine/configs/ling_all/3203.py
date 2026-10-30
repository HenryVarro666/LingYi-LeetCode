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

E1 = [[0, 1], [0, 2], [0, 3]]
E2 = [[0, 1], [1, 2], [2, 3]]


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


def _sim_len(ch):
    ret = {}

    def go(u):
        m = 0
        for v in ch[u]:
            m = max(m, go(v) + 1)
        ret[u] = m
        return m
    go(0)
    return ret


def _diam(ch):
    best = [0]

    def go(u):
        m = 0
        for v in ch[u]:
            s = go(v) + 1
            best[0] = max(best[0], m + s)
            m = max(m, s)
        return m
    go(0)
    return best[0]


D = [_diam(t[0]) for t in TREES]
RETS = [_sim_len(t[0]) for t in TREES]


def _g(S, k):
    return S['_inner'].get(k)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    inner = S.get('_inner', {})
    x, y = inner.get('x'), inner.get('y')
    line = S.get('_line', 0)
    d1, d2 = S.get('d1'), S.get('d2')
    active = 0 if d1 is None else (1 if d2 is None else -1)
    if S.get('_line', 0) >= MERGE_LINE and d1 is not None and d2 is not None:
        active = -1
    if active == 0 and x is None and line < DIAM_LINE_START:
        pass
    mid = (x0 + x1) / 2
    for k in range(2):
        ch, par, order = TREES[k]
        bx = (x0, y0, mid - 6, y1) if k == 0 else (mid + 6, y0, x1, y1)
        done = (k == 0 and d1 is not None) or (k == 1 and d2 is not None)
        if k == active and x is not None:
            fin = fin_set(ch, order, par, x, y, line, CALL_LINE, FOR_LINE, RET_LINE, B['_inner'].get('y'))
            hot = y if (y in ch[x] and line in (ANS_LINE, MAX_LINE)) else None
            draw_gtree(cv, T, bx, ch, 0, par, x, hot, fin, {u: f'{RETS[k][u]}' for u in fin}, (),
                       title=f'第 {k + 1} 棵树（绿 = 已返回）')
        else:
            draw_gtree(cv, T, bx, ch, 0, par, None, None, set(order) if done else set(), {u: f'{RETS[k][u]}' for u in order} if done else None, (),
                       title=f'第 {k + 1} 棵树' + (f'：直径 `d{k + 1}` = {D[k]}'.replace('`', '') if done else '（还没算）'))
CODE = '''
class Solution:
    def diameter(self, edges: List[List[int]]) -> int:
        g = [[] for _ in range(len(edges) + 1)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        res = 0
        def dfs(x: int, fa: int) -> int:
            nonlocal res
            max_len = 0
            for y in g[x]:
                if y != fa:
                    sub_len = dfs(y, x) + 1
                    res = max(res, max_len + sub_len)
                    max_len = max(max_len, sub_len)
            return max_len
        dfs(0, -1)
        return res

    def minimumDiameterAfterMerge(self, edges1: List[List[int]], edges2: List[List[int]]) -> int:
        d1 = self.diameter(edges1)
        d2 = self.diameter(edges2)
        return max(d1, d2, (d1 + 1) // 2 + (d2 + 1) // 2 + 1)
'''
_CL = CODE.strip('\n').split('\n')


def _ln(sub):
    return [i + 1 for i, t in enumerate(_CL) if sub in t][0]


CALL_LINE, FOR_LINE, RET_LINE, ANS_LINE, MAX_LINE = _ln('sub_len = dfs'), _ln('for y in g[x]'), _ln('return max_len'), _ln('res = max(res'), _ln('max_len = max(max_len')
MERGE_LINE, DIAM_LINE_START = _ln('return max(d1'), 0


def _cap_call(S, B, ret):
    return f"进入孩子 `{_g(S, 'x')}`：先相信递归，算出它往下的最长链，再 `+1` 算上这条边"


def _cap_res(S, B, ret):
    return (f"拼接：已有最长链 `{B.max_len}` + 新链 `{S.sub_len}` 是经过 x 的一条路径 → "
            f"`res = max({B.res}, {B.max_len} + {S.sub_len}) = {S.res}`（==最大值 + 次大值==）")


def _cap_max(S, B, ret):
    return f"`max_len = max({B.max_len}, {S.sub_len}) = {S.max_len}`：留下最长的一条往下的链"


CONFIG = dict(
    num=3203, title='合并两棵树后的最小直径', difficulty='Hard',
    category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='树的直径 · 取直径中点连接',
    tags=['动态规划', '链表树与回溯', '难度分 2266'],
    code=CODE,
    call='Solution().minimumDiameterAfterMerge([[0,1],[0,2],[0,3]], [[0,1],[1,2],[2,3]])',
    expect=4,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='text', fn=lambda S: (f"`d1 = {S.get('d1')}`　`d2 = {S.get('d2')}`" if S.get('d1') is not None else '先分别求两棵树的直径 `d1`、`d2`'), size=26, h=50),
        dict(type='text', fn=lambda S: '节点下方数字 = 该点往下的最长链（返回值）', size=20, h=34),
        dict(type='calls', h=200),
    ],
    watch=[('x', lambda S: _g(S, 'x'), 'blue'), ('fa', lambda S: _g(S, 'fa')), ('max_len', lambda S: _g(S, 'max_len'), 'yellow'),
           ('res', lambda S: S.get('res'), 'green'), ('d1', lambda S: S.get('d1')), ('d2', lambda S: S.get('d2'))],
    captions={
        'g = [[] for': '建邻接表：节点数 = 边数 + 1',
        'for x, y in edges': '无向边：两个方向都要记录',
        'res = 0': '`res` 记录这棵树的直径（最长路径的==边数==）',
        'max_len = 0': lambda S, B, r: f"进入节点 `{_g(S, 'x')}`（父亲 `{_g(S, 'fa')}`）：往下最长链先记 `0`",
        'for y in g[x]': lambda S, B, r: (f"枚举 `{_g(S, 'x')}` 的邻居 `{_g(S, 'y')}`" if _g(S, 'y') != B['_inner'].get('y') else f"`{_g(S, 'x')}` 的邻居都看完了，返回"),
        'if y != fa': lambda S, B, r: (f"`{S.y}` 是来时的父亲 `fa`，不能回头" if S.y == S.fa else f"`{S.y}` 是孩子，可以往下走"),
        'sub_len = dfs': _cap_call,
        'res = max(res': _cap_res,
        'max_len = max(max_len': _cap_max,
        'return max_len': lambda S, B, ret: f"节点 `{_g(S, 'x')}` 往下的最长链 = `{ret}`，返回给父亲",
        'dfs(0, -1)': '从节点 `0` 出发，没有父亲（`fa = -1`）',
        'return res': '这棵树的直径 = `{res}`',
        'd1 = self.diameter': '先求第一棵树的直径 `d1`',
        'd2 = self.diameter': '`d1 = {d1}`；再求第二棵树的直径 `d2`',
        'return max(d1': ('三种情况取最大：只看第一棵 `d1 = {d1}`；只看第二棵 `d2 = {d2}`；'
                         '经过新边：`({d1}+1)//2 + ({d2}+1)//2 + 1 = {(d1 + 1) // 2 + (d2 + 1) // 2 + 1}` → ==`{ret}`=='),
    },
    skip=['nonlocal res', 'g[x].append(y)', 'g[y].append(x)', 'dfs(0, -1)'],
    max_steps=120,
    cards=dict(
        one_liner='新直径 = max(d1, d2, 半径1 + 半径2 + 1)：连在两棵树的直径中点',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['给两棵无向树 `edges1`、`edges2`，各选一个点，用一条边连起来',
                 '要使新树的==直径最小==，返回这个最小直径',
                 '本视频：`edges1 = [[0,1],[0,2],[0,3]]`，`edges2 = [[0,1],[1,2],[2,3]]` → `4`'],
        quote='新树的直径相当于以下三部分之和：x1 到第一棵树最远点的距离；x2 到第二棵树最远点的距离；x1-x2 这条边的长度，即 1。选 x1 为第一棵树的直径中点，可以让 x1 到第一棵树最远点的距离最小。',
        quote_src='—— 灵茶山艾府题解',
        idea=['新树的直径要么还在原来某棵树里（`d1` 或 `d2`），要么经过新边',
              '经过新边时：连两树的==直径中点==，各自最远距离最小，分别是 `ceil(d/2)`',
              '`diameter` 用树形 DP 求：每个点合并「最长」和「次长」两条往下的链'],
        result='运行结束，返回 `4`：`d1=2`、`d2=3`，经过新边 `1 + 2 + 1 = 4`',
        summary=['时间 `O(n+m)`，空间 `O(n+m)`',
                 '易错：直径按==边数==算；`ceil(d/2)` 写成 `(d + 1) // 2`',
                 '易错：别忘了和 `d1`、`d2` 取最大，其中一棵树可能特别长',
                 '`max_len + sub_len` 无论先后，都能遇到最大值 + 次大值的组合'],
    ),
)
