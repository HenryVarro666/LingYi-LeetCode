CONFIG = dict(
    num=156, title='上下翻转二叉树', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='递归 · 先翻转左子树再接线',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def upsideDownBinaryTree(self, root):

        if not root:
            return None
        
        if not root.left:
            return root
        
        res = self.upsideDownBinaryTree(root.left)
        root.left.right = root
        root.left.left = root.right
        root.left = root.right = None
        return res
''',
    call='Solution().upsideDownBinaryTree(Tr([1,2,3,4,5]))',
    expect=[4, 5, 2, None, None, 3, 1],
    result_fn=tree_list,
    views=[
        dict(type='tree', label='二叉树（蓝 = root）', pointers={'root': 'blue'}, h=330),
        dict(type='text', fn=lambda S: f"本层返回的新树根 `res = {S['res'].val}`" if S['_inner'].get('res') is not None else '', size=26, h=56),
        dict(type='calls', h=170),
    ],
    watch=[('root', lambda S: S['_inner']['root'].val if S['_inner'].get('root') else None, 'blue'),
           ('res', lambda S: S['_inner']['res'].val if S['_inner'].get('res') else None, 'green')],
    captions={
        4: lambda S, B, r: '`root` 非空，继续' if S.root else '空树直接返回 `None`',
        7: lambda S, B, r: (f'`{S.root.val}` 没有左孩子 → 它是最左侧节点，==就是新的树根==，原样返回' if not S.root.left else f'`{S.root.val}` 有左孩子 `{S.root.left.val}` → 先翻转左子树'),
        'res = self.upsideDownBinaryTree': '左子树翻转完成，最左节点 `res = {res.val}` 一路传上来：它是最终的新根',
        'root.left.right = root': '左孩子 `{root.left.val}` 的右孩子改成 `{root.val}`（原根变成右孩子）',
        'root.left.left = root.right': lambda S, B, r: (f'左孩子 `{S.root.left.val}` 的左孩子改成原右孩子 `{S.root.right.val}`' if S.root.right else f'`{S.root.val}` 没有右孩子 → 左孩子的左孩子为空'),
        'root.left = root.right = None': '切断 `{root.val}` 原来的左右指针，避免成环：它现在是叶子',
        'return res': '返回新树根 `{res.val}`',
    },
    skip=[],
    cards=dict(
        one_liner='最左侧节点是新根，回溯时把每个根接到它左孩子的右边',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['给你一棵二叉树，==原来的左孩子变成新的根==，原来的根变成它的右孩子，原来的右孩子变成它的左孩子',
                 '题目保证右节点要么是叶子，要么为空，且逐层向上翻转',
                 '本视频：`root = [1,2,3,4,5]` → `[4,5,2,null,null,3,1]`'],
        quote='需要注意的是，题目要求返回新的树根，这很明显就是原树中最左侧的节点，那么就可以在递归求解时一层一层往上回传这个最左侧的节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['翻转规则：`now.left` 当新根，`now` 变成它的右孩子，`now.right` 变成它的左孩子',
              '`now.right` 是孤立的，所以先递归把左子树翻转好，再做这一层的接线',
              '递归到没有左孩子的节点即最左节点，它就是答案，每层原样返回'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '接线顺序：先改 `root.left` 的右、左孩子，最后再清空 `root.left`，顺序反了会丢指针',
                 '最后一行必须断开 `root.left`、`root.right`，否则新树里有环',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行'],
    ),
)
