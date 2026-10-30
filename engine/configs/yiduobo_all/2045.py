import math as _m

N0, EDGES0, TIME0, CHANGE0 = 5, [[1, 2], [1, 3], [1, 4], [3, 4], [4, 5]], 3, 5
POS = {0: (0.06, 0.5), 1: (0.36, 0.12), 2: (0.36, 0.88), 3: (0.66, 0.5), 4: (0.94, 0.5)}
EDG = [(x - 1, y - 1) for x, y in EDGES0]


def _dispv(v):
    return '?' if v is None else v


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    first, second = S.get('first'), S.get('second')
    now = S.get('now') if 'q' in S and 'next_t' in S or ('now' in S and 'l' in S and 'r' in S) else None
    nxt = S.get('next') if 'next_t' in S and S.get('_line') is not None else None
    cv.text((x0 + 18, y0 + 4), '城市图（边权都当 1）：节点旁 = first / second，绿 = 最短已到，橙 = 次短也到了，蓝 = 正在展开', 20, T['muted'], bold=True)
    R = 32
    Lx, Rx, Tp, Bt = x0 + 70, x1 - 70, y0 + 80 + R, y1 - R - 40
    P = {u: (Lx + fx * (Rx - Lx), Tp + fy * (Bt - Tp)) for u, (fx, fy) in POS.items()}
    for u, v in EDG:
        a, b = P[u], P[v]
        d = _m.hypot(b[0] - a[0], b[1] - a[1])
        ux, uy = (b[0] - a[0]) / d, (b[1] - a[1]) / d
        hot = (now is not None and nxt is not None and {u, v} == {now, nxt})
        cv.line([(a[0] + ux * R, a[1] + uy * R), (b[0] - ux * R, b[1] - uy * R)], T['yellow'] if hot else T['dim'], 6 if hot else 3)
    for u, (px, py) in P.items():
        if now is not None and u == now:
            fill = T['blue']
        elif second is not None and second[u] is not None:
            fill = T['orange']
        elif first is not None and first[u] is not None:
            fill = T['green']
        else:
            fill = T['panel2']
        cv.d.ellipse((px - R, py - R, px + R, py + R), fill=fill, outline=T['yellow'] if (nxt == u) else T['border'], width=4 if nxt == u else 2)
        cv.text((px, py), u + 1, 28, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)
        if first is not None:
            s = f'{_dispv(first[u])} / {_dispv(second[u])}'
            if py < (Tp + Bt) / 2 - 5:
                cv.text((px, py - R - 6), s, 22, T['yellow'], anchor='mb', bold=True, mono=True)
            else:
                cv.text((px, py + R + 6), s, 22, T['yellow'], anchor='mt', bold=True, mono=True)


def _txt(S, B):
    if 'res' in S and 'index' in S:
        k = S['res'] // CHANGE0
        return (f"第二步：每走一条边加 `time = {TIME0}`；已用 `res = {S['res']}`，含 `k = {k}` 个 change（{'奇数 → 红灯，要等' if k % 2 else '偶数 → 绿灯，直接走'}）")
    if 'first' in S and S.get('first') is not None and 'next' not in S:
        return '第一步：把图当成边权 1，用 BFS 找 1 到 n 的次短边数（每点两次机会）'
    return '节点编号减 1；`first` / `second`：到该点的最短、次短边数'


def _cap_res(S, B, r):
    k = B.res // S.change
    if k % 2 == 1:
        return f'`res // change = {k}`，奇数 → 红灯，==等到下次绿灯== `({k} + 1) * {S.change}` = {S.res}'
    return f'`res // change = {k}`，偶数 → 绿灯，不用等'


