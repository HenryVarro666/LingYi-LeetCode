PAL = ['blue', 'orange', 'purple']
COMP = {0: 0, 2: 0, 4: 0, 5: 0, 1: 1, 6: 1, 3: 2}
POS = {0: (0.08, 0.22), 2: (0.30, 0.22), 5: (0.08, 0.80), 4: (0.30, 0.80), 1: (0.55, 0.22), 6: (0.55, 0.80), 3: (0.82, 0.50)}
EDGES = [(0, 2), (0, 5), (2, 4), (5, 4), (1, 6)]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '无向图（染色 = 已访问，同色 = 同一个连通块，白环 = 当前正在访问的点）', 21, T['muted'], bold=True)
    W, H = x1 - x0 - 80, y1 - y0 - 100
    P = {k: (x0 + 40 + W * a, y0 + 64 + H * b) for k, (a, b) in POS.items()}
    for a, b in EDGES:
        cv.line([P[a], P[b]], T['border'], 4)
    seen = set(S.get('used') or ())
    cur = S.get('now') if 22 <= S.get('_line', 0) <= 29 else None
    for k, (px, py) in P.items():
        on = k in seen
        fill = T[PAL[COMP[k]]] if on else T['panel2']
        cv.rect((px - 34, py - 34, px + 34, py + 34), fill=fill, outline=T['border'], r=34)
        cv.text((px, py), k, 34, T['bg'] if on else T['muted'], anchor='mm', bold=True)
        if k == cur:
            cv.rect((px - 44, py - 44, px + 44, py + 44), outline=T['text'], width=5, r=44)


CONFIG = dict(
    num=2316, title='统计无向图中无法互相到达点对数', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='种子染色法 + 补集计数', tags=['灵神题单·图论算法', '灵神题单·数学算法', '难度分 1604'],
    code='''
class Solution(object):
    def countPairs(self, n, edges):

        used = set()
        g = {}
        for x, y in edges:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            
            g[x].add(y)
            g[y].add(x)
        
        res = n * (n - 1) // 2
        for index in range(n):
            if index not in used:
                used.add(index)
                q = [index]
                l = 0
                r = 1
                while l < r:
                    now = q[l]
                    l += 1
                    for next in g.get(now, set()):
                        if next not in used:
                            q.append(next)
                            r += 1
                            used.add(next)
                
                res -= r * (r - 1) // 2
        
        return res
''',
    call='Solution().countPairs(7, [[0,2],[0,5],[2,4],[1,6],[5,4]])',
    expect=14,
    views=[
        dict(type='custom', draw=_draw, h=290),
        dict(type='array', var=lambda S: S.get('q'), label='q（当前连通块的 BFS 队列，l 指向下一个出队的）', cell=90, h=190,
             pointers={'l': 'blue'}, dim=lambda S, i, v: i < S.get('l', 0)),
        dict(type='text', h=60, fn=lambda S: (f"总点对 `{S['n']}×{S['n']-1}//2` 先全算上，每个连通块再减去块内点对：`res = {S['res']}`" if 'res' in S else '')),
    ],
    watch=['index', 'now', ('r', 'r', 'orange'), ('res', 'res', 'green')],
    captions={
        'used = set()': '`used` 记录已经染过色的点',
        'g[y].add(x)': '无向边 `{x}—{y}`：两个方向都记',
        'res = n * (n - 1)': '先假设所有点对都不通：`{n}×{n-1}//2` → =={res}==',
        'if index not in used': lambda S, B, r: (f'点 `{S.index}` 还没染色 → 新连通块的种子' if S.index not in S.used else f'点 `{S.index}` 已经染过色，跳过'),
        'now = q[l]': '出队 `now = {now}`，找它的邻居',
        'if next not in used': lambda S, B, r: (f'邻居 `{S.next}` 没染过 → 入队、染色' if S.next not in S.used else f'邻居 `{S.next}` 已染过 → 跳过'),
        'res -= r * (r - 1)': '这个块的大小 `r = {r}`，块内互通点对 `{r}×{r-1}//2` 要扣掉 → `res = {res}`',
        'return res': '扣掉所有连通块内部的点对，剩下的就是互不相通的 =={res}==',
    },
    skip=['l = 0', 'r = 1', 'l += 1', 'r += 1', 'q.append', 'if x not in g', 'if y not in g', 'g[x] = set', 'g[y] = set', 'used.add(next)', 'used.add(index)'],
    max_steps=120,
    cards=dict(
        one_liner='总点对数 减去 每个连通块内部的点对数',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['`n` 个点的无向图，`edges` 是边，问有多少对点互相无法到达',
                 '同一连通块内能互通，不同连通块之间不能',
                 '示例：`n=7, edges=[[0,2],[0,5],[2,4],[1,6],[5,4]]` → `14`'],
        quote='可以反过来思考，使用n * (n - 1) / 2减去可以互相到达的点对数。对于一个大小为k的连通块，其中的点对数目为k * (k - 1) / 2。',
        quote_src='—— yiduobo 题解原文',
        idea=['n 个点一共有 `n(n-1)/2` 对，先全算上',
              '用种子染色（BFS）求出每个连通块大小 `k`',
              '块内的 `k(k-1)/2` 对是能互通的，从总数里扣掉'],
        summary=['时间 `O(n + m)`，空间 `O(n + m)`',
                 '本例：`21 − 6 − 1 − 0 = 14`（块大小 4、2、1）',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（否则得到浮点数）',
                 '孤立点没有边，不在 `g` 里，所以用 `g.get(now, set())`',
                 '对比灵神：灵神用乘法原理累加不通的对数，这里用补集'],
    ),
)
