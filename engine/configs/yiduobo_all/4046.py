GRID = [[1, 9], [3, 4]]
DN = ['右', '下', '左', '上']


def _gc(S, i, j, v):
    if 'now_x' not in S:
        return None
    if (i, j) == (S['now_x'], S['now_y']):
        return 'yellow'
    f = S.get('f')
    if f and any(f[i][j][kk][d] is not None for kk in range(len(f[i][j])) for d in range(4)):
        return 'blue'
    return None


def _txt(S):
    if 'now_x' not in S:
        return '`f[x][y][k][d]`：站在 `(x,y)`、已转向 `k` 次、方向 `d` 时，到终点的最小代价（-1 = 到不了）'
    nd = S.get('now_d')
    return (f'当前状态：`({S["now_x"]},{S["now_y"]})`，已转向 ==' + str(S['now_k']) + '== 次（最多 ' + str(S['k']) + '），方向 ==' + DN[nd] + '==')


def _chk(S, B, r):
    d = B.d
    nx, ny, nk = B.nxt_x, B.nxt_y, B.nxt_k
    head = f'`({B.now_x},{B.now_y})` 朝{DN[B.now_d]}，试方向 `{DN[d]}` → `({nx},{ny})`'
    head += '，==要转向==' if d != B.now_d else '，直走'
    return head + f'（转向 {nk} 次 ≤ k）→ 递归去算（出界、超过 k 的方向被 if 滤掉了）'


CONFIG = dict(
    num=4046, title='至多 K 次转向的最小路径代价', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='记忆化搜索（分层状态）',
    code='''
class Solution(object):
    def minCost(self, grid, k):
        

        m = len(grid)
        n = len(grid[0])

        f = [[[[None] * 4 for _ in range(k + 1)] for _ in range(n)] for _ in range(m)]
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        def calc(now_x, now_y, now_k, now_d):
            if f[now_x][now_y][now_k][now_d] is None:
                if now_x == m - 1 and now_y == n - 1:
                    f[now_x][now_y][now_k][now_d] = grid[now_x][now_y]
                else:
                    best = -1
                    for d in range(4):
                        nxt_x = now_x + dx[d]
                        nxt_y = now_y + dy[d]
                        nxt_k = now_k
                        if d != now_d:
                            nxt_k += 1
                        nxt_d = d
                        if 0 <= nxt_x < m and 0 <= nxt_y < n and nxt_k <= k:
                            cost = calc(nxt_x, nxt_y, nxt_k, nxt_d)
                            if cost != -1 and (best == -1 or best > cost + grid[now_x][now_y]):
                                best = cost + grid[now_x][now_y]

                    f[now_x][now_y][now_k][now_d] = best
            
            return f[now_x][now_y][now_k][now_d]
                     
        calc(0, 0, 0, 0)
        calc(0, 0, 0, 1)
        if f[0][0][0][0] == -1:
            return f[0][0][0][1]
        
        if f[0][0][0][1] == -1:
            return f[0][0][0][0]

        return min(f[0][0][0][0], f[0][0][0][1])
''',
    call=f'Solution().minCost({GRID}, 1)',
    expect=8,
    skip=['m = len', 'n = len', 'dx = [', 'dy = [', 'nxt_x = ', 'nxt_y = ', 'nxt_k = now_k', 'nxt_k += 1', 'if d != now_d', 'nxt_d = d', 'for d in range(4)', 'if 0 <= nxt_x',
          'if f[now_x][now_y][now_k][now_d] is None', 'best = -1', 'f[now_x][now_y][now_k][now_d] = grid'],
    views=[
        dict(type='text', fn=_txt, size=22, h=60),
        dict(type='grid', var='grid', label='grid（黄 = 当前格，蓝 = 已有记忆的格子）', h=230, cell=80, color=_gc,
             cursors=[('now_x', 'now_y', 'yellow')]),
        dict(type='calls', h=430),
    ],
    watch=['now_x', 'now_y', 'now_k', 'now_d', 'best', 'cost'],
    max_steps=80,
    captions={
        'f = [[[[None]': '`f` 是四维记忆表：`f[x][y][k][d]` 一开始都是 `None`（没算过）',
        'cost = calc': _chk,
        'if now_x == m - 1': lambda S, B, r: (f'`({S.now_x},{S.now_y})` 是终点 → 代价就是这格的 `{S.grid[S.now_x][S.now_y]}`' if S.now_x == S.m - 1 and S.now_y == S.n - 1
                                              else f'`({S.now_x},{S.now_y})` 朝{DN[S.now_d]}，已转向 {S.now_k} 次，不是终点 → 枚举下一步方向'),
        'if cost != -1': lambda S, B, r: (f'`cost = {S.cost}`：走不通，忽略' if S.cost == -1 else f'`{S.cost} + 本格 {S.grid[S.now_x][S.now_y]}` = {S.cost + S.grid[S.now_x][S.now_y]}，与 `best = {S.best}` 比，更小就更新'),
        'best = cost + grid': '`best` 更新为 =={best}==',
        'f[now_x][now_y][now_k][now_d] = best': '记下 `f[{now_x}][{now_y}][{now_k}][{now_d}] = {best}`，下次遇到同一状态直接用',
        'return f[now_x]': '`({now_x},{now_y})` 返回 `{f[now_x][now_y][now_k][now_d]}`',
        'calc(0, 0, 0, 0)': '从起点出发，初始方向「右」，已转向 0 次',
        'calc(0, 0, 0, 1)': '再从起点出发，初始方向「下」',
        'if f[0][0][0][0] == -1': '两个初始方向都算完：`f[0][0][0][0] = {f[0][0][0][0]}`，`f[0][0][0][1] = {f[0][0][0][1]}`',
        'return min': '两个起点方向都能到 → 取较小的 =={ret}==',
    },
    cards=dict(
        one_liner='状态 = 位置 + 转向次数 + 方向，记忆化搜索到终点',
        complexity='时间 `O(m·n·k·4·4)`，空间 `O(m·n·k)`',
        problem=['网格每格有代价，从左上走到右下，四个方向都能走，==转向不超过 k 次==',
                 '路径代价是经过的格子之和，重复经过要重复计入；到不了返回 -1',
                 '本视频：`grid=[[1,9],[3,4]], k=1` → `8`'],
        quote='本题中要回到之前访问过的单元格，必然经历了至少一次转向操作，因此使用记忆化搜索也是可行的选择。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[x][y][k][d]`：站在 `(x,y)`、已用 `k` 次转向、当前朝 `d`，到终点的最小代价',
              '枚举下一步方向 `d`：和当前方向不同则转向次数加 1，超过 `k` 就不能走',
              '回头路必然转向，所以状态不会成环，递归能结束；入口是起点的两个方向（右、下）'],
        summary=['时间 `O(m·n·k)`（每个状态只算一次），空间 `O(m·n·k)`',
                 '用 `-1` 表示到不了，更新前要先判断 `cost != -1`',
                 '方向编号：0 右、1 下、2 左、3 上；入口只有右、下两个起始方向',
                 '原文为 Python 2 风格，本题无需改动即可在 Python 3 运行',
                 '对比灵神：他倒着走 + `@cache`，另有 Dijkstra 与递推写法；yiduobo 从起点往后搜、手写记忆表'],
    ),
)
