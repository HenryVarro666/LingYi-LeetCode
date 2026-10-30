GRID = [[0, 0, 0, 0, 0],
        [1, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0]]


def _color(S, i, j, v):
    if v == 2:
        return 'cyan'
    if v == 1:
        return 'green' if S.get('res') is not None else 'yellow'
    return None


def _nb(S, B, ret):
    x, y = S.x, S.y
    m, n = S.m, S.n
    if not (0 < x < m - 1 and 0 < y < n - 1):
        return f'邻居 `({x},{y})` 不在内部（边上的已经处理过 / 出界）→ 跳过'
    v = B.grid[x][y]
    if v == 1:
        return f'邻居 `({x},{y})` 是陆地 `1` → 能走到边界，==入队并置为 2=='
    if v == 2:
        return f'邻居 `({x},{y})` 已经是 `2` → 跳过'
    return f'邻居 `({x},{y})` 是海 `0` → 跳过'


def _while(S, B, ret):
    if S.l < S.r:
        return f'`l = {S.l} < r = {S.r}`：队列不空，继续 BFS'
    return f'`l == r = {S.r}`：队列空了，BFS 结束'


def _qstr(S):
    q = S.get('q')
    if not q:
        return None
    return [f'{a},{b}' for a, b in q]


CONFIG = dict(
    num=1020, title='飞地的数量', difficulty='Medium', category='网格图',
    author='yiduobo', technique='从四条边反向 BFS',
    tags=['labuladong', '灵神核心路线'],
    code='''
class Solution(object):
    def numEnclaves(self, grid):

        q = []
        m = len(grid)
        n = len(grid[0])
        for i in range(m):
            if grid[i][0] == 1:
                grid[i][0] = 2
                q.append([i, 0])
            if grid[i][n - 1] == 1:
                grid[i][n - 1] = 2
                q.append([i, n - 1])

        for j in range(n):
            if grid[0][j] == 1:
                grid[0][j] = 2
                q.append([0, j])
            if grid[m - 1][j] == 1:
                grid[m - 1][j] = 2
                q.append([m - 1, j])

        l = 0
        r = len(q)
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        while l < r:
            nowx, nowy = q[l]
            l += 1
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x > 0 and x < m - 1 and y > 0 and y < n - 1 and grid[x][y] == 1:
                    q.append([x, y])
                    r += 1
                    grid[x][y] = 2

        res = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    res += 1

        return res
''',
    call=f'Solution().numEnclaves({GRID})',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: '黄 = 陆地 `1`　青 = 能走到边界的陆地（置为 `2`）　绿 = 飞地（计数）　深色 = 海 `0`', size=22, h=56),
        dict(type='grid', var='grid', cell=92, h=400, color=_color,
             cursors=[('nowx', 'nowy', 'blue', '出队'),
                      (lambda S: S.get('x') if S.get('_line') == 33 else None, 'y', 'pink'),
                      (lambda S: S.get('i') if S.get('_line') == 42 else None, 'j', 'green')]),
        dict(type='array', var=_qstr, label='q（暗 = 已出队，l 指向下一个出队的）', cell=78, h=170,
             pointers={'l': 'blue'}, dim=lambda S, i, v: i < S.get('l', 0)),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r'), ('res', 'res', 'green')],
    skip=[8, 10, 11, 13, 16, 18, 19, 21, 'q = []', 'dx = [', 'dy = [', 'l += 1', 'for index in range(4)',
          'x = nowx', 'y = nowy', 'q.append([x, y])', 'r += 1', 40, 41],
    captions={
        'm = len(grid)': '网格 `{m}` 行；`1` 是陆地，`0` 是海',
        'n = len(grid[0])': '`{n}` 列。飞地 = ==走不到四条边==的陆地 → 反过来从边上出发',
        7: lambda S, B, ret: (f'扫描左右两条边：第 `{S.i}` 行' if S.get('i') != B.get('i') else '左右两条边扫描完毕'),
        9: '左边 `({i},0)` 是陆地 → ==置为 2 并入队==',
        12: '右边 `({i},{n - 1})` 是陆地 → ==置为 2 并入队==',
        15: lambda S, B, ret: (f'扫描上下两条边：第 `{S.j}` 列' if S.get('j') != B.get('j') else '上下两条边扫描完毕'),
        17: '上边 `(0,{j})` 是陆地 → ==置为 2 并入队==',
        20: '下边 `({m - 1},{j})` 是陆地 → ==置为 2 并入队==',
        23: '数组当队列：`l` 是队首',
        24: '`r = len(q) = {r}`：四条边上共有 `{r}` 块陆地',
        27: _while,
        28: '出队 `({nowx},{nowy})`，看右、下、左、上四个邻居',
        33: _nb,
        36: '`grid[{x}][{y}] = 2`：它和边界连通，不是飞地',
        38: 'BFS 结束：==没被遍历到的 1== 就是飞地，数一数',
        39: lambda S, B, ret: (f'扫描第 `{S.i}` 行' if S.get('i') != B.get('i') or B.get('_line') == 38 else '扫描完毕'),
        42: '`({i},{j})` 还是 `1`：走不到边界 → 飞地 `res` = =={res}==',
        44: '共 =={ret}== 块飞地',
    },
    max_steps=70,
    cards=dict(
        one_liner='反过来从四条边上的陆地 BFS，没被遍历到的陆地就是飞地',
        complexity='时间 `O(mn)`，空间 `O(mn)`（队列）',
        problem=['`m × n` 网格，`0` 是海，`1` 是陆地；每次可以走到上下左右相邻的陆地',
                 '飞地：==无论怎么走都走不出网格边界==的陆地格子，求飞地格子数',
                 '示例：`[[0,0,0,0],[1,0,1,0],[0,1,1,0],[0,0,0,0]]` → `3`',
                 '本视频：左边 3 块和边界相连，右边 2 块走不出去 → `2`'],
        quote='题目中所说的飞地实际上指的是==不与四条边上相连的点==，那么我们可以反过来从四条边上的点开始进行bfs，那么最后没有被遍历到的点就是飞地。',
        quote_src='—— yiduobo 题解原文',
        idea=['四条边上所有值为 `1` 的点加入队列，并置为 `2`',
              'BFS：把当前点周围值为 `1` 的点入队，同样置为 `2`',
              'BFS 结束后，地图中剩余 `1` 的数量就是答案'],
        summary=['时间 `O(mn)`：每个格子最多入队一次',
                 '==入队时就置为 2==，防止重复入队',
                 'BFS 只扩展内部格子（`0 < x < m-1` 且 `0 < y < n-1`），边上的已经在第一步处理过',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改',
                 '同类题：1254. 统计封闭岛屿的数目（数岛的个数，而不是格子数）'],
    ),
)
