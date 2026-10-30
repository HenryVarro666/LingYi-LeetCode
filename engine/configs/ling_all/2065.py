import math

_POS = {0: (0.14, 0.5), 1: (0.45, 0.0), 3: (0.45, 1.0), 2: (0.82, 0.0)}
_EDGES = [(0, 1, 10), (1, 2, 15), (0, 3, 10)]
_VALUES = [0, 32, 10, 43]


def _graph(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 2), '绿 = 价值已算入（即 vis 为 True）　蓝圈 = 当前点　边上 = 耗时', 22, T['muted'], bold=True)
    W, Hh = x1 - x0 - 120, y1 - y0 - 200
    pt = {k: (x0 + 60 + p[0] * W, y0 + 75 + p[1] * Hh) for k, p in _POS.items()}
    inn = S.get('_inner', {})
    cur = inn.get('x') if 'dfs' in S.get('_stack', ['dfs']) or True else None
    vis = S.get('vis')
    dis = S.get('dis')
    for a, b, t in _EDGES:
        (ax, ay), (bx, by) = pt[a], pt[b]
        hot = cur in (a, b) and 'y' in inn and inn.get('y') in (a, b) and inn.get('y') != cur
        cv.line([(ax, ay), (bx, by)], T['yellow'] if hot else T['dim'], 5 if hot else 3)
        mx, my = (ax + bx) / 2, (ay + by) / 2
        cv.rect((mx - 24, my - 16, mx + 24, my + 16), fill=T['panel'], r=8)
        cv.text((mx, my), t, 24, T['text'], anchor='mm', bold=True)
    for k, (px, py) in pt.items():
        col = T['panel2']
        out = T['border']
        if vis is not None and vis[k]:
            col, out = T['green'], T['green']
        if k == cur:
            out = T['blue']
        cv.d.ellipse((px - 34, py - 34, px + 34, py + 34), fill=col, outline=out, width=6 if k == cur else 3)
        cv.text((px, py), k, 34, T['bg'] if (vis is not None and vis[k]) else T['text'], anchor='mm', bold=True)
        cv.text((px, py + 52), f'价值 {_VALUES[k]}', 22, T['muted'], anchor='mm')
        if dis is not None and dis[k] != float('inf'):
            cv.text((px, py + 78), f'回0最短 {dis[k]}', 22, T['cyan'], anchor='mm')


def _info(S):
    inn = S.get('_inner', {})
    if 'sum_time' in inn:
        return (f"当前点 `{inn['x']}`，已用时间 ==`{inn['sum_time']}`== / {S['max_time']}，"
                f"路径价值 ==`{inn['sum_value']}`==，最佳答案 `{S.get('ans', '-')}`")
    return '先用 Dijkstra 求每个点回到 0 的最短时间，再暴搜'


