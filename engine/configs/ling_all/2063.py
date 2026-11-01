def _txt(S):
    if 'i' not in S or 'ans' not in S:
        return ''
    n = len(S['word'])
    i = S['i']
    if S['word'][i] in 'aeiou':
        return f"`{S['word'][i]}` 是元音：左端点 `{i+1}` 种 × 右端点 `{n-i}` 种 = =={(i+1)*(n-i)}== 个子串包含它"
    return f"`{S['word'][i]}` 不是元音，不贡献"


CONFIG = dict(
    num=2063, title='所有子字符串中的元音', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='贡献法 · (i+1)(n-i)（Go 原文转写）',
    tags=['灵神题单', '贪心与思维', '难度分 1663'],
    code='''
class Solution:
    def countVowels(self, word: str) -> int:
        ans = 0
        for i, ch in enumerate(word):
            if ch in "aeiou":
                ans += (i + 1) * (len(word) - i)
        return ans
''',
    call='Solution().countVowels("abeco")',
    expect=19,
    views=[
        dict(type='string', var='word', label='word（蓝 = 当前字符 i，绿 = 已累计的元音）', cell=96, pointers={'i': 'blue'},
             color=lambda S, i, v: ('green' if v in 'aeiou' and 'i' in S and i <= S['i'] else None)),
        dict(type='text', size=34, h=140, fn=_txt),
    ],
    watch=[('i', 'i', 'blue'), 'ch', ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 累计「每个元音出现在多少个子串里」',
        'for i, ch': '考察第 `{i}` 个字符 `{ch}`',
        'if ch in': lambda S, B, r: (f"`{S.ch}` 是元音 → 统计它的贡献" if S.ch in 'aeiou' else f"`{S.ch}` 不是元音 → 跳过"),
        'ans += (i + 1)': '包含 `word[{i}]` 的子串：左端点 `0..{i}` 共 `{i+1}` 种，右端点 `{i}..{len(word)-1}` 共 `{len(word)-i}` 种 → `{(i+1)*(len(word)-i)}`，`ans` 从 {B.ans} 变成 =={ans}==',
        'return ans': '所有元音的贡献之和 =={ans}==',
    },
    cards=dict(
        one_liner='不数子串，数每个元音出现在多少个子串里',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['求 `word` 所有子字符串中元音字母（`aeiou`）的总个数',
                 '示例：`"aba"` → `6`',
                 '本视频：`"abeco"` → `19`'],
        quote='遍历 word，若 word[i] 是元音，我们考察它能出现在多少个子字符串中。……这样的 l 有 i+1 个，r 有 n-i 个，因此有 (i+1)(n-i) 个子字符串。',
        quote_src='—— 灵茶山艾府题解',
        idea=['子串 `word[l..r]` 含 `word[i]` ⇔ `0 ≤ l ≤ i` 且 `i ≤ r ≤ n-1`',
              'l 有 `i+1` 个选择，r 有 `n-i` 个，相乘就是出现次数',
              '把所有元音的出现次数加起来就是答案'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(n)`，空间 `O(1)`',
                 '易错点：答案可能超过 32 位整数（Go 用 int64，Python 不用担心）',
                 '同类「贡献法」：不枚举整体，枚举每个元素的贡献'],
    ),
)
