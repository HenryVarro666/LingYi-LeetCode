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


POS = {0: (0.08, 0.15), 1: (0.28, 0.85), 2: (0.62, 0.12), 3: (0.50, 0.88), 4: (0.92, 0.88)}
EDGES = [(0, 1), (2, 3), (2, 4)]
COMP = {0: 0, 1: 0, 2: 1, 3: 1, 4: 1}
PAL = ['green', 'orange']


def _draw(cv, S, B, box, T):
    vis = S.get('vis')
    seen = set(vis) if vis is not None else set()
    ln = S.get('_line', 0)
    cur = S.get('now') if 17 <= ln <= 23 else (S.get('x') if 26 <= ln <= 29 else None)
    _graph(cv, box, T, '无向图（染色 = vis 里已访问；白环 = 当前处理的点；同色 = 同一连通分量）', POS, EDGES,
           lambda k: T[PAL[COMP[k]]] if k in seen else None, ring=cur,
           ecol=lambda e: ((T[PAL[COMP[e[0]]]], 5) if e[0] in seen and e[1] in seen else (T['border'], 4)))


def _deg(S):
    q, g = S.get('q'), S.get('g')
    if not isinstance(q, list) or not isinstance(g, dict) or S.get('_line', 0) < 25:
        return ''
    x = S.get('x')
    cur = f"点 `{x}` 的度 `len(g[{x}]) = {len(g[x])}`" if x in g else ''
    return f"连通分量 `q = {q}`，大小 `{len(q)}` → 完全图每个点的度都应是 ==`{len(q) - 1}`==。{cur}"


CONFIG = dict(
    num=2685, title='统计完全连通分量的数量', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='BFS 找连通分量 + 逐点检查度数', tags=['灵神题单·图论算法', '难度分 1769'],
    code='''
class Solution(object):
    def countCompleteComponents(self, n, edges):

        g = {index : set() for index in range(n)}
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)
        
        res = 0
        vis = set()
        for index in range(n):
            if index not in vis:
                q = [index]
                vis.add(index)
                head, tail = 0, 1
                while head < tail:
                    now = q[head]
                    head += 1
                    for nxt in g[now]:
                        if nxt not in vis:
                            vis.add(nxt)
                            q.append(nxt)
                            tail += 1

                flag = True
                for x in q:
                    if len(g[x]) != len(q) - 1:
                        flag = False
                        break
                
                if flag:
                    res += 1
        
        return res
''',
    call='Solution().countCompleteComponents(5, [[0,1],[2,3],[2,4]])',
    expect=1,
    views=[
        dict(type='custom', draw=_draw, h=280),
        dict(type='array', var='q', label='q（当前连通分量的所有点，BFS 顺序）', h=150),
        dict(type='text', h=90, fn=_deg),
    ],
    watch=['index', 'now', ('head', 'head', 'blue'), ('tail', 'tail', 'pink'), ('flag', 'flag', 'orange'), ('res', 'res', 'green')],
    captions={
        'g = {index': '`g[x]` 是点 x 的邻居集合',
        'g[y].add(x)': '无向边 `{x}—{y}`：两个方向都记',
        'res = 0': '`res` 统计完全连通分量个数',
        'vis = set()': '`vis` 记录已访问的点',
        'if index not in vis': lambda S, B, r: (f'点 `{S.index}` 没访问过 → 新的连通分量，从它开始 BFS' if S.index not in S.vis else f'点 `{S.index}` 已属于某个分量，跳过'),
        'q = [index]': '队列 `q` 从点 `{index}` 开始（`q[head:tail]` 是还没处理的点），最后会装下整个连通分量',
        'while head < tail': lambda S, B, r: (f'队列里还有点（`head={S.head} < tail={S.tail}`）→ 继续' if S.head < S.tail else '队列空了 → 这个连通分量找全了'),
        'now = q[head]': '取出队头 `{now}`（`head` 后移）',
        'if nxt not in vis': lambda S, B, r: (f'邻居 `{S.nxt}` 没访问过 → 入队' if S.nxt not in S.vis else f'邻居 `{S.nxt}` 已访问，跳过'),
        'q.append(nxt)': '`{nxt}` 入队（`tail` 后移），也属于这个分量',
        'flag = True': '分量找全了，大小 `len(q) = {len(q)}`；`flag` 假设它是完全的',
        'if len(g[x]) != len(q) - 1': lambda S, B, r: (
            f'点 `{S.x}` 的度 `{len(S.g[S.x])}` ' + ('≠' if len(S.g[S.x]) != len(S.q) - 1 else '=') +
            f' `{len(S.q) - 1}` → ' + ('==少连了边==，不是完全图' if len(S.g[S.x]) != len(S.q) - 1 else '和分量里其它点都相连')),
        'flag = False': '有点没连满 → 这个分量不完全',
        'if flag': lambda S, B, r: ('每个点都连满了 → 完全连通分量，`res` 加 1' if S.flag else '这个分量不完全，不计数'),
        'res += 1': '`res = {res}`',
        'return res': '共 =={res}== 个完全连通分量',
    },
    skip=['head += 1', 'tail += 1', 'vis.add(index)', 'head, tail = 0, 1'],
    max_steps=140,
    cards=dict(
        one_liner='BFS 找出分量，再看每个点的度是不是 分量大小 − 1',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['无向图，`n` 个点，`edges` 是边',
                 '分量内每对点之间都有边，才是==完全连通分量==',
                 '求完全连通分量的个数',
                 '本例：`n=5` → `1`（只有 `{0,1}`）'],
        quote='对于单个连通分量，遍历其中的所有节点，通过当前连通分量的大小以及该节点的度，就能判断这个节点是否与连通分量中的其他点都相连。',
        quote_src='—— yiduobo 题解原文',
        idea=['先 BFS 把每个连通分量的点都装进 `q`',
              '分量大小是 `len(q)`，完全图里每个点的度必须是 `len(q) - 1`',
              '只要有一个点不满足，`flag = False` 并 `break`'],
        summary=['时间 `O(n + m)`，空间 `O(n + m)`',
                 '`g` 用集合存邻居，度数 = `len(g[x])`，不会重复计边',
                 '孤立点：分量大小 1，度 0 = 1 − 1，也算完全连通分量',
                 '本例 `{2,3,4}`：点 3 的度是 1，≠ 2 → 不是',
                 '对照灵神：灵神 DFS 里累计 `e` 与 `v(v-1)` 比较；yiduobo 是逐点比度数'],
    ),
)
