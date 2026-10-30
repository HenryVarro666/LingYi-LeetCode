MAZE = ["S.#.", "...#", "#..#", "..T."]


def _maze(S):
    return [list(r) for r in S['maze']]


def _dis(S):
    d = S.get('dis_from_t')
    if d is None:
        return None
    return [['#' if MAZE[i][j] == '#' else ('∞' if v == float('inf') else v) for j, v in enumerate(row)]
            for i, row in enumerate(d)]


def _mcolor(S, i, j, v):
    vis = S.get('vis')
    md = S.get('max_dis')
    if vis is not None and md is not None and vis[i][j] == md and v != 'T':
        return 'green'
    if v == '#':
        return 'red'
    return None


def _dcolor(S, i, j, v):
    md = S.get('max_dis')
    if md is not None and v not in ('#', '∞') and v > md:
        return 'orange'
    if v == '#':
        return 'red'
    return None


def _text(S):
    md = S.get('max_dis')
    if md is None:
        return '上图：迷宫；下图：每个格子到终点 `T` 的最短距离（`#` 墙，`∞` 到不了）'
    return f'二分试探 `max_dis = {md}`：下图 ==橙色格子（距离 > {md}）== 一旦被传送到，小扣就输了'


def _tp(S, B, r):
    i, j, n, m = S.i, S.j, S.n, S.m
    d, md = S.dis_from_t, S.max_dis
    if S.maze[i][j] != '.':
        return f'`({i},{j})` 不是空地，守护者不能在这里发动传送，继续走'
    a = (i, n - 1 - j)
    b = (m - 1 - i, j)
    bad = [p for p in (a, b) if S.maze[p[0]][p[1]] != '#' and d[p[0]][p[1]] > md]
    hv = f'水平镜像 `{a}`、竖直镜像 `{b}`'
    if bad:
        p = bad[0]
        return f'标记已走；{hv}：传到 `{p}` 后距离 `{d[p[0]][p[1]]}` > {md} → 守护者会这么干，==这个位置小扣不能走=='
    return f'标记已走；{hv}：传过去距离都 ≤ {md}（或是墙）→ 守护者传送也没用，可以继续走'


