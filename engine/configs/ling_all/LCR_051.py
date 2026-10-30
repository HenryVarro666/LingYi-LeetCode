TREE_H = 380
DONE = {}
SNAP = {}  # id(S) -> 该步结束时已返回的节点 {uid: 链和}；绘制时按步取，避免被后面的步骤污染


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
    root = S.get('root')
    if root is None:
        return
    pos, rad, order = _layout(root, (box[0], box[1] - TREE_H, box[2], box[1]))
    for n in order:
        d = SNAP.get(id(S), {}).get(n._uid)
        if d is None:
            continue
        X, Y = pos[n._uid]
        s = f'链 {d}'
        w = cv.tlen(s, 19, bold=True) + 16
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 18), s, 19, T['green'], anchor='mm', bold=True)


def track(fn, record=False):
    def cap(S, B, ret):
        if record and S.node is not None:
            DONE[S.node._uid] = ret
        SNAP[id(S)] = dict(DONE)
        return fn(S, B, ret) if callable(fn) else fn
    return cap


def cap_pair(S, B, ret):
    n = S.node
    return (f'左链 `{S.l_val}` + 右链 `{S.r_val}` + 自己 `{n.val}` = `{S.l_val + S.r_val + n.val}`：'
            f'==两条链在 `{n.val}` 处拼成一条路径==，和已有最大值 `{B.ans}` 比 → '
            + (f'==更新 `ans = {S.ans}`==' if S.ans != B.ans else f'不更新，`ans` 仍是 `{S.ans}`'))


def cap_ret(S, B, ret):
    n = S.node
    best = max(S.l_val, S.r_val)
    if best + n.val < 0:
        return f'`max({best} + {n.val}, 0) = 0`：这条链是负的，==宁可不要，当作 0== 返回给父节点'
    return f'`max(max({S.l_val}, {S.r_val}) + {n.val}, 0) = {ret}`：只能选一侧的链接上自己，往上返回'


CONFIG = dict(
    num='LCR 051', title='二叉树中的最大路径和', difficulty='Hard', category='二叉树与回溯',
    author='灵茶山艾府', technique='树形 DP · 最大链和',
    code='''
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        ans = -inf
        def dfs(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0  # 没有节点，和为 0
            l_val = dfs(node.left)  # 左子树最大链和
            r_val = dfs(node.right)  # 右子树最大链和
            nonlocal ans
            ans = max(ans, l_val + r_val + node.val)  # 两条链拼成路径
            return max(max(l_val, r_val) + node.val, 0)  # 当前子树最大链和
        dfs(root)
        return ans
''',
    call='''root = Tr([-10,9,20,None,None,15,7])
Solution().maxPathSum(root)''',
    expect=42,
    views=[
        dict(type='tree', label='二叉树（绿 = 已返回的最大链和）', pointers={'node': 'blue'}, h=TREE_H,
             color=lambda S, n: 'green' if n._uid in SNAP.get(id(S), {}) else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='calls', h=240),
    ],
    watch=[('node', lambda S: S['_inner'].get('node').val if S['_inner'].get('node') is not None else None, 'blue'),
           ('l_val', lambda S: S['_inner'].get('l_val')), ('r_val', lambda S: S['_inner'].get('r_val')),
           ('ans', lambda S: S.get('ans'), 'green')],
    captions={
        'ans = -inf': track('`ans` 记录==最大路径和==，初始是负无穷（节点值可能全为负）'),
        'if node is None': track(lambda S, B, r: ('空节点 → 没有链可选，是==递归边界==' if S.node is None
                                           else f'节点 `{S.node.val}` 非空 → 要先拿到左右子树的最大链和')),
        'return 0': track('没有节点，和为 `0`'),
        'l_val = dfs': track(lambda S, B, r: (f'递归左子树 `dfs({B.node.left.val})`：==相信它返回左子树的最大链和==' if B.node.left is not None
                                       else '没有左儿子 → `dfs(None)` 直接返回 `0`')),
        'r_val = dfs': track(lambda S, B, r: (f'左链 `l_val = {B.l_val}` 已拿到；递归右子树 `dfs({B.node.right.val})`' if B.node.right is not None
                                       else f'左链 `l_val = {B.l_val}` 已拿到；没有右儿子 → `dfs(None)` 返回 `0`')),
        'ans = max': track(cap_pair),
        'return max': track(cap_ret, record=True),
        'dfs(root)': track('从根节点开始递归'),
        'return ans': track('所有节点都当过「拐点」，最大路径和 = ==`{ans}`=='),
    },
    max_steps=90,
    cards=dict(
        one_liner='每个节点当一次拐点：左链 + 右链 + 自己；往上只返回一条链',
        complexity='时间 `O(n)`，空间 `O(n)`（最坏退化成链的递归栈）',
        problem=['路径：沿父子边走，每个节点至多一次，至少一个节点，不必过根',
                 '路径和 = 路径上节点值之和，求最大路径和',
                 '示例：`[-10,9,20,null,null,15,7]` → `42`（`15 → 20 → 7`）'],
        quote='ans = max(ans, l_val + r_val + node.val)  # 两条链拼成路径',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['`dfs(node)` 返回以 `node` 为==链顶==、向下走的最大链和',
              '路径的最高点是 `node` 时：==左链 + 右链 + node.val==，用它更新 `ans`',
              '返回给父节点只能选一侧：`max(l, r) + node.val`，负数就 `max(…, 0)` 舍掉'],
        result='运行结束，返回 `42`：最优路径 `15 → 20 → 7`，在节点 `20` 处拼成',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：更新答案用「左链 + 右链 + 自己」，返回给父节点却只能带一侧',
                 '易错：`ans` 初始要是负无穷，节点值可以全为负；空节点返回 `0`，负链用 `max(…, 0)` 舍掉',
                 '同类题：543. 二叉树的直径、2246. 相邻字符不同的最长路径、687. 最长同值路径'],
    ),
)
