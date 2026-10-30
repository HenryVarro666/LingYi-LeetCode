W1, W2, TG = 'ab', 'ab', 'ab'
HID = (24, 28, 36)
ROWS = ['×', '∅'] + [W1[:k] for k in range(1, len(W1) + 1)]
COLS = ['×', '∅'] + [W2[:k] for k in range(1, len(W2) + 1)]


def _cells(S):
    """当前格 (j+1, k+1)；返回 (j, k) 或 None"""
    j, k = S.get('j'), S.get('k')
    if S.get('_line', 0) in (14, 16, 18, 19) and j is not None and k is not None:
        return j, k
    return None


def _nf_color(S, a, b, v):
    if a == 0 or b == 0:
        return HID
    jk = _cells(S)
    if jk is None:
        return None
    j, k = jk
    if (a, b) == (j + 1, k + 1):
        return 'yellow'
    if S.get('_line') == 14 and (a, b) in ((j, k + 1), (j + 1, k), (j, k)):
        return 'blue'
    return None


def _f_color(S, a, b, v):
    if a == 0 or b == 0:
        return HID
    jk = _cells(S)
    if jk is None:
        return None
    j, k = jk
    ln = S.get('_line')
    if ln == 16 and (a, b) in ((j, k + 1), (j, k)):
        return 'blue'
    if ln == 18 and (a, b) in ((j + 1, k), (j, k)):
        return 'blue'
    return None


def _f14(S, B, ret):
    j, k = S.j, S.k
    return (f'算 `nf[{j+1}][{k+1}]`。==容斥==：`nf[{j}][{k+1}] + nf[{j+1}][{k}] − nf[{j}][{k}]` '
            f'= {S.nf[j][k+1]} + {S.nf[j+1][k]} − {S.nf[j][k]} = =={S.res}==')


def _f16(S, B, ret):
    j, k = S.j, S.k
    return (f'`word1[{j-1}] = {S.ch}` 匹配 `target[{S.i}]`：其余 word1 前 {j-1} 个、word2 前 {k} 个，且 word2 末尾要用上 → '
            f'`f[{j}][{k+1}] − f[{j}][{k}]` = {S.f[j][k+1]} − {S.f[j][k]}，`res` = =={S.res}==')


def _f18(S, B, ret):
    j, k = S.j, S.k
    return (f'`word2[{k-1}] = {S.ch}` 匹配 `target[{S.i}]`：其余 word1 前 {j} 个、word2 前 {k-1} 个，且 word1 末尾要用上 → '
            f'`f[{j+1}][{k}] − f[{j}][{k}]` = {S.f[j+1][k]} − {S.f[j][k]}，`res` = =={S.res}==')


