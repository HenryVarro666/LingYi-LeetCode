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
        if record and S.root is not None:
            DONE[S.root._uid] = S.mx <= S.root.val
        for n in _walk(S.get('self.tree')):
            n._g = DONE.get(n._uid)
        return fn(S, B, ret) if callable(fn) else fn
    return cap


def _fmt(x):
    return '-inf' if x == -inf else str(x)


def _txt(S):
    I = S.get('_inner', {})
    r = I.get('root')
    if r is None or 'mx' not in I:
        return '`mx`：从根到当前节点之前，路径上的最大值'
    return f'节点 `{r.val}`：路径最大值 `mx = {_fmt(I["mx"])}`，`{_fmt(I["mx"])} <= {r.val}` 吗？ ==' + ('好节点' if I['mx'] <= r.val else '不是好节点') + '=='


def cap_if(S, B, ret):
    if S.root is None:
        return '空节点，没有好节点 → 递归边界，返回 `0`'
    return f'进入节点 `{S.root.val}`，从根走到这里的最大值 `mx = {_fmt(S.mx)}`'


def cap_l(S, B, ret):
    return f'左子树：带着 `max(mx, {S.root.val}) = {_fmt(max(S.mx, S.root.val))}` 往下，拿到左边好节点数 `left = {S.left}`' if 'left' in S else f'递归左子树，把路径最大值更新为 `max({_fmt(S.mx)}, {S.root.val}) = {_fmt(max(S.mx, S.root.val))}` 传下去'


def cap_ret(S, B, ret):
    good = S.mx <= S.root.val
    why = f'`{_fmt(S.mx)} <= {S.root.val}` ==成立，自己是好节点==，+1' if good else f'`{_fmt(S.mx)} <= {S.root.val}` 不成立（路径上有更大的值），自己不算'
    return f'节点 `{S.root.val}`：{why} → `{S.left} + {S.right} + {int(good)} = {ret}`'


CONFIG = dict(
    num=1448, title='统计二叉树中好节点的数目', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='自顶向下 DFS · 携带路径最大值',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1360'],
    code='''
class Solution:
    def goodNodes(self, root: TreeNode, mx=-inf) -> int:
        if root is None:
            return 0
        left = self.goodNodes(root.left, max(mx, root.val))
        right = self.goodNodes(root.right, max(mx, root.val))
        return left + right + (mx <= root.val)
''',
    call='''s = Solution()
s.tree = Tr([3,1,4,3,None,1,5])
s.goodNodes(s.tree)''',
    expect=4,
    views=[
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='tree', label='二叉树（绿 = 好节点，粉 = 不是好节点）', pointers={'root': 'blue'}, h=330,
             color=lambda S, n: 'green' if getattr(n, '_g', None) is True else ('pink' if getattr(n, '_g', None) is False else None)),
        dict(type='calls', h=250),
    ],
    watch=[('root', 'root', 'blue'), ('mx', lambda S: S['_inner'].get('mx'), 'orange'),
           ('left', lambda S: S['_inner'].get('left')), ('right', lambda S: S['_inner'].get('right'))],
    captions={
        'if root is None': track(lambda S, B, r: cap_if(S, B, r), record=True),
        'return 0': track('空节点 → 好节点数 `0`，返回给上一层'),
        'left = self': track(lambda S, B, r: f'递归左子树，把路径最大值 `max(mx, root.val) = {_fmt(S.mx)}` 传下去'),
        'right = self': track(lambda S, B, r: f'左子树算完，再递归右子树，同样传下去 `max(mx, root.val) = {_fmt(S.mx)}`'),
        'return left + right': track(cap_ret),
    },
    cards=dict(
        one_liner='往下递归时带一个 mx：到当前节点之前路径上的最大值',
        complexity='时间 `O(n)`，空间 `O(n)`（最坏退化成链）',
        problem=['二叉树里「好节点」X：从根到 X 的路径上，没有任何节点的值大于 X',
                 '统计好节点的个数，根节点一定是好节点',
                 '示例：`[3,1,4,3,null,1,5]` → `4`'],
        quote='我们可以在向下递归的同时，额外维护一个参数 mx 表示从根节点到当前节点之前，==路径上的最大节点值==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`mx` 初始为 `-inf`：根前面什么都没有，所以根一定是好节点',
              '递归左右子树时，把 `max(mx, root.val)` 传下去',
              '`mx <= root.val` 就是好节点，返回 `左 + 右 + 1`，否则 `左 + 右`'],
        result='运行结束，返回 `4`：好节点是 `3`、`4`、`3`（根的左边那条路上的第二个 3）、`5`',
        summary=['时间 `O(n)`：每个节点递归一次；空间 `O(n)`：最坏是链',
                 '易错：比较用 `mx <= root.val`（相等也算好节点），不要写成 `<`',
                 '`mx` 要在递归==之前==用当前节点更新，传给儿子的是包含自己的最大值',
                 '空节点返回 `0`；`(mx <= root.val)` 是布尔值，直接参与加法']),
)
