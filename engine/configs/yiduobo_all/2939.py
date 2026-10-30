def _row(name, label, note=''):
    def f(S):
        if name not in S:
            return ''
        v = S[name]
        return f'{label} = `{v:06b}`  ({v}){note}'
    return dict(type='text', fn=f, size=29, h=54)


def _prod(S):
    if 'first' not in S or S.get('_line', 0) < 30:
        return ''
    A = S['a_high'] + S['common'] + S['first']
    Bv = S['b_high'] + S['common'] + S['second']
    return f'a^x = {A}，b^x = {Bv}，乘积 = =={A * Bv}=='


CONFIG = dict(
    num=2939, title='最大异或乘积', difficulty='Medium', category='位运算',
    author='yiduobo', technique='拆成 high / common / 分配三段',
    tags=['位运算', '贪心与思维', '难度分 2128'],
    code='''
class Solution(object):
    def maximumXorProduct(self, a, b, n):

        mod = 10 ** 9 + 7

        if n == 0:
            return a * b % mod

        a_high = a >> n << n
        b_high = b >> n << n
        
        a ^= a_high
        b ^= b_high
        c = a ^ b
        common = c ^ ((1 << n) - 1)

        first = second = 0

        if c != 0:
            if a_high == b_high:
                first = (1 << (len(bin(c)) - 3))
                second = c ^ first
            elif a_high > b_high:
                first = 0
                second = c
            else:
                first = c
                second = 0

        return (a_high + common + first) * (b_high + common + second) % mod
''',
    call='Solution().maximumXorProduct(17, 6, 4)',
    expect=360,
    views=[
        _row('a_high', 'a_high '), _row('b_high', 'b_high '), _row('a', 'a_low  '), _row('b', 'b_low  '),
        _row('c', 'c      ', '  不同位'), _row('common', 'common ', '  同为 1 的位'),
        _row('first', 'first  ', '  给 a^x'), _row('second', 'second ', '  给 b^x'),
        dict(type='text', fn=_prod, size=30, h=56),
    ],
    watch=['n', 'c', 'common', 'first', 'second'],
    captions={
        'mod = ': '先定模数 `mod`',
        'if n == 0': lambda S, B, r: '`n = 0`：x 只能是 0，直接返回 a*b' if S.n == 0 else f'`n = {S.n} != 0`：x 有 n 位可选，往下走一般情况',
        'a_high = a >>': '右移再左移，抹掉低 n 位：`a_high = {a_high:b}`，x 改不了这部分',
        'b_high = b >>': '`b_high = {b_high:b}`',
        'a ^= a_high': '去掉高位，剩下会和 x 异或的 `a_low = {a:b}`',
        'b ^= b_high': '`b_low = {b:b}`',
        'c = a ^ b': '`c = a_low ^ b_low = {c:04b}`：两数不同的位，异或后一定是一个 0 一个 1',
        'common =': '`c` 取反（在 n 位内）= 两数相同的位：x 取反让两边都是 1，`common = {common:04b}`',
        'first = second': '`first`、`second` 是 c 的 1 分给 a^x、b^x 的两份，先置 0',
        'if c != 0': lambda S, B, r: ('`c != 0`：有位可分' if S.c != 0 else '`c = 0`：没有可分的位'),
        'if a_high == b_high': lambda S, B, r: (f'`a_high == b_high`：高位一样，只要 first×second 最大' if S.a_high == S.b_high
                                                else f'`a_high != b_high`：高位已经分出大小，不能均分'),
        'first = (1 <<': '两数和一定 → 越接近积越大：first 取 c 的最高位 `{first:b}`',
        'second = c ^ first': 'second 取剩下的位 `{second:b}`',
        'elif a_high > b_high': lambda S, B, r: ('`a_high > b_high`：a 这边已经更大，c 全分给 second 让 b 追上去' if S.a_high > S.b_high
                                                  else '`a_high < b_high`：与上面对称'),
        'first = 0': '`first = 0`',
        'second = c': '`second = c = {second:b}`：全给 b^x',
        'first = c': '`first = c`：全给 a^x',
        'second = 0': '`second = 0`',
        'return (a_high': '`(a_high+common+first) × (b_high+common+second)` = `{a_high + common + first} × {b_high + common + second}` → 取模后 =={ret}==',
    },
    cards=dict(
        one_liner='三段互不重叠：高位固定、同位全 1、不同位按大小分',
        complexity='时间 `O(n)`（`bin` 长度），空间 `O(1)`',
        problem=['给 `a`、`b`、`n`，在 `0 ≤ x < 2^n` 里选 `x`',
                 '使 `(a^x) × (b^x)` 最大，结果对 `10^9+7` 取模',
                 '本视频：`a=17, b=6, n=4` → `360`'],
        quote='无论x如何取值，异或结果中也是一个0和一个1，此时就需要将c分成first和second，使得最终的异或结果乘积最大。',
        quote_src='—— yiduobo 题解原文',
        idea=['`a^x = a_high + common + first`，`b^x = b_high + common + second`',
              '展开乘积：只有 `a_high*second + b_high*first + first*second` 取决于分配',
              '高位相等看 `first*second`（均分）；高位 a 大就全给 second，反之全给 first'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`n == 0` 要单独处理：x 只能为 0',
                 '`a >> n << n` 取出高位，`common = c ^ ((1<<n)-1)` 要限定在 n 位内',
                 '原文为 Python 2 写法，无需改动即可在 Python 3 运行',
                 '对比灵神：灵神先交换保证 a≥b；这里按 high 大小三种情况分别分配'],
    ),
)
