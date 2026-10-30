# ---- 树上“已返回”标注：caption 回调里记录每个节点返回的 (高度, lca)，custom 叠加层（h=0）画在节点下方
TREE_H = 330
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
        if record and S.get('node') is not None and ret is not None:
            DONE[S.node._uid] = (ret[0], ret[1].val if ret[1] is not None else None)
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
        s = f'高 {d[0]}'
        w = cv.tlen(s, 19, bold=True) + 16
        c = T['yellow'] if d[1] == n.val else T['green']
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=c, width=2, r=8)
        cv.text((X, Y + rad + 18), s, 19, c, anchor='mm', bold=True)


def nv(x):
    return '空' if x is None else str(x.val)


def cap_none(S, B, ret):
    if S.node is None:
        return '`node` 是空节点 → 高度 `0`，没有叶子，`lca` 为 `None`：这是==递归边界=='
    return f'节点 `{S.node.val}` 非空 → 先问左右子树各自「最深叶子多深、lca 是谁」'


def cap_ret0(S, B, ret):
    return '空子树：返回 `(0, None)`，交给上一层去 `+1`'


def cap_l(S, B, ret):
    return f'递归左儿子 `dfs({nv(S.node.left) if ret is None and S.get("node") is not None and False else ""}`'


def cap_call_l(S, B, ret):
    return f'问左儿子 `{nv(B.node.left)}`：它的子树有多高、最深叶子的 lca 是谁？==相信递归会给出正确答案=='


def cap_call_r(S, B, ret):
    return (f'左边拿到了：高度 `{B.left_height}`；再问右儿子 `{nv(B.node.right)}`')


def cap_gt(S, B, ret):
    lh, rh = S.left_height, S.right_height
    if lh > rh:
        return f'`{lh} > {rh}`：==左子树更高==，最深叶子都在左边 → 答案只会在左子树里'
    return f'`{lh} > {rh}` 不成立 → 左子树不更高，再看右边'


def cap_lt(S, B, ret):
    lh, rh = S.left_height, S.right_height
    if lh < rh:
        return f'`{lh} < {rh}`：==右子树更高==，最深叶子都在右边 → 答案只会在右子树里'
    return f'`{lh} < {rh}` 不成立 → 两边一样高，最深叶子左右都有'


CONFIG = dict(
    num=1123, title='最深叶节点的最近公共祖先', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='递归 · 自底向上返回 (高度, lca)',
    tags=['灵神题单', '链表树与回溯', '难度分 1607'],
    code='''
class Solution:
    def lcaDeepestLeaves(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        def dfs(node: Optional[TreeNode]) -> Tuple[int, Optional[TreeNode]]:
            if node is None:
                return 0, None
            left_height, left_lca = dfs(node.left)
            right_height, right_lca = dfs(node.right)
            if left_height > right_height:  # 左子树更高
                return left_height + 1, left_lca
            if left_height < right_height:  # 右子树更高
                return right_height + 1, right_lca
            return left_height + 1, node  # 一样高
        return dfs(root)[1]
''',
    call='''s = Solution()
s.tree = Tr([3,5,1,6,2])
s.lcaDeepestLeaves(s.tree)''',
    result_fn=tree_list,
    expect=[5, 6, 2],
    views=[
        dict(type='tree', label='二叉树（蓝 = node，绿 = 已返回高度，黄 = 该子树的 lca 就是自己）', pointers={'node': 'blue'}, h=TREE_H,
             color=lambda S, n: ('yellow' if getattr(n, '_d', None) is not None and n._d[1] == n.val else 'green') if getattr(n, '_d', None) is not None else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='calls', h=250),
    ],
    watch=[('node', lambda S: S['_inner']['node'].val if S['_inner'].get('node') is not None else None, 'blue'),
           ('left_height', lambda S: S['_inner'].get('left_height'), 'pink'),
           ('right_height', lambda S: S['_inner'].get('right_height'), 'orange')],
    captions={
        'if node is None': track(cap_none),
        'return 0, None': track(cap_ret0, record=True),
        'left_height, left_lca = dfs': track(cap_call_l),
        'right_height, right_lca = dfs': track(cap_call_r),
        'if left_height > right_height': track(cap_gt),
        'return left_height + 1, left_lca': track(lambda S, B, r: f'左边更高：高度 `{S.left_height} + 1 = {r[0]}`，lca 沿用左子树的 `{nv(r[1])}`', record=True),
        'if left_height < right_height': track(cap_lt),
        'return right_height + 1, right_lca': track(lambda S, B, r: f'右边更高：高度 `{S.right_height} + 1 = {r[0]}`，lca 沿用右子树的 `{nv(r[1])}`', record=True),
        'return left_height + 1, node': track(lambda S, B, r: f'==一样高==（都是 `{S.left_height}`）：最深叶子左右都有 → lca 就是当前节点 `{S.node.val}`，高度 `{r[0]}`', record=True),
        'return dfs(root)[1]': track(lambda S, B, r: '从根节点开始递归：返回值是 `(高度, lca)`，最后取下标 `[1]`' if r is None else f'根的返回值是 `(高度, lca)`，取下标 `[1]` → 答案节点 `{nv(r)}`'),
    },
    cards=dict(
        one_liner='每棵子树返回 (高度, lca)：左高取左，右高取右，一样高就是自己',
        complexity='时间 `O(n)`，空间 `O(n)`（最坏退化成链的递归栈）',
        problem=['给你二叉树的根 `root`，返回它==最深叶节点==的最近公共祖先',
                 '最深叶子可能有多个：答案是它们所有的 lca；只有一个时就是它自己',
                 '示例：`[3,5,1,6,2,0,8,null,null,7,4]` → 节点 `2`（子树 `[2,7,4]`）',
                 '本视频：`[3,5,1,6,2]` → 最深叶子 `6`、`2`，lca 是 `5`，返回 `[5,6,2]`'],
        quote='把每棵子树都看成是一个「子问题」……需要知道：这棵子树最深叶子的深度（相当于这棵子树的**高度**），以及这棵子树的最深叶子的最近公共祖先 lca。',
        quote_src='—— 灵茶山艾府题解 · 方法二：自底向上',
        idea=['`leftHeight > rightHeight`：最深叶子全在左边 → lca 取左子树的 lca',
              '`leftHeight < rightHeight`：同理取右子树的 lca',
              '一样高：左右各有最深叶子，当前节点就是它们的 ==最近公共祖先==',
              '空节点返回 `(0, None)`，每层把高度 `+1`'],
        result='运行结束，返回节点 `5`（子树 `[5,6,2]`）：最深叶子 `6`、`2` 的 lca',
        summary=['时间 `O(n)`：每个节点恰好访问一次；空间 `O(n)`',
                 '易错：节点 `1` 也左右一样高，但它不最深，上层比较高度会丢掉它',
                 '空节点高度是 `0`，不是 `-1`；叶子两边都空，lca 是自己',
                 '方法一：传 `depth`，用全局 `max_depth` 和 `ans` 判断',
                 '同类题：236（最近公共祖先）、865（本题重复）'],
    ),
)
