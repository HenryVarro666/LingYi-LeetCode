G0 = [[2, 0, 5], [1, 4, 0], [3, 0, 6]]


def _gcolor(S, r, c, v):
    i = S.get('i')
    if i is None:
        return None
    if c == i:
        return 'pink'
    if c == i - 1:
        return 'blue'
    return None


def _fcolor(S, j, k, v):
    if S.get('_line', 0) < 36 and 'i' not in S:
        return 'yellow' if (S.get('j') == j and S.get('k') == k) else None
    return 'yellow' if (S.get('j') == j and S.get('k') == k) else None


def _gtab(S, j, k, v):
    if S.get('i') is None:
        return None
    if S.get('k') is not None and S.get('j') is not None and j == S['k']:
        if S['k'] == 0 and S.get('t') == k:
            return 'yellow'
        return 'blue'
    return None


def _info(S):
    i = S.get('i')
    if i is None:
        return '先算前两列：`f[j][k]` = 第 1 列染 `j` 个、第 0 列染 `k` 个时的最大得分'
    j, k = S.get('j'), S.get('k')
    base = f'`i = {i}`：新加第 {i} 列。`f[j][k]`：第 {i} 列染 j 个，第 {i - 1} 列染 k 个'
    if j is None:
        return base
    return base + f'；现在 `j={j}`，`k={k}`'


