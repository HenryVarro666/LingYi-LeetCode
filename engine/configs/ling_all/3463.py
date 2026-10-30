def _ctab():
    MX = 5
    c = [[0] * MX for i in range(MX)]
    for i in range(MX):
        c[i][0] = c[i][i] = 1
        for j in range(1, i):
            c[i][j] = c[i - 1][j - 1] + c[i - 1][j]
    return c


CTAB = _ctab()


def _hi(S):
    I = S.get('_inner', {})
    if S.get('_line') == 11 and 'p' in I and I['k'] != 0:
        return (I['n'] % I['p'], I['k'] % I['p'])
    return None


def _text(S):
    I = S.get('_inner', {})
    ln = S.get('_line')
    if 'p' in I and 'k' in I:
        n, k, p = I['n'], I['k'], I['p']
        if k == 0:
            return f'`C({n}, 0) mod {p} = 1`：k 已经是 0，递归到底'
        return f'`C({n}, {k}) mod {p}` = `c[{n % p}][{k % p}]` × `C({n // p}, {k // p}) mod {p}`（按 {p} 进制逐位算）'
    if 'n' in I and 'k' in I:
        n, k = I['n'], I['k']
        return f'`C({n}, {k}) mod 10`：先求 mod 2 和 mod 5，再用中国剩余定理拼成 `5*r2 + 6*r5`'
    return '系数 `C(n-2, i)` × 相邻两数之差，求和 mod 10，为 0 就相等'


def _color(S, i, j, v):
    h = _hi(S)
    return 'yellow' if h == (i, j) else None


CONFIG = dict(
    num=3463, title='判断操作后字符串中的数字是否相等 II', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='组合数 + 扩展 Lucas',
    tags=['灵神题单', '难度分 2286'],
    code='''
# 预处理组合数
MX = 5
c = [[0] * MX for i in range(MX)]
for i in range(MX):
    c[i][0] = c[i][i] = 1
    for j in range(1, i):
        c[i][j] = c[i - 1][j - 1] + c[i - 1][j]

# 计算 C(n, k) % p，要求 p 是质数
def lucas(n: int, k: int, p: int) -> int:
    if k == 0:
        return 1
    return c[n % p][k % p] * lucas(n // p, k // p, p) % p

def comb(n: int, k: int) -> int:
    # 结果至多为 5 + 4 * 6 = 29，无需中途取模
    return lucas(n, k, 2) * 5 + lucas(n, k, 5) * 6

class Solution:
    def hasSameDigits(self, s: str) -> bool:
        n = len(s)
        s = map(ord, s)
        return sum(comb(n - 2, i) * (x - y) for i, (x, y) in enumerate(pairwise(s))) % 10 == 0
''',
    call='Solution().hasSameDigits("3902")',
    expect=True,
    views=[
        dict(type='text', fn=_text, size=26),
        dict(type='table', var=lambda S: CTAB, h=330, cell=80, color=_color, label='预处理 c[i][j]（只到 4）'),
        dict(type='calls', h=240),
    ],
    captions={
        'n = len(s)': '`n = {n}`：相邻和要做 `n-2 = {n - 2}` 轮，最后剩 2 个数',
        'return sum(': '把「左边剩的数」减「右边剩的数」展开：==求和 `C(n-2, i) * (s[i] - s[i+1])`==，模 10 为 0 就相等',
        'return lucas(n, k, 2)': '`C({n}, {k}) mod 10`：模 10 不是质数 → 分别求 ==mod 2== 和 ==mod 5==，再合成 `5*r2 + 6*r5`',
        'if k == 0': lambda S, B, ret: (f'`k = 0`：组合数 `C({S["n"]}, 0) = 1`，递归到底' if S['k'] == 0 else f'`k = {S["k"]}` 还不是 0：继续按 {S["p"]} 进制拆下一位'),
        'return 1': '`k = 0` → 返回 `1`',
        'return c[': lambda S, B, ret: f'Lucas：`C({B.n},{B.k}) ≡ C({B.n % B.p},{B.k % B.p}) * C({B.n // B.p},{B.k // B.p})`（mod {B.p}）；==查表 `c[{B.n % B.p}][{B.k % B.p}]`== 是 {CTAB[B.n % B.p][B.k % B.p]}，高位交给下一层',
    },
    cards=dict(
        one_liner='系数是杨辉三角，模 10 拆成模 2 和模 5',
        complexity='时间 `O(n log n)`，空间 `O(log n)`',
        problem=['每次把相邻两数之和模 10 得到新字符串，直到只剩 2 位',
                 '剩下两位相同返回 `true`，否则 `false`',
                 '示例：`"3902"` → `292` → `11` → `true`；`n` 最大 `10^5`'],
        quote='这和 118. 杨辉三角 的计算过程是一样的……所以（根据数学归纳法）系数就是组合数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['最终两个数各是原数的组合数加权和，系数 `C(m-1, i)`；比较时只看差 `s[i]-s[i+1]` 的加权和',
              '10 不是质数，不能直接求逆元：用扩展 Lucas 分别算 `C mod 2`、`C mod 5`',
              '中国剩余定理：`C mod 10 = (5*r2 + 6*r5) mod 10`'],
        after=[dict(heading='另一种写法：提取因子 2 和 5', lines=[
            '灵神方法一：阶乘里去掉因子 2、5，剩下的与 10 互质，用欧拉定理 `a^3` 求逆元',
            '再把 2、5 的幂次乘回去，预处理后每个组合数 `O(1)`，总 `O(n)`'])],
        summary=['`n` 是字符串长度，组合数是 `C(n-2, i)`，不是 `C(n-1, i)`',
                 '差值 `x - y` 可能为负，Python 取模仍得到 0–9，放心 `% 10 == 0`',
                 '`lucas` 里 `p` 必须是质数，所以要拆成 2 和 5 分别算',
                 '预处理 `c` 只需到 `MX = 5`（最大的质数 5）；同类题：2221'],
    ),
    watch=[('n', 'n', 'purple'), ('k', 'k', 'blue'), ('p', 'p', 'pink')],
)
