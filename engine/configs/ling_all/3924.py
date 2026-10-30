N_ = 6
EDGES = [[0, 1, 5], [1, 2, 3], [3, 4, 4], [4, 5, 1], [1, 4, 2]]
SRC, TGT, KK = 0, 3, 1
POS = {0: (0.08, 0.5), 1: (0.32, 0.5), 2: (0.32, 0.12), 4: (0.62, 0.5), 3: (0.9, 0.5), 5: (0.62, 0.88)}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    th = S.get('threshold')
    dis = S.get('dis') if th is not None else None
    cur = S.get('x') if th is not None else None
    W, H = x1 - x0 - 120, y1 - y0 - 150
    P = {k: (x0 + 60 + v[0] * W, y0 + 70 + v[1] * H) for k, v in POS.items()}
    cv.text((x0 + 18, y0 + 4), '图（绿线 = 轻边 0，红线 = 重边 1；节点旁 = 到该点最少重边数 dis）', 22, T['muted'], bold=True)
    for a, b, w in EDGES:
        heavy = th is not None and w > th
        c = T['red'] if heavy else (T['green'] if th is not None else T['dim'])
        cv.line([P[a], P[b]], c, 5)
        mx, my = (P[a][0] + P[b][0]) / 2, (P[a][1] + P[b][1]) / 2
        cv.rect((mx - 22, my - 17, mx + 22, my + 17), fill=T['panel2'], r=8)
        cv.text((mx, my), w, 26, c, anchor='mm', bold=True)
    for v, (px, py) in P.items():
        d = dis[v] if dis is not None else None
        reached = d is not None and d != float('inf')
        fill = T['blue'] if reached else T['panel2']
        out = T['yellow'] if v == cur else (T['pink'] if v == TGT else T['border'])
        cv.rect((px - 32, py - 32, px + 32, py + 32), fill=fill, outline=out, width=6 if (v == cur or v == TGT) else 2, r=32)
        cv.text((px, py), v, 32, T['bg'] if reached else T['text'], anchor='mm', bold=True)
        if v == SRC:
            cv.text((px, py - 46), '起点', 20, T['cyan'], anchor='mb', bold=True)
        if v == TGT:
            cv.text((px, py - 46), '终点', 20, T['pink'], anchor='mb', bold=True)
        if d is not None:
            cv.text((px + 38, py + 30), 'dis=' + ('∞' if not reached else str(d)), 22, T['cyan'] if reached else T['dim'], anchor='la', bold=True, mono=True)


def _top(S):
    th = S.get('threshold')
    if th is None:
        return f'`threshold` 越大重边越少，越容易到达终点 → ==二分阈值==；要求重边数 `≤ k = {KK}`'
    hv = [w for _, _, w in EDGES if w > th]
    return f'`threshold = {th}`：权重 `> {th}` 的是重边 {hv if hv else "无"}；求最少重边数'


def _if_t(S, B, ret):
    return f'`x = {S.x}`' + (' 就是终点 → 这个阈值可行，返回 ==True==' if S.x == TGT else ' 不是终点，继续')


def _dis(S, B, ret):
    return (f'弹出的距离 `d = {S.d}` {">" if S.d > S.dis[S.x] else "=="} `dis[{S.x}] = {S.dis[S.x]}`：' +
            ('是旧的过期记录 → 跳过' if S.d > S.dis[S.x] else '是最新的 → 处理'))


def _new(S, B, ret):
    ok = S.new_dis < S.dis[S.y]
    return f'走到 `{S.y}`：`{S.wt and "重边 +1" or "轻边 +0"}`，新距离 `{S.new_dis}` {"<" if ok else ">="} 当前 `{S.dis[S.y]}` → {"更近，更新" if ok else "不更近，跳过"}'


