CONFIG = dict(
    num=2351, title='第一个出现两次的字母', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='位掩码当集合（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def repeatedCharacter(self, s: str) -> str:
        mask = 0
        for c in map(ord, s):
            if mask >> (c & 31) & 1 > 0:
                return chr(c)
            mask |= 1 << (c & 31)
        return ''
''',
    call="Solution().repeatedCharacter('abcdcb')",
    expect='c',
    views=[
        dict(type='string', var='s', label='s（黄 = 当前字符）', cell=100, h=190,
             color=lambda S, i, v: 'yellow' if 'mask' in S and 'c' in S and i == bin(S['mask']).count('1') - (1 if S['_line'] == 7 else 0) else None),
        dict(type='array', var=lambda S: [chr(97 + k) for k in range(26)] if 'mask' in S else None,
             label='mask 的 26 个二进制位（绿 = 该字母已出现过）', cell=32, h=170, index=False,
             color=lambda S, i, v: 'green' if S['mask'] >> (i + 1) & 1 else None),
        dict(type='text', h=80, size=28,
             fn=lambda S: f"`mask` = {S['mask']:026b}（右边是 a）" if 'mask' in S else ''),
    ],
    watch=[('c', 'c', 'blue'), ('mask', 'mask', 'green')],
    captions={
        'mask = 0': '`mask` 的第 `k` 位表示字母 k 是否出现过：用一个整数当集合，初始为空',
        'for c in map(ord, s)': lambda S, B, r: (f'取下一个字符 `{chr(S.c)}`（编码 {S.c}）' if 'c' in S else '遍历结束'),
        'if mask >> (c & 31) & 1 > 0': lambda S, B, r: (
            f'`c & 31` = {S.c & 31}（a 对应 1）：看 `mask` 的第 {S.c & 31} 位 = `{S.mask >> (S.c & 31) & 1}`'
            + ('，已经出现过 → ==这就是第二次出现==' if S.mask >> (S.c & 31) & 1 else '，还没出现过')),
        'return chr(c)': '`{chr(c)}` 是第一个凑够两次的字母，立刻返回',
        'mask |= 1 << (c & 31)': '把 `{chr(c)}` 对应的位置 1：`mask = {mask}`',
        "return ''": 'Go 原文这里返回 0；题目保证有重复字母，走不到',
    },
    cards=dict(
        one_liner='用一个整数的 26 个二进制位当集合，第一次碰到已有的位就返回',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['小写字母串 `s`，找第一个出现==第二次==的字母',
                 '比的是第二次出现的位置，谁的第二次更靠前谁就是答案',
                 '本视频：`"abcdcb"` → `"c"`（c 的第二次在下标 4，b 在 5）'],
        quote='mask>>(c&31)&1 > 0',
        quote_src='—— 灵茶山艾府题解（Go 原文）',
        idea=['`c & 31` 把字母 a–z 映射到 1–26，当作 `mask` 的位下标',
              '该位已是 1：这个字母之前出现过，现在是第二次 → 返回',
              '否则 `mask |= 1 << (c & 31)` 记下来'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`range s` 的 rune → `map(ord, s)`，`byte(c)` → `chr(c)`，结尾 `return 0` → `return \'\'`）',
                 '时间 `O(n)`，空间 `O(1)`：只有一个整数',
                 '易错：先判断再置位，顺序反了会把第一次也当成重复',
                 '位运算优先级：`mask >> k & 1 > 0` 先移位再按位与，最后比较'],
    ),
)
