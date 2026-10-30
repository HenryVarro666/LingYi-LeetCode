import math as _m


def _fnum(v):
    if v is None:
        return '?'
    if isinstance(v, float) and _m.isinf(v):
        return '∞'
    return str(v)


def _gdraw(cv, box, T, pos, edges, ncol=None, nlab=None, ecol=None, elab=None, arrows=None, r=28, title=None, pad=70):
    """pos: [(fx,fy)]; edges: [(u,v,w)]; ncol(i)->(r,g,b)|None; nlab(i)->[str..] 画在节点下方;
    ecol(k)->((r,g,b), width)|None; elab(k)->str|None; arrows: set of (u,v) 有向画箭头"""
    x0, y0, x1, y1 = box
    if title:
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    ax0, ay0, ax1, ay1 = x0 + pad, y0 + 84, x1 - pad, y1 - 100
    P = [(ax0 + fx * (ax1 - ax0), ay0 + fy * (ay1 - ay0)) for fx, fy in pos]
    for k, (u, v, w) in enumerate(edges):
        c, wd = (ecol(k) if ecol else None) or (T['border'], 3)
        (xa, ya), (xb, yb) = P[u], P[v]
        L = _m.hypot(xb - xa, yb - ya) or 1
        ux, uy = (xb - xa) / L, (yb - ya) / L
        if arrows and (u, v) in arrows:
            cv.arrow((xa + ux * r, ya + uy * r), (xb - ux * (r + 4), yb - uy * (r + 4)), c, wd, head=16)
        elif arrows and (v, u) in arrows:
            cv.arrow((xb - ux * r, yb - uy * r), (xa + ux * (r + 4), ya + uy * (r + 4)), c, wd, head=16)
        else:
            cv.line([(xa, ya), (xb, yb)], c, wd)
    for k, (u, v, w) in enumerate(edges):
        t = elab(k) if elab else str(w)
        if t is None:
            continue
        c, wd = (ecol(k) if ecol else None) or (T['border'], 3)
        mx, my = (P[u][0] + P[v][0]) / 2, (P[u][1] + P[v][1]) / 2
        tw = cv.tlen(t, 22, bold=True) + 14
        cv.rect((mx - tw / 2, my - 15, mx + tw / 2, my + 15), fill=T['panel'], r=8)
        cv.text((mx, my), t, 22, c if c != T['border'] else T['muted'], anchor='mm', bold=True)
    for i, (X, Y) in enumerate(P):
        c = ncol(i) if ncol else None
        cv.d.ellipse((X - r, Y - r, X + r, Y + r), fill=c or T['panel2'], outline=T['border'] if not c else c, width=3)
        cv.text((X, Y), i if not isinstance(i, str) else i, 28, T['bg'] if c else T['text'], anchor='mm', bold=True, mono=True)
        for j, s in enumerate((nlab(i) if nlab else []) or []):
            if isinstance(s, tuple):
                s, sc = s
            else:
                sc = T['muted']
            cv.text((X, Y + r + 6 + j * 24), s, 20, sc, anchor='mt', bold=True, mono=True)

N = 4
ROADS = [[0, 1, 1], [0, 2, 2], [1, 2, 1], [1, 3, 3], [2, 3, 2]]
POS = [(0.0, 0.5), (0.5, 0.0), (0.5, 1.0), (1.0, 0.5)]


def _draw(cv, S, B, box, T):
    dis, cnt = S.get('dis'), S.get('cnt')
    heap = S.get('heap') or []
    inheap = {p[1] for p in heap}
    cur = S.get('now_node')
    pre = S.get('pre_node')
    nxt = S.get('next_node')
    line = S.get('_line', 0)
    hot = None
    if cur is not None and 'next_node' in S and 26 <= line <= 27 and nxt is not None:
        hot = {cur, nxt}
    elif cur is not None and pre is not None:
        hot = {cur, pre}

    def ncol(i):
        if dis is None:
            return None
        if i == cur:
            return T['pink']
        if hot and 'next_node' in S and 26 <= line <= 27 and i == nxt:
            return T['blue']
        if dis[i] is not None:
            return T['green']
        return T['yellow'] if i in inheap else None

    def ecol(k):
        u, v, w = ROADS[k]
        if hot and {u, v} == hot:
            return (T['yellow'], 6)
        return None

    def nlab(i):
        if dis is None:
            return []
        return [(f'dis={_fnum(dis[i])}', T['cyan']), (f'cnt={cnt[i]}', T['green'])]
    _gdraw(cv, box, T, POS, ROADS, ncol=ncol, nlab=nlab, ecol=ecol, r=30,
           title='粉 = 刚弹出的点　蓝 = 正在入堆的邻居　黄 = 在堆里　绿 = 已确定')


