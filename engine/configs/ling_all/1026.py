CONFIG = dict(
    num=1026, title='节点与其祖先之间的最大差值', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='自顶向下 DFS · 维护路径最值',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1446'],
    code='''
class Solution:
    def maxAncestorDiff(self, root: Optional[TreeNode]) -> int:
        ans = 0
        def dfs(node: Optional[TreeNode], mn: int, mx: int) -> None:
            if node is None:
                nonlocal ans
                ans = max(ans, mx - mn)
                return
            mn = min(mn, node.val)
            mx = max(mx, node.val)
            dfs(node.left, mn, mx)
            dfs(node.right, mn, mx)
        dfs(root, root.val, root.val)
        return ans
''',
    call='''s = Solution()
s.tree = Tr([8,3,10,1,6,None,14])
s.maxAncestorDiff(s.tree)''',
    expect=7,
    views=[
        dict(type='text', fn=lambda S: (f"根到当前路径：最小 `mn = {S['_inner'].get('mn')}`，最大 `mx = {S['_inner'].get('mx')}`，差 `{S['_inner']['mx'] - S['_inner']['mn']}`　`ans = {S.get('ans')}`" if isinstance(S['_inner'].get('mn'), int) else ''), size=26, h=56),
        dict(type='tree', label='二叉树（蓝 = node）', pointers={'node': 'blue'}, h=300),
        dict(type='calls', h=250),
    ],
    watch=[('node', lambda S: (S['_inner'].get('node').val if S['_inner'].get('node') is not None else '空'), 'blue'),
           ('mn', lambda S: S['_inner'].get('mn'), 'cyan'), ('mx', lambda S: S['_inner'].get('mx'), 'pink'),
           ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 记录最大差值，先置 0',
        'dfs(root, root.val': '从根出发，`mn = mx = root.val = {root.val}`：路径上目前只有根',
        'if node is None': lambda S, B, r: ('走到空节点 → 一条根到叶的路径结束了，路径上的 `mn` / `mx` 已齐全' if B.node is None else f'节点 `{B.node.val}` 非空，继续往下'),
        'ans = max': '这条路径上任意两点的最大差 = `mx - mn` = `{mx} - {mn}` = {mx - mn}；`ans = max({B.ans}, {mx - mn})` = =={ans}==',
        'mn = min': '路径最小值：`min({B.mn}, {node.val})` = =={mn}==',
        'mx = max': '路径最大值：`max({B.mx}, {node.val})` = =={mx}==',
        'dfs(node.left': '带着 `mn = {mn}`、`mx = {mx}` 去左子树',
        'dfs(node.right': '带着 `mn = {mn}`、`mx = {mx}` 去右子树',
        'return ans': '所有路径都看完，最大差值 `ans` = =={ans}==',
    },
    skip=['nonlocal ans', 'return\n'],
    max_steps=110,
    cards=dict(
        one_liner='枚举下面的节点 B，路径上只需记录最小值和最大值',
        complexity='时间 `O(n)`，空间 `O(n)`（链状时的递归栈）',
        problem=['找不同节点 `A`、`B`，`A` 是 `B` 的祖先，使 `|A.val - B.val|` 最大',
                 '返回这个最大差值',
                 '示例：`[8,3,10,1,6,null,14]` → `|8 - 1| = 7`'],
        quote='无需记录路径中的全部节点值，只需记录路径中的最小节点值 mn 和最大节点值 mx。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举下面的节点 `B`：它的祖先就是从根到 `B` 的路径',
              'A 比 B 小时越小越好，比 B 大时越大越好 → 只要路径的 `mn` 和 `mx`',
              '优化：一条路径上任意两点的最大差就是 `mx - mn`，走到空节点时更新一次答案'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '「不同节点」的限制不影响结果：同一个点的差是 0',
                 '先更新 `mn`、`mx` 再往下传；空节点处才更新 `ans`',
                 '原文还有：每个节点都更新答案的写法，以及「归」方法（返回子树最值）'],
    ),
)
