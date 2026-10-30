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
        s = f'链长 {d}'
        w = cv.tlen(s, 18, bold=True) + 14
        cv.rect((X - w / 2, Y + rad + 4, X + w / 2, Y + rad + 28), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 16), s, 18, T['green'], anchor='mm', bold=True)


def nv(x):
    return '空' if x is None else str(x.val)


def cap_if(S, B, ret):
    if S.node is None:
        return '空节点 → 递归边界'
    return f'节点 `{S.node.val}` 非空 → 先算左右两条链'


def cap_l(S, B, ret):
    if S.node is None:
        return f'`{B.node.val}` 没有左儿子：`dfs(None)` 返回 `-1`，`+1` 后左链为 `0`'
    return f'左子树最大链长+1：递归 `dfs({S.node.val})`，返回后 `+1` 补上==到左儿子的那条边=='


def cap_r(S, B, ret):
    if S.node is None:
        return f'左链 `l_len = {B.l_len}`；没有右儿子，右链会是 `-1 + 1 = 0`'
    return f'左链 `l_len = {B.l_len}`；右子树最大链长+1：递归 `dfs({S.node.val})`'


def cap_ans(S, B, ret):
    s = S.l_len + S.r_len
    tail = '，==刷新答案==' if S.ans > B.ans else ''
    return (f'两条链拼成路径：在 `{S.node.val}` 拐弯，`{S.l_len} + {S.r_len} = {s}`，'
            f'`ans = max({B.ans}, {s}) = {S.ans}`{tail}')


def cap_ret(S, B, ret):
    return f'当前子树最大链长：往上==只能交一条链==，`max({S.l_len}, {S.r_len}) = {ret}`'


CONFIG = dict(
    num=543, title='二叉树的直径', difficulty='Easy', category='二叉树',
    author='灵茶山艾府', technique='树形 DP · 枚举拐弯点',
    code='''
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        ans = 0

        # 返回 node 子树的最大链长
        def dfs(node: Optional[TreeNode]) -> int:
            if node is None:
                return -1  # 对于叶子来说，链长就是 -1+1=0
            l_len = dfs(node.left) + 1  # 左子树最大链长+1
            r_len = dfs(node.right) + 1  # 右子树最大链长+1
            nonlocal ans
            ans = max(ans, l_len + r_len)  # 两条链拼成路径
            return max(l_len, r_len)  # 当前子树最大链长

        dfs(root)
        return ans
''',
    call='''s = Solution()
s.tree = Tr([1,2,None,3,4,5,None,None,6])
s.diameterOfBinaryTree(s.tree)''',
    expect=4,
    views=[
        dict(type='tree', label='二叉树（绿 = 已返回链长）', pointers={'node': 'blue'}, h=TREE_H,
             color=lambda S, n: 'green' if getattr(n, '_d', None) is not None else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='calls', h=225),
    ],
    watch=[('node', 'node', 'blue'), ('l_len', lambda S: S['_inner'].get('l_len')), ('r_len', lambda S: S['_inner'].get('r_len')), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': track('`ans` 记录直径（边数），先设为 `0`'),
        'if node is None': track(cap_if),
        'return -1': track('空节点返回 `-1`：对于叶子来说，链长就是 `-1 + 1 = 0`'),
        'l_len = dfs': track(cap_l),
        'r_len = dfs': track(cap_r),
        'ans = max': track(cap_ans),
        'return max': track(cap_ret, key='node'),
        'dfs(root)': track('从根开始 `dfs`：==每个节点都试一次“在这里拐弯”=='),
        'return ans': track(lambda S, B, ret: f'所有拐弯点都试过了，返回 `ans = {ret}`'),
    },
    cards=dict(
        one_liner='枚举拐弯点：左链 + 右链，往上只交一条链',
        complexity='时间 `O(n)`，空间 `O(h)`（`h` 为树高）',
        problem=['二叉树的直径：任意两个节点之间==最长路径的边数==',
                 '这条路径==可能不经过根节点==',
                 '示例：`[1,2,3,4,5]` → `3`（路径 `4-2-1-3`）；本视频用一棵直径不过根的树'],
        quote='枚举每个点，从这个点往左走到最深，往右走到最深，用==两条链拼起来的长度==，更新答案的最大值。',
        quote_src='—— 灵茶山艾府题解「核心思路」',
        idea=['`dfs(node)` 返回 `node` 子树的==最大链长==（叶子到 `node` 的边数）',
              '在 `node` 拐弯的路径 = 左链 + 右链，用它更新 `ans`',
              '空节点返回 `-1`，叶子链长才是 `-1 + 1 = 0`'],
        result='运行结束，返回 `4`：路径 `5-3-2-4-6` 在节点 2 拐弯，==没有经过根节点 1==',
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '易错：`dfs` 返回的是==链==的长度，不是直径；返回直径就没法和上面的链继续拼接',
                 '易错：直径可能在 `root` 下面某个节点拐弯，所以要在每个节点更新 `ans`',
                 '写法二：空节点返回 `0`，`return max(l_len, r_len) + 1`，等价'],
    ),
)
