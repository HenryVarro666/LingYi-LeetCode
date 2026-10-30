M = ["..A", "A#."]


def _mcol(S, i, j, v):
    if v == '#':
        return 'red'
    if v.isalpha():
        return 'purple'
    return None


def _nb(S, B, r):
    x, y = S.x, S.y
    if not (0 <= x < S.m and 0 <= y < S.n):
        return f'邻居 `({x},{y})` 越界，跳过'
    if S.matrix[x][y] == '#':
        return f'邻居 `({x},{y})` 是障碍物，不能走'
    if S.dis[x][y] != -1:
        return f'邻居 `({x},{y})` 已经到过（`dis` 不是 -1）→ 不重复入队'
    if S.matrix[x][y].isupper():
        return f'邻居 `({x},{y})` 是传送门 `{S.matrix[x][y]}` → ==它和同字母的所有格子一起入队=='
    return f'邻居 `({x},{y})` 是没到过的空格 → 入队'


CONFIG = dict(
    num=3552, title='网格传送门旅游', difficulty='Medium', category='网格图',
    author='yiduobo', technique='普通 BFS + 首次遇到传送门就全部入队',
    tags=['灵神题单', '网格图', '难度分 2036'],
    code='''
class Solution(object):
    def minMoves(self, matrix):
        
        m = len(matrix)
        n = len(matrix[0])

        transport = {}
        for i in range(m):
            for j in range(n):
                if 'A' <= matrix[i][j] <= 'Z':
                    if matrix[i][j] not in transport:
                        transport[matrix[i][j]] = []
                    transport[matrix[i][j]].append((i, j))
    
        q = deque()
        dis = [[-1] * n for _ in range(m)]
        if 'A' <= matrix[0][0] <= 'Z':
            for x, y in transport[matrix[0][0]]:
                q.append((x, y))
                dis[x][y] = 0
        else:
            q.append((0, 0))
            dis[0][0] = 0
        
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        while q:
            nowx, nowy = q.popleft()
            for d in range(4):
                x = nowx + dx[d]
                y = nowy + dy[d]
                if 0 <= x < m and 0 <= y < n and matrix[x][y] != '#' and dis[x][y] == -1:
                    if 'A' <= matrix[x][y] <= 'Z':
                        for tx, ty in transport[matrix[x][y]]:
                            q.append((tx, ty))
                            dis[tx][ty] = dis[nowx][nowy] + 1
                    else:
                        q.append((x, y))
                        dis[x][y] = dis[nowx][nowy] + 1
        
        return dis[-1][-1]
''',
    call=f'Solution().minMoves({M})',
    expect=2,
    skip=['m = len', 'n = len', 'transport = {}', 'for i in range(m)', 'for j in range(n)', "if 'A' <= matrix[i][j]",
          'if matrix[i][j] not in', 'transport[matrix[i][j]]', 'q = deque', 'dx = [', 'dy = [', 'for d in range(4)',
          'x = nowx', 'y = nowy', 'dis = [[-1]', 'q.append((tx', 'q.append((x, y))'],
    views=[
        dict(type='grid', var=lambda S: [list(r) for r in S['matrix']] if 'matrix' in S else None, label='matrix（紫 = 传送门字母，红 = 障碍；蓝框 = 出队格，粉框 = 邻居）',
             cell=90, h=220, color=_mcol, cursors=[('nowx', 'nowy', 'blue'), ('x', 'y', 'pink')]),
        dict(type='grid', var='dis', label='dis（-1 = 还没到过；否则是最少移动次数）', cell=90, h=220,
             color=lambda S, i, j, v: 'green' if v != -1 else None),
        dict(type='queue', var='q', fmt=lambda p: f'({p[0]},{p[1]})', label='q（普通 BFS 队列）', h=120),
    ],
    watch=[('nowx', 'nowx', 'blue'), ('nowy', 'nowy', 'blue'), ('x', 'x', 'pink'), ('y', 'y', 'pink')],
    captions={
        'transport = {}': '`transport[字母]` = 这个传送门所有格子的位置',
        "if 'A' <= matrix[0][0]": lambda S, B, r: ('起点本身就是传送门 → ==出发前就能传送==，要把同字母的所有格子都作为起点' if 'A' <= B.matrix[0][0] <= 'Z' else '起点是普通格子，只从 `(0,0)` 出发'),
        'dis[x][y] = 0': '同字母的格子都以 0 次移动入队：`dis[{x}][{y}] = 0`',
        'dis[0][0] = 0': '起点 `dis[0][0] = 0`',
        'while q': lambda S, B, r: ('队列非空，继续 BFS' if B.q else '队列空了，BFS 结束'),
        'nowx, nowy = q.popleft()': '出队 `({nowx},{nowy})`，向右、下、左、上四个方向各走一步',
        'if 0 <= x < m': _nb,
        "if 'A' <= matrix[x][y] <= 'Z'": lambda S, B, r: (f'`{S.matrix[S.x][S.y]}` 是传送门：首次遇到就用，==去同字母任意格子都不再多花步数==' if S.matrix[S.x][S.y].isupper() else '是普通空格，只入队它自己'),
        'for tx, ty in transport': '把 `{matrix[x][y]}` 的所有位置依次入队',
        'dis[tx][ty] =': '`dis[{tx}][{ty}] = dis[{nowx}][{nowy}] + 1 = {dis[tx][ty]}`：走进传送门花 1 步，传送本身免费',
        'dis[x][y] = dis[nowx][nowy] + 1': '`dis[{x}][{y}] = {dis[x][y]}`',
        'return dis[-1][-1]': '终点 `dis` = `{ret}`（若仍是 -1 就是到不了）',
    },
    max_steps=110,
    cards=dict(
        one_liner='BFS 里第一次踩到传送门，就把同字母的所有格子一起入队',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['网格里 `.` 是空格，`#` 是障碍，大写字母是传送门',
                 '从左上角走到右下角，走一步算 1 次移动',
                 '踏入字母格可以免费传送到同字母的另一格，每个字母最多用一次',
                 '本视频：`["..A","A#."]` → `2`'],
        quote='对于传送门单元格，如果需要使用某种传送门的话，就应该在首次遇到这种传送门的时候就使用，因为使用传送门可以到达的单元格是相同的，而首次到达这种传送门所需的时间显然小于等于第k次到达这种传送门所需的时间。',
        quote_src='—— yiduobo 题解原文',
        idea=['传送门越早用越好：首次到达它时步数最少',
              '遇到传送门格子，就把同字母的所有格子一起入队，`dis` 都设成当前 `+ 1`',
              '`dis == -1` 去重，所以同字母格子不会被重复展开'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '易错：起点就是传送门时，要把同字母所有格子都作为 BFS 起点（`dis = 0`）',
                 '`dis[tx][ty]` 与走进传送门格的值相同，所以传送「免费」',
                 '原文为 Python 2 风格，但在 Python 3 下无需修改，代码原样运行',
                 '对比灵神：灵神用 0-1 BFS，传送为 0 边权并 `del pos[c]`；这里用普通 BFS 一次性入队'],
    ),
)
