MAZE = [[0, 0, 0], [0, 1, 0]]
BALL, HOLE = [1, 2], [0, 0]
DIRN = ['左 l', '上 u', '右 r', '下 d']


def _mcolor(S, i, j, v):
    if v == 1:
        return 'orange'
    if 'dis' in S and (i, j) in S['dis']:
        return 'green'
    return None


def _draw_d(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '预处理 d[方向][格子]：朝该方向滚到停下的距离（左/上为负）', 22, T['muted'], bold=True)
    d = S.get('d')
    if not d:
        cv.text(((x0 + x1) / 2, (y0 + y1) / 2 + 10), '（还没计算）', 26, T['dim'], anchor='mm')
        return
    m, n = len(d[0]), len(d[0][0])
    gap = 24
    cell = min(52, ((x1 - x0 - 40) - 3 * gap) / (4 * n), (y1 - y0 - 100) / m)
    tw = cell * n
    sx = x0 + 20 + ((x1 - x0 - 40) - (4 * tw + 3 * gap)) / 2
    sy = y0 + 76
    for k in range(4):
        X0 = sx + k * (tw + gap)
        cv.text((X0 + tw / 2, sy - 8), DIRN[k], 22, T['text'], anchor='mb', bold=True)
        for i in range(m):
            for j in range(n):
                v = d[k][i][j]
                wall = MAZE[i][j] == 1
                hot = 'nowx' in S and 'index' in S and k == S['index'] and (i, j) == (S['nowx'], S['nowy'])
                fill = T['orange'] if wall else (T['yellow'] if hot else T['panel2'])
                cv.rect((X0 + j * cell + 1, sy + i * cell + 1, X0 + (j + 1) * cell - 1, sy + (i + 1) * cell - 1), fill=fill, r=5, outline=T['border'])
                if not wall:
                    cv.text((X0 + j * cell + cell / 2, sy + i * cell + cell / 2), v, 22, T['bg'] if hot else T['text'], anchor='mm', bold=True)


