GRID = [[0, 0, 0], [1, 1, 0], [1, 1, 0]]


def _cell(S, i, j, v):
    if v == 1:
        return 'red'
    used = S.get('used')
    if used and used[i][j]:
        q, l, r = S['q'], S['l'], S['r']
        k = next((t for t, p in enumerate(q) if p == [i, j]), -1)
        if k >= r:
            return 'green'      # 下一层（本轮新加入）
        if l <= k < r:
            return 'cyan'       # 当前层
        return 'purple'         # 更早的层
    return None


def _chk(S, B, ret):
    x, y, n = S.x, S.y, S.n
    if not (0 <= x < n and 0 <= y < n):
        return f'方向 {S.index}：`({x},{y})` 越界'
    if B.grid[x][y] == 1:
        return f'方向 {S.index}：`({x},{y})` 是 1，==不能走=='
    if B.used[x][y]:
        return f'方向 {S.index}：`({x},{y})` 已经访问过，跳过'
    return f'方向 {S.index}：`({x},{y})` 是 0 且没访问过 → ==入队==，它在第 `{S.step}` 层'


CONFIG = dict(
    num=1091, title='二进制矩阵中的最短路径', difficulty='Medium', category='网格图',
    author='yiduobo', technique='八方向 BFS（按层扩展）',
    tags=['labuladong', '灵神题单·网格图'],
    code='''
class Solution(object):
    def shortestPathBinaryMatrix(self, grid):

        n = len(grid)
        if grid[0][0] == 1 or grid[n - 1][n - 1] == 1:
            return -1

        if n == 1:
            return 1

        used = [[False] * n for _ in range(n)]
        q = [[0, 0]]
        used[0][0] = True
        dx = [0, 1, 1, 1, 0, -1, -1, -1]
        dy = [1, 1, 0, -1, -1, -1, 0, 1]
        l = 0
        r = 1
        step = 1
        while l < r:
            step += 1
            for nowx, nowy in q[l : r]:
                for index in range(8):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < n and y >= 0 and y < n and grid[x][y] == 0 and not used[x][y]:
                        q.append([x, y])
                        used[x][y] = True
                        if used[n - 1][n - 1]:
                            return step
            l, r = r, len(q)

        return -1
''',
    call=f'Solution().shortestPathBinaryMatrix({GRID})',
    expect=4,
    views=[
        dict(type='grid', var='grid', cell=110, h=420, cols=lambda S: ['', '', ''],
             label='grid（红 = 1 不能走；紫 = 早先的层，青 = 当前层，绿 = 新入队）',
             color=_cell, cursors=[('nowx', 'nowy', 'blue', 'now'),
                                   ('x if _line == 25 else None', 'y', 'pink', '(x,y)')]),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']] if 'q' in S else None,
             label='q（暗 = 已处理的层，[l, r) 是当前层）', cell=84, h=180,
             window=('l', 'r - 1'), pointers={'l': 'blue'},
             dim=lambda S, i, v: i < S.get('l', 0)),
    ],
    watch=[('step', 'step', 'green'), ('l', 'l', 'blue'), 'r', ('now', lambda S: (S['nowx'], S['nowy']) if 'nowx' in S else None)],
    skip=['dx = [', 'dy = [', 'l = 0', 'r = 1', 'for index in range(8)', 'x = nowx', 'y = nowy',
          'used[x][y] = True', 'if n == 1', 'used = [[False]'],
    captions={
        'n = len(grid)': '`n = {n}`，从左上 `(0,0)` 走到右下 `({n-1},{n-1})`',
        'if grid[0][0] == 1 or': lambda S, B, r: ('起点和终点都是 0，可以开始 BFS' if r is None and S.grid[0][0] == 0
                                                 else '起点或终点是 1 → 直接返回 -1'),
        'q = [[0, 0]]': '起点入队：`q` 当队列，`[l, r)` 是==当前这一层==',
        'used[0][0] = True': '标记起点已访问；起点自己算路径长度 1',
        'step = 1': '`step = 1`：当前层的路径长度（单元格个数）',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`：还有一层要扩展' if S.l < S.r else '队列空了'),
        'step += 1': '扩展下一层：新入队的格子路径长度是 `step = {step}`',
        'for nowx, nowy in q[l : r]': lambda S, B, r: ('当前层的格子都扩展完了' if 'nowx' in B and (B.nowx, B.nowy) == (S.nowx, S.nowy)
                                                        else f'取当前层的格子 `({S.nowx},{S.nowy})`，看==八个方向=='),
        'if x >= 0 and x < n': _chk,
        'q.append([x, y])': '`({x},{y})` 入队并标记 `used`',
        'if used[n - 1][n - 1]': lambda S, B, r: (f'终点 `({S.n-1},{S.n-1})` 被访问到了！' if S.used[S.n - 1][S.n - 1]
                                                  else '终点还没访问到，继续'),
        'return step': '第一次到达终点时的轮次就是最短路径：返回 =={ret}==',
        'l, r = r, len(q)': '这一层处理完：`[l, r)` 移到新入队的部分 `[{l}, {r})`',
    },
    max_steps=60,
    cards=dict(
        one_liner='八个方向的按层 BFS：第一次到达右下角时的层数就是答案',
        complexity='时间 `O(n²)`，空间 `O(n²)`',
        problem=['`n × n` 的 01 矩阵，从左上角走到右下角，只能走 `0`',
                 '每步可以走到==八个方向==相邻的格子，返回最短路径经过的格子数，走不到返回 `-1`',
                 '示例：`[[0,0,0],[1,1,0],[1,1,0]]` → `4`'],
        quote='首先判断特殊情况。当起点或终点对应的值为1时，直接返回-1。……接下来执行传统的bfs，不过需要注意==这里有八个方向==。',
        quote_src='—— yiduobo 题解原文',
        idea=['特判：起点或终点是 1 → `-1`；边长为 1 → `1`',
              '用数组 `q` + 区间 `[l, r)` 按层 BFS，每层 `step + 1`',
              '若 bfs 过程中达到了终点，那么==轮次即为最终答案=='],
        summary=['时间 `O(n²)`：每个格子最多入队一次，每次看 8 个方向',
                 '易错：是==八方向==，`dx`、`dy` 各 8 个；路径长度按格子数算，起点就是 1',
                 '入队时就标记 `used`，避免同一格子被重复入队',
                 '队列没出现过终点 → 返回 `-1`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
