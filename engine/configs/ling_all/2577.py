G0 = [[0, 1, 3], [5, 4, 2]]

CONFIG = dict(
    num=2577, title='在网格图中访问一个格子的最少时间', difficulty='Hard', category='网格图',
    author='灵茶山艾府', technique='Dijkstra + 奇偶性修正（反复横跳等待）',
    tags=['灵神题单·网格图', '灵神题单·图论算法', '难度分 2382'],
    code='''
class Solution:
    def minimumTime(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        if grid[0][1] > 1 and grid[1][0] > 1:  # 无法「等待」
            return -1

        dis = [[inf] * n for _ in range(m)]
        dis[0][0] = 0
        h = [(0, 0, 0)]
        while True:  # 可以等待，就一定可以到达终点
            d, i, j = heappop(h)
            if d > dis[i][j]: continue
            if i == m - 1 and j == n - 1:  # 找到终点，此时 d 一定是最短路
                return d
            for x, y in (i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1):  # 枚举周围四个格子
                if 0 <= x < m and 0 <= y < n:
                    nd = max(d + 1, grid[x][y])
                    nd += (nd - x - y) % 2  # nd 必须和 x+y 同奇偶
                    if nd < dis[x][y]:
                        dis[x][y] = nd  # 更新最短路
                        heappush(h, (nd, x, y))
''',
    call=f'Solution().minimumTime({G0})',
    expect=5,
    views=[
        dict(type='grid', var='grid', label='grid（每格 = 最早可进入时刻）', cursors=[('i', 'j', 'yellow')], h=170, cell=64),
        dict(type='table', var='dis', label='dis[i][j]：到达该格的最小时刻（inf = 还没到过）', cursors=[('x', 'y', 'pink')], h=170, cell=64,
             color=lambda S, i, j, v: 'green' if v != float('inf') else None),
        dict(type='heap', var='h', fmt=lambda t: f'{t[0]}@({t[1]},{t[2]})', label='h 最小堆（时刻@格子）', top_color='blue', h=130),
    ],
    watch=[('d', 'd', 'blue'), ('i', 'i'), ('j', 'j'), ('nd', 'nd', 'green')],
    max_steps=90,
    skip=['m, n = len', 'for x, y in', 'while True', 16, 17, 12, 13],
    captions={
        'if grid[0][1] > 1 and grid[1][0] > 1': lambda S, B, ret: (
            f'`grid[0][1] = {S.grid[0][1]}`，`grid[1][0] = {S.grid[1][0]}`：只要有一个 `≤ 1`，就能 ==在起点和它之间反复横跳「等待」== → 一定能到终点'
            if not (S.grid[0][1] > 1 and S.grid[1][0] > 1) else '两个邻居都要等到 `> 1` 才开放，起点又不能原地不动 → 走不出去，返回 `-1`'),
        'dis = [[inf]': '`dis[i][j]`：到达格子 `(i,j)` 的最小时刻，先全设成无穷大',
        'dis[0][0] = 0': '出发时刻是 `0`',
        'h = [(0, 0, 0)]': '最小堆里放 `(时刻, 行, 列)`，每次取时刻最小的格子（Dijkstra）',
        'd, i, j = heappop(h)': '取出时刻最小的：`d = {d}`，格子 `({i},{j})`',
        'if d > dis[i][j]': lambda S, B, ret: (f'`d = {S.d}` 比 `dis[{S.i}][{S.j}] = {S.dis[S.i][S.j]}` 大 → ==过期的旧记录==，跳过' if S.d > S.dis[S.i][S.j] else f'`d = {S.d} = dis[{S.i}][{S.j}]`，是最新记录 → 继续'),
        'if i == m - 1 and j == n - 1': lambda S, B, ret: (f'`({S.i},{S.j})` 是终点：==堆顶最小，所以 d 就是最短时刻==' if (S.i == S.m - 1 and S.j == S.n - 1) else f'`({S.i},{S.j})` 还不是终点，向四周扩展'),
        'return d': '到达终点，最早时刻 `{d}`',
        'if 0 <= x < m and 0 <= y < n': lambda S, B, ret: (f'邻居 `({S.x},{S.y})` ' + ('在网格内' if (0 <= S.x < S.m and 0 <= S.y < S.n) else '越界，跳过')),
        'nd = max(d + 1, grid[x][y])': '走一步要 `d+1 = {d + 1}`，但格子 `({x},{y})` 最早 `{grid[x][y]}` 才开放（可以在前面反复横跳等）→ 取较大：`nd = {nd}`',
        'nd += (nd - x - y) % 2': lambda S, B, ret: (
            f'邻居 `({S.x},{S.y})`：走一步 `d+1 = {S.d + 1}`，格子 `{S.grid[S.x][S.y]}` 才开放（可横跳等）→ 取大 `nd = {B.nd}`。到它的时刻必须和 `x+y = {S.x + S.y}` 同奇偶（棋盘染色），`nd` 与它' + ('同奇偶 → 不用加' if (B.nd - S.x - S.y) % 2 == 0 else '不同奇偶 → ==多等 1 步==，`nd += 1`') + f' → `{S.nd}`'),
        'if nd < dis[x][y]': lambda S, B, ret: (f'`nd = {S.nd}` < `dis[{S.x}][{S.y}] = {S.dis[S.x][S.y]}` → 更近，更新' if S.nd < S.dis[S.x][S.y] else f'`nd = {S.nd}` ≥ `dis[{S.x}][{S.y}] = {S.dis[S.x][S.y]}` → 不比已知的好，不更新'),
        'dis[x][y] = nd': '更新最短路：`dis[{x}][{y}] = {nd}`',
        'heappush(h, (nd, x, y))': '把 `({nd}, {x}, {y})` 压入堆，等它成为最小再扩展',
    },
    cards=dict(
        one_liner='Dijkstra 求最短时刻：边权是等待后的时刻，再按 x+y 奇偶性修正',
        complexity='时间 `O(mn log mn)`，空间 `O(mn)`',
        problem=['`grid[i][j]` 是能进入该格的==最早时刻==，从左上角时刻 0 出发，右下角是终点',
                 '每秒必须移动到相邻格子，不能停留；求最早到达右下角的时刻，到不了返回 `-1`',
                 '本视频示例：`[[0,1,3],[5,4,2]]` → `5`'],
        quote='如果 grid[0][1]≤1 或者 grid[1][0]≤1，那么可以通过「反复横跳」来「等待」。否则根本就无法移动到这两个格子，也就无法到达终点，返回 -1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['能「反复横跳」等待，所以到格子 `(i,j)` 的时刻只受 `grid[i][j]` 下限限制',
              '但每步换一次棋盘颜色，==到达时刻的奇偶性必须等于 `i+j` 的奇偶性==，不同就再等 1 秒',
              '于是 `nd = max(d+1, grid[x][y])`，再 `nd += (nd-x-y)%2`，其余就是标准 Dijkstra'],
        summary=['时间 `O(mn log mn)`，空间 `O(mn)`',
                 '易错点：-1 的判断只看起点两个邻居，其余格子都能靠横跳等待',
                 '易错点：奇偶修正要在 `max` 之后做，且要同时考虑 `grid` 下限和 `d+1`',
                 '灵神另有「二分答案 + BFS」写法（从终点倒着一刻不停地走判断能否在 `endTime` 到达），视频只演示 Dijkstra',
                 '`while True` 不会死循环：能等待就一定能到终点，堆不会空'],
    ),
)
