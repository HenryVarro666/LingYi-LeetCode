# ---- 树上"已返回"标注：caption 回调里记录每个节点返回的 (选, 不选)，custom 叠加层（h=0）画在节点下方
TREE_H = 360
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
        for n in _walk(S.get('root')):
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
    root = S.get('root')
    if root is None:
        return
    pos, rad, order = _layout(root, (box[0], box[1] - TREE_H, box[2], box[1]))
    for n in order:
        d = getattr(n, '_d', None)
        if d is None:
            continue
        X, Y = pos[n._uid]
        s = f'({d[0]}, {d[1]})'
        w = cv.tlen(s, 18, bold=True) + 14
        cv.rect((X - w / 2, Y + rad + 4, X + w / 2, Y + rad + 28), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 16), s, 18, T['green'], anchor='mm', bold=True)


def nv(x):
    return '空' if x is None else str(x.val)


def _inner(*names):
    def f(S):
        I = S['_inner']
        if names[0] not in I:
            return None
        return tuple(I[k] for k in names)
    return f


def formula(S):
    I = S['_inner']
    ln = S.get('_line')
    if ln == 8 and 'rob' in I:
        return f"==选== `{I['node'].val}`：`{I['l_not_rob']} + {I['r_not_rob']} + {I['node'].val} = {I['rob']}`（儿子都不选）"
    if ln in (9, 10) and 'not_rob' in I:
        return (f"==不选== `{I['node'].val}`：`max({I['l_rob']},{I['l_not_rob']}) + max({I['r_rob']},{I['r_not_rob']})"
                f" = {I['not_rob']}`（儿子随意）")
    return '`dfs(node)` 返回 `(选 node 的最大值, 不选 node 的最大值)`'


def cap_if(S, B, ret):
    if S.node is None:
        return '空节点 → 递归边界'
    return f'节点 `{S.node.val}`：先算出左右子树的结果，再算自己（==后序遍历==）'


def cap_l(S, B, ret):
    if S.node is None:
        return f'`{B.node.val}` 没有左儿子：`dfs(None)` 会返回 `(0, 0)`'
    return f'递归左子树 `dfs({S.node.val})`'


def cap_r(S, B, ret):
    head = f'左子树返回 `(选 {B.l_rob}, 不选 {B.l_not_rob})`；'
    if S.node is None:
        return head + '没有右儿子，`dfs(None)` 返回 `(0, 0)`'
    return head + f'递归右子树 `dfs({S.node.val})`'


def cap_rob(S, B, ret):
    return (f'右子树返回 `({S.r_rob}, {S.r_not_rob})`。==选== `{S.node.val}`：两个儿子都==不能选== → '
            f'`{S.l_not_rob} + {S.r_not_rob} + {S.node.val} = {S.rob}`')


def cap_not(S, B, ret):
    return (f'==不选== `{S.node.val}`：儿子选不选随意，各取较大的 → '
            f'`max({S.l_rob},{S.l_not_rob}) + max({S.r_rob},{S.r_not_rob}) = {S.not_rob}`')


CONFIG = dict(
    num=337, title='打家劫舍 III', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='树形 DP · 选或不选',
    tags=['热题173'],
    code='''
class Solution:
    def rob(self, root: Optional[TreeNode]) -> int:
        def dfs(node: Optional[TreeNode]) -> Tuple[int, int]:
            if node is None:  # 递归边界
                return 0, 0  # 没有节点，怎么选都是 0
            l_rob, l_not_rob = dfs(node.left)  # 递归左子树
            r_rob, r_not_rob = dfs(node.right)  # 递归右子树
            rob = l_not_rob + r_not_rob + node.val  # 选
            not_rob = max(l_rob, l_not_rob) + max(r_rob, r_not_rob)  # 不选
            return rob, not_rob

        return max(dfs(root))  # 根节点选或不选的最大值
''',
    call='Solution().rob(Tr([3,2,3,None,3,None,1]))',
    expect=7,
    views=[
        dict(type='tree', var='root', label='房子二叉树（绿 = 已算完，下方 = (选, 不选) 的最大金额）', pointers={'node': 'blue'},
             h=TREE_H, color=lambda S, n: 'green' if getattr(n, '_d', None) is not None else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='text', fn=formula, size=26, h=60),
        dict(type='calls', h=200),
    ],
    watch=[('node', lambda S: S['node'].val if S.get('node') is not None else None, 'blue'), ('左', _inner('l_rob', 'l_not_rob')),
           ('右', _inner('r_rob', 'r_not_rob')), ('自己', _inner('rob', 'not_rob'), 'green')],
    captions={
        'return max(dfs(root))': track('从根开始递归：每个节点都返回==两个数==——选它 / 不选它时，子树的最大金额'),
        'if node is None': track(cap_if),
        'return 0, 0': track('没有节点，怎么选都是 `0` → 返回 `(0, 0)`'),
        'l_rob, l_not_rob = dfs': track(cap_l),
        'r_rob, r_not_rob = dfs': track(cap_r),
        'rob = l_not_rob': track(cap_rob),
        'not_rob = max': track(cap_not),
        'return rob, not_rob': track(lambda S, B, ret: f'节点 `{S.node.val}` 算完，把 `(选 {ret[0]}, 不选 {ret[1]})` 交给父节点',
                                     key='node'),
    },
    cards=dict(
        one_liner='每个节点返回两个数：选它的最大金额、不选它的最大金额',
        complexity='时间 `O(n)`，空间 `O(n)`（最坏退化成链的递归栈）',
        problem=['房子排成一棵二叉树，==直接相连==的两间房子同一晚被偷会报警',
                 '求不触动警报时最多能偷多少钱',
                 '示例：`root = [3,2,3,null,3,null,1]` → `7`（`3 + 3 + 1`）'],
        quote='`rob = l_not_rob + r_not_rob + node.val  # 选`\n`not_rob = max(l_rob, l_not_rob) + max(r_rob, r_not_rob)  # 不选`',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['对每个节点「==选或不选==」：选它，左右儿子都不能选；不选它，儿子选不选都行',
              '`dfs(node)` 同时返回两种情况的最大值，父节点只需要儿子的这两个数',
              '空节点返回 `(0, 0)`；答案是根节点两种情况取 `max`'],
        result='根节点返回 `(7, 6)`：选根 `3 + 3 + 1 = 7` 比不选根的 `6` 大 → 答案 `7` ✓',
        summary=['时间 `O(n)`：每个节点递归恰好一次；空间 `O(n)`：最坏是一条链',
                 '易错：选当前节点时，用的是儿子的「==不选==」值，不是 `max`',
                 '易错：不能简单地「隔一层选一层」：`[2,1,3,null,4]` 最优是 `3 + 4 = 7`',
                 '灵神：这就是树形 DP「选或不选」，类比 198 打家劫舍的线性版本'],
    ),
)
