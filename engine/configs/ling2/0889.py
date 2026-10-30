PRE = [1, 2, 4, 5, 3, 6, 7]
POST = [4, 5, 2, 6, 7, 3, 1]
POS = {x: i for i, x in enumerate(POST)}


def _split(S):
    """当前 dfs 的 (pre_l, pre_r, post_l, left_size)；区间为空时返回 None；只有一个节点时 left_size = 0"""
    a, b, c = S.get('pre_l'), S.get('pre_r'), S.get('post_l')
    if not all(isinstance(x, int) for x in (a, b, c)) or a >= b:
        return None
    ls = POS[PRE[a + 1]] - c + 1 if b - a >= 2 else 0
    return a, b, c, ls


def _pre_color(S, i, v):
    sp = _split(S)
    if sp is None:
        return None
    a, b, c, ls = sp
    if i == a:
        return 'orange'
    if a + 1 <= i < a + 1 + ls:
        return 'blue'
    if a + 1 + ls <= i < b:
        return 'pink'
    return None


def _post_color(S, i, v):
    sp = _split(S)
    if sp is None:
        return None
    a, b, c, ls = sp
    n = b - a
    if i == c + n - 1:
        return 'orange'
    if c <= i < c + ls:
        return 'blue'
    if c + ls <= i < c + n - 1:
        return 'pink'
    return None


def _dim_pre(S, i, v):
    sp = _split(S)
    return sp is not None and not (sp[0] <= i < sp[1])


def _dim_post(S, i, v):
    sp = _split(S)
    return sp is not None and not (sp[2] <= i < sp[2] + sp[1] - sp[0])


def _cap_empty(S, B, ret):
    if B['pre_l'] == B['pre_r']:
        return f'`pre_l == pre_r = {B["pre_l"]}`：区间为空 → ==空节点=='
    return f'区间 `[{B["pre_l"]}, {B["pre_r"]})` 有 {B["pre_r"] - B["pre_l"]} 个数，不是空节点'


def _cap_leaf(S, B, ret):
    a, b = B['pre_l'], B['pre_r']
    if a + 1 == b:
        return f'区间里只有 `{PRE[a]}` 一个数 → ==叶子节点==，直接创建返回'
    return (f'区间 `[{a}, {b})` 不止一个数：根是 `preorder[{a}] = {PRE[a]}`，'
            f'==规定== `preorder[{a + 1}] = {PRE[a + 1]}` 是==左子树的根==')


def _cap_size(S, B, ret):
    x = PRE[S['pre_l'] + 1]
    return (f'左子树的根 `{x}` 在后序里是==左子树的最后一个==：下标 `index[{x}] = {POS[x]}`，'
            f'减 `post_l = {S["post_l"]}` 再加 1 → ==左子树大小 {S["left_size"]}==')


def _cap_left(S, B, ret):
    a, ls, c = B['pre_l'], B['left_size'], B['post_l']
    return (f'递归建==左子树==：前序 `[{a + 1}, {a + 1 + ls})`（跳过根），'
            f'后序从 `{c}` 开始取 {ls} 个')


def _cap_right(S, B, ret):
    a, b, ls, c = B['pre_l'], B['pre_r'], B['left_size'], B['post_l']
    lt = B.get('left')
    got = f'左子树建好了（根 `{lt.val}`）' if lt is not None else '左子树是空的'
    return f'{got}；再递归==右子树==：前序 `[{a + 1 + ls}, {b})`，后序从 `{c + ls}` 开始'


def _cap_ret(S, B, ret):
    l, r = B.get('left'), B.get('right')
    f = lambda x: '空' if x is None else f'`{x.val}`'
    return f'左右子树都有了：创建根 =={ret.val}==，左 = {f(l)}，右 = {f(r)}，返回给上一层'


