CONFIG = dict(
    num=3827, title='统计单比特整数', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='全 1 数 = 2^k − 1，数 k 的个数',
    tags=['灵神题单', '位运算'],
    code='''
class Solution:
    def countMonobit(self, n: int) -> int:
        return (n + 1).bit_length()
''',
    call='Solution().countMonobit(10)',
    expect=4,
    views=[
        dict(type='text', size=32, fn=lambda S: f"`n + 1 = {S['n'] + 1}` = ==`{bin(S['n'] + 1)[2:]}`==，二进制长度 `w = {(S['n'] + 1).bit_length()}`"),
        dict(type='text', size=32, fn=lambda S: "单比特数 = `0` 或 `2^k − 1`：" + '、'.join(str((1 << k) - 1) for k in range((S['n'] + 1).bit_length())) + f"（都 `≤ {S['n']}`）"),
        dict(type='text', size=32, fn=lambda S: f"`k = 0 ~ w−1`，共 ==`{(S['n'] + 1).bit_length()}`== 个"),
    ],
    watch=[('n', 'n', 'blue'), ('w', '(n + 1).bit_length()', 'cyan')],
    captions={
        'return': '`n + 1 = {n + 1}` 的二进制长度是 `w = {(n + 1).bit_length()}`，`k` 取 `0 ~ {(n + 1).bit_length() - 1}` 共 =={(n + 1).bit_length()}== 个 `2^k − 1` → 答案 {ret}',
    },
    cards=dict(
        one_liner='单比特数就是 0 或 2^k−1，数一数有几个 k',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['二进制所有位都相同的数叫 ==单比特数==，求 `[0, n]` 里有多少个',
                 '示例：`n = 4` → `3`（`0`、`1`、`3`）',
                 '本视频：`n = 10` → `4`（`0`、`1`、`3`、`7`）'],
        quote='非负整数 x 二进制的所有位都相同，意味着 x = 0 或者 x 的二进制全为 1，即 x = 2^k − 1，其中 k 是非负整数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['问题变成：`[0, n]` 里有多少个不同的 `k`，使 `0 ≤ 2^k − 1 ≤ n`',
              '等价于 `1 ≤ 2^k ≤ n + 1`，所以 `k ≤ w − 1`，`w` 是 `n+1` 的二进制长度',
              '`k = 0 ~ w−1` 恰好 `w` 个，答案就是 `(n+1).bit_length()`'],
        after=[dict(heading='用示例核对公式', lines=['`n = 4`：`n + 1 = 5 = 101`，长度 3 → 答案 `3`（`0, 1, 3`）',
                                              '`n = 1`：`n + 1 = 2 = 10`，长度 2 → 答案 `2`（`0, 1`）',
                                              '`n = 10`：`n + 1 = 11 = 1011`，长度 4 → 答案 `4`（`0, 1, 3, 7`）'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '是 `n + 1` 的二进制长度，不是 `n` 的：`n = 7` 时答案是 4，不是 3',
                 '`0` 也是单比特数，它对应 `k = 0`（`2^0 − 1 = 0`），不要漏',
                 '全 0 和全 1 合并成一个式子，是这题的关键观察'],
    ),
)
