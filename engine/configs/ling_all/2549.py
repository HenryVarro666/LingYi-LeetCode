CONFIG = dict(
    num=2549, title='统计桌面上的不同数字', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='n % (n-1) = 1 一路递推',
    tags=['贪心与思维', '脑筋急转弯', '难度分 1266'],
    code='''
class Solution:
    def distinctIntegers(self, n: int) -> int:
        return n - 1 if n > 1 else 1  # max(n - 1, 1)
''',
    call='Solution().distinctIntegers(5)',
    expect=4,
    views=[
        dict(type='array', var=lambda S: list(range(1, S['n'] + 1)) if 'n' in S else [], label='最终桌面上的数字 1..n（绿 = 会出现在桌面上）', h=240,
             color=lambda S, i, v: 'green' if v >= 2 else None, dim=lambda S, i, v: v < 2),
        dict(type='text', fn=lambda S: f"`n = {S['n']}`：数字 `2 ~ {S['n']}` 都会出现，共 `{S['n']} - 1` = =={max(S['n'] - 1, 1)}== 个" if 'n' in S and S['n'] > 1 else ('`n = 1`：桌面上只有 1' if 'n' in S else ''), size=30),
    ],
    watch=[('n', 'n', 'blue')],
    captions={
        'return': '`n > 1` 成立 → 答案 `n - 1 = {n - 1}`：`n % (n-1) = 1`，所以 `n-1` 上桌，再往下 `n-2`…直到 2，返回 =={ret}==',
    },
    cards=dict(
        one_liner='n % (n-1) = 1 恒成立，数字从 n 一路递推到 2',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['桌面上有正整数 `n`，每天对每个桌上的 `x`，把所有满足 `x % i == 1`（`1<=i<=n`）的 `i` 也放上桌',
                 '求 `10^9` 天后，桌上有几个不同的数',
                 '示例：`n = 5` → `4`（桌上是 2、3、4、5）'],
        quote='由于 n mod (n-1) = 1 一定满足要求，我们可以从 n 开始，不断生成 n-1, n-2, ...，最后 [2,n] 中的数字都会在桌面上。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`n % (n-1) = 1`，所以 `n-1` 上桌；同理 `n-1 % (n-2) = 1`，`n-2` 也上桌',
              '一直递推到 2，`[2, n]` 全部出现，共 `n-1` 个',
              '`10^9` 天足够长，不用模拟天数'],
        after=[dict(heading='特判与简写', lines=['`n = 1` 时桌上只有 1，`n - 1 = 0` 是错的，所以答案是 1', '代码注释里的 `max(n - 1, 1)` 是等价的简写', '1 永远不会出现：任何 `x % 1` 都是 0'])],
        summary=['时间、空间都是 `O(1)`',
                 '易错点：`n = 1` 要特判，答案是 1 而不是 0',
                 '`n = 2` 时 `n - 1 = 1`，结果也对（桌上只有 2）',
                 '同类题：脑筋急转弯 · 找不变量/递推链'],
    ),
)
