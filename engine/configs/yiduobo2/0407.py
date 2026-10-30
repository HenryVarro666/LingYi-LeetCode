import heapq as _hq

H = [[1, 4, 3, 1, 3, 2], [3, 2, 1, 3, 2, 4], [2, 3, 3, 2, 3, 1]]
M, N = len(H), len(H[0])
CORNERS = {(0, 0), (0, N - 1), (M - 1, 0), (M - 1, N - 1)}


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


def _heapset(S):
    return {(e[0], e[1][0], e[1][1]) for e in S.get('heap') or []}


def _inheap(S):
    return {(x, y) for _, x, y in _heapset(S)}


def _used(S, i, j):
    u = S.get('used')
    return u is not None and u[i][j]


def _color(S, i, j, v):
    if (i, j) in CORNERS:
        return None
    if (i, j) in _inheap(S):
        return 'orange'
    if _used(S, i, j):
        return None
    return 'blue'


def _water_grid(S):
    if 'res' not in S:
        return None
    return [[(WATER[i][j] if _used(S, i, j) and 0 < i < M - 1 and 0 < j < N - 1 else '')
             for j in range(N)] for i in range(M)]


def _cap_pop(S, B, ret):
    hgt = S.now_height
    x0, y0 = S.pos
    u = B.used
    new = [(x0 + dx, y0 + dy) for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0))
           if 0 < x0 + dx < M - 1 and 0 < y0 + dy < N - 1 and not u[x0 + dx][y0 + dy]]
    head = f'取出==最矮的边界== `({x0},{y0})`，高 `{hgt}`'
    if not new:
        return head + '：相邻的内部格子都考察过了'
    xs = '、'.join(f'`({x},{y})`' for x, y in new)
    return head + f'：考察相邻且没考察过的 {xs}'


def _cap_cmp(S, B, ret):
    hgt, x, y = S.now_height, S.x, S.y
    hv = H[x][y]
    if hgt > hv:
        return f'`({x},{y})` 高 `{hv}` 比边界 `{hgt}` 矮 → ==能储水=='
    return f'`({x},{y})` 高 `{hv}` ≥ 边界 `{hgt}` → 储不了水'


