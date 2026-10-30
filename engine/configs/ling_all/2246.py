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

PARENT = [-1, 0, 0, 1, 1, 2, 1]
STR = 'abacbed'
N = len(PARENT)
CH = {i: [] for i in range(N)}
for _i in range(1, N):
    CH[PARENT[_i]].append(_i)
PAR = {i: (PARENT[i] if i else None) for i in range(N)}
BAD = {(PARENT[i], i) for i in range(1, N) if STR[PARENT[i]] == STR[i]}
ORDER = _preorder(CH, 0)
RET = {}


def _sim(x):
    ml = 0
    for y in CH[x]:
        ln = _sim(y) + 1
        if STR[y] != STR[x]:
            ml = max(ml, ln)
    RET[x] = ml
    return ml


_sim(0)


def _draw(cv, S, B, box, T):
    inner = S.get('_inner', {})
    x = inner.get('x')
    y = inner.get('y')
    line = S.get('_line', 0)
    fin = fin_set(CH, ORDER, PAR, x, y, line, LEN_LINE, FOR_LINE, RET_LINE, B['_inner'].get('y'))
    # 子树已全部结束的节点：不在栈上且已访问；处于 for 循环中的父节点，已处理完的孩子也算完成
    hot = y if (x is not None and y is not None and y in CH[x] and line in (IF_LINE, ANS_LINE, MAX_LINE)) else None
    draw_gtree(cv, T, box, CH, 0, PAR, x, hot, fin, {u: f'返回 {RET[u]}' for u in fin}, BAD,
               label_fn=lambda u: f'{u}', title='树（节点内 = 编号，下方字母 = s[i]；红虚线 = 两端字符相同，不能走）')
    for u, (X, Y) in _tree_pos(CH, 0, box)[0].items():
        cv.text((X + 30, Y - 6), f"'{STR[u]}'", 22, T['yellow'], anchor='lm', bold=True, mono=True)


CODE = '''
class Solution:
    def longestPath(self, parent: List[int], s: str) -> int:
        n = len(parent)
        g = [[] for _ in range(n)]
        for i in range(1, n):
            g[parent[i]].append(i)

        ans = 0
        def dfs(x: int) -> int:
            nonlocal ans
            max_len = 0
            for y in g[x]:
                len = dfs(y) + 1
                if s[y] != s[x]:
                    ans = max(ans, max_len + len)
                    max_len = max(max_len, len)
            return max_len
        dfs(0)
        return ans + 1
'''
_CL = CODE.strip('\n').split('\n')


def _ln(sub):
    return [i + 1 for i, t in enumerate(_CL) if sub in t][0]


FOR_LINE = _ln('for y in g[x]')
RET_LINE, LEN_LINE, IF_LINE, ANS_LINE, MAX_LINE = _ln('return max_len'), _ln('len = dfs(y)'), _ln('if s[y]'), _ln('ans = max(ans'), _ln('max_len = max(max')


def _g(S, k):
    return S['_inner'].get(k)


def _cap_len(S, B, ret):
    return f"进入孩子 `{_g(S, 'x')}`：先==相信递归==，让它算出自己往下的最长链，再 `+1` 算上父子这条边"


def _cap_if(S, B, ret):
    x, y = _g(S, 'x'), _g(S, 'y')
    ok = STR[x] != STR[y]
    return f"孩子返回后 `len = {S['len']}`（含边 {x}-{y}）。相邻字符 `s[{x}]='{STR[x]}'` 与 `s[{y}]='{STR[y]}'` " + ('不同 → 这条边可以走，可以拼接' if ok else '相同 → ==这条边不能走==，孩子的链直接丢掉')


def _cap_ans(S, B, ret):
    return (f"把「已有最长链 `{B.max_len}`」和「这条新链 `{S['len']}`」拼起来（在 x 处合并两条链）："
            f"`ans = max({B.ans}, {B.max_len} + {S['len']}) = {S.ans}`")


