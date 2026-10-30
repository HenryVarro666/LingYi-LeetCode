import views as V

K0 = 3
INORDER = [1, 2, 3, 4, 5, 6]  # BST 的中序遍历 = 节点值从小到大


def _counted(S):
    k = S.get('k', K0)
    return K0 - k if isinstance(k, int) else 0


def _cyc_root(S):
    """rightest.right = now 之后、now.left = None 之前，树里有一个环（没有"无父节点"的根），这时以 now 为根来画"""
    now = S.get('now')
    if now is None:
        return None
    seen, st = set(), [now.left, now.right]
    while st:
        n = st.pop()
        if n is None or n._uid in seen:
            continue
        if n._uid == now._uid:
            return now
        seen.add(n._uid)
        st += [n.left, n.right]
    return None


def tree_view(**spec):
    """迭代写法没有递归路径：画树时不传调用栈参数，避免把 root 误标成"递归路径" """
    def draw(cv, S, B, box, T):
        V.v_tree(cv, spec, {'_S': S, '_B': B, '_frames': [dict(args=[], locals=S)]}, box, 0, {})
    return dict(type='custom', draw=draw, h=spec.get('h', 380))


def _cap_if_left(S, B, ret):
    now = B['now']
    if now.left is not None:
        return f'`{now.val}` 有左子树：比它小的还没数 → 先把左子树「拉」到它前面'
    return f'`{now.val}` 没有左子树 → ==它就是剩下的节点里最小的==，数它'


def _cap_while_r(S, B, ret):
    r = B['rightest']
    if r.right is not None:
        return f'`{r.val}` 还有右儿子 → 继续往右走'
    return f'`{r.val}` 没有右儿子 → 它是==左子树最右边的节点==，中序里紧挨在 `{B["now"].val}` 前面'


def _cap_k0(S, B, ret):
    if S['k'] == 0:
        return f'`k == 0`：`{S["now"].val}` ==就是第 {K0} 小==，返回'
    return f'`k = {S["k"]}`，还没数够 {K0} 个，继续'


CONFIG = dict(
    num=230, title='二叉搜索树中第 K 小的元素', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='改树结构的一趟中序遍历（拉直左子树）',
    code='''
class Solution(object):
    def kthSmallest(self, root, k):
        now = root
        while now:
            if now.left:
                rightest = now.left
                while rightest.right:
                    rightest = rightest.right
                rightest.right = now
                tmp = now.left
                now.left = None
                now = tmp

            else:
                k -= 1
                if k == 0:
                    return now.val
                now = now.right
''',
    call='Solution().kthSmallest(Tr([5,3,6,2,4,None,None,1]), 3)',
    expect=3,
    views=[
        dict(type='array', var=lambda S: INORDER, label='中序遍历序列（BST → 从小到大，绿 = 已数过）', cell=60,
             color=lambda S, i, v: ('orange' if i == K0 - 1 and _counted(S) == K0 else 'green') if i < _counted(S) else None),
        tree_view(var=_cyc_root, label='二叉树（结构会被修改）', h=470,
                  pointers={'now': 'blue', 'rightest': 'pink', 'tmp': 'purple'},
                  color=lambda S, n: ('orange' if n.val == INORDER[K0 - 1] and _counted(S) == K0 else 'green') if n.val in INORDER[:_counted(S)] else None),
    ],
    watch=[('k', 'k', 'yellow'), ('now', 'now', 'blue'), ('rightest', 'rightest', 'pink'), ('tmp', 'tmp', 'purple')],
    captions={
        'while now:': lambda S, B, ret: (f'`now = {B["now"].val}` 不为空，继续遍历' if B['now'] is not None else '`now` 为空 → 遍历结束'),
        'if now.left:': _cap_if_left,
        'rightest = now.left': '从左儿子 `{rightest.val}` 出发，找左子树里最右边的节点',
        'while rightest.right:': _cap_while_r,
        'rightest = rightest.right': '往右走到 `{rightest.val}`',
        'rightest.right = now': '把 `{now.val}` 接到 `{rightest.val}` 的右边：==中序里 {rightest.val} 后面本来就是 {now.val}==，顺序不变',
        'tmp = now.left': '记下左儿子 `{tmp.val}`，等会儿从它继续',
        'now.left = None': '砍掉 `{now.val}` 的左指针：左子树已经接到它前面了，==不砍会死循环==',
        'now = tmp': '`now` 移到 `{now.val}`：它现在是最上面的节点，左子树又少了一层',
        'now = root': '`now` 从根 `{now.val}` 出发',
        'k -= 1': lambda S, B, ret: f'数一个：`{S["now"].val}` 是第 `{K0 - S["k"]}` 小，`k` 从 {B["k"]} 减到 =={S["k"]}==',
        'if k == 0': _cap_k0,
        'return now.val': '返回答案 =={ret}==',
        'now = now.right': lambda S, B, ret: ('中序的下一个就在右边：`now` → ' + (f'`{S["now"].val}`' if S['now'] is not None else '`None`')),
    },
    skip=['while now:'],
    max_steps=60,
    cards=dict(
        one_liner='把左子树一层层「拉直」到右边，树变成链，顺着数到第 k 个',
        complexity='时间 `O(n)`，额外空间 `O(1)`（会修改树）',
        problem=['给一棵==二叉搜索树==的根 `root` 和整数 `k`，求第 `k` 小的节点值（k 从 1 开始）',
                 'BST：左子树的值 < 根 < 右子树的值',
                 '示例：`root = [5,3,6,2,4,null,null,1]`，`k = 3` → `3`'],
        quote='题目要求bst中第k小的元素，可以看成==求bst中序遍历结果的第k个元素==，于是可以参照之前94题的做法，==修改树的结构然后一趟遍历==就行了。',
        quote_src='—— yiduobo 知乎题解',
        idea=['`now` 有左子树：找到左子树==最右边的节点==，它在中序里正好排在 `now` 前面',
              '把 `now` 接到它的右边，再砍掉 `now.left` → 中序顺序不变，左子树少了一层',
              '`now` 没有左子树 → 它就是剩下最小的：`k -= 1`，减到 0 即答案，否则往右走'],
        summary=['时间 `O(n)`，不用递归栈，额外空间 `O(1)`；代价是==树的结构被改掉了==',
                 '易错：`rightest.right = now` 之后要 `now.left = None`，否则死循环',
                 '进阶（频繁增删 + 查询）：每个节点维护子树大小，比较 `k` 与左子树节点数，每次 `O(h)`',
                 '原文为 Python 2 风格（类型说明写在文档字符串里），已删去文档字符串，代码未改'],
    ),
)
