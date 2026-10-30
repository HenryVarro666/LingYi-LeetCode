G = [[0, 0, 0, 0], [0, 1, 0, 0], [1, 0, 0, 0]]
M, N = len(G), len(G[0])


def _full_dp():
    f = [[0] * (N + 1) for _ in range(M + 1)]
    f[0][1] = 1
    for i in range(M):
        for j in range(N):
            if G[i][j] == 0:
                f[i + 1][j + 1] = f[i][j + 1] + f[i + 1][j]
    return [r[1:] for r in f[1:]]


DP = _full_dp()


def _i(S):
    row, g = S.get('row'), S.get('obstacleGrid')
    if row is None or g is None:
        return None
    for k, r in enumerate(g):
        if r is row:
            return k
    return None


def _prog(S):
    """(已算完的格子数, 当前格子)"""
    line = S.get('_line')
    if line == 12:
        return M * N, None
    i, j = _i(S), S.get('j')
    if i is None or j is None:
        return 0, None
    if line == 8:
        return i * N + j, (i, j)
    if line in (9, 11):
        return i * N + j + 1, (i, j)
    return 0, None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '网格（红 = 障碍；格内数字 = 走到这里的路径数；蓝 = 上，粉 = 左）', 22, T['muted'], bold=True)
    done, cur = _prog(S)
    cell = min(104, (y1 - y0 - 80) / M)
    gw = cell * N
    sx = x0 + (x1 - x0 - gw) / 2 + 20
    sy = y0 + 64
    for j in range(N):
        cv.text((sx + j * cell + cell / 2, sy - 6), f'j={j}', 18, T['dim'], anchor='mb', mono=True)
    for i in range(M):
        cv.text((sx - 12, sy + i * cell + cell / 2), f'i={i}', 18, T['dim'], anchor='rm', mono=True)
        for j in range(N):
            k = i * N + j
            X, Y = sx + j * cell, sy + i * cell
            ob = G[i][j] == 1
            fill = (90, 38, 40) if ob else T['panel2']
            if cur and (i, j) == cur and S.get('_line') in (9, 11):
                fill = T['red'] if ob else T['green']
            elif cur and S.get('_line') == 8:
                ci, cj = cur
                if (i, j) == (ci - 1, cj) and not ob:
                    fill = T['blue']
                elif (i, j) == (ci, cj - 1) and not ob:
                    fill = T['pink']
            cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), fill=fill, r=10, outline=T['border'], width=1)
            hot = fill in (T['green'], T['blue'], T['pink'], T['red'])
            if k < done:
                cv.text((X + cell / 2, Y + cell / 2), DP[i][j], 38, T['bg'] if hot else T['text'], anchor='mm', bold=True)
            elif ob:
                cv.text((X + cell / 2, Y + cell / 2), '障', 30, T['red'], anchor='mm', bold=True)
            else:
                cv.text((X + cell / 2, Y + cell / 2), '?', 30, T['dim'], anchor='mm', bold=True)
    if cur:
        ci, cj = cur
        X, Y = sx + cj * cell, sy + ci * cell
        cv.rect((X - 1, Y - 1, X + cell + 1, Y + cell + 1), outline=T['yellow'], width=5, r=12)
        cv.text((X + cell / 2, Y + cell + 4), '当前', 18, T['yellow'], anchor='mt', bold=True)
    # 起点 / 终点标记
    cv.text((sx - 12, sy - 8), '起点↘', 18, T['cyan'], anchor='rb', bold=True)
    cv.text((sx + gw + 8, sy + M * cell), '←终点', 18, T['cyan'], anchor='lb', bold=True)


def _formula(S):
    line = S.get('_line')
    j, f = S.get('j'), S.get('f')
    if line == 9:
        return f'`f[{j + 1}] += f[{j}]`：上 + 左 = =={f[j + 1]}=='
    if line == 11:
        return f'障碍：`f[{j + 1}] = 0`'
    if line == 8:
        return f'`f[{j + 1}]` 此刻还是==上一行==的值（上），`f[{j}]` 已是==本行==的值（左）'
    return '一维 `f`：`f[j+1]` = 当前行第 `j` 列的路径数，`f[0]` 恒为 0'


def _f_color(S, k, v):
    line, j = S.get('_line'), S.get('j')
    if j is None:
        return 'green' if line == 5 and k == 1 else None
    if line == 8:
        return 'blue' if k == j + 1 else 'pink' if k == j else None
    if line == 9:
        return 'green' if k == j + 1 else 'pink' if k == j else None
    if line == 11:
        return 'red' if k == j + 1 else None
    if line == 12:
        return 'green' if k == N else None
    return None


def _cap_if(S, B, ret):
    i, j, x = _i(S), S.j, S.x
    head = f'新的一行 `i = {i}`：' if j == 0 else ''
    if x == 0:
        return head + f'`({i},{j})` 是空地：上 = 旧 `f[{j + 1}] = {S.f[j + 1]}`，左 = `f[{j}] = {S.f[j]}`'
    return head + f'`({i},{j})` 是==障碍==，任何路径都进不来'


