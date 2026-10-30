def _mid_txt(S):
    if 'base' not in S or 'm' not in S:
        return '反回文：对称位置 `i` 和 `n-1-i` 的字母不能相同'
    b, n = S['base'], len(S['base'])
    bad = [i for i in range(n // 2) if b[i] == b[n - 1 - i]]
    if bad:
        return '对称位置字母相同的下标：' + '、'.join(f'`{i}↔{n - 1 - i}`' for i in bad) + '  ==还要调换=='
    return '每一对对称位置的字母都不同 ==反回文成立=='


def _color(S, i, v):
    if 'base' not in S:
        return None
    n = len(S['base'])
    return 'orange' if S['base'][i] == S['base'][n - 1 - i] else None


CONFIG = dict(
    num=3088, title='使字符串反回文', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='排序 · 调换中间重复字母',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def makeAntiPalindrome(self, s):

        m = len(s) // 2

        max_freq = max(Counter(s).values())
        if max_freq > m:
            return "-1"
        
        base = sorted(s)
        left = m - 1
        right = m
        while base[left] == base[m]:
            left -= 1
        while base[right] == base[m - 1]:
            right += 1
        
        left_length = m - 1 - left
        right_length = right - m

        tmp = base[m]
        for index in range(left_length):
            base[m + index] = base[right + index]
        for index in range(right_length):
            base[m + left_length + index] = tmp
            
        return ''.join(base)
''',
    call='Solution().makeAntiPalindrome("babcab")',
    expect='aabcbb',
    views=[
        dict(type='text', fn=_mid_txt, size=28, h=90),
        dict(type='array', var='base', label='base（排序后的字符；橙 = 与对称位置相同）', cell=100, h=300,
             pointers={'left': 'blue', 'right': 'pink', 'm': 'green'}, color=_color),
        dict(type='text', fn=lambda S: (f"`left_length = {S['left_length']}`，`right_length = {S['right_length']}`，中间字母 `tmp = '{S['tmp']}'`"
                                        if 'right_length' in S else ''), size=26, h=80),
    ],
    watch=[('m', 'm', 'green'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), 'left_length', 'right_length', ('index', 'index')],
    captions={
        'm = len(s)': '`m = n // 2 = {m}`：对称的两半以 `m` 为界',
        'max_freq = max': '最多的字母出现 `{max_freq}` 次',
        'if max_freq > m': lambda S, B, r: (f'`{S.max_freq} > {S.m}`：鸽笼原理，必有一对对称位置同字母 → 无解' if S.max_freq > S.m
                                            else f'`{S.max_freq} <= {S.m}`：不超过一半 → ==一定有解=='),
        'base = sorted': '先排序：这是字典序最小的排列 `{"".join(base)}`，但正中间 `m-1`、`m` 可能同字母',
        'left = m - 1': '`left` 从 `m - 1` 出发，向左找第一个不等于 `base[m]` 的位置',
        'right = m': '`right` 从 `m` 出发，向右找第一个不等于 `base[m-1]` 的位置',
        'while base[left] == base[m]': lambda S, B, r: (f"`base[{S.left}] = '{S.base[S.left]}'` == `base[{S.m}] = '{S.base[S.m]}'`：还是同一种字母，`left` 继续左移"
                                                        if S.base[S.left] == S.base[S.m] else f"`base[{S.left}] = '{S.base[S.left]}'` 不同了，`left` 停在 {S.left}"),
        'while base[right] == base[m - 1]': lambda S, B, r: (f"`base[{S.right}] = '{S.base[S.right]}'` == `base[{S.m - 1}]`：还是同一种字母，`right` 继续右移"
                                                             if S.base[S.right] == S.base[S.m - 1] else f"`base[{S.right}] = '{S.base[S.right]}'` 不同了，`right` 停在 {S.right}"),
        'left -= 1': '`left` → {left}',
        'right += 1': '`right` → {right}',
        'left_length =': '中间字母在前半有 `left_length = {m} - 1 - {left} = {left_length}` 个',
        'right_length =': '中间字母在后半有 `right_length = {right} - {m} = {right_length}` 个',
        'tmp = base[m]': '先记下要挪走的字母 `tmp = {tmp!r}`',
        'for index in range(left_length)': '把后面的其他字母换到 `[m, m+left_length)`：前半的字母不动，字典序才最小',
        'base[m + index] = base[right + index]': '`base[{m + index}] = base[{right + index}]` = `{base[m + index]!r}`：换成别的字母',
        'for index in range(right_length)': '被挪走的 `tmp` 要放回后面，填到 `m + left_length` 开始的位置',
        'base[m + left_length + index] = tmp': '`base[{m + left_length + index}] = {tmp!r}`：重复字母被推到更靠后的位置',
        'return': '每一对对称位置都不同，返回 `{"".join(base)}`',
    },
    cards=dict(
        one_liner='先排序，再把正中间重复的字母换成后面的字母',
        complexity='时间 `O(n log n)`（排序），空间 `O(n)`',
        problem=['==反回文==：对称位置 `s[i]` 和 `s[n-1-i]` 的字母都不能相同',
                 '把 `s` 重新排列成字典序最小的反回文串，不存在返回 `"-1"`',
                 '本视频：`s = "babcab"` → `"aabcbb"`'],
        quote='若字符串中某种字符的数量超过了字符串长度的一半，那么必然存在一组对称位置上的字符都是该字符，也就是说这种情况下是无法构造的。',
        quote_src='—— yiduobo 题解原文',
        idea=['某字母超过一半 → 鸽笼原理 → 无解；否则一定有解',
              '排序后最小，唯一可能冲突的是正中间：相等字母只会是同一种',
              '保留前半，调换后半：把 `right` 起的字母换到 `m` 处，重复字母放到更后面'],
        result='`aabcbb`：`a-b、a-b、b-c` 三对都不同 ✓',
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '无解时返回的是字符串 `"-1"`，不是 `-1`',
                 '易错：只能换后半部分的字母，保留前半才能保证字典序最小',
                 '`left_length` 与 `right_length` 大小不同，但两种情况统一为同一个调换方案',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
