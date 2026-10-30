def nv(x):
    return '空' if x is None else str(x.val)


def _fa(S):
    fa = S.get('fa')
    if fa is None:
        return '哨兵' if 'now' in S else None
    return fa.val


def _ch(S):  # now 是 fa 的哪个孩子
    fa, now = S.get('fa'), S.get('now')
    if fa is None or now is None:
        return '孩子'
    return '左孩子' if fa.left is not None and fa.left._uid == now._uid else '右孩子'


def cap_while(S, B, ret):
    if B.now is not None and B.now.val != B.key:
        return f'`{B.now.val} != {B.key}` → 继续往下找'
    return f'找到了要删除的节点 `{B.now.val}`'


def cap_cmp(S, B, ret):
    if S.now.val > S.key:
        return f'`{S.now.val} > {S.key}` → key 在左子树'
    return f'`{S.now.val} < {S.key}` → key 在右子树'


def cap_sink(S, B, ret):
    n = S.now
    if n.left or n.right:
        kids = '、'.join(x for x in [n.left and f'左 {n.left.val}', n.right and f'右 {n.right.val}'] if x)
        return f'`{n.val}` 还有孩子（{kids}）→ ==用旋转把它往下沉=='
    return f'`{n.val}` 已经是==叶子==了 → 可以直接删掉'


def cap_which(S, B, ret):
    n = S.now
    if n.left:
        return f'有左孩子 `{n.left.val}` → ==右旋==：让左孩子顶上来，`{n.val}` 沉到它的右边'
    return f'没有左孩子，有右孩子 `{n.right.val}` → ==左旋==：让右孩子顶上来，`{n.val}` 沉到它的左边'


def cap_side(S, B, ret):
    return f'`now = {S.now.val}` 是 `fa = {S.fa.val}` 的{_ch(S)}'


def text(S):
    ln = S.get('_line')
    if 'tmp' in S and S.get('_inner', {}).get('tmp') is not None and 31 <= ln <= 51:
        return f"旋转中：`now = {nv(S['now'])}`，`tmp = {nv(S['tmp'])}`，`fa = {_fa(S)}`；BST 的大小顺序始终不变"
    if 'now' not in S:
        return f"在 BST 中删除 `key = {S.get('key')}`"
    return f"`now = {nv(S['now'])}`（要删的点），`fa = {_fa(S)}`（它的父亲）"