CONFIG = dict(
    num=407, title='接雨水 II', difficulty='Hard', category='堆',
    author='yiduobo', technique='堆 · 总是先考察最矮的边界',
    tags=['字节30天'],
    code='''
import heapq

class Solution(object):
    def trapRainWater(self, heightMap):

        if len(heightMap) <= 2:
            return 0

        if len(heightMap[0]) <= 2:
            return 0

        m = len(heightMap)
        n = len(heightMap[0])

        used = [[False] * n for _ in range(m)]
        heap = []
        for index in range(1, m - 1):
            heap.append([heightMap[index][0], [index, 0]])
            used[index][0] = True
            heap.append([heightMap[index][n - 1], [index, n - 1]])
            used[index][n - 1] = True

        for index in range(1, n - 1):
            heap.append([heightMap[0][index], [0, index]])
            used[0][index] = True
            heap.append([heightMap[m - 1][index], [m - 1, index]])
            used[m - 1][index] = True

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        res = 0
        heapq.heapify(heap)
        while heap:
            now_height, pos = heapq.heappop(heap)
            nowx, nowy = pos
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x > 0 and x < m - 1 and y > 0 and y < n - 1 and not used[x][y]:
                    if now_height > heightMap[x][y]:
                        res += now_height - heightMap[x][y]
                        heapq.heappush(heap, [now_height, [x, y]])
                    else:
                        heapq.heappush(heap, [heightMap[x][y], [x, y]])
                    used[x][y] = True
        return res
''',
    call=f'Solution().trapRainWater({H})',
    expect=4,
    skip=[6, 9, 18, 19, 20, 21, 24, 25, 26, 27, 29, 30, 34, 36, 37, 38, 39, 40, 46],
    views=[
        dict(type='grid', var=lambda S: H, label='heightMap（橙 = 当前边界，蓝 = 还没考察的内部格，四个角用不到）', h=260, cell=70,
             color=_color,
             cursors=[('pos[0] if _line >= 35 else None', 'pos[1]', 'yellow'),
                      ('x if _line in (41, 42, 43, 45) else None', 'y', 'pink')]),
        dict(type='grid', var=_water_grid, label='内部格子的储水量', h=230, cell=62,
             color=lambda S, i, j, v: 'cyan' if isinstance(v, int) and v > 0 else None),
        dict(type='set', var=lambda S: _heapset(S) if 'heap' in S and S.get('_line', 0) >= 33 else None,
             label='heap 里的边界 高度@行,列（从小到大，第一个 = 最矮的边界）', fmt=lambda t: f'{t[0]}@{t[1]},{t[2]}',
             font=22, h=130),
    ],
    watch=[('now_height', 'now_height', 'yellow'), ('pos', 'pos', 'yellow'), ('(x, y)', '(x, y)', 'pink'),
           ('res', 'res', 'green')],
    captions={
        'm = len(heightMap)': '`m = {m}`；行数或列数 ≤ 2 时根本没有内部格子，直接返回 0',
        'n = len(heightMap[0])': '`n = {n}`',
        'used = [[False]': '`used[x][y]`：这个格子是否已经考察过',
        'heap = []': '初始的边界就是==最外围的这一圈柱子==（四个角不和内部相邻，不用放）',
        17: lambda S, B, r: (f'第 `{S.index}` 行的左右两端入堆' if len(S.heap) < 2 * (M - 2) else '左右两列放好了'),
        23: lambda S, B, r: (f'第 `{S.index}` 列的上下两端入堆' if len(S.heap) < 2 * (M - 2) + 2 * (N - 2) else '上下两行也放好了：初始边界就绪'),
        'res = 0': '`res` 累计储水量',
        'heapq.heapify(heap)': '堆化：每次弹出==最矮的边界==',
        'now_height, pos = heapq.heappop': _cap_pop,
        'if now_height > heightMap[x][y]': _cap_cmp,
        'res += now_height': '储水 `{now_height} − {heightMap[x][y]} = {now_height - heightMap[x][y]}`，`res = {res}`',
        43: '`({x},{y})` 成为新的边界，高度取==边界与格子的较大值== `{now_height}`',
        45: '`({x},{y})` 成为新的边界，高度就是它自己 `{heightMap[x][y]}`',
        'return res': '所有格子都考察完 → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='不考察最矮的格子，而是考察最矮的边界',
        complexity='时间 `O(mn log(mn))`，空间 `O(mn)`',
        problem=['`m × n` 的矩阵是二维高度图，求下雨后最多能接多少体积的雨水',
                 '示例：`[[1,4,3,1,3,2],[3,2,1,3,2,4],[2,3,3,2,3,1]]` → `4`',
                 '（接水 `1 + 2 + 1 = 4`）'],
        quote='若这个边界相邻的格子并没有被考察过，且高度比边界要矮，那么这个相邻格子就能储水。……这个格子就可以作为新的边界加入到边界中，而==高度则应该取边界以及当前格子高度的较大值==。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一种想法：反复找最矮区域、填到周围最矮的墙，最坏 `O((mn)^2)`，太慢',
              '转换思路：初始边界 = 最外一圈，==优先考察最矮的边界==',
              '每个格子只算一次，用堆找最矮 → `O(mn log(mn))`'],
        summary=['时间 `O(mn log(mn))`，空间 `O(mn)`（`used` + 堆）',
                 '新边界高度 = `max(边界高, 格子高)`：矮格子灌满水后就和边界一样高',
                 '细节：四个角不入堆，邻居只考察 ==内部格子==；行或列 ≤ 2 直接返回 0',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改',
                 '对比灵神：思路相同；灵神用“木桶短板”比喻，并把访问过的格子原地改成 -1'],
    ),
)
