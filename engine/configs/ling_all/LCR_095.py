S0, T0 = 'abcde', 'ace'


def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line', 0) < 7:
        return None
    if (r, c) == (i + 1, j + 1):
        return 'yellow'
    if S['x'] == S['y']:
        return 'green' if (r, c) == (i, j) else None
    return 'blue' if (r, c) in ((i, j + 1), (i + 1, j)) else None


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return '`f[i][j]` = `s` 前 `i` 个字母与 `t` 前 `j` 个字母的最长公共子序列长度'
    if S['x'] == S['y']:
        return f'`s[{i}] = t[{j}] = {S["x"]}`：`f[{i+1}][{j+1}] = f[{i}][{j}] + 1`'
    return f'`s[{i}] = {S["x"]} ≠ t[{j}] = {S["y"]}`：`f[{i+1}][{j+1}] = max(f[{i}][{j+1}], f[{i+1}][{j}])`'


CONFIG = dict(
    num='LCR 095', title='最长公共子序列', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='二维 DP（记忆化搜索 1:1 翻译成递推）',
    tags=[],
    code='''
class Solution:
    def longestCommonSubsequence(self, s: str, t: str) -> int:
        n, m = len(s), len(t)
        f = [[0] * (m + 1) for _ in range(n + 1)]
        for i, x in enumerate(s):
            for j, y in enumerate(t):
                f[i + 1][j + 1] = f[i][j] + 1 if x == y else \\
                                  max(f[i][j + 1], f[i + 1][j])
        return f[n][m]
''',
    call=f'Solution().longestCommonSubsequence({S0!r}, {T0!r})',
    expect=3,
    skip=['max(f[i][j + 1]', 'for i, x in enumerate', 'for j, y in enumerate', 'n, m = len'],
    views=[
        dict(type='string', var='s', label='s', h=135, cell=70, pointers={'i': 'blue'},
             color=lambda S, k, v: 'blue' if k == S.get('i') and 'x' in S else None),
        dict(type='string', var='t', label='t', h=160, cell=70, pointers={'j': 'pink'},
             color=lambda S, k, v: 'pink' if k == S.get('j') and 'y' in S and S.get('_line', 0) >= 8 else None),
        dict(type='text', fn=_formula, size=24, h=70),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算，绿/蓝 = 它依赖的格子）', h=320, cell=64,
             rows=lambda S: ['空'] + [f'{k}{c}' for k, c in enumerate(S0)], cols=lambda S: ['空'] + [f'{k}{c}' for k, c in enumerate(T0)],
             color=_cell),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('x', 'x', 'blue'), ('y', 'y', 'pink')],
    captions={
        'f = [[0]': '`f[i][j]` 对应 `dfs(i-1, j-1)`：多留一行一列表示空串，值全为 0（边界）',
        'f[i + 1][j + 1] = f[i][j] + 1': lambda S, B, ret: (
            f'`{S.x} == {S.y}`：这对字母可以==配对==，前面各去掉一个再 +1：`f[{S.i+1}][{S.j+1}] = {S.f[S.i][S.j]} + 1 = {S.f[S.i+1][S.j+1]}`'
            if S.x == S.y else
            (f'`{S.x} ≠ {S.y}`：不能同时配对，只能丢掉一个' if S.f[S.i+1][S.j+1] != max(S.f[S.i][S.j+1], S.f[S.i+1][S.j])
             else f'丢掉谁？取 `max(上 {S.f[S.i][S.j+1]}, 左 {S.f[S.i+1][S.j]})` = =={S.f[S.i+1][S.j+1]}==，写入 `f[{S.i+1}][{S.j+1}]`')),
        'return f[n][m]': '整个 `s` 与整个 `t` 的答案 `f[{n}][{m}]` = =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='看末尾两个字母：相同就一起选，不同就丢掉其中一个',
        complexity='时间 `O(nm)`，空间 `O(nm)`',
        problem=['给两个字符串 `text1`、`text2`，求最长==公共子序列==的长度',
                 '子序列：不改变顺序，删去若干字符（或不删）',
                 '示例：`"abcde"`、`"ace"` → `3`（`"ace"`）'],
        quote='递归搜索 + 保存计算结果 = 记忆化搜索；1:1 翻译成递推：dfs 改成 f 数组，递归改成循环，i、j 的下标整体加 1 避免负数。',
        quote_src='—— 灵茶山艾府题解（一、二）',
        idea=['`dfs(i, j)` 看 `s[i]`、`t[j]`：相等 → `dfs(i-1, j-1) + 1`',
              '不相等 → 要么不选 `s[i]`，要么不选 `t[j]`，取 `max`',
              '翻译成递推：`f[i+1][j+1]` 对应 `dfs(i, j)`，多出的第 0 行/列是空串'],
        result='最长公共子序列长度 3',
        summary=['时间 `O(nm)`（状态数 × O(1) 转移），空间 `O(nm)`',
                 '易错：`f` 是 `(n+1) × (m+1)`，下标整体右移一位',
                 '滚动数组：只依赖上一行，两个数组交替使用，空间 `O(m)`',
                 '一个数组：用变量 `pre` 保存左上角的 `f[i][j]`，空间 `O(m)`',
                 '同类题：1035. 不相交的线、72. 编辑距离'],
    ),
)
