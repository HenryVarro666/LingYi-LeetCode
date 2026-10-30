VALS = [1, 2, 3, 4, 5, 6, 7]
N, X = 7, 2


def _col(S, n):
    if n.val == S.get('x'):
        return 'orange'
    return None


def _after(S, B, r):
    ls, rs = S['ls'], S['rs']
    n = S.get('n') or N
    return f'节点 `{S.node.val}` 的左子树 `{ls}`、右子树 `{rs}`'


def _info(S):
    if 'lsz' not in S:
        return '一号选了 `x`：以 `x` 为根，三个邻居各对应一棵子树（左、右、父）'
    lsz, rsz = S['lsz'], S['rsz']
    n = S['n']
    if lsz == 0 and rsz == 0:
        return f'还没遇到 `x = {S["x"]}`，`lsz = rsz = 0`'
    par = n - 1 - lsz - rsz
    return f'`x = {S["x"]}`：左 `{lsz}`、右 `{rsz}`、父 `n−1−lsz−rsz = {par}` → 二号最多染 ==`{max(lsz, rsz, par)}`=='


CONFIG = dict(
    num=1145, title='二叉树着色游戏', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='x 切出三棵子树 · 取最大 · DFS 求子树大小',
    tags=['灵神题单·贪心与思维', '灵神题单·链表树与回溯', '难度分 1741'],
    code='''
class Solution:
    def btreeGameWinningMove(self, root: Optional[TreeNode], n: int, x: int) -> bool:
        lsz = rsz = 0
        def dfs(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0
            ls = dfs(node.left)
            rs = dfs(node.right)
            if node.val == x:
                nonlocal lsz, rsz
                lsz, rsz = ls, rs
            return ls + rs + 1
        dfs(root)
        return max(lsz, rsz, n - 1 - lsz - rsz) * 2 > n
''',
    setup=f'root = Tr({VALS})',
    call=f'Solution().btreeGameWinningMove(root, {N}, {X})',
    expect=True,
    skip=['lsz = rsz = 0', 'nonlocal', 'dfs(root)'],
    max_steps=75,
    views=[
        dict(type='tree', var='root', label='二叉树（橙 = 一号选的 x，黄圈 = 当前递归路径）', pointers={'node': 'blue'}, h=330, color=_col),
        dict(type='text', h=80, size=28, fn=_info),
        dict(type='calls', h=200),
    ],
    watch=[('x', 'x', 'orange'), ('lsz', 'lsz', 'blue'), ('rsz', 'rsz', 'pink'),
           ('ls', lambda S: S['_inner'].get('ls')), ('rs', lambda S: S['_inner'].get('rs'))],
    captions={
        'if node is None': lambda S, B, r: ('空节点：大小为 0，递归边界' if S.node is None else f'节点 `{S.node.val}`：它的子树大小 = 左 + 右 + 1'),
        'return 0': '空子树大小为 `0`',
        'ls = dfs': lambda S, B, r: ('左子树大小 `ls = {}`'.format(S['_inner'].get('ls')) if 'ls' in S['_inner'] else '先递归左子树，==相信它返回左子树的大小=='),
        'rs = dfs': lambda S, B, r: ('右子树大小 `rs = {}`'.format(S['_inner'].get('rs')) if 'rs' in S['_inner'] else '再递归右子树'),
        'if node.val == x': lambda S, B, r: (f'`node.val = {S.node.val}` 就是 `x`：==x 的左右子树大小就在手上=={chr(10) if False else ""}'
                                             if S.node.val == S.x else f'`node.val = {S.node.val}` ≠ `x = {S.x}`，不用记录'),
        'lsz, rsz = ls, rs': '记下 `lsz = {lsz}`，`rsz = {rsz}`；父节点那一侧的大小是 `n - 1 - lsz - rsz = {n - 1 - lsz - rsz}`',
        'return ls + rs + 1': '节点 `{node.val}` 的子树大小 = `{ls} + {rs} + 1 =` ==`{ret}`==',
        'return max(lsz': lambda S, B, r: (f'二号最多染 `max({S.lsz}, {S.rsz}, {S.n - 1 - S.lsz - S.rsz}) = {max(S.lsz, S.rsz, S.n - 1 - S.lsz - S.rsz)}`，'
                                           f'乘 2 得 `{max(S.lsz, S.rsz, S.n - 1 - S.lsz - S.rsz) * 2}` {">" if r else "不>"} `n = {S.n}` → ==`{r}`=='),
    },
    cards=dict(
        one_liner='x 把树切成三块：左子树、右子树、父那一侧。二号选最大的一块，超过一半就赢',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['`n` 个节点的二叉树（`n` 为奇数），值 1..n 互不相同',
                 '一号先选 `x` 染红，二号选 `y` 染蓝，之后轮流往==未染色的相邻节点==扩展',
                 '二号能否选一个 `y` 保证最终染得更多？',
                 '示例：`root=[1,2,3,4,5,6,7]`，`n=7`，`x=2` → `true`'],
        quote='以 x 为根，它的三个邻居（左儿子、右儿子和父节点）就对应着三棵子树……哪棵子树最大，二号玩家就选哪棵。',
        quote_src='—— 灵茶山艾府题解',
        idea=['二号选 `x` 的某个邻居，就能抢下那一整棵子树，其余全归一号',
              '父节点那一侧大小 = `n − 1 − lsz − rsz`',
              '`n2 = max(lsz, rsz, n−1−lsz−rsz)`，二号赢 ⇔ `2·n2 > n`',
              '`dfs` 返回子树大小，遇到 `x` 时顺手记下它的左右子树大小'],
        summary=['时间 `O(n)`，空间 `O(n)`：每个节点访问一次，最坏链状递归深 `n`',
                 '易错：父节点那块要用 `n − 1 − lsz − rsz`，别漏掉 `x` 自己的那个 `1`',
                 '判定是 `2 * n2 > n`（严格大于），`n` 为奇数不会平局',
                 '`nonlocal` 让内层 `dfs` 能修改外层的 `lsz`、`rsz`',
                 '思考题：一号若能自选 `x`，选树的重心就必胜'],
    ),
)