CONFIG = dict(
    num=1976, title='到达目的地的方案数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='Dijkstra 记录来源 · 距离相等时累加条数',
    tags=['图论算法', '难度分 2095'],
    code='''
class Solution(object):
    def countPaths(self, n, roads):

        dis = [None] * n
        cnt = [0] * n

        g = {}
        for x, y, t in roads:
            if x not in g:
                g[x] = {}
            if y not in g:
                g[y] = {}
            g[x][y] = t
            g[y][x] = t
        
        mod = 10 ** 9 + 7
        heap = [(0, 0, None)]
        while heap:
            now_t, now_node, pre_node = heapq.heappop(heap)
            if dis[now_node] is None:
                dis[now_node] = now_t
                if pre_node is None:
                    cnt[now_node] = 1
                else:
                    cnt[now_node] = cnt[pre_node]
                for next_node, next_t in g.get(now_node, {}).items():
                    heapq.heappush(heap, [now_t + next_t, next_node, now_node])
            elif dis[now_node] == now_t:
                cnt[now_node] += cnt[pre_node]
                if cnt[now_node] >= mod:
                    cnt[now_node] -= mod
        
        return cnt[-1]
''',
    call=f'Solution().countPaths({N}, {ROADS})',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='heap', var='heap', fmt=lambda p: f'{p[1]}:{p[0]}←{p[2]}', label='堆（点:距离←来源）', top_color='purple', h=110),
    ],
    watch=[('now_t', 'now_t', 'purple'), ('now_node', 'now_node', 'pink'), ('pre_node', 'pre_node', 'orange'),
           ('cnt[n-1]', lambda S: S['cnt'][N - 1] if 'cnt' in S else None, 'green')],
    skip=['dis = [None]', 'cnt = [0]', 'g = {}', 'for x, y, t in roads', 'if x not in g', 'g[x] = {}', 'if y not in g',
          'g[y] = {}', 'g[x][y] = t', 'g[y][x] = t', 'mod = 10'],
    captions={
        'heap = [(0, 0, None)]': '堆里放三元组 `(距离, 点, 来源)`：起点 `(0, 0, None)`，没有来源。`dis` 记最短距离，`cnt` 记最短路条数',
        'while heap': lambda S, B, r: (f'堆里还有 {len(S.heap)} 项，继续弹出' if S.heap else '堆空了：所有点都处理完'),
        'heapq.heappop': '弹出 `({now_t}, {now_node}, 来源 {pre_node})`：距离最小的一项',
        'if dis[now_node] is None': lambda S, B, r: (f'`dis[{S.now_node}]` 还没有值：==第一次到达==，这个距离 `{S.now_t}` 就是最短路' if S.dis[S.now_node] is None
                                                     else f'`dis[{S.now_node}]` 已有值，看是否一样长'),
        'dis[now_node] = now_t': '确定 `dis[{now_node}] = {now_t}`',
        'if pre_node is None': lambda S, B, r: ('没有来源：这是起点' if S.pre_node is None else f'来源是 `{S.pre_node}`，不是起点'),
        'cnt[now_node] = 1': '起点原地不动算一种：`cnt[0] = 1`',
        'cnt[now_node] = cnt[pre_node]': '最短路是从 `{pre_node}` 走来的：`cnt[{now_node}] = cnt[{pre_node}]` = =={cnt[now_node]}==',
        'for next_node': lambda S, B, r: (f'`{S.now_node}` 的邻居都入堆了' if B.get('next_node') == S.next_node and B.get('now_node') == S.now_node
                                          else f'邻居 `{S.next_node}`，路长 `{S.next_t}`'),
        'heapq.heappush': '`{now_t} + {next_t}` = {now_t + next_t}：把 `({now_t + next_t}, {next_node}, 来源 {now_node})` 入堆，==连已确定的点也入堆==，为了发现“一样长”的路',
        'elif dis[now_node] == now_t': lambda S, B, r: (f'`dis[{S.now_node}] = {S.dis[S.now_node]}`，这次距离 `{S.now_t}`：==一样长==，又找到一批最短路' if S.dis[S.now_node] == S.now_t
                                                       else f'`dis[{S.now_node}] = {S.dis[S.now_node]} < {S.now_t}`：更长，不是最短路，丢弃'),
        'cnt[now_node] += cnt[pre_node]': '来源 `{pre_node}` 的条数也算上：`cnt[{now_node}]` = {B.cnt[now_node]} + {cnt[pre_node]} = =={cnt[now_node]}==',
        'if cnt[now_node] >= mod': '条数没超过 `mod`，不用减',
        'return cnt[-1]': '终点最短路条数 =={ret}==',
    },
    max_steps=120,
    cards=dict(
        one_liner='Dijkstra 多记一个来源：碰到一样长的路，就把来源的条数加上',
        complexity='时间 `O(m log m)`，空间 `O(n + m)`',
        problem=['`n` 个路口，双向道路带耗时；求从 `0` 到 `n-1` ==耗时最少==的路径条数，对 `10^9+7` 取模',
                 '边权都是正数，可以直接用 Dijkstra',
                 '本视频：`n=4`，点 2 和点 3 都有多条等长最短路'],
        quote='如果碰到已经更新过的节点，则需要判断当前距离是否等于已知的最短距离，若相等，则更新路径条数。',
        quote_src='—— yiduobo 题解原文',
        idea=['堆里除了距离和点，还要多存==来源 prev==',
              '第一次弹出某点：确定 `dis`，`cnt` 直接继承来源的 `cnt`',
              '再次弹出同一点且距离相等：`cnt += cnt[prev]`；更长的直接丢掉'],
        summary=['时间 `O(m log m)`，空间 `O(n + m)`',
                 '邻居==不管有没有处理过==都入堆，否则发现不了“一样长”的路',
                 '`cnt[pre_node]` 必须已经定型：边权为正，来源一定先于当前点出堆',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '对比灵神：灵神在更新 `dis` 时顺手更新 `f`，不用把来源放进堆'],
    ),
)
