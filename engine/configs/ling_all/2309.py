def _letters(S, k):
    m = S.get('masks')
    if not m:
        return ''
    return ' '.join(chr(64 + b) if k == 0 else chr(96 + b) for b in range(1, 27) if m[k] >> b & 1) or '（空）'


def _txt(S):
    if 'masks' not in S:
        return ''
    s = f"大写集合 masks[0]：{_letters(S, 0)}\n小写集合 masks[1]：{_letters(S, 1)}"
    return s


CONFIG = dict(
    num=2309, title='兼具大小写的最好英文字母', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='两个整数当位集合，按位与取最高位（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def greatestLetter(self, s: str) -> str:
        masks = [0, 0]
        for c in map(ord, s):
            masks[c >> 5 & 1] |= 1 << (c & 31)
        mask = masks[0] & masks[1]
        if mask == 0:
            return ""
        return chr(ord('A') + mask.bit_length() - 2)
''',
    call="Solution().greatestLetter('arRAzFif')",
    expect='R',
    views=[
        dict(type='string', var='s', h=170,
             color=lambda S, i, v: 'blue' if 'c' in S and S['_line'] in (5,) and ord(v) == S['c'] else None),
        dict(type='text', fn=lambda S: (f"大写集合 `masks[0]`：{_letters(S, 0)}" if 'masks' in S else ''), h=60),
        dict(type='text', fn=lambda S: (f"小写集合 `masks[1]`：{_letters(S, 1)}" if 'masks' in S else ''), h=60),
        dict(type='text', fn=lambda S: (f"都出现的字母 `mask = {S['mask']:027b}` → 最高位 {S['mask'].bit_length()}" if 'mask' in S else ''), h=60),
    ],
    watch=['c', ('masks[0]', 'masks[0] if "masks" in S else 0', 'cyan'), ('masks[1]', 'masks[1] if "masks" in S else 0', 'pink')],
    captions={
        'masks = [0, 0]': '`masks[0]` 存大写字母、`masks[1]` 存小写字母，每个字母占一位',
        'for c in map': '取下一个字符，`c` 是它的 ASCII 码 {c}（`{chr(c)}`）',
        'masks[c >> 5': '大写 ASCII 第 5 位是 0、小写是 1，所以 `c >> 5 & 1 = {c >> 5 & 1}` 选 {"小写" if c >> 5 & 1 else "大写"}集合；`c & 31` = {c & 31} 是它在字母表中的位置 → 置位',
        'mask = masks[0] & masks[1]': '两个集合按位与：只留下==大小写都出现==的字母，`mask = {mask:b}`',
        'if mask == 0': '{"没有任何字母两种形式都出现" if mask == 0 else "至少有一个字母满足，取最高位"}',
        'return ""': '没有满足的字母，返回空串',
        'return chr': '`mask` 最高位是 {mask.bit_length()}，字母 = `A + {mask.bit_length()} − 2`（因为 A 在第 1 位） → =={ret}==',
    },
    cards=dict(
        one_liner='大小写各存成一个整数位集合，按位与后最高位就是答案',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找出大小写形式在 `s` 中都出现的字母，返回其中字母表最靠后的大写形式',
                 '没有就返回空串',
                 '示例：`"arRAzFif"` → `"R"`'],
        quote='位运算做法：存储每个字符是否出现过，然后大写字母区域和小写字母区域按位与，二进制数的长度就是第几个大写字母。这样可以做到 O(1) 空间复杂度。',
        quote_src='—— 灵茶山艾府题解',
        idea=['大写 ASCII 的第 5 位是 0，小写是 1 → `c >> 5 & 1` 区分',
              '`c & 31` 把字母映射到 1~26 位',
              '两个集合 `&` 之后，二进制长度就是最大字母的位置，用 `bit_length` 取出'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python；原文有三种写法，这里取最后一种（两个整数）',
                 '另两种：哈希表从 Z 到 A 枚举；一个 mask 里 `mask &= mask >> 32` 后取最高位',
                 '时间 `O(n)`，空间 `O(1)`',
                 '易错：A 在第 1 位而非第 0 位，所以长度要减 2 才对应 `A`'],
    ),
)
