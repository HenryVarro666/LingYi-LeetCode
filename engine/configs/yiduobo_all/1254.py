GRID = [[1, 1, 1, 1, 1],
        [0, 0, 1, 0, 1],
        [1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1]]


def _color(S, i, j, v):
    if v == 0:
        return 'yellow'
    if v >= 2:
        return 'green'
    if GRID[i][j] == 0:
        return 'cyan'
    return None


def _nb(S, B, ret):
    x, y = S.x, S.y
    m, n = S.m, S.n
    if not (0 <= x < m and 0 <= y < n):
        return f'邻居 `({x},{y})` 出界'
    v = B.grid[x][y]
    if v == 0:
        return f'邻居 `({x},{y})` 是 `0` → ==标记并入队=='
    if GRID[x][y] == 0:
        return f'邻居 `({x},{y})` 已经标记过（值 `{v}`）→ 跳过'
    return f'邻居 `({x},{y})` 是水 `1` → 跳过'


def _while(S, B, ret):
    if S.l < S.r:
        return f'`l = {S.l} < r = {S.r}`：队列不空，继续 BFS'
    return f'`l == r = {S.r}`：队列空了，这一轮 BFS 结束'


def _qstr(S):
    q = S.get('q')
    if not q:
        return None
    return [f'{a},{b}' for a, b in q]


CONFIG = dict(
    num=1254, title='统计封闭岛屿的数目', difficulty='Medium', category='网格图',
    author='yiduobo', technique='边界 BFS 淹掉 + 剩余连通块染色计数',
    tags=['labuladong', '灵神核心路线', '难度分 1659'],
    code='''
class Solution(object):
    def closedIsland(self, grid):

        m = len(grid)
        n = len(grid[0])
        q = []
        for i in range(n):
            if grid[0][i] == 0:
                q.append([0, i])
                grid[0][i] = 1
            if grid[m - 1][i] == 0:
                q.append([m - 1, i])
                grid[m - 1][i] = 1

        for i in range(m):
            if grid[i][0] == 0:
                q.append([i, 0])
                grid[i][0] = 1
            if grid[i][n - 1] == 0:
                q.append([i, n - 1])
                grid[i][n - 1] = 1

        l = 0
        r = len(q)
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        while l < r:
            nowx, nowy = q[l]
            l += 1
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 0:
                    grid[x][y] = 1
                    q.append([x, y])
                    r += 1

        now_color = 2
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 0:
                    grid[i][j] = now_color
                    q = [[i, j]]
                    l = 0
                    r = 1
                    while l < r:
                        nowx, nowy = q[l]
                        l += 1
                        for index in range(4):
                            x = nowx + dx[index]
                            y = nowy + dy[index]
                            if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 0:
                                grid[x][y] = now_color
                                q.append([x, y])
                                r += 1

                    now_color += 1

        return now_color - 2
''',
    call=f'Solution().closedIsland({GRID})',
    expect=1,
    views=[
        dict(type='text', fn=lambda S: '黄 = 还是 `0` 的陆地　青 = 从边界 BFS 到的（改成 1）　绿 = 染成 `now_color` 的封闭岛', size=22, h=56),
        dict(type='grid', var='grid', cell=92, h=400, color=_color,
             cursors=[('nowx', 'nowy', 'blue', '出队'),
                      (lambda S: S.get('x') if S.get('_line') in (33, 52) else None, 'y', 'pink'),
                      (lambda S: S.get('i') if S.get('_line') in (42,) else None, 'j', 'yellow')]),
        dict(type='array', var=_qstr, label='q（暗 = 已出队，l 指向下一个出队的）', cell=78, h=170,
             pointers={'l': 'blue'}, dim=lambda S, i, v: i < S.get('l', 0)),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r'), ('now_color', 'now_color', 'green')],
    skip=[8, 11, 16, 19, 9, 12, 17, 20, 'q = []', 'dx = [', 'dy = [', 'l += 1', 'for index in range(4)',
          'x = nowx', 'y = nowy', 'q.append([x, y])', 'r += 1', 'for j in range(n)', 41, 43, 44, 45],
    captions={
        'm = len(grid)': '网格 `{m}` 行；`0` 是陆地，`1` 是水',
        'n = len(grid[0])': '`{n}` 列。与地图==边缘相邻的连通块不可能是封闭岛==',
        10: '上边 `(0,{i})` 是 `0` → ==入队并置为 1==',
        13: '下边 `({m - 1},{i})` 是 `0` → ==入队并置为 1==',
        18: '左边 `({i},0)` 是 `0` → ==入队并置为 1==（它所在的岛不可能封闭）',
        21: '右边 `({i},{n - 1})` 是 `0` → ==入队并置为 1==',
        7: lambda S, B, ret: (f'扫描上下两条边：第 `{S.i}` 列' if S.get('i') != B.get('i') else '上下两条边扫描完毕'),
        15: lambda S, B, ret: (f'扫描左右两条边：第 `{S.i}` 行' if S.get('i') != B.get('i') or B.get('_line') != 15 or S.i == 0 else '四条边扫描完毕'),
        23: '数组当队列：`l` 是队首',
        24: '`r = len(q) = {r}`：边界上共有 `{r}` 个 `0` 在队列里',
        27: _while,
        28: '出队 `({nowx},{nowy})`，看下、右、上、左四个邻居',
        33: _nb,
        34: '`grid[{x}][{y}] = 1`，入队：和边界连通，也不可能封闭',
        38: '边界连通块都淹掉了。现在剩下的 `0` 各自组成封闭岛，用 `now_color = 2` 开始染色',
        39: lambda S, B, ret: (f'扫描第 `{S.i}` 行，找还是 `0` 的格子' if S.i != B.get('i') or 'now_color' not in B else '扫描完毕'),
        42: '`({i},{j})` 还是 `0` → ==新的封闭岛==！染成 `now_color = {now_color}`，从它开始 BFS',
        46: _while,
        47: '出队 `({nowx},{nowy})`',
        52: _nb,
        53: '染色 `grid[{x}][{y}] = {now_color}`，入队',
        57: '这座岛染完了，换下一种颜色：`now_color` → `{now_color}`',
        59: '用掉的颜色 `2 … {now_color - 1}` 共 `{now_color} - 2` = =={ret}== 种 → 封闭岛数',
    },
    max_steps=72,
    cards=dict(
        one_liner='先从四条边 BFS 淹掉边界岛，再给剩下的每块 0 染一种颜色',
        complexity='时间 `O(mn)`，空间 `O(mn)`（队列）',
        problem=['`0` 是陆地，`1` 是水；四方向相连的 `0` 组成岛',
                 '封闭岛：上下左右==完全被 1 包围==，求封闭岛的个数',
                 '本视频：4×5 网格，左边的岛碰到边界，右边的封闭 → `1`'],
        quote='与地图边缘相邻的连通块就不可能是最终的答案。因此我们可以先枚举地图的边缘，记录下其中0的位置，然后==从这些位置开始进行bfs，并将遍历到的格子置为1==。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一步：四条边上的 `0` 全部入队并置 1，BFS 把和它们相连的 `0` 也置 1',
              '第二步：扫描全图，遇到 `0` 就用一个新颜色 BFS 染色',
              '染色的种数（`now_color - 2`）就是封闭岛的数目'],
        summary=['时间 `O(mn)`：每个格子最多入队一次',
                 '==入队时就修改格子==，避免同一格子重复入队',
                 '队列用数组 + `l`、`r` 两个下标模拟，`r` 始终等于 `len(q)`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改',
                 '对比灵神：灵神用 DFS 且只扫边界格子；这里是 BFS + 染色计数'],
    ),
)
