import math as _m


def _graph(cv, T, box, pos, edges, ncol, nsub, ecol, title, directed=True):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    R = 30
    L, Rr, Tp, Bt = x0 + 70, x1 - 70, y0 + 70 + R, y1 - R - 34
    P = {u: (L + fx * (Rr - L), Tp + fy * (Bt - Tp)) for u, (fx, fy) in pos.items()}
    for u, v, w in edges:
        c, wd = ecol(u, v)
        (ax, ay), (bx, by) = P[u], P[v]
        dd = _m.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / dd, (by - ay) / dd
        if directed:
            cv.arrow((ax + ux * R, ay + uy * R), (bx - ux * (R + 2), by - uy * (R + 2)), c, wd, 16)
        else:
            cv.line([(ax + ux * R, ay + uy * R), (bx - ux * R, by - uy * R)], c, wd)
        mx, my = (ax + bx) / 2 - uy * 20, (ay + by) / 2 + ux * 20
        cv.rect((mx - 17, my - 15, mx + 17, my + 15), fill=T['bg'], r=6)
        cv.text((mx, my), w, 22, c if c != T['dim'] else T['muted'], anchor='mm', bold=True, mono=True)
    for u, (px, py) in pos.items():
        px, py = P[u]
        fc = ncol(u)
        cv.d.ellipse((px - R, py - R, px + R, py + R), fill=fc, outline=T['border'], width=2)
        cv.text((px, py), u, 28, T['bg'] if fc != T['panel2'] else T['text'], anchor='mm', bold=True)
        s = nsub(u)
        if s is not None:
            if py < (Tp + Bt) / 2 - 5:
                cv.text((px, py - R - 4), s, 20, T['yellow'], anchor='mb', bold=True, mono=True)
            else:
                cv.text((px, py + R + 4), s, 20, T['yellow'], anchor='mt', bold=True, mono=True)

N = 5
EDGES = [(0, 1, 2), (1, 2, 1), (0, 2, 4), (2, 3, 1), (3, 4, 3)]
DISAPPEAR = [1, 2, 5, 6, 9]
POS = {0: (0.02, 0.5), 1: (0.3, 0.04), 2: (0.34, 0.96), 3: (0.68, 0.5), 4: (0.98, 0.5)}

CODE = '''
class Solution:
    def minimumTime(self, n: int, edges: List[List[int]], disappear: List[int]) -> List[int]:
        g = [[] for _ in range(n)]  # 稀疏图用邻接表
        for x, y, wt in edges:
            g[x].append((y, wt))
            g[y].append((x, wt))

        dis = [-1] * n
        dis[0] = 0
        h = [(0, 0)]
        while h:
            dx, x = heappop(h)
            if dx > dis[x]:  # x 之前出堆过
                continue
            for y, wt in g[x]:
                new_dis = dx + wt
                if new_dis < disappear[y] and (dis[y] < 0 or new_dis < dis[y]):
                    dis[y] = new_dis  # 更新 x 的邻居的最短路
                    heappush(h, (new_dis, y))
        return dis
'''
_L = CODE.strip('\n').split('\n')
FOR_LINE = next(i + 1 for i, l in enumerate(_L) if 'for y, wt in g[x]' in l)


def _draw(cv, S, B, box, T):
    dis = S.get('dis')
    dx = S.get('dx') if 'x' in S else None
    x = S.get('x') if dx is not None else None
    line = S.get('_line')
    y = S.get('y') if line in range(FOR_LINE, FOR_LINE + 6) else None
    done = dis is not None and line == len(_L)

    def ncol(u):
        if dis is None or dis[u] < 0:
            return T['panel2']
        if u == x and not done:
            return T['blue']
        if done or (dx is not None and dis[u] < dx):
            return T['green']
        return T['orange']

    def nsub(u):
        d = '?' if dis is None else ('-' if dis[u] < 0 else dis[u])
        return f'dis={d}  消失@{DISAPPEAR[u]}'

    def ecol(u, v):
        if y is not None and {u, v} == {x, y}:
            return T['yellow'], 6
        return T['dim'], 3

    _graph(cv, T, box, POS, EDGES, ncol, nsub, ecol,
           '蓝 = 刚出堆，绿 = 已确定，橙 = 暂定，灰 = 没到；黄字 = 最短路 / 消失时刻', directed=False)


def _text(S, B):
    line = S.get('_line')
    if 'new_dis' in S and line in range(FOR_LINE + 1, FOR_LINE + 5):
        y = S['y']
        ok = S['new_dis'] < S['disappear'][y]
        return f"走到 `{y}` 的时刻 `{S['new_dis']}`，`{y}` 在 `{S['disappear'][y]}` 消失 → " + ('==来得及==' if ok else '==来不及，不更新==')
    if 'dx' in S:
        return f"刚出堆：`dx = {S['dx']}`，`x = {S['x']}`"
    return '堆里存 `(最短路, 节点)`：每次弹出最短路最小的节点'


