EDGES = [[0, 1], [1, 2], [2, 0], [1, 3]]
POS = {0: (0.18, 0.30), 1: (0.50, 0.30), 2: (0.34, 0.78), 3: (0.84, 0.30)}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '无向图（蓝 = 当前点，描边 = 已访问；红线 = 割边）', 24, T['muted'], bold=True)
    W, H = x1 - x0, y1 - y0 - 50
    P = {k: (x0 + a * W, y0 + 60 + b * H) for k, (a, b) in POS.items()}
    inner = S.get('_inner', {})
    now = inner.get('now')
    fa = inner.get('fa')
    nxt = inner.get('next')
    dfn, low = S.get('dfn'), S.get('low')
    res = S.get('res') or []
    bridges = {frozenset(e) for e in res}
    for a, b in EDGES:
        c, w = T['border'], 4
        if frozenset((a, b)) in bridges:
            c, w = T['red'], 8
        elif now is not None and nxt is not None and frozenset((a, b)) == frozenset((now, nxt)) and S.get('_line') in (28, 30, 31, 32, 33, 34, 35):
            c, w = T['pink'], 6
        cv.line([P[a], P[b]], c, w)
    r = 38
    for k, (px, py) in P.items():
        seen = dfn is not None and dfn[k] is not None
        cur = (k == now)
        fill = T['blue'] if cur else T['panel2']
        cv.rect((px - r, py - r, px + r, py + r), fill=fill, outline=T['blue'] if seen else T['border'], width=4, r=r)
        cv.text((px, py), k, 36, T['bg'] if cur else T['text'], anchor='mm', bold=True, mono=True)
        if seen:
            lw = low[k] if low[k] is not None else '-'
            cv.text((px, py + r + 8), f'dfn={dfn[k]}  low={lw}', 22, T['cyan'], anchor='mt', bold=True)
        if cur and fa is not None:
            cv.text((px, py - r - 8), f'来自 {fa}', 20, T['muted'], anchor='mb')


def _show(name):
    return lambda S: [('-' if v is None else v) for v in S[name]] if name in S else None


CONFIG = dict(
    num=1192, title='查找集群内的「关键连接」', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='Tarjan 求割边（dfn / low）',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def criticalConnections(self, n, connections):

        g = {}
        for x, y in connections:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)
        
        dfn = [None] * n
        low = [None] * n
        res = []
        self.dfs(0, g, dfn, low, None, res, 0)
        return res

    def dfs(self, now, g, dfn, low, fa, res, cnt):
        dfn[now] = low[now] = cnt
        for next in g.get(now, set()):
            if dfn[next] is None:
                self.dfs(next, g, dfn, low, now, res, cnt + 1)
                low[now] = min(low[now], low[next])
                if low[next] > dfn[now]:
                    res.append([now, next])
            elif next != fa:
                low[now] = min(low[now], dfn[next])
