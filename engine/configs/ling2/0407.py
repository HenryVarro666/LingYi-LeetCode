import heapq as _hq

H = [[1, 4, 3, 1, 3, 2], [3, 2, 1, 3, 2, 4], [2, 3, 3, 2, 3, 1]]
M, N = len(H), len(H[0])


def _final_water():
    vis = [[False] * N for _ in range(M)]
    hp = []
    for i in range(M):
        for j in range(N):
            if i in (0, M - 1) or j in (0, N - 1):
                hp.append((H[i][j], i, j))
                vis[i][j] = True
    _hq.heapify(hp)
    w = [[0] * N for _ in range(M)]
    while hp:
        mh, i, j = _hq.heappop(hp)
        for x, y in (i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j):
            if 0 <= x < M and 0 <= y < N and not vis[x][y]:
                w[x][y] = max(mh - H[x][y], 0)
                _hq.heappush(hp, (max(mh, H[x][y]), x, y))
                vis[x][y] = True
    return w


WATER = _final_water()


def _inheap(S):
    return {(x, y) for _, x, y in S.get('h') or []}


def _visited(S, i, j):
    g = S.get('heightMap')
    return g is not None and g[i][j] == -1


def _color(S, i, j, v):
    if (i, j) in _inheap(S):
        return 'orange'
    if _visited(S, i, j):
        return None
    return 'blue'


def _water_grid(S):
    if 'ans' not in S:
        return None
    return [[(WATER[i][j] if _visited(S, i, j) and 0 < i < M - 1 and 0 < j < N - 1 else '')
             for j in range(N)] for i in range(M)]


def _cap_pop(S, B, ret):
    mh, i, j = S.min_height, S.i, S.j
    g = B.heightMap
    new = [(x, y) for x, y in ((i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j))
           if 0 <= x < M and 0 <= y < N and g[x][y] >= 0]
    head = f'弹出最短的木板 `({i},{j})`，高 `{mh}`'
    if not new:
        return head + '：邻居都访问过了，直接去掉这块木板'
    xs = '、'.join(f'`({x},{y})`' for x, y in new)
    return head + f'：邻居 {xs} 的水位就是 =={mh}==（再高会从这块短板流出去）'


def _cap_ans(S, B, ret):
    mh, x, y = S.min_height, S.x, S.y
    hv = H[x][y]
    if mh > hv:
        return f'`({x},{y})` 高 `{hv}` < 短板 `{mh}` → 接水 `{mh} − {hv}` = =={mh - hv}==，`ans = {S.ans}`'
    return f'`({x},{y})` 高 `{hv}` ≥ 短板 `{mh}` → 接不了水'


def _cap_push(S, B, ret):
    mh, x, y = S.min_height, S.x, S.y
    hv = H[x][y]
    if mh > hv:
        return f'把 `({x},{y})` 填上==水泥==到高 `{mh}`，作为新木板入堆，替换掉 `({S.i},{S.j})`'
    return f'`({x},{y})` 本身高 `{hv}`，作为新木板入堆，替换掉 `({S.i},{S.j})`'


