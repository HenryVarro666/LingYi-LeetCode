def _graph(cv, box, T, pos, edges, fill_fn, label_fn, sub_fn=None, title='', hot_edges=(), size=30, R=34):
    """pos: {node: (fx, fy)} 0..1; fill_fn(i)->颜色名/None; label_fn(i)->节点内文字; sub_fn(i)->节点下方小字"""
    x0, y0, x1, y1 = box
    if title:
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    W, H = x1 - x0 - 2 * (R + 40), y1 - y0 - 2 * (R + 50)
    P = {i: (x0 + R + 40 + fx * W, y0 + R + 50 + fy * H) for i, (fx, fy) in pos.items()}
    for a, b in edges:
        hot = (a, b) in hot_edges or (b, a) in hot_edges
        cv.line([P[a], P[b]], T['yellow'] if hot else T['border'], 6 if hot else 3)
    for i, (X, Y) in P.items():
        c = fill_fn(i)
        cv.rect((X - R, Y - R, X + R, Y + R), fill=T[c] if c else T['panel2'], outline=T['border'], r=R)
        cv.text((X, Y), label_fn(i), size, T['bg'] if c else T['text'], anchor='mm', bold=True)
        if sub_fn:
            s = sub_fn(i)
            if s:
                cv.text((X, Y + R + 8), s, 22, T['muted'], anchor='mt', bold=True)
_E = [(0, 1), (1, 2), (2, 3)]
_POS = {0: (.06, .5), 1: (.35, .5), 2: (.65, .5), 3: (.94, .5)}
_INF = 10 ** 9
_FRESH = {'f': False}


def _pop(S, B, r):
    _FRESH['f'] = True
    return f'取队首 `p = (节点 {S.p[0]+1}, 时间 {S.p[1]})`，出队后剩 `{len(S.q) - 1}` 个'


def _forw(S, B, r):
    fresh, _FRESH['f'] = _FRESH['f'], False
    if fresh or B.get('w') != S.w:
        return f'看节点 `{S.p[0]+1}` 的邻居 `{S.w+1}`'
    return f'节点 `{S.p[0]+1}` 的邻居看完了'


def _gdraw(cv, S, B, box, T):
    dis = S.get('dis')
    p = S.get('p')
    w = S.get('w') if 'w' in S and p is not None else None

    def f(i):
        if p is not None and i == p[0] and S.get('_line') is not None:
            return 'pink'
        if w is not None and i == w and S.get('_line') is not None:
            return 'yellow'
        if dis is None:
            return None
        if dis[i][1] < _INF:
            return 'green'
        if dis[i][0] < _INF and i != 0:
            return 'blue'
        return 'blue' if i == 0 else None

    def sub(i):
        if dis is None:
            return ''
        a, b = dis[i]
        return f"最短 {a if a < _INF else '∞'} · 次短 {b if b < _INF else '∞'}"
    _graph(cv, box, T, _POS, _E, f, lambda i: str(i + 1), sub, size=30,
           title='城市图（粉 = 出队 p，黄 = 邻居 w，蓝 = 有最短，绿 = 有次短）')


def _nxt(S, B):
    if 'p' not in S or S['p'] is None:
        return ''
    d = S['p'][1]
    ch, tm = S['change'], S['time']
    times = d // ch
    out = (times + 1) * ch + tm if times % 2 == 1 else d + tm
    st = '红灯，等到绿灯再走' if times % 2 == 1 else '绿灯，直接走'
    return f"出队时间 `d = {d}`：`{d} // {ch} = {times}` 次切换（{'奇数' if times % 2 else '偶数'}）→ {st} → 到达邻居的时间 =={out}=="


