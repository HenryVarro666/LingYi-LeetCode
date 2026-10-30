ROOT = [3, 4, 4, 1, None, 1, None, 0]
SUB = [4, 1]


def _v(x):
    return 'None' if x is None else str(x.val)


def _main(S):
    r, sub = S.get('root'), S.get('subRoot')
    if r is None or (sub is not None and r._uid == sub._uid):  # getHeight(subRoot) 内部：root 参数是 subRoot
        return None
    return r


def _text(S, B):
    sh = S.get('sub_height')
    if sh is None:
        return '先算 `subRoot` 的高度，只有高度相同的节点才值得比较'
    line = S.get('_line')
    if line == 30 and 'node_h' in S:
        h = S['node_h']
        return (f"`sub_height = {sh}`；节点 `{S['node'].val}` 高度 `{h}`" +
                (' = sub_height → ==比较== isSameTree' if h == sh else ' ≠ sub_height → ==跳过==，不比较'))
    return f"`sub_height = {sh}`：只在高度为 `{sh}` 的节点上调用 isSameTree"


def _cap_ret30(S, B, ret):
    h, sh, nd = S.node_h, S.sub_height, S.node
    if h != sh:
        return f'节点 `{nd.val}` 高度 `{h}` ≠ `{sh}`：==不可能匹配==，直接返回 `({h}, False)`'
    return f'节点 `{nd.val}` 高度 `{h}` = `{sh}`：调用 ==isSameTree== 和 subRoot 比一比'


def _cap_same12(S, B, ret):
    p, q = S.p, S.q
    if p is None or q is None:
        return f'`p = {_v(p)}`，`q = {_v(q)}`：有空节点'
    if p.val != q.val:
        return f'`p.val = {p.val} ≠ q.val = {q.val}` → `and` 短路，==直接返回 False=='
    return f'`p.val = q.val = {p.val}` → 还要比较左右子树'


CONFIG = dict(
    num=572, title='另一棵树的子树', difficulty='Easy', category='二叉树',
    author='灵茶山艾府', technique='只在高度相同时匹配 · O(n+m)',
    tags=['热题173'],
    code='''
class Solution:
    # 104. 二叉树的最大深度（高度）
    def getHeight(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        left_h = self.getHeight(root.left)
        right_h = self.getHeight(root.right)
        return max(left_h, right_h) + 1

    # 100. 相同的树
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if p is None or q is None:
            return p is q  # 必须都是 None
        return p.val == q.val and \\
            self.isSameTree(p.left, q.left) and \\
            self.isSameTree(p.right, q.right)

    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        sub_height = self.getHeight(subRoot)

        # 返回 node 的高度，以及是否找到了 subRoot
        def dfs(node: Optional[TreeNode]) -> Tuple[int, bool]:
            if node is None:
                return 0, False
            left_h, left_found = dfs(node.left)
            right_h, right_found = dfs(node.right)
            if left_found or right_found:
                return 0, True
            node_h = max(left_h, right_h) + 1
            return node_h, node_h == sub_height and self.isSameTree(node, subRoot)

        return dfs(root)[1]
''',
    call=f'Solution().isSubtree(Tr({ROOT}), Tr({SUB}))',
    expect=True,
    views=[
        dict(type='text', fn=_text, size=26, h=64),
        dict(type='tree', var=_main, label='root（黄圈 = 当前递归路径）', h=300,
             pointers={'node': 'blue', 'p': 'green'}),
        dict(type='tree', var='subRoot', label='subRoot', h=150, pointers={'q': 'pink'}),
        dict(type='calls', h=120, hide=('subRoot',)),
    ],
    watch=[('sub_height', 'sub_height', 'yellow'), ('node', 'node', 'blue'), ('left_h', 'left_h'), ('right_h', 'right_h'),
           ('node_h', 'node_h', 'green')],
    skip=[4, 5, 6, 7, 8, 'if node is None', 14],
    captions={
        'sub_height = self.getHeight': '先用 104 题算出 subRoot 的高度：`sub_height = 2`（getHeight 内部步骤略）',
        'return 0, False': '空节点：高度 0，没找到',
        'left_h, left_found = dfs': lambda S, B, ret: f'后序遍历：先递归左子树 `{_v(B.node.left)}`',
        'right_h, right_found = dfs': lambda S, B, ret: f'左子树高 `{B.left_h}`；再递归右子树 `{_v(B.node.right)}`',
        'if left_found or right_found': lambda S, B, ret: (
            '子树里已经找到了 → 一路返回 True' if S.left_found or S.right_found
            else f'左右子树都没找到（左高 `{S.left_h}`，右高 `{S.right_h}`）'),
        'return 0, True': '找到了，高度已经不重要，返回 `(0, True)`',
        'node_h = max': '`node_h = max({left_h}, {right_h}) + 1 = {node_h}`',
        'return node_h, node_h ==': _cap_ret30,
        'if p is None or q is None': _cap_same12,
        'return p is q': lambda S, B, ret: f'两个都是 None 才算相同 → `{ret}`',
        15: lambda S, B, ret: f'`p.val == q.val`，递归比较左子树 `({_v(B.p.left)}, {_v(B.q.left)})`',
        16: lambda S, B, ret: f'左子树相同，递归比较右子树 `({_v(B.p.right)}, {_v(B.q.right)})`',
        'return dfs(root)[1]': '从根开始后序遍历：`dfs` 返回（高度，是否找到）',
    },
    max_steps=70,
    cards=dict(
        one_liner='先算 subRoot 的高度，只在高度相同的节点上做「相同的树」判断',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['给你两棵二叉树 `root` 和 `subRoot`，判断 `root` 中是否有一棵子树与 `subRoot` ==结构和节点值都相同==',
                 '子树 = 某个节点和它的==所有后代==；`root` 本身也算',
                 '示例：`root = [3,4,5,1,2]`，`subRoot = [4,1,2]` → `true`',
                 f'本视频：`root = [3,4,4,1,null,1,null,0]`，`subRoot = {SUB}` → `true`'],
        before=[dict(heading='方法一：暴力匹配', chapter='② 思路', lines=[
            '对 `root` 的每个节点，都和 `subRoot` 跑一次 100 题「相同的树」',
            '最坏 `O(n·min(n,m))`：比如两棵全是 1 的链，每次匹配都要走很深',
            '注意：节点值一样、上面几层一样也不行，==下面多出来的节点==也要一致'])],
        quote='root 中的所有与 h_s 高度相同的节点，对应的子树两两不相交，这些子树的节点个数之和不超过 n，所以==总的匹配次数也不会超过 n==',
        quote_src='—— 灵茶山艾府题解「方法二：只在高度相同时匹配」',
        idea=['节点高度 = 到最深叶子的节点数；匹配的子树高度必须等于 `sub_height`',
              '后序遍历 `dfs` 一边算高度，一边只在 `node_h == sub_height` 时比较',
              '高度相同的节点互不为祖先 → 被比较的子树互不相交 → 总共 `O(n)`'],
        result='左边的 4 高度为 3，不比较；右边的 4 高度为 2，比较后匹配 → `True` ✓',
        summary=['时间 `O(n + m)`：`getHeight` `O(m)`，`dfs` + 所有比较 `O(n)`',
                 '`p is None or q is None` 时返回 `p is q`：必须==都==为空',
                 '找到后返回 `(0, True)`，上层看到 `found` 直接返回，不再比较',
                 '本视频的 getHeight 内部步骤已省略'],
    ),
)
