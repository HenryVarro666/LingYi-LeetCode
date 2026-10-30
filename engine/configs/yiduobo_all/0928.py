GRAPH = [[1, 1, 0, 1, 0, 0],
         [1, 1, 1, 0, 0, 0],
         [0, 1, 1, 0, 0, 1],
         [1, 0, 0, 1, 1, 0],
         [0, 0, 0, 1, 1, 0],
         [0, 0, 1, 0, 0, 1]]
INITIAL = [1, 5]
N = 6
ORI = {1: 'blue', 5: 'orange'}


def _pos(box):
    import math
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 24
    R = min((x1 - x0) / 2 - 90, (y1 - y0) / 2 - 90)
    return [(cx + R * math.cos(-math.pi / 2 + 2 * math.pi * k / N), cy + R * math.sin(-math.pi / 2 + 2 * math.pi * k / N)) for k in range(N)]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '网络（红框 = 传播源；普通点颜色 = 感染它的传播源，紫 = 被多个传播源感染）', 20, T['muted'], bold=True)
    P = _pos(box)
    for i in range(N):
        for j in range(i + 1, N):
            if GRAPH[i][j]:
                cv.line([P[i], P[j]], T['border'], 4)
    con = S.get('connect')
    ini = S.get('initial_set') or set()
    cur = S.get('_inner', {}).get('now') if S.get('_line', 0) >= 33 else None
    org = S.get('_inner', {}).get('origin') if S.get('_line', 0) >= 33 else None
    for k in range(N):
        x, y = P[k]
        r = 30
        fill = T['panel2']
        if k in ini:
            fill = T['panel2']
        elif con is not None and len(con[k]) == 1:
            fill = T[ORI.get(con[k][0], 'cyan')]
        elif con is not None and len(con[k]) >= 2:
            fill = T['purple']
        cv.rect((x - r, y - r, x + r, y + r), fill=fill, outline=T['red'] if k in ini else T['muted'], width=5 if k in ini else 2, r=r)
        cv.text((x, y), k, 32, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)
        if con is not None and k not in ini and con[k]:
            cv.text((x, y + r + 6), '来源 ' + ','.join(map(str, con[k])), 20, T['muted'], anchor='mt')
        if cur == k:
            cv.rect((x - r - 7, y - r - 7, x + r + 7, y + r + 7), outline=T['yellow'], width=5, r=r + 7)
    if org is not None:
        cv.text((x0 + 18, y0 + 34), f'现在从传播源 {org} 出发，看它会感染谁', 24, T[ORI.get(org, 'cyan')], anchor='la', bold=True)