def _upd(S, B, r):
    y, nd, dp = S.y, S.new_dis, S.disappear[S.y]
    if nd >= dp:
        return f'`{nd} >= disappear[{y}] = {dp}`：==到达时 {y} 已经消失==，不更新，也不入堆'
    if B.dis[y] < 0:
        return f'`{nd} < disappear[{y}] = {dp}` 来得及，且 `dis[{y}]` 还是 -1（没到过）→ 更新'
    if nd < B.dis[y]:
        return f'`{nd} < disappear[{y}] = {dp}` 来得及，且比 `dis[{y}] = {B.dis[y]}` 更短 → 更新'
    return f'`{nd} < disappear[{y}] = {dp}` 来得及，但不比 `dis[{y}] = {B.dis[y]}` 短 → 不更新'


def _skip(S, B, r):
    if S.dx > S.dis[S.x]:
        return f'`dx = {S.dx} > dis[{S.x}] = {S.dis[S.x]}`：==x 之前出堆过==，旧记录'
    return f'`dx = {S.dx} == dis[{S.x}]`：x 首次出堆，去更新邻居'


CONFIG = dict(
    num=3112, title='访问消失节点的最少时间', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='Dijkstra：到得太晚就不更新',
    tags=['灵神题单·图论算法', '难度分 1757'],
    code=CODE,
    call=f'Solution().minimumTime({N}, {[list(e) for e in EDGES]}, {DISAPPEAR})',
    expect=[0, -1, 4, 5, 8],
    skip=['for x, y, wt in edges', 'g[x].append', 'g[y].append', 'dis = [-1]', 'dis[0] = 0'],
    max_steps=80,
    views=[
        dict(type='text', fn=_text, h=56, size=24),
        dict(type='custom', draw=_draw, h=370),
        dict(type='array', var=lambda S: list(S['dis']) if 'dis' in S else None, label='dis[i]：0 到 i 的最短时间（-1 = 到不了）', h=150, cell=90,
             color=lambda S, i, v: 'blue' if 'x' in S and 'dx' in S and i == S['x'] else ('green' if v >= 0 else None)),
        dict(type='heap', var='h', label='h（最小堆，元素 = (最短路, 节点)）', h=130, fmt=lambda t: f'({t[0]},{t[1]})'),
    ],
    watch=[('dx', 'dx', 'blue'), ('x', 'x', 'blue'), ('y', 'y', 'yellow'), ('wt', 'wt'), ('new_dis', 'new_dis', 'orange')],
    captions={
        'g = [[] for': '无向图：每条边在 `g[x]` 和 `g[y]` 里各存一份',
        'dis = [-1] * n': '`dis[i] = -1`：还没到过（或者到不了）',
        'dis[0] = 0': '起点 `0` 到自己 `0`',
        'h = [(0, 0)]': '堆里放 `(0, 0)`：最短路 0 的节点 0',
        'while h': lambda S, B, r: '堆非空，继续' if S.h else '堆空了：能及时到达的点都处理完',
        'dx, x = heappop': '弹出堆顶 `({dx}, {x})`：==最短路最小==的节点',
        'if dx > dis[x]': _skip,
        'continue': '这个记录已经过时，邻居早用更小的值更新过 → ==跳过==',
        'for y, wt in g[x]': lambda S, B, r: (f'`{S.x}` 的邻居都看完了' if 'y' in B and (B.x, B.y, B.wt) == (S.x, S.y, S.wt) else f'看边 `{S.x} - {S.y}`，边权 `{S.wt}`'),
        'new_dis = dx + wt': '走这条边到 `{y}` 的时刻：`{dx} + {wt}` = =={new_dis}==',
        'if new_dis < disappear[y]': _upd,
        'dis[y] = new_dis': '更新邻居：`dis[{y}]` = =={dis[y]}==',
        'heappush(h,': '`({new_dis}, {y})` 入堆',
        'return dis': '`dis` 就是答案：==-1 的点要么不连通，要么来不及到达==',
    },
    cards=dict(
        one_liner='跑 Dijkstra，更新最短路前先看：到的时候点还在不在',
        complexity='时间 `O(n + m log m)`，空间 `O(n + m)`',
        problem=['无向带权图，`disappear[i]` 是节点 `i` 消失的时刻，那一刻及以后不能访问',
                 '求 `0` 到每个点的最少时间，到不了返回 `-1`',
                 '本视频：5 个点，`disappear = [1,2,5,6,9]`，节点 1 消失得最早'],
        quote='在更新最短路之前，如果最短路长度 >= disappear[i]，说明无法及时到达节点 i，不更新。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`answer` 几乎就是 Dijkstra 的 `dis` 数组',
              '只多一个判断：`new_dis < disappear[y]` 才更新、才入堆',
              '到不了的点不进堆，后面的点也就不会借道它'],
        summary=['时间 `O(n + m log m)`：堆里最多有 `O(m)` 个元素',
                 '易错：不能先跑普通 Dijkstra 再把 `dis[i] >= disappear[i]` 改成 -1',
                 '原因：近处的点 x 消失得早，会挡住远处的 y，事后改只会漏掉这种连锁',
                 '`new_dis` 等于 `disappear[y]` 时也算消失：要用严格小于'],
    ),
)
