import views as V

# ---- 两棵树并排画：值比对相等的一对涂绿，暴露出结构差异的节点涂红（caption 回调里记录）
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


def _sync(S):
    for n in _walk(S.get('self.P')) + _walk(S.get('self.Q')):
        n._d = DONE.get(n._uid)


def track(fn):
    def cap(S, B, ret):
        out = fn(S, B, ret) if callable(fn) else fn
        _sync(S)
        return out
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


def cap_val(S, B, ret):
    if S.p.val == S.q.val:
        DONE[S.p._uid] = DONE[S.q._uid] = 'green'
        return f'`check`：根的值 `{S.p.val} == {S.q.val}` ✓ → 接着看左右儿子'
    return f'根的值 `{S.p.val} != {S.q.val}` → 不同'


def cap_pl(S, B, ret):
    if S.p.left:
        return f'p 的节点 `{S.p.val}` ==有左儿子== `{S.p.left.val}` → q 也必须有，并且左子树要相同'
    return f'p 的节点 `{S.p.val}` ==没有左儿子== → 那 q 也不能有'


def cap_pr(S, B, ret):
    if S.p.right:
        return f'p 的节点 `{S.p.val}` ==有右儿子== `{S.p.right.val}` → q 也必须有，并且右子树要相同'
    return f'p 的节点 `{S.p.val}` ==没有右儿子== → 那 q 也不能有'


def cap_ql(S, B, ret):
    if S.q.left:
        DONE[S.q.left._uid] = 'red'
        return f'可是 q 的节点 `{S.q.val}` 有左儿子 `{S.q.left.val}` → ==结构不同=='
    return f'q 的节点 `{S.q.val}` 也没有左儿子 ✓'


def cap_qr(S, B, ret):
    if S.q.right:
        DONE[S.q.right._uid] = 'red'
        return f'可是 q 的节点 `{S.q.val}` 有右儿子 `{S.q.right.val}` → ==结构不同=='
    return f'q 的节点 `{S.q.val}` 也没有右儿子 ✓'


def cap_or(side):
    def f(S, B, ret):
        if getattr(S.p, '_uid', None) != getattr(B.p, '_uid', None):
            return (f'q 也有{side}儿子 → 递归 `check({nv(S.p)}, {nv(S.q)})`：'
                    f'==只有两边都非空才递归==')
        return f'检查{side}儿子是否一致'
    return f


def cap_false(S, B, ret):
    ln = S.get('_line')
    side = '左' if ln == 19 else '右' if ln == 26 else None
    if side:
        ch = getattr(S.q, 'left' if side == '左' else 'right')
        if ch is not None:
            return f'{side}子树的 `check` 返回了 `False` → 节点 `{S.p.val}` 这一层也返回 `False`，==层层向上=='
        return f'q 的节点 `{S.q.val}` 没有{side}儿子 → 返回 `False`'
    return '发现不同 → 返回 `False`'


CONFIG = dict(
    num=100, title='相同的树', difficulty='Easy', category='二叉树',
    author='yiduobo', technique='递归 · 先判空再进 check',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def isSameTree(self, p, q):
        if not p:
            if not q:
                return True
            else:
                return False
        elif not q:
            return False
        else:
            return self.check(p, q)

    def check(self, p, q):
        if p.val != q.val:
            return False

        if p.left:
            if not q.left or not self.check(p.left, q.left):
                return False
        else:
            if q.left:
                return False

        if p.right:
            if not q.right or not self.check(p.right, q.right):
                return False
        else:
            if q.right:
                return False

        return True
''',
    call='''s = Solution()
s.P = Tr([1,2,3,None,4])
s.Q = Tr([1,2,3,None,4,5])
s.isSameTree(s.P, s.Q)''',
    expect=False,
    views=[
        dict(type='custom', draw=two_trees, h=330),
        dict(type='text', fn=lambda S: f"当前一对：`p = {nv(S['p'])}`  vs  `q = {nv(S['q'])}`", size=28, h=60),
        dict(type='calls', h=250),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink')],
    captions={
        'if not p:': track(lambda S, B, ret: f'入口：先处理空树。`p = {nv(S.p)}` 不为空'),
        'elif not q': track(lambda S, B, ret: f'`q = {nv(S.q)}` 也不为空 → 两棵都非空，交给 `check`'),
        'return self.check(p, q)': track('`check(p, q)` 的约定：==传进来的两个节点都不为空=='),
        'if p.val != q.val': track(cap_val),
        'if p.left:': track(cap_pl),
        'if not q.left or not self.check': track(cap_or('左')),
        'if q.left:': track(cap_ql),
        'if p.right:': track(cap_pr),
        'if not q.right or not self.check': track(cap_or('右')),
        'if q.right:': track(cap_qr),
        'return True': track(lambda S, B, ret: f'节点 `{S.p.val}` 的值、左子树、右子树都一致 → 这一对子树==相同==，返回 `True`'),
        'return False': track(cap_false),
    },
    cards=dict(
        one_liner='先比根的值，再分别检查左右儿子：一边有一边没有就不同',
        complexity='时间 `O(min(n,m))`，空间 `O(h)`（递归栈）',
        problem=['给你两棵二叉树的根节点 `p` 和 `q`，判断这两棵树是否相同',
                 '相同：==结构相同==，并且对应节点的==值相同==',
                 '示例：`p = [1,2]`，`q = [1,null,2]` → `false`'],
        quote='对于两棵树，可以先比较二者根节点的值是否相同，然后递归地比较左子树和右子树即可。过程中需要注意==判断左子树或者右子树为空的情况==。',
        quote_src='—— yiduobo 知乎题解',
        idea=['`isSameTree` 只负责处理空树的情况，两边都非空才进入 `check`',
              '`check`：值不同 → `False`；p 有某个儿子而 q 没有（或反过来）→ `False`',
              '两边都有这个儿子才递归 `check`，所以 ==check 永远碰不到空节点=='],
        result='返回 `False`：节点 3 在 p 里没有左儿子，在 q 里有左儿子 5 → ==结构不同==',
        summary=['时间 `O(min(n,m))`：一发现不同就层层返回 `False`',
                 '易错：p 没有某个儿子时，别忘了检查 q 是否有（`else: if q.left`）',
                 '对比灵神：他用 `return p is q` 在递归边界统一处理空节点，代码只有 3 行',
                 '原文为 Python 2 风格：删去了文档字符串和 TreeNode 注释，逻辑未改'],
    ),
)
