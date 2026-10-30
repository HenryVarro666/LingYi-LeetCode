def _info(S):
    if 'l' not in S:
        return '只有 `a`、`b` 两种字符：==全 a 是回文，全 b 也是回文== → 最多删 2 次'
    l, r, s = S['l'], S['r'], S['s']
    if l >= r:
        return f'`l = {l} ≥ r = {r}`：指针相遇，整串是回文 → 一次删完'
    if s[l] == s[r]:
        return f'`s[{l}] = {s[l]}` 等于 `s[{r}] = {s[r]}`：这一对对得上，继续往里走'
    return f'`s[{l}] = {s[l]}` ≠ `s[{r}] = {s[r]}`：对不上 → 不是回文 → 两次删完'


CONFIG = dict(
    num=1332, title='删除回文子序列', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='只有 a、b · 答案只会是 0/1/2',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def removePalindromeSub(self, s):

        if len(s) == 0:
            return 0
        
        l = 0
        r = len(s) - 1
        while l < r and s[l] == s[r]:
            l += 1
            r -= 1
        
        if l >= r:
            return 1
        
        return 2
''',
    call="Solution().removePalindromeSub('baabbab')",
    expect=2,
    views=[
        dict(type='text', fn=_info, size=26, h=70),
        dict(type='string', var='s', label='s（蓝 = l，粉 = r）', pointers={'l': 'blue', 'r': 'pink'}, window=('l', 'r'), cell=100, h=260,
             color=lambda S, i, v: ('green' if (S.get('l') is not None and (i < S['l'] or i > S['r'])) else None)),
    ],
    watch=[('l', lambda S: S.get('l'), 'blue'), ('r', lambda S: S.get('r'), 'pink')],
    captions={
        'if len(s) == 0': '空串不用删，答案 `0`；`s` 长度为 `{len(s)}`，不是空串，往下走',
        'l = 0': '回文判断：左指针从头开始 `l = 0`',
        'r = len(s) - 1': '右指针从尾开始 `r = {r}`，两边一起往中间走',
        'while l < r': lambda S, B, r: (f'`l < r` 且 `s[{S.l}] = {S.s[S.l]}` 等于 `s[{S.r}] = {S.s[S.r]}` → 这对字符对称，继续'
                                         if S.l < S.r and S.s[S.l] == S.s[S.r] else
                                         (f'`l = {S.l} ≥ r = {S.r}` → 所有字符都配好对了' if S.l >= S.r else
                                          f'`s[{S.l}] = {S.s[S.l]}` ≠ `s[{S.r}] = {S.s[S.r]}` → 停下，不是回文')),
        'l += 1': '这一对已配好，`l` → {l}',
        'r -= 1': '`r` → {r}，继续比较里面一对',
        'if l >= r': lambda S, B, r: (f'`l = {S.l} ≥ r = {S.r}` → 是回文，==一步就能删完==' if S.l >= S.r else
                                      f'`l = {S.l} < r = {S.r}` → 中途对不上，不是回文'),
        'return 1': '整串是回文 → 答案 `1`',
        'return 2': '不是回文：先删所有 `a`（全 a 是回文），再删所有 `b` → 答案 ==2==',
    },
    cards=dict(
        one_liner='只有 a 和 b：整串回文删 1 次，否则最多 2 次',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串 `s` 只含字母 `a` 和 `b`，每次可以删掉一个回文==子序列==',
                 '返回删空 `s` 所需的最少次数',
                 '本视频：`s = "baabbab"` → `2`'],
        quote='当一个字符中所有字符相同时，该字符串必然是回文串，因此我们最多只需要两步就能删完，即先选出字符串中的所有a……',
        quote_src='—— yiduobo 题解原文',
        idea=['子序列不要求连续：先把所有 `a` 挑出来删，再删所有 `b`，==最多 2 步==',
              '如果 `s` 本身就是回文，一步删完',
              '所以只需判断 `s` 是不是回文：双指针从两端往中间比'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '空串要返回 `0`，不能漏掉',
                 '注意是==子序列==不是子串：这才让「删所有 a」成立',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
