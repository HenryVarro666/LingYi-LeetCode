G0 = [[0, 1, 2], [2, 0, 1]]
K0 = 2


def _row(S):
    g, row = S.get('grid'), S.get('row')
    if g is None or row is None:
        return None
    for r, rw in enumerate(g):
        if rw is row:
            return r
    return None


def _fcell(S, r, c, v):
    j, k, nk = S.get('j'), S.get('k'), S.get('new_k')
    if j is None or k is None or S.get('_line', 0) < 14:
        return None
    if (r, c) == (j + 1, k + 1):
        return 'yellow'
    if nk is not None:
        if (r, c) == (j + 1, nk + 1):
            return 'blue'
        if (r, c) == (j, nk + 1):
            return 'green'
    return None


def _formula(S):
    j, k, x = S.get('j'), S.get('k'), S.get('x')
    if j is None or k is None or x is None or S.get('_line', 0) < 14:
        return '`f[j][k+1]` = 走到当前列、花费不超过 `k` 的最大分数；`-inf` = 走不到'
    nk = k - 1 if x else k
    return f'格子 `x = {x}`：花费 `{1 if x else 0}`，查 `k = {k}` 前一状态 `new_k = {nk}`；`f[{j + 1}][{k + 1}] = max(上, 左) + {x}`'


CONFIG = dict(
    num=3742, title='网格中得分最大的路径', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='网格 DP + 花费维度（滚动数组）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1804'],
    code='''
# 手写 max 更快
max = lambda a, b: b if b > a else a

class Solution:
    def maxPathScore(self, grid: List[List[int]], K: int) -> int:
        n = len(grid[0])
        f = [[-inf] * (K + 2) for _ in range(n + 1)]
        f[1][1:] = [0] * (K + 1)

        for row in grid:
            for j, x in enumerate(row):
                for k in range(K, -1, -1):
                    new_k = k - 1 if x else k
                    f[j + 1][k + 1] = max(f[j + 1][new_k + 1], f[j][new_k + 1]) + x

        ans = f[n][-1]
        return -1 if ans < 0 else ans
''',
    call=f'Solution().maxPathScore({G0}, {K0})',
    expect=3,
    max_steps=90,
    skip=['# 手写 max', 'max = lambda', 'for j, x in', 'for row in grid', 'n = len(grid[0])', 'for k in range'],
    views=[
        dict(type='grid', var='grid', label='grid（黄框 = 当前格子 x）', h=190, cell=70,
             cursors=[(lambda S: _row(S), 'j', 'yellow', 'x')]),
        dict(type='text', fn=_formula, size=22, h=60),
        dict(type='table', var='f', label='f[j+1][k+1]：黄 = 正在算，蓝 = 同列旧值（上一行），绿 = 左边格子', h=300, cell=80,
             rows=lambda S: [f'j={r - 1}' for r in range(len(S['f']))] if 'f' in S else [],
             cols=lambda S: [f'k={c - 1}' for c in range(len(S['f'][0]))] if 'f' in S else [],
             color=_fcell),
    ],
    watch=[('j', 'j', 'blue'), ('x', 'x', 'yellow'), ('k', 'k', 'pink'), ('new_k', 'new_k', 'purple'), ('ans', 'ans', 'green')],
    captions={
        'f = [[-inf]': '`f[j][k+1]`：走到当前行第 `j-1` 列、花费不超过 `k` 的最大分数；初始 `-inf` 表示走不到',
        'f[1][1:] = ': '起点上方的虚拟行：`f[1][k+1] = 0`（`k ≥ 0`），而 `f[1][0] = -inf`（花费不能为负）→ ==起点无需特判==',
        'new_k = ': lambda S, B, r: (f'`k = {S.k}`，`x = {S.x} > 0`：这格要花 1，所以==前一格的花费上限是 `k-1 = {S.new_k}`==' if S.x else f'`k = {S.k}`，`x = 0`：不花费，前一格的上限仍是 `{S.new_k}`'),
        'f[j + 1][k + 1] = max': '`f[{j+1}][{k+1}] = max(上 {B.f[j+1][new_k+1]}, 左 {f[j][new_k+1]}) + {x}` = =={f[j+1][k+1]}=='
                                  '',
        'ans = f[n][-1]': '终点列、花费上限 `K` 的格子就是答案：`ans = {ans}`',
        'return -1': lambda S, B, r: f'`ans = {S.ans}`' + ('，小于 0 → 没有合法路径，返回 -1' if S.ans < 0 else '，合法 → 直接返回'),
    },
    cards=dict(
        one_liner='把花费 k 当成状态的一维，往前一格就扣掉这格的花费',
        complexity='时间 `O(mnk)`，空间 `O(nk)`',
        problem=['`m×n` 网格只能向右或向下走，格值 0/1/2：得分 = 格值，格值 > 0 还要花 1',
                 '总花费不超过 `k` 时，求走到右下角的==最大得分==；没有合法路径返回 `-1`',
                 '示例：`grid=[[0,1],[2,0]], k=1` → `2`'],
        quote='定义 dfs(i,j,k) 表示从 (0,0) 走到 (i,j)，在总花费不超过 k 的情况下，可以获得的最大分数。……两种情况取最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['64 题的网格 DP 再加一维 `k`：从上方或左边来，取较大值',
              '格值 `x > 0` 时花费 1，所以来源状态的 `k` 要减 1：`new_k = k - 1`',
              '递推把「出界」变成虚拟的 `-inf` 行；去掉行维度后，`k` 倒序枚举（像 0-1 背包）避免覆盖'],
        summary=['时间 `O(mnk)`，空间优化后 `O(nk)`',
                 '易错：`-inf` 保证 `max` 不选非法状态；最后 `ans < 0` 要返回 `-1`',
                 '`k` 必须倒序，否则 `f[j+1][new_k+1]` 已被本行覆盖',
                 '原文另有：记忆化搜索、三维递推、以及 `k` 取 `min(K, m+n-2)` 的循环优化，这里演示滚动数组版'],
    ),
)
