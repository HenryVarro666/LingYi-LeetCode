INO = [9, 3, 15, 20, 7]
POST = [9, 15, 7, 20, 3]
POS = {x: i for i, x in enumerate(INO)}


def _split(S):
    """当前 dfs 的 (in_l, post_l, post_r, left_size)；区间为空时返回 None"""
    il, pl, pr = S.get('in_l'), S.get('post_l'), S.get('post_r')
    if not isinstance(pl, int) or not isinstance(pr, int) or pl >= pr:
        return None
    return il, pl, pr, POS[POST[pr - 1]] - il


def _post_color(S, i, v):
    sp = _split(S)
    if sp is None:
        return None
    il, pl, pr, ls = sp
    if i == pr - 1:
        return 'orange'
    if pl <= i < pl + ls:
        return 'blue'
    if pl + ls <= i < pr - 1:
        return 'pink'
    return None


def _in_color(S, i, v):
    sp = _split(S)
    if sp is None:
        return None
    il, pl, pr, ls = sp
    if i == il + ls:
        return 'orange'
    if il <= i < il + ls:
        return 'blue'
    if il + ls < i < il + (pr - pl):
        return 'pink'
    return None


def _dim_post(S, i, v):
    sp = _split(S)
    return sp is not None and not (sp[1] <= i < sp[2])


def _dim_in(S, i, v):
    sp = _split(S)
    return sp is not None and not (sp[0] <= i < sp[0] + sp[2] - sp[1])


def _cap_if(S, B, ret):
    if B['post_l'] == B['post_r']:
        return f'`post_l == post_r = {B["post_l"]}`：区间为空 → ==空节点==，返回 `None`'
    pr = B['post_r']
    return f'区间 `[{B["post_l"]}, {pr})` 非空：后序==最后一个== `postorder[{pr - 1}] = {POST[pr - 1]}` 就是根'


def _cap_size(S, B, ret):
    root = POST[S['post_r'] - 1]
    return (f'根 `{root}` 在 inorder 的下标 `index[{root}] = {POS[root]}`，'
            f'减去 `in_l = {S["in_l"]}` → ==左子树大小 {S["left_size"]}==')


def _cap_left(S, B, ret):
    pl, ls, il = B['post_l'], B['left_size'], B['in_l']
    return (f'递归建==左子树==：postorder 取==开头== {ls} 个 `[{pl}, {pl + ls})`，'
            f'inorder 从 `{il}` 开始')


def _cap_right(S, B, ret):
    pl, ls, il, pr = B['post_l'], B['left_size'], B['in_l'], B['post_r']
    lt = B.get('left')
    got = f'左子树建好了（根 `{lt.val}`）' if lt is not None else '左子树是空的'
    return (f'{got}；再递归==右子树==：postorder `[{pl + ls}, {pr - 1})`（==去掉末尾的根==），'
            f'inorder 跳过根，从 `{il + ls + 1}` 开始')


def _cap_ret(S, B, ret):
    l, r = B.get('left'), B.get('right')
    fmt = lambda x: '空' if x is None else f'`{x.val}`'
    return f'左右子树都有了：创建根 =={ret.val}==，左 = {fmt(l)}，右 = {fmt(r)}，返回给上一层'


CONFIG = dict(
    num=106, title='从中序与后序遍历序列构造二叉树', difficulty='Medium', category='二叉树',
    author='灵茶山艾府', technique='递归分治 + 哈希表 + 左闭右开区间',
    tags=['面试经典150'],
    code='''
class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        index = {x: i for i, x in enumerate(inorder)}

        # 根据 inorder[in_l:in_r] 和 postorder[post_l:post_r] 生成二叉树
        # 其中 in_r 没用到，可以省略
        def dfs(in_l: int, post_l: int, post_r: int) -> Optional[TreeNode]:
            if post_l == post_r:  # 空节点
                return None
            left_size = index[postorder[post_r - 1]] - in_l  # 左子树的大小
            left = dfs(in_l, post_l, post_l + left_size)
            right = dfs(in_l + left_size + 1, post_l + left_size, post_r - 1)
            return TreeNode(postorder[post_r - 1], left, right)

        return dfs(0, 0, len(postorder))  # 左闭右开区间
''',
    call=f'Solution().buildTree({INO}, {POST})',
    result_fn=tree_list,
    expect=[3, 9, 20, None, None, 15, 7],
    views=[
        dict(type='array', var='postorder', label='postorder（橙 = 根，蓝 = 左子树，粉 = 右子树）', cell=64,
             window=('post_l', 'post_r - 1'), color=_post_color, dim=_dim_post),
        dict(type='array', var='inorder', label='inorder', cell=64,
             window=('in_l', 'in_l + post_r - post_l - 1'), color=_in_color, dim=_dim_in),
        dict(type='tree', label='已经建好的子树（自底向上拼起来）', h=250),
        dict(type='calls', h=170),
    ],
    watch=[('in_l', 'in_l', 'purple'), ('post_l', 'post_l', 'cyan'), ('post_r', 'post_r', 'cyan'),
           ('left_size', 'left_size', 'blue')],
    captions={
        'if post_l == post_r': _cap_if,
        'left_size = ': _cap_size,
        'left = dfs(': _cap_left,
        'right = dfs(': _cap_right,
        'return TreeNode(': _cap_ret,
        'return dfs(0': '`index` 记下每个数在 inorder 的下标；从整棵树开始：postorder `[0, 5)`，inorder 从 `0` 开始（==左闭右开==）',
    },
    skip=['index = {', 'return None'],
    max_steps=60,
    cards=dict(
        one_liner='后序最后一个是根，在中序里找到根，左边就是左子树',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给出同一棵树的==中序遍历== `inorder` 和==后序遍历== `postorder`，构造这棵二叉树',
                 '中序：左-根-右；后序：左-右-根；节点值==互不相同==',
                 '示例：`inorder = [9,3,15,20,7]`，`postorder = [9,15,7,20,3]`',
                 '→ 构造出 `[3,9,20,null,null,15,7]`'],
        quote='用一个==哈希表==预处理 inorder 每个元素的下标，这样就可以 O(1) 查到 postorder[n-1] 在 inorder 的位置；把递归参数改成子数组下标区间（==左闭右开区间==）的左右端点，从而避免复制数组。',
        quote_src='—— 灵茶山艾府题解（写法二）',
        idea=['`postorder[post_r-1]` 是根；它在中序的下标 − `in_l` = ==左子树大小==',
              '后序：左子树 `left_size` 个 | 右子树 | 根；中序：左子树 | 根 | 右子树',
              '和 105 题同一个套路，只是根从==开头==换到了==末尾=='],
        result='子树自底向上拼好：返回 `[3,9,20,null,null,15,7]` ✓ 与示例一致',
        summary=['时间 `O(n)`：每个节点递归一次、每次 `O(1)`；空间 `O(n)`',
                 '易错：右子树在后序里是 `[post_l + left_size, post_r - 1)`，要==去掉末尾的根==',
                 '易错：右子树在中序里从 `in_l + left_size + 1` 开始（跳过根）',
                 '写法一：切片 + `inorder.index`，好写但 `O(n²)`',
                 '（原代码第 5 行的长注释拆成了两行，便于阅读）'],
    ),
)
