GRID = [[1, 1, 1], [0, 1, 0]]
R, C = len(GRID), len(GRID[0])


def _cut_cells():
    """brute-force: land cells whose removal disconnects the remaining land (for highlighting only)"""
    land = [(i, j) for i in range(R) for j in range(C) if GRID[i][j]]
    out = set()
    for rm in land:
        rest = [c for c in land if c != rm]
        if not rest:
            continue
        seen, st = {rest[0]}, [rest[0]]
        while st:
            a, b = st.pop()
            for da, db in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                c = (a + da, b + db)
                if c in rest and c not in seen:
                    seen.add(c)
                    st.append(c)
        if len(seen) < len(rest):
            out.add(rm)
    return out


CUT = _cut_cells()


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    inner = S.get('_inner', {})
    dfn, low = S.get('dfn'), S.get('low')
    tarjan = dfn is not None and 'nowx' in inner and 'lastx' in inner
    used = S.get('used')
    flag = (bool(getattr(S.get('self'), 'flag', False)) or S.get('_line') == 60) if 'dfn' in S else False
    title = ('Tarjan：格内是 dfn / low（红 = 割点，删掉就断开）' if dfn is not None
             else 'BFS 数连通块（绿 = 已染色，蓝框 = 出队，粉框 = 邻居）')
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    cell = min(170, (x1 - x0 - 60) / C, (y1 - y0 - 150) / R)
    sx = x0 + ((x1 - x0) - cell * C) / 2
    sy = y0 + 60
    nx, ny = inner.get('nowx'), inner.get('nowy')
    px, py = inner.get('x'), inner.get('y')
    for i in range(R):
        for j in range(C):
            X, Y = sx + j * cell, sy + i * cell
            land = GRID[i][j] == 1
            fill = T['panel2']
            if land and used is not None and used[i][j] and dfn is None:
                fill = T['green']
            if land and dfn is not None and dfn[i][j] is not None:
                fill = T['blue']
            if flag and (i, j) in CUT:
                fill = T['red']
            cv.rect((X + 5, Y + 5, X + cell - 5, Y + cell - 5), fill=fill, alpha=(255 if fill != T['panel2'] and not land else 90 if fill != T['panel2'] else 255),
                    outline=T['border'], width=2, r=14)
            if not land:
                cv.text((X + cell / 2, Y + cell / 2), '0', 34, T['dim'], anchor='mm', mono=True)
                continue
            if dfn is not None and dfn[i][j] is not None:
                cv.text((X + cell / 2, Y + cell / 2 - 12), f'dfn={dfn[i][j]}', 28, T['text'], anchor='mm', bold=True)
                cv.text((X + cell / 2, Y + cell / 2 + 22), f'low={low[i][j]}', 28, T['cyan'], anchor='mm', bold=True)
            else:
                cv.text((X + cell / 2, Y + cell / 2), '1', 40, T['text'], anchor='mm', bold=True, mono=True)
            cv.text((X + 12, Y + 10), f'({i},{j})', 16, T['dim'], mono=True)
    if nx is not None and ny is not None:
        cv.rect((sx + ny * cell + 2, sy + nx * cell + 2, sx + (ny + 1) * cell - 2, sy + (nx + 1) * cell - 2),
                outline=T['blue'], width=6, r=16)
    if px is not None and py is not None and 0 <= px < R and 0 <= py < C and S.get('_line') in (25, 26, 27, 28, 52, 53, 54, 55, 58, 59, 60, 62, 63):
        cv.rect((sx + py * cell + 10, sy + px * cell + 10, sx + (py + 1) * cell - 10, sy + (px + 1) * cell - 10),
                outline=T['pink'], width=5, r=12)
    if dfn is None and 'q' in S:
        qs = ' '.join(f'({a},{b})' for a, b in S['q'])
        l_ = S.get('l', 0)
        cv.text((sx + C * cell / 2, sy + R * cell + 8), f'队列 q = {qs}', 22, T['muted'], anchor='mt')
        cv.text((sx + C * cell / 2, sy + R * cell + 38), f'l = {l_}（下一个出队），r = {S.get("r", 0)}', 22, T['green'], anchor='mt', bold=True)
    if dfn is not None and 'nowx' in inner and inner.get('lastx') is not None:
        a, b = inner['lastx'], inner['lasty']
        cv.text((sx + C * cell / 2, sy + R * cell + 8), f'当前 ({nx},{ny})，来自 ({a},{b})', 22, T['muted'], anchor='mt')


def _bq(S):
    if 'q' not in S:
        return None
    return [f'{a},{b}' for a, b in S['q']]


_NB = lambda S, B, r: (
    f'邻居 `({S.x},{S.y})` 越界' if not (0 <= S.x < S.m and 0 <= S.y < S.n)
    else f'邻居 `({S.x},{S.y})` 是水' if S.grid[S.x][S.y] == 0
    else f'邻居 `({S.x},{S.y})` 是陆地但已经染过' if S.used[S.x][S.y]
    else f'邻居 `({S.x},{S.y})` 是没染过的陆地 → ==染色并入队==')

