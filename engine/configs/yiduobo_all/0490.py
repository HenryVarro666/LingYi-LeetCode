MAZE = [[0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [1, 1, 0, 0, 0]]
START = [0, 4]
DEST = [3, 2]
ARROW = '←↑→↓'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    m, n = len(MAZE), len(MAZE[0])
    cv.text((x0 + 18, y0 + 4), '迷宫（黑 = 墙，黄 = 起点，绿 = 终点，蓝 = 已到过的停点；格内数字 = 往该方向滚动能走的格数）', 20, T['muted'], bold=True)
    cell = min(112, (x1 - x0 - 40) / n, (y1 - y0 - 60) / m)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    sy = y0 + 48
    d = S.get('d')
    bfs = 'head' in S
    vis = S.get('vis') or set()
    cur = (S['nowx'], S['nowy']) if bfs and 'nowx' in S else None
    tgt = None
    if bfs and 'index' in S and 'nowx' in S:
        ln = S.get('_line')
        v = d[S['index']][S['nowx']][S['nowy']]
        if ln == 47 and v != 0:
            tgt = (S['nowx'], S['nowy'] + v) if S['index'] % 2 == 0 else (S['nowx'] + v, S['nowy'])
        elif ln in (55, 56, 60) and 'x' in S:
            tgt = (S['x'], S['y'])
    for i in range(m):
        for j in range(n):
            X, Y = sx + j * cell, sy + i * cell
            wall = MAZE[i][j] == 1
            fill = (35, 38, 44) if wall else T['panel2']
            if not wall and (i, j) in vis:
                fill = T['blue']
            if [i, j] == START:
                fill = T['yellow']
            if [i, j] == DEST:
                fill = T['green']
            cv.rect((X + 2, Y + 2, X + cell - 2, Y + cell - 2), fill=fill, r=8, outline=T['border'])
            if wall:
                continue
            lit = fill != T['panel2']
            tc = T['bg'] if lit else T['muted']
            if d is not None:
                pos = [(X + 8, Y + cell / 2, 'lm'), (X + cell / 2, Y + 6, 'mt'), (X + cell - 8, Y + cell / 2, 'rm'),
                       (X + cell / 2, Y + cell - 6, 'mb')]
                for k in range(4):
                    v = abs(d[k][i][j])
                    if v:
                        cv.text(pos[k][:2], f'{ARROW[k]}{v}', 19, tc, anchor=pos[k][2], bold=True)
            else:
                cv.text((X + cell / 2, Y + cell / 2), '空', 22, T['dim'], anchor='mm')
    if cur:
        X, Y = sx + cur[1] * cell, sy + cur[0] * cell
        cv.rect((X - 1, Y - 1, X + cell + 1, Y + cell + 1), outline=T['blue'], width=5, r=10)
    if tgt and 0 <= tgt[0] < m and 0 <= tgt[1] < n:
        X, Y = sx + tgt[1] * cell, sy + tgt[0] * cell
        cv.rect((X - 1, Y - 1, X + cell + 1, Y + cell + 1), outline=T['pink'], width=5, r=10)


def _roll(S, B, r):
    k = S.index
    v = S.d[k][S.nowx][S.nowy]
    names = '左上右下'
    if v == 0:
        return f'`({S.nowx},{S.nowy})` 往{names[k]}踢：一步也动不了（`d = 0`）→ 跳过'
    tx, ty = (S.nowx, S.nowy + v) if k % 2 == 0 else (S.nowx + v, S.nowy)
    return f'`({S.nowx},{S.nowy})` 往{names[k]}踢，滚动 `{abs(v)}` 格，停在 `({tx},{ty})`'


def _vis(S, B, r):
    if (S.x, S.y) in B.vis:
        return f'`({S.x},{S.y})` 已经到过 → 不重复入队'
    return f'`({S.x},{S.y})` 是新的停点 → ==加入 vis 并入队=='


CONFIG = dict(
    num=490, title='迷宫', difficulty='Medium', category='网格图',
    author='yiduobo', technique='预处理滚动距离 + BFS',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def hasPath(self, maze, start, destination):

        m = len(maze)
        n = len(maze[0])

        d = [[[0 for j in range(n)] for i in range(m)] for _ in range(4)]

        def get_len(startx, endx, starty, endy, trans, delta, f):
            if startx < endx:
                deltax = 1
            else:
                deltax = -1

            if starty < endy:
                deltay = 1
            else:
                deltay = -1

            for i in range(startx, endx, deltax):
                cnt = None
                for j in range(starty, endy, deltay):
                    final_i = trans[0] * i + trans[1] * j
                    final_j = trans[0] * j + trans[1] * i
                    if maze[final_i][final_j] == 0:
                        if cnt is None:
                            cnt = 0
                        else:
                            cnt += delta
                            f[final_i][final_j] = cnt
                    else:
                        cnt = None

        get_len(0, m, 0, n, [1, 0], -1, d[0])
        get_len(0, n, 0, m, [0, 1], -1, d[1])
        get_len(0, m, n - 1, -1, [1, 0], 1, d[2])
        get_len(0, n, m - 1, -1, [0, 1], 1, d[3])

        vis = set([(start[0], start[1])])
        q = [start]
        head, tail = 0, 1
        while head < tail:
            nowx, nowy = q[head]
            head += 1
            
            for index in range(4):
                if d[index][nowx][nowy] != 0:
                    x = nowx
                    y = nowy
                    if index % 2 == 0:
                        y += d[index][nowx][nowy]
                    else:
                        x += d[index][nowx][nowy]

                    if (x, y) not in vis:
                        vis.add((x, y))
                        q.append([x, y])
                        tail += 1
                    
                    if (destination[0], destination[1]) in vis:
                        return True

        return False
''',
    call=f'Solution().hasPath({MAZE}, {START}, {DEST})',
    expect=True,
    skip=['m = len', 'n = len', 'def get_len', 'if startx < endx', 'deltax =', 'if starty < endy', 'deltay =',
          'for i in range(startx', 'cnt = None', 'for j in range(starty', 'final_i =', 'final_j =',
          'if maze[final_i]', 'if cnt is None', 'cnt = 0', 'cnt += delta', 'f[final_i]',
          'for index in range(4)', 'x = nowx', 'y = nowy', 'if index % 2', 'y += d', 'x += d',
          'q.append([x, y])', 'vis.add', 'tail += 1', 'head += 1', 'head, tail = 0, 1'],
    max_steps=80,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']] if 'q' in S else None,
             label='q（暗 = 已出队，head 指向下一个出队的）', cell=80, pointers={'head': 'blue'},
             dim=lambda S, i, v: i < S.get('head', 0), h=170),
    ],
    watch=[('head', 'head', 'blue'), ('tail', 'tail', 'pink'), ('vis', 'len(vis)', 'green')],
    captions={
        'd = [[[0': '`d[k][i][j]`：从格子 `(i,j)` 往第 k 个方向（左、上、右、下）踢，==能滚动多少格==，先全设为 0',
        'get_len(0, m, 0, n': '预处理「向左」：每行从左往右扫，遇墙清零，数出每格离==左侧停点==的距离（存负数）',
        'get_len(0, n, 0, m': '预处理「向上」：每列从上往下扫，同样数到上方停点的距离',
        'get_len(0, m, n - 1': '预处理「向右」：每行从右往左扫，距离存正数',
        'get_len(0, n, m - 1': '预处理「向下」：每列从下往上扫。四个方向都有了，==每次踢球 O(1) 查表==',
        'vis = set': '`vis` 记录已到过的停点，起点 `({start[0]},{start[1]})` 先放进去',
        'q = [start]': '起点入队，开始 BFS',
        'while head < tail': lambda S, B, r: (f'`head = {B.head} < tail = {B.tail}`：队列还有停点，继续' if B.head < B.tail
                                              else f'`head = {B.head} >= tail = {B.tail}`：队列空了，终点没被到过'),
        'nowx, nowy = q[head]': '出队停点 `({nowx},{nowy})`：依次往左、上、右、下踢球',
        'if d[index][nowx][nowy] != 0': _roll,
        'if (x, y) not in vis': _vis,
        'if (destination[0], destination[1]) in vis': lambda S, B, r: (
            f'终点 `({B.destination[0]},{B.destination[1]})` 已在 vis 里 → ==可以到达==' if (S.destination[0], S.destination[1]) in S.vis
            else f'终点 `({S.destination[0]},{S.destination[1]})` 还不在 vis 里，继续'),
        'return True': '球能停在终点：返回 `True`',
        'return False': 'BFS 结束都没停在终点：返回 `False`',
    },
    cards=dict(
        one_liner='球一滚到底，先预处理每格往四个方向的滚动距离，再 BFS',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['迷宫里 `0` 是空地、`1` 是墙，球朝一个方向滚动，==撞墙才停==',
                 '给定起点和终点，判断球能否刚好停在终点',
                 '本视频：4×5 迷宫，起点 `[0,4]`，终点 `[3,2]` → `True`'],
        quote='当球往某个方向踢出去时，其停下的位置也随之确定了。在这里为了提高效率，可以提前预处理出球从每个空格向四个方向踢出去后停下的位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['停下的位置只由方向决定：==预处理 `d[方向][i][j]`== 记录滚动格数',
              '预处理沿每行 / 每列扫一遍，遇到墙就把计数清零',
              'BFS 的节点只有「停点」，每次向四个方向各查一次表'],
        summary=['时间 `O(mn)`：预处理 4 次扫描 + BFS 每个停点最多处理一次',
                 '终点必须是球==停下==的位置，滚过终点不算',
                 '`d` 等于 0 表示这个方向一步也动不了（贴墙）',
                 '代码在 Python 3 下直接可运行，未做修改；视频中预处理的内部循环已折叠，只展示每个方向扫完的结果'],
    ),
)
