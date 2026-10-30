MAZE = [[0, 1, 0], [0, 1, 0], [0, 0, 0]]
START = [0, 0]
DEST = [0, 2]
ARROW = '←↑→↓'
NAMES = '左上右下'


def _target(S):
    k, v = S['index'], S['d'][S['index']][S['nowx']][S['nowy']]
    return (S['nowx'], S['nowy'] + v) if k % 2 == 0 else (S['nowx'] + v, S['nowy'])


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    m, n = len(MAZE), len(MAZE[0])
    cv.text((x0 + 18, y0 + 4), '迷宫（黄 = 起点，绿 = 终点，蓝 = 已确定最短距离的停点，中间大数字 = 最短距离）', 20, T['muted'], bold=True)
    cell = min(120, (x1 - x0 - 40) / n, (y1 - y0 - 60) / m)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    sy = y0 + 48
    d = S.get('d')
    dis = S.get('dis') or {}
    cur = (S['nowx'], S['nowy']) if 'heap' in S and 'nowx' in S else None
    tgt = None
    if cur and 'index' in S and S.get('_line') in (HEAPPUSH,):
        tgt = _target(S)
    for i in range(m):
        for j in range(n):
            X, Y = sx + j * cell, sy + i * cell
            wall = MAZE[i][j] == 1
            fill = (35, 38, 44) if wall else T['panel2']
            if not wall and (i, j) in dis:
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
                        cv.text(pos[k][:2], f'{ARROW[k]}{v}', 17, tc, anchor=pos[k][2], bold=True)
            else:
                cv.text((X + cell / 2, Y + cell / 2), '空', 22, T['dim'], anchor='mm')
            if (i, j) in dis:
                cv.text((X + cell / 2, Y + cell / 2), dis[(i, j)], 34, T['bg'], anchor='mm', bold=True)
    if cur:
        X, Y = sx + cur[1] * cell, sy + cur[0] * cell
        cv.rect((X - 1, Y - 1, X + cell + 1, Y + cell + 1), outline=T['blue'], width=5, r=10)
    if tgt and 0 <= tgt[0] < m and 0 <= tgt[1] < n:
        X, Y = sx + tgt[1] * cell, sy + tgt[0] * cell
        cv.rect((X - 1, Y - 1, X + cell + 1, Y + cell + 1), outline=T['pink'], width=5, r=10)


def _push(S, B, r):
    k = S.index
    v = abs(S.d[k][S.nowx][S.nowy])
    tx, ty = _target(S)
    if v == 0:
        return f'往{NAMES[k]}踢不动→ 推入原地（稍后丢弃）'
    return f'往{NAMES[k]}滚 `{v}` 格到 `({tx},{ty})`：距离 `{S.nowd} + {v}` = =={S.nowd + v}==，推入堆'


CONFIG = dict(
    num=505, title='迷宫 II', difficulty='Medium', category='网格图',
    author='yiduobo', technique='预处理滚动距离 + Dijkstra',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def shortestDistance(self, maze, start, destination):

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

        dis = {}
        path = {}
        heap = [[0, start[0], start[1]]]

        while heap:
            nowd, nowx, nowy = heapq.heappop(heap)
            key = (nowx, nowy)

            if key not in dis:
                dis[key] = nowd
            else:
                continue
            
            for index in range(4):
                x = nowx
                y = nowy
                if index % 2 == 0:
                    y += d[index][nowx][nowy]
                else:
                    x += d[index][nowx][nowy]
                
                heapq.heappush(heap, [nowd + abs(d[index][nowx][nowy]), x, y])

        return dis.get((destination[0], destination[1]), -1)
''',
    call=f'Solution().shortestDistance({MAZE}, {START}, {DEST})',
    expect=6,
    skip=['m = len', 'n = len', 'def get_len', 'if startx < endx', 'deltax =', 'if starty < endy', 'deltay =',
          'for i in range(startx', 'cnt = None', 'for j in range(starty', 'final_i =', 'final_j =',
          'if maze[final_i]', 'if cnt is None', 'cnt = 0', 'cnt += delta', 'f[final_i]',
          'for index in range(4)', 'x = nowx', 'y = nowy', 'if index % 2', 'y += d', 'x += d',
          'key = (nowx', 'path = {}', 'while heap', 'continue'],
    max_steps=110,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='heap', var='heap', fmt=lambda x: f'{x[0]}:({x[1]},{x[2]})',
             label='heap（小根堆：距离 : 停点）', h=240),
    ],
    watch=[('nowd', 'nowd', 'blue'), ('已确定', 'len(dis)', 'green')],
    captions={
        'd = [[[0': '`d[k][i][j]`：从格子 `(i,j)` 往第 k 个方向（左、上、右、下）滚动，==能走多少格==，先全设为 0',
        'get_len(0, m, 0, n': '预处理「向左」：每行从左往右扫，遇墙清零，数出每格离左侧停点的距离',
        'get_len(0, n, 0, m': '预处理「向上」：每列从上往下扫',
        'get_len(0, m, n - 1': '预处理「向右」：每行从右往左扫',
        'get_len(0, n, m - 1': '预处理「向下」：四个方向都有了，==滚一次 = 查一次表，代价就是格数==',
        'dis = {}': '`dis` 记录每个停点的最短距离',
        'heap = [[0': '堆里放 `[距离, x, y]`，起点距离 0',
        'while heap': lambda S, B, r: ('堆非空，继续取最小距离的停点' if B.heap else '堆空了：能到的停点都确定了'),
        'heapq.heappop': '弹出距离最小的 `[{nowd}, {nowx}, {nowy}]`（堆非空才继续）',
        'if key not in dis': lambda S, B, r: (f'`({S.nowx},{S.nowy})` 第一次弹出 → ==这就是它的最短距离== `{S.nowd}`' if (S.nowx, S.nowy) not in B.dis
                                              else f'`({S.nowx},{S.nowy})` 早就确定过了 → 这条旧记录丢弃'),
        'dis[key] = nowd': '记下 `dis[({nowx},{nowy})] = {nowd}`',
        'continue': '已经确定过，丢弃这条旧记录，取下一个',
        'heapq.heappush': _push,
        'return dis.get': '终点 `({destination[0]},{destination[1]})` 的最短距离：=={ret}==（没到过则返回 `-1`）',
    },
    cards=dict(
        one_liner='把 490 题最后的 BFS 换成 Dijkstra，边权就是滚动的格数',
        complexity='时间 `O(mn log(mn))`，空间 `O(mn)`',
        problem=['和 490 题一样：球朝一个方向滚动，==撞墙才停==',
                 '求从起点滚到终点（必须停在终点）的最短距离，到不了返回 `-1`',
                 '本视频：3×3 迷宫，起点 `[0,0]`，终点 `[0,2]` → `6`（下、右、上各滚 2 格）'],
        quote='直接在490题的基础上，将最后的bfs改成dijkstra算法计算最短路就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['同 490：预处理 `d[方向][i][j]`，滚一次就是一条边，权值 = 滚动的格数',
              '边权不再是 1，所以 BFS 换成小根堆的 Dijkstra',
              '每个停点第一次弹出时的距离就是最短距离，之后再弹出的直接丢弃'],
        summary=['时间 `O(mn log(mn))`：每个停点最多展开一次，堆操作 `O(log)`',
                 '往贴墙的方向推入的是原地、距离不变的记录，会被 `dis` 判重丢弃',
                 '`path` 是 499 题（洞）用的，本题没用上',
                 '代码在 Python 3 下直接可运行，未做修改；预处理内部循环已折叠，只展示每个方向扫完的结果'],
    ),
)
HEAPPUSH = 61
