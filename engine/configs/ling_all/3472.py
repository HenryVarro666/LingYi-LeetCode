S0 = 'abc'
K0 = 1


def _sd(S):
    return ''.join(map(chr, S['s'])) if 's' in S and S['s'] and isinstance(S['s'][0], int) else S0


def _ok(S):
    return all(k in S for k in ('k', 'i', 'j', 'f')) and S.get('_line', 0) >= 14


def _cell(S, r, c, v):
    if not _ok(S):
        return None
    i, j = S['i'], S['j']
    if r == i and c == j:
        return 'yellow'
    if j > i and (r, c) in ((i + 1, j), (i, j - 1)):
        return 'blue'
    return None


def _formula(S):
    if not _ok(S) or S['j'] <= S['i']:
        return '`f[k][i][j]` = 最多 `k` 次操作，`s[i..j]` 的最长回文子序列长度'
    k, i, j, s = S['k'], S['i'], S['j'], S['s']
    d = abs(s[i] - s[j])
    op = min(d, 26 - d)
    if op <= k:
        return f'`k={k}`：配对要 `op={op}` ≤ k → 可选 `f[{k - op}][{i + 1}][{j - 1}] + 2`'
    return f'`k={k}`：配对要 `op={op}` > k → 只能放弃一端'


def _cap_op(S, B, ret):
    k, i, j, s = S.k, S.i, S.j, S.s
    d = abs(s[i] - s[j])
    op = min(d, 26 - d)
    return (f'`{chr(s[i])}` 变 `{chr(s[j])}`：`d={d}`，直接走 `{d}` 步，绕过 z→a 要 `{26 - d}` 步 → `op = {op}`')


def _cap_cmp(S, B, ret):
    k, i, j, op = S.k, S.i, S.j, S.op
    if op <= k:
        return f'`op = {op} ≤ k = {k}`：次数够，可以把两端变成一样，两端==都选=='
    return f'`op = {op} > k = {k}`：次数不够，不能配对，只能放弃 `s[i]` 或 `s[j]`'


CONFIG = dict(
    num=3472, title='至多 K 次操作后的最长回文子序列', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='区间 DP 多一维剩余操作数',
    tags=['灵神题单', '动态规划', '难度分 1884'],
    code='''
class Solution:
    def longestPalindromicSubsequence(self, s: str, K: int) -> int:
        s = list(map(ord, s))  # 避免频繁计算 ord
        n = len(s)
        cnt = 0
        for i in range(n // 2):
            d = abs(s[i] - s[-1 - i])
            cnt += min(d, 26 - d)
        if cnt <= K:
            return n

        f = [[[0] * n for _ in range(n)] for _ in range(K + 1)]
        for k in range(K + 1):
            for i in range(n - 1, -1, -1):
                f[k][i][i] = 1
                for j in range(i + 1, n):
                    res = max(f[k][i + 1][j], f[k][i][j - 1])
                    d = abs(s[i] - s[j])
                    op = min(d, 26 - d)
                    if op <= k:
                        res = max(res, f[k - op][i + 1][j - 1] + 2)
                    f[k][i][j] = res
        return f[K][0][-1]
''',
    call=f'Solution().longestPalindromicSubsequence({S0!r}, {K0})',
    expect=2,
    skip=['for j in range', 'd = abs(s[i] - s[-1 - i])', 'cnt = 0', 'd = abs(s[i] - s[j])'],
    max_steps=90,
    views=[
        dict(type='string', var=_sd, label='s（蓝 = i，粉 = j）', h=200, cell=80, pointers={'i': 'blue', 'j': 'pink'}),
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='table', var='f[k]', label='当前这一层 f[k][i][j]（黄 = 正在算，蓝 = 放弃一端时依赖的格子）', h=380, cell=70,
             rows=lambda S: [f'{k}{c}' for k, c in enumerate(S0)], cols=lambda S: [f'{k}{c}' for k, c in enumerate(S0)],
             color=_cell),
    ],
    watch=[('k', 'k', 'green'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('op', 'op', 'orange'), ('res', 'res', 'yellow')],
    captions={
        'list(map(ord': '先把字符转成 ASCII 码，后面算距离不用反复 `ord`',
        'if cnt <= K': lambda S, B, r: f'把 `s` 整个改成回文要 `{S.cnt}` 次，`K = {S.K}`：不够，继续做 DP' if S.cnt > S.K else f'`cnt = {S.cnt} ≤ K`：整串都能改成回文，直接返回 `n`',
        'f = [[[0]': '`f[k][i][j]`：最多 `k` 次操作时 `s[i..j]` 的答案；==k 放第一维==，只会访问相近的几层',
        'for k in range': lambda S, B, r: (f'`k = {S.k}`：枚举操作次数上限，`f[k - op]` 的层更小，已经算过' if S.get('k') != B.get('k') else '各层都算完了'),
        'for i in range(n - 1': lambda S, B, r: (f'`i = {S.i}`：`i` 从大到小，保证 `f[·][i+1][·]` 已算好' if S.get('i') != B.get('i') or S.get('k') != B.get('k') else '这一层的所有区间都算完了'),
        'f[k][i][i] = 1': '`f[{k}][{i}][{i}] = 1`：单个字母本身就是回文',
        'res = max(f[k][i + 1][j]': '先看放弃一端：`max(f[{k}][{i+1}][{j}], f[{k}][{i}][{j-1}])` = `{res}`',
        'd = abs': '两端字母距离 `d = |s[i] - s[j]|` = `{d}`',
        'op = min': _cap_op,
        'if op <= k': _cap_cmp,
        'res = max(res, f[k - op]': '配对：剩 `{k} - {op}` 次，里面 `s[{i+1}..{j-1}]` 的答案 + 2，`res` = =={res}==',
        'f[k][i][j] = res': '`f[{k}][{i}][{j}] = {res}`',
        'return f[K][0][-1]': '`f[{K}][0][{n-1}]`：整串、最多 `K` 次操作 → =={ret}==',
    },
    cards=dict(
        one_liner='区间 DP 再带一维：还剩几次操作，配对就花 min(d, 26-d)',
        complexity='时间 `O(n^2 k)`，空间 `O(n^2 k)`',
        problem=['字符串 `s` 和整数 `k`：每次可把一个字符改成字母表相邻的字母（循环，z 后面是 a）',
                 '最多 `k` 次操作后，求 `s` 的==最长回文子序列==长度',
                 '示例：`s = "abced"`，`k = 2` → `3`；本视频：`"abc"`，`k = 1` → `2`'],
        quote='在 516 题的基础上，增加一个参数 k，表示剩余操作次数。……把 s[i] 和 s[j] 都变成一样的，设操作 op 次且 op ≤ k，那么问题变成 dfs(i+1,j-1,k-op)+2。',
        quote_src='—— 灵茶山艾府题解',
        idea=['和 516 一样看两端：不选 `s[i]`、不选 `s[j]`，或者把两端改成一样',
              '改成一样的代价：`d = |s[i]-s[j]|`，`op = min(d, 26-d)`，后者是绕过 z→a',
              '代价从剩余次数里扣：`f[k-op][i+1][j-1] + 2`'],
        summary=['时间、空间都是 `O(n^2 k)`',
                 '提前判断：整串改成回文要 `cnt` 次，`cnt ≤ K` 直接返回 `n`',
                 '把 `k` 放第一维：只访问最近的几层，减少 cache miss',
                 '易错：`op` 要取 `min(d, 26 - d)`；`i` 倒序、`j` 正序',
                 '另一种写法：记忆化搜索 `dfs(i,j,k)`，与递推 1:1 对应'],
    ),
)
