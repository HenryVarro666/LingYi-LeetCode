N = 5
EDGES = [[1, 2, 1], [1, 3, 3], [1, 4, 5], [2, 3, 2], [3, 4, 2], [4, 0, 1]]
POS = {0: (0.92, 0.55), 4: (0.68, 0.55), 3: (0.40, 0.88), 2: (0.40, 0.12), 1: (0.08, 0.55)}
FRAC = {(1, 4): 0.2, (2, 3): 0.3}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '原图（箭头 = 原方向；搜索从 0 出发沿箭头反着走；蓝 = 刚出堆，粉 = 正在看的边）', 20, T['muted'], bold=True)
    W, H = x1 - x0 - 120, y1 - y0 - 110
    ox, oy = x0 + 60, y0 + 60

    def P(k):
        return ox + POS[k][0] * W, oy + POS[k][1] * H

    line = S.get('_line', 0)
    dis = S.get('dis')
    cur = S.get('x') if line >= 14 and 'h' in S else None
    hot = None
    if line >= 18 and 'y' in S and 'x' in S and 'w' in S and 'dis' in S:
        hot = (S['y'], S['x'])           # 原图中的边 y -> x
    R = 30
    for a, b, w in EDGES:
        (ax, ay), (bx, by) = P(a), P(b)
        dx, dy = bx - ax, by - ay
        L = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / L, dy / L
        p0 = (ax + ux * R, ay + uy * R)
        p1 = (bx - ux * (R + 4), by - uy * (R + 4))
        c = T['border']
        wd = 3
        if hot == (a, b):
            c, wd = T['pink'], 6
        elif dis is not None and dis[a] != inf and dis[b] != inf and False:
            c = T['muted']
        cv.arrow(p0, p1, c, width=wd, head=14)
        f = FRAC.get((a, b), 0.5)
        mx, my = p0[0] + (p1[0] - p0[0]) * f - uy * 16, p0[1] + (p1[1] - p0[1]) * f + ux * 16
        cv.text((mx, my), w, 22, T['pink'] if hot == (a, b) else T['yellow'], anchor='mm', bold=True)
    for k in range(N):
        X, Y = P(k)
        fill = T['panel2']
        if dis is not None and dis[k] != inf:
            fill = T['green']
        cv.rect((X - R, Y - R, X + R, Y + R), fill=fill, r=R, outline=T['border'])
        if cur == k:
            cv.rect((X - R - 5, Y - R - 5, X + R + 5, Y + R + 5), outline=T['blue'], width=5, r=R + 5)
        cv.text((X, Y), k, 28, T['bg'] if fill == T['green'] else T['text'], anchor='mm', bold=True)
        if dis is not None:
            cv.text((X, Y + R + 6), '∞' if dis[k] == inf else f'd={dis[k]}', 20, T['green'] if dis[k] != inf else T['dim'], anchor='mt', bold=True)


def _X(S):
    return S.get('x') if S.get('_line', 0) >= 14 and 'h' in S else None


