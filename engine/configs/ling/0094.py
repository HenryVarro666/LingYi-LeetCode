# ---- Morris 遍历会给树加“线索”（pre.right 指回祖先），tree 视图的自动布局处理不了环，
# ---- 所以用 custom 视图：节点位置按原树固定，边按当前真实指针画，非原树的边画成粉色弧线箭头。
VALS = [4, 2, 5, 1, 3]
REF = Tr(VALS)            # 只用来算固定布局和“原来的儿子是谁”
PTRS = [('root', 'blue'), ('pre', 'pink')]
OUT = 'ans'
THREAD = '线索'


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
    cv.text((x0 + 18, y0 + 4), f'二叉树（粉色箭头 = {THREAD}，虚线 = 被断开的原边，绿 = 已输出）', 24, T['muted'], bold=True)
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
    if B.root is not None:
        return f'`root = {B.root.val}` 不为空 → 继续'
    return '`root` 为空 → 遍历结束'


def cap_if_left(S, B, ret):
    if S.root.left:
        return f'`{S.root.val}` 有左子树 → 先找它的前驱 `pre`（中序遍历中 root 的上一个节点）'
    return f'`{S.root.val}` 没有左子树 → 直接记录它'


def cap_wpre(S, B, ret):
    p = S.pre
    if p.right is None:
        return f'`{p.val}.right` 为空 → 走到尽头，前驱就是 `{p.val}`'
    if p.right is S.root:
        return f'`{p.val}.right` 指向 root → 遇到了==之前建的线索=='
    return f'`{p.val}` 还有右儿子 → 继续向右走'


def cap_if_none(S, B, ret):
    if S.pre.right is None:
        return '`pre.right` 为空 → root 的左子树==尚未访问=='
    return '`pre.right` 是线索 → root 的左子树==已经访问完毕=='


def cap_back(S, B, ret):
    if S.root is None:
        return f'`{B.root.val}` 没有右子树也没有线索 → `root = None`'
    if KIDS[B.root.val][1] != S.root.val:
        return f'没有右子树，==顺着线索==回到 `{S.root.val}`'
    return f'进入右子树：`root = {S.root.val}`'


CONFIG = dict(
    num=94, title='二叉树的中序遍历', difficulty='Easy', category='二叉树',
    author='灵茶山艾府', technique='Morris 遍历（线索二叉树）',
    code='''
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        ans = []

        while root:
            if root.left:
                # 找 root 的前驱 pre：在中序遍历中，root 的上一个节点
                # 从 root.left 开始，一直向右走，直到走到尽头，或者遇到指向 root 的线索（回到 root 的路）
                pre = root.left
                while pre.right and pre.right is not root:
                    pre = pre.right

                # root 的左子树尚未访问
                if pre.right is None:
                    pre.right = root  # 建立线索（回到 root 的路），相当于把 pre.right 当作栈
                    root = root.left  # 访问左子树
                    continue

                # root 的左子树访问完毕，去掉线索，恢复原样
                pre.right = None  # 注：如果调用完 inorderTraversal 不再使用这棵二叉树，这行代码可以去掉

            # root 的左子树访问完毕
            ans.append(root.val)  # 记录当前节点的值
            root = root.right  # 如果有右子树就访问右子树，没有就顺着线索回到指向的节点

        return ans
''',
    # s.nodes 只是让可视化能拿到全部节点（Morris 过程中有的节点暂时没有变量指着）
    call='''s = Solution()
t = Tr([4, 2, 5, 1, 3])
s.nodes = [t, t.left, t.right, t.left.left, t.left.right]
s.inorderTraversal(t)''',
    expect=[1, 2, 3, 4, 5],
    views=[
        dict(type='custom', draw=draw_morris, h=420),
        dict(type='array', var='ans', label='ans（中序结果）', cell=72),
    ],
    watch=[('root', 'root', 'blue'), ('pre', 'pre', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = []': '`ans` 收集中序遍历结果；==全程不用递归、不用栈==',
        'while root:': cap_while,
        'if root.left:': cap_if_left,
        'pre = root.left': lambda S, B, ret: f'从 `root.left = {S.pre.val}` 开始找前驱',
        'while pre.right and': cap_wpre,
        'pre = pre.right': lambda S, B, ret: f'一直向右走：`pre = {S.pre.val}`',
        'if pre.right is None': cap_if_none,
        'pre.right = root': lambda S, B, ret: (f'建立线索 `{S.pre.val}.right → {S.root.val}`：'
                                               f'==走完左子树就能顺着它回到 {S.root.val}==（相当于把 pre.right 当作栈）'),
        'root = root.left': lambda S, B, ret: f'访问左子树：`root = {S.root.val}`',
        'continue': '`continue`：回到循环开头处理新的 `root`',
        'pre.right = None': lambda S, B, ret: f'去掉线索 `{S.pre.val}.right`，恢复原样',
        'ans.append': lambda S, B, ret: (f'左子树访问完毕，记录当前节点 `{S.root.val}` → `ans = {S.ans}`' if S.root.left
                                         else f'没有左子树，记录当前节点 `{S.root.val}` → `ans = {S.ans}`'),
        'root = root.right': cap_back,
        'return ans': lambda S, B, ret: f'返回 `{ret}`，树也已经恢复原样',
    },
    cards=dict(
        one_liner='用前驱的空右指针当“回去的路”，O(1) 空间完成中序遍历',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计）',
        problem=['给定二叉树的根节点 `root`，返回它的==中序==遍历（左-根-右）',
                 '示例：`[1,null,2,3]` → `[1,3,2]`',
                 '本视频：`[4,2,5,1,3]` → `[1,2,3,4,5]`'],
        before=[dict(heading='先看递归写法', lines=[
            '递归：`dfs(左)` → 记录 `node.val` → `dfs(右)`',
            '递归需要 `O(h)` 的栈空间。能不能做到 `O(1)` ==空间==？',
            '不能写递归，也不能用栈模拟递归 → Morris 遍历'])],
        quote='从 root.left 开始，一直向右走，直到走到尽头，或者遇到指向 root 的线索。建立线索（回到 root 的路），==相当于把 pre.right 当作栈==。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['root 的前驱 `pre` = 左子树里最右边的节点，它的 `right` 一定是空的',
              '第一次到 root：让 `pre.right` 指向 root（建线索），然后去左子树',
              '第二次到 root（发现线索）：左子树已走完，拆掉线索，记录 root，去右子树'],
        result='运行结束，返回 `[1,2,3,4,5]`，所有线索都已拆除，树恢复原样',
        summary=['时间 `O(n)`：每条边至多访问三次；空间 `O(1)`',
                 '易错：找前驱时要判断 `pre.right is not root`，否则会顺着线索死循环',
                 '`pre.right = None` 负责恢复原树；如果之后不再用这棵树，可以去掉',
                 '练习（灵神推荐）：用 Morris 实现 144 前序、145 后序遍历'],
    ),
)
