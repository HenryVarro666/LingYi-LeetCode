def _dep(S, i, j, v):
    ci, cj = S.get('i'), S.get('j')
    if ci is None or cj is None:
        return None
    if S['text1'][ci - 1] == S['text2'][cj - 1]:
        return 'green' if (i, j) == (ci - 1, cj - 1) else None   # 匹配：左上
    if (i, j) == (ci - 1, cj):
        return 'blue'                                           # 浪费 text1[i-1]
    if (i, j) == (ci, cj - 1):
        return 'pink'                                           # 浪费 text2[j-1]
    return None


def _formula(S):
    if 'j' not in S:
        return '`f[i][j]` = text1 ==前 i 个==字符与 text2 ==前 j 个==字符的 LCS 长度'
    i, j, a, b, f = S['i'], S['j'], S['text1'], S['text2'], S['f']
    x, y = a[i - 1], b[j - 1]
    if x == y:
        return f'text1[{i - 1}] = text2[{j - 1}] = {x}：匹配，f[{i - 1}][{j - 1}] + 1 = =={f[i - 1][j - 1] + 1}=='
    return f'{x} ≠ {y}：浪费一个，max(f[{i - 1}][{j}], f[{i}][{j - 1}]) = =={max(f[i - 1][j], f[i][j - 1])}=='


CONFIG = dict(
    num=1143, title='最长公共子序列', difficulty='Medium', category='多维动态规划',
    author='yiduobo', technique='经典二维 DP：匹配 or 浪费',
    code='''
class Solution(object):
    def longestCommonSubsequence(self, text1, text2):

        m = len(text1)
        n = len(text2)
        f = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    f[i][j] = f[i - 1][j - 1] + 1
                else:
                    f[i][j] = max(f[i - 1][j], f[i][j - 1])

        return f[-1][-1]
''',
    call='Solution().longestCommonSubsequence("abcde", "ace")',
    expect=3,
    skip=['n = len(text2)', 'f = [[0] * (n + 1)', 'for i in range(1, m + 1)', 'for j in range(1, n + 1)'],
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='table', var='f', label='f[i][j]（行头 i:text1 第 i 个字符，列头 j:text2 第 j 个字符）',
             rows=lambda S: ['0'] + [f'{k + 1}:{c}' for k, c in enumerate(S['text1'])],
             cols=lambda S: ['0'] + [f'{k + 1}:{c}' for k, c in enumerate(S['text2'])],
             cursors=[('m', 'n', 'green'), ('i', 'j', 'yellow')], color=_dep, cell=84, h=574),
    ],
    watch=['i', 'j', ('text1[i-1]', 'text1[i - 1]', 'orange'), ('text2[j-1]', 'text2[j - 1]', 'orange'),
           ('f[-1][-1]', 'f[-1][-1]', 'green')],
    captions={
        'm = len(text1)': '情况 1：`i` 或 `j` 为 0 时（某一边是空串）显然 `f[i][j] = 0`，所以 f 先全填 0',
        'if text1[i - 1] == text2[j - 1]': lambda S, B, ret: (
            (f'第 `{S.i}` 行：text1 前 {S.i} 个字符。' if S.j == 1 else '') + f'比较 `text1[{S.i - 1}] = {S.text1[S.i - 1]}` 和 `text2[{S.j - 1}] = {S.text2[S.j - 1]}` → '
            + ('==相等==' if S.text1[S.i - 1] == S.text2[S.j - 1] else '不相等')),
        'f[i][j] = f[i - 1][j - 1] + 1': '情况 2：应该让这两个字符==匹配== → `f[{i}][{j}] = f[{i-1}][{j-1}] + 1 = {f[i][j]}`',
        'f[i][j] = max(': '情况 3：浪费 `text1[{i-1}]` 得 `{f[i-1][j]}`，浪费 `text2[{j-1}]` 得 `{f[i][j-1]}` → 取大 =={f[i][j]}==',
        'return f[-1][-1]': '`f[-1][-1]` 就是 `f[m][n]`：LCS 长度 =={ret}==',
    },
    cards=dict(
        one_liner='相同就匹配，不同就浪费掉其中一个',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['求 `text1` 和 `text2` 的==最长公共子序列==的长度，没有则返回 0',
                 '子序列：删掉若干字符、不改变相对顺序得到的串',
                 '示例：`"abcde"`, `"ace"` → `3`（`"ace"`）'],
        quote='当i和j都不为0，且text1[i - 1] = text2[j - 1]，那么我们应该让这两个字符进行匹配……其他情况下，则需要浪费掉text1[i - 1]或者text2[j - 1]',
        quote_src='—— yiduobo 题解',
        idea=['`f[i][j]`：text1 前 `i` 个字符与 text2 前 `j` 个字符的 LCS 长度',
              '情况 1：`i` 或 `j` 为 0 → 0',
              '情况 2：最后两个字符相等 → 匹配它们：`f[i-1][j-1] + 1`',
              '情况 3：不相等 → 浪费哪个取决于谁大：`max(f[i-1][j], f[i][j-1])`'],
        summary=['时间 `O(mn)`，空间 `O(mn)`；只依赖上一行，可用滚动数组降到 `O(n)`',
                 '易错：f 下标从 1 开始，比较的是 `text1[i-1]` 和 `text2[j-1]`',
                 '`f[-1][-1]` 就是右下角 `f[m][n]`',
                 '原文为 Python 2 风格，仅删去了 `"""type"""` 文档字符串'],
    ),
)
