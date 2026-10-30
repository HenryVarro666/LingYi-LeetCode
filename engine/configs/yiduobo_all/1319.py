def _graph(cv, box, T, title, POS, EDGES, fill, label=None, ecol=None, elab=None, directed=False, ring=None):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 21, T['muted'], bold=True)
    Wd, Hd = x1 - x0 - 120, y1 - y0 - 110
    P = {k: (x0 + 60 + Wd * a, y0 + 66 + Hd * b) for k, (a, b) in POS.items()}
    R = 30
    for e in EDGES:
        a, b = e[0], e[1]
        col, wd = ecol(e) if ecol else (T['border'], 4)
        (ax, ay), (bx, by) = P[a], P[b]
        if directed:
            d = max(1.0, ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5)
            ux, uy = (bx - ax) / d, (by - ay) / d
            cv.arrow((ax + ux * R, ay + uy * R), (bx - ux * (R + 3), by - uy * (R + 3)), col, wd, head=16)
        else:
            cv.line([P[a], P[b]], col, wd)
        if elab:
            mx, my = (ax + bx) / 2, (ay + by) / 2
            s = elab(e)
            cv.rect((mx - 22, my - 16, mx + 22, my + 16), fill=T['bg'], r=8)
            cv.text((mx, my), s, 22, col, anchor='mm', bold=True)
    for k, (px, py) in P.items():
        f = fill(k)
        cv.rect((px - R, py - R, px + R, py + R), fill=f or T['panel2'], outline=T['border'], r=R)
        cv.text((px, py), k if label is None else label(k), 32, T['bg'] if f else T['muted'], anchor='mm', bold=True)
        if ring is not None and ring == k:
            cv.rect((px - R - 10, py - R - 10, px + R + 10, py + R + 10), outline=T['text'], width=5, r=R + 10)


PAL = ['blue', 'orange', 'purple', 'cyan', 'pink', 'green']
POS = {0: (0.10, 0.15), 1: (0.40, 0.50), 2: (0.10, 0.85), 3: (0.70, 0.20), 4: (0.90, 0.80)}
EDGES = [(0, 1), (0, 2), (1, 2), (3, 4)]


def _col(S):
    c = S.get('color')
    return c if isinstance(c, list) else [None] * 5


def _draw(cv, S, B, box, T):
    c = _col(S)
    inner = S.get('_inner') or {}
    cur = inner.get('now') if 'now' in inner else None
    _graph(cv, box, T, '无向图（同色 = 同一个连通分量，白环 = 正在染色的点，灰 = 还没染）', POS, EDGES,
           lambda k: T[PAL[c[k] % 6]] if c[k] is not None else None, ecol=lambda e: (
               (T[PAL[c[e[0]] % 6]], 5) if c[e[0]] is not None and c[e[0]] == c[e[1]] else (T['border'], 4)), ring=cur)


CONFIG = dict(
    num=1319, title='连通网络的操作次数', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='染色数连通分量：答案 = 颜色数 − 1', tags=['灵神题单·图论算法'],
    code='''
class Solution(object):
    def makeConnected(self, n, connections):

        if len(connections) < n - 1:
            return -1
        
        g = {}
        for x, y in connections:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)
        
        color = [None] * n
        now_color = 0
        for x in range(n):
            if color[x] is None:
                self.dfs(x, now_color, color, g)
                now_color += 1
        
        return now_color - 1
    
    def dfs(self, now, now_color, color, g):
        color[now] = now_color
        if now not in g:
            return
        for next in g[now]:
            if color[next] is None:
                self.dfs(next, now_color, color, g)
''',
    call='Solution().makeConnected(5, [[0,1],[0,2],[1,2],[3,4]])',
    expect=1,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var='color', label='color（每个点的颜色编号，空 = 未染）', h=160,
             color=lambda S, i, v: PAL[v % 6] if v is not None else None),
        dict(type='text', h=60, fn=lambda S: (f"已染完 `{S['now_color']}` 个连通分量；最后：答案 = 颜色数 `- 1`" if 'now_color' in S else '')),
        dict(type='calls', h=170),
    ],
    watch=['x', 'now', ('now_color', 'now_color', 'orange')],
    captions={
        'if len(connections) < n - 1': lambda S, B, r: (f'`n` 个点至少要 `n-1 = {S.n - 1}` 条边才能连通；现在有 `{len(S.connections)}` 条 → ' +
                                                        ('边不够，必定 ==返回 -1==' if len(S.connections) < S.n - 1 else '==够了==，一定有解')),
        'return -1': '边数不足，怎么调整都连不起来',
        'g[x].add(y)': '无向边 `{x}—{y}`：两个方向都记进邻接表',
        'color = [None]': '`color[i]` 记录点 i 属于哪个连通分量（None = 还没染）',
        'now_color = 0': '`now_color` 是下一个要用的新颜色',
        'if color[x] is None': lambda S, B, r: (f'点 `{S.x}` 还没颜色 → 它属于==新的连通分量==' if S.color[S.x] is None else f'点 `{S.x}` 已染色，跳过'),
        'self.dfs(x': '从点 `{x}` 出发，把整个连通分量染成颜色 `{now_color}`',
        'now_color += 1': '这一块染完了，下一块换新颜色：`now_color = {now_color}`',
        'color[now] = now_color': '点 `{now}` 染成颜色 `{now_color}`',
        'if now not in g': lambda S, B, r: ('点 `%s` 没有任何边，染完就返回' % S.now if S.now not in S.g else '点 `%s` 有邻居，继续往下染' % S.now),
        'if color[next] is None': lambda S, B, r: (f'邻居 `{S.next}` 还没染 → 继续递归' if S.color[S.next] is None else f'邻居 `{S.next}` 已经是颜色 `{S.color[S.next]}`，不再重复访问'),
        'self.dfs(next': '递归到邻居 `{next}`',
        'return now_color - 1': '共 `{now_color}` 个连通分量，用 ==`{now_color} - 1`== 条多余的边把它们接起来',
    },
    skip=['g[y] = set()', 'g[x] = set()'],
    max_steps=140,
    cards=dict(
        one_liner='先看边够不够，再数连通分量：答案 = 分量数 − 1',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['`n` 台电脑，`connections` 是网线，可以拔掉一根线接到别处',
                 '问最少拔插几次能让所有电脑连通，做不到返回 `-1`',
                 '本例：`n=5`，4 条线 → `1`'],
        quote='对于n个点的图，其至少需要n - 1条边才能成为一个连通图，那么当n - 1 > m时，直接返-1即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['边数 `m >= n-1` 时必有解：连通分量内部只用 `n-k` 条，==多出来至少 `k-1` 条==',
              '而把 `k` 个分量连起来恰好要 `k-1` 条',
              '所以只需给图染色，数出颜色数 `color`，答案 `color - 1`'],
        summary=['时间 `O(n + m)`，空间 `O(n + m)`（邻居表 + 递归栈）',
                 '先判 `len(connections) < n - 1`，不够直接 `-1`',
                 '孤立点不在 `g` 里，所以 `dfs` 要先判 `now not in g`',
                 '对照灵神的并查集写法：数连通块的思路相同，本文用 DFS 染色'],
    ),
)
