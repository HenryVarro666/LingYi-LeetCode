def _isv(ch):
    return ch in 'AEIOUaeiou'


CONFIG = dict(
    num=2785, title='将字符串中的元音字母排序', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='元音位运算判断 · 排序填空',
    tags=[],
    code='''
class Solution:
    def sortVowels(self, s: str) -> str:
        VOWEL_MASK = 0x208222
        is_vowel = lambda ch: VOWEL_MASK >> (ord(ch) & 31) & 1

        vowels = sorted(filter(is_vowel, s))
        t = list(s)  # str 无法修改，转成 list
        j = 0
        for i, ch in enumerate(t):
            if is_vowel(ch):
                t[i] = vowels[j]  # 填空
                j += 1
        return ''.join(t)
''',
    call='Solution().sortVowels("lEetcOde")',
    expect='lEOtcede',
    views=[
        dict(type='text', fn=lambda S: ('元音排好序后，按顺序填回元音的位置（辅音不动）' if 'vowels' in S else '先找出所有元音（二进制位判断）'), size=26),
        dict(type='string', var='s', label='s（原串）', cell=84,
             color=lambda S, i, v: 'orange' if _isv(v) else None),
        dict(type='array', var='vowels', label='vowels（排序后的元音，ASCII 小的在前，大写在小写前）', cell=84,
             pointers={'j': 'pink'}, color=lambda S, k, v: 'green' if k < S.get('j', 0) else None),
        dict(type='array', var='t', label='t（辅音原地不动，元音逐个填空）', cell=84,
             pointers={'i': 'blue'}, color=lambda S, k, v: ('green' if _isv(v) and k < S.get('i', 0) else None)),
    ],
    watch=[('i', 'i', 'blue'), ('ch', 'ch'), ('j', 'j', 'pink')],
    captions={
        'VOWEL_MASK =': '元音 `aeiou` 是第 1,5,9,15,21 个字母，压成一个整数 `0x208222`：==第 k 位为 1 就表示第 k 个字母是元音==',
        'is_vowel =': '`ord(ch) & 31` 把大小写字母统一成 1~26，再右移 `& 1` 就是查表：大小写同一套规则',
        'vowels = sorted': '`vowels = {vowels}`：把元音挑出来排序，大写 ASCII 更小所以排前面',
        't = list(s)': '字符串不能修改，转成 list：`t = {t}`',
        'j = 0': '`j` 指向下一个要填的元音：`vowels[{j}]`',
        'for i, ch': lambda S, B, r: f"遍历 t：`i = {S.i}`，`ch = '{S.ch}'`",
        'if is_vowel(ch)': lambda S, B, r: (f"`'{S.ch}'` 是元音 → 这是个==空位==，要填入排好序的元音" if _isv(S.ch)
                                            else f"`'{S.ch}'` 是辅音 → 原地不动"),
        't[i] = vowels[j]': "空位 `t[{i}]` 填入 `vowels[{j}] = '{t[i]}'`",
        'j += 1': '用掉一个元音，`j` → {j}',
        "return ''.join": "拼回字符串：`\"{ret}\"`",
    },
    cards=dict(
        one_liner='元音挑出来排序，再按顺序填回元音留下的空位',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['把 `s` 里的元音（大小写 `aeiou`）按 ASCII 非递减重排，==辅音留在原位==',
                 '示例：`s = "lEetcOde"` → `"lEOtcede"`',
                 '元音 `EeOe` 排序后为 `EOee`'],
        quote='原来的 s 视作 l__tc_d_，包含 4 个空位。在空位依次填入 EOee，得到答案 lEOtcede。',
        quote_src='—— 灵茶山艾府题解',
        idea=['元音集合 `{a,e,i,o,u}` 看成整数 `2^1+2^5+2^9+2^15+2^21 = 0x208222`',
              '`ch & 31` 把大小写都变成 1~26，`mask >> k & 1` 即可判断是否元音',
              '先排序元音，再遍历 `t`，遇到元音位置就按顺序填空'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错：str 不可变，要先 `list(s)`；大写 ASCII 比小写小，排序后大写在前',
                 '另有写法一（`ch in "AEIOUaeiou"` 判断）和写法三（计数排序，`O(n+|Σ|)`），思路相同',
                 '位运算技巧：`ch & 31` 忽略大小写，集合压成整数做 O(1) 判断'],
    ),
)
