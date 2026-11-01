CONFIG = dict(
    num='LCS 01', title='下载插件', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='二进制位数（Go 原文转写）',
    tags=['贪心与思维'],
    code='''
class Solution:
    def leastMinutes(self, n: int) -> int:
        return (n - 1).bit_length() + 1
''',
    call='Solution().leastMinutes(13)',
    expect=5,
    views=[
        dict(type='text', fn=lambda S: f"`n = {S['n']}`　`n - 1 = {S['n'] - 1}` = 二进制 `{bin(S['n'] - 1)[2:]}`，一共 =={(S['n'] - 1).bit_length()}== 位", size=30),
        dict(type='text', fn=lambda S: '翻倍 ==k== 次：带宽 `2^k`，再下载 1 分钟 → 共 `k + 1` 分钟' if S['_line'] >= 3 else '', size=26),
        dict(type='text', fn=lambda S: f"翻倍 `{(S['n'] - 1).bit_length()}` 次，带宽 `{2 ** (S['n'] - 1).bit_length()}` ≥ `{S['n']}`，下载 1 次，共 =={(S['n'] - 1).bit_length() + 1}== 分钟", size=28),
    ],
    watch=[('n', 'n')],
    captions={
        'return': '`n - 1 = {n - 1}` 的二进制长度是 `{(n - 1).bit_length()}`：翻倍 `{(n - 1).bit_length()}` 次、下载 1 次 → 共 =={ret}== 分钟',
    },
    cards=dict(
        one_liner='先把带宽翻倍到不小于 n，最后一分钟一次下完',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['带宽初始每分钟下载 1 个插件；每分钟可选择下载，或把带宽加倍',
                 '下载的插件数可以超过 `n`，求下载 `n` 个插件最少多少分钟',
                 '示例：`n = 2` → `2`；`n = 4` → `3`'],
        quote='func leastMinutes(n int) int { return bits.Len(uint(n-1)) + 1 }',
        quote_src='—— 灵茶山艾府题解代码',
        idea=['先翻倍再下载总是不亏：所以前面全部翻倍、最后只下载一次',
              '翻倍 `k` 次后带宽为 `2^k`，需要 `2^k ≥ n`，即 `2^k > n - 1`',
              '最小的 `k` 正是 `n - 1` 的二进制长度，再加 1 次下载'],
        after=[dict(heading='验证 n = 4', lines=['`n - 1 = 3 = 11₂`，长度 2', '翻倍 2 次 → 带宽 4，再下载 1 次 → 3 分钟', '和题目示例 2 的答案 3 一致'])],
        result='`n = 13`：`12 = 1100₂` 长度 4 → 4 次翻倍 + 1 次下载 = 5 分钟 ✓',
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`bits.Len(uint(x))` 即 `x.bit_length()`）',
                 '`n = 1` 时 `n - 1 = 0`，长度为 0，答案 1：直接下载一次',
                 '易错：`n` 恰好是 2 的幂时不用多翻一次，所以用 `n - 1` 而不是 `n`',
                 '时间 `O(1)`，空间 `O(1)`'],
    ),
)
