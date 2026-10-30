def _isl(c):
    return ('a' <= c <= 'z') or ('A' <= c <= 'Z')


CONFIG = dict(
    num=917, title='仅仅反转字母', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='相向双指针 · 跳过非字母再交换',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution(object):
    def reverseOnlyLetters(self, S):

        l = 0
        r = len(S) - 1

        s_list = list(S)

        while l < r:
            while l < r and not((S[l] >= 'a' and S[l] <= 'z') or (S[l] >= 'A' and S[l] <= 'Z')):
                l += 1
            if l == r:
                break

            while r > l and not((S[r] >= 'a' and S[r] <= 'z') or (S[r] >= 'A' and S[r] <= 'Z')):
                r -= 1
            if l == r:
                break

            s_list[l], s_list[r] = s_list[r], s_list[l]
            l += 1
            r -= 1

        return ''.join(s_list)
''',
    call='Solution().reverseOnlyLetters("a-bC-dEf")',
    expect='f-Ed-Cba',
    views=[
        dict(type='string', var='S', label='S（原串，指针在上面扫描）', cell=84, pointers={'l': 'blue', 'r': 'pink'},
             dim=lambda S, i, v: not _isl(v), h=240),
        dict(type='string', var='s_list', label='s_list（交换发生在这里；暗格 = 非字母）', cell=84,
             dim=lambda S, i, v: not _isl(v),
             color=lambda S, i, v: 'green' if ('l' in S and 'r' in S and (i < S['l'] or i > S['r']) and _isl(v)) else None, h=240),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink')],
    captions={
        'l = 0': '`l` 从头往后扫',
        'r = len': '`r = len(S) - 1 = {r}`，从尾往头扫',
        's_list = list': '`S` 不能改，复制一份列表 `s_list` 用来交换',
        'while l < r:': lambda S, B, r: (f'`l = {S.l} < r = {S.r}` → 还有没配对的字母，继续' if S.l < S.r else f'`l = {S.l} >= r = {S.r}` → 指针相遇，交换完毕'),
        'while l < r and not': lambda S, B, r: (f"`S[{S.l}] = '{S.S[S.l]}'` 不是字母 → ==跳过==" if S.l < S.r and not _isl(S.S[S.l]) else f"`S[{S.l}] = '{S.S[S.l]}'` 是字母（或已碰头），`l` 停下"),
        'if l == r': '`l = {l}`，`r = {r}`：{"==相遇了，没有字母可配对，退出==" if l == r else "还没相遇，继续"}',
        'while r > l and not': lambda S, B, r: (f"`S[{S.r}] = '{S.S[S.r]}'` 不是字母 → ==跳过==" if S.r > S.l and not _isl(S.S[S.r]) else f"`S[{S.r}] = '{S.S[S.r]}'` 是字母（或已碰头），`r` 停下"),
        's_list[l], s_list[r]': lambda S, B, r: f"`l` 和 `r` 都停在字母上 → ==交换== `{B.s_list[S.l]}` 与 `{B.s_list[S.r]}` → `{''.join(S.s_list)}`",
        'return': '返回 `{ret}`',
    },
    skip=[],
    cards=dict(
        one_liner='两个指针各自跳过非字母，停下后交换',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['反转字符串中的==所有字母==（大小写都算）',
                 '非字母字符留在原来的位置不动',
                 '示例：`"a-bC-dEf"` → `"f-Ed-Cba"`'],
        quote='使用两个指针l和r，l从头往后扫描，直到碰到一个字母；r从尾往头扫描，同样是碰到字母停止。若此时的l依然小于r，那么就交换l和r上的字母。',
        quote_src='—— yiduobo 题解原文',
        idea=['`l` 往右找字母，`r` 往左找字母，非字母统统跳过',
              '两个都停在字母上就交换，然后各走一步',
              '`l >= r` 时所有字母都配好对了，结束'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：内层循环也要带 `l < r`（或 `r > l`）条件，避免越过对方',
                 '易错：内层跳完后要判断 `l == r`，相遇说明没有字母可交换',
                 '判断字母用 `a-z` 与 `A-Z` 两个区间，因为大小写都要反转',
                 '原文已是 Python 3 可运行的写法，未做修改；与第 344 题同属相向双指针'],
    ),
)
