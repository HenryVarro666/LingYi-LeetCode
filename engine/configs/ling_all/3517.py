def _top(S):
    if 'n' not in S:
        return ''
    n = S['n']
    mid = f'，正中间 `s[{n // 2}] = {S["s"][n // 2]}` 固定不动' if n % 2 else '，长度为偶数没有中心'
    if 't' not in S:
        return f'`n = {n}`：只关心左半部分 `s[:{n // 2}]`{mid}'
    return f'左半部分排序得 `t = {"".join(S["t"])}`{mid}'


def _res(S):
    if 'ans' not in S:
        return ''
    return f'当前拼出：`ans = {S["ans"]}`'


CONFIG = dict(
    num=3517, title='最小回文排列 I', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='只排序左半部分',
    tags=['灵神题单', '难度分 1357'],
    code='''
class Solution:
    def smallestPalindrome(self, s: str) -> str:
        n = len(s)
        t = sorted(s[:n // 2])

        ans = ''.join(t)
        if n % 2:
            ans += s[n // 2]
        return ans + ''.join(reversed(t))
''',
    call='''Solution().smallestPalindrome("dcbabcd")
Solution().smallestPalindrome("daccad")''',
    expect='acddca',
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='s', label='s（蓝 = 左半部分，粉 = 回文中心）', cell=84,
             color=lambda S, i, v: ('blue' if i < S['n'] // 2 else 'pink' if (S['n'] % 2 and i == S['n'] // 2) else None) if 'n' in S else None,
             dim=lambda S, i, v: 'n' in S and i >= S['n'] // 2 + S['n'] % 2),
        dict(type='array', var='t', label='t = 排序后的左半部分', cell=84,
             color=lambda S, i, v: 'green'),
        dict(type='text', fn=_res, size=30),
    ],
    watch=['n', ('ans', 'ans', 'green')],
    captions={
        'n = len(s)': '`n = len(s) = {n}`',
        't = sorted': '回文的右半部分由左半部分决定 → 只排序左半 `{s[:n // 2]}`，得到 `{"".join(t)}`（==字典序最小==）',
        "ans = ''.join(t)": '`ans` 先放排好序的左半部分：`{ans}`',
        'if n % 2': lambda S, B, r: (f'`n = {S.n}` 是奇数：中间那个字母出现奇数次，重排后还得在正中间' if S.n % 2
                                     else f'`n = {S.n}` 是偶数，没有回文中心，直接拼右半'),
        'ans += s[n // 2]': '加上回文中心 `{s[n // 2]}` → `{ans}`',
        'return': '右半部分 = 反转左半部分 `{"".join(reversed(t))}` → 最终答案 `{ret}`',
    },
    cards=dict(
        one_liner='回文只看左半：把左半排序，右半反转，奇数再补中心',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给一个==回文串== `s`，把字符重新排列，返回字典序最小的回文串',
                 '示例：`"babab"` → `"abbba"`',
                 '本视频依次跑：`"dcbabcd"` → `"bcdadcb"`；`"daccad"` → `"acddca"`'],
        quote='由于 s 是回文串，我们只需关心左半部分如何排列。要求字典序最小，那么把左半部分排序即可。右半部分通过反转左半部分得到。',
        quote_src='—— 灵茶山艾府题解',
        idea=['奇数长度时，正中间字母出现奇数次，重排后仍必须在正中间',
              '所以无论奇偶，只需排列左半部分（奇数去掉中心）',
              '左半越小越靠前，字典序就越小；右半是左半的镜像'],
        after=[dict(heading='写法二：计数排序', lines=[
            '左半只有 26 种小写字母，不必比较排序',
            '`cnt = Counter(s[:n // 2])`，按 a 到 z 依次拼 `ch * cnt[ch]`',
            '时间降到 `O(n + |Σ|)`，其中 `|Σ| = 26`'])],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：奇数长度别漏掉中心字母 `s[n // 2]`',
                 '写法二：只有 26 个小写字母，用 `Counter` 计数排序，时间 `O(n + |Σ|)`',
                 '同类题：3518 最小回文排列 II，同样先看左半'],
    ),
)
