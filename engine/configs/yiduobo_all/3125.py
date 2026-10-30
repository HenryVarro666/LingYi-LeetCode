def _bits(S):
    if 'n' not in S:
        return ''
    n = S['n']
    return f"`n` = ==`{n:08b}`== = {n}"


def _low(S):
    if 'n' not in S:
        return ''
    n = S['n']
    if n & (n - 1):
        return f"`n-1` = `{n - 1:08b}`，`n & (n-1)` = `{n & (n - 1):08b}`（最低位的 1 被抹掉）"
    return f"`n` 只剩最高位的 1：`{n:08b}`，再减 1 → `{n - 1:08b}`"


CONFIG = dict(
    num=3125, title='使得按位与结果为0的最大数字', difficulty='Medium', category='位运算',
    author='yiduobo', technique='去掉低位 1，只留最高位再减 1',
    tags=['灵神题单·位运算', '灵神题单·贪心与思维'],
    code='''
class Solution(object):
    def maxNumber(self, n):

        while n & (n - 1):
            n &= (n - 1)
        return n - 1
''',
    call='Solution().maxNumber(45)',
    expect=31,
    views=[
        dict(type='text', fn=_bits, size=34, h=80),
        dict(type='text', fn=_low, size=28, h=80),
        dict(type='text', fn=lambda S: '目标：找最大的 `x`，使 `x` 到 `n` 之间所有整数按位与为 0' , size=26, h=70),
    ],
    watch=[('n', 'n', 'blue')],
    captions={
        'while n & (n - 1)': lambda S, B, r: (f'`n & (n-1)` = {S.n & (S.n - 1)} ≠ 0：`n` 还有不止一个 1，继续去掉低位的 1' if S.n & (S.n - 1)
                                             else f'`n & (n-1)` = 0：`n` = {S.n} 只剩最高位的 1 → 停'),
        'n &= (n - 1)': '去掉最低位的 1：`n` → =={n}== = `{n:08b}`',
        'return n - 1': '`n` 已是 10000… 形式，`n-1` 是 01111…：它俩的 AND 就是 0，答案 =={n - 1}==',
    },
    cards=dict(
        one_liner='区间里只要同时有 1000…0 和 0111…1，AND 就是 0',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['给定正整数 `n`，求最大的 `x`，使 `x` 到 `n` 之间所有整数的按位与为 `0`',
                 '示例：`n=7` → `3`',
                 '本视频：`n=45` → `31`'],
        quote='对于1XXXX...XXX到0YYYY...YYY之间的整数，其中必然存在10000...000以及01111...111，二者按位与结果就已经为0了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n` 的最高位一定是 1，要让 AND 为 0，区间里必须有最高位为 0 的数',
              '区间跨过 `10…0` 时，必含 `10…0` 和 `01…1`，AND 为 0',
              '所以 `x` 最大取 `10…0 - 1`：把 `n` 低位的 1 全去掉再减 1'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '`n & (n-1)` 每次抹掉最低位的 1，直到只剩最高位',
                 '等价于：答案 = 小于等于 n 的最大 2 的幂 − 1',
                 '原文为 Python 2 风格，本题无需改动代码'],
    ),
)