CONFIG = dict(
    num=2045, title='到达目的地的第二短时间', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='BFS 次短路 + 红绿灯模拟',
    tags=['灵神题单·图论算法', '难度分 2202'],
    code='''
class Solution(object):
    def secondMinimum(self, n, edges, time, change):

        g = {x : set() for x in range(n)}
        for x, y in edges:
            x -= 1
            y -= 1
            g[x].add(y)
            g[y].add(x)

        first = [None] * n
        second = [None] * n
        first[0] = 0
        q = [(0, 0)]
        l = 0
        r = 1
        while l < r:
            now, t = q[l]
            l += 1
            for next in g[now]:
                next_t = t + 1
                if first[next] is None:
                    first[next] = next_t
                    q.append((next, next_t))
                    r += 1
                elif second[next] is None and first[next] < next_t:
                    second[next] = next_t
                    q.append((next, next_t))
                    r += 1
        
        res = 0
        for index in range(second[-1]):
            if (res // change) % 2 == 1:
                res = (res // change + 1) * change
            res += time

        return res
''',
    call=f'Solution().secondMinimum({N0}, {EDGES0}, {TIME0}, {CHANGE0})',
    expect=13,
    max_steps=66,
    skip=['x -= 1', 'y -= 1', 'g[x].add', 'g[y].add', 'for x, y in edges', 'g = {x', 'l += 1', 'r += 1', 'l = 0', 'r = 1'],
    views=[
        dict(type='text', fn=_txt, h=50, size=22),
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var=lambda S: [_dispv(v) for v in S['first']] if S.get('first') is not None else None,
             label='first[i]：最短边数（节点 i+1）', h=135, cell=64),
        dict(type='array', var=lambda S: [_dispv(v) for v in S['second']] if S.get('second') is not None else None,
             label='second[i]：次短边数（严格更大）', h=135, cell=64),
        dict(type='queue', var=lambda S: S.get('q'), label='q（BFS 队列，元素 = (节点, 边数)）', h=100, fmt=lambda p: f'({p[0]},{p[1]})'),
    ],
    watch=[('now', 'now', 'blue'), ('t', 't'), ('next', 'next', 'yellow'), ('next_t', 'next_t', 'orange'), ('res', 'res', 'green'), ('index', 'index')],
    captions={
        'first = [None]': '`first[i]`：到 i 的==最短==边数，`None` = 还没到过',
        'second = [None]': '`second[i]`：到 i 的==次短==边数（严格大于最短）',
        'first[0] = 0': '起点 0 号（原图 1 号）：最短 `0` 条边',
        'q = [(0, 0)]': '队列放 `(节点, 边数)`，用列表 + 下标 `l` 当队头',
        'while l < r': lambda S, B, r: '队列没空，继续取队头' if S.l < S.r else 'BFS 结束：每个点最短、次短都求出来了',
        'now, t = q[l]': '取队头 `now = {now}`（原图 {now + 1} 号），已走 `t = {t}` 条边',
        'for next in g[now]': lambda S, B, r: f'`{S.now}` 的邻居都看完了' if ('next' in B and B.next == S.next and B.now == S.now) else f'看相邻的 `{S.next}`（原图 {S.next + 1} 号）',
        'next_t = t + 1': '走一条边：`next_t = {t} + 1 = {next_t}`',
        'if first[next] is None': lambda S, B, r: f'`first[{S.next}]` 为空 → 第一次到，==这就是最短== `{S.next_t}`' if S.first[S.next] is None else f'`first[{S.next}] = {S.first[S.next]}` 已有最短，看看能不能当次短',
        'first[next] = next_t': '记下最短：`first[{next}] = {next_t}`',
        'elif second[next] is None': lambda S, B, r: (f'`second[{S.next}]` 为空，且 `first = {S.first[S.next]} < {S.next_t}`：==严格更大 → 次短==' if (S.second[S.next] is None and S.first[S.next] < S.next_t) else (f'`second[{S.next}]` 已有次短，不再收' if S.second[S.next] is not None else f'`{S.next_t}` 不比最短 `{S.first[S.next]}` 大，不能当次短')),
        'second[next] = next_t': '记下次短：`second[{next}] = {next_t}`',
        'q.append': '`({next}, {next_t})` 入队，之后从它继续扩展',
        'res = 0': '第二步：边数已知，现在按红绿灯算时间。起点绿灯，`res = 0`',
        'for index in range': lambda S, B, r: '`second[-1]` 条边都走完了' if ('index' in B and B.index == S.index) else f'第 `{S.index + 1}` 条边（共 `second[-1] = {S.second[-1]}` 条）',
        'if (res // change) % 2': lambda S, B, r: f'`res // change = {S.res // S.change}`：' + ('奇数 → 现在是红灯' if (S.res // S.change) % 2 else '偶数 → 现在是绿灯'),
        'res = (res // change + 1)': '红灯要等到下一个绿灯：`(k + 1) * change` = =={res}==',
        'res += time': '穿过一条边：`res += {time}` → =={res}==',
        'return res': '走完 `second[-1]` 条边，总时间 =={ret}==',
    },
    cards=dict(
        one_liner='红绿灯先放一边：图当成边权 1，BFS 求次短边数，再按灯算时间',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['`n` 个路口，双向边，过一条边花 `time` 分钟；红绿灯每 `change` 分钟同时变色',
                 '绿灯才能离开，红灯要等；求节点 1 到 n 的==第二短时间==（严格大于最短）',
                 '示例：`n=5`，`time=3`，`change=5` → 最短 6，第二短 `13`'],
        quote='若满足dis[u] <= dis[v]，那么即使按最短路径到达u因为等红灯耽误了，从u出发的时间也不会比从v出发的时间更晚。……在这里还是使用bfs来得最方便。',
        quote_src='—— yiduobo 题解',
        idea=['所有灯同时变、边权相同 → ==先到的点后面也不会更晚==，可以先忽略红绿灯',
              '次短路 BFS：每个点给两次机会，第一次是最短，第二次是==严格更大==的次短',
              '得到次短边数后，从 0 开始逐条边累加 `time`；`res // change` 是奇数就等红灯'],
        summary=['时间 `O(n + m)`：每个点最多入队两次',
                 '易错：次短必须严格大于最短，所以 `first[next] < next_t` 不能写 `<=`',
                 '易错：红灯等待发生在==离开节点前==，先判断再加 `time`',
                 '原文为 Python 2 写法，整数除法 `res / change` 已改为 `res // change`（两处）',
                 '灵神题解仅供参考：同样用 BFS 看成边权为 1 的次短路'],
    ),
)
