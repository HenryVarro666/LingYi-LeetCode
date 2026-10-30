def _center(S):
    if 'i' not in S or 'l' not in S:
        return '枚举 `i = 0 … 2n-2`：`l = ⌊i/2⌋`，`r = ⌊(i+1)/2⌋`'
    i = S['i']
    a, b = i // 2, (i + 1) // 2
    kind = f'奇回文，中心 `s[{a}]`' if a == b else f'偶回文，中心 `s[{a}]` 和 `s[{b}]` 之间'
    l, r = S['l'], S['r']
    pal = f'，当前回文 `s[{l + 1}..{r - 1}] = "{S["s"][l + 1:r]}"`' if r - l - 1 > 0 else ''
    return f'i = {i}：{kind}{pal}'


def _while_cap(S, B, ret):
    l, r, s, n = S.l, S.r, S.s, S.n
    if l < 0:
        return f'`l = {l}` 出界 → 停'
    if r >= n:
        return f'`r = {r}` 出界 → 停'
    if s[l] != s[r]:
        return f'`s[{l}] = {s[l]}` ≠ `s[{r}] = {s[r]}` → ==停止扩展=='
    if l == r:
        return f'单个字母 `{s[l]}` 本身是回文 → 往外扩'
    return f'`s[{l}] = s[{r}] = {s[l]}`，中间已是回文 → `s[{l}..{r}]` ==也是回文=='


def _if_cap(S, B, ret):
    l, r = S.l, S.r
    cur, best = r - l - 1, S.ans_right - S.ans_left
    if cur == 0:
        return '没扩出回文（空串）→ 跳过'
    head = f'回文 `s[{l + 1}..{r - 1}]` 长 `r-l-1 = {cur}`，答案长 `{best}`'
    return head + (' → ==更新==' if cur > best else ' → 不更新')


CONFIG = dict(
    num=5, title='最长回文子串', difficulty='Medium', category='多维动态规划',
    author='灵茶山艾府', technique='中心扩展法（奇偶合二为一）',
    code='''
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        ans_left = ans_right = 0

        for i in range(2 * n - 1):
            l, r = i // 2, (i + 1) // 2
            while l >= 0 and r < n and s[l] == s[r]:
                l -= 1
                r += 1
            # 循环结束后，s[l+1] 到 s[r-1] 是回文串
            if r - l - 1 > ans_right - ans_left:
                ans_left, ans_right = l + 1, r  # 左闭右开区间

        return s[ans_left: ans_right]
''',
    call='Solution().longestPalindrome("babad")',
    expect='bab',
    skip=['for i in range(2 * n - 1)', 'l -= 1'],
    views=[
        dict(type='text', fn=_center, h=64),
        dict(type='string', var='s', label='s（框 = 已确认的回文 s[l+1..r-1]）', pointers={'l': 'blue', 'r': 'pink'},
             window=('l + 1', 'r - 1'), cell=100, h=270),
        dict(type='string', var='s', label='答案 s[ans_left : ans_right]（左闭右开）',
             color=lambda S, i, v: 'green' if S['ans_left'] <= i < S['ans_right'] else None, cell=100, h=190),
    ],
    watch=['i', ('l', 'l', 'blue'), ('r', 'r', 'pink'), 'ans_left', 'ans_right',
           ('答案', 's[ans_left:ans_right]', 'green')],
    captions={
        'n = len(s)': '`n = {n}`：一共 `2n - 1 = {2*n-1}` 个回文中心（`n` 个字母 + `n-1` 个缝隙）',
        'ans_left = ans_right = 0': '答案用==左闭右开==区间 `[ans_left, ans_right)` 记录，先是空串',
        'l, r = i // 2': lambda S, B, ret: (
            f'`i = {S.i}` 偶数 → ==奇回文==，`l = r = {S.l}`' if S.l == S.r else
            f'`i = {S.i}` 奇数 → ==偶回文==，`l = {S.l}, r = {S.r}`'),
        'while l >= 0': _while_cap,
        'r += 1': '向外扩一圈：`l = {l}`，`r = {r}`',
        'if r - l - 1 >': _if_cap,
        'ans_left, ans_right = l + 1, r': '答案 = `[{ans_left}, {ans_right})` = =={s[ans_left:ans_right]}==（左闭右开，右端存 `r`）',
        'return s[ans_left': '返回 `s[{ans_left}:{ans_right}]` = =={ret}==（`"aba"` 一样长，但没有更长，所以不替换）',
    },
    cards=dict(
        one_liner='从回文中心向外扩展，每次 O(1) 判断更长的子串',
        complexity='时间 `O(n²)`，空间 `O(1)`',
        problem=['给你一个字符串 `s`，找到 `s` 中==最长的回文子串==',
                 '示例：`s = "babad"` → `"bab"`（`"aba"` 也对）',
                 '示例：`s = "cbbd"` → `"bb"`'],
        quote='能不能 O(1) 判断一个子串是不是回文的？……如果中间的 bcb 是回文串，那么我们就能 O(1) 地知道 abcba 是回文串。既然如此，==为什么不直接从 c 开始向外扩展呢？==',
        quote_src='—— 灵茶山艾府题解',
        idea=['暴力：`O(n²)` 个子串 × `O(n)` 判断 = `O(n³)`，太慢',
              '回文 = ==两端相同 + 中间是回文== → 从中心往外扩，每扩一步 `O(1)` 判断',
              '奇回文从 `l = r = i` 出发，偶回文从 `l = i, r = i+1` 出发',
              '合二为一：枚举 `i = 0 … 2n-2`，`l = ⌊i/2⌋`，`r = ⌊(i+1)/2⌋`'],
        summary=['时间 `O(n²)`，空间 `O(1)`；`2n-1` 个中心，每个最多扩 `O(n)` 次',
                 '易错：循环结束时 `s[l]`、`s[r]` 已经不匹配，回文是 `s[l+1..r-1]`，长度 `r-l-1`',
                 '「两端相同 + 中间回文」正是区间 DP 的转移，中心扩展省掉了二维表',
                 '原文还有：写法一奇偶分开枚举；Manacher 算法 `O(n)`'],
    ),
)
