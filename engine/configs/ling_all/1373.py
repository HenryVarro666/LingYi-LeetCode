def _f(x):
    return '∞' if x == float('inf') else '-∞' if x == float('-inf') else str(x)


def _info(S):
    I = S['_inner']
    if 'node' not in I or I['node'] is None:
        return '每棵子树返回三元组 `(最小值, 最大值, 节点和)`，不是 BST 就返回 `(-∞, ∞, 0)`'
    parts = []
    if 'l_min' in I:
        parts.append(f"左 `({_f(I['l_min'])}, {_f(I['l_max'])}, {I['l_sum']})`")
    if 'r_min' in I:
        parts.append(f"右 `({_f(I['r_min'])}, {_f(I['r_max'])}, {I['r_sum']})`")
    head = f"节点 `{I['node'].val}`：" + '　'.join(parts) if parts else f"节点 `{I['node'].val}`：先递归左右子树"
    return head + f"　最大和 `ans = {S.get('ans', 0)}`"


def _bad(S, B, ret):
    x = S['x']
    if x <= S['l_max']:
        return f'`{x} <= l_max = {_f(S["l_max"])}`：左子树有不小于它的值 → ==不是 BST==，返回 `(-∞, ∞, 0)`'
    return f'`{x} >= r_min = {_f(S["r_min"])}`：右子树有不大于它的值 → ==不是 BST==，返回 `(-∞, ∞, 0)`'


def _chk(S, B, ret):
    x = S.x
    ok = not (x <= S.l_max or x >= S.r_min)
    return (f'`x = {x}`，`l_max = {_f(S.l_max)}`，`r_min = {_f(S.r_min)}`：'
            + ('`l_max < x < r_min` → ==是 BST==' if ok else '不满足 `l_max < x < r_min` → ==不是 BST=='))


CONFIG = dict(
    num=1373, title='二叉搜索子树的最大键值和', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='后序遍历 · 返回 (min, max, sum)',
    tags=['灵神题单', '链表树与回溯', '难度分 1914'],
    code='''
class Solution:
    def maxSumBST(self, root: Optional[TreeNode]) -> int:
        ans = 0  # 二叉搜索树可以为空

        def dfs(node: Optional[TreeNode]) -> Tuple:
            if node is None:
                return inf, -inf, 0

            l_min, l_max, l_sum = dfs(node.left)  # 递归左子树
            r_min, r_max, r_sum = dfs(node.right)  # 递归右子树
            x = node.val
            if x <= l_max or x >= r_min:  # 不是二叉搜索树
                return -inf, inf, 0

            s = l_sum + r_sum + x  # 这棵子树的所有节点值之和
            nonlocal ans
            ans = max(ans, s)

            return min(l_min, x), max(r_max, x), s

        dfs(root)
        return ans
''',
    call='Solution().maxSumBST(Tr([5,6,8,2,None,7,9]))',
    expect=24,
    views=[
        dict(type='text', fn=_info, size=24, h=64),
        dict(type='tree', label='二叉树（蓝 = 当前节点，黄圈 = 递归路径）', pointers={'node': 'blue'}, h=360),
        dict(type='calls', h=230),
    ],
    watch=[('node', lambda S: getattr(S['_inner'].get('node'), 'val', None), 'blue'),
           ('x', lambda S: S['_inner'].get('x'), 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans = 0`：==二叉搜索树可以为空==，所以答案至少是 0（全是负数时返回 0）',
        'if node is None': lambda S, B, r: ('空节点：当作空 BST → 返回 `(∞, -∞, 0)`，这样父节点的比较自然成立'
                                         if S.node is None else f'来到节点 `{S.node.val}`'),
        'return inf, -inf, 0': '空节点 = 空 BST，返回 `(∞, -∞, 0)`：空树的 `min = ∞`、`max = -∞`、和为 0：任何 `x` 都满足 `x > -∞` 且 `x < ∞`',
        'dfs(node.left)': '先递归左子树，拿回 `(l_min, l_max, l_sum)`',
        'dfs(node.right)': '再递归右子树，拿回 `(r_min, r_max, r_sum)`',
        'x = node.val': '当前节点值 `x = {x}`',
        'if x <= l_max': _chk,
        'return -inf, inf, 0': _bad,
        's = l_sum': '这棵子树是 BST：`s = {l_sum} + {r_sum} + {x} =` =={s}==',
        'ans = max': '`ans = max({B.ans}, {s}) =` =={ans}==：每棵 BST 子树都来更新一次答案',
        'return min(l_min': '返回 `(min, max, 和) = ({min(l_min, x)}, {max(r_max, x)}, {s})`，父节点据此判断自己是不是 BST',
        'dfs(root)': '从根开始后序遍历',
        'return ans': '所有节点都访问过，最大键值和 `{ans}`',
    },
    skip=['nonlocal ans', 'if node is None', 'x = node.val'],
    max_steps=110,
    cards=dict(
        one_liner='后序遍历：每棵子树返回 (最小值, 最大值, 和)，不是 BST 就返回 (-∞, ∞, 0)',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给你一棵二叉树，求其中==任意二叉搜索子树==的最大键值和',
                 'BST：左子树都小于当前值，右子树都大于当前值，且左右子树也是 BST',
                 '示例 1：`[1,4,3,2,4,2,5,null,null,null,null,null,null,4,6]` → `20`',
                 '本视频：`[5,6,8,2,null,7,9]` → `24`（子树 8 的和 `8+7+9`）'],
        quote='如果左子树的最大值 ≥ 当前节点值，或者右子树的最小值 ≤ 当前节点值，都不符合二叉搜索树的定义，那么当前这棵子树不是二叉搜索树。此时可以返回 -∞, ∞, 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['后序遍历：先拿到左右子树的 `(min, max, sum)`，再判断当前节点',
              '不是 BST 就返回 `(-∞, ∞, 0)`：父节点再比较时 `x <= l_max` 或 `x >= r_min` 必然成立，==自动传染变成非 BST==',
              '是 BST 就用 `l_sum + r_sum + x` 更新答案，并把 `(min, max, 和)` 交给父节点'],
        summary=['时间 `O(n)`；空间 `O(n)`（链状树时递归栈最深 n 层）',
                 '易错：左子树不是 BST 也==不能提前返回==，答案可能在右子树里（如示例 1 的节点 3；本视频里根 5 不是 BST，答案在右子树 8）',
                 '`ans` 初始为 0：空树也算 BST；`nonlocal` 才能在内层函数里更新它',
                 '前置题：98. 验证二叉搜索树（同样用后序遍历实现）'],
    ),
)
