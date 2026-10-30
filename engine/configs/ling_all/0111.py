VALS = [1, 2, 3, 4, 5, None, 6, 7]


def _v(x):
    return '空' if x is None else str(x.val)


def _info(S):
    a = S.get('ans')
    if a is None:
        return '自顶向下：把路径上的节点数 `cnt` ==往下传==，到叶子时更新答案'
    cnt = S['_inner'].get('cnt')
    a = '∞' if a == float('inf') else a
    if cnt is None:
        return f'当前最小深度 `ans = {a}`'
    return f'路径节点数 `cnt = {cnt}`，当前最小深度 `ans = {a}`'


def _if(S, B, ret):
    if S.node is None:
        return '空节点：不是叶子，什么也不做，返回'
    return f'来到节点 `{S.node.val}`'


def _cnt(S, B, ret):
    return f'`{S.node.val}` 加入路径：`cnt = {B.cnt} + 1 = {S.cnt}`'


def _prune(S, B, ret):
    a = '∞' if S.ans == float('inf') else S.ans
    if S.cnt >= S.ans:
        return f'`cnt = {S.cnt} ≥ ans = {a}`：再往下走只会更深，不可能让 ans 变小 → =={"剪枝"}=='
    return f'`cnt = {S.cnt} < ans = {a}`：还有希望更新答案，继续'


def _leaf(S, B, ret):
    n = S.node
    if n.left is None and n.right is None:
        return f'`{n.val}` 是==叶子==：找到一条根到叶子的路径，长 `{S.cnt}`'
    return f'`{n.val}` 不是叶子，继续往下递归'


def _ans(S, B, ret):
    return f'因为 `cnt < ans` 才走到这里，直接 `ans = {S.ans}`（不用再取 min）'


CONFIG = dict(
    num=111, title='二叉树的最小深度', difficulty='Easy', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='自顶向下 DFS · 最优性剪枝',
    tags=['labuladong', '灵神核心路线'],
    code='''
class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        ans = inf
        def dfs(node: Optional[TreeNode], cnt: int) -> None:
            if node is None:
                return
            nonlocal ans
            cnt += 1
            if cnt >= ans:
                return  # 最优性剪枝
            if node.left is None and node.right is None:  # node 是叶子
                ans = cnt
                return
            dfs(node.left, cnt)
            dfs(node.right, cnt)
        dfs(root, 0)
        return ans if root else 0
''',
    call=f'Solution().minDepth(Tr({VALS}))',
    expect=3,
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='tree', label='二叉树（蓝 = 当前节点，黄圈 = 递归路径）', pointers={'node': 'blue'}, h=380),
        dict(type='calls', h=210),
    ],
    watch=[('node', lambda S: getattr(S['_inner'].get('node'), 'val', None), 'blue'),
           ('cnt', lambda S: S['_inner'].get('cnt'), 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = inf': '`ans` 初始为 `inf`，后面在叶子处取最小',
        'dfs(root, 0)': '从根开始，递归前路径上还没有节点：`cnt = 0`',
        'if node is None': _if,
        'cnt += 1': _cnt,
        'if cnt >= ans': _prune,
        'return  # 最优性剪枝': '剪枝：这棵子树里不会有更浅的叶子，直接返回',
        'if node.left is None and node.right is None': _leaf,
        'ans = cnt': _ans,
        13: '叶子没有儿子，返回',
        'dfs(node.left, cnt)': lambda S, B, r: f'把 `cnt = {B.cnt}` 带到左儿子 `{_v(B.node.left)}`',
        'dfs(node.right, cnt)': lambda S, B, r: f'左边搜完，把 `cnt = {B.cnt}` 带到右儿子 `{_v(B.node.right)}`',
        'return ans if root': '`root` 非空，返回 `ans = {ret}`',
    },
    skip=[6, 'nonlocal ans'],
    cards=dict(
        one_liner='带着路径长度往下走，到叶子更新答案，走不出更优就剪枝',
        complexity='时间 `O(n)`，空间 `O(n)`（最坏退化成链）',
        problem=['求二叉树的最小深度：根到==最近叶子==的路径上的节点数',
                 '叶子 = 没有子节点的节点',
                 '示例：`[3,9,20,null,null,15,7]` → `2`；本视频：`[1,2,3,4,5,null,6,7]` → `3`'],
        quote='如果递归中发现 `cnt ≥ ans`，由于继续向下递归也不会让 ans 变小，直接返回。这一技巧叫做==「最优性剪枝」==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['DFS 时额外传入 `cnt`：路径上的节点个数，每往下一层加一',
              '走到叶子，用 `cnt` 更新答案',
              '剪枝后能走到叶子说明 `cnt < ans`，所以直接 `ans = cnt`'],
        result='运行结束：最近的叶子是 `5`（或 `6`），最小深度 `3`；节点 `6` 被剪枝',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：只有==叶子==才能更新答案，单侧为空的节点不是叶子',
                 '空树要返回 `0`，所以最后是 `ans if root else 0`',
                 '方法二「自底向上」：`min(左, 右) + 1`，但某侧为空时只能取另一侧'],
    ),
)
