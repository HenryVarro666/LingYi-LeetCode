S0 = 'cbbad'


def _cell(S, r, c, v):
    if S.get('left') is None:
        return None
    if (r, c) == (S['left'], S['right']):
        return 'yellow'
    return 'green' if v is not None else None


def _cap_memo(S, B, ret):
    l, r = S.left, S.right
    v = B.f[l][r]
    if v is not None:
        return f'`f[{l}][{r}] = {v}` ==已经算过== → 直接返回，不再递归（记忆化）'
    return f'`f[{l}][{r}]` 还没算过 → 分情况计算 `s[{l}..{r}] = "{S.s[l:r + 1]}"`'


def _cap_pair(S, B, ret):
    l, r, s = S.left, S.right, S.s
    if s[l] == s[r]:
        return f'`left == right − 1`：只有两个字符，且 `{s[l]} == {s[r]}` → 长度 2'
    return f'`left == right − 1`：只有两个字符，且 `{s[l]} ≠ {s[r]}` → 只能留一个，长度 1'


def _cap_eq(S, B, ret):
    l, r, s = S.left, S.right, S.s
    if s[l] == s[r]:
        return f'`s[{l}] == s[{r}] == {s[l]}`：这两个字符==必然是子序列的一部分== → `f[{l + 1}][{r - 1}] + 2`'
    return f'至少三个字符，`s[{l}] = {s[l]} ≠ s[{r}] = {s[r]}`：两个字符中==必然要去掉一个=='


CONFIG = dict(
    num=516, title='最长回文子序列', difficulty='Medium', category='多维动态规划',
    author='yiduobo', technique='区间 DP · 记忆化搜索',
    tags=['热题173'],
    code='''
class Solution(object):
    def longestPalindromeSubseq(self, s):

        l = len(s)
        f = [[None] * l for _ in range(l)]

        return self.dfs(0, l - 1, s, f)

    def dfs(self, left, right, s, f):
        if f[left][right] is not None:
            return f[left][right]

        if left == right:
            f[left][right] = 1
        elif left == right - 1:
            if s[left] == s[right]:
                f[left][right] = 2
            else:
                f[left][right] = 1
        elif s[left] == s[right]:
            f[left][right] = self.dfs(left + 1, right - 1, s, f) + 2
        else:
            f[left][right] = max(self.dfs(left + 1, right, s, f), self.dfs(left, right - 1, s, f))

        return f[left][right]
''',
    call=f'Solution().longestPalindromeSubseq({S0!r})',
    expect=2,
    max_steps=75,
    skip=[13, 15],
    views=[
        dict(type='string', var='s', label='s（蓝/粉 = 当前区间 [left, right]）', h=205, cell=70,
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right')),
        dict(type='table', var='f', label='f[l][r]（· = 还没算；绿 = 已记忆，黄 = 当前区间）', h=255, cell=56,
             rows=lambda S: [f'{k}{c}' for k, c in enumerate(S0)], cols=lambda S: [f'{k}{c}' for k, c in enumerate(S0)],
             color=_cell),
        dict(type='calls', h=176, hide=('s', 'f')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('f[left][right]', 'f[left][right]', 'green')],
    captions={
        4: '`l = {l}`',
        5: '`f[l][r]`：`s[l..r]` 最长回文子序列的长度；`None` 表示还没算',
        7: lambda S, B, r: ('求整个串 `dfs(0, l − 1)`' if r is None else f'答案 `f[0][{len(S0) - 1}]` = =={r}=='),
        10: _cap_memo,
        11: '返回记忆的值 `{ret}`',
        13: lambda S, B, r: ('`left == right`：只有一个字符 → 1' if S.left == S.right else '不止一个字符'),
        14: '`f[{left}][{left}] = 1`',
        15: lambda S, B, r: ('`left == right − 1`：只有两个字符' if S.left == S.right - 1 else '至少三个字符'),
        16: _cap_pair,
        17: '`f[{left}][{right}] = 2`',
        19: '`f[{left}][{right}] = 1`',
        20: _cap_eq,
        21: lambda S, B, r: f'递归算里面 `dfs({B.left + 1}, {B.right - 1})`，结果 + 2',
        23: lambda S, B, r: (f'去掉 `s[{B.left}]` 或去掉 `s[{B.right}]`，取较大者：'
                             f'`max(dfs({B.left + 1}, {B.right}), dfs({B.left}, {B.right - 1}))`'),
        25: '返回 `f[{left}][{right}] = {ret}`',
    },
    cards=dict(
        one_liner='f[l][r] 只看两端：相等都要，不等去掉一个',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['给你一个字符串 `s`，找出其中==最长的回文子序列==，返回它的长度',
                 '子序列：不改变顺序，删除某些字符（或不删）得到的序列',
                 '示例：`"bbbab"` → `4`；`"cbbd"` → `2`',
                 f'本视频：`"{S0}"` → `2`（`"bb"`）'],
        quote='若s[l]等于s[r]，那么将这两个字符==必然是f[l][r]代表的子序列的一部分==……若s[l]不等于s[r]，那么这两个字符中==必然要去掉一个==。',
        quote_src='—— yiduobo 题解原文',
        idea=['经典区间 DP：`f[l][r]` 表示 `l` 到 `r` 这一段最长的回文子序列长度',
              '边界：一个字符为 1；两个字符相等为 2，否则为 1',
              '循环顺序要注意 → 方便起见用==记忆化搜索==，`f` 同时当缓存'],
        summary=['时间 `O(n^2)`：每个区间只算一次，之后直接查表',
                 '`f` 初始化成 `None` 而不是 0，才能区分“没算过”',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改',
                 '对比灵神：灵神把记忆化搜索 1:1 翻译成递推，再空间优化到 `O(n)`'],
    ),
)
