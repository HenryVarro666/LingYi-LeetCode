POS, TER, OBS = [0, 0], [[2, 1], [0, 0]], [[0, 0], [0, 1]]


def _speeds(S):
    vis = S.get('vis')
    if vis is None:
        return ''
    rows = []
    for i, r in enumerate(vis):
        for j, c in enumerate(r):
            vs = [v for v, ok in enumerate(c) if ok]
            rows.append(f'`({i},{j})`: 速度 {vs if vs else "无"}')
    return '访问过的状态（位置, 速度）：\n' + '    '.join(rows)


def _cell(S, i, j, v):
    vis = S.get('vis')
    if vis and vis[i][j][1] and (i, j) != tuple(POS):
        return 'green'
    return None


def _ok(S, B, r):
    x, y = S.x, S.y
    if not (0 <= x < S.m and 0 <= y < S.n):
        return f'邻居 `({x},{y})` 出界，跳过'
    return f'邻居 `({x},{y})` 在场地内，算新速度'


def _nv(S, B, r):
    return (f'`v = {S.nowv} + {S.terrain[S.nowx][S.nowy]} − {S.terrain[S.x][S.y]} − {S.obstacle[S.x][S.y]}` = =={S.v}=='
            '；' + _new(S, B, r))


def _new(S, B, r):
    if S.v <= 0:
        return f'`v = {S.v} <= 0`：骑不动了，这条路作废'
    if B.vis[S.x][S.y][S.v]:
        return f'`({S.x},{S.y})` 速度 `{S.v}` 以前来过 → 不重复入队'
    return f'`({S.x},{S.y})` 第一次以速度 `{S.v}` 到达 → ==入队=='


CONFIG = dict(
    num='LCP 45', title='自行车炫技赛场', difficulty='Medium', category='网格图',
    author='yiduobo', technique='BFS · 状态 (x, y, 速度)',
    tags=['网格图'],
    code='''
class Solution(object):
    def bicycleYard(self, position, terrain, obstacle):

        m = len(terrain)
        n = len(terrain[0])
        max_v = 101

        vis = [[[False] * (max_v + 1) for _ in range(n)] for _ in range(m)]
        vis[position[0]][position[1]][1] = True
        q = [[position[0], position[1], 1]]
        head, tail = 0, 1
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        while head < tail:
            nowx, nowy, nowv = q[head]
            head += 1
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                
                if x >= 0 and x < m and y >= 0 and y < n:
                    v = nowv + terrain[nowx][nowy] - terrain[x][y] - obstacle[x][y]
                    if v > 0 and not vis[x][y][v]:
                        q.append([x, y, v])
                        tail += 1
                        vis[x][y][v] = True
        
        res = []
        for x in range(m):
            for y in range(n):
                if (x != position[0] or y != position[1]) and vis[x][y][1]:
                    res.append([x, y])
        
        return res
''',
    call=f'Solution().bicycleYard({POS}, {TER}, {OBS})',
    expect=[[0, 1], [1, 0], [1, 1]],
    skip=['m = len', 'n = len', 'max_v = 101', 'vis = [[[False]', 'head, tail = 0, 1', 'dx = [', 'dy = [',
          'head += 1', 'for index in range(4)', 'x = nowx', 'y = nowy', 'tail += 1', 'for y in range(n)', 'vis[x][y][v] = True', 'if v > 0 and not vis', 'if x >= 0 and x < m'],
    max_steps=90,
    views=[
        dict(type='grid', var='terrain', label='terrain（高度；蓝框 = 当前出队的位置，粉框 = 邻居，绿 = 能以速度 1 到达）', cell=100, h=250,
             color=_cell, cursors=[('nowx', 'nowy', 'blue'), ("x if _line in (19, 20, 21, 22, 23, 24) else None", 'y', 'pink')]),
        dict(type='grid', var='obstacle', label='obstacle（减速值）', cell=70, h=170),
        dict(type='array', var=lambda S: [f'{a}{b}/{c}' for a, b, c in S['q']] if 'q' in S else None,
             label='q（位置 xy / 速度；暗 = 已处理，head 指向下一个出队的）', cell=110, pointers={'head': 'blue'},
             dim=lambda S, i, v: i < S.get('head', 0), h=150),
        dict(type='text', fn=_speeds, size=21, h=90),
    ],
    watch=[('head', 'head', 'blue'), ('tail', 'tail'), ('nowv', 'nowv', 'cyan'), ('v', 'v', 'pink')],
    captions={
        'vis[position[0]][position[1]][1] = True': '起点以速度 1 出发：状态 `(起点, 1)` 标记为访问过',
        'q = [[position': '起点状态入队',
        'while head < tail': lambda S, B, r: (f'队列里还有 `{B.tail - B.head}` 个状态没处理，继续 BFS' if B.head < B.tail
                                              else '队列空了：所有可达的 (位置, 速度) 都找全了'),
        'nowx, nowy, nowv = q[head]': '出队 `({nowx},{nowy})`，速度 `{nowv}`，向四个邻居骑',
        'if x >= 0 and x < m': _ok,
        'v = nowv + terrain': _nv,
        'q.append': '状态 `({x},{y}, v={v})` 入队并标记访问：速度最大 101，可直接开三维数组',
        'vis[x][y][v] = True': '标记访问：速度范围小（最大 101），可以直接开三维数组',
        'res = []': 'BFS 结束，收集答案：哪些位置的 `vis[x][y][1]` 为真',
        'if (x != position[0]': lambda S, B, r: (f'`({S.x},{S.y})` 是起点自己，不算' if (S.x, S.y) == tuple(S.position)
                                                  else (f'`({S.x},{S.y})` 能以速度 1 到达 → ==收进答案==' if S.vis[S.x][S.y][1]
                                                        else f'`({S.x},{S.y})` 到不了速度 1，不收')),
        'return res': '返回 `{res}`（按行、列升序扫出来，天然有序）',
    },
    cards=dict(
        one_liner='速度有上限 101，把「位置 + 速度」当状态做 BFS',
        complexity='时间 `O(n·m·101)`，空间 `O(n·m·101)`',
        problem=['每走一步，速度变化 = `h1 − h2 − o2`（高度差 − 目标格减速）',
                 '起点速度为 1，骑行中速度不能 `<= 0`',
                 '求能==刚好以速度 1==到达的其他位置，按行、列升序返回',
                 '示例：`position=[1,1]`，`terrain=[[5,0],[0,6]]` → `[[0,1]]`；本视频用另一个 2×2 例子'],
        quote='最大的v就是h1取上限，后面全部取0的情况，也就是==101==。这个数据规模是完全可行的。',
        quote_src='—— yiduobo 题解原文',
        idea=['怕速度没有上限？推一下：走到 `hk` 时速度 = `1 + h1 − hk − o2 − … − ok`',
              'h、o 都 ≥ 0，所以速度 `<= 1 + h1 <= 101`，状态只有 `n·m·102` 个',
              '`vis[x][y][v]` 记录 (位置, 速度) 是否到过，从起点速度 1 出发 BFS',
              '最后扫一遍：`vis[x][y][1]` 为真且不是起点的位置，就是答案'],
        summary=['时间、空间都是 `O(n·m·101)`',
                 '易错：起点不能算进答案；`v <= 0` 的状态必须丢弃',
                 '关键是先证明速度上界，才敢开三维数组',
                 '原文为 Python 2 风格，代码未做改动（直接是 Python 3 可运行）'],
    ),
)
