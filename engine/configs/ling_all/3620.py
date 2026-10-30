import math


def _layout(n):
    if n == 4:
        return [(0.1, 0.5), (0.5, 0.12), (0.5, 0.88), (0.9, 0.5)]
    if n == 5:
        return [(0.08, 0.5), (0.5, 0.12), (0.33, 0.88), (0.67, 0.88), (0.92, 0.5)]
    return [(0.1 + 0.8 * i / max(1, n - 1), 0.5 + (0.3 if i % 2 else -0.3)) for i in range(n)]


def _make_draw(low_key, node_cur, node_nb, node_text):
    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        edges, online = S['edges'], S['online']
        n = len(online)
        low = S.get(low_key)
        lay = _layout(n)
        W, H = x1 - x0 - 160, y1 - y0 - 150
        pos = [(x0 + 80 + a * W, y0 + 70 + b * H) for a, b in lay]
        cv.text((x0 + 18, y0 + 4), '图（箭头旁的数 = 恢复成本；绿 = 当前下界下可用的边，灰 = 成本太小被排除，红 = 离线节点）', 20, T['muted'], bold=True)
        cur, nb = node_cur(S), node_nb(S)
        R = 30
        for u, v, w in edges:
            a, b = pos[u], pos[v]
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy)
            p0 = (a[0] + dx / L * R, a[1] + dy / L * R)
            p1 = (b[0] - dx / L * (R + 4), b[1] - dy / L * (R + 4))
            dead = not (online[u] and online[v])
            ok = (low is not None) and w >= low and not dead
            hot = cur == u and nb == v
            col = T['yellow'] if hot else T['red'] if dead else T['green'] if ok else T['dim']
            cv.arrow(p0, p1, col, 6 if hot else 4 if ok else 2)
            mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
            nx, ny = -dy / L * 18, dx / L * 18
            cv.text((mx + nx, my + ny), w, 22, col if (ok or hot or dead) else T['muted'], anchor='mm', bold=True)
        for i in range(n):
            X, Y = pos[i]
            fill = T['panel2'] if online[i] else (90, 40, 46)
            ring = T['yellow'] if cur == i else (T['red'] if not online[i] else T['border'])
            cv.rect((X - R, Y - R, X + R, Y + R), fill=fill, outline=ring, width=5 if cur == i else 2, r=R)
            cv.text((X, Y), i, 28, T['text'], anchor='mm', bold=True)
            t = node_text(S, i)
            if t:
                cv.text((X, Y + R + 8), t, 20, T['cyan'], anchor='mt', bold=True)
            if i == 0:
                cv.text((X, Y - R - 6), '起点', 18, T['muted'], anchor='mb')
            if i == n - 1:
                cv.text((X, Y - R - 6), '终点', 18, T['muted'], anchor='mb')
    return draw


def _ntext(S, i):
    if 'res' in S and S.get('x') == i and S.get('res') is not None and S['res'] != float('inf'):
        return f"res = {S['res']}"
    if 'res' in S and S.get('x') == i and S.get('res') == float('inf'):
        return 'res = inf'
    return ''


_draw = _make_draw('lower', lambda S: S.get('x') if 'lower' in S else None, lambda S: S.get('y') if 'lower' in S else None, _ntext)


