GRAPH = [[1, 1, 0, 0, 0], [1, 1, 1, 0, 0], [0, 1, 1, 0, 0], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1]]
POS = {0: (0.04, 0.15), 1: (0.24, 0.85), 2: (0.44, 0.15), 3: (0.72, 0.85), 4: (0.96, 0.15)}
PAL = ['blue', 'pink', 'purple', 'orange', 'cyan']


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    color = S.get('color')
    if color is None:
        return
    inn = S['_inner']
    ini = S.get('initial', [])
    n = len(color)
    cur = inn.get('now') if 'now_color' in inn and 'next' in inn or ('now' in inn and 'now_color' in inn) else None
    if cur is None and 'now_color' in S and 'color_cnt' in S:
        cur = S.get('i')
    gw = x1 - x0
    R = 34

    def P(u):
        fx, fy = POS[u]
        return x0 + 60 + fx * (gw - 120), y0 + 90 + fy * (y1 - y0 - 400)

    for i in range(n):
        for j in range(i + 1, n):
            if GRAPH[i][j]:
                cv.line([P(i), P(j)], T['muted'], 3)
    for u in range(n):
        X, Y = P(u)
        c = color[u]
        fill = T[PAL[c % len(PAL)]] if c is not None else T['panel2']
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=fill,
                     outline=T['yellow'] if u == cur else (T['red'] if u in ini else T['border']),
                     width=7 if u == cur else (5 if u in ini else 2))
        cv.text((X, Y), u, 30, T['bg'] if c is not None else T['text'], anchor='mm', bold=True)
        if u in ini:
            cv.text((X, Y + R + 12), '传播源', 20, T['red'], anchor='mt', bold=True)
    cv.text((x0 + 20, y0 + 14), '填充色 = 连通子图的颜色，红圈 = 传播源，黄圈 = 当前节点', 20, T['dim'])
    cv.rect((x0 + 20, y1 - 190, x1 - 20, y1 - 14), fill=T['panel2'], r=10)
    rows = [('color_cnt（每种颜色的节点数）', S.get('color_cnt'), 'cyan'),
            ('color_flag（每种颜色里的传播源数）', S.get('color_flag'), 'orange'),
            ('res / remove_cnt', None, 'green')]
    for k, (name, v, c) in enumerate(rows):
        yy = y1 - 172 + k * 54
        if v is not None:
            cv.text((x0 + 40, yy), f'{name} = {v}', 24, T[c], bold=True)
        elif name.startswith('res'):
            cv.text((x0 + 40, yy), f"res = {S.get('res', '—')}，remove_cnt = {S.get('remove_cnt', '—')}", 24, T[c], bold=True)
        else:
            cv.text((x0 + 40, yy), f'{name} = —', 24, T['dim'])


