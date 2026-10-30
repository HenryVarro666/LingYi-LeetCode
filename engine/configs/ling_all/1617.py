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

N = 3
EDGES = [[1, 2], [2, 3]]
ROOT = 1   # 只用于布局：路径 0-1-2 以 1 为中心画
CH = {1: [0, 2], 0: [], 2: []}


def _bits(m):
    return {i for i in range(N) if m >> i & 1}


def _draw(cv, S, B, box, T):
    inner = S.get('_inner', {})
    mask = S.get('mask')
    if mask is None:
        mask = 0
    vis = S.get('vis') if isinstance(S.get('vis'), int) else 0
    x, y = inner.get('x'), inner.get('y')
    line = S.get('_line', 0)
    ms, vs = _bits(mask), _bits(vis)

    def nc(u):
        if u in vs:
            return 'green'
        if u in ms:
            return 'cyan'
        return None
    hot = y if (y is not None and x is not None and line in (IF_LINE, ML_LINE, DIA_LINE, MAXL_LINE)) else None
    draw_gtree(cv, T, box, CH, ROOT, {}, x if (x is not None and 'max_len' in inner) else None, hot, set(), None, (),
               label_fn=lambda u: f'{u}', node_color=nc,
               title='树（城市编号已改为从 0 开始；青 = 在 mask 里，绿 = 已访问，灰 = 不在子集里）')
    X0, Y0 = box[0] + 24, box[3] - 38
CODE = '''
class Solution:
    def countSubgraphsForEachDiameter(self, n: int, edges: List[List[int]]) -> List[int]:
        # 建树
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x - 1].append(y - 1)
            g[y - 1].append(x - 1)  # 编号改为从 0 开始

        ans = [0] * (n - 1)
        #  二进制枚举
        for mask in range(3, 1 << n):
            if (mask & (mask - 1)) == 0:  # 需要至少两个点
                continue
            # 求树的直径
            vis = diameter = 0
            def dfs(x: int) -> int:
                nonlocal vis, diameter
                vis |= 1 << x  # 标记 x 访问过
                max_len = 0
                for y in g[x]:
                    if (vis >> y & 1) == 0 and mask >> y & 1:  # y 没有访问过且在 mask 中
                        ml = dfs(y) + 1
                        diameter = max(diameter, max_len + ml)
                        max_len = max(max_len, ml)
                return max_len
            dfs(mask.bit_length() - 1)  # 从一个在 mask 中的点开始递归
            if vis == mask:
                ans[diameter - 1] += 1
        return ans
'''
_CL = CODE.strip('\n').split('\n')


def _ln(sub):
    return [i + 1 for i, t in enumerate(_CL) if sub in t][0]


IF_LINE, ML_LINE, DIA_LINE, MAXL_LINE = _ln('if (vis >> y'), _ln('ml = dfs'), _ln('diameter = max(diameter'), _ln('max_len = max(max_len')


def _g(S, k):
    return S['_inner'].get(k)


def _mask_txt(S):
    m = S.get('mask')
    if m is None:
        return '枚举所有城市子集：用二进制数 `mask` 表示，第 i 位为 1 表示选了城市 i'
    vis = S.get('vis')
    sub = '{' + ','.join(str(i) for i in range(N) if m >> i & 1) + '}'
    t = f"`mask = {m:0{N}b}` → 子集 `{sub}`"
    if isinstance(vis, int):
        t += f"　`vis = {vis:0{N}b}`　`diameter = {S.get('diameter')}`"
    return t


def _cap_mask(S, B, r):
    m = S.mask
    if B.get('mask') == m:
        return f"所有子集枚举完毕（`mask` 到 `{m:0{N}b}` 为止）"
    sub = '{' + ','.join(str(i) for i in range(N) if m >> i & 1) + '}'
    return f"试下一个子集：`mask = {m:0{N}b}` 对应城市 `{sub}`"


def _cap_two(S, B, r):
    m = S.mask
    if (m & (m - 1)) == 0:
        return f"试子集 `mask = {m:0{N}b}`：只有 1 个城市，直径是 0，没有对应的 `d`，跳过"
    sub = '{' + ','.join(str(i) for i in range(N) if m >> i & 1) + '}'
    return f"试子集 `mask = {m:0{N}b}` = `{sub}`：至少 2 个城市，值得算直径"


def _cap_if(S, B, r):
    x, y = _g(S, 'x'), _g(S, 'y')
    vis, m = S.vis, S.mask
    if vis >> y & 1:
        return f"邻居 `{y}` 已经访问过（是来时的路），不回头"
    if not (m >> y & 1):
        return f"邻居 `{y}` 不在 `mask` 里，这条边被排除"
    return f"邻居 `{y}` 在 `mask` 里且没访问过 → 往下走"


def _cap_vis(S, B, r):
    return f"进入节点 `{_g(S, 'x')}`，标记访问：`vis = {S.vis:0{N}b}`（`vis`、`diameter` 每个子集重新从 0 开始；`max_len` 记往下最长链，先为 0）"


