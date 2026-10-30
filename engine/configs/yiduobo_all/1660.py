def _qvals(S):
    return [n.val for n in S['q']] if 'q' in S else []


def _nv(x):
    return '空' if x is None else str(x.val)


def _cap_for(S, B, ret):
    return f'扫描当前层 `q[{S.head}:{S.tail}]`：取出节点 `{S.now.val}`，检查它的==孩子==是否是错误节点'


def _cap_right(S, B, ret):
    if S.now.right is None:
        return f'取当前层 `q[{S.head}:{S.tail}]` 的节点 `{S.now.val}`：没有右孩子 → 跳过右边'
    return f'取当前层 `q[{S.head}:{S.tail}]` 的节点 `{S.now.val}`：有右孩子 `{S.now.right.val}` → 先检查它（检查的是==孩子==）'


def _cap_left(S, B, ret):
    if S.now.left is None:
        return f'`{S.now.val}` 没有左孩子 → 跳过左边'
    return f'`{S.now.val}` 有左孩子 `{S.now.left.val}` → 再检查左孩子'


def _cap_bad_r(S, B, ret):
    c = S.now.right
    r = c.right
    if r is None:
        return f'右孩子 `{c.val}` 没有右指针 → 正常'
    if r.val in S.vis:
        return f'`{c.val}.right` 指向 `{r.val}`，而 `{r.val}` ==已经被指过一次（在 vis 里）== → `{c.val}` 是错误节点'
    return f'`{c.val}.right` 指向 `{r.val}`，`vis` 里还没有它 → 正常'


def _cap_bad_l(S, B, ret):
    c = S.now.left
    r = c.right
    if r is None:
        return f'左孩子 `{c.val}` 没有右指针 → 正常'
    if r.val in S.vis:
        return f'`{c.val}.right` 指向 `{r.val}`，而 `{r.val}` ==已经被指过一次（在 vis 里）== → `{c.val}` 是错误节点'
    return f'`{c.val}.right` 指向 `{r.val}`，`vis` 里还没有它 → 正常'


CONFIG = dict(
    num=1660, title='纠正二叉树', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='层序遍历 · 从右往左 + 集合',
    tags=['灵神题单·链表树与回溯'],
    setup='''
n1, n2, n3, n4, n5 = [TreeNode(v) for v in (1, 2, 3, 4, 5)]
n1.left, n1.right = n2, n3
n2.left = n4
n3.left = n5
n4.right = n5
''',
    code='''
class Solution(object):
    def correctBinaryTree(self, root):

        vis = set([root.val])
        head, tail = 0, 1
        q = [root]
        while head < tail:
            for now in q[head : tail]:
                if now.right:
                    if now.right.right and now.right.right.val in vis:
                        now.right = None
                        return root
                    
                    q.append(now.right)
                    vis.add(now.right.val)
                
                if now.left:
                    if now.left.right and now.left.right.val in vis:
                        now.left = None
                        return root
                
                    q.append(now.left)
                    vis.add(now.left.val)
            
            head, tail = tail, len(q)
''',
    call='Solution().correctBinaryTree(n1)',
    expect=[1, 2, 3, None, None, 5],
    result_fn=tree_list,
    views=[
        dict(type='tree', label='二叉树（蓝 = now；4 的右指针错指到 5）', pointers={'now': 'blue'}, path=False, h=300,
             color=lambda S, n: 'green' if n.val in S.get('vis', ()) else None),
        dict(type='array', var=_qvals, label='队列 q（q[head:tail] 是当前层）',
             pointers={'head': 'green', 'tail': 'pink'}, cell=64, h=130),
        dict(type='set', var='vis', label='vis（已被指向过的节点值）', h=110),
    ],
    watch=[('head', 'head', 'green'), ('tail', 'tail', 'pink'), ('now', lambda S: S['now'].val if 'now' in S else None, 'blue')],
    skip=['for now in q'],
    captions={
        'vis = set': '`vis` 记录==已经被指向过==的节点值（根没有父亲，先放进去）',
        'head, tail = 0, 1': '`q[head:tail]` 是当前层，现在只有根',
        'q = [root]': '队列用列表实现，从根开始层序遍历',
        'while head < tail': '`head < tail` → 当前层非空，继续',
        'for now in q': _cap_for,
        'if now.right:': _cap_right,
        'if now.right.right and': _cap_bad_r,
        'now.right = None': '==直接把错误节点从父亲那里删掉==（连同它的子树），返回 `root`',
        'q.append(now.right)': '右孩子正常 → 入队，下一层也从右往左处理',
        'vis.add(now.right.val)': '右孩子 `{now.right.val}` 被 `{now.val}` 指向了 → 记入 `vis`：`{vis}`',
        'if now.left:': _cap_left,
        'if now.left.right and': _cap_bad_l,
        'now.left = None': '==删掉错误的左孩子==（它的右指针指向了同层右侧已被指过的节点），返回 `root`',
        'q.append(now.left)': '左孩子正常 → 入队',
        'vis.add(now.left.val)': '左孩子 `{now.left.val}` 被 `{now.val}` 指向了 → 记入 `vis`：`{vis}`',
        'head, tail = tail': '本层处理完：下一层是 `q[{head}:{tail}]`',
        'return root': '已纠正，返回 `root`',
    },
    cards=dict(
        one_liner='层序遍历从右往左，右指针指向已见节点的就是错误节点',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二叉树里有一个错误节点：它的==右孩子指针==错指到了同一层、更右边的另一个节点',
                 '要求删除这个错误节点以及它的子树（但不删被它错指的那个节点），返回根',
                 '本视频：`4.right` 错指到 `5`，删掉 `4` 后得到 `[1,2,3,null,null,5]`'],
        quote='每一层应该从右向左执行，理由是题目是要找出发出错误指针的节点，而不是被错误指针指向的节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['从右往左：被指向的节点（在右边）会==先入集合==，再轮到发出错误指针的节点',
              '检查的是==孩子==：`孩子.right` 的值已在 `vis` 里 → 孩子是错误节点',
              '发现后直接 `now.left/right = None` 删掉孩子，就等于删掉了整棵子树',
              '节点值互不相同，所以可以用值的集合判重'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：必须从右往左，否则只能知道“某节点被指两次”，反查不到谁发出的指针',
                 '易错：检查孩子而不是自己，才能直接把孩子置空',
                 '先检查右孩子再检查左孩子；`vis` 在入队时同步加入',
                 '原文为 Python 2 风格，本题代码无需修改，直接在 Python 3 运行'],
    ),
)
