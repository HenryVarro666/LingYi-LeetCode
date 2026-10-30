W1, W2 = 'ab', 'ba'
SS = W1 + W2


def _live(S):
    return all(x in S for x in ('l', 'r', 'length', 'f')) and S.get('_line', 0) <= 17


def _cell(S, a, b, v):
    if S.get('_line', 0) >= 19:
        fp, lp = S.get('first_pos', {}), S.get('last_pos', {})
        ch = S.get('char')
        if ch in fp and ch in lp and fp[ch] + 1 <= lp[ch] - 1 and S.get('_line', 0) >= 28:
            return 'green' if (a, b) == (fp[ch] + 1, lp[ch] - 1) else None
        return None
    if not _live(S):
        return None
    l, r = S['l'], S['r']
    if (a, b) == (l, r):
        return 'yellow'
    if r > l and S['s'][l] == S['s'][r]:
        return 'green' if (a, b) == (l + 1, r - 1) else None
    if r > l:
        return 'blue' if (a, b) in ((l + 1, r), (l, r - 1)) else None
    return None


def _formula(S):
    if S.get('_line', 0) >= 19 and 'first_pos' in S:
        return '再看跨过中心（下标 `< m` 与 `≥ m`）的字母：`f[first+1][last-1] + 2`'
    if not _live(S) or S['r'] <= S['l']:
        return '`f[l][r]`：区间 `l..r` 的最长回文子序列；==按区间长度从小到大==算'
    l, r, s = S['l'], S['r'], S['s']
    if s[l] == s[r]:
        return f'`s[{l}] = s[{r}] = {s[l]}`：`f[{l}][{r}] = f[{l + 1}][{r - 1}] + 2`'
    return f'`s[{l}] = {s[l]} ≠ s[{r}] = {s[r]}`：`f[{l}][{r}] = max(f[{l + 1}][{r}], f[{l}][{r - 1}])`'


