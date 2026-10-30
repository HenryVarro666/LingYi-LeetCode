W1, W2 = 'sea', 'eat'


def _dep(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or 'f' not in S:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    line = S.get('_line')
    if line == 23 and (r, c) == (i, j - 1):
        return 'blue'
    if line == 28 and (r, c) == (i - 1, j):
        return 'blue'
    if line == 31 and (r, c) == (i - 1, j - 1):
        return 'green'
    if line == 33 and (r, c) in ((i - 1, j), (i, j - 1)):
        return 'blue'
    return None


def _eq(S, B, ret):
    a, b = S.word1[S.i], S.word2[S.j]
    i, j = S.i, S.j
    if a == b:
        return f'`word1[{i}] = word2[{j}] = {a}`：最后一位能==匹配上=='
    return f'`word1[{i}] = {a} ≠ word2[{j}] = {b}`：至少要删掉一个'


CONFIG = dict(
    num=583, title='两个字符串的删除操作', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='编辑距离式 DP（只有删除）',
    tags=['labuladong', '灵神核心路线'],
    code='''
class Solution(object):
    def minDistance(self, word1, word2):

        m = len(word1)
        n = len(word2)
        if m == 0:
            return n
        if n == 0:
            return m
        f = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        if word1[i] == word2[j]:
                            f[i][j] = 0
                        else:
                            f[i][j] = 2
                    else:
                        if word1[i] == word2[j]:
                            f[i][j] = j
                        else:
                            f[i][j] = f[i][j - 1] + 1
                elif j == 0:
                    if word1[i] == word2[j]:
                        f[i][j] = i
                    else:
                        f[i][j] = f[i - 1][j] + 1
                else:
                    if word1[i] == word2[j]:
                        f[i][j] = f[i - 1][j - 1]
                    else:
                        f[i][j] = min(f[i - 1][j], f[i][j - 1]) + 1

        return f[m - 1][n - 1]
''',
    call=f'Solution().minDistance({W1!r}, {W2!r})',
    expect=2,
    skip=['for j in range(n)', 'if m == 0', 'if n == 0'],
    max_steps=60,
    views=[
        dict(type='string', var='word1', label='word1', h=200, cell=80, pointers={'i': 'blue'}),
        dict(type='string', var='word2', label='word2', h=200, cell=80, pointers={'j': 'pink'}),
        dict(type='table', var='f', label='f[i][j]：word1 前 i 位与 word2 前 j 位（含）匹配的最少删除次数', h=280, cell=72,
             rows=lambda S: [f'{k}{ch}' for k, ch in enumerate(W1)], cols=lambda S: [f'{k}{ch}' for k, ch in enumerate(W2)],
             color=_dep),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('f[i][j]', 'f[i][j]', 'yellow')],
    captions={
        'm = len(word1)': '`m = {m}`',
        'n = len(word2)': '`n = {n}`',
        'f = [[0] * n': '`f[i][j]`：下标 ==含 i、含 j==，所以 i = 0、j = 0 要单独讨论',
        'for i in range(m)': lambda S, B, r: (f'第 `{S.i}` 行：`word1[{S.i}] = {S.word1[S.i]}`' if B.get('i') != S.i else '整张表填完'),
        'if i == 0': lambda S, B, r: ('`i = 0`：word1 只有第 0 位' if S.i == 0 else f'`i = {S.i} ≠ 0`'),
        14: lambda S, B, r: ('`j = 0`：两边都只有一位' if S.j == 0 else f'`j = {S.j} ≠ 0`：word2 有 {S.j + 1} 位'),
        24: lambda S, B, r: ('`j = 0`：word2 只有第 0 位，与情况 2 对称' if S.j == 0 else f'`j = {S.j}`：两维都不为 0，一般情况'),
        'if word1[i] == word2[j]': _eq,
        "f[i][j] = 0": '两个单字符相同 → 不用删，`f[0][0] = 0`',
        "f[i][j] = 2": '两个单字符不同 → 各删一个，`f[0][0] = 2`',
        "f[i][j] = j": '`f[0][{j}] = {j}`：删去 word2 前面 {j} 位',
        "f[i][j] = f[i][j - 1] + 1": '删去 word2 第 {j} 位：`f[0][{j}] = f[0][{j-1}] + 1 = {f[i][j]}`',
        "f[i][j] = i": '`f[{i}][0] = {i}`：删去 word1 前面 {i} 位',
        "f[i][j] = f[i - 1][j] + 1": '删去 word1 第 {i} 位：`f[{i}][0] = f[{i-1}][0] + 1 = {f[i][j]}`',
        "f[i][j] = f[i - 1][j - 1]": '匹配上 → 无需删除：`f[{i}][{j}] = f[{i-1}][{j-1}]` = =={f[i][j]}==',
        "f[i][j] = min(": '删 word1 第 i 位或删 word2 第 j 位：`min({f[i-1][j]}, {f[i][j-1]}) + 1` = =={f[i][j]}==',
        'return f[m - 1][n - 1]': '`f[{m-1}][{n-1}]` = =={ret}==：最少删除 {ret} 次',
    },
    cards=dict(
        one_liner='编辑距离的简化版：只能删除，不同就删掉其中一个',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['给两个单词 `word1`、`word2`，每步可以删除任一字符串中的一个字符',
                 '求使两个单词==相同==所需的最少步数',
                 f'示例 / 本视频：`"{W1}"`、`"{W2}"` → `2`（删 s、删 t）'],
        quote='若word1[i]等于word2[j]，那么就有f[i][j] = f[i - 1][j - 1]，否则尝试删去word1的第i位字符或者删去word2的第j为字符，即f[i][j] = min(f[i - 1][j], f[i][j - 1]) + 1。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：word1 前 i 位和 word2 前 j 位==（含 i、j）==匹配需要的操作数',
              '下标从 0 开始含自身，所以第 0 行、第 0 列按 4 种情况单独初始化',
              '一般情况：相同就继承左上，不同就删一个取较小 + 1'],
        summary=['时间 / 空间 `O(mn)`',
                 '易错：`i = 0` 且字符相同时 `f[0][j] = j`，不是 `f[0][j-1]`',
                 '这种「含自身」的定义边界较繁琐；多开一行一列（空串）可省掉分类讨论',
                 '原文代码在 Python 3 下可直接运行，未做修改',
                 '同类题：72. 编辑距离、712. 最小 ASCII 删除和'],
    ),
)
