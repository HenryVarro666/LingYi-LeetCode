CONFIG = dict(
    num=1668, title='最大重复子字符串', difficulty='Easy', category='字符串',
    author='yiduobo', technique='公共子串 DP · 结尾对齐 word',
    tags=['灵神题单·字符串'],
    code='''
class Solution(object):
    def maxRepeating(self, sequence, word):

        m = len(sequence)
        n = len(word)
        p = m // n
        f = [[0] * (n * p) for _ in range(m)]
        res = 0
        for i in range(m):
            for j in range(n * p):
                if sequence[i] == word[j % n]:
                    f[i][j] = 1
                    if i > 0 and j > 0:
                        f[i][j] += f[i - 1][j - 1]
                
                res = max(res, f[i][j] // n - (1 if j % n != n - 1 else 0))

        return res
''',
    call='Solution().maxRepeating("ababa", "ab")',
    expect=2,
    max_steps=60,
    views=[
        dict(type='string', var='sequence', label='sequence（行）', cell=60, pointers={'i': 'blue'}, h=210),
        dict(type='table', var='f', label='f[i][j]：sequence 以 i 结尾、word 重复串以 j 结尾的最长公共子串',
             rows=lambda S: list(S['sequence']), cols=lambda S: [S['word'][j % S['n']] for j in range(S['n'] * S['p'])],
             cursors=[('i', 'j', 'yellow', '(i,j)')], cell=80, h=380),
        dict(type='text', fn=lambda S: (f"`word` 重复成 `{S['word'] * S['p']}`（`p = {S['p']}` 份），在列上做 DP" if 'p' in S else ''), size=24, h=60),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('res', 'res', 'green')],
    captions={
        'm = len(sequence)': '`m = {m}`',
        'n = len(word)': '`n = {n}`',
        'p = m': '`word` 最多重复 `m // n = {p}` 次，列数 `n*p = {n*p}`',
        'f = [[0]': '建 `f`：行是 sequence，列是 word 重复 p 次',
        'res = 0': '`res` 保存答案',
        'for i in range': '`i = {i}`：sequence 的第 {i} 个字符 `{sequence[i]}`',
        'for j in range': '`j = {j}`：重复串第 {j} 个字符 `{word[j % n]}`',
        'if sequence[i] == word[j % n]': lambda S, B, r: (
            f"`sequence[{S.i}] = '{S.sequence[S.i]}'` == `word[{S.j % S.n}] = '{S.word[S.j % S.n]}'` → 公共子串可以延长"
            if S.sequence[S.i] == S.word[S.j % S.n]
            else f"`sequence[{S.i}] = '{S.sequence[S.i]}'` ≠ `word[{S.j % S.n}] = '{S.word[S.j % S.n]}'` → `f[{S.i}][{S.j}] = 0`"),
        'f[i][j] = 1': '先记长度 `1`',
        'f[i][j] += f[i - 1][j - 1]': '接在左上角后面：`f[{i}][{j}]` = =={f[i][j]}==',
        'res = max': lambda S, B, r: (
            f"长度 `{S.f[S.i][S.j]}` 重复 `{S.f[S.i][S.j]}//{S.n} = {S.f[S.i][S.j] // S.n}` 次；"
            + (f"结尾已对齐 word 末尾，不用减" if S.j % S.n == S.n - 1 else "结尾没对齐 word 末尾，==减 1==")
            + f"；`res = {S.res}`"),
        'return res': '最大重复次数 `{res}`',
    },
    cards=dict(
        one_liner='把 word 铺满，求最长公共子串，结尾要对齐 word 末尾',
        complexity='时间 `O(m·n·p)`，空间 `O(m·n·p)`',
        problem=['`word` 重复 `k` 次后是 `sequence` 的子串，求最大的 `k`',
                 '本视频：`sequence = "ababa"`，`word = "ab"` → `2`'],
        quote='公共子串的结尾恰好对应了word的结尾，那么说明这个公共子串的后缀就是由word复制若干遍得到的',
        quote_src='—— yiduobo 题解原文',
        idea=['先把 word 重复到 sequence 的长度，再求与 sequence 的最长公共子串',
              '公共子串长度除以 `n` 得到重复次数',
              '但结尾没对齐 word 末尾时（如 `bcabca`）会多算一次，所以要减 1'],
        summary=['时间 `O(m·n·p)`，空间同阶；数据小，直接用 `O(n^2)` DP',
                 '易错：不对齐就多算，要 `- (1 if j % n != n - 1 else 0)`',
                 '原文提到后缀数组可做到 `O(n)`，作者为了省事用了 DP',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
