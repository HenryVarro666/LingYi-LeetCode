def _hi(S):
    return [2 * k - 1 for k in range((S['high'] + 1) // 2 + 1) if k >= 1]


def _lo(S):
    return [2 * k - 1 for k in range(1, S['low'] // 2 + 1)]


def _text(S, B):
    if 'low' not in S:
        return ''
    low, high = S['low'], S['high']
    k1, k2 = (high + 1) // 2, low // 2
    return (f'`[1, {high}]`：`k = ({high} + 1) // 2` = =={k1}==；`[1, {low - 1}]`：`k = ({low - 1} + 1) // 2` = =={k2}==')


CONFIG = dict(
    num=1523, title='在区间范围内统计奇数数目', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='前缀思想 · 奇数写成 2k−1',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1209'],
    code='''
class Solution(object):
    def countOdds(self, low, high):

        return (high + 1) // 2 - low // 2
''',
    call='''Solution().countOdds(3, 7)
Solution().countOdds(8, 10)
Solution().countOdds(2, 2)''',
    expect=0,
    views=[
        dict(type='text', fn=_text, h=95, size=26),
        dict(type='array', var=_hi, label='[1, high] 里的奇数 = 1×2−1, 2×2−1, …, k×2−1（橙 = 同时在 [1, low−1] 里，要减掉）', cell=84,
             color=lambda S, i, v: 'orange' if v < S['low'] else 'green', index=False, h=150),
        dict(type='array', var=_lo, label='[1, low−1] 里的奇数（k = low // 2 个；空的话就是没有）', cell=84,
             color=lambda S, i, v: 'orange', index=False, h=150),
        dict(type='text', fn=lambda S: f"`{(S['high'] + 1) // 2} − {S['low'] // 2}` = =={(S['high'] + 1) // 2 - S['low'] // 2}== 个绿色的奇数留下来" if 'low' in S else '', h=60, size=28),
    ],
    watch=[('low', 'low', 'blue'), ('high', 'high', 'pink'), ('(high+1)//2', '(high + 1) // 2', 'green'), ('low//2', 'low // 2', 'orange')],
    captions={
        'return': lambda S, B, ret: (f'`[1, {S.high}]` 的奇数个数 `k = ({S.high} + 1) // 2 = {(S.high + 1) // 2}`；`[1, {S.low - 1}]` 的是 `{S.low // 2}`'
                                     f' → 差 =={ret}==' + ('：`[2, 2]` 里只有偶数 2，没有奇数' if (S.low, S.high) == (2, 2) else '')),
    },
    cards=dict(
        one_liner='用前缀相减避开边界判断：[1, high] 的奇数 − [1, low−1] 的奇数',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给两个非负整数 `low`、`high`，返回 `[low, high]`（含两端）里的奇数个数',
                 '示例：`low=3, high=7` → `3`；`low=8, high=10` → `1`',
                 '本视频再多演示 `low=2, high=2` → `0`（区间里只有偶数）'],
        quote='直接统计[low, high]中奇数数目的话涉及到low和high边界的判断，稍显复杂，那么也可以利用前缀来进行判断……',
        quote_src='—— yiduobo 题解原文',
        idea=['`[low, high]` 的奇数 = `[1, high]` 的奇数 − `[1, low−1]` 的奇数，不用管端点是奇是偶',
              '`[1, x]` 的奇数写成 `1×2−1, 2×2−1, …, k×2−1`，找最大的 `k` 满足 `2k − 1 ≤ x`',
              '解得 `k = (x + 1) // 2`（整除），`k` 就是奇数的个数',
              '代入：`(high + 1) // 2 − (low − 1 + 1) // 2 = (high + 1) // 2 − low // 2`'],
        result='三个例子：`3`、`1`、`0` ✓（`expect` 取最后一个）',
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '`[1, x]` 的奇数个数是 `(x + 1) // 2`，注意是整除',
                 '把 `low − 1` 代进去，`(low − 1 + 1) // 2` 就化简成 `low // 2`',
                 '原文为 Python 2 写法，`/` 是整除，已改为 `//`',
                 '对比灵神：思路相同，灵神用「正奇数 = 2k−1」直接解不等式，这里写成逐项列出再找最大 k'],
    ),
)
