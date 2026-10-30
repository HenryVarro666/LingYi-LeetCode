def _c(name):
    def f(S, r, c, v):
        i, j = S.get('i'), S.get('j')
        if i is None:
            return None
        if (r, c) == (i, j) or (name == 'g' and j is None and (r, c) == (i, 1)):
            return 'yellow'
        return 'green' if v else None
    return f


def _txt(S):
    i, j = S.get('i'), S.get('j')
    if i is None:
        return '`f[i][j]`：最后一条线段右端恰为 i；`g[i][j]`：f[j..i][j] 之和（前缀和）'
    if j is None or j < 2:
        return f'`i = {i}`：只有 1 条线段，左端在 0 ~ {i - 1} 任选，共 `i = {i}` 种'
    return f"`f[{i}][{j}] = f[{i - 1}][{j}] + g[{i - 1}][{j - 1}]`，`g[{i}][{j}] = g[{i - 1}][{j}] + f[{i}][{j}]`"


CONFIG = dict(
    num=1621, title='大小为 K 的不重叠线段的数目', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='动态规划 · 前缀和优化',
    tags=['灵神题单', '数学算法', '难度分 2198'],
    code='''
class Solution(object):
    def numberOfSets(self, n, k):

        f = [[0] * (k + 1) for _ in range(n)]
        g = [[0] * (k + 1) for _ in range(n)]
        mod = 10 ** 9 + 7
        for i in range(1, n):
            f[i][1] = i
            g[i][1] = g[i - 1][1] + i 
            for j in range(2, min(i, k) + 1):
                f[i][j] = f[i - 1][j] + g[i - 1][j - 1]
                f[i][j] %= mod

                g[i][j] = g[i - 1][j] + f[i][j]
                g[i][j] %= mod

        return g[-1][-1]

        \'\'\'
        f[i][j] = f[j - 1][j - 1] * (i - j + 1) +
                  f[j][j - 1] * (i - j) +
                  ... +
                  f[i - 1][j - 1]

                = f[j - 1][j - 1] +
                  f[j][j - 1] + f[j - 1][j - 1] +
                  ... +
                  f[i - 1][j - 1] + ... + f[j - 1][j - 1]
                
        g[i][j] = f[i][j] + ... + f[j][j]
        g[i][j] = g[i - 1][j] + f[i][j]

        f[i][j] = g[j - 1][j - 1] + g[j][j - 1] + ... + g[i - 1][j - 1]
        f[i][j] = f[i - 1][j] + g[i - 1][j - 1]
        \'\'\'
''',
    call='Solution().numberOfSets(5, 3)',
    expect=7,
    views=[
        dict(type='table', var='f', label='f[i][j]：前 i+1 个点放 j 条线段，最后一条右端恰为 i', color=_c('f'), rows=lambda S: list(range(len(S['f']))), cols=lambda S: list(range(len(S['f'][0]))), h=250, cell=80),
        dict(type='table', var='g', label='g[i][j]：f[j][j] + … + f[i][j]（沿 i 的前缀和）', color=_c('g'), rows=lambda S: list(range(len(S['g']))), cols=lambda S: list(range(len(S['g'][0]))), h=250, cell=80),
        dict(type='text', h=80, size=28, fn=_txt),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'f = [[0]': '`f[i][j]`：前 `i+1` 个点（0 ~ i）放 `j` 条线段，且最后一条线段右端恰好是 `i`',
        'g = [[0]': '`g[i][j]`：`f[i][j] + f[i-1][j] + … + f[j][j]`，把转移里的求和变成前缀和',
        'mod = ': '结果对 `{mod}` 取模',
        'for i in range(1, n)': lambda S, B, r: ('每个右端 `i` 都枚举完了' if B.get('i') == S.i
                                                 else f'枚举最后一条线段的右端 `i = {S.i}`'),
        'f[i][1] = i': '只有 1 条线段：右端是 `i`，左端在 `0 ~ {i - 1}` 任选 → `f[{i}][1] = {i}`',
        'g[i][1] =': '`g[{i}][1] = g[{i - 1}][1] + {i}` = `{g[i][1]}`',
        'for j in range(2': lambda S, B, r: (f'`i = {S.i}`：不够放 2 条线段（至少要 3 个点），跳过' if min(S.i, S.k) < 2
                                             else '`i` 对应的 `j` 都算完了' if B.get('j') == S.j and S.f[S.i][S.j] != 0
                                             else f'线段数 `j` 从 2 到 `min(i, k) = {min(S.i, S.k)}`（`j` 条线段至少要 `j+1` 个点），现在 `j = {S.j}`'),
        'f[i][j] = f[i - 1][j]': '`f[{i}][{j}] = f[{i - 1}][{j}] + g[{i - 1}][{j - 1}]` = `{f[i][j]}`：去掉枚举 `cut_pos` 的求和',
        'f[i][j] %= mod': '取模 → `f[{i}][{j}] = {f[i][j]}`',
        'g[i][j] = g[i - 1][j] + f[i][j]': '`g[{i}][{j}] = g[{i - 1}][{j}] + f[{i}][{j}]` = `{g[i][j]}`',
        'g[i][j] %= mod': '取模 → `g[{i}][{j}] = {g[i][j]}`',
        'return g[-1][-1]': '`g[n−1][k]` = 所有右端 `<= n−1` 的方案之和 → 答案 =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='先写 O(nk^2) 的 DP，再用前缀和 g 把转移压成 O(1)',
        complexity='时间 `O(nk)`，空间 `O(nk)`',
        problem=['`n` 个点在 `x = 0 … n−1`，选恰好 `k` 条不重叠、至少覆盖两个点的线段（端点整数，可重合）',
                 '求方案数，对 `10^9+7` 取模',
                 '示例：`n = 5, k = 3` → `7`'],
        quote='令f[i][j]表示0到i这些点用j条线段去覆盖，且最后一条线段覆盖住了i这个点的情况总数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：最后一条线段右端固定为 `i`；`j = 1` 时左端任选，共 `i` 种',
              '一般情况：枚举前 `j-1` 条的右边界 `cut_pos`，再乘 `(i - cut_pos)`，`O(n^2 k)` 太慢',
              '展开后发现是连续和 → 引入 `g[i][j] = f[i][j] + … + f[j][j]`',
              '于是 `f[i][j] = f[i-1][j] + g[i-1][j-1]`，`g[i][j] = g[i-1][j] + f[i][j]`，降到 `O(nk)`'],
        summary=['时间 `O(nk)`，空间 `O(nk)`',
                 '`j` 条线段至少占 `j+1` 个点，所以 `j` 的上界是 `min(i, k)`',
                 '`f[i][1] = i`、`g[i][1]` 是前缀和，要单独初始化',
                 '答案是 `g[-1][-1]`（所有右端的和），不是 `f[-1][-1]`',
                 '对比灵神：灵神用隔板法直接得到 `C(n+k-1, 2k)`，`O(1)`；yiduobo 走 DP 路线'],
    ),
)
