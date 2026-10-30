def _bits(S):
    n = S.get('n')
    if not (10 <= S.get("_line", 0) <= 16):
        return '利用对称性：只留 `k×k` 矩阵（反对角线左上全为 1），`F[n] = M^(n-1) × F[1]`，答案 = 元素和 × 2'
    return f'剩余指数 `n = {n}`（二进制 `{bin(n)[2:] if n else "0"}`）：最低位为 1 就把当前的 `a` 乘进 `res`'


CONFIG = dict(
    num=3700, title='锯齿形数组的总数 II', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='矩阵快速幂优化 DP（对称性）',
    tags=['难度分 2435'],
    code='''
MOD = 1_000_000_007

# a @ b，其中 @ 是矩阵乘法
# 更快的写法见另一份代码【NumPy】
def mul(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    return [[sum(x * y for x, y in zip(row, col)) % MOD for col in zip(*b)]
            for row in a]

# a^n @ f1
def pow_mul(a: List[List[int]], n: int, f1: List[List[int]]) -> List[List[int]]:
    res = f1
    while n:
        if n & 1:
            res = mul(a, res)
        a = mul(a, a)
        n >>= 1
    return res

class Solution:
    def zigZagArrays(self, n: int, l: int, r: int) -> int:
        k = r - l + 1
        m = [[0] * k for _ in range(k)]
        for i in range(k):
            for j in range(k - 1 - i):
                m[i][j] = 1

        f1 = [[1] for _ in range(k)]
        fn = pow_mul(m, n - 1, f1)
        return sum(row[0] for row in fn) * 2 % MOD
''',
    call='Solution().zigZagArrays(6, 1, 4)',
    expect=314,
    skip=['return [[sum', 'for row in a]', 'for i in range(k)', 'for j in range(k - 1 - i)', 'm[i][j] = 1'],
    max_steps=60,
    views=[
        dict(type='text', fn=_bits, size=22, h=90),
        dict(type='table', var=lambda S: S.get('a') or S.get('m') or [[0]], label='a（先是 M：反对角线左上全为 1，之后每轮自乘）', h=260, cell=70),
        dict(type='table', var=lambda S: S.get('res') or S.get('f1') or [[0]], label='res（列向量，初值全 1 = F[1]）', h=300, cell=70),
    ],
    watch=[('n', 'n', 'blue'), ('res', 'res', 'green')],
    captions={
        'k = r - l + 1': '取值有 `k = {k}` 种（`{l}` 到 `{r}`），按 `v - l` 编号成 `0 .. k-1`',
        'm = [[0]': '`k×k` 的全 0 系数矩阵 `M`；填入 `m[i][j] = 1`（`j < k-1-i`）：升降交替，对称后只需一半',
        'f1 = ': '`F[1]`：长为 1 的数组，以每个值结尾各 1 种，全 1 列向量',
        'fn = pow_mul': '`F[n] = M^(n-1) × F[1]`，指数 `n - 1`，用快速幂（`n` 最大 `10^9`）',
        'res = f1': '`res` 先放 `F[1]`，相当于 `M^0 × F[1]`',
        'while n': lambda S, B, r: (f'指数 `{S.n}` 还没用完 → 看最低位' if S.n else '指数用完了，`res = M^(n-1) × F[1]`'),
        'if n & 1': lambda S, B, r: ('`n & 1 = 1`：最低位是 1 → ==这一块 M^(2^k) 要乘进 res==' if S.n & 1
                                     else '`n & 1 = 0`：最低位是 0 → 这一块不要'),
        'res = mul(a, res)': '`res = a @ res`：多走 `2^k` 步',
        'a = mul(a, a)': '`a` 自乘：`M^(2^k)` 变成 `M^(2^(k+1))`',
        'n >>= 1': '`n` 右移一位 → {n}',
        'return res': '返回 `M^(n-1) × F[1]`',
        'return sum(row[0]': '元素和 `{sum(row[0] for row in fn)}`，因升降对称再 ×2，取模 = =={ret}==',
    },
    cards=dict(
        one_liner='升降交替的 DP 写成矩阵，利用对称性缩小一半再快速幂',
        complexity='时间 `O(k^3 log n)`，空间 `O(k^2)`',
        problem=['长为 `n` 的数组，元素在 `[l, r]`，相邻不等，且任意三个连续元素不单调（锯齿形）',
                 '求个数对 `10^9+7` 取模，`n` 最大 `10^9`，`r-l` 最大 74',
                 '本视频：`n = 6, l = 1, r = 4` → `314`'],
        quote='可以只使用 k×k 大小的系数矩阵，这个矩阵在反对角线的左上全为 1。',
        quote_src='—— 灵茶山艾府题解（利用对称性优化）',
        idea=['`f0/f1[i][j]`：第 i 个数为 j，且最后一步递增 / 递减的个数，递增递减交替',
              '合并成 `2k×2k` 矩阵，`F[n] = M^(n-1) × F[1]`',
              '递增与递减对称（`j` 换成 `k-1-j`），只留 `k×k` 的一半，答案乘 2'],
        summary=['时间 `O(k^3 log n)`，空间 `O(k^2)`，`k = r-l+1`',
                 '易错：指数是 `n-1`；最后一步别忘 `×2`；每次乘法后取模',
                 '不用对称性的写法是 `2k×2k` 矩阵，慢 8 倍',
                 '灵神还给了 Berlekamp-Massey + Kitamasa 写法，同类题 3337、790']
    ),
)