CONFIG = dict(
    num=889, title='从前序与后序遍历序列构造二叉树', difficulty='Medium', category='二叉树',
    author='灵茶山艾府', technique='规定 preorder[1] 是左子树的根 + 哈希表 + 左闭右开',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def constructFromPrePost(self, preorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        index = {x: i for i, x in enumerate(postorder)}

        # 注意 post_r 可以省略
        def dfs(pre_l: int, pre_r: int, post_l: int) -> Optional[TreeNode]:
            if pre_l == pre_r:  # 空节点
                return None
            if pre_l + 1 == pre_r:  # 叶子节点
                return TreeNode(preorder[pre_l])
            left_size = index[preorder[pre_l + 1]] - post_l + 1  # 左子树的大小
            left = dfs(pre_l + 1, pre_l + 1 + left_size, post_l)
            right = dfs(pre_l + 1 + left_size, pre_r, post_l + left_size)
            return TreeNode(preorder[pre_l], left, right)

        return dfs(0, len(preorder), 0)  # 左闭右开区间
''',
    call=f'Solution().constructFromPrePost({PRE}, {POST})',
    result_fn=tree_list,
    expect=[1, 2, 3, 4, 5, 6, 7],
    views=[
        dict(type='array', var='preorder', label='preorder（橙 = 根，蓝 = 左子树，粉 = 右子树）', cell=64,
             window=('pre_l', 'pre_r - 1'), color=_pre_color, dim=_dim_pre),
        dict(type='array', var='postorder', label='postorder', cell=64,
             window=('post_l', 'post_l + pre_r - pre_l - 1'), color=_post_color, dim=_dim_post),
        dict(type='tree', label='已经建好的子树（自底向上拼起来）', h=250),
        dict(type='calls', h=170),
    ],
    watch=[('pre_l', 'pre_l', 'purple'), ('pre_r', 'pre_r', 'purple'), ('post_l', 'post_l', 'cyan'),
           ('left_size', lambda S: S['_inner'].get('left_size'), 'blue')],
    captions={
        'if pre_l == pre_r': _cap_empty,
        'if pre_l + 1 == pre_r': _cap_leaf,
        'return TreeNode(preorder[pre_l])': '叶子 =={ret.val}== 建好，返回',
        'left_size = ': _cap_size,
        'left = dfs(': _cap_left,
        'right = dfs(': _cap_right,
        'return TreeNode(preorder[pre_l], left': _cap_ret,
        'return dfs(0': '`index` 记下每个数在 postorder 的下标；从整棵树开始：前序 `[0, 7)`，后序从 `0` 开始（==左闭右开==）',
    },
    skip=['index = {', 'return None', 'if pre_l == pre_r'],
    max_steps=60,
    cards=dict(
        one_liner='规定 preorder[1] 是左子树的根，它在后序里的位置决定左子树大小',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给出同一棵树的==前序遍历== `preorder` 和==后序遍历== `postorder`，构造这棵二叉树',
                 '前序：根-左-右；后序：左-右-根；值互不相同；==答案不唯一时返回任意一个==',
                 '示例：`preorder = [1,2,4,5,3,6,7]`，`postorder = [4,5,2,6,7,3,1]`',
                 '→ `[1,2,3,4,5,6,7]`'],
        quote='题目说，如果存在多个答案，我们可以返回其中任何一个。那么不妨==规定==：无论什么情况，在前序遍历中，==preorder[1] 都是左子树的根节点值==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只知道前序和后序，树==不一定唯一==（如 `[1,2,3,4]` / `[3,4,2,1]` 对应两棵树）',
              '`preorder[1]` 是左子树的根 → 它在后序里是==左子树的最后一个== → 下标差 + 1 = 左子树大小',
              '递归边界：长度 0 返回空，长度 1 直接建叶子'],
        result='子树自底向上拼好：返回 `[1,2,3,4,5,6,7]`，与示例一致',
        summary=['时间 `O(n)`：哈希表 `O(1)` 查下标 + 传区间端点不复制数组；空间 `O(n)`',
                 '易错：长度为 1 时==必须特判==叶子，否则 `preorder[pre_l + 1]` 越界',
                 '易错：左子树大小要 `+ 1`（左子树的根在后序里是左子树的==最后一个==）',
                 '写法一：切片 + `postorder.index`，好写但 `O(n²)`；同套路：105、106'],
    ),
)