CONFIG = dict(
    num=3419, title='图的最大边权的最小值', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='反向建图 + Dijkstra（+ 改成 max）',
    tags=['难度分 2243'],
    code='''
class Solution:
    def minMaxWeight(self, n: int, edges: List[List[int]], _: int) -> int:
        if len(edges) < n - 1:
            return -1

        g = [[] for _ in range(n)]
        for x, y, w in edges:
            g[y].append((x, w))

        dis = [inf] * n
        dis[0] = 0
        h = [(0, 0)]  # (路径最大边权, 节点编号)
        while h:
            d, x = heappop(h)
            if d > dis[x]:
                continue
            for y, w in g[x]:
                new_d = max(d, w)
                if new_d < dis[y]:
                    dis[y] = new_d
                    heappush(h, (new_d, y))

        ans = max(dis)
        return -1 if ans == inf else ans
''',
    call=f'Solution().minMaxWeight({N}, {EDGES}, 1)',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var=lambda S: ['∞' if v == inf else v for v in S['dis']] if 'dis' in S else None,
             label='dis（0 到各点路径最大边权的最小值）', cell=84, h=150, pointers={_X: 'blue'},
             pointer_labels={_X: 'x'},
             color=lambda S, i, v: 'green' if v != '∞' else None),
        dict(type='heap', var='h', label='堆 h：(路径最大边权, 节点)', fmt=lambda t: f'{t[0]}@{t[1]}', h=130),
    ],
    watch=[('d', 'd', 'blue'), ('x', 'x'), ('y', 'y', 'pink'), ('w', 'w', 'yellow'), ('new_d', 'new_d', 'green')],
    skip=['for x, y, w in edges', 'for y, w in g[x]', 'g = [[]', 'dis = [inf]', 'ans = max(dis)'],
    captions={
        'if len(edges) < n - 1': '`n = {n}` 个点要连成一棵树至少 `n−1 = {n - 1}` 条边；现有 `{len(edges)}` 条，够用',
        'g[y].append': '原图边 `{x}→{y}`（权 `{w}`）==反向==：`g[{y}]` 里加 `({x}, {w})`',
        'dis[0] = 0': '起点 0 到自己：路径上没有边，最大边权 `dis[0] = 0`',
        'h = [(0, 0)]': '起点入堆 `(0, 0)`',
        'while h': lambda S, B, r: ('堆不空，继续取最小的' if S.h else '堆空了：所有能到的点都定下了'),
        'd, x = heappop(h)': '堆里==最大边权最小==的出堆：节点 `{x}`，`d = {d}`',
        'if d > dis[x]': lambda S, B, r: (f'`d = {S.d} > dis[{S.x}] = {S.dis[S.x]}`：过期记录，==跳过==' if S.d > S.dis[S.x]
                                          else f'`d = {S.d}` 就是 `dis[{S.x}]`，从节点 {S.x} 往外扩展'),
        'continue': '过期记录（同一节点之前已经用更小的值出堆）→ 丢掉',
        'new_d = max(d, w)': '走反向边 `{x}→{y}`（原图 `{y}→{x}`，权 `{w}`）：路径最大边权 `max({d}, {w}) = {new_d}`',
        'if new_d < dis[y]': lambda S, B, r: (f'`{S.new_d} < {"∞" if S.dis[S.y] == inf else S.dis[S.y]}` → 找到更优的路，更新' if S.new_d < S.dis[S.y]
                                              else f'`{S.new_d}` 不比 `dis[{S.y}] = {S.dis[S.y]}` 小 → 不更新'),
        'dis[y] = new_d': '`dis[{y}] = {new_d}`',
        'heappush': '`({new_d}, {y})` 入堆（懒更新：旧记录留着，出堆时再丢）',
        'return -1 if ans == inf': lambda S, B, r: f'`ans = max(dis) = {max(S.dis)}`：最大的那个点决定答案 → ==返回 {r}==',
    },
    max_steps=130,
    cards=dict(
        one_liner='边反向后，从 0 出发做 max 版 Dijkstra，答案是 max(dis)',
        complexity='时间 `O(m log m)`，空间 `O(m)`',
        problem=['有向带权图，删一些边，使所有点都能到达 0',
                 '并且剩余边的==最大边权尽量小==，每个点出边至多 `threshold` 条',
                 '无解返回 `-1`；示例：`n = 5`，6 条边 → `2`'],
        quote='把图中的每条边反向，那么原问题等价于删边之后：从 0 出发，必须能访问到所有点。每个点的入度至多为 threshold。所以 threshold 是多余的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['反向后从 0 出发的 DFS 树里，每个点入度恰好为 1，==threshold 自动满足==',
              '要让所有点可达，且最大边权最小 → 到每个点的「路径最大边权」取最小',
              '这就是 Dijkstra 把 `+` 改成 `max`，答案 = `max(dis)`'],
        summary=['时间 `O(m log m)`，空间 `O(m)`',
                 '边数 `< n−1` 一定连不通，先返回 `-1`；`dis` 里还有 `inf` 同样返回 `-1`',
                 '易错：必须反向建图；只用 DFS 优先走小边会有反例',
                 '另一种写法：二分上限 `upper` + DFS，看只走 `w <= upper` 的边能否访问所有点',
                 '同类题：1631 最小体力消耗路径、778 水位上升的泳池中游泳'],
    ),
)
