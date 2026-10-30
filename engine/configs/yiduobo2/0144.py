# ---- 这种写法会给树“加边”（最右节点的 right 指向别处），tree 视图的自动布局会乱，
# ---- 所以用 custom 视图：节点位置按原树固定；原来的边画灰线，新连上的右指针画粉色弧线。
VALS = [1, 2, 3, 4, 5, None, 6]
REF = Tr(VALS)            # 只用来算固定布局和“原来的儿子是谁”
PTRS = [('now', 'blue'), ('rightest', 'pink')]


def _ref_info(root):
    pos, kids, order = {}, {}, []

    def ino(n, d):
        if n is None:
            return
        ino(n.left, d + 1)
        order.append((n.val, d))
        ino(n.right, d + 1)
        kids[n.val] = (n.left.val if n.left else None, n.right.val if n.right else None)
    ino(root, 0)
    for i, (v, d) in enumerate(order):
        pos[v] = (i, d)
    return pos, kids


POS, KIDS = _ref_info(REF)


def _nodes(S):
    out, st = {}, [S.get('root')]
    while st:
        x = st.pop()
        if x is None or x.val in out:
            continue
        out[x.val] = x
        st += [x.left, x.right]
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '二叉树（粉色弧线 = 新连上的右指针，绿 = 已记录）', 24, T['muted'], bold=True)
    nodes = _nodes(S)
    n_cols = len(POS)
    sp = min(130, (x1 - x0 - 80) / n_cols)
    dy, rad = 110, 30
    sx = x0 + 40 + ((x1 - x0 - 80) - sp * n_cols) / 2 + sp / 2

    def P(v):
        i, d = POS[v]
        return sx + i * sp, y0 + 90 + d * dy

    done = set(S.get('res') or [])
    for v, (lv, rv) in KIDS.items():
        for cv_ in (lv, rv):
            if cv_ is not None:
                cv.line([P(v), P(cv_)], T['border'], 4)
    for v, n in nodes.items():
        ch = n.right
        if ch is None or ch.val == KIDS[v][1]:
            continue
        (X, Y), (X2, Y2) = P(v), P(ch.val)
        if abs(Y - Y2) < 1:   # 同一层：从下面绕过去
            p0, p1 = (X + rad * 0.5, Y + rad * 0.9), (X2 - rad * 0.5, Y2 + rad + 6)
            mid = cv.arc_arrow(p0, p1, -70, T['pink'], 3, 13)
            cv.text((mid[0], mid[1] + 8), f'{v}.right → {ch.val}', 20, T['pink'], anchor='mt', bold=True)
        else:                 # 指向更高层：从上面绕过去
            p0, p1 = (X + rad * 0.7, Y - rad * 0.75), (X2 - rad * 0.55, Y2 + rad + 6)
            mid = cv.arc_arrow(p0, p1, max(60, (Y - Y2) * 0.5 + 40), T['pink'], 3, 13)
            cv.text((mid[0] - 6, mid[1] - 8), f'{v}.right → {ch.val}', 20, T['pink'], anchor='rb', bold=True)
    hits = {}
    for name, c in PTRS:
        x = S.get(name)
        if isinstance(x, TreeNode):
            hits.setdefault(x.val, []).append((name, T[c]))
    for v in POS:
        X, Y = P(v)
        hs = hits.get(v, [])
        fill = T['green'] if v in done else T['panel2']
        outline = hs[0][1] if hs else T['border']
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=outline, width=5 if hs else 2)
        cv.text((X, Y), str(v), 28, T['bg'] if v in done else T['text'], anchor='mm', bold=True)
        for r, (name, c) in enumerate(hs):
            cv.text((X - rad - 6, Y - rad - 2 - r * 24), name, 21, c, anchor='rb', bold=True)


def _cap_while(S, B, ret):
    if B.now is not None:
        return f'`now = {B.now.val}` 不为空 → 继续'
    return '`now` 为空 → 结束'


def _cap_if_left(S, B, ret):
    v = S.now
    if v.left is not None:
        r = f'，右子树 `{v.right.val}` ==不能丢==' if v.right is not None else ''
        return f'`{v.val}` 有左孩子 → 下一步去左子树{r}'
    return f'`{v.val}` 没有左孩子'


def _cap_wr(S, B, ret):
    r = S.rightest
    if r.right is not None:
        return f'`{r.val}` 还有右孩子 → 继续往右'
    return f'`{r.val}` 没有右孩子 → 它就是左子树的最右节点：==左子树里最后被先序访问到的=='


