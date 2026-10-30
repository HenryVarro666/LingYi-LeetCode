def _bits(S):
    m = S.get('mask')
    if m is None:
        return None
    return [(m >> k) & 1 for k in range(10)]


def _scol(S, i, v):
    m = S.get('mask', 0)
    c = S.get('c')
    if c is not None and v == c:
        return 'blue'
    if (m >> (ord(v) - 97)) & 1:
        return 'green'
    return None


def _txt(S):
    if 'mask' not in S:
        return '答案 = s 中不同字母的个数 = mask 里 1 的个数'
    return f"mask = `{S['mask']:b}`（二进制），已有 ==`{S['mask'].bit_count()}`== 种字母"


CONFIG = dict(
    num=2716, title='最小化字符串长度', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='位运算 · 集合压成 mask',
    tags=[],
    code='''
class Solution:
    def minimizedStringLength(self, s: str) -> int:
        mask = 0
        for c in s:
            mask |= 1 << (ord(c) - ord('a'))  # 把 c-'a' 加到集合中
        return mask.bit_count()  # 集合的大小
''',
    call='Solution().minimizedStringLength("aabcacb")',
    expect=3,
    views=[
        dict(type='text', fn=_txt, size=28, h=60),
        dict(type='string', var='s', label='s（蓝 = 当前字母，绿 = 已进入集合）', cell=84, h=200, color=_scol),
        dict(type='array', var=_bits, label='mask 的低 10 位（第 k 位 = 1 表示字母 chr(97+k) 出现过）', cell=70, h=200,
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=[('c', 'c', 'blue'), ('mask', 'mask', 'green'), ('种类', "mask.bit_count() if 'mask' in S else 0", 'yellow')],
    captions={
        'mask = 0': '`mask = 0`：用一个整数当集合，第 k 位表示字母 `chr(97 + k)` 在不在 s 中，现在是==空集==',
        'for c in s': '取下一个字母 `c = {c}`',
        'mask |= 1 <<': lambda S, B, ret: f"`1 << {ord(S.c) - 97}` 是字母 `{S.c}` 的那一位，`|=` 把它加入集合 → `mask = {S.mask:b}`" + ("，==新字母，集合变大==" if S.mask != B.mask else "；这位本来就是 1，==重复字母，mask 不变=="),
        'return': '集合里有 `{mask.bit_count()}` 种字母，每种最多删到只剩 1 个 → 最小长度 ==`{ret}`==',
    },
    cards=dict(
        one_liner='只要有重复字母就能删，最后每种字母只剩一个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['选下标 `i`，删掉 `s[i]` 左右两侧各一个最近的同字母，操作任意次',
                 '求能达到的最短长度',
                 '示例：`"aaabc"` → `3`；`"dddaaa"` → `2`'],
        quote='根据题意，只要有重复字母，就可以继续操作。如果每种字母都只剩下一个，则无法操作。所以答案为 s 中不同字母的个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['有重复字母就能继续删，所以最终==每种字母恰好剩一个==',
              '问题变成：数 s 里有几种不同的字母',
              '灵神的位运算写法：整数 `mask` 当集合，字母 `c` 对应第 `ord(c)-97` 位'],
        summary=['时间 `O(n)`，空间 `O(1)`（只有 26 个字母）',
                 '写法一更短：`len(set(s))`，写法二用位运算压缩集合',
                 '`mask.bit_count()` 数二进制里 1 的个数，即集合大小',
                 '本视频演示 `"aabcacb"`，不同字母 `a b c` → 3'],
    ),
)
