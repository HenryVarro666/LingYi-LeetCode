import math as _m

TIMES = [[1, 2, 4], [1, 3, 1], [3, 2, 2], [2, 4, 1], [3, 4, 5], [4, 5, 3]]
N, K = 5, 1
# 代码里节点编号减 1：这里的坐标按 0..4 给出
POS = {0: (0.06, 0.5), 1: (0.36, 0.1), 2: (0.36, 0.9), 3: (0.66, 0.5), 4: (0.94, 0.5)}
EDGES = [(x - 1, y - 1, d) for x, y, d in TIMES]
FOR_LINE = 14


def _inf(v):
    return '∞' if v == math.inf else v


def _graph(cv, T, box, pos, edges, ncol, nsub, ecol, title):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    R = 32
    L, Rr, Tp, Bt = x0 + 60, x1 - 60, y0 + 64 + R, y1 - R - 30
    P = {u: (L + fx * (Rr - L), Tp + fy * (Bt - Tp)) for u, (fx, fy) in pos.items()}
    for u, v, w in edges:
        c, wd = ecol(u, v)
        (ax, ay), (bx, by) = P[u], P[v]
        dd = _m.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / dd, (by - ay) / dd
        cv.arrow((ax + ux * R, ay + uy * R), (bx - ux * (R + 2), by - uy * (R + 2)), c, wd, 16)
        mx, my = (ax + bx) / 2 - uy * 20, (ay + by) / 2 + ux * 20
        cv.rect((mx - 17, my - 15, mx + 17, my + 15), fill=T['bg'], r=6)
        cv.text((mx, my), w, 22, c if c != T['dim'] else T['muted'], anchor='mm', bold=True, mono=True)
    for u, (px, py) in P.items():
        fc = ncol(u)
        cv.d.ellipse((px - R, py - R, px + R, py + R), fill=fc, outline=T['border'], width=2)
        cv.text((px, py), u, 28, T['bg'] if fc != T['panel2'] else T['text'], anchor='mm', bold=True)
        s = nsub(u)
        if s is not None:
            if py < (Tp + Bt) / 2 - 5:
                cv.text((px, py - R - 4), s, 20, T['yellow'], anchor='mb', bold=True, mono=True)
            else:
                cv.text((px, py + R + 4), s, 20, T['yellow'], anchor='mt', bold=True, mono=True)


def _draw(cv, S, B, box, T):
    dis = S.get('dis')
    x = S.get('x') if 'dx' in S else None
    dx = S.get('dx')
    line = S.get('_line')
    y = S.get('y') if line in range(FOR_LINE, FOR_LINE + 6) else None

    def ncol(u):
        if dis is None:
            return T['panel2']
        if u == x:
            return T['blue']
        if dis[u] == math.inf:
            return T['panel2']
        if dx is not None and dis[u] < dx or 'mx' in S:
            return T['green']
        return T['orange']

    def nsub(u):
        return None if dis is None else f'dis={_inf(dis[u])}'

    def ecol(u, v):
        if u == x and v == y:
            return T['yellow'], 5
        return T['dim'], 3

    _graph(cv, T, box, POS, EDGES, ncol, nsub, ecol,
           '有向图（蓝 = 刚出堆的 x，绿 = 最短路已确定，橙 = 暂定，灰 = 还没到达）')


def _text(S, B):
    line = S.get('_line')
    if 'new_dis' in S and line in (FOR_LINE + 1, FOR_LINE + 2, FOR_LINE + 3, FOR_LINE + 4):
        y = S['y']
        old = B['dis'][y] if 'dis' in B else S['dis'][y]
        return f"经过 `{S['x']}` 到 `{y}`：`dx + d = {S['dx']} + {S['d']}` = =={S['new_dis']}==　对比 `dis[{y}] = {_inf(old)}`"
    if 'dx' in S:
        return f"刚出堆：`dx = {S['dx']}`，`x = {S['x']}`，此时 `dis[{S['x']}] = {_inf(S['dis'][S['x']])}`"
    return '堆里存 `(dis, 节点)`：每次弹出 dis 最小的节点'


def _skip(S, B, r):
    if S.dx > S.dis[S.x]:
        return f'`dx = {S.dx} > dis[{S.x}] = {S.dis[S.x]}`：==x 之前出堆过==，这是过时的旧记录'
    return f'`dx = {S.dx} == dis[{S.x}]`：x ==首次出堆==，`dis[{S.x}]` 已是最短路，去更新邻居'


def _for(S, B, r):
    same = 'y' in B and (B.y, B.d) == (S.y, S.d)
    if 'y' not in S or same and not ('new_dis' in B and B.new_dis == B.dx + B.d):
        return f'`{S.x}` 没有出边，什么都不用做'
    if 'y' in B and (B.y, B.d) == (S.y, S.d):
        return f'`{S.x}` 的出边都看完了'
    return f'看边 `{S.x} → {S.y}`，边权 `{S.d}`'


def _cmp(S, B, r):
    y = S.y
    if S.new_dis < S.dis[y]:
        return f'`{S.new_dis} < dis[{y}] = {_inf(S.dis[y])}`：==找到更短的路=='
    return f'`{S.new_dis} ≥ dis[{y}] = {S.dis[y]}`：不比原来短，不更新'


