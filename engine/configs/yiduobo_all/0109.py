def _hp(S):
    h = S.get('self.head')
    return h.val - 1 if h else 5


def _rng(S):
    if 'left' not in S or 'right' not in S:
        return '先数出链表长度 `l`，再用下标区间 `[left, right)` 表示「这棵子树要生成几个节点」'
    n = S['right'] - S['left']
    return f"当前要生成区间 `[{S['left']}, {S['right']})`，共 =={n}== 个节点；链表指针 `self.head` 指向「下一个要用的值」"


def _cap_empty(S, B, ret):
    if S.left == S.right:
        return f'`left == right == {S.left}`：区间为空，没有节点要生成 → 返回 `None`'
    return f'`left = {S.left}` ≠ `right = {S.right}`：还有 `{S.right - S.left}` 个节点要生成'


def _cap_root(S, B, ret):
    return f'左子树生成完了，==链表当前指的就是根==：`TreeNode({S.root.val})`'


def _cap_mid(S, B, ret):
    return f'`mid = ({S.left} + {S.right}) // 2 = {S.mid}`：左边 `[{S.left}, {S.mid})` 有 `{S.mid - S.left}` 个节点，右边 `[{S.mid + 1}, {S.right})` 有 `{S.right - S.mid - 1}` 个'


def _cap_ret(S, B, ret):
    return f'返回以 `{ret.val}` 为根的子树' if ret is not None else '返回 `None`（空子树）'


CONFIG = dict(
    num=109, title='有序链表转换二叉搜索树', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='中序遍历建树 · 链表指针随之后移',
    tags=['链表树与回溯'],
    code='''
class Solution(object):
    def sortedListToBST(self, head):

        self.head = head
        l = 0
        while head:
            l += 1
            head = head.next

        return self.dfs(0, l)

    def dfs(self, left, right):
        if left == right:
            return None
        mid = (left + right) // 2
        left_tree = self.dfs(left, mid)
        root = TreeNode(self.head.val)
        self.head = self.head.next
        right_tree = self.dfs(mid + 1, right)
        root.left = left_tree
        root.right = right_tree
        return root
''',
    call='Solution().sortedListToBST(L([1,2,3,4,5]))',
    expect=[3, 2, 5, 1, None, 4],
    result_fn=tree_list,
    views=[
        dict(type='text', fn=_rng, size=26, h=60),
        dict(type='array', var='[1, 2, 3, 4, 5]', label='有序链表（蓝 = self.head：下一个要用的值，灰 = 已用掉）', cell=90, h=190,
             dim=lambda S, i, v: 'self.head' in S and i < _hp(S),
             color=lambda S, i, v: 'blue' if 'self.head' in S and i == _hp(S) else None),
        dict(type='tree', label='生成中的二叉搜索树', pointers={'root': 'green'}, h=300),
        dict(type='calls', h=210, hide=()),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'),
           ('self.head', lambda S: S['self.head'].val if S.get('self.head') else None, 'cyan'), ('l', 'l', 'green')],
    captions={
        'self.head = head': '`self.head` 记住链表头：它会==随着建树一步步后移==，永远指向「下一个要用的值」',
        'l += 1': '数长度：`l = {l}`',
        'head = head.next': '`head` 往后走一步',
        'return self.dfs(0, l)': '链表长度 `l = {l}`：用区间 `[0, {l})` 开始递归建树',
        'if left == right': _cap_empty,
        'mid = (': _cap_mid,
        'left_tree = self.dfs': '==先生成左子树==（中序：左 - 根 - 右），区间 `[{left}, {mid})`',
        'root = TreeNode': _cap_root,
        'self.head = self.head.next': '根用掉了当前节点 → 链表指针后移一步，==下一个值留给右子树==',
        'right_tree = self.dfs': '再生成右子树，区间 `[{mid + 1}, {right})`',
        'root.left = left_tree': '把左子树挂到 `{root.val}` 的左边',
        'root.right = right_tree': '把右子树挂到 `{root.val}` 的右边',
        'return root': _cap_ret,
        'return None': '区间为空，返回 `None`',
    },
    skip=['l = 0', 8, 14, 'root.left = left_tree'],
    max_steps=130,
    cards=dict(
        one_liner='中序遍历的顺序正好是链表顺序：左 - 根 - 右，边建边走',
        complexity='时间 `O(n)`，空间 `O(log n)`（递归栈）',
        problem=['给定一个单链表，元素按升序排列',
                 '把它转换成一棵==高度平衡==的二叉搜索树（左右子树高度差不超过 1）',
                 '示例：`[1,2,3,4,5]` → 根为 `3`，左 `2(1)`，右 `5(4)`'],
        quote='由于这里采用中序遍历的方式来生成，这个有序的链表正好能与中序遍历得到的序列对应，因此在递归过程中逐个往后移动链表的指针即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['108 题（数组）能直接取中点当根；链表取不到中点，就改成==中序：先左、再根、后右==',
              '`dfs(left, right)` 只负责生成区间里的 `right - left` 个节点，中点 `mid` 只用来==分配左右各几个==',
              '左子树建完时，链表指针恰好停在根的值上；用掉后后移，剩下的留给右子树'],
        summary=['时间 `O(n)`：每个节点生成一次，链表只走一遍；空间 `O(log n)`',
                 '易错点：必须==先建左子树，再取 `self.head.val`==，顺序反了值就错位',
                 '`self.head` 是跨递归共享的指针，不是参数；右子树区间是 `[mid + 1, right)`',
                 '对比 108：数组版「根 - 左 - 右」，链表版「左 - 根 - 右」',
                 '原文为 Python 2 写法，`(left + right) / 2` 已改为 `//` 整除'],
    ),
)
