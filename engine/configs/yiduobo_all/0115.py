S0 = 'babga'
T0 = 'ba'


def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line') not in (12, 16, 17, 18):
        return None
    if r == i and c == j:
        return 'yellow'
    if i > 0 and j > 0 and S.get('_line') in (16, 17, 18):
        if (r, c) == (i - 1, j):
            return 'blue'
        if (r, c) == (i - 1, j - 1) and S['s'][i - 1] == S['t'][j - 1]:
            return 'green'
    return None


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return '`f[i][j]` = `s[:i]` 的子序列中 `t[:j]` 出现的次数'
    if j == 0:
        return f'`f[{i}][0] = 1`：`t[:0]` 是空串，必定是子序列'
    if i == 0:
        return f'`f[0][{j}] = 0`：`s[:0]` 是空串，凑不出非空的 `t[:{j}]`'
    s, t = S['s'], S['t']
    if s[i - 1] == t[j - 1]:
        return f'`s[{i-1}] = t[{j-1}] = {s[i-1]}`：`f[{i}][{j}] = f[{i-1}][{j}] + f[{i-1}][{j-1}]`'
    return f'`s[{i-1}] = {s[i-1]} ≠ t[{j-1}] = {t[j-1]}`：`f[{i}][{j}] = f[{i-1}][{j}]`'


CONFIG = dict(
    num=115, title='不同的子序列', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='二维 DP（s 前 i 位 × t 前 j 位）',
    tags=['灵神题单', 'LCS 进阶'],
    code='''
class Solution(object):
    def numDistinct(self, s, t):

        m = len(s)
        n = len(t)

        f = [[0] * (n + 1) for index in range(m + 1)]

        for i in range(m + 1):
            for j in range(n + 1):
                if j == 0:
                    f[i][j] = 1
                elif i == 0:
                    continue
                else:
                    f[i][j] = f[i - 1][j]
                    if s[i - 1] == t[j - 1]:
                        f[i][j] += f[i - 1][j - 1]
        
        return f[m][n]
''',
    call=f'Solution().numDistinct({S0!r}, {T0!r})',
    expect=3,
    skip=['for j in range', 'continue', 'm = len', 'n = len', 'elif i == 0', 'else:', 'if j == 0'],
    max_steps=80,
    views=[
        dict(type='string', var='s', label='s', h=130, cell=70),
        dict(type='string', var='t', label='t', h=150, cell=70),
        dict(type='text', fn=_formula, size=24, h=70),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算；蓝 = 不用 s[i-1]；绿 = 用 s[i-1] 匹配）', h=380, cell=76,
             rows=lambda S: ['空'] + [f'{k}{c}' for k, c in enumerate(S0)], cols=lambda S: ['空'] + [f'{k}{c}' for k, c in enumerate(T0)],
             color=_cell),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('f[i][j]', 'f[i][j]', 'green')],
    captions={
        'f = [[0]': '`f[i][j]`：`s` 前 `i` 位的子序列里，`t` 前 `j` 位出现的次数；先全部填 0',
        'f[i][j] = 1': '`j = 0`：`t[:0]` 是空串，删光 `s` 就得到它，所以 `f[{i}][0]` = ==1==',
        'f[i][j] = f[i - 1][j]': lambda S, B, r: f'`s[:{S.i-1}]` 的子序列也都是 `s[:{S.i}]` 的子序列 → 先继承 `f[{S.i-1}][{S.j}] = {S.f[S.i-1][S.j]}`（不用 `s[{S.i-1}]`）',
        'if s[i - 1] == t[j - 1]': lambda S, B, r: (f'`s[{S.i-1}] = {S.s[S.i-1]}` 等于 `t[{S.j-1}] = {S.t[S.j-1]}` → 它们可以固定配对，再加 `f[{S.i-1}][{S.j-1}]`'
                                                 if S.s[S.i-1] == S.t[S.j-1] else f'`s[{S.i-1}] = {S.s[S.i-1]}` 不等于 `t[{S.j-1}] = {S.t[S.j-1]}` → 无法配对，不加'),
        'f[i][j] += f[i - 1][j - 1]': '配对后剩下 `s[:{i-1}]` 对 `t[:{j-1}]` 的情况 `f[{i-1}][{j-1}] = {f[i-1][j-1]}` → `f[{i}][{j}]` = =={f[i][j]}==',
        'return f[m][n]': '答案 `f[{m}][{n}]` = =={ret}==（`s` 的子序列中 `t` 出现的次数）',
    },
    cards=dict(
        one_liner='f[i][j]：先继承不用 s[i-1] 的，能配对再加上配对的',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['给你字符串 `s` 和 `t`，统计 `s` 的==子序列==中 `t` 出现的个数',
                 '示例：`s = "babga", t = "ba"` → `3`'],
        quote='若s[i - 1] == t[j - 1]，那么f[i][j]应该再额外加上f[i - 1][j - 1]的值，这里的原理是s[:i]的最后一位s[i - 1]与t[:j]的最后一位t[j - 1]固定匹配住。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i][j]` 表示 `s[:i]` 的子序列中 `t[:j]` 出现的次数',
              '`j = 0`：空串，恒为 1；`i = 0` 且 `j > 0`：凑不出，为 0',
              '一般情况：`s[:i-1]` 的子序列也是 `s[:i]` 的子序列，先取 `f[i-1][j]`',
              '最后一位能配对，再加 `f[i-1][j-1]`；原文说可用滚动数组优化到 `O(n)`'],
        summary=['时间 `O(mn)`，空间 `O(mn)`（可滚动数组压到 `O(n)`）',
                 '易错：`j = 0` 时 `f[i][0] = 1`，空串要算一种方案',
                 '易错：下标 `i-1`、`j-1`：`f` 比字符串多一行一列',
                 '原文变量 `index` 只用于建表，和后面的 `i`、`j` 无关'],
    ),
)
