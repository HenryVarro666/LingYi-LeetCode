G = [[0, 0, 1, 0], [0, 0, 0, 0], [0, 1, 0, 0]]
M, N = len(G), len(G[0])
ASSIGN = (12, 15, 17, 19, 21)


def _prog(S):
    """(已算完的格子数, 当前格子)"""
    line = S.get('_line')
    if line == 22:
        return M * N, None
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return 0, None
    if line in ASSIGN:
        return i * N + j + 1, (i, j)
    return i * N + j, (i, j)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g = S.get('obstacleGrid')
    if g is None:
        return
    cv.text((x0 + 18, y0 + 4), 'obstacleGrid 原地变成 f（红框 = 原障碍；灰字 = 还没覆盖的原始值）', 22, T['muted'], bold=True)
    done, cur = _prog(S)
    line = S.get('_line')
    cell = min(128, (y1 - y0 - 150) / M)
    gw = cell * N
    sx = x0 + (x1 - x0 - gw) / 2 + 20
    sy = y0 + 66
    for j in range(N):
        cv.text((sx + j * cell + cell / 2, sy - 6), f'j={j}', 18, T['dim'], anchor='mb', mono=True)
    src = {}
    if cur and line in ASSIGN:
        ci, cj = cur
        if line in (17, 21):
            src[(ci, cj - 1)] = 'pink'
        if line in (19, 21):
            src[(ci - 1, cj)] = 'blue'
    for i in range(M):
        cv.text((sx - 12, sy + i * cell + cell / 2), f'i={i}', 18, T['dim'], anchor='rm', mono=True)
        for j in range(N):
            k = i * N + j
            X, Y = sx + j * cell, sy + i * cell
            ob = G[i][j] == 1
            fill = T['panel2']
            if (i, j) in src:
                fill = T[src[(i, j)]]
            elif cur and (i, j) == cur and line in ASSIGN:
                fill = T['red'] if ob else T['green']
            cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), fill=fill, r=10,
                    outline=T['red'] if ob else T['border'], width=4 if ob else 1)
            hot = fill != T['panel2']
            if k < done:
                cv.text((X + cell / 2, Y + cell / 2), g[i][j], 40, T['bg'] if hot else T['text'], anchor='mm', bold=True)
            else:
                cv.text((X + cell / 2, Y + cell / 2), g[i][j], 30, T['red'] if ob else T['dim'], anchor='mm')
    if cur:
        ci, cj = cur
        X, Y = sx + cj * cell, sy + ci * cell
        cv.rect((X - 1, Y - 1, X + cell + 1, Y + cell + 1), outline=T['yellow'], width=5, r=12)
    # 五种情况图例
    lx, ly = x0 + 30, sy + M * cell + 26
    cases = [('障碍', '→ 0', 12), ('起点', '→ 1', 15), ('第一行', '← 左', 17), ('第一列', '↑ 上', 19), ('其他', '上 + 左', 21)]
    w = (x1 - x0 - 60) / len(cases)
    for k, (a, b, ln) in enumerate(cases):
        X = lx + k * w
        on = line == ln
        cv.rect((X + 4, ly, X + w - 4, ly + 64), fill=T['yellow'] if on else T['panel2'], r=10)
        cv.text((X + w / 2, ly + 18), a, 22, T['bg'] if on else T['muted'], anchor='mm', bold=True)
        cv.text((X + w / 2, ly + 46), b, 20, T['bg'] if on else T['dim'], anchor='mm', bold=True)


def _cap_ob(S, B, ret):
    i, j = S.i, S.j
    head = f'新的一行 `i = {i}`：' if j == 0 and i > 0 else ''
    if G[i][j] == 1:
        return head + f'`({i},{j})` 是障碍物 → 情况 1'
    return head + f'`({i},{j})` 不是障碍物，继续看它在哪一行、哪一列'


