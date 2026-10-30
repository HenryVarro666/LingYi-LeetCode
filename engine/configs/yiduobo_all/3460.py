CONFIG = dict(
    num=3460, title='最多删除一次后的最长公共前缀', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='双指针 · 失配后跳过 s 的一个字符',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def longestCommonPrefix(self, s, t):
        
        p = 0
        q = 0
        while p < len(s) and q < len(t) and s[p] == t[q]:
            p += 1
            q += 1

        p += 1
        while p < len(s) and q < len(t) and s[p] == t[q]:
            p += 1
            q += 1
        
        return q
''',
    call="Solution().longestCommonPrefix('abxcd', 'abcdef')",
    expect=4,
    views=[
        dict(type='string', var='s', label='s（p 在这里走，最多跳过一个字符）', pointers={'p': 'blue'}, h=170,
             color=lambda S, i, v: 'green' if ('p' in S and i < S['p'] and S.get('_line', 0) <= 8) else None),
        dict(type='string', var='t', label='t（q 在这里走，q 就是公共前缀长度）', pointers={'q': 'pink'}, h=170,
             color=lambda S, i, v: 'green' if ('q' in S and i < S['q']) else None),
        dict(type='text', fn=lambda S: f"已匹配的公共前缀长度 q = =={S['q']}==" if 'q' in S else ''),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink')],
    captions={
        'p = 0': '`p` 在 `s` 上走',
        'q = 0': '`q` 在 `t` 上走，最终答案就是 `q`',
        6: lambda S, B, r: ('`s[p] == t[q]`（{} = {}）→ 相等，这段前缀不用删，继续匹配'.format(S.s[S.p], S.t[S.q]) if (S.p < len(S.s) and S.q < len(S.t) and S.s[S.p] == S.t[S.q])
                            else (f'`s[{S.p}] = {S.s[S.p]}`，`t[{S.q}] = {S.t[S.q]}`：==不相等== → 第一段匹配结束' if (S.p < len(S.s) and S.q < len(S.t)) else '有一边走到末尾 → 第一段匹配结束')),
        7: '匹配成功，`p` 前进：`p = {p}`',
        8: '`q` 同步前进：`q = {q}`',
        10: '`s[p]` 无法匹配 `t[q]` → ==删掉 s[p]==（只有一次机会），`p` 跳到 `{p}`，`q` 不动',
        11: lambda S, B, r: ((f'`s[{S.p}] = {S.s[S.p]}`，`t[{S.q}] = {S.t[S.q]}`：相等 → 继续匹配') if (S.p < len(S.s) and S.q < len(S.t) and S.s[S.p] == S.t[S.q])
                             else (f'`s[{S.p}] = {S.s[S.p]}`，`t[{S.q}] = {S.t[S.q]}`：不相等 → 公共前缀到此为止' if (S.p < len(S.s) and S.q < len(S.t)) else '有一边走到末尾 → 匹配结束')),
        12: '`p` 前进：`p = {p}`',
        13: '`q` 前进：`q = {q}`，匹配长度 +1',
        'return q': 't 中走过的字符就是公共前缀，长度 `q = {ret}`',
    },
    cards=dict(
        one_liner='先正常匹配，失配时删掉 s 的那个字符，再继续匹配',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给两个字符串 `s` 和 `t`，可以从 `s` 中==最多删除一个字符==（也可以不删）',
                 '求删除后 `s` 与 `t` 的最长公共前缀的长度',
                 '本视频：`s = "abxcd"`，`t = "abcdef"` → `4`'],
        quote='若s的某个前缀可以与t的某个前缀相同，那么就不应该从这个前缀中删除任何字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['`p` 在 `s` 上、`q` 在 `t` 上，同时往后走，直到失配或走到末尾',
              '失配时 `s[p]` 无法匹配 `t[q]`，==此处正是该删的字符==：`p += 1`',
              '跳过后继续同样的匹配；`t` 中走过的字符就是公共前缀，长度为 `q`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '删除只会发生在第一次失配处：之前删任何字符都不会更好',
                 '`p += 1` 不管有没有失配都执行：已经完全匹配时，多跳一格不影响 `q`',
                 '两段循环结构相同，只差中间的一次 `p += 1`（相当于删除）',
                 '原文已是 Python 3 可运行，未做改动'],
    ),
)
