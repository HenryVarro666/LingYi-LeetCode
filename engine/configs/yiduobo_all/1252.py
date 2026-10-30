M, N = 3, 4
IND = [[0, 1], [1, 2], [2, 1]]


def _grid(S):
    m, n = S['m'], S['n']
    r, c = S.get('r_cnt'), S.get('c_cnt')
    if r is None or c is None:
        return [[0] * n for _ in range(m)]
    # 每个单元格 = 所在行被操作次数 + 所在列被操作次数（只有 r_cnt / c_cnt 已统计完成的部分才算数）
    return [[r[i] + c[j] for j in range(n)] for i in range(m)]


def _gcolor(S, i, j, v):
    return 'orange' if v % 2 == 1 else None


CONFIG = dict(
    num=1252, title='奇数值单元格的数目', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='统计行列操作次数 + 容斥',
    code='''
class Solution(object):
    def oddCells(self, m, n, indices):

        r_cnt = [0] * m
        c_cnt = [0] * n
        for x, y in indices:
            r_cnt[x] += 1
            c_cnt[y] += 1
        
        r = c = 0
        for index in range(m):
            if r_cnt[index] % 2 == 1:
                r += 1
        
        for index in range(n):
            if c_cnt[index] % 2 == 1:
                c += 1
        
        return r * n + c * m - 2 * r * c
''',
    call=f'Solution().oddCells({M}, {N}, {IND!r})',
    expect=9,
    views=[
        dict(type='array', var='r_cnt', label='r_cnt（每一行被操作的次数）', cell=96, h=190,
             color=lambda S, i, v: 'orange' if v % 2 == 1 else None),
        dict(type='array', var='c_cnt', label='c_cnt（每一列被操作的次数）', cell=96, h=190,
             color=lambda S, i, v: 'orange' if v % 2 == 1 else None),
        dict(type='grid', var=_grid, label='最终矩阵（每格 = 行次数 + 列次数；橙 = 奇数）', cell=80, h=330,
             color=_gcolor),
        dict(type='text', h=90, fn=lambda S: f"`r = {S['r']}` 行奇数，`c = {S['c']}` 列奇数" if 'r' in S and 'c' in S else ''),
    ],
    watch=['r', 'c', ('r_cnt', 'r_cnt', 'blue'), ('c_cnt', 'c_cnt', 'pink')],
    captions={
        'r_cnt = [0]': '`r_cnt[x]`：第 `x` 行被操作了几次，共 `m = {m}` 行',
        'c_cnt = [0]': '`c_cnt[y]`：第 `y` 列被操作了几次，共 `n = {n}` 列',
        'for x, y in indices': lambda S, B, r: '所有操作读完，行列次数统计完毕' if B.get('x') == S.x and B.get('y') == S.y else f'读一条操作 `[{S.x}, {S.y}]`：第 {S.x} 行、第 {S.y} 列各加 1',
        'r_cnt[x] += 1': '第 `{x}` 行被操作 → `r_cnt = {r_cnt}`',
        'c_cnt[y] += 1': '第 `{y}` 列被操作 → `c_cnt = {c_cnt}`',
        'r = c = 0': '`r`：操作次数为奇数的行数；`c`：为奇数的列数',
        'for index in range(m)': lambda S, B, r: '所有行数完了' if B.get('index') == S.index == S.m - 1 else f'数行：看第 `{S.index}` 行',
        'if r_cnt[index] % 2 == 1': lambda S, B, r: (f'`r_cnt[{S.index}] = {S.r_cnt[S.index]}` 是奇数 → 这一行整行是奇数' if S.r_cnt[S.index] % 2 == 1 else f'`r_cnt[{S.index}] = {S.r_cnt[S.index]}` 是偶数 → 这一行整行是偶数，不算'),
        'r += 1': '奇数行又多一行：`r = {r}`',
        'for index in range(n)': lambda S, B, r: '所有列数完了' if B.get('index') == S.index == S.n - 1 else f'数列：看第 `{S.index}` 列',
        'if c_cnt[index] % 2 == 1': lambda S, B, r: (f'`c_cnt[{S.index}] = {S.c_cnt[S.index]}` 是奇数 → 这一列整列是奇数' if S.c_cnt[S.index] % 2 == 1 else f'`c_cnt[{S.index}] = {S.c_cnt[S.index]}` 是偶数 → 不算'),
        'c += 1': '奇数列又多一列：`c = {c}`',
        'return r * n': '`r·n + c·m − 2·r·c` = `{r}×{n} + {c}×{m} − 2×{r}×{c}` = =={ret}==：交叉的 `r·c` 格是偶数，要扣两次',
    },
    cards=dict(
        one_liner='不用造矩阵：只数奇数行、奇数列，再容斥掉交叉格',
        complexity='时间 `O(m + n + 操作数)`，空间 `O(m + n)`',
        problem=['`m×n` 的矩阵初始全 0，每条操作 `[ri, ci]` 让第 `ri` 行、第 `ci` 列的所有格子各加 1',
                 '做完所有操作后，问矩阵里有多少个奇数',
                 f'本视频：`m={M}, n={N}`，操作 `{IND}` → `9`'],
        quote='因此我们可以统计对每一行和每一列最终的操作次数，分别记为r_cnt和c_cnt。',
        quote_src='—— yiduobo 题解原文',
        idea=['一行被操作奇数次，整行都是奇数：`r` 个奇数行共 `r × n` 格；同理奇数列 `c × m` 格',
              '行列交叉的 `r × c` 格被统计了两次，实际行加奇数次再列加奇数次 = ==偶数==',
              '所以要把这些格子减掉两次：`r·n + c·m − 2·r·c`'],
        summary=['时间 `O(m + n + len(indices))`，空间 `O(m + n)`',
                 '==交叉格要减 2 次==：它们先被算进行、又被算进列，但其实是偶数',
                 '只有 `r_cnt[x]` 的奇偶性有用，所以也可以用异或代替计数',
                 '原文无 Python 2 专有写法，代码照搬'],
    ),
)
