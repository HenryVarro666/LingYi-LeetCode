def _txt(S):
    if 'i' not in S:
        return '找最小的 `i`，使 `s[i] == s[n-1-i]`（`s[-1-i]` 就是对称位置）'
    i, s = S['i'], S['s']
    return f"比较 `s[{i}] = '{s[i]}'` 与对称位置 `s[{-1 - i}] = '{s[-1 - i]}'`"


CONFIG = dict(
    num=3884, title='双端字符匹配', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='只枚举左半边 · 对称下标 -1-i',
    tags=[],
    code='''
class Solution:
    def firstMatchingIndex(self, s: str) -> int:
        for i in range(len(s) // 2 + 1):
            if s[i] == s[-1 - i]:
                return i
        return -1
''',
    call="Solution().firstMatchingIndex('abcdxyzcb')",
    expect=4,
    views=[
        dict(type='text', h=90, size=30, fn=_txt),
        dict(type='string', var='s', label='s（蓝 = s[i]，粉 = 对称位置 s[-1-i]）', cell=100, h=300,
             pointers={'i': 'blue', 'len(s) - 1 - i': 'pink'},
             color=lambda S, k, v: ('blue' if k == S['i'] else 'pink' if k == len(S['s']) - 1 - S['i'] else None) if 'i' in S else None),
    ],
    watch=['i', ('对称下标', 'len(s) - 1 - i', 'pink')],
    captions={
        'for i in range': '只需枚举 `0 .. n/2`：左半没有匹配，右半就是同样的配对，不用再看；`n` 为奇数时中间位置自己配自己',
        'if s[i] == s[-1 - i]': lambda S, B, r: (
            f"`s[{S.i}] = '{S.s[S.i]}'`，`s[{-1 - S.i}] = '{S.s[-1 - S.i]}'` → "
            + ('==相等，这就是最小的 i==' if S.s[S.i] == S.s[-1 - S.i] else '不相等，继续看下一个 i')),
        'return i': '下标 `{i}` 是第一个满足条件的，直接返回 =={i}==',
        'return -1': '左半边都没找到匹配，返回 `-1`',
    },
    cards=dict(
        one_liner='只看左半边：左半没匹配，右半也不会有',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['在长为 `n` 的字符串 `s` 里找最小下标 `i`，使 `s[i] == s[n-i-1]`',
                 '找不到返回 `-1`',
                 '本视频：`s = "abcdxyzcb"` → `4`（正中心自己配自己）'],
        quote='如果在 s 的左半边没有找到匹配的字母，那么右半边也和左半边不匹配，无需遍历。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`i` 与 `n-1-i` 成对出现，`i` 过了一半，配对就和左半边重复了',
              '所以遍历下标 `0` 到 `n/2`，Python 里 `s[-1-i]` 正好是对称位置',
              '`n` 为奇数时，`n//2` 是正中心，自己和自己一定相等，所以范围写成 `len(s)//2 + 1`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '范围是 `len(s) // 2 + 1`，别漏掉奇数长度的正中心',
                 '`s[-1 - i]` 即 `s[n - 1 - i]`',
                 '例 `"abc"`：`i = 1` 是中心，答案 `1`'],
    ),
)
