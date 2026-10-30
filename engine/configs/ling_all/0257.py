VALS = [1, 2, 3, None, 5, 6]


def _v(x):
    return '空' if x is None else str(x.val)


def _info(S):
    return '回溯：`path` 是 DFS 外的变量，==进来时 append，离开时 pop=='


def _if(S, B, ret):
    if S.node is None:
        return '空节点 → 什么也不做，返回'
    return f'来到节点 `{S.node.val}`'


def _leaf(S, B, ret):
    n = S.node
    if n.left is None and n.right is None:
        return f'`{n.val}` 是==叶子==：`path` 就是一条从根到叶子的完整路径'
    return f'`{n.val}` 不是叶子 → 继续递归左右子树'


CONFIG = dict(
    num=257, title='二叉树的所有路径', difficulty='Easy', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='回溯 · 路径为外部变量',
    tags=['labuladong', '灵神题单·链表树与回溯'],
    code='''
class Solution:
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        ans = []
        path = []

        def dfs(node: Optional[TreeNode]) -> None:
            if node is None:
                return
            path.append(str(node.val))
            if node.left is None and node.right is None:  # 叶子节点
                ans.append("->".join(path))
            else:
                dfs(node.left)
                dfs(node.right)
            path.pop()  # 恢复现场，撤销上面的 path.append(str(node.val))

        dfs(root)
        return ans
''',
    call=f'Solution().binaryTreePaths(Tr({VALS}))',
    expect=['1->2->5', '1->3->6'],
    views=[
        dict(type='text', fn=_info, size=26, h=56),
        dict(type='tree', label='二叉树（蓝 = 当前节点，黄圈 = 递归路径）', pointers={'node': 'blue'}, h=300),
        dict(type='array', var='path', label='path（当前路径，外部变量）', cell=80, h=120),
        dict(type='text', fn=lambda S: f"答案 `ans = {S['ans']}`" if 'ans' in S else '', size=24, h=50),
        dict(type='calls', h=210),
    ],
    watch=[('node', lambda S: getattr(S['_inner'].get('node'), 'val', None), 'blue')],
    captions={
        'ans = []': '`ans` 收集所有路径',
        'path = []': '`path` 放在 DFS ==外面==：所有递归共用同一个列表',
        'if node is None': _if,
        9: '`{node.val}` 加到路径末尾 → `{path}`',
        'if node.left is None and node.right is None': _leaf,
        'ans.append': '用 `"->"` 连起来，加入答案：==`{ans[-1]}`==',
        'dfs(node.left)': lambda S, B, r: f'先递归左子树 `{_v(B.node.left)}`',
        'dfs(node.right)': lambda S, B, r: f'左子树搜完，再递归右子树 `{_v(B.node.right)}`',
        15: lambda S, B, r: f'`{B.path[-1]}` 的子树处理完了 → ==恢复现场==，弹出它：`path = {S.path}`',
        'dfs(root)': '从根节点开始递归',
        'return ans': '返回所有路径 `{ret}`',
    },
    skip=[8],
    cards=dict(
        one_liner='进入节点时加入路径，离开时弹出，叶子处记录答案',
        complexity='时间 `O(n^2 log U)`，空间 `O(n log U)`（不计答案）',
        problem=['给你二叉树的根 `root`，按任意顺序返回所有==从根到叶子==的路径',
                 '示例：`root = [1,2,3,null,5]` → `["1->2->5","1->3"]`',
                 '本视频：`[1,2,3,null,5,6]` → `["1->2->5","1->3->6"]`'],
        quote='递归完了左子树，就要==倒回去==，递归右子树。倒回去的过程中，之前加到 path 中的数据（在左子树中）是垃圾数据，要及时清除掉（==恢复现场==）。',
        quote_src='—— 灵茶山艾府题解 · 方法二',
        idea=['`path` 声明在 DFS 外，所有递归共享',
              '进入节点：`append`；到叶子：`"->".join(path)` 加入答案',
              '离开节点前：`pop`，让 `path` 回到进入前的样子'],
        summary=['时间 `O(n^2 log U)`：最坏 `O(n)` 条路径、每条长 `O(n log U)`',
                 '易错：叶子也要 `pop`，所以 `pop` 写在 if/else 之后',
                 '方法一：把字符串 `path` 当参数传下去，天然不用恢复现场',
                 '同类：113 路径总和 II、回溯模板'],
    ),
)
