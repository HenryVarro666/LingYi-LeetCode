N, M = 3, 3
BROKEN = [[0, 0], [2, 1], [2, 2]]


def _nm(S, k):
    m, n = S['m'], S['n']
    if k == 0:
        return 'S'
    if k == m * n + 1:
        return 'T'
    return f'({(k - 1) // m},{(k - 1) % m})'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n, m = N, M
    cell = min(120, (x1 - x0 - 80) / m, (y1 - y0 - 120) / n)
    sx = x0 + ((x1 - x0) - cell * m) / 2
    sy = y0 + 70
    cv.text((x0 + 18, y0 + 4), '棋盘（灰 X = 破损；绿块 = 已放的骨牌；黄 = 正在处理；青框 = BFS 到过；粉框 = 增广路）', 21, T['muted'], bold=True)
    broken = {r * m + c + 1 for r, c in BROKEN}
    live = 'c' in S and 't' in S
    c = S['c'] if live else None
    t = S['t'] if live else None

    def xy(k):
        return sx + ((k - 1) % m) * cell, sy + ((k - 1) // m) * cell

    # 已放的骨牌：黑格 u 向白格 v 的原边被流过 ⇒ 反向边 c[v][u] > 0
    doms = []
    if live:
        for u in range(1, m * n + 1):
            if u in broken or ((u - 1) // m + (u - 1) % m) % 2:
                continue
            r0, c0 = (u - 1) // m, (u - 1) % m
            for v in [u + 1 if c0 < m - 1 else None, u - 1 if c0 > 0 else None,
                      u + m if r0 < n - 1 else None, u - m if r0 > 0 else None]:
                if v is not None and v not in broken and c[v][u] > 0:
                    doms.append((u, v))
    matched = {k for d in doms for k in d}
    pre = S.get('pre') if live else None
    q = set(S.get('q', [])) if live else set()
    path = set()
    if pre and pre[t] is not None:
        k = t
        while k is not None and k != -1:
            path.add(k)
            k = pre[k]
    for k in range(1, m * n + 1):
        X, Y = xy(k)
        r, cc = (k - 1) // m, (k - 1) % m
        black = (r + cc) % 2 == 0
        if k in broken:
            cv.rect((X + 5, Y + 5, X + cell - 5, Y + cell - 5), fill=(46, 50, 58), r=10)
            cv.text((X + cell / 2, Y + cell / 2), '×', 44, T['dim'], anchor='mm', bold=True)
            continue
        fill = T['panel2'] if black else (30, 36, 46)
        if k in matched:
            fill = (36, 110, 72)
        cv.rect((X + 5, Y + 5, X + cell - 5, Y + cell - 5), fill=fill, r=10, outline=T['border'])
        if k in path:
            cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), outline=T['pink'], width=5, r=12)
        elif k in q:
            cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), outline=T['cyan'], width=4, r=12)
        if live and S.get('now') == k and S.get('_line') == 37:
            cv.rect((X + 5, Y + 5, X + cell - 5, Y + cell - 5), fill=T['yellow'], alpha=120, r=10)
        cv.text((X + cell / 2, Y + cell / 2 - 6), '黑' if black else '白', 30, T['text'] if black else T['muted'], anchor='mm', bold=True)
        cv.text((X + cell / 2, Y + cell - 16), f'{r},{cc}', 16, T['dim'], anchor='mb', mono=True)
    for u, v in doms:
        ax, ay = xy(u)
        bx, by = xy(v)
        if ay == by:
            lo = min(ax, bx) + cell
            cv.rect((lo - 8, ay + cell * 0.3, lo + 8, ay + cell * 0.7), fill=(36, 110, 72))
        else:
            lo = min(ay, by) + cell
            cv.rect((ax + cell * 0.3, lo - 8, ax + cell * 0.7, lo + 8), fill=(36, 110, 72))


def _dummy():
    pass


def _txt(S):
    if 'res' not in S:
        return '黑白染色：相邻格颜色不同 → 骨牌 = 一条黑白边 → 二分图最大匹配（用最大流）'
    return f"已放骨牌 `res = {S['res']}` 块（每找到一条增广路 +1）"


