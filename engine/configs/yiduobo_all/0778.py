GRID = [[0, 2, 6], [1, 5, 4]]


def _nb(S, B, r):
    x, y = B.x, B.y
    m, n, mid = B.m, B.n, B.mid
    if not (0 <= x < m and 0 <= y < n):
        return f'邻居 `({x},{y})` 越界'
    h = B.grid[x][y]
    if h > mid:
        return f'邻居 `({x},{y})` 高度 `{h}` > `mid = {mid}`：水位淹不到 → 不能走'
    if B.used[x][y] == mid:
        return f'邻居 `({x},{y})` 高度 `{h}` 但本轮已经访问过 → 不重复入队'
    return f'邻居 `({x},{y})` 高度 `{h}` <= `mid = {mid}`，且本轮没访问过 → ==入队=='


def _info(S):
    if 'min_h' not in S:
        return ''
    if 'mid' in S and S.get('_line', 0) >= 17:
        return f'二分高度（水位）：`[{S["min_h"]}, {S["max_h"]}]`，当前 `mid = {S["mid"]}`'
    return f'二分高度（水位）：`[{S["min_h"]}, {S["max_h"]}]`'


CONFIG = dict(
    num=778, title='水位上升的泳池中游泳', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='二分水位 + BFS 判连通',
    tags=['难度分 2097'],
    code='''
class Solution(object):
    def swimInWater(self, grid):

        m = len(grid)
        n = len(grid[0])

        max_h = 0
        for i in range(m):
            for j in range(n):
                max_h = max(max_h, grid[i][j])
        min_h = max(grid[0][0], grid[-1][-1])

        used = [[None] * n for _ in range(m)]
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        while min_h < max_h:
            mid = (min_h + max_h) >> 1
            q = [[0, 0]]
            used[0][0] = mid
            l = 0
            r = 1
            while l < r:
                nowx, nowy = q[l]
                l += 1
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] <= mid and used[x][y] != mid:
                        q.append([x, y])
                        used[x][y] = mid
                        r += 1

            if used[m - 1][n - 1] == mid:
                max_h = mid
            else:
                min_h = mid + 1
            
        return min_h
''',
    call=f'Solution().swimInWater({GRID})',
    expect=5,
    views=[
        dict(type='text', fn=_info, h=56),
        dict(type='grid', var='grid', label='grid（绿 = 本轮 BFS 访问到；蓝框 = 出队的格子，粉框 = 正在看的邻居）', cell=76, h=270,
             color=lambda S, i, j, v: 'green' if 'mid' in S and S['_line'] >= 17 and S['used'][i][j] == S['mid'] else None,
             dim=lambda S, i, j, v: 'mid' in S and S['_line'] >= 17 and v > S['mid'],
             cursors=[('nowx if _line >= 17 and l > 0 else None', 'nowy', 'blue'),
                      ('x if _line >= 23 and 0 <= x < m and 0 <= y < n else None', 'y', 'pink')]),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']] if 'q' in S and S['_line'] >= 17 else None,
             label='q（暗 = 已出队，l 指向下一个出队的）', cell=70, pointers={'l': 'blue'},
             dim=lambda S, i, v: i < S.get('l', 0), h=170),
    ],
    watch=[('min_h', 'min_h', 'blue'), ('max_h', 'max_h', 'pink'), ('mid', 'mid', 'yellow'), ('l', 'l'), ('r', 'r')],
    skip=['m = len(grid)', 'n = len(grid[0])', 'max_h = 0', 'for i in range(m)', 'for j in range(n)',
          'used = [[None]', 'dx = [', 'dy = [', 'l = 0', 'r = 1', 'l += 1', 'for index in range(4)',
          'x = nowx', 'y = nowy', 'r += 1', 'q.append', 'used[0][0] = mid'],
    captions={
        'max_h = max(max_h, grid[i][j])': '扫描记录最高的格子：`max_h = max({B.max_h}, {grid[i][j]}) = {max_h}`',
        'min_h = max': '水位至少要淹到起点和终点：`min_h = max({grid[0][0]}, {grid[-1][-1]}) = {min_h}`',
        'while min_h < max_h': lambda S, B, r: (f'`min_h = {B.min_h} < max_h = {B.max_h}`：水位还没锁定，继续二分' if B.min_h < B.max_h
                                                else f'`min_h == max_h = {B.min_h}`：最低可行水位找到了'),
        'mid = (min_h + max_h)': '试水位 `mid = ({min_h} + {max_h}) >> 1 = {mid}`：只走高度 `<= mid` 的格子，BFS 看能不能到终点',
        'q = [[0, 0]]': '起点入队，`used` 记下==本轮的 mid==，不用每轮重置访问数组',
        'while l < r': lambda S, B, r: (f'`l = {B.l} < r = {B.r}`：队列不空，继续' if B.l < B.r
                                        else f'`l == r = {B.r}`：队列空了，本轮 BFS 结束'),
        'nowx, nowy = q[l]': '出队 `({nowx},{nowy})`，看四个方向的邻居',
        'if x >= 0 and x < m': _nb,
        'used[x][y] = mid': '`({x},{y})` 入队并标记 `used = {mid}`',
        'if used[m - 1][n - 1] == mid': lambda S, B, r: (f'终点本轮被访问到 → 水位 `{S.mid}` ==够用==' if S.used[S.m - 1][S.n - 1] == S.mid
                                                         else f'终点本轮没访问到 → 水位 `{S.mid}` ==不够=='),
        'max_h = mid': '够用 → 答案 <= mid，上界收到 `max_h = {max_h}`',
        'min_h = mid + 1': '不够 → 答案 > mid，下界抬到 `min_h = {min_h}`',
        'return min_h': '`min_h == max_h`，最少等待时间 =={min_h}==',
    },
    max_steps=130,
    cards=dict(
        one_liner='水位越高越容易连通：二分水位，BFS 判断起点能否到终点',
        complexity='时间 `O(n² log n)`，空间 `O(n²)`',
        problem=['`n × n` 网格，`grid[i][j]` 是平台高度，时间 `t` 时水位为 `t`',
                 '相邻两格都被淹没才能游过去，求从左上到右下的最少时间',
                 '本视频：`[[0,2,6],[1,5,4]]` → `5`'],
        quote='高度满足二分的性质，于是可以先记录所有格子中最高和最低的高度，然后二分最终答案的高度并通过bfs检测，这样一来，总体的时间复杂度就降下来了。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想到「从低到高枚举水位 + BFS」，但高度太大会超时',
              '水位越高越容易连通，==满足单调性== → 改成二分水位',
              '下界取起点和终点的较大值：水位低于它们，根本出不了发'],
        summary=['时间 `O(n² log n)`，空间 `O(n²)`',
                 '`used[x][y] = mid` 用本轮水位当访问标记，省去每轮重建数组',
                 '闭区间：够用 `max_h = mid`，不够 `min_h = mid + 1`',
                 '原文为 Python 2 风格（继承 object），代码未改',
                 '对比灵神：灵神也可用 Dijkstra，一次搜索，不用二分'],
    ),
)
