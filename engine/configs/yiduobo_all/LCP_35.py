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

PATHS = [[0, 1, 1], [1, 2, 2], [0, 1, 3]]
CNT = 2
START, END = 0, 2
CHARGE = [1, 2, 1]
N = 3
EDGES = [(0, 1, 2), (1, 2, 3)]
POS = {0: (0.0, 0.5), 1: (0.5, 0.5), 2: (1.0, 0.5)}

CODE = '''
class Solution(object):
    def electricCarPlan(self, paths, cnt, start, end, charge):

        n = len(charge)
        g = {index : {} for index in range(n)}
        for x, y, v in paths:
            if y not in g[x]:
                g[x][y] = g[y][x] = v
            else:
                g[x][y] = min(g[x][y], v)
                g[y][x] = min(g[y][x], v)

        heap = [(0, start * (cnt + 1))]
        dis = {}
        while heap:
            d, now_state = heapq.heappop(heap)
            if now_state in dis:
                continue
            dis[now_state] = d
            now_node, now_cnt = now_state // (cnt + 1), now_state % (cnt + 1)
            if now_node == end:
                return d
            for next_node in g[now_node]:
                if g[now_node][next_node] <= now_cnt:
                    next_cnt = now_cnt - g[now_node][next_node]
                    next_state = next_node * (cnt + 1) + next_cnt
                    heapq.heappush(heap, (d + g[now_node][next_node], next_state))

            if now_cnt < cnt:
                heapq.heappush(heap, (d + charge[now_node], now_state + 1))

        return -1
'''
_L = CODE.strip('\n').split('\n')
DEC_LINE = next(i + 1 for i, l in enumerate(_L) if 'now_node, now_cnt =' in l)
FOR_LINE = next(i + 1 for i, l in enumerate(_L) if 'for next_node in g[now_node]' in l)
RET_LINE = next(i + 1 for i, l in enumerate(_L) if 'return d' in l)
HEAP_LINE = next(i + 1 for i, l in enumerate(_L) if 'heap = [(0' in l)


def _cur(S):
    line = S.get('_line') or 0
    if line >= DEC_LINE and 'now_node' in S and 'now_cnt' in S and 'dis' in S and S.get('now_state') in S['dis']:
        return S['now_node'], S['now_cnt']
    return None


def _draw(cv, S, B, box, T):
    cur = _cur(S)
    line = S.get('_line') or 0
    nxt = S.get('next_node') if cur and line >= FOR_LINE and line < RET_LINE + 12 and 'next_node' in S else None
    charging = cur and 'heap' in S and line > FOR_LINE + 5

    def ncol(u):
        if cur and u == cur[0]:
            return T['green'] if line == RET_LINE and u == END else T['blue']
        if u == END:
            return T['purple']
        return T['panel2']

    def nsub(u):
        if cur and u == cur[0]:
            return f'电{cur[1]}/{CNT} 充{CHARGE[u]}'
        tag = '起 ' if u == START else ('终 ' if u == END else '')
        return f'{tag}充{CHARGE[u]}'

    def ecol(u, v):
        if cur and nxt is not None and {u, v} == {cur[0], nxt} and line >= FOR_LINE + 1:
            return T['yellow'], 6
        return T['dim'], 3

    _graph(cv, T, box, POS, EDGES, ncol, nsub, ecol,
           '边权 = 路程；黄字：电 a/b = 电量/上限，充 = 每充 1 电耗时', directed=False)


def _grid(S):
    dis = S.get('dis')
    if dis is None:
        return None
    return [[dis.get(i * (CNT + 1) + j) for j in range(CNT + 1)] for i in range(N)]


def _text(S, B):
    cur = _cur(S)
    if cur is None:
        return '状态 = (城市, 剩余电量)：开车耗电、原地充电，都是新图里的边'
    return f"当前状态：城市 `{cur[0]}`，电量 `{cur[1]}`，已用时间 `{S['d']}`"


def _fmtheap(t):
    return f'({t[0]}|城{t[1] // (CNT + 1)}·电{t[1] % (CNT + 1)})'


def _skip(S, B, r):
    return f'`{S.now_state}`（城{S.now_state // (CNT + 1)}·电{S.now_state % (CNT + 1)}）==已经出过堆==，当时的时间更小 → 跳过'


_V = {}


def _forcap(S, B, r):
    k = S.now_state
    c = _V.get(k, 0)
    nb = list(S.g[S.now_node])
    if c >= len(nb):
        _V.pop(k, None)
        return f'城市 `{S.now_node}` 的邻居都看完了，再考虑原地充电'
    _V[k] = c + 1
    return f'枚举邻居城市 `{nb[c]}`'


def _drive(S, B, r):
    nn, w = S.next_node, S.g[S.now_node][S.next_node]
    if w <= S.now_cnt:
        return f'路程 `{w} <= {S.now_cnt}`（当前电量）→ ==电量够开到 {nn}=='
    return f'路程 `{w} > {S.now_cnt}` → 电量不够，这条路先不能走'


