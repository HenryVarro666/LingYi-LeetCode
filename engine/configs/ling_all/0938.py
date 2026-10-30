CONFIG = dict(
    num=938, title='二叉搜索树的范围和', difficulty='Easy', category='二叉树与回溯',
    author='灵茶山艾府', technique='递归 · 利用 BST 剪枝',
    tags=['灵神题单', '链表树与回溯', '难度分 1335'],
    code='''
class Solution:
    def rangeSumBST(self, root: Optional[TreeNode], low: int, high: int) -> int:
        if root is None:
            return 0
        x = root.val
        if x > high:  # 右子树没有节点在范围内，只需递归左子树
            return self.rangeSumBST(root.left, low, high)
        if x < low:  # 左子树没有节点在范围内，只需递归右子树
            return self.rangeSumBST(root.right, low, high)
        return x + self.rangeSumBST(root.left, low, high) + \\
                   self.rangeSumBST(root.right, low, high)
''',
    call='''s = Solution()
s.tree = Tr([10,5,15,3,7,None,18])
s.rangeSumBST(s.tree, 7, 15)''',
    expect=32,
    views=[
        dict(type='text', h=50, fn=lambda S: '范围 `[low, high] = [7, 15]`，只有范围内的节点才累加'),
        dict(type='tree', label='BST（黄圈 = 当前递归路径）', pointers={'root': 'blue'}, h=340,
             color=lambda S, n: 'green' if 7 <= n.val <= 15 else None),
        dict(type='calls', h=210),
    ],
    watch=[('root', lambda S: S['_inner'].get('root').val if S['_inner'].get('root') is not None else None, 'blue'),
           ('x', lambda S: S['_inner'].get('x'), 'cyan')],
    captions={
        'if root is None': lambda S, B, r: ('空节点 → 没有值可加，==递归边界==' if S['_inner'].get('root') is None
                                            else f"节点 `{S['_inner']['root'].val}` 非空，继续判断它和范围的关系"),
        'return 0': '空节点贡献 `0`',
        'x = root.val': '当前节点值 `x = {x}`，范围 `[{low}, {high}]`',
        'if x > high': lambda S, B, r: (f"`{S.x} > {S.high}`：它和==右子树==全都比 high 大 → 只看左子树" if S.x > S.high
                                        else f"`{S.x} > {S.high}` 不成立 → 继续判断"),
        'if x < low': lambda S, B, r: (f"`{S.x} < {S.low}`：它和==左子树==全都比 low 小 → 只看右子树" if S.x < S.low
                                       else f"`{S.x} < {S.low}` 不成立 → `{S.x}` 在范围内"),
        'return self.rangeSumBST(root.left, low, high)': '只递归左子树，右子树整块剪掉',
        'return self.rangeSumBST(root.right, low, high)': '只递归右子树，左子树整块剪掉',
        'return x +': lambda S, B, r: (f"`{S.x}` 在范围内：`{S.x}` + 左子树和 + 右子树和 = =={r}==" if r is not None
                                       else f"`{S.x}` 在范围内：要加上 `{S.x}`，再分别递归左、右子树"),
    },
    cards=dict(
        one_liner='BST 的大小关系，让我们整棵子树地跳过',
        complexity='时间 `O(n)`，空间 `O(n)`（最坏退化成链）',
        problem=['给 BST 的根 `root` 和范围 `[low, high]`，求值在范围内的所有节点之和',
                 '示例：`root = [10,5,15,3,7,null,18], low = 7, high = 15` → `32`'],
        quote='如果 x>high，那么 x 不在范围内，并且根据二叉搜索树的性质，右子树的所有节点值都大于 x，从而大于 high，所以我们只需计算左子树的和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x > high`：右子树整块出界 → 只递归左子树',
              '`x < low`：左子树整块出界 → 只递归右子树',
              '否则 `x` 在范围内：`x` + 左子树和 + 右子树和'],
        summary=['时间 `O(n)`，空间 `O(n)`：BST 不保证平衡，最坏是一条链',
                 '写法二：先算 `s = x if low <= x <= high else 0`，再按 `x > low`、`x < high` 决定是否递归两边',
                 '灵神提示：这段代码其实就是线段树的 `query`',
                 '易错：三种情况的比较别写成 `>=`，边界值 `low`、`high` 本身要算进去'],
    ),
)
