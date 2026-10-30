G1 = [[1, 1, 1, 1],
      [1, 0, 1, 0]]
G2 = [[1, 1, 0, 1],
      [0, 1, 0, 0]]
R, C = len(G2), len(G2[0])


def _islands():
    """（只用来上色）给 grid2 的每块岛屿编号；返回 编号表、每个岛屿的起点、每个岛屿是不是子岛屿"""
    idx = [[-1] * C for _ in range(R)]
    starts, sub = [], []
    for i in range(R):
        for j in range(C):
            if G2[i][j] and idx[i][j] < 0:
                k = len(starts)
                starts.append((i, j))
                st, ok = [(i, j)], True
                idx[i][j] = k
                while st:
                    x, y = st.pop()
                    ok = ok and G1[x][y] == 1
                    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                        a, b = x + dx, y + dy
                        if 0 <= a < R and 0 <= b < C and G2[a][b] and idx[a][b] < 0:
                            idx[a][b] = k
                            st.append((a, b))
                sub.append(ok)
    return idx, starts, sub


IDX, STARTS, SUB = _islands()


def _c2(S, a, b, v):
    """grid2：蓝 = 还没访问的陆地；黄 = 正在访问的岛屿（已淹掉）；岛屿查完后：绿 = 子岛屿，红 = 不是"""
    if G2[a][b] == 0:
        return None
    if v > 0:
        return 'blue'
    k = IDX[a][b]
    i, j = S.get('i'), S.get('j')
    if i is None:
        done = True
    elif STARTS[k] < (i, j):
        done = True
    elif STARTS[k] == (i, j):
        done = S.get('_line', 0) >= 22      # `if ok:` 这一行已经执行：结论出来了
    else:
        done = False
    if not done:
        return 'yellow'
    return 'green' if SUB[k] else 'red'


def _c1(S, a, b, v):
    return 'cyan' if v else None


def _info(S):
    if 'ok' not in S:
        return ''
    ln = S.get('_line', 0)
    if 'x' in S:
        flag = '==False==：已经碰到水域，这块岛屿不是子岛屿' if not S['ok'] else '==True==：到目前为止，这块岛屿的格子在 grid1 里都是陆地'
        return f'`ok` = {flag}'
    return f'`ok` = `{S["ok"]}`，已统计子岛屿 `ans = {S["ans"]}` 个'


