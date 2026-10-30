TERRAIN = [[3, 0, 2]]
OBSTACLE = [[0, 1, 0]]


def _vis_cells(S):
    if 'vis' not in S:
        return None
    return [[','.join(str(s) for s in range(len(S['vis'][i][j])) if S['vis'][i][j][s]) for j in range(len(S['vis'][i]))]
            for i in range(len(S['vis']))]


CONFIG = dict(
    num='LCP 45', title='自行车炫技赛场', difficulty='Medium', category='网格图',
    author='yiduobo', technique='BFS · 先估速度上限',
    tags=['灵神题单', '网格图'],
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
    call=f'Solution().bicycleYard([0, 0], {TERRAIN}, {OBSTACLE})',
    expect=[[0, 2]],
    views=[
        dict(type='grid', var='terrain', label='terrain（蓝框 = 出队位置，粉框 = 邻居）', cell=80, h=230,
             cursors=[('nowx', 'nowy', 'blue'), ('x if _line in (19, 21, 22, 23, 24, 25, 26) else None', 'y', 'pink')]),
        dict(type='grid', var=_vis_cells, label='vis[x][y]：到过的速度（绿 = 含速度 1）', cell=110, h=240,
             color=lambda S, i, j, v: 'green' if '1' in v.split(',') else None),
        dict(type='array', var=lambda S: [f'({a},{b},{c})' for a, b, c in S['q']] if 'q' in S else None,
             label='q（暗 = 已出队，head 指向下一个出队的）', cell=110, h=190, pointers={'head': 'blue'},
             dim=lambda S, i, v: i < S.get('head', 0)),
    ],
    watch=[('head', 'head', 'blue'), ('tail', 'tail'), ('nowv', 'nowv', 'blue'), ('v', 'v', 'pink'), ('res', 'res', 'green')],
    captions={
        'max_v = 101': '速度上限：只有下坡才加速，==h 与 o 都非负==，最大是 `1 + 100 = 101`',
        'vis = [[[False]': '`vis[x][y][v]`：是否能以速度 `v` 到达 `(x,y)`',
        'vis[position[0]]': '起点速度为 1，先标记',
        'q = [[position': '用数组当 BFS 队列，`head`、`tail` 是队首和队尾',
        'while head < tail': lambda S, B, r: (f'`head = {B.head} < tail = {B.tail}`：队列不空，继续' if B.head < B.tail else '`head == tail`：队列空了，所有状态都搜完'),
        'nowx, nowy, nowv = q[head]': '`head` 后移一位，出队：位置 `({nowx},{nowy})`，速度 `{nowv}`',
        'y = nowy': '朝方向 `{index}` 看邻居 `({x},{y})`',
        'if x >= 0': lambda S, B, r: (f'`({S.x},{S.y})` 在界内' if 0 <= S.x < S.m and 0 <= S.y < S.n else f'`({S.x},{S.y})` 出界，跳过'),
        'v = nowv': '新速度 `v = {nowv} + {terrain[nowx][nowy]} - {terrain[x][y]} - {obstacle[x][y]}` = =={v}==',
        'if v > 0': lambda S, B, r: (f'`v = {S.v}`，且 `({S.x},{S.y})` 没以这个速度到过 → 入队' if S.v > 0 and not S.vis[S.x][S.y][S.v] else (f'`v = {S.v} <= 0`：停车了，不能走' if S.v <= 0 else f'`({S.x},{S.y})` 速度 `{S.v}` 已到过，不重复入队')),
        'q.append': '`({x},{y},{v})` 入队',
        'vis[x][y][v] = True': '标记 `vis[{x}][{y}][{v}]`',
        'res = []': 'BFS 完毕，开始收集答案',
        '(x != position[0]': lambda S, B, r: (f'`({S.x},{S.y})` 是起点，不算' if (S.x == S.position[0] and S.y == S.position[1]) else (f'`({S.x},{S.y})` 速度 1 到过过 → 加入答案' if S.vis[S.x][S.y][1] else f'`({S.x},{S.y})` 速度 1 没到过')).replace('到过过', '到过'),
        'res.append': '答案加入 `({x},{y})`',
    },
    skip=['dx = [', 'dy = [', 'head, tail = 0', 'head += 1', 'tail += 1', 'x = nowx', 'for index in range(4)'],
    max_steps=110,
    cards=dict(
        one_liner='先证明速度不会超过 101，再对 (位置, 速度) 做 BFS',
        complexity='时间 `O(mn·101)`，空间 `O(mn·101)`',
        problem=['从 `h1` 走到相邻 `h2`，速度变化 `h1 - h2 - o2`，初速度 1',
                 '问哪些位置（不含起点）能刚好以速度 1 到达，要保持速度 `> 0`',
                 '本视频：`terrain = [[3,0,2]]`，`obstacle = [[0,1,0]]`'],
        quote='走到hk的速度就应该是1 + h1 - hk - o2 - o3 - ... - ok。由于式子中的h和o都是非负数，那么实际上最大的v就是h1取上限，后面全部取0的情况，也就是101。',
        quote_src='—— yiduobo 题解原文',
        idea=['先问：状态 `f[x][y][v]` 的 `v` 会不会无限大？', '速度沿路径是 `1 + h1 - hk - o2 - ... - ok`，只会越走越小，上限 101',
              '于是三维 BFS 可行，最后看 `v = 1` 的格子'],
        summary=['时间、空间 `O(mn·101)`',
                 '先估 `v` 的上限是这题的关键推导',
                 '起点要排除：`(x != position[0] or y != position[1])`',
                 '原文为 Python 2 风格，代码无需改动（已是 Python 3 可运行）'],
    ),
)