CONFIG = dict(
    num=3225, title='网格图操作后的最大分数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='按列 DP · best 数组 + k=0 暴力',
    tags=['其他线性 DP', '多维 DP', '难度分 3028'],
    code='''
class Solution(object):
    def maximumScore(self, grid):

        n = len(grid)

        if n < 2:
            return 0
        
        s = [[0] * (n + 1) for _ in range(n)]
        for i in range(n):
            for j in range(n):
                s[i][j + 1] = s[i][j] + grid[j][i]

        best_f1 = [0] * (n + 1)
        best_f2 = [0] * (n + 1)
        f = [[0] * (n + 1) for _ in range(n + 1)]
        for j in range(n + 1):
            for k in range(n + 1):
                if j >= k:
                    f[j][k] = s[0][j] - s[0][k]
                    best_f1[j] = max(best_f1[j], f[j][k])
                else:
                    f[j][k] = s[1][k] - s[1][j]
                    best_f2[j] = max(best_f2[j], f[j][k])

        for i in range(2, n):
            g = f[:]
            f = [[0] * (n + 1) for _ in range(n + 1)]

            best_g1 = best_f1[:]
            best_g2 = best_f2[:]
            best_f1 = [0] * (n + 1)
            best_f2 = [0] * (n + 1)

            for j in range(n + 1):
                for k in range(n + 1):
                    if k == 0:
                        for t in range(n + 1):
                            if j >= t:
                                f[j][k] = max(f[j][k], g[k][t] + s[i - 1][j] - s[i - 1][t])
                            else:
                                f[j][k] = max(f[j][k], g[k][t])

                        best_f1[j] = max(best_f1[j], f[j][k])
                    
                    elif j >= k:
                        f[j][k] = max(f[j][k], best_g1[k] + s[i - 1][j] - s[i - 1][k])
                        best_f1[j] = max(best_f1[j], f[j][k])
                    
                    else:
                        f[j][k] = max(f[j][k], max(best_g1[k], best_g2[k]) + s[i][k] - s[i][j])
                        best_f2[j] = max(best_f2[j], f[j][k])

        return max(max(best_f1), max(best_f2))
''',
    call=f'Solution().maximumScore({G0!r})',
    expect=17,
    views=[
        dict(type='text', fn=_info, size=22, h=64),
        dict(type='grid', var='grid', h=170, cell=56, label='grid（蓝 = 第 i-1 列，粉 = 第 i 列）', color=_gcolor),
        dict(type='table', var='f', h=250, cell=56, label='f[j][k]（黄 = 正在算）', color=_fcolor,
             rows=['j=0', 'j=1', 'j=2', 'j=3'], cols=['k=0', 'k=1', 'k=2', 'k=3']),
        dict(type='table', var='g', h=250, cell=56, label='g = 上一列的 f（蓝 = 第 k 行是依据）', color=_gtab,
             rows=['0', '1', '2', '3'], cols=['0', '1', '2', '3']),
    ],
    watch=[('i', lambda S: S.get('i', ''), 'blue'), ('j', lambda S: S.get('j', ''), 'pink'),
           ('k', lambda S: S.get('k', ''), 'cyan'), ('t', lambda S: S.get('t', ''), 'orange')],
    captions={
        'if n < 2': '只有一列：左右没有邻居，得不到分，返回 0',
        'f[j][k] = s[0][j] - s[0][k]': '前两列，`j ≥ k`：第 0 列第 `k+1..j` 格得分 `s[0][{j}] - s[0][{k}]` = =={f[j][k]}==',
        'f[j][k] = s[1][k] - s[1][j]': '`j < k`：第 1 列第 `j+1..k` 格得分 `s[1][{k}] - s[1][{j}]` = =={f[j][k]}==',
        'g = f[:]': lambda S, B, r: f'前两列已按公式填好：较大那列多出的格子得分。现在加第 `{S.i}` 列：旧 `f` 存成 `g`，`best` 存成 `best_g1/2`（`t ≤ k` 与 `t > k` 的最大值）',
        'f[j][k] = max(f[j][k], g[k][t] + s[i - 1][j] - s[i - 1][t])': lambda S, B, r: (
            f'`k=0`（左列全白）暴力枚举 `t`：`j ≥ t`，第 {S.i - 1} 列第 `t+1..j` 格得分 → `g[0][{S.t}] + {S.s[S.i - 1][S.j] - S.s[S.i - 1][S.t]}`，`f[{S.j}][0]` = =={S.f[S.j][S.k]}=='),
        'f[j][k] = max(f[j][k], g[k][t])': lambda S, B, r: (
            f'`k=0`，`j < t`：中间列黑得更少，没有新得分 → 直接取 `g[0][{S.t}]`，`f[{S.j}][0]` = =={S.f[S.j][S.k]}=='),
        'f[j][k] = max(f[j][k], best_g1[k] + s[i - 1][j] - s[i - 1][k])': lambda S, B, r: (
            f'`0 < k ≤ j`：中间列（第 {S.i - 1} 列）第 `k+1..j` 格得分，最优的 `t ≤ k` 已存在 `best_g1[{S.k}]={S.best_g1[S.k]}` → `f[{S.j}][{S.k}]` = =={S.f[S.j][S.k]}=='),
        'f[j][k] = max(f[j][k], max(best_g1[k], best_g2[k])': lambda S, B, r: (
            f'`k > j`：第 {S.i} 列第 `j+1..k` 格得分，与 `t` 无关 → `max(best_g1, best_g2) + s[i][k] - s[i][j]` = =={S.f[S.j][S.k]}=='),
        'return max(max(best_f1)': '`best_f1`、`best_f2` 里的最大值就是答案 =={ret}==',
    },
    skip=['for j in range', 'for k in range', 'for t in range', 'best_f1[j] = max', 'best_f2[j] = max',
          'if j >= k', 'if j >= t', 'if k == 0', 'best_g1 =', 'best_g2 =', 'best_f1 = [0]', 'best_f2 = [0]',
          'f = [[0] * (n + 1) for _ in range(n + 1)]\n            best', 's[i][j + 1]', 'n = len(grid)', 'for i in range', 'f[j][k] = s[0][j]', 'f[j][k] = s[1][k]', 's = [[0]', 'f = [[0] * (n + 1) for _ in range(n + 1)]', 'best_f1 = [0] * (n + 1)'],
    max_steps=80,
    cards=dict(
        one_liner='f 记两列的黑格数；转移里 t 只在 k=0 时才暴力',
        complexity='时间 `O(n³)`，空间 `O(n²)`',
        problem=['每列可以从顶端染黑一段（也可以不染），染后某个白格左右至少有一个黑格就得分',
                 '求最大总分',
                 '示例：3×3 网格 `[[2,0,5],[1,4,0],[3,0,6]]` → `17`'],
        quote='对于 k < t ≤ j 以及 k ≤ j < t，都只需要考虑 k = 0 的情况，这样一来，就可以照常暴力枚举 t。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[j][k]`：前 i 列，最后一列染 `j` 个，左边那列染 `k` 个；得分都是某列里连续的格子，用列前缀和 `s` 取区间和',
              '直接枚举再左一列的黑格数 `t`，是 `O(n⁴)`；`best1/best2` 记下 `t ≤ k` 与 `t > k` 的最大值',
              '中间列染得比两边都少时不如全白，所以只有 `k=0` 才暴力枚举 `t`'],
        summary=['时间 `O(n³)`，空间 `O(n²)`（`f`、`best` 只与上一轮有关，滚动更新）',
                 '易错点：`s[i]` 是第 `i` 列的前缀和（`s[i][j+1] = s[i][j] + grid[j][i]`），不是行',
                 '`k = 0` 与 `k > 0` 的转移不同，别漏了 `best_f1` 的更新',
                 '原文本身是 Python 3 兼容写法，没有修改'],
    ),
)