CONFIG = dict(
    num=3620, title='恢复网络路径', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='二分答案 + DAG 上记忆化 DP', tags=['灵神题单·二分算法', '难度分 1998'],
    code='''
class Solution:
    def findMaxPathScore(self, edges: List[List[int]], online: List[bool], k: int) -> int:
        n = len(online)
        g = [[] for _ in range(n)]
        max_wt = -1
        for x, y, wt in edges:
            if online[x] and online[y]:
                g[x].append((y, wt))
                if x == 0:
                    max_wt = max(max_wt, wt)

        def check(lower: int) -> bool:
            @cache
            def dfs(x: int) -> int:
                if x == n - 1:  # 到达终点
                    return 0
                res = inf
                for y, wt in g[x]:
                    if wt >= lower:
                        res = min(res, dfs(y) + wt)
                return res
            return dfs(0) <= k

        left, right = -1, max_wt + 1
        while left + 1 < right:
            mid = (left + right) // 2
            if check(mid):
                left = mid
            else:
                right = mid
        return left
''',
    call='Solution().findMaxPathScore([[0,1,5],[1,3,10],[0,2,3],[2,3,4]], [True,True,True,True], 10)',
    expect=3, max_steps=110,
    skip=['n = len(online)', 'g = [[]', 'max_wt = -1', 'for x, y, wt in edges', 'if online[x] and online[y]', 'g[x].append', 'if x == 0', 'max_wt = max', 'for y, wt in g[x]', 'res = inf', 'if x == n - 1', '@cache', 'def dfs', 'def check'],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='text', h=70, fn=lambda S: (f"开区间 `({S['left']}, {S['right']})`：`check(left)` 真，`check(right)` 假" + (f"；现在试下界 `lower = {S['lower']}`" if 'lower' in S else '') if 'left' in S and 'right' in S else '')),
        dict(type='calls', h=130),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('lower', 'lower', 'green'), ('k', 'k', 'orange')],
    captions={
        'left, right = -1': '开区间 `(-1, {right})`：`-1` 人为规定可行；`{right}` = 0 的出边最大边权 + 1，一定不可行',
        'if wt >= lower': lambda S, B, r: (f'边 `{B.x} → {B.y}` 成本 `{B.wt} ≥ {B.lower}`：边权够大，可以走' if B.wt >= B.lower
                                           else f'边 `{B.x} → {B.y}` 成本 `{B.wt} < {B.lower}`：低于下界，不能走'),
        'res = min': '`dfs({B.x})` 走边 `{B.x} → {B.y}`：先递归算 `dfs({B.y})`（{B.y} 到终点的最小成本），再加上边权 `{B.wt}`，取较小值',
        'return 0': '到达终点 `{x}`：还需成本 0',
        'return res': lambda S, B, r: (f'`dfs(0) = {S.res}`，和 `k = {S.k}` 比：' + ('==≤ k，路径有效，`check` 为真==' if S.res <= S.k else '==> k，`check` 为假=='))
                                      if S.x == 0 else (f'`dfs({S.x}) = {S.res}`：从 {S.x} 到终点的最小总成本' if S.res != float('inf') else f'`dfs({S.x}) = inf`：{S.x} 走不到终点'),
        'return dfs(0) <= k': '`check({B.lower})`：算出 0 到终点的最小总成本 `dfs(0)`，再和 `k = {B.k}` 比',
        'mid = (': '猜下界 `mid = ({left} + {right}) // 2 = {mid}`：只走成本 `≥ {mid}` 的边，最短路够不够短？',
        'if check(mid)': '调用 `check({mid})`',
        'left = mid': '`check({mid})` 为真：最小边成本 ≥ {mid} 的有效路径存在 → `left = {left}`',
        'right = mid': '`check({mid})` 为假：下界 {mid} 太高 → `right = {right}`',
        'while left + 1 < right': lambda S, B, r: ('开区间 `(left, right)` 里还有数，继续' if S.left + 1 < S.right else f'开区间空了：答案 = `left = {S.left}`'),
        'return left': '最大的使 `check` 为真的下界：==返回 {left}==',
    },
    cards=dict(
        one_liner='最大化最小边权：二分下界，再在 DAG 上算最短路是否 ≤ k',
        complexity='时间 `O((n+m) log U)`，空间 `O(n+m)`',
        problem=['DAG 上走 0 → n-1，中间点都在线，总成本 ≤ k；路径分数 = 最小边成本',
                 '求最大的分数，没有有效路径返回 -1',
                 '示例：`edges=[[0,1,5],[1,3,10],[0,2,3],[2,3,4]]`，`k=10` → `3`'],
        quote='「最大化最小值」是二分答案的代名词。由于题目保证图是一个 DAG，计算 DP 无后效性，可以用 DAG DP 解决。定义 dfs(x) 表示从 x 到 n-1 的有效路径的总恢复成本的最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['下界 `lower` 越小越宽松：有单调性 → 二分猜答案',
              '给定 `lower`，只用边权 `≥ lower` 的边；`dfs(x)` = x 到终点的最短路，DAG 上记忆化即可',
              '`dfs(0) ≤ k` 就说明答案 `≥ lower`。建图时两端点都在线才连边，省去 DP 里判断在线'],
        summary=['时间 `O((n+m) log U)`，比 Dijkstra 少一个 `log m`',
                 '`left` 初值 `-1`：人为规定可行，最后若还是 `-1` 就是无解',
                 '`right` 初值取 0 的出边最大边权 + 1（一定不可行）',
                 '`@cache` 要写在 `check` 里面：每换一个 `lower`，缓存要重来',
                 '写法二：拓扑排序（刷表法）+ `bisect_left`，本视频不展开；示例点都在线，离线节点只是不建边'],
    ),
)