CONFIG = dict(
    num='LCP 75', title='传送卷轴', difficulty='Hard', category='网格图',
    author='灵茶山艾府', technique='BFS 预处理 + 二分答案 + DFS',
    tags=['灵神题单', '网格图 · 综合应用'],
    code='''
class Solution:
    def challengeOfTheKeeper(self, maze: List[str]) -> int:
        m, n = len(maze), len(maze[0])

        # 1. 找到起点终点坐标
        for i, row in enumerate(maze):
            for j, c in enumerate(row):
                if c == 'S':
                    sx, sy = i, j
                elif c == 'T':
                    tx, ty = i, j

        # 2. BFS 计算终点到其余点的最短距离
        dis_from_t = [[inf] * n for _ in range(m)]
        dis_from_t[tx][ty] = 0
        q = [(tx, ty)]
        step = 1
        while q:
            tmp = q
            q = []
            for i, j in tmp:
                for x, y in (i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1):
                    if 0 <= x < m and 0 <= y < n and maze[x][y] != '#' and dis_from_t[x][y] == inf:
                        dis_from_t[x][y] = step
                        q.append((x, y))
            step += 1

        # 3. 剪枝：如果 S 无法到达 T，直接返回 -1
        if dis_from_t[sx][sy] == inf:
            return -1

        # 4. 二分答案 https://www.bilibili.com/video/BV1AP41137w7/
        vis = [[-1] * n for _ in range(m)]
        def check(max_dis: int) -> bool:
            # DFS，看能否在「附加负面效果」的情况下，移动不超过 max_dis 步到达终点
            def dfs(i: int, j: int) -> bool:
                if i < 0 or i >= m or j < 0 or j >= n or vis[i][j] == max_dis or maze[i][j] == '#':
                    return False
                if maze[i][j] == 'T':  # 到达终点
                    return True
                vis[i][j] = max_dis  # 为避免反复创建 vis，用一个每次二分都不一样的数来标记
                # 守护者使用卷轴传送小扣，如果小扣无法在 maxDis 步内到达终点，则返回 false
                if maze[i][j] == '.' and \\
                   (maze[i][n - 1 - j] != '#' and dis_from_t[i][n - 1 - j] > max_dis or
                    maze[m - 1 - i][j] != '#' and dis_from_t[m - 1 - i][j] > max_dis):
                    return False
                for x, y in (i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1):
                    if dfs(x, y):
                        return True
                return False
            return dfs(sx, sy)
        ans = bisect_left(range(m * n + 1), True, key=check)
        return -1 if ans > m * n else ans
''',
    call=f'Solution().challengeOfTheKeeper({MAZE!r})',
    expect=3,
    skip=['m, n = len', 'for i, row in enumerate', 'for j, c in enumerate', "if c == 'S'", "sx, sy = i, j",
          "elif c == 'T'", "tx, ty = i, j", 'dis_from_t = [[inf]', 'dis_from_t[tx][ty] = 0', 'step = 1', 'tmp = q',
          'q = []', 'for i, j in tmp', 'for x, y in (i + 1', 'q.append', 'step += 1',
          'vis = [[-1]', 'def check', 'def dfs', 'if i < 0 or i >= m', "if maze[i][j] == 'T'",
          'if dfs(x, y)', 'return False', 'return True', 'if 0 <= x < m and 0 <= y < n',
          'while q', "maze[i][n - 1 - j] != '#'", 'maze[m - 1 - i][j] != \'#\'', 'vis[i][j] = max_dis'],
    max_steps=64,
    views=[
        dict(type='grid', var=_maze, label='maze（绿 = 本轮 DFS 走过；蓝框 = DFS 当前格）', cell=76, h=330, color=_mcolor,
             cursors=[('i', 'j', 'blue')]),
        dict(type='grid', var=_dis, label='dis_from_t（到终点的最短距离）', cell=76, h=330, color=_dcolor),
        dict(type='text', fn=_text, size=24, h=90),
    ],
    watch=[('max_dis', 'max_dis', 'blue'), ('step', 'step'), ('ans', 'ans', 'green')],
    captions={
        '_unused_while': lambda S, B, r: (f'`q` 还有 {len(S.q)} 个点，处理 BFS 的下一层' if S.q else 'BFS 结束：终点到所有可达点的距离算完'),
        'if 0 <= x < m and 0 <= y < n': lambda S, B, r: (
            f'`({S.x},{S.y})` 是没算过的空地 → 距离 ==`{S.step}`== 入队'
            if 0 <= S.x < S.m and 0 <= S.y < S.n and S.maze[S.x][S.y] != '#' and B.dis_from_t[S.x][S.y] == inf
            else f'`({S.x},{S.y})` 越界、是墙或已算过，跳过'),
        'dis_from_t[x][y] = step': '`dis_from_t[{x}][{y}] = {step}`：第 `{step}` 层，离终点 {step} 步',
        'if dis_from_t[sx][sy] == inf': lambda S, B, r: ('起点到不了终点 → 直接返回 `-1`' if S.dis_from_t[S.sx][S.sy] == inf
                                                         else f'起点 `S` 离终点 `{S.dis_from_t[S.sx][S.sy]}` 步，可达，继续二分'),
        'maze[i][j] == \'#\'': '撞墙、越界或本轮已走过 → 回溯',
        'if maze[i][j] == \'.\' and': _tp,
        'return dfs(sx, sy)': '试探 `max_dis = {max_dis}`：从 `S` 出发 DFS，==被守护者「卡住」的格子不能走==，能走到 `T` 吗？',
        'ans = bisect_left': lambda S, B, r: f'二分得到最小能行的 `max_dis`：=={S.ans}==',
        'return -1 if ans > m * n': '`ans = {ans}` 没超过 `m*n`，说明有解，返回 `{ans}`',
    },
    cards=dict(
        one_liner='二分「传送后最多还要走几步」，DFS 判断小扣能否走到终点',
        complexity='时间 `O(mn log(mn))`，空间 `O(mn)`',
        problem=['正方形迷宫：`S` 起点，`T` 终点，`#` 墙，`.` 空地',
                 '小扣站在空地时，守护者可把他传到水平或竖直镜像位置（不能是墙）',
                 '传送后小扣想最快到终点，守护者想让他最慢；求最少还要走几步，无解 `-1`',
                 '本视频：`["S.#.","...#","#..#","..T."]` → `3`'],
        quote='二分答案 maxDis：看能否在「附加负面效果」的情况下，移动不超过 maxDis 步到达终点。我写的 DFS，如果 DFS 中的某个位置，守护者使用卷轴传送小扣，并将小扣传送到一个无法到达终点，或者无法在 maxDis 步内到达终点的位置，则不再 DFS。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先从 `T` 做 BFS，得到每格到终点的距离 `dis_from_t`',
              '二分 `max_dis`：传送目的地距离 > `max_dis` 的空地，守护者会在那里传送，小扣不能走',
              '剩下的格子上 DFS，能走到 `T` 就说明答案 ≤ `max_dis`'],
        summary=['时间 `O(mn log(mn))`，空间 `O(mn)`',
                 '易错：只有站在 `.` 上才能被传送，`S` 起点不行；传送目标是墙则不算',
                 '易错：镜像位置可能就是原位，水平、竖直两个方向都要判断',
                 '`vis` 用 `max_dis` 作标记，二分时不必反复清空',
                 '`bisect_left(range, True, key=check)` 需要 Python 3.10+'],
    ),
)
