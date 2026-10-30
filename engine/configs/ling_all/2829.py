def _nums(S):
    return list(range(1, S['k'] + S['n']))


def _color(S, i, v):
    if 'm' not in S:
        return None
    m, n, k = S['m'], S['n'], S['k']
    if v <= m:
        return 'green'
    if k <= v <= k + n - m - 1:
        return 'blue'
    return None


def _dim(S, i, v):
    if 'm' not in S:
        return False
    m, n, k = S['m'], S['n'], S['k']
    return not (v <= m or k <= v <= k + n - m - 1)


def _text(S):
    n, k = S['n'], S['k']
    if 'm' not in S:
        return f'`1` 与 `k-1={k-1}`、`2` 与 `k-2={k-2}`…… 每对和为 `k={k}`，只能选一个 → 选小的'
    m = S['m']
    s1 = m * (m + 1) // 2
    s2 = (k * 2 + n - m - 1) * (n - m) // 2
    return f'第一部分 `1..{m}` = =={s1}==　　第二部分 `{k}..{k+n-m-1}`（{n-m} 个）= =={s2}=='


CONFIG = dict(
    num=2829, title='k-avoiding 数组的最小总和', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='贪心选小 + 等差数列求和',
    tags=['灵神题单', '难度分 1347'],
    code='''
class Solution:
    def minimumSum(self, n: int, k: int) -> int:
        m = min(k // 2, n)
        return (m * (m + 1) + (k * 2 + n - m - 1) * (n - m)) // 2
''',
    call='Solution().minimumSum(5, 4)',
    expect=18,
    views=[
        dict(type='text', fn=_text, h=110, size=28),
        dict(type='array', var=_nums, color=_color, dim=_dim, h=240, cell=70,
             label='候选正整数（绿 = 前 m 个小数，蓝 = 从 k 开始补的数，灰 = 被丢弃）'),
    ],
    watch=['n', 'k', ('m', 'm', 'green')],
    captions={
        'm = min': '`1..k-1` 里每对 `(i, k-i)` 只能选一个，选小的：最多选到 `k//2 = {k // 2}`，数量不超过 `n` → `m = min({k // 2}, {n}) = {m}`',
        'return': '前 `{m}` 个数 + 从 `k` 开始的 `{n - m}` 个数：`({m}×{m + 1} + ({k}×2+{n}-{m}-1)×{n - m}) // 2` = =={ret}==',
    },
    cards=dict(
        one_liner='小于 k 的数每对只选小的，不够再从 k 往上补',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['选 `n` 个 ==不同的正整数==，任意两数之和都不能等于 `k`',
                 '求这 `n` 个数的最小总和',
                 '示例：`n = 5, k = 4` → `[1,2,4,5,6]`，总和 `18`'],
        quote='1 和 k-1 只能选其中一个，不能都选，不然两数之和为 k。既然只能选一个，那么选 1 比选 k-1 更好。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`[1,k-1]` 内成对出现：`(1,k-1)`、`(2,k-2)`…… 选小的，直到 `k//2`',
              '还差 `n-m` 个时，只能选 `>= k` 的数：和任何数都凑不出 `k`',
              '两段都是连续整数，各用等差数列公式求和'],
        after=[dict(heading='验算 n = 5, k = 4', lines=['`m = min(2, 5) = 2`，选 `1, 2`，和 `3`',
                                                       '还差 `3` 个：从 `4` 开始 `4, 5, 6`，和 `15`',
                                                       '合计 `3 + 15 = 18`'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错：==`k` 本身可以选==，题目限制的是两数之和',
                 '`m` 要和 `n` 取最小：`n` 很小时一段就够了',
                 '`k` 是偶数时 `k/2` 也能选（只有一个，不会和自己配对）'],
    ),
)
