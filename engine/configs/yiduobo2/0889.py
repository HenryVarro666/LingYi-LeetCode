PRE = [1, 2, 4, 3, 5, 6]
POST = [4, 2, 5, 6, 3, 1]
POS = {x: i for i, x in enumerate(POST)}


def _split(S):
    """当前 build 的闭区间 (pre_l, pre_r, post_l, post_r, left_len)"""
    a, b, c, d = (S['_inner'].get(k) for k in ('pre_l', 'pre_r', 'post_l', 'post_r'))
    if not all(isinstance(x, int) for x in (a, b, c, d)):
        return None
    ln = POS[PRE[a + 1]] - c + 1 if a < b else 0
    return a, b, c, d, ln


def _pre_color(S, i, v):
    sp = _split(S)
    if sp is None:
        return None
    a, b, c, d, ln = sp
    if i == a:
        return 'orange'
    if a + 1 <= i <= a + ln:
        return 'blue'
    if a + ln + 1 <= i <= b:
        return 'pink'
    return None


def _post_color(S, i, v):
    sp = _split(S)
    if sp is None:
        return None
    a, b, c, d, ln = sp
    if i == d:
        return 'orange'
    if c <= i <= c + ln - 1:
        return 'blue'
    if c + ln <= i <= d - 1:
        return 'pink'
    return None


def _dim_pre(S, i, v):
    sp = _split(S)
    return sp is not None and not (sp[0] <= i <= sp[1])


def _dim_post(S, i, v):
    sp = _split(S)
    return sp is not None and not (sp[2] <= i <= sp[3])


def _cap_now(S, B, ret):
    a, b = S['pre_l'], S['pre_r']
    return (f'`pre[{a}] = {PRE[a]}` 是当前子树的根（也等于 `post[{S["post_r"]}]`），先建出节点 `{PRE[a]}`')


def _cap_if(S, B, ret):
    a, b = B['pre_l'], B['pre_r']
    if a < b:
        return f'`pre_l = {a} < pre_r = {b}`：子树不止一个节点，还要建孩子'
    return f'`pre_l == pre_r = {a}`：只有根一个节点 → ==叶子==，直接返回'


def _cap_len(S, B, ret):
    a, c = S['pre_l'], S['post_l']
    x = PRE[a + 1]
    p = POS[x]
    return (f'认为 `pre[{a + 1}] = {x}` 是左孩子；它在后序里的位置 `p = {p}` → '
            f'`post[{c}..{p}]` 是左子树，==长度 {S["left_len"]}==')


def _cap_left(S, B, ret):
    a, c, ln = B['pre_l'], B['post_l'], B['left_len']
    return f'左子树：前序 `[{a + 1}, {a + ln}]`，后序 `[{c}, {c + ln - 1}]`（==闭区间==），递归'


def _cap_has_right(S, B, ret):
    a, b, ln = B['pre_l'], B['pre_r'], B['left_len']
    rest = b - a - ln
    nd = B['now']
    if rest > 0:
        return f'除去根和左子树还剩 `{rest}` 个节点 → `{nd.val}` 有右子树'
    return f'`pre_r - pre_l - left_len = 0`：节点全给了左子树 → `{nd.val}` ==没有右孩子=='


def _cap_right(S, B, ret):
    a, b, c, d, ln = B['pre_l'], B['pre_r'], B['post_l'], B['post_r'], B['left_len']
    return f'右子树：前序 `[{a + ln + 1}, {b}]`，后序 `[{c + ln}, {d - 1}]`（==去掉末尾的根==），递归'


def _cap_ret(S, B, ret):
    l, r = ret.left, ret.right
    f = lambda x: '空' if x is None else f'`{x.val}`'
    return f'返回子树根 =={ret.val}==（左 = {f(l)}，右 = {f(r)}）'


