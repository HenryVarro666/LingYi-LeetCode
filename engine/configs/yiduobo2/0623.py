def _info(S):
    if 'now' not in S['_inner']:
        return f"目标：在第 `d = {S.get('d')}` 层插入一整行值为 `{S.get('v')}` 的节点（绿 = 新节点）"
    dep, d = S['_inner'].get('depth'), S['_inner'].get('d')
    if dep == d - 1:
        return f"`depth = {dep} = d - 1`：插入层就是 `now` 的==下一层== → 在这里挂新节点"
    return f"`depth = {dep} < d - 1 = {d - 1}`：还没到，继续往下一层递归"


def _cap_if_side(side, word):
    def f(S, B, ret):
        ch = getattr(B.now, side)
        if ch is not None:
            return f'`{B.now.val}` 有{word}孩子 `{ch.val}` → 递归下去，深度 `{B.depth} + 1`'
        return f'`{B.now.val}` 没有{word}孩子 → 跳过'
    return f


def _cap_depth(S, B, ret):
    if S.depth == S.d - 1:
        return f'`depth = {S.depth}` 等于 `d - 1 = {S.d - 1}` → ==当前节点下面就是要插入的那一层=='
    return f'`depth = {S.depth}` 还不到 `d - 1 = {S.d - 1}` → 继续往下找'


CONFIG = dict(
    num=623, title='在二叉树中增加一行', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='带深度递归 · 到 d-1 层就地插入',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def addOneRow(self, root, v, d):
        if d == 1:
            tmp = TreeNode(v)
            tmp.left = root
            return tmp

        self.dfs(root, 1, v, d)
        return root

    def dfs(self, now, depth, v, d):
        if depth == d - 1:
            tmp = TreeNode(v)
            tmp.left = now.left
            now.left = tmp
            tmp = TreeNode(v)
            tmp.right = now.right
            now.right = tmp
        else:
            if now.left:
                self.dfs(now.left, depth + 1, v, d)
            if now.right:
                self.dfs(now.right, depth + 1, v, d)
''',
    call='Solution().addOneRow(Tr([4, 2, 6, 3, 1, 5]), 7, 3)',
    expect=[4, 2, 6, 7, 7, 7, 7, 3, None, None, 1, 5],
    result_fn=tree_list,
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='tree', label='二叉树（蓝 = now，紫 = tmp，绿 = 新插入的节点）',
             pointers={'now': 'blue', 'tmp': 'purple'},
             color=lambda S, n: 'green' if n.val == 7 else None, h=420),
        dict(type='calls', h=170, hide=('v', 'd')),
    ],
    watch=[('depth', lambda S: S['_inner'].get('depth'), 'yellow'), ('d - 1', lambda S: S['d'] - 1 if 'd' in S else None, 'cyan'),
           ('now', lambda S: S['_inner']['now'].val if 'now' in S['_inner'] else None, 'blue')],
    captions={
        'if d == 1': '`d = {d}`：如果插在第 1 层，新节点要当==新根==，单独处理；这里不是',
        'self.dfs(root, 1, v, d)': '从根出发，带上==当前深度== `1` 往下递归',
        'if depth == d - 1': _cap_depth,
        13: '新建节点 `{v}`：它要插到 `{now.val}` 的==左边==',
        16: '再新建一个 `{v}`：它要插到 `{now.val}` 的==右边==',
        'tmp.left = now.left': lambda S, B, r: (f'新节点的==左孩子==先接住 `{S.now.val}` 原来的左子树 `{S.tmp.left.val}`'
                                                if S.tmp.left else f'`{S.now.val}` 原来没有左子树，新节点左边为空'),
        'now.left = tmp': '`now.left = tmp`：新节点插到 `{now.val}` 和原左子树之间',
        'tmp.right = now.right': lambda S, B, r: (f'新节点的==右孩子==接住 `{S.now.val}` 原来的右子树 `{S.tmp.right.val}`'
                                                  if S.tmp.right else f'`{S.now.val}` 原来没有右子树 → 新节点右边为空'),
        'now.right = tmp': '`now.right = tmp`：`{now.val}` 下面这一层插好了，==无须再往下递归==',
        'if now.left:': _cap_if_side('left', '左'),
        'if now.right:': _cap_if_side('right', '右'),
        'self.dfs(now.left': lambda S, B, r: f'进入左孩子 `{S.now.val}`（深度 `{S.depth}`）',
        'self.dfs(now.right': lambda S, B, r: f'进入右孩子 `{S.now.val}`（深度 `{S.depth}`）',
        'return root': '根没变，返回 `root`：第 `{d}` 层已整行变成 `{v}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='带着深度往下递归，走到 d-1 层就把新节点“夹”进去',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['给二叉树 `root`、值 `val`、深度 `depth`（根在第 1 层）',
                 '在第 `depth` 层插入一整行值为 `val` 的节点：',
                 '原来的左子树挂到新节点的==左边==，右子树挂到新节点的==右边==',
                 '`depth = 1` 时新节点当根，原树当它的左子树',
                 '本视频：`[4,2,6,3,1,5]`，`val = 7`，`depth = 3`'],
        quote='若当前节点的深度为d - 1，说明需要插入的层就是当前节点的下一层，于是可以新建两个节点left和right……==由于再往下的树结构就不会产生变化了，因此无须继续往下递归。==',
        quote_src='—— yiduobo 题解原文',
        idea=['从根开始带上深度递归：`depth < d - 1` 就往左右孩子走，深度 + 1',
              '`depth == d - 1`：新建两个节点，左的接原左子树、右的接原右子树',
              '插完直接停：更深的结构不变；`d == 1` 时新节点当新根'],
        result='第 3 层整行插入 `7`，返回 `[4,2,6,7,7,7,7,3,null,null,1,5]`',
        summary=['时间 `O(n)`：最多只访问前 `d-1` 层；空间 `O(h)`',
                 '易错：`d == 1` 要特判（新节点成为根，原树挂在它的==左边==）',
                 '易错：新节点要先接上原子树，再挂到 `now` 下面，否则原子树会丢',
                 '也可以用 BFS 走到第 `d-1` 层，对整层统一插入',
                 '原文为 Python 2 风格：删去了文档字符串与模板注释；参数名 `v, d` 即新版的 `val, depth`'],
    ),
)
