POS = {'EUR': (0.1, 0.18), 'USD': (0.9, 0.18), 'JPY': (0.9, 0.82), 'CHF': (0.1, 0.82)}


def _fmt(v):
    return f'{v:.4g}'


def _draw(cv, S, B, box, T):
    import math
    x0, y0, x1, y1 = box
    inn = S['_inner']
    gg = inn.get('g')
    if not isinstance(gg, dict):
        gg = S.get('g2') or S.get('g1') or {}
    p1, p2 = S.get('pairs1'), S.get('pairs2')
    if p1 is None:
        return
    day = 1 if ('g1' not in S or gg == S['g1']) else 2
    ps, rs = (p1, S['rates1']) if day == 1 else (p2, S['rates2'])
    orient = {(a, b): rt for (a, b), rt in zip(ps, rs)}
    rr = inn.get('r')
    rr = rr if isinstance(rr, dict) else {}
    cur = inn.get('x') if isinstance(rr, dict) and rr and 'q' in inn else None
    nxt = inn.get('y') if cur else None
    gw = (x1 - x0) * 0.58
    R = 46

    def P(u):
        fx, fy = POS[u]
        return x0 + 70 + fx * (gw - 140), y0 + 90 + fy * (y1 - y0 - 220)

    cv.text((x0 + 20, y0 + 12), f'第 {day} 天汇率图（箭头旁 = 汇率）', 22, T['muted'], bold=True)
    for (a, b), rt in orient.items():
        if not (a in gg and b in gg[a]):
            continue
        (ax, ay), (bx, by) = P(a), P(b)
        d = math.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / d, (by - ay) / d
        hot = (cur == a and nxt == b) or (cur == b and nxt == a)
        cv.arrow((ax + ux * R, ay + uy * R), (bx - ux * (R + 4), by - uy * (R + 4)),
                 T['yellow'] if hot else T['muted'], 6 if hot else 3, 16 if hot else 12)
        cv.text(((ax + bx) / 2 - uy * 24, (ay + by) / 2 + ux * 24), f'×{rt}', 24, T['yellow'] if hot else T['cyan'],
                anchor='mm', bold=True)
    for u in POS:
        X, Y = P(u)
        seen = u in rr
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=T['green'] if seen else T['panel2'],
                     outline=T['yellow'] if u == cur else T['border'], width=6 if u == cur else 2)
        cv.text((X, Y - (12 if seen else 0)), u, 22, T['bg'] if seen else T['text'], anchor='mm', bold=True)
        if seen:
            cv.text((X, Y + 16), _fmt(rr[u]), 22, T['bg'], anchor='mm', bold=True)
    lx = x0 + gw + 20
    yy = y0 + 16
    for name, dct, c in (('r（本次 BFS）', rr, 'yellow'), ('r1', S.get('r1'), 'cyan'), ('r2', S.get('r2'), 'orange')):
        if not dct:
            continue
        cv.text((lx, yy), name, 21, T[c], bold=True)
        yy += 36
        for k, v in dct.items():
            cv.text((lx + 12, yy), f'{k}: {_fmt(v)}', 22, T['text'], mono=True)
            yy += 30
        yy += 12


def _chk(S, B, ret):
    y = S.y
    if y in B.r:
        return f'`{S.x}` 的邻居 `{y}` 已经在 `r` 里 → 算过了，跳过'
    return f'`{S.x}` 的邻居 `{y}` 不在 `r` 里 → 第一次到达，要算金额并入队'


def _ret(S, B, ret):
    return f'枚举同时出现在 r1、r2 里的货币：`r1[tmp] / r2[tmp]` 取最大 → =={_fmt(ret)}=='


