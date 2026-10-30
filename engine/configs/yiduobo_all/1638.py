def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line') is None:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if i > 0 and j > 0 and (r, c) == (i - 1, j - 1):
        return 'blue'
    return None


def _tx(S):
    if 'i' not in S or 'j' not in S:
        return '`f` = 结尾相同的子串数；`g` = 恰好差一个字符的子串数'
    i, j, s, t = S['i'], S['j'], S['s'], S['t']
    if i == 0 or j == 0:
        return f"边界：`s[{i}]`={s[i]!r}，`t[{j}]`={t[j]!r}，单个字符对"
    if s[i] == t[j]:
        return f"{s[i]!r} = {t[j]!r}：`f[{i}][{j}] = f[{i-1}][{j-1}] + 1`，`g[{i}][{j}] = g[{i-1}][{j-1}]`"
    return f"{s[i]!r} ≠ {t[j]!r}：`g[{i}][{j}] = f[{i-1}][{j-1}] + 1`"


CONFIG = dict(
    num=1638, title='统计只差一个字符的子串数目', difficulty='Medium', category='字符串',
    author='yiduobo', technique='二维 DP：f 全同、g 差一个',
    tags=[],
    code='''
class Solution(object):
    def countSubstrings(self, s, t):

        m = len(s)
        n = len(t)
        f = [[0] * n for _ in range(m)]
        g = [[0] * n for _ in range(m)]

        res = 0
        for i in range(m):
            for j in range(n):
                if i == 0 or j == 0:
                    if s[i] == t[j]:
                        f[i][j] = 1
                    else:
                        g[i][j] = 1
                elif s[i] == t[j]:
                    f[i][j] = f[i - 1][j - 1] + 1
                    g[i][j] = g[i - 1][j - 1]
                else:
                    g[i][j] = f[i - 1][j - 1] + 1
                
                res += g[i][j]
        
        return res
''',
    call='Solution().countSubstrings("aba", "baba")',
    expect=6,
    views=[
        dict(type='string', var='s', label='s', h=130, cell=70, pointers={'i': 'blue'}),
        dict(type='string', var='t', label='t', h=130, cell=70, pointers={'j': 'pink'}),
        dict(type='table', var='f', label='f：以 s[i]、t[j] 结尾且完全相同', h=190, color=_cell,
             rows=lambda S: list(S['s']), cols=lambda S: list(S['t'])),
        dict(type='table', var='g', label='g：以 s[i]、t[j] 结尾且恰差一个字符', h=190, color=_cell,
             rows=lambda S: list(S['s']), cols=lambda S: list(S['t'])),
        dict(type='text', fn=_tx, size=24, h=60),
    ],
    watch=['i', 'j', ('res', 'res', 'green')],
    captions={
        'm = len(s)': '`m = {m}`',
        'n = len(t)': '`n = {n}`',
        'f = [[0]': '`f[i][j]`：以 `s[i]`、`t[j]` 结尾、==完全相同==的子串对数',
        'g = [[0]': '`g[i][j]`：以 `s[i]`、`t[j]` 结尾、==恰好差一个字符==的子串对数',
        'res = 0': '`res` 累加所有 `g[i][j]`',
        'if i == 0 or j == 0': lambda S, B, r: ('在边界：前面没有字符可延伸，只能是单个字符对' if (S.i == 0 or S.j == 0) else '不在边界：可以从 `(i-1, j-1)` 延伸'),
        'if s[i] == t[j]': lambda S, B, r: (f"`s[{S.i}] = {S.s[S.i]!r}`，`t[{S.j}] = {S.t[S.j]!r}`：" + ('相同' if S.s[S.i] == S.t[S.j] else '不同')),
        'f[i][j] = 1': '单字符相同：`f[{i}][{j}] = 1`',
        'g[i][j] = 1': '单字符不同：恰差一个，`g[{i}][{j}] = 1`',
        'f[i][j] = f[i - 1][j - 1] + 1': '末尾相同：在 `f[i-1][j-1]` 的全同子串后各加一个字符，再加上单独一对 → `f = {f[i][j]}`',
        'g[i][j] = g[i - 1][j - 1]': '末尾相同：差异必须在前面，沿用 `g[i-1][j-1]` → `g = {g[i][j]}`（单独一对不算）',
        'g[i][j] = f[i - 1][j - 1] + 1': '末尾不同：前面必须全同，`f[i-1][j-1] + 1`（含单独一对）→ `g = {g[i][j]}`',
        'res += g[i][j]': '答案累加 `g[{i}][{j}] = {g[i][j]}` → `res = {res}`',
        'return res': '所有 `g` 之和 = `{res}`',
    },
    cards=dict(
        one_liner='f 记全同的，g 记差一个的，沿对角线转移',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['给两个字符串 `s`、`t`，统计 `s` 的子串与 `t` 的子串==恰好只有一个字符不同==的配对数',
                 '示例：`s="aba"`，`t="baba"`',
                 '结果 `6`'],
        quote='令f[i][j]表示以s[i]和t[j]结尾的相同子串的数目，令g[i][j]表示以s[i]和t[j]结尾的只差一个字符的子串数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['末尾相同：`f = f[i-1][j-1] + 1`，`g = g[i-1][j-1]`',
              '末尾不同：已经用掉那一个差异，前面必须全同：`g = f[i-1][j-1] + 1`',
              '所有 `g[i][j]` 之和就是答案；原文说明也可用滚动数组'],
        summary=['时间 `O(mn)`，空间 `O(mn)`（可滚动优化）',
                 '易错点：末尾相同时，单独一对不算「差一个」，所以 `g` 不加 1',
                 '边界 `i=0` 或 `j=0` 只有单字符对',
                 '原文为 Python 2 风格，代码未改动'],
    ),
)