CONFIG = dict(
    num='LCP 04', title='覆盖', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='棋盘黑白染色 → 二分图最大匹配（BFS 增广）',
    tags=['网络流', '二分图', '状压 DP'],
    code='''
class Solution(object):
    def domino(self, n, m, broken):

        broken_set = set()
        for x, y in broken:
            broken_set.add(x * m + y + 1)
        s = 0
        t = m * n + 1
        c = [[0] * (t + 1) for _ in range(t + 1)]
        
        for i in range(n):
            for j in range(m):
                now = i * m + j + 1
                if now in broken_set:
                    continue
                if (i + j) % 2 == 0:
                    c[s][now] = 1
                    if j < m - 1 and now + 1 not in broken_set:
                        c[now][now + 1] = 1
                    if i < n - 1 and now + m not in broken_set:
                        c[now][now + m] = 1
                else:
                    c[now][t] = 1
                    if j < m - 1 and now + 1 not in broken_set:
                        c[now + 1][now] = 1
                    if i < n - 1 and now + m not in broken_set:
                        c[now + m][now] = 1

        res = 0
        while True:
            pre = [None] * (m * n + 2)
            pre[s] = -1
            head = 0
            tail = 1
            q = [s]
            while head < tail:
                now = q[head]
                head += 1
                for next in range(m * n + 2):
                    if c[now][next] > 0 and pre[next] is None:
                        pre[next] = now
                        q.append(next)
                        tail += 1
            
            if pre[t] is None:
                break
            
            res += 1
            now = t
            while now != s:
                last = pre[now]
                c[last][now] -= 1
                c[now][last] += 1
                now = last
        
        return res
''',
    call=f'Solution().domino({N}, {M}, {BROKEN})',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=430),
        dict(type='array', var='q', label='q（BFS 队列，存结点编号；0 = 源点 S，编号 = 行×m+列+1）', h=130, cell=52),
        dict(type='text', fn=_txt, size=22, h=60),
    ],
    watch=[('res', 'res', 'green'), ('now', 'now', 'yellow'), ('head', 'head', 'blue'), ('tail', 'tail', 'pink')],
    skip=['broken_set = set()', 'for x, y in broken', 'broken_set.add', 's = 0', 't = m * n + 1', 'for i in range(n)',
          'for j in range(m)', 'now = i * m + j + 1', 'if now in broken_set', 'continue', 'if (i + j) % 2 == 0',
          'c[s][now]', 'c[now][now', 'c[now][t]', 'c[now + 1][now]', 'c[now + m][now]', 'if j < m - 1', 'if i < n - 1',
          'while True', 'pre[s] = -1', 'head = 0', 'tail = 1', 'q = [s]', 'while head < tail', 'head += 1',
          'for next in range', 'if c[now][next]', 'pre[next] = now', 'q.append', 'tail += 1', 'now = t',
          'while now != s', 'last = pre[now]', 'c[last][now] -= 1', 'c[now][last] += 1', 'now = last', 'break'],
    captions={
        'broken_set': '破损格编号成 `x*m + y + 1`',
        'c = [[0]': '建图：黑格从源点 `S` 进水（容量 1），白格向汇点 `T` 出水（容量 1），黑格 → 相邻白格连边（破损格不参与）',
        'res = 0': '图建好：==一条 S→黑→白→T 的流 = 一块骨牌==；最大流 = 最多骨牌数',
        'pre = [None]': '新一轮 BFS：`pre[k]` 记录从哪个点走到 k，从 `S` 出发找增广路',
        'now = q[head]': lambda S, B, r: f'取出队首 `{_nm(S, S.q[S.head])}`，把它能到达、还没到过的点入队（青框 = 到过）',
        'if pre[t] is None': lambda S, B, r: ('BFS 没能走到汇点 `T` → ==没有增广路了==，最大匹配已找到' if S.pre[S.t] is None
                                               else 'BFS 走到了汇点 `T` → 找到一条增广路'),
        'res += 1': '沿 `pre` 从 `T` 倒推回 `S`：路径上每条边容量 −1、反向边 +1（可反悔）→ 多放一块骨牌，`res` = {res}',
        'return res': '最多放 `{ret}` 块骨牌',
    },
    max_steps=80,
    cards=dict(
        one_liner='骨牌 = 黑白格之间的一条边：二分图最大匹配，用网络流求',
        complexity='时间约 `O(V³)`：至多 `V/2` 次 BFS，每次 `O(V²)`；`V = n·m + 2`；空间 `O(V²)`',
        problem=['`n × m` 的棋盘，有些格子破损（不能放）',
                 '用 `1 × 2` 的骨牌覆盖，骨牌不重叠、不压破损格，求==最多能放几块==',
                 '示例：`n=3, m=3, broken=[[0,0],[2,1],[2,2]]` → `3`'],
        quote='相邻格子间的颜色都互不相同。……一块骨牌实际上就相当于图中的一条边，那么现在的问题就变成了如何从图中选择尽量多的边，且这些边不能连接到同一个节点。这是一个经典的二分图最大匹配问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['国际象棋式黑白染色：相邻的两格一黑一白 → 二分图',
              '建图 `S → 黑格 → 白格 → T`，容量全是 1；一块骨牌 = 一条增广路',
              '边容量都是 1，用 BFS 找增广路，沿路径回溯更新容量并加反向边'],
        result='共 3 块骨牌，第 3 条增广路绕了一圈（用到反向边）',
        summary=['原文已是 Python 3 可运行写法；变量名 `next` 保持原样',
                 '易错：破损格编号是 `x*m + y + 1`，0 号留给源点，`m*n+1` 号是汇点',
                 '易错：只有黑格连向白格，别把方向建反',
                 '做不到的原因是图的结构，不是 BFS 顺序；每轮 BFS 找不到路就结束',
                 '状压 DP 也能做（按行压缩），但网络流/匈牙利更简洁'],
    ),
)
