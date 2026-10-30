def _tree_pos(ch, root=0):
    """一般树自动布局：叶子按顺序排开，父亲在孩子中间。返回 {节点: (x 0~1, 深度)}"""
    pos, cnt = {}, [0]
    leaves = sum(1 for _ in _leaves(ch, root))
    def go(u, d):
        kids = ch.get(u, [])
        if not kids:
            pos[u] = ((cnt[0] + 0.5) / leaves, d); cnt[0] += 1
        else:
            for k in kids:
                go(k, d + 1)
            pos[u] = ((pos[kids[0]][0] + pos[kids[-1]][0]) / 2, d)
    go(root, 0)
    return pos


def _leaves(ch, u):
    kids = ch.get(u, [])
    if not kids:
        yield u
    for k in kids:
        yield from _leaves(ch, k)


def _gt_draw(cv, S, B, box, T, ch, pos, edges, node_fn, extra=None, title=''):
    """edges: [(父,子,颜色名或None,虚线)]；node_fn(S,u)->(填充色, 主文字, 副文字)"""
    x0, y0, x1, y1 = box
    maxd = max(d for _, d in pos.values())
    W, H = x1 - x0 - 300, y1 - y0 - 110
    P = {u: (x0 + 110 + px * W, y0 + 70 + (d / max(maxd, 1)) * H) for u, (px, d) in pos.items()}
    if title:
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    for a, b, col, dash in edges:
        pa, pb = P[a], P[b]
        if dash == 'arc':  # 从孩子 b 绕一道弧线指向 a（向左侧鼓出）
            cx, cy = min(pa[0], pb[0]) - 110, (pa[1] + pb[1]) / 2
            pts = [((1 - t) ** 2 * pb[0] + 2 * (1 - t) * t * cx + t * t * pa[0],
                    (1 - t) ** 2 * pb[1] + 2 * (1 - t) * t * cy + t * t * pa[1]) for t in [0.12 + 0.76 * i / 30 for i in range(31)]]
            cv.line(pts, T[col], 5)
            cv.arrow(pts[-3], pts[-1], T[col], 5, 16)
        elif dash:
            cv.dashed(pb, pa, T[col], 4)
        else:
            cv.line([pa, pb], T[col] if col else T['border'], 4 if col else 3)
    R = 24
    for u, (X, Y) in P.items():
        fill, main, sub = node_fn(S, u)
        cv.rect((X - R, Y - R, X + R, Y + R), fill=T[fill] if isinstance(fill, str) else fill, outline=T['border'], r=R, width=2)
        cv.text((X, Y), main, 24, T['text'] if fill == 'panel2' else T['bg'], anchor='mm', bold=True, mono=True)
        if sub:
            cv.text((X + R + 8, Y), sub, 20, T['text'], anchor='lm', bold=True)
    if extra:
        extra(cv, P, T)
    return P
PAR = [-1, 0, 4, 0, 1]
STR = 'abbba'
CH = {}
for _i in range(1, len(PAR)):
    CH.setdefault(PAR[_i], []).append(_i)
POS = _tree_pos(CH)
_X = lambda S: S['_inner'].get('x')


def _node(S, u):
    I = S['_inner']
    size = S.get('size')
    sub = f'{STR[u]} · size {size[u]}' if size else STR[u]
    if I.get('x') == u:
        return 'yellow', str(u), sub
    anc = S.get('ancestor') or {}
    if u in anc.values():
        return 'cyan', str(u), sub
    return 'panel2', str(u), sub


def _extra(cv, P, T):
    pass


def _draw(cv, S, B, box, T):
    I = S['_inner']
    edges = [(a, b, None, False) for a, ks in CH.items() for b in ks]
    x, y, anc = I.get('x'), I.get('y'), I.get('anc')
    if y is not None and anc is not None and S['_line'] in (15, 16):
        edges = [e for e in edges if e[1] != y or anc < 0]
        if anc >= 0:
            edges.append((anc, y, 'orange', 'arc'))
        edges.append((x, y, 'green', False) if anc < 0 else (x, y, 'red', True))
    _gt_draw(cv, S, B, box, T, CH, POS, edges, _node,
             title='原树（黄 = 当前 x，青 = 路径上各字母的最近节点，橙弧线 = 改挂到同字母祖先）')


def _fmt_anc(k, v):
    return f'{v}'


def _txt(S):
    I = S['_inner']
    if 'y' in I and 'anc' in I and S['_line'] in (15, 16):
        y, anc, x = I['y'], I['anc'], I['x']
        tgt = x if anc < 0 else anc
        return f"`s[{y}] = '{STR[y]}'`：最近同字母祖先 = {'无' if anc < 0 else anc}，`size[{y}]` 加到 ==size[{tgt}]=="
    if 'x' in I:
        return f"进入节点 `{I['x']}`（字母 `{STR[I['x']]}`）"
    return ''


