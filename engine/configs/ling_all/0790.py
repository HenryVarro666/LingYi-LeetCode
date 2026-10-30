def _bits(S):
    n = S.get('n')
    if n is None or not (9 <= S.get('_line', 0) <= 15):
        return '`f[n] = 2·f[n-1] + f[n-3]`，写成矩阵：`F[n] = M × F[n-1]`，所以 `F[n] = M^(n-2) × F[2]`'
    return f'剩余指数 `n = {n}`（二进制 `{bin(n)[2:] if n else "0"}`）：最低位为 1 就把当前的 `a` 乘进 `res`'


CONFIG = dict(
    num=790, title='多米诺和托米诺平铺', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='矩阵快速幂优化 DP',
    tags=[],
    code='''
MOD = 1_000_000_007

# a @ b，其中 @ 是矩阵乘法
def mul(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    return [[sum(x * y for x, y in zip(row, col)) % MOD for col in zip(*b)]
            for row in a]

# a^n @ f
def pow_mul(a: List[List[int]], n: int, f: List[List[int]]) -> List[List[int]]:
    res = f
    while n:
        if n & 1:
            res = mul(a, res)
        a = mul(a, a)
        n >>= 1
    return res

class Solution:
    def numTilings(self, n: int) -> int:
        if n == 1:
            return 1
        f2 = [[2], [1], [1]]
        m = [[2, 0, 1], [1, 0, 0], [0, 1, 0]]
        fn = pow_mul(m, n - 2, f2)
        return fn[0][0]
''',
    call='Solution().numTilings(7)',
    expect=117,
    skip=['return [[sum', 'for row in a]'],
    max_steps=60,
    views=[
        dict(type='text', fn=_bits, size=24, h=70),
        dict(type='table', var='a', label='a（先是 M，之后每轮自乘：M, M^2, M^4 ...）', h=260, cell=76),
        dict(type='table', var='res', label='res（列向量，初值 F[2] = [f2, f1, f0]）', h=260, cell=76),
    ],
    watch=[('n', 'n', 'blue'), ('res', 'res', 'green')],
    captions={
        'if n == 1': '`n = 1` 时只有一种平铺，直接返回；否则矩阵里的 `F[2]` 才成立',
        'f2 = ': '`F[2] = [f[2], f[1], f[0]] = [2, 1, 1]`，其中 `f[0] = 1` 是为了递推方便',
        'm = ': '系数矩阵 `M`：第一行 `[2,0,1]` 表示 `f[i] = 2·f[i-1] + f[i-3]`，下面两行负责平移',
        'fn = pow_mul': '要算 `F[n] = M^(n-2) × F[2]`，指数是 `n - 2`，用快速幂',
        'res = f': '`res` 先放 `F[2]`，相当于 `M^0 × F[2]`',
        'while n': lambda S, B, r: (f'`n = {S.n}` 还没用完 → 继续看它的最低位' if S.n else '指数用完了，`res = M^(n-2) × F[2]`'),
        'if n & 1': lambda S, B, r: (f'`n & 1 = {S.n & 1}`：最低位是 1 → ==这一块 M^(2^k) 要乘进答案==' if S.n & 1
                                     else f'`n & 1 = 0`：最低位是 0 → 这一块不需要'),
        'res = mul(a, res)': '`res = a @ res`：把当前的 `a`（M 的 2^k 次幂）乘进 `res`',
        'a = mul(a, a)': '`a` 自乘，从 `M^(2^k)` 变成 `M^(2^(k+1))`，为下一位二进制做准备',
        'n >>= 1': '`n` 右移一位 → {n}',
        'return fn[0][0]': '`F[n]` 的第一项就是 `f[n]` = =={ret}==',
    },
    cards=dict(
        one_liner='把递推写成矩阵乘法，用快速幂跳到第 n 项',
        complexity='时间 `O(D^3 log n)`（D=3），空间 `O(D^2)`',
        problem=['有 `2×1` 多米诺和 L 形托米诺两种瓷砖（可旋转），求铺满 `2×n` 面板的方案数，对 `10^9+7` 取模',
                 '示例：`n = 3` → `5`；`n = 1` → `1`',
                 '本视频：`n = 7` → `117`'],
        quote='考虑最右边那一对 L 型的铺设方法，这一对 L 型必须一左一右，中间的都是 2×1 横着摆。……即使 n=10^18 也能轻松通过。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i] = f[i-1] + f[i-2] + 2·Σf[j]`，化简得 `f[i] = 2·f[i-1] + f[i-3]`',
              '三项递推 → `3×3` 系数矩阵 `M`，`F[n] = M^(n-2) × F[2]`',
              '`M^(n-2)` 按指数二进制拆开：每位平方一次，该位为 1 就乘进 `res`'],
        summary=['时间 `O(3^3 · log n)`，空间 `O(1)`，`n` 再大也行',
                 '易错：初始向量是 `F[2] = [2,1,1]`（含 `f[0]=1`），指数是 `n-2`，`n=1` 要单独特判',
                 '写法一二是 `O(n)` 递推（`f[i]=2f[i-1]+f[i-3]`，可滚动成 3 个变量），写法三预处理 1000 以内',
                 '矩阵快速幂模板：`mul` + `pow_mul`，同类题 3337、3700、2851'],
    ),
)