CONFIG = dict(
    num=2065, title='最大化一张图中的路径价值', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='暴搜 + Dijkstra 最短路剪枝',
    tags=['灵神题单·图论算法', '难度分 2178'],
    code='''
class Solution:
    def maximalPathQuality(self, values: List[int], edges: List[List[int]], max_time: int) -> int:
        n = len(values)
        g = [[] for _ in range(n)]
        for x, y, t in edges:
            g[x].append((y, t))
            g[y].append((x, t))

        # Dijkstra 算法
        dis = [inf] * n
        dis[0] = 0
        h = [(0, 0)]
        while h:
            dx, x = heappop(h)
            if dx > dis[x]:  # x 之前出堆过
                continue
            for y, d in g[x]:
                new_dis = dx + d
                if new_dis < dis[y]:
                    dis[y] = new_dis  # 更新 x 的邻居的最短路
                    heappush(h, (new_dis, y))

        def dfs(x: int, sum_time: int, sum_value: int) -> None:
            if x == 0:
                nonlocal ans
                ans = max(ans, sum_value)
                # 注意这里没有 return，还可以继续走
            for y, t in g[x]:
                # 相比方法一，这里多了 dis[y]
                if sum_time + t + dis[y] > max_time:
                    continue
                if vis[y]:
                    dfs(y, sum_time + t, sum_value)
                else:
                    vis[y] = True
                    # 每个节点的价值至多算入价值总和中一次
                    dfs(y, sum_time + t, sum_value + values[y])
                    vis[y] = False  # 恢复现场

        ans = 0
        vis = [False] * n
        vis[0] = True
        dfs(0, 0, values[0])
        return ans
''',
    call='Solution().maximalPathQuality([0, 32, 10, 43], [[0, 1, 10], [1, 2, 15], [0, 3, 10]], 40)',
    expect=75,
    views=[
        dict(type='custom', draw=_graph, h=460),
        dict(type='text', fn=_info, size=24, h=60),
        dict(type='calls', h=170),
    ],
    watch=['ans', ('x', lambda S: S['_inner'].get('x'), 'blue'), ('dis', 'dis', 'cyan')],
    skip=['n = len(values)', 'g = [[] for', 'for x, y, t in edges', 'g[x].append', 'g[y].append', 'h = [(0, 0)]',
          'while h:', 'for y, d in g[x]', 'new_dis = dx + d', 'for y, t in g[x]', '                continue',
          'ans = 0', 'if vis[y]', 'vis[y] = True', 'heappush', 'dis[y] = new_dis'],
    captions={
        'dis = [inf]': '`dis[i]` = 起点 0 到 i 的最短时间，先全设为 ∞',
        'dis[0] = 0': '起点 0 到自己的时间是 `0`，堆里放入 `(0, 0)`',
        'dx, x = heappop': '堆顶出堆：离 0 最近的点 `{x}`，距离 `{dx}`',
        'if dx > dis[x]': lambda S, B, r: (f'`dx = {S.dx} > dis[{S.x}] = {S.dis[S.x]}` → 这是旧记录，==跳过=='
                                           if S.dx > S.dis[S.x] else f'`dx = {S.dx}` 就是 `dis[{S.x}]` → 第一次出堆，用它去松弛邻居'),
        'if new_dis < dis[y]': lambda S, B, r: (f'经 `{S.x}` 走到 `{S.y}`：`{S.new_dis}` < `dis[{S.y}]` → ==更短==，`dis[{S.y}]` 记为 `{S.new_dis}` 并入堆'
                                               if S.new_dis < S.dis[S.y] else f'经 `{S.x}` 到 `{S.y}` 要 `{S.new_dis}`，不比现有的 `{S.dis[S.y]}` 短'),
        'dis[y] = new_dis': '`dis[{y}] = {new_dis}`：这也是 `{y}` 回到 0 的最短时间',
        'heappush': '把 `({new_dis}, {y})` 放进堆，之后再用它松弛邻居',
        'vis = [False]': '`vis[i]` 记录节点 i 的价值是否已算入；每个点价值至多算一次',
        'vis[0] = True': '起点 0 一开始就算入（价值 `{values[0]}`）',
        'dfs(0, 0, values[0])': '从 0 出发开始暴搜：时间 `0`，价值 `{values[0]}`',
        'if x == 0': lambda S, B, r: (f'回到了 0：路径合法，用当前价值 `{S.sum_value}` 更新答案' if S.x == 0
                                      else f'当前在 `{S.x}`，不是 0，不能结算，继续走'),
        'ans = max': '`ans = max({B.ans}, {sum_value}) = {ans}`',
        'if sum_time + t + dis[y]': lambda S, B, r: (
            f'去 `{S.y}`：`{S.sum_time}+{S.t}+{S.dis[S.y]}` = {S.sum_time + S.t + S.dis[S.y]}'
            + (f' > {S.max_time}，回不来 → ==剪枝==' if S.sum_time + S.t + S.dis[S.y] > S.max_time
               else f' <= {S.max_time}，来得及回 0')),
        'dfs(y, sum_time + t, sum_value)': '`{y}` 价值已算过：只加时间 `+{t}`，价值不变，递归到 `{y}`',
                'dfs(y, sum_time + t, sum_value + values[y])': '`{y}` 第一次到：标记 `vis[{y}]`，时间 `+{t}`，价值 `+{values[y]}`，递归到 `{y}`',
        'vis[y] = False': '回溯：撤销标记，别的路径里 `{y}` 仍是第一次到',
        'return ans': '搜索结束，最大价值 =={ret}==',
    },
    max_steps=64,
    cards=dict(
        one_liner='路径最多 10 条边，直接暴搜，最短路只负责剪枝',
        complexity='时间 `O(n+m log m+4^k)`，`k = maxTime / min(time)`',
        problem=['无向图，每个点有价值；找一条从 `0` 出发并回到 `0`、总时间不超过 `maxTime` 的路径',
                 '价值 = 路径经过的==不同==节点的价值之和（可重复经过）',
                 '示例：`values=[0,32,10,43]`，`maxTime=40`（原题为 49） → `75`'],
        quote='路径至多有 maxTime/min(time) ≤ 10 条边……搜索树至多有 11 层；每个节点至多有 4 条边，搜索树的每个节点至多有 4 个儿子。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`time ≥ 10`、`maxTime ≤ 100` → 最多走 10 条边；度 ≤ 4 → 四叉树，层数 ≤ 11，暴搜够快',
              '`vis` 记录价值是否算过：第一次到才加价值，回溯时撤销',
              '方法二先用 Dijkstra 求每点回 0 的最短时间：回不来就不往下搜'],
        result='最大价值 75（走 0→1→0→3→0）',
        summary=['时间 `O(n+m log m+4^k)`，空间 `O(n+m+k)`',
                 '`x == 0` 处不要 return：回到 0 以后还可以继续走',
                 '重复经过的点只加时间，不加价值；回溯时要把 `vis[y]` 恢复',
                 '灵神方法一是不带 Dijkstra 的纯暴搜，本视频演示的是加最短路剪枝的方法二'],
    ),
)
