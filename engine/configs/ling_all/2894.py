CONFIG = dict(
    num=2894, title='分类求和并作差', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='等差数列求和 · O(1)', tags=[],
    code='''
class Solution:
    def differenceOfSums(self, n: int, m: int) -> int:
        return n * (n + 1) // 2 - n // m * (n // m + 1) * m
''',
    call='Solution().differenceOfSums(10, 3)',
    expect=19,
    views=[
        dict(type='text', size=34, fn=lambda S: f"`[1, {S['n']}]` 中 `{S['m']}` 的倍数有 `k = {S['n']} // {S['m']}` = =={S['n']//S['m']}== 个"),
        dict(type='text', size=34, fn=lambda S: f"全部之和 `n(n+1)/2` = =={S['n']*(S['n']+1)//2}=="),
        dict(type='text', size=34, fn=lambda S: f"倍数之和 `num2 = k(k+1)/2 × m` = =={S['n']//S['m']*(S['n']//S['m']+1)//2*S['m']}=="),
        dict(type='text', size=34, fn=lambda S: f"答案 = 全部之和 − 2 × num2 = =={S['n']*(S['n']+1)//2 - S['n']//S['m']*(S['n']//S['m']+1)*S['m']}=="),
    ],
    watch=['n', 'm'],
    captions={
        'return': '全部之和 `{n*(n+1)//2}` 减去 `2 × num2`（`k(k+1)m = {n//m*(n//m+1)*m}`）→ =={ret}==',
    },
    cards=dict(
        one_liner='num1 − num2 = 全部之和 − 2 × 倍数之和',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`[1, n]` 中，不能被 `m` 整除的数之和为 `num1`，能被整除的为 `num2`',
                 '返回 `num1 - num2`',
                 '示例：`n=10, m=3` → `37 - 18 = 19`'],
        quote='num1 相当于 (1+2+…+n) - num2，所以 num1 - num2 = n(n+1)/2 - num2·2 = n(n+1)/2 - k(k+1)m。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`[1,n]` 里 `m` 的倍数有 `k = n // m` 个：`m, 2m, ..., km`',
              '它们的和 = `(1+…+k)·m = k(k+1)/2 · m`',
              'num1 = 总和 − num2，所以差 = 总和 − 2·num2，一行公式搞定'],
        after=[dict(heading='验算示例 n=10, m=3', lines=[
            '倍数：`3, 6, 9`，`k = 10 // 3 = 3`，`num2 = 3×4/2×3 = 18`',
            '总和 `10×11/2 = 55`，`num1 = 55 - 18 = 37`',
            '`num1 - num2 = 55 - 2×18 = ==19==`',
            '对照暴力：逐个判断整除，也是 19，但要 `O(n)`'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '`n // m` 向下取整，`n < m` 时 `k = 0`，num2 = 0',
                 '`m = 1` 时全是倍数，答案为负：`-n(n+1)/2`',
                 '对比暴力遍历 `O(n)`：公式直接算出，不用枚举'],
    ),
)
