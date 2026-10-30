_DN = ['右', '下', '左', '上']


def _g(S, i, j, v):
    u = S.get('used')
    if u is None:
        return None
    if 'x' in S and 'nowx' in S and (i, j) == (S['nowx'], S['nowy']):
        return 'yellow'
    return 'green' if u[i][j] else None


def _chk(S, B, ret):
    x, y, d, m, n = S.x, S.y, S.d, S.m, S.n
    idx = S.index
    if d < 0:
        return f'街道 `{idx}` 在方向 `{_DN[S.nowd]}` 进入不了：`dd = {d}` < 0 → ==这条路走不通=='
    if not (0 <= x < m and 0 <= y < n):
        return f'新位置 `({x},{y})` ==出界=='
    if S.used[x][y]:
        return f'`({x},{y})` ==已走过== → 不回头'
    return f'`({x},{y})` 合法且没走过 → ==入队==，新的进入方向是 `{_DN[d]}`'


CONFIG = dict(
    num=1391, title='检查网格中是否存在有效路径', difficulty='Medium', category='网格图',
    author='yiduobo', technique='BFS 模拟 · 维护进入方向',
    tags=['灵神题单', '网格图', '难度分 1746'],
    code='''
class Solution(object):
    def hasValidPath(self, grid):

        m = len(grid)
        n = len(grid[0])
        if m == 1 and n == 1:
            return True
            
        used = [[False] * n for _ in range(m)]
        used[0][0] = True
        q = []
        if (grid[0][0] == 1 or grid[0][0] == 4 or grid[0][0] == 6) and n > 1:
            q.append([0, 1, 0])
            used[0][1] = True
        if (grid[0][0] == 2 or grid[0][0] == 3 or grid[0][0] == 4) and m > 1:
            q.append([1, 0, 1])
            used[1][0] = True
        
        l, r = 0, len(q)
        dx = [[0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 1, 0, -1],
              [1, 0, 0, 0],
              [0, 0, 1, 0],
              [-1, 0, 0, 0],
              [0, 0, -1, 0]]
        dy = [[0, 0, 0, 0],
              [1, 0, -1, 0],
              [0, 0, 0, 0],
              [0, 0, 0, -1],
              [0, 0, 0, 1],
              [0, -1, 0, 0],
              [0, 1, 0, 0]]
        dd = [[0, 0, 0, 0],
              [0, -1, 2, -1],
              [-1, 1, -1, 3],
              [1, -1, -1, 3],
              [-1, -1, 1, 0],
              [3, 2, -1, -1],
              [-1, 0, 3, -1]]

        while l < r:
            nowx, nowy, nowd = q[l]
            l += 1
            index = grid[nowx][nowy]
            x = nowx + dx[index][nowd]
            y = nowy + dy[index][nowd]
            d = dd[index][nowd]
            if d >= 0 and x >= 0 and x < m and y >= 0 and y < n and not used[x][y]:
                q.append([x, y, d])
                used[x][y] = True
                r += 1
                if x == m - 1 and y == n - 1 and dd[grid[x][y]][d] >= 0:
                    return True
        
        return False
''',
    call='Solution().hasValidPath([[2,4,3],[6,5,2]])',
    expect=True,
    skip=['m = len', 'n = len', 'dx = [[', 'dy = [[', 'dd = [[', 'used = [[', 'q = []', 'l += 1', 'r += 1'] + list(range(21, 27)) + list(range(28, 34)) + list(range(35, 41)),
    views=[
        dict(type='grid', var='grid', label='grid（街道编号；绿 = 已入队，黄 = 当前出队的格子）', cell=92, h=300,
             color=_g, cursors=[('nowx', 'nowy', 'blue', '')]),
        dict(type='array', var=lambda S: [f'{a},{b},{_DN[c]}' for a, b, c in S['q']] if 'q' in S else None,
             label='q（x,y,进入方向；暗 = 已出队，l 指向队首）', cell=110, pointers={'l': 'blue'},
             dim=lambda S, i, v: i < S.get('l', 0), h=190),
        dict(type='text', h=70, fn=lambda S: (f"街道 `{S['index']}`，进入方向 `{_DN[S['nowd']]}` → 新状态 `({S['x']},{S['y']})` 方向 `{_DN[S['d']] if S['d'] >= 0 else '无'}`" if 'd' in S and 'nowd' in S and S['_line'] >= 48 else '')),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r'), ('nowd', "_DN[nowd] if 'nowd' in _inner else None", 'pink'), ('index', "index if 'index' in _inner else None", 'yellow')],
    captions={
        'if m == 1 and n == 1': '`m = {m}`，`n = {n}`：不是单个格子，需要真正走',
        'used[0][0] = True': '起点标记走过',
        'if (grid[0][0] == 1': lambda S, B, r: (f'起点街道 `{S.grid[0][0]}` 属于 1、4、6 → ==能往右走==，进入 `(0,1)`，方向记为 右' if S.grid[0][0] in (1, 4, 6) and S.n > 1
                                                else f'起点街道 `{S.grid[0][0]}` 不属于 1、4、6 → 右边走不了'),
        'if (grid[0][0] == 2': lambda S, B, r: (f'起点街道 `{S.grid[0][0]}` 属于 2、3、4 → ==能往下走==，进入 `(1,0)`，方向记为 下' if S.grid[0][0] in (2, 3, 4) and S.m > 1
                                                else f'起点街道 `{S.grid[0][0]}` 不属于 2、3、4 → 下边走不了'),
        'l, r = 0, len(q)': '`l` 是队首、`r` 是队尾：队里是起点出发的第一步（0 到 2 个状态）',
        'while l < r': lambda S, B, r: (f'`l = {B.l} < r = {B.r}`：还有状态没处理' if B.l < B.r
                                        else f'`l = r = {B.r}`：队空了，没有走到终点'),
        'nowx, nowy, nowd = q[l]': '出队：当前在 `({nowx},{nowy})`，是从 ==`{_DN[nowd]}`== 方向走进来的',
        'index = grid[nowx][nowy]': '这格是街道 `{index}`：要查 `dx/dy/dd[{index}][{nowd}]`',
        'x = nowx': '`x = nowx + dx[{index}][{nowd}] = {x}`：下一格的行',
        'y = nowy': '`y = nowy + dy[{index}][{nowd}] = {y}`：下一格的列',
        'd = dd[index][nowd]': '`dd[{index}][{nowd}] = {d}`：新的进入方向，==-1 表示这种街道从这个方向进不来==',
        'if d >= 0 and x >= 0': _chk,
        'q.append': '新状态 `[{x},{y},{d}]` 入队',
        'used[x][y] = True': '`({x},{y})` 标记走过，之后不再进入',
        'if x == m - 1 and y == n - 1': lambda S, B, r: (
            f'到达右下角 `({S.x},{S.y})`，再看这格街道 `{S.grid[S.x][S.y]}` 能否从方向 `{_DN[S.d]}` 进入：`dd = {S.dd[S.grid[S.x][S.y]][S.d]}`'
            if (S.x, S.y) == (S.m - 1, S.n - 1) else f'`({S.x},{S.y})` 不是终点 → 继续 BFS'),
        'return True': '终点街道也接得上 → ==存在有效路径==',
        'return False': '队列空了还没到终点 → 返回 False',
    },
    cards=dict(
        one_liner='模拟走路：除了位置，还要记住是从哪个方向进来的',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['网格每格是一条街道（1~6），连接两个方向',
                 '从 `(0,0)` 出发只能沿街道走，能否到达 `(m-1,n-1)`',
                 '示例：`[[2,4,3],[6,5,2]]` → `true`'],
        quote='需要注意的是，在模拟过程中除了常规的维护当前位置(x, y)之外，还需要额外维护方向，表示上一步是从哪个方向走到当前格子的。',
        quote_src='—— yiduobo 题解原文',
        idea=['状态是 `(x, y, d)`：位置 + 进入方向',
              '三张表 `dx/dy/dd[街道][进入方向]`：给出新位置和新方向，-1 表示进不来',
              '用 `used` 防止走回头，BFS 数组 + 双下标做队列'],
        summary=['时间 `O(mn)`，每格最多入队一次',
                 '易错：起点要先按街道种类手动走第一步；终点也要检查能否从 `d` 方向进入',
                 '原文是 Python 2 风格写法，但无需改动，代码未改',
                 '对比灵神：灵神 DFS 里用「邻居含反方向」判断连通，yiduobo 用查表 + 进入方向'],
    ),
)
