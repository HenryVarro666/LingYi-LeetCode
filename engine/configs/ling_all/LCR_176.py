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
        if record and S.get('node') is not None:
            DONE[S.node._uid] = ret
        for n in _walk(S.get('root_')):
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
    root = S.get('root_')
    if root is None:
        return
    pos, rad, order = _layout(root, (box[0], box[1] - TREE_H, box[2], box[1]))
    for n in order:
        d = getattr(n, '_d', None)
        if d is None:
            continue
        X, Y = pos[n._uid]
        s = '不平衡 -1' if d == -1 else f'高度 {d}'
        w = cv.tlen(s, 19, bold=True) + 16
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=(T['red'] if d == -1 else T['green']), width=2, r=8)
        cv.text((X, Y + rad + 18), s, 19, (T['red'] if d == -1 else T['green']), anchor='mm', bold=True)


def nv(x):
    return '空' if x is None else str(x.val)


def cap_if(S, B, ret):
    if S.node is None:
        return '`node` 是空节点 → 高度为 0，==递归边界=='
    return f'节点 `{S.node.val}`：先求左子树高度'


def cap_ret(S, B, ret):
    if ret == -1:
        return f'节点 `{S.node.val}`：左右高度差 `|{S.left_h} - {S.right_h}| = {abs(S.left_h - S.right_h)} > 1` → ==不平衡，返回 -1 一路向上报告=='
    return f'节点 `{S.node.val}`：高度差 `|{S.left_h} - {S.right_h}| <= 1` 平衡，高度 `max({S.left_h}, {S.right_h}) + 1 = {ret}`'


def cap_left_exit(S, B, ret):
    if S.left_h == -1:
        return f'左子树已不平衡（`left_h = -1`）→ ==提前退出，不再递归右子树==，直接返回 -1'
    return f'左子树平衡，高度 `left_h = {S.left_h}`，继续检查右子树'


def cap_right(S, B, ret):
    return f'再递归右子树 `get_height({nv(S.node)})`'


def cap_right_check(S, B, ret):
    if S.right_h == -1:
        return '右子树不平衡（`right_h = -1`）→ 返回 -1'
    d = abs(S.left_h - S.right_h)
    if d > 1:
        return f'`|{S.left_h} - {S.right_h}| = {d} > 1` → ==左右高度差超过 1，不平衡，返回 -1=='
    return f'`|{S.left_h} - {S.right_h}| = {d} <= 1` → 这个节点平衡'


CONFIG = dict(
    num='LCR 176', title='判断是否为平衡二叉树', difficulty='Easy', category='二叉树与回溯',
    author='灵茶山艾府', technique='递归 · 求高度 + 提前退出', tags=[],
    code='''
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def get_height(node: Optional[TreeNode]) -> int:
            if node is None: return 0
            left_h = get_height(node.left)
            if left_h == -1: return -1  # 提前退出，不再递归
            right_h = get_height(node.right)
            if right_h == -1 or abs(left_h - right_h) > 1: return -1
            return max(left_h, right_h) + 1
        return get_height(root) != -1
''',
    call='''root = Tr([1,2,2,3,None,None,None,4])
root_ = root
Solution().isBalanced(root)''',
    expect=False,
    views=[
        dict(type='tree', label='二叉树（绿 = 已返回高度，红 = 发现不平衡）', pointers={'node': 'blue'}, h=TREE_H,
             color=lambda S, n: ('red' if getattr(n, '_d', None) == -1 else 'green') if getattr(n, '_d', None) is not None else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='calls', h=230),
    ],
    watch=[('node', lambda S: S['_inner'].get('node'), 'blue'), ('left_h', lambda S: S['_inner'].get('left_h')), ('right_h', lambda S: S['_inner'].get('right_h'))],
    captions={
        'if node is None': track(cap_if),
        'left_h = get_height': track(lambda S, B, r: f'递归左子树 `get_height({nv(S.node)})`：==相信它返回左子树高度（或 -1 表示不平衡）=='),
        'if left_h == -1': track(cap_left_exit),
        'right_h = get_height': track(cap_right),
        'if right_h == -1': track(cap_right_check),
        'return max': track(cap_ret, record=True),
        'return get_height(root) != -1': track(lambda S, B, r: '调用 `get_height(root)`：返回 -1 表示不平衡，否则是树高' ),
    },
    cards=dict(
        one_liner='求高度时顺便判断：不平衡就返回 -1，一路传到根',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['任意节点的左右子树深度相差不超过 1，就是平衡二叉树',
                 '判断给定的二叉树是否平衡',
                 '题目示例：`[3,9,20,null,null,15,7]` → `true`；`[1,2,2,3,3,null,null,4,4]` → `false`',
                 '本视频用 `[1,2,2,3,null,null,null,4]`（左边一条链）→ `false`'],
        quote='`if left_h == -1: return -1  # 提前退出，不再递归`。看完这两期视频，让你对递归的理解更上一层楼！',
        quote_src='—— 灵茶山艾府题解',
        idea=['`get_height` 返回子树高度；一旦发现不平衡，返回特殊值 `-1`',
              '左子树已是 -1 → 提前退出，右子树不用再看',
              '左右高度差 `> 1` 或右子树是 -1 → 返回 -1，否则返回 `max + 1`'],
        result='运行结束，`get_height(root) = -1`，返回 `False`：左子树高 2、右子树高 0',
        summary=['时间 `O(n)`：每个节点至多递归一次，有提前退出更快；空间 `O(n)`',
                 '不要在每个节点都重新求高度，那样是 `O(n^2)`',
                 '易错：-1 要先于高度差判断，不能把 -1 当作正常高度参与 `abs`',
                 '同主站 110 题'],
    ),
)
