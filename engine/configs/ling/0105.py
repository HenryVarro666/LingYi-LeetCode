PRE = [3, 9, 20, 15, 7]
INO = [9, 3, 15, 20, 7]
POS = {x: i for i, x in enumerate(INO)}


def _split(S):
    """当前 dfs 的 (pre_l, pre_r, in_l, left_size)；区间为空时返回 None"""
    pl, pr, il = S.get('pre_l'), S.get('pre_r'), S.get('in_l')
    if not isinstance(pl, int) or pl >= pr:
        return None
    return pl, pr, il, POS[PRE[pl]] - il


def _pre_color(S, i, v):
    sp = _split(S)
    if sp is None:
        return None
    pl, pr, il, ls = sp
    if i == pl:
        return 'orange'
    if pl < i <= pl + ls:
        return 'blue'
    if pl + ls < i < pr:
        return 'pink'
    return None


def _in_color(S, i, v):
    sp = _split(S)
    if sp is None:
        return None
    pl, pr, il, ls = sp
    if i == il + ls:
        return 'orange'
    if il <= i < il + ls:
        return 'blue'
    if il + ls < i < il + (pr - pl):
        return 'pink'
    return None


def _dim_pre(S, i, v):
    sp = _split(S)
    return sp is not None and not (sp[0] <= i < sp[1])


def _dim_in(S, i, v):
    sp = _split(S)
    return sp is not None and not (sp[2] <= i < sp[2] + sp[1] - sp[0])


def _cap_if(S, B, ret):
    if B['pre_l'] == B['pre_r']:
        return f'`pre_l == pre_r = {B["pre_l"]}`：区间为空 → 空节点，返回 `None`'
    return f'区间 `[{B["pre_l"]}, {B["pre_r"]})` 非空：先序第一个 `preorder[{B["pre_l"]}] = {PRE[B["pre_l"]]}` 就是==根=='


def _cap_size(S, B, ret):
    root = PRE[S['pre_l']]
    return (f'根 `{root}` 在 inorder 的下标 `index[{root}] = {POS[root]}`，'
            f'左边有 `{POS[root]} - {S["in_l"]} = {S["left_size"]}` 个数 → ==左子树大小 {S["left_size"]}==')


def _cap_left(S, B, ret):
    pl, ls, il = B['pre_l'], B['left_size'], B['in_l']
    return (f'递归建==左子树==：preorder 取根后面 {ls} 个 `[{pl + 1}, {pl + 1 + ls})`，'
            f'inorder 从 `{il}` 开始')


def _cap_right(S, B, ret):
    pl, ls, il, pr = B['pre_l'], B['left_size'], B['in_l'], B['pre_r']
    lt = B.get('left')
    got = f'左子树建好了（根 `{lt.val}`）' if lt is not None else '左子树是空的'
    return f'{got}；再递归==右子树==：preorder 剩下的 `[{pl + 1 + ls}, {pr})`，inorder 跳过根，从 `{il + 1 + ls}` 开始'


def _cap_ret(S, B, ret):
    l, r = B.get('left'), B.get('right')
    fmt = lambda x: '空' if x is None else f'`{x.val}`'
    return f'左右子树都有了：创建根 =={ret.val}==，左 = {fmt(l)}，右 = {fmt(r)}，返回给上一层'


CONFIG = dict(
    num=105, title='从前序与中序遍历序列构造二叉树', difficulty='Medium', category='二叉树',
    author='灵茶山艾府', technique='递归分治 + 哈希表 + 下标区间',
    code='''
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        index = {x: i for i, x in enumerate(inorder)}

        # 根据 preorder[pre_l:pre_r] 和 inorder[in_l:in_r] 生成二叉树
        # 其中 in_r 没用到，可以省略
        def dfs(pre_l: int, pre_r: int, in_l: int) -> Optional[TreeNode]:
            if pre_l == pre_r:  # 空节点
                return None
            left_size = index[preorder[pre_l]] - in_l  # 左子树的大小
            left = dfs(pre_l + 1, pre_l + 1 + left_size, in_l)
            right = dfs(pre_l + 1 + left_size, pre_r, in_l + 1 + left_size)
            return TreeNode(preorder[pre_l], left, right)

        return dfs(0, len(preorder), 0)  # 左闭右开区间
''',
    call='Solution().buildTree([3,9,20,15,7], [9,3,15,20,7])',
    result_fn=tree_list,
    expect=[3, 9, 20, None, None, 15, 7],
    views=[
        dict(type='array', var='preorder', label='preorder（橙 = 根，蓝 = 左子树，粉 = 右子树）', cell=64,
             window=('pre_l', 'pre_r - 1'), color=_pre_color, dim=_dim_pre),
        dict(type='array', var='inorder', label='inorder', cell=64,
             window=('in_l', 'in_l + pre_r - pre_l - 1'), color=_in_color, dim=_dim_in),
        dict(type='tree', label='已经建好的子树', h=250),
        dict(type='calls', h=170),
    ],
    watch=[('pre_l', 'pre_l', 'cyan'), ('pre_r', 'pre_r', 'cyan'), ('in_l', 'in_l', 'purple'), ('left_size', 'left_size', 'blue')],
    captions={
        'if pre_l == pre_r': _cap_if,
        'left_size = ': _cap_size,
        'left = dfs(': _cap_left,
        'right = dfs(': _cap_right,
        'return TreeNode(': _cap_ret,
        'return dfs(0': '已用哈希表 `index` 记下每个数在 inorder 的下标；从整棵树开始：preorder `[0, 5)`，inorder 从 `0` 开始（==左闭右开==）',
    },
    skip=['index = {', 'return None'],
    max_steps=60,
    cards=dict(
        one_liner='先序第一个是根，在中序里找到根，左边就是左子树',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给出同一棵树的==先序遍历== `preorder` 和==中序遍历== `inorder`，构造这棵二叉树',
                 '先序：根-左-右；中序：左-根-右；节点值==互不相同==',
                 '示例：`preorder = [3,9,20,15,7]`，`inorder = [9,3,15,20,7]`',
                 '→ 构造出 `[3,9,20,null,null,15,7]`'],
        quote='用一个==哈希表==预处理 inorder 每个元素的下标，O(1) 知道左子树的大小；把递归参数改成子数组==下标区间（左闭右开）==的端点，从而避免复制数组。',
        quote_src='—— 灵茶山艾府题解（写法二）',
        idea=['`preorder[pre_l]` 是根；它在中序的下标 − `in_l` = ==左子树大小== `left_size`',
              '先序：根 | 左子树 `left_size` 个 | 右子树；中序：左子树 | 根 | 右子树',
              '`in_r` 用不到：子树大小 `pre_r - pre_l` 已经知道了'],
        summary=['时间 `O(n)`：每个节点递归一次、每次 `O(1)`；空间 `O(n)`',
                 '易错：区间统一用==左闭右开==，空区间是 `pre_l == pre_r`',
                 '易错：右子树在中序里从 `in_l + 1 + left_size` 开始（要跳过根）',
                 '写法一：切片 + `inorder.index`，好写但 `O(n²)`；106、889 题同一套路',
                 '（原代码第 5 行的长注释拆成了两行，便于阅读）'],
    ),
)
