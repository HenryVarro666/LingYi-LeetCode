G = [[1, 0, 0, 0, 1], [0, 1, 1, 1, 0], [1, 0, 0, 1, 0]]


def _cells(S):
    """(cells, color) currently being examined"""
    if 'm' not in S or 'n' not in S:
        return [], None
    m, n, L = S['m'], S['n'], S['_line']
    if L <= 9 and 'i' in S and 'j' in S:
        i, j = S['i'], S['j']
        return [(i, j), (i, n - 1 - j), (m - 1 - i, j), (m - 1 - i, n - 1 - j)], 'blue'
    if L in (11, 13):
        return [(m // 2, n // 2)], 'pink'
    if 16 <= L <= 23 and 'j' in S:
        return [(m // 2, S['j']), (m // 2, n - 1 - S['j'])], 'orange'
    if L >= 24 and 'i' in S:
        return [(S['i'], n // 2), (m - 1 - S['i'], n // 2)], 'orange'
    return [], None


def _gc(S, i, j, v):
    cells, c = _cells(S)
    return c if (i, j) in cells else None


def _txt(S):
    if 'm' not in S:
        return '行列都回文：四个镜像格必须相同；中间行/列另算'
    cells, c = _cells(S)
    vals = [S['a'][i][j] for i, j in cells]
    if c == 'blue':
        return f"四个镜像格 `{vals}`：全变 0 要 {sum(vals)} 次，全变 1 要 {4 - sum(vals)} 次"
    if c == 'pink':
        return f"正中央格 `{vals[0]}`：必须是 0（否则 1 的个数是奇数）"
    if c == 'orange':
        return f"中间{'行' if S['_line'] < 24 else '列'}镜像对 `{vals}`：{'相同' if vals[0] == vals[1] else '不同，必须翻一个'}"
    return f"答案累计 `ans = {S.get('ans', 0)}`；中间行列：diff = {S.get('diff', '-')}，cnt1 = {S.get('cnt1', '-')}"


CONFIG = dict(
    num=3240, title='最少翻转次数使二进制矩阵回文 II', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='四格一组 · 中间行列分类讨论',
    tags=['灵神题单', '思维题', '难度分 2080'],
    code='''
class Solution:
    def minFlips(self, a: List[List[int]]) -> int:
        m, n = len(a), len(a[0])
        ans = 0
        for i in range(m // 2):
            row, row2 = a[i], a[-1 - i]
            for j in range(n // 2):
                cnt1 = row[j] + row[-1 - j] + row2[j] + row2[-1 - j]
                ans += min(cnt1, 4 - cnt1)  # 全为 1 或全为 0

        if m % 2 and n % 2:
            # 正中间的数必须是 0
            ans += a[m // 2][n // 2]

        diff = cnt1 = 0
        if m % 2:
            # 统计正中间这一排
            row = a[m // 2]
            for j in range(n // 2):
                if row[j] != row[-1 - j]:
                    diff += 1
                else:
                    cnt1 += row[j] * 2
        if n % 2:
            # 统计正中间这一列
            for i in range(m // 2):
                if a[i][n // 2] != a[-1 - i][n // 2]:
                    diff += 1
                else:
                    cnt1 += a[i][n // 2] * 2

        return ans + (diff if diff else cnt1 % 4)
''',
    call=f'Solution().minFlips({G})',
    expect=5,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='grid', var='a', label='a（蓝 = 四个镜像格，粉 = 正中央，橙 = 中间行/列的镜像对）', cell=110, color=_gc, h=420),
    ],
    watch=[('ans', 'ans', 'green'), ('cnt1', 'cnt1', 'blue'), ('diff', 'diff', 'pink')],
    captions={
        'm, n = len(a)': '`{m} × {n}` 的矩阵。行列都回文 → 每个格子和它的三个镜像格必须相同',
        'ans = 0': '`ans` 累计翻转次数',
        5: '只枚举左上角 `i < m // 2`（上半部分），镜像格是 `m-1-i`',
        'row, row2 = ': '`row = a[{i}]`，`row2 = a[{m - 1 - i}]`：上下镜像的两行',
        7: '只枚举左半 `j < n // 2`，镜像列是 `n-1-j`',
        'cnt1 = row[j]': '四个镜像格 `({i},{j})({i},{n - 1 - j})({m - 1 - i},{j})({m - 1 - i},{n - 1 - j})` 里有 `cnt1 = {cnt1}` 个 1',
        'ans += min(cnt1, 4 - cnt1)': '全变 0 要 `{cnt1}` 次，全变 1 要 `{4 - cnt1}` 次 → 取小 `{min(cnt1, 4 - cnt1)}`，`ans = {ans}`',
        'if m % 2 and n % 2': lambda S, B, r: ('`m`、`n` 都是奇数：有==正中央格==，四格一组之外还剩它' if (B.m % 2 and B.n % 2) else '没有正中央格'),
        'ans += a[m // 2][n // 2]': '其余格子两两成对，1 的个数已是偶数；中央格若是 1 则总数为奇数 → ==中央必须是 0==，`ans = {ans}`',
        'diff = cnt1 = 0': '`diff` 数镜像不同的==对数==，`cnt1` 数镜像相同的 ==1 的个数==（重新计数，只管中间行/列）',
        'if m % 2:': '`m` 是奇数 → 有正中间一排，要单独处理',
        'row = a[m // 2]': '正中间一排 `row = {row}`',
        19: '逐对检查中间这一排：`j` 从 0 到 `n // 2 - 1`，镜像是 `-1 - j`',
        26: '逐对检查中间这一列：`i` 从 0 到 `m // 2 - 1`，镜像是 `-1 - i`',
        'if row[j] != row[-1 - j]': lambda S, B, r: (f'`row[{B.j}] = {B.row[B.j]}` 与镜像 `row[{B.n - 1 - B.j}] = {B.row[-1 - B.j]}`：' + ('==不同，必须翻一个，diff +1==' if B.row[B.j] != B.row[-1 - B.j] else '相同')),
        'diff += 1': '`diff = {diff}`：这一对一个 0 一个 1，至少翻 1 次',
        'cnt1 += row[j] * 2': '这一对相同（值 `{row[j]}`）：1 的个数 `cnt1 += 2 × {row[j]}` → `{cnt1}`',
        'if n % 2:': '`n` 是奇数 → 有正中间一列，也要处理',
        'if a[i][n // 2] != a[-1 - i][n // 2]': lambda S, B, r: (f'`a[{B.i}][{B.n // 2}] = {B.a[B.i][B.n // 2]}` 与镜像 `{B.a[-1 - B.i][B.n // 2]}`：' + ('==不同，diff +1==' if B.a[B.i][B.n // 2] != B.a[-1 - B.i][B.n // 2] else '相同')),
        'cnt1 += a[i][n // 2] * 2': '这一对相同，`cnt1 = {cnt1}`',
        'return ans +': '`diff = {diff}`、`cnt1 = {cnt1}`：{"diff > 0 → 翻其中一对成 11，其余成 00，凑出 4 的倍数，额外加 diff" if diff else "diff = 0 → 只能把 cnt1 个 1 里的 cnt1 % 4 个变 0，额外加 " + str(cnt1 % 4)}。==答案 {ans + (diff if diff else cnt1 % 4)}==',
    },
    cards=dict(
        one_liner='四格一组翻成同色；中间行列再凑 4 的倍数',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`m × n` 的 0/1 矩阵，可翻转任意格子',
                 '要求==所有行和列都回文==，且 1 的个数是 4 的倍数，求最少翻转次数',
                 '示例：`[[1,0,0],[0,1,0],[0,0,1]]` → `3`；本视频用 3×5 的矩阵 → `5`'],
        quote='中间的格子需要翻转成回文的，且 1 的数目需要能被 4 整除。如果 diff > 0，额外把 diff 加入答案；如果 diff = 0，额外把 cnt1 mod 4 加入答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['行列都回文 → `a[i][j]`、`a[i][n-1-j]`、`a[m-1-i][j]`、`a[m-1-i][n-1-j]` 必须相同',
              '四个一组，全变 0 要 `cnt1` 次，全变 1 要 `4-cnt1` 次，取小；这部分自带 4 的倍数',
              '剩下中间行/列：镜像不同的 `diff` 对必翻一个；`diff = 0` 时再用 `cnt1 % 4` 修正'],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '易错：正中央格若是 1 必须翻成 0（m、n 都是奇数时）',
                 '`diff` 数的是数对，`cnt1` 数的是 1 的个数（所以每对乘 2）',
                 '`diff > 0` 时，让某一对翻成 11 就能调整 4 的倍数，不用额外代价',
                 '第一次的 `cnt1` 在这里被重新赋值为 0，后面只统计中间行/列'],
    ),
)
