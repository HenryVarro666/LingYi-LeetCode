_pending = set()   # (i, j)：x != y 时这一行会触发两次（先判断、再赋值），用来区分两步


def _dep(S, i, j, v):
    ci, cj = S['i'], S['j']
    if S['x'] == S['y']:
        return 'green' if (i, j) == (ci, cj) else None          # 左上
    if (i, j) == (ci, cj + 1):
        return 'blue'                                           # 上：丢掉 x
    if (i, j) == (ci + 1, cj):
        return 'pink'                                           # 左：丢掉 y
    return None


def _formula(S):
    if 'y' not in S:
        return '`f[i+1][j+1]` = `s` 前 `i+1` 个字母与 `t` 前 `j+1` 个字母的 LCS 长度'
    i, j, x, y, f = S['i'], S['j'], S['x'], S['y'], S['f']
    if x == y:
        return f'x = y = {x}：f[{i + 1}][{j + 1}] = 左上 {f[i][j]} + 1 = =={f[i][j] + 1}=='
    a, b = f[i][j + 1], f[i + 1][j]
    return f'x = {x} ≠ y = {y}：f[{i + 1}][{j + 1}] = max(上 {a}, 左 {b}) = =={max(a, b)}=='


def _cap_cell(S, B, ret):
    i, j, x, y, f = S.i, S.j, S.x, S.y, S.f
    if j == 0 and i > 0 and (x == y or (i, j) not in _pending):
        return f'外层换到 `x = {x}`。' + _cap_cell2(S, B, ret)
    return _cap_cell2(S, B, ret)


def _cap_cell2(S, B, ret):
    i, j, x, y, f = S.i, S.j, S.x, S.y, S.f
    if x == y:
        return (f'`x = y = {x}`：最后一个字母相同，==一定选== → '
                f'`dfs(i-1, j-1) + 1` = 左上 `{f[i][j]}` + 1 = `{f[i + 1][j + 1]}`')
    if (i, j) not in _pending:
        _pending.add((i, j))
        if (i, j) == (0, 1):
            return f'`x = {x}` ≠ `y = {y}`：不能一起选 → 走 `else`，看丢掉哪一个更好'
        return f'`x = {x}` ≠ `y = {y}` → 走 `else`'
    _pending.discard((i, j))
    return f'`max(丢 x：上 {f[i][j + 1]}, 丢 y：左 {f[i + 1][j]}) = {f[i + 1][j + 1]}`'


CONFIG = dict(
    num=1143, title='最长公共子序列', difficulty='Medium', category='多维动态规划',
    author='灵茶山艾府', technique='线性 DP：记忆化搜索 → 1:1 翻译成递推',
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
    call='Solution().longestCommonSubsequence("abcde", "ace")',
    expect=3,
    skip=['f = [[0] * (m + 1)', 'for i, x in enumerate(s)', 'for j, y in enumerate(t)', 'max(f[i][j + 1], f[i + 1][j])'],
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='table', var='f', label='f（行头 = s 的字母 x，列头 = t 的字母 y；第 0 行 / 列 = 空串）',
             rows=lambda S: ['∅'] + list(S['s']), cols=lambda S: ['∅'] + list(S['t']),
             cursors=[('n', 'm', 'purple'), ('i + 1', 'j + 1', 'yellow')], color=_dep, cell=84, h=574),
    ],
    watch=['i', 'j', ('x', 'x', 'orange'), ('y', 'y', 'orange'), ('f[n][m]', 'f[n][m]', 'purple')],
    captions={
        'n, m = len(s), len(t)': 'f 开 `(n+1) × (m+1)`，第 0 行 / 第 0 列 = ==空串==，LCS 为 0（翻译自 `dfs(-1, j) = dfs(i, -1) = 0`）',
        'f[i + 1][j + 1] = f[i][j] + 1 if x == y else': _cap_cell,
        'return f[n][m]': '`f[n][m]` 翻译自递归入口 `dfs(n-1, m-1)`：LCS 长度 =={ret}==（`"ace"`）',
    },
    cards=dict(
        one_liner='只看两个字符串的最后一个字母：相同就选，不同就丢一个',
        complexity='时间 `O(nm)`，空间 `O(nm)`（可优化到 `O(m)`）',
        problem=['求 `text1` 和 `text2` 的==最长公共子序列==的长度，没有则返回 0',
                 '子序列：删掉若干字符、不改变相对顺序得到的串（`"ace"` 是 `"abcde"` 的子序列）',
                 '示例：`"abcde"`, `"ace"` → `3`（`"ace"`）'],
        quote='一、递归搜索 + 保存计算结果 = 记忆化搜索 …… 二、==1:1 翻译成递推==',
        quote_src='—— 灵茶山艾府题解（小标题）',
        idea=['`dfs(i,j)` = `s[0..i]` 与 `t[0..j]` 的 LCS 长度，只看最后的 `s[i]`、`t[j]`',
              '相同：`dfs(i-1,j-1) + 1`；不同：`max(dfs(i-1,j), dfs(i,j-1))`',
              '边界 `i < 0` 或 `j < 0` 返回 0；入参重复 → `@cache` 记忆化',
              '去掉「递」只留「归」：`f[i+1][j+1]` ==就是== `dfs(i,j)`，+1 给空串留位置'],
        after=[dict(heading='记忆化搜索 → 递推：逐项对照', lines=[
            '`dfs(i, j)` ↔ `f[i+1][j+1]`（下标整体 +1）',
            '边界 `dfs(-1, j) = dfs(i, -1) = 0` ↔ 第 0 行 / 第 0 列全是 0',
            '`dfs(i-1, j-1) + 1` ↔ 左上 `f[i][j] + 1`',
            '`max(dfs(i-1, j), dfs(i, j-1))` ↔ `max(上, 左)`',
            '递归入口 `dfs(n-1, m-1)` ↔ 答案 `f[n][m]`',
        ])],
        summary=['时间 `O(nm)`，空间 `O(nm)`',
                 '易错：f 的下标比 s、t 多 1：比较的是 `s[i]`、`t[j]`，写入的是 `f[i+1][j+1]`',
                 '原文还有滚动数组和一个数组的写法，空间 `O(m)`',
                 '一个数组时 ==j 不能倒序==：`f[i+1][j+1]` 要用到本行刚算好的 `f[i+1][j]`'],
    ),
)
