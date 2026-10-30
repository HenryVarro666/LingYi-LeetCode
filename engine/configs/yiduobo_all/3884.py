def _txt(S):
    if 'index' not in S:
        return '从 `index = 0` 往后找，直到对称的两个字符相同，或两个指针错开'
    i, n, s = S['index'], len(S['s']), S['s']
    if i > n - i - 1:
        return f'`index = {i}` 已越过对称位置 `{n - i - 1}`：没有匹配'
    return f"`s[{i}] = '{s[i]}'` 对 `s[{n - i - 1}] = '{s[n - i - 1]}'`"


CONFIG = dict(
    num=3884, title='双端字符匹配', difficulty='Easy', category='字符串',
    author='yiduobo', technique='while 循环 · index 与对称位置相遇为止',
    tags=[],
    code='''
class Solution(object):
    def firstMatchingIndex(self, s):
        
        index = 0
        n = len(s)
        while index <= n - index - 1 and s[index] != s[n - index - 1]:
            index += 1
        
        if index <= n - index - 1:
            return index
        return -1
''',
    call="Solution().firstMatchingIndex('abcdab')",
    expect=-1,
    views=[
        dict(type='text', h=90, size=30, fn=_txt),
        dict(type='string', var='s', label='s（蓝 = index，粉 = n−index−1）', cell=100, h=300,
             pointers={'index': 'blue', 'n - index - 1': 'pink'},
             window=('index', 'n - index - 1'),
             color=lambda S, k, v: ('blue' if k == S['index'] else 'pink' if k == len(S['s']) - 1 - S['index'] else None) if 'n' in S else None),
    ],
    watch=['index', 'n', ('对称下标', 'n - index - 1', 'pink')],
    captions={
        'index = 0': '`index` 从 0 开始，一路往上找',
        'n = len(s)': '`n = {n}`，`index` 的对称位置是 `n - index - 1`',
        'while index <= n': lambda S, B, r: (
            f"`{S.index} <= {S.n - S.index - 1}` 且 `s[{S.index}] = '{S.s[S.index]}'` "
            f"{'≠' if S.s[S.index] != S.s[S.n - S.index - 1] else '='} `s[{S.n - S.index - 1}] = '{S.s[S.n - S.index - 1]}'` → "
            + ('==不匹配，继续往后==' if S.s[S.index] != S.s[S.n - S.index - 1] else '==相等，停下==')
        ) if S.index <= S.n - S.index - 1 else f'`index = {S.index} > {S.n - S.index - 1}`：两个位置已经错开 → ==退出循环==',
        'index += 1': '这一对不同，`index` → {index}',
        'if index <= n': lambda S, B, r: ('`index` 还没越过对称位置 → 说明是==匹配上停下的==' if S.index <= S.n - S.index - 1
                                          else '`index` 越过了对称位置 → 一对都没匹配上'),
        'return index': '返回 `{index}`',
        'return -1': '遍历到相遇都没有相同的一对 → 返回 `-1`',
    },
    cards=dict(
        one_liner='index 从 0 往上走，直到匹配或与对称位置错开',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给小写字符串 `s`，求最小的 `index` 使 `s[index] == s[n-index-1]`',
                 '不存在返回 `-1`',
                 '本视频演示无解的例子：`s = "abcdab"` → `-1`'],
        quote='若直到index > n - index - 1都没有出现这样的index，那么答案就是-1。',
        quote_src='—— yiduobo 题解原文',
        idea=['按题目要求直接从 0 开始向上遍历 `index`',
              '循环条件写成 `index <= n - index - 1 且 两字符不同`：一旦匹配就停',
              '循环结束后再看 `index` 有没有越界：没越界 → 答案；越界 → `-1`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`index <= n - index - 1` 同时包含奇数长度的正中心（自己配自己）',
                 '原文用 while 加双重出口，灵神则用 for 枚举到 `n//2` 再直接返回',
                 '易错点：循环后要重新判断 `index` 是否越界，才知道是匹配停下还是走完'],
    ),
)
