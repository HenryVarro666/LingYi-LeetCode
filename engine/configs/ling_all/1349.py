SEATS = [['.', '#'], ['.', '.'], ['.', '#']]
M, NC = len(SEATS), len(SEATS[0])
A = [sum((c == '.') << j for j, c in enumerate(r)) for r in SEATS]


def b(x):
    return format(x, f'0{NC}b')


def _cell(S, i, j, v):
    line, ci, cj = S.get('_line'), S.get('i'), S.get('j')
    if line in (7, 8, 9) and cj is not None and i == 0:
        lb = cj & -cj
        if j == cj:
            return 'yellow'
        if line == 9 and j == (cj & ~(lb * 3)):
            return 'blue'
        return None
    if ci is not None and line is not None and 13 <= line <= 21:
        if (i, j) == (ci, cj) and line != 21:
            return 'yellow'
        if line in (13, 21) and (i, j) == (ci - 1, A[ci - 1]):
            return 'blue'
        if line == 21 and (i, j) == (ci, 0):
            return 'yellow'
        if line in (18, 19) and 't' in S and (i, j) == (ci - 1, S['t']):
            return 'blue'
        if line in (18, 19) and 's' in S and (i, j) == (0, S['s']):
            return 'cyan'
    return None


def _seats(S):
    return ' / '.join(f"第 {k} 排 `{''.join(r)}` → `a[{k}] = {b(A[k])}`" for k, r in enumerate(SEATS))


def _state(S):
    line, i = S.get('_line'), S.get('i')
    if i is None or line is None or line < 10:
        return '二进制从右往左读：第 k 位 = 第 k 把椅子；`1` = 可坐 / 坐了学生'
    if line in (21,):
        return f'第 {i} 排没有人时：`f[{i}][0]`'
    j = S.get('j')
    out = f'第 {i} 排：可用椅子 `a[{i}] = {b(A[i])}`，现在考虑 `j = {b(j)}`'
    if 's' in S and line >= 14 and line <= 19:
        s = S['s']
        out += f'；这排实际坐 `s = {b(s)}`'
        if 't' in S and line >= 17:
            out += f'；上排还能坐 `t = {b(S["t"])}`'
    return out


