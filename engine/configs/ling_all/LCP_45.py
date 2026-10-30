TERRAIN = [[3, 0, 2]]
OBSTACLE = [[0, 1, 0]]


def _vis_cells(S):
    if 'vis' not in S:
        return None
    return [[','.join(str(s) for s in range(102) if S['vis'][i][j][s]) for j in range(len(S['vis'][i]))]
            for i in range(len(S['vis']))]


CONFIG = dict(
    num='LCP 45', title='自行车炫技赛场', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='BFS（状态 x,y,speed）（Go 原文转写）',
    tags=['灵神题单', '网格图'],
    code='''
dir4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

class Solution:
    def bicycleYard(self, position: List[int], terrain: List[List[int]], obstacle: List[List[int]]) -> List[List[int]]:
        ans = []
        n, m = len(terrain), len(terrain[0])
        vis = [[[False] * 102 for _ in range(m)] for _ in range(n)]

        sx, sy = position[0], position[1]
        vis[sx][sy][1] = True
        q = [(sx, sy, 1)]
        while len(q) > 0:
            p = q[0]
            q = q[1:]
            x, y, speed = p
            for dx, dy in dir4:
                xx, yy = x + dx, y + dy
                if 0 <= xx < n and 0 <= yy < m:
                    s = speed + terrain[x][y] - terrain[xx][yy] - obstacle[xx][yy]
                    if s > 0 and not vis[xx][yy][s]:
                        vis[xx][yy][s] = True
                        q.append((xx, yy, s))

        vis[sx][sy][1] = False  # 起点不计入答案
        for i, row in enumerate(vis):
            for j, b in enumerate(row):
                if b[1]:
                    ans.append([i, j])
        return ans
''',
    call=f'Solution().bicycleYard([0, 0], {TERRAIN}, {OBSTACLE})',
    expect=[[0, 2]],
    views=[
        dict(type='grid', var='terrain', label='terrain（蓝框 = 出队位置，粉框 = 邻居）', cell=80, h=250,
             cursors=[('x', 'y', 'blue'), ('xx if _line in (17, 18, 19, 20, 21) else None', 'yy', 'pink')]),
        dict(type='grid', var=_vis_cells, label='vis：每格到达过的速度集合（黄 = 刚加入；绿 = 含速度 1）', cell=110, h=260,
             color=lambda S, i, j, v: 'green' if '1' in v.split(',') else None),
        dict(type='array', var=lambda S: [f'({a},{b},{c})' for a, b, c in S['q']] if 'q' in S else None,
             label='q（队列：x, y, speed）', cell=110, h=170),
    ],
    watch=[('speed', 'speed', 'blue'), ('s', 's', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'vis = [[[False]': '`vis[x][y][s]`：到过 `(x,y)` 且速度为 `s` 吗？速度最大 101，所以开 102 格',
        'vis[sx][sy][1] = True': '起点 `({sx},{sy})`，速度 1 入状态',
        'q = [(sx, sy, 1)]': 'BFS 队列里放 `(x, y, speed)` 三元组',
        'while len(q) > 0': lambda S, B, r: (f'队列里还有 `{len(B.q)}` 个状态 → 继续取队首' if len(B.q) > 0 else '队列空了，所有可达状态都搜完'),
        'x, y, speed = p': '取队首并出队：位置 `({x},{y})`，速度 `{speed}`',
        'xx, yy = x + dx, y + dy': '看邻居 `({xx},{yy})`',
        '0 <= xx < n': lambda S, B, r: (f'`({S.xx},{S.yy})` 在场地内' if 0 <= S.xx < S.n and 0 <= S.yy < S.m else f'`({S.xx},{S.yy})` 出界，换下一个方向'),
        's = speed + terrain': '新速度 `s = {speed} + {terrain[x][y]} - {terrain[xx][yy]} - {obstacle[xx][yy]}` = =={s}==',
        'if s > 0 and not vis': lambda S, B, r: (f'`s = {S.s}` 且这个状态没到过 → 值得继续' if S.s > 0 and not S.vis[S.xx][S.yy][S.s] else (f'`s = {S.s} <= 0`：速度不能为 0 或负，不能走' if S.s <= 0 else f'`({S.xx},{S.yy})` 速度 `{S.s}` 已经到过，不重复入队')),
        'vis[xx][yy][s] = True': '标记 `({xx},{yy})` 速度 `{s}` 已访问',
        'q.append': '入队 `({xx},{yy},{s})`',
        'vis[sx][sy][1] = False': '起点一开始标过速度 1，但题目要求「其他位置」→ 清掉',
        'if b[1]': lambda S, B, r: (f'`({S.i},{S.j})` 速度 1 到过 → 计入答案' if S.b[1] else f'`({S.i},{S.j})` 速度 1 没到过'),
        'ans.append': '答案加入 `({i},{j})`',
    },
    skip=['for dx, dy in dir4', 'p = q[0]', 'q = q[1:]'],
    max_steps=90,
    cards=dict(
        one_liner='速度有上限 101，把 (x, y, speed) 当状态跑 BFS',
        complexity='时间 `O(nm·101)`，空间 `O(nm·101)`',
        problem=['从 `h1` 走到相邻 `h2`，速度变化 `h1 - h2 - o2`，初速度 1',
                 '求哪些位置（不含起点）能刚好以速度 1 到达',
                 '骑行过程中速度必须始终 `> 0`'],
        quote='根据题目的数据范围，选手到任意位置的速度至多为 101，那么可以用 (x,y,speed) 表示状态，从起点 (position[0],position[1],1) 开始跑 BFS。',
        quote_src='—— 灵茶山艾府题解',
        idea=['速度只有 1~101 共 102 种取值，状态数有限', 'BFS 结束后，凡是 `vis[x][y][1]` 为真的格子都是答案',
              '起点一开始就标记过，必须最后清掉'],
        summary=['时间、空间都是 `O(nm·U)`，`U = 102`',
                 '易错：起点不计入答案，最后要 `vis[sx][sy][1] = False`',
                 '易错：速度 `s <= 0` 不能走',
                 '原文为 Go，已按原逻辑逐行转写为 Python'],
    ),
)
