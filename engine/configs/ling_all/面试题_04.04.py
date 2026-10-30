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


def track(fn, record=False):
    def cap(S, B, ret):
        nd = S.get('node')
        if record and nd is not None and ret is not None:
            DONE[nd._uid] = ret
        for n in _walk(S.get('self.tree')):
            n._d = DONE.get(n._uid)
        return fn(S, B, ret) if callable(fn) else fn
    return cap


def _layout(root, box):
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
        s = '失衡' if d == -1 else f'高 {d}'
        c = T['red'] if d == -1 else T['green']
        w = cv.tlen(s, 19, bold=True) + 16
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=c, width=2, r=8)
        cv.text((X, Y + rad + 18), s, 19, c, anchor='mm', bold=True)


def nv(x):
    return '空' if x is None else str(x.val)


def cap_if(S, B, ret):
    if S.node is None:
        return '空节点：高度 `0`，==递归边界=='
    return f'节点 `{S.node.val}`：先去左子树拿高度'


def cap_lh(S, B, ret):
    return f'递归左子树 `{nv(S.node)}`：先拿到左边的高度'


def cap_lh1(S, B, ret):
    if S.left_h == -1:
        return f'`left_h == -1`：左子树已经不平衡 → ==提前退出==，右子树不用再看，直接往上返回 `-1`'
    return f'左子树高度 `left_h = {S.left_h}`，没有失衡 → 继续看右子树'


def cap_rh(S, B, ret):
    return f'递归右子树 `{nv(S.node)}`'


def cap_chk(S, B, ret):
    if S.right_h == -1:
        return f'右子树失衡（`right_h = -1`）→ 当前也失衡，返回 `-1`'
    d = abs(S.left_h - S.right_h)
    if d > 1:
        return f'`|{S.left_h} − {S.right_h}| = {d} > 1`：节点 `{S.node.val}` 的两棵子树==高度差超过 1== → 返回 `-1`'
    return f'`|{S.left_h} − {S.right_h}| = {d} ≤ 1`：节点 `{S.node.val}` 平衡'


def cap_ret(S, B, ret):
    return f'`max({S.left_h}, {S.right_h}) + 1 = {ret}`：节点 `{S.node.val}` 的高度，往上交给父节点'


CONFIG = dict(
    num='面试题 04.04', title='检查平衡性', difficulty='Easy', category='二叉树与回溯',
    author='灵茶山艾府', technique='递归求高度，失衡返回 -1', tags=[],
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
    call='''s = Solution()
s.tree = Tr([1,2,2,3,3,None,None,4,4])
s.isBalanced(s.tree)''',
    expect=False,
    views=[
        dict(type='tree', label='二叉树（绿 = 已算出高度，红 = 失衡）', pointers={'node': 'blue'}, h=TREE_H,
             color=lambda S, n: ('red' if getattr(n, '_d', None) == -1 else 'green') if getattr(n, '_d', None) is not None else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='calls', h=230, hide=('isBalanced',)),
    ],
    watch=[('node', lambda S: S['_inner'].get('node') and S['_inner']['node'].val, 'blue'),
           ('left_h', lambda S: S['_inner'].get('left_h')), ('right_h', lambda S: S['_inner'].get('right_h'))],
    captions={
        'if node is None': track(cap_if),
        'left_h = get_height': track(cap_lh),
        'if left_h == -1': track(cap_lh1, record=True),
        'right_h = get_height': track(cap_rh),
        'if right_h == -1': track(cap_chk, record=True),
        'return max': track(cap_ret, record=True),
        'return get_height(root) != -1': '从根节点开始求高度；最后看返回值是不是 `-1`：不是 `-1` 才是平衡树',
    },
    max_steps=80,
    cards=dict(
        one_liner='求高度的同时检查平衡，一旦失衡就用 `-1` 一路报告上去',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['判断二叉树是否平衡：==任意节点==的左右子树高度差不超过 1',
                 '示例 1：`[3,9,20,null,null,15,7]` → `true`',
                 '示例 2：`[1,2,2,3,3,null,null,4,4]` → `false`'],
        quote='提前退出，不再递归',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['`get_height` 返回子树高度；一旦发现失衡，改返回 ==-1==',
              '拿到 `-1` 的父节点不用再算，直接继续返回 `-1`',
              '这样每个节点只算一次，不会像「每个节点都重新求高度」那样重复'],
        result='根返回 `-1`：根的左子树高 3、右子树高 1，差 2 > 1 → `False`',
        summary=['时间 `O(n)`，空间 `O(n)`（最坏是一条链的递归栈）',
                 '易错：必须检查==每个==节点，不能只看根的左右高度差',
                 '`-1` 既当「失衡」标记又不会和合法高度（≥ 0）冲突',
                 '左子树失衡后右子树不递归，这就是提前退出'],
    ),
)
