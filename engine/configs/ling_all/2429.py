def _bin(S):
    n = S.get('num1')
    if n is None:
        return ''
    return (f"`num1 = {n:06b}`（{n}）　置位数 `c1 = {S['c1']}`　目标 `c2 = {S['c2']}`"
            if 'c2' in S else f"`num1 = {n:06b}`")

def _diff(S):
    if 'c2' not in S:
        return ''
    c1, c2 = S['c1'], S['c2']
    return ('c2 == c1：1 的个数刚好相同，x = num1' if c2 == c1 else
            f"c2 {'<' if c2 < c1 else '>'} c1：还差 =={abs(c1 - c2)}== 个 1 {'要去掉' if c2 < c1 else '要补上'}")

CONFIG = dict(
    num=2429, title='最小异或', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='lowbit 技巧改 num1',
    tags=['灵神题单', '位运算', '难度分 1532'],
    code='''
class Solution:
    def minimizeXor(self, num1: int, num2: int) -> int:
        c1 = num1.bit_count()
        c2 = num2.bit_count()
        while c2 < c1:
            num1 &= num1 - 1  # 最低的 1 变成 0
            c2 += 1
        while c2 > c1:
            num1 |= num1 + 1  # 最低的 0 变成 1
            c2 -= 1
        return num1
''',
    call='Solution().minimizeXor(22, 1)',
    expect=16,
    views=[
        dict(type='text', fn=_bin, size=34, h=90),
        dict(type='text', fn=_diff, size=30, h=80),
        dict(type='text', fn=lambda S: (f"`num1 - 1 = {S['num1']-1:06b}`，`num1 & (num1-1)` = =={S['num1'] & (S['num1']-1):06b}==" if 'num1' in S else ''), size=28, h=80),
    ],
    watch=['num1', 'c1', ('c2', 'c2', 'yellow')],
    captions={
        'c1 =': '`num1` 有 `{c1}` 个 1',
        'c2 =': '`num2` 有 `{c2}` 个 1 → `x` 也要恰好 `{c2}` 个 1',
        'while c2 < c1': lambda S, B, ret: f"判断 `c2 < c1`（{S['c2']} < {S['c1']}）→ {'num1 的 1 比 x 允许的多，要去掉一个' if S['c2'] < S['c1'] else '不成立，不需要再去掉 1'}",
        'num1 &= num1 - 1': '多出来的 1 要去掉，且为了让异或和小，==去掉最低位的 1==（高位的 1 留着和 x 的 1 抵消）：`{B.num1:b}` → `{num1:b}`',
        'c2 += 1': '已去掉一个 1，还差 `{c1 - c2}` 个',
        'while c2 > c1': lambda S, B, ret: f"判断 `c2 > c1`（{S['c2']} > {S['c1']}）→ {'num1 的 1 不够，要在 0 位补一个 1' if S['c2'] > S['c1'] else '不成立，个数已匹配'}",
        'num1 |= num1 + 1': '多出的 1 放在 ==最低位的 0== 上，对异或和影响最小：`{B.num1:b}` → `{num1:b}`',
        'c2 -= 1': '已补上一个 1，还差 `{c2 - c1}` 个',
        'return': '1 的个数与 `num2` 相同，且高位 1 全部和 `num1` 对齐 → x = =={ret}==（`{ret:b}`）',
    },
    cards=dict(
        one_liner='高位的 1 和 num1 对齐，多退少补都从低位动手',
        complexity='时间 `O(|log num1 - log num2|)`，空间 `O(1)`',
        problem=['找正整数 `x`：置位数与 `num2` 相同，且 `x XOR num1` 最小',
                 '置位数 = 二进制里 1 的个数',
                 '示例：`num1=3, num2=5` → `3`；`num1=1, num2=12` → `3`'],
        quote='为了让异或和尽量小，这些 1 应当从高位到低位匹配 num1 中的 1；如果匹配完了还有多余的 1，那么就从低位到高位把 0 改成 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x` 的 1 与 `num1` 的 1 在同一位会抵消，高位抵消收益最大',
              '`c2 < c1`：`num1 &= num1-1` 去掉最低的 1，直到个数相同',
              '`c2 > c1`：`num1 |= num1+1` 把最低的 0 变 1，直到个数相同'],
        after=[dict(heading='两个 lowbit 小技巧', lines=['`n & (n-1)`：把最低的 1 变成 0',
                                                      '`n | (n+1)`：把最低的 0 变成 1',
                                                      '`c2 >= num1 二进制长度` 时补的 1 会补出 `2^c2 - 1`，代码自然覆盖'])],
        summary=['时间 `O(|log num1 - log num2|)`，空间 `O(1)`',
                 '先比较置位数：相等直接返回 `num1`',
                 '少了 1 就去最低的 1，多了 1 就补最低的 0',
                 '易错：别把“去掉最低的 1”写成去掉最高位'],
    ),
)
