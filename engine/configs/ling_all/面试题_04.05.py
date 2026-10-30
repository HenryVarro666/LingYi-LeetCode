# 每个访问过的节点下方标出它的合法开区间 (left, right)：绿 = 合法，红 = 不合法，黄 = 正在检查
TREE_H = 380
INFO = {}
SEEN6 = set()


def f(v):
    return '-∞' if v == -inf else ('∞' if v == inf else str(v))


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


def track(fn, visit=False, result=False):
    def cap(S, B, ret):
        r = B.get('root')
        if visit and r is not None:
            INFO[r._uid] = [f"({f(B['left'])}, {f(B['right'])})", 'run']
            SEEN6.discard(r._uid)
        if result and ret is not None and r is not None and r._uid in INFO:
            INFO[r._uid][1] = 'ok' if ret else 'bad'
        for n in _walk(S.get('self.tree')):
            n._d = tuple(INFO[n._uid]) if n._uid in INFO else None
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
        c = {'run': T['yellow'], 'ok': T['green'], 'bad': T['red']}[d[1]]
        w = cv.tlen(d[0], 18, bold=True) + 14
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=c, width=2, r=8)
        cv.text((X, Y + rad + 18), d[0], 18, c, anchor='mm', bold=True)


def tree_color(S, n):
    d = getattr(n, '_d', None)
    if d is None:
        return None
    return {'run': 'yellow', 'ok': 'green', 'bad': 'red'}[d[1]]


def nv(x):
    return '空' if x is None else str(x.val)


def cap_if(S, B, ret):
    if B.root is None:
        return '空树没有违规的地方 → 返回 `True`，==递归边界=='
    return f'节点 `{B.root.val}` 非空，要检查它是否落在合法区间里'


def cap_x(S, B, ret):
    return f'`x = {B.root.val}`，这个节点必须满足 `{f(B.left)} < x < {f(B.right)}`'


def cap_ret(S, B, ret):
    if ret is None and B.root._uid in SEEN6:
        return f'左子树返回 `True`（合法）→ `and` 继续，去检查右子树'
    if ret is None:
        SEEN6.add(B.root._uid)
        return f'先判断 `{f(B.left)} < {B.root.val} < {f(B.right)}`，成立才递归左子树，区间变成 `({f(B.left)}, {B.root.val})`'
    x = B.root.val
    if not (B.left < x < B.right):
        return f'`{f(B.left)} < {x} < {f(B.right)}` ==不成立==：`{x}` 越出了祖先给的范围 → 返回 `False`，后面不用再看'
    return f'`{x}` 在 `({f(B.left)}, {f(B.right)})` 内，左右子树也都合法 → 返回 `{ret}`'


CONFIG = dict(
    num='面试题 04.05', title='合法二叉搜索树', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='前序遍历 · 传下界和上界', tags=[],
    code='''
class Solution:
    def isValidBST(self, root: Optional[TreeNode], left=-inf, right=inf) -> bool:
        if root is None:
            return True
        x = root.val
        return left < x < right and \\
               self.isValidBST(root.left, left, x) and \\
               self.isValidBST(root.right, x, right)
''',
    call='''s = Solution()
s.tree = Tr([5,1,4,None,None,3,6])
s.isValidBST(s.tree)''',
    expect=False,
    views=[
        dict(type='tree', label='二叉树（下方 = 合法区间；黄 检查中 / 绿 合法 / 红 不合法）', pointers={'root': 'blue'},
             h=TREE_H, color=tree_color),
        dict(type='custom', draw=badges, h=0),
        dict(type='calls', h=200, hide=('isValidBST',)),
    ],
    watch=[('root', lambda S: S['_inner'].get('root') and S['_inner']['root'].val, 'blue'),
           ('left', lambda S: f(S['_inner']['left']) if 'left' in S['_inner'] else None, 'cyan'),
           ('right', lambda S: f(S['_inner']['right']) if 'right' in S['_inner'] else None, 'pink')],
    captions={
        'if root is None': track(cap_if, visit=True),
        'return True': track('空节点：没有任何数违反规则 → 返回 `True`', result=True),
        'x = root.val': track(cap_x),
        'return left < x < right': track(cap_ret, result=True),
        'self.isValidBST(root.left': track(lambda S, B, ret: (
            f'左子树里所有数都要 `< {B.root.val}`：下界不变 `{f(B.left)}`，上界收紧成 `{B.root.val}`'
            if ret is None else f'返回 `{ret}`'), result=True),
        'self.isValidBST(root.right': track(lambda S, B, ret: (
            f'右子树里所有数都要 `> {B.root.val}`：下界抬高成 `{B.root.val}`，上界不变 `{f(B.right)}`'
            if ret is None else f'返回 `{ret}`'), result=True),
    },
    max_steps=60,
    cards=dict(
        one_liner='每个节点都有一个合法区间，往左收上界、往右抬下界',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['判断一棵二叉树是不是二叉搜索树（BST）',
                 '左子树所有值 ==小于== 根，右子树所有值 ==大于== 根，且每棵子树也是 BST',
                 '示例 1：`[2,1,3]` → `true`',
                 '示例 2：`[5,1,4,null,null,3,6]` → `false`'],
        quote='前序遍历在某些数据下不需要递归到边界（base case）就能返回，而另外两种至少要递归到一个边界，从这个角度上来说它是最快的。',
        quote_src='—— 灵茶山艾府题解点评',
        idea=['只比较父子不够：`3` 在 `4` 的左边，却比根 `5` 小才对，所以要把==祖先的限制==带下去',
              '递归参数 `left`、`right` 就是当前节点必须落在的开区间',
              '往左走：上界变成当前值；往右走：下界变成当前值'],
        result='`3` 落在右子树，要求 `> 5`，不成立 → 返回 `False`',
        summary=['时间 `O(n)`，空间 `O(n)`（最坏退化成链的递归栈）',
                 '易错：只比较节点和它的儿子会漏判（如 `3` 在根 `5` 的右子树里）',
                 '易错：BST 不允许相等值，所以是严格小于（`<`）',
                 '另外两种：中序遍历看是否严格递增；后序遍历自底向上返回子树 (最小值, 最大值)'],
    ),
)
