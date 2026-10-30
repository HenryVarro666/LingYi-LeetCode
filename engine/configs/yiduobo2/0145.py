# ---- yiduobo 的写法会改树：leftest.left 指向 now.left，一个节点会有两个“父亲”。tree 视图的自动布局会乱，
# ---- 所以用 custom 视图：节点位置按原树固定；原来的边画灰色实线，新连的边画成节点下方的粉色弧线。
VALS = [1, 2, 3, 4, 5, 6]
REF = Tr(VALS)
PTRS = [('now', 'blue'), ('leftest', 'pink')]


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
        n = st.pop()
        if n is None or n.val in out:
            continue
        out[n.val] = n
        st += [n.left, n.right]
    return out


def draw_tree(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '二叉树（灰 = 原来的边，粉色弧线 = 新连的 left，绿 = 已记录）', 24, T['muted'], bold=True)
    nodes = _nodes(S)
    bnodes = _nodes(B)
    n_cols = len(POS)
    sp = min(140, (x1 - x0 - 80) / n_cols)
    dy, rad = 95, 28
    sx = x0 + 40 + ((x1 - x0 - 80) - sp * n_cols) / 2 + sp / 2

    def P(v):
        i, d = POS[v]
        return sx + i * sp, y0 + 80 + d * dy

    done = set(S.get('res') or [])
    for v, (lv, rv) in KIDS.items():
        for cv_ in (lv, rv):
            if cv_ is not None:
                cv.line([P(v), P(cv_)], T['border'], 4)
    for v, n in nodes.items():
        ch = n.left
        if ch is None or ch.val == KIDS[v][0]:
            continue
        bn = bnodes.get(v)
        new = bn is None or bn.left is None or bn.left.val != ch.val
        (X, Y), (X2, Y2) = P(v), P(ch.val)
        c = T['yellow'] if new else T['pink']
        lift = -(40 + abs(X2 - X) * 0.18) - (Y - Y2 if Y > Y2 else 0) * 0
        mid = cv.arc_arrow((X - rad * 0.3, Y + rad), (X2 + rad * 0.3, Y2 + rad + 3), lift - max(0, Y - Y2), c, 3, 13)
        cv.text((mid[0], mid[1] + 6), f'{v}.left', 19, c, anchor='mt', bold=True)
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
        cv.text((X, Y), str(v), 26, T['bg'] if v in done else T['text'], anchor='mm', bold=True)
        for r, (name, c) in enumerate(hs):
            cv.text((X + rad + 6, Y - rad - 2 - r * 24), name, 21, c, anchor='lb', bold=True)
    for name, c in PTRS:
        if name in S and S[name] is None:
            cv.text((x1 - 20, y0 + 40), f'{name} = None', 22, T[c], anchor='ra', mono=True)


def _res_text(S):
    if 'res' not in S:
        return ''
    return '`res` 是==根-右-左==的顺序，最后反过来就是==后序==（左-右-根）'


def _cap_if(S, B, ret):
    n = S.now
    if n.right:
        return f'`{n.val}` 有右孩子 `{n.right.val}` → 先找右子树中==最左侧的节点==（根-右-左里它最后才被访问）'
    if n.left:
        return f'`{n.val}` 没有右孩子 → 直接去左边 `{n.left.val}`'
    return f'`{n.val}` 没有右孩子，也没有左孩子 → `now` 将变成 None'


def _cap_wl(S, B, ret):
    l = B.leftest
    if l.left:
        return f'`{l.val}` 还有左孩子 → 继续往左'
    return f'`{l.val}` 没有左孩子 → 它就是 `leftest`'


def _cap_else(S, B, ret):
    if S.now is None:
        return f'`{B.now.val}` 的左边也是空的 → `now = None`'
    if KIDS[B.now.val][0] != S.now.val:
        return f'顺着新连的边走到 `{S.now.val}`：==左子树被“接”到了这里=='
    return f'去左孩子：`now = {S.now.val}`'


