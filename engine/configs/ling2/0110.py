# ---- 树上“已返回”标注：caption 回调里记录每个节点的返回值，custom 叠加层（h=0）画在 tree 视图里的节点下方
TREE_H = 400
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


def track(fn, key=None):
    def cap(S, B, ret):
        if key and S.get(key) is not None:
            DONE[S[key]._uid] = ret
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
        s = '不平衡 -1' if d == -1 else f'高度 {d}'
        c = T['red'] if d == -1 else T['green']
        w = cv.tlen(s, 18, bold=True) + 14
        cv.rect((X - w / 2, Y + rad + 4, X + w / 2, Y + rad + 28), fill=T['panel'], outline=c, width=2, r=8)
        cv.text((X, Y + rad + 16), s, 18, c, anchor='mm', bold=True)


def _nc(S, n):
    d = getattr(n, '_d', None)
    if d is None:
        return None
    return 'red' if d == -1 else 'green'


def nv(x):
    return '空' if x is None else str(x.val)


def cap_if(S, B, ret):
    if S.node is None:
        return '空节点 → 递归边界'
    return f'节点 `{S.node.val}` 非空 → 先算左子树高度'


def cap_l(S, B, ret):
    return f'递归 `get_height({nv(S.node)})`：求 `{B.node.val}` 的==左子树==高度'


def cap_lchk(S, B, ret):
    if S.left_h == -1:
        return f'`left_h = -1`：左子树已经不平衡 → ==整棵树一定不平衡=='
    return f'左子树高度 `left_h = {S.left_h}`，不是 -1，继续算右子树'


def cap_r(S, B, ret):
    return f'递归 `get_height({nv(S.node)})`：求 `{B.node.val}` 的==右子树==高度'


def cap_rchk(S, B, ret):
    l, r = S.left_h, S.right_h
    if r == -1:
        return '`right_h = -1`：右子树不平衡 → 返回 -1'
    if abs(l - r) > 1:
        return f'`|{l} - {r}| = {abs(l - r)} > 1`：节点 `{S.node.val}` 的左右子树==高度差超过 1== → 不平衡'
    return f'`right_h = {r}`，`|{l} - {r}| = {abs(l - r)} ≤ 1` → 以 `{S.node.val}` 为根的子树平衡'


CONFIG = dict(
    num=110, title='平衡二叉树', difficulty='Easy', category='二叉树',
    author='灵茶山艾府', technique='后序递归求高度 · -1 表示不平衡',
    tags=['热题173'],
    code='''
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def get_height(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0
            left_h = get_height(node.left)
            if left_h == -1:
                return -1  # 提前退出，不再递归
            right_h = get_height(node.right)
            if right_h == -1 or abs(left_h - right_h) > 1:
                return -1
            return max(left_h, right_h) + 1
        return get_height(root) != -1
''',
    call='''s = Solution()
s.tree = Tr([1,2,3,4,None,None,None,5])
s.isBalanced(s.tree)''',
    expect=False,
    views=[
        dict(type='tree', label='二叉树（绿 = 已返回高度，红 = 返回 -1）', pointers={'node': 'blue'}, h=TREE_H, color=_nc),
        dict(type='custom', draw=badges, h=0),
        dict(type='calls', h=225),
    ],
    watch=[('node', 'node', 'blue'), ('left_h', lambda S: S['_inner'].get('left_h')),
           ('right_h', lambda S: S['_inner'].get('right_h'))],
    captions={
        'if node is None': track(cap_if),
        'return 0': track('空节点高度为 `0`'),
        'left_h = get_height': track(cap_l),
        'if left_h == -1': track(cap_lchk),
        'return -1  #': track('提前退出：==不再递归右子树==，直接把 `-1` 往上传', key='node'),
        'right_h = get_height': track(cap_r),
        'if right_h == -1': track(cap_rchk),
        11: track(lambda S, B, ret: f'节点 `{S.node.val}` 不平衡：返回 `-1`，这个 -1 会==一路向上返回==', key='node'),
        'return max(': track(lambda S, B, ret: f'平衡：高度 = `max({S.left_h}, {S.right_h}) + 1 = {ret}`', key='node'),
        'return get_height(root) != -1': track(lambda S, B, ret: ('从根节点开始递归：`get_height(root)` 不是 -1 就说明平衡' if ret is None
                                                                  else f'返回 `{ret}`')),
    },
    max_steps=60,
    cards=dict(
        result='`get_height(root) = -1` → 返回 `False`；右子树（节点 3）==根本没被访问==',
        one_liner='递归求高度，一旦发现不平衡就返回 -1，一路传到根',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['判断二叉树是不是==平衡二叉树==',
                 '平衡：==每个节点==的左右子树高度差都不超过 1',
                 '示例：`[3,9,20,null,null,15,7]` → `true`；`[1,2,2,3,3,null,null,4,4]` → `false`',
                 '本视频：`[1,2,3,4,null,null,null,5]` → `false`'],
        quote='问：代码中的 -1 是怎么产生的？怎么返回的？答：在某次递归中，发现左右子树高度绝对差大于 1，我们会返回 -1。这个 -1 会一路向上不断返回，直到根节点。',
        quote_src='—— 灵茶山艾府题解「答疑」',
        idea=['`get_height(node)`：平衡就返回高度，不平衡就返回 `-1`（高度不可能是负数）',
              '后序：先拿到左右子树的结果，再判断当前节点',
              '写法二：左子树已经是 -1 就==提前退出==，连右子树都不用递归'],
        summary=['时间 `O(n)`：每个节点最多访问一次；空间 `O(n)`（链状树的递归栈）',
                 '用 -1 同时表达“不平衡”和“高度”，一次递归搞定，不用每个节点重复求高度',
                 '易错：只比较根的左右高度不够，==每个节点==都要平衡',
                 '写法一：不提前退出，左右都递归完再统一判断，复杂度相同'],
    ),
)
