def _pre(S):
    v = S.get('pre')
    return '-∞' if v is None or v == float('-inf') else str(v)


def _ans(S):
    v = S.get('ans')
    return '∞' if v is None or v == float('inf') else str(v)


CONFIG = dict(
    num=783, title='二叉搜索树节点最小距离', difficulty='Easy', category='二叉树与回溯',
    author='灵茶山艾府', technique='中序遍历 · 相邻差最小',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution:
    def minDiffInBST(self, root: Optional[TreeNode]) -> int:
        ans = inf
        pre = -inf

        def dfs(node: Optional[TreeNode]) -> None:
            if node is None:
                return
            dfs(node.left)
            nonlocal ans, pre
            ans = min(ans, node.val - pre)
            pre = node.val
            dfs(node.right)

        dfs(root)
        return ans
''',
    call='Solution().minDiffInBST(Tr([4,2,6,1,3]))',
    expect=1,
    views=[
        dict(type='tree', label='BST（黄圈 = 当前递归路径）', pointers={'node': 'blue'}, h=330),
        dict(type='text', h=60, fn=lambda S: f"中序遍历上一个值 `pre = {_pre(S)}`，当前最小差 `ans = {_ans(S)}`"),
        dict(type='calls', h=200),
    ],
    watch=[('node', lambda S: S['_inner'].get('node').val if S['_inner'].get('node') is not None else None, 'blue'),
           ('pre', lambda S: _pre(S), 'cyan'), ('ans', lambda S: _ans(S), 'green')],
    captions={
        'ans = inf': '`ans` 记录最小差值，初始为正无穷',
        'pre = -inf': '`pre` 是中序遍历中==上一个节点值==，初始为负无穷',
        'if node is None': lambda S, B, r: ('空节点 → 递归边界' if S['_inner'].get('node') is None else f"节点 `{S['_inner']['node'].val}` 非空 → 先递归左子树"),
        'return ans': '中序序列 `[1,2,3,4,6]` 的相邻差最小是 `{ans}`',
        'return': '空节点直接返回，回到上一层',
        'dfs(node.left)': lambda S, B, r: f"先走左子树（中序：左 → 根 → 右）",
        'ans = min': lambda S, B, r: f"相邻两数差：`{S['_inner']['node'].val} − ({B.pre if B.pre != float('-inf') else '-∞'})`，`ans = min(...) = {_ans(S)}`",
        'pre = node.val': '更新 `pre = {pre}`：给下一个节点当「前一个数」',
        'dfs(node.right)': '左子树和当前节点处理完，再走右子树',
        'dfs(root)': '从根开始中序遍历',
    },
    cards=dict(
        one_liner='BST 的中序遍历有序，最小差只会出在相邻两数之间',
        complexity='时间 `O(n)`，空间 `O(n)`（最坏退化成链）',
        problem=['给二叉搜索树的根 `root`，求任意两不同节点值之差的最小值',
                 '示例：`root = [4,2,6,1,3]` → `1`'],
        quote='最小差值一定是相邻两个数的差值。由于二叉搜索树的中序遍历得到的序列是有序的，我们可以计算中序遍历中的相邻两数的差值，取最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['数字排序后，最小差一定在相邻两数之间',
              'BST 中序遍历（左 → 根 → 右）天然有序，不用另外排序',
              '用 `pre` 记上一个节点值，到每个节点时更新 `ans`'],
        summary=['时间 `O(n)`；空间 `O(n)`，最坏退化成链',
                 '`pre` 初始 `-inf`，第一个节点的差是 `inf`，不会影响 `ans`',
                 '`nonlocal ans, pre` 别漏，否则赋值会变成局部变量',
                 '同类题：530、98 验证 BST（也是中序遍历 + pre）'],
    ),
)