CONFIG = dict(
    num=743, title='网络延迟时间', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='堆优化 Dijkstra',
    tags=['labuladong', '灵神题单·图论算法'],
    code='''
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        g = [[] for _ in range(n)]  # 邻接表
        for x, y, d in times:
            g[x - 1].append((y - 1, d))

        dis = [inf] * n
        dis[k - 1] = 0
        h = [(0, k - 1)]
        while h:
            dx, x = heappop(h)
            if dx > dis[x]:  # x 之前出堆过
                continue
            for y, d in g[x]:
                new_dis = dx + d
                if new_dis < dis[y]:
                    dis[y] = new_dis  # 更新 x 的邻居的最短路
                    heappush(h, (new_dis, y))
        mx = max(dis)
        return mx if mx < inf else -1
''',
    call=f'Solution().networkDelayTime({TIMES}, {N}, {K})',
    expect=7,
    skip=['for x, y, d in times', 'g[x - 1].append'],
    max_steps=70,
    views=[
        dict(type='text', fn=_text, h=56, size=24),
        dict(type='custom', draw=_draw, h=390),
        dict(type='array', var=lambda S: [_inf(v) for v in S['dis']] if 'dis' in S else None,
             label='dis[i]：起点 0 到 i 的最短路', h=170, cell=90,
             color=lambda S, i, v: 'blue' if 'dx' in S and i == S['x'] else None),
        dict(type='heap', var='h', label='h（最小堆，元素 = (dis, 节点)）', h=130,
             fmt=lambda t: f'({t[0]},{t[1]})'),
    ],
    watch=[('dx', 'dx', 'blue'), ('x', 'x', 'blue'), ('y', 'y', 'yellow'), ('d', 'd'), ('new_dis', 'new_dis', 'orange'),
           ('mx', 'mx', 'green')],
    captions={
        'g = [[] for': '建邻接表：`g[x]` 存 `(y, d)`，==节点编号减 1==，从 0 开始',
        'dis = [inf] * n': '`dis[i]`：起点到 i 的最短路；先全设为 ∞（尚未算出）',
        'dis[k - 1] = 0': '起点 `{k - 1}` 到自己的距离是 `0`',
        'h = [(0, k - 1)]': '把 `(dis[k], k)` = `(0, {k - 1})` 入堆',
        'while h': lambda S, B, r: '堆非空，继续' if S.h else '堆空了：所有能到的点都处理完',
        'dx, x = heappop': '弹出堆顶 `({dx}, {x})`：==堆里 dis 最小==的节点',
        'if dx > dis[x]': _skip,
        'continue': '它的邻居早被更小的 `dis[{x}]` 更新过，用旧值不可能更短 → ==跳过==',
        'for y, d in g[x]': _for,
        'new_dis = dx + d': '走 `{x} → {y}`：`{dx} + {d}` = =={new_dis}==',
        'if new_dis < dis[y]': _cmp,
        'dis[y] = new_dis': '更新邻居：`dis[{y}]` = =={dis[y]}==',
        'heappush(h,': '`({new_dis}, {y})` 入堆，之后可能还会有更小的 `{y}` 入堆',
        'mx = max(dis)': '所有节点都收到信号的时间 = 最短路的==最大值== `{mx}`',
        'return mx': lambda S, B, r: f'`mx = {S.mx} < inf`：都能到达，返回 =={r}==' if r != -1 else '有节点到不了，返回 `-1`',
    },
    cards=dict(
        one_liner='每次取出 dis 最小的点，它的最短路就确定了，再用它更新邻居',
        complexity='时间 `O(m log m)`，空间 `O(m)`',
        problem=['`n` 个节点（编号 1~n），`times[i] = (u, v, w)` 是一条有向边，传递时间 `w`',
                 '从节点 `k` 发出信号，求==所有节点都收到==的时间；有收不到的返回 `-1`',
                 '示例：`[[2,1,1],[2,3,1],[3,4,1]], n=4, k=2` → `2`',
                 '本视频：5 个节点、6 条边，`k = 1`（代码里编号减 1，起点是 0）'],
        quote='如果 `dx > dis[x]` 说明 x 之前出堆过，我们已经更新了 x 的邻居的最短路，所以这次就==不用更新了==，继续外层循环。',
        quote_src='—— 灵茶山艾府题解 · 写法二：堆优化 Dijkstra',
        idea=['取未确定点中 `dis` 最小的：==没有负权边==，不可能绕路更短 → 它已确定',
              '用最小堆找最小值：更新 `dis[y]` 时把 `(dis[y], y)` 入堆',
              '同一节点可能在堆里出现多次，出堆时用 `dx > dis[x]` 过滤旧记录'],
        summary=['时间 `O(m log m)`：堆里至多 `O(m)` 个元素',
                 '题解还有写法一：==朴素 Dijkstra== `O(n^2)`，用 `done` 数组 + 邻接矩阵，适合稠密图',
                 '易错：不判断 `dx > dis[x]` 也能对，但会重复扫邻居，变慢',
                 '答案是 `max(dis)`；有 `inf` 说明有节点收不到 → `-1`'],
    ),
)
