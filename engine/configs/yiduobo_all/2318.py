N = 6
NB = ['2 3 4 5 6', '1 3 5', '1 2 4 5', '1 3 5', '1 2 3 4 6', '1 5']   # 与 j+1 互质且不同的数


def _idx(S):
    """正在写入 f[idx]（由行号推出），其它行返回 None"""
    ln = S.get('_line')
    return {28: 0, 29: 1, 30: 2, 31: 3, 32: 4, 33: 5}.get(ln)


def _col(S, i, v):
    k = _idx(S)
    return 'yellow' if k is not None and i == k else None


MULT = [4, 2, 3, 2, 4, 1]


def _fj(j):
    def f(S, B, ret):
        ks = [int(x) - 1 for x in NB[j].split()]
        tot = sum(S.g[k] for k in ks)
        return (f'长度 `{S.index + 1}`、以 `{j + 1}` 结尾：上一轮 `g` 里可接的 `{NB[j]}` 求和 `{tot}`，'
                f'再减 `{MULT[j]} × {B.f[j]}`（上上轮）→ ==`{S.f[j]}`==')
    return f


def _gpost(S, B, ret):
    return f'第 2 轮 `g = {S.g}`：以 `j+1` 结尾，上一个数只需与它互质且不同，个数就是 `len(g_set[j])`'


def _g(S, B, ret):
    if 'g' in S:
        return _gpost(S, B, ret)
    return '第 2 轮：`g[j]` = 上一个数可选的 `f` 之和（`f` 全是 1，所以就是个数）'


def _f3(S, B, ret):
    if S.f != B.f:
        return f'第 3 轮 `f = {S.f}`（总和 `{sum(S.f)}`，与 `n = 3` 直接返回的 66 一致）'
    return '第 3 轮：还没有“第 i-3 位”，要把 `g_set[j]` 个 `f[i-2][j]` 全部减掉（`- 5, - 3, - 4 ...`）'


CONFIG = dict(
    num=2318, title='不同骰子序列的数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='二维 DP + 滚动数组（手工展开）',
    tags=['难度分 2090'],
    code='''
class Solution(object):
    def distinctSequences(self, n):

        if n == 1:
            return 6
        elif n == 2:
            return 22
        elif n == 3:
            return 66
        else:
            f = [1] * 6
            g = [f[1] + f[2] + f[3] + f[4] + f[5],
                 f[0] + f[2] + f[4],
                 f[0] + f[1] + f[3] + f[4],
                 f[0] + f[2] + f[4],
                 f[0] + f[1] + f[2] + f[3] + f[5],
                 f[0] + f[4]]
            f = [g[1] + g[2] + g[3] + g[4] + g[5] - 5,
                 g[0] + g[2] + g[4] - 3,
                 g[0] + g[1] + g[3] + g[4] - 4,
                 g[0] + g[2] + g[4] - 3,
                 g[0] + g[1] + g[2] + g[3] + g[5] - 5,
                 g[0] + g[4] - 2]
            
            f, g = g, f
            mod = 10 ** 9 + 7
            for index in range(3, n):
                f[0] = (g[1] + g[2] + g[3] + g[4] + g[5] - 4 * f[0] + 4 * mod) % mod
                f[1] = (g[0] + g[2] + g[4] - 2 * f[1] + 2 * mod) % mod
                f[2] = (g[0] + g[1] + g[3] + g[4] - 3 * f[2] + 3 * mod) % mod
                f[3] = (g[0] + g[2] + g[4] - 2 * f[3] + 2 * mod) % mod
                f[4] = (g[0] + g[1] + g[2] + g[3] + g[5] - 4 * f[4] + 4 * mod) % mod
                f[5] = (g[0] + g[4] - f[5] + mod) % mod
            
                f, g = g, f
            
            return sum(g) % mod
''',
    call=f'Solution().distinctSequences({N})',
    expect=1472,
    views=[
        dict(type='text', size=26, h=80, fn=lambda S: ('`f[j] ← Σ g[k] − m·f[j]`，`m` = 可接的数的个数 − 1'
                                                       if 'mod' in S else '`f[j]` / `g[j]`：以数字 `j+1` 结尾的合法序列数')),
        dict(type='array', var='g', label='g（上一轮的方案数）', h=190, cell=110, index=True),
        dict(type='array', var='f', label='f（正在更新的一轮，黄 = 刚算出的）', h=190, cell=110, index=True, color=_col),
    ],
    watch=[('n', 'n', 'blue'), ('index', 'index', 'pink'), ('g', 'g', 'cyan'), ('f', 'f', 'yellow')],
    skip=list(range(13, 18)) + list(range(19, 24)),
    captions={
        'if n == 1': '`n = {n}` 超过 3：前三轮单独算，`n` 更大时进入 else',
        'elif n == 2': '`n = {n}` 也不是 2',
        'elif n == 3': '`n = {n}` 也不是 3，走 else 的递推',
        'f = [1] * 6': '第 1 轮：点数 1~6 都能当第一个，各 `1` 种',
        'g = [f[1]': _g,
        'f = [g[1]': _f3,
        'f, g = g, f': lambda S, B, r: ('交换：`f` 变成第 2 轮、`g` 变成第 3 轮；之后 `f` 里的旧值就是“上上轮”' if 'index' not in S
                                        else f'滚动：`g` ← 刚算出的第 `{S.index + 1}` 轮，`f` ← 上一轮，留给下一轮覆盖'),
        'mod = 10': '取模用的 `mod`',
        'for index': lambda S, B, r: (f'`index = {S.index}`：这一轮算长度 `{S.index + 1}`，用 `g`（长度 `{S.index}`）和 `f`（长度 `{S.index - 1}`）'
                                      if S.get('index') != B.get('index') else f'`g` 里就是长度 `{S.index + 1}` 的方案数，循环结束'),
        'f[0] = (': _fj(0), 'f[1] = (': _fj(1), 'f[2] = (': _fj(2),
        'f[3] = (': _fj(3), 'f[4] = (': _fj(4), 'f[5] = (': _fj(5),
        'return sum(g)': '`g` 六个数相加：`{g}` → =={ret}==',
    },
    cards=dict(
        one_liner='二维 DP：一轮的值只跟上一轮、上上轮有关，用两个数组滚动',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['掷骰子 `n` 次：相邻两数互质，相等的数下标差 `> 2`',
                 '求不同序列的总数，对 `10^9 + 7` 取模',
                 '本视频：`n = 6` → `1472`'],
        quote='f[i][j] = sum(f[i - 1][k]) - f[i - 2][j] * (len(g_set[j]) - 1)，其中k + 1属于g_set[j]',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]` = 前 `i` 次、最后一次点数是 `j+1` 的方案数；上一个数 `k+1` 要与它互质',
              '直接加 `f[i-1][k]` 会多算“倒数第三位是 `k+1`”的情况，推导后只需减 `f[i-2][j] × (m−1)`',
              '`i = 2`、`i = 3` 单独处理，之后六个公式写死，每轮 `f, g = g, f` 滚动'],
        summary=['时间 `O(n)`，空间 `O(1)`；前 3 轮手工算好（`n ≤ 3` 直接返回 6、22、66）',
                 '易错：减去的倍数 `4, 2, 3, 2, 4, 1` 对应 `m = 互质个数 − 1`；`+ k * mod` 防止取模前出现负数',
                 '原文可用矩阵快速幂加速（作者没实现）',
                 '对比灵神：灵神用循环 + `gcd` 生成转移；yiduobo 把六个转移手工展开'],
    ),
)