def _cap_link(S, B, ret):
    r, now = S.rightest, S.now
    if now.right is None:
        return f'`{now.val}` 没有右子树：`{r.val}.right = None`，什么也不变'
    return (f'`{r.val}.right = {now.val}.right`（即 `{now.right.val}`）：'
            f'==左子树走完，就自然走到右子树==')


def _cap_elif(S, B, ret):
    v = S.now
    if v.right is None:
        return f'`{v.val}` 左右都没有路'
    if KIDS[v.val][1] != v.right.val:
        return f'`{v.val}` 没有原来的右孩子，但有==之前连上的边== → `{v.right.val}`'
    return f'`{v.val}` 有右孩子 `{v.right.val}` → 往右走'


def _cap_go_right(S, B, ret):
    b = B.now
    if KIDS[b.val][1] != S.now.val:
        return f'顺着连好的边，从左子树==跳到右子树== `{S.now.val}`'
    return f'进入右子树：`now = {S.now.val}`'


CONFIG = dict(
    num=144, title='二叉树的前序遍历', difficulty='Easy', category='二叉树',
    author='yiduobo', technique='非递归 · 左子树最右节点接上右子树',
    tags=['字节30天', '热题173'],
    code='''
class Solution(object):
    def preorderTraversal(self, root):
        if not root:
            return []

        res = []
        now = root
        while now:
            res.append(now.val)
            if now.left:
                rightest = now.left
                while rightest.right:
                    rightest = rightest.right
                rightest.right = now.right
                now = now.left
            elif now.right:
                now = now.right
            else:
                break

        return res
''',
    call=f'Solution().preorderTraversal(Tr({VALS}))',
    expect=[1, 2, 4, 5, 3, 6],
    views=[
        dict(type='custom', draw=_draw, h=440),
        dict(type='array', var='res', label='res（先序：根-左-右）', cell=80),
    ],
    watch=[('now', 'now', 'blue'), ('rightest', 'rightest', 'pink'), ('res', 'res', 'green')],
    captions={
        'if not root': '树非空，开始遍历',
        'res = []': '`res` 按==根-左-右==收集节点值',
        'now = root': '`now` 从根出发：==不用递归，也不用栈==',
        'while now:': _cap_while,
        'res.append(now.val)': '先序：一走到 `{now.val}` 就记录 → `res = {res}`',
        'if now.left:': _cap_if_left,
        'rightest = now.left': '从左孩子 `{rightest.val}` 出发，一直往右找最右节点',
        'while rightest.right:': _cap_wr,
        'rightest = rightest.right': '往右走：`rightest = {rightest.val}`',
        'rightest.right = now.right': _cap_link,
        'now = now.left': '安心进入左子树：`now = {now.val}`',
        'elif now.right:': _cap_elif,
        'now = now.right': _cap_go_right,
        'break': '没有任何路可走 → ==所有节点都访问过了==，跳出循环',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='把左子树最右节点的 right 接到右子树，一路“有左走左、否则走右”',
        complexity='时间 `O(n)`，额外空间 `O(1)`',
        problem=['给你二叉树的根节点 `root`，返回它节点值的==前序==遍历（根-左-右）',
                 '示例：`[1,null,2,3]` → `[1,2,3]`',
                 '本视频：`[1,2,3,4,5,null,6]` → `[1,2,4,5,3,6]`'],
        quote='相比中序遍历的左-根-右，将左子树的最右节点的右孩子设置为根节点，这里前序遍历的根-左-右则是==将左子树的最右节点的右孩子设置为根节点的右孩子==即可。',
        quote_src='—— yiduobo 题解',
        idea=['先序访问完左子树后紧接着就是右子树；左子树里==最后==访问的是它的最右节点',
              '让 `rightest.right = now.right`：走完左子树就自然走进右子树',
              '于是每个节点：记录 → 有左走左，否则走右，无路可走就结束'],
        result='运行结束，返回 `[1,2,4,5,3,6]` ✓（树上多了两条粉色的边）',
        summary=['时间 `O(n)`，额外空间 `O(1)`（不用栈和递归）',
                 '和第 94 题同一个套路：中序连回==根==，先序连向==根的右孩子==',
                 '注意：连上的边不会被拆掉，==原树结构被修改了==',
                 '易错：必须先 `rightest.right = now.right`，再 `now = now.left`',
                 '原文为 Python 2 风格，仅删去 docstring 和 TreeNode 定义注释'],
    ),
)
