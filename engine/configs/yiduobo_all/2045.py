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
_FRESH = {'f': False}


def _gdraw(cv, S, B, box, T):
    first, second = S.get('first'), S.get('second')
    now, nxt = S.get('now'), S.get('next')
    ing = 'l' in S and S.get('_line') is not None and S['_line'] < 30

    def f(i):
        if ing and now is not None and i == now:
            return 'pink'
        if ing and nxt is not None and i == nxt:
            return 'yellow'
        if second and second[i] is not None:
            return 'green'
        if first and first[i] is not None:
            return 'blue'
        return None

    def sub(i):
        if first is None:
            return ''
        a, b = first[i], second[i] if second else None
        return f"最短 {'∞' if a is None else a} · 次短 {'∞' if b is None else b}"
    _graph(cv, box, T, _POS, _E, f, lambda i: str(i + 1), sub,
           title='按边数（边权 1）：粉 = now，黄 = next，蓝 = 有最短，绿 = 有次短')


def _phase2(S, B):
    if 'index' not in S or 'second' not in S:
        return ''
    k = S['second'][-1]
    return f"BFS 得到终点次短路 `{k}` 条边；现在按 time = `{S['time']}`、change = `{S['change']}` 逐条边累加时间：第 `{S['index'] + 1}` / `{k}` 条，当前 `res = {S['res']}`"


def _pop(S, B, r):
    _FRESH['f'] = True
    return f'出队 `now = {S.now + 1}`，它的步数 `t = {S.t}`'


def _fornext(S, B, r):
    fresh, _FRESH['f'] = _FRESH['f'], False
    if fresh or B.get('next') != S.next:
        return f'看节点 `{S.now + 1}` 的邻居 `{S.next + 1}`'
    return f'节点 `{S.now + 1}` 的邻居看完了'


CONFIG = dict(
    num=2045, title='到达目的地的第二短时间', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='BFS 求次短路条数 + 红绿灯逐边累加',
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
    call='Solution().secondMinimum(4, [[1,2],[2,3],[3,4]], 3, 5)',
    expect=23,
    views=[
        dict(type='custom', draw=_gdraw, h=330),
        dict(type='queue', var='q', fmt=lambda x: f'节点{x[0]+1}:{x[1]}步', label='队列 q（节点:步数）', h=120),
        dict(type='text', fn=_phase2, h=110, size=24),
    ],
    skip=['g = {x', 'for x, y in edges', 'x -= 1', 'y -= 1', 'g[x].add', 'g[y].add', 'r += 1', 'l = 0', 'r = 1', 'first = [None]', 'l += 1'],
    max_steps=65,
    watch=['l', 'now', 'next', 'next_t', ('res', 'res', 'green')],
    captions={
        'second = [None]': '`first[i]` / `second[i]`：到节点 i 的最短 / 次短==边数==（先不管红绿灯）',
        'first[0] = 0': '起点（节点 1）的最短是 0 条边',
        'q = [(0, 0)]': '队列放 `(节点, 步数)`，`[l, r)` 是还没处理的区间',
        'while l < r': lambda S, B, r_: '队列里还有状态，继续' if S.l < S.r else 'BFS 结束：终点的次短条数已经有了',
        'now, t = q[l]': _pop,
        'for next in g[now]': _fornext,
        'next_t = t + 1': '走一条边：`next_t = {t} + 1 = {next_t}` 条边',
        'if first[next] is None': lambda S, B, r_: (f'节点 `{S.next + 1}` 第一次到达 → 这是最短' if S.first[S.next] is None else f'节点 `{S.next + 1}` 已有最短 `{S.first[S.next]}`，再看是不是次短'),
        'first[next] = next_t': '最短 `first[{next + 1}] = {first[next]}`',
        'elif second[next] is None': lambda S, B, r_: (f'次短还空着，且 `first = {S.first[S.next]} < {S.next_t}`（严格大于最短）→ 这就是次短' if S.second[S.next] is None and S.first[S.next] < S.next_t
                                                      else f'次短已有或不严格大于最短 `{S.first[S.next]}` → 丢弃'),
        'second[next] = next_t': '次短 `second[{next + 1}] = {second[next]}`，再入队一次',
        'q.append': '节点 `{next + 1}` 带着步数 `{next_t}` 入队：共 `{len(q)}` 个状态',
        'res = 0': '开始算时间：现在节点 `1`，`res = 0`',
        'for index in range': lambda S, B, r_: f'走第 `{S.index + 1}` 条边（共 `{S.second[-1]}` 条）' if B.get('index') != S.index else '全部边都走完了',
        'if (res // change) % 2 == 1': lambda S, B, r_: (f'`{S.res} // {S.change} = {S.res // S.change}`，奇数 → 现在是红灯，要等' if (S.res // S.change) % 2 == 1
                                                         else f'`{S.res} // {S.change} = {S.res // S.change}`，偶数 → 绿灯，直接走'),
        'res = (res // change + 1) * change': '等到下一次变绿：`({B.res} // {change} + 1) × {change} = {res}`',
        'res += time': '走完这条边：`res` += `{time}` → =={res}==',
        'return res': '第二短时间 = `{res}`',
    },
    cards=dict(
        one_liner='先忽略红绿灯，BFS 求次短路条数，再逐条边算时间',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['无向图，每条边耗时 `time`，所有信号灯每 `change` 分钟同步变色，红灯不能离开',
                 '求节点 `1` 到 `n` 的第二短时间（严格大于最短）',
                 '示例：`n=5, edges=[[1,2],[1,3],[1,4],[3,4],[4,5]], time=3, change=5` → `13`',
                 '本视频：4 个点的链 `1-2-3-4` → `23`'],
        quote='若某个节点之前被访问过，且当前这次的时间比之前得到的最短耗时要长，就说明当前时间就是到达该点的第二短时间。此时需要再次将该点加入到bfs队列中，同时设置该点之后不能再次访问。',
        quote_src='—— yiduobo 题解原文',
        idea=['所有灯同时变色、边权相同：先出发的不会比后出发的更晚，可以把边权当 1，红绿灯留到最后',
              '次短路：每个点给两次机会，`first` 记最短步数，`second` 记严格更大的下一个步数',
              '得到终点的次短步数 `k` 后，从 0 开始累加 `time`；已过 `change` 的次数为奇数就等到变绿'],
        summary=['原文为 Python 2 写法，`/` 是整数除法，已改为 `//`（共两处）',
                 '时间 `O(n + m)`，空间 `O(n + m)`',
                 '易错点：次短必须严格大于最短（`first[next] < next_t`）；每点最多入队两次',
                 '红灯判断是 `(res // change) % 2 == 1`，等到 `(res // change + 1) * change`',
                 '对比灵神：他把红绿灯放进 BFS 的时间里直接比较；这里先数边数，最后再模拟时间'],
    ),
)
