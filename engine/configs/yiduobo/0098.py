# ---- 每个节点返回 (最小值, 最大值) 后，在它下方标出 [min, max]；返回 (None, None) 标“非法”
TREE_H = 380
INFO = {}      # uid -> (文字, 状态)，元组不可变，每一步拍下的是当时的状态


def _walk(root):
    out, st, seen = [], [root], set()
    while st:
        n = st.pop()
        if n is None or n._uid in seen:
            continue
        seen.add(n._uid)
        out.append(n)
        st += [n.left, n.right]
    return out


def track(fn, key=None):
    def cap(S, B, ret):
        r = S.get(key) if key else None
        if r is not None and isinstance(ret, tuple):
            INFO[r._uid] = (f'[{ret[0]}, {ret[1]}]', 'ok') if ret[0] is not None else ('非法', 'bad')
        for n in _walk(S.get('self.tree')):
            n._d = INFO.get(n._uid)
        return fn(S, B, ret) if callable(fn) else fn
    return cap


def _layout(root, box):  # 与 views.v_tree 相同的布局
    x0, y0, x1, y1 = box
    order, depth = [], {}

    def ino(n, d):
        if n is None or n._uid in depth:
            return
        depth[n._uid] = d
        ino(n.left, d + 1)
        order.append(n)
        ino(n.right, d + 1)
    ino(root, 0)
    maxd = max(depth.values()) + 1
    sp = min(78, (x1 - x0 - 60) / max(1, len(order)))
    dy = min(95, (y1 - y0 - 80) / max(1, maxd))
    rad = max(14, min(26, sp * 0.4, dy * 0.32))
    sx = x0 + 30 + ((x1 - x0 - 60) - sp * len(order)) / 2 + sp / 2
    pos = {n._uid: (sx + i * sp, y0 + 60 + depth[n._uid] * dy + rad) for i, n in enumerate(order)}
    return pos, rad, order


def badges(cv, S, B, box, T):
    root = S.get('self.tree')
    if root is None:
        return
    pos, rad, order = _layout(root, (box[0], box[1] - TREE_H, box[2], box[1]))
    for n in order:
        d = getattr(n, '_d', None)
        if not d:
            continue
        X, Y = pos[n._uid]
        c = {'ok': T['green'], 'bad': T['red']}[d[1]]
        w = cv.tlen(d[0], 17, bold=True, mono=True) + 12
        cv.rect((X - w / 2, Y + rad + 4, X + w / 2, Y + rad + 27), fill=T['panel'], outline=c, width=2, r=8)
        cv.text((X, Y + rad + 15), d[0], 17, c, anchor='mm', bold=True, mono=True)


def tree_color(S, n):
    d = getattr(n, '_d', None)
    return {'ok': 'green', 'bad': 'red'}.get(d[1]) if d else None


def nv(x):
    return '空' if x is None else str(x.val)


def cap_minmax(S, B, ret):
    return f'先把 `min_val = max_val = {S.root.val}`：只有自己时最小最大都是它'


def cap_lif(S, B, ret):
    if S.root.left:
        return f'`{S.root.val}` 有左子树 → 递归求左子树的最小、最大值'
    return f'`{S.root.val}` 没有左子树'


def cap_rif(S, B, ret):
    if S.root.right:
        return f'`{S.root.val}` 有右子树 → 递归求右子树的最小、最大值'
    return f'`{S.root.val}` 没有右子树'


def cap_lchk(S, B, ret):
    if S.max_left is None:
        return '左子树不合法（返回了 `None`）'
    if S.max_left >= S.root.val:
        return f'左子树最大值 `{S.max_left} >= {S.root.val}` → ==左边有数不比根小=='
    return f'左子树合法，且最大值 `{S.max_left} < {S.root.val}` ✓'


def cap_rchk(S, B, ret):
    if S.min_right is None:
        return '右子树不合法（返回了 `None`）'
    if S.min_right <= S.root.val:
        return f'右子树最小值 `{S.min_right} <= {S.root.val}` → ==右边有数不比根大=='
    return f'右子树合法，且最小值 `{S.min_right} > {S.root.val}` ✓'


