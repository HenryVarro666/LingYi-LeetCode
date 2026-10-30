def _txt(S):
    if 'mod' not in S:
        return '`f[i][j]`：前 `i` 个字符、最后 `j` 个字符成一个数的方案数；`s[i][j]` 是 `f[i][1..j]` 的前缀和；`g` 是后缀 LCP'
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return ''
    num = S['num']
    return f'最后一个数 `num[{i - j}:{i}]` = `{num[i - j:i]}`；上一个数长度 `k` 必须满足 `≤` 它'


CONFIG = dict(
    num=1977, title='划分数字的方案数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='前缀和优化 DP + 后缀 LCP 比大小',
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
    call="Solution().numberOfCombinations('327')",
    expect=2,
    skip=['for j in range(n - 1, -1, -1)', "if num[i - j] == '0'", 'if j - 1 <= i - j', 'for j in range(1, i + 1)', 'f = [[0]', 's = [[0]', 'g = [[0]', 'if i == n - 1 or j == n - 1', 'else:', 'mod = 10', 'if f[i][j] >= mod', 'f[i][j] -= mod', 'if s[i][j] >= mod', 's[i][j] -= mod', 'if res >= mod', 'res -= mod', 'n = len'],
    views=[
        dict(type='string', var='num', label='num', h=210, cell=70),
        dict(type='text', fn=_txt, size=22, h=90),
        dict(type='table', var='f', label='f[i][j]（行 i = 前 i 个字符，列 j = 最后一个数的长度）', h=240, cell=54,
             cursors=[('i', 'j', 'yellow', '')]),
        dict(type='table', var='s', label='s[i][j] = f[i][1] + … + f[i][j]', h=240, cell=54,
             cursors=[('i', 'j', 'yellow', '')]),
        dict(type='table', var='g', label='g[a][b]：后缀 num[a:] 与 num[b:] 的最长公共前缀', h=210, cell=54),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'yellow'), ('res', 'res', 'green')],
    captions={
        'for i in range(n - 1': '先预处理 `g`：从后往前，`g[i][j]` = 后缀 `num[i:]` 与 `num[j:]` 的最长公共前缀',
        'if num[i] == num[j]': lambda S, B, r: f'`num[{S.i}] = {S.num[S.i]}`，`num[{S.j}] = {S.num[S.j]}`：' + ('相同 → LCP 至少 1，等于后一对 `+1`' if S.num[S.i] == S.num[S.j] else '不同 → LCP 为 0'),
        'g[i][j] = g[i + 1][j + 1] + 1': '`g[{i}][{j}] = g[{i+1}][{j+1}] + 1` = =={g[i][j]}==',
        'if num[0] == \'0\'': lambda S, B, r: ('第一个数不能有前导 0 → 直接返回 0' if S.num[0] == '0' else '`num[0] = ' + S.num[0] + '`，不是 0，可以继续'),
        'f[1][1] = 1': '只有 1 个字符，整体就是一个数 → `f[1][1] = 1`',
        's[1][1] = 1': '`s[1][1] = f[1][1] = 1`',
        'for i in range(2': lambda S, B, r: ('每个前缀 `i` 都算完了' if B.get('i') == S.i else f'考虑前 `{S.i}` 个字符：最后一个数的长度 `j` 可以是 `1..{S.i}`'),
        'f[i][i] = 1': '`j = i`：整段当成一个数，只有 1 种 → `f[{i}][{i}] = 1`',
        'for j in range(i - 1': lambda S, B, r: ('`j` 都试完了，回去算前缀和 `s`' if S.j == 1 and B.get('j') == 1 else f'最后一个数长度 `j = {S.j}`：它是 `num[{S.i - S.j}:{S.i}]`'),
        's[i - j][j - 1]': lambda S, B, r: (f'上一个数更短（长度 `k < {S.j}`）一定更小，前面只有 `{S.i - S.j}` 个字符 → `k ≤ {min(S.j - 1, S.i - S.j)}`：`f[{S.i}][{S.j}] = s[{S.i - S.j}][{S.j - 1}]` = =={S.f[S.i][S.j]}==，前缀和一步取'
                                            if min(S.j - 1, S.i - S.j) > 0 else f'`j = {S.j}`：前面没有更短的上一个数可接 → `s[{S.i - S.j}][{S.j - 1}]` = =={S.f[S.i][S.j]}=='),
        's[i - j][i - j]': '前面字符不足 `j` 个，上一个数长度 `1..{i-j}` 全部更短 → `f[{i}][{j}] = s[{i-j}][{i-j}]` = =={f[i][j]}==',
        'if i - j - j >= 0': lambda S, B, r: (f'再看上一个数恰好和它等长（也是 `{S.j}` 位）：要有 `{2 * S.j}` 个字符且不以 0 开头；`i − 2j = {S.i - 2 * S.j}`' + ('，不够 → 不可能' if S.i - 2 * S.j < 0 else '，够')),
        'f[i][j] += f[i - j][j]': '等长且 `上一个 ≤ 当前`（LCP ≥ j 相同，或 LCP 后第一位更小）→ 加上 `f[{i-j}][{j}]` = {f[i-j][j]} → `f[{i}][{j}]` = =={f[i][j]}==',
        's[i][j] = s[i][j - 1] + f[i][j]': '`s[{i}][{j}] = s[{i}][{j-1}] + f[{i}][{j}]` = =={s[i][j]}==：第 `i` 行算完才能给后面用',
        'res = 0': '`res` 累加最后一行 `f[n][·]`',
        'res += f[n][i]': '`res` += `f[{n}][{i}]` = {f[n][i]} → =={res}==',
        'return res': '`num` 的所有合法划分数 = `sum(f[n])` = =={ret}==',
    },
    cards=dict(
        one_liner='f[i][j] 记最后一个数的长度，比大小靠最长公共前缀',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['把数字串 `num` 切成若干个==非递减==的正整数，不能有前导 0',
                 '返回划分方案数（模 `10^9+7`）',
                 '示例：`"327"` → `2`（`3,27` 和 `327`）；本视频就用它'],
        quote='令f[i][j]表示字符串中的前i个字符，将最后j个字符划分成一个单独数字时可行的方案数。……若这个字符长度k < j，那么显然满足nums[i - j - k : i - j] < nums[i - j : i]，而相对的，若k > j，那么显然有nums[i - j - k : i - j] > nums[i - j : i]。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：前 `i` 个字符、最后 `j` 个字符成一个数。上一个数长度为 `k`',
              '`k < j` 一定更小，`k > j` 一定更大，只有 `k = j` 要比较字符串',
              '`k < j` 的部分是 `f[i−j][1..j−1]` 的和 → 用前缀和 `s` 一步取',
              '`k = j` 的比较：预处理后缀 LCP `g`，看第一个不同位的大小'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`；朴素转移是 `O(n^3)`，靠前缀和和 LCP 优化',
                 '易错：以 `0` 开头的数 `f = 0`；第一个字符是 `0` 直接返回 0',
                 '等长比较用 LCP：`g ≥ j` 表示完全相同，否则比 LCP 后第一个字符',
                 '原文为 Python 2 风格，但语法在 Python 3 下可直接运行，代码未改动',
                 '对比灵神：灵神 `f[i][j]` 记「最后一个数起点为 i」，向两端扩展累加；yiduobo 记「最后 j 个字符」，用前缀和 s 一步取'],
    ),
)