_NB2 = lambda S, B, r: (
    f'邻居 `({S.x},{S.y})` 越界或是水 → 跳过' if not (0 <= S.x < S.m and 0 <= S.y < S.n and S.grid[S.x][S.y] == 1)
    else f'邻居 `({S.x},{S.y})` 是陆地 → 看它有没有访问过')

_VIS = lambda S, B, r: (
    f'`dfn[{S.x}][{S.y}]` 还是 None → ==树边==，往下 dfs' if S.dfn[S.x][S.y] is None
    else f'`({S.x},{S.y})` 已访问过（`dfn = {S.dfn[S.x][S.y]}`）→ 看是不是回边')

_BACK = lambda S, B, r: (
    f'`({S.x},{S.y})` 就是来路 → 跳过' if (S.x == S.lastx and S.y == S.lasty)
    else f'`({S.x},{S.y})` 不是来路 → ==回边==：用它的 dfn 更新 low')

CONFIG = dict(
    num=1568, title='使陆地分离的最少天数', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='BFS 数连通块 + Tarjan 求割点',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def minDays(self, grid):

        m = len(grid)
        n = len(grid[0])
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        q = []
        l = r = 0
        used = [[False] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1 and not used[i][j]:
                    if r > 0:
                        return 0
                    q.append([i, j])
                    used[i][j] = True
                    r = 1
                    while l < r:
                        nowx, nowy = q[l]
                        l += 1
                        for index in range(4):
                            x = nowx + dx[index]
                            y = nowy + dy[index]
                            if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 1 and not used[x][y]:
                                q.append([x, y])
                                used[x][y] = True
                                r += 1

        if r == 1:
            return 1

        self.flag = False
        self.cnt = 0
        dfn = [[None] * n for _ in range(m)]
        low = [[None] * n for _ in range(m)]
        self.dfs(q[0][0], q[0][1], dfn, low, None, None, m, n, dx, dy, grid)
        if self.flag:
            return 1
        else:
            return 2

    def dfs(self, nowx, nowy, dfn, low, lastx, lasty, m, n, dx, dy, grid):
        self.cnt += 1
        dfn[nowx][nowy] = self.cnt
        low[nowx][nowy] = self.cnt

        child_cnt = 0
        for index in range(4):
            x = nowx + dx[index]
            y = nowy + dy[index]
            if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 1:
                if dfn[x][y] is None:
                    child_cnt += 1
                    self.dfs(x, y, dfn, low, nowx, nowy, m, n, dx, dy, grid)
                    if self.flag:
                        return
                    low[nowx][nowy] = min(low[nowx][nowy], low[x][y])
                    if lastx is not None and low[x][y] >= dfn[nowx][nowy]:
                        self.flag = True
                        return
                elif x != lastx or y != lasty:
                    low[nowx][nowy] = min(low[nowx][nowy], dfn[x][y])
        
        if lastx is None and child_cnt > 1:
            self.flag = True
''',
    call='Solution().minDays(%s)' % GRID,
    expect=1,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='calls', h=170, hide=('dfn', 'low', 'grid', 'dx', 'dy', 'm', 'n')),
    ],
    watch=[('r', 'r', 'green'), ('cnt', lambda S: getattr(S.get('self'), 'cnt', None), 'blue'),
           ('flag', lambda S: getattr(S.get('self'), 'flag', None), 'red')],
    skip=['m = len(grid)', 'n = len(grid[0])', 'dx = [', 'dy = [', 'q = []', 'l = r = 0', 'for i in range(m)', 'for j in range(n)',
          'q.append', 'l += 1', 'for index in range(4)', 'x = nowx', 'y = nowy', 'r += 1', 'self.flag = False', 'self.cnt = 0',
          'low = [[None]', 'low[nowx][nowy] = self.cnt', 'child_cnt = 0', 15, 57, 61, 'else:'],
    captions={
        'used = [[False]': '`used[i][j]` 标记陆地格子有没有被染过色',
        13: lambda S, B, r: (
            f'`({S.i},{S.j})` 是水，跳过' if S.grid[S.i][S.j] == 0
            else f'`({S.i},{S.j})` 是陆地，但已经染过色，跳过' if S.used[S.i][S.j]
            else f'`({S.i},{S.j})` 是==没染过的陆地==：一块新的连通分量'),
        14: lambda S, B, r: ('`r > 0`：前面已经染完一块，这里又发现一块 → ==两个连通分量，答案 0=='
                             if S.r > 0 else '`r = 0`：这是第一块陆地，从它开始 BFS'),
        'used[i][j] = True': '起点染色并入队',
        'r = 1': '`r = 1`：队里有 1 个格子，`r` 同时记录这块陆地的大小',
        'while l < r': lambda S, B, r: (f'`l = {B.l} < r = {B.r}`：队里还有格子，继续 BFS' if B.l < B.r
                                        else f'`l == r = {B.r}`：队空，这块陆地染完，一共 `{B.r}` 格'),
        'nowx, nowy = q[l]': '出队 `({nowx},{nowy})`，依次看右、下、左、上四个邻居',
        25: _NB,
        'used[x][y] = True': '`({x},{y})` 染色并入队，之后不会重复进队',
        'if r == 1': lambda S, B, r: (f'`r = {S.r}`：只有 1 格陆地，删掉它就没有陆地了 → 答案 1' if S.r == 1
                                      else f'`r = {S.r}`：恰好一块、不止 1 格 → 答案只可能是 1 或 2，要判断有没有==割点=='),
        'dfn = [[None]': '`dfn` 记录 dfs 的访问序号，`low` 记录能回到的最早序号，`None` = 未访问',
        'self.dfs(q[0][0]': '把陆地看成图（上下左右相邻 = 有边），从第一个陆地格 `({q[0][0]},{q[0][1]})` 开始 Tarjan 找割点',
        'self.cnt += 1': '进入新格子：全局计数 `cnt` 加一 → `{self.cnt}`',
        'dfn[nowx][nowy] = self.cnt': '`dfn[{nowx}][{nowy}] = low[{nowx}][{nowy}] = {self.cnt}`：先让 low 等于自己',
        52: _NB2,
        53: _VIS,
        'child_cnt += 1': '又多一个 dfs 树上的孩子：`child_cnt = {child_cnt}`',
        'self.dfs(x, y': lambda S, B, r: f'递归进入 `({B.x},{B.y})`，来路是 `({B.nowx},{B.nowy})`',
        56: lambda S, B, r: ('子树里已经找到割点 → 直接一路返回' if S.self.flag else '孩子子树里没有发现割点 → 继续'),
        'low[nowx][nowy] = min(low[nowx][nowy], low[x][y])': '孩子 `({x},{y})` 能回到 `low = {low[x][y]}` → `low[{nowx}][{nowy}]` 更新为 =={low[nowx][nowy]}==',
        'if lastx is not None and low': lambda S, B, r: (
            f'`low[{S.x}][{S.y}] = {S.low[S.x][S.y]} >= dfn[{S.nowx}][{S.nowy}] = {S.dfn[S.nowx][S.nowy]}`：孩子这一侧回不到更早的格子 → ==删掉 ({S.nowx},{S.nowy}) 陆地就断开了，是割点=='
            if S.lastx is not None and S.low[S.x][S.y] >= S.dfn[S.nowx][S.nowy]
            else '不满足割点条件（根节点要看孩子数）'),
        'self.flag = True': lambda S, B, r: '标记：存在割点 → ==答案是 1==',
        'elif x != lastx': _BACK,
        'low[nowx][nowy] = min(low[nowx][nowy], dfn[x][y])': '回边：`low[{nowx}][{nowy}]` 更新为 =={low[nowx][nowy]}==',
        'if lastx is None and child_cnt': lambda S, B, r: (
            '不是根节点，不用看孩子数' if S.lastx is not None else
            f'根节点有 `{S.child_cnt}` 个孩子 > 1 → 删掉根就分成几块，是割点' if S.child_cnt > 1
            else f'根节点只有 `{S.child_cnt}` 个孩子，不是割点'),
        38: lambda S, B, r: ('`self.flag` 为真：存在割点 → 删 1 个格子即可，答案 `1`' if S.self.flag
                              else '没有割点 → 删 1 个格子不够，答案 `2`（角上的格子最多 2 个邻居）'),
    },
    max_steps=100,
    cards=dict(
        one_liner='先数连通块；一块时看有没有割点：有答案 1，没有答案 2',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`grid` 里 1 是陆地、0 是水，上下左右相连的陆地算一座岛',
                 '每天可以把一格陆地变成水，求最少几天让陆地==不连通（不是恰好一座岛）==',
                 '本视频：`[[1,1,1],[0,1,0]]` → `1`（删掉 `(0,1)` 就断开）'],
        quote='若将地图上的1视为一张无向连通图，那么如果将图中的某个割点删去，无向连通图就会变得不连通，此时的答案同样为1。',
        quote_src='—— yiduobo 题解原文',
        idea=['陆地数不是一块（0 块或 ≥ 2 块）→ 本来就不连通，答案 `0`',
              '只有 1 格陆地 → 答案 `1`；否则角上的格子最多 2 个邻居，==答案上界是 2==',
              '把陆地看成无向图：有割点答案 `1`，没有答案 `2`；割点用 Tarjan 的 `dfn / low` 判断，根节点要看孩子数 > 1'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '分四种情况：连通块 ≠ 1 → 0；只有 1 格 → 1；有割点 → 1；否则 2',
                 '非根节点：孩子 `low >= dfn[当前]` 就是割点；根节点：孩子数 `> 1`',
                 '`elif x != lastx or y != lasty`：来路不算回边',
                 '原文是 Python 2 风格，代码无需修改，直接运行',
                 '同类题：1192 查找集群内的关键连接（割边）'],
    ),
)