CONFIG = dict(
    num='LCP 35', title='电动车游城市', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='(城市, 电量) 状态 Dijkstra',
    tags=['灵神题单·图论算法'],
    code=CODE,
    call=f'Solution().electricCarPlan({PATHS}, {CNT}, {START}, {END}, {CHARGE})',
    expect=7,
    max_steps=76,
    views=[
        dict(type='text', fn=_text, h=56, size=24),
        dict(type='custom', draw=_draw, h=250),
        dict(type='grid', var=_grid, rows=list(range(N)), cols=list(range(CNT + 1)), h=260, cell=64,
             label='dis：已确定的最短时间（行 = 城市，列 = 电量）',
             color=lambda S, i, j, v: 'blue' if _cur(S) == (i, j) else None),
        dict(type='heap', var='heap', label='heap：(时间 | 城市·电量)', h=110, fmt=_fmtheap),
    ],
    watch=[('d', 'd', 'blue'), ('now_node', 'now_node', 'blue'), ('now_cnt', 'now_cnt', 'cyan'), ('next_node', 'next_node', 'yellow')],
    captions={
        'n = len(charge)': '`n = {n}` 座城市',
        'g = {index': '`g[x][y]`：x 到 y 的路程，用字典存',
        'for x, y, v in paths': lambda S, B, r: f'读第 `{S.paths.index([S.x, S.y, S.v]) + 1}` 条路 `{S.x} - {S.y}`，长 `{S.v}`',
        'if y not in g[x]': lambda S, B, r: ('`{}` 到 `{}` 还没有路 → 直接记下'.format(S.x, S.y) if S.y not in S.g[S.x] else '`{}` 到 `{}` 已经有路了 → ==重边==，要取较小的'.format(S.x, S.y)),
        'g[x][y] = g[y][x] = v': '无向边：`g[{x}][{y}]` 和 `g[{y}][{x}]` 都是 `{v}`',
        'g[x][y] = min': '重边取小：`g[{x}][{y}]` = =={g[x][y]}==',
        'g[y][x] = min': '反方向同步：`g[{y}][{x}]` = =={g[y][x]}==',
        'heap = [(0, start': '状态编码成一个整数 `node*(cnt+1)+电量`；起点：城市 {start}、电量 0，时间 0',
        'dis = {}': '`dis[状态]` 记录已经确定的最短时间',
        'while heap': lambda S, B, r: '堆非空，继续' if S.heap else '堆空了都没到终点 → 返回 -1',
        'heapq.heappop': '弹出时间最小的状态 `{now_state}`（城{now_state // (cnt + 1)}·电{now_state % (cnt + 1)}），时间 `{d}`',
        'if now_state in dis': lambda S, B, r: ('这个状态已经出过堆 → 成立' if S.now_state in S.dis else '这个状态第一次出堆 → 不成立，往下处理'),
        'continue': _skip,
        'dis[now_state] = d': '确定：状态 `{now_state}` 的最短时间 = =={d}==',
        'now_node, now_cnt =': '解码状态：城市 `{now_node}`，电量 `{now_cnt}`',
        'if now_node == end': lambda S, B, r: f'城市 `{S.now_node}`，终点是 `{S.end}`：' + ('==到终点了==' if S.now_node == S.end else '还没到'),
        'return d': '终点首次出堆，时间就是最短时间 ==`{d}`==',
        'for next_node in g[now_node]': _forcap,
        'if g[now_node][next_node] <= now_cnt': _drive,
        'next_cnt = ': '开到 `{next_node}` 后剩余电量：`{now_cnt} - {g[now_node][next_node]}` = =={next_cnt}==',
        'next_state = ': '新状态编码 `{next_node}*{cnt + 1}+{next_cnt}` = {next_state}',
        'heapq.heappush(heap, (d + g[now_node]': '开车：时间 `{d} + {g[now_node][next_node]}` = =={d + g[now_node][next_node]}==，入堆',
        'if now_cnt < cnt': lambda S, B, r: f'电量 `{S.now_cnt}` ' + (f'< 上限 `{S.cnt}` → 可以原地充 1 单位' if S.now_cnt < S.cnt else f'已满（上限 `{S.cnt}`），不能再充'),
        'now_state + 1': '原地充 1 电：时间 `{d} + {charge[now_node]}` = =={d + charge[now_node]}==，状态 +1（电量 +1）',
        'return -1': '堆空了：==到不了终点==，返回 -1',
    },
    cards=dict(
        one_liner='把「剩余电量」并进节点：状态 (城市, 电量) 上跑 Dijkstra',
        complexity='时间 `O(n·cnt·(deg + log))`，空间 `O(n·cnt)`',
        problem=['无向图，电动车电量上限 `cnt`，出发电量 0，行驶 1 单位路程耗电 1、耗时 1',
                 '城市 `i` 每充 1 单位电要花 `charge[i]` 时间；求 `start` 到 `end` 的最短时间',
                 f'本视频：3 座城市，`cnt = {CNT}`，路程 `[0-1: 1, 1-2: 2]`，另有一条重边 `0-1: 3`'],
        quote='直接将其与原图中的节点组合编码完全是可行。这样一来，就得到了一张新图，其中的每个节点都表示为(node, cnt)，表示当前处于原图中的node这个节点，且剩余油量为cnt。',
        quote_src='—— yiduobo 题解原文',
        idea=['新图每个点 `(node, cnt)`，两种边：开车去邻居（耗电 = 路程）、原地充 1 电（耗时 = `charge`）',
              '起点 `(start, 0)`，第一次弹出任意 `(end, *)` 就是答案',
              '题目有重边：建图时要取较小的路程'],
        summary=['时间约 `O(n·cnt·(deg + log))`，状态数 `n × (cnt+1)`',
                 '易错：重边必须取 `min`，否则可能用到更长的路',
                 '易错：充电每次只充 1 电（状态 +1），这样才能精确停在需要的电量',
                 '原文为 Python 2 写法，`now_state / (cnt + 1)` 已改为整除 `//`'],
    ),
)
