import itertools
from math import comb as _comb

N, M, K = 5, 3, 2
EXP = sum(1 for a in itertools.product(range(1, M + 1), repeat=N)
          if sum(a[i - 1] == a[i] for i in range(1, N)) == K)
EX = [1, 1, 2, 3, 3]          # 一个好数组：恰好 2 对相邻相同（下标 0-1 和 3-4）
SEG = [0, 0, 1, 2, 2]         # 它被「不同的相邻对」切成 3 段
SEG_COL = ['blue', 'pink', 'green']


def _rows(S):
    n, m, k = N, M, K
    if 'MOD' not in S:
        return f'`n = {n}, m = {m}, k = {k}`：先划分，再填数'
    return (f'划分：`C({n - 1}, {k})` = =={_comb(n - 1, k)}==　第一段：`m` = =={m}==　其余 `{n - k - 1}` 段：`({m} - 1)^{n - k - 1}` = =={(m - 1) ** (n - k - 1)}==')


def _segs(S):
    return f'示例数组 `{EX}`：{N - 1} 个空隙里有 {N - 1 - K} 个「不同」→ 切成 {N - K} 段，每段内数字相同'


CONFIG = dict(
    num=3405, title='统计恰好有 K 个相等相邻元素的数组数目', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='先划分再填数 + 组合数',
    tags=['灵神题单', '难度分 2310'],
    code='''
class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 1_000_000_007
        return comb(n - 1, k) % MOD * m * pow(m - 1, n - k - 1, MOD) % MOD
''',
    call=f'Solution().countGoodArrays({N}, {M}, {K})',
    expect=EXP,
    views=[
        dict(type='text', fn=_segs, size=24, h=90),
        dict(type='array', var=lambda S: EX, label='一个好数组（颜色 = 同一段）', h=230, cell=100,
             color=lambda S, i, v: SEG_COL[SEG[i]]),
        dict(type='text', fn=_rows, size=28, h=140),
    ],
    watch=['n', 'm', 'k', 'MOD'],
    captions={
        'MOD = ': '答案可能很大，先约定模数 `MOD = 10^9 + 7`',
        'return comb': lambda S, B, ret: f'`C({S["n"] - 1},{S["k"]}) * m * (m-1)^(n-k-1)` = `{_comb(S["n"] - 1, S["k"])} * {S["m"]} * {(S["m"] - 1) ** (S["n"] - S["k"] - 1)}` = =={ret}==（取模后结果不变，因为 {ret} < MOD）',
    },
    cards=dict(
        one_liner='先划分数组，再往每一段里填数字',
        complexity='时间 `O(log(n-k))`，空间 `O(1)`',
        problem=['长为 `n` 的数组，元素在 `[1, m]` 内，==恰好== `k` 个下标 `i` 满足 `arr[i-1] == arr[i]`',
                 '求这样的数组个数，对 `10^9 + 7` 取模',
                 '示例：`n=3, m=2, k=1` → `4`；`n=4, m=2, k=2` → `6`'],
        quote='恰好有 k 对相邻元素相同，等价于恰好有 n-1-k 对相邻元素不同。把这 n-1-k 对不同元素，看成 n-1-k 条分割线……核心想法：先划分数组，再填数字。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`n-1` 个空隙里选 `n-1-k` 条分割线：`C(n-1, k)` 种，得到 `n-k` 段，段内数字全相同',
              '第一段任选：`m` 种；之后每段不能和上一段相同：`m-1` 种，共 `n-k-1` 段',
              '乘法原理：`C(n-1,k) * m * (m-1)^(n-k-1)`'],
        after=[dict(heading='组合数怎么算（预处理版本）', lines=[
            '灵神另给了 Python3 预处理写法：先算阶乘 `f` 和阶乘逆元 `inv_f`',
            '`C(n, m) = f[n] * inv_f[m] * inv_f[n-m] % MOD`',
            '快速幂用内置 `pow(m-1, n-k-1, MOD)`，对数时间'])],
        summary=['公式 `C(n-1,k) * m * (m-1)^(n-k-1)`，时间 `O(log(n-k))`（预处理忽略）',
                 '易错点：不同的相邻对是 `n-1-k` 个，所以段数是 `n-k`',
                 '`comb` 的结果很大，先 `% MOD` 再乘，防止数字过大',
                 '代码用到 `math.comb`（已注入）；同类题：2221、3463'],
    ),
)
