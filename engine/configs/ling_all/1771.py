W1, W2 = 'ab', 'cba'


def _live(S):
    return all(x in S for x in ('i', 'j', 'f')) and S.get('_line', 0) >= 7


def _cell(S, r, c, v):
    if not _live(S):
        return None
    i, j = S['i'], S['j']
    if (r, c) == (i, j):
        return 'yellow'
    if j > i:
        if S['s'][i] == S['s'][j]:
            return 'green' if (r, c) == (i + 1, j - 1) else None
        return 'blue' if (r, c) in ((i + 1, j), (i, j - 1)) else None
    return None


def _formula(S):
    if not _live(S) or S['j'] <= S['i']:
        return '`f[i][j]` = `s[i..j]` 的最长回文子序列；==只在 `s[i]=s[j]` 且横跨两个单词时更新答案=='
    i, j, s = S['i'], S['j'], S['s']
    if s[i] == s[j]:
        return f'`s[{i}] = s[{j}] = {s[i]}`：`f[{i}][{j}] = f[{i + 1}][{j - 1}] + 2`'
    return f'`s[{i}] = {s[i]} ≠ s[{j}] = {s[j]}`：`f[{i}][{j}] = max(f[{i + 1}][{j}], f[{i}][{j - 1}])`'


def _cross(S, B, ret):
    i, j, m = S.i, S.j, len(W1)
    if i < m <= j:
        return f'`{i} < {m} ≤ {j}`：`s[i]` 在 word1、`s[j]` 在 word2，两端==横跨两个单词== → 可以拿 `f[{i}][{j}] = {S.f[i][j]}` 更新答案'
    return f'`i = {i}`，`j = {j}`：两端在同一个单词里（不满足 `i < {m} ≤ j`），不能更新答案'


CONFIG = dict(
    num=1771, title='由子序列构造的最长回文串的长度', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='区间 DP · 两端相等时更新答案',
    tags=['灵神题单', '动态规划', '难度分 2182'],
    code='''
class Solution:
    def longestPalindrome(self, word1: str, word2: str) -> int:
        s = word1 + word2
        ans, n = 0, len(s)
        f = [[0] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            f[i][i] = 1
            for j in range(i + 1, n):
                if s[i] == s[j]:
                    # 这里的 2 是 s[i] 和 s[j]，所以 f[i][j] 一定包含 s[i] 和 s[j]
                    f[i][j] = f[i + 1][j - 1] + 2
                    if i < len(word1) <= j:
                        ans = max(ans, f[i][j])
                else:
                    f[i][j] = max(f[i + 1][j], f[i][j - 1])
        return ans
''',
    call=f'Solution().longestPalindrome({W1!r}, {W2!r})',
    expect=5,
    skip=['for j in range', 'ans, n = 0'],
    max_steps=80,
    views=[
        dict(type='string', var='s', label='s = word1 + word2（蓝 = i，粉 = j）', h=200, cell=80, pointers={'i': 'blue', 'j': 'pink'},
             color=lambda S, k, v: 'cyan' if k < len(W1) else None),
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算，蓝/绿 = 依赖）', h=380, cell=64,
             rows=lambda S: [f'{k}{c}' for k, c in enumerate(W1 + W2)], cols=lambda S: [f'{k}{c}' for k, c in enumerate(W1 + W2)],
             color=_cell),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ans', 'ans', 'green')],
    captions={
        's = word1': '拼成 `s = word1 + word2`，下标 `< {len(word1)}` 的属于 `word1`',
        'f = [[0]': '`f[i][j]`：`s[i..j]` 的最长回文子序列长度（同 516 题）',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：`i` 从大到小，保证 `f[i+1][·]` 已算好' if S.get('i') != B.get('i') else '所有区间都算完了'),
        'f[i][i] = 1': '`f[{i}][{i}] = 1`：单个字母',
        'if s[i] == s[j]': lambda S, B, r: (f'`s[{S.i}] = s[{S.j}] = {S.s[S.i]}`：两端相同，可以配对' if S.s[S.i] == S.s[S.j] else f'`s[{S.i}] = {S.s[S.i]} ≠ s[{S.j}] = {S.s[S.j]}`：两端不同'),
        'f[i][j] = f[i + 1][j - 1] + 2': '两端都选，`f[{i}][{j}] = {f[i+1][j-1]} + 2` = =={f[i][j]}==：这个回文串==一定包含 s[i] 和 s[j]==',
        'if i < len(word1)': _cross,
        'f[i][j] = max(': '不选其中一端：`f[{i}][{j}] = max({f[i+1][j]}, {f[i][j-1]})` = =={f[i][j]}==，这一格不更新答案',
        'ans = max(ans': '`ans = max({B.ans}, {f[i][j]})` = =={ans}==',
        'return ans': '答案 =={ret}==',
    },
    cards=dict(
        one_liner='先求整串最长回文子序列，只在两端相等且横跨两词时更新答案',
        complexity='时间 `O((n+m)^2)`，空间 `O((n+m)^2)`',
        problem=['从 `word1` 选一个==非空==子序列，从 `word2` 选一个==非空==子序列，拼接成回文串',
                 '求能构造出的最长回文串长度，构造不出返回 `0`',
                 '示例：`"cacb"`、`"cbba"` → `5`；本视频：`"ab"`、`"cba"` → `5`（`abcba`）'],
        quote='当 s[i]=s[j] 时，算出的 f[i][j] 一定包含 s[i] 和 s[j]，所以应当在此处更新答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['直接对 `word1 + word2` 求 516 的答案会错：回文串可能全在一个单词里，子序列不能为空',
              '`f[i][j]` 只有在 `s[i] == s[j]` 时才一定包含两端',
              '再要求 `i < len(word1) <= j`，两端就一个在 word1、一个在 word2，两边都非空'],
        summary=['时间、空间都是 `O((n+m)^2)`',
                 '易错：不能遍历所有 `f[i][j]` 取最大，那样可能没用到其中一个单词',
                 '易错：更新答案要放在 `s[i] == s[j]` 分支里，条件 `i < len(word1) <= j`',
                 '前置题：516 最长回文子序列（区间 DP）'],
    ),
)
