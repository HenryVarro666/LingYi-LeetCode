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
_D = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3}


def _fill(S):
    def f(i):
        if 'v' in S and S.get('_in_loop') and S['v'] == i:
            return 'pink'
        if 'tmp' in S and i in S['tmp']:
            return 'yellow' if 'd' in S and _D[i] == S['d'] else 'green'
        if 'q' in S and i in S['q']:
            return 'blue'
        if 'vis' in S and S['vis'][i]:
            return 'green'
        return None
    return f


def _gdraw(cv, S, B, box, T):
    f = _fill(S)
    if 'v' in S and 'tmp' in S and S['v'] in S['tmp']:
        S = dict(S); S['_in_loop'] = True
        f = _fill(S)
    _graph(cv, box, T, _POS, _E, f, lambda i: str(i), lambda i: ('主服务器' if i == 0 else f'patience={_P[i]}'),
           title='网络图（粉 = 当前 v，黄 = 本层 tmp，蓝 = 下一层 q，绿 = 已访问）')


def _calc(S, B):
    if 'v' not in S or 'tmp' not in S or S['v'] not in S['tmp'] or S['v'] == 0 or 'd' not in S:
        return ''
    d, p = S['d'], _P[S['v']]
    t = p if 2 * d % p == 0 else 2 * d % p
    return f"节点 `{S['v']}`：d = {d}，p = {p}，t = {t}，空闲时刻 `4×{d}−{t}+1` = =={4*d-t+1}=="


CONFIG = dict(
    num=2039, title='网络空闲的时刻', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='BFS 求层数 d + 公式算空闲时刻（Go 原文转写）',
    tags=['灵神题单·图论算法', '难度分 1865'],
    code='''
class Solution:
    def networkBecomesIdle(self, edges: List[List[int]], patience: List[int]) -> int:
        ans = 0
        n = len(patience)
        g = [[] for _ in range(n)]
        for e in edges:
            v, w = e[0], e[1]
            g[v].append(w)
            g[w].append(v)

        vis = [False] * n
        vis[0] = True
        q = [0]
        d = 0
        while q:
            tmp = q
            q = []
            for v in tmp:
                if v > 0:
                    p = patience[v]
                    t = p  # 计算最后一条消息发出的秒数
                    if 2 * d % p > 0:
                        t = 2 * d % p
                    ans = max(ans, 4 * d - t + 1)
                for w in g[v]:
                    if not vis[w]:
                        vis[w] = True
                        q.append(w)
            d += 1
        return ans
''',
    call='Solution().networkBecomesIdle([[0,1],[0,2],[1,3],[2,4],[4,5]], [0,2,3,1,4,2])',
    expect=11,
    views=[
        dict(type='custom', draw=_gdraw, h=380),
        dict(type='text', fn=_calc, h=60, size=28),
        dict(type='queue', var='tmp', label='本层 tmp（距离 = d）', h=110),
        dict(type='queue', var='q', label='下一层 q', h=110),
    ],
    skip=['ans = 0', 'n = len', 'g = [[]', 'for e in edges', 'v, w = e[0]', 'g[v].append', 'g[w].append', 'vis = [False]', 'vis[w] = True', 't = p', 'q = []'],
    max_steps=78,
    watch=['d', 'v', 'p', 't', ('ans', 'ans', 'green')],
    captions={
        'vis[0] = True': '从主服务器 `0` 开始 BFS（先按 `edges` 建好邻接表 `g`），标记已访问',
        'q = [0]': '队列初始只有 `0`，当前层数 `d = 0`',
        'while q': lambda S, B, r: f'队列非空，处理第 `d = {S.d}` 层' if S.q else '队列空了，所有节点都处理过 → 结束',
        'tmp = q': '`tmp` 是本层所有节点 `{tmp}`，它们到 `0` 的最短路都是 `d = {d}`',
        'q = []': '`q` 清空，用来收集下一层',
        'for v in tmp': lambda S, B, r: f'取本层节点 `v = {S.v}`' if B.get('v') != S.v else '本层节点处理完',
        'if v > 0': lambda S, B, r: f'`v = {S.v} > 0` → 是数据服务器，要算它的空闲时刻' if S.v > 0 else '`v = 0` 是主服务器，不发消息，跳过',
        'p = patience[v]': '`p = patience[{v}] = {p}`：每 `p` 秒重发一次',
        't = p': '先假设 `p` 整除 `2d`：最后一条消息恰好发出 `p` 秒（`t = {t}`）',
        'if 2 * d % p': lambda S, B, r: (f'`2d % p = {2*S.d} % {S.p} = {2*S.d % S.p}` > 0 → 不整除，最后一条消息发出了 `2d mod p` 秒'
                                          if 2 * S.d % S.p > 0 else f'`2d % p = {2*S.d} % {S.p} = 0` → 整除，`t` 保持 `p`'),
        't = 2 * d % p': '`t = 2d mod p = {t}`：最后一次重发离首条回复还差的秒数',
        'ans = max': '首条回复在 `2d` 秒到，最后回复在 `4d − t` 秒到，下一秒空闲：`4×{d}−{t}+1 = {4*d-t+1}`，`ans = {ans}`',
        'for w in g[v]': lambda S, B, r: f'看 `v = {S.v}` 的邻居 `w = {S.w}`' if not (B.get('w') == S.w and B.get('v') == S.v) else f'`{S.v}` 的邻居都看完了',
        'if not vis[w]': lambda S, B, r: f'`w = {S.w}` 还没访问 → 属于下一层' if not S.vis[S.w] else f'`w = {S.w}` 已访问过，距离不会更短，跳过',
        'vis[w] = True': '标记 `{w}` 已访问',
        'q.append(w)': '标记 `{w}` 已访问并入队，它的距离是 `d + 1`：`q = {q}`',
        'd += 1': '本层处理完，层数 `d` → {d}',
        'return ans': '所有数据服务器空闲时刻的最大值 = `{ans}`',
    },
    cards=dict(
        one_liner='BFS 层数就是最短路 d，回复往返 2d，再用取余算最后一次重发',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['`n` 台服务器连成网络，`0` 号是主服务器，其余每台在 0 秒发信息并等回复',
                 '没收到回复时，服务器 `i` 每 `patience[i]` 秒重发一次',
                 '求网络变为空闲的最早秒数。示例：`edges=[[0,1],[1,2]], patience=[0,2,1]` → `8`',
                 '本视频：6 台服务器的小例子'],
        quote='用 BFS 求出 0 号节点到其余节点的最短路长度，在 BFS 的同时求出每个节点变为空闲状态的最早秒数，其最大值就是整个计算机网络变为空闲状态的时间。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`v` 到 `0` 的距离是 `d`，首条回复在 `2d` 秒到达',
              '`p` 整除 `2d`：最后一条消息发出了 `p` 秒；否则发出了 `2d mod p` 秒，记作 `t`',
              '最后一条回复到达时刻 `2d + (2d − t) = 4d − t`，下一秒才空闲，所以取 `4d − t + 1`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`q = nil` 对应 `q = []`）',
                 '时间 `O(n + m)`，空间 `O(n + m)`',
                 '易错点：`p` 整除 `2d` 时 `t` 取 `p` 而不是 0',
                 '主服务器 `0` 不发消息，要用 `v > 0` 跳过',
                 '答案是各节点空闲时刻的最大值，注意最后 `+1`'],
    ),
)
