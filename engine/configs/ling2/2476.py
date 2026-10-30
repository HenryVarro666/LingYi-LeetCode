VALS = [6, 2, 13, 1, 4, 9, 15]
QS = [2, 5, 16]


def _q_phase(S):
    return 'q' in S and S.get('_line', 0) >= 15


def _mn_mx(S):
    """当前询问已经算出来的 mn / mx（值）"""
    out = {}
    if not _q_phase(S):
        return out
    if 'mx' in S and S.get('_line', 0) >= 16:
        out['mx'] = S['mx']
    if 'mn' in S and S.get('_line', 0) >= 19:
        out['mn'] = S['mn']
    return out


def _tree_color(S, nd):
    if _q_phase(S):
        mm = _mn_mx(S)
        if nd.val == mm.get('mn'):
            return 'blue'
        if nd.val == mm.get('mx'):
            return 'pink'
        return None
    return 'green' if nd.val in (S.get('a') or []) else None


def _a_color(S, k, v):
    mm = _mn_mx(S)
    if v == mm.get('mn') and v == mm.get('mx'):
        return 'purple'
    if v == mm.get('mn'):
        return 'blue'
    if v == mm.get('mx'):
        return 'pink'
    return None


def _text(S):
    if not _q_phase(S):
        return '中序遍历（左 → 根 → 右）：二叉搜索树会得到==严格递增==的数组'
    q, j, a = S['q'], S.get('j'), S['a']
    mm = _mn_mx(S)
    s = f'询问 `q = {q}`'
    if 'mx' in mm:
        s += f'；max = 大于等于 q 的最小值 = `{mm["mx"]}`'
    if 'mn' in mm:
        s += f'；min = 小于等于 q 的最大值 = `{mm["mn"]}`'
    return s


def _cap_j(S, B, ret):
    j, n, q = S.j, S.n, S.q
    if j == n:
        return f'`j = bisect_left(a, {q}) = {j} = n`：所有数都 `< {q}`'
    return f'`j = bisect_left(a, {q}) = {j}`：`a[{j}] = {S.a[j]}` 是第一个 `≥ {q}` 的数'


def _cap_if(S, B, ret):
    j, n, q, a = B.j, B.n, B.q, B.a
    if j == n:
        return '`j == n`：小于等于 q 的最大值只能是 `a[j-1]`'
    if a[j] != q:
        return f'`a[{j}] = {a[j]} ≠ {q}`：说明 `a[{j}] > q`、`a[{j - 1}] < q` → 往左挪一位'
    return f'`a[{j}] == {q}`：q 就在树里，min 也是它'


