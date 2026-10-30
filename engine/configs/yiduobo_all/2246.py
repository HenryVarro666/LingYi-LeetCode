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

PARENT = [-1, 0, 0, 1, 1, 2]
STR = 'aabcba'
N = len(PARENT)
CH = {i: [] for i in range(N)}
for _i in range(1, N):
    CH[PARENT[_i]].append(_i)
PAR = {i: (PARENT[i] if i else None) for i in range(N)}
BAD = {(PARENT[i], i) for i in range(1, N) if STR[PARENT[i]] == STR[i]}
ORDER = _preorder(CH, 0)
RET = {}


def _sim(now):
    res, chain = 1, 1
    for ch in CH[now]:
        r, c = _sim(ch)
        res = max(res, r)
        if STR[now] != STR[ch]:
            res = max(res, chain + c)
            chain = max(chain, c + 1)
    RET[now] = (res, chain)
    return res, chain


_sim(0)


def _g(S, k):
    return S['_inner'].get(k)


def _draw(cv, S, B, box, T):
    inner = S.get('_inner', {})
    x = inner.get('now')
    child = inner.get('child')
    line = S.get('_line', 0)
    fin = fin_set(CH, ORDER, PAR, x, child, line, R_LINE, FOR_LINE, RET_LINE, B['_inner'].get('child'))
    hot = child if (x is not None and child is not None and child in CH[x] and line in (RES1_LINE, IF_LINE, RES2_LINE, CHAIN_LINE)) else None
    draw_gtree(cv, T, box, CH, 0, PAR, x, hot, fin, {u: f'({RET[u][0]}, {RET[u][1]})' for u in fin}, BAD,
               label_fn=lambda u: f'{u}', title='树（节点内 = 编号，旁边字母 = s[i]；红虚线 = 两端字符相同，不能拼）')
    for u, (X, Y) in _tree_pos(CH, 0, box)[0].items():
        cv.text((X + 30, Y - 6), f"'{STR[u]}'", 22, T['yellow'], anchor='lm', bold=True, mono=True)
CODE = '''
class Solution(object):
    def longestPath(self, parent, s):

        childs = {}
        for index, p in enumerate(parent):
            if index > 0:
                if p not in childs:
                    childs[p] = set()
                childs[p].add(index)

        def dfs(now):
            res = 1
            chain = 1

            for child in childs.get(now, set()):
                r, c = dfs(child)
                res = max(res, r)
                if s[now] != s[child]:
                    res = max(res, chain + c)
                    chain = max(chain, c + 1)

            return res, chain
        
        return dfs(0)[0]
'''
_CL = CODE.strip('\n').split('\n')


def _ln(sub):
    return [i + 1 for i, t in enumerate(_CL) if sub in t][0]


FOR_LINE = _ln('for child in')
RET_LINE, R_LINE, RES1_LINE, IF_LINE, RES2_LINE, CHAIN_LINE = (_ln('return res, chain'), _ln('r, c = dfs'), _ln('res = max(res, r)'),
                                                              _ln('if s[now]'), _ln('chain + c'), _ln('c + 1'))


def _cap_r(S, B, ret):
    return f"进入孩子 `{_g(S, 'now')}`（初始 `res = chain = 1`，只有它自己）：先让它递归算出（子树最长路径 `r`，以它为端点的最长链 `c`）"


def _cap_res1(S, B, ret):
    return f"孩子 `{_g(S, 'child')}` 返回 `r = {S.r}`、`c = {S.c}`：先用 `r` 更新答案（最长路径可能整个在孩子子树里）→ `res = {S.res}`"


def _cap_if(S, B, ret):
    n, c = S.now, S.child
    ok = STR[n] != STR[c]
    return f"`s[{n}]='{STR[n]}'` 与 `s[{c}]='{STR[c]}'` " + ('不同 → 孩子的链可以接在 now 下面' if ok else '相同 → 这条链不能用，跳过')


def _cap_res2(S, B, ret):
    return f"两条链在 `now` 处拼接：现有链 `chain = {B.chain}` + 孩子的链 `c = {S.c}` → `res = max({B.res}, {B.chain + S.c}) = {S.res}`"


def _cap_chain(S, B, ret):
    return f"链长更新：孩子的链 `c + 1 = {S.c + 1}`（把 now 算进去），`chain = max({B.chain}, {S.c + 1}) = {S.chain}`"


