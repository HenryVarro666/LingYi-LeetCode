CONFIG = dict(
    num=2265, title='统计值等于子树平均值的节点数', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='自底向上 DFS',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1473'],
    code='''
class Solution:
    def averageOfSubtree(self, root: TreeNode) -> int:
        ans = 0

        # 返回 node 子树的节点值之和、节点个数
        def dfs(node: TreeNode | None) -> tuple[int, int]:
            if node is None:
                return 0, 0
            left_sum, left_size = dfs(node.left)  # 拆解问题：递归计算左子树的信息
            right_sum, right_size = dfs(node.right)  # 拆解问题：递归计算右子树的信息
            sum_ = left_sum + right_sum + node.val  # node 子树的节点值之和
            size = left_size + right_size + 1  # node 子树的节点个数
            if node.val == sum_ // size:  # 题目要求下取整
                nonlocal ans
                ans += 1
            return sum_, size

        dfs(root)
        return ans
''',
    call='Solution().averageOfSubtree(Tr([4,8,5,0,1,None,6]))',
    expect=5,
    views=[
        dict(type='tree', label='二叉树（蓝 = 当前 node）', pointers={'node': 'blue'}, h=300),
        dict(type='text', fn=lambda S: (f"子树 `sum = {S['_inner']['sum_']}`，`size = {S['_inner']['size']}`，平均值 = ==" +
                                         f"{S['_inner']['sum_'] // S['_inner']['size']}==") if 'size' in S['_inner'] else '', size=26, h=56),
        dict(type='text', fn=lambda S: f"满足条件的节点数 `ans = {S['ans']}`" if 'ans' in S else '', size=26, h=56),
        dict(type='calls', h=210),
    ],
    watch=[('node', lambda S: S['_inner'].get('node') and S['_inner']['node'].val, 'blue'),
           ('sum_', lambda S: S['_inner'].get('sum_'), 'yellow'),
           ('size', lambda S: S['_inner'].get('size'), 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'if node is None': lambda S, B, r: ('空节点：和为 0、个数为 0，这是==递归边界==' if S.node is None
                                           else f'节点 `{S.node.val}` 非空 → 先递归求左右子树的信息'),
        'return 0, 0': '空子树 `(sum, size) = (0, 0)`，不影响上层累加',
        'left_sum, left_size': '左子树返回：节点值之和 `{left_sum}`，节点个数 `{left_size}`',
        'right_sum, right_size': '右子树返回：节点值之和 `{right_sum}`，节点个数 `{right_size}`',
        'sum_ =': '`sum_ = {left_sum} + {right_sum} + {node.val} = {sum_}`',
        'size =': '`size = {left_size} + {right_size} + 1 = {size}`（加 1 是自己）',
        'if node.val == sum_': lambda S, B, r: (f'平均值 `{S.sum_} // {S.size} = {S.sum_ // S.size}`，等于 `{S.node.val}` → ==满足=='
                                                if S.node.val == S.sum_ // S.size else
                                                f'平均值 `{S.sum_} // {S.size} = {S.sum_ // S.size}`，不等于 `{S.node.val}` → 不满足'),
        'ans += 1': '`ans = {B.ans} + 1 = {ans}`',
        'return sum_, size': '把 `(sum, size) = ({sum_}, {size})` 交给父节点',
        'ans = 0': '`ans` 统计满足条件的节点数',
    },
    skip=['nonlocal ans'],
    cards=dict(
        one_liner='子树要返回两个量：节点值之和、节点个数',
        complexity='时间 `O(n)`，空间 `O(h)`',
        problem=['找出节点值 ==等于其子树平均值== 的节点数',
                 '平均值 = 子树节点值之和 ÷ 节点个数，向下取整',
                 '示例：`root = [4,8,5,0,1,null,6]` → `5`'],
        quote='为了求出子树平均值，我们需要知道子树的节点值之和 sum，以及子树节点个数 size，那么子树平均值就是 floor(sum/size)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(node)` 返回 `(sum, size)`',
              '拆解问题：左右子树的信息交给递归',
              '合并：和 = 左 + 右 + 自己，个数 = 左 + 右 + 1',
              '`node.val == sum // size` 就把答案加一'],
        summary=['时间 `O(n)`，空间 `O(h)`，`h` 是树高',
                 '易错：平均值要向下取整，Python 里用 `//`',
                 '空节点返回 `(0, 0)`，省去判空分支',
                 '同类题：需要同时返回多个子树信息的自底向上递归'],
    ),
)
