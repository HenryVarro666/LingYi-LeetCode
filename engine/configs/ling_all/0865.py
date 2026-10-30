CONFIG = dict(
    num=865, title='具有所有最深节点的最小子树', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='自底向上递归 · 返回高度和 lca',
    tags=['灵神题单', '链表树与回溯', '难度分 1534'],
    code='''
class Solution:
    def subtreeWithAllDeepest(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        def dfs(node: Optional[TreeNode]) -> Tuple[int, Optional[TreeNode]]:
            if node is None:
                return 0, None

            left_height, left_lca = dfs(node.left)
            right_height, right_lca = dfs(node.right)

            if left_height > right_height:  # 左子树更高
                return left_height + 1, left_lca
            if left_height < right_height:  # 右子树更高
                return right_height + 1, right_lca
            return left_height + 1, node  # 一样高

        return dfs(root)[1]
''',
    call='Solution().subtreeWithAllDeepest(Tr([3,5,1,6,2,0,None,None,None,7,4]))',
    expect=[2, 7, 4],
    result_fn=tree_list,
    views=[
        dict(type='text', fn=lambda S: (f"当前节点 `{S['_inner']['node'].val}`：左高 `{S['_inner'].get('left_height','?')}`，右高 `{S['_inner'].get('right_height','?')}`" if S['_inner'].get('node') is not None else '空节点：高度 0，没有 lca') if 'node' in S['_inner'] else '', size=26, h=56),
        dict(type='tree', label='二叉树（蓝 = node，黄圈 = 递归路径）', pointers={'node': 'blue'}, h=340),
        dict(type='calls', h=260, hide=('root',)),
    ],
    watch=[('node', lambda S: S['_inner'].get('node').val if S['_inner'].get('node') else None, 'blue'),
           ('left_height', lambda S: S['_inner'].get('left_height'), 'cyan'),
           ('right_height', lambda S: S['_inner'].get('right_height'), 'orange')],
    captions={
        'return 0, None': '空节点：高度 `0`，lca 为 None',
        'left_height, left_lca = dfs': '递：先算左子树，归回来拿到 `left_height = {left_height}`，`left_lca = {left_lca.val if left_lca else None}`',
        'right_height, right_lca = dfs': '再算右子树：`right_height = {right_height}`，`right_lca = {right_lca.val if right_lca else None}`',
        'if left_height > right_height': '`{left_height} > {right_height}`？' + '{"左边更高 → 最深叶子只在左子树" if left_height > right_height else "不是左边更高"}',
        'if left_height < right_height': '`{left_height} < {right_height}`？' + '{"右边更高 → 最深叶子只在右子树" if left_height < right_height else "不是右边更高"}',
        'return left_height + 1, left_lca': '左边更高：高度 `{left_height}+1`，lca 沿用左子树的 `{left_lca.val}`',
        'return right_height + 1, right_lca': '右边更高：高度 `{right_height}+1`，lca 沿用右子树的 `{right_lca.val}`',
        'return left_height + 1, node': lambda S, B, r: (f'`{S.node.val}` 是叶子（左右都空，一样高）→ lca 是它自己，高度 1' if S.left_height == 0 else f'==一样高==：最深叶子分居两侧 → 最近公共祖先就是 `{S.node.val}`，高度 `{S.left_height}+1`'),
        'return dfs(root)[1]': '取返回值的第二项，就是答案：节点 `{ret.val}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='左右一样高，当前节点就是所有最深叶子的最近公共祖先',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['找包含树中==所有最深节点==的最小子树，返回它的根',
                 '最深 = 到根的距离最大',
                 '本视频：`[3,5,1,6,2,0,null,null,null,7,4]`',
                 '最深节点是 `7, 4`，答案是节点 `2`'],
        quote='如果 leftHeight = rightHeight，那么子树的高度为 leftHeight + 1，==lca 就是 node==。反证法：lca 在左子树中，那么 lca 不是右子树的最深叶结点的祖先，这不对。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['把每棵子树当子问题：需要知道==高度==和==最深叶子的 lca==',
              '左高：高度取左 +1，lca 取左子树的；右高同理',
              '一样高：左右各有最深叶子，lca 只能是当前节点'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '方法一：全局 `max_depth` + 递时传深度；左右深度都等于全局最大时更新答案，后面可能被更深的覆盖',
                 '方法二无需全局变量，高度是叶子在==子树内==的深度',
                 '与 1123 题完全相同；前置题 236 最近公共祖先'],
    ),
)
