G0 = [[0, 1, 2], [2, 0, 1]]
K0 = 2
M0, N0 = len(G0), len(G0[0])


def _flat(S):
    f = S.get('f')
    if f is None:
        return None
    return [f[i][j] for i in range(M0) for j in range(N0)]


def _fcell(S, r, c, v):
    i, j, t, s = S.get('i'), S.get('j'), S.get('t'), S.get('s')
    if i is None or j is None or S.get('_line', 0) < 17:
        return None
    if (r, c) == (i * N0 + j, t if t is not None else -1):
        return 'yellow'
    if t is not None and s is not None and t - s >= 0:
        if i > 0 and (r, c) == ((i - 1) * N0 + j, t - s):
            return 'blue'
        if j > 0 and (r, c) == (i * N0 + j - 1, t - s):
            return 'green'
    return None


def _formula(S):
    i, j, t, s = S.get('i'), S.get('j'), S.get('t'), S.get('s')
    if i is None or j is None or t is None or s is None:
        return '`f[i][j][t]` = 走到 `(i,j)` 且花费恰好 `t` 时的最大分数，`-1` = 到不了'
    return f'`(i,j) = ({i},{j})`，格值 `{S["grid"][i][j]}`，花费 `s = {s}`：`f[{i}][{j}][{t}]` 来自上/左格的 `t - s = {t - s}` 这一列'


CONFIG = dict(
    num=3742, title='网格中得分最大的路径', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='三维 DP：花费恰好为 t',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1804'],
    code='''
class Solution(object):
    def maxPathScore(self, grid, k):
        
        m = len(grid)
        n = len(grid[0])

        f = [[[-1] * (k + 1) for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if grid[i][j] > 0:
                    s = 1
                else:
                    s = 0
                for t in range(s, k + 1):
                    if i == 0:
                        if j == 0:
                            f[i][j][t] = 0
                        else:
                            if f[i][j - 1][t - s] != -1:
                                f[i][j][t] = f[i][j - 1][t - s] + grid[i][j]
                    elif j == 0:
                        if f[i - 1][j][t - s] != -1:
                            f[i][j][t] = f[i - 1][j][t - s] + grid[i][j]
                    else:
                        if f[i][j - 1][t - s] != -1:
                            f[i][j][t] = f[i][j - 1][t - s] + grid[i][j]
                        if f[i - 1][j][t - s] != -1 and (f[i][j][t] == -1 or f[i][j][t] < f[i - 1][j][t - s] + grid[i][j]):
                            f[i][j][t] = f[i - 1][j][t - s] + grid[i][j]
        
        return max(f[-1][-1])
''',
    call=f'Solution().maxPathScore({G0}, {K0})',
    expect=3,
    max_steps=100,
    skip=['m = len', 'n = len', 'for j in range', 'if grid[i][j] > 0', 's = 1', 's = 0', 'else:', 'for t in range', 'if i == 0:', 'if j == 0:'],
    views=[
        dict(type='grid', var='grid', label='grid（黄框 = 当前格子）', h=190, cell=70,
             cursors=[('i', 'j', 'yellow', '(i,j)')]),
        dict(type='text', fn=_formula, size=22, h=60),
        dict(type='table', var=_flat, label='f[i][j][t]：每行一个格子 i,j，每列一个花费 t（-1 = 到不了）', h=380, cell=62,
             rows=lambda S: [f'{i},{j}' for i in range(M0) for j in range(N0)],
             cols=lambda S: [f't={t}' for t in range(K0 + 1)], color=_fcell),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'blue'), ('s', 's', 'purple'), ('t', 't', 'pink')],
    captions={
        'f = [[[-1]': '`f[i][j][t]`：走到 `(i,j)` 且花费==恰好== `t` 的最大分数，`-1` 表示这种花费到不了',
        17: '起点 `(0,0)`：花费 `t = {t}`、得分 `0`（`grid[0][0] = 0`，其他 `t` 同理）',
        19: '第一行只能从左边来：`f[{i}][{j-1}][{t - s}] = {f[i][j-1][t-s]}`，是 `-1` 就说明这条路走不通',
        20: '`f[{i}][{j}][{t}] = f[{i}][{j-1}][{t-s}] + {grid[i][j]}` = =={f[i][j][t]}==',
        22: '第一列只能从上边来：`f[{i-1}][{j}][{t - s}] = {f[i-1][j][t-s]}`，不是 `-1` 才能转移',
        23: '`f[{i}][{j}][{t}] = f[{i-1}][{j}][{t-s}] + {grid[i][j]}` = =={f[i][j][t]}==',
        25: '一般格子先试左边：`f[{i}][{j-1}][{t - s}] = {f[i][j-1][t-s]}`，花费 `t` 要从 `t - s` 转移',
        26: '`f[{i}][{j}][{t}] = f[{i}][{j-1}][{t-s}] + {grid[i][j]}` = =={f[i][j][t]}==',
        27: '再试上边：`f[{i-1}][{j}][{t - s}] = {f[i-1][j][t-s]}`，==可达且比目前的更大（或目前是 -1）==才更新',
        28: '`f[{i}][{j}][{t}] = f[{i-1}][{j}][{t-s}] + {grid[i][j]}` = =={f[i][j][t]}==，取左上两边较大者',
        'return max': '终点各个花费 `t = 0..k` 中取最大：`max({f[-1][-1]})` = =={ret}==',
    },
    cards=dict(
        one_liner='k 不大，直接把花费编码进状态：f[i][j][t]',
        complexity='时间 `O(mnk)`，空间 `O(mnk)`',
        problem=['`m×n` 网格只能向右或向下，格值 > 0 得分 = 格值、且花费 1',
                 '总花费不超过 `k`，求到右下角的最大得分，无路返回 `-1`',
                 '示例：`[[0,1,2],[2,0,1]], k=2` → `3`'],
        quote='若不考虑代价，那么本题就是非常经典的动态规划问题……由于本题的数据规模不大，因此可以直接将 k 编码到状态表示中。',
        quote_src='—— yiduobo 题解',
        idea=['经典版：`f[i][j] = f[i-1][j] + f[i][j-1]` 类似的转移，这里取 `max`',
              '加一维 `t`：花费==恰好==为 `t`，格值 > 0 时从 `t-1` 转移',
              '`-1` 表示不可达；第一行/第一列只有一个来源，要单独处理'],
        summary=['时间/空间都是 `O(mnk)`',
                 '易错：`-1` 不能参与取大；`i = 0` 或 `j = 0` 只有一个来源',
                 '最后在终点格对所有 `t ≤ k` 取最大值，全是 `-1` 就返回 `-1`',
                 '原文 `max(f[-1][-1])` 本身在无路时给出 `-1`，不需要额外判断'],
    ),
)
