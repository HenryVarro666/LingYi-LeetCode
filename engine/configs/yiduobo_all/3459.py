GR = [[0, 1, 0], [0, 0, 2], [0, 0, 0]]
DN = ['右上', '右下', '左下', '左上']


def _tab(S):
    f = S.get('f')
    if f is None:
        return None
    return [[''.join(str(x) for x in c) for c in row] for row in f]


def _tcol(S, r, c, v):
    if 'i' in S and 'j' in S and S.get('_line', 0) < 50 and (r, c) == (S['i'], S['j']):
        return 'yellow'
    return None


def _gcol(S, r, c, v):
    return 'green' if v == 1 else None


def _fcap(S, B, ret):
    i, j = S.i, S.j
    new, old = S.f[i][j], B.f[i][j]
    d = next((x for x in range(4) if new[x] != old[x]), None)
    if d is None:
        d = next((x for x in range(4) if new[x]), 0)
    nm = DN[d]
    ni, nj = i + (-1, 1, 1, -1)[d], j + (1, 1, -1, -1)[d]
    if 0 <= ni < len(S.grid) and 0 <= nj < len(S.grid[0]) and S.grid[i][j] + S.grid[ni][nj] == 2:
        return f'`({i},{j})` 的下一格 `({ni},{nj})` 与它之和为 2（2、0 交替成立）→ 沿{nm}延伸：`f[{i}][{j}][{d}] = f[{ni}][{nj}][{d}] + 1 = {new[d]}`'
    return f'沿{nm}：`f[{i}][{j}][{d}]` = `1`'


def _wh(S, B, r):
    x, y, n, m = S.x, S.y, S.n, S.m
    if not (0 <= x < n and 0 <= y < m):
        return f'`({x},{y})` 出界 → 这一段到头了，换下一个方向'
    if S.grid[x][y] != S.target:
        return f'`grid[{x}][{y}] = {S.grid[x][y]}` ≠ 目标 `{S.target}` → 这一段到头了，换下一个方向'
    return f'`grid[{x}][{y}] = {S.target}` 符合 → 这一格可以走，且可以在这里右转'