CONFIG = dict(
    num=2246, title='相邻字符不同的最长路径', difficulty='Hard',
    category='链表、二叉树与回溯',
    author='yiduobo', technique='树形 DP · 返回 (最长路径, 最长链)',
    tags=['动态规划', '链表树与回溯', '难度分 2126'],
    code=CODE,
    call="Solution().longestPath([-1,0,0,1,1,2], 'aabcba')",
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=lambda S: (f"当前节点 `now = {_g(S, 'now')}`　`res = {_g(S, 'res')}`　`chain = {_g(S, 'chain')}`" if _g(S, 'now') is not None else ''), size=24, h=50),
        dict(type='calls', h=210),
    ],
    watch=[('now', lambda S: _g(S, 'now'), 'blue'), ('child', lambda S: _g(S, 'child'), 'pink'),
           ('res', lambda S: _g(S, 'res'), 'green'), ('chain', lambda S: _g(S, 'chain'), 'yellow'),
           ('r', lambda S: _g(S, 'r')), ('c', lambda S: _g(S, 'c'))],
    captions={
        'childs = {}': '`childs` 记录每个节点的孩子集合（原文用字典 + 集合建树）',
        'childs[p].add(index)': '`index` 是 `p` 的孩子：`childs[{p}]` 里加入 `{index}`',
        'res = 1': lambda S, B, r: f"进入节点 `{_g(S, 'now')}`：叶子的路径只有它自己，`res = 1`（数点）",
        'chain = 1': '`chain` = 以 now 为端点往下的最长链（点数），先是 `1`',
        'for child in': lambda S, B, r: (f"枚举孩子 `{_g(S, 'child')}`" if _g(S, 'child') != B['_inner'].get('child') else f"`{_g(S, 'now')}` 的孩子都处理完了，该返回了"),
        'r, c = dfs(child)': _cap_r,
        'res = max(res, r)': _cap_res1,
        'if s[now] != s[child]': _cap_if,
        'chain + c': _cap_res2,
        'c + 1': _cap_chain,
        'return res, chain': lambda S, B, ret: f"节点 `{_g(S, 'now')}` 返回 `(res, chain) = {ret}`：子树最长路径 `{ret[0]}`，以它为端点的链 `{ret[1]}`",
        'return dfs(0)[0]': '整棵树的 `res` 就是答案：`{ret}`',
    },
    skip=['res = 1', 'chain = 1', 'for index, p in enumerate', 'if index > 0', 'if p not in childs', 'childs[p] = set()'],
    max_steps=140,
    cards=dict(
        one_liner='每个节点返回两个数：子树里最长路径、以自己为端点的最长链',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['有根树，`parent[i]` 是 `i` 的父亲，节点 `i` 的字符是 `s[i]`',
                 '找一条路径，==相邻节点字符都不同==，使点数最多',
                 '本视频：`parent = [-1,0,0,1,1,2]`，`s = "aabcba"` → `3`'],
        quote='对于以节点root为根节点的子树来说，这颗数中的最长路径可能有两种情况。第一种是出现在更深的子树当中，通常的做法是递归求解。另一种则是由至多两条以root某个孩子为端点的树链，与root拼接起来形成的路径。',
        quote_src='—— yiduobo 知乎题解',
        idea=['路径要么藏在某个孩子的子树里（取 `r`），要么经过 now，由两条链拼成',
              '递归返回 `res`（子树最长路径）和 `chain`（以当前节点为端点的最长链）',
              '孩子字符和 now 相同时，既不能拼接也不能延长链；叶子的 `res = chain = 1`'],
        result='运行结束，返回 `res = 3`：路径 `3 → 1 → 4`（字符 c a b）',
        summary=['时间 `O(n)`，空间 `O(n)`（递归栈 + 孩子字典）',
                 '易错：这里 `res` 和 `chain` 都按==点数==从 1 开始，不用像灵神那样最后加 1',
                 '易错：先用旧的 `chain` 拼接 `chain + c`，再更新 `chain`，顺序不能反',
                 '对比灵神：灵神把 `ans` 放外面、返回单个值；yiduobo 每层返回 `(res, chain)`',
                 '原文已是 Python 3 可运行的写法，没有改动代码'],
    ),
)
