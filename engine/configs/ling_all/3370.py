CONFIG = dict(
    num=3370, title='仅含置位位的最小整数', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='二进制长度 → 2^m − 1',
    tags=['灵神题单', '位运算', '难度分 1199'],
    code='''
class Solution:
    def smallestNumber(self, n: int) -> int:
        return (1 << n.bit_length()) - 1
''',
    call='Solution().smallestNumber(10)',
    expect=15,
    views=[
        dict(type='text', size=34, fn=lambda S: f"`n = {S['n']}` 的二进制：==`{bin(S['n'])[2:]}`==，长度 `m = {S['n'].bit_length()}`"),
        dict(type='text', size=34, fn=lambda S: f"`1 << m` = `{bin(1 << S['n'].bit_length())[2:]}`（{1 << S['n'].bit_length()}）"),
        dict(type='text', size=34, fn=lambda S: f"减一后全是 1：==`{bin((1 << S['n'].bit_length()) - 1)[2:]}`== = {(1 << S['n'].bit_length()) - 1}"),
    ],
    watch=[('n', 'n', 'blue'), ('m', "n.bit_length()", 'cyan'), ('答案', "(1 << n.bit_length()) - 1", 'green')],
    captions={
        'return': '`m = {n.bit_length()}`：`1 << {n.bit_length()}` = {1 << n.bit_length()}（1 后面 {n.bit_length()} 个 0），再减一 → {n.bit_length()} 个 1 = =={(1 << n.bit_length()) - 1}==',
    },
    cards=dict(
        one_liner='答案的二进制长度和 n 一样，全填 1 就是 2^m − 1',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给正整数 `n`，求 ==不小于 n== 且二进制全为 1 的最小整数',
                 '示例：`n = 5` → `7`（`111`）；`n = 10` → `15`（`1111`）',
                 '本视频：`n = 10` → `15`'],
        quote='计算 n 的二进制长度 m，那么答案的二进制长度至少是 m。由于长为 m 的全为 1 的二进制数 ≥ n，满足要求，所以答案的二进制长度就是 m。',
        quote_src='—— 灵茶山艾府题解',
        idea=['长度 `m` 的二进制数里，最大的就是全 1，必然 `≥ n`',
              '长度小于 `m` 的全 1 数都 `< n`，所以答案长度恰好是 `m`',
              '`1 << m` 是 1 后跟 m 个 0，减一就变成 m 个 1'],
        after=[dict(heading='再验证两个例子', lines=['`n = 5 = 101`，长度 3 → `2^3 − 1 = 7 = 111`',
                                              '`n = 3 = 11`，长度 2 → `2^2 − 1 = 3`，已经全是 1',
                                              '`n = 10 = 1010`，长度 4 → `15 = 1111`'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '`n.bit_length()` 就是二进制长度，别写成 `bit_count()`（那是 1 的个数）',
                 '`n = 3` 本身就是全 1，公式给出 `3`，不会多一位',
                 '思考题：改成 `> n` 时，对 `n + 1` 套同样的公式即可'],
    ),
)