CONFIG = dict(
    num=3459, title='最长 V 形对角线段的长度', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='预处理转向后的延伸长度 · 枚举起点和转向前的路径',
    tags=['灵神题单', '网格图 DP', '难度分 2337'],
    code='''
class Solution(object):
    def lenOfVDiagonal(self, grid):
        
        dx = [-1, 1, 1, -1]
        dy = [1, 1, -1, -1]
        n = len(grid)
        m = len(grid[0])
        f = [[[0] * 4 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 1:
                    continue
                
                if i - 1 >= 0:
                    if j - 1 >= 0 and grid[i - 1][j - 1] + grid[i][j] == 2:
                        f[i][j][3] = f[i - 1][j - 1][3] + 1
                    else:
                        f[i][j][3] = 1
                
                    if j + 1 < m and grid[i - 1][j + 1] + grid[i][j] == 2:
                        f[i][j][0] = f[i - 1][j + 1][0] + 1
                    else:
                        f[i][j][0] = 1

                else:
                    f[i][j][3] = 1
                    f[i][j][0] = 1

        for i in range(n - 1, -1, -1):
            for j in range(m):
                if grid[i][j] == 1:
                    continue
                
                if i + 1 < n:
                    if j - 1 >= 0 and grid[i + 1][j - 1] + grid[i][j] == 2:
                        f[i][j][2] = f[i + 1][j - 1][2] + 1
                    else:
                        f[i][j][2] = 1

                    if j + 1 < m and grid[i + 1][j + 1] + grid[i][j] == 2:
                        f[i][j][1] = f[i + 1][j + 1][1] + 1
                    else:
                        f[i][j][1] = 1

                else:
                    f[i][j][2] = 1
                    f[i][j][1] = 1

        res = 0
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 1:
                    for d in range(4):
                        target = 2
                        x = i + dx[d]
                        y = j + dy[d]
                        length = 1
                        res = max(res, 1)
                        while 0 <= x < n and 0 <= y < m and grid[x][y] == target:
                            length += 1
                            res = max(res, length + f[x][y][(d + 1) % 4] - 1)
                            target = 2 - target
                            x += dx[d]
                            y += dy[d]
                        
        
        return res
''',
    call=f'Solution().lenOfVDiagonal({GR})',
    expect=3,
    skip=['for j in range', 'if grid[i][j] == 1', 'continue', 'if i - 1 >= 0', 'if j - 1 >= 0 and', 'if j + 1 < m and', 'if i + 1 < n',
          'else:', 'target = 2', 'length = 1', 'length += 1', 'res = max(res, 1)', 'x = i + dx', 'x += dx', 'dx = ', 'dy = ', 'n = len', 'm = len',
          18, 23, 26, 27, 38, 43, 46, 47, 50],
    views=[
        dict(type='grid', var='grid', label='grid（绿 = 1；蓝 = 当前起点，粉 = 沿方向走到的格子）', cell=60, h=200, color=_gcol,
             cursors=[('i', 'j', 'blue', ''), ('x if x is not None and 0 <= x < n and 0 <= y < m else None', 'y', 'pink', '')]),
        dict(type='table', var=_tab, label='f[i][j]：四位数字依次是方向 0/1/2/3（右上/右下/左下/左上）能延伸的格数', cell=110, h=400, color=_tcol),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j'), ('d', 'd'), ('length', 'length'), ('res', 'res', 'green')],
    captions={
        'f = [[[0]': '`f[i][j][d]`：从 `(i,j)` 沿方向 `d` 走，只经过 `0`/`2` 且相邻两格之和为 `2` 时最多能走几格；这是==转向之后==那一段；不能延伸的格子都是 `1`（只有自己）',
        9: lambda S, B, r: (f'先算方向 `0`（右上）、`3`（左上）：下一格在上一行，所以 `i` 从上往下；现在 `i = {S.i}`' if S.i != B.get('i') else '方向 0、3 算完'),
        29: lambda S, B, r: (f'再算方向 `1`（右下）、`2`（左下）：下一格在下一行，所以 `i` 从下往上；现在 `i = {S.i}`' if not (S.i == B.get('i') and S.i == 0) else '预处理全部完成'),
        'f[i][j][': _fcap,
        'res = 0': '`res = 0`：预处理做完了，接下来枚举每个值为 `1` 的起点',
        'for d in range(4)': '起点 `({i},{j})` 是 `1`，朝方向 `{d}`（{DN[d]}）走',
        'y = j + dy[d]': '第一步走到 `({x},{y})`，下一格目标值 `target = 2`',
        'while 0 <= x < n': _wh,
        'res = max(res, length + f': lambda S, B, r: (f'假设在 `({S.x},{S.y})` 右转：转向后方向 `{(S.d + 1) % 4}`（{DN[(S.d + 1) % 4]}），'
                                                       f'预处理给出 `f = {S.f[S.x][S.y][(S.d + 1) % 4]}`（含这一格）→ 总长 `{S.length} + {S.f[S.x][S.y][(S.d + 1) % 4]} - 1 = {S.length + S.f[S.x][S.y][(S.d + 1) % 4] - 1}`，更新 `res = {S.res}`'),
        'y += dy[d]': '沿方向 `{d}` 继续，下一格目标 `{target}` → 看 `({x},{y})`',
        'return res': '所有起点、所有转向位置都试过：最长 `{res}`',
    },
    cards=dict(
        one_liner='先预处理转向后的延伸长度，再暴力枚举起点和转向点',
        complexity='时间 `O(nm)`，空间 `O(nm)`',
        problem=['网格里是 `0/1/2`；线段从 `1` 开始，后面依次 `2,0,2,0...`',
                 '沿一个对角方向走，最多顺时针转 90° 一次，求最长长度',
                 '本视频：`[[0,1,0],[0,0,2],[0,0,0]]` → `3`（`(0,1)→(1,2)`，右转 `→(2,1)`）'],
        quote='注意到本题中规定了从值为1的单元格出发，而1越多0和2就越少，也就是说可以作为起点的单元格越多，可以用作路径中的单元格就越少，直观感觉上来说暴力枚举起点以及转向前的路径应该也是可行的。',
        quote_src='—— yiduobo 题解原文',
        idea=['先算转向后的那段：`f[i][j][d]` = 从 `(i,j)` 沿 `d` 走、只经过 `0/2` 的最多格数',
              '方向 0、3 的下一格在上方 → 从上往下；方向 1、2 → 从下往上',
              '再枚举每个 `1` 和转向前的方向，沿途每一格都试着右转：`length + f[x][y][(d+1)%4] - 1`'],
        summary=['时间 `O(nm)`，空间 `O(nm)`',
                 '易错：转向方向是 `(d + 1) % 4`；`f` 含转向点自身，所以总长要 `- 1`',
                 '起点自己长度为 1：不转弯的情况由 `f` 的 `+1` 之外的 `res = max(res, 1)` 兜底',
                 '原文本身可直接在 Python 3 运行，代码未改',
                 '对比灵神：灵神用记忆化搜索 `dfs(i,j,k,can_turn,target)`；yiduobo 把转向后的一段预处理成 `f`'],
    ),
)
