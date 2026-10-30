VALS = [4, 2, 6, 1, 3, 5, 7]
SUF = [0]  # 处理了 k 个节点后 s 的值（按原值从大到小）
for _v in sorted(VALS, reverse=True):
    SUF.append(SUF[-1] + _v)


def _inorder(root):
    out, st, cur = [], [], root
    while st or cur:
        while cur:
            st.append(cur)
            cur = cur.left
        cur = st.pop()
        out.append(cur)
        cur = cur.right
    return out


def _done(S):
    """已经被替换成「更大和」的节点 uid 集合：中序遍历的最后 k 个"""
    root, s = S.get('root'), S.get('s', 0)
    if root is None:
        return set()
    k = SUF.index(s) if s in SUF else 0
    order = _inorder(root)
    return {n._uid for n in order[len(order) - k:]} if k else set()


def _color(S, n):
    if n._uid in _done(S):
        return 'green'
    return None


def _info(S):
    if 's' not in S:
        return '遍历顺序：==右子树 → 根 → 左子树==（从大到小访问）'
    return f"已访问节点之和 `s = {S['s']}`：都是 ==≥ 下一个要访问的节点== 的值"


def _v(x):
    return '空' if x is None else str(x.val)


def _if(S, B, ret):
    if S.node is None:
        return '空节点 → 递归边界，直接返回'
    return f'节点 `{S.node.val}` 非空 → 先把比它大的右子树全部处理完'


def _right(S, B, ret):
    if B.node.right is None:
        return f'`{B.node.val}` 没有右子树 → 没有比它更大的待加节点'
    return f'从 `{B.node.val}` 递归右子树 `{_v(B.node.right)}`：右边的值都比 `{B.node.val}` 大，==必须先加进 s=='


def _add(S, B, ret):
    return f'右子树已处理完，`s = {B.s} + {S.node.val} = =={S.s}==`'


def _set(S, B, ret):
    return f'`s` 正好是所有 ==≥ {B.node.val}== 的节点值之和 → 节点改成 `{S.node.val}`'


def _left(S, B, ret):
    if B.node.left is None:
        return '没有左子树，这个节点处理完毕，返回上一层'
    return f'再递归左子树 `{_v(B.node.left)}`：左边的值都更小，它们需要的 s ==已经包含了当前节点=='


CONFIG = dict(
    num=1038, title='从二叉搜索树到更大和树', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='反向中序遍历 · 累加和',
    tags=['labuladong', '灵神题单·链表树与回溯'],
    code='''
class Solution:
    def bstToGst(self, root: TreeNode) -> TreeNode:
        s = 0
        def dfs(node: TreeNode) -> None:
            if node is None:
                return
            dfs(node.right)  # 递归右子树
            # 递归结束后，s 就等于右子树的所有节点值之和
            nonlocal s
            s += node.val
            node.val = s  # 此时 s 就是 >= node.val 的所有数之和
            dfs(node.left)  # 递归左子树
        dfs(root)
        return root
''',
    call=f'Solution().bstToGst(Tr({VALS}))',
    result_fn=tree_list,
    expect=[22, 27, 13, 28, 25, 18, 7],
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='tree', label='BST（绿 = 已替换成更大和）', pointers={'node': 'blue'}, color=_color, h=380),
        dict(type='calls', h=220),
    ],
    watch=[('node', lambda S: getattr(S['_inner'].get('node'), 'val', None), 'blue'),
           ('s', 's', 'green')],
    captions={
        's = 0': '`s` 记录已访问节点值之和，初始为 `0`',
        'dfs(root)': '从根节点开始递归',
        'if node is None': _if,
        'dfs(node.right)': _right,
        's += node.val': _add,
        'node.val = s': _set,
        'dfs(node.left)': _left,
        'return root': '每个节点都替换完毕，返回 `root`',
    },
    skip=[6],
    max_steps=70,
    cards=dict(
        one_liner='右 → 根 → 左遍历，边走边累加，s 就是答案',
        complexity='时间 `O(n)`，空间 `O(n)`（最坏退化成链）',
        problem=['给一棵 BST，把每个节点的值换成树中 ==≥ 该节点值== 的所有节点值之和',
                 '示例：`[4,1,6,0,2,5,7,null,null,null,3,null,null,null,8]` → 根变成 `30`',
                 '本视频：`[4,2,6,1,3,5,7]` → `[22,27,13,28,25,18,7]`'],
        quote='为了算出节点值之和，==必须先访问所有节点值大于当前节点值的节点==。……这样就确定了递归的顺序：右子树-根-左子树。',
        quote_src='—— 灵茶山艾府题解',
        idea=['BST 右子树都比根大：先把右子树处理完，`s` 就是右子树之和',
              '再加上根自己，`s` 就是所有 `≥ node.val` 的和，直接赋给 `node.val`',
              '最后递归左子树：它需要的“更大的数”都已在 `s` 里'],
        result='运行结束：反向中序依次得到 `7, 13, 18, 22, 25, 27, 28`',
        summary=['时间 `O(n)`：每个节点访问一次；空间 `O(n)`：递归栈（树不一定平衡）',
                 '顺序是 ==右 → 根 → 左==，即反向中序遍历',
                 '易错：`s` 要跨递归共享，Python 里需要 `nonlocal s`',
                 '先 `s += node.val` 再赋值，因为题目要的是 ≥（包含自己）',
                 '与 538 题完全相同'],
    ),
)
