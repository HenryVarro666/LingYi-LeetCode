def _txt(S):
    i, j = S.get('i'), S.get('j')
    num = S['num']
    if i is None or j is None or S.get('_line', 0) < 20 or 'f' not in S:
        return '`f[i][j]`：前 i 个字符，最后 j 个字符作为最后一个数的方案数'
    if S.get('_line') >= 33 and 'j' in S and S['_line'] >= 36:
        return '`s[i][j]` = `f[i][1] + … + f[i][j]` 的前缀和（模 mod），下一轮直接取用'
    return f'最后一个数 `num[{i - j}:{i}]` = {num[i - j:i]}；上一个数取更短时一定更小，累加 `s[{i - j}][·]`'


CONFIG = dict(
    num=1977, title='划分数字的方案数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='f[i][j] + 前缀和 + 最长公共前缀 g',
    tags=['灵神题单·动态规划', '灵神题单·字符串', '难度分 2817'],
    code='''
class Solution(object):
    def numberOfCombinations(self, num):
        n = len(num)
        f = [[0] * (n + 1) for _ in range(n + 1)]
        s = [[0] * (n + 1) for _ in range(n + 1)]
        g = [[0] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if num[i] == num[j]:
                    if i == n - 1 or j == n - 1:
                        g[i][j] = 1
                    else:
                        g[i][j] = g[i + 1][j + 1] + 1

        if num[0] == '0':
            return 0

        f[1][1] = 1
        s[1][1] = 1
        mod = 10 ** 9 + 7
        for i in range(2, n + 1):
            f[i][i] = 1
            for j in range(i - 1, 0, -1):
                if num[i - j] == '0':
                    f[i][j] = 0
                    continue
                if j - 1 <= i - j:
                    f[i][j] = s[i - j][j - 1]
                else:
                    f[i][j] = s[i - j][i - j]

                if i - j - j >= 0 and num[i - j - j] != '0' and (g[i - j][i - j - j] >= j or num[i - j + g[i - j][i - j - j]] > num[i - j - j + g[i - j][i - j - j]]):
                        f[i][j] += f[i - j][j]
                        if f[i][j] >= mod:
                            f[i][j] -= mod

            for j in range(1, i + 1):
                s[i][j] = s[i][j - 1] + f[i][j]
                if s[i][j] >= mod:
                    s[i][j] -= mod

        res = 0
        for i in range(n + 1):
            res += f[n][i]
            if res >= mod:
                res -= mod

        return res
''',
    call="Solution().numberOfCombinations('32071')",
    expect=3,
    views=[
        dict(type='string', var='num', label='num（i = 已考虑的前缀长度；最后一个数 = 末尾 j 个字符）', cell=80, h=180),
        dict(type='table', var='f', label='f[i][j]：前 i 个字符，最后 j 个字符为最后一个数的方案数', cell=48, h=290,
             rows=lambda S: list(range(len(S['f']))), cols=lambda S: list(range(len(S['f']))),
             color=lambda S, i, j, v: 'green' if v else None,
             cursors=[('i', 'j', 'yellow')]),
        dict(type='table', var='s', label='s[i][j] = f[i][1..j] 的前缀和', cell=48, h=290,
             rows=lambda S: list(range(len(S['s']))), cols=lambda S: list(range(len(S['s']))),
             color=lambda S, i, j, v: 'cyan' if v else None,
             cursors=[('i', 'j', 'yellow')]),
        dict(type='text', fn=_txt, size=24, h=70),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('res', 'res', 'green')],
    skip=['for i in range(n - 1, -1, -1)', 'for j in range(n - 1, -1, -1)', 'if num[i] == num[j]', 'if i == n - 1 or j == n - 1',
          'g[i][j] = 1', 'g[i][j] = g[i + 1][j + 1] + 1', 'else:', 'f = [[0]', 's = [[0]', 'g = [[0]', 'continue', 'mod = ',
          'res = 0', 'if f[i][j] >= mod', 'f[i][j] -= mod', 'if s[i][j] >= mod', 's[i][j] -= mod', 'if res >= mod', 'res -= mod', 'for j in range(1, i + 1)', 'f[i][j] = 0', 'if j - 1 <= i - j', 'for i in range(n + 1)'],
    max_steps=64,
    captions={
        'n = len(num)': '`n = {n}`；先建三张表：`f`、前缀和 `s`、最长公共前缀 `g`',
        'if num[0] == ': lambda S, B, r: ('开头是 `0`，不可能 → 返回 0' if S.num[0] == '0' else '开头不是 `0`；`g` 已算好（后缀 `i`、`j` 的最长公共前缀）'),
        'f[1][1] = 1': '只有 1 个字符：`f[1][1] = 1`，`s[1][1] = 1`',
        's[1][1] = 1': '前缀和 `s[1][1] = 1`',
        'for i in range(2, n + 1)': lambda S, B, r: (f'考虑前 `i = {S.i}` 个字符' if S.get('i') != B.get('i') else '所有前缀都算完'),
        'f[i][i] = 1': '整个前缀 `num[0:{i}]` 当作一个数：`f[{i}][{i}] = 1`',
        'for j in range(i - 1, 0, -1)': lambda S, B, r: (f'最后一个数取末尾 `j = {S.j}` 个字符：`num[{S.i - S.j}:{S.i}]` = {S.num[S.i - S.j:S.i]}'
                                                         if not (S.j == B.get('j') == 1) else '这个 i 的所有 j 都算完'),
        'if num[i - j] == ': lambda S, B, r: (f'`num[{S.i - S.j}] = 0` → 最后一个数有前导零 → `f[{S.i}][{S.j}] = 0`' if S.num[S.i - S.j] == '0'
                                              else f'`num[{S.i - S.j}] = {S.num[S.i - S.j]}`，没有前导零'),
                'if j - 1 <= i - j': lambda S, B, r: (f'前 `{S.i - S.j}` 个字符里上一个数最长 `{S.i - S.j}`；上一个数比最后一个数（长 {S.j}）短，一定更小'),
        'f[i][j] = s[i - j][j - 1]': '上一个数长度 `1..j-1`：全部可以 → `f[{i}][{j}] = s[{i-j}][{j-1}]` = =={f[i][j]}==',
        'f[i][j] = s[i - j][i - j]': '上一个数最长只有 `i-j`（不到 j）：全部可以 → `f[{i}][{j}] = s[{i-j}][{i-j}]` = =={f[i][j]}==',
        'if i - j - j >= 0': lambda S, B, r: ((f'上一个数也有 `{S.j}` 位：`num[{S.i - 2 * S.j}:{S.i - S.j}]` = {S.num[S.i - 2 * S.j:S.i - S.j]} 和 `num[{S.i - S.j}:{S.i}]` = {S.num[S.i - S.j:S.i]} 等长，要比大小'
                                                 if S.i - 2 * S.j >= 0 and S.num[S.i - 2 * S.j] != '0' else
                                                 '没有等长的上一个数（越界或前导零）→ 不加')
                                               ),
        'f[i][j] += f[i - j][j]': '等长且不更大：再加上 `f[{i-j}][{j}]` → `f[{i}][{j}]` = =={f[i][j]}==',
        'for j in range(1, i + 1)': lambda S, B, r: (f'算 `s[{S.i}][·]`：`f[{S.i}]` 的前缀和' if not (S.j == B.get('j') == S.i) else '前缀和算完'),
        's[i][j] = s[i][j - 1]': '算 `s[{i}][·]`：`s[{i}][{j}] = s[{i}][{j-1}] + f[{i}][{j}]` = =={s[i][j]}==',
        'res += f[n][i]': '`res += f[{n}][{i}]` → =={res}==',
        'return res': '所有 `f[n][·]` 之和：`{ret}` 种方案',
    },
    cards=dict(
        one_liner='末尾 j 位当最后一个数，用前缀和累加更短的，用 g 比较等长的',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['把数字串拆成若干个==非递减、无前导零==的正整数，求拆法数（对 `10^9+7` 取模）',
                 '`"327"` → `2`；`"094"` → `0`',
                 '本视频：`num = "32071"` → `3`'],
        quote='令f[i][j]表示字符串中的前i个字符，将最后j个字符划分成一个单独数字时可行的方案数。',
        quote_src='—— yiduobo 题解原文',
        idea=['先写 `O(n^3)`：`f[i][j]` 从 `f[i-j][k]` 转移；`k<j` 一定更小，`k>j` 一定更大，`k=j` 要比较',
              '`k<j` 的一整段求和 → 用前缀和 `s` 一步取出',
              '`k=j` 的比较 → 预处理最长公共前缀 `g`，`O(1)` 比较'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`',
                 '原文已是 Python 3 可运行的写法，仅删去了类型说明文档字符串',
                 '易错点：前导零要判两次（最后一个数 `num[i-j]`、上一个数 `num[i-j-j]`）；每次加法后记得取模',
                 '对比灵神：灵神的 `f[i][j]` 以最后一个数的==起点==为状态，yiduobo 以末尾==长度==为状态'],
    ),
)
