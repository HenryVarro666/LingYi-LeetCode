def _text(S):
    I = S.get('_inner', {})
    if 'root' in I:
        l = len(I.get('left', []))
        r = len(I.get('right', []))
        return f'根 `{I["root"]}`：左子树 {l} 个节点，右子树 {r} 个节点；子树内部方案数 × 交错方式 `C({l}+{r}, {l})`'
    if 'c' in S:
        return '先预处理组合数表 `c[i][j] = C(i, j)`（杨辉三角）'
    return '数组第一个数是根，其余按大小分到左右子树'


def _cur(S, name):
    I = S.get('_inner', {})
    return I.get(name, [])


CONFIG = dict(
    num=1569, title='将子数组重新排序得到同一个二叉查找树的方案数', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='递归分左右 + 组合数交错',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def numOfWays(self, nums):

        n = len(nums)
        c = [[0] * n for _ in range(n)]

        mod = 10 ** 9 + 7
        for i in range(n):
            for j in range(i + 1):
                if j == 0:
                    c[i][j] = 1
                elif j + j > i:
                    c[i][j] = c[i][i - j]
                else:
                    c[i][j] = (c[i - 1][j - 1] + c[i - 1][j]) % mod
        
        return (self.dfs(nums, c, mod) - 1 + mod) % mod
    
    def dfs(self, nums, c, mod):
        if not nums:
            return 1
        
        root = nums[0]
        left = []
        right = []
        for num in nums[1:]:
            if num < root:
                left.append(num)
            else:
                right.append(num)
        
        l_res = self.dfs(left, c, mod)
        r_res = self.dfs(right, c, mod)
        
        res = 1
        res = res * l_res % mod
        res = res * r_res % mod
        res = res * c[len(nums) - 1][len(left)] % mod

        return res
''',
    call='Solution().numOfWays([2,1,4,3])',
    expect=2,
    views=[
        dict(type='text', fn=_text, size=24, h=90),
        dict(type='array', var=lambda S: _cur(S, 'nums'), label='当前子数组 nums（首位 = 根）', h=150, cell=80,
             color=lambda S, i, v: 'yellow' if i == 0 and S.get('_inner', {}).get('root') is not None else None),
        dict(type='array', var=lambda S: _cur(S, 'left'), label='left（比根小 → 左子树）', h=110, cell=70, color=lambda S, i, v: 'blue'),
        dict(type='array', var=lambda S: _cur(S, 'right'), label='right（比根大 → 右子树）', h=110, cell=70, color=lambda S, i, v: 'pink'),
        dict(type='table', var=lambda S: S['c'] if 'c' in S else [[0]], label='c[i][j] = C(i, j)', h=240, cell=64,
             color=lambda S, i, j, v: 'yellow' if S.get('_line') == 29 and j == len(S.get('_inner', {}).get('left', [])) and i == len(S.get('_inner', {}).get('nums', [])) - 1 else None),
        dict(type='calls', h=200),
    ],
    watch=[('root', 'root', 'yellow'), ('l_res', 'l_res', 'blue'), ('r_res', 'r_res', 'pink'), ('res', 'res', 'green')],
    skip=['for i in range(n)', 'for j in range(i + 1)', 'j == 0', 'j + j > i', 'c[i][j] = ', 'mod = 10', 'left = []', 'right = []', 'res = 1', 'res = res * l_res', 'res = res * r_res'],
    captions={
        'n = len(nums)': '一共 `n = {n}` 个数；先预处理组合数表，最大只需要 `C(n-1, *)`',
        'c = [[0]': '建 `n × n` 的表 `c`，下面按杨辉三角 `C(i,j) = C(i-1,j-1) + C(i-1,j)` 填满，`j > i/2` 时直接用对称性 `C(i,i-j)`',
        'return (self.dfs': '表填好（高亮之外是杨辉三角）。`dfs` 算「以第一个数为根」的总方案数，最后 ==减去原数组自己这 1 种==',
        'if not nums': lambda S, B, ret: ('空数组：没有节点，只有 1 种（空树）' if not S['nums'] else f'`nums = {S["nums"]}` 非空，首位 `{S["nums"][0]}` 一定是根'),
        'return 1': '空子树只有 `1` 种方案，返回 `1`',
        'root = nums[0]': '数组第一个数一定先插入，所以它是根：`root = {root}`',
        'for num in nums[1:]': lambda S, B, ret: ('其余的数都分完了' if S.get('num') is not None and 'num' in B and B.num == S['num'] and len(B.get('left', [])) + len(B.get('right', [])) >= len(S['nums']) - 1 else f'逐个看其余的数：`{S["num"]}` 和根 `{S["root"]}` 比'),
        'if num < root': lambda S, B, ret: f'`{S["num"]} < {S["root"]}` → ==成立，进左子树==' if S['num'] < S['root'] else f'`{S["num"]} > {S["root"]}` → ==不成立，进右子树==',
        'left.append': '放进 `left`：保持它们在原数组里的相对顺序',
        'right.append': '放进 `right`：保持它们在原数组里的相对顺序',
        'l_res = self.dfs': '`left = {left}` 内部有 `l_res` 种合法顺序（递归）',
        'r_res = self.dfs': '`right = {right}` 内部有 `r_res` 种合法顺序（递归）',
        'c[len(nums) - 1][len(left)]': '左 `{len(left)}` 个、右 `{len(right)}` 个：除根外 `{len(nums) - 1}` 个位置里选 `{len(left)}` 个放左子树的数 → `C({len(nums) - 1}, {len(left)})`，得 `res = {res}`',
        'return res': '这棵子树共有 `{res}` 种合法排列，返回给上一层',
    },
    cards=dict(
        one_liner='首位是根，左右子树内部排列 × 交错方式数',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['`nums` 是 `1..n` 的排列，按顺序插入得到一棵二叉查找树',
                 '问有多少种重排 `nums` 的方式，得到==同一棵==树（不含原排列本身）',
                 '示例：`[2,1,3]` → `1`；`[3,4,5,1,2]` → `5`'],
        quote='对于给出的数组，其首位必然会被当做bst的根节点，那么根据这个节点的大小，就可以将数组中其他的数划分到左子树和右子树中。',
        quote_src='—— yiduobo 题解',
        idea=['首位是根；比根小的归 `left`，大的归 `right`，各自递归',
              '左右子树各自的排列固定后，要把两个序列交错拼起来：`C(l + r, r)` 种',
              '`f[now] = f[now.left] * f[now.right] * C(l+r, r)`；组合数用杨辉三角预处理',
              '总数里包含原数组这 1 种，最后 `- 1`'],
        result='`dfs` 返回 `3`（含原排列），减去自己这 1 种 → 返回 `2`',
        summary=['时间 `O(n^2)`（建表 + 每层分左右），空间 `O(n^2)`',
                 '易错点：交错数是 `C(len(nums)-1, len(left))`，要去掉根',
                 '最后 `(dfs - 1 + mod) % mod`，加 `mod` 防止出现负数',
                 '原文为 Python 2 风格，但代码在 Python 3 下可直接运行，未改动'],
    ),
    max_steps=110,
)
