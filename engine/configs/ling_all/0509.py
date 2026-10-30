def _bits(S):
    if 'n' not in S or 'res' not in S:
        return ''
    n = S['n']
    if not isinstance(n, int):
        return ''
    b = bin(n)[2:] if n else '0'
    return f'剩余指数 `n = {n}`，二进制 `{b}`：==最低位是 1== 就把当前的 `a` 乘进 `res`'


def _pw(S):
    """当前 a 是 M 的几次方（a = M^(2^k)）"""
    a = S.get('a')
    if not a or not isinstance(a, list) or len(a) != 2:
        return None
    x, k = [[1, 1], [1, 0]], 1
    for _ in range(12):
        if x == a:
            return k
        x = [[sum(p * q for p, q in zip(r, c)) for c in zip(*x)] for r in x]
        k *= 2
    return None


def _a_label(S):
    k = _pw(S)
    return f'a = M^{k}' if k else 'a'


def _mm(a, b):
    return [[sum(x * y for x, y in zip(r, c)) for c in zip(*b)] for r in a]


def _if(S, B, ret):
    n = S.n
    if n & 1:
        return f'`n = {n}` 二进制最低位是 ==1== → 需要乘上当前的 `a = M^{_pw(S)}`'
    return f'`n = {n}` 二进制最低位是 0 → 这一位不乘，`res` 不变'


CONFIG = dict(
    num=509, title='斐波那契数', difficulty='Easy', category='动态规划',
    author='灵茶山艾府', technique='矩阵快速幂',
    tags=['labuladong', '灵神题单·动态规划'],
    code='''
# a @ b，其中 @ 是矩阵乘法
def mul(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)]
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
    def fib(self, n: int) -> int:
        if n == 0:
            return 0
        m = [[1, 1], [1, 0]]
        f1 = [[1], [0]]
        fn = pow_mul(m, n - 1, f1)
        return fn[0][0]
''',
    call='Solution().fib(10)',
    expect=55,
    views=[
        dict(type='text', fn=lambda S: '递推写成矩阵：`[f(i), f(i-1)]^T = M × [f(i-1), f(i-2)]^T`，`M = [[1,1],[1,0]]`', h=60, size=24),
        dict(type='text', fn=_bits, h=60, size=24),
        dict(type='grid', var=lambda S: S.get('a') if 'res' in S else S.get('m'), label='当前的 a（依次是 M, M^2, M^4, M^8 …）', cell=110, h=300,
             color=lambda S, i, j, v: 'purple'),
        dict(type='grid', var=lambda S: S.get('res', S.get('f1')), label='res（初始 F[1] = [f(1), f(0)]^T，乘完是 F[n]）', cell=110, h=300,
             color=lambda S, i, j, v: 'green' if i == 0 else 'cyan'),
    ],
    watch=[('n', 'n', 'blue'), ('a 是 M 的几次方', _pw, 'purple'), ('res', 'res', 'green')],
    captions={
        'if n == 0': '`n = {n}` 不是 0，用矩阵快速幂',
        'm = [[1, 1], [1, 0]]': '转移矩阵 `M`：第一行算 `f(i) = f(i-1) + f(i-2)`，第二行把 `f(i-1)` 挪下来',
        'f1 = [[1], [0]]': '初始列向量 `F[1] = [f(1), f(0)]^T = [1, 0]^T`',
        'fn = pow_mul(m, n - 1, f1)': '`F[n] = M^(n-1) × F[1]`：调用 `pow_mul(m, {B.n - 1}, f1)`，`{B.n - 1}` 的二进制是 `{bin(B.n - 1)[2:]}`',
        'res = f0': '`res` 从 `F[1]` 出发，每次把需要的 `a` 左乘上去',
        'while n': lambda S, B, ret: (f'`n = {S.n}` 还没变成 0：继续看二进制下一位' if S.n
                                      else '`n = 0`：指数的每一位都处理完了'),
        'if n & 1': _if,
        'res = mul(a, res)': lambda S, B, ret: f'把 `a = M^{_pw(B)}` 乘进来：`res = a × res` = =={_mm(B.a, B.res)}==',
        'a = mul(a, a)': lambda S, B, ret: f'`a` 自乘：==M 的指数翻倍== → `M^{2 * _pw(B)}` = `{_mm(B.a, B.a)}`',
        'n >>= 1': '`n` 右移一位 → `{n}`，去看下一个二进制位',
        'return res': '返回 `res = {res}`',
        'return [[sum': lambda S, B, ret: f'矩阵乘法：行 × 列逐项相乘再求和 → `{ret}`',
        'return fn[0][0]': '`F[n]` 的第一项就是 `f(n)` = =={ret}==',
    },
    skip=['return [[sum', 'for row in a'],
    max_steps=60,
    cards=dict(
        one_liner='把递推写成矩阵乘法，M 的 n-1 次方用快速幂算',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['`F(0) = 0`，`F(1) = 1`，`F(n) = F(n-1) + F(n-2)`，给定 `n` 求 `F(n)`',
                 '示例：`n = 4` → `3`',
                 '本视频：`n = 10` → `55`'],
        quote='把上式中的三个矩阵分别记作 `F[i], M, F[i-1]`，即 `F[i] = M×F[i-1]`……`= M^(n-1)×F[1]`，其中 ==M^(n-1) 可以用快速幂计算==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['一步递推 = 左乘一次 `M = [[1,1],[1,0]]`，`n-1` 步就是 `M^(n-1)`',
              '快速幂：把指数 `n-1` 拆成二进制，`a` 依次是 `M, M^2, M^4…`',
              '二进制位为 1 时把当前的 `a` 乘进 `res`；本例 `9` 的二进制是 `1001`，乘 `M^8` 和 `M^1`'],
        summary=['时间 `O(log n)`；2×2 矩阵乘法是常数',
                 '`n = 0` 要特判：`n - 1 = -1` 不能做快速幂',
                 '`res` 一开始就是 `F[1]`，所以 `pow_mul` 直接算出 `M^(n-1)×F[1]`',
                 '题解还给了 `f[i] = f[i-1] + f[i-2]` 递推（`O(n)` 空间）和 `f0, f1` 滚动（`O(1)` 空间）两种写法',
                 '同类题：70. 爬楼梯、1137. 第 N 个泰波那契数'],
    ),
)
