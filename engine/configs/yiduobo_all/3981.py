W1, W2, TG = 'ab', 'ab', 'ab'
ROWS = ['空'] + [f'{c}{k}' for k, c in enumerate(W1, 1)]
COLS = ['空'] + [f'{c}{k}' for k, c in enumerate(W2, 1)]


def _f_col(S, a, b, v):
    ln, i, j = S.get('_line', 0), S.get('i'), S.get('j')
    if i is None or j is None:
        return None
    if ln in (33, 40, 47) and (a, b) == (i, j):
        return 'yellow'
    if ln == 31 and a == i:
        return 'cyan'
    if ln == 38 and b == j:
        return 'cyan'
    return None


def _s1_col(S, a, b, v):
    ln, i, j = S.get('_line', 0), S.get('i'), S.get('j')
    if i is None or j is None:
        return None
    if ln == 16 and (a, b) == (0, j):
        return 'yellow'
    if ln == 18:
        if (a, b) == (i, j):
            return 'yellow'
        if (a, b) in ((i - 1, j),):
            return 'blue'
    if ln == 33 and (a, b) == (i - 1, j):
        return 'blue'
    return None


def _s2_col(S, a, b, v):
    ln, i, j = S.get('_line', 0), S.get('i'), S.get('j')
    if i is None or j is None:
        return None
    if ln == 23 and (a, b) == (i, 0):
        return 'yellow'
    if ln == 25:
        if (a, b) == (i, j):
            return 'yellow'
        if (a, b) == (i, j - 1):
            return 'blue'
    if ln == 40 and (a, b) == (i, j - 1):
        return 'blue'
    return None


