def _b(x, w=4):
    return list(format(x, '0%db' % w))

CONFIG = dict(
    num=1009, title='十进制整数的反码', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='全 1 掩码异或 + 特判 0',
    tags=['位运算', '基础题'],
    code='''
class Solution:
    def bitwiseComplement(self, n: int) -> int:
        if n == 0:
            return 1
        w = n.bit_length()
        return ((1 << w) - 1) ^ n
''',
    call='Solution().bitwiseComplement(10)',
    expect=5,
    views=[
        dict(type='string', var=lambda S: _b(S['n']), label='n = 10', h=160),
        dict(type='string', var=lambda S: _b((1 << S['w']) - 1) if 'w' in S else _b(0), label='掩码 (1 << w) - 1',
             color=lambda S, i, v: 'blue' if v == '1' else None, h=160),
        dict(type='string', var=lambda S: _b(((1 << S['w']) - 1) ^ S['n']) if 'w' in S else _b(0), label='掩码 ^ n = 反码',
             color=lambda S, i, v: 'green' if v == '1' else None, h=160),
    ],
    watch=['n', ('w', 'w', 'blue')],
    captions={
        'if n == 0': '`n = {n}`，`n == 0` → {"成立" if n == 0 else "不成立，走一般情况"}（0 的二进制是 `0`，反码是 1，库函数算出长度 0 会出错）',
        'w = n.bit_length()': '`n = {n}` 二进制 `{n:b}`，长度 `w = {w}`：只取反低 {w} 位',
        'return ((1': '`1 << {w}` = {1 << w}，减 1 得掩码 `{(1 << w) - 1:b}`；异或 `n` 把每一位翻转 → =={ret}==',
    },
    cards=dict(
        one_liner='只翻转低 w 位：和 w 个 1 异或',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['把 `N` 的二进制每位取反（无前导零），求对应十进制数',
                 '特殊：`N = 0` 的反码是 `1`',
                 '示例：`10 = 1010` → `0101` = `5`'],
        quote='所以对于这个例子，要只把 n 的低 5 位取反，也就是计算 n 和 11111 的异或。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`~n` 会把高位的 0 也取反，不能直接用',
              '`w = n.bit_length()`，`(1 << w) - 1` 是 w 个 1',
              '`n = 0` 时库函数得到长度 0，要特判返回 1'],
        after=[dict(heading='特判 n = 0', lines=['题意：`0` 的二进制是 `0`，反码是 `1`', '但 `(0).bit_length()` 是 0', '掩码 `(1 << 0) - 1 = 0`，异或后还是 0，答案错', '所以开头单独 `if n == 0: return 1`']), dict(heading='位运算小结', lines=['异或 `1`：翻转该位；异或 `0`：保持不变', '全 1 掩码异或，等于「只翻转这几位」', '`(1 << w) - 1` 是构造低 w 位掩码的常用写法', '同类思路在位运算基础题里反复出现'])],
        summary=['时间、空间都是 `O(1)`',
                 '易错：忘记特判 `n == 0`，会返回 0',
                 '与第 476 题基本相同，只多了 0 的特判'],
    ),
)
