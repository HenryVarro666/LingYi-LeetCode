def _fcolor(S, r, c, v):
    i, j, k = S.get('i'), S.get('j'), S.get('k')
    if i is None or j is None or 'f' not in S:
        return None
    if r == i and c == j:
        return 'yellow'
    if k is not None and S.get('_line', 0) >= 14 and r == i + k and c == max(j, k):
        return 'pink'
    return None


def _fml(S):
    i, j, k = S.get('i'), S.get('j'), S.get('k')
    if i is None or j is None:
        return '`f[i][j]`：从第 i 堆开始、M=j 时，先手最多拿多少；`s` = `sum(piles[i:])`'
    n = len(S['piles'])
    if i + 2 * j >= n:
        return f'`i + 2j = {i + 2 * j} ≥ {n}` → 能全拿：`f[{i}][{j}] = s = {S["s"]}`'
    if k is None or S.get('_line', 0) < 14:
        return f'`i + 2j = {i + 2 * j} < {n}`：枚举拿 `k = 1..{2 * j}` 堆'
    return f'拿 `{k}` 堆：`s − f[{i + k}][{max(j, k)}]` = {S["s"]} − {S["f"][i + k][max(j, k)]} = =={S["s"] - S["f"][i + k][max(j, k)]}=='


CONFIG = dict(
    num=1140, title='石子游戏 II', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='先手最优 DP · 枚举拿几堆', tags=['动态规划', '数学算法', '难度分 2035'],
    code='''
class Solution(object):
    def stoneGameII(self, piles):

        n = len(piles)
        f = [[0] * (n + 1) for _ in range(n)]
        s = 0
        for i in range(n - 1, -1, -1):
            s += piles[i]
            for j in range(1, n + 1):
                if i + j * 2 >= n:
                    f[i][j] = s
                else:
                    for k in range(1, j * 2 + 1):
                        f[i][j] = max(f[i][j], s - f[i + k][max(j, k)])

        return f[0][1]
''',
    call='Solution().stoneGameII([2, 7, 9, 4])',
    expect=9,
    skip=['n = len', 'f = [[0]', 's = 0', 'for j in range', 'for k in range', 'for i in range'],
    max_steps=90,
    views=[
        dict(type='text', fn=_fml, size=24, h=50),
        dict(type='array', var='piles', label='piles', h=110, cell=70,
             color=lambda S, k, v: 'blue' if S.get('i') is not None and k >= S['i'] else None),
        dict(type='table', var='f', label='f[i][j]（行 i，列 j）', h=330, cell=60,
             rows=lambda S: list(range(len(S['piles']))), cols=lambda S: list(range(len(S['piles']) + 1)), color=_fcolor),
        dict(type='text', fn=lambda S: (f'后手接下来最多拿 `f[{S["i"] + S["k"]}][{max(S["j"], S["k"])}]`，剩下的全归先手' if S.get('k') is not None and S.get('_line', 0) >= 14 else ''), size=24, h=50),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('k', 'k', 'orange'), ('s', 's', 'green')],
    captions={
        's += piles[i]': '`s` = `sum(piles[{i}:])` = =={s}==：只与 `i` 有关，用变量迭代就行',
        'if i + j * 2 >= n': lambda S, B, r: (f'`i + 2j = {S.i + 2 * S.j}` ' + ('≥' if S.i + 2 * S.j >= len(S.piles) else '<') + f' `n = {len(S.piles)}` → ' + ('先手可以拿走后面所有石头' if S.i + 2 * S.j >= len(S.piles) else '拿不完，要枚举这一次拿几堆')),
        'f[i][j] = s': '`f[{i}][{j}] = s` = =={s}==',
        'f[i][j] = max': '拿 `k={k}` 堆：先手得 `s − f[{i+k}][max({j},{k})]` = {s} − {f[i+k][max(j,k)]} = {s - f[i+k][max(j,k)]}；当前最优 `f[{i}][{j}]` = =={f[i][j]}==',
        'return f[0][1]': '从第 0 堆、`M=1` 开始，先手最多 `f[0][1]` = =={ret}==',
    },
    cards=dict(
        one_liner='拿「前 X 堆」的博弈：f[i][j] = 剩余总数 − 后手的最优',
        complexity='时间 `O(n³)`，空间 `O(n²)`',
        problem=['石子排成一行，每次拿走前 `X` 堆（`1 ≤ X ≤ 2M`），然后 `M = max(M, X)`，Alice 先手',
                 '双方都最优，求 Alice 最多拿多少',
                 '示例：`[2,7,9,4,4]` → `10`；本视频：`[2,7,9,4]`'],
        quote='拿着摆明了就是动态规划的问题。令f[i][j]表示从第i堆石子开始，当前的M等于j时，先手最多可以拿到多少石子。',
        quote_src='—— yiduobo 题解原文',
        idea=['若 `i + 2j ≥ n`：先手一口气全拿走，`f = sum(piles[i:])`',
              '否则枚举拿 `k` 堆：后手得到 `f[i+k][max(j,k)]`，先手得到 `s − 它`，取最大',
              '依赖 `i + k` 的状态，所以 `i` 从后向前；区间和用变量 `s` 迭代'],
        summary=['时间 `O(n³)`，空间 `O(n²)`：状态 `n²`，每个枚举 `O(n)`',
                 '`j` 一律枚举到 `n`，比灵神的 `i//2+1` 多算一些用不到的状态',
                 '`f[i][j]` 先手视角：对手的最优已经隐含在 `f[i+k][·]` 里',
                 '代码为 Python 2 风格但无需改动，直接在 Python 3 运行'],
    ),
)
