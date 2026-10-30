PEN = [[5, 3], [1, 4]]


def _dis(r):
    return lambda S: [[(c[r] if c[r] is not None else '∞') for c in row] for row in S['dis']] if 'dis' in S else [[0]]


def _hfmt(t):
    return f'{t[0]}@({t[1]},{t[2]}) r{t[3]}'


CONFIG = dict(
    num=4003, title='交替方向的最小路径代价 III', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='分层图最短路 + Dijkstra',
    tags=[],
    code='''
class Solution(object):
    def minCost(self, m, n, penalty):
        
        dis = [[[None] * 2 for _ in range(n)] for _ in range(m)]
        heap = [(1, 0, 0, 1)]

        dx = [[-1, 0], [1, 0]]
        dy = [[0, -1], [0, 1]]

        res = 0
        while heap:
            d, x, y, r = heapq.heappop(heap)
            if dis[x][y][r] is None:
                if x == m - 1 and y == n - 1:
                    res = d
                    break
                
                dis[x][y][r] = d
                if dis[x][y][1 - r] is None:
                    heapq.heappush(heap, (d + penalty[x][y], x, y, 1 - r))

                for t in range(2):
                    if t != r:
                        p = penalty[x][y]
                    else:
                        p = 0

                    for index in range(2):
                        xx = x + dx[t][index]
                        yy = y + dy[t][index]
                        if 0 <= xx < m and 0 <= yy < n:
                            cost = (xx + 1) * (yy + 1) + p
                            if dis[xx][yy][1 - r] is None:
                                heapq.heappush(heap, (d + cost, xx, yy, 1 - r))

        return res
''',
    call=f'Solution().minCost(2, 2, {PEN})',
    expect=8,
    views=[
        dict(type='table', var=_dis(1), label='奇数图 dis[x][y][1]（已定最短）', cell=90, h=150,
             cursors=[('x', 'y', 'yellow')]),
        dict(type='table', var=_dis(0), label='偶数图 dis[x][y][0]（已定最短）', cell=90, h=150,
             cursors=[('x', 'y', 'yellow')]),
        dict(type='heap', var='heap', label='堆 heap：(d, x, y, r)', fmt=_hfmt, top_color='blue', h=150),
        dict(type='text', size=30, h=70, fn=lambda S: (
            f"弹出 `({S['x']},{S['y']})`，第 `{S['r']}` 层图，距离 `{S['d']}`" if 'r' in S and 'd' in S and 'x' in S else '')),
    ],
    watch=['d', 'x', 'y', 'r', 'p', 'cost', 'res'],
    captions={
        'dis = [[[None]': '分层图：每个格子两份，`dis[x][y][r]` 表示在第 `r` 层（r=1 奇数行动图，r=0 偶数行动图）的最短距离，`None` = 还没定',
        'heap = [(1, 0, 0, 1)]': '从奇数层的 `(0,0)` 出发，已付入口代价 `1`',
        'dx = [[-1': '`dx[0]`、`dy[0]`：左、上；`dx[1]`、`dy[1]`：右、下 —— 下标就是「行动奇偶」',
        'd, x, y, r = heapq.heappop': '弹出距离最小的点：`({x},{y})`，第 `{r}` 层，距离 `{d}`',
        'if dis[x][y][r] is None': '这个点{"还没定最短距离，处理它" if B.dis[x][y][r] is None else "已经定过了（旧状态），跳过"}',
        'if x == m - 1': '是终点吗？`({x},{y})` vs `({m-1},{n-1})` → {"是" if x == m-1 and y == n-1 else "不是"}',
        'res = d': '第一次弹出终点就是最短：`res = {res}`',
        'break': '终点最短路已确定，退出循环',
        'dis[x][y][r] = d': '确定 `dis[{x}][{y}][{r}] = {d}`',
        'if dis[x][y][1 - r] is None': '原地挂机到另一层：另一层{"还没定" if B.dis[x][y][1-r] is None else "已定"}',
        'heapq.heappush(heap, (d + penalty[x][y]': '原地挂机：付 `penalty = {penalty[x][y]}`，入堆 `({d + penalty[x][y]}, {x}, {y}, {1-r})`',
        'for t in range(2)': '枚举方向组 `t`：0 = 左/上，1 = 右/下',
        'if t != r': '`t = {t}`，`r = {r}`：{"方向组与行动奇偶不符 → 违规" if t != r else "方向组与行动奇偶相符 → 遵守规则"}',
        'p = penalty[x][y]': '违规：额外付 `p = penalty[{x}][{y}] = {p}`',
        'p = 0': '遵守规则：不加惩罚，`p = 0`',
        'if 0 <= xx < m': '邻居 `({xx},{yy})`：{"在网格内" if 0 <= xx < m and 0 <= yy < n else "越界，跳过"}',
        'cost = (xx + 1)': '移动代价 = 入口 `{(xx+1)*(yy+1)}` + 惩罚 `{p}` = `{cost}`',
        'if dis[xx][yy][1 - r] is None': '邻居在另一层{"还没定，可以入堆" if B.dis[xx][yy][1-r] is None else "已定，不用入堆"}',
        'heapq.heappush(heap, (d + cost': '入堆 `({d + cost}, {xx}, {yy}, {1-r})`',
        'return res': '最小总代价 =={res}==',
    },
    skip=['dx = [', 'dy = [', 'res = 0', 'while heap', 'for index in range(2)', 'yy = y + dy', 'xx = x + dx', 'else:'],
    max_steps=62,
    cards=dict(
        one_liner='把网格复制成奇、偶两层，在分层图上跑 Dijkstra',
        complexity='时间 `O(mn log(mn))`，空间 `O(mn)`',
        problem=['网格 `m×n`，从 `(0,0)` 到 `(m-1,n-1)`，进入 `(i,j)` 付 `(i+1)(j+1)`，起点也要付',
                 '奇数行动向右/下，偶数行动向左/上；违规加上移动前格子的 `penalty`；原地挂机付 `penalty`',
                 '示例：`m=2, n=2, penalty=[[5,3],[1,4]]` → `8`'],
        quote='非常标准的分层图最短路问题。将网格视为一个m * n个节点的图，接下来这张图复制一份，得到的两张图分别对应奇数编号的行动以及偶数编号的行动。',
        quote_src='—— yiduobo 题解原文',
        idea=['奇数层的点向偶数层连边：同一格（挂机，权 `penalty`）+ 四邻居（右/下权=入口，左/上权=入口+`penalty`）',
              '偶数层对称：左/上遵守规则，右/下违规',
              '不真的建图：堆里存 `(d, x, y, r)`，按 `t` 与 `r` 是否相等算边权'],
        summary=['时间 `O(mn log(mn))`，空间 `O(mn)`',
                 '`dis` 用 `None` 表示「还没确定」，弹出时才确定，所以弹出旧状态要跳过',
                 '终点弹出就 `break`，两层谁先弹出都行',
                 '原文可直接在 Python 3 运行，未做修改',
                 '对比灵神：灵神用 `k^1` 翻转并在入堆时更新 `dis`；yiduobo 在弹出时才写 `dis`'],
    ),
)
