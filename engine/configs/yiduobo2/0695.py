GRID = [[1, 1, 0],
        [0, 1, 0],
        [1, 0, 0]]


def _gcolor(S, i, j, v):
    if v == 1:
        return 'blue'
    if GRID[i][j] == 1:
        return 'green'
    return None


def _nb(S, B, ret):
    x, y, m, n = S.x, S.y, S.m, S.n
    if not (0 <= x < m and 0 <= y < n):
        return f'邻居 `({x},{y})` ==出界==，跳过'
    if B.grid[x][y] == 1:
        return f'邻居 `({x},{y})` 是 1 → 同一座岛，==标记并入队=='
    if GRID[x][y] == 1:
        return f'邻居 `({x},{y})` 已经入过队（改成了 0），跳过'
    return f'邻居 `({x},{y})` 是水，跳过'


def _seed(S, B, ret):
    i, j = S.i, S.j
    if S.grid[i][j] == 1:
        return f'`({i},{j})` 是 1 → ==发现新岛==，从这里开始 BFS'
    if GRID[i][j] == 1:
        return f'`({i},{j})` 已被改成 0（属于前面的岛），跳过'
    return f'`({i},{j})` 是水，跳过'


CONFIG = dict(
    num=695, title='岛屿的最大面积', difficulty='Medium', category='图论',
    author='yiduobo', technique='BFS · 队列长度即面积',
    tags=['字节30天', '热题173'],
    code='''
class Solution(object):
    def maxAreaOfIsland(self, grid):
        if not grid:
            return 0

        m = len(grid)
        n = len(grid[0])
        res = 0

        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    grid[i][j] = 0
                    q = [[i, j]]
                    l, r = 0, 1
                    while l < r:
                        now_x, now_y = q[l]
                        l += 1
                        for index in range(4):
                            x = now_x + dx[index]
                            y = now_y + dy[index]
                            if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 1:
                                grid[x][y] = 0
                                q.append([x, y])
                                r += 1
                    res = max(res, len(q))

        return res
''',
    call=f'Solution().maxAreaOfIsland({GRID})',
    expect=3,
    skip=['n = len(grid[0])', 'dy = [0', 'for i in range(m)', 'for j in range(n)', 'l, r = 0, 1', 'l += 1',
          'for index in range(4)', 'x = now_x', 'y = now_y', 'q.append', 'r += 1'],
    views=[
        dict(type='text', fn=lambda S: '蓝 = 未访问的 1　绿 = 已入队（改成 0）　黄框 = 出队格　粉框 = 邻居', size=24),
        dict(type='grid', var='grid', cell=104, h=360, color=_gcolor,
             cursors=[('now_x', 'now_y', 'yellow', '出队'), ('x', 'y', 'pink')]),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']] if 'q' in S else None,
             label='q（BFS 队列，暗 = 已出队；只追加不删除）', cell=96, h=200,
             pointers={'l': 'blue', 'r': 'pink'}, dim=lambda S, i, v: i < S['l']),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('len(q)', 'len(q)'), ('res', 'res', 'green')],
    captions={
        'if not grid': '`grid` 非空（空网格直接返回 0）',
        'm = len(grid)': '网格 `{m}` 行 `{len(grid[0])}` 列',
        'res = 0': '`res` 记录最大的岛屿面积',
        'dx = [': '`dx`、`dy` 配合表示==下、右、上、左==四个方向',
        'if grid[i][j] == 1': _seed,
        'grid[i][j] = 0': '起点先改成 0 再入队：==入队时就标记==，保证每格只入队一次',
        'q = [[i, j]]': '队列 `q` 里只有起点；`l = 0` 指向队头，`r = 1` 是队尾',
        'while l < r': lambda S, B, ret: (f'`l = {B.l} < r = {B.r}` → 队列非空，继续扩展' if B.l < B.r
                                          else f'`l == r == {B.r}` → 队列空了，这座岛==遍历完=='),
        'now_x, now_y = q[l]': '取出队头 `({now_x},{now_y})`，看它的四个邻居',
        'if x >= 0 and x < m': _nb,
        'grid[x][y] = 0': '`({x},{y})` 改成 0 并加入队尾',
        'res = max(res, len(q))': '==这次 BFS 队列的长度就是岛的面积==：`len(q) = {len(q)}` → `res = {res}`',
        'return res': '最大的岛屿面积 =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='从每个 1 出发 BFS，队列的最终长度就是这座岛的面积',
        complexity='时间 `O(mn)`，空间 `O(mn)`（队列）',
        problem=['`m × n` 的二进制矩阵 `grid`，上下左右相连的 `1` 组成一座==岛屿==',
                 '岛屿面积 = 岛上 `1` 的个数；返回==最大==的岛屿面积，没有岛返回 0',
                 '本视频：`[[1,1,0],[0,1,0],[1,0,0]]` → 两座岛，面积 3 和 1 → `3`'],
        quote='直接枚举地图上的每个点，若该点的值为1，那么从该点开始进行bfs，将相邻的值为1的点加入到bfs队列中，同时将其值修改为0。在完成一次bfs之后，这次bfs队列的长度就是这一块岛屿的面积。',
        quote_src='—— yiduobo 题解',
        idea=['枚举每个格子，值为 1 就从它开始 BFS',
              '相邻的 1 入队的==同时改成 0==，保证不会重复入队',
              '`q` 只追加、用下标 `l` 模拟出队 → BFS 结束时 `len(q)` 正好是面积'],
        result='两次 BFS 的队列长度分别是 `3` 和 `1` → 返回 `3` ✓',
        summary=['时间 `O(mn)`：每个格子最多入队一次；空间 `O(mn)`',
                 '列表 + 下标 `l` 当队列：元素不真的弹出，所以 `len(q)` 就是面积',
                 '易错：要在==入队时==改 0，出队时才改会让同一格重复入队、面积算多',
                 '对比灵神：灵神用 DFS 递归返回面积；BFS 不用担心递归太深',
                 '原文为 Python 2 风格，代码未改，仅删去 docstring'],
    ),
)
