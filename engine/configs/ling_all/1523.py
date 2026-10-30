def _odd_color(S, i, v):
    if v % 2 == 0:
        return None
    return 'green' if v >= S['low'] else 'orange'


def _text(S, B):
    if 'low' not in S:
        return ''
    low, high = S['low'], S['high']
    a, b = (high + 1) // 2, low // 2
    return (f'`[1, {high}]` 有 `({high} + 1) // 2` = =={a}== 个奇数，`[1, {low - 1}]` 有 `{low} // 2` = =={b}== 个 → `{a} − {b}` = =={a - b}==')


CONFIG = dict(
    num=1523, title='在区间范围内统计奇数数目', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='数学公式 · 前缀和思想',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1209'],
    code='''
class Solution:
    def countOdds(self, low: int, high: int) -> int:
        return (high + 1) // 2 - low // 2
''',
    call='''Solution().countOdds(3, 7)
Solution().countOdds(8, 10)
Solution().countOdds(0, 10)''',
    expect=5,
    views=[
        dict(type='text', fn=_text, h=95, size=26),
        dict(type='array', var=lambda S: list(range(1, S['high'] + 1)),
             label='1 ~ high（框 = [low, high]；绿 = 区间里的奇数；橙 = [1, low−1] 里的奇数，要减掉）', cell=84,
             window=(lambda S: max(S['low'], 1) - 1, lambda S: S['high'] - 1), index=False,
             color=_odd_color, dim=lambda S, i, v: v % 2 == 0, h=190),
        dict(type='array', var=lambda S: [2 * k - 1 for k in range(1, (S['high'] + 1) // 2 + 1)],
             label='[1, high] 里的正奇数 = 2k − 1（k = 1, 2, …, (high+1)//2），共 (high+1)//2 个', cell=84,
             color=lambda S, i, v: 'orange' if v < S['low'] else 'green', h=150),
    ],
    watch=[('low', 'low', 'blue'), ('high', 'high', 'pink'), ('(high+1)//2', '(high + 1) // 2', 'green'), ('low//2', 'low // 2', 'orange')],
    captions={
        'return': lambda S, B, ret: (f'`[1, {S.high}]` 有 `({S.high} + 1) // 2 = {(S.high + 1) // 2}` 个正奇数，`[1, {S.low - 1}]` 有 `{S.low} // 2 = {S.low // 2}` 个'
                                     f' → 相减得 =={ret}== 个'
                                     + ('；`low = 0` 时后一项是 0，也成立' if S.low == 0 else '')),
    },
    cards=dict(
        one_liner='[low, high] 的奇数 = [1, high] 的奇数 − [1, low−1] 的奇数',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给两个非负整数 `low`、`high`，返回 `[low, high]`（含两端）里的奇数个数',
                 '示例：`low=3, high=7` → `3`（3、5、7）；`low=8, high=10` → `1`（9）',
                 '本视频再多演示一个 `low=0, high=10` → `5`'],
        quote='[low, high] 中的正奇数个数，等于 [1, high] 中的正奇数个数，减去 [1, low-1] 中的正奇数个数。（这个想法类似前缀和）',
        quote_src='—— 灵茶山艾府题解',
        idea=['正奇数写成 `2k − 1`（`k` 是正整数）',
              '`[1, n]` 里：`1 ≤ 2k − 1 ≤ n` → `1 ≤ k ≤ (n+1)//2`，共 `(n+1)//2` 个',
              '套用前缀和：答案 = `(high + 1) // 2 − low // 2`（`n = low − 1` 时 `(n+1)//2 = low//2`）'],
        result='三个例子都对上了：`3`、`1`、`5` ✓',
        after=[dict(heading='思考题（灵神留的）', lines=[
            '1. 计算 `[low, high]` 中==每一位都是奇数==的整数个数',
            '2. 计算 `[low, high]` 中每一位都是奇数的整数==之和==',
            '提示：同样用前缀和的思路，转成 `[1, n]` 再相减，按位数分类数',
            '欢迎在评论区分享你的思路 / 代码'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '关键：`[1, n]` 里的奇数个数是 `(n + 1) // 2`，不是 `n // 2`',
                 '前缀和思想：区间答案 = 右端点前缀 − (左端点 − 1) 的前缀',
                 '`low = 0` 时 `low // 2 = 0`，`[1, -1]` 为空，公式依然成立'],
    ),
)