CONFIG = dict(
    num=450, title='删除二叉搜索树中的节点', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='旋转下沉 · 把待删节点转成叶子再删',
    tags=['热题173'],
    code='''
class Solution(object):
    def deleteNode(self, root, key):
        p_head = TreeNode
        p_head.left = root

        now = root
        fa = p_head
        while now and now.val != key:
            fa = now
            if now.val > key:
                now = now.left
            else:
                now = now.right

        if not now:
            return p_head.left

        while now.left or now.right:
            if now.left:
                fa = self.rightRotate(now, fa)
            else:
                fa = self.leftRotate(now, fa)

        if fa.left == now:
            fa.left = None
        else:
            fa.right = None

        return p_head.left

    def leftRotate(self, now, fa):
        tmp = now.right
        if now == fa.left:
            fa.left = tmp
        else:
            fa.right = tmp

        now.right = tmp.left
        tmp.left = now
        return tmp

    def rightRotate(self, now, fa):
        tmp = now.left
        if now == fa.left:
            fa.left = tmp
        else:
            fa.right = tmp

        now.left = tmp.right
        tmp.right = now
        return tmp
''',
    call='Solution().deleteNode(Tr([5,3,6,2,4,None,7]), 3)',
    result_fn=tree_list,
    expect=[5, 2, 6, None, 4, None, 7],
    views=[
        dict(type='tree', label='二叉搜索树（左 < 根 < 右）', path=False, h=400,
             pointers={'now': 'blue', 'fa': 'pink', 'tmp': 'green'},
             color=lambda S, n: 'blue' if S.get('now') is not None and n._uid == S['now']._uid else None),
        dict(type='text', fn=text, size=26, h=70, lines=2),
        dict(type='calls', h=160, hide=('root',)),
    ],
    watch=[('key', 'key', 'yellow'), ('now', lambda S: S['now'].val if S.get('now') is not None else None, 'blue'),
           ('fa', _fa, 'pink'), ('tmp', lambda S: S['tmp'].val if S.get('tmp') is not None else None, 'green')],
    captions={
        'p_head = TreeNode': '哨兵 `p_head`：让根节点也有父亲（原文直接用了类 `TreeNode` 本身，没写括号）',
        'p_head.left = root': '根挂在哨兵的左边，最后返回 `p_head.left` 就是新的根',
        'now = root': '按 BST 的性质，从根开始找 `key = {key}`',
        'fa = p_head': '`fa` 始终记录 `now` 的父亲，一开始是哨兵',
        'while now and now.val != key': cap_while,
        'fa = now': '往下走之前，先记下父亲 `fa = {fa.val}`',
        'if now.val > key': cap_cmp,
        'now = now.left': '`now` → `{now.val}`',
        'now = now.right': '`now` → `{now.val}`',
        'if not now:': '`now` 不为空 → key 存在，开始删除',
        'while now.left or now.right': cap_sink,
        'if now.left:': cap_which,
        'fa = self.rightRotate': lambda S, B, ret: f'调用 `rightRotate`：`{B.now.val}` 和左孩子 `{B.now.left.val}` 交换父子关系',
        'fa = self.leftRotate': lambda S, B, ret: f'调用 `leftRotate`：`{B.now.val}` 和右孩子 `{B.now.right.val}` 交换父子关系',
        'tmp = now.left': '`tmp = {tmp.val}`：左孩子，转完后它会占据 `now` 原来的位置',
        'tmp = now.right': '`tmp = {tmp.val}`：右孩子，转完后它会占据 `now` 原来的位置',
        'if now == fa.left': cap_side,
        'fa.left = tmp': '`fa.left = {tmp.val}`：tmp 接替 now，挂到 fa 下面',
        'fa.right = tmp': '`fa.right = {tmp.val}`：tmp 接替 now，挂到 fa 下面',
        'now.left = tmp.right': lambda S, B, ret: (f'`now.left = tmp.right`（{nv(S.now.left)}）：'
                                                   f'这部分比 `{S.tmp.val}` 大、比 `{S.now.val}` 小，挂在 now 左边正合适'),
        'now.right = tmp.left': lambda S, B, ret: (f'`now.right = tmp.left`（{nv(S.now.right)}）：'
                                                   f'这部分比 `{S.now.val}` 大、比 `{S.tmp.val}` 小，挂在 now 右边正合适'),
        'tmp.right = now': '`tmp.right = now`：`{now.val}` 成了 `{tmp.val}` 的右孩子，==往下沉了一层==',
        'tmp.left = now': '`tmp.left = now`：`{now.val}` 成了 `{tmp.val}` 的左孩子，==往下沉了一层==',
        'return tmp': '返回 `tmp = {tmp.val}`：它就是 now 的==新父亲== `fa`',
        'if fa.left == now': lambda S, B, ret: f'`{S.now.val}` 是 `fa = {S.fa.val}` 的{_ch(S)}',
        'fa.left = None': '`fa.left = None`：直接摘掉叶子 `{now.val}`',
        'fa.right = None': '`fa.right = None`：直接摘掉叶子 `{now.val}`',
        'return p_head.left': '返回 `p_head.left`：删除完成，树仍然是 BST',
    },
    cards=dict(
        one_liner='用左旋 / 右旋把待删节点一路转到叶子，再直接摘掉',
        complexity='时间 `O(h)`，空间 `O(1)`（`h` 为树高）',
        problem=['给定二叉搜索树的根 `root` 和一个值 `key`，删除值为 `key` 的节点',
                 '删除后仍要保持 BST 性质，返回新的根（答案可能不唯一）',
                 '示例：`root = [5,3,6,2,4,null,7]`，`key = 3` → 删掉 3 之后仍是 BST'],
        quote='可以将待删除节点与该节点的左孩子或者右孩子==通过旋转操作进行调换==，直到待删除节点变为一个叶子节点，最后直接将该节点删除。',
        quote_src='—— yiduobo 知乎题解',
        idea=['左旋、右旋不改变 BST 的大小顺序，只把两个节点的==父子关系调换==',
              '有左孩子就右旋，否则左旋：每转一次，待删节点往下沉一层',
              '沉到叶子后，让父亲指向它的指针置空即可；哨兵 `p_head` 处理删根的情况'],
        result='返回 `[5,2,6,null,4,null,7]`：3 被转成叶子后摘掉，中序遍历仍是 `2,4,5,6,7` ✓',
        summary=['时间 `O(h)`：先找 `O(h)`，每次旋转下沉一层；空间 `O(1)`',
                 '旋转要先改 `fa` 的指针，再改 `now` 和 `tmp` 之间的指针，顺序别乱',
                 '原文 `p_head = TreeNode` 把类当哨兵（少了括号），能跑但会给类加属性，写 `TreeNode()` 更稳妥',
                 '原文为 Python 2 风格：删去了文档字符串和 TreeNode 注释，逻辑未改',
                 '常见写法是找右子树最小节点替换；旋转法不用复制值'],
    ),
)
