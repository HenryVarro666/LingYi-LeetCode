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
    num='LCR 194', title='二叉树的最近公共祖先', difficulty='Easy', category='二叉树与回溯',
    author='灵茶山艾府', technique='递归：返回最近公共祖先的候选项',
    tags=[],
    code='''
class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        if root in (None, p, q):
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:
            return root
        return left or right
''',
    call='''root = Tr([3,5,1,6,2,0,8,None,None,7,4])
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
        4: lambda S, B, ret: ('返回 `None`：这棵空子树里什么也没找到' if ret is None else f'返回 `{ret.val}`，告诉上一层「这边找到了 `{ret.val}`」'),
        'left = self.': _cap_left,
        'right = self.': _cap_right,
        'if left and right': _cap_both,
        8: '`{root.val}` ==就是最近公共祖先==：p、q 分居它的左右两边',
        'return left or right': _cap_or,
    },
    max_steps=80,
    cards=dict(
        one_liner='左右都找到，我就是答案；只找到一边，就把那边的结果往上交',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给定二叉树和其中两个节点 `p`、`q`，找它们的==最近公共祖先==',
                 '祖先：深度尽量大；==一个节点也可以是它自己的祖先==',
                 '示例：`root = [3,5,1,6,2,0,8,null,null,7,4]`，`p = 5, q = 1 → 3`；`p = 5, q = 4 → 5`',
                 '本视频：`p = 6`，`q = 4` → `5`'],
        quote='晕递归的同学请先看「深刻理解递归」。空间复杂度：O(n)。最坏情况下，二叉树是一条链，因此递归需要 O(n) 的栈空间。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`root in (None, p, q)`：碰到空、`p`、`q` 就直接返回它，不再往下',
              '递归左右子树，得到 `left`、`right`',
              '==两边都非空== → p、q 分居两侧，当前节点是答案',
              '只有一边非空 → 返回那一边；都为空 → 返回 `None`'],
        summary=['时间 `O(n)`，空间 `O(n)`（最坏是一条链的递归栈）',
                 '返回值是「候选项」：可能是 p、q、LCA 或 `None`',
                 '`left or right`：一边为 `None` 时自然取另一边',
                 '易错：依赖题目保证 p、q 都在树中',
                 '对比 LCR 193：BST 有大小关系，只需往一边走'],
    ),
)