CONFIG = dict(
    num=145, title='二叉树的后序遍历', difficulty='Easy', category='二叉树',
    author='yiduobo', technique='根-右-左遍历 + 结果反转 · 不用栈',
    tags=['热题173'],
    code='''
class Solution(object):
    def postorderTraversal(self, root):
        if not root:
            return []

        res = []

        now = root
        while now:
            res.append(now.val)
            if now.right:
                leftest = now.right
                while leftest.left:
                    leftest = leftest.left
                leftest.left = now.left
                now = now.right
            else:
                now = now.left

        res.reverse()
        return res
''',
    call='Solution().postorderTraversal(Tr([1, 2, 3, 4, 5, 6]))',
    expect=[4, 5, 2, 6, 3, 1],
    views=[
        dict(type='custom', draw=draw_tree, h=420),
        dict(type='array', var='res', label='res（根-右-左 的访问顺序）', cell=72, h=150),
        dict(type='text', fn=_res_text, size=24),
    ],
    watch=[('now', 'now', 'blue'), ('leftest', 'leftest', 'pink'), ('res', 'res', 'green')],
    captions={
        'if not root': '`root` 不为空 → 继续（空树直接返回 `[]`）',
        'res = []': '`res` 收集==根-右-左==的遍历结果',
        'now = root': '`now` 从根开始；==不用递归，也不用栈==',
        'while now:': lambda S, B, ret: f'`now = {B.now.val}` 不为空 → 继续' if B.now else '`now` 为空 → 遍历结束',
        'res.append': lambda S, B, ret: f'先访问根：记录 `{S.now.val}` → `res = {S.res}`',
        'if now.right': _cap_if,
        'leftest = now.right': lambda S, B, ret: f'从右孩子 `{S.leftest.val}` 出发往左找',
        'while leftest.left': _cap_wl,
        'leftest = leftest.left': lambda S, B, ret: f'往左走：`leftest = {S.leftest.val}`',
        'leftest.left = now.left': lambda S, B, ret: (
            f'把 `{S.now.val}` 的左子树 `{S.now.left.val}` 接到 `{S.leftest.val}.left`：'
            f'==走完右子树后，自然接着走左子树==' if S.now.left else
            f'`{S.now.val}` 没有左子树：`{S.leftest.val}.left = None`'),
        'now = now.right': lambda S, B, ret: f'去右子树：`now = {S.now.val}`',
        'now = now.left': _cap_else,
        'res.reverse()': lambda S, B, ret: f'根-右-左 `{B.res}` ==反过来== → 左-右-根 `{S.res}`',
        'return res': lambda S, B, ret: f'返回后序遍历 `{ret}`（注意：原树结构已被修改）',
    },
    cards=dict(
        one_liner='后序 = 根-右-左 反过来；把左子树接到右子树最左节点下',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计）',
        problem=['给你一棵二叉树的根节点 `root`，返回其节点值的==后序==遍历（左-右-根）',
                 '示例：`[1,null,2,3]` → `[3,2,1]`',
                 '本视频：`[1,2,3,4,5,6]` → `[4,5,2,6,3,1]`'],
        quote='反过来看这个后序遍历，就会发现实际上后序遍历就是==将根-右-左这种遍历方式得到的结果反过来==。',
        quote_src='—— yiduobo 题解',
        idea=['先做根-右-左：每次找到右子树的==最左侧节点==',
              '把它的 `left` 指向当前节点的左子树：走完右边自然走到左边',
              '最后 `res.reverse()` 得到左-右-根'],
        result='运行结束：返回 `[4,5,2,6,3,1]` ✓',
        summary=['时间 `O(n)`（每个节点找最左节点的路径总长有限），空间 `O(1)`',
                 '和 94 题同一套路：改指针代替栈；但这里是“接左子树”而不是“连回根”',
                 '会==修改原树==（多出 left 指针），面试时要说明',
                 '直接找“左右子树的首尾节点”太复杂，所以换成根-右-左再反转',
                 '原文为 Python 2 风格，仅删去 docstring 和定义注释'],
    ),
)
