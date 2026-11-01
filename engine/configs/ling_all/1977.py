def _txt(S):
    ln = S.get('_line', 0)
    s = S['s']
    i, j, k = S.get('i'), S.get('j'), S.get('k')
    if 'f' not in S or i is None or j is None or ln < 28:
        return '`lcp[i][j]`：后缀 `s[i:]` 与 `s[j:]` 的最长公共前缀长度'
    if k is None or k < 0:
        return f'`f[{i}][{j}]`：最后一个数是 `s[{i}:{j + 1}]` = {s[i:j + 1]}；前面已没有数字可接'
    return (f'上一个数 `s[{k}:{i}]` = {s[k:i]}（长 {i - k}），最后一个数 `s[{i}:{j + 1}]` = {s[i:j + 1]}（长 {j - i + 1}）；'
            f'sum = {S["sum"]}')


def _cur_f(S):
    i, j = S.get('i'), S.get('j')
    return (i, j) if S.get('_line', 0) >= 28 and isinstance(i, int) and isinstance(j, int) and 'f' in S else (None, None)


def _cur_lcp(S):
    i, j = S.get('i'), S.get('j')
    return (i, j) if S.get('_line', 0) < 28 and isinstance(i, int) and isinstance(j, int) else (None, None)


CONFIG = dict(
    num=1977, title='划分数字的方案数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='LCP + 前缀和优化 DP（Go 原文转写）',
    tags=['灵神题单·动态规划', '灵神题单·字符串', '难度分 2817'],
    code='''
mod = 10 ** 9 + 7


class Solution:
    def numberOfCombinations(self, s: str) -> int:
        ans = 0
        if s[0] == '0':
            return ans

        n = len(s)
        # 计算 lcp
        lcp = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if s[i] == s[j]:
                    lcp[i][j] = lcp[i + 1][j + 1] + 1

        # 返回 s[l1:l2] <= s[l2:r2]
        def lessEq(l1: int, l2: int, r2: int) -> bool:
            l = lcp[l1][l2]
            return l >= r2 - l2 or s[l1 + l] < s[l2 + l]

        f = [[0] * n for _ in range(n)]
        for j in range(n):
            f[0][j] = 1
        for i in range(1, n):
            if s[i] == '0':
                continue
            # k 和 j 同时向左向右扩展
            k, sum = i - 1, 0
            for j in range(i, n):
                f[i][j] = sum  # 对应上面所说的长度小于最后一个划分出的整数
                if k < 0:
                    continue
                if s[k] > '0' and lessEq(k, i, j + 1):
                    f[i][j] = (f[i][j] + f[k][i - 1]) % mod  # 对应上面所说的长度等于最后一个划分出的整数
                sum = (sum + f[k][i - 1]) % mod
                k -= 1
        for row in f:
            ans = (ans + row[n - 1]) % mod
        return ans
''',
    call="Solution().numberOfCombinations('32071')",
    expect=3,
    views=[
        dict(type='string', var='s', label='s（蓝 = i：最后一个数的起点；粉 = j：终点；橙 = k：上一个数的起点）', cell=80, h=150,
             pointers={'i': 'blue', 'j': 'pink', 'k': 'orange'}),
        dict(type='table', var='lcp', label='lcp[i][j]', cell=44, h=250, rows=lambda S: list(range(len(S['s']) + 1)),
             cols=lambda S: list(range(len(S['s']) + 1)),
             color=lambda S, i, j, v: 'green' if v else None,
             cursors=[(lambda S: _cur_lcp(S)[0], lambda S: _cur_lcp(S)[1], 'yellow')]),
        dict(type='table', var='f', label='f[i][j]：最后一个数是 s[i..j] 时的方案数', cell=44, h=250,
             rows=lambda S: list(range(len(S['s']))), cols=lambda S: list(range(len(S['s']))),
             color=lambda S, i, j, v: 'green' if v else None,
             cursors=[(lambda S: _cur_f(S)[0], lambda S: _cur_f(S)[1], 'yellow')]),
        dict(type='text', fn=_txt, size=24, h=80),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('k', 'k', 'orange'), ('sum', 'sum', 'cyan'), ('ans', 'ans', 'green')],
    skip=['for i in range(n - 1, -1, -1)', 'for j in range(n - 1, -1, -1)', 'if s[i] == s[j]', 'ans = 0', 'for j in range(n):',
          'f[0][j] = 1', 'continue', 'if k < 0', 'l = lcp[l1][l2]', 'for row in f'],
    max_steps=72,
    captions={
        'if s[0] == \'0\'': lambda S, B, r: ('开头是 `0` → 有前导零，答案 0' if S.s[0] == '0' else '开头不是 `0`，继续'),
        'lcp = [[0]': '`lcp[i][j]`：后缀 `s[i:]` 与 `s[j:]` 的最长公共前缀；大小 `(n+1)×(n+1)`，边界为 0',
        'lcp[i][j] = lcp[i + 1][j + 1] + 1': '`s[{i}] = s[{j}]`：`lcp[{i}][{j}] = lcp[{i + 1}][{j + 1}] + 1` = =={lcp[i][j]}==',
        'f = [[0] * n': '`f[i][j]`：最后一个数是 `s[i..j]` 时的方案数；`f[0][·] = 1`（整段做一个数）',
        'if s[i] == \'0\'': lambda S, B, r: (f'`s[{S.i}] = 0`：数字不能有前导零，`f[{S.i}][·]` 都是 0 → 跳过' if S.s[S.i] == '0'
                                             else f'`i = {S.i}`：最后一个数从 `s[{S.i}]` 开始'),
        'k, sum = i - 1, 0': '`k = {k}` 是上一个数的起点，先取长度 1；`sum` 累加更短的上一个数的方案',
        'for j in range(i, n)': lambda S, B, r: (f'`j = {S.j}`：最后一个数是 `s[{S.i}:{S.j + 1}]`，长 {S.j - S.i + 1}'
                                                  if (S.get('j') != B.get('j') or B.get('k') == B.get('i') - 1) else '这个 i 枚举完了'),
        'f[i][j] = sum': lambda S, B, r: (f'上一个数比它==短==的方案都行：`f[{S.i}][{S.j}] = sum` = =={S.f[S.i][S.j]}==' +
                                          ('；`k < 0`，没有等长的上一个数了' if S.k < 0 else '')),
        'if s[k] > \'0\'': lambda S, B, r: (f'上一个数 `s[{B.k}:{B.i}]` = {B.s[B.k:B.i]}（长 {B.i - B.k}），最后一个数 `s[{B.i}:{B.j + 1}]` = {B.s[B.i:B.j + 1]}（长 {B.j - B.i + 1}）：等长，要比大小'
                                              if B.s[B.k] > '0' else f'上一个数 `s[{B.k}:{B.i}]` 以 `0` 开头，有前导零 → 不能接'),
        'f[i][j] = (f[i][j] + f[k][i - 1])': '长度相等且 `s[{k}:{i}] ≤ s[{i}:{j+1}]`：加上 `f[{k}][{i-1}]` → `f[{i}][{j}]` = =={f[i][j]}==',
        'sum = (sum + f[k][i - 1])': '`sum` 加上 `f[{k}][{i-1}]`（上一个数从 `s[{k}]` 开始的方案）：下一个 j 时它就比最后一个数短 → `sum` = =={sum}==',
        'k -= 1': '`k` 左移，上一个数变长一位：`k` → {k}',
        'l = lcp[l1][l2]': '`lcp[{l1}][{l2}]` = {l}',
        'return l >= r2 - l2': lambda S, B, r: (f'`lcp` = {S.l}，不小于长度 {S.r2 - S.l2} → 两数完全相同，`≤` 成立' if S.l >= S.r2 - S.l2 else f'`lcp` = {S.l} 小于长度 {S.r2 - S.l2}：比较下一个字符 `{S.s[S.l1 + S.l]}` 和 `{S.s[S.l2 + S.l]}` → ==返回 {r}=='),
        'for row in f': '把每个 `f[·][n-1]` 加起来：最后一个数一定要到 `s` 末尾',
        'ans = (ans + row[n - 1])': '`ans += f[·][{n-1}]` → =={ans}==',
        'return ans': '一共 `{ret}` 种方案',
    },
    cards=dict(
        one_liner='f[i][j]：最后一个数是 s[i..j]；用 lcp 在 O(1) 比较等长两数',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['把数字串拆成若干个==非递减、无前导零==的正整数，求有多少种拆法（对 `10^9+7` 取模）',
                 '`"327"` → `2`（`3,27` 和 `327`）',
                 '本视频：`s = "32071"` → `3`'],
        quote='若其长度小于最后一个划分出的整数，则可以将其方案数加到 f[i][j] 上；若其长度等于最后一个划分出的整数，则需要比较两个整数的大小，这可以通过比较两个整数（子串）最长公共前缀的下一个字符得出。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i][j]`：最后一个数是 `s[i..j]` 时的方案数，答案 = `Σ f[i][n-1]`',
              '上一个数比它==短==：一定更小，累加前缀和 `sum`（k、j 一起往外扩）',
              '上一个数和它==等长==：靠 `lcp` 比较大小；比它==长==：不行'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`',
                 '原文为 Go，已按原逻辑逐行转写为 Python：三段式 `for j, k, sum := ...` 写成 `k, sum = ...` + `for j in range(i, n)`，`const mod` 放在类外',
                 '易错点：前导零（`s[i] == \'0\'` 和 `s[k] > \'0\'` 两处）；`lcp` 数组要开 `(n+1)×(n+1)`',
                 '同类题：Z 函数 / 前缀和优化 DP'],
    ),
)
