EDGES = [[0, 1], [0, 2], [1, 3], [2, 3]]
POS = {0: (0.04, 0.5), 1: (0.5, 0.12), 2: (0.5, 0.88), 3: (0.96, 0.5)}


def _draw(cv, S, B, box, T):
    import math
    x0, y0, x1, y1 = box
    if 'vis' not in S or 'start' not in S:
        return
    start, vis = S['start'], S['vis']
    cur = S['_inner'].get('x')
    yy = S['_inner'].get('y')
    gw = (x1 - x0) * 0.58
    R = 32

    def P(u):
        fx, fy = POS[u]
        return x0 + 50 + fx * (gw - 100), y0 + 50 + fy * (y1 - y0 - 100)

    for a, b in EDGES:
        (ax, ay), (bx, by) = P(a), P(b)
        d = math.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / d, (by - ay) / d
        hot = cur == a and yy == b
        col = T['yellow'] if hot else T['muted']
        cv.arrow((ax + ux * R, ay + uy * R), (bx - ux * (R + 4), by - uy * (R + 4)), col, 6 if hot else 3, 16 if hot else 12)
    for u in range(4):
        X, Y = P(u)
        seen = vis[u] == start
        fill = T['green'] if seen and u != start else T['blue'] if u == start else T['panel2']
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=fill,
                     outline=T['yellow'] if u == cur else T['border'], width=6 if u == cur else 2)
        cv.text((X, Y), u, 30, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)
    cv.text((x0 + 20, y1 - 22), f'蓝 = 本轮起点 start={start}，绿 = 本轮访问过，黄圈 = 当前 x', 20, T['dim'], anchor='lm')
    lx = x0 + gw + 30
    cv.text((lx, y0 + 20), 'ans（每个点的祖先）', 24, T['muted'], bold=True)
    for i, lst in enumerate(S['ans']):
        old = B.get('ans')
        fresh = old is not None and i < len(old) and old[i] != lst
        cv.text((lx, y0 + 70 + i * 54), f'ans[{i}] = {lst}', 30, T['yellow'] if fresh else T['text'], bold=fresh, mono=True)


def _chk(S, B, ret):
    y, st = S.y, S.start
    if B.vis[y] == st:
        return f'`vis[{y}] = {st} = start`：本轮已经访问过 {y} → 不再递归'
    return f'`vis[{y}] = {B.vis[y]} ≠ {st}`：本轮还没到过 {y} → 它是 {st} 的后代'


CONFIG = dict(
    num=2192, title='有向无环图中一个节点的所有祖先', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='正向 DFS · vis 记起点',
    tags=['灵神题单', '图论算法', '难度分 1788'],
    code='''
class Solution:
    def getAncestors(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)

        def dfs(x: int) -> None:
            vis[x] = start  # 避免重复访问
            for y in g[x]:
                if vis[y] != start:
                    ans[y].append(start)  # start 是访问到的点的祖先
                    dfs(y)  # 只递归没有访问过的点

        ans = [[] for _ in range(n)]
        vis = [-1] * n
        for start in range(n):
            dfs(start)  # 从 start 开始 DFS
        return ans
''',
    call='Solution().getAncestors(4, [[0,1],[0,2],[1,3],[2,3]])',
    expect=[[], [0], [0], [0, 1, 2]],
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='array', var='vis', label='vis（vis[x] = start 表示本轮访问过）', cell=70, h=190, pointers={'start': 'blue'}),
        dict(type='calls', h=170),
    ],
    watch=[('start', 'start', 'blue'), ('x', lambda S: S['_inner'].get('x'), 'yellow'), ('y', lambda S: S['_inner'].get('y'), 'pink')],
    skip=['g = [[] for', 'for x, y in edges', 'ans = [[] for', 'vis = [-1]', 'for y in g[x]', 'for start in range'],
    max_steps=90,
    captions={
        'g[x].append(y)': '正向建图：`{x} → {y}`',
        'vis[x] = start': '标记 `vis[{x}] = {start}`：==本轮 DFS（起点 {start}）== 到过 {x}，不用每轮重置 vis',
        'if vis[y] != start': _chk,
        'ans[y].append(start)': '`{start}` 能走到 `{y}` → 它是 {y} 的祖先：`ans[{y}] = {ans[y]}`',
        'dfs(y)': '继续往下走：递归 `dfs({y})`',
        'dfs(start)': '枚举起点 `start = {start}`（从小到大，ans 天然升序）：从它出发 DFS，沿途的点都把 `{start}` 记为祖先',
        'return ans': '4 个点的祖先都算完：`{ret}`',
    },
    cards=dict(
        one_liner='从小到大枚举起点 DFS，沿途把起点记成祖先',
        complexity='时间 `O(n(n+m))`，空间 `O(n+m)`',
        problem=['有向无环图 `n` 个点，求每个点的所有祖先（能到达它的点），升序',
                 '示例：`n=8` 的图 → `[[],[],[],[0,1],[0,2],...]`',
                 '本视频：`n=4`，边 `0→1,0→2,1→3,2→3`'],
        quote='依次从起点 start=0,1,2,…,n-1 出发 DFS，途中把 start 加到能访问到的点的 answer 中。由于 start 从小到大枚举，所以 answer[i] 列表自然就是有序的了。',
        quote_src='—— 灵茶山艾府题解 · 方法二',
        idea=['“谁是我的祖先”反过来看：==从 start 出发能走到谁，谁的祖先里就有 start==',
              '`vis[x] = start` 表示本轮访问过：n 轮 DFS 起点各不相同，不必每轮重新初始化',
              '另一种写法（方法一）：反向建图，对每个点 DFS 一次，vis 为 True 的点就是祖先'],
        summary=['时间 `O(n(n+m))`，空间 `O(n+m)`（返回值不计）',
                 '==先 append 再递归==；vis 标记在 dfs 开头，所以起点自己不会进自己的 ans',
                 '这个方法不要求无环，有环也对',
                 '方法一（反向建图 + 每点 DFS）要在 DFS 后 `vis[i] = False` 去掉自己'],
    ),
)
