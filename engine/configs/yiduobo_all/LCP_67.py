def nv(x):
    return '空' if x is None else str(x.val)


def cap_if_l(S, B, ret):
    n = S.now
    if n.left is None:
        return f'`now = {n.val}` 没有左孩子 → 左边不用处理'
    if n.left.val == -1:
        return f'`now = {n.val}` 左边已经隔了一个 `-1`，原来的左子树在 `-1.left` 下'
    return f'`now = {n.val}` 有左孩子 `{n.left.val}` → 要在它们中间插入一个 `-1`'


def cap_if_r(S, B, ret):
    n = S.now
    if n.right is None:
        return f'`now = {n.val}` 没有右孩子 → 右边不用处理'
    if n.right.val == -1:
        return f'`now = {n.val}` 右边已经隔了一个 `-1`，原来的右子树在 `-1.right` 下'
    return f'`now = {n.val}` 有右孩子 `{n.right.val}` → 同样要插入 `-1`'


CONFIG = dict(
    num='LCP 67', title='装饰树', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='DFS · 先递归再插入节点',
    tags=['灵神核心路线', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def expandBinaryTree(self, root):

        def dfs(now):
            if now.left:
                node = TreeNode(-1)
                dfs(now.left)
                node.left = now.left
                now.left = node
            
            if now.right:
                node = TreeNode(-1)
                dfs(now.right)
                node.right = now.right
                now.right = node
        
        dfs(root)
        return root
''',
    call='''s = Solution()
s.tree = Tr([7,5,6,3])
s.expandBinaryTree(s.tree)''',
    expect=[7, -1, -1, 5, None, None, 6, -1, None, None, None, 3],
    result_fn=tree_list,
    views=[
        dict(type='tree', label='二叉树（绿 = 新插入的 -1 节点）', pointers={'now': 'blue'}, h=400,
             color=lambda S, n: 'green' if n.val == -1 else None),
        dict(type='calls', h=200),
    ],
    watch=[('now', 'now', 'blue'), ('node', lambda S: nv(S['_inner'].get('node')) if S['_inner'].get('node') else None, 'green'),
           ('now.left', lambda S: nv(S['_inner'].get('now').left) if S['_inner'].get('now') else None),
           ('now.right', lambda S: nv(S['_inner'].get('now').right) if S['_inner'].get('now') else None)],
    captions={
        'if now.left': cap_if_l,
        'if now.right': cap_if_r,
        'node = TreeNode(-1)': '新建灯饰节点 `node = -1`，先不接，等子树处理完再插',
        'dfs(now.left)': '先把 `now.left` 这棵子树自己处理好（它内部的父子之间也要插）',
        'dfs(now.right)': '先把 `now.right` 这棵子树自己处理好',
        'node.left = now.left': '`-1` 的左孩子接上原来的左子树 `{now.left.val}`',
        'now.left = node': '`now.left` 换成 `-1`：`{now.val} → -1 → 原左孩子`，插入完成',
        'node.right = now.right': '`-1` 的右孩子接上原来的右子树 `{now.right.val}`',
        'now.right = node': '`now.right` 换成 `-1`：`{now.val} → -1 → 原右孩子`，插入完成',
        'dfs(root)': '从根节点开始向下 dfs',
        'return root': '全部处理完，根节点没变，返回 `root`',
    },
    cards=dict(
        one_liner='每个父子之间插一个 `-1`：先递归子树，再挂接',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['给二叉树 `root`，在每对父子节点之间插入值为 `-1` 的节点',
                 '插在左孩子上方的 `-1` 做左孩子，右边同理',
                 '示例：`[7,5,6]` → `[7,-1,-1,5,null,null,6]`'],
        quote='对于当前节点now，若now.left非空，那么递归求解now.left，然后构造一个值为-1的节点node，将node.left置为now.left，然后将now.left置为node即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['从根向下 `dfs(now)`，只看当前节点和它的两个孩子',
              '有左孩子：新建 `node`，递归左孩子，`node.left = now.left`，`now.left = node`',
              '有右孩子：同样处理，只是挂在 `node.right`'],
        summary=['时间 `O(n)`：每个节点处理一次；空间 `O(h)`',
                 '易错：必须先接 `node.left = now.left`，再改 `now.left`，顺序反了会丢子树',
                 '叶子节点两个孩子都为空，什么也不做',
                 '原文代码未改动（本来就是 Python 3 可运行）'],
    ),
)
