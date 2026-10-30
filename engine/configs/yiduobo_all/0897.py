CONFIG = dict(
    num=897, title='递增顺序搜索树', difficulty='Easy', category='二叉树与回溯',
    author='yiduobo', technique='中序遍历 + 新建右链', tags=[],
    code='''
class Solution(object):
    def increasingBST(self, root):

        self.ans = TreeNode(0)
        p_root = self.ans
        self.dfs(root)
        return p_root.right

    def dfs(self, now):
        if now.left:
            self.dfs(now.left)
        self.ans.right = TreeNode(now.val)
        self.ans = self.ans.right
        if now.right:
            self.dfs(now.right)
''',
    call='Solution().increasingBST(Tr([5,3,6,2,4,None,8]))',
    expect=[2, None, 3, None, 4, None, 5, None, 6, None, 8],
    result_fn=tree_list,
    views=[
        dict(type='tree', var='root', label='原树（蓝 = now）', pointers={'now': 'blue'}, h=230),
        dict(type='tree', var='p_root', label='答案（p_root 是哑节点 0，右链越长越多）', pointers={'self.ans': 'pink'}, h=260),
        dict(type='calls', h=170),
    ],
    watch=[('now', 'now.val', 'blue'), ('ans', 'self.ans.val', 'pink')],
    captions={
        'self.ans = TreeNode(0)': '`self.ans` 是答案链最右的节点，先放一个哑节点 `0`',
        'p_root = self.ans': '`p_root` 记住哑节点，最后返回它的右儿子',
        'self.dfs(root)': '中序遍历原树：左 - 根 - 右',
        'return p_root.right': '哑节点的右儿子就是答案的根（最小值）',
        'if now.left': lambda S, B, r: (f'`{S.now.val}` 有左儿子 `{S.now.left.val}` → 先递归左边' if S.now.left else f'`{S.now.val}` 没有左儿子 → 轮到自己'),
        'self.dfs(now.left)': '进入左子树',
        'self.ans.right = TreeNode': '新建值为 `{now.val}` 的节点，接在答案链末尾',
        'self.ans = self.ans.right': '`self.ans` 后移到新节点 `{now.val}`',
        'if now.right': lambda S, B, r: (f'`{S.now.val}` 有右儿子 `{S.now.right.val}` → 递归右边' if S.now.right else f'`{S.now.val}` 没有右儿子 → 返回上一层'),
        'self.dfs(now.right)': '进入右子树',
    },
    cards=dict(
        one_liner='中序遍历时，把每个值依次新建节点接到右链末尾',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给你一棵二叉搜索树，按==中序遍历==重新排列', '使树中最左节点成为根，且每个节点没有左儿子、只有一个右儿子',
                 '本视频：`[5,3,6,2,4,null,8]` → `2→3→4→5→6→8`'],
        quote='使用一个变量p表示当前答案中最右侧的节点，然后对原树执行中序遍历，设目前执行到节点now，根据中序遍历左-根-右的顺序……',
        quote_src='—— yiduobo 题解原文',
        idea=['`self.ans` 始终指向答案链的最右节点', '中序：先左子树，再新建 `now.val` 的节点挂到 `self.ans.right`，最后右子树', '哑节点 `p_root` 让第一个节点不用特判'],
        summary=['时间 `O(n)`，空间 `O(n)`（新建了 n 个节点）',
                 '新建节点而不是改原树，避免改指针时丢失子树',
                 '最后返回 `p_root.right`，不是哑节点本身',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
