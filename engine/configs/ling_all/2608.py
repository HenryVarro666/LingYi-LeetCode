EDGES = [[0, 1], [1, 2], [2, 0], [2, 3]]
POS = {0: (0.18, 0.22), 1: (0.18, 0.78), 2: (0.5, 0.5), 3: (0.85, 0.5)}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '图（绿 = 已有最短路 dis，蓝 = 正在出队的 x，粉 = 遇到的 y）', 22, T['muted'], bold=True)
    W, H = x1 - x0 - 80, y1 - y0 - 90

    def P(i):
        return (x0 + 40 + POS[i][0] * W, y0 + 60 + POS[i][1] * H)
    dis = S.get('dis') if isinstance(S.get('dis'), list) else None
    x = S.get('x') if dis is not None else None
    y = S.get('y') if dis is not None else None
    start = S.get('start') if dis is not None else None
    for a, b in EDGES:
        col, w = T['border'], 4
        if x is not None and y is not None and {a, b} == {x, y} and S.get('_line') in (16, 17, 18, 19, 20):
            col, w = T['yellow'], 7
        cv.line([P(a), P(b)], col, w)
    for i in POS:
        px, py = P(i)
        fill, tc = T['panel2'], T['muted']
        if dis is not None and dis[i] >= 0:
            fill, tc = T['green'], T['bg']
        if i == start:
            fill, tc = T['cyan'], T['bg']
        if i == x:
            fill, tc = T['blue'], T['bg']
        if i == y and S.get('_line') in (16, 17, 18, 19, 20):
            fill, tc = T['pink'], T['bg']
        cv.rect((px - 34, py - 34, px + 34, py + 34), fill=fill, r=34, outline=T['border'], width=2)
        cv.text((px, py), i, 34, tc, anchor='mm', bold=True)
        if dis is not None and dis[i] >= 0:
            cv.text((px + 40, py - 44), f'dis={dis[i]}', 22, T['green'], anchor='lm', bold=True)


CONFIG = dict(
    num=2608, title='图中的最短环', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='枚举起点 BFS，遇到已访问点就成环', tags=['灵神题单', '广度优先搜索', '难度分 1904'],
    code='''
class Solution:
    def findShortestCycle(self, n: int, edges: List[List[int]]) -> int:
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)  # 建图

        def bfs(start: int) -> int:
            ans = inf
            dis = [-1] * n  # dis[i] 表示从 start 到 i 的最短路长度
            dis[start] = 0
            q = deque([(start, -1)])
            while q:
                x, fa = q.popleft()
                for y in g[x]:
                    if dis[y] < 0:  # 第一次遇到
                        dis[y] = dis[x] + 1
                        q.append((y, x))
                    elif y != fa:  # 第二次遇到
                        ans = min(ans, dis[x] + dis[y] + 1)
            return ans

        ans = min(bfs(i) for i in range(n))
        return ans if ans < inf else -1
''',
    call='Solution().findShortestCycle(4, EDGES)',
    setup=f'EDGES = {EDGES}',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var=lambda S: S['dis'] if isinstance(S.get('dis'), list) else None, label='dis（-1 = 还没到过）', pointers={'x': 'blue', 'y': 'pink'},
             color=lambda S, i, v: 'green' if v >= 0 else None, h=170),
        dict(type='queue', var=lambda S: S['q'] if 'dis' in S and 'q' in S else None, label='队列 q：(点, 父节点)', fmt=lambda t: f'({t[0]},{t[1]})', h=110),
    ],
    watch=['start', 'x', 'fa', 'y', ('ans', 'ans', 'green')],
    captions={
        'dis[y] < 0': lambda S, B, ret: (f"`dis[{S['y']}] = -1`：==第一次遇到 {S['y']}==，走树边" if S['dis'][S['y']] < 0 else f"`dis[{S['y']}] = {S['dis'][S['y']]}`：{S['y']} 之前遇到过，转去判断是不是环"),
        'dis[y] = dis[x] + 1': '树边：`dis[{y}] = dis[{x}] + 1 = {dis[y]}`，{y} 入队，父节点记为 {x}',
        'elif y != fa': lambda S, B, ret: (f"{S['y']} 已到过且不是父节点 `{S['fa']}`：==到同一点有两条不同路径 → 成环==" if S['y'] != S['fa'] else f"{S['y']} 就是来时的父节点 `{S['fa']}`，这是走过的那条边，不是环"),
        'ans = min(ans, dis[x]': '环长 = `dis[{x}] + dis[{y}] + 1` = {dis[x]} + {dis[y]} + 1 = =={dis[x]+dis[y]+1}==，更新 `ans = {ans}`',
        'return ans': '从 `{start}` 出发的最短环是 `{ans}`（inf = 没有环）',
        'ans = min(bfs': '枚举完所有起点，取最小：`ans = {ans}`',
        'return ans if ans < inf': '答案 {ans}，有环就返回它，否则 -1',
    },
    skip=['g[x].append', 'g[y].append', 'for x, y in edges', 'g = [[]', 'dis[start] = 0', 'ans = inf', 'dis = [-1]'],
    max_steps=60,
    cards=dict(
        one_liner='枚举起点做 BFS：碰到已访问的非父节点，就找到一个环',
        complexity='时间 `O(nm)`，空间 `O(n + m)`',
        problem=['无向图 `n` 个点，每对点至多一条边',
                 '求图中==最短环==的长度，没有环返回 `-1`',
                 '示例：`n=4`，边 `0-1, 1-2, 2-0, 2-3` → `3`（三角形 0-1-2）'],
        quote='为什么说发现一个已经入队的点，就说明有环？ 这说明到同一个点有两条不同的路径，这两条路径组成了一个环。',
        quote_src='—— 灵茶山艾府题解 · 答疑',
        idea=['以每个点为起点各做一次 BFS，`dis[i]` 记录起点到 i 的最短路',
              '遇到 `dis[y] >= 0` 且 `y` 不是父节点：到 y 有两条路，环长 `dis[x]+dis[y]+1`',
              '起点恰好在最短环上时，这个值才是真正的环长；其余起点只会算出更大的值，取最小即可'],
        summary=['时间 `O(nm)`：n 次 BFS，每次 `O(m)`',
                 '==必须排除父节点 `fa`==：否则 x-y 这条树边会被当成长度 2 的环',
                 '用 `inf` 表示无环，最后判断 `ans < inf` 再返回',
                 '思考题：最大环等价于哈密顿回路，是 NP 完全问题，只能暴搜'],
    ),
)
