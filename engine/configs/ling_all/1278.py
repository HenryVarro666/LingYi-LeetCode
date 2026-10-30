S0 = 'abcde'
K0 = 3


def _cands(S):
    i, r = S.get('i'), S.get('r')
    if i is None or r is None or S.get('_line') != 12 or 'min_change' not in S:
        return None
    return [(l, S['f'][l - 1], S['min_change'][l][r]) for l in range(i, r + 1)]


def _txt(S):
    c = _cands(S)
    if c is None:
        if S.get('i') is None:
            return '`min_change[l][r]`：把 `s[l..r]` 改成回文串的最少修改数'
        return f'第 `{S["i"]}` 刀：`f[r]` = 把 `s[0..r]` 分成 `{S["i"] + 1}` 段的最少修改数'
    r = S['r']
    parts = '，'.join(f'l={l}: {a}+{b}={a + b}' for l, a, b in c)
    return f'`f[{r}]` = min( {parts} ) = =={min(a + b for _, a, b in c)}=='


def _mc(S, a, b, v):
    c = _cands(S)
    if c is not None:
        r = S['r']
        if any(b == r and a == l for l, _, _ in c):
            return 'yellow' if min(x + y for _, x, y in c) == next(x + y for l, x, y in c if l == a) else 'blue'
        return None
    if S.get('_line') == 7 and S.get('i') == a and S.get('j') == b:
        return 'yellow'
    return None


def _fc(S, k, v):
    c = _cands(S)
    if c is None:
        return None
    if k == S['r']:
        return 'yellow'
    if any(l - 1 == k for l, _, _ in c):
        return 'blue'
    return None


CONFIG = dict(
    num=1278, title='分割回文串 III', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP · 预处理回文修改次数 + 空间优化',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1979'],
    code='''
class Solution:
    def palindromePartition(self, s: str, k: int) -> int:
        n = len(s)
        min_change = [[0] * n for _ in range(n)]
        for i in range(n - 2, -1, -1):
            for j in range(i + 1, n):
                min_change[i][j] = min_change[i + 1][j - 1] + (1 if s[i] != s[j] else 0)

        f = min_change[0]  # 无需 copy
        for i in range(1, k):
            for r in range(n - k + i, i - 1, -1):
                f[r] = min(f[l - 1] + min_change[l][r] for l in range(i, r + 1))
        return f[-1]
''',
    call=f'Solution().palindromePartition({S0!r}, {K0})',
    expect=1,
    skip=['n = len(s)', 'for j in range(i + 1, n)'],
    views=[
        dict(type='string', var='s', label='s', h=150, cell=70,
             color=lambda S, k, v: ('blue' if S.get('_line') == 7 and k == S.get('i') else 'pink' if S.get('_line') == 7 and k == S.get('j') else None)),
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='table', var='min_change', label='min_change[l][r]（行 l，列 r；黄 = 最优，蓝 = 候选）', h=300, cell=60,
             rows=lambda S: list(range(len(S['s']))), cols=lambda S: list(range(len(S['s']))), color=_mc),
        dict(type='array', var='f', label='f[r]（注意：f 就是 min_change[0] 本身，无需 copy）', h=190, cell=80,
             pointers={'r': 'pink'}, color=_fc),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'cyan'), ('r', 'r', 'pink'), ('k', 'k', 'yellow')],
    captions={
        'min_change = [[0]': '`min_change[i][j]` = `s[i..j]` 改成回文串的最少次数；单字母、空串都是 0',
        'for i in range(n - 2': lambda S, B, r: (f'`i = {S.i}`：算 `[i][·]` 要先有 `[i+1][·]` → ==i 从大到小==' if S.get('i') != B.get('i') else 'min_change 全部算完'),
        'min_change[i][j] =': lambda S, B, r: (
            f'`s[{S.i}] = {S.s[S.i]}`，`s[{S.j}] = {S.s[S.j]}`：' + ('相等，无需修改' if S.s[S.i] == S.s[S.j] else '不等，必须改一个字母')
            + f' → `min_change[{S.i}][{S.j}] = min_change[{S.i + 1}][{S.j - 1}] + {0 if S.s[S.i] == S.s[S.j] else 1}` = =={S.min_change[S.i][S.j]}=='),
        'f = min_change[0]': '只切 0 刀：`f[r]` 就是 `min_change[0][r]`',
        'for i in range(1, k)': lambda S, B, r: (f'现在切第 `{S.i}` 刀（分成 `{S.i + 1}` 段）；`f` 里是上一轮（`{S.i}` 段）的结果' if S.get('i') != B.get('i') else '`k - 1` 刀都切完了'),
        'for r in range(n - k + i': lambda S, B, r: (f'右端点 `r = {S.r}`：右边还要留 `k-1-i = {S.k - 1 - S.i}` 个子串；==r 倒序==，保证 `f[l-1]` 还是旧值'
                                                    if S.get('r') != B.get('r') else f'`i = {S.i}` 的所有 `r` 都更新完'),
        'f[r] = min(': lambda S, B, r: _txt(S).replace('`f[', '`f[', 1),
        'return f[-1]': '`f[n-1]` = =={ret}==：整个字符串分成 `{k}` 段的最少修改数',
    },
    cards=dict(
        one_liner='先预处理每段改成回文的代价，再枚举最后一段做划分 DP',
        complexity='时间 `O(n^2 + (n-k)^2·k)`，空间 `O(n^2)`',
        problem=['字符串 `s` 可以先改若干字母，再分成 `k` 个非空子串，要求每个子串都是回文串',
                 '求最少修改次数',
                 '示例：`s = "abcde", k = 3` → `1`（`"a" "b" "cde"` 改成 `"cdc"`）'],
        quote='枚举最后一段子串的左端点 l，那么接下来要解决的问题是，把 s[0] 到 s[l-1] 划分成 i 个非空子串……注意 l 最小是 i，因为剩余的 i 个子串必须是非空的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`min_change[i][j] = min_change[i+1][j-1] + [s[i] != s[j]]`：两端不同就改一个',
              '`f[r] = min(f[l-1] + min_change[l][r])`：枚举最后一段左端点 `l`',
              '`f[i-1]` 只用于 `f[i]` → 像 0-1 背包去掉一维，`r` ==倒序=='],
        summary=['时间 `O(n^2 + (n-k)^2·k)`，空间 `O(n^2)`',
                 '`r` 上限 `n-k+i`：右边还要给 `k-1-i` 个子串留位置',
                 '`f = min_change[0]` 不 copy 也行，因为 `min_change[0]` 之后不再被读',
                 '另有记忆化搜索、二维递推写法，本视频演示空间优化版'],
    ),
)