CONFIG = dict(
    num=98, title='验证二叉搜索树', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='后序遍历 · 返回子树最小 / 最大值',
    code='''
class Solution(object):
    def isValidBST(self, root):
        if not root:
            return True

        min_tree, max_tree = self.dfs(root)
        return min_tree is not None

    def dfs(self, root):
        min_val = max_val = root.val

        if root.left:
            min_left, max_left = self.dfs(root.left)
            if max_left is None or max_left >= root.val:
                return None, None
            min_val = min(min_val, min_left)

        if root.right:
            min_right, max_right = self.dfs(root.right)
            if min_right is None or min_right <= root.val:
                return None, None
            max_val = max(max_val, max_right)

        return min_val, max_val
''',
    call='''s = Solution()
s.tree = Tr([5,4,6,None,None,3,7])
s.isValidBST(s.tree)''',
    expect=False,
    views=[
        dict(type='tree', label='二叉树（下方 = dfs 返回的 [最小值, 最大值]）', pointers={'root': 'blue'},
             h=TREE_H, color=tree_color),
        dict(type='custom', draw=badges, h=0),
        dict(type='calls', h=210),
    ],
    watch=[('root', 'root', 'blue'),
           ('min_val', lambda S: S['_inner'].get('min_val')), ('max_val', lambda S: S['_inner'].get('max_val'))],
    captions={
        'if not root': track('根不为空'),
        'min_tree, max_tree = self.dfs': track('对整棵树做 `dfs`，拿到它的最小值和最大值'),
        'return min_tree is not None': track(lambda S, B, ret: f'`min_tree = {S.min_tree}` → 返回 `{ret}`'),
        'min_val = max_val = root.val': track(cap_minmax),
        'if root.left': track(cap_lif),
        'min_left, max_left = self.dfs': track(lambda S, B, ret: f'进入 `dfs({S.root.val})` 求左子树的 `(min, max)`'),
        'if max_left is None': track(cap_lchk),
        'min_val = min(': track(lambda S, B, ret: f'用左子树最小值更新：`min_val = min({B.min_val}, {S.min_left}) = {S.min_val}`'),
        'if root.right': track(cap_rif),
        'min_right, max_right = self.dfs': track(lambda S, B, ret: f'进入 `dfs({S.root.val})` 求右子树的 `(min, max)`'),
        'if min_right is None': track(cap_rchk),
        'max_val = max(': track(lambda S, B, ret: f'用右子树最大值更新：`max_val = max({B.max_val}, {S.max_right}) = {S.max_val}`'),
        'return None, None': track(lambda S, B, ret: f'以 `{S.root.val}` 为根的树==不合法== → 返回 `(None, None)`', key='root'),
        'return min_val, max_val': track(lambda S, B, ret: f'`{S.root.val}` 这棵子树合法，返回 `({ret[0]}, {ret[1]})` 给上一层', key='root'),
    },
    cards=dict(
        one_liner='左右子树先算出最小、最大值，再和根比较',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['判断二叉树是否是==有效的二叉搜索树==',
                 '左子树==所有==节点 < 根 < 右子树==所有==节点，且子树也是 BST',
                 '本视频：`[5,4,6,null,null,3,7]` → `false`'],
        quote='分别验证左右子树是否合法，同时在验证的过程中统计出左子树与右子树中==最大和最小值==是多少，然后再判断当前树是否合法，并更新当前树的最大和最小值。',
        quote_src='—— yiduobo 题解',
        idea=['`dfs` 返回子树 `(最小值, 最大值)`，不合法返回 `(None, None)`',
              '根要大于==左子树最大值==、小于==右子树最小值==',
              '自底向上：先拿到孩子的结果，再判断自己（后序遍历）'],
        result='运行结束，返回 `False`：右子树的最小值是 `3`，不大于根 `5`',
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '约定：子树不合法时返回 `(None, None)`，上层一看到 `None` 就继续往上报',
                 '易错：只比较父子是不够的，要比较整棵子树的最值',
                 '原文为 Python 2 风格，仅删去 docstring 和定义注释，其余照搬'],
    ),
)