CONFIG = dict(
    num=2476, title='二叉搜索树最近节点查询', difficulty='Medium', category='二分查找',
    author='灵茶山艾府', technique='中序遍历 + 二分查找',
    tags=['字节30天'],
    code='''
class Solution:
    def closestNodes(self, root: Optional[TreeNode], queries: List[int]) -> List[List[int]]:
        a = []
        def dfs(node: Optional[TreeNode]) -> None:
            if node is None:
                return
            dfs(node.left)
            a.append(node.val)
            dfs(node.right)
        dfs(root)

        n = len(a)
        ans = []
        for q in queries:
            j = bisect_left(a, q)
            mx = a[j] if j < n else -1
            if j == n or a[j] != q:  # a[j]>q, a[j-1]<q
                j -= 1
            mn = a[j] if j >= 0 else -1
            ans.append([mn, mx])
        return ans
''',
    call=f'Solution().closestNodes(Tr({VALS}), {QS})',
    expect=[[2, 2], [4, 6], [15, -1]],
    skip=['if node is None', 6],
    views=[
        dict(type='tree', label='二叉搜索树（绿 = 已加入 a；询问时 蓝 = min，粉 = max）', h=300,
             pointers={'node': 'yellow'}, color=_tree_color),
        dict(type='array', var='a', label='a（中序遍历结果，严格递增）', cell=84, pointers={'j': 'yellow'},
             color=_a_color),
        dict(type='text', fn=_text, h=56, size=24),
        dict(type='stack', var='ans', label='ans', fmt=lambda x: f'[{x[0]},{x[1]}]', h=96),
    ],
    watch=[('q', 'q', 'cyan'), ('j', 'j', 'yellow'), ('mn', 'mn', 'blue'), ('mx', 'mx', 'pink')],
    captions={
        'a = []': '`a` 收集中序遍历的结果',
        'dfs(node.left)': lambda S, B, r: f'`{B.node.val}`：先遍历左子树',
        'a.append(node.val)': '左子树走完，记录 `{node.val}` → `a = {a}`',
        'dfs(node.right)': lambda S, B, r: f'`{B.node.val}`：再遍历右子树',
        'dfs(root)': '中序遍历整棵树：==二叉搜索树的中序遍历是严格递增的==',
        'n = len(a)': '`a` 有序 → 每个询问在 `a` 上==二分查找==，`O(log n)`（树不一定平衡，直接在树上找最坏 `O(n)`）',
        'ans = []': '`ans` 存每个询问的 `[min, max]`',
        'for q in queries': lambda S, B, r: (f'询问 `q = {S.q}`' if 'q' not in B or S.q != B.q else '询问处理完'),
        'j = bisect_left(a, q)': _cap_j,
        'mx = a[j] if j < n else -1': lambda S, B, r: (
            f'`j < n` → max = `a[{S.j}]` = =={S.mx}==' if S.mx != -1 else '`j == n`：没有 `≥ q` 的数 → max = ==-1=='),
        'if j == n or a[j] != q': _cap_if,
        'j -= 1': '`j` → `{j}`',
        'mn = a[j] if j >= 0 else -1': lambda S, B, r: (
            f'min = `a[{S.j}]` = =={S.mn}==' if S.mn != -1 else '`j < 0`：没有 `≤ q` 的数 → min = ==-1=='),
        'ans.append([mn, mx])': '`[{mn}, {mx}]` 加入答案',
        'return ans': '返回 `{ret}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='中序遍历得到有序数组，每个询问二分找第一个 ≥ q 的数',
        complexity='时间 `O(n + q log n)`，空间 `O(n)`',
        problem=['给二叉搜索树 `root` 和询问数组 `queries`，对每个 `q` 求 `[min, max]`',
                 '`min`：树中 ==≤ q 的最大值==；`max`：树中 ==≥ q 的最小值==；不存在用 `-1`',
                 '示例：`[6,2,13,1,4,9,15,null,…,14]`，`[2,5,16]` → `[[2,2],[4,6],[15,-1]]`',
                 '本视频去掉了节点 14：`[6,2,13,1,4,9,15]`，答案不变'],
        quote='题目没说二叉搜索树是==平衡==的，最坏情况下这棵树是一条链……可以通过一次中序遍历得到一个==严格递增==数组 a，再在 a 上做二分查找。',
        quote_src='—— 灵茶山艾府题解',
        idea=['设 `j` 是第一个 `≥ q` 的数的下标（不存在则 `j = n`）：`j < n` 时 max = `a[j]`，否则 -1',
              '`a[j] == q` 时 min = `a[j]`；否则 min = `a[j-1]`（`j = 0` 时为 -1）',
              '代码里统一成：不相等就 `j -= 1`，再看 `j >= 0`'],
        result='`[[2,2],[4,6],[15,-1]]` ✓',
        summary=['时间 `O(n + q log n)`：中序遍历 `O(n)`，每个询问二分 `O(log n)`',
                 '为什么不直接在树上找？树==不一定平衡==，最坏退化成链，单次 `O(n)`',
                 '易错：`j == n` 时不能访问 `a[j]`，要先判断',
                 '`bisect_left` 返回第一个 `≥ q` 的位置，是二分查找的标准用法'],
    ),
)