def _cap_max(S, B, ret):
    return f"更新从 x 出发的最长链 `max_len = max({B.max_len}, {S['len']}) = {S.max_len}`，留给 x 的父亲用"


CONFIG = dict(
    num=2246, title='相邻字符不同的最长路径', difficulty='Hard',
    category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='树形 DP · 树的直径',
    tags=['动态规划', '链表树与回溯', '难度分 2126'],
    code=CODE,
    call="Solution().longestPath([-1,0,0,1,1,2,1], 'abacbed')",
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=lambda S: f"当前答案 `ans = {S.get('ans', 0)}`（最后返回 `ans + 1`，因为题目数的是点）", size=24, h=50),
        dict(type='calls', h=210),
    ],
    watch=[('x', lambda S: _g(S, 'x'), 'blue'), ('y', lambda S: _g(S, 'y'), 'pink'), ('max_len', lambda S: _g(S, 'max_len'), 'yellow'),
           ('len', lambda S: _g(S, 'len')), ('ans', 'ans', 'green')],
    captions={
        'n = len(parent)': '`parent[i]` 是 i 的父亲，节点数 `n = {n}`',
        'g[parent[i]].append(i)': '把 `i` 挂到父亲 `parent[i]` 的孩子列表里：`g[x]` = x 的所有孩子',
        'ans = 0': '`ans` 记录最长路径的==边数==',
        'max_len = 0': lambda S, B, r: f"进入节点 `{_g(S, 'x')}`：从 x 往下的最长合法链先记为 `0`",
        'for y in g[x]': lambda S, B, r: (f"枚举 `{_g(S, 'x')}` 的孩子 `{_g(S, 'y')}`" if _g(S, 'y') != B['_inner'].get('y') else f"`{_g(S, 'x')}` 的孩子都处理完了，该返回了"),
        'len = dfs(y) + 1': _cap_len,
        'if s[y] != s[x]': _cap_if,
        'ans = max(ans': _cap_ans,
        'max_len = max(max': _cap_max,
        'return max_len': lambda S, B, ret: f"节点 `{_g(S, 'x')}` 处理完：最长合法链长 `{ret}`，返回给父亲",
        'dfs(0)': '从根节点 `0` 出发，只遍历一遍',
        'return ans + 1': '`ans` 是边数，点数 = 边数 + 1 → 返回 `{ans + 1}`',
    },
    skip=['nonlocal ans', 'dfs(0)', 'for i in range(1, n)'],
    max_steps=130,
    cards=dict(
        one_liner='树的直径 + 一个 `if`：只合并字符不同的孩子',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['有根树，`parent[i]` 是 `i` 的父亲，节点 `i` 的字符是 `s[i]`',
                 '找一条路径，==任意相邻两点字符都不同==，使点数最多',
                 '示例：`parent = [-1,0,0,1,1,2]`，`s = "abacbe"` → `3`（本视频用 7 个节点的小树）'],
        quote='考虑用树形 DP 求直径。枚举子树 x 的所有子树 y，维护从 x 出发的最长路径 maxLen，那么可以更新答案为从 y 出发的最长路径加上 maxLen，再加上 1（边 x-y），即合并从 x 出发的两条路径。',
        quote_src='—— 灵茶山艾府题解',
        idea=['没有字符限制时，这就是「树的直径」：每个点 x 合并两条最长往下的链',
              '本题只在 `s[y] != s[x]` 时才让孩子 y 参与，其余照抄',
              '`max_len + len` 一定会遇到「最大值 + 次大值」的组合：先后顺序无所谓'],
        result='运行结束，`ans = 2` 条边 → 返回 `2 + 1 = 3`',
        summary=['时间 `O(n)`，空间 `O(n)`（递归栈）',
                 '易错：`ans` 数的是边，题目要点数，最后 `+1`',
                 '易错：字符相同的孩子既不能更新 `ans`，也不能更新 `max_len`',
                 '代码里把 `len` 当变量名，会遮住内置函数 `len`；所以建树要写在前面'],
    ),
)
