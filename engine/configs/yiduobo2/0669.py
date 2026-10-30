LOW, HIGH = 2, 4


def _is_head(S, n):
    ph = S.get('phead')
    return ph is not None and n._uid == ph._uid


def _color(S, n):
    if _is_head(S, n):
        return 'purple'
    if n.val < LOW or n.val > HIGH:
        return 'red'
    return None


def _cap_if_not(S, B, ret):
    now = S.get('now')
    if now is None:
        return '`now` 为空：这棵子树没东西可剪，直接返回'
    return f'`now = {now.val}`，父亲 `fa = {_name(S, S["fa"])}`'


def _name(S, n):
    return 'phead(哑结点)' if _is_head(S, n) else str(n.val)


def _cap_lt(S, B, ret):
    now = S['now']
    if now.val < LOW:
        return f'`{now.val} < low = {LOW}`：删掉它，==左子树更小，一起删==，用右孩子顶替'
    return f'`{now.val} >= low`，不用从左边剪'


def _cap_gt(S, B, ret):
    now = S['now']
    if now.val > HIGH:
        return f'`{now.val} > high = {HIGH}`：删掉它，==右子树更大，一起删==，用左孩子顶替'
    return f'`{LOW} <= {now.val} <= {HIGH}`：==合法结点==，保留，递归修剪左右子树'


def _cap_side(S, B, ret):
    now, fa = S['now'], S['fa']
    side = '左' if now is fa.left else '右'
    return f'顶替前要知道 `{now.val}` 是 `{_name(S, fa)}` 的==哪个孩子==：是{side}孩子'


def _v(n):
    return None if n is None else n.val


CONFIG = dict(
    num=669, title='修剪二叉搜索树', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='递归 + 记录父亲，非法结点用孩子顶替',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def trimBST(self, root, low, high):
        phead = TreeNode(left = root)
        self.cut(root, phead, low, high)

        return phead.left

    def cut(self, now, fa, low, high):
        if not now:
            return

        if now.val < low:
            if now == fa.left:
                fa.left = now.right
            else:
                fa.right = now.right

            self.cut(now.right, fa, low, high)

        elif now.val > high:
            if now == fa.left:
                fa.left = now.left
            else:
                fa.right = now.left

            self.cut(now.left, fa, low, high)

        else:
            self.cut(now.left, now, low, high)
            self.cut(now.right, now, low, high)
''',
    call=f'''root = Tr([1, 0, 4, None, None, 2, 5, None, 3])
Solution().trimBST(root, {LOW}, {HIGH})''',
    result_fn=tree_list,
    expect=[4, 2, None, None, 3],
    views=[
        dict(type='text', fn=lambda S: f'保留区间 `[low, high] = [{LOW}, {HIGH}]`；紫 = 哑结点 phead，红 = 不在区间内的值', h=60),
        dict(type='tree', var='phead', label='从哑结点 phead 往下看', h=420,
             pointers={'now': 'blue', 'fa': 'pink'}, color=_color),
        dict(type='calls', h=200, hide=('low', 'high')),
    ],
    watch=[('now', lambda S: _v(S.get('now')), 'blue'),
           ('fa', lambda S: ('phead' if S.get('fa') is not None and _is_head(S, S['fa']) else _v(S.get('fa'))) if 'fa' in S else None, 'pink'),
           ('phead.left', lambda S: _v(S['phead'].left) if S.get('phead') else None, 'purple')],
    captions={
        'phead = TreeNode': '建一个==哑结点== `phead`，`phead.left = root`：根也可能被删，这样根也有父亲',
        'self.cut(root, phead': '从根开始修剪，根的父亲是 `phead`',
        'if not now': _cap_if_not,
        'if now.val < low': _cap_lt,
        'elif now.val > high': _cap_gt,
        'if now == fa.left': _cap_side,
        'fa.left = now.right': '`{fa.left.val if fa.left else None}` 顶替到 `{B.now.val}` 的位置：`fa.left = now.right`',
        'fa.right = now.right': '右孩子顶替：`fa.right = {fa.right.val if fa.right else None}`',
        'self.cut(now.right, fa': '顶替上来的右子树里==可能还有 < low 的==，继续以 `fa` 为父亲修剪它',
        'fa.left = now.left': '左孩子顶替：`fa.left = {fa.left.val if fa.left else None}`',
        'fa.right = now.left': '`{B.now.val}` 被删，左孩子顶替：`fa.right = {fa.right.val if fa.right else None}`',
        'self.cut(now.left, fa': '顶替上来的左子树里==可能还有 > high 的==，继续修剪',
        'self.cut(now.left, now': '递归修剪 `{B.now.val}` 的左子树，父亲是 `{B.now.val}`',
        'self.cut(now.right, now': '递归修剪 `{B.now.val}` 的右子树，父亲是 `{B.now.val}`',
        'return phead.left': '新根就是 `phead.left` = =={ret.val}==（原来的根 1 已被删掉）',
    },
    skip=[10],
    max_steps=70,
    cards=dict(
        one_liner='值太小就用右孩子顶替，值太大就用左孩子顶替，合法就往下递归',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['给二叉搜索树的根 `root` 和边界 `low`、`high`',
                 '修剪树，使所有结点值都在 `[low, high]` 内，==保持原有的相对结构==',
                 '示例：`[3,0,4,null,2,null,null,1], low = 1, high = 3` → `[3,2,null,1]`',
                 '本视频：`[1,0,4,null,null,2,5,null,3]`，`[2, 4]` → `[4,2,null,null,3]`'],
        quote='若node.val < low，说明此时node应该被删除掉，同时由于==node左子树中所有结点的值都必然小于node.val==，因此node左子树也应该一起删除掉。于是此时==直接将node的右孩子顶替到node的位置上==即可',
        quote_src='—— yiduobo 知乎题解',
        idea=['`val < low`：连同左子树删掉，右孩子顶替；`val > high` 对称，左孩子顶替',
              '`low <= val <= high`：结点合法，递归修剪左右子树',
              '顶替要改父亲的指针：递归时==带上父亲 fa==，判断自己是左孩子还是右孩子'],
        result='修剪后返回新根 `4`：`[4,2,null,null,3]` ✓',
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '哑结点 `phead`：==根被删时也有父亲可改==，最后返回 `phead.left`',
                 '易错：顶替上来的子树还要==继续修剪==（它里面可能还有越界的值）',
                 '原文为 Python 2 风格：已删去文档字符串和结点定义注释，代码未改'],
    ),
)