CONFIG = dict(
    num=928, title='尽量减少恶意软件的传播 II', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='传播源 DFS · 只被一个源感染才算数',
    tags=['灵神题单·图论算法', '难度分 1985'],
    code='''
class Solution(object):
    def minMalwareSpread(self, graph, initial):

        n = len(graph)
        g = {}
        for i in range(n):
            g[i] = set()
            for j in range(n):
                if i != j and graph[i][j] == 1:
                    g[i].add(j)

        initial_set = set(initial)

        connect = [[] for _ in range(n)]

        for i in initial:
            self.dfs(i, i, g, initial_set, connect)

        connect_cnt = [0] * n
        for i in range(n):
            if len(connect[i]) == 1:
                connect_cnt[connect[i][0]] += 1
        
        res = None
        for i in range(n):
            if i in initial_set and (res is None or connect_cnt[i] > connect_cnt[res]):
                res = i
        
        return res

    def dfs(self, now, origin, g, initial_set, connect):
        for next in g[now]:
            if next not in initial_set and (len(connect[next]) == 0 or connect[next][-1] != origin):
                connect[next].append(origin)
                self.dfs(next, origin, g, initial_set, connect)
''',
    call=f'Solution().minMalwareSpread({GRAPH!r}, {INITIAL!r})',
    expect=1,
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='array', var='connect_cnt', label='connect_cnt（删掉该传播源能救的点数）', h=150, cell=70),
        dict(type='calls', h=190, hide=('graph', 'g', 'connect', 'initial_set', 'initial')),
    ],
    watch=[('now', 'now', 'blue'), ('origin', 'origin', 'orange'), ('i', 'i', 'yellow'), ('res', 'res', 'green')],
    skip=['n = len', 'g = {}', 6, 'g[i] = set()', 'for j in range(n)', 'if i != j and graph', 'g[i].add(j)', 'for i in initial:', 'connect = [[]'],
    captions={
        'initial_set = set': '`initial_set = {initial_set}`：传播源集合（邻接表 `g` 已建好，去掉了自环）',
        'self.dfs(i, i, g': lambda S, B, ret: f'从传播源 `{S.i}` 出发 DFS，看它能感染哪些普通点；`connect[x]` 记录感染 x 的传播源',
        'for next in g[now]': '遍历点 `{now}` 的邻居 `{sorted(g[now])}`（走完就回到上一层）',
        'if next not in initial_set': lambda S, B, ret: (
            f'邻居 `{S.next}` 是传播源，不用管' if S.next in S.initial_set else
            f'`{S.next}` 已被源 `{S.origin}` 记录过，不重复走' if S.connect[S.next] and S.connect[S.next][-1] == S.origin else
            f'`{S.next}` 是普通点，还没被源 `{S.origin}` 记录 → 感染到了'),
        'connect[next].append(origin)': '`connect[{next}] = {connect[next]}`：点 `{next}` 会被传播源 `{origin}` 感染',
        'self.dfs(next, origin': '继续从 `{next}` 往外扩',
        'connect_cnt = [0]': '`connect_cnt[x]`：只被传播源 `x` 感染的点数',
        'if len(connect[i]) == 1': lambda S, B, ret: (f'点 `{S.i}` 只被传播源 `{S.connect[S.i][0]}` 感染 → 删掉 `{S.connect[S.i][0]}` 就能救下点 `{S.i}`' if len(S.connect[S.i]) == 1
                                                      else (f'点 `{S.i}` 来源 `{S.connect[S.i]}`' + ('：被多个源感染，必然被感染' if len(S.connect[S.i]) > 1 else '：没有源能感染它')
                                                            if S.i not in S.initial_set else f'点 `{S.i}` 本身是传播源，跳过')),
        'connect_cnt[connect[i][0]] += 1': '`connect_cnt = {connect_cnt}`',
        'res = None': '`res` 记录目前最优的传播源',
        'for i in range(n):\n            if i in initial_set': '',
        'if i in initial_set and': lambda S, B, ret: (f'传播源 `{S.i}`：能救 `{S.connect_cnt[S.i]}` 个点' + ('，比当前最优多 → 更新' if S.res is None or S.connect_cnt[S.i] > S.connect_cnt[S.res] else '，不比当前最优多 → 不换')
                                                       if S.i in S.initial_set else f'`{S.i}` 不是传播源，跳过'),
        'res = i': '`res = {res}`',
        'return res': '删掉传播源 `{res}` 救下的点最多',
    },
    max_steps=100,
    cards=dict(
        one_liner='从每个传播源 DFS，只被一个源感染的点才是删它能救的',
        complexity='时间 约 `O(m·n + n^2)`（m 为传播源数），空间 `O(n)`',
        problem=['无向图用邻接矩阵给出，`initial` 中的点最初被感染，感染沿边扩散',
                 '从 `initial` 中删一个点（连同它的边），使最终感染点数最少，多解取编号小的',
                 '本视频：6 个点，`initial = [1,5]` → 删 `1`'],
        quote='反过来，我们可以从这些传播源开始进行dfs，看看这些节点将会感染到哪些节点。那么对于一个初始没有被感染的节点，若该节点会被两个或以上的传播源感染，那么无论怎么操作，该节点最终必然会被感染',
        quote_src='—— yiduobo 题解原文',
        idea=['先建邻接表，再从每个传播源 DFS，不进入其他传播源',
              '`connect[x]` 记录感染 `x` 的传播源；`len == 1` 才有希望被救',
              '统计每个传播源独占的点数 `connect_cnt`，取最大（并列取编号小）'],
        summary=['DFS 时不进入其他传播源：相当于把它们当成已删除',
                 '`connect[next][-1] != origin` 防止同一源重复访问同一点',
                 '`connect_cnt[i] > connect_cnt[res]` 用严格大于 → 并列保留编号小的',
                 '原文代码在 Python 3 下无需改动',
                 '对比灵神：灵神从普通点 DFS 找唯一的源（O(n²)）；这里从每个源 DFS（O(m·n)）'],
    ),
)