CONFIG = dict(
    num=407, title='接雨水 II', difficulty='Hard', category='堆',
    author='灵茶山艾府', technique='最小堆 · 木桶短板效应',
    tags=['字节30天'],
    code='''
class Solution:
    def trapRainWater(self, heightMap: List[List[int]]) -> int:
        m, n = len(heightMap), len(heightMap[0])
        h = []
        for i, row in enumerate(heightMap):
            for j, height in enumerate(row):
                if i == 0 or i == m - 1 or j == 0 or j == n - 1:
                    h.append((height, i, j))
                    row[j] = -1  # 标记 (i,j) 访问过
        heapify(h)

        ans = 0
        while h:
            min_height, i, j = heappop(h)  # min_height 是木桶的短板
            for x, y in (i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j):
                if 0 <= x < m and 0 <= y < n and heightMap[x][y] >= 0:  # (x,y) 没有访问过
                    # 如果 (x,y) 的高度小于 min_height，那么接水量为 min_height - heightMap[x][y]
                    ans += max(min_height - heightMap[x][y], 0)
                    # 给木桶新增一块高为 max(min_height, heightMap[x][y]) 的木板
                    heappush(h, (max(min_height, heightMap[x][y]), x, y))
                    heightMap[x][y] = -1  # 标记 (x,y) 访问过
        return ans
''',
    call=f'Solution().trapRainWater({H})',
    expect=4,
    skip=[6, 7, 8, 9, 13, 15, 16, 21],
    views=[
        dict(type='grid', var=lambda S: H, label='高度图（橙 = 木桶当前的木板，蓝 = 还没访问，暗 = 已确定）', h=260, cell=70,
             color=_color,
             cursors=[('i if _line >= 14 else None', 'j', 'yellow'), ('x if _line in (18, 20) else None', 'y', 'pink')]),
        dict(type='grid', var=_water_grid, label='每格接水量（访问到时就确定了）', h=230, cell=62,
             color=lambda S, i, j, v: 'cyan' if isinstance(v, int) and v > 0 else None),
        dict(type='set', var=lambda S: set(S['h']) if 'h' in S and S.get('_line', 0) >= 10 else None,
             label='最小堆里的木板 高度@行,列（从小到大，第一个 = 堆顶 = 最短木板）', fmt=lambda t: f'{t[0]}@{t[1]},{t[2]}',
             font=22, h=130),
    ],
    watch=[('min_height', 'min_height', 'yellow'), ('(i, j)', '(i, j)', 'yellow'), ('(x, y)', '(x, y)', 'pink'),
           ('ans', 'ans', 'green')],
    captions={
        'm, n = len': '`m = {m}` 行，`n = {n}` 列',
        'h = []': '最外面一圈格子==接不了水==，它们是木桶最初的木板',
        'for i, row in enumerate': lambda S, B, r: (f'第 `{S.i}` 行：属于最外圈的格子 `(高度, i, j)` 入堆，并标记 -1 表示访问过'
                                                    if S.get('i') != B.get('i') else '最外一圈都进了堆'),
        'heapify(h)': '堆化：每次都能 `O(log)` 取出==最短的木板==',
        'ans = 0': '`ans` 累计接水量',
        'min_height, i, j = heappop': _cap_pop,
        'ans += max(': _cap_ans,
        'heappush(h, (max(': _cap_push,
        'return ans': '堆空了：每个格子都确定了水位 → 总接水量 =={ret}==',
    },
    cards=dict(
        one_liner='把最外圈当木桶，每次从最短的木板往里灌水',
        complexity='时间 `O(mn log(mn))`，空间 `O(mn)`',
        problem=['`m × n` 的矩阵是二维高度图，求下雨后最多能接多少体积的雨水',
                 '示例：`[[1,4,3,1,3,2],[3,2,1,3,2,4],[2,3,3,2,3,1]]` → `4`',
                 '（蓝色方块接水 `1 + 2 + 1 = 4`）'],
        quote='继续，从当前木板中，==找到一根最短的木板==。……由于每次都要找最短的木板，所以用一个==最小堆==维护木板的高度。',
        quote_src='—— 灵茶山艾府题解',
        idea=['最外面一圈接不了水，视作==木桶的木板==',
              '最短木板的邻居：水位不能超过它（会流出去），也一定能达到它（其它木板更高）',
              '邻居矮就灌==水泥==到短板高度，替换成新木板；用最小堆每次取最短'],
        summary=['时间 `O(mn log(mn))`：每个格子进出堆各一次',
                 '和 42 题双指针的联系：42 维护左右两个指针，本题维护==一圈指针==',
                 '易错：入堆高度是 `max(min_height, 高度)`，不是原高度',
                 '写法二只遍历最外一圈初始化，避免扫描整个矩阵'],
    ),
)