CONFIG = dict(
    num=3387, title='两天自由外汇交易后的最大货币数', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='建图 + 两次 BFS · 枚举中转货币',
    tags=['灵神题单', '图论算法', '难度分 1788'],
    code='''
class Solution(object):
    def maxAmount(self, initialCurrency, pairs1, rates1, pairs2, rates2):
        
        def build_graph(pairs, rates):
            g = {}
            for p, r in zip(pairs, rates):
                x, y = p
                if x not in g:
                    g[x] = {}
                if y not in g:
                    g[y] = {}
                g[x][y] = r
                g[y][x] = 1 / r
            
            return g
        
        def calc(g):
            q = [initialCurrency]
            r = {initialCurrency : 1.0}
            head, tail = 0, 1
            while head < tail:
                for x in q[head : tail]:
                    for y in g.get(x, {}):
                        if y not in r:
                            r[y] = r[x] * g[x][y]
                            q.append(y)
                
                head, tail = tail, len(q)
            
            return r
        
        g1 = build_graph(pairs1, rates1)
        g2 = build_graph(pairs2, rates2)
        r1 = calc(g1)
        r2 = calc(g2)
        res = 0
        for tmp in r1:
            if tmp in r2:
                r = r1[tmp] / r2[tmp]
                res = max(res, r)
        return res
''',
    call='Solution().maxAmount("EUR", [["EUR","USD"],["USD","JPY"]], [2.0,3.0], [["JPY","USD"],["USD","CHF"],["CHF","EUR"]], [4.0,5.0,6.0])',
    expect=720.0,
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='queue', var='q', label='q（BFS 队列，head ~ tail 是当前层）', h=130),
    ],
    watch=[('head', 'head', 'cyan'), ('tail', 'tail', 'cyan'), ('res', 'res', 'green')],
    skip=['g = {}', 'x, y = p', 'if x not in g', 'g[x] = {}', 'if y not in g', 'g[y] = {}', 'return g', 'return r',
          'for p, r in zip', 'for x in q[head', 'for tmp in r1', 'q = [initial', 'g[y][x] = 1 / r', 'head, tail = 0, 1', 'for y in g.get', 'if tmp in r2'],
    max_steps=90,
    captions={
        'g[x][y] = r': '建图：`{x} → {y}` 汇率 `{r}`（下一行同时建反向边 `1 / {r}`）',
        'r = {initialCurrency': '`r[{initialCurrency}] = 1.0`：起点金额 1.0，`r` 记录 1 单位能换到的各货币金额',
        'while head < tail': lambda S, B, ret: (f'`head = {S.head} < tail = {S.tail}`：当前层还有货币，继续' if S.head < S.tail
                                                else f'`head = tail = {S.tail}`：没有新货币了，BFS 结束'),
        'if y not in r': _chk,
        'r[y] = r[x] * g[x][y]': '`r[{y}] = r[{x}] × g[{x}][{y}] = {r[x]:.4g} × {g[x][y]:.4g}` = =={r[y]:.4g}==',
        'q.append(y)': '`{y}` 入队，下一层再扩展它：`q = {q}`',
        'head, tail = tail': '这一层处理完：`head, tail = {head}, {tail}`，下一层是 `q[{head}:{tail}]`',
        'res = 0': '`res = 0`：记录最大的 r1[tmp] / r2[tmp]',
        'r = r1[tmp] / r2[tmp]': '经 `{tmp}` 中转：第 1 天换到 `{r1[tmp]:.4g}`，第 2 天换回 1 单位要 `{r2[tmp]:.4g}` → =={r:.4g}==',
        'res = max(res, r)': '`res = max({B.res:.4g}, {r:.4g})` = =={res:.4g}==',
        'return res': _ret,
    },
    cards=dict(
        one_liner='两天各 BFS 一次，经 tmp 中转：r1[tmp] / r2[tmp] 取最大',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['初始 1.0 单位 `initialCurrency`，两天各有一组汇率，可任意次兑换',
                 '每对货币反向汇率为 `1 / rate`，求两天后最多有多少初始货币',
                 '示例：`EUR` 两天汇率如图 → `720.0`'],
        quote='分别计算出两天内1单位的initialCurrency可以兑换的各种货币的数量，分别记为r1和r2。接下来枚举每种同时出现在r1和r2中的货币tmp，……可以的得到的initialCurrency就是r1[tmp] / r2[tmp]。',
        quote_src='—— yiduobo 题解原文',
        idea=['货币是点，兑换是带权边；正反两条边，权重是 `rate` 和 `1/rate`',
              '题目保证图中没有循环，所以 BFS 第一次到一个点算出的金额就对',
              '第 2 天把 tmp 换回初始货币，相当于除以 `r2[tmp]`'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`（货币名长度视为常数）',
                 '==`y not in r` 才入队==：每个货币只算一次金额',
                 '`res` 初值 0：初始货币自己就在 r1、r2 里，比值至少是 1',
                 '原文是 Python 2 写法，这里代码无需改动，`1 / r` 的 r 是浮点数',
                 '对比灵神：灵神用递归 DFS，yiduobo 用 BFS 分层，结果相同'],
    ),
)
