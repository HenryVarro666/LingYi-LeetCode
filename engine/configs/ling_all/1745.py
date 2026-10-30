S0 = 'abcbdd'


def _mc_color(S, r, c, v):
    ln = S.get('_line')
    if 'min_change' not in S or 'i' not in S:
        return None
    if ln in (7,) and 'j' in S and (r, c) == (S['i'], S['j']):
        return 'yellow'
    if ln in (11, 12) and 'l' in S and 'r' in S and c == S['r'] and r == S['l']:
        return 'yellow'
    if v == 0 and c >= r and ln not in (7,):
        return None
    return None


def _f_color(S, k, v):
    if S.get('_line') in (12, 13) and 'r' in S and k == S['r']:
        return 'yellow'
    return None


def _txt(S):
    ln = S.get('_line')
    if 'min_change' not in S:
        return '把 `s` 分成 3 段，每段都是回文 ⇔ 最少修改次数 = 0'
    if 'l' in S and 'r' in S and 'i' in S and ln in (12, 13):
        return f"第 {S['i'] + 1} 段取 `s[{S['l']}..{S['r']}]`：`f[{S['l'] - 1}] + min_change[{S['l']}][{S['r']}]`"
    if 'j' in S and 'i' in S and ln == 7:
        return f"`min_change[{S['i']}][{S['j']}]`：把 `s[{S['i']}..{S['j']}]` 改成回文的最少次数"
    return '`min_change[i][j]`：把 `s[i..j]` 改成回文串的最少修改次数'


CONFIG = dict(
    num=1745, title='分割回文串 IV', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP · 复用 1278 分割成 k 段',
    tags=['灵神题单·动态规划', '灵神题单·字符串'],
    code='''
class Solution:
    # 1278. 分割回文串 III
    def palindromePartition(self, s: str, k: int) -> int:
        n = len(s)
        min_change = [[0] * n for _ in range(n)]
        for i in range(n - 2, -1, -1):
            for j in range(i + 1, n):
                min_change[i][j] = min_change[i + 1][j - 1] + (1 if s[i] != s[j] else 0)

        f = min_change[0]
        for i in range(1, k):
            for r in range(n - k + i, i - 1, -1):
                f[r] = min(f[l - 1] + min_change[l][r] for l in range(i, r + 1))
        return f[-1]

    def checkPartitioning(self, s: str) -> bool:
        return self.palindromePartition(s, 3) == 0
''',
    call=f'Solution().checkPartitioning({S0!r})',
    expect=True,
    skip=['for j in range', 'n = len(s)'],
    max_steps=80,
    views=[
        dict(type='string', var='s', label='s', h=150, cell=80),
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='table', var='min_change', label='min_change[i][j]（黄 = 正在用 / 正在算）', h=330, cell=60,
             rows=lambda S: [f'{k}{c}' for k, c in enumerate(S0)], cols=lambda S: [f'{k}{c}' for k, c in enumerate(S0)],
             color=_mc_color),
        dict(type='array', var='f', label='f（就是 min_change[0]，f[r] = 把 s[0..r] 分成 i+1 段的最少修改）', h=190, cell=80,
             pointers={'r': 'pink'}, color=_f_color),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('l', 'l', 'cyan'), ('r', 'r', 'pink')],
    captions={
        'min_change = [[0]': '`min_change[i][j]` = 把 `s[i..j]` 变成回文串的最少修改次数',
        'for i in range(n - 2': lambda S, B, ret: (f'`i = {S.i}`：算 `[i][·]` 要用 `[i+1][·]` → ==i 倒序==' if S.get('i') != B.get('i') else '区间都算完了'),
        'min_change[i][j] =': '`s[{i}] = {s[i]}`，`s[{j}] = {s[j]}`：{"相同，不用改" if s[i] == s[j] else "不同，要改 1 次"} → `min_change[{i}][{j}]` = =={min_change[i][j]}==',
        'f = min_change[0]': '`f` 直接复用第 0 行：`f[r]` 就是把 `s[0..r]` 分成 ==1 段==的最少修改',
        'for i in range(1, k)': lambda S, B, ret: (f'开始划分第 `{S.i + 1}` 段（共 k = {S.k} 段）' if S.get('i') != B.get('i') or 'i' not in B else '分段结束'),
        'for r in range': lambda S, B, ret: (f'`r = {S.r}`：前 `r + 1` 个字符分成 `{S.i + 1}` 段' if S.get('r') != B.get('r') or 'r' not in B else '这一段的所有 `r` 都算完了'),
        'f[r] = min(': '枚举最后一段起点 `l`，取 `f[l-1] + min_change[l][r]` 最小：`f[{r}]` = =={f[r]}==',
        'return f[-1]': '`f[-1]` = 整个 `s` 分成 3 段的最少修改 = =={ret}==，等于 0 说明三段都是回文',
        'return self.palindromePartition': '调用 1278 的 `palindromePartition(s, 3)`，再判断返回值是不是 `0`',
    },
    cards=dict(
        one_liner='分成 k 段回文，就是最少修改次数为 0',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['给你字符串 `s`，判断能否分成 ==三个非空回文子串==',
                 '示例：`"abcbdd"` = `"a"` + `"bcb"` + `"dd"` → `true`',
                 '`"bcbddxy"` → `false`；本视频用 `"abcbdd"`'],
        quote='如果最少修改次数等于 0，那么每段都是回文串。所以直接调用 1278 题的代码，判断返回值是否为 0 即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['进阶：分成 `k` 段都是回文？本题是 `k = 3`',
              '1278 题已算出“分成 k 段的最少修改次数”：先预处理任意区间改成回文的代价',
              '再用划分型 DP 枚举最后一段起点，最后看结果是不是 `0`'],
        result='分成 3 段的最少修改次数为 0 → `True` ✓',
        summary=['时间 `O(n^2 + (n-k)^2·k)`，`k = 3`，空间 `O(n^2)`',
                 '复用 1278：同一份代码也能解分成 4 段、5 段的问题',
                 '`f = min_change[0]` 直接复用第一行当“分成 1 段”的状态',
                 '易错：`r` 要倒序且下界是 `i`，保证每段非空、`f[l-1]` 还没被覆盖'],
    ),
)