CONFIG = dict(
    num=1349, title='参加考试的最大学生数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='状压 DP · 枚举子集的子集（递推）',
    tags=['图论算法', '难度分 2386'],
    code='''
class Solution:
    def maxStudents(self, seats: List[List[str]]) -> int:
        m, n = len(seats), len(seats[0])
        # a[i] 是第 i 排可用椅子的下标集合
        a = [sum((c == '.') << j for j, c in enumerate(s)) for s in seats]
        f = [[0] * (1 << n) for _ in range(m)]
        for j in range(1, 1 << n):
            lb = j & -j
            f[0][j] = f[0][j & ~(lb * 3)] + 1
        for i in range(1, m):
            j = a[i]
            while j:  # 枚举 a[i] 的子集 j
                f[i][j] = f[i - 1][a[i - 1]]  # 第 i 排空着
                s = j
                while s:  # 枚举 j 的子集 s
                    if (s & (s >> 1)) == 0:  # s 没有连续的 1
                        t = a[i - 1] & ~(s << 1 | s >> 1)  # 去掉不能坐人的位置
                        f[i][j] = max(f[i][j], f[i - 1][t] + f[0][s])
                    s = (s - 1) & j
                j = (j - 1) & a[i]
            f[i][0] = f[i - 1][a[i - 1]]
        return f[-1][a[-1]]
''',
    call=f'Solution().maxStudents({SEATS!r})',
    expect=3,
    max_steps=75,
    skip=['lb = j & -j', 's = j', 's = (s - 1) & j', 'j = (j - 1) & a[i]', 'j = a[i]'],
    views=[
        dict(type='text', fn=_seats, size=21, h=60),
        dict(type='table', var='f', label='f[i][j]：第 i 排可用椅子为 j 时，前 i 排最多学生数（黄 = 正在算，蓝 = 依赖，青 = f[0][s]）', h=250, cell=84,
             rows=lambda S: [f'排{k}' for k in range(M)], cols=lambda S: [b(k) for k in range(1 << NC)], color=_cell),
        dict(type='text', fn=_state, size=22, h=90),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'yellow'), ('s', 's', 'pink'), ('t', 't', 'cyan')],
    captions={
        'm, n = len': '`m = {m}` 排，`n = {n}` 把椅子/排',
        'a = [sum': '`a[i]` 用二进制记第 `i` 排哪些椅子能坐：{[format(x, "0" + str(n) + "b") for x in a]}（从右往左读）',
        'f = [[0]': '`f[i][j]`：第 `i` 排可用椅子为 `j` 时，前 `i` 排的最大学生数',
        'for j in range(1, 1 << n)': lambda S, B, r: (('第 0 排算完（每个 `j` 都从最左可用椅子坐起，隔一把再坐）' if B.get('j') == S.get('j') else f'第 0 排：可用椅子 `j = {S.j:0{S.n}b}`') if 'j' in S else '第 0 排：从 `j = 1` 到 `2^n-1` 枚举所有可用椅子集合'),
        'f[0][j] =': '最左的可用椅子 `lb = j & -j` 坐人，`lb*3` 去掉它和相邻的一把 → `f[0][{j:0{n}b}] = {f[0][j]}`',
        'for i in range(1, m)': lambda S, B, r: (f'开始处理第 `{S.i}` 排：它只和第 `{S.i - 1}` 排有关（看不到前后，只看左上右上）' if 'i' in S and S.get('i') != B.get('i') else '所有排处理完'),
        'while j': lambda S, B, r: (f'`j = {S.j:0{S.n}b}`（`a[i]` 的一个子集，用 `(j-1) & a[i]` 依次枚举）→ 算这种可用椅子集合' if S.j else '`j` 减到 0：`a[i]` 的子集都枚举完了'),
        'f[i][j] = f[i - 1][a[i - 1]]': '先枚举第 `{i}` 排空着：答案至少是上一排的最优 `f[{i - 1}][{a[i - 1]:0{n}b}]` = {f[i][j]}',
        'while s': lambda S, B, r: (f'`s = {S.s:0{S.n}b}`（`j` 的一个子集，用 `(s-1) & j` 依次枚举）→ 检查这种坐法' if S.s else '`j` 的子集 `s` 都试完了'),
        'if (s & (s >> 1)) == 0': lambda S, B, r: (f'`s = {S.s:0{S.n}b}` 没有相邻的 1：同排不挨着坐 → 合法' if (S.s & (S.s >> 1)) == 0 else f'`s = {S.s:0{S.n}b}` 有相邻的 1：同排相邻会作弊 → 跳过'),
        't = a[i - 1]': '上一排：去掉左上、右上被占的椅子 → `t = {t:0{n}b}`',
        'f[i][j] = max(': '`f[{i}][{j:0{n}b}] = max(旧值, f[{i - 1}][{t:0{n}b}] + f[0][{s:0{n}b}])` → =={f[i][j]}==（`f[0][s]` 就是 `s` 里的学生数）',
        'f[i][0] = ': '没有可用椅子（`j = 0`）：只能继承上一排 → `f[{i}][0] = {f[i][0]}`',
        'return f[-1][a[-1]]': '最后一排椅子全部可用时的最优 `f[{m - 1}][{a[-1]:0{n}b}]` = =={ret}==',
    },
    cards=dict(
        one_liner='一排一排考虑：这排坐哪些人，只由上一排决定',
        complexity='时间 `O(m·3^n)`，空间 `O(m·2^n)`',
        problem=['教室 `m×n` 座位，`.` 好座位、`#` 坏座位',
                 '学生能看到左、右、左上、右上的答卷，不能同时坐在互相能看见的位置',
                 '求最多容纳多少学生。示例：`[[.,#],[.,.],[.,#]]` → `3`'],
        quote='定义 dfs(i,j) 表示在第 i 排的座位状态为 j 的情况下，前 i 排的最大学生数。……s 是 j 的子集，且 s 的二进制数中不能有两个 1 是相邻的。',
        quote_src='—— 灵茶山艾府题解（二、递归怎么写）',
        idea=['`a[i]`：第 `i` 排可用椅子的二进制集合；`f[i][j]`：可用椅子为 `j` 时前 `i` 排的最大人数',
              '枚举这排坐的 `s ⊆ j`：同排不相邻（`s & (s>>1) == 0`）',
              '上一排可坐的位置 `t = a[i-1]` 去掉 `s<<1 | s>>1`（左上右上）→ `f[i-1][t] + |s|`'],
        summary=['时间 `O(m·3^n)`：每排枚举子集的子集，总数 `3^n`',
                 '易错：`j` 必须是 `a[i]` 的子集，所以用 `(j-1) & a[i]` 枚举',
                 '`|s|` 直接用 `f[0][s]`：`s` 没有相邻 1，它恰好是 `s` 能坐的人数',
                 '另有记忆化搜索（`@cache`）和「选或不选」写法，后者 `O(mn·1.618^n)` 更快'],
    ),
)
