N0 = 10


def _b32(x):
    return [int(c) for c in format(x & 0xFFFFFFFF, '032b')]


def _in_rev(S):
    return S['_line'] >= 9 and S['_line'] <= 18


def _cur(S):
    if _in_rev(S):
        return S['_inner']['n']
    return N0


def _row1(S):
    return _b32(_cur(S))


def _c1(S, k, v):
    x = _cur(S)
    hi = x.bit_length()
    if _in_rev(S):
        return 'blue' if v else None
    return 'yellow' if 32 - k <= hi else None


def _row2(S):
    if S['_line'] == 4 and 'rev' in S['_inner']:
        r = S['_inner']['rev']
        return _b32(N0 ^ r)
    return []


def _title1(S):
    if _in_rev(S):
        return '正在反转的 32 位数（把 n 当成 32 位整数，高位补 0）'
    if S['_line'] == 4:
        return 'n 的二进制（黄色 = 有效的 4 位）'
    return 'n 的二进制，补成 32 位（黄色 = 有效位）'


def _top(S):
    ln = S['_line']
    if ln == 3:
        return f"`n = {N0}` = `{N0:b}`，只有 `{N0.bit_length()}` 位：先当 32 位整数反转，再右移 `32 - {N0.bit_length()}` 位丢掉多余的 0"
    if ln == 4:
        r = S['_inner']['rev']
        return f"`n = {N0:b}`　`rev = {r:b}`（补成同样 {N0.bit_length()} 位对比）→ 异或看哪些位不同"
    return f"反转 5 步：每步把相邻的块互换，块越来越小（16 → 8 → 4 → 2 → 1）"


def _rev_label(S):
    if S['_line'] == 4:
        return f"上面一行是 `n ^ rev` = `{N0 ^ S['_inner']['rev']:04b}`（粉色 = 不同的位，每个都要翻转一次）"
    return ''


CONFIG = dict(
    num=3750, title='最少翻转次数得到反转二进制字符串', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='位反转 + 异或 + bit_count',
    tags=['灵神题单', '位运算', '难度分 1289'],
    code='''
class Solution:
    def minimumFlips(self, n: int) -> int:
        rev = self.reverseBits(n) >> (32 - n.bit_length())
        return (n ^ rev).bit_count()

    # 190. 颠倒二进制位
    def reverseBits(self, n: int) -> int:
        # 交换 16 位
        n = ((n >> 16) | (n << 16)) & 0xFFFFFFFF
        # 交换每个 8 位块
        n = (((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8)) & 0xFFFFFFFF
        # 交换每个 4 位块
        n = (((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4)) & 0xFFFFFFFF
        # 交换每个 2 位块
        n = (((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2)) & 0xFFFFFFFF
        # 交换相邻位
        n = (((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1)) & 0xFFFFFFFF
        return n
''',
    call='Solution().minimumFlips(10)',
    expect=4,
    views=[
        dict(type='text', fn=_top, size=24, h=90),
        dict(type='array', var=_row1, label='32 位二进制（从高位到低位；蓝色 = 1，黄框 = n 原有的有效位）', color=_c1, index=False, cell=31, h=170),
        dict(type='array', var=_row2, label='', color=lambda S, k, v: 'pink' if v and k >= 28 else None, index=False, cell=31, h=170),
        dict(type='text', fn=_rev_label, size=26, h=80),
    ],
    watch=[('n', lambda S: S['_inner'].get('n'), 'blue'), ('rev', lambda S: S.get('rev') if 'rev' in S['_inner'] else None, 'pink')],
    captions={
        'rev = self.reverseBits': lambda S, B, r: f"先调用 `reverseBits(n)`：把 `{N0}` 当 32 位整数反转；结果再右移 `32 - {N0.bit_length()} = {32 - N0.bit_length()}` 位，只留下原来那 {N0.bit_length()} 位的反转",
        '交换 16 位': '',
        'n >> 16) | (n << 16)': lambda S, B, r: f"高低 16 位互换：`n = {S.n:032b}`",
        '0xFF00FF00': lambda S, B, r: f"每个 8 位块内，高 4 位和低 4 位互换，`n = {S.n:032b}`"[:0] + f"相邻的两个 8 位块互换：`{S.n:032b}`",
        '0xF0F0F0F0': lambda S, B, r: f"每个 8 位块里，高 4 位和低 4 位互换：`{S.n:032b}`",
        '0xCCCCCCCC': lambda S, B, r: f"每个 4 位块里，高 2 位和低 2 位互换：`{S.n:032b}`（`1010` 恰好对称，没变）",
        '0xAAAAAAAA': lambda S, B, r: f"每个 2 位块里，两个比特互换：`{S.n:032b}` → 整个 32 位已完全反转",
        'return n': '`reverseBits` 返回反转后的 32 位数',
        'return (n ^ rev)': lambda S, B, r: f"`n ^ rev = {N0:04b} ^ {S.rev:04b} = {N0 ^ S.rev:04b}`：异或为 1 的位就是==不同的位==，`bit_count()` 数出共 =={(N0 ^ S.rev).bit_count()}== 个，每个都要翻转一次",
    },
    cards=dict(
        one_liner='n 与它的反转异或，1 的个数就是答案',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['正整数 `n` 的二进制 `s`，每次可翻转 `s` 的一位',
                 '求使 `s` 变成它自己的反转串，最少翻转几次',
                 '示例：`n = 10`（`1010`，反转 `0101`）→ `4`'],
        quote='计算 n 和 rev 有多少个位置不同，等价于计算 n ⊕ rev 的二进制中有多少个 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每个位置要么已经和反转串相同，要么必须翻转它自己，互不影响',
              '所以答案 = ==两个串不同的位数==，不同位用异或标出',
              '反转用 190 题的模板：5 次「交换相邻块」，每步 `O(1)`'],
        result='`10 ^ 5 = 1111`，四位全不同 → 返回 `4` ✓',
        after=[dict(heading='方法一：转成字符串', lines=[
            '`s = bin(n)[2:]`，遍历前一半下标 `i`',
            '`s[i] != s[-1-i]` 时，这一对都要翻转，答案加 `2`',
            '示例 `1010`：`i=0`、`i=1` 各加 2 → `4`'])],
        summary=['时间、空间都是 `O(1)`（32 位固定）',
                 '易错：反转得到的是 32 位，必须右移 `32 - n.bit_length()` 去掉高位的 0',
                 '易错：别忘了每个 `& 0xFFFFFFFF`，Python 整数不会自动溢出',
                 '同类：190 颠倒二进制位、3769 二进制反射排序'],
    ),
)
