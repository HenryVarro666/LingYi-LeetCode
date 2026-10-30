import views as V


def tree_view(**spec):
    """迭代写法没有递归路径：画树时不传调用栈参数，避免把 root 误标成"递归路径" """
    def draw(cv, S, B, box, T):
        V.v_tree(cv, spec, {'_S': S, '_B': B, '_frames': [dict(args=[], locals=S)]}, box, 0, {})
    return dict(type='custom', draw=draw, h=spec.get('h', 380))


def _v(x):
    return 'None' if x is None else x.val


def _cap_if(S, B, ret):
    now = B['now']
    if now.left is not None:
        return f'`{now.val}` ==有左子树==（情况 3）：左孩子要接到 `{now.val}` 后面，原来的右子树得先挪走'
    if now.right is not None:
        return f'`{now.val}` 只有右子树（情况 2）：什么都不用改，直接去算右子树'
    return f'`{now.val}` 是叶子（情况 1）：什么都不用做'


def _cap_while_r(S, B, ret):
    r = B['rightest']
    if r.right is not None:
        return f'`{r.val}` 还有右儿子 → 继续往右走'
    return f'`{r.val}` 没有右儿子 → 它就是==左子树最右边的节点==（先序里左子树的最后一个）'


CONFIG = dict(
    num=114, title='二叉树展开为链表', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='迭代：右子树接到左子树最右节点后面',
    code='''
class Solution(object):
    def flatten(self, root):
        now = root
        while now:
            if now.left:
                rightest = now.left
                while rightest.right:
                    rightest = rightest.right
                rightest.right = now.right
                now.right = now.left
                now.left = None
                now = now.right
            else:
                now = now.right

        return root
''',
    call='Solution().flatten(Tr([1,2,5,3,4,None,6]))',
    result_fn=tree_list,
    expect=[1, None, 2, None, 3, None, 4, None, 5, None, 6],
    views=[
        tree_view(label='二叉树（原地修改）', h=600, pointers={'now': 'blue', 'rightest': 'pink'}),
    ],
    watch=[('now', 'now', 'blue'), ('rightest', 'rightest', 'pink')],
    captions={
        12: '继续处理 `{now.val}`：它原来是左孩子，现在挂在右边了',
        14: lambda S, B, ret: (f'`now` 沿右指针走到 `{S["now"].val}`' if S['now'] is not None
                               else '右边没有节点了 → 整棵树处理完毕'),
        'now = root': '`now` 从根 `{now.val}` 出发，一路沿右指针往下处理',
        'while now:': lambda S, B, ret: (f'`now = {B["now"].val}` 不为空，继续' if B['now'] is not None else '`now` 为空 → 结束'),
        'if now.left:': _cap_if,
        'rightest = now.left': '找左子树==最右边的节点==：从左孩子 `{rightest.val}` 出发',
        'while rightest.right:': _cap_while_r,
        'rightest = rightest.right': '往右走到 `{rightest.val}`',
        'rightest.right = now.right': lambda S, B, ret: (f'把 `{S["now"].val}` 原来的右子树 `{_v(S["rightest"].right)}` 接到 `{S["rightest"].val}` 的==后面==：'
                                                         f'先序里左子树走完才轮到右子树'),
        'now.right = now.left': '左孩子 `{now.right.val}` 变成 `{now.val}` 的==右孩子==，紧跟在它后面',
        'now.left = None': '`{now.val}` 的左指针置空：链表的 `left` 必须是 `None`',
        'return root': '每个节点都只剩右指针：返回 `root`，链表就是 `1→2→3→4→5→6`',
    },
    skip=['while now:'],
    max_steps=60,
    cards=dict(
        one_liner='有左子树就把右子树接到左子树最右节点后面，再把左子树挪到右边',
        complexity='时间 `O(n)`，额外空间 `O(1)`',
        problem=['把二叉树==原地==展开成单链表：`right` 指向下一个节点，`left` 全部为空',
                 '链表顺序 = 二叉树的==先序遍历==（根-左-右）',
                 '示例：`[1,2,5,3,4,null,6]` → `1→2→3→4→5→6`'],
        quote='p拥有左子树：这个链表是树的前序遍历，于是==左孩子应该接在p后面==，成为p的右孩子，而p原来的右孩子则应该接在==左子树最右边节点的后面==。',
        quote_src='—— yiduobo 知乎题解',
        idea=['叶子：什么都不做；只有右子树：直接往右走',
              '有左子树：先序里左子树的最后一个就是它==最右边的节点== → 右子树接到它后面',
              '再把左子树挪到右边、左指针置空，然后继续处理右孩子'],
        summary=['每个节点最多被「找最右节点」扫一次 → 时间 `O(n)`；不用递归，额外空间 `O(1)`',
                 '易错：先把 `now.right` 接到最右节点后面，再覆盖 `now.right`，否则右子树丢了',
                 '和 94 题的 Morris 中序遍历同一个套路：找左子树最右节点',
                 '原文为 Python 2 风格（类型说明写在文档字符串里），已删去文档字符串，代码未改'],
    ),
)
