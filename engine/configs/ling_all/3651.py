GRID = [[1, 3, 3], [2, 5, 4], [4, 3, 5]]


def _live(S):
    return S.get('_line') in (21, 22) and 'row' in S and 'x' in S


def _r(S):
    return S['grid'].index(S['row']) if _live(S) else None


def _cell_color(S, i, j, v):
    r = _r(S)
    if r is None:
        return None
    if (i, j) == (r, S['j']):
        return 'yellow'
    if (i, j) < (r, S['j']):
        return 'green'
    return None


def _fc(S, i, v):
    return 'yellow' if _live(S) and i == S['j'] + 1 else None


def _sc(S, i, v):
    return 'yellow' if _live(S) and i == S['x'] else None


def _text(S):
    if not _live(S):
        return '`f[j+1]`：当前行走到第 `j` 列的最小成本；`suf_min_f[x]`：上一轮传送后，值 >= x 的格子的最小成本'
    r = _r(S)
    return f"格子 `({r}, {S['j']})`，值 ==x {S['x']}==：普通走 `min(左, 上) + x`，或传送 `suf_min_f[{S['x']}]`"


CONFIG = dict(
    num=3651, title='带传送的最小路径成本', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='网格 DP + 传送次数一维 + 后缀最小值',
    tags=['灵神题单', '动态规划', '难度分 2411'],
    code='''
# 手写 min 更快
min = lambda a, b: b if b < a else a

class Solution:
    def minCost(self, grid: List[List[int]], k: int) -> int:
        if k and grid[0][0] >= grid[-1][-1]:
            return 0

        n = len(grid[0])
        mx = max(map(max, grid))

        suf_min_f = [inf] * (mx + 2)
        for _ in range(k + 1):
            min_f = [inf] * (mx + 1)

            # 64. 最小路径和（空间优化写法）
            f = [inf] * (n + 1)
            f[1] = -grid[0][0]  # 起点的成本不算
            for row in grid:
                for j, x in enumerate(row):
                    f[j + 1] = min(min(f[j], f[j + 1]) + x, suf_min_f[x])
                    min_f[x] = min(min_f[x], f[j + 1])
   
            tmp = suf_min_f.copy()
            # 计算 min_f 的后缀最小值
            for i in range(mx, -1, -1):
                suf_min_f[i] = min(suf_min_f[i + 1], min_f[i])
            if suf_min_f == tmp:
                # 收敛了：传送不改变 suf_min_f，那么无论再传送多少次都不会改变 suf_min_f
                break

        return f[n]
''',
    call=f'Solution().minCost({GRID}, 1)',
    expect=7,
    skip=['min = lambda', 'n = len', 'mx = max', 'tmp = suf_min_f.copy()', 'for row in grid', 'for j, x in enumerate', 'for i in range(mx', 'min_f[x] = min(min_f[x]'],
    max_steps=90,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='grid', var='grid', color=_cell_color, h=190, cell=76),
        dict(type='array', var='f', label='f（当前行的 DP，f[0] 是哨兵 inf）', color=_fc, h=160),
        dict(type='array', var='min_f', label='min_f[x]：本轮值为 x 的格子的最小成本', color=_sc, h=160),
        dict(type='array', var='suf_min_f', label='suf_min_f[x]：上一轮里值 >= x 的最小成本（传送来源）', color=_sc, h=160),
    ],
    watch=[('t', '_', 'blue'), ('x', 'x', 'yellow'), ('j', 'j', 'pink'), ('k', 'k', 'green')],
    captions={
        'if k and grid': '`k = {k}` 且起点值 `{grid[0][0]}` >= 终点值 `{grid[-1][-1]}`？不成立 → 不能一步传送到终点，往下算',
        'suf_min_f = [inf]': '`suf_min_f[x]`：==上一轮==里，值 >= x 的格子的最小成本。第 0 轮还没有传送来源，全是 `inf`',
        'for _ in range': lambda S, B, r: (f"第 `{S['_']}` 轮：恰好传送 `{S['_']}` 次" if B.get('_') != S.get('_') or '_' not in B else '轮数用完或已收敛，结束'),
        'min_f = [inf]': '`min_f[x]`：本轮值为 x 的格子的最小成本，先清空',
        'f = [inf]': '`f[j+1]`：当前行第 `j` 列的最小成本（滚动数组），`f[0]` 是哨兵',
        'f[1] = -grid': '起点成本不计，先记 `-{grid[0][0]}`，走进起点时再加上 `x` 抵消',
        'f[j + 1] = min': '格子 `x = {x}`：普通走 `min(左 {B.f[j]}, 上 {B.f[j+1]}) + {x}`，传送 `suf_min_f[{x}] = {suf_min_f[x]}` → `f[{j+1}]` = =={f[j+1]}==；下一行把它并入 `min_f[{x}]`（取最小）',
        'min_f[x] = min': '值为 `{x}` 的格子最小成本记到 `min_f[{x}]` = =={min_f[x]}==',
        'suf_min_f[i] = min': '后缀最小值：`suf_min_f[{i}] = min(suf_min_f[{i+1}], min_f[{i}])` = =={suf_min_f[i]}==',
        'if suf_min_f == tmp': lambda S, B, r: ('`suf_min_f` 和上一轮完全相同 → ==收敛==，再传送也不会更优，提前结束' if r is None and S.suf_min_f == S.tmp else '`suf_min_f` 变了，传送还有改进空间，继续下一轮'),
        'return f[n]': '到达右下角的最小成本 `f[{n}] = {f[n]}`',
    },
    cards=dict(
        one_liner='传送次数当一维，传送来源用「值 >= x 的后缀最小」',
        complexity='时间 `O((mn+U)k)`，空间 `O(n+U)`',
        problem=['网格从左上走到右下，只能右/下，成本是目标格的值（起点不算）',
                 '可传送到值不大于当前格的任意格，成本 0，最多 `k` 次',
                 '本视频：`[[1,3,3],[2,5,4],[4,3,5]], k=1` → `7`'],
        quote='传送：设 x = grid[i][j]，我们可以从格子值 >= x 的任意格子传送到 (i,j)。如何快速得到这些 f 的最小值？定义 sufMinF 表示满足 grid[i][j] >= x 的 f 的最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['没有传送就是 64 题最小路径和；加一维 `t` 表示传送次数',
              '`f[t][i][j] = min(左 + x, 上 + x, sufMinF[t-1][x])`',
              '每轮先把 `f` 按值存进 `min_f`，倒序求后缀最小得 `suf_min_f`，供下一轮传送'],
        summary=['时间 `O((mn+U)k)`，`U` 是格子最大值；空间 `O(n+U)`',
                 '「至多 k 次」等于「恰好 k 次」：可以原地传送，次数多不会更差',
                 '优化：`suf_min_f` 一轮没变就收敛，直接退出；起点值 >= 终点值且 `k>0` 直接返回 0',
                 '易错：起点成本不计，所以 `f[1] = -grid[0][0]`'],
    ),
)
