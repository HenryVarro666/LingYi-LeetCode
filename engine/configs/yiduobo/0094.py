# ---- yiduobo 的写法会改树：rightest.right 指回 now、断开 now.left。tree 视图的自动布局会让节点乱跳/消失，
# ---- 所以用 custom 视图：节点位置按原树固定，边按当前真实指针画；新连的边画粉色弧线，被断开的原边画虚线。
VALS = [4, 2, 5, 1, 3]
REF = Tr(VALS)            # 只用来算固定布局和“原来的儿子是谁”
PTRS = [('now', 'blue'), ('rightest', 'pink')]
OUT = 'res'
THREAD = '新连的边'


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


def nv(x):
    return '空' if x is None else str(x.val)


def draw_morris(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), f'二叉树（粉色箭头 = {THREAD}，虚线 = 被断开的原边，绿 = 已记录）', 24, T['muted'], bold=True)
    nodes = {n.val: n for n in S.get('self.nodes', [])}
    n_cols = len(POS)
    sp = min(150, (x1 - x0 - 80) / n_cols)
    dy, rad = 105, 28
    sx = x0 + 40 + ((x1 - x0 - 80) - sp * n_cols) / 2 + sp / 2

    def P(v):
        i, d = POS[v]
        return sx + i * sp, y0 + 90 + d * dy

    done = set(S.get(OUT) or [])
    # 原树的边：还在就画实线，断开了画虚线
    for v, (lv, rv) in KIDS.items():
        n = nodes.get(v)
        for side, cv_ in (('left', lv), ('right', rv)):
            if cv_ is None:
                continue
            ch = getattr(n, side) if n is not None else None
            (X, Y), (X2, Y2) = P(v), P(cv_)
            if ch is not None and ch.val == cv_:
                cv.line([(X, Y), (X2, Y2)], T['border'], 4)
            else:
                cv.dashed((X, Y), (X2, Y2), T['dim'], 2, 8, 8)
    # 不在原树里的边（线索）
    for v, n in nodes.items():
        for side, idx in (('left', 0), ('right', 1)):
            ch = getattr(n, side)
            if ch is None or ch.val == KIDS[v][idx]:
                continue
            (X, Y), (X2, Y2) = P(v), P(ch.val)
            p0, p1 = (X + rad * 0.95, Y), (X2, Y2 + rad + 2)
            mid = cv.arc_arrow(p0, p1, (Y2 + rad) - Y, T['pink'], 3, 13)
            cv.text((mid[0] + 8, mid[1] + 4), THREAD, 19, T['pink'], anchor='lt', bold=True)
    hits = {}
    for k, (name, c) in enumerate(PTRS):
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


def cap_while(S, B, ret):
    if B.now is not None:
        return f'`now = {B.now.val}` 不为空 → 继续'
    return '`now` 为空 → 遍历结束'


def cap_if(S, B, ret):
    if S.now.left is None:
        if KIDS[S.now.val][0] is not None:
            return f'`{S.now.val}` 的左孩子==已经被断开==（左子树走完了）→ 记下它，去右边'
        return f'`{S.now.val}` 的左孩子为空 → 记下它的值，然后去右子树'
    return f'`{S.now.val}` 有左孩子 → 先找左子树中==最右侧的节点== `rightest`'


def cap_wr(S, B, ret):
    r = S.rightest
    if r.right is None:
        return f'`{r.val}` 没有右孩子 → 它就是 `rightest`：==左子树中最后被遍历到的节点=='
    return f'`{r.val}` 还有右孩子 → 继续往右'


def cap_next(S, B, ret):
    if S.now is None:
        return f'`{B.now.val}` 没有右边的路了 → `now = None`'
    if KIDS[B.now.val][1] != S.now.val:
        return f'顺着之前连的边，==自然回到== `{S.now.val}`'
    return f'进入右子树：`now = {S.now.val}`'


CONFIG = dict(
    num=94, title='二叉树的中序遍历', difficulty='Easy', category='二叉树',
    author='yiduobo', technique='非递归 · 最右节点连回当前节点',
    code='''
class Solution(object):
    def inorderTraversal(self, root):
        res = []
        now = root
        while now:
            if now.left is None:
                res.append(now.val)
                now = now.right
            else:
                rightest = now.left
                while rightest.right:
                    rightest = rightest.right
                rightest.right = now
                now = now.left
                rightest.right.left = None

        return res
''',
    # s.nodes 只是让可视化能拿到全部节点（这种写法会断开左孩子，已记录的节点会变得没有变量能指到）
    call='''s = Solution()
t = Tr([4, 2, 5, 1, 3])
s.nodes = [t, t.left, t.right, t.left.left, t.left.right]
s.inorderTraversal(t)''',
    expect=[1, 2, 3, 4, 5],
    views=[
        dict(type='custom', draw=draw_morris, h=420),
        dict(type='array', var='res', label='res（中序结果）', cell=72),
    ],
    watch=[('now', 'now', 'blue'), ('rightest', 'rightest', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = []': '`res` 收集中序遍历结果（左-根-右）',
        'now = root': '`now` 从根开始；==不用递归，也不用栈==',
        'while now:': cap_while,
        'if now.left is None': cap_if,
        'res.append': lambda S, B, ret: f'记录 `{S.now.val}` → `res = {S.res}`',
        'now = now.right': cap_next,
        'rightest = now.left': lambda S, B, ret: f'从左孩子 `{S.rightest.val}` 出发找最右节点',
        'while rightest.right': cap_wr,
        'rightest = rightest.right': lambda S, B, ret: f'往右走：`rightest = {S.rightest.val}`',
        'rightest.right = now': lambda S, B, ret: (f'让 `{S.rightest.val}.right` 指向 `{S.now.val}`：'
                                                   f'==遍历完左子树后，自然会从 {S.rightest.val} 回到 {S.now.val}=='),
        'now = now.left': lambda S, B, ret: f'开始遍历左子树：`now = {S.now.val}`',
        'rightest.right.left = None': lambda S, B, ret: (f'断开 `{S.rightest.right.val}` 与左子树的连接：'
                                                         f'==否则回到它时又会再进左子树，死循环=='),
        'return res': lambda S, B, ret: f'返回 `{ret}`（注意：原树的结构已经被改掉了）',
    },
    cards=dict(
        one_liner='把左子树的最右节点连回当前节点，遍历完左边就能自然回来',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计）',
        problem=['给定二叉树的根节点 `root`，返回它的==中序==遍历（左-根-右）',
                 '示例：`[1,null,2,3]` → `[1,3,2]`',
                 '本视频：`[4,2,5,1,3]` → `[1,2,3,4,5]`'],
        quote='问题就变成了==如何在不回溯的情况下遍历完当前节点左子树之后返回到当前节点==。',
        quote_src='—— yiduobo 题解',
        idea=['左子树中最右侧的节点 `rightest` 一定最后被遍历到，且没有右孩子',
              '让 `rightest.right = now`：走完左子树就自然回到 `now`',
              '为了避免死循环，要==断开 now 与左子树的连接=='],
        result='运行结束，返回 `[1,2,3,4,5]`；原树被改成了一条只往右走的链',
        summary=['时间 `O(n)`：每个节点找一次最右节点；空间 `O(1)`',
                 '和标准 Morris 的区别：不拆“回去的边”，而是直接断开左孩子 → ==会破坏原树==',
                 '易错：漏掉 `rightest.right.left = None` 会死循环',
                 '原文为 Python 2 风格，仅删去 docstring 和定义注释'],
    ),
)
