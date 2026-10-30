S0 = '1110'


def _r(S):
    if 'index' not in S or S['_line'] <= 14:
        return 0
    return S['index'] + 1 if S['_line'] >= 17 else S['index']


def _rot(S):
    s, r = S['s'], _r(S)
    return s[r:] + s[:r]


def _col(S, i, v):
    if v != '1':
        return None
    return 'cyan' if i % 2 == 0 else 'pink'


def _txt(S):
    if 'even_one' not in S or 'n' not in S:
        return '`even_one` / `odd_one`：偶数位 / 奇数位上 1 的个数'
    e, o, n = S['even_one'], S['odd_one'], S['n']
    return (f"`even_one = {e}`，`odd_one = {o}`：1010… 要 `{(n + 1) // 2} − {e} + {o} = {(n + 1) // 2 - e + o}` 次；"
            f"0101… 要 `{e} + {n // 2} − {o} = {e + n // 2 - o}` 次")


CONFIG = dict(
    num=1888, title='使二进制字符串字符交替的最少反转次数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举移位 · 奇偶位 1 的计数',
    tags=['灵神题单·滑动窗口与双指针', '难度分 2006'],
    code='''
class Solution(object):
    def minFlips(self, s):

        odd_one = 0
        even_one = 0
        n = len(s)
        for index, char in enumerate(s):
            if char == '1':
                if index % 2 == 0:
                    even_one += 1
                else:
                    odd_one += 1

        res = min((n + 1) // 2 - even_one + odd_one, even_one + n // 2 - odd_one)

        for index in range(n - 1):
            odd_one, even_one = even_one, odd_one
            if s[index] == '1' and n & 1:
                odd_one -= 1
                even_one += 1

            res = min(res, (n + 1) // 2 - even_one + odd_one, even_one + n // 2 - odd_one)

        return res
''',
    call=f'Solution().minFlips({S0!r})',
    expect=1,
    views=[
        dict(type='string', var=_rot, label='当前移位后的串（青 = 偶数位上的 1，粉 = 奇数位上的 1）', cell=96, h=190, color=_col),
        dict(type='text', h=130, size=28, fn=_txt),
    ],
    watch=[('even_one', 'even_one', 'cyan'), ('odd_one', 'odd_one', 'pink'), ('res', 'res', 'green')],
    captions={
        'odd_one = 0': '`odd_one`：奇数位上 1 的个数',
        'even_one = 0': '`even_one`：偶数位上 1 的个数',
        'n = len(s)': '`n = {n}`',
        'for index, char in enumerate': lambda S, B, ret: (f'`s[{S.index}] = {S.char!r}`' if 'index' not in B or S.index != B.index else '统计结束'),
        'even_one += 1': lambda S, B, ret: (f'偶数位 `{S.index}` 上有 1：`even_one = {S.even_one}`' if S._line == 10
                                             else f'修正：移走的 1 在末尾仍算偶数位 → `even_one = {S.even_one}`'),
        'odd_one += 1': '奇数位 `{index}` 上有 1：`odd_one = {odd_one}`',
        'res = min((n + 1)': '1010… 要 `{(n + 1) // 2 - even_one + odd_one}` 次，0101… 要 `{even_one + n // 2 - odd_one}` 次，取小：`res = {res}`',
        'for index in range': lambda S, B, ret: (f'循环左移一位：把 `s[{S.index}] = {S.s[S.index]!r}` 移到末尾' if 'index' not in B or S.index != B.index else '所有移位试完'),
        'odd_one, even_one = even_one': '左移一位 = 所有字符奇偶互换（奇数长度稍后修正）：`even_one = {even_one}`，`odd_one = {odd_one}`',
        "if s[index] == '1' and n & 1": lambda S, B, ret: (
            f'`n` 为奇数且移走的 `s[{S.index}]` 是 1：它到末尾后==奇偶性不变==，要修正' if (S.s[S.index] == '1' and S.n & 1)
            else ('`n` 为偶数：左移后每个字符奇偶都变，不需要修正' if not S.n & 1 else '移走的是 0，不影响 1 的分布，不需要修正')),
        'odd_one -= 1': '修正：这个 1 并没有换到奇数位 → `odd_one = {odd_one}`',
        'res = min(res': '`res = min({B.res}, {(n + 1) // 2 - even_one + odd_one}, {even_one + n // 2 - odd_one}) = {res}`',
        'return res': '最少反转 `{res}` 次',
    },
    cards=dict(
        one_liner='移位免费：O(1) 更新奇偶位上 1 的个数，逐个移位取最小',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['类型 1：首字符移到末尾；类型 2：反转一个字符',
                 '求变成交替串所需类型 2 的最少次数',
                 f'本视频：`s = "{S0}"` → `1`'],
        quote='两种操作交替进行是没有意义的，完全可以先循环位移到最终的位置，然后再执行反转。……不妨设odd_one和even_one分别表示奇数位上1的个数以及偶数位上1的个数。',
        quote_src='—— yiduobo 题解原文',
        idea=['先试每种循环移位，再只做反转：目标有 `1010…` 和 `0101…` 两种',
              '长度为偶数：左移一位 = ==奇偶位互换==，交换两个计数即可',
              '长度为奇数：被移走的 1 在末尾后奇偶性不变，要多减多加一次'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`1010…` 要反转：偶数位的 0 + 奇数位的 1；`0101…` 反过来',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '对比灵神：灵神把 `s+s` 当大串滑窗；这里不滑窗，只更新两个计数'],
    ),
)
