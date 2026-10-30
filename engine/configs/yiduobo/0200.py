COLORS = {'1': 'blue', '2': 'green', '3': 'purple', '4': 'orange', '5': 'cyan'}


def _nb(S, B, ret):
    x, y = S.new_x, S.new_y
    m, n = S.m, S.n
    if not (0 <= x < m and 0 <= y < n):
        return f'邻居 `({x},{y})` ==出界==，跳过'
    v = B.grid[x][y]
    if v == '1':
        return f'邻居 `({x},{y})` 是还没染色的 `1` → ==染上颜色 {S.now}== 并入队'
    if v == '0':
        return f'邻居 `({x},{y})` 是水，跳过'
    return f'邻居 `({x},{y})` 已经染成 `{v}`，==不会重复入队=='


def _seed(S, B, ret):
    v = S.grid[S.i][S.j]
    if v == '1':
        return f'`({S.i},{S.j})` 还是初始颜色 `1` → ==新的种子==，从这里开始 BFS 染色'
    if v == '0':
        return f'`({S.i},{S.j})` 是水，跳过'
    return f'`({S.i},{S.j})` 已被染成 `{v}`（属于之前的岛），跳过'


CONFIG = dict(
    num=200, title='岛屿数量', difficulty='Medium', category='图论',
    author='yiduobo', technique='种子染色法 · BFS',
    code='''
class Solution(object):
    def numIslands(self, grid):
        if not grid:
            return 0

        m = len(grid)
        n = len(grid[0])

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        now = 2
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '1':
                    grid[i][j] = str(now)
                    q = [[i, j]]
                    l = 0
                    r = 1
                    while l < r:
                        x, y = q[l]
                        l += 1
                        for index in range(4):
                            new_x = x + dx[index]
                            new_y = y + dy[index]
                            if new_x >= 0 and new_x < m and new_y >= 0 and new_y < n and grid[new_x][new_y] == '1':
                                grid[new_x][new_y] = str(now)
                                q.append([new_x, new_y])
                                r += 1
                    now += 1
        return now - 2
''',
    call='Solution().numIslands([list("1100"), list("0110"), list("0001")])',
    expect=2,
    skip=['n = len(grid[0])', 'dy = [1, 0', '                    l = 0', '                    r = 1', 'for j in range(n)', 'for index in range(4)', 'new_x = x + dx', 'new_y = y + dy',
          'q.append([new_x', 'r += 1'],
    views=[
        dict(type='text', fn=lambda S: f"下一种颜色 `now = {S['now']}`　蓝 = 未染色的 `1`　绿 = 颜色 2　紫 = 颜色 3"
             if 'now' in S else '蓝 = 未染色的 `1`', size=24),
        dict(type='grid', var='grid', cell=88, h=330,
             cursors=[('x', 'y', 'yellow', '出队'), ('new_x', 'new_y', 'pink', '邻居')],
             color=lambda S, i, j, v: COLORS.get(v)),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']], label='q（BFS 队列，灰色 = 已出队）',
             pointers={'l': 'blue', 'r': 'pink'}, dim=lambda S, i, v: i < S['l'], cell=84),
    ],
    watch=[('now', 'now', 'green'), 'l', 'r', ('出队格', lambda S: (S['x'], S['y']))],
    captions={
        'if not grid': '空网格直接返回 0（防御性判断）',
        'm = len(grid)': '网格 `{m}` 行 `{len(grid[0])}` 列',
        'dx = [': '`dx`、`dy` 两个数组配合，表示==右、下、左、上==四个方向',
        'now = 2': '`now = 2`：第一座岛染成 2，之后每座岛换一种新颜色 3、4、5……',
        'for i in range(m)': lambda S, B, ret: f'扫描第 `{S.i}` 行' if B.get('i') != S.i or 'i' not in B else '所有格子扫描完毕',
        "if grid[i][j] == '1'": _seed,
        'grid[i][j] = str(now)': '种子 `({i},{j})` 先染成 `{now}`，再入队，==入队前就染色==，保证每格只进一次队',
        'q = [[i, j]]': '队列 `q` 里只有种子；`l = 0` 指向队头，`r = 1` 是队尾（已入队个数）',
        'while l < r': lambda S, B, ret: (f'`l < r`（`{B.l} < {B.r}`）→ 队列非空，继续扩散' if B.l < B.r
                                          else f'`l == r == {B.r}` → 队列空了，这座岛==染色完毕=='),
        'x, y = q[l]': '取出队头 `({x},{y})`，看它的四个邻居',
        'l += 1': '`l` 后移到 {l}：`({x},{y})` 正式出队',
        'if new_x >= 0': _nb,
        'grid[new_x][new_y] = str(now)': '`({new_x},{new_y})` 染成 `{now}`，加入队尾，`r` → {B.r + 1}',
        'now += 1': '这座岛染完了，换下一种颜色：`now` = {now}',
        'return now - 2': '颜色从 2 开始用，==下一次准备染的颜色减 2== 就是岛屿数：`{B.now} - 2 = {ret}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='种子染色：每发现一个 1，就用一种新颜色把整座岛 BFS 染掉',
        complexity='时间 `O(mn)`，空间 `O(mn)`（队列）',
        problem=['网格里 `1` 是陆地、`0` 是水，上下左右相连的陆地组成一座岛',
                 '求岛屿数量（斜着不算相连）',
                 '本视频示例：`["1100","0110","0001"]` → ==2== 座岛'],
        quote='又是经典的种子染色法。扫描整个地图，若当前单元格颜色为初始颜色1，那么从当前单元格开始做bfs，并将bfs遍历到的所有单元格染上新的颜色。',
        quote_src='—— yiduobo 题解',
        idea=['第一座岛染成 `2`，之后每座岛依次染 `3`、`4`、`5`……',
              '用列表 `q` 加两个下标 `l`、`r` 手写队列：`q[l]` 出队，`append` 入队',
              '最后答案 = ==下一次准备染的颜色 − 2=='],
        summary=['时间 `O(mn)`：每个格子最多染色、入队一次',
                 '==入队时立刻染色==，否则同一格可能被多个邻居重复入队',
                 '染不同颜色的好处：结束后网格里能直接看出每座岛',
                 '和 DFS 插旗本质相同，BFS 不会有递归栈过深的问题',
                 '原文为 Python 2 风格，删去了 `"""type"""` 文档字符串'],
    ),
)
