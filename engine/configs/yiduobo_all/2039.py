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
_E = [[0,1],[0,2],[1,3],[2,4],[4,5]]
_P = [0,2,3,1,4,2]
_POS = {0: (0, .5), 1: (.33, .12), 2: (.33, .88), 3: (.66, .12), 4: (.66, .88), 5: (1, .88)}


def _gdraw(cv, S, B, box, T):
    dis = S.get('dis', {})
    now, nxt = S.get('now'), S.get('next')
    live = S.get('_line') is not None and 'q' in S

    def f(i):
        if i == now and 'l' in S and S['l'] > 1 or (i == now and now is not None):
            return 'pink'
        if i == nxt and i in dis:
            return 'yellow'
        if i in dis:
            return 'green'
        return None
    _graph(cv, box, T, _POS, _E, f, lambda i: str(i),
           lambda i: (f'dis={dis[i]}' if i in dis else ('主服务器' if i == 0 else '未访问')) + ('' if i == 0 else f'  p={_P[i]}'),
           title='网络图（粉 = 正在出队的 now，黄 = 刚发现的 next，绿 = 已有 dis）')


def _calc(S, B):
    nx = S.get('next')
    if nx is None or 'dis' not in S or nx not in S['dis'] or 'query_cnt' not in S:
        return ''
    d, p = S['dis'][nx], _P[nx]
    return f"节点 `{nx}`：dis = {d}，p = {p}，发 `{S['query_cnt']}` 条，最后一次收到回复在 `({S['query_cnt']}−1)×{p} + 2×{d}` = =={(S['query_cnt']-1)*p+2*d}=="


CONFIG = dict(
    num=2039, title='网络空闲的时刻', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='BFS 求距离 + 统计重发次数',
    tags=['灵神题单·图论算法', '难度分 1865'],
    code='''
class Solution(object):
    def networkBecomesIdle(self, edges, patience):

        g = {}
        for x, y in edges:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)

        dis = {0: 0}
        q = [0]
        l = 0
        r = 1
        res = 0
        while l < r:
            now = q[l]
            l += 1
            for next in g.get(now, set()):
                if next not in dis:
                    dis[next] = dis[now] + 1
                    query_cnt = (dis[next] + dis[next] - 1) // patience[next] + 1
                    res = max(res, (query_cnt - 1) * patience[next] + dis[next] + dis[next])
                    q.append(next)
                    r += 1
        
        return res + 1
''',
    call='Solution().networkBecomesIdle([[0,1],[0,2],[1,3],[2,4],[4,5]], [0,2,3,1,4,2])',
    expect=11,
    views=[
        dict(type='custom', draw=_gdraw, h=380),
        dict(type='text', fn=_calc, h=60, size=28),
        dict(type='array', var='q', pointers={'l': 'blue'}, label='队列 q（蓝箭头 = 队首 l）', h=130),
    ],
    skip=['g = {}', 'for x, y in edges', 'if x not in g', 'g[x] = set()', 'if y not in g', 'g[y] = set()', 'g[x].add', 'g[y].add', 'res = 0', 'r += 1'],
    max_steps=78,
    watch=[('l', 'l', 'blue'), 'r', 'now', 'next', ('query_cnt', 'query_cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'dis = {0: 0}': '`dis` 记录到主服务器的距离，`0` 的距离是 0（先按 `edges` 建好邻接表 `g`）',
        'q = [0]': '`q` 当队列，`[l, r)` 是待处理区间',
        'l = 0': '`l = 0` 是队首位置',
        'while l < r': lambda S, B, r_: f'`l = {S.l} < r = {S.r}`：队列里还有节点' if S.l < S.r else f'`l = {S.l} ≥ r = {S.r}`：队列空了 → BFS 结束',
        'now = q[l]': '出队 `now = q[{l}] = {now}`',
        'l += 1': '`l` → {l}',
        'for next in': lambda S, B, r_: f'看 `now = {S.now}` 的邻居 `next = {S.next}`' if B.get('next') != S.next or B.get('now') != S.now else f'`{S.now}` 的邻居看完了',
        'if next not in dis': lambda S, B, r_: (f'`{S.next}` 还没有距离 → 第一次到达，BFS 保证这就是最短距离' if S.next not in S.dis
                                                else f'`{S.next}` 已有 `dis = {S.dis[S.next]}` → 跳过'),
        'dis[next] = dis[now] + 1': '`dis[{next}] = dis[{now}] + 1 = {dis[next]}`',
        'query_cnt =': '回复要等 `2×dis = {2*dis[next]}` 秒，之前 `2×dis−1 = {2*dis[next]-1}` 秒内每 `{patience[next]}` 秒重发：共 `1 + {(2*dis[next]-1)//patience[next]}` = =={query_cnt}== 条',
        'res = max': '最后一次发送在 `({query_cnt}−1)×{patience[next]}` 秒，再加 `2×dis` 秒才收到回复 → `res = {res}`',
        'q.append(next)': '`{next}` 入队：`q = {q}`',
        'return res': '最后一条回复到达的最大时刻是 `{res}`，网络下一秒空闲 → `res + 1 = {res+1}`',
    },
    cards=dict(
        one_liner='每台服务器互不影响：算出它最后一次收到回复的时刻，取最大再加 1',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['`n` 台服务器，`0` 号是主服务器，其余每台在 0 秒发信息，收到回复前每 `patience[i]` 秒重发',
                 '求网络变为空闲的最早秒数',
                 '示例：`edges=[[0,1],[1,2]], patience=[0,2,1]` → `8`',
                 '本视频：6 台服务器的小例子'],
        quote='由于各个数据服务之间是互不影响的，因此只需要找出每个数据服务器接收最后一条回复的时间，其中的最大值就是网络中最后一个还有消息存在的时刻，那么这个时刻加上1就是最终答案了。',
        quote_src='—— yiduobo 题解原文',
        idea=['从 `0` 做 BFS 得到每台服务器的距离 `dis`，首次回复在 `2×dis` 秒到',
              '这之前的 `2×dis − 1` 秒里额外重发 `(2×dis−1) // p` 次，总共 `query_cnt` 条',
              '最后一次发送在 `(query_cnt − 1) × p`，再加 `2×dis` 就是最后一次回复到达的时刻'],
        summary=['原文为 Python 2 写法，`/` 是整数除法，已改为 `//`',
                 '时间 `O(n + m)`，空间 `O(n + m)`',
                 '易错点：重发只发生在首次回复之前的 `2×dis − 1` 秒，所以用 `2×dis − 1` 而不是 `2×dis`',
                 '最后的 `+ 1`：回复到达那一秒还算有消息，下一秒才空闲',
                 '对比灵神：他用 `2d mod p` 求最后一次发送距首条回复的秒数，公式 `4d − t + 1`；这里直接数重发条数'],
    ),
)
