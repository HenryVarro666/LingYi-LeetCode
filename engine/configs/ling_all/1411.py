MOD = 1_000_000_007


def _sg(v):
    return v if v <= MOD // 2 else v - MOD


def _mat(cv, T, x, y, M, color, label, cw=150, ch=78):
    cv.text((x + cw, y), label, 24, T['muted'], anchor='mm', bold=True)
    y += 24
    for r, row in enumerate(M):
        for c, v in enumerate(row):
            X, Y = x + c * (cw + 8), y + r * (ch + 8)
            cv.rect((X, Y, X + cw, Y + ch), fill=color, r=10)
            cv.text((X + cw / 2, Y + ch / 2), _sg(v), 34, T['bg'], anchor='mm', bold=True, mono=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'a' not in S or 'res' not in S:
        return
    mid = (x0 + x1) / 2
    _mat(cv, T, x0 + 60, y0 + 40, S['a'], T['blue'], 'a = M 的 2^k 次方（负数按 −x 显示）')
    cv.text((mid + 20, y0 + 150), '→ 乘进', 22, T['dim'], anchor='mm')
    _mat(cv, T, mid + 90, y0 + 40, S['res'], T['green'], 'res = 已乘进结果的列向量', cw=170, ch=78)
    cv.text((x0 + 20, y1 - 40), '每个数都对 10^9+7 取模；res 的第一项最终就是 f[n]', 22, T['muted'])


def _txt(S):
    if 'n' not in S or 'res' not in S or 'a' not in S:
        return '递推 `f[i] = 5·f[i-1] − 2·f[i-2]`，写成矩阵 `[f[i], f[i-1]] = M × [f[i-1], f[i-2]]`'
    n = S['n']
    if S.get('_line') in (None,):
        return ''
    return f"剩余指数 `n = {n}`（二进制 `{bin(n)[2:] if n else '0'}`）：最低位为 1 就把当前 `a` 乘进结果"


def _lab(S):
    return 'a（M 的 2^k 次方，对 MOD 取模）'


CONFIG = dict(
    num=1411, title='给 N x 3 网格图涂色的方案数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='找规律递推 + 矩阵快速幂',
    tags=['灵神题单', '难度分 1845'],
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
    def numOfWays(self, n: int) -> int:
        m = [[5, -2], [1, 0]]
        f1 = [[12], [3]]
        fn = pow_mul(m, n - 1, f1)
        return fn[0][0]
''',
    call='Solution().numOfWays(7)',
    expect=106494,
    skip=['return [[sum', 'for row in a]', 'def ', 'MOD = '],
    views=[
        dict(type='text', h=70, size=26, fn=_txt),
        dict(type='custom', draw=_draw, h=380),
    ],
    watch=[('n', 'n', 'blue'), ('n 二进制', lambda S: bin(S['n'])[2:] if 'n' in S else '', 'cyan')],
    captions={
        'm = [[5': '转移矩阵 `M = [[5, -2], [1, 0]]`：`f[i] = 5·f[i-1] − 2·f[i-2]`，第二行只是把 `f[i-1]` 往下挪',
        'f1 = [[12]': '初始列向量 `F[1] = [f[1], f[0]] = [12, 3]`（`f[0] = 3` 是倒推出来的）',
        'fn = pow_mul': '`F[n] = M^(n-1) × F[1]`：要乘 `n-1 = {B.n - 1}` 次 M，用快速幂',
        'res = f0': '`res` 先放 `F[1]`，之后每遇到二进制的 1 就左乘一个 `a`',
        'while n': lambda S, B, r: (f'`n = {S.n}` 还没用完 → 继续看它的最低位' if S.n else '`n = 0`：所有二进制位都处理完，结束'),
        'if n & 1': lambda S, B, r: (f'`n = {S.n}` 最低位是 ==1== → 这一位对应的 `a` 要乘进结果' if S.n & 1
                                      else f'`n = {S.n}` 最低位是 ==0== → 这一位不用乘'),
        'res = mul(a, res)': '`res = a @ res`：把当前的 `M^(2^k)` 乘进结果（乘法结果看下一步的 `res` 表）',
        'a = mul(a, a)': '`a = a @ a`：`M^(2^k)` 平方成 `M^(2^(k+1))`（对应二进制的下一位）',
        'n >>= 1': '`n` 右移一位，换下一个二进制位：`n = {n}`；此时 `a` = `{a}`，`res` = `{res}`',
        'return res': '`res` = `M^(n-1) @ F[1]` = `{res}`',
        'return fn[0][0]': '答案是 `F[n]` 的第一项 `f[n]` = =={ret}==',
    },
    cards=dict(
        one_liner='把线性递推写成矩阵，再用快速幂算 M 的 n−1 次方',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['`n × 3` 的网格，每格涂红/黄/绿，相邻格颜色不同，求方案数（对 `10^9+7` 取模）',
                 '示例：`n = 1` → `12`；`n = 2` → `54`；`n = 3` → `246`',
                 '本视频：`n = 7` → `106494`'],
        quote='DP 过程是一个线性递推（从 (n-1)×3 网格图最后一行的所有涂色方案线性转移到 n×3 网格图的最后一行），所以必然有线性递推式。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先用记忆化搜索（轮廓线 DP）暴力求出前几项，再用 Berlekamp-Massey 找到递推 `f[i] = 5f[i-1] − 2f[i-2]`',
              '把递推写成 `F[i] = M × F[i-1]`，于是 `F[n] = M^(n-1) × F[1]`',
              '`M^(n-1)` 用快速幂：看 `n-1` 的二进制，为 1 的位乘进结果，每步 `a` 自乘'],
        after=[dict(heading='灵神的另外两种写法', lines=[
            '方法一：记忆化搜索（轮廓线 DP），`dfs(i, j, pre_row, cur_row)`，时间 `O(nmk^(2m+1))`',
            '方法二：递推 `f[i] = (5·f[i-1] − 2·f[i-2]) % MOD`，`f[0]=3, f[1]=12`，时间 `O(n)`',
            '本视频演示方法三：矩阵快速幂，`n` 达到 `10^18` 也能算'])],
        summary=['时间 `O(log n)`（矩阵固定 2×2），空间 `O(1)`',
                 '`f[0] = 3` 由 `f[2] = 5f[1] − 2f[0]` 倒推得到，初始向量是 `[f[1], f[0]]`',
                 '矩阵里有负数 `-2`：Python 的 `%` 结果非负，所以可以放心取模',
                 '快速幂只需 `n-1` 次幂，不是 `n` 次',
                 '同类题：1931 用三种颜色涂 m×n 网格（矩阵更大）'],
    ),
)
