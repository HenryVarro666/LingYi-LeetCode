def _col(S, i, j, v):
    c = S.get('color')
    if c is None:
        return None
    if c[i][j] == 0:
        return None
    if S.get('now_color') is not None and c[i][j] == S['now_color']:
        return 'green'
    return 'cyan'


def _chk(S, B, ret):
    x, y, nowx, nowy = S.x, S.y, S.nowx, S.nowy
    m, n = S.m, S.n
    if not (0 <= x < m and 0 <= y < n):
        return f'邻居 `({x},{y})` ==出界=='
    if x == S.lastx and y == S.lasty:
        return f'邻居 `({x},{y})` 就是 `({nowx},{nowy})` 的来路 → 不能回头'
    if S.grid[x][y] != S.v:
        return f'邻居 `({x},{y})` 是 `{S.grid[x][y]}`，不等于 `{S.v}` → 不算'
    if S.color[x][y] == 0:
        return f'邻居 `({x},{y})` 同值、没处理过 → ==扩展入队=='
    if S.l >= 4:
        return f'邻居 `({x},{y})` 同值、已处理过、不是来路，且 `l = {S.l} >= 4` → ==成环=='
    return f'邻居 `({x},{y})` 同值、已处理过，但 `l = {S.l} < 4` → 还不算环'


CONFIG = dict(
    num=1559, title='二维网格图中探测环', difficulty='Medium', category='网格图',
    author='yiduobo', technique='BFS 染色 · 遇到已处理的非来路格子',
    tags=['灵神题单', '网格图', '难度分 1838'],
    code='''
class Solution(object):
    def containsCycle(self, grid):

        m = len(grid)
        n = len(grid[0])
        color = [[0] * n for _ in range(m)]

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        now_color = 0
        for i in range(m):
            for j in range(n):
                if color[i][j] == 0:
                    v = grid[i][j]
                    now_color += 1
                    color[i][j] = 1
                    q = [[i, j, None, None]]
                    l, r = 0, 1
                    while l < r:
                        nowx, nowy, lastx, lasty = q[l]
                        l += 1
                        for index in range(4):
                            x = nowx + dx[index]
                            y = nowy + dy[index]
                            if x >= 0 and x < m and y >= 0 and y < n and (x != lastx or y != lasty) and grid[x][y] == v:
                                if color[x][y] == 0:
                                    q.append([x, y, nowx, nowy])
                                    r += 1
                                    color[x][y] = now_color
                                elif l >= 4:
                                    return True
        
        return False
''',
    call="Solution().containsCycle([['b','a','a','c'],['b','a','a','c']])",
    expect=True,
    skip=['m = len', 'n = len', 'color = [[', 'dx = [', 'dy = [', 'l += 1', 'r += 1', 'q.append', 'for index in range', 23, 24],
    views=[
        dict(type='grid', var='grid', label='grid（绿 = 当前这一轮 BFS 处理过；青 = 之前轮次；蓝框 = 出队格）', cell=96, h=250,
             color=_col, cursors=[('nowx', 'nowy', 'blue', '')]),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b, _c, _d in S['q']] if 'q' in S else None,
             label='q（本轮 BFS 队列；暗 = 已出队）', cell=80, pointers={'l': 'blue'},
             dim=lambda S, i, v: i < S.get('l', 0), h=190),
        dict(type='text', h=60, fn=lambda S: (f"出队 `({S['nowx']},{S['nowy']})`，来路 `({S['lastx']},{S['lasty']})`" if 'lastx' in S else '')),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r'), ('v', 'v', 'green'), ('now_color', 'now_color', 'cyan')],
    captions={
        'for i in range(m)': '外层逐格扫描：行 `i = {i}`',
        'for j in range(n)': '列 `j = {j}`',
        'if color[i][j] == 0': lambda S, B, r: (f'`({S.i},{S.j})` 还没染色 → 开一轮新的 BFS' if S.color[S.i][S.j] == 0
                                                else f'`({S.i},{S.j})` 已被之前的 BFS 处理过 → 跳过'),
        'v = grid[i][j]': '这一轮只走值为 `{v}` 的格子',
        'now_color += 1': '`now_color = {now_color}`：每一轮 BFS 一个编号',
        'color[i][j] = 1': '起点染色（标记已处理）',
        'q = [[i, j, None, None]]': '起点入队，来路 `None, None`：起点没有来路',
        'l, r = 0, 1': '`l` 队首、`r` 队尾',
        'while l < r': lambda S, B, r: (f'`l = {B.l} < r = {B.r}`：队列不空，继续' if B.l < B.r
                                        else f'`l = r = {B.r}`：这个连通块没发现环，换下一个起点'),
        'nowx, nowy, lastx, lasty = q[l]': '出队 `({nowx},{nowy})`，它是从 `({lastx},{lasty})` 扩展来的',
        'x = nowx': '看邻居 `x = {x}`',
        'y = nowy': '看邻居 `y = {y}`',
        'if x >= 0 and x < m': _chk,
        'if color[x][y] == 0': lambda S, B, r: ('没处理过 → 入队，来路记为当前格' if S.color[S.x][S.y] == 0 else '已处理过，且不是来路 → 看队列走了多远'),
        'color[x][y] = now_color': '`({x},{y})` 入队并染成 `{now_color}`，来路是 `({nowx},{nowy})`',
        'elif l >= 4': lambda S, B, r: (f'`l = {S.l} >= 4` → 找到长度 `>= 4` 的环' if S.l >= 4 else f'`l = {S.l} < 4` → 不够'),
        'return True': '==找到环==，返回 True',
        'return False': '所有连通块都没环 → False',
    },
    cards=dict(
        one_liner='BFS 扩展时，撞上已处理且不是来路的同值格子，就是环',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['字符网格里，同值格子沿四邻移动，找长度 `>= 4` 的环',
                 '不能回到上一步所在的格子',
                 '示例：`[[b,a,a,c],[b,a,a,c]]` → `true`（中间 2×2 的 a）'],
        quote='只要bfs队列的长度大于等于4，且当前处理的格子的相邻格子中有已经处理过的格子，并且满足当前格子不是由这个处理过的格子扩展得到的，那么就说明找到了一个环。',
        quote_src='—— yiduobo 题解原文',
        idea=['按格子扫描，没处理过就开一轮 BFS',
              '队列项记录 `[x, y, 来路x, 来路y]`',
              '同值邻居若已染色且不是来路，再用 `l >= 4` 过滤，成环'],
        summary=['时间 `O(mn)`，每格最多入队一次',
                 '易错：必须排除来路格子，否则相邻两格会互相算成环',
                 '`l >= 4`：至少出队过 4 个格子才可能成环',
                 '原文是 Python 2 风格写法，但无需改动，代码未改',
                 '对比灵神：灵神用 DFS 传 `(px, py)`，yiduobo 用 BFS 队列里带来路'],
    ),
)
