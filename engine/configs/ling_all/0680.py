S0 = 'abcdxfdcba'


def _txt(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return f'`s = "{S0}"`：最多删一个字母，能否变成回文串？'
    if S.get('_line') == 12 or S.get('_line') == 13:
        return '`s` 本身已是回文，或前后各删一个都试过'
    return f'当前检查：`s[{i}] = {S0[i]}`，`s[{j}] = {S0[j]}`'


CONFIG = dict(
    num=680, title='验证回文串 II', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='相向双指针 · 失配后删左或删右',
    tags=['贪心与思维'],
    code='''
class Solution:
    def isPalindrome(self, s: str) -> bool:
        return s == s[::-1]

    def validPalindrome(self, s: str) -> bool:
        i, j = 0, len(s) - 1
        while i < j:
            if s[i] != s[j]:
                # 删除 s[i] 或者 s[j]
                return self.isPalindrome(s[i + 1: j + 1]) or self.isPalindrome(s[i: j])
            i += 1
            j -= 1
        return True  # s 本身就是回文串
''',
    call=f'Solution().validPalindrome({S0!r})',
    expect=True,
    views=[
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='string', var=lambda S: S0, label='s（蓝 = i，粉 = j，绿 = 已配对相等）', h=260, cell=84,
             pointers={'i': 'blue', 'j': 'pink'},
             color=lambda S, k, v: ('green' if (k < S['i'] or k > S['j']) else None) if 'i' in S and 'j' in S else None),
        dict(type='text', fn=lambda S: (f"删 `s[i]` 后剩 `{S0[S['i']+1:S['j']+1]}`；删 `s[j]` 后剩 `{S0[S['i']:S['j']]}`"
                                       if 'i' in S and 'j' in S and S0[S['i']] != S0[S['j']] else ''), size=26, h=60),
    ],
    watch=['i', 'j'],
    captions={
        'i, j = 0': '双指针从两端出发：`i = 0`，`j = {j}`',
        'while i < j': lambda S, B, r: (f'`i = {S.i} < j = {S.j}`，还有没比较的两端' if S.i < S.j else f'`i = {S.i} >= j = {S.j}`：全部配对成功'),
        'if s[i] != s[j]': lambda S, B, r: (f"`s[{S.i}] = {S.s[S.i]}` 和 `s[{S.j}] = {S.s[S.j]}` ==不相等== → 必须删一个" if S.s[S.i] != S.s[S.j]
                                             else f"`s[{S.i}] = s[{S.j}] = {S.s[S.i]}` 相等 → 两端都不删，不会错过答案"),
        'return self.isPalindrome': lambda S, B, r: f"失配：只能删 `s[i]` 或 `s[j]`，判断剩余子串是不是回文：先试删 `s[{S.i}]`，剩 `{S0[S.i + 1:S.j + 1]}`",
        'return s == s[::-1]': '`{s}` 和反转后 `{s[::-1]}` 比较 → ==`{ret}`==',
        'i += 1': '相等，`i` → {i}',
        'j -= 1': '相等，`j` → {j}',
        'return True': '`i` 与 `j` 相遇，`s` 本身就是回文 → `True`',
    },
    cards=dict(
        one_liner='两端相等就都不删，失配了才删左或删右',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定字符串 `s`，==最多==删除一个字符',
                 '判断能否得到回文串',
                 '示例：`"abca"` → `true`（删 `c`）；`"abc"` → `false`'],
        quote='如果 s[0] = s[n-1]，不删除 s[0] 也不删除 s[n-1]，是不会错过正确答案的！问题变成判断下标在 [1,n-2] 的子串，能否在删至多一个字母的情况下变成回文串。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`s[0] ≠ s[n-1]`：==必须删==，删左或删右，剩下的子串直接判回文',
              '`s[0] = s[n-1]`：删了这两端之一，总能换成删它旁边的同字母，结果一样 → ==不用删==',
              '所以相等就收缩，第一次失配时再分两种情况'],
        result='`i = 4`、`j = 5` 失配：删 `x` 剩 `f`，是回文 → `True` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`（灵神注：Python 忽略切片的时间）',
                 '易错：失配后切片要写成 `s[i+1:j+1]` 和 `s[i:j]`，别丢掉另一端',
                 '失配时用 `or`：删左、删右任意一个成功即可',
                 '思考题：有多少个 `s[i]` 删掉后能得到回文串？'],
    ),
)
