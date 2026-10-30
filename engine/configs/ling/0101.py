# ---- 值已经配对相等的节点涂绿：caption 回调里记录，tree 视图 color 读取
DONE = set()


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


def track(fn, mark=False):
    def cap(S, B, ret):
        if mark and ret is None and B.p is not None and B.q is not None and B.p.val == B.q.val:
            DONE.update([B.p._uid, B.q._uid])
        for n in _walk(S.get('self.tree')):
            n._d = n._uid in DONE
        return fn(S, B, ret) if callable(fn) else fn
    return cap


def parent_of(root, x):
    for n in _walk(root):
        if n.left is x or n.right is x:
            return n
    return None


def side(S):
    """这一对是外侧（p.left vs q.right）还是内侧（p.right vs q.left）"""
    t = S.get('self.tree')
    for x, outer in ((S.p, 'left'), (S.q, 'right')):
        if x is not None:
            par = parent_of(t, x)
            if par is t:
                return '根的左右子树'
            return '外侧' if getattr(par, outer) is x else '内侧'
    return ''


def nv(x):
    return '空' if x is None else str(x.val)


def cap_if(S, B, ret):
    sd = side(S)
    if S.p is None and S.q is None:
        return '这一对两边都是空 → 递归边界'
    if S.p is None or S.q is None:
        return f'{sd}这一对：`p = {nv(S.p)}`，`q = {nv(S.q)}`，==一空一不空=='
    return f'比较{sd}这一对：`p = {S.p.val}`，`q = {S.q.val}`，都不为空 → 看值和儿子'


def cap_is(S, B, ret):
    if ret:
        return '`p is q`：两个都是 `None` → 返回 `True`，==空对空也是镜像=='
    return '`p is q`：一个空一个不空 → ==不是镜像==，返回 `False`'


def cap_main(S, B, ret):
    if ret is not None:  # 值不相等，短路返回
        return f'`{B.p.val} != {B.q.val}` → ==值不同，不是镜像==，返回 `False`'
    return (f'`{B.p.val} == {B.q.val}` ✓ → 递归比较==外侧==：`p.left`（{nv(S.p)}）与 `q.right`（{nv(S.q)}）；'
            f'成功后再比内侧 `p.right` 与 `q.left`')


CONFIG = dict(
    num=101, title='对称二叉树', difficulty='Easy', category='二叉树',
    author='灵茶山艾府', technique='递归 · 相同的树改成镜像判断',
    code='''
class Solution:
    # 100. 相同的树（改成镜像判断）
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if p is None or q is None:
            return p is q
        return p.val == q.val and self.isSameTree(p.left, q.right) and self.isSameTree(p.right, q.left)

    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        return self.isSameTree(root.left, root.right)
''',
    call='''s = Solution()
s.tree = Tr([1,2,2,3,4,4,3])
s.isSymmetric(s.tree)''',
    expect=True,
    views=[
        dict(type='tree', label='二叉树（绿 = 这一对的值已配对相等）', pointers={'p': 'blue', 'q': 'pink'}, h=380,
             color=lambda S, n: 'green' if getattr(n, '_d', False) else None),
        dict(type='calls', h=240),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink')],
    captions={
        'return self.isSameTree(root.left': track('把树拆成左子树 `p` 和右子树 `q`：判断它们是否==互为镜像=='),
        'if p is None or q is None': track(cap_if),
        'return p is q': track(cap_is),
        'return p.val == q.val': track(cap_main, mark=True),
    },
    cards=dict(
        one_liner='把「相同的树」改成镜像判断：左儿子对右儿子',
        complexity='时间 `O(n)`，空间 `O(n)`（最坏退化成链的递归栈）',
        problem=['给你二叉树的根 `root`，检查它是否==轴对称==',
                 '示例 1：`[1,2,2,3,4,4,3]` → `true`',
                 '示例 2：`[1,2,2,null,3,null,3]` → `false`'],
        quote='把二叉树拆分成左子树 p 和右子树 q。类似 100. 相同的树，必须满足：p.val 等于 q.val；==p 的左儿子与 q 的右儿子互为镜像==；p 的右儿子与 q 的左儿子……',
        quote_src='—— 灵茶山艾府题解「思路」',
        idea=['和「100. 相同的树」只差一点：==左配右、右配左==',
              '边界：`p`、`q` 至少一个为空时，只有两个都空才是镜像（`p is q`）',
              '`and` 会短路：一旦发现不对称，后面的递归都不再执行'],
        result='运行结束，返回 `True`：每一对镜像位置的值都相等，树是对称的',
        summary=['时间 `O(n)`：每个节点比较一次；空间 `O(n)`：最坏退化成链',
                 '易错：外侧 `p.left` 配 `q.right`，内侧 `p.right` 配 `q.left`',
                 '`return p is q` 一行同时处理「都空」和「一空一不空」',
                 '思考题（灵神）：能否 `O(n)` 求出有多少棵子树是对称的？'],
    ),
)
