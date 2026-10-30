import math as _m

TIMES = [[2, 1, 1], [2, 3, 4], [1, 3, 2], [3, 4, 1], [1, 4, 5]]
N, K = 4, 2
POS = {2: (0.04, 0.5), 1: (0.42, 0.06), 3: (0.42, 0.94), 4: (0.96, 0.5)}


def _graph(cv, T, box, pos, edges, ncol, nsub, ecol, title):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    R = 32
    L, Rr, Tp, Bt = x0 + 70, x1 - 70, y0 + 64 + R, y1 - R - 30
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
                cv.text((px, py - R - 4), s, 20, T['green'], anchor='mb', bold=True, mono=True)
            else:
                cv.text((px, py + R + 4), s, 20, T['green'], anchor='mt', bold=True, mono=True)


LOOP = (16, 17, 18)


def _draw(cv, S, B, box, T):
    res = S.get('res')
    live = res is not None and 'heap' in S
    u = S.get('u') if live and 'dis' in S else None
    v = S.get('v') if S.get('_line') in LOOP else None

    def ncol(x):
        if not live:
            return T['panel2']
        if x == u and S.get('_line') not in (20, 21, 23):
            return T['blue']
        return T['green'] if x in res else T['panel2']

    def nsub(x):
        return f'res={res[x]}' if live and x in res else None

    def ecol(a, b):
        if a == u and b == v:
            return T['yellow'], 5
        return T['dim'], 3

    _graph(cv, T, box, POS, [tuple(e) for e in TIMES], ncol, nsub, ecol,
           '有向图（蓝 = 刚弹出的 u，绿 = 已加入答案 res）')


def _text(S):
    if 'res' not in S or 'heap' not in S:
        return '`edge[u][v] = w`：从 u 出发的边'
    if not S['res']:
        return '答案 `res` 还是空的：先把起点放进堆'
    done = '、'.join(f"`{k}:{v}`" for k, v in S['res'].items())
    return f"已确定最短距离：{done}"


def _new(S, B, r):
    if S.u in S.res:
        return f'`{S.u}` ==已经在答案中==：这是更远的旧记录，丢掉，继续弹'
    return f'`{S.u}` 不在答案中 → 它就是当前离 `{S.K}` ==最近==的点'


def _for(S, B, r):
    items = list(S.edge.get(S.u, {}).items())
    if (S.get('v'), S.get('w')) not in items:
        return f'`{S.u}` 没有出边'
    if 'v' in B and (B.v, B.w) == (S.v, S.w):
        return f'`{S.u}` 的出边都处理完了'
    return f'看边 `{S.u} → {S.v}`，权重 `{S.w}`'


def _vin(S, B, r):
    if S.v in S.res:
        return f'`{S.v}` 已在答案中，最短距离定了，==不用再入堆=='
    return f'`{S.v}` 还没确定：候选距离 `{S.dis} + {S.w} = {S.dis + S.w}`'


CONFIG = dict(
    num=743, title='网络延迟时间', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='Dijkstra · 二叉堆',
    tags=['labuladong', '灵神题单·图论算法'],
    code='''
class Solution(object):
    def networkDelayTime(self, times, N, K):
        edge = {}
        for u, v, w in times:
            if u not in edge:
                edge[u] = {}
            edge[u][v] = w

        res = {}
        heap = [[0, K]]

        while heap:
            dis, u = heapq.heappop(heap)
            if u not in res:
                res[u] = dis
                for v, w in edge.get(u, {}).items():
                    if v not in res:
                        heapq.heappush(heap, [dis + w, v])

        if len(res) != N:
            return -1
        else:
            return max(res.values())
''',
    call=f'Solution().networkDelayTime({TIMES}, {N}, {K})',
    expect=4,
    skip=['for u, v, w in times', 'if u not in edge', 'edge[u] = {}', 'edge[u][v] = w'],
    views=[
        dict(type='text', fn=_text, h=56, size=24),
        dict(type='custom', draw=_draw, h=400),
        dict(type='heap', var='heap', label='heap（元素 = [到起点距离, 节点]）', h=130,
             fmt=lambda t: f'[{t[0]},{t[1]}]'),
        dict(type='map', var='res', label='res（节点 → 最短距离）', h=130),
    ],
    watch=[('dis', 'dis', 'orange'), ('u', 'u', 'blue'), ('v', 'v', 'yellow'), ('w', 'w'),
           ('len(res)', lambda S: len(S['res']) if 'res' in S and 'heap' in S else None, 'green')],
    captions={
        'edge = {}': '用字典存图：`edge[u][v] = w`（已建好）',
        'res = {}': '`res[u]`：==已加入答案==的点和它的最短距离',
        'heap = [[0, K]]': '起点 `{K}` 距离为 0，入堆',
        'while heap': lambda S, B, r: '堆非空，继续' if S.heap else '堆空了：能到的点都已加入答案',
        'dis, u = heapq.heappop': '弹出堆顶 `[{dis}, {u}]`：堆里距离==最小==的',
        'if u not in res': _new,
        'res[u] = dis': '`res[{u}] = {dis}`：边权非负，==绕别的点只会更远==',
        'for v, w in edge.get': _for,
        'if v not in res': _vin,
        'heapq.heappush': '`[{dis + w}, {v}]` 入堆',
        'if len(res) != N': lambda S, B, r: (f'`len(res) = {len(S.res)}`，`N = {S.N}`：' +
                                             ('==所有点都收到了==' if len(S.res) == S.N else '有点到不了')),
        'return -1': '有节点收不到信号，返回 `-1`',
        'return max(res.values())': '最后收到信号的点决定总时间：`max` = =={ret}==',
    },
    cards=dict(
        one_liner='每次把离起点最近的点加入答案，再用它的出边更新别人',
        complexity='时间 `O(m log n)`，空间 `O(n + m)`',
        problem=['`N` 个节点（编号 1~N），`times[i] = (u, v, w)`：u 到 v 的有向边，传递时间 w',
                 '从 `K` 发出信号，多久==所有节点==都能收到？收不全返回 `-1`',
                 '示例：`[[2,1,1],[2,3,1],[3,4,1]], N=4, K=2` → `2`',
                 '本视频：`N=4, K=2`，5 条边 → `4`'],
        quote='若目前到p距离最短的点为q，那么p到q的距离就必然是dis[q]，而==不可能是p先经过某个中间点r==，然后从r再到q。',
        quote_src='—— yiduobo 题解原文',
        idea=['中间点 r 满足 `dis[r] ≥ dis[q]`，边权又非负 → 绕 r 不会更近',
              '用堆维护 `(u, dis)`：弹出的 u 已在答案中就继续弹',
              '不在答案中：记下 `res[u]`，把出边终点 `[dis + w, v]` 入堆'],
        summary=['时间 `O(m log n)`：每条边至多入堆出堆一次；朴素写法 `O(n^2)`',
                 '和灵神写法的区别：不维护 dis 数组，==出堆时才判断==是否已确定',
                 '最后用 `len(res) != N` 判断是否所有点都能到',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改',
                 '原文提到斐波那契堆可做到更优复杂度，但常数大、实际很少用'],
    ),
)
