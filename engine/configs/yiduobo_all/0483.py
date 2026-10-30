CONFIG = dict(
    num=483, title='最小好进制', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='枚举位数 p + 开方定 k',
    tags=[],
    setup='from math import log',
    code='''
class Solution(object):
    def smallestGoodBase(self, n):

        max_p = int(log(float(n)) / log(2))
        for p in range(max_p, 1, -1):
            k = int(float(n) ** (1 / float(p)))
            if (k ** (p + 1) - 1) == int(n) * (k - 1):
                return str(k)

        return str(int(n) - 1)
''',
    call="Solution().smallestGoodBase('13')",
    expect='3',
    views=[
        dict(type='text', fn=lambda S: (f"`n = {S['n']}`，枚举 1 的个数：`p + 1` 位全是 1，`k ≈ n^(1/p)`" if 'p' not in S else
                                         f"`p = {S['p']}` → `k = int({S['n']}^(1/{S['p']}))` = =={S['k']}==" if 'k' in S else ''), size=30, h=90),
        dict(type='text', fn=lambda S: (f"验证：`k^(p+1) − 1 = {S['k']**(S['p']+1)-1}`，`n×(k−1) = {int(S['n'])*(S['k']-1)}`" if 'k' in S and 'p' in S else ''), size=30, h=90),
    ],
    watch=['max_p', 'p', ('k', 'k', 'green')],
    captions={
        'max_p = int': '`1 + k + … + k^p = n`，`k ≥ 2` 时 `n ≥ 2^p`，所以 `p` 最多是 n 的二进制位数：`max_p = {max_p}`',
        'for p in': '从大到小枚举 `p`：`p` 越大，`k` 越小，第一个成立的就是最小的好进制（`p = {p}`）',
        'k = int': '由 `n^(1/p) - 1 < k < n^(1/p)` 知 `k` 只能是取整：`k = int({n}^(1/{p}))` = =={k}==',
        'if (k ** (p + 1) - 1)': lambda S, B, r: (f'`k^(p+1) − 1 = {S.k**(S.p+1)-1}`，`n×(k−1) = {int(S.n)*(S.k-1)}`，相等 → `{S.k}` 进制下 n 是 {S.p + 1} 个 1' if (S.k ** (S.p + 1) - 1) == int(S.n) * (S.k - 1)
                                                else f'`k^(p+1) − 1 = {S.k**(S.p+1)-1}`，`n×(k−1) = {int(S.n)*(S.k-1)}`，不相等 → `k = {S.k}` 不行，换更小的 p'),
        'return str(k)': '`n` 在 `{k}` 进制下是 `{p + 1}` 个 1 → ==返回 "{k}"==',
        'return str(int(n) - 1)': '找不到 `p ≥ 2` 的解：只剩 `p = 1`，`n = 1 + k` → `k = n - 1`',
    },
    cards=dict(
        one_liner='枚举 1 的个数 p，用不等式夹出唯一可能的 k',
        complexity='时间 `O(log²n)`，空间 `O(1)`',
        problem=['`n` 的 `k` 进制表示若全是 `1`，则 `k` 是 `n` 的“好进制”',
                 '给定字符串 `n`，求最小的好进制（以字符串返回）',
                 '示例：`n = "13"` → `"3"`（13 = 111 的 3 进制）'],
        quote='综上就有n^(1/p) - 1 < k < n^(1/p)。对于这个p，存在一个上界，即最多为n在2进制下的位数，于是我们可以枚举这里的p，然后通过上面这个不等式确定k。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n = 1 + k + … + k^p`，等比求和得 `nk − n + 1 = k^(p+1)`',
              '夹逼得 `n^(1/p) − 1 < k < n^(1/p)`，区间内只有 `int(n^(1/p))` 一个整数',
              '`p` 从大到小枚举（位数越多进制越小），验证 `k^(p+1) − 1 = n(k − 1)`'],
        summary=['时间 `O(log²n)`：`p` 最多 `log n` 个，每个 `k^(p+1)` 的计算要 `O(log n)`',
                 '全部不成立时 `p = 1`：`n = 1 + (n - 1)`，答案是 `n - 1`',
                 '用 `float` 开方，大数时有精度风险，所以最后用整数等式验证',
                 '原文用到 `log` 但没写导入；视频里补了 `from math import log`，其余照搬'],
    ),
)
