VALS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]


def _levels(S):
    """uid -> (层号, 层序下标)"""
    root = S.get('root')
    out, q, d, pos = {}, [root] if root else [], 0, 0
    while q:
        for nd in q:
            out[nd._uid] = (d, pos)
            pos += 1
        q = [c for nd in q for c in (nd.left, nd.right) if c]
        d += 1
    return out


def _color(S, node):
    info = _levels(S).get(node._uid)
    if info is None:
        return None
    d, pos = info
    if node.val != VALS[pos]:
        return 'green'                       # 已经换过值
    return 'purple' if d % 2 == 1 else None  # 奇数层、还没换


def _v(x):
    return '空' if x is None else str(x.val)


def _cap_none(S, B, ret):
    if B.node1 is None:
        return '`node1` 是空节点：已经越过叶子 → 直接返回'
    return f'`node1 = {B.node1.val}`、`node2 = {B.node2.val}` 都非空，继续'


def _cap_swap(S, B, ret):
    if B.is_odd_level:
        return (f'==奇数层==：交换两个节点的值 `{B.node1.val}` ↔ `{B.node2.val}`'
                f'（只换值，不动树的结构）')
    return f'偶数层：`{B.node1.val}`、`{B.node2.val}` 不用换'


def _cap_outer(S, B, ret):
    n1, n2 = B.node1.left, B.node2.right
    if n1 is None:
        return '外侧配对：`node1.left`、`node2.right` 都为空（越过叶子）→ 进去立刻 `return`'
    return f'外侧配对：`node1.left = {n1.val}` 与 `node2.right = {n2.val}` 在下一层==镜像对称==，一起递归'


def _cap_inner(S, B, ret):
    n1, n2 = B.node1.right, B.node2.left
    if n1 is None:
        return '内侧配对：`node1.right`、`node2.left` 也都为空 → 立刻 `return`，这一对处理完毕'
    return f'内侧配对：`node1.right = {n1.val}` 与 `node2.left = {n2.val}`，同样镜像对称'


CONFIG = dict(
    num=2415, title='反转二叉树的奇数层', difficulty='Medium', category='二叉树',
    author='灵茶山艾府', technique='DFS 同时递归左右子树 · 交换值',
    tags=['字节30天'],
    code='''
class Solution:
    def reverseOddLevels(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        def dfs(node1: Optional[TreeNode], node2: Optional[TreeNode], is_odd_level: bool) -> None:
            if node1 is None: return
            if is_odd_level: node1.val, node2.val = node2.val, node1.val
            dfs(node1.left, node2.right, not is_odd_level)
            dfs(node1.right, node2.left, not is_odd_level)
        dfs(root.left, root.right, True)
        return root
''',
    call=f'Solution().reverseOddLevels(Tr({VALS}))',
    result_fn=tree_list,
    expect=[1, 3, 2, 4, 5, 6, 7, 15, 14, 13, 12, 11, 10, 9, 8],
    views=[
        dict(type='tree', label='二叉树（紫 = 奇数层待交换，绿 = 已交换）', h=430,
             pointers={'node1': 'blue', 'node2': 'pink'}, color=_color),
        dict(type='calls', h=200, label='递归调用栈'),
    ],
    watch=[('node1.val', 'node1.val', 'blue'), ('node2.val', 'node2.val', 'pink'), ('is_odd_level', 'is_odd_level')],
    captions={
        'dfs(root.left, root.right, True)': '第 0 层只有根，不用动；从第 1 层（==奇数层==）的左右孩子开始==成对==递归',
        'if node1 is None': _cap_none,
        'if is_odd_level': _cap_swap,
        'dfs(node1.left, node2.right': _cap_outer,
        'dfs(node1.right, node2.left': _cap_inner,
        'return root': '每一对镜像位置都处理过了，返回原来的根',
    },
    skip=[4],   # `if node1 is None: return`：空节点的返回已在调用字幕里说明
    max_steps=60,
    cards=dict(
        one_liner='同时递归一对镜像节点，奇数层就交换它们的值',
        complexity='时间 `O(n)`，空间 `O(log n)`（完美二叉树的高度）',
        problem=['给一棵==完美==二叉树，把每个==奇数层==（根为第 0 层）的节点值反转',
                 '例如某层是 `[2,1,3,4,7,11,29,18]`，反转后是 `[18,29,11,7,4,3,1,2]`',
                 '示例：`[2,3,5,8,13,21,34]` → `[2,5,3,8,13,21,34]`'],
        quote='依然是交换值的思路，==通过同时递归左右子树实现==。不了解这一做法的同学可以做做 101. 对称二叉树。',
        quote_src='—— 灵茶山艾府题解（方法二：DFS）',
        idea=['反转一层 = 这一层==镜像位置==上的两个节点交换值',
              '镜像对：`(node1.left, node2.right)` 和 `(node1.right, node2.left)`，和 101 题一模一样',
              '递归时带上 `is_odd_level`，每下一层取反；奇数层就交换'],
        summary=['时间 `O(n)`，空间 `O(log n)`：完美二叉树高度是 `log n`',
                 '只交换 `val`，不改指针，所以递归时树的结构始终不变',
                 '完美二叉树保证 `node1`、`node2` 同时为空，只判 `node1` 就够',
                 '方法一 BFS：逐层收集节点，奇数层首尾对换值'],
    ),
)
