S0 = 'mbadm'


def _tbl(S):
    f = S.get('f')
    if not f:
        return [[]]
    return [['·' if v is None else v for v in row] for row in f]


def _cell(S, r, c, v):
    l, rr = S.get('l'), S.get('r')
    if l is None or rr is None:
        return None
    if (r, c) == (l, rr):
        return 'yellow'
    if S.get('_line') in (12, 16, 18):
        if S['s'][l] == S['s'][rr]:
            return 'green' if (r, c) == (l + 1, rr - 1) else None
        return 'blue' if (r, c) in ((l + 1, rr), (l, rr - 1)) else None
    return None


def _top(S):
    l, r = S.get('l'), S.get('r')
    if l is None or r is None:
        return '`f[l][r]`：把 `s[l..r]` 变成回文串的最少插入次数（`·` = 还没算）'
    s = S['s']
    if l == r:
        return f'`f[{l}][{r}]`：只有一个字符 `{s[l]}`，本身就是回文，0 次'
    if s[l] == s[r]:
        return f'`s[{l}] = s[{r}] = {s[l]}`：两端已配对，看里面 `f[{l+1}][{r-1}]`'
    return f'`s[{l}] = {s[l]} ≠ s[{r}] = {s[r]}`：补一个字符 → `min(f[{l+1}][{r}], f[{l}][{r-1}]) + 1`'


CONFIG = dict(
    num=1312, title='让字符串成为回文串的最少插入次数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='区间 DP · 记忆化搜索',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def minInsertions(self, s):

        n = len(s)
        f = [[None] * n for _ in range(n)]
        return self.dfs(0, n - 1, s, f)
    
    def dfs(self, l, r, s, f):
        if f[l][r] is None:
            if l == r:
                f[l][r] = 0
            elif s[l] == s[r]:
                if l == r - 1:
                    f[l][r] = 0
                else:
                    f[l][r] = self.dfs(l + 1, r - 1, s, f)
            else:
                f[l][r] = min(self.dfs(l + 1, r, s, f), self.dfs(l, r - 1, s, f)) + 1
        
        return f[l][r]
''',
    call=f'Solution().minInsertions({S0!r})',
    expect=2,
    skip=['else:'],
    max_steps=60,
    views=[
        dict(type='text', fn=_top, size=25, h=70),
        dict(type='string', var='s', label='s（蓝 = l，粉 = r）', cell=80, h=150,
             color=lambda S, k, v: ('blue' if k == S.get('l') else 'pink' if k == S.get('r') else None) if S.get('l') is not None else None),
        dict(type='table', var=_tbl, label='f[l][r]（黄 = 正在算，绿/蓝 = 依赖的格子）', h=330, cell=70,
             rows=[f'{k}{c}' for k, c in enumerate(S0)], cols=[f'{k}{c}' for k, c in enumerate(S0)], color=_cell),
        dict(type='calls', h=200, hide=('s', 'f')),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink')],
    captions={
        'n = len(s)': '`n = {n}`',
        'f = [[None]': '`f[l][r]` 记录 `s[l..r]` 的答案，`None` 表示还没算（记忆化）',
        'return self.dfs(0, n - 1': lambda S, B, r: (f'从整个字符串 `dfs(0, {S.n - 1})` 开始' if r is None else f'整个 `s` 的答案：==`{r}`== 次插入'),
        'if f[l][r] is None': lambda S, B, r: (f'`f[{S.l}][{S.r}]` 还没算过 → 往下算' if S.f[S.l][S.r] is None else f'`f[{S.l}][{S.r}] = {S.f[S.l][S.r]}` 已经算过 → ==直接用==，不再递归'),
        'if l == r': lambda S, B, r: (f'`l == r = {S.l}`：长度为 1' if S.l == S.r else f'`l = {S.l} ≠ r = {S.r}`，长度大于 1'),
        'f[l][r] = 0': lambda S, B, r: (f'一个字符、或两个相同字符，本来就是回文 → `f[{S.l}][{S.r}] = 0`'),
        'elif s[l] == s[r]': lambda S, B, r: (f'`s[{S.l}] = {S.s[S.l]}`，`s[{S.r}] = {S.s[S.r]}`：' + ('==相同==，两端互相配对' if S.s[S.l] == S.s[S.r] else '==不同==，要补一个字符')),
        'if l == r - 1': lambda S, B, r: ('`l == r - 1`：两个相同字符，不用插入 → 0' if S.l == S.r - 1 else '中间还有字符，交给 `dfs(l+1, r-1)`'),
        'f[l][r] = self.dfs(l + 1, r - 1': '递归 `dfs({l}, {r})`：两端配对不动，只处理里面',
        'f[l][r] = min': '两种补法取小：左边补一个配 `s[{B.r}]` → 看 `f[{B.l + 1}][{B.r}]`；右边补一个配 `s[{B.l}]` → 看 `f[{B.l}][{B.r - 1}]`；再 `+ 1`',
        'return f[l][r]': '`f[{l}][{r}]` = =={ret}==',
    },
    cards=dict(
        one_liner='两端相同就配对，不同就补一个字符，取更小',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['给你字符串 `s`，每次操作可在任意位置==插入一个字符==',
                 '求让 `s` 变成回文串的==最少插入次数==',
                 '示例：`"zzazz"` → `0`；本视频：`"mbadm"` → `2`（如 `"mbdadbm"`）'],
        quote='令f[l][r]表示将l到r这一段子串变为回文串所需的最少插入次数。……若s[l] != s[r]，那么我们必须想办法在s[l]左侧插入一个字符，与s[r]进行匹配，或者在s[r]右侧插入一个字符，与s[l]进行匹配。',
        quote_src='—— yiduobo 题解原文',
        idea=['`s[l] == s[r]`：两端已经配对，`f[l][r] = f[l+1][r-1]`（长度 2 时为 0）',
              '`s[l] != s[r]`：补一个字符配 `s[r]`（剩 `l+1..r`）或配 `s[l]`（剩 `l..r-1`），`+1`',
              '作者用记忆化搜索写：`f` 先填 `None`，算过的直接用'],
        summary=['时间 `O(n^2)`：区间个数 `O(n^2)`，每个 `O(1)`',
                 '易错：`l == r - 1` 且两字符相同时答案是 0，别再递归到 `l > r`',
                 '作者也提到可以改成递推：先枚举区间长度，再枚举起点',
                 '答案 = `n − 最长回文子序列长度`（对比 516 题）',
                 '原文已是 Python 3 可运行的写法，无需修改'],
    ),
)
