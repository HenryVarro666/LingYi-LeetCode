def _top(S):
    ln = S['_line']
    if ln <= 8:
        if 'i' in S and 'j' in S and ln >= 5:
            return f"`f[i+1][j]`：以 `s[{S['i']}]` 结尾的子串（倒序）与以 `t[{S['j']}]` 开头的子串的最长匹配长度"
        return '`f[i+1][j]`：以 `s[i]` 结尾的子串（倒序）与以 `t[j]` 开头的子串的最长匹配长度'
    if ln <= 10:
        return '`mx[i]` = `f[i]` 这一行的最大值；`|x| = |y|` 时答案 = 全局最大匹配 × 2'
    if 'l' in S and 'r' in S:
        l, r = S['l'], S['r']
        if l >= 0 and r < len(S['s']):
            return f"中心扩展：`s[{l}]` 与 `s[{r}]` 往两边比；回文 `s[{l + 1}..{r - 1}]` 之外，左边还能和 `t` 配 `mx[{l + 1}]` 对"
        return f"扩展停止：回文是 `s[{l + 1}..{r - 1}]`（长 {r - l - 1}）"
    return '|x| > |y|：枚举 s 的回文中心，回文越长越好'


def _fcolor(S, r, c, v):
    if S['_line'] > 8 or 'i' not in S or 'j' not in S:
        return None
    if r == S['i'] + 1 and c == S['j']:
        return 'yellow'
    if r == S['i'] and c == S['j'] + 1 and S['s'][S['i']] == S['t'][S['j']]:
        return 'blue'
    return None


def _scolor(S, i, v):
    if S['_line'] >= 13 and 'l' in S and 'r' in S:
        l, r = S['l'], S['r']
        if l + 1 <= i <= r - 1:
            return 'green'
    return None