CONFIG = dict(
    num=3331, title='修改后子树的大小', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='一次 DFS · 最近同字母祖先',
    tags=['灵神题单', '链表树与回溯', '难度分 2046'],
    code='''
class Solution:
    def findSubtreeSizes(self, parent: List[int], s: str) -> List[int]:
        n = len(parent)
        g = [[] for _ in range(n)]
        for i in range(1, n):
            g[parent[i]].append(i)

        size = [1] * n
        ancestor = defaultdict(lambda: -1)
        def dfs(x: int) -> None:
            old = ancestor[s[x]]
            ancestor[s[x]] = x
            for y in g[x]:
                dfs(y)
                anc = ancestor[s[y]]
                size[x if anc < 0 else anc] += size[y]
            ancestor[s[x]] = old  # 恢复现场
        dfs(0)
        return size
''',
    call="Solution().findSubtreeSizes([-1,0,4,0,1], 'abbba')",
    expect=[5, 2, 1, 1, 1],
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var='size', label='size（每个点先算自己 = 1）', cell=60, h=140,
             pointers={_X: 'yellow'}, pointer_labels={_X: 'x'}),
        dict(type='map', var='ancestor', label='ancestor：字母 → 路径上最深的节点（-1 = 没有）', h=120,
             fmt=lambda k, v: f'{k}: {v}'),
        dict(type='calls', h=100),
    ],
    watch=[('x', "x if 'x' in _inner else ''", 'yellow'), ('y', "y if 'y' in _inner else ''", 'blue'), ('anc', "anc if 'anc' in _inner else ''", 'orange')],
    captions={
        'old = ancestor': '先记下 `old = ancestor[{s[x]!r}] = {old}`：这是进入 `{x}` 之前，字母 `{s[x]}` 的最近节点，回溯时要还原',
        'ancestor[s[x]] = x': '`{x}` 成为字母 `{s[x]}` 的最近节点：==它的后代里同字母的点都会挂到它下面==',
        'dfs(y)': '先递归孩子 `{y}`：等它的 `size[{y}]` 算完再往上加',
        'anc = ancestor': "`{y}` 的字母是 `{s[y]}`，最近的同字母祖先 `anc = {anc}`" + "（-1 表示没有，保留原来的父亲）",
        'size[x if': '`{y}` 的子树大小 `{size[y]}` 加到 ==size[{(x if anc < 0 else anc)}]==：' + '{"没有同字母祖先，仍加给父亲 x" if anc < 0 else "改挂到同字母祖先 anc，而不是父亲 x"}',
        'ancestor[s[x]] = old': '回溯：`ancestor[{s[x]!r}]` 还原成 `{old}`，兄弟分支看不到 `{x}`',
        'dfs(0)': '从根 `0` 开始，一次 DFS 同时完成「改边」和「算子树大小」',
        'return size': '`size = {size}`',
    },
    cards=dict(
        one_liner='递归时记下每个字母最近的祖先，回来时把大小直接加给它',
        complexity='时间 `O(n+|Σ|)`，空间 `O(n)`',
        problem=['树由 `parent` 给出，`s[i]` 是节点 `i` 的字母',
                 '每个点 `x` 同时改挂到==最近的同字母祖先== `y`（没有就不动）',
                 '求改完后每个点的子树大小。示例：`[-1,0,4,0,1]`，`"abbba"` → `[5,2,1,1,1]`'],
        quote='把两个 DFS 结合起来。在 dfs(y) 结束后，分类讨论：如果 y 没有对应的祖先，把 size[x] 增加 size[y]；如果 y 有对应的祖先 anc，把 size[anc] 增加 size[y]。',
        quote_src='—— 灵茶山艾府题解（方法二：一次 DFS）',
        idea=['「同时」改边的关键：祖先要按==原树==来找，所以不真的改树',
              '递的时候维护 `ancestor[字母]` = 路径上该字母最深的节点',
              '归的时候 `size[y]` 加给 `ancestor[s[y]]`，没有才加给父亲 `x`'],
        summary=['时间 `O(n+|Σ|)`，空间 `O(n)`',
                 '易错点：==回溯时要还原 ancestor==，否则兄弟分支会串味',
                 '易错点：先 `dfs(y)` 再读 `ancestor[s[y]]`，此时 y 自己已还原，读到的是它的真正祖先',
                 '方法一是两次 DFS：先改边再算大小，写法更长，注意遍历列表时别遍历到新加入的点'],
    ),
)
