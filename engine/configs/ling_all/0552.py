N = 5
LAB = ['00', '01', '02', '10', '11', '12']   # 状态 (j, k)：j = 右边 A 的个数，k = 右边连续 L 的个数


def _mat(*names):
    def g(S):
        I = S['_inner']
        for nm in names:
            v = I.get(nm)
            if isinstance(v, list) and v and isinstance(v[0], list):
                return v
        return None
    return g


def _bits(S):
    I = S['_inner']
    n = I.get('n')
    if 'res' not in I or not isinstance(n, int):
        return f'目标：`sum(M^{N}[0])`；`{N}` 的二进制是 `{N:b}`，从最低位开始扫'
    return f'剩余 `n = {n}`（二进制 `{n:b}`）：最低位是 =={n & 1}==' + ('，要把当前的 `a` 乘进 `res`' if n & 1 else '，不乘，只把 `a` 平方') if n else '`n = 0`，所有二进制位都处理完'


CONFIG = dict(
    num=552, title='学生出勤记录 II', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='6 状态转移矩阵 + 快速幂',
    tags=['动态规划'],
    code='''
MOD = 1_000_000_007

# 返回矩阵 a 和矩阵 b 相乘的结果
def mul(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    return [[sum(x * y for x, y in zip(row, col)) % MOD for col in zip(*b)]
            for row in a]

# 返回 n 个矩阵 a 相乘的结果
def pow(a: List[List[int]], n: int) -> List[List[int]]:
    size = len(a)
    res = [[0] * size for _ in range(size)]
    for i in range(size):
        res[i][i] = 1  # 单位矩阵
    while n:
        if n & 1:
            res = mul(res, a)
        a = mul(a, a)
        n >>= 1
    return res

class Solution:
    def checkRecord(self, n: int) -> int:
        m = [[1, 1, 0, 1, 0, 0],
             [1, 0, 1, 1, 0, 0],
             [1, 0, 0, 1, 0, 0],
             [0, 0, 0, 1, 1, 0],
             [0, 0, 0, 1, 0, 1],
             [0, 0, 0, 1, 0, 0]]
        return sum(pow(m, n)[0]) % MOD
''',
    call=f'Solution().checkRecord({N})',
    expect=94,
    skip=['for i in range(size)', 'res[i][i] = 1', 5, 6, 24, 25, 26, 27, 28],
    views=[
        dict(type='text', fn=_bits, size=26, h=60),
        dict(type='table', var=_mat('a', 'm'), label='a（M 的 2^k 次方；一开始就是 M）', h=250, cell=70, rows=LAB, cols=LAB),
        dict(type='table', var=_mat('res'), label='res（已经乘进来的部分，初始 = 单位矩阵）', h=250, cell=70, rows=LAB, cols=LAB),
        dict(type='text', fn=lambda S: '状态 `jk`：`j` = A 的个数（0/1），`k` = 末尾连续 L 的个数（0/1/2）', size=22, h=40),
    ],
    watch=[('n', lambda S: S['_inner'].get('n'), 'blue'), ('n & 1', lambda S: (S['_inner']['n'] & 1) if isinstance(S['_inner'].get('n'), int) else '', 'pink')],
    captions={
        23: lambda S, B, r: ('把 6 个状态转移方程写成矩阵 `M`：行列都是状态 `(j,k)`' if 'm' not in S else '`F[i] = M × F[i-1]`，所以 `F[n] = M^n × F[0]`，下面求 `M^n`'),
        29: '调用 `pow(m, n)` 求 `M^n`，再把第 0 行（对应 `f[n][0]`）求和取模',
        10: '`size = {size}`：6×6 的方阵',
        11: '`res` 先开成 6×6 的零矩阵，下面把对角线置 1 变成==单位矩阵==（矩阵乘法里的“1”）',
        14: lambda S, B, r: (f'`while n`：n = {S.n}，还有二进制位没处理' if S.n else '`n` 变成 0：所有二进制位处理完了'),
        15: lambda S, B, r: (f'`n & 1 = {S.n & 1}`：这一位是 1 → 答案里需要乘上当前的 `a`（`M^(2^k)`）' if S.n & 1
                             else f'`n & 1 = 0`：这一位是 0，答案里不乘'),
        16: '`res = res × a`：把这一位对应的 `M^(2^k)` 乘进 `res`（`mul`：第 i 行 · 第 j 列逐项相乘求和再取模）',
        17: '`a = a × a`：平方，`M^(2^k)` → `M^(2^(k+1))`，为下一位做准备',
        18: '`n >>= 1`：二进制右移一位，`n = {n}`',
        19: lambda S, B, r: '`res` = `M^5` 算完；第 0 行 `%s` 求和取模 = ==%d==' % (' + '.join(map(str, S.res[0])), sum(S.res[0]) % 1_000_000_007),
    },
    cards=dict(
        one_liner='6 个状态 → 6×6 转移矩阵 → 快速幂把 O(n) 降到 O(log n)',
        complexity='时间 `O(K^3 log n)`（K = 6），空间 `O(K^2)`',
        problem=['长为 `n` 的出勤记录由 `A`（缺勤）`L`（迟到）`P`（到场）组成',
                 '可奖励：==A 至多 1 个==，且==不含连续 3 个 L==；求这样的记录数，对 `10^9+7` 取模',
                 '示例：`n = 2` → `8`；本视频 `n = 5` → `94`'],
        quote='答案 f[n][0] 是 F[n] 的第一项，根据矩阵乘法，其等于 M^n 的第一行乘以 F[0]。由于 F[0] 全为 1，答案也等于 M^n 第一行的元素和。',
        quote_src='—— 灵茶山艾府题解（五、矩阵快速幂优化）',
        idea=['从右往左填字母：状态 `(j, k)` = 右边已有几个 A、右边连续几个 L，共 `2×3 = 6` 个',
              '递推 `f[i][j][k]` 展开成 6 个式子，写成 `F[i] = M × F[i-1]`，于是 `F[n] = M^n × F[0]`',
              '`M^n` 用快速幂：n 的二进制每位对应一个 `M^(2^k)`，为 1 的位乘进 `res`'],
        summary=['时间 `O(K^3 log n)`，K=6；空间 `O(K^2)`',
                 '易错：`F[0]` 全是 1，所以答案 = `M^n` 第一行元素之和，不是单个元素',
                 '易错：`res` 要初始化成单位矩阵，不是零矩阵',
                 '题解还给了 `O(n)` 记忆化/递推（`f[i][j][k]`）和 Berlekamp-Massey + Kitamasa 写法，本视频选矩阵快速幂',
                 '同类题：1220. 统计元音字母序列的数目（矩阵快速幂优化 DP）'],
    ),
)
