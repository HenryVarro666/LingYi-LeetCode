K0 = 3
INORDER = [1, 2, 3, 4, 5, 6]  # BST 的中序遍历 = 节点值从小到大


def _seen(S):
    """已经按中序访问过的节点个数 = 初始 k − 当前 k"""
    k = S.get('k', K0)
    return K0 - k if isinstance(k, int) else 0


def _cap_left(S, B, ret):
    me = B['node'].val
    kid = S.get('node')
    tail = f'（左儿子是 `{kid.val}`）' if kid is not None else '（左边是空节点）'
    return f'中序第一步 ==左==：先去 `{me}` 的左子树里找{tail}'


def _cap_check_left(S, B, ret):
    r = S['left_res']
    if r != -1:
        return f'左子树返回 `{r}` ≠ `-1` → ==答案在左子树里==，直接往上交，右边不用看了'
    return f'左子树返回 `-1`：左边没找到 → 轮到当前节点 `{S["node"].val}`'


def _cap_k(S, B, ret):
    return (f'中序 ==根==：访问 `{S["node"].val}`，它是第 `{_seen(S)}` 小的数，'
            f'`k` 从 {B["k"]} 减到 =={S["k"]}==')


def _cap_k0(S, B, ret):
    if S['k'] == 0:
        return f'`k == 0`：==当前节点就是第 {K0} 小==，答案是 `{S["node"].val}`'
    return f'`k = {S["k"]}`，还没数到第 {K0} 个 → 答案不在这里，去右子树找'


def _cap_right(S, B, ret):
    me = B['node'].val
    kid = S.get('node')
    tail = f'`{kid.val}`' if kid is not None else '空节点'
    return f'中序 ==右==：去 `{me}` 的右子树（{tail}）。右边找到就返回答案，找不到返回 `-1`，==直接把它的结果交上去=='


CONFIG = dict(
    num=230, title='二叉搜索树中第 K 小的元素', difficulty='Medium', category='二叉树',
    author='灵茶山艾府', technique='中序遍历 + 提前返回',
    code='''
class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        def dfs(node: Optional[TreeNode]) -> int:
            if node is None:
                return -1  # 题目保证节点值非负，用 -1 表示没有找到
            left_res = dfs(node.left)
            if left_res != -1:  # 答案在左子树中
                return left_res
            nonlocal k
            k -= 1
            if k == 0:  # 答案就是当前节点
                return node.val
            return dfs(node.right)  # 右子树会返回答案或者 -1
        return dfs(root)
''',
    call='Solution().kthSmallest(Tr([5,3,6,2,4,None,None,1]), 3)',
    expect=3,
    views=[
        dict(type='array', var=lambda S: INORDER, label='中序遍历序列（BST → 从小到大，绿 = 已数过）', cell=60,
             color=lambda S, i, v: ('orange' if i == K0 - 1 and _seen(S) == K0 else 'green') if i < _seen(S) else None),
        dict(type='tree', pointers={'node': 'blue'}, h=400,
             color=lambda S, n: ('orange' if n.val == INORDER[K0 - 1] and _seen(S) == K0 else 'green') if n.val in INORDER[:_seen(S)] else None),
        dict(type='calls', h=170),
    ],
    watch=[('k', 'k', 'pink'), 'node', ('left_res', 'left_res', 'cyan')],
    captions={
        'if node is None': lambda S, B, ret: ('`node` 是空节点 → 这里什么都没有' if B['node'] is None
                                              else f'`node = {B["node"].val}` 不是空节点，继续'),
        'return -1': '返回 `-1`：表示「没找到」。==节点值非负==，所以 -1 不会和答案混淆',
        'left_res = dfs': _cap_left,
        'if left_res != -1': _cap_check_left,
        'return left_res': '把左子树找到的答案 `{left_res}` 原样往上返回',
        'k -= 1': _cap_k,
        'if k == 0': _cap_k0,
        'return node.val': '返回答案 =={ret}==，它会沿着递归一层层原样传回去',
        'return dfs(node.right)': _cap_right,
        'return dfs(root)': '从根 `{root.val}` 开始中序遍历「左-根-右」，按从小到大的顺序数节点',
    },
    max_steps=60,
    cards=dict(
        one_liner='中序遍历就是从小到大遍历，数到第 k 个就是答案',
        complexity='时间 `O(n)`，空间 `O(h)`（h 为树高）',
        problem=['给一棵==二叉搜索树==的根 `root` 和整数 `k`，求第 `k` 小的节点值（k 从 1 开始）',
                 'BST：左子树的值 < 根 < 右子树的值',
                 '示例：`root = [5,3,6,2,4,null,null,1]`，`k = 3` → `3`'],
        quote='由于==中序遍历就是在从小到大遍历节点值==，所以遍历到的第 k 个节点值就是答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['「左-根-右」：每递归完左子树，就把 `k` 减一，表示==访问了一个节点==',
              '`k` 减到 0，当前节点就是答案；空节点返回 `-1` 表示没找到',
              '左子树返回的不是 `-1` → 答案在左边，==直接返回，不再往下遍历=='],
        summary=['时间 `O(n)`，空间 `O(h)`：递归栈深度等于树高，最坏是一条链',
                 '易错：`k` 是外层变量，`k -= 1` 前要写 `nonlocal k`',
                 '易错：必须先递归左子树、再减 `k`，顺序反了就不是从小到大',
                 '写法一：用外部变量 `ans` 记录答案；思考题：第 k 大 → 改成「右-根-左」'],
    ),
)
