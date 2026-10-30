def _color(S, x, v):
    if 'i' not in S or 'j' not in S:
        return None
    i, j, k = S['i'], S['j'], S.get('k', 0)
    if S['_line'] >= 15:
        return 'green' if i <= x < i + len(S['s']) - S['numFriends'] + 1 else None
    if i <= x < i + k or j <= x < j + k:
        return 'green'
    if x == i + k and i + k < len(S['s']):
        return 'blue'
    if x == j + k and j + k < len(S['s']):
        return 'pink'
    return None


CONFIG = dict(
    num=3403, title='从盒子中找出字典序最大的字符串 I', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='字典序最大后缀 · 双指针',
    tags=['灵神题单·贪心与思维', '灵神题单·字符串', '难度分 1762'],
    code='''
class Solution:
    def answerString(self, s: str, numFriends: int) -> str:
        if numFriends == 1:
            return s
        n = len(s)
        i, j = 0, 1
        while j < n:
            k = 0
            while j + k < n and s[i + k] == s[j + k]:
                k += 1
            if j + k < n and s[i + k] < s[j + k]:
                i, j = j, max(j + 1, i + k + 1)
            else:
                j += k + 1
        return s[i: i + n - numFriends + 1]
''',
    call='Solution().answerString("cacbcacb", 3)',
    expect='cbcacb',
    views=[
        dict(type='string', var='s', label='s（绿 = 已相等的前缀，蓝 = s[i+k]，粉 = s[j+k]）', cell=84, h=250,
             pointers={'i': 'blue', 'j': 'pink'}, color=_color),
        dict(type='text', size=26, fn=lambda S: (
            f"最优后缀起点 `i = {S['i']}`，候选起点 `j = {S['j']}`，已相等长度 `k = {S.get('k', 0)}`" if 'j' in S else '')),
        dict(type='text', size=24, fn=lambda S: (
            f"答案至多 `n − numFriends + 1 = {len(S['s']) - S['numFriends'] + 1}` 位" if 'n' in S else '')),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('k', 'k', 'yellow')],
    captions={
        'if numFriends == 1': '`numFriends = {numFriends}`：不是 1，需要真的分割；为 1 时只能不分，答案是整个 `s`',
        'n = len(s)': '`n = {n}`：其余 `numFriends - 1` 段至少各 1 个字母，所以答案长度至多 `n - numFriends + 1 = {n - numFriends + 1}`',
        'i, j = 0, 1': '先算字典序最大的==后缀==：`i` 是当前最大后缀的起点，`j` 是待比较的候选起点',
        'while j < n': lambda S, B, r: (f'`j = {S.j} < n = {S.n}`：还有候选后缀要比' if S.j < S.n
                                        else f'`j = {S.j} >= n`：所有候选都比完，最大后缀从 `i = {S.i}` 开始'),
        'k = 0': '从 0 开始比较 `s[i:]` 和 `s[j:]` 的公共前缀长度',
        'while j + k < n and s[i + k] == s[j + k]': lambda S, B, r: (
            f"`s[{S.i + S.k}] = {S.s[S.i + S.k]}` == `s[{S.j + S.k}] = {S.s[S.j + S.k]}` → 前缀还一样，继续比" if S.j + S.k < S.n and S.s[S.i + S.k] == S.s[S.j + S.k]
            else (f"`j + k = {S.j + S.k}` 到末尾了，比较结束" if S.j + S.k >= S.n
                  else f"`s[{S.i + S.k}] = {S.s[S.i + S.k]}` ≠ `s[{S.j + S.k}] = {S.s[S.j + S.k]}` → 找到第一个不同的字母")),
        'k += 1': '公共前缀长度 `k` → {k}',
        'if j + k < n and s[i + k] < s[j + k]': lambda S, B, r: (
            f"`s[{S.i + S.k}] = {S.s[S.i + S.k]}` < `s[{S.j + S.k}] = {S.s[S.j + S.k]}` → ==j 开头的后缀更大==" if S.j + S.k < S.n and S.s[S.i + S.k] < S.s[S.j + S.k]
            else (f"`j + k = {S.j + S.k}` 到头了：`j` 后缀是 `i` 后缀的前缀，不会更大" if S.j + S.k >= S.n
                  else f"`s[{S.i + S.k}] = {S.s[S.i + S.k]}` > `s[{S.j + S.k}] = {S.s[S.j + S.k]}` → `i` 后缀更大，保留")),
        'i, j = j, max': '更新最优起点 `i = {i}`；`j = max({B.j}+1, {B.i}+{k}+1) = {j}`：公共前缀内的位置不可能更优，直接跳过',
        'j += k + 1': 'j 开头的后缀不更大；`s[j..j+k]` 起头的后缀也都不会超过 `i`，一口气跳过：`j` → {j}',
        'return s[i:': lambda S, B, r: f"最大后缀从 `i = {S.i}` 开始，截取长度 `{S.n - S.numFriends + 1}`，答案 `{r}`",
    },
    cards=dict(
        one_liner='答案是字典序最大的后缀，截取到长度 n−k+1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把 `word` 分成 `numFriends` 个非空子串，所有分法的所有子串放进盒子',
                 '求盒子中==字典序最大==的子串',
                 '示例：`word = "dbca"`，`numFriends = 2` → `"dbc"`；本视频：`"cacbcacb"`，`3` → `"cbcacb"`'],
        quote='如果固定子串的左端点，那么子串越长，字典序越大。……也可以先把字典序最大的后缀算出来，然后取它的长度至多为 n−k+1 的前缀，作为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['左端点固定时越长越大，但长度至多 `n − (k−1)`（其余 `k−1` 段各留 1 个字母）',
              '所以答案 = 字典序最大后缀的前 `n−k+1` 位；`k = 1` 时答案是 `s` 本身',
              '最大后缀用双指针 `i, j` 在 `O(n)` 内求出（同 1163 题）'],
        result='最大后缀 `"cbcacb"`，长度恰好 `n−k+1 = 6` → `"cbcacb"` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`numFriends == 1` 必须特判：不能分割，答案是整个 `s`',
                 '`i, j = j, max(j+1, i+k+1)`：跳过公共前缀，保证线性',
                 '方法一：枚举左端点，取 `s[i: i+n-k+1]` 的最大值，`O(n(n−k))`，写法更短，本视频演示方法二'],
    ),
)