CONFIG = dict(
    num=63, title='不同路径 II', difficulty='Medium', category='多维动态规划',
    author='yiduobo', technique='网格 DP · 五种情况 · 原地修改',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def uniquePathsWithObstacles(self, obstacleGrid):
        if not obstacleGrid:
            return 0

        m = len(obstacleGrid)
        n = len(obstacleGrid[0])

        for i in range(m):
            for j in range(n):
                if obstacleGrid[i][j] == 1:
                    obstacleGrid[i][j] = 0
                elif i == 0:
                    if j == 0:
                        obstacleGrid[i][j] = 1
                    else:
                        obstacleGrid[i][j] = obstacleGrid[i][j - 1]
                elif j == 0:
                    obstacleGrid[i][j] = obstacleGrid[i - 1][j]
                else:
                    obstacleGrid[i][j] = obstacleGrid[i - 1][j] + obstacleGrid[i][j - 1]
        return obstacleGrid[m - 1][n - 1]
''',
    call=f'Solution().uniquePathsWithObstacles({G})',
    expect=4,
    skip=['for i in range(m)', 'for j in range(n)'],
    views=[
        dict(type='custom', draw=_draw, h=620),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), 'm', 'n'],
    captions={
        'if not obstacleGrid': '特判空网格：这里不为空，继续',
        'm = len': '`m = {m}` 行',
        'n = len': '`n = {n}` 列；下面==直接在原矩阵上 dp==，不另开 f 数组',
        'if obstacleGrid[i][j] == 1': _cap_ob,
        'obstacleGrid[i][j] = 0': '情况 1：障碍物 `f[{i}][{j}] = 0`，==没有路能经过它==（原来的 1 被覆盖成 0）',
        'elif i == 0': lambda S, B, r: (f'`i = 0`：在第一行' if S.i == 0 else f'`i = {S.i}`，不在第一行'),
        14: lambda S, B, r: ('`j = 0`：这是最原始的位置' if S.j == 0 else f'`j = {S.j}`：第一行但不是起点'),
        'obstacleGrid[i][j] = 1': '情况 2：起点 `f[0][0] = 1`',
        'obstacleGrid[i][j] = obstacleGrid[i][j - 1]': lambda S, B, r: (
            f'情况 3：第一行只能从左边来 → `f[0][{S.j}] = f[0][{S.j - 1}]` = =={S.obstacleGrid[0][S.j]}=='
            + ('（左边被障碍挡住，后面全是 0）' if S.obstacleGrid[0][S.j] == 0 else '')),
        18: lambda S, B, r: ('`j = 0`：在第一列' if S.j == 0 else f'`j = {S.j}`，也不在第一列'),
        'obstacleGrid[i][j] = obstacleGrid[i - 1][j] +': lambda S, B, r: (
            f'情况 5：上 `f[{S.i - 1}][{S.j}] = {S.obstacleGrid[S.i - 1][S.j]}` + 左 `f[{S.i}][{S.j - 1}] = {S.obstacleGrid[S.i][S.j - 1]}`'
            f' = =={S.obstacleGrid[S.i][S.j]}=='),
        19: lambda S, B, r: f'情况 4：第一列只能从上边来 → `f[{S.i}][0] = f[{S.i - 1}][0]` = =={S.obstacleGrid[S.i][0]}==',
        'return obstacleGrid': '右下角 `f[{m - 1}][{n - 1}]` 就是答案：=={ret}== 种走法',
    },
    cards=dict(
        one_liner='f[i][j] 分五种情况讨论；只依赖上和左，直接在原矩阵上 dp',
        complexity='时间 `O(mn)`，额外空间 `O(1)`',
        problem=['`m × n` 网格，`1` 是障碍物；机器人从左上角出发，==只能向下或向右==',
                 '路径不能经过障碍物，求走到右下角的不同路径数',
                 '示例：`[[0,0,0],[0,1,0],[0,0,0]]` → `2`',
                 '本视频：`[[0,0,1,0],[0,0,0,0],[0,1,0,0]]` → `4`'],
        quote='如果不是障碍物，且i和j都不为0，那么此时可能==从上一行的同一列走过来，或者从同一行的左边一格走过来==，于是就有f[i][j] = f[i - 1][j] + f[i][j - 1]。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：到达第 `i` 行第 `j` 列一共有多少种走法',
              '障碍 → 0；起点 → 1；第一行 ← 左；第一列 ↑ 上；其余 = 上 + 左',
              'f 只由上一行和本行得到 → ==直接在原矩阵上 dp==，不额外开数组'],
        result='`f[2][3] = 4`：右下角共有 4 种走法',
        summary=['时间 `O(mn)`，原地修改，额外空间 `O(1)`（会改坏输入）',
                 '第一行被障碍挡住后，右边全为 0：第一行只能从左边来',
                 '判断顺序：==先判障碍==，再按「第一行 / 第一列 / 其他」分类',
                 '原文提到组合数学可能用母函数，但不如 dp 方便',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
