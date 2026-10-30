import math as _m


def _graph(cv, T, box, pos, edges, ncol, nsub, ecol, title, directed=True, R=30):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    L, Rr, Tp, Bt = x0 + 70, x1 - 70, y0 + 60 + R, y1 - R - 34
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
    for u in pos:
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
EDGES = [(0, 1, 1), (1, 4, 1), (0, 2, 1), (2, 3, 1), (3, 4, 1)]
POWER = 4
COST = [2, 3, 1, 1, 1]
POS = {0: (0.0, 0.5), 1: (0.5, 0.0), 2: (0.3, 1.0), 3: (0.72, 1.0), 4: (1.0, 0.5)}

CODE = '''
class Solution:
    def minTimeMaxPower(self, n: int, edges: list[list[int]], power: int, cost: list[int], source: int, target: int) -> list[int]:
        g = [[] for _ in range(n)]
        for x, y, t in edges:
            g[x].append((y, t))

        dis = [[inf] * (power + 1) for _ in range(n)]
        dis[source][power] = 0
        h = [(0, -power, source)]  # (最短路长度, -剩余电量, 节点编号)

        while h:
            d, rem, x = heappop(h)
            rem = -rem
            if x == target:
                return [d, rem]
            if d > dis[x][rem] or rem < cost[x]:
                continue
            rem -= cost[x]
            for y, t in g[x]:
                new_dis = d + t
                if new_dis < dis[y][rem]:
                    dis[y][rem] = new_dis
                    heappush(h, (new_dis, -rem, y))

        return [-1, -1]
'''
_L = CODE.strip('\n').split('\n')
WHILE_LINE = next(i + 1 for i, l in enumerate(_L) if 'while h' in l)
FOR_LINE = next(i + 1 for i, l in enumerate(_L) if 'for y, t in g[x]' in l)
RET_LINE = next(i + 1 for i, l in enumerate(_L) if 'return [d, rem]' in l)


def _draw(cv, S, B, box, T):
    line = S.get('_line') or 0
    live = line > WHILE_LINE and 'rem' in S and 'x' in S and 'd' in S
    x = S['x'] if live else None
    y = S['y'] if live and line >= FOR_LINE else None
    dis = S.get('dis')
    done = line == RET_LINE

    def ncol(u):
        if u == x:
            return T['green'] if done else T['blue']
        if dis is not None and any(v < inf for v in dis[u]):
            return T['orange']
        return T['panel2']

    def nsub(u):
        if dis is None:
            return None
        s = ' '.join(f'{v}@{r}' for r, v in enumerate(dis[u]) if v < inf)
        return s or None

    def ecol(u, v):
        if y is not None and (u, v) == (x, y):
            return T['yellow'], 6
        return T['dim'], 3

    _graph(cv, T, box, POS, EDGES, ncol, nsub, ecol,
           '边权 = 时间；黄字 = 到该点的 (最短时间@剩余电量)；蓝 = 刚出堆', directed=True)


def _text(S, B):
    line = S.get('_line') or 0
    if line == WHILE_LINE:
        return '从堆里取下一个状态（时间最小的先出）'
    if line < WHILE_LINE or 'x' not in S or 'rem' not in S:
        return '分层图：状态 = (节点, 剩余电量)，每层是一种剩余电量'
    x, rem = S['x'], S['rem']
    if line > FOR_LINE and 'y' in S and 'new_dis' in S:
        return f"`{x}` 出发后电量 `{rem}`，走边 `{x}→{S['y']}` 到 `({S['y']}, 电量{rem})`：时间 `{S['new_dis']}`"
    return f"当前状态：节点 `{x}`，电量 `{rem}`，已用时间 `{S.get('d', '?')}`；转发要花 `{S['cost'][x]}` 电量"


def _skip(S, B, r):
    if S.rem < S.cost[S.x]:
        return f'`rem = {S.rem} < cost[{S.x}] = {S.cost[S.x]}`：==电量不够转发==，这条路死了'
    return f'`d = {S.d} > dis[{S.x}][{S.rem}] = {S.dis[S.x][S.rem]}`：旧记录，==已经有更短的到过这个状态=='


def _cmp(S, B, r):
    if S.d > S.dis[S.x][S.rem]:
        return f'`{S.d} > dis[{S.x}][{S.rem}] = {S.dis[S.x][S.rem]}` → 成立：这是过时的堆记录，跳过'
    if S.rem < S.cost[S.x]:
        return f'`{S.rem} < cost[{S.x}] = {S.cost[S.x]}` → 成立：==剩余电量不够从 {S.x} 转发==，跳过'
    return f'`d` 没过时，且 `rem = {S.rem} >= cost[{S.x}] = {S.cost[S.x]}` → 能继续转发'


def _upd(S, B, r):
    y, rem, nd = S.y, S.rem, S.new_dis
    if nd < S.dis[y][rem]:
        old = S.dis[y][rem]
        return f'`{nd} < dis[{y}][{rem}] = {"∞" if old == inf else old}` → 状态 `({y}, 电量{rem})` 找到更短路，更新'
    return f'`{nd}` 不比 `dis[{y}][{rem}] = {S.dis[y][rem]}` 短，不更新'


def _ret(S, B, r):
    return f'==目标节点首次出堆==：时间 `{S.d}` 最短，且（同样最短时）剩余电量 `{S.rem}` 最大 → 返回 `[{S.d}, {S.rem}]`'


