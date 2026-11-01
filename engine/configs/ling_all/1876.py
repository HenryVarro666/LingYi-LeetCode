CONFIG = dict(
    num=1876, title='长度为三且各字符不同的子字符串', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='定长窗口 · 三字符两两比较（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def countGoodSubstrings(self, s: str) -> int:
        ans = 0
        for i in range(2, len(s)):
            if s[i-2] != s[i-1] and s[i-2] != s[i] and s[i-1] != s[i]:
                ans += 1
        return ans
''',
    call='Solution().countGoodSubstrings("aababcabc")',
    expect=4,
    views=[
        dict(type='string', var='s', window=(lambda S: S['i'] - 2, 'i'), cell=80, h=240,
             pointers={'i': 'blue'},
             color=lambda S, i, v: 'green' if 'i' in S and S['i'] - 2 <= i <= S['i'] and len({S['s'][S['i']-2], S['s'][S['i']-1], S['s'][S['i']]}) == 3 else None),
        dict(type='text', size=30, h=80, fn=lambda S: f"窗口 `{S['s'][S['i']-2:S['i']+1]}`" if 'i' in S else ''),
    ],
    watch=['i', ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 统计好子串个数',
        'for i in range': '窗口右端点 `i = {i}`，窗口是 `s[{i-2}..{i}]` = `{s[i-2:i+1]}`',
        'if s[i-2]': lambda S, B, r: (f'`{S.s[S.i-2]}` `{S.s[S.i-1]}` `{S.s[S.i]}` 两两都不同 → ==是好子串==' if len({S.s[S.i-2], S.s[S.i-1], S.s[S.i]}) == 3
                                      else f'`{S.s[S.i-2]}` `{S.s[S.i-1]}` `{S.s[S.i]}` 有重复字符 → 不是'),
        'ans += 1': '好子串 +1：`ans = {ans}`',
        'return': '共 `{ret}` 个好子串',
    },
    cards=dict(
        one_liner='窗口只有 3 个字符，两两比较三次就够',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['不含重复字符的字符串叫好字符串',
                 '求 `s` 中长度为 3 的好子串个数（重复出现要重复计）',
                 '示例：`"aababcabc"` → `4`'],
        quote='func countGoodSubstrings(s string) (ans int) { for i := 2; i < len(s); i++ { if s[i-2] != s[i-1] && s[i-2] != s[i] && s[i-1] != s[i] { ans++ } } return }',
        quote_src='—— 灵茶山艾府题解（Go 原文）',
        idea=['枚举窗口右端点 `i`，窗口就是 `s[i-2], s[i-1], s[i]`',
              '三个字符两两不等就是好子串，`ans++`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(n)`，空间 `O(1)`',
                 '易错点：`i` 从 2 开始，保证 `i-2 >= 0`',
                 '三对都要比：`i-2` 与 `i-1`、`i-2` 与 `i`、`i-1` 与 `i`'],
    ),
)
