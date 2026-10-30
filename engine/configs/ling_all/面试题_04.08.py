def _v(x):
    return 'None' if x is None else str(x.val)


def _is(a, b):
    return a is not None and b is not None and a._uid == b._uid


def cap_if(S, B, ret):
    r = B['root']
    if r is None:
        return '空节点：这边什么都没有 → 返回 `None`'
    if _is(r, B['p']):
        return f'`{r.val}` 就是 `p` → ==不用再往下==，直接把它交上去'
    if _is(r, B['q']):
        return f'`{r.val}` 就是 `q` → ==不用再往下==，直接把它交上去'
    return f'`{r.val}` 既不是空也不是 `p`/`q` → 到左右子树里各找一遍'


def cap_left(S, B, ret):
    kid = S.get('root')
    return f'先在==左子树==里找（`{_v(kid)}`）'


def cap_right(S, B, ret):
    kid = S.get('root')
    return f'左边交上来 `{_v(B["left"])}`；再去==右子树==找（`{_v(kid)}`）'


def cap_both(S, B, ret):
    l, r = B['left'], B['right']
    if l and r:
        return f'`left = {l.val}`、`right = {r.val}` 都非空：p、q ==分在两边== → 当前节点 `{B["root"].val}` 是首个共同祖先'
    return f'`left = {_v(l)}`、`right = {_v(r)}`：没有同时在两边找到'


def cap_ret(S, B, ret):
    l, r = B['left'], B['right']
    if l is None and r is None:
        return '两边都没找到 → 返回 `None`'
    side = '左' if l else '右'
    return f'只有{side}边找到了 `{_v(ret)}` → 原样往上交：p、q 要么都在这一边，要么另一个就是它的后代'


CONFIG = dict(
    num='面试题 04.08', title='首个共同祖先', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='递归：左右各找一个', tags=[],
    code='''
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if root in (None, p, q):
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:
            return root
        return left if left else right
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
        dict(type='calls', h=200, hide=('lowestCommonAncestor',)),
    ],
    watch=[('root', lambda S: S['_inner'].get('root') and S['_inner']['root'].val, 'blue'),
           ('left', lambda S: _v(S['_inner']['left']) if 'left' in S['_inner'] else None, 'cyan'),
           ('right', lambda S: _v(S['_inner']['right']) if 'right' in S['_inner'] else None, 'purple')],
    captions={
        'if root in (None, p, q)': cap_if,
        'return root': lambda S, B, ret: ('返回 `None`' if ret is None else
                                           f'返回 `{ret.val}`：告诉上一层「这边找到了 `{ret.val}`」'),
        'left = self.': cap_left,
        'right = self.': cap_right,
        'if left and right': cap_both,
        'return left if left else right': cap_ret,
    },
    max_steps=70,
    cards=dict(
        one_liner='p、q 分居左右两边的那个节点，就是首个共同祖先',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['在二叉树里找 `p`、`q` 两个节点的第一个共同祖先',
                 '节点值唯一，`p`、`q` 一定在树中；==节点可以是自己的祖先==',
                 '示例：`[3,5,1,6,2,0,8,null,null,7,4]`',
                 '`p = 5, q = 1` → `3`；`p = 5, q = 4` → `5`',
                 '本视频用 `p = 6, q = 4` → `5`'],
        quote='if root in (None, p, q): return root',
        quote_src='—— 灵茶山艾府题解代码（本题题解只有代码）',
        idea=['遇到空、`p`、`q` 就停：直接把当前节点往上交',
              '左右子树==都==交上来非空：p、q 分在两边，当前节点就是答案',
              '只有一边非空：把那一边的结果继续往上交；都空返回 `None`'],
        result='根 `3` 左边交上 `5`、右边交上 `None` → 返回 `5`',
        summary=['时间 `O(n)`，空间 `O(n)`（最坏是一条链的递归栈）',
                 '返回值不是「一定是祖先」，而是「这棵子树里找到的 p/q 或它们的祖先」',
                 '`p` 是 `q` 的祖先时，在 `p` 处就返回，不会再往下找 `q`，答案正好是 `p`',
                 '易错：题目保证 p、q 都存在，否则这个写法会把单个 p 当成答案'],
    ),
)
