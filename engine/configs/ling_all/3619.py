IMG = [[1, 2, 0, 3], [0, 3, 0, 4], [6, 0, 3, 0]]
KK = 3
M, N = 3, 4


def _islands():
    seen, out = set(), []
    for i in range(M):
        for j in range(N):
            if IMG[i][j] and (i, j) not in seen:
                st, cells = [(i, j)], []
                seen.add((i, j))
                while st:
                    x, y = st.pop()
                    cells.append((x, y))
                    for a, b in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                        if 0 <= a < M and 0 <= b < N and IMG[a][b] and (a, b) not in seen:
                            seen.add((a, b))
                            st.append((a, b))
                out.append(cells)
    return out


ISL = _islands()
ISL_OF = {c: k for k, cells in enumerate(ISL) for c in cells}
ISL_SUM = [sum(IMG[x][y] for x, y in cells) for cells in ISL]


def _cur(S):
    """正在 DFS 的岛编号（不在 dfs 内时为 None）"""
    I = S['_inner']
    if 'res' in I:
        return ISL_OF.get((I['i'], I['j']))
    return None


def _color(S, i, j, v):
    if IMG[i][j] == 0:
        return None
    if v != 0:
        return 'blue'            # 还没访问的陆地
    k = ISL_OF[(i, j)]
    if k == _cur(S):
        return 'yellow'          # 当前岛，已访问
    return 'green' if ISL_SUM[k] % KK == 0 else 'red'


def _info(S):
    k = _cur(S)
    if k is None:
        return f'绿 = 总价值是 `{KK}` 的倍数的岛　红 = 不是　蓝 = 未访问陆地　　已数到 ==`{S.get("ans", 0)}`== 个'
    got = sum(IMG[x][y] for x, y in ISL[k] if S['grid'][x][y] == 0)
    return f'黄 = 当前岛，已访问格子之和 ==`{got}`==　　已数到 ==`{S.get("ans", 0)}`== 个'


CONFIG = dict(
    num=3619, title='总价值可以被 K 整除的岛屿数目', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='网格图 DFS · 顺便累加岛屿元素和',
    tags=['灵神核心路线', '灵神题单·网格图', '难度分 1461'],
    code='''
class Solution:
    def countIslands(self, grid: List[List[int]], k: int) -> int:
        m, n = len(grid), len(grid[0])

        def dfs(i: int, j: int) -> int:
            res = grid[i][j]
            grid[i][j] = 0  # 标记 (i,j) 访问过
            for x, y in (i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j):
                if 0 <= x < m and 0 <= y < n and grid[x][y]:
                    res += dfs(x, y)
            return res

        ans = 0
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                if x and dfs(i, j) % k == 0:
                    ans += 1
        return ans
''',
    call=f'Solution().countIslands({IMG}, {KK})',
    expect=3,
    skip=['for x, y in', 'for i, row in', 'for j, x in', 'm, n = len', 'if 0 <= x < m'],
    views=[
        dict(type='text', fn=_info, size=22),
        dict(type='grid', var='grid', cursors=[('i', 'j', 'yellow', '(i,j)')], cell=96, h=330,
             color=_color),
        dict(type='calls', label='递归调用栈（dfs 深度）', h=230),
    ],
    watch=[('ans', 'ans', 'green'), ('k', 'k'), ('res', lambda S: S['_inner'].get('res'), 'yellow')],
    captions={
        'res = grid[i][j]': '到达 `({i},{j})`，把它的值 `{grid[i][j]}` 记进这座岛的总价值 `res`',
        'grid[i][j] = 0': '把 `({i},{j})` 置 `0`：==标记访问过==，之后依次看右、左、下、上四邻，出界/水/已访问的直接跳过',
        'res += dfs': lambda S, B, r: (
            f'邻居 `({S.x},{S.y})` 在界内且是没访问的陆地 → 递归进去，把它那部分岛的和累加到 `res`'
            if S.grid[S.x][S.y] else f'`({S.x},{S.y})` 那部分岛已走完，`res` 累加到 `{S.res}`'),
        'return res': lambda S, B, r: (
            f'整座岛走完，总价值 `res = {r}`，`{r} % {S.k} = {r % S.k}` → '
            + ('==整除==，外层会 `ans += 1`' if r % S.k == 0 else '==不能整除==，这座岛不计入答案')
            if r == ISL_SUM[_cur(S)] else f'这个格子往下能到的陆地都走完了 → 返回这部分的和 `res = {r}`'),
        'ans = 0': '`ans = 0`：还没数到任何一座合格的岛，开始逐格扫描',
        'if x and dfs': lambda S, B, r: (f'`({S.i},{S.j})` 是陆地且没访问过 → ==发现新岛==，DFS 求总价值再 `% k`'
                                         if S.x else f'`({S.i},{S.j})` 是水或已访问 → 跳过'),
        'ans += 1': '这座岛总价值是 `k = {k}` 的倍数 → 答案加一：`ans = {ans}`',
        'return ans': '扫描结束，总价值能被 `k` 整除的岛有 ==`{ret}`== 座',
    },
    max_steps=110,
    cards=dict(
        one_liner='岛屿数量模板：DFS 一座岛，顺便把格子值加起来',
        complexity='时间 `O(mn)`，空间 `O(mn)`（蛇形岛递归栈）',
        problem=['`m×n` 矩阵，正整数是陆地，上下左右相连的陆地组成岛屿',
                 '岛屿总价值 = 岛上所有格子的值之和',
                 '求总价值能被 `k` 整除的岛屿数量',
                 '本视频示例：3×4 网格，`k = 3` → ==3=='],
        quote='做法同 200. 岛屿数量，我的题解，在 DFS 岛屿的同时统计岛屿格子的元素和。如果岛屿元素和是 k 的倍数，那么把答案加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i, j)` 返回「从 `(i,j)` 出发能走到的这部分岛」的元素和',
              '进入格子先把它置 `0`，当作访问标记，不再走回头路',
              '四个邻居里是陆地的递归累加：`res += dfs(x, y)`',
              '外层扫描遇到未访问的陆地，岛的总和 `% k == 0` 就 `ans += 1`'],
        result='运行结束，返回 `3`：总价值 6、6、3 的三座岛能被 3 整除，总价值 7 的不能',
        summary=['时间 `O(mn)`：每格访问一次；空间 `O(mn)`：之字形岛递归很深',
                 '易错：陆地判断用 `grid[x][y]` 非零，==值本身就是访问标记==，访问后置 `0`',
                 '岛屿和要在 DFS 返回后==整座岛==再取模，不能每个子树单独判',
                 '会修改输入 `grid`；和岛屿数量（200）是同一套模板'],
    ),
)
