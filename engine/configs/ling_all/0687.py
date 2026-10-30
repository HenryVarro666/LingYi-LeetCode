# ---- 已返回节点：caption 回调里记录每个节点 dfs 的返回值（最长链长），在节点下方画徽标
TREE_H = 380
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
        if record and nd is not None:
            DONE[nd._uid] = ret
        root = S.get('root')
        if root is not None:
            for n in _walk(root):
                n._d = DONE.get(n._uid)
        if callable(fn):
            return fn(S, B, ret)
        g = dict(S)
        g.update(B=B, ret=ret)
        try:
            return eval('f' + repr(fn), g)
        except Exception:
            return fn
    cap._t = True
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
    root = S.get('root')
    if root is None:
        return
    pos, rad, order = _layout(root, (box[0], box[1] - TREE_H, box[2], box[1]))
    for n in order:
        d = getattr(n, '_d', None)
        if d is None:
            continue
        X, Y = pos[n._uid]
        s = f'链长 {d}'
        w = cv.tlen(s, 19, bold=True) + 16
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 18), s, 19, T['green'], anchor='mm', bold=True)


def _l(S, B, ret):
    n = S.node
    if n.left and n.left.val != n.val:
        return f'左儿子 `{n.left.val}` ≠ `{n.val}` → 接不上，左链视作 ==0=='
    if n.left:
        return f'左儿子 `{n.left.val}` = `{n.val}` → 左链保留 `l_len = {S.l_len}`'
    return '没有左儿子（`-1 + 1 = 0`），左链长 0'


def _r(S, B, ret):
    n = S.node
    if n.right and n.right.val != n.val:
        return f'右儿子 `{n.right.val}` ≠ `{n.val}` → 接不上，右链视作 ==0=='
    if n.right:
        return f'右儿子 `{n.right.val}` = `{n.val}` → 右链保留 `r_len = {S.r_len}`'
    return '没有右儿子，右链长 0'


CONFIG = dict(
    num=687, title='最长同值路径', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='树形 DP · 二叉树的直径',
    tags=['灵神题单·动态规划', '灵神题单·链表树与回溯'],
    code='''
class Solution:
    def longestUnivaluePath(self, root: Optional[TreeNode]) -> int:
        ans = 0
        def dfs(node: Optional[TreeNode]) -> int:
            if node is None:
                return -1  # 下面 +1 后，对于叶子节点就刚好是 0
            l_len = dfs(node.left) + 1  # 左子树最大链长+1
            r_len = dfs(node.right) + 1  # 右子树最大链长+1
            if node.left and node.left.val != node.val: l_len = 0  # 视作 0
            if node.right and node.right.val != node.val: r_len = 0  # 视作 0
            nonlocal ans
            ans = max(ans, l_len + r_len)  # 两条链拼成路径
            return max(l_len, r_len)  # 当前子树最大链长
        dfs(root)
        return ans
''',
    call='Solution().longestUnivaluePath(Tr([5,4,5,1,1,5]))',
    expect=2,
    views=[
        dict(type='tree', label='二叉树（蓝 = node，绿 = 已返回链长）', pointers={'node': 'blue'}, h=TREE_H,
             color=lambda S, n: 'green' if getattr(n, '_d', None) is not None else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='text', fn=lambda S: (f"两条链拼成路径：`{S['_inner']['l_len']} + {S['_inner']['r_len']}`　当前答案 `ans = {S.get('ans', 0)}`"
                                        if 'l_len' in S['_inner'] and 'r_len' in S['_inner'] else f"当前答案 `ans = {S.get('ans', 0)}`"), size=24, h=50),
        dict(type='calls', h=210),
    ],
    watch=[('node', lambda S: S['node'].val if S.get('node') is not None else None, 'blue'),
           ('l_len', lambda S: S['_inner'].get('l_len')), ('r_len', lambda S: S['_inner'].get('r_len')),
           ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 记录全局最长路径（边数），先设为 0',
        'if node is None': lambda S, B, r: ('空节点：没有链可言，当作 `-1`' if S.node is None
                                           else f'节点 `{S.node.val}`：先递归左右子树，再决定能不能接上'),
        'return -1': track('空节点返回 `-1`，上一层 `+1` 后 → 叶子的链长刚好是 `0`'),
        'l_len = dfs': track('递归左子树 `dfs(node.left)`，返回的链长 `+1` 才算上连向左儿子的那条边'),
        'r_len = dfs': track('递归右子树，同样 `+1`。==先递归、后判断==，每个节点才都访问到'),
        'if node.left and': track(_l),
        'if node.right and': track(_r),
        'nonlocal ans': '声明 `ans` 是外层变量，下面才能更新它',
        'ans = max': track('左右两条链在 `node` 处拼成路径：`{l_len} + {r_len}` = {l_len + r_len}；`ans = max({B.ans}, {l_len + r_len})` → =={ans}=='),
        'return max': track('只能向父亲延伸一条链：返回 `max({l_len}, {r_len})` = =={ret}==', record=True),
        'dfs(root)': '从根节点开始递归',
        'return ans': '最长同值路径 = `{ans}` 条边',
    },
    max_steps=95,
    cards=dict(
        one_liner='直径模板：左右链长拼起来，值不同就当作 0',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给你二叉树 `root`，返回最长的、==每个节点值都相同==的路径长度',
                 '路径长度 = 边数；可以不经过根',
                 '示例：`[5,4,5,1,1,5]` → `2`（三个 5 连成一条路径）'],
        quote='先判断节点值是否相同，不同则不往下递归的写法是错误的。想一想，如果正确答案在更下面的子树当中呢？必须保证每个节点都访问到。',
        quote_src='—— 灵茶山艾府题解「常见错误」',
        idea=['在 543 二叉树的直径上改：直径 = 左链 + 右链',
              '儿子的值和自己不同 → 这一侧的链长视作 `0`',
              '`dfs` 返回「以 node 为顶的最长单链」，更新答案时拼上两侧'],
        summary=['时间 `O(n)`，空间 `O(n)`（链状树递归栈）',
                 '空节点返回 `-1`：`+1` 后叶子刚好是 `0`，边数口径统一',
                 '==先递归再判断==：不能因为值不同就不往下走，答案可能在更深的子树',
                 '同类题：543 直径、124 最大路径和、2246 相邻字符不同的最长路径'],
    ),
)

CONFIG['captions'] = {k: (v if getattr(v, '_t', False) else track(v)) for k, v in CONFIG['captions'].items()}