CONFIG = dict(
    num=2045, title='到达目的地的第二短时间', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='BFS 同时维护最短 / 次短时间（Go 原文转写）',
    tags=['灵神题单·图论算法', '难度分 2202'],
    code='''
class Solution:
    def secondMinimum(self, n: int, edges: List[List[int]], time: int, change: int) -> int:
        g = [[] for _ in range(n)]
        for e in edges:  # 建图
            v, w = e[0] - 1, e[1] - 1
            g[v].append(w)
            g[w].append(v)

        # 传入当前时间 d，返回到达下一个节点的时间
        def next(d: int) -> int:
            times = d // change
            if times % 2 == 1:  # 如果红绿灯切换次数为奇数，则现在是红灯
                return (times + 1) * change + time  # 等绿灯再出发
            return d + time  # 绿灯，直接出发

        dis = [[0, 0] for _ in range(n)]  # 距离数组同时存 [最短路, 次短路]
        dis[0][1] = int(1e9)
        for i in range(1, n):
            dis[i] = [int(1e9), int(1e9)]
        q = [(0, 0)]
        while len(q) > 0:  # BFS 求最短路和次短路
            p = q[0]  # 取队首
            q = q[1:]
            for w in g[p[0]]:
                d = next(p[1])  # 到达节点 w 的时间
                if d < dis[w][0]:  # d 比最短路小，就更新最短路
                    dis[w][0] = d
                    q.append((w, d))
                elif dis[w][0] < d < dis[w][1]:  # d 比最短路大又比次短路小，就更新次短路
                    dis[w][1] = d
                    q.append((w, d))
        return dis[n - 1][1]
''',
    call='Solution().secondMinimum(4, [[1,2],[2,3],[3,4]], 3, 5)',
    expect=23,
    views=[
        dict(type='custom', draw=_gdraw, h=400),
        dict(type='text', fn=_nxt, h=70, size=24),
        dict(type='queue', var='q', fmt=lambda x: f'节点{x[0]+1}@{x[1]}', label='队列 q（节点 @ 到达时间）', h=110),
    ],
    skip=['g = [[]', 'for e in edges', 'v, w = e[0]', 'g[v].append', 'g[w].append', 'for i in range(1, n)', 'dis[i] = [', 'dis[0][1]', 'times = d // change', 'q = q[1:]', 'dis[w][0] = d', 'dis[w][1] = d'],
    max_steps=62,
    watch=[('d', 'd', 'blue'), ('w', 'w', 'yellow'), ('ans', 'dis[n - 1]', 'green')] if False else ['d', 'w', ('终点次短', "'∞' if dis[n - 1][1] >= 10**9 else dis[n - 1][1]", 'green')],
    captions={
        'dis = [[0, 0]': '`dis[i]` = [最短, 次短] 到达时间；起点最短是 0，其余先设为很大（`1e9`）',
        'q = [(0, 0)]': '队列里放 `(节点, 到达时间)`，从节点 `1`（下标 0）、时间 0 出发',
        'while len(q)': lambda S, B, r: f'队列里还有 `{len(S.q)}` 个状态' if S.q else '队列空了：每个点的最短、次短都定下来了',
        'p = q[0]': _pop,
        'for w in g[p[0]]': _forw,
        'times % 2 == 1': lambda S, B, r: f'`times = {S.times}` 是奇数 → 现在是红灯' if S.times % 2 == 1 else f'`times = {S.times}` 是偶数 → 现在是绿灯',
        'return (times + 1)': '红灯：等到下一次绿灯 `({times}+1)×{change}` 再出发，加上 `time = {time}` → =={ret}==',
        'return d + time': '绿灯：直接出发，到达时间 `{d} + {time}` = =={ret}==',
        'd = next(p[1])': '调用 `next({p[1]})`：从节点 {p[0]+1} 出发，算到达邻居 {w+1} 的时间',
        'if d < dis[w][0]': lambda S, B, r: (f'`d = {S.d}` < 最短 `{S.dis[S.w][0]}` → 更新最短时间（`dis[{S.w+1}][0] = {S.d}`）' if S.d < S.dis[S.w][0] else f'`d = {S.d}` 不比最短 `{S.dis[S.w][0]}` 小'),
        'elif dis[w][0] < d': lambda S, B, r: (f'`{S.dis[S.w][0]} < {S.d} < 次短` → 严格大于最短又比次短小 → 更新次短时间（`dis[{S.w+1}][1] = {S.d}`）' if S.dis[S.w][0] < S.d < S.dis[S.w][1]
                                               else f'`d = {S.d}` 等于最短或不小于次短 `{S.dis[S.w][1] if S.dis[S.w][1] < 10**9 else "∞"}` → 丢弃'),
                'q.append((w, d))': lambda S, B, r: f'`dis[{S.w+1}]` = {S.dis[S.w][0]}/{S.dis[S.w][1] if S.dis[S.w][1] < _INF else "∞"} 已更新，`(节点 {S.w+1}, 时间 {S.d})` 入队：`q` 里共 `{len(S.q)}` 个',
        'return dis[n - 1]': '终点（节点 {n}）的次短到达时间 = `{dis[n - 1][1]}`',
    },
    cards=dict(
        one_liner='红绿灯固定，边数决定时间：转成求严格次短路的 BFS',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['无向图，走过每条边花 `time` 分钟，信号灯每 `change` 分钟变色，红灯时必须等绿灯才能离开',
                 '求从节点 `1` 到节点 `n` 的第二短时间（严格大于最短时间）',
                 '示例：`n=5, edges=[[1,2],[1,3],[1,4],[3,4],[4,5]], time=3, change=5` → `13`'],
        quote='由于 time 和 change 是固定的，经过多少条边就知道花费了多少时间。因此这题本质上可以看成边权均为 1 的图，我们要求的就是 1 到 n 的严格次短路的长度。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dis[v]` 同时存最短、次短两个到达时间，BFS 里每个点最多入队两次',
              '`next(d)`：先看 `d // change` 是奇数还是偶数，奇数是红灯，要等到下一次绿灯',
              '`d` 小于最短就更新最短；严格介于最短和次短之间就更新次短'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`q = q[1:]` 出队，`pair` 用元组 `(v, d)` 表示）',
                 '时间 `O(n + m)`，空间 `O(n + m)`',
                 '易错点：次短要严格大于最短（`dis[w][0] < d`），相等的不能算',
                 '更新了次短的点也要入队，因为从它出发的路可能给邻居带来新的次短',
                 '红灯等待只在 `next(d)` 里处理，`d` 的奇偶决定是否要等'],
    ),
)