CONFIG = dict(
    num=1771, title='由子序列构造的最长回文串的长度', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='区间 DP + 枚举跨中心的最外层字母',
    tags=['灵神题单', '动态规划', '难度分 2182'],
    code='''
class Solution(object):
    def longestPalindrome(self, word1, word2):

        m = len(word1)
        s = word1 + word2
        n = len(s)
        f = [[0] * n for _ in range(n)]
        for length in range(1, n + 1):
            for l in range(n - length + 1):
                r = l + length - 1
                if length == 1:
                    f[l][r] = 1
                elif s[l] == s[r]:
                    f[l][r] = f[l + 1][r - 1] + 2
                else:
                    f[l][r] = max(f[l + 1][r], f[l][r - 1])

        first_pos = {}
        last_pos = {}
        for index, char in enumerate(s):
            if char not in first_pos:
                first_pos[char] = index
            last_pos[char] = index
        
        res = 0
        for index in range(26):
            char = chr(index + 97)
            if char in first_pos:
                if first_pos[char] < m and last_pos[char] >= m:
                    res = max(res, f[first_pos[char] + 1][last_pos[char] - 1] + 2)
        
        return res
''',
    call=f'Solution().longestPalindrome({W1!r}, {W2!r})',
    expect=4,
    skip=['if length == 1', 'for l in range', 'r = l + length - 1', 'for index, char in enumerate', 'for index in range(26)', 'char = chr(', 'if char in first_pos', 'if char not in first_pos', 'last_pos = {}', 'first_pos = {}', 'else:', 'elif s[l]'],
    max_steps=80,
    views=[
        dict(type='string', var='s', label='s = word1 + word2（蓝 = l，粉 = r）', h=190, cell=80, pointers={'l': 'blue', 'r': 'pink'},
             color=lambda S, k, v: 'cyan' if k < len(W1) else None),
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='table', var='f', label='f[l][r]（黄 = 正在算，蓝/绿 = 依赖）', h=250, cell=56,
             rows=lambda S: [f'{k}{c}' for k, c in enumerate(SS)], cols=lambda S: [f'{k}{c}' for k, c in enumerate(SS)],
             color=_cell),
        dict(type='map', var='first_pos', label='first_pos（每个字母第一次出现的位置）', h=130),
        dict(type='map', var='last_pos', label='last_pos（最后一次出现的位置）', h=130),
    ],
    watch=[('length', 'length', 'green'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('res', 'res', 'green')],
    captions={
        'm = len(word1)': '`m = {m}`：下标 `< m` 的字符来自 `word1`',
        's = word1': '拼起来 `s = word1 + word2`，先当成一个字符串求最长回文子序列',
        'f = [[0]': '`f[l][r]`：区间 `l..r` 的最长回文子序列长度',
        'for length in range': lambda S, B, r: (f'区间长度 `length = {S.length}`：短的先算' if S.get('length') != B.get('length') else '所有区间都算完了'),
        'f[l][r] = 1': '只有一个字符，必然回文：`f[{l}][{r}] = 1`',
        'f[l][r] = f[l + 1][r - 1] + 2': '`s[{l}] = s[{r}]` 两端配对：`f[{l}][{r}] = {f[l+1][r-1]} + 2` = =={f[l][r]}==',
        'f[l][r] = max(': '两端不同，牺牲一个：`max({f[l+1][r]}, {f[l][r-1]})` = =={f[l][r]}==',
        'first_pos[char] = index': '`{char}` 第一次出现在 `{index}`',
        'last_pos[char] = index': '`{char}` 最后一次出现在 `{index}`（出现一次就覆盖一次）',
        'res = 0': 'DP 表算完。接下来保证回文串==跨过中心==：最外层字母要一个在 word1、一个在 word2',
        'if first_pos[char] < m': lambda S, B, r: (f'`{S.char}`：first = {S.first_pos[S.char]} < m = {S.m}，last = {S.last_pos[S.char]} ≥ {S.m}：==横跨两个单词==' if S.first_pos[S.char] < S.m and S.last_pos[S.char] >= S.m else f'`{S.char}`：不横跨两个单词，跳过'),
        'res = max(res': '最外层用 `{char}`：`f[first+1][last-1] + 2` = `{f[first_pos[char]+1][last_pos[char]-1]} + 2`，`res` = =={res}==',
        'return res': '答案 =={ret}==',
    },
    cards=dict(
        one_liner='把两词拼起来求回文子序列，再强制最外层字母横跨中心',
        complexity='时间 `O((n+m)^2)`，空间 `O((n+m)^2)`',
        problem=['从 `word1`、`word2` 各选一个==非空==子序列，拼接后形成回文串',
                 '求最长回文串长度，做不到返回 `0`',
                 '示例：`"ab"`、`"ab"` → `3`；本视频：`"ab"`、`"ba"` → `4`（`abba`）'],
        quote='题目实际上就相当于要求从subsequence1和subsequence2组合后的字符串后找出最长回文子序列，同时要求这个回文子序列是跨越中心连接点的。',
        quote_src='—— yiduobo 题解原文',
        idea=['拼成 `s`，经典区间 DP 求 `f[i][j]`：相等 `+2`，不等牺牲一端',
              '回文串最外层的一对字母必须一个在 word1、一个在 word2',
              '小写字母只有 26 种：记下每个字母第一次和最后一次出现的位置',
              '对横跨中心的字母，答案 `f[first+1][last-1] + 2`，取最大'],
        summary=['时间 `O((n+m)^2)`，空间 `O((n+m)^2)`',
                 '外层字母取 ==首次出现 / 最后一次出现==，里面的区间最大，所以不会漏',
                 '易错：用 `first_pos < m <= last_pos` 保证两边非空',
                 '原文已是 Python 3 可运行的写法，代码未做改动',
                 '对比灵神：灵神在 DP 过程中遇到 `s[i]==s[j]` 且横跨时直接更新答案'],
    ),
)
