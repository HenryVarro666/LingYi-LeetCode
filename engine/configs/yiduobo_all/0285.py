def _v(x):
    return '空' if x is None else str(x.val)


def _info(S):
    I = S['_inner']
    if 'p' not in I:
        return '找比 `p` 大的最小节点：有右子树看右子树，没有就看祖先'
    s = f"目标 `p = {I['p'].val}`"
    if 'res' in I:
        s += f"　候选 `res = {_v(I['res'])}`"
    if 'now' in I:
        s += f"　当前 `now = {_v(I['now'])}`"
    return s


CONFIG = dict(
    num=285, title='二叉搜索树中的中序后继', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='BST 性质 · 右子树最左 / 最近的更大祖先',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def inorderSuccessor(self, root, p):

        if p.right:
            res = p.right
            while res.left:
                res = res.left
            return res

        res = None
        now = root
        while now != p:
            if now.val > p.val:
                res = now
                now = now.left
            else:
                now = now.right

        return res
''',
    setup='''
root = Tr([20, 10, 30, 5, 15, 25, 35, None, None, 12])
P1 = root.left
P2 = root.left.right
''',
    call='''a = Solution().inorderSuccessor(root, P1).val
b = Solution().inorderSuccessor(root, P2).val
[a, b]''',
    expect=[12, 20],
    views=[
        dict(type='text', fn=_info, size=24, h=60),
        dict(type='tree', label='BST（蓝 = now / res，粉 = p）', pointers={'p': 'pink', 'now': 'blue', 'res': 'green'}, path=False, h=420),
        dict(type='text', fn=lambda S: f"本视频跑两次：`p = 10`（有右子树）和 `p = 15`（没有右子树）", size=22, h=50),
    ],
    watch=[('p', lambda S: getattr(S['_inner'].get('p'), 'val', None), 'pink'),
           ('now', lambda S: getattr(S['_inner'].get('now'), 'val', None), 'blue'),
           ('res', lambda S: getattr(S['_inner'].get('res'), 'val', None), 'green')],
    captions={
        'if p.right': lambda S, B, r: (f'`p = {B.p.val}` 有右孩子 `{B.p.right.val}` → 后继一定在右子树里' if B.p.right
                                       else f'`p = {B.p.val}` 没有右子树 → 后继只能是某个祖先'),
        'res = p.right': '从右孩子 `{res.val}` 出发，右子树里最小的就是最左边的节点',
        'while res.left': lambda S, B, r: (f'`{B.res.val}` 还有左孩子 `{B.res.left.val}` → 继续往左，更小' if B.res.left
                                           else f'`{B.res.val}` 没有左孩子 → 已经是右子树的最小值'),
        'res = res.left': '`res` 往左走一步 → `{res.val}`',
        'return res': lambda S, B, r: f'后继是 `{_v(r)}`',
        'res = None': '没有右子树：从根往下找 `p`，路上记录==最后一个比 p 大的节点==；先设 `res = None`',
        'now = root': '从根出发',
        'while now != p': lambda S, B, r: (f'`now = {_v(S.now)}`，还没走到 `p = {S.p.val}`，继续' if S.now is not S.p
                                           else f'走到了 `p`，`res = {_v(S.res)}` 就是最近的更大祖先'),
        'if now.val > p.val': lambda S, B, r: (f'`{B.now.val} > {B.p.val}`：它比 p 大，是候选；p 在它的左子树'
                                               if B.now.val > B.p.val else f'`{B.now.val} < {B.p.val}`：它比 p 小，不是候选；p 在它的右子树'),
        'res = now': '候选更新：`res = {res.val}`（越往下越接近 p，所以更小也更好）',
        'now = now.left': '`p` 更小 → 往左走，`now = {now.val}`',
        'now = now.right': '`p` 更大 → 往右走，`now = {now.val}`',
    },
    skip=['now = root'],
    cards=dict(
        one_liner='有右子树就取右子树最左；否则找最近的比 p 大的祖先',
        complexity='时间 `O(h)`，空间 `O(1)`',
        problem=['给定 BST 的根 `root` 和其中一个节点 `p`，求 `p` 的==中序后继==',
                 '即中序遍历中紧跟在 `p` 后面的节点，也就是大于 `p.val` 的最小节点',
                 '不存在就返回 `null`（会员题）',
                 '本视频：`[20,10,30,5,15,25,35,null,null,12]`，`p = 10` 得 `12`，`p = 15` 得 `20`'],
        quote='当p存在右孩子时，下一个比p大的节点就必然是p右子树中最左侧的那个节点……若p不存在右孩子，那么下一个比p大的节点就是比p大的祖先节点中离p最近的那一个。',
        quote_src='—— yiduobo 题解原文',
        idea=['有右子树：右子树里的值都比 `p` 大，最小的就是最左节点',
              '没有右子树：从根往下找 `p`，每次遇到比 `p` 大的节点就更新 `res` 并向左',
              '最后一个更新的 `res` 离 `p` 最近，就是后继；一次都没更新就是 `None`'],
        summary=['时间 `O(h)`，空间 `O(1)`，不需要中序遍历整棵树',
                 '`while now != p` 比较的是节点本身（引用），不是值',
                 '相等或更小时往右走，不更新 `res`',
                 '不存在后继（`p` 是最大节点）时 `res` 保持 `None`',
                 '原文是 Python 2 风格，本代码无需改动'],
    ),
)
