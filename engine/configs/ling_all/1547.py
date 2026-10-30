def _cand(S):
    i, j, f, c = S['i'], S['j'], S['f'], S['cuts']
    return [(k, f[i][k] + f[k][j]) for k in range(i + 1, j)]


def _color(S, r, cc, v):
    if S.get('_line') != 10 or 'j' not in S or S['j'] < S['i'] + 2:
        return None
    i, j = S['i'], S['j']
    cand = _cand(S)
    best = min(cand, key=lambda t: t[1])[0]
    if (r, cc) == (i, j):
        return 'yellow'
    if (r, cc) in ((i, best), (best, j)):
        return 'green'
    if any((r, cc) in ((i, k), (k, j)) for k, _ in cand):
        return 'blue'
    return None


def _formula(S):
    if S.get('_line') != 10 or 'j' not in S or S['j'] < S['i'] + 2:
        return '`f[i][j]` = 切 `cuts[i]`~`cuts[j]` 这根棍子的最小成本；`i` 倒序、`j` 正序'
    i, j, c = S['i'], S['j'], S['cuts']
    cand = _cand(S)
    s = '，'.join(f'k={k}: {v}' for k, v in cand)
    best = min(v for _, v in cand)
    return f'棍长 `{c[j]} − {c[i]}` = {c[j] - c[i]}；第一刀 k 的 `f[i][k]+f[k][j]`：{s} → 最小 {best}，`f[{i}][{j}]` = =={S["f"][i][j]}=='


CONFIG = dict(
    num=1547, title='切棍子的最小成本', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='区间 DP（枚举第一刀）',
    tags=['灵神题单', '动态规划', '难度分 2116'],
    code='''
class Solution:
    def minCost(self, n: int, cuts: List[int]) -> int:
        cuts.sort()
        cuts = [0] + cuts + [n]

        m = len(cuts)
        f = [[0] * m for _ in range(m)]
        for i in range(m - 3, -1, -1):
            for j in range(i + 2, m):
                f[i][j] = min(f[i][k] + f[k][j] for k in range(i + 1, j)) + cuts[j] - cuts[i]
        return f[0][-1]
''',
    call='Solution().minCost(7, [5,3,1,4])',
    expect=16,
    skip=['for j in range'],
    views=[
        dict(type='array', var='cuts', label='cuts（含端点 0 和 n）', h=215, cell=80, pointers={'i': 'blue', 'j': 'pink'},
             window=('i', 'j')),
        dict(type='text', fn=_formula, size=24, h=110),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算，蓝 = 候选，绿 = 最优的第一刀）', h=360, cell=70,
             rows=lambda S: [str(x) for x in S['cuts']] if len(S['cuts']) == len(S['f']) else None,
             cols=lambda S: [str(x) for x in S['cuts']] if len(S['cuts']) == len(S['f']) else None,
             color=_color),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('m', 'm')],
    captions={
        'cuts.sort()': '先排序：这样 `cuts[i]`~`cuts[j]` 之间的切点是连续的一段 `{cuts}`',
        'cuts = [0]': '把木棍端点 `0` 和 `n` 也放进来：`{cuts}`',
        'm = len': '`m = {m}`，状态 `f[i][j]` = 左端点 `cuts[i]`、右端点 `cuts[j]` 的棍子的最小切割成本',
        'f = [[0]': '`f[i][i+1] = 0`：两端点之间没有切点，无需切割',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：算 `f[i][j]` 要用 `f[k][j]`（k > i）→ ==i 从大到小== 枚举' if S.get('i') != B.get('i')
                                           else '所有区间都算完了'),
        'f[i][j] = min': lambda S, B, r: (f'`j = {S.j}`：枚举第一刀 `k`，成本 = `f[i][k] + f[k][j]` + 棍长 `{S.cuts[S.j]} − {S.cuts[S.i]}`'
                                          f' → `f[{S.i}][{S.j}]` = =={S.f[S.i][S.j]}=='),
        'return f[0][-1]': '整根棍子 `{cuts[0]}~{cuts[-1]}` 的最小总成本 `f[0][{m-1}]` = =={ret}==',
    },
    cards=dict(
        one_liner='枚举第一刀切在哪，两段各自变成更小的子问题',
        complexity='时间 `O(m^3)`，空间 `O(m^2)`',
        problem=['长度为 `n` 的木棍，要在 `cuts` 的位置切开，每次切割成本 = 当前这根棍子的长度',
                 '可以任意安排切割顺序，求最小总成本',
                 '示例：`n = 7, cuts = [1,3,4,5]` → `16`'],
        quote='把 0 和 n 也视作切开的位置（木棍端点）……定义状态为 dfs(i,j)，表示切割一根左端点为 cuts[i]，右端点为 cuts[j] 的棍子的最小成本。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举第一刀切在 `cuts[k]`：棍子分成 `(i,k)` 和 `(k,j)` 两段，各自是相似的子问题',
              '`f[i][j] = min(f[i][k] + f[k][j]) + cuts[j] − cuts[i]`，棍长与 `k` 无关，提到外面',
              '1:1 翻译成递推：要用 `f[k][j]` 所以 `i` 倒序，要用 `f[i][k]` 所以 `j` 正序'],
        summary=['时间 `O(m^3)`：状态 `O(m^2)` × 枚举 `k` 的 `O(m)`，`m` 是加了端点后的长度',
                 '易错：别忘了先排序，再把 `0` 和 `n` 加进去；`i` 从 `m-3` 开始',
                 '灵神题解主推 `@cache` 记忆化搜索，这里演示的是它 1:1 翻译出的递推',
                 '同类区间 DP：1039 多边形三角剖分、1000 合并石头'],
    ),
)