CONFIG = dict(
    num=3981, title='统计从两个字符串形成目标字符串的不同方案数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='三维 DP · 容斥 · 滚动数组',
    tags=['灵神题单·动态规划', '难度分 2128'],
    code='''
class Solution:
    def interleaveCharacters(self, word1: str, word2: str, target: str) -> int:
        MOD = 1_000_000_007
        m1, m2 = len(word1), len(word2)
        f = [[0] * (m2 + 2) for _ in range(m1 + 2)]
        for j in range(1, m1 + 2):
            for k in range(1, m2 + 2):
                f[j][k] = 1

        for i, ch in enumerate(target):
            nf = [[0] * (m2 + 2) for _ in range(m1 + 2)]
            for j in range(m1 + 1):
                for k in range(max(0, i + 1 - j), m2 + 1):
                    res = nf[j][k + 1] + nf[j + 1][k] - nf[j][k]
                    if j > 0 and word1[j - 1] == ch:
                        res += f[j][k + 1] - f[j][k]
                    if k > 0 and word2[k - 1] == ch:
                        res += f[j + 1][k] - f[j][k]
                    nf[j + 1][k + 1] = res % MOD
            f = nf

        return (f[m1 + 1][m2 + 1] - f[m1 + 1][1] - f[1][m2 + 1]) % MOD
''',
    call=f'Solution().interleaveCharacters({W1!r}, {W2!r}, {TG!r})',
    expect=2,
    skip=['for j in range', 'for k in range', 'f[j][k] = 1', 'if j > 0 and', 'if k > 0 and', 'MOD = ', 'm1, m2 =', 'nf = [[0]', 'f = nf'],
    max_steps=100,
    views=[
        dict(type='string', var='target', label='target（i 指向正在匹配的字符 ch）', h=120, cell=70,
             color=lambda S, k, v: 'blue' if k == S.get('i') else None),
        dict(type='table', var='f', label='f：上一轮（target 前 i 个字符）；行 = word1 前缀，列 = word2 前缀', h=250, cell=50,
             rows=ROWS, cols=COLS, color=_f_color),
        dict(type='table', var='nf', label='nf：这一轮（target 前 i+1 个字符），黄 = 正在算，蓝 = 容斥用到的格子', h=250, cell=50,
             rows=ROWS, cols=COLS, color=_nf_color),
    ],
    watch=[('i', 'i', 'blue'), ('ch', 'ch', 'blue'), ('j', 'j', 'cyan'), ('k', 'k', 'pink'), ('res', 'res', 'orange')],
    captions={
        5: '行/列 = word1/word2 前缀长度 `+1`；第 0 行/列是出界，恒为 0',
        'for i, ch in enumerate': lambda S, B, r: (
            ('初始 `f[j][k] = 1`：空 target 只有 1 种凑法。开始匹配 `target[0] = ' + S.ch + '`') if S.i == 0 and B.get('i') is None
            else (f'`i = {S.i}`：开始匹配 `target[{S.i}] = {S.ch}`，`f` 已经是上一轮的结果' if S.get('i') is not None and S.get('i') != B.get('i')
                  else '`target` 全部匹配完，看最后的 `f`')),
        'res = nf[j][k + 1]': _f14,
        'res += f[j][k + 1]': _f16,
        'res += f[j + 1][k]': _f18,
        'nf[j + 1][k + 1] = res': '`nf[{j+1}][{k+1}] = {res} % MOD` = =={nf[j+1][k+1]}==',
        'return (f[m1 + 1]': lambda S, B, r: f'`f[{S.m1+1}][{S.m2+1}]` = 允许任一方为空 = {S.f[S.m1+1][S.m2+1]}；减去只用 word1（`f[{S.m1+1}][1]` = {S.f[S.m1+1][1]}）和只用 word2（`f[1][{S.m2+1}]` = {S.f[1][S.m2+1]}） = =={r}=='

    },
    cards=dict(
        one_liner='允许一方为空 + 容斥算「都选」，最后减去只用一方的方案',
        complexity='时间 `O(n·m1·m2)`，空间 `O(m1·m2)`（滚动数组）',
        problem=['用 `word1`、`word2` 各取一个递增下标的子序列，拼出 `target`（逐字符选自其一）',
                 '要求两个单词==至少各选一个字符==，两种方案只要有一个位置来源不同就算不同',
                 '示例：`word1="abc", word2="bac", target="abc"` → `5`',
                 '本视频：`"ab"`、`"ab"`、`"ab"` → `2`'],
        quote='根据容斥原理，前三种情况的方案数之和为 dfs(i,j-1,k) + dfs(i,j,k-1) - dfs(i,j-1,k-1)。……情况四（word1[j] 和 word2[k] 都在 target 中）：要么 word1[j] 与 target[i] 匹配，要么 word2[k] 与 target[i] 匹配。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i,j,k)`：两个前缀里任选（可空）凑出 `target[0..i]` 的方案数',
              '对 `word1[j]`、`word2[k]` 选或不选，共 4 种；前 3 种用容斥合成一个式子',
              '「都选」时，必有一个去匹配 `target[i]`；另一个必须被用上，再用容斥减掉「它没被用」',
              '最后答案 = 两边允许为空的总数 − 只用 word1 − 只用 word2'],
        summary=['时间 `O(n·m1·m2)`，滚动数组空间 `O(m1·m2)`',
                 '易错：`k` 的起点 `max(0, i+1-j)`，字符不够凑时直接剪掉',
                 '易错：答案要减去只用一方的方案，别忘取模（`1e9+7`）',
                 '选最后的滚动数组写法；前面还有记忆化搜索、三维递推两种',
                 '同类：115 不同的子序列（只有一个单词）'],
    ),
)
