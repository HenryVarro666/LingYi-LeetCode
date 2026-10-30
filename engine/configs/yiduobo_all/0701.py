_ORIG = {4, 2, 7, 1, 3}


def _cmp(S, B, r):
    v = S.now.val
    if v < S.val:
        return f'`{v} < {S.val}`：`{S.val}` 应该放在 `{v}` 的==右侧=='
    return f'`{v} > {S.val}`：`{S.val}` 应该放在 `{v}` 的==左侧=='


def _child(side, word):
    def f(S, B, r):
        ch = getattr(S.now, side)
        if ch:
            return f'`{S.now.val}` 的{word}儿子是 `{ch.val}`，不空 → 继续和它比较'
        return f'`{S.now.val}` 的{word}儿子==为空== → 就插在这里'
    return f


def _info(S):
    if 'val' not in S:
        return '插入后仍要满足：左子树 < 根 < 右子树'
    return f"插入 `val = {S['val']}`：沿着查找路径往下走，走到空位就挂上去"


CONFIG = dict(
    num=701, title='二叉搜索树中的插入操作', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='BST 迭代找空位',
    tags=['labuladong', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def insertIntoBST(self, root, val):

        if not root:
            return TreeNode(val)

        now = root
        while True:
            if now.val < val:
                if now.right:
                    now = now.right
                else:
                    now.right = TreeNode(val)
                    break
            else:
                if now.left:
                    now = now.left
                else:
                    now.left = TreeNode(val)
                    break

        return root
''',
    setup='root = Tr([4,2,7,1,3])',
    call='''root = Solution().insertIntoBST(root, 5)
root = Solution().insertIntoBST(root, 6)
tree_list(root)''',
    expect=[4, 2, 7, 1, 3, 5, None, None, None, None, None, None, 6],
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='tree', label='BST（蓝 = now，绿 = 新插入的节点）', pointers={'now': 'blue'}, path=False, h=470,
             color=lambda S, node: 'green' if node.val not in _ORIG else None),
    ],
    watch=[('val', 'val', 'green'), ('now.val', lambda S: S['now'].val if S.get('now') else None, 'blue')],
    captions={
        'if not root:': '树不空，不用直接新建根',
        'now = root': '从根出发：`now = {now.val}`，要插入 `val = {val}`',
        'if now.val < val': _cmp,
        'if now.right': _child('right', '右'),
        'now = now.right': '`now` → 右儿子 `{now.val}`',
        'now.right = TreeNode': '新建节点 `{val}`，挂到 `{now.val}` 的==右边==',
        'if now.left': _child('left', '左'),
        'now = now.left': '`now` → 左儿子 `{now.val}`',
        'now.left = TreeNode': '新建节点 `{val}`，挂到 `{now.val}` 的==左边==',
        'break': '插好了，跳出循环',
        'return root': '根没有变，返回原来的 `root`',
    },
    skip=['while True'],
    cards=dict(
        one_liner='像查找一样往下走，走到空位就把新节点挂上去',
        complexity='时间 `O(h)`（h 为树高），空间 `O(1)`',
        problem=['给你二叉搜索树的根 `root` 和要插入的值 `val`（保证与树中所有值不同）',
                 '插入后返回根节点，仍需是二叉搜索树；==任意一种合法插法都可以==',
                 '本视频：在 `[4,2,7,1,3]` 中依次插入 `5`、`6`'],
        quote='若now.val小于val，说明我们需要将val插入到now的右侧。若此时now.right为空，那么now.right = Node(val)，否则继续考察now.right.val与val的关系。',
        quote_src='—— yiduobo 题解原文',
        idea=['比较 `now.val` 和 `val`，决定往右还是往左',
              '那一侧有儿子就继续往下；==没有儿子就是空位==，新节点直接挂上',
              '`while True`：值互不相同，==一定能走到空位==；新节点总是叶子'],
        summary=['时间 `O(h)`，迭代写法空间 `O(1)`',
                 '空树要特判：直接返回 `TreeNode(val)`',
                 '挂上新节点后要 `break`，否则会死循环',
                 '原文为 Python 2 风格（`class Solution(object)`），代码未改动'],
    ),
)
