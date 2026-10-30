PEN = [[5, 3], [1, 4]]


def _dis(k):
    return lambda S: [[(c[k] if c[k] != float('inf') else '∞') for c in row] for row in S['dis']] if 'dis' in S else [[0]]


def _hfmt(t):
    return f'{t[0]}@({t[1]},{t[2]}) k{t[3]}'


CONFIG = dict(
    num=4003, title='交替方向的最小路径代价 III', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='分层 Dijkstra（状态含行动编号奇偶）',
    tags=[],
    code='''
# 奇数下标 1,3 对应向右或向下
# 偶数下标 0,2 对应向左或向上
DIRS = (0, -1), (0, 1), (-1, 0), (1, 0)

class Solution:
    def minCost(self, m: int, n: int, penalty: list[list[int]]) -> int:
        dis = [[[inf] * 2 for _ in range(n)] for _ in range(m)]

        # 支付 1 的入口代价
        dis[0][0][1] = 1
        h = [(1, 0, 0, 1)]  # (dis, x, y, k)

        while True:
            d, i, j, k = heappop(h)
            if i == m - 1 and j == n - 1:
                return d
            if d > dis[i][j][k]:
                continue
            p = penalty[i][j]

            # 原地不动
            new_dis = d + p
            if new_dis < dis[i][j][k ^ 1]:
                dis[i][j][k ^ 1] = new_dis
                heappush(h, (new_dis, i, j, k ^ 1))  # k^1 切换行动编号的奇偶性

            # 移动一步
            for idx, (dx, dy) in enumerate(DIRS):
                x, y = i + dx, j + dy
                if 0 <= x < m and 0 <= y < n:
                    # 如果 k 和 idx 的奇偶性不同，那么违反了奇偶性规则，需要额外支付 p 的代价
                    new_dis = d + (x + 1) * (y + 1) + (idx % 2 ^ k) * p
                    if new_dis < dis[x][y][k ^ 1]:
                        dis[x][y][k ^ 1] = new_dis
                        heappush(h, (new_dis, x, y, k ^ 1))  # k^1 切换行动编号的奇偶性
''',
    call=f'Solution().minCost(2, 2, {PEN})',
    expect=8,
    views=[
        dict(type='table', var=_dis(1), label='dis[x][y][1]：下一步是奇数行动（右/下）', cell=90, h=150,
             cursors=[('i', 'j', 'yellow')]),
        dict(type='table', var=_dis(0), label='dis[x][y][0]：下一步是偶数行动（左/上）', cell=90, h=150,
             cursors=[('i', 'j', 'yellow')]),
        dict(type='heap', var='h', label='堆 h：(dis, x, y, k)', fmt=_hfmt, top_color='blue', h=150),
        dict(type='text', size=30, h=70, fn=lambda S: (
            f"取出 `({S['i']},{S['j']})`，k=`{S['k']}`，已付 `{S['d']}`，penalty=`{PEN[S['i']][S['j']]}`" if 'k' in S and 'i' in S and 'd' in S else '')),
    ],
    watch=['d', 'i', 'j', 'k', 'new_dis', 'x', 'y'],
    captions={
        'dis = [[[inf]': '`dis[x][y][k]`：到格子 `(x,y)` 且==下一次行动编号奇偶性为 k==的最小代价，初始全是 ∞',
        'dis[0][0][1] = 1': '起点 `(0,0)` 要先付入口代价 `1`；下一次是行动 1（奇数），所以 `k = 1`',
        'h = [(1, 0, 0, 1)]': '堆里放 `(代价, x, y, k)`，Dijkstra 每次取代价最小的状态',
        'd, i, j, k = heappop': '取出代价最小的状态：`({i},{j})`，`k={k}`，代价 `{d}`',
        'if i == m - 1 and j == n - 1': '到终点了吗？`({i},{j})` vs `({m-1},{n-1})` → {"是，此时 d 就是最小代价" if i == m-1 and j == n-1 else "不是，继续扩展"}',
        'return d': '第一次弹出终点，代价最小：返回 =={ret}==',
        'if d > dis[i][j][k]': '`d = {d}`，已记录 `dis = {dis[i][j][k]}` → {"这是过期的旧状态，跳过" if d > dis[i][j][k] else "不过期，继续扩展"}',
        'p = penalty': '本格惩罚 `p = penalty[{i}][{j}] = {p}`（等待或违规都要付）',
        'new_dis = d + p': '原地等待：付 `p = {p}`，代价 `{d} + {p} = {new_dis}`，行动编号奇偶翻转',
        'if new_dis < dis[i][j][k ^ 1]': '`{new_dis}` 比 `dis[{i}][{j}][{k^1}] = {dis[i][j][k^1]}` {"更小 → 更新并入堆" if new_dis < dis[i][j][k^1] else "不更小 → 不更新"}',
        'for idx, (dx, dy)': '枚举四个方向：`idx` 0/2 是左/上（偶数行动），1/3 是右/下（奇数行动）',
        'x, y = i + dx': '尝试走到 `({x},{y})`',
        'if 0 <= x < m': '`({x},{y})` {"在网格内" if 0 <= x < m and 0 <= y < n else "越界，跳过"}',
        'new_dis = d + (x + 1)': '移动代价 = 入口 `{(x+1)*(y+1)}` + ({idx%2^k}) × p；`idx%2 ^ k = {idx%2^k}`：{"方向与行动奇偶不符，违规要加 p=" + str(p) if idx%2^k else "遵守规则，不加惩罚"} → `{new_dis}`',
        'if new_dis < dis[x][y][k ^ 1]': '`{new_dis}` vs `dis[{x}][{y}][{k^1}] = {dis[x][y][k^1]}` → {"更小，更新并入堆" if new_dis < dis[x][y][k^1] else "不更小，放弃"}',
        'dis[i][j][k ^ 1] = new_dis': '`dis[{i}][{j}][{k^1}]` 改为 `{new_dis}`',
        'dis[x][y][k ^ 1] = new_dis': '`dis[{x}][{y}][{k^1}]` 改为 `{new_dis}`',
    },
    skip=['DIRS =', 'x, y = i + dx', 'while True', 'for idx, (dx, dy)', 'p = penalty', 'if 0 <= x < m', 'dis[x][y][k ^ 1] = new_dis', 'dis[i][j][k ^ 1] = new_dis'],
    max_steps=48,
    cards=dict(
        one_liner='在 Dijkstra 状态里加一维：行动编号的奇偶 k',
        complexity='时间 `O(mn log(mn))`，空间 `O(mn)`',
        problem=['网格 `m×n` 从 `(0,0)` 走到 `(m-1,n-1)`，进入 `(i,j)` 付 `(i+1)(j+1)`，起点也要付',
                 '奇数行动应向右/下，偶数行动向左/上；违规多付移动前格子的 `penalty`；原地等待付 `penalty`',
                 '示例：`m=2, n=2, penalty=[[5,3],[1,4]]` → `8`'],
        quote='本题可以上下左右走，是个有环图，求最短路长度可以用 Dijkstra 算法。在标准 Dijkstra 算法的基础上，额外添加参数 k，表示当前行动编号的奇偶性。',
        quote_src='—— 灵茶山艾府题解',
        idea=['状态 `(x, y, k)`，`dis[x][y][k]` 是到达它的最小代价',
              '每次行动后 `k ^ 1` 翻转奇偶；方向下标 `idx` 的奇偶与 `k` 不同就违规，多付 `p`',
              '原地等待也是一条边，权为 `p`，只翻转 `k`'],
        summary=['时间 `O(mn log(mn))`，空间 `O(mn)`',
                 '起点代价是 `1`，且下一次行动是奇数：`dis[0][0][1] = 1`',
                 '答案：第一次弹出终点就返回，不必区分 `k`',
                 '不能只往右下走：有 `penalty` 很大的格子相当于墙，必须考虑四个方向'],
    ),
)
