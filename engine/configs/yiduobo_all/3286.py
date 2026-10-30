G = [[0, 1, 0], [1, 1, 0]]


def _seen(S, i, j, v):
    f = S.get('f')
    if not f:
        return None
    if i == 0 and j == 0 and False:
        return None
    if any(f[i][j]):
        return 'green' if v == 0 else 'orange'
    return 'red' if v == 1 else None


def _nb(S, B, r):
    x, y, nh = S.x, S.y, S.nowh
    m, n = S.m, S.n
    if not (0 <= x < m and 0 <= y < n):
        return f'`({x},{y})` 越界，跳过'
    h = nh - S.grid[x][y]
    if h <= 0:
        return f'走进 `({x},{y})`：血量 `{nh} − {S.grid[x][y]} = {h}` ≤ 0 → ==血量耗尽==，不能走'
    if S.f[x][y][h]:
        return f'状态 `({x},{y},{h})` 已经访问过 → 不重复入队'
    return f'血量 `{nh} − {S.grid[x][y]} = {h}` > 0，且状态 `({x},{y},{h})` 没访问过 → ==入队=='


CONFIG = dict(
    num=3286, title='穿越网格图的安全路径', difficulty='Medium', category='网格图',
    author='yiduobo', technique='分层图 BFS（位置 + 血量）',
    tags=['灵神题单', '网格图'],
    code='''
class Solution(object):
    def findSafeWalk(self, grid, health):

        if health - grid[0][0] == 0:
            return False

        m = len(grid)
        n = len(grid[0])

        f = [[[False] * (m + n + 1) for _ in range(n)] for _ in range(m)]
        f[0][0][health - grid[0][0]] = True
        q = [[0, 0, health - grid[0][0]]]
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        head, tail = 0, 1
        while head < tail:
            for nowx, nowy, nowh in q[head : tail]:
                for d in range(4):
                    x = nowx + dx[d]
                    y = nowy + dy[d]
                    if 0 <= x < m and 0 <= y < n:
                        h = nowh - grid[x][y]
                        if h > 0 and not f[x][y][h]:
                            q.append([x, y, h])
                            f[x][y][h] = True
                            if x == m - 1 and y == n - 1:
                                return True

            head, tail = tail, len(q)
        
        return False
''',
    call=f'Solution().findSafeWalk({G}, 3)',
    expect=True,
    skip=['m = len', 'n = len', 'dx = [', 'dy = [', 'x = nowx', 'y = nowy', 'head, tail = 0', 'f = [[', 'for d in range(4)'],
    views=[
        dict(type='grid', var='grid', label='grid（绿/橙 = 已访问；红 = 不安全格；蓝框 = 当前状态，粉框 = 邻居）', cell=100, h=300,
             color=_seen, cursors=[('nowx', 'nowy', 'blue'), ('x if _line in (21, 22, 23, 24, 25, 26) else None', 'y', 'pink')]),
        dict(type='array', var=lambda S: [f'{a},{b},{c}' for a, b, c in S['q']] if 'q' in S else None,
             label='q（状态：行,列,剩余血量；暗 = 已处理）', cell=110, h=170,
             dim=lambda S, i, v: i < S.get('head', 0)),
    ],
    watch=[('head', 'head', 'blue'), ('tail', 'tail'), ('nowh', 'nowh', 'green'), ('h', 'h', 'pink')],
    captions={
        'if health - grid[0][0] == 0': lambda S, B, r: (f'起点若是不安全格且 `health = 1`，一进门血量就是 0 → ==直接 False==' if B.health - B.grid[0][0] == 0
                                                       else f'起点血量 `{B.health} − {B.grid[0][0]} = {B.health - B.grid[0][0]}` > 0，可以出发'),
        'f[0][0][health': '`f[x][y][h]`：到过 `(x,y)` 且剩余血量为 `h` 吗？起点 `f[0][0][{health - grid[0][0]}] = True`',
        'q = [[0, 0': '初始状态 `(0, 0, 血 {health - grid[0][0]})` 入队：==状态 = 位置 + 血量==',
        'while head < tail': lambda S, B, r: (f'`head = {B.head} < tail = {B.tail}`：这一层还有状态，开始一层 BFS' if B.head < B.tail
                                              else '这一层为空，终点到不了'),
        'for nowx, nowy, nowh in': '遍历 `q[head:tail]`（一层）里的每个状态：位置 `({nowx},{nowy})`，剩余血量 `{nowh}`',
        'for d in range(4)': '依次尝试右、下、左、上四个邻居',
        'if 0 <= x < m': lambda S, B, r: (f'`({B.x},{B.y})` 在界内' if 0 <= B.x < B.m and 0 <= B.y < B.n else f'`({B.x},{B.y})` 越界，跳过'),
        'h = nowh - grid[x][y]': '走进 `({x},{y})`：血量 `{nowh} − {grid[x][y]} = {h}`（不安全格才扣血）',
        'if h > 0': _nb,
        'q.append': '新状态 `({x},{y},{h})` 入队',
        'f[x][y][h] = True': '标记 `f[{x}][{y}][{h}] = True`：==同位置同血量只处理一次==',
        'if x == m - 1': lambda S, B, r: ('到达右下角且血量 > 0 → 返回 True' if S.x == S.m - 1 and S.y == S.n - 1 else '还没到右下角'),
        'head, tail = tail': '一层处理完：`head = {head}`，`tail = {tail}`，下一层就是新加入的状态',
        'return True': '到了终点，血量为正 → `True`',
        'return False': 'BFS 耗尽也没到终点 → `False`',
    },
    max_steps=120,
    cards=dict(
        one_liner='普通 BFS 再加一维血量：状态是（位置，剩余血量）',
        complexity='时间 `O(mn(m+n))`，空间 `O(mn(m+n))`',
        problem=['`grid[i][j] = 1` 是不安全格，走进去扣 1 点血，血量必须始终为正',
                 '从左上角走到右下角，问能否到达',
                 '示例：`[[0,1,0,0,0],[0,1,0,1,0],[0,0,0,1,0]]`，`health = 1` → `true`',
                 '本视频：`[[0,1,0],[1,1,0]]`，`health = 3` → `true`'],
        quote='经典的分层图bfs的问题，在常规bfs的基础上需要新增当前血量这一状态。初始情况下玩家位于(0, 0)，血量为health - grid[0][0]。',
        quote_src='—— yiduobo 题解原文',
        idea=['同一个格子，血量不同就是不同状态：用 `f[x][y][h]` 去重',
              '走进邻居后血量变成 `h = nowh - grid[x][y]`，==h > 0 才合法==',
              '第一次走到右下角就能返回 True；BFS 空了就是 False'],
        summary=['血量最大 `health ≤ m+n`，所以第三维开 `m+n+1`',
                 '起点是不安全格时先扣血：`health - grid[0][0] == 0` 直接 False',
                 '状态数 `m·n·(m+n)`，比灵神的 0-1 BFS 最短路多一个维度',
                 '原文是 Python 2 风格，但在 Python 3 下无需修改，代码原样运行'],
    ),
)