CONFIG = dict(
    num=924, title='尽量减少恶意软件的传播', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='DFS 染色分连通子图 · 数传播源',
    tags=['灵神题单', '图论算法', '难度分 1869'],
    code='''
class Solution(object):
    def minMalwareSpread(self, graph, initial):

        n = len(graph)
        color = [None] * n
        g = {}
        for i in range(n):
            g[i] = set()
            for j in range(n):
                if i != j and graph[i][j] == 1:
                    g[i].add(j)
        
        now_color = 0
        for i in range(n):
            if color[i] is None:
                self.dfs(i, now_color, color, g)
                now_color += 1
        
        color_cnt = [0] * now_color
        for i in range(n):
            color_cnt[color[i]] += 1
        
        color_flag = [0] * now_color
        for i in initial:
            color_flag[color[i]] += 1
        
        res = None
        remove_cnt = None
        for i in initial:
            if color_flag[color[i]] == 1:
                now_remove = color_cnt[color[i]]
            else:
                now_remove = 0
            if res is None or now_remove > remove_cnt or (now_remove == remove_cnt and res > i):
                res = i
                remove_cnt = now_remove

        return res

    def dfs(self, now, now_color, color, g):
        color[now] = now_color
        for next in g[now]:
            if color[next] is None:
                self.dfs(next, now_color, color, g)
''',
    call=f'Solution().minMalwareSpread({GRAPH}, [1, 2, 3])',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='calls', h=150),
    ],
    watch=[('now_color', 'now_color', 'blue'), ('now', lambda S: S['_inner'].get('now'), 'yellow'), ('res', 'res', 'green'),
           ('remove_cnt', 'remove_cnt', 'green')],
    skip=[4, 5, 6, 7, 8, 9, 10, 11, 20, 24, 29, 32, 42, 'now_remove = 0'],
    max_steps=90,
    captions={
        13: '`g` 已经建好邻接表（去掉了自环）。`now_color` 是下一个要用的颜色编号',
        15: lambda S, B, ret: (f'节点 `{S.i}` 还没染色 → 它属于一个新的连通子图' if S.color[S.i] is None
                               else f'节点 `{S.i}` 已有颜色 `{S.color[S.i]}` → 已经被之前的 dfs 染过'),
        16: '从 `{i}` 开始 dfs 染色，把整个连通子图染成颜色 `{now_color}`',
        17: '这个连通子图染完 → 换下一种颜色：`now_color = {now_color}`',
        21: '`{i}` 的颜色是 `{color[i]}` → `color_cnt[{color[i]}] = {color_cnt[color[i]]}`（该子图的节点数）',
        25: '传播源 `{i}` 在颜色 `{color[i]}` 的子图里 → `color_flag[{color[i]}] = {color_flag[color[i]]}`（该子图的传播源数）',
        30: lambda S, B, ret: (f'传播源 `{S.i}`：它的子图只有 1 个传播源 → 移除它能救下整个子图'
                               if S.color_flag[S.color[S.i]] == 1 else f'传播源 `{S.i}`：它的子图有 {S.color_flag[S.color[S.i]]} 个传播源 → 移除它也没用，能救 0 个'),
        31: '`now_remove = color_cnt[{color[i]}]` = =={now_remove}==：能少感染这么多节点',
        33: '`now_remove = 0`：子图里还有别的传播源，救不了',
        34: lambda S, B, ret: (f'`res` 还是 None → 先选 `{S.i}`' if B.res is None
                               else (f'`now_remove = {S.now_remove}` vs 当前最好 `{B.remove_cnt}`：'
                                     + ('更大 → 更新' if S.now_remove > B.remove_cnt else
                                        (f'一样大，且 `res = {B.res}` > `{S.i}` → 取下标小的，更新' if S.now_remove == B.remove_cnt and B.res > S.i
                                         else '没有更好 → 不更新')))),
        35: '`res = {res}`',
        36: '`remove_cnt = {remove_cnt}`',
        38: '返回 `{ret}`',
        41: '`color[{now}] = {now_color}`：给 {now} 染上当前颜色',
        43: lambda S, B, ret: (f'邻居 `{S.next}` 没有颜色 → 递归染色' if S.color[S.next] is None
                               else f'邻居 `{S.next}` 已经染过 → 跳过'),
        44: '递归染色邻居 `{next}`',
    },
    cards=dict(
        one_liner='先把图分成连通子图，只含一个传播源的子图里，选节点数最多的',
        complexity='时间 `O(n²)`，空间 `O(n²)`',
        problem=['`graph` 是邻接矩阵，`initial` 是最初被感染的节点，感染沿边扩散到整个连通子图',
                 '从 `initial` 里移除一个节点，使最终感染节点数最少；并列取下标最小',
                 '本视频：5 个点，两个连通子图 `{0,1,2}`、`{3,4}`，`initial=[1,2,3]`'],
        quote='若某个连通子图中有两个或者更多的传播源，那么即使去掉其中某一个，这个连通子图中的节点最终也还是会被感染。那么现在就可以明确，我们应该将目标锁定在那些只有一个传播源的连通子图上。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用 dfs ==染色==：同一个连通子图染成同一种颜色',
              '`color_cnt` 数每种颜色的节点数，`color_flag` 数每种颜色里的传播源数',
              '对每个传播源：子图只有它一个传播源 → 能救 `color_cnt` 个，否则能救 0 个；取最大，并列取小下标'],
        summary=['时间 `O(n²)`（建图 + 染色），空间 `O(n²)`',
                 '==传播源数为 1 才有用==；多个传播源的子图移除谁都救不了',
                 '所有传播源 `now_remove` 都是 0 时，`res` 自然是下标最小的那个（并列取小）',
                 '建图时用 `i != j` 去掉自环',
                 '对比灵神：灵神一边 DFS 一边用状态机数传播源，yiduobo 先染色、再分别统计'],
    ),
)
