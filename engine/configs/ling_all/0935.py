CONFIG = dict(
    num=935, title='骑士拨号器', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='4 类格子 + 矩阵快速幂优化 DP',
    tags=['灵神核心路线', '灵神题单·动态规划'],
    code='''
MOD = 1_000_000_007

# a @ b，其中 @ 是矩阵乘法
def mul(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    return [[sum(x * y for x, y in zip(row, col)) % MOD for col in zip(*b)]
            for row in a]

# a^n @ f0
def pow_mul(a: List[List[int]], n: int, f0: List[List[int]]) -> List[List[int]]:
    res = f0
    while n:
        if n & 1:
            res = mul(a, res)
        a = mul(a, a)
        n >>= 1
    return res

class Solution:
    def knightDialer(self, n: int) -> int:
        if n == 1:
            return 10
        m = [[0, 1, 1, 0], [2, 0, 0, 0], [2, 0, 0, 1], [0, 0, 2, 0]]
        f0 = [[1], [1], [1], [1]]
        fn = pow_mul(m, n - 1, f0)
        return (fn[0][0] * 4 + fn[1][0] * 2 + fn[2][0] * 2 + fn[3][0]) % MOD
''',
    call='Solution().knightDialer(6)',
    expect=544,
    skip=['return [[sum', 'for row in a]'],
    views=[
        dict(type='text', h=70, size=24, fn=lambda S: '4 类格子：`A`=1,3,7,9　`B`=2,8　`C`=4,6　`D`=0（答案 = 4A + 2B + 2C + D）'),
        dict(type='table', var='a', label='a = 转移矩阵的 2^k 次方（每轮自乘）', h=300, cell=70,
             rows=['A', 'B', 'C', 'D'], cols=['A', 'B', 'C', 'D']),
        dict(type='table', var='res', label='res = 已累乘的结果（4×1 列向量）', h=300, cell=70, rows=['A', 'B', 'C', 'D'], cols=['']),
        dict(type='text', h=60, size=26, fn=lambda S: (f"`n` = {S['n']} = 二进制 `{bin(S['n'])[2:]}`：最低位是 1 就乘进 `res`" if 'n' in S and 'res' in S else '')),
    ],
    watch=[('n', 'n', 'blue'), ('n & 1', 'n & 1', 'orange')],
    captions={
        'if n == 1': '`n = 1` 直接返回 10；这里 n > 1，马的初始位置不能是 5',
        'm = [[': '`m` 是 4×4 转移矩阵：`f[i] = M × f[i-1]`，代表 `A,B,C,D` 四类格子的转移',
        'f0 = [[': '`f0`：移动 0 步时，每类格子各有 1 种方案（就是号码本身）',
        'fn = pow_mul': '求 `M^(n-1) × f0`，用快速幂：`n - 1 = 5` = 二进制 `101`，逐位处理',
        'res = f0': '`res` 先放 `f0`',
        'while n': lambda S, B, r: (f'`n = {S.n}` ≠ 0，继续处理最低位' if S.n else '`n = 0`，所有二进制位都处理完'),
        'if n & 1': lambda S, B, r: (f'`n & 1 = {S.n & 1}` → 最低位是 1：当前的 `a = M^(2^k)` 要乘进 `res`' if S.n & 1 else f'`n & 1 = 0` → 这一位是 0，不乘'),
        'res = mul(a, res)': '`res = a @ res`：已累乘的幂又多了 `2^k` 步',
        'a = mul(a, a)': '`a` 自乘：`M^(2^k)` → `M^(2^(k+1))`',
        'n >>= 1': '`n` 右移一位 → `{n}`',
        'return res': '`fn = M^(n-1) × f0`：走 `n-1` 步后每类格子的方案数',
        'return (fn': '答案 = `4×A + 2×B + 2×C + 1×D` 取模 = =={ret}==',
    },
    cards=dict(
        one_liner='骑士只有 4 类本质不同的格子，转移写成 4×4 矩阵，再快速幂',
        complexity='时间 `O(D^3 log n)`，`D = 4`；空间 `O(D^2)`',
        problem=['骑士只能站在电话键盘的数字格上，按「日」字走',
                 '放在任意数字格，走 `n-1` 步得到长度为 `n` 的号码',
                 '求能拨出多少个不同号码，对 `1e9+7` 取模',
                 '示例：`n = 1` → `10`，`n = 2` → `20`'],
        quote='其实只有 4 种本质不同的数字。把 A,B,C,D 类分别用 0,1,2,3 表示，作为 dfs 的第二个参数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先记忆化搜索 `dfs(i, j)`：还剩 i 步、站在 j 格，再 1:1 翻成递推',
              '左右、上下对称，10 个格子合并成 4 类，转移是常数系数的线性式',
              '写成 `F[i] = M × F[i-1]`，用矩阵快速幂求 `M^(n-1)`'],
        summary=['时间 `O(D^3 log n)`；`n ≤ 5000` 时递推预处理也够用',
                 '易错：`n = 1` 要单独返回 10，格子 5 在 `n ≥ 2` 时不可用',
                 '易错：答案按各类格子个数加权（4,2,2,1），不是直接求和',
                 '视频演示矩阵快速幂写法（题解方法五）；方法二～四（记忆化 / 递推）和 BM + Kitamasa 一句话带过'],
    ),
)
