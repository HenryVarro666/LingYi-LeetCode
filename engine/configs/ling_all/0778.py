GRID = [[0, 3, 2], [1, 8, 4], [7, 6, 5]]


def _nb(S, B, ret):
    x, y = S.x, S.y
    if not (0 <= x < S.n and 0 <= y < S.n):
        return f'邻居 `({x},{y})` 越界，跳过'
    nd = max(S.d, S.grid[x][y])
    cur = S.dis[x][y]
    c = '∞' if cur == inf else cur
    if nd < cur:
        return f'邻居 `({x},{y})` 高度 `{S.grid[x][y]}`：`max({S.d}, {S.grid[x][y]}) = {nd}` < 旧值 `{c}` → ==更小，可以更新=='
    return f'邻居 `({x},{y})` 高度 `{S.grid[x][y]}`：`max({S.d}, {S.grid[x][y]}) = {nd}` >= 旧值 `{c}` → 不更新'


def _dcell(S, i, j, v):
    if 'h' not in S:
        return None
    return 'green' if v != inf else None


CONFIG = dict(
    num=778, title='水位上升的泳池中游泳', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='Dijkstra（+ 改成 max）',
    tags=['难度分 2097'],
    code='''
class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        dis = [[inf] * n for _ in range(n)]
        dis[0][0] = grid[0][0]
        h = [(grid[0][0], 0, 0)]  # 堆中保存 (起点到 (i,j) 的最少时间, i, j)

        while True:
            d, i, j = heappop(h)
            if i == j == n - 1:  # 到终点的最短路已确定
                return d
            if d > dis[i][j]:  # (i,j) 之前出堆过
                continue
            for x, y in (i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j):  # 顺序无所谓，我们只看堆中最小的
                if 0 <= x < n and 0 <= y < n:
                    new_dis = max(d, grid[x][y])
                    if new_dis < dis[x][y]:
                        dis[x][y] = new_dis  # 更新 (i,j) 的邻居的最短路
                        # 懒更新堆：只插入数据，不更新堆中数据
                        # 相同节点可能有多个不同的 new_dis，除了最小的 new_dis，其余值都会触发上面的 continue
                        heappush(h, (new_dis, x, y))
''',
    call=f'Solution().swimInWater({GRID})',
    expect=5,
    views=[
        dict(type='grid', var='grid', label='grid（平台高度；蓝框 = 刚出堆的格子，粉框 = 正在看的邻居）', cell=76, h=260,
             cursors=[('i', 'j', 'blue'), ('x if _line >= 15 and 0 <= x < n and 0 <= y < n else None', 'y', 'pink')]),
        dict(type='grid', var=lambda S: [[('∞' if v == inf else v) for v in r] for r in S['dis']] if 'dis' in S else None,
             label='dis（起点到该格路径上的最大高度；∞ = 还没到过）', cell=76, h=260,
             color=lambda S, i, j, v: 'green' if v != '∞' else None,
             cursors=[('i', 'j', 'blue')]),
        dict(type='heap', var='h', label='堆 h：(最大高度, i, j)，最小的先出', fmt=lambda t: f'{t[0]}@{t[1]},{t[2]}', h=170),
    ],
    watch=[('d', 'd', 'blue'), ('i', 'i'), ('j', 'j'), ('new_dis', 'new_dis', 'yellow')],
    skip=['n = len(grid)', 'dis = [[inf]', 'dis[0][0] = grid[0][0]', 'for x, y in', 'while True', 'new_dis = max', 'if new_dis < dis[x][y]'],
    captions={
        'h = [(grid[0][0]': '起点入堆：`dis[0][0] = {grid[0][0]}`，堆里存的是 ==路径上的最大高度==，不是路程和',
        'd, i, j = heappop(h)': '堆里最小的出堆：`({i},{j})`，到它路径最大高度 `d = {d}`',
        'if i == j == n - 1': lambda S, B, r: (f'`({S.i},{S.j})` 就是终点：它出堆时 `d` 已是最小 → 答案 =={S.d}==' if S.i == S.j == S.n - 1
                                               else f'`({S.i},{S.j})` 不是终点 `({S.n - 1},{S.n - 1})`，继续扩展'),
        'if d > dis[i][j]': lambda S, B, r: (f'`d = {S.d} > dis = {S.dis[S.i][S.j]}`：这是旧记录，==懒删除==，直接跳过' if S.d > S.dis[S.i][S.j]
                                             else f'`d = {S.d}` 等于 `dis[{S.i}][{S.j}]`：是最新的，往四周扩展'),
        'continue': '过期记录，丢掉',
        'if 0 <= x < n': _nb,
        'dis[x][y] = new_dis': '更新 `dis[{x}][{y}] = {new_dis}`：水位要同时淹没两格，所以取 `max`',
        'heappush(h, (new_dis, x, y))': '新记录入堆 `({new_dis}, {x}, {y})`：==只插入，不改堆里的旧数据==（懒更新）',
        'return d': '终点出堆，最少等待时间 `{d}`',
    },
    max_steps=130,
    cards=dict(
        one_liner='Dijkstra 把「路径和」换成「路径最大值」',
        complexity='时间 `O(n² log n)`，空间 `O(n²)`',
        problem=['`n × n` 的网格，`grid[i][j]` 是平台高度，时间 `t` 水位为 `t`',
                 '相邻两格都被水淹没才能游过去，从 `(0,0)` 游到 `(n-1,n-1)`',
                 '求最少需要等到的时间，也就是==路径上最大高度的最小值==',
                 '本视频：`[[0,3,2],[1,8,4],[7,6,5]]` → `5`'],
        quote='本题计算的不是路径边权和的最小值，而是路径点权最大值的最小值。把 Dijkstra 算法中的 + 改成 max 即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dis[i][j]` = 起点到 `(i,j)` 的路径中，最大高度的最小值',
              '松弛时把 `d + w` 换成 `max(d, grid[x][y])`',
              '==懒更新堆==：只插入新值，旧值出堆时用 `d > dis` 丢掉'],
        summary=['时间 `O(n² log n)`，空间 `O(n²)`',
                 '`max` 版 Dijkstra 的前提：路径值只增不减，所以第一次出堆就是最优',
                 '易错：终点出堆时才能返回，入堆时还不是最终值',
                 '另一种写法：二分答案 mx + DFS，判断只走 `<= mx` 的格子能否到终点',
                 '思考题：每走一步要 1 秒呢？需要同时记录时间和高度'],
    ),
)
