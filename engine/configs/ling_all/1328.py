def _top(S):
    if 'n' not in S:
        return ''
    if S['n'] == 1:
        return '长度为 1：改哪个字母都还是回文'
    if 'i' not in S:
        return f"回文串只需看前一半：下标 `0 ~ {S['n'] // 2 - 1}`"
    s, i = S['s'], S['i']
    if s[i] == 'a':
        return f"`s[{i}] = 'a'` 已经最小，改它没有收益"
    return f"`s[{i}] = '{s[i]}'` 不是 a → 改成 ==a== 最划算"


CONFIG = dict(
    num=1328, title='破坏回文串', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='字符串贪心 · 前一半找非 a',
    tags=['灵神题单', '贪心算法', '难度分 1474'],
    code='''
class Solution:
    def breakPalindrome(self, s: str) -> str:
        n = len(s)
        if n == 1:
            return ""
        # 把第一个不等于 a 的字母改成 a
        # 只需找前一半，如果前一半没有不等于 a 的字母，那么后一半肯定也没有
        for i in range(n // 2):
            if s[i] != 'a':
                return s[:i] + 'a' + s[i + 1:]
        # 除了回文中心，全是 a
        return s[:-1] + 'b'  # 最后一个字母改成 b
''',
    call='Solution().breakPalindrome("aabcbaa")',
    expect='aaacbaa',
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='string', var='s', label='s（回文串，只看前一半）', cell=84,
             pointers={'i': 'blue'},
             window=('0', 'n // 2 - 1'),
             color=lambda S, k, v: ('blue' if S.get('i') == k else None),
             dim=lambda S, k, v: 'n' in S and k >= S['n'] // 2),
        dict(type='text', fn=lambda S: '示例 `"aabcbaa"`：前一半 `aab` 里第一个非 a 在下标 2，改成 a → `"aaacbaa"`', size=24),
    ],
    watch=[('n', 'n'), ('i', 'i', 'blue')],
    captions={
        'n = len': '`n = {n}`',
        'if n == 1': '`n = {n}`：长度不为 1，还有位置可以改',
        'for i in range': '只枚举前一半：`i` 取 `{i}`（后一半与前一半对称，不用看）',
        'if s[i] != ': lambda S, B, r: (f"`s[{S.i}] = '{S.s[S.i]}'` ≠ 'a' → 改成 a 能让字典序变小" if S.s[S.i] != 'a'
                                        else f"`s[{S.i}] = 'a'` 已经是最小字母，继续看下一个"),
        "return s[:i]": '前面的字母越靠前越重要，所以==改第一个非 a 的字母==：返回 `{ret}`',
        "return s[:-1]": '前一半全是 a（中心之外全是 a）→ 只能把最后一个字母改成 b：`{ret}`',
    },
    cards=dict(
        one_liner='把第一个不是 a 的字母改成 a；全是 a 就把最后一个改成 b',
        complexity='时间 `O(n)`，空间 `O(n)` 或 `O(1)`',
        problem=['回文串 `palindrome`，改动==恰好一个==字符，使结果不是回文串，且字典序最小',
                 '做不到就返回空串',
                 '示例：`"abccba"` → `"aaccba"`；`"a"` → `""`'],
        quote='要使字典序最小，改前面比改后面更好。',
        quote_src='—— 灵茶山艾府题解',
        idea=['改任何不在正中心的字母，都会破坏对称性',
              '前面的字母没有变小，后面怎么改都不是最优 → 从左到右找==第一个不是 a 的字母==改成 a',
              '只需找前一半：前一半没有非 a，后一半也不会有'],
        summary=['时间 `O(n)`，空间 `O(n)`（可原地改则 `O(1)`）',
                 '易错：长度为 1 要返回空串',
                 '易错：奇数长度时不能改中心字母，所以循环到 `n // 2`',
                 '全是 a 时只能把最后一个改成 b，改前面会让字典序更大'],
    ),
)
