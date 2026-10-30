def nv(x):
    return '空' if x is None else str(x.val)


def cap_left(S, B, ret):
    r = S.root
    if r.left is None:
        return f'节点 `{r.val}` 没有左儿子 → 左边什么都不用插'
    if r.left.val == -1:
        return f'节点 `{r.val}` 的左边已插入 `-1`，原左子树 `{nv(r.left.left)}` 挂在它的 `left` 下'
    return (f'节点 `{r.val}` 有左儿子 `{r.left.val}` → 先递归把左子树扩展好，'
            f'==再在中间插一个 `-1`== 当新的左儿子')


def cap_right(S, B, ret):
    r = S.root
    if r.right is None:
        extra = '；左边的 `-1` 已经插好' if r.left is not None and r.left.val == -1 else ''
        return f'节点 `{r.val}` 没有右儿子 → 右边不用插{extra}'
    if r.right.val == -1:
        return f'节点 `{r.val}` 的右边已插入 `-1`，原右子树 `{nv(r.right.right)}` 挂在它的 `right` 下'
    return (f'节点 `{r.val}` 有右儿子 `{r.right.val}` → 同理：递归右子树，'
            f'新建 `-1` 挂在右边，原右子树接到它的 `right`')


CONFIG = dict(
    num='LCP 67', title='装饰树', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='递归（后序）· 子树先扩展再接线',
    tags=['灵神核心路线', '灵神题单·链表树与回溯'],
    code='''
class Solution:
    def expandBinaryTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if root.left: root.left = TreeNode(-1, left=self.expandBinaryTree(root.left))
        if root.right: root.right = TreeNode(-1, right=self.expandBinaryTree(root.right))
        return root
''',
    call='''s = Solution()
s.tree = Tr([7,5,6,3])
s.expandBinaryTree(s.tree)''',
    expect=[7, -1, -1, 5, None, None, 6, -1, None, None, None, 3],
    result_fn=tree_list,
    views=[
        dict(type='tree', label='二叉树（绿 = 新插入的 -1 灯饰）', pointers={'root': 'blue'}, h=400,
             color=lambda S, n: 'green' if n.val == -1 else None),
        dict(type='calls', h=200),
    ],
    watch=[('root', 'root', 'blue'), ('root.left', lambda S: nv(S['_inner'].get('root').left) if S['_inner'].get('root') else None),
           ('root.right', lambda S: nv(S['_inner'].get('root').right) if S['_inner'].get('root') else None)],
    captions={
        'if root.left': cap_left,
        'if root.right': cap_right,
        'return root': '节点 `{root.val}` 的左右子树都扩展完 → 返回 `root` 给上一层接线',
    },
    cards=dict(
        one_liner='先递归扩展子树，再在父子之间塞一个 `-1`',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈，h 为树高）',
        problem=['在二叉树每对父子之间插入一个值为 `-1` 的节点',
                 '左儿子之间的 `-1` 作为左儿子，右儿子之间的作为右儿子',
                 '示例：`[7,5,6]` → `[7,-1,-1,5,null,null,6]`'],
        quote='if root.left: root.left = TreeNode(-1, left=self.expandBinaryTree(root.left))',
        quote_src='—— 灵茶山艾府题解（一行代码）',
        idea=['`expandBinaryTree(root)` 返回扩展好的子树根，就是 `root` 本身',
              '有左儿子：新建 `-1`，它的 `left` 指向递归扩展好的左子树',
              '右边同理，`-1` 的 `right` 指向扩展后的右子树'],
        result='运行结束，每对父子之间都多了一个 `-1`',
        summary=['时间 `O(n)`：每个节点访问一次；空间 `O(h)`',
                 '易错：`-1` 在左边要用 `left=`，在右边要用 `right=`，位置不能错',
                 '没有儿子就不插，叶子本身不变',
                 '题解是后序写法：先递归得到扩展后的子树，再挂到新节点上'],
    ),
)
