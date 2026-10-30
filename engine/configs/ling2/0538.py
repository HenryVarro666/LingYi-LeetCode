TREE = [4, 1, 6, 0, 2, 5, 7]
LEVEL = [v for v in TREE if v is not None]          # Tr() 按层序给节点编号，uid 差 = 层序下标
DESC = sorted(LEVEL, reverse=True)                  # 反向中序 = 从大到小
CUM = [sum(DESC[:k + 1]) for k in range(len(DESC))]

CODE = '''
class Solution:
    def convertBST(self, root: TreeNode) -> TreeNode:
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
'''
_LINES = CODE.strip('\n').split('\n')
L_RET_NONE = [k + 1 for k, t in enumerate(_LINES) if t.strip() == 'return'][0]
L_SET = [k + 1 for k, t in enumerate(_LINES) if 'node.val = s' in t][0]


def _orig(S, nd):
    return LEVEL[nd._uid - S['root']._uid]


def _done_k(S):
    """已经改写成累加值的节点个数（按从大到小的顺序）"""
    s = S.get('s', 0)
    k = sum(1 for c in CUM if c <= s)
    if k and S.get('_line') != L_SET and S.get('_line') is not None:
        nd = S.get('node')
        # s 已经加上了当前节点，但 node.val = s 还没执行
        if nd is not None and S.get('_line') == L_SET - 1 and _orig(S, nd) == DESC[k - 1]:
            k -= 1
    return k


def _color(S, nd):
    if 'root' not in S:
        return None
    k = _done_k(S)
    return 'green' if _orig(S, nd) in DESC[:k] else None


def _s_cap(S, B, r):
    o = B.node.val
    return f'右子树都处理完了：`s = {B.s} + {o} = {S.s}`（右子树之和 + 自己）'


CONFIG = dict(
    num=538, title='把二叉搜索树转换为累加树', difficulty='Medium', category='二叉树',
    author='灵茶山艾府', technique='反向中序遍历（右 → 根 → 左）',
    tags=['热题173'],
    code=CODE,
    call=f'Solution().convertBST(Tr({TREE}))',
    result_fn=tree_list,
    expect=[22, 25, 13, 25, 24, 18, 7],
    skip=[L_RET_NONE],
    views=[
        dict(type='text', fn=lambda S: (f"`s = {S['s']}`：已经访问过的节点值之和（它们都 ==大于等于== 下一个要访问的节点）"
                                        if 's' in S else ''), h=60),
        dict(type='tree', label='BST（绿 = 已改成累加值）', h=360,
             pointers={'node': 'blue'}, color=_color),
        dict(type='array', var=lambda S: DESC, label='反向中序访问顺序 = 原值从大到小', cell=80, h=130,
             color=lambda S, i, v: 'green' if 'root' in S and i < _done_k(S) else None),
        dict(type='array', var=lambda S: [CUM[i] if 'root' in S and i < _done_k(S) else None for i in range(len(DESC))],
             label='对应的累加值 s', cell=80, h=130),
    ],
    watch=[('s', 's', 'green')],
    captions={
        's = 0': '`s`：累加和，按==从大到小==的顺序把节点值加进来',
        'if node is None': lambda S, B, r: ('空节点 → 返回' if B.node is None else f'到达节点 `{B.node.val}`'),
        'dfs(node.right)': lambda S, B, r: (f'先递归右子树：右边的值都 ==比 {B.node.val} 大==，要先加进 s' if B.node.right
                                            else f'先递归右子树（`{B.node.val}` 没有右儿子，马上返回）'),
        's += node.val': _s_cap,
        'node.val = s': '此时 s 就是==大于等于原值==的所有数之和 → `node.val = {s}`',
        'dfs(node.left)': lambda S, B, r: f'再递归左子树：左边的值都比它小，它们的累加值要包含 `{B.s}`',
        'dfs(root)': '从根开始，按「右 → 根 → 左」的顺序递归',
        'return root': '每个节点都改成了累加值，返回 `root`',
    },
    max_steps=70,
    cards=dict(
        result='累加树：`[22,25,13,25,24,18,7]` ✓ 与预期一致',
        one_liner='先右后左的中序遍历 = 从大到小访问，边走边累加',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['给二叉==搜索==树的根，节点值各不相同',
                 '把每个节点的值改成：==原值 + 所有比它大的节点值之和==',
                 '示例：`[3,2,4,1]` → `[7,9,4,10]`；`[1,0,2]` → `[3,3,2]`',
                 '本视频：`[4,1,6,0,2,5,7]` → `[22,25,13,25,24,18,7]`'],
        quote='为了算出节点值之和，==必须先访问所有节点值大于当前节点值的节点==。……这样就确定了递归的顺序：右子树-根-左子树。',
        quote_src='—— 灵茶山艾府题解：简洁写法，利用二叉搜索树的性质',
        idea=['BST 的右子树都比根大：要先把右子树遍历完',
              '右子树递归结束时，`s` = 右子树所有节点值之和',
              '`s += node.val` 后 `s` 就是 `>= node.val` 的所有数之和，直接替换'],
        summary=['时间 `O(n)`；空间 `O(n)`，树退化成链时递归栈最深',
                 '`s` 定义在外层，内层要写 `nonlocal s` 才能修改',
                 '易错：顺序是==右 → 根 → 左==，写成普通中序就变成「比它小的和」',
                 '同题：1038. 从二叉搜索树到更大和树'],
    ),
)
