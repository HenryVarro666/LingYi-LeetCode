VALS = [4, 2, 6, 1, 3]
SORTED = sorted(v for v in VALS if v is not None)


def f(x):
    return '∞' if x == inf else ('-∞' if x == -inf else str(x))


def nv(x):
    return '空' if x is None else f'`{x.val}`'


def _pre(S):
    return S.get('pre', -inf)


PRE_IDX = lambda S: SORTED.index(S['pre']) if S.get('pre', -inf) in SORTED else None   # noqa: E731


def _seq_color(S, i, v):
    p = _pre(S)
    if v < p:
        return 'green'
    if v == p:
        return 'cyan'
    return None


def _diff_text(S):
    if 'ans' not in S:
        return ''
    node = S.get('node')
    if S.get('_line') == 11 and node is not None:
        return f"`node.val − pre` = `{node.val} − {f(S['pre'])}` = `{f(node.val - S['pre'])}` → `ans = {f(S['ans'])}`"
    return f"中序遍历是有序的：只需比较==相邻==两个数。`pre = {f(_pre(S))}`，`ans = {f(S['ans'])}`"


def _if(S, B, ret):
    if B.node is None:
        return '空节点 → 直接返回'
    return f'节点 `{B.node.val}`：中序遍历 = 左子树 → 根 → 右子树'


def _ans(S, B, ret):
    v, p = S.node.val, B.pre
    if p == -inf:
        return f'左子树走完，轮到 `{v}`：它是中序第一个数，`{v} − (−∞) = ∞`，`ans` 仍是 `∞`'
    return f'轮到 `{v}`：和中序的上一个数 `{p}` 相减 → `{v - p}`；`ans = min({f(B.ans)}, {v - p})` = =={S.ans}=='


CONFIG = dict(
    num=530, title='二叉搜索树的最小绝对差', difficulty='Easy', category='二叉树',
    author='灵茶山艾府', technique='中序遍历 · 相邻两数之差',
    tags=['面试经典150'],
    code='''
class Solution:
    def getMinimumDifference(self, root: Optional[TreeNode]) -> int:
        ans = inf
        pre = -inf

        def dfs(node: Optional[TreeNode]) -> None:
            if node is None:
                return
            dfs(node.left)
            nonlocal ans, pre
            ans = min(ans, node.val - pre)
            pre = node.val
            dfs(node.right)

        dfs(root)
        return ans
''',
    call=f'Solution().getMinimumDifference(Tr({VALS}))',
    expect=1,
    skip=[8],
    views=[
        dict(type='text', fn=_diff_text, h=60),
        dict(type='tree', h=270, pointers={'node': 'blue'},
             color=lambda S, n: 'green' if n.val < _pre(S) else ('cyan' if n.val == _pre(S) else None),
             label='BST（青 = pre，绿 = 已按中序访问过）'),
        dict(type='array', var=lambda S: SORTED, label='中序遍历序列 = 排好序的数组', cell=80, h=185,
             pointers={PRE_IDX: 'cyan'}, pointer_labels={PRE_IDX: 'pre'}, color=_seq_color),
        dict(type='calls', h=165, label='调用栈'),
    ],
    watch=[('node', 'node', 'blue'), ('pre', 'pre', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = inf': '`ans` 记录最小差值，先设为 `∞`',
        'pre = -inf': '`pre`：中序遍历中==上一个==节点的值，先设为 `-∞`',
        'if node is None': _if,
        'dfs(node.left)': lambda S, B, r: f'先递归左子树 {nv(B.node.left)}',
        'ans = min(ans, node.val - pre)': _ans,
        'pre = node.val': '`pre = {pre}`：下一个访问的节点要和它比',
        'dfs(node.right)': lambda S, B, r: f'再递归右子树 {nv(B.node.right)}',
        'dfs(root)': '从根开始中序遍历',
        'return ans': '中序相邻两数之差的最小值 → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='BST 的中序遍历是有序的，最小差值一定出现在相邻两数之间',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['给二叉搜索树的根节点 `root`，返回==任意两不同节点值之差的最小值==（正数）',
                 '示例 1：`root = [4,2,6,1,3]` → `1`',
                 '示例 2：`root = [1,0,48,null,null,12,49]` → `1`'],
        quote='最小差值一定是相邻两个数的差值。由于二叉搜索树的==中序遍历得到的序列是有序的==，我们可以计算中序遍历中的相邻两数的差值，取最小值，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['中序遍历：左子树 → 根 → 右子树，BST 上得到的是==升序序列==',
              '用 `pre` 记住上一个访问的数，访问 `node` 时算 `node.val − pre`',
              '`pre` 初始为 `-∞`：第一个数算出 `∞`，不会影响答案'],
        summary=['时间 `O(n)`；空间 `O(n)`，最坏情况树退化成链',
                 '因为有序，差值 `node.val − pre` 一定为正，==不用取绝对值==',
                 '易错：`ans`、`pre` 要在 `dfs` 里声明 `nonlocal`',
                 '本题与 783 相同；同类题见二叉树题单 §2.9 二叉搜索树'],
    ),
)
