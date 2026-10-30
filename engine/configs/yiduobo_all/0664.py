S0 = 'abca'


def _tc(S, r, c, v):
    I = S.get('_inner', {})
    l, rr = I.get('l'), I.get('r')
    if l is not None and rr is not None and (r, c) == (l, rr) and l <= rr:
        return 'yellow'
    if v is not None:
        return 'green'
    return None


CONFIG = dict(
    num=664, title='奇怪的打印机', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='区间 DP · 记忆化搜索',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def strangePrinter(self, s):

        if not s:
            return 0

        n = len(s)
        f = [[None] * n for _ in range(n)]
        
        return self.dfs(0, n - 1, f, s)

    def dfs(self, l, r, f, s):
        if l > r:
            return 0
        if l == r:
            return 1
        if f[l][r] is None:
            f[l][r] = self.dfs(l, r - 1, f, s) + 1
            for cut_pos in range(l, r):
                if s[r] == s[cut_pos]:
                    f[l][r] = min(f[l][r], self.dfs(l, cut_pos - 1, f, s) + self.dfs(cut_pos + 1, r, f, s))
        
        return f[l][r]
''',
    call=f'Solution().strangePrinter({S0!r})',
    expect=3,
    skip=['if not s', 'n = len(s)', 'for cut_pos'],
    views=[
        dict(type='string', var='s', label='s（蓝 = l，粉 = r）', h=190, cell=80,
             pointers={'l': 'blue', 'r': 'pink'}),
        dict(type='table', var='f', label='f[l][r]：打印 s[l..r] 的最少次数（黄 = 当前区间，绿 = 已算好）', h=290, cell=56,
             rows=lambda S: [f'{k}{c}' for k, c in enumerate(S0)], cols=lambda S: [f'{k}{c}' for k, c in enumerate(S0)],
             color=_tc),
        dict(type='calls', h=200, hide=('f', 's')),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('cut_pos', 'cut_pos', 'purple')],
    captions={
        'f = [[None]': '`f[l][r]`：打印 `s[l..r]` 的最少次数，None 表示还没算',
        'return self.dfs(0': '从整个字符串 `[0, {n-1}]` 开始记忆化搜索',
        'if l > r': lambda S, B, r: ('`l = %d > r = %d`：空区间，不需要打印，返回 ==0==' % (S.l, S.r) if S.l > S.r else '`l = %d <= r = %d`：区间非空' % (S.l, S.r)),
        'if l == r': lambda S, B, r: (f'`l == r`：只有一个字符 `{S.s[S.l]}`，打印 1 次，返回 ==1==' if S.l == S.r else f'`l = {S.l} < r = {S.r}`，区间有多个字符，继续'),
        'if f[l][r] is None': lambda S, B, r: ('`f[%d][%d]` 还没算过，现在算' % (S.l, S.r) if S.f[S.l][S.r] is None else '`f[%d][%d]` 算过了，直接用' % (S.l, S.r)),
        'f[l][r] = self.dfs(l, r - 1, f, s) + 1': '先给基础方案：先打好 `s[{B.l}..{B.r-1}]`，再单独打印 `s[{B.r}]`，共 `f[{B.l}][{B.r-1}] + 1` 次',
        'if s[r] == s[cut_pos]': lambda S, B, r: (f'`s[{S.r}] = {S.s[S.r]}` 与 `s[{S.cut_pos}] = {S.s[S.cut_pos]}` ' + ('==相同==：打印 `s[%d]` 时可以顺带把末尾那格刷出来，不用多花一次' % S.cut_pos if S.s[S.r] == S.s[S.cut_pos] else '不同，不能复用')),
        'f[l][r] = min': '拆成 `[{B.l}, {B.cut_pos-1}]` 与 `[{B.cut_pos+1}, {B.r}]` 两段分别求解，相加后和基础方案 `min` 取小',
        'return f[l][r]': lambda S, B, r: f'`dfs({S.l}, {S.r})` 返回 =={r}==',
    },
    cards=dict(
        one_liner='末尾字符若和前面某个相同，就能顺带多刷一格，不多花一次',
        complexity='时间 `O(n^3)`，空间 `O(n^2)`',
        problem=['打印机每次只能打印同一个字符的一段，可以从任意位置开始、覆盖原有字符',
                 '给你字符串 `s`，求打印出它所需的==最少次数==',
                 '示例：`"aaabbb"` → `2`；本视频：`"abca"` → `3`'],
        quote='对于新加入的s[j]，若其与之前的某个s[k]相等，那么我们可以分别打印s[i]到s[k - 1]以及s[k]到s[j]，其中s[k]到s[j]的部分由于首尾相等，因此可以视为在打印这一部分时首先全部都打印了s[k]。',
        quote_src='—— yiduobo 题解原文（原文把「打印」写作「答应」，已更正）',
        idea=['`f[l][r]` = 打印 `s[l..r]` 的最少次数',
              '基础方案：先打 `s[l..r-1]`，再单独打 `s[r]` → `f[l][r-1] + 1`',
              '若 `s[r] == s[k]`：`s[k]` 那次打印顺带覆盖到 `r`，拆成 `f[l][k-1] + f[k+1][r]`',
              '用记忆化搜索，边界 `l > r` 为 0、`l == r` 为 1'],
        summary=['时间 `O(n^3)`，空间 `O(n^2)`',
                 '易错：拆分后不是 `f[k+1][r-1] + 1`，因为中间可能还有和 `s[r]` 相同的字符',
                 '易错：`l > r` 返回 0，必须先于 `l == r` 判断，`cut_pos - 1` 可能小于 `l`',
                 '原文为 Python 2 风格，代码未做修改即可在 Python 3 运行',
                 '同类区间 DP：1000. 合并石头的最低成本、516. 最长回文子序列'],
    ),
)
