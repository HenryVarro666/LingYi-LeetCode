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
EDGES = [(0, 1, 3), (3, 1, 1), (2, 3, 4), (0, 2, 2), (3, 4, 2)]
POS = {0: (0.02, 0.5), 1: (0.36, 0.04), 2: (0.36, 0.96), 3: (0.68, 0.5), 4: (0.98, 0.5)}

CODE = '''
class Solution(object):
    def minCost(self, n, edges):
        
        g = [[] for _ in range(n)]
        for x, y, w in edges:
            g[x].append((y, w))
            g[y].append((x, w * 2))

        dis = [-1] * n
        heap = [(0, 0)]
        while heap:
            d, now = heapq.heappop(heap)
            if dis[now] != -1:
                continue
            dis[now] = d
            for nxt, w in g[now]:
                if dis[nxt] == -1:
                    heapq.heappush(heap, (d + w, nxt))
                    
        return dis[-1]
'''
_L = CODE.strip('\n').split('\n')
FOR_LINE = next(i + 1 for i, l in enumerate(_L) if 'for nxt, w in g[now]' in l)


def _fwd(x, y, w):
    return any(e[0] == x and e[1] == y and e[2] == w for e in EDGES)


def _draw(cv, S, B, box, T):
    dis = S.get('dis')
    line = S.get('_line')
    heap = S.get('heap') or []
    inheap = {e[1] for e in heap}
    x = S.get('now') if 'd' in S else None
    y = S.get('nxt') if line in (FOR_LINE, FOR_LINE + 1, FOR_LINE + 2) and 'nxt' in S else None
    w = S.get('w')
    active = line is not None and 11 <= line <= FOR_LINE + 2

    def ncol(u):
        if dis is None:
            return T['panel2']
        if u == x and active and dis[u] != -1:
            return T['blue']
        if dis[u] != -1:
            return T['green']
        if u in inheap:
            return T['orange']
        return T['panel2']

    def nsub(u):
        return None if dis is None else f"dis={'-' if dis[u] < 0 else dis[u]}"

    def ecol(u, v):
        if y is not None and ((u == x and v == y and _fwd(x, y, w)) or (v == x and u == y and not _fwd(x, y, w))):
            return T['yellow'], 6
        return T['dim'], 3

    _graph(cv, T, box, POS, EDGES, ncol, nsub, ecol, '绿 = 出堆定值，橙 = 在堆里，灰 = 没到；黄边 = 正在走的边')


def _text(S, B):
    line = S.get('_line')
    if 'nxt' in S and line in (FOR_LINE + 1, FOR_LINE + 2):
        x, y, w = S['now'], S['nxt'], S['w']
        how = '原边' if _fwd(x, y, w) else f'原边 `{y} → {x}` 反转，成本 `2×{w // 2}`'
        return f"`{x} → {y}`：{how}，到 `{y}` 总成本 `{S['d'] + w}`"
    if 'd' in S:
        return f"出堆：`d = {S['d']}`，`now = {S['now']}`"
    return '每条边建两份：正向 `w`，反向 `w * 2`'


def _chk(S, B, r):
    if S.dis[S.now] != -1:
        return f'`dis[{S.now}] = {S.dis[S.now]}` 已定 → ==重复记录，跳过=='
    return f'`dis[{S.now}] == -1`：节点 {S.now} 第一次出堆'


def _for(S, B, r):
    if 'nxt' in B and (B.now, B.nxt, B.w) == (S.now, S.nxt, S.w):
        return f'`{S.now}` 的边都看完了'
    how = '原边' if _fwd(S.now, S.nxt, S.w) else '==反转边（w 已乘 2）=='
    return f'看 `{S.now} → {S.nxt}`：{how}，边权 `{S.w}`'


def _in(S, B, r):
    if S.dis[S.nxt] == -1:
        return f'`dis[{S.nxt}] == -1`：还没定 → 入堆候选 `({S.d + S.w}, {S.nxt})`'
    return f'`dis[{S.nxt}] = {S.dis[S.nxt]}` 已定 → 不用再入堆'


CONFIG = dict(
    num=3650, title='边反转的最小路径总成本', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='建反向 2w 边 + 标准 Dijkstra',
    tags=['灵神题单·图论算法', '难度分 1854'],
    code=CODE,
    call=f'Solution().minCost({N}, {[list(e) for e in EDGES]})',
    expect=7,
    skip=['for x, y, w in edges', 'g[x].append', 'g[y].append', 'dis = [-1]', 'heap = [(0, 0)]', 'g = [[]'],
    max_steps=90,
    views=[
        dict(type='text', fn=_text, h=56, size=24),
        dict(type='custom', draw=_draw, h=370),
        dict(type='array', var=lambda S: list(S['dis']) if 'dis' in S else None, label='dis[i]：最小成本（-1 = 还没定）', h=150, cell=90,
             color=lambda S, i, v: 'green' if v >= 0 else None),
        dict(type='heap', var='heap', label='heap（元素 = (成本, 节点)）', h=130, fmt=lambda t: f'({t[0]},{t[1]})'),
    ],
    watch=[('d', 'd', 'blue'), ('now', 'now', 'blue'), ('nxt', 'nxt', 'yellow'), ('w', 'w')],
    captions={
        'while heap': lambda S, B, r: '堆非空，继续' if S.heap else '堆空了：能到的点都定值了',
        'd, now = heapq.heappop': '弹出 `({d}, {now})`：成本最小的记录',
        'if dis[now] != -1': _chk,
        'continue': '这个点最短路已定，旧记录直接扔掉',
        'dis[now] = d': '`dis[{now}] = {d}`：==第一次出堆的 d 就是最短路==',
        'for nxt, w in g[now]': _for,
        'if dis[nxt] == -1': _in,
        'heapq.heappush': '`({d + w}, {nxt})` 入堆',
        'return dis[-1]': '`dis[-1] = dis[{n - 1}]`：终点的最小成本 `{dis[-1]}`',
    },
    cards=dict(
        one_liner='开关只能用一次？最优路径本来就不会重复经过同一点',
        complexity='时间 `O(n + m log m)`，空间 `O(n + m)`',
        problem=['有向带权图，到节点后可以用开关把一条入边反转并穿过，成本 `2w`',
                 '每个节点的开关最多用一次，求 `0` 到 `n-1` 的最小成本',
                 '本视频：5 个点，答案 `7`（反转了 `3→1` 这条边）'],
        quote='由于在最优路径上每个节点也最多经过一次，因此这个开关只能用一次的条件可以直接无视，而使用开关就相当于在原始(u, v, w)的基础上，新建立了一条(v, u, w * 2)的边。',
        quote_src='—— yiduobo 题解原文',
        idea=['不考虑开关，就是标准的最短路问题',
              '最优路径每个点最多经过一次 → 「开关最多用一次」可以忽略',
              '建图时每条边多加一条反向边 `w * 2`，再跑一遍 Dijkstra'],
        summary=['时间 `O(n + m log m)`，空间 `O(n + m)`',
                 '原文用 `dis[now] != -1` 标记已出堆，入堆前再过滤一次已定的点',
                 '不提前返回：堆跑空，最后返回 `dis[-1]`',
                 '终点不可达时 `dis[-1]` 保持 -1，正好符合题意'],
    ),
)
