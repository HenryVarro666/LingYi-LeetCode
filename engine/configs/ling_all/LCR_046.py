CONFIG = dict(
    num='LCR 046', title='二叉树的右视图', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='DFS · 先右后左，每层第一个遇到的节点',
    tags=[],
    code='''
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        ans = []
        def dfs(node: Optional[TreeNode], depth: int) -> None:
            if node is None: return
            if depth == len(ans):  # 这个深度首次遇到
                ans.append(node.val)
            dfs(node.right, depth + 1)  # 先递归右子树，保证首次遇到的一定是最右边的节点
            dfs(node.left, depth + 1)
        dfs(root, 0)
        return ans
''',
    call='Solution().rightSideView(Tr([1,2,3,4,None,None,5]))',
    expect=[1, 3, 5],
    views=[
        dict(type='tree', label='二叉树（黄圈 = 递归路径，蓝 = 当前节点）', pointers={'node': 'blue'}, h=340,
             color=lambda S, n: 'green' if n.val in S.get('ans', []) else None),
        dict(type='array', var='ans', label='ans（下标 = 深度，绿 = 各层看到的节点）', cell=80, h=120),
        dict(type='calls', h=230),
    ],
    watch=[('node', lambda S: S['_inner']['node'].val if S['_inner'].get('node') else None, 'blue'),
           ('depth', lambda S: S['_inner'].get('depth'), 'orange'), ('len(ans)', lambda S: len(S['ans']) if 'ans' in S else None, 'green')],
    captions={
        'ans = []': '`ans[d]` 存第 `d` 层看到的节点值',
        'if node is None': lambda S, B, r: ('空节点 → ==递归边界==，直接返回' if S.node is None else f'节点 `{S.node.val}` 非空，继续'),
        'if depth == len(ans)': lambda S, B, r: (
            f'`depth = {S.depth}` == `len(ans) = {len(S.ans)}`：这一层==第一次==有节点到访，而右子树先访问 → 它就是最右边的' if S.depth == len(S.ans)
            else f'`depth = {S.depth}` < `len(ans) = {len(S.ans)}`：这一层已有更靠右的节点，`{S.node.val}` 被挡住'),
        'ans.append': '节点 `{node.val}` 加入答案 → `{ans}`',
        'dfs(node.right': '==先==递归右子树，进入第 `{depth + 1}` 层',
        'dfs(node.left': '右子树走完，再递归左子树，进入第 `{depth + 1}` 层',
        'dfs(root, 0)': '从根节点、深度 `0` 开始',
        'return ans': '各层第一个到访的节点就是右视图 → `{ret}`',
    },
    skip=['def dfs'],
    cards=dict(
        one_liner='先走右子树：每层第一个到访的节点就是看得见的那个',
        complexity='时间 `O(n)`，空间 `O(n)`（最坏退化成链）',
        problem=['站在二叉树右侧，按从上到下的顺序返回能看到的节点值',
                 '示例：`[1,2,3,null,5,null,4]` → `[1,3,4]`',
                 '本视频：`[1,2,3,4,null,null,5]` → `[1,3,5]`'],
        quote='先递归右子树，保证首次遇到的一定是最右边的节点。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['`dfs(node, depth)` 带上深度；`ans` 的长度就是已经见过几层',
              '`depth == len(ans)` 说明这层还没记录 → 这个节点是该层首个到访者',
              '先右后左：每层先到访的必然是最右的节点，不需要再比较'],
        summary=['时间 `O(n)`，空间 `O(n)`：最坏退化成一条链，递归栈 `O(n)`',
                 '易错：先递归左子树的话，得到的是左视图',
                 '右视图看的是每层最右节点，不一定是右儿子（左子树更深时会露出左侧节点）',
                 '同类写法：BFS 取每层最后一个节点'],
    ),
)