CONFIG = dict(
    num=3977, title='有限电量到达目标节点的最少时间', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='分层图 Dijkstra',
    tags=['灵神题单·图论算法', '灵神题单·动态规划', '难度分 2103'],
    code=CODE,
    call=f'Solution().minTimeMaxPower({N}, {[list(e) for e in EDGES]}, {POWER}, {COST}, 0, 4)',
    expect=[3, 0],
    skip=['for x, y, t in edges', 'g[x].append'],
    max_steps=80,
    views=[
        dict(type='text', fn=_text, h=56, size=24),
        dict(type='custom', draw=_draw, h=360),
        dict(type='grid', var='dis', rows=list(range(N)), cols=list(range(POWER + 1)), h=300, cell=70,
             label='dis[节点][剩余电量]（行 = 节点，列 = 剩余电量）',
             color=lambda S, i, j, v: 'blue' if S.get('_line', 0) > WHILE_LINE and 'x' in S and 'rem' in S and (i, j) == (S['x'], S['rem']) and S.get('_line') <= FOR_LINE - 1 else None),
        dict(type='heap', var='h', label='h：(时间, -电量, 节点)', h=110, fmt=lambda t: f'({t[0]},{t[1]},{t[2]})'),
    ],
    watch=[('d', 'd', 'blue'), ('rem', 'rem', 'cyan'), ('x', 'x', 'blue'), ('y', 'y', 'yellow'), ('new_dis', 'new_dis', 'orange')],
    captions={
        'g = [[] for': '有向图：邻接表 `g[x]` 存 `(终点, 耗时)`',
        'dis = [[inf]': '`dis[x][rem]`：到 x 且此时剩余电量恰为 rem 的最短时间 → ==分层图的一个点==',
        'dis[source][power] = 0': '起点在满电 `{power}` 时，用时 0',
        'h = [(0, -power, source)]': '堆元素 `(时间, -电量, 节点)`：时间小优先；时间相同则电量大优先（电量取负）',
        'while h': lambda S, B, r: '堆非空，继续' if S.h else '堆空了：目标一直没出堆，说明到不了',
        'd, rem, x = heappop': '弹出 `({d}, {rem}, {x})`，即时间 {d}、节点 {x}：当前时间最小，同时间电量最大',
        'rem = -rem': '还原剩余电量：`rem = {rem}`',
        'if x == target': lambda S, B, r: f'`x = {S.x}`，目标是 `{S.target}`：' + ('==到达目标=='if S.x == S.target else '还没到'),
        'return [d, rem]': _ret,
        'if d > dis[x][rem] or': _cmp,
        'continue': _skip,
        'rem -= cost[x]': '从 `{x}` 转发出去，电量 `{B.rem}` → ==`{rem}`==（每条出边都扣同样的 `cost[{x}]`）',
        'for y, t in g[x]': lambda S, B, r: (f'`{S.x}` 的出边都看完了' if 'y' in B and (B.x, B.y, B.t) == (S.x, S.y, S.t) else f'看出边 `{S.x}→{S.y}`，耗时 `{S.t}`'),
        'new_dis = d + t': '到 `{y}` 的时间：`{d} + {t}` = =={new_dis}==',
        'if new_dis < dis[y][rem]': _upd,
        'dis[y][rem] = new_dis': '`dis[{y}][{rem}]` = =={new_dis}==',
        'heappush(h,': '`({new_dis}, {-rem}, {y})` 入堆',
        'return [-1, -1]': '堆空了都没弹出过 `target`：==无法到达==，返回 `[-1, -1]`',
    },
    cards=dict(
        one_liner='把「剩余电量」当作层数：分层图上跑 Dijkstra',
        complexity='时间 `O(nk + mk log(mk))`，空间 `O(nk + mk)`，`k = power`',
        problem=['有向带权图，从 `source` 出发带 `power` 电量，离开节点 `u` 要花 `cost[u]` 电量',
                 '求到 `target` 的 ==最短时间==，以及最短时的 ==最大剩余电量==',
                 '本视频：5 个点，`power = 4`，示例 → `[3, 0]`'],
        quote='堆中元素按照最短路长度为第一关键字升序，剩余电量为第二关键字降序排序。根据 Dijkstra 算法的原理，当终点 target 首次出堆时，我们就算出了从起点到终点的最短路，且剩余电量最大，可以直接返回答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dis[x][rem]`：到 x 且剩 rem 电量的最短时间，状态共 `n × (power+1)` 个',
              '堆里电量取负：同样的时间，电量大的先出堆',
              '终点首次出堆就是答案，不用再比较其他状态'],
        after=[dict(heading='另一种写法：DAG DP', lines=[
            '每走一步电量严格减少（`cost > 0`），分层图是 ==DAG==',
            '从大到小枚举剩余电量，用刷表法更新下一层，无需堆',
            '时间 `O(k(n+m))`，空间 `O(kn)`'])],
        summary=['时间 `O(nk + mk log(mk))`：状态数 `nk`，边数 `mk`，堆是懒更新',
                 '易错：电量要在出堆后再扣（`rem -= cost[x]`），并且不够就跳过',
                 '易错：堆元素第二关键字是 `-rem`，别忘了出堆后取负还原',
                 '灵神还给了 DAG DP 的写法，思路相同但不用堆'],
    ),
)
