def _v(x):
    return 'None' if x is None else str(x.val)


def _is(a, b):
    return a is not None and b is not None and a._uid == b._uid


def _cap_if(S, B, ret):
    r = B['root']
    if r is None:
        return '`root` 是空节点 → 满足条件，返回它'
    if _is(r, B['p']):
        return f'`{r.val}` 就是 `p` → ==找到了，不再往下递归==，直接返回它（下面就算有 q，答案也是它）'
    if _is(r, B['q']):
        return f'`{r.val}` 就是 `q` → ==找到了，不再往下递归==，直接返回它'
    return f'`{r.val}` 不是空节点，也不是 `p`/`q` → 去左右子树里找'


def _cap_left(S, B, ret):
    kid = S.get('root')
    return f'递归 `{B["root"].val}` 的==左子树==' + ('（空）' if kid is None else f'（`{kid.val}`）')


def _cap_right(S, B, ret):
    kid = S.get('root')
    return (f'左子树返回 `{_v(B["left"])}`；再递归==右子树==' + ('（空）' if kid is None else f'（`{kid.val}`）'))


def _cap_both(S, B, ret):
    l, r = B['left'], B['right']
    if l is not None and r is not None:
        return f'`left = {l.val}`、`right = {r.val}`：p 和 q ==分别在左右两边== → 当前节点就是答案'
    return f'`left = {_v(l)}`、`right = {_v(r)}`：没有两边都找到'


def _cap_or(S, B, ret):
    l, r = B['left'], B['right']
    if l is None and r is None:
        return '左右子树都没找到 → 返回 `None`'
    side = '左' if l is not None else '右'
    if B['root'].val == 3:  # 最外层
        return f'只有{side}子树找到了 → 返回 `{_v(ret)}`。这是最外层，候选项就是==最终答案=='
    return f'只有{side}子树找到了 → 把{side}边的返回值 `{_v(ret)}` 往上交（它是 LCA 的==候选项==）'


CONFIG = dict(
    num=236, title='二叉树的最近公共祖先', difficulty='Medium', category='二叉树',
    author='灵茶山艾府', technique='递归：返回最近公共祖先的候选项',
    code='''
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if root in (None, p, q):  # 找到 p 或 q 就不往下递归了，原因见上面答疑
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:  # 左右都找到
            return root  # 当前节点是最近公共祖先
        # 如果只有左子树找到，就返回左子树的返回值
        # 如果只有右子树找到，就返回右子树的返回值
        # 如果左右子树都没有找到，就返回 None（注意此时 right = None）
        return left or right
''',
    call='''root = Tr([3,5,1,6,2,None,None,None,None,None,4])
p = root.left.left
q = root.left.right.right
Solution().lowestCommonAncestor(root, p, q)''',
    result_fn=lambda x: x.val,
    expect=5,
    views=[
        dict(type='tree', h=420, pointers={'root': 'blue', 'p': 'green', 'q': 'pink'},
             color=lambda S, n: 'green' if _is(n, S.get('p')) else ('pink' if _is(n, S.get('q')) else None)),
        dict(type='calls', h=200),
    ],
    watch=[('root', 'root', 'blue'), ('left', 'left', 'cyan'), ('right', 'right', 'purple')],
    captions={
        'if root in (None, p, q)': _cap_if,
        'return root  #': '`{root.val}` ==就是最近公共祖先==：再往上，p 和 q 都在同一侧子树里',
        'return root': lambda S, B, ret: ('返回 `None`：这棵空子树里什么也没找到' if ret is None else f'返回 `{ret.val}`，告诉上一层「这边找到了 `{ret.val}`」'),
        'left = self.': _cap_left,
        'right = self.': _cap_right,
        'if left and right': _cap_both,
        'return left or right': _cap_or,
    },
    max_steps=60,
    cards=dict(
        one_liner='左右子树各找到一个，当前节点就是答案；只找到一个就往上交',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给定二叉树和其中两个节点 `p`、`q`，找它们的==最近公共祖先==（LCA）',
                 'LCA：是 p、q 的祖先且深度尽量大；==一个节点也可以是它自己的祖先==',
                 '示例：`root = [3,5,1,6,2,null,null,null,null,null,4]`',
                 '`p = 6`，`q = 4` → 最近公共祖先是 `5`'],
        quote='返回值的准确含义是「==最近公共祖先的候选项==」…在递归过程中，返回值可能是最近公共祖先，也可能是空节点、节点 p 或者节点 q。',
        quote_src='—— 灵茶山艾府题解答疑',
        idea=['当前节点是空、`p` 或 `q` → 直接返回它：下面就算还有另一个，答案也是它',
              '左右子树==都==返回非空 → p、q 分居两侧，当前节点就是 LCA',
              '只有一边非空 → 返回那一边；都为空 → 返回 `None`'],
        summary=['时间 `O(n)`，空间 `O(n)`（最坏是一条链的递归栈）',
                 '为什么找到 p 就不往下了？下面有 q → 答案就是 p；下面没有 → 也不用找了',
                 '返回值不一定是 LCA，而是「候选项」：可能是 p、q 或 None',
                 '易错：题目保证 p、q 都在树中，否则这个写法会把单独的 p 当成答案'],
    ),
)