CONFIG = dict(
    num=3504, title='子字符串连接后的最长回文串 II', difficulty='Hard', category='字符串',
    author='灵茶山艾府', technique='最长公共子串 DP + 中心扩展',
    tags=['灵神题单', '字符串', '难度分 2398'],
    code='''
class Solution:
    def calc(self, s: str, t: str) -> int:
        n, m = len(s), len(t)
        f = [[0] * (m + 1) for _ in range(n + 1)]
        for i, x in enumerate(s):
            for j, y in enumerate(t):
                if x == y:
                    f[i + 1][j] = f[i][j + 1] + 1
        mx = list(map(max, f))
        ans = max(mx) * 2  # |x| = |y| 的情况

        # 计算 |x| > |y| 的情况，中心扩展法
        for i in range(2 * n - 1):
            l, r = i // 2, (i + 1) // 2
            while l >= 0 and r < n and s[l] == s[r]:
                l -= 1
                r += 1
            if l + 1 <= r - 1:  # s[l+1] 到 s[r-1] 是非空回文串
                ans = max(ans, r - l - 1 + mx[l + 1] * 2)
        return ans

    def longestPalindrome(self, s: str, t: str) -> int:
        return max(self.calc(s, t), self.calc(t[::-1], s[::-1]))
''',
    call='Solution().longestPalindrome("abb", "a")',
    expect=4,
    max_steps=90,
    skip=['for i, x in enumerate(s)', 'for j, y in enumerate(t)', 'n, m = len(s)', 'for i in range(2 * n - 1)'],
    views=[
        dict(type='text', fn=_top, size=22, h=60),
        dict(type='string', var='s', label='s（青/粉 = 中心扩展的 l、r，绿 = 当前回文）', color=_scolor,
             pointers={'i if _line <= 8 else None': 'blue', 'l if _line >= 13 else None': 'cyan', 'r if _line >= 13 else None': 'pink'},
             pointer_labels={'i if _line <= 8 else None': 'i', 'l if _line >= 13 else None': 'l', 'r if _line >= 13 else None': 'r'}, cell=56, h=190),
        dict(type='string', var='t', label='t（蓝 = 当前比较的 t[j]）',
             color=lambda S, k, v: 'blue' if S['_line'] <= 8 and S.get('j') == k else None, cell=56, h=120),
        dict(type='grid', var='f', label='f（黄 = 当前格 f[i+1][j]，蓝 = 依赖的 f[i][j+1]）',
             rows=lambda S: list(range(len(S['f']))), cols=lambda S: list(range(len(S['f'][0]))), color=_fcolor, cell=52, h=270),
        dict(type='array', var='mx', label='mx[i] = max(f[i])', cell=56, h=130),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'blue'), ('l', 'l', 'cyan'), ('r', 'r', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'f = [[0]': '`f[i+1][j]`：以 `s[i]` 结尾的子串（==倒序==）与以 `t[j]` 开头的子串，最长能匹配多长；多开一行 `f[0]` 放初始值 0',
        'if x == y': lambda S, B, ret: (f"`s[{S.i}] = {S.x}` == `t[{S.j}] = {S.y}`：相等，可以接在更短的匹配上" if S.x == S.y
                                        else f"`s[{S.i}] = {S.x}` ≠ `t[{S.j}] = {S.y}`：`f[{S.i + 1}][{S.j}]` 保持 0"),
        'f[i + 1][j] = f[i][j + 1] + 1': '去掉这两个字母，剩下 `f[{i}][{j + 1}]`，再加 1 → `f[{i + 1}][{j}]` = =={f[i + 1][j]}==',
        'mx = list': '`mx[i]`：`f[i]` 这一行的最大值（以 `s[i-1]` 结尾的子串，最多能和 t 配多长）',
        'ans = max(mx)': '`|x| = |y|`：最长匹配 `{max(mx)}` 对，两边各一份 → `ans = {ans}`',
        'l, r = i // 2': '枚举回文中心 `i = {i}`（共 `2n-1` 个）：`l = {l}`，`r = {r}`（`l == r` 是奇回文，`l + 1 == r` 是偶回文）',
        'while l >= 0': lambda S, B, ret: (f"`s[{S.l}] = {S.s[S.l]}` == `s[{S.r}] = {S.s[S.r]}` → ==相等==，向两边扩" if S.l >= 0 and S.r < S.n and S.s[S.l] == S.s[S.r]
                                           else (f'`l = {S.l}` 或 `r = {S.r}` 越界，停止' if not (S.l >= 0 and S.r < S.n)
                                                 else f"`s[{S.l}] = {S.s[S.l]}` ≠ `s[{S.r}] = {S.s[S.r]}` → 停止")),
        'l -= 1': '`l` → {l}',
        'r += 1': '`r` → {r}',
        'if l + 1 <= r - 1': lambda S, B, ret: (f'回文是 `s[{S.l + 1}..{S.r - 1}]`，长 `{S.r - S.l - 1}`，非空 → ==可以作为 x 的后缀=='
                                                 if S.l + 1 <= S.r - 1 else '没有回文，跳过'),
        'ans = max(ans, r - l - 1': '回文 `{r - l - 1}` + 前面 `x\'` 与 `t` 的最长匹配 `mx[{l + 1}] × 2 = {mx[l + 1] * 2}` → 总长 `{r - l - 1 + mx[l + 1] * 2}`，`ans` = =={ans}==',
        'return ans': '这个方向（`|x| >= |y|`）的最长回文是 =={ret}==',
        'return max(self.calc': lambda S, B, ret: (f'两个方向取较大者 → =={ret}==' if ret is not None
                                                   else '先算 `calc(s, t)`（`|x| >= |y|`）；再算互换并翻转后的 `calc(t[::-1], s[::-1])`，覆盖 `|x| < |y|`'),
    },
    cards=dict(
        one_liner='分三种长度关系：|x| = |y| 用 DP，|x| > |y| 用中心扩展，|x| < |y| 翻转复用',
        complexity='时间 `O(nm + n^2 + m^2)`，空间 `O(n^2 + m^2)`',
        problem=['从 `s` 和 `t` 各选一个子串（可以为空），按顺序拼接',
                 '求能拼出的==最长回文串==的长度',
                 '示例：`s = "abcde"`，`t = "ecdba"` → `5`（`abc` + `ba`）；本视频：`s = "abb"`，`t = "a"` → `4`（`abb` + `a` = `abba`）'],
        quote='假设回文子串是 s[l+1] 到 s[r-1]，再加上以 s[l] 结尾的子串（倒序）与以 t[j] 开头的子串的最长匹配长度（乘以 2），可以得到一个长为 r-l-1 + 2·max f[l+1][j] 的回文串。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`|x| = |y|`：`y` 必须是 `x` 的翻转 → 类似最长公共子串的 DP，答案 = 最大匹配 × 2',
              '`|x| > |y|`：`x` 的某个后缀是回文，去掉它剩下的翻转后等于 `y` → 枚举回文中心，回文越长越好',
              '`|x| < |y|`：`s` 与 `t` 互换并翻转，重新调用同一个 `calc`'],
        result='`abb` + `a` = `abba`，长度 4 ✓',
        summary=['时间 `O(nm + n^2 + m^2)`，空间 `O(n^2 + m^2)`（滚动数组可降到线性）',
                 '`f` 多开一行：`f[0]` 放初始值，免去 `i = 0` 的特判',
                 '中心有 `2n - 1` 个：奇回文和偶回文都要枚举',
                 '另一种写法：后缀数组 + 高度数组 + Manacher，可做到 `O(n + m)`（题解附录）'],
    ),
)