CONFIG = dict(
    num=3981, title='统计从两个字符串形成目标字符串的不同方案数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='「必须用」状态 + 二维前缀和',
    tags=['灵神题单·动态规划', '难度分 2128'],
    code='''
class Solution(object):
    def interleaveCharacters(self, word1, word2, target):

        len1 = len(word1)
        len2 = len(word2)
        n = len(target)

        f = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        s1 = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        s2 = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        f[0][0] = 1
        mod = 10 ** 9 + 7
        rnd = 1
        for c in target:
            for j in range(len2 + 1):
                s1[0][j] = f[0][j]
                for i in range(1, len1):
                    s1[i][j] = s1[i - 1][j] + f[i][j]
                    if s1[i][j] >= mod:
                        s1[i][j] -= mod

            for i in range(len1 + 1):
                s2[i][0] = f[i][0]
                for j in range(1, len2):
                    s2[i][j] = s2[i][j - 1] + f[i][j]
                    if s2[i][j] >= mod:
                        s2[i][j] -= mod

            f = [[0] * (len2 + 1) for _ in range(len1 + 1)]
            for i in range(1, len1 + 1):
                if word1[i - 1] == c:
                    for j in range(len2 + 1):
                        f[i][j] += s1[i - 1][j]
                        if f[i][j] >= mod:
                            f[i][j] -= mod

            for j in range(1, len2 + 1):
                if word2[j - 1] == c:
                    for i in range(len1 + 1):
                        f[i][j] += s2[i][j - 1]
                        if f[i][j] >= mod:
                            f[i][j] -= mod

        res = 0
        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                res += f[i][j]
                if res >= mod:
                    res -= mod
        return res
''',
    call=f'Solution().interleaveCharacters({W1!r}, {W2!r}, {TG!r})',
    expect=2,
    skip=[4, 5, 6, 8, 9, 10, 12, 13, 15, 16, 17, 19, 23, 31, 38, 20, 22, 24, 26, 27, 30, 32, 34, 35, 37, 39, 41, 42, 45, 46, 48, 49],
    max_steps=100,
    views=[
        dict(type='string', var='target', label='target（蓝 = 当前要匹配的字符 c）', h=110, cell=70,
             color=lambda S, k, v: 'blue' if S.get('c') is not None and S.get('_line', 0) < 44 and v == S['c'] else None),
        dict(type='table', var='f', label='f[i][j]：word1[i] 和 word2[j] 都是「最后用到的」时的方案数（空 = 还没用）', h=190, cell=48,
             rows=ROWS, cols=COLS, color=_f_col),
        dict(type='table', var='s1', label='s1：f 沿 word1 方向的前缀和（s1[i][j] = f[0..i][j] 之和）', h=190, cell=48,
             rows=ROWS, cols=COLS, color=_s1_col),
        dict(type='table', var='s2', label='s2：f 沿 word2 方向的前缀和（s2[i][j] = f[i][0..j] 之和）', h=190, cell=48,
             rows=ROWS, cols=COLS, color=_s2_col),
    ],
    watch=[('c', 'c', 'blue'), ('i', 'i', 'cyan'), ('j', 'j', 'pink'), ('res', 'res', 'green')],
    captions={
        11: '`f[0][0] = 1`：还没匹配任何字符，两个单词都还没用过（空）',
        14: lambda S, B, r: (f'`c = {S.c}`：这一轮用 `word1` 或 `word2` 的某个字符去匹配它' if S.get('c') is not None and S.get('c') != B.get('c') or B.get('c') is None
                             else '`target` 的字符都匹配完了，开始汇总答案'),
        16: '`s1[0][{j}] = f[0][{j}]` = {s1[0][j]}：先算 word1 方向的前缀和，打头一格',
        18: '`s1[{i}][{j}] = s1[{i-1}][{j}] + f[{i}][{j}]` = {s1[i][j]}：沿 word1 方向的前缀和 `f[0..{i}][{j}]`',
        23: '`s2[{i}][0] = f[{i}][0]` = {s2[i][0]}：再算 word2 方向的前缀和，打头一格',
        25: '`s2[{i}][{j}] = s2[{i}][{j-1}] + f[{i}][{j}]` = {s2[i][j]}：沿 word2 方向的前缀和 `f[{i}][0..{j}]`',
        29: '`f` 清零重算：新的 `f` 只靠上一轮的 `s1`、`s2` 转移，不会重复',
        31: lambda S, B, r: (f'`word1[{S.i-1}] = {S.word1[S.i-1]}` 等于 `c = {S.c}` → 它可以匹配这个字符' if S.word1[S.i-1] == S.c
                             else f'`word1[{S.i-1}] = {S.word1[S.i-1]}` 不等于 `c = {S.c}` → 这一行保持 0'),
        33: '`word1[{i-1}] = c = {c}` 匹配成功：`f[{i}][{j}] += s1[{i-1}][{j}]`，上一个用的 word1 位置可以是 `0..{i-1}` 任意一个（前缀和）→ {f[i][j]}',
        38: lambda S, B, r: (f'`word2[{S.j-1}] = {S.word2[S.j-1]}` 等于 `c = {S.c}` → 它可以匹配这个字符' if S.word2[S.j-1] == S.c
                             else f'`word2[{S.j-1}] = {S.word2[S.j-1]}` 不等于 `c = {S.c}` → 这一列保持 0'),
        40: '`word2[{j-1}] = c = {c}` 匹配成功：`f[{i}][{j}] += s2[{i}][{j-1}]`，上一个用的 word2 位置是 `0..{j-1}` 任意一个 → {f[i][j]}',
        44: '汇总：两个单词都至少用到一个，所以只累加 `i ≥ 1` 且 `j ≥ 1` 的格子',
        47: '`res += f[{i}][{j}]` → =={res}==',
        50: '所有「两边都用过」的方案数之和 = =={ret}==',
    },
    cards=dict(
        one_liner='换成「末尾一定被用」的状态，转移就没有重复，再用前缀和加速',
        complexity='时间 `O(n·m1·m2)`，空间 `O(m1·m2)`',
        problem=['从 `word1`、`word2` 各选递增下标的字符，拼成 `target`',
                 '每个字符取自其中一个单词；两个单词==至少各选一个==',
                 '示例：`word1="abc", word2="bac", target="abc"` → `5`',
                 '本视频：`"ab"`、`"ab"`、`"ab"` → `2`'],
        quote='我不太想处理这些重复的逻辑，于是选用了更复杂的状态表示：f[i][j][k]表示……word1的第j个字符以及word2的第k个字符必须被使用的方案数。',
        quote_src='—— yiduobo 题解原文',
        idea=['常规「前缀」状态会让后继包含前驱，两边都不选时出现重复计算',
              '所以让 `f[i][j]` 里 word1[i]、word2[j] ==都是最后用到的==，不同状态必有字符差异，不重复',
              '转移要枚举上一个用到的位置：`f[i][j] += f[0..i-1][j]`，这是前缀和 `s1`；另一边同理 `s2`',
              '`f` 由上一轮的 `s1/s2` 得到，`s1/s2` 由 `f` 得到，互相迭代，省掉 target 这一维'],
        summary=['时间 `O(n·m1·m2)`，空间 `O(m1·m2)`',
                 '易错：`f` 里 `i`、`j` 为 0 表示「那个单词还没用」，初始只有 `f[0][0] = 1`',
                 '易错：答案只累加 `i ≥ 1` 且 `j ≥ 1` 的格子（两边至少各用一个）',
                 '原文已是 Python 3 可运行写法，未作修改',
                 '对比灵神：灵神靠容斥合并「不选」的情况；yiduobo 换状态避免重复，再用前缀和'],
    ),
)
