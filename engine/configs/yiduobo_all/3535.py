def _lay(edges):
    n = len(edges) + 1
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)
    depth, kids, seen, q = [0] * n, {i: [] for i in range(n)}, {0}, [0]
    for x in q:
        for y in g[x]:
            if y not in seen:
                seen.add(y)
                depth[y] = depth[x] + 1
                kids[x].append(y)
                q.append(y)
    pos, cnt = {}, [0]
    def go(x):
        if not kids[x]:
            pos[x] = cnt[0]
            cnt[0] += 1
        else:
            for y in kids[x]:
                go(y)
            pos[x] = (pos[kids[x][0]] + pos[kids[x][-1]]) / 2
    go(0)
    return pos, depth, cnt[0], max(depth) + 1, kids


def _tree(cv, T, edges, box, label, fill=None, ring=None, sub=None, title=None, r=26, elabel=None, below=False):
    """通用树绘制：label(i)=节点内文字，fill(i)=颜色名或None，ring(i)=描边颜色名，sub(i)=节点下方小字"""
    x0, y0, x1, y1 = box
    pos, depth, w, h, kids = _lay(edges)
    if title:
        cv.text((x0 + 14, y0 + 2), title, 22, T['muted'], bold=True)
        y0 += 36
    dx = min(110, (x1 - x0 - 2 * r - 20) / max(w - 1, 1)) if w > 1 else 0
    dy = min(120, (y1 - y0 - 2 * r - 30) / max(h - 1, 1)) if h > 1 else 0
    sx = (x0 + x1) / 2 - dx * (w - 1) / 2
    P = {i: (sx + pos[i] * dx, y0 + r + 10 + depth[i] * dy) for i in pos}
    for a, b in edges:
        cv.line([P[a], P[b]], T['border'], 3)
        if elabel:
            cv.text((P[a][0] * 0.4 + P[b][0] * 0.6 + 8, P[a][1] * 0.4 + P[b][1] * 0.6), elabel(a, b), 20, T['yellow'], anchor='lm', bold=True)
    for i, (X, Y) in P.items():
        f = fill(i) if fill else None
        rg = ring(i) if ring else None
        cv.rect((X - r, Y - r, X + r, Y + r), fill=T[f] if f else T['panel2'], outline=T[rg] if rg else T['border'], width=5 if rg else 2, r=r)
        cv.text((X, Y), label(i), 26, T['bg'] if f else T['text'], anchor='mm', bold=True)
        cv.text((X - r - 2, Y - r - 2), i, 16, T['dim'], anchor='rb', mono=True)
        if sub and sub(i):
            if below:
                cv.text((X, Y + r + 4), sub(i), 20, T['muted'], anchor='mt', bold=True)
            else:
                cv.text((X + r + 8, Y), sub(i), 20, T['muted'], anchor='lm', bold=True)

CONV = [[0, 1, 2], [0, 2, 6], [1, 3, 3]]


def _draw(cv, S, B, box, T):
    dis = S.get('dis')
    now = S.get('now')
    edges = [[a, b] for a, b, w in CONV]
    fw = {(a, b): w for a, b, w in CONV}
    def fill(i):
        return 'green' if dis is not None and dis[i] is not None else None
    def ring(i):
        return 'yellow' if i == now else None
    def sub(i):
        return f'dis={dis[i]}' if dis is not None and dis[i] is not None else ''
    _tree(cv, T, edges, box, lambda i: i, fill=fill, ring=ring, sub=sub, r=26,
          elabel=lambda a, b: f'×{fw[(a, b)]}', below=True,
          title='边上 ×w：1 个 s 单位 = w 个 t 单位；绿 = 已算出 dis，黄框 = 当前出队')


def _inv(S, B, ret):
    x, w = S.x, S.w
    return f'反向边 `{S.y}→{x}`：权重是 `{w}` 的逆元 `w^(mod-2) % mod = {S.g[S.y][-1][1]}`（费马小定理），==用快速幂求=='


def _query(S, B, ret):
    x, y = S.x, S.y
    return f'`{x}→{y}`：`dis[{y}] * inv(dis[{x}]) % mod` = `{S.res[-1]}`（先把 `dis[{x}]` 求逆元，再乘 `dis[{y}]`）'