CONFIG = dict(
    num=1905, title='统计子岛屿', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='网格图 DFS · 淹没 grid2 岛屿并检查 grid1 水域（Go 原文转写）',
    tags=['labuladong', '灵神核心路线', '难度分 1679'],
    code='''
dir4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

class Solution:
    def countSubIslands(self, grid1: List[List[int]], grid2: List[List[int]]) -> int:
        ans = 0
        ok = False
        n, m = len(grid2), len(grid2[0])
        def dfs(x: int, y: int) -> None:
            nonlocal ok
            grid2[x][y] = 0
            if grid1[x][y] == 0:  # 找到水域
                ok = False
            for dx, dy in dir4:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < m and grid2[nx][ny] > 0:
                    dfs(nx, ny)
        for i, row in enumerate(grid2):
            for j, v in enumerate(row):
                if v > 0:
                    ok = True  # 重置
                    dfs(i, j)
                    if ok:
                        ans += 1
        return ans
''',
    call=f'Solution().countSubIslands({G1}, {G2})',
    expect=1,
    skip=['for i, row in enumerate', 'for j, v in enumerate', 'for dx, dy in dir4', 'nx, ny = x + dx'],
    views=[
        dict(type='grid', var='grid1', label='grid1（青 = 陆地，空 = 水域；黄框 = dfs 当前格子）', cell=84, h=215,
             color=_c1, cursors=[('x', 'y', 'yellow')]),
        dict(type='grid', var='grid2', label='grid2（蓝 = 没访问的陆地，黄 = 正在淹的岛，绿 = 子岛屿，红 = 不是；粉框 = 邻居）', cell=84, h=215,
             color=_c2, cursors=[('x', 'y', 'yellow'), ('nx if _line == 15 else None', 'ny', 'pink'),
                                 ('i if _line in (19, 20, 21, 22, 23) else None', 'j', 'blue')]),
        dict(type='text', fn=_info, size=26, h=80),
        dict(type='calls', label='dfs 调用栈', h=120, hide=('grid1', 'grid2')),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'blue'), ('x', 'x', 'yellow'), ('y', 'y', 'yellow'), ('ok', 'ok', 'orange'), ('ans', 'ans', 'green')],
    max_steps=90,
    captions={
        'ans = 0': '`ans` 统计子岛屿个数',
        6: '`ok` 记录当前这块岛屿还是不是子岛屿（Go 里是包级变量 `var ok bool`，这里放在函数里用 `nonlocal`）',
        'n, m = len(grid2)': '`n = {n}` 行，`m = {m}` 列',
        'grid2[x][y] = 0': '访问 `({x},{y})`：把它改成 0，当作 visited，不会重复进来',
        'if grid1[x][y] == 0': lambda S, B, r: (f'`grid1[{S.x}][{S.y}] = 0`：grid1 这里是==水域==，但 grid2 这格是陆地 → 这块岛不可能被包含'
                                                if S.grid1[S.x][S.y] == 0 else f'`grid1[{S.x}][{S.y}] = 1`：grid1 这里也是陆地，没问题'),
        12: '`ok = False`：标记失败，但==不能提前返回==，整块岛屿还是要淹完，否则剩下的格子会被当成新岛屿',
        'if 0 <= nx < n': lambda S, B, r: (f'邻居 `({S.nx},{S.ny})` 出界了' if not (0 <= S.nx < S.n and 0 <= S.ny < S.m)
                                           else (f'邻居 `({S.nx},{S.ny})` 在界内，`grid2` 是 `{S.grid2[S.nx][S.ny]}` → ==是没淹过的陆地==，继续 dfs'
                                                 if S.grid2[S.nx][S.ny] > 0 else
                                                 f'邻居 `({S.nx},{S.ny})` 在界内，但 `grid2` 是 0（水或已访问），不进')),
        'dfs(nx, ny)': '递归进入 `({nx},{ny})`',
        'if v > 0': lambda S, B, r: (f'扫描 `({S.i},{S.j})`：`grid2` 是 {S.v} → ==新岛屿的起点==' if S.v > 0
                                     else (f'扫描 `({S.i},{S.j})`：这格原本是陆地，已经被前面的 dfs ==淹掉== → 跳过' if G2[S.i][S.j]
                                           else f'扫描 `({S.i},{S.j})`：是水 → 跳过')),
        'ok = True': '新岛屿：先假设它是子岛屿，`ok = True`（每块岛屿开始前==重置==）',
        'dfs(i, j)': '`dfs(x, y)` 会把从 `({i},{j})` 连出去的==整块岛屿淹掉==（改成 0），顺便对照 grid1',
        'if ok:': lambda S, B, r: ('dfs 结束，`ok` 仍是 True：这块岛屿没碰到过 grid1 的水域 → ==是子岛屿=='
                                   if S.ok else 'dfs 结束，`ok` 是 False：碰到过水域 → 不是子岛屿'),
        'ans += 1': '子岛屿 +1：`ans = {ans}`',
        'return ans': '返回子岛屿的个数 =={ret}==',
    },
    cards=dict(
        one_liner='淹 grid2 的岛，只要有一格在 grid1 是水，这块岛就不是子岛屿',
        complexity='时间 `O(nm)`，空间 `O(nm)`（递归栈）',
        problem=['`grid1`、`grid2` 都是 0/1 网格，1 是陆地，岛屿由上下左右相连的 1 组成',
                 '`grid2` 的一块岛，若被 `grid1` 的某一块岛==完全包含==，就是子岛屿；求个数',
                 f'示例：`grid1 = {G1}`，`grid2 = {G2}` → `1`'],
        quote='其实注意到只要 grid2 的岛屿在 grid1 对应位置上不存在水域，那其就是子岛屿。',
        quote_src='—— 灵茶山艾府题解',
        idea=['一开始想给 grid1 的每个岛都求连通分量，太复杂；其实==不需要==',
              'grid2 的一块岛本身是连通的：它在 grid1 里对应的格子若全是陆地，就必然在同一块岛里',
              '所以对 grid2 每块岛 dfs：碰到 `grid1` 为 0 的格子就 `ok = False`；dfs 结束时 `ok` 仍为 True 才计数'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python；`ok` 原是包级变量，转写时放进方法里用 `nonlocal`',
                 'Go 里 `if x, y := x+d.x, y+d.y` 会遮蔽外层 `x, y`；Python 里不能同名覆盖，改用 `nx, ny`',
                 '时间 `O(nm)`，每个格子最多访问一次；dfs 里把 `grid2` 改成 0 兼作 visited',
                 '易错：发现水域后==不能提前退出==，要把整块岛淹完；`ok` 每块新岛屿前要重置为 True'],
    ),
)
