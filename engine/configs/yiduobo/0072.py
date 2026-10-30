def _dep(S, i, j, v):
    ci, cj = S.get('i'), S.get('j')
    if ci is None or cj is None or ci == 0 or cj == 0:
        return None
    if S['word1'][ci - 1] == S['word2'][cj - 1]:
        return 'green' if (i, j) == (ci - 1, cj - 1) else None    # 情况 4：左上
    if (i, j) == (ci - 1, cj):
        return 'blue'       # 在 word2[j-1] 后插入 word1[i-1]
    if (i, j) == (ci, cj - 1):
        return 'pink'       # 删去 word2[j-1]
    if (i, j) == (ci - 1, cj - 1):
        return 'purple'     # 替换
    return None


def _formula(S):
    if 'j' not in S:
        return '`f[i][j]`：word2 前 j 位==变成== word1 前 i 位的最少操作数'
    i, j, f, a, b = S['i'], S['j'], S['f'], S['word1'], S['word2']
    if i == 0 or j == 0:
        return f'边界：f[{i}][{j}] = {max(i, j)}'
    if a[i - 1] == b[j - 1]:
        return f'{a[i - 1]} = {b[j - 1]}：f[{i}][{j}] = f[{i - 1}][{j - 1}] = =={f[i - 1][j - 1]}=='
    p, q, r = f[i - 1][j], f[i][j - 1], f[i - 1][j - 1]
    return f'{a[i - 1]} ≠ {b[j - 1]}：min(插 {p}, 删 {q}, 换 {r}) + 1 = =={min(p, q, r) + 1}=='


def _cap5(S, B, ret):
    i, j, f, a, b = S.i, S.j, S.f, S.word1, S.word2
    p, q, r = f[i - 1][j], f[i][j - 1], f[i - 1][j - 1]
    if (i, j) == (1, 1):
        return (f'情况 5：`{a[i - 1]}` ≠ `{b[j - 1]}`。插入 `{a[i - 1]}`：`{p}+1`；删去 `{b[j - 1]}`：`{q}+1`；'
                f'替换：`{r}+1` → 最小 =={f[i][j]}==')
    return f'情况 5：`{a[i - 1]}` ≠ `{b[j - 1]}` → `min(插 {p}, 删 {q}, 换 {r}) + 1 = {f[i][j]}`'


CONFIG = dict(
    num=72, title='编辑距离', difficulty='Medium', category='多维动态规划',
    author='yiduobo', technique='二维 DP：五种情况分类讨论',
    code='''
class Solution(object):
    def minDistance(self, word1, word2):

        m = len(word1)
        n = len(word2)

        f = [[0 for i in range(n + 1)] for j in range(m + 1)]

        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0:
                    if j == 0:
                        f[i][j] = 0
                    else:
                        f[i][j] = j
                else:
                    if j == 0:
                        f[i][j] = i
                    else:
                        if word1[i - 1] == word2[j - 1]:
                            f[i][j] = f[i - 1][j - 1]
                        else:
                            f[i][j] = min(f[i - 1][j - 1], f[i][j - 1], f[i - 1][j]) + 1
        return f[m][n]
''',
    call='Solution().minDistance("horse", "ros")',
    expect=3,
    skip=['n = len(word2)', 'f = [[0 for i', 'for i in range(m + 1)', 'for j in range(n + 1)',
          'if i == 0', 'if j == 0', 'if word1[i - 1] == word2[j - 1]'],
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='table', var='f', label='f[i][j]（蓝 = 插入 word1[i-1] · 粉 = 删去 word2[j-1] · 紫 = 替换）',
             rows=lambda S: ['0'] + [f'{k + 1}:{c}' for k, c in enumerate(S['word1'])],
             cols=lambda S: ['0'] + [f'{k + 1}:{c}' for k, c in enumerate(S['word2'])],
             cursors=[('m', 'n', 'green'), ('i', 'j', 'yellow')], color=_dep, cell=84, h=574),
    ],
    watch=['i', 'j', ('word1[i-1]', 'word1[i - 1]', 'orange'), ('word2[j-1]', 'word2[j - 1]', 'orange'),
           ('f[m][n]', 'f[m][n]', 'green')],
    captions={
        'm = len(word1)': '把所有操作都看成作用在 ==word2== 上：`f[i][j]` = word2 前 j 位变成 word1 前 i 位的最少操作数',
        'f[i][j] = 0': '情况 1：`i`、`j` 都为 0，两边都是空串 → `0`',
        'f[i][j] = j': lambda S, B, ret: (
            f'情况 2：`i = 0`，word2 必须==删去所有前 j 位== → `f[0][{S.j}] = {S.j}`' if S.j == 1
            else f'情况 2：删去前 `{S.j}` 位 → `{S.j}`'),
        'f[i][j] = i': lambda S, B, ret: (
            f'情况 3：`j = 0`，word2 必须==完全复制== word1 的前 i 位（插入 i 位）→ `f[{S.i}][0] = {S.i}`' if S.i == 1
            else f'情况 3：插入 `{S.i}` 位 → `{S.i}`'),
        'f[i][j] = f[i - 1][j - 1]': '情况 4：`word1[{i-1}] = word2[{j-1}] = {word1[i-1]}`，==不需要任何操作== → `f[{i}][{j}] = f[{i-1}][{j-1}] = {f[i][j]}`',
        'f[i][j] = min(': _cap5,
        'return f[m][n]': '返回 `f[m][n]` = =={ret}==',
    },
    cards=dict(
        one_liner='先把三种操作统一成「只改 word2」，再分五种情况递推',
        complexity='时间 `O(mn)`，空间 `O(mn)`（滚动数组 `O(min(m, n))`）',
        problem=['把 `word1` 变成 `word2`，每次可以==插入、删除或替换==一个字符',
                 '求最少操作数',
                 '示例：`"horse"` → `"ros"`：`3`'],
        quote='所有操作都可以认为是在同一个字符串上进行的，于是就可以问题当成从字符串word1变换到固定的字符串word2需要多少步。',
        quote_src='—— yiduobo 题解',
        idea=['改 word1 的字符 = 改 word2 对应的字符',
              '删 word1 的字符 = 在 word2 对应位置插入；插入同理 = 删 word2 的字符',
              '于是 `f[i][j]` 只看 word2 前 j 位怎么变成 word1 前 i 位',
              '分五种情况：两空 / `i=0` / `j=0` / 末字符相等 / 末字符不等（插、删、换取最小）'],
        after=[dict(heading='原文答疑：情况 4 为什么不考虑插入、删除？', lines=[
            '`f[i-1][j-1]` 与 `f[i][j-1]`、`f[i-1][j]` 的差值==至多为 1==',
            '一次操作就能消除这两种状态所代表的串之间的差异',
            '故 `f[i-1][j-1] ≤ min(f[i][j-1], f[i-1][j]) + 1`，继承左上最优',
        ])],
        summary=['时间 `O(mn)`；空间 `O(mn)`，用滚动数组可降到 `O(min(m, n))`',
                 '易错：边界 `f[0][j] = j`、`f[i][0] = i`，不是 0',
                 '易错：比较的是 `word1[i-1]` 和 `word2[j-1]`（f 的下标从 1 开始）',
                 '原文为 Python 2 风格，仅删去了 `"""type"""` 文档字符串，代码未改'],
    ),
)
