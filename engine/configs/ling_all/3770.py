N = 20


def _isp(v):
    return v >= 2 and all(v % d for d in range(2, int(v ** 0.5) + 1))


def _special():
    out, s = [0], 0
    p = 2
    while s + p <= 500000:
        s += p
        if _isp(s):
            out.append(s)
        p += 1
        while not _isp(p):
            p += 1
    return out


SPECIAL = _special()


def _arr(S):
    return SPECIAL[:8]


def _col(S, i, v):
    if 'i' in S and i == S['i']:
        return 'green'
    return None


def _txt(S):
    if 'i' not in S:
        return f'`special_primes` 是预处理好的升序表：`{SPECIAL[:6]}...`（共 {len(SPECIAL) - 1} 个，最前面的 `0` 是哨兵）'
    return f'`bisect_right(special_primes, {S["n"]}) − 1 = {S["i"]}`：表里最后一个 `<= {S["n"]}` 的数是 =={SPECIAL[S["i"]]}=='


CONFIG = dict(
    num=3770, title='可表示为连续质数和的最大质数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='预处理质数前缀和 + 二分',
    tags=['灵神题单·数学算法', '难度分 1547'],
    code='''
MX = 500_000

is_prime = [False] * 2 + [True] * (MX - 1)  # 0 和 1 不是质数
primes = []
for i in range(2, MX + 1):
    if is_prime[i]:
        primes.append(i)
        for j in range(i * i, MX + 1, i):
            is_prime[j] = False  # j 是质数 i 的倍数

special_primes = [0]  # 哨兵
sum_p = 0
for p in primes:
    sum_p += p
    if sum_p > MX:
        break
    if is_prime[sum_p]:
        special_primes.append(sum_p)

class Solution:
    def largestPrime(self, n: int) -> int:
        # 二分找 <= n 的最大特殊质数
        i = bisect_right(special_primes, n) - 1
        return special_primes[i]
''',
    call=f'Solution().largestPrime({N})',
    expect=17,
    views=[
        dict(type='text', fn=_txt, h=80),
        dict(type='array', var=_arr, pointers={'i': 'blue'}, color=_col, h=300,
             label='special_primes 前 8 项（绿 = 二分找到的位置）'),
    ],
    watch=['n', ('i', 'i', 'blue')],
    captions={
        'i = bisect_right': lambda S, B, r: (f'二分：`bisect_right(special_primes, {S.n})` 返回第一个 `> {S.n}` 的位置 `{S.i + 1}`，'
                                             f'减 1 得 `i = {S.i}`，==就是最后一个 `<= {S.n}` 的位置=='),
        'return special_primes[i]': lambda S, B, r: (f'`special_primes[{S.i}] = {SPECIAL[S.i]}`：`{S.n}` 以内最大的特殊质数'
                                                      + ('；`i = 0` 时落在哨兵 0 上，正好表示「不存在」' if S.i == 0 else '')),
    },
    cards=dict(
        one_liner='把所有「前缀和是质数」的数预处理出来，二分一查',
        complexity='时间 `O(log K)`，空间 `O(1)`（不计预处理）',
        problem=['找 `<= n` 的最大质数，且它能写成 ==从 2 开始的连续质数== 之和',
                 '不存在就返回 0',
                 f'本视频：`n = {N}` → `17`（`17 = 2 + 3 + 5 + 7`）'],
        quote='计算质数列表的前缀和，如果前缀和是质数，那么加到特殊质数列表 specialPrimes 中。',
        quote_src='—— 灵茶山艾府题解（写法一）',
        idea=['埃氏筛预处理 `5×10^5` 以内的质数 `primes`',
              '累加 `2, 3, 5, ...`，前缀和是质数就放进 `special_primes`（升序，仅 40 个）',
              '`special_primes` 最前面放哨兵 `0`，二分结果减 1 就不用特判'],
        after=[dict(heading='写法二：双指针预处理所有答案', lines=[
            '用指针 `j` 枚举质数累加，对每个 `i` 预处理 `ans[i]`',
            '如果 `sum_p + primes[j] <= i`，就把下一个质数加进和里',
            '和是质数就更新 `last`，`ans[i] = last`，询问 `O(1)`'])],
        summary=['预处理时空复杂度 `O(U log log U)`，`U = 5×10^5`，不计入',
                 '`bisect_right(...) - 1`：找最后一个 `<= n` 的位置',
                 '易错：`sum_p > MX` 就 break；`n = 1` 时没有答案，靠哨兵 `0` 返回 0',
                 '本题范围内只有 40 个特殊质数'],
    ),
)
