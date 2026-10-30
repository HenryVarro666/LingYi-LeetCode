S0 = 'bbbab'


def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    line = S.get('_line', 0)
    if i is None or j is None or line not in (8, 9, 11) or j <= i:
        if i is not None and r == i and c == i and line == 6:
            return 'yellow'
        return None
    if r == i and c == j:
        return 'yellow'
    if S['s'][i] == S['s'][j]:
        return 'green' if (r, c) == (i + 1, j - 1) else None
    return 'blue' if (r, c) in ((i + 1, j), (i, j - 1)) else None


def _cap_if(S, B, ret):
    s, i, j = S.s, S.i, S.j
    if s[i] == s[j]:
        inner = '空串 = 0' if i + 1 > j - 1 else f'`f[{i + 1}][{j - 1}]`'
        return f'`s[{i}] = s[{j}] = {s[i]}`：两端==都选==，再加上里面 {inner}'
    return f'`s[{i}] = {s[i]} ≠ s[{j}] = {s[j]}`：==枚举哪个不选=='


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or j <= i or S.get('_line') not in (8, 9, 11):
        return '`f[i][j]` = `s[i..j]` 的最长回文子序列长度；`i` 从大到小，`j` 从小到大'
    s = S['s']
    if s[i] == s[j]:
        return f'`f[{i}][{j}] = f[{i + 1}][{j - 1}] + 2`'
    return f'`f[{i}][{j}] = max(f[{i + 1}][{j}], f[{i}][{j - 1}])`'


CONFIG = dict(
    num=516, title='最长回文子序列', difficulty='Medium', category='多维动态规划',
    author='灵茶山艾府', technique='区间 DP（记忆化搜索 1:1 翻译成递推）',
    tags=['热题173'],
    code='''
class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        n = len(s)
        f = [[0] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            f[i][i] = 1
            for j in range(i + 1, n):
                if s[i] == s[j]:
                    f[i][j] = f[i + 1][j - 1] + 2
                else:
                    f[i][j] = max(f[i + 1][j], f[i][j - 1])
        return f[0][-1]
''',
    call=f'Solution().longestPalindromeSubseq({S0!r})',
    expect=4,
    skip=['for j in range'],
    views=[
        dict(type='string', var='s', label='s', h=170, cell=80, pointers={'i': 'blue', 'j': 'pink'},
             color=lambda S, k, v: ('blue' if k == S.get('i') else 'pink' if k == S.get('j') and S.get('_line') in (8, 9, 11) else None)),
        dict(type='text', fn=_formula, size=26, h=60),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算，绿/蓝 = 它依赖的格子）', h=380, cell=70,
             rows=lambda S: [f'{k}{c}' for k, c in enumerate(S0)], cols=lambda S: [f'{k}{c}' for k, c in enumerate(S0)],
             color=_cell),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('s[i]', 's[i]', 'blue'), ('s[j]', 's[j]', 'pink')],
    captions={
        'n = len(s)': '`n = {n}`',
        'f = [[0] * n': '`f[i][j]` 对应 `dfs(i, j)`；`i > j` 是空串，值为 0',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：算 `f[i][·]` 要先有 `f[i+1][·]` → ==i 从大到小==枚举' if S.get('i') != B.get('i')
                                           else '所有区间都算完了'),
        'f[i][i] = 1': '`f[{i}][{i}] = 1`：只有一个字母',
        'if s[i] == s[j]': _cap_if,
        'f[i][j] = f[i + 1][j - 1] + 2': '`f[{i}][{j}] = {f[i+1][j-1]} + 2` = =={f[i][j]}==',
        'f[i][j] = max(': '`f[{i}][{j}] = max({f[i+1][j]}, {f[i][j-1]})` = =={f[i][j]}==',
        'return f[0][-1]': '整个字符串 `s[0..{n-1}]` 的答案 `f[0][{n-1}]` = =={ret}==',
    },
    cards=dict(
        one_liner='看两端：相同都选，不同就枚举哪个不选',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['给你一个字符串 `s`，找出其中==最长的回文子序列==，返回它的长度',
                 '子序列：不改变顺序，删除某些字符（或不删）得到的序列',
                 '示例：`s = "bbbab"` → `4`（`"bbbb"`）；`s = "cbbd"` → `2`'],
        quote='要计算 f[i][j]，必须先把 f[i+1][·] 算出来，那么只有 ==i 从大到小==枚举才能做到。……需要用到 f[i][j−1]，所以 ==j 必须从小到大==枚举。',
        quote_src='—— 灵茶山艾府题解（二、1:1 翻译成递推）',
        idea=['记忆化搜索 `dfs(i, j)`：`s[i] == s[j]` 都选 `+2`；否则 `max(dfs(i+1,j), dfs(i,j-1))`',
              '1:1 翻译成递推：`dfs` 改成 `f` 数组，递归改成循环',
              '`i ≥ j` 是递归边界，所以 `j` 从 `i + 1` 开始'],
        summary=['时间 `O(n^2)` = 状态个数 `O(n^2)` × 单个状态转移 `O(1)`',
                 '易错：循环顺序 ==i 倒序、j 正序==，否则用到还没算的状态',
                 '空间优化：用一维 `f` + 变量 `pre` 保存 `f[i+1][j-1]`，空间 `O(n)`',
                 '同类区间 DP：1312. 让字符串成为回文串的最少插入次数'],
    ),
)
