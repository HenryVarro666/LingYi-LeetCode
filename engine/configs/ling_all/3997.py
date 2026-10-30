CONFIG = dict(
    num=3997, title='统计二叉树中支配节点的数量', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='自底向上 DFS',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1427'],
    code='''
class Solution:
    def countDominantNodes(self, root: TreeNode | None) -> int:
        # dfs(node) 返回 node 子树中的最大节点值
        def dfs(node: TreeNode | None) -> int:
            if node is None:
                return 0
            mx = max(dfs(node.left), dfs(node.right), node.val)
            if node.val == mx:
                # node.val 是 node 子树中的最大节点值
                nonlocal ans
                ans += 1
            return mx

        ans = 0
        dfs(root)
        return ans
''',
    call='Solution().countDominantNodes(Tr([5,3,8,2,4,7,1]))',
    expect=5,
    views=[
        dict(type='tree', label='完全二叉树（蓝 = 当前 node）', pointers={'node': 'blue'}, h=330),
        dict(type='text', fn=lambda S: f"支配节点计数 `ans = {S['ans']}`" if 'ans' in S else '', size=28, h=60),
        dict(type='calls', h=210),
    ],
    watch=[('node', lambda S: S['_inner'].get('node') and S['_inner']['node'].val, 'blue'),
           ('mx', lambda S: S['_inner'].get('mx'), 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'if node is None': lambda S, B, r: ('空节点 → 没有任何值，这是==递归边界==' if S.node is None
                                           else f'节点 `{S.node.val}` 非空 → 先去问左右子树的最大值'),
        'return 0': '空子树返回 `0`；题目保证 `val >= 1`，所以不会影响 `max`',
        'mx = max': '子树最大值 `mx = max(左, 右, {node.val}) = {mx}`',
        'if node.val == mx': lambda S, B, r: (f'`{S.node.val} == {S.mx}` → 自己就是子树最大值，==是支配节点=='
                                              if S.node.val == S.mx else
                                              f'`{S.node.val} != {S.mx}` → 子树里有更大的值，不是支配节点'),
        'ans += 1': '支配节点 +1：`ans = {B.ans} + 1 = {ans}`',
        'return mx': '把子树最大值 `{ret}` 交给父节点去比较',
        'ans = 0': '`ans` 统计支配节点的个数',
        'dfs(root)': '自底向上：从根出发，先递归到叶子再逐层返回',
    },
    skip=['nonlocal ans'],
    cards=dict(
        one_liner='后序遍历：子树最大值等于自己，就是支配节点',
        complexity='时间 `O(n)`，空间 `O(log n)`（完全二叉树深度 `log n`）',
        problem=['节点值等于其子树所有值的 ==最大值==，称为支配节点',
                 '给一棵完全二叉树，返回支配节点的数量',
                 '示例：`root = [5,3,8,2,4,7,1]` → `5`（四个叶子和 `8`）'],
        quote='写一个自底向上的 DFS，递归函数返回当前子树的最大节点值。如果当前节点值等于当前子树的最大节点值，那么答案加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(node)` 返回 `node` 子树的最大值',
              '先拿到左右子树最大值，再和自己的值取 `max`',
              '`node.val == mx` 说明没有更大的后代 → 答案加一'],
        summary=['时间 `O(n)`，每个节点只访问一次；空间 `O(log n)`，完全二叉树深度为 `log n`',
                 '空节点返回 `0` 是安全的，因为 `1 <= val`',
                 '叶子节点一定是支配节点，因为子树只有它自己',
                 '同类题：二叉树自底向上收集子树信息（2265、543、124 等）'],
    ),
)