CONFIG = dict(
    num=3924, title='有限重边的最小阈值路径', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='二分答案 · 0-1 BFS',
    tags=['灵神题单·二分算法', '灵神题单·图论算法', '难度分 2080'],
    code='''
class Solution:
    def minimumThreshold(self, n: int, edges: List[List[int]], source: int, target: int, k: int) -> int:
        g = [[] for _ in range(n)]
        max_wt = 0
        for x, y, wt in edges:
            g[x].append((y, wt))
            g[y].append((x, wt))
            max_wt = max(max_wt, wt)

        def check(threshold: int) -> bool:
            dis = [inf] * n
            dis[source] = 0
            q = deque([(source, 0)])

            while q:
                x, d = q.popleft()
                if x == target:
                    return True
                if d > dis[x]:
                    continue
                for y, w in g[x]:
                    wt = 1 if w > threshold else 0
                    new_dis = d + wt
                    if new_dis < dis[y]:
                        dis[y] = new_dis
                        if wt == 0:
                            q.appendleft((y, new_dis))
                        elif new_dis <= k:
                            q.append((y, new_dis))

            return False

        ans = bisect_left(range(max_wt + 1), True, key=check)
        return -1 if ans > max_wt else ans
''',
    call=f'Solution().minimumThreshold({N_}, {EDGES}, {SRC}, {TGT}, {KK})',
    expect=4,
    views=[
        dict(type='text', fn=_top, size=24, h=80),
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', fn=lambda S: f"队列 `q = {list(S['q'])}`" if 'q' in S and 'threshold' in S else '', size=24, h=70),
    ],
    watch=[('threshold', 'threshold', 'yellow'), ('x', 'x', 'blue'), ('d', 'd', 'cyan'), ('y', 'y', 'pink'), ('max_wt', 'max_wt', 'green')],
    captions={
        'g = [[]': '邻接表 `g[x]` 存 `(邻居, 边权)`，无向边两头都要加',
        'for x, y, wt in edges': lambda S, B, r: ('建图完成：`max_wt` 是二分上界，此时所有边都是轻边' if 'wt' in B and B.get('x') == S.get('x') and B.get('wt') == S.get('wt') and B.get('y') == S.get('y')
                                                  else f'读入边 `{S.x} - {S.y}`（权 {S.wt}），两头都加进邻接表，`max_wt` 取最大'),
        'dis = [inf]': '`threshold = {threshold}`：`dis[v]` = 到 v 至少要走几条重边，先全设为无穷',
        'dis[source] = 0': '起点不用走边：`dis[{source}] = 0`',
        'q = deque': '0-1 BFS 的双端队列，装 `(节点, 重边数)`',
        'while q': lambda S, B, r: (f'队列非空 `{list(S.q)}` → 继续' if S.q else '队列空了，没找到终点 → 这个阈值不行'),
        'x, d = q.popleft()': '取队首：`x = {x}`，已用重边 `d = {d}`',
        'if x == target': _if_t,
        'if d > dis[x]': _dis,
        'for y, w in g[x]': lambda S, B, r: (f'`{S.x}` 的邻居都看完了，回到队列' if B.get('x') == S.x and B.get('y') == S.y
                                             else f'枚举 `{S.x}` 的邻居：`y = {S.y}`，边权 `w = {S.w}`'),
        'wt = 1 if w': '`w = {w}` {">" if w > threshold else "<="} `threshold = {threshold}` → ==权重 {wt}==（{"重边" if wt else "轻边"}）',
        'new_dis = d + wt': '经 `{x}` 走到 `{y}` 的重边数 `{d} + {wt} = {new_dis}`',
        'if new_dis < dis[y]': _new,
        'dis[y] = new_dis': '更新 `dis[{y}] = {new_dis}`',
        'if wt == 0': '{"轻边：距离不变，放队首（0-1 BFS 优先处理）" if wt == 0 else "重边：距离 +1，放队尾"}',
        'q.appendleft': '放到队首：`({y}, {new_dis})`',
        'elif new_dis <= k': '`new_dis = {new_dis}` {"<=" if new_dis <= k else ">"} `k = {k}`：{"还没超限，放队尾" if new_dis <= k else "已经超过 k 条重边，剪枝丢弃"}',
        'q.append': '放到队尾：`({y}, {new_dis})`',
        'return False': '队列耗尽也没到终点 → `threshold = {threshold}` ==不可行==',
        'ans = bisect_left': '`check` 对 `threshold` 单调：从 0 到 `max_wt` 找第一个 True → ==最小阈值=={ans}==',
        'return -1 if': '`ans = {ans}` {"> max_wt：不连通 → -1" if ans > max_wt else "<= max_wt：有解"} → 返回 =={ret}==',
    },
    skip=['g[x].append', 'g[y].append', 'max_wt = max'], max_steps=60,
    cards=dict(
        one_liner='阈值越大重边越少：二分阈值，0-1 BFS 判定能否到达',
        complexity='时间 `O((n+m) log U)`，空间 `O(n+m)`',
        problem=['无向带权图，边权 `> threshold` 的是重边，路径至多含 `k` 条重边才有效',
                 '求使 `source` 到 `target` 有有效路径的==最小整数== `threshold`，没有返回 `-1`',
                 f'本视频：`n = 6, source = 0, target = 3, k = 1` → `4`'],
        quote='把边权 ≤ threshold 的边视作 0，边权 > threshold 的边视作 1，问题变成 3286. 穿越网格图的安全路径。这可以用 0-1 BFS 解决。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`threshold` 越大，重边越少，越能找到路径 → 单调，可以==二分猜答案==',
              '判定：轻边权 0、重边权 1，最少重边数 `≤ k` 即可行',
              '0 权边放队首、1 权边放队尾，就是 0-1 BFS，每个点只需少量处理'],
        summary=['时间 `O((n+m) log U)`，`U = max(w)`；空间 `O(n+m)`',
                 '开区间二分，`range(max_wt + 1)` 里找第一个 True；全是 False 说明不连通，返回 `-1`',
                 '`elif new_dis <= k` 剪掉超过 k 条重边的状态',
                 '题解还有“写法二”：只在排序去重后的边权里二分，复杂度 `O((n+m) log m)`',
                 '起点 == 终点时，`check(0)` 直接为 True，答案 0'],
    ),
)
