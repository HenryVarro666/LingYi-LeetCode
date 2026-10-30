VALS = [1, 2, 3, 4, 5, None, None, 6, 7]
N, X = 7, 1


def _col(S, n):
    if n.val == S.get('x'):
        return 'orange'
    return None


def _info(S):
    n = S.get('n') or N
    return f'二号只能选 `x` 的邻居：抢左子树、右子树，或父亲那一侧（`n = {n}`，要抢到 `> n/2`）'


CONFIG = dict(
    num=1145, title='二叉树着色游戏', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='分三种 y 的情况 · 递归求子树大小',
    tags=['灵神题单·贪心与思维', '灵神题单·链表树与回溯', '难度分 1741'],
    code='''
class Solution(object):
    def btreeGameWinningMove(self, root, n, x):

        self.res = False
        self.dfs(root, n, x)
        return self.res
    
    def dfs(self, now, n, x):
        l_cnt = r_cnt = 0
        
        if now.left:
            l_cnt = self.dfs(now.left, n, x)
            if now.val == x and l_cnt > n // 2:
                self.res = True
        
        if now.right:
            r_cnt = self.dfs(now.right, n, x)
            if now.val == x and r_cnt > n // 2:
                self.res = True
        
        tot = l_cnt + r_cnt + 1
        if now.val == x and tot * 2 < n:
            self.res = True
        
        return tot
''',
    setup=f'root = Tr({VALS})',
    call=f'''s = Solution()
s.tree = root
s.btreeGameWinningMove(root, {N}, {X})''',
    expect=True,
    skip=['l_cnt = r_cnt = 0', 'self.res = False', 'self.dfs(root'],
    max_steps=70,
    views=[
        dict(type='tree', var='root', label='二叉树（橙 = 一号选的 x，黄圈 = 当前递归路径）', pointers={'now': 'blue'}, h=330, color=_col),
        dict(type='text', h=80, size=28, fn=_info),
        dict(type='calls', h=200, hide=('n', 'x')),
    ],
    watch=[('x', 'x', 'orange'), ('l_cnt', lambda S: S['_inner'].get('l_cnt'), 'blue'),
           ('r_cnt', lambda S: S['_inner'].get('r_cnt'), 'pink'), ('tot', lambda S: S['_inner'].get('tot'), 'green'),
           ('res', 'self.res', 'yellow')],
    captions={
        'if now.left': lambda S, B, r: (f'节点 `{S.now.val}` 有左孩子 `{S.now.left.val}` → 递归求左子树大小' if S.now.left else f'节点 `{S.now.val}` 没有左孩子，`l_cnt` 保持 0'),
        'l_cnt = self.dfs': '进入左孩子，递归求它的子树节点数；返回后存进 `l_cnt`',
        'if now.val == x and l_cnt': lambda S, B, r: (
            f'`now.val = x`：y 取左孩子，二号抢到 `l_cnt = {S.l_cnt}`，`{S.l_cnt} > {S.n // 2}` → ==成立，二号必胜=='
            if S.now.val == S.x and S.l_cnt > S.n // 2
            else (f'`now.val = {S.now.val}` 不是 x，这里不用判' if S.now.val != S.x else f'`now.val = x`：左孩子子树 `{S.l_cnt}` 不超过一半，这种选法不行')),
        'if now.right': lambda S, B, r: (f'节点 `{S.now.val}` 有右孩子 `{S.now.right.val}` → 递归求右子树大小' if S.now.right else f'节点 `{S.now.val}` 没有右孩子，`r_cnt` 保持 0'),
        'r_cnt = self.dfs': '进入右孩子，递归求它的子树节点数；返回后存进 `r_cnt`',
        'self.res = True': '二号找到了必胜的选法 → `res = True`',
        'if now.val == x and r_cnt': lambda S, B, r: (
            f'`now.val = x`：y 取右孩子，二号抢到 `r_cnt = {S.r_cnt}`，`{S.r_cnt} > {S.n // 2}` → ==成立=='
            if S.now.val == S.x and S.r_cnt > S.n // 2
            else (f'`now.val = {S.now.val}` 不是 x，这里不用判' if S.now.val != S.x else f'`now.val = x`：右孩子子树 `{S.r_cnt}` 不超过一半，这种选法不行')),
        'tot = l_cnt': '以 `{now.val}` 为根的子树共 `{l_cnt} + {r_cnt} + 1 =` ==`{tot}`== 个节点',
        'if now.val == x and tot': lambda S, B, r: (
            f'`now.val = x`：y 取父亲，一号只剩 x 的子树 `{S.tot}` 个，二号得 `{S.n} − {S.tot} = {S.n - S.tot}`；`{S.tot * 2} < {S.n}` → ==成立，二号必胜=='
            if S.now.val == S.x and S.tot * 2 < S.n
            else (f'`now.val = {S.now.val}` 不是 x，不用判' if S.now.val != S.x else f'`now.val = x`：x 子树 `{S.tot}`，父亲那侧 `{S.n - S.tot}` 不够多，这种选法不行')),
        'return tot': '返回子树大小 `{tot}` 给上一层',
        'return self.res': '三种选法里只要有一种成立：`res = {self.res}`',
    },
    cards=dict(
        one_liner='y 必须贴着 x：只有三种选法，各自算二号能抢多少，一种够赢就行',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['`n` 个节点的二叉树（`n` 为奇数），值 1..n 互不相同',
                 '一号先选 `x` 染红，二号选 `y` 染蓝，之后轮流往==未染色的相邻节点==扩展',
                 '二号能否选一个 `y` 保证染得更多？',
                 '本视频：`root=[1,2,3,4,5,null,null,6,7]`，`n=7`，`x=1`'],
        quote='选择的y必然是跟x直接相连的，因为这样一来就不会有x和y之间的部分可以让一号玩家占便宜了。',
        quote_src='—— yiduobo 题解原文',
        idea=['y 贴着 x，有三种：x 的父亲、左孩子、右孩子',
              'y 是父亲：一号占 `f[x]`，二号占 `n − f[x]`',
              'y 是左（右）孩子：二号占 `f[y]`，其余给一号',
              '`f` = 子树节点数，递归求；遇到 x 时分别检查三种情况，有一种成立就为 `True`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '三个条件：`n − f[x] > f[x]`、`f[左] > n/2`、`f[右] > n/2`',
                 '易错：父亲那种情况只在 x 不是根时才有意义；x 是根时 `f[x] = n`，`tot*2 < n` 自然不成立',
                 '原文为 Python 2 写法，整数除法 `n / 2` 已改为 `n // 2`（`n` 为奇数，判定结果不变）',
                 '对比灵神：灵神把三块取 `max`，`2·max > n` 一次判完'],
    ),
)
