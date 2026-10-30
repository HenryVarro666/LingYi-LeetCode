def _v(x):
    return 'None' if x is None else x.val


def _cap_left(S, B, ret):
    kid = S.get('root')
    return (f'先把 `{B["root"].val}` 的==左子树==展开成链表，拿到它的尾节点'
            + ('（左儿子是空的）' if kid is None else f'（从 `{kid.val}` 开始）'))


def _cap_right(S, B, ret):
    kid = S.get('root')
    return (f'左子树链表的尾节点 `left_tail = {_v(B["left_tail"])}`；再展开==右子树=='
            + ('（右儿子是空的）' if kid is None else f'（从 `{kid.val}` 开始）'))


def _cap_if(S, B, ret):
    lt = B['left_tail']
    if lt is not None:
        return f'左链表非空（尾巴是 `{lt.val}`）→ 要把 `{B["root"].val}`、左链、右链==穿针引线=='
    return f'左子树是空的：`{B["root"].val}` 后面本来就是右链表，什么都不用改'


def _cap_ret(S, B, ret):
    rt, lt = B.get('right_tail'), B.get('left_tail')
    why = '右链尾' if rt is not None else ('右边为空 → 左链尾' if lt is not None else '左右都空 → 自己')
    return f'返回合并后链表的尾节点（{why}）：`{_v(ret)}`'


CONFIG = dict(
    num=114, title='二叉树展开为链表', difficulty='Medium', category='二叉树',
    author='灵茶山艾府', technique='分治：返回链表尾节点',
    code='''
class Solution:
    def flatten(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if root is None:
            return None
        left_tail = self.flatten(root.left)
        right_tail = self.flatten(root.right)
        if left_tail:
            left_tail.right = root.right  # 左子树链表的尾节点 -> 右子树链表的头节点
            root.right = root.left  # root -> 左子树链表的头节点
            root.left = None
        return right_tail or left_tail or root
''',
    call='root = Tr([1,2,5,3,4,None,6])\nSolution().flatten(root)\nroot',
    result_fn=tree_list,
    expect=[1, None, 2, None, 3, None, 4, None, 5, None, 6],
    views=[
        dict(type='tree', pointers={'root': 'blue', 'left_tail': 'green', 'right_tail': 'pink'}, h=440),
        dict(type='calls', h=190),
    ],
    watch=[('root', 'root', 'blue'), ('left_tail', 'left_tail', 'green'), ('right_tail', 'right_tail', 'pink')],
    captions={
        'if root is None': lambda S, B, ret: ('空节点' if B['root'] is None else f'`root = {B["root"].val}` 不是空节点'),
        'return None': '空子树没有链表 → 尾节点返回 `None`',
        'left_tail = self.flatten': _cap_left,
        'right_tail = self.flatten': _cap_right,
        'if left_tail:': _cap_if,
        'left_tail.right = root.right': lambda S, B, ret: f'① 左链尾 `{S["left_tail"].val}` → 右链头 `{_v(S["left_tail"].right)}`：==两条链先接起来==',
        'root.right = root.left': lambda S, B, ret: f'② `{S["root"].val}` → 左链头 `{S["root"].right.val}`：把整条链挂到 `root` 的右边',
        'root.left = None': '③ 左指针置空：以 `{root.val}` 为根的子树==变成了一条链==',
        'return right_tail or left_tail or root': _cap_ret,
    },
    skip=['if root is None'],
    max_steps=60,
    cards=dict(
        one_liner='先把左右子树各自展开成链，再把根、左链、右链串起来',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['把二叉树==原地==展开成单链表：`right` 指向下一个节点，`left` 全部为空',
                 '链表顺序 = 二叉树的==先序遍历==（根-左-右）',
                 '示例：`[1,2,5,3,4,null,6]` → `1→2→3→4→5→6`'],
        quote='假如我们计算出了 root 左子树的链表 2→3→4，以及右子树的链表 5→6，那么接下来只需要==穿针引线==，把节点 1 和两条链表连起来。',
        quote_src='—— 灵茶山艾府题解（方法二：分治）',
        idea=['穿针引线需要==左链表的尾节点==，所以 `dfs` 返回展开后链表的尾节点',
              '① 左链尾 → 右链头；② `root` → 左链头；③ `root.left = None`',
              '返回值：右链尾，右边为空就返回左链尾，都空就返回 `root` 自己'],
        summary=['时间 `O(n)`，空间 `O(n)`（递归栈，最坏是一条链）',
                 '易错：①② 顺序不能反，先用 `root.right` 接到左链尾，再覆盖 `root.right`',
                 '易错：返回 `right_tail or left_tail or root`，右链为空时尾巴在左链',
                 '方法一：头插法，按「右-左-根」遍历，把节点依次插到链表头 `head` 前面'],
    ),
)
