# ---- 树上“已返回”标注：caption 回调里记录每个节点的返回值，custom 叠加层（h=0）画在 tree 视图里的节点下方
TREE_H = 390
DONE = {}


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


def track(fn, record=False):
    def cap(S, B, ret):
        if record and S.root is not None:
            DONE[S.root._uid] = ret
        for n in _walk(S.get('self.tree')):
            n._d = DONE.get(n._uid)
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
        if d is None:
            continue
        X, Y = pos[n._uid]
        s = f'深度 {d}'
        w = cv.tlen(s, 19, bold=True) + 16
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 18), s, 19, T['green'], anchor='mm', bold=True)


def nv(x):
    return '空' if x is None else str(x.val)


def cap_if(S, B, ret):
    if S.root is None:
        return '`root` 是空节点 → 空树深度为 0，这是==递归边界=='
    return f'节点 `{S.root.val}` 不是空节点 → 它的深度取决于左右子树的深度'


def cap_l(S, B, ret):
    if S.root is None:
        return f'节点 `{B.root.val}` 没有左儿子 → `maxDepth(None)` 会直接碰到边界'
    return f'递归左子树 `maxDepth({S.root.val})`：==相信它一定返回左子树的深度==，不用钻进去想'


def cap_r(S, B, ret):
    return f'左子树深度 `l_depth = {B.l_depth}` 已拿到；再递归右子树 `maxDepth({nv(S.root)})`'


def cap_ret(S, B, ret):
    return (f'节点 `{S.root.val}`：`max({S.l_depth}, {S.r_depth}) + 1 = {ret}`，'
            f'==取较深的子树，再加上自己这一层==')


CONFIG = dict(
    num=104, title='二叉树的最大深度', difficulty='Easy', category='二叉树',
    author='灵茶山艾府', technique='递归 · 自底向上',
    code='''
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        l_depth = self.maxDepth(root.left)
        r_depth = self.maxDepth(root.right)
        return max(l_depth, r_depth) + 1
''',
    call='''s = Solution()
s.tree = Tr([3,9,20,None,None,15,7])
s.maxDepth(s.tree)''',
    expect=3,
    views=[
        dict(type='tree', label='二叉树（绿 = 已返回深度）', pointers={'root': 'blue'}, h=TREE_H,
             color=lambda S, n: 'green' if getattr(n, '_d', None) is not None else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='calls', h=230),
    ],
    watch=[('root', 'root', 'blue'), ('l_depth', lambda S: S['_inner'].get('l_depth')), ('r_depth', lambda S: S['_inner'].get('r_depth'))],  # 只显示当前这层的局部变量
    captions={
        'if root is None': track(cap_if),
        'return 0': track('空节点没有任何节点 → 返回 `0`，交给上一层去 `+1`'),
        'l_depth = self': track(cap_l),
        'r_depth = self': track(cap_r),
        'return max': track(cap_ret, record=True),
    },
    cards=dict(
        one_liner='子树的深度交给递归，自己只做 `max(左, 右) + 1`',
        complexity='时间 `O(n)`，空间 `O(n)`（最坏退化成链的递归栈）',
        problem=['给你二叉树的根 `root`，返回它的最大深度',
                 '最大深度 = 从根到最远叶子的路径上的 ==节点数==',
                 '示例：`root = [3,9,20,null,null,15,7]` → `3`'],
        quote='「在写递归函数时，可以假设递归返回的结果一定是正确的」。其实这种说法本质上就是==数学归纳法==。',
        quote_src='—— 灵茶山艾府题解「注」',
        idea=['==自底向上==：深度信息从儿子传给父亲',
              '边界：空节点深度是 `0`',
              '非空节点：左右子树深度取 `max`，再 `+1` 算上自己'],
        result='运行结束，返回 `3`：最长路径 `3 → 20 → 15`（或 `7`）共 3 个节点',
        summary=['时间 `O(n)`：每个节点恰好递归一次；空间 `O(n)`：最坏退化成链',
                 '易错：别忘了 `+1`；空节点返回 `0` 而不是 `-1`',
                 '方法二「自顶向下」：`dfs(node, depth)` 把深度往下传，沿途更新 `ans`',
                 '两种方法的区别在于==深度信息往哪个方向传==：子→父，还是父→子'],
    ),
)
