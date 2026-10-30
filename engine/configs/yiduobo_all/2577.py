G0 = [[0, 1, 3], [5, 4, 2]]

CONFIG = dict(
    num=2577, title='在网格图中访问一个格子的最少时间', difficulty='Hard', category='网格图',
    author='yiduobo', technique='类 Dijkstra：先修正奇偶，再取堆顶',
    tags=['灵神题单·网格图', '灵神题单·图论算法', '难度分 2382'],
    code='''
class Solution(object):
    def minimumTime(self, grid):

        m = len(grid)
        n = len(grid[0])

        if grid[1][0] > 1 and grid[0][1] > 1:
            return -1
        
        f = [[None] * n for _ in range(m)]
        heap = [[0, 0, 0]]
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        while heap:
            nowt, nowx, nowy = heapq.heappop(heap)
            if f[nowx][nowy] is None:
                f[nowx][nowy] = nowt
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n and f[x][y] is None:
                        delta = (grid[x][y] % 2)^((x + y) % 2)
                        if grid[x][y] + delta <= nowt + 1:
                            heapq.heappush(heap, [nowt + 1, x, y])
                        else:
                            heapq.heappush(heap, [grid[x][y] + delta, x, y])
        

        return f[-1][-1]
''',
    call=f'Solution().minimumTime({G0})',
    expect=5,
    views=[
        dict(type='grid', var='grid', label='grid（每格 = 最早可进入时刻）', cursors=[('nowx', 'nowy', 'yellow')], h=170, cell=64),
        dict(type='table', var='f', label='f[i][j]：确定的最早到达时刻（None = 还没确定）', cursors=[('x', 'y', 'pink')], h=170, cell=64,
             color=lambda S, i, j, v: 'green' if v is not None else None),
        dict(type='heap', var='heap', fmt=lambda t: f'{t[0]}@({t[1]},{t[2]})', label='heap 最小堆（预计时刻@格子）', top_color='blue', h=130),
    ],
    watch=[('nowt', 'nowt', 'blue'), ('nowx', 'nowx'), ('nowy', 'nowy'), ('delta', 'delta', 'green')],
    skip=['m = len', 'n = len', 'dx = [', 'dy = [', 'for index in range(4)', 'x = nowx', 'y = nowy', 'while heap', 'if x >= 0 and x < m'],
    max_steps=90,
    captions={
        'if grid[1][0] > 1 and grid[0][1] > 1': lambda S, B, ret: (
            f'`grid[1][0] = {S.grid[1][0]}`、`grid[0][1] = {S.grid[0][1]}`：有一个 `≤ 1`，就能在起点和它之间==反复横跳==，一直等下去 → 必然有解'
            if not (S.grid[1][0] > 1 and S.grid[0][1] > 1) else '两个邻居都 `> 1`，第 1 秒必须移动却哪都去不了 → 无解 `-1`'),
        'f = [[None]': '`f[i][j]`：格子 `(i,j)` 最早可到达的时刻，`None` 表示还没确定',
        'heap = [[0, 0, 0]]': '堆里放 `[预计时刻, x, y]`，起点时刻 `0`',
        'heapq.heappop(heap)': '弹出预计时刻最小的：时刻 `{nowt}`，格子 `({nowx},{nowy})`',
        'if f[nowx][nowy] is None': lambda S, B, ret: (f'`f[{S.nowx}][{S.nowy}]` 还是 `None` → 它是第一次弹出，==时刻 {S.nowt} 就是最早=='
                                                       if S.f[S.nowx][S.nowy] is None else f'`({S.nowx},{S.nowy})` 已经确定过更早的时刻 → 跳过这条旧记录'),
        'f[nowx][nowy] = nowt': '确定 `f[{nowx}][{nowy}] = {nowt}`：贪心——堆顶最小，之后不可能更早',
        'delta = (grid[x][y] % 2)^((x + y) % 2)': '邻居 `({x},{y})`：`grid` 奇偶 `{grid[x][y] % 2}`，`x+y` 奇偶 `{(x + y) % 2}` → 异或得 `delta = {delta}`（不同奇偶就要多等 1 秒）',
        'if grid[x][y] + delta <= nowt + 1': lambda S, B, ret: (
            f'修正后最早开放 `{S.grid[S.x][S.y]} + {S.delta} = {S.grid[S.x][S.y] + S.delta}`，不超过 `nowt+1 = {S.nowt + 1}`：不用等，走过去，==时刻 nowt+1=='
            if S.grid[S.x][S.y] + S.delta <= S.nowt + 1 else
            f'修正后最早开放 `{S.grid[S.x][S.y] + S.delta}` > `nowt+1 = {S.nowt + 1}`：要先在旁边横跳等到开放'),
        'heapq.heappush(heap, [nowt + 1': '压入 `[{nowt + 1}, {x}, {y}]`：直接走过去，时刻 `nowt + 1`',
        'heapq.heappush(heap, [grid[x][y] + delta': '压入 `[{grid[x][y] + delta}, {x}, {y}]`：等到 `grid + delta` 才能进入',
        'return f[-1][-1]': '右下角的 `f` 就是答案：`{ret}`',
    },
    cards=dict(
        one_liner='能反复横跳就能等：贪心取最早时刻，奇偶不符的多等 1 秒',
        complexity='时间 `O(mn log mn)`，空间 `O(mn)`',
        problem=['`grid[i][j]` 是能进入该格的==最早时刻==，从左上角时刻 0 出发，每秒必须移动一格',
                 '求最早到达右下角的时刻，到不了返回 `-1`',
                 '本视频示例：`[[0,1,3],[5,4,2]]` → `5`'],
        quote='只要单元格(0, 1)和(1, 0)，有一个格子的最早可访问时间小于等于1，那么就必然可以到达矩阵右下角，反之就是无解，直接返回-1。',
        quote_src='—— yiduobo 题解原文',
        idea=['没规定不能走回头路 → 相邻格子间反复横跳 = 等待，只要起点能「动起来」就有解',
              '每秒必移动：到 `(x,y)` 的时刻奇偶性固定等于 `(x+y)` 的奇偶 → 不符的格子最早时刻 `+1`（`delta`）',
              '类 Dijkstra：堆顶最早的格子确定 `f`，邻居预计时刻 = `max(nowt+1, grid+delta)`'],
        summary=['时间 `O(mn log mn)`，空间 `O(mn)`',
                 '易错点：`delta` 用异或判断奇偶是否一致，一致为 0，不同为 1',
                 '易错点：同一个格子会被多次压堆，弹出时用 `f is None` 过滤旧记录',
                 '原文本身已是 Python 3 可运行的写法（用到 `heapq`，引擎已注入），代码未做修改',
                 '对比灵神：灵神把奇偶修正写成 `nd += (nd-x-y)%2`，并用 `dis` 数组松弛；这里是「弹出时才确定」的写法'],
    ),
)
