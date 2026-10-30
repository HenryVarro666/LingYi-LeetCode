import views as V

# ---- 两棵树并排画：值已比对相等的一对涂绿，发现不同的涂红（caption 回调里记录）
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


def track(fn, mark=False, bad=False):
    def cap(S, B, ret):
        p, q = B.get('p'), B.get('q')
        if mark and ret is None and p is not None and q is not None and p.val == q.val:
            DONE[p._uid] = DONE[q._uid] = 'green'
        if bad and ret is False:
            for x in (p, q):
                if x is not None:
                    DONE[x._uid] = 'red'
        for n in _walk(S.get('self.P')) + _walk(S.get('self.Q')):
            n._d = DONE.get(n._uid)
        return fn(S, B, ret) if callable(fn) else fn
    return cap


def _color(S, n):
    return getattr(n, '_d', None)


def two_trees(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    mid = (x0 + x1) / 2
    st = {'_S': S, '_B': B}
    V.v_tree(cv, dict(var='self.P', label='树 p', pointers={'p': 'blue'}, path=False, color=_color),
             st, (x0, y0, mid, y1), 0, {})
    V.v_tree(cv, dict(var='self.Q', label='树 q', pointers={'q': 'pink'}, path=False, color=_color),
             st, (mid, y0, x1, y1), 0, {})
    cv.line([(mid, y0 + 10), (mid, y1 - 10)], T['border'], 2)


def nv(x):
    return '空' if x is None else str(x.val)


def cap_if(S, B, ret):
    if S.p is None and S.q is None:
        return '`p`、`q` 都是空 → 递归边界'
    if S.p is None or S.q is None:
        return f'`p = {nv(S.p)}`，`q = {nv(S.q)}`：==有一个是空== → 递归边界'
    par = next((n for n in _walk(S.get('self.P')) if n.right is S.p), None)
    pre = '左子树相同 ✓ → 再比右子树：' if par is not None else ''
    return pre + f'`p = {S.p.val}`，`q = {S.q.val}` 都不为空 → 比较值，再递归比较儿子'


def cap_is(S, B, ret):
    if ret:
        return '`p is q`：两个都是 `None` → `True`，==空树和空树相同=='
    return f'`p is q`：`p = {nv(B.p)}`，`q = {nv(B.q)}`，一空一不空 → ==False=='


def cap_main(S, B, ret):
    if ret is not None:
        return f'`{B.p.val} != {B.q.val}` → 值不同，`and` 短路，直接返回 `False`'
    return (f'`{B.p.val} == {B.q.val}` ✓ → 递归比较==左子树==：`p.left`（{nv(S.p)}）与 `q.left`（{nv(S.q)}）；'
            f'相同才会接着比右子树')


CONFIG = dict(
    num=100, title='相同的树', difficulty='Easy', category='二叉树',
    author='灵茶山艾府', technique='递归 · 原问题 = 根相同 + 左子树相同 + 右子树相同',
    tags=['面试经典150'],
    code='''
class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if p is None or q is None:
            return p is q  # 必须都是 None
        return p.val == q.val and self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
''',
    call='''s = Solution()
s.P = Tr([1,2,3,None,4,5])
s.Q = Tr([1,2,3,None,4,None,5])
s.isSameTree(s.P, s.Q)''',
    expect=False,
    views=[
        dict(type='custom', draw=two_trees, h=330),
        dict(type='text', fn=lambda S: f"正在比较：`p = {nv(S['p'])}`  vs  `q = {nv(S['q'])}`", size=28, h=60),
        dict(type='calls', h=250),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink')],
    captions={
        'if p is None or q is None': track(cap_if),
        'return p is q': track(cap_is, bad=True),
        'return p.val == q.val': track(cap_main, mark=True),
    },
    cards=dict(
        one_liner='两棵树相同 = 根的值相同 + 左子树相同 + 右子树相同',
        complexity='时间 `O(min(n,m))`，空间 `O(min(n,m))`',
        problem=['给你两棵二叉树的根节点 `p` 和 `q`，判断这两棵树是否相同',
                 '相同：==结构相同==，并且对应节点的==值相同==',
                 '示例：`p = [1,2]`，`q = [1,null,2]` → `false`（结构不同）'],
        quote='`return p is q  # 必须都是 None`',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['原问题拆成三个子问题：根的值相等、左子树相同、右子树相同，==子问题和原问题一模一样== → 递归',
              '边界：`p`、`q` 有一个为空时，只有==两个都为空==才相同，一行 `p is q` 搞定',
              '本例两棵树只差最后一个节点：`5` 在左还是在右'],
        result='`False` 一路短路返回到根：节点 3 下面 p 有左儿子 5，q 没有 → ==结构不同==',
        summary=['时间 `O(min(n,m))`：发现不同就停；空间同阶（最坏退化成链的递归栈）',
                 '`and` 短路：左子树不同，右子树就不会再比',
                 '易错：只判断 `p is None` 就去访问 `q.val`，会对空节点报错',
                 '同一个框架改一改：101 对称二叉树（左配右）、110 平衡二叉树、199 右视图'],
    ),
)