def _cap_add(S, B, ret):
    i, j = _i(S), S.j
    up, left, v = B.f[j + 1], S.f[j], S.f[j + 1]
    if i == 0 and j == 0:
        return f'起点 `(0,0)`：上方是预置的 `f[1] = 1`，左边 `f[0] = 0` → =={v}=='
    if i == 0:
        return f'第 0 行上方出界（0 条）→ 只能从左边来：`{up} + {left}` = =={v}=='
    if j == 0:
        return f'第 0 列左边是 `f[0] = 0` → 只能从上面来：`{up} + 0` = =={v}=='
    if up == 0 and left == 0:
        return f'上方 `({i - 1},{j})` 和左边 `({i},{j - 1})` 都是 0 条 → 这里==也走不到=='
    return f'上方 `({i - 1},{j})` 有 `{up}` 条 + 左边 `({i},{j - 1})` 有 `{left}` 条 → 加法原理 =={v}=='


def _cap_zero(S, B, ret):
    i, j = _i(S), S.j
    old = B.f[j + 1]
    tail = f'不能保留上一行的旧值 `{old}`' if old else '旧值恰好是 0，但这行不能省'
    return f'`({i},{j})` 是障碍 → `f[{j + 1}] = 0`：{tail}'


CONFIG = dict(
    num=63, title='不同路径 II', difficulty='Medium', category='多维动态规划',
    author='灵茶山艾府', technique='网格图 DP · 记忆化搜索 → 递推 → 空间优化',
    tags=['面试经典150'],
    code='''
class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        n = len(obstacleGrid[0])
        f = [0] * (n + 1)
        f[1] = 1
        for row in obstacleGrid:
            for j, x in enumerate(row):
                if x == 0:
                    f[j + 1] += f[j]
                else:
                    f[j + 1] = 0
        return f[n]
''',
    call=f'Solution().uniquePathsWithObstacles({G})',
    expect=3,
    skip=['for row in', 'for j, x in'],
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='custom', draw=_draw, h=440),
        dict(type='array', var='f', label='f（长 n+1；f[j+1] 对应第 j 列，f[0] = 左边出界）', cell=96, color=_f_color),
    ],
    watch=[('i', _i, 'yellow'), ('j', 'j', 'yellow'), 'x', ('f[n]', 'f[n]', 'green')],
    captions={
        'n = len': '网格有 `n = {n}` 列',
        'f = [0]': '`f` 长 `n + 1 = {n + 1}`：多出来的 `f[0]` ==恒为 0==，代表左边出界',
        'f[1] = 1': '`f[1] = 1`：翻译自 `f[0][1] = 1`，让起点 `(0,0)` 也能用 ==上 + 左== 算出 1',
        'if x == 0': _cap_if,
        'f[j + 1] += f[j]': _cap_add,
        'f[j + 1] = 0': _cap_zero,
        'return f[n]': '最后一行的 `f[n]` 就是右下角：共 =={ret}== 条路径',
    },
    cards=dict(
        one_liner='最后一步从上或左来；障碍格清零，一维数组滚动',
        complexity='时间 `O(mn)`，空间 `O(n)`',
        problem=['`m × n` 网格，`1` 是障碍物；机器人从左上角出发，==只能向下或向右==',
                 '路径不能经过障碍物，求走到右下角的不同路径数',
                 '示例：`[[0,0,0],[0,1,0],[0,0,0]]` → `2`',
                 '本视频：`[[0,0,0,0],[0,1,0,0],[1,0,0,0]]` → `3`'],
        quote='定义状态为 dfs(i,j)，表示从起点 (0,0) 走到 (i,j) 的==方案数==。……如果 obstacleGrid[i][j]=1，那么 dfs(i,j)=0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['想最后一步：`dfs(i,j) = dfs(i-1,j) + dfs(i,j-1)`；出界为 0，`dfs(0,0) = 1`',
              '1:1 翻译成递推 `f[i+1][j+1]`；它==只依赖上一行和本行左边==',
              '压成一维：旧的 `f[j+1]` 就是「上」，刚算好的 `f[j]` 就是「左」',
              '所以 `f[j+1] += f[j]`，遇到障碍直接 `f[j+1] = 0`'],
        result='`f = [0,0,1,1,3]`：右下角 `f[4] = 3` 条路径',
        after=[dict(heading='原文的四种写法', lines=[
            '记忆化搜索：`@cache dfs(i,j)`，时间空间都是 `O(mn)`',
            '递推：`f` 开 `(m+1)×(n+1)`，`f[0][1] = 1` 省掉起点特判',
            '空间优化（本视频）：只留一行 `n+1` 个数，正序更新',
            '原地修改：拿 `obstacleGrid[0]` 当 f，`O(1)` 额外空间，但要特判边界',
        ])],
        summary=['时间 `O(mn)`，空间 `O(n)`',
                 '易错：障碍格必须写 `f[j+1] = 0`，==不能跳过==，否则残留上一行的值',
                 '易错：数组开 `n + 1`，`f[0]` 恒为 0 当左边界；答案是 `f[n]`',
                 '和完全背包一样==正序==遍历：用到的 `f[j]` 必须已是本行新值',
                 '对比 62 题：同一套「最后一步」思路，只多一个障碍判断'],
    ),
)