CONFIG = dict(
    num=3535, title='单位转换 II', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='BFS 求汇率 + 费马小定理求逆元',
    tags=['灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def queryConversions(self, conversions, queries):

        mod = 10 ** 9 + 7
        
        def quick_pow(base, p):
            if p == 0:
                return 1
            if p == 1:
                return base
            
            res = quick_pow(base, p // 2)
            res = res * res % mod
            if p & 1:
                res = res * base % mod
            return res
        
        n = len(conversions) + 1
        g = [[] for _ in range(n)]
        for x, y, w in conversions:
            g[x].append((y, w))
            g[y].append((x, quick_pow(w, mod - 2)))
        
        q = deque()
        q.append(0)
        dis = [None] * n
        dis[0] = 1
        while q:
            now = q.popleft()
            for nxt, w in g[now]:
                if dis[nxt] is None:
                    dis[nxt] = dis[now] * w % mod
                    q.append(nxt)
        
        res = []
        for x, y in queries:
            res.append(quick_pow(dis[x], mod - 2) * dis[y] % mod)
        return res
''',
    call='Solution().queryConversions([[0,1,2],[0,2,6],[1,3,3]], [[1,2],[3,1]])',
    expect=[3, 333333336],
    views=[
        dict(type='custom', draw=_draw, h=440),
        dict(type='queue', var='q', label='q（BFS 队列）', h=90),
        dict(type='array', var='dis', label='dis[x]：1 个 0 号单位 = dis[x] 个 x 号单位（None = 还没算）', cell=80, h=110),
        dict(type='array', var='res', label='res（查询结果）', cell=150, h=90),
    ],
    watch=['mod', ('now', 'now', 'yellow'), ('nxt', 'nxt', 'blue'), ('w', 'w', 'orange')],
    skip=['for x, y, w in conversions', 'g[x].append((y, w))', 7, 8, 9, 10, 12, 13, 14, 15, 16, 'n = len(conversions)', 'for nxt, w in g[now]', 'q = deque()', 'dis = [None]'],
    captions={
        'mod = ': '结果要对 `mod = 10^9 + 7` 取模：分数 `p/q` 要写成 `p * inv(q) % mod`',
        'g = [[] for': '建图：每条换算要建==双向边==，邻接表里存 `(目标, 权重)`',
        'g[y].append((x, quick_pow': '反向边的权重 = `w` 的乘法逆元：用快速幂算 `w^(mod-2) % mod`（费马小定理），进入 `quick_pow`',
        'q.append(0)': '从 0 号单位开始 BFS（题目保证 0 能到达所有单位）',
        'dis[0] = 1': '`dis[x]` = 1 个 0 号单位等于多少个 x 号单位；`dis[0] = 1`',
        'while q': lambda S, B, r: (f'队列非空：`q = {list(S.q)}`' if S.q else '队列空了：所有单位的汇率都算完'),
        'now = q.popleft()': '取出单位 `{now}`，看它能换成哪些单位',
        'if dis[nxt] is None': lambda S, B, r: (f'邻居 `{S.nxt}`（汇率 `{S.w}`）：`dis[{S.nxt}]` 还没算 → 第一次到达' if S.dis[S.nxt] is None else f'邻居 `{S.nxt}`（汇率 `{S.w}`）：`dis[{S.nxt}]` 已经有了（走回头路）→ 跳过'),
        'dis[nxt] = dis[now] * w % mod': '`dis[{nxt}] = dis[{now}] * {w} % mod = {dis[nxt]}`：汇率沿路径连乘',
        'q.append(nxt)': '`{nxt}` 入队',
        'res = []': '汇率都有了。任意两点 `a→b` = `dis[b] / dis[a]`，除法要用逆元',
        'for x, y in queries': '处理查询 `{x} → {y}`',
        'res.append': '查询：`dis[b] * inv(dis[a]) % mod`，先用 `quick_pow(dis[a], mod-2)` 求 `dis[a]` 的逆元',
        38: '全部查询结果：`{res}`',
    },
    cards=dict(
        one_liner='先求 0 号单位到各点的汇率，任意两点相除（取逆元）',
        complexity='时间 `O((n+q) log mod)`，空间 `O(n)`',
        problem=['`n` 种单位，`conversions[i] = [s, t, f]`：1 个 s 单位 = f 个 t 单位，共 `n-1` 条，保证 0 号单位能唯一换算到任何单位',
                 '每个查询 `[a, b]`：1 个 a 单位等于多少个 b 单位，分数 `p/q` 要返回 `p * inv(q) % (10^9+7)`',
                 '示例：`[[1,2],[3,1]]` → `[3, 333333336]`'],
        quote='对于一组conversions[index] = [source[index], target[index], factor[index]]，除了建立source到target的权重为factor的边之外，还需要建立target到source的权重为inv[factor]的边。',
        quote_src='—— yiduobo 题解原文',
        idea=['建双向边：正向权重 `w`，反向权重 `w` 的乘法逆元',
              '从 0 号点 BFS：`dis[x]` = 0 到 x 的汇率（沿路径连乘取模）',
              '查询 `a→b`：`dis[b] * inv(dis[a]) % mod`；逆元 = `a^(mod-2)`（费马小定理）'],
        summary=['时间 `O((n+q) log mod)`，空间 `O(n)`',
                 '逆元用快速幂 `quick_pow(a, mod - 2)`，`mod` 是质数才成立',
                 '每步乘法都要取模，防止数字过大',
                 '原文本身是 Python 2 风格，但代码无需改动即可在 Python 3 运行',
                 '与上一题 3528 的区别：这里要反向换算，所以多了逆元'],
    ),
)
