def _v(x):
    return '空' if x is None else str(x.val)


def _top(S):
    n = S['_inner'].get('node')
    while n is not None and getattr(n, 'parent', None) is not None:
        n = n.parent
    return n


def _info(S):
    I = S['_inner']
    n = I.get('node')
    if n is None:
        return '每个节点带 `parent` 指针：有右子树看右子树，否则沿 `parent` 往上走'
    return f"起点是目标节点，当前 `node = {n.val}`，它的 `parent = {_v(n.parent)}`"


CONFIG = dict(
    num=510, title='二叉搜索树的中序后继 II', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='parent 指针 · 右子树最左 / 向上找更大祖先',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def inorderSuccessor(self, node):

        if node.right:
            now = node.right
            while now.left:
                now = now.left
            return now

        while node.parent:
            if node.parent.val > node.val:
                return node.parent
            node = node.parent

        return None
''',
    setup='''
root = Tr([20, 10, 30, 5, 15, 25, 35, None, None, 12])
root.parent = None
_st = [root]
while _st:
    _n = _st.pop()
    for _c in (_n.left, _n.right):
        if _c is not None:
            _c.parent = _n
            _st.append(_c)
N1 = root.left
N2 = root.left.right
''',
    call='''a = Solution().inorderSuccessor(N1).val
b = Solution().inorderSuccessor(N2).val
[a, b]''',
    expect=[12, 20],
    views=[
        dict(type='text', fn=_info, size=24, h=60),
        dict(type='tree', var=_top, label='BST（蓝 = node，绿 = now；每个节点还有 parent 指针）', pointers={'node': 'blue', 'now': 'green'}, path=False, h=420),
        dict(type='text', fn=lambda S: '本视频跑两次：节点 `10`（有右子树）和节点 `15`（没有右子树）', size=22, h=50),
    ],
    watch=[('node', lambda S: getattr(S['_inner'].get('node'), 'val', None), 'blue'),
           ('now', lambda S: getattr(S['_inner'].get('now'), 'val', None), 'green'),
           ('parent', lambda S: getattr(getattr(S['_inner'].get('node'), 'parent', None), 'val', None), 'yellow')],
    captions={
        'if node.right': lambda S, B, r: (f'`{B.node.val}` 有右子树 → 后继在右子树里（情况 2）' if B.node.right
                                          else f'`{B.node.val}` 没有右子树 → 后继是祖先，或者不存在（情况 3 / 1）'),
        'now = node.right': '右子树的根 `{now.val}`：里面最小的值就是后继',
        'while now.left': lambda S, B, r: (f'`{B.now.val}` 有左孩子 `{B.now.left.val}` → 继续往左，值更小' if B.now.left
                                           else f'`{B.now.val}` 没有左孩子 → 右子树最小值找到了'),
        'now = now.left': '往左走一步 → `{now.val}`',
        'return now': '后继是右子树里最左的 `{now.val}`',
        'while node.parent': lambda S, B, r: (f'`{B.node.val}` 还有父节点 `{B.node.parent.val}` → 继续看是否更大' if B.node.parent
                                              else '已经到根了，一路上没遇到更大的祖先'),
        'if node.parent.val > node.val': lambda S, B, r: (
            f'父节点 `{B.node.parent.val}` > `{B.node.val}`：说明 `node` 在它的左子树 → ==它就是后继=='
            if B.node.parent.val > B.node.val else
            f'父节点 `{B.node.parent.val}` < `{B.node.val}`：`node` 在它的右子树，它不可能是后继 → 继续向上'),
        'return node.parent': '返回第一个比它大的祖先 `{node.parent.val}`',
        'node = node.parent': '向上走一步 → `node = {node.val}`',
        'return None': '走到根都没有更大的祖先：`node` 是最大节点，没有后继',
    },
    cards=dict(
        one_liner='有右子树取最左；没有就沿 parent 向上找第一个更大的祖先',
        complexity='时间 `O(h)`，空间 `O(1)`',
        problem=['BST 的每个节点有 `val`、`left`、`right`、==`parent`== 指针，给你其中一个节点 `node`（没有根）',
                 '返回 `node` 的中序后继：值比 `node` 大的最小节点，没有返回 `null`（会员题）',
                 '本视频：`[20,10,30,5,15,25,35,null,null,12]`，节点 `10` 得 `12`，节点 `15` 得 `20`'],
        quote='若node不存在右子树，那么就从node开始不停向上行走，直到遇到某个值大于node的祖先节点为止，而这个节点就是最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['后继有三种：不存在、在右子树、是某个祖先',
              '有右子树：右子树里全是更大的值，取最左边的',
              '没有右子树：第一个比 `node` 大的祖先最近，更远的祖先要么更小要么更大，都不如它'],
        summary=['时间 `O(h)`，空间 `O(1)`，只靠 `parent`，不需要根节点',
                 '与 285 的区别：285 给了根，要从根往下找 `p`；这里给 `parent` 指针，向上走即可',
                 '`while node.parent` 退出说明到根了，返回 `None`',
                 '原文开头的 `Node` 类定义在 `"""` 注释里，仅是 LeetCode 模板，视频里已省略；视频的 setup 为节点补了 `parent`'],
    ),
)