''',
    call='Solution().criticalConnections(4, [[0,1],[1,2],[2,0],[1,3]])',
    expect=[[1, 3]],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='calls', h=190, hide=('g', 'dfn', 'low', 'res')),
        dict(type='stack', var='res', label='res（割边）', h=90, fmt=lambda x: f'{x[0]}-{x[1]}'),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'blue'), ('next', lambda S: S['_inner'].get('next'), 'pink'),
           ('fa', lambda S: S['_inner'].get('fa'), 'cyan')],
    skip=['g = {}', 'for x, y in connections', 'if x not in g', 'if y not in g', 'g[x] = set()', 'g[y] = set()',
          'res = []', 'return res'],
    captions={
        'g[x].add(y)': '建无向图：边 `{x}-{y}`，`g[{x}]` 和 `g[{y}]` 互相加入对方',
        'g[y].add(x)': '邻接表 `g = {g}`',
        'dfn = [None] * n': '`dfn[i]`：点 i 的访问序号，`None` 表示还没访问',
        'low = [None] * n': '`low[i]`：从 i 出发（不走回头路）能到达的最早序号',
        'self.dfs(0, g': '从点 0 开始 dfs，没有来路 `fa = None`，序号从 `0` 开始',
        'dfn[now] = low[now] = cnt': '`dfn[{now}] = low[{now}] = {cnt}`：点 {now} 的序号（这里等于递归深度），初始 low 就是自己',
        'for next in g.get': lambda S, B, r: (
            f'`{S.now}` 的邻居都看完了 → 返回上一层' if S.get('next') == B.get('next') and B.get('next') is not None and S.get('_inner', {}).get('now') == B.get('now')
            else f'枚举 `{S.now}` 的邻居，当前看 `next = {S.next}`'),
        'if dfn[next] is None': lambda S, B, r: (
            f'邻居 `{S.next}` 还没访问 → 它是 dfs 树边，先递归下去' if S.dfn[S.next] is None
            else f'邻居 `{S.next}` 已访问过（`dfn = {S.dfn[S.next]}`）→ 看下面是不是回边'),
        'self.dfs(next, g': '递归进入点 `{next}`：来路 `fa = {B.now}`，序号 `{B.cnt} + 1 = {B.cnt + 1}`',
        'low[now] = min(low[now], low[next])': '`{next}` 子树能回到 `low[{next}] = {low[next]}` → 更新 `low[{now}]` = =={low[now]}==',
        'if low[next] > dfn[now]': lambda S, B, r: (
            f'`low[{S.next}] = {S.low[S.next]} > dfn[{S.now}] = {S.dfn[S.now]}`：{S.next} 这一侧回不到 {S.now} 或更早的点 → ==边 {S.now}-{S.next} 是割边=='
            if S.low[S.next] > S.dfn[S.now]
            else f'`low[{S.next}] = {S.low[S.next]} ≤ dfn[{S.now}] = {S.dfn[S.now]}`：{S.next} 这一侧能绕回来（在环上）→ 不是割边'),
        'res.append([now, next])': '记录割边 `[{now}, {next}]` → `res = {res}`',
        'elif next != fa': lambda S, B, r: (
            f'`{S.next}` 就是来路 `fa` → 这条边只是刚走过的树边，跳过' if S.next == S.fa
            else f'`{S.next}` 已访问且不是来路 → ==回边=='),
        'low[now] = min(low[now], dfn[next])': '回边回到序号 `dfn[{next}] = {dfn[next]}` → `low[{now}]` 更新为 =={low[now]}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='dfs 时记 dfn 和 low：子树回不到我或更早 → 割边',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['`n` 台服务器，由 `connections` 里的无向边连成一个网络',
                 '找出所有==关键连接==：删掉它之后，有服务器会和其它服务器断开',
                 '本视频：`n = 4`，边 `[[0,1],[1,2],[2,0],[1,3]]` → `[[1,3]]`'],
        quote='若 `low[next] > dfn[now]`，说明 next 没有方法回到 now 或者比 now 更早的节点，也就是说从 now 到 next 只有这唯一的一条边，因此这条边必然是割边。',
        quote_src='—— yiduobo 题解原文',
        idea=['`dfn`：dfs 的访问序号；`low`：不走回头路，从这个点能回到的最早序号',
              '回边 `now → next`（next 已访问且不是来路）会把 `low[now]` 拉低',
              '树边 `now → next` 递归回来后：`low[next] > dfn[now]` 就说明 next 一侧回不去 → 割边'],
        summary=['时间 `O(n + m)`，空间 `O(n + m)`；Tarjan 求割边',
                 '`elif next != fa`：来路这条边不能当回边，否则所有边都会被算成环',
                 '原文传的 `cnt + 1` 是==递归深度==而不是全局计数，沿祖先链仍然保持递增，所以结果正确',
                 '原文是 Python 2 风格，代码无需修改，直接运行',
                 '同类题：1568 使陆地分离的最少天数（割点）'],
    ),
)