CONFIG = dict(
    num=499, title='迷宫 III', difficulty='Hard', category='网格图',
    author='yiduobo', technique='预处理滚动距离 + Dijkstra（带路径）',
    tags=['灵神题单', '网格图'],
    code='''
class Solution(object):
    def findShortestWay(self, maze, ball, hole):

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
                        if cnt is None or (final_i == hole[0] and final_j == hole[1]):
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
        heap = [[0, ball[0], ball[1], None, None, '']]

        dir_char = ['l', 'u', 'r', 'd']

        while heap:
            nowd, nowx, nowy, prex, prey, choose = heapq.heappop(heap)
            key = (nowx, nowy)

            if key not in dis:
                dis[key] = nowd
                if prex is not None:
                    path[key] = path[(prex, prey)] + choose
                else:
                    path[key] = ''
            else:
                if dis[key] == nowd and prex is not None:
                    new_path = path[(prex, prey)] + choose
                    if new_path < path[key]:
                        path[key] = new_path
                continue
            
            for index in range(4):
                x = nowx
                y = nowy
                if index % 2 == 0:
                    y += d[index][nowx][nowy]
                else:
                    x += d[index][nowx][nowy]
                
                heapq.heappush(heap, [nowd + abs(d[index][nowx][nowy]), x, y, nowx, nowy, dir_char[index]])

        return path.get((hole[0], hole[1]), 'impossible')
''',
    call=f'Solution().findShortestWay({MAZE}, {BALL}, {HOLE})',
    expect='ul',
    skip=['startx', 'starty', 'deltax', 'deltay', 'cnt', 'final_', 'm = len', 'n = len', 'x = nowx', 'y = nowy', 'key = (nowx', 'dir_char = [', 'for index in range(4)', 'index % 2', 'new_path = path', 'if new_path < path[key]', 'continue', 'y += d[index]', 'x += d[index]'],
    max_steps=62,
    views=[
        dict(type='grid', var='maze', label='maze（橙墙，红框 = 洞，蓝框 = 出发点，粉框 = 停点，绿 = 已定）', cell=76, h=260,
             color=_mcolor, cursors=[(str(HOLE[0]), str(HOLE[1]), 'red'), ('nowx', 'nowy', 'blue'),
                                     ('x if _line == 70 else None', 'y', 'pink')]),
        dict(type='custom', draw=_draw_d, h=190),
        dict(type='map', var='path', label='path（到每个格子的最短路径字符串）', fmt=lambda k, v: f'{k}: "{v}"', h=120),
        dict(type='heap', var='heap', label='heap = [距离, x, y, 来自x, 来自y, 方向]', fmt=lambda e: f'{e[0]}:({e[1]},{e[2]}){e[5]}', h=130),
    ],
    watch=[('nowd', 'nowd', 'blue'), ('choose', 'choose', 'pink'), ('index', 'index')],
    captions={
        'd = [[[0': '`d[k][i][j]`：从 `(i,j)` 朝第 k 个方向（左、上、右、下）滚到停下的==距离==，先全填 0',
        'get_len(0, m, 0, n, [1, 0], -1, d[0])': '向左滚：每行从左往右扫，遇墙清零；距离记成负数。==洞特殊处理==：滚到洞就停在洞里',
        'get_len(0, n, 0, m, [0, 1], -1, d[1])': '向上滚：每列从上往下扫，同样处理墙和洞',
        'get_len(0, m, n - 1, -1, [1, 0], 1, d[2])': '向右滚：每行从右往左扫，距离记成正数',
        'get_len(0, n, m - 1, -1, [0, 1], 1, d[3])': '向下滚：每列从下往上扫。四张表备齐，之后每次「滚一下」都是 `O(1)`',
        'dis = {}': '`dis`：每个停点的最短滚动距离（定下来就不再改）',
        'path = {}': '`path`：到每个停点的最短路径字符串，字典序最小',
        'heap = [': '堆里放 `[已滚距离, x, y, 来自x, 来自y, 方向]`：先出距离最小，距离相同再比 x、y',
        'while heap': lambda S, B, r: (f'堆里还有 `{len(S.heap)}` 个状态 → 继续' if S.heap else '堆空了：能到的停点都定下来了，结束'),
        'heapq.heappop': '弹出==最小==的状态：`({nowx},{nowy})`，已滚 `{nowd}`，最后一步方向 `{choose!r}`',
        'if key not in dis': lambda S, B, r: (f'`({S.nowx},{S.nowy})` 第一次出堆 → 这就是它的最短距离 `{S.nowd}`' if S.key not in S.dis
                                              else f'`({S.nowx},{S.nowy})` 已经定过了 → 只看路径长度是否并列'),
        'dis[key] = nowd': '记下 `dis[({nowx},{nowy})] = {nowd}`',
        'if prex is not None': lambda S, B, r: ('有来源 → 路径 = 来源的路径 + 这一步方向' if S.prex is not None else '起点：没有来源，路径为空串'),
        'path[key] = path[': '`path[({nowx},{nowy})] = "{path[key]}"`（来源路径 + `{choose}`）',
        "path[key] = ''": '起点的路径是空串',
        'dis[key] == nowd and prex': lambda S, B, r: (
            ('这一步原地没动（球贴着墙或洞），不是新路线' if (S.prex, S.prey) == (S.nowx, S.nowy)
             else f'距离 `{S.nowd}` 和已定的 `{S.dis[S.key]}` ==并列最短== → 比较路径字典序')
            if (S.dis[S.key] == S.nowd and S.prex is not None) else '比已定的距离更长，丢弃'),
        'if new_path < path[key]': lambda S, B, r: (
            '原地没动，路径不会更小 → 保留' if (S.prex, S.prey) == (S.nowx, S.nowy) else
            (f'新路径 `{S.new_path!r}` < 现有 `{S.path[S.key]!r}` → ==字典序更小，替换==' if S.new_path < S.path[S.key]
             else f'新路径 `{S.new_path!r}` 不比现有 `{S.path[S.key]!r}` 小 → 保留')),
        'path[key] = new_path': '更新为字典序更小的 `{path[key]!r}`',
        'continue': '这个停点已经处理过，不再展开，取下一个',
        'heapq.heappush': '朝方向 `{dir_char[index]}` 滚：停在 `({x},{y})`，距离 `{nowd}` + `{abs(d[index][nowx][nowy])}` = `{nowd + abs(d[index][nowx][nowy])}`，入堆',
        'return path.get': lambda S, B, r: (f'洞 `{tuple(S.hole)}` 的路径 ==`{r}`== 就是答案' if r != 'impossible' else '洞没被到过 → `impossible`'),
    },
    cards=dict(
        one_liner='球会滚到停下：先预处理滚动距离，再用 Dijkstra 找最短且字典序最小的路径',
        complexity='时间 `O(mn · log(mn))`，空间 `O(mn)`',
        problem=['迷宫里 `0` 空地、`1` 墙；球朝一个方向滚，==撞墙才停==，或者==滚过洞就掉进去==',
                 '求球掉进洞的最短路径（用 `l u r d` 记方向）；有多条就取字典序最小，掉不进去返回 `impossible`',
                 '本视频：`[[0,0,0],[0,1,0]]`，球 `(1,2)`，洞 `(0,0)` → `"ul"`'],
        quote='球最后会落入洞中，那么就可以将其视为某种特殊的障碍物，不过与常规障碍物不同的是，球遇到常规障碍物将停在障碍物相邻的单元格，而对于洞而言则是会停在洞所在的单元格。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把「朝某方向滚到停下」的距离预处理好，洞当作会==在洞里停下==的障碍',
              'Dijkstra 的边权就是滚动距离；另用 `path` 字典记最短路径字符串',
              '最短距离更新、或堆顶弹出的距离恰好等于已知最短时，都要拿字典序更小的路径更新'],
        summary=['时间 `O(mn · log(mn))`，空间 `O(mn)`',
                 '洞的处理：扫描时遇到洞就把 `cnt` 清零，球停在洞里，所以不会穿过洞',
                 '==距离并列时==要比较字符串，否则不满足「字典序最小」',
                 '堆元素把方向放在最后，加上 x、y，天然让距离相同时按位置排',
                 '505 迷宫 II 同款：去掉路径和洞，Dijkstra 的 `dis` 即是答案'],
    ),
)