def _cap_check(S, B, r):
    m, v = S.mask, S.vis
    if v == m:
        return f"`vis == mask`：子集里的城市全访问到了 → 是一棵连通的树，直径 `{S.diameter}` → `ans[{S.diameter - 1}] += 1`"
    return f"`vis = {v:0{N}b}` ≠ `mask = {m:0{N}b}`：有城市没连上 → 是森林，不算"


CONFIG = dict(
    num=1617, title='统计子树中城市之间最大距离', difficulty='Hard',
    category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='二进制枚举子集 + 树的直径',
    tags=['动态规划', '数学算法', '难度分 2309'],
    code=CODE,
    call='Solution().countSubgraphsForEachDiameter(3, [[1,2],[2,3]])',
    expect=[2, 1],
    views=[
        dict(type='custom', draw=_draw, h=250),
        dict(type='text', fn=_mask_txt, size=24, h=50),
        dict(type='array', var=lambda S: S.get('ans') if isinstance(S.get('ans'), list) else [], label='ans[d-1]：直径恰好为 d 的子树数', cell=84, h=130),
        dict(type='calls', h=150, hide=('edges',)),
    ],
    watch=[('mask', 'mask', 'blue'), ('vis', lambda S: S.get('vis'), 'green'), ('diameter', lambda S: S.get('diameter'), 'yellow'),
           ('x', lambda S: _g(S, 'x'), 'blue'), ('max_len', lambda S: _g(S, 'max_len'))],
    captions={
        'g = [[] for': '建树：`g[x]` 是城市 x 的邻居（编号减 1，改成从 0 开始）',
        'ans = [0] * (n - 1)': '`ans[d-1]` 记录最大距离恰为 `d` 的子树个数',
        'for mask in range': _cap_mask,
        'if (mask & (mask - 1)) == 0': _cap_two,
        'vis = diameter = 0': '`vis` 也是二进制：记录 DFS 走到过哪些城市；`diameter` 记录直径',
        'vis |= 1 << x': _cap_vis,
        'max_len = 0': lambda S, B, r: f"进入节点 `{_g(S, 'x')}`：往下最长链先记 `0`",
        'for y in g[x]': lambda S, B, r: (f"枚举 `{_g(S, 'x')}` 的邻居 `{_g(S, 'y')}`" if _g(S, 'y') != B['_inner'].get('y') else f"`{_g(S, 'x')}` 的邻居都看完了"),
        'if (vis >> y': _cap_if,
        'ml = dfs(y) + 1': lambda S, B, r: f"进入 `{_g(S, 'x')}`：往下找最长链，回来后 `+1` 算上这条边",
        'diameter = max(diameter': lambda S, B, r: f"在 `{_g(S, 'x')}` 处拼接两条链：`max({B.diameter}, {B.max_len} + {S.ml}) = {S.diameter}`",
        'max_len = max(max_len': lambda S, B, r: f"`max_len = max({B.max_len}, {S.ml}) = {S.max_len}`",
        'return max_len': lambda S, B, ret: f"节点 `{_g(S, 'x')}` 往下最长链 `{ret}`，返回给父亲",
        'dfs(mask.bit_length() - 1)': '从 `mask` 里的最高位城市出发 DFS，这个点一定在子集里',
        'if vis == mask': _cap_check,
        'ans[diameter - 1] += 1': '`ans = {ans}`',
        'return ans': '所有子集枚举完：`ans = {ret}`',
    },
    skip=['for mask in range', 'for y in g[x]', 'vis = diameter = 0', 'max_len = 0', 'nonlocal vis', 'continue', 'g[x - 1].append', 'g[y - 1].append'],
    max_steps=120,
    cards=dict(
        one_liner='枚举所有城市子集，只统计连通的，再用树形 DP 求直径',
        complexity='时间 `O(n·2^n)`，空间 `O(n)`',
        problem=['`n` 个城市组成一棵树，对每个 `d = 1..n-1`',
                 '数出「最大距离恰好为 `d` 的连通子集」有多少个',
                 '本视频：`n = 3`，`edges = [[1,2],[2,3]]` → `[2, 1]`'],
        quote='枚举的子集不一定是一棵树，可能是森林。我们可以在计算树形 DP 的同时去统计访问过的点，看看是否与子集相等，只有相等才是一棵树。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`n ≤ 15`，直接用二进制数 `mask` 枚举 `2^n` 个子集',
              '对每个 `mask`，从其中一点 DFS，只走 `mask` 里的点，同时求直径',
              '`vis == mask` 说明所有点都连上了，才是一棵树；否则是森林，丢掉'],
        result='运行结束，返回 `[2, 1]`：直径 1 的有 `{0,1}`、`{1,2}`；直径 2 的有 `{0,1,2}`',
        summary=['时间 `O(n·2^n)`，空间 `O(n)`',
                 '易错：必须检查 `vis == mask`，否则不连通的子集会被误计',
                 '易错：只有 1 个点的子集直径为 0，没有对应的 `d`，要跳过',
                 '方法一用回溯枚举子集；方法三枚举直径端点 + 乘法原理，`O(n^3)`'],
    ),
)