CONFIG = dict(
    num=889, title='从前序与后序遍历序列构造二叉树', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='认为 pre[1] 是左孩子 + 闭区间递归',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def constructFromPrePost(self, pre, post):

        pos_dict = {x : index for index, x in enumerate(post)}
        return self.build(0, len(pre) - 1, 0, len(post) - 1, pre, post, pos_dict)

    def build(self, pre_l, pre_r, post_l, post_r, pre, post, pos_dict):
        now = TreeNode(pre[pre_l])
        if pre_l < pre_r:
            left_len = pos_dict[pre[pre_l + 1]] - post_l + 1
            if left_len > 0:
                now.left = self.build(pre_l + 1, pre_l + left_len, post_l, post_l + left_len - 1, pre, post, pos_dict)
            if pre_r - pre_l - left_len > 0:
                now.right = self.build(pre_l + left_len + 1, pre_r, post_l + left_len, post_r - 1, pre, post, pos_dict)
        return now
''',
    call=f'Solution().constructFromPrePost({PRE}, {POST})',
    result_fn=tree_list,
    expect=[1, 2, 3, 4, None, 5, 6],
    views=[
        dict(type='array', var='pre', label='pre（橙 = 根，蓝 = 左子树，粉 = 右子树）', cell=64,
             window=(lambda S: S['_inner'].get('pre_l'), lambda S: S['_inner'].get('pre_r')),
             color=_pre_color, dim=_dim_pre),
        dict(type='array', var='post', label='post', cell=64,
             window=(lambda S: S['_inner'].get('post_l'), lambda S: S['_inner'].get('post_r')),
             color=_post_color, dim=_dim_post),
        dict(type='tree', label='构造中的树（先建根，再挂孩子）', h=250),
        dict(type='calls', h=170, hide=('pre', 'post', 'pos_dict')),
    ],
    watch=[('pre_l', lambda S: S['_inner'].get('pre_l'), 'purple'), ('pre_r', lambda S: S['_inner'].get('pre_r'), 'purple'),
           ('post_l', lambda S: S['_inner'].get('post_l'), 'cyan'), ('post_r', lambda S: S['_inner'].get('post_r'), 'cyan'),
           ('left_len', lambda S: S['_inner'].get('left_len'), 'blue')],
    captions={
        'pos_dict = {': '`pos_dict` 记下每个值在后序 `post` 中的位置，`O(1)` 查找',
        'return self.build(0': '整棵树：前序 `[0, {len(pre) - 1}]`、后序 `[0, {len(post) - 1}]`（==闭区间==）',
        'now = TreeNode(pre[pre_l])': _cap_now,
        'if pre_l < pre_r': _cap_if,
        'left_len = ': _cap_len,
        'now.left = self.build': _cap_left,
        'if pre_r - pre_l - left_len > 0': _cap_has_right,
        'now.right = self.build': _cap_right,
        'return now': _cap_ret,
    },
    skip=['if left_len > 0'],
    max_steps=60,
    cards=dict(
        one_liner='前序的 pre[1] 当作左孩子，在后序里找到它，就切出了左子树',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给出同一棵树的==前序遍历== `pre` 和==后序遍历== `post`，构造这棵二叉树',
                 '值互不相同；==可能有多个答案，返回任意一个==',
                 '演示：`pre = [1,2,4,3,5,6]`，`post = [4,2,5,6,3,1]`',
                 '节点 2 只有一个孩子 4：它是左是右都行，这里会被当成==左孩子=='],
        quote='我们可以认为==pre[1]为当前子树根节点的左孩子==，那么找到pre[1]在后续遍历post中的位置p，就可以确定==从post[0]到post[p]这一段==就是当前子树后序遍历中左子树的那一部分。',
        quote_src='—— yiduobo 知乎题解',
        idea=['`pre[0]` 和 `post[-1]` 都是当前子树的根',
              '`pre[1]` 当左孩子，它在 `post` 中的位置 `p` → `post[0..p]` 是左子树',
              '剩下的（除根之外）是右子树；左右分别递归，直到建完整棵树'],
        summary=['时间 `O(n)`（`pos_dict` 让查找 `O(1)`），空间 `O(n)`',
                 '区间全是==闭区间==：右子树后序是 `[post_l + left_len, post_r - 1]`，别忘了去掉根',
                 '`pre_r - pre_l - left_len == 0` 时没有右子树，此时不能递归',
                 '只有一个孩子时树不唯一，按“当左孩子”的规则构造一种即可',
                 '原文为 Python 2 风格（类型写在文档字符串里），已删去文档字符串和 TreeNode 定义注释，代码未改'],
    ),
)
