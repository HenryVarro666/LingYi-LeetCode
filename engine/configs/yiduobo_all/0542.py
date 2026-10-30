MAT = [[0, 0, 0], [0, 1, 0], [1, 1, 1]]


def _cell(S, i, j, v):
    u = S.get('used')
    if u is None:
        return None
    if u[i][j]:
        return 'green'
    return None


def _nb(S, B, r):
    x, y = S.x, S.y
    if not (0 <= x < S.m and 0 <= y < S.n):
        return f'邻居 `({x},{y})` 越界 → 跳过'
    if S.used[x][y]:
        return f'邻居 `({x},{y})` 已经用过（距离已确定）→ 跳过'
    return f'邻居 `({x},{y})` 没用过 → ==这是最短路径第一次到达它==，距离 = 当前 + 1'


CONFIG = dict(
    num=542, title='01 矩阵', difficulty='Medium', category='网格图',
    author='yiduobo', technique='多源 BFS（从所有 0 出发）',
    tags=['灵神题单', '网格图'],
    code='''
class Solution(object):
    def updateMatrix(self, matrix):

        m = len(matrix)
        n = len(matrix[0])
        used = [[False] * n for _ in range(m)]
        q = []
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 0:
                    q.append([i,j])
                    used[i][j] = True

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
                if x >= 0 and x < m and y >= 0 and y < n and not used[x][y]:
                    matrix[x][y] = matrix[nowx][nowy] + 1
                    q.append([x, y])
                    r += 1
                    used[x][y] = True
        
        return matrix
''',
    call=f'Solution().updateMatrix({MAT})',
    expect=[[0, 0, 0], [0, 1, 0], [1, 2, 1]],
    skip=['m = len', 'n = len', 'l = 0', 'r = len', 'dx = [', 'dy = [', 'l += 1', 'for index in range(4)',
          'x = nowx', 'y = nowy', 'q.append([x, y])', 'r += 1', 'for i in range', 'for j in range', 'q = []'],
    views=[
        dict(type='grid', var='matrix', label='matrix（绿 = 已用/距离已确定；蓝框 = 出队的格子，粉框 = 正在看的邻居）', cell=110, h=400,
             color=_cell, cursors=[('nowx', 'nowy', 'blue'),
                                   ('x if _line == 24 else None', 'y', 'pink')]),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']] if 'q' in S else None,
             label='q（暗 = 已出队，l 指向下一个出队的）', cell=80, pointers={'l': 'blue'},
             dim=lambda S, i, v: i < S.get('l', 0), h=190),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r')],
    captions={
        'used = [[False]': '`used` 标记哪些格子的距离已经确定',
        'if matrix[i][j] == 0': lambda S, B, r: (f'`({S.i},{S.j})` 是 0 → ==作为 BFS 的起点入队==' if S.matrix[S.i][S.j] == 0
                                                  else f'`({S.i},{S.j})` 是 1，先不管'),
        'q.append([i,j])': '`({i},{j})` 入队',
        'used[i][j] = True': '0 的距离就是 0，标记为已用',
        'while l < r': lambda S, B, r: (f'`l = {B.l} < r = {B.r}`：队列不空，继续' if B.l < B.r
                                        else f'`l == r = {B.r}`：队列空了，所有格子都算好了'),
        'nowx, nowy = q[l]': '出队 `({nowx},{nowy})`，当前距离 `{matrix[nowx][nowy]}`，向四个方向扩展一步',
        'if x >= 0 and x < m': _nb,
        'matrix[x][y] = matrix': '`matrix[{x}][{y}] = {matrix[nowx][nowy]} + 1 = {matrix[x][y]}`：比出队格子远一步',
        'used[x][y] = True': '`({x},{y})` 入队并标记，以后不再重复',
        'return matrix': '返回 `matrix`：每格都是到最近 0 的距离',
    },
    cards=dict(
        one_liner='把所有 0 同时当起点，一趟 BFS 往外扩，层数就是距离',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['给定只含 `0` 和 `1` 的矩阵 `matrix`',
                 '求每个格子到==最近的 0==的距离，相邻格子距离为 1',
                 '本视频：`[[0,0,0],[0,1,0],[1,1,1]]` → `[[0,0,0],[0,1,0],[1,2,1]]`'],
        quote='从矩阵中的每个0开始，一趟bfs，每次往当前值不为0且没有被使用过的地方扩展一步即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把所有 0 入队并标记，它们的距离是 0',
              '出队一个格子，把没用过的邻居距离设为 `当前 + 1`',
              '多源同时扩张：第一次碰到某格子的就是最近的 0'],
        summary=['时间 `O(mn)`：每个格子只入队一次',
                 '易错：必须先把==所有== 0 入队再开始 BFS，不能逐个 0 单独搜',
                 '队列用数组加 `l`、`r` 下标模拟；入队时就标记 `used`，避免重复入队',
                 '直接在 `matrix` 上原地写距离，所以返回的是同一个矩阵',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
