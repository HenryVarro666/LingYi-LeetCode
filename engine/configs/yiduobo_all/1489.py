N0 = 4
EDGES = [[0, 1, 1], [1, 2, 1], [2, 3, 2], [0, 3, 2], [1, 3, 5]]
POS = {0: (0.10, 0.80), 1: (0.28, 0.10), 2: (0.62, 0.85), 3: (0.90, 0.35)}
LBL = {0: 0.5, 1: 0.5, 2: 0.5, 3: 0.3, 4: 0.5}


def _state(S):
    """sorted edges / group bounds / classification of each original edge index"""
    se = S.get('edges')
    sorted_ok = bool(se) and len(se[0]) == 4
    crit = list(S.get('critical', []) or [])
    pseu = list(S.get('pseudo', []) or [])
    l = S.get('l', 0) if sorted_ok else 0
    r = S.get('r', 0) if sorted_ok else 0
    st = {}
    cur = set()
    if sorted_ok:
        for pos, (x, y, w, idx) in enumerate(se):
            if idx in crit:
                st[idx] = 'critical'
            elif idx in pseu:
                st[idx] = 'pseudo'
            elif pos < l:
                st[idx] = 'dropped'
            elif l <= pos < r and 'r' in S and S.get('_line', 0) >= 17:
                st[idx] = 'cur'
                cur.add(idx)
            else:
                st[idx] = 'wait'
    else:
        for i in range(len(EDGES)):
            st[i] = 'wait'
    return sorted_ok, se, st, cur


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    sorted_ok, se, st, cur = _state(S)
    me = S.get('self')
    cut = set(getattr(me, 'cut_edge', set()) or set())
    pse = set(getattr(me, 'pseudo_edge', set()) or set())
    cv.text((x0 + 18, y0 + 4), '绿 = 关键边　黄 = 伪关键边　蓝 = 当前组　红虚线 = 多余的边', 20, T['muted'], bold=True)
    gx0, gy0 = x0 + 50, y0 + 60
    gw, gh = (x1 - x0) - 100, (y1 - y0) - 60 - 190
    P = {k: (gx0 + v[0] * gw, gy0 + v[1] * gh) for k, v in POS.items()}
    # components from finalized edges
    par = list(range(N0))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for i, (x, y, w) in enumerate(EDGES):
        if st.get(i) in ('critical', 'pseudo'):
            par[find(x)] = find(y)
    colors = ['cyan', 'purple', 'orange', 'pink', 'blue', 'green']
    roots = sorted({find(k) for k in range(N0)})
    ccol = {rt: colors[j % len(colors)] for j, rt in enumerate(roots)}
    for i, (x, y, w) in enumerate(EDGES):
        s = st.get(i, 'wait')
        if s == 'cur':
            s = 'critical_p' if i in cut else ('pseudo_p' if i in pse else 'cur')
        col = {'critical': T['green'], 'critical_p': T['green'], 'pseudo': T['yellow'], 'pseudo_p': T['yellow'],
               'dropped': T['red'], 'cur': T['blue'], 'wait': (95, 103, 115)}[s]
        wd = 3 if s == 'wait' else 7
        if s == 'dropped':
            cv.dashed(P[x], P[y], col, 4)
        else:
            cv.line([P[x], P[y]], col, wd)
        t = LBL.get(i, 0.5)
        mx, my = P[x][0] + (P[y][0] - P[x][0]) * t, P[x][1] + (P[y][1] - P[x][1]) * t
        cv.rect((mx - 44, my - 16, mx + 44, my + 16), fill=T['bg'], r=8)
        cv.text((mx, my), f'e{i}:{w}', 22, col if s != 'wait' else T['muted'], anchor='mm', bold=True, mono=True)
    for k in range(N0):
        X, Y = P[k]
        cv.rect((X - 28, Y - 28, X + 28, Y + 28), fill=T['panel2'], outline=T[ccol[find(k)]], width=5, r=28)
        cv.text((X, Y), k, 28, T['text'], anchor='mm', bold=True)
    # 当前 tarjan 所在的“连通分量缩点”说明
    if sorted_ok and 'cnt' in S and S.get('_line', 0) >= 28:
        cv.text((x0 + 18, y1 - 168), f"当前组建出的缩点图：{S['cnt']} 个连通分量（圈的颜色 = 并查集分量）", 22, T['cyan'], bold=True)
    # 排序后的边条
    yb = y1 - 130
    cv.text((x0 + 18, yb - 4), '按权重排序后的边，同权重分成一组（竖线分隔）', 20, T['muted'], bold=True)
    if sorted_ok:
        n = len(se)
        cell = min(150, (x1 - x0 - 40) / n)
        sx = x0 + 20
        for pos, (x, y, w, idx) in enumerate(se):
            s = st.get(idx, 'wait')
            fill = {'critical': T['green'], 'pseudo': T['yellow'], 'dropped': T['red'], 'cur': T['blue'], 'wait': T['panel2']}[s]
            X = sx + pos * cell
            cv.rect((X + 3, yb + 30, X + cell - 3, yb + 100), fill=fill, r=8, outline=T['border'], alpha=255 if s != 'wait' else 255)
            cv.text((X + cell / 2, yb + 52), f'e{idx}  w={w}', 20, T['bg'] if s != 'wait' else T['muted'], anchor='mm', bold=True, mono=True)
            cv.text((X + cell / 2, yb + 80), f'{x}-{y}', 22, T['bg'] if s != 'wait' else T['muted'], anchor='mm', bold=True, mono=True)
            if pos > 0 and se[pos - 1][2] != w:
                cv.line([(X, yb + 24), (X, yb + 108)], T['text'], 3)
    else:
        cv.text((x0 + 20, yb + 50), '（还没排序）', 22, T['dim'])


def _sum(S):
    ok, se, st, cur = _state(S)
    c = [i for i, v in st.items() if v == 'critical']
    p = [i for i, v in st.items() if v == 'pseudo']
    return f'关键边 `critical = {sorted(c)}`　伪关键边 `pseudo = {sorted(p)}`'


CONFIG = dict(
    num=1489, title='找到最小生成树里的关键边和伪关键边', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='分组 Kruskal + Tarjan 求桥',
    tags=['灵神题单·图论算法'],
    code='''
class Solution(object):
    def findCriticalAndPseudoCriticalEdges(self, n, edges):

        edges = sorted([[x, y, w, index] for index, [x, y, w] in enumerate(edges)], key=lambda d:d[2])
        m = len(edges)
        l = 0
        fa = list(range(n))
        critical = []
        pseudo = []
        while l < m:
            r = l + 1
            while r < m and edges[r][2] == edges[l][2]:
                r += 1

            candidate = []
            cnt = 0
            g = {}
            node_mapping = {}
            self.pseudo_edge = set()
            for x, y, w, index in edges[l : r]:
                fa_x = self.find(x, fa)
                fa_y = self.find(y, fa)

                if fa_x != fa_y:
                    candidate.append([x, y, index])

                    if fa_x not in node_mapping:
                        node_mapping[fa_x] = cnt
                        cnt += 1
                    node_x = node_mapping[fa_x]
                    if node_x not in g:
                        g[node_x] = {}

                    if fa_y not in node_mapping:
                        node_mapping[fa_y] = cnt
                        cnt += 1
                    node_y = node_mapping[fa_y]
                    if node_y not in g:
                        g[node_y] = {}

                    if node_y in g[node_x]:
                        self.pseudo_edge.add(g[node_x][node_y])
                        self.pseudo_edge.add(index)
                    else:
                        g[node_x][node_y] = g[node_y][node_x] = index

            self.cut_edge = set()
            self.dfs_order = 0
            low = [None] * cnt
            dfn = [None] * cnt
            for now in range(cnt):
                if dfn[now] is None:
                    self.tarjan(now, None, g, low, dfn)

            for x, y, index in candidate:
                if index in self.cut_edge:
                    critical.append(index)
                else:
                    pseudo.append(index)
                
                fa_x = self.find(x, fa)
                fa_y = self.find(y, fa)
                if fa_x < fa_y:
                    fa[fa_y] = fa_x
                else:
                    fa[fa_x] = fa_y
            
            l = r

        return [critical, pseudo]
                
    def tarjan(self, now, fa, g, low, dfn):
        low[now] = dfn[now] = self.dfs_order
        self.dfs_order += 1
        for next, index in g[now].items():
            if dfn[next] is None:
                self.tarjan(next, index, g, low, dfn)
                low[now] = min(low[now], low[next])
                if low[next] > dfn[now] and index not in self.pseudo_edge:
                    self.cut_edge.add(index)
            elif index != fa:
                low[now] = min(low[now], dfn[next])

    def find(self, x, fa):
        if x != fa[x]:
            fa[x] = self.find(fa[x], fa)
        return fa[x]
''',
    call='Solution().findCriticalAndPseudoCriticalEdges(4, [[0,1,1],[1,2,1],[2,3,2],[0,3,2],[1,3,5]])',
    expect=[[0, 1], [2, 3]],
    views=[
        dict(type='custom', draw=_draw, h=560),
        dict(type='text', fn=_sum, size=26, h=50),
        dict(type='array', var='dfn', label='dfn（dfs 序）', h=140, cell=52),
        dict(type='array', var='low', label='low（回边能到的最小 dfs 序）', h=140, cell=52),
    ],
    max_steps=110,
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('critical', 'critical', 'green'), ('pseudo', 'pseudo', 'yellow')],
    skip=['self.pseudo_edge.add(index)', 'l = r', 'critical.append', 'pseudo.append', 'self.pseudo_edge.add(g[node_x][node_y])', 'g[node_x][node_y] = g[node_y][node_x]', 'for x, y, w, index in', 'for next, index in g[now].items()', 'for now in range', 'if fa_x < fa_y', 'self.pseudo_edge = set()', 'while r < m and', 'l = 0', 'fa_x = self.find', 'fa_y = self.find', 'dfn = [None]', 'low = [None]', 'self.dfs_order += 1', 'if dfn[now] is None', 'low[now] = min(low[now], dfn[next])', 'if x != fa[x]', 'fa[x] = self.find', 'r = l + 1', 'cnt = 0', 'candidate.append', 'm = len(edges)', 'candidate = []', 'g = {}', 'node_mapping = {}', 'node_x = ', 'node_y = ', 'if node_x not in g', 'if node_y not in g',
          'g[node_x] = {}', 'g[node_y] = {}', 'self.dfs_order = 0', 'self.cut_edge = set()', 'critical = []', 'pseudo = []', 'if fa_x not in node_mapping',
          'if fa_y not in node_mapping', 'node_mapping[fa_', 'cnt += 1', 'r += 1', 'return fa[x]'],
    captions={
        'edges = sorted': '边按权重从小到大排序，同时带上原下标：`{[(e[3], e[2]) for e in edges]}`（下标, 权重）',
        'fa = list(range(n))': '并查集 `fa`：一开始每个点自成一个连通分量',
        'while l < m': lambda S, B, r: ('所有分组都处理完了 → 结束' if S.l >= len(S.edges) else (f'`l = {S.l} < m`：上一组处理完了，还有边 → 开始新的一组' if S.l > 0 else '`l = 0 < m`：开始处理第一组')),
        'while r < m and': '权重等于 `{edges[l][2]}` 的边划成一组，向后扩：目前是 `edges[{l}:{r}]`',
        'if fa_x != fa_y': lambda S, B, r: (f'`{S.fa_x} ≠ {S.fa_y}`：这条边连接两个不同分量 → ==候选边==（关键或伪关键）' if S.fa_x != S.fa_y
                                             else f'`fa_x = fa_y = {S.fa_x}`：两端早已连通，且之前的边权更小 → ==这条边完全不需要==，直接丢掉'),
        'candidate.append': '`e{index}` 记入候选边 `candidate`',
        'if node_y in g[node_x]': lambda S, B, r: (f'缩点图里分量 `{S.node_x}` — `{S.node_y}` 之间已经有一条边 `e{S.g[S.node_x][S.node_y]}` → 两条==平行边==，互相可替代 → `e{S.g[S.node_x][S.node_y]}` 和 `e{S.index}` 都是伪关键边' if S.node_y in S.g[S.node_x]
                                                    else f'缩点图里分量 `{S.node_x}` — `{S.node_y}` 之间还没有边 → 把 `e{S.index}` 加进去'),
        'self.tarjan(now, None': '这组候选边已建成缩点图（共 `{cnt}` 个点）→ ==Tarjan 找桥==：从点 `{now}` 开始 dfs，`dfn` 是 dfs 序，`low` 是回边能到的最小 dfs 序',
        'if dfn[now] is None': lambda S, B, r: (f'`dfn[{S.now}]` 还没访问 → 从它开始 dfs' if S.dfn[S.now] is None else f'`dfn[{S.now}] = {S.dfn[S.now]}` 已访问过，跳过'),
        'low[now] = dfn[now] = self.dfs_order': '给点 `{now}` 编号：`dfn[{now}] = low[{now}] = {dfn[now]}`',
        'self.dfs_order += 1': 'dfs 序计数加一：`dfs_order = {self.dfs_order}`',
        'if dfn[next] is None': lambda S, B, r: (f'`dfn[{S.next}]` 为空：没访问过 → 沿树边 `e{S.index}` 递归过去' if S.dfn[S.next] is None
                                                 else f'`dfn[{S.next}] = {S.dfn[S.next]}`：已访问过 → 这是条回边或父边'),
        'self.tarjan(next, index': '递归进入 `{next}`，记下父边 `e{index}`',
        'low[now] = min(low[now], low[next])': '子树的回边也算上：`low[{now}] = min({B.low[now]}, {low[next]}) = {low[now]}`',
        'if low[next] > dfn[now]': lambda S, B, r: (
            f'`low[{S.next}] = {S.low[S.next]} > dfn[{S.now}] = {S.dfn[S.now]}`：子树出不去 → 边 `e{S.index}` 是==桥==，且不是平行边 → 关键边' if S.low[S.next] > S.dfn[S.now] and S.index not in S.self.pseudo_edge
            else f'`low[{S.next}] = {S.low[S.next]} > dfn[{S.now}]` 但 `e{S.index}` 有平行边可替代 → 不是关键边' if S.low[S.next] > S.dfn[S.now]
            else f'`low[{S.next}] = {S.low[S.next]} ≤ dfn[{S.now}] = {S.dfn[S.now]}`：子树能绕回来 → 不是桥'),
        'self.cut_edge.add(index)': '`e{index}` 加入桥集合：`cut_edge = {sorted(self.cut_edge)}`',
        'elif index != fa': '`e{index}` 不是父边 → 是回边：用 `dfn[{next}]` 更新 `low[{now}]`',
        'low[now] = min(low[now], dfn[next])': '`low[{now}] = {low[now]}`',
        'if index in self.cut_edge': lambda S, B, r: (f'`e{S.index}` 在桥集合中 → ==关键边==，加入 critical' if S.index in S.self.cut_edge else f'`e{S.index}` 不是桥 → ==伪关键边==（可被同权重的边替代），加入 pseudo'),
        'fa[fa_y] = fa_x': '这组边分类完后再合并并查集（先分类再合并，同组边才互不影响）：`fa[{fa_y}] = {fa_x}`',
        'fa[fa_x] = fa_y': '合并并查集：`fa[{fa_x}] = {fa_y}`',
        'l = r': '这一组处理完，`l` 跳到下一组起点 `{r}`',
        'return [critical': '关键边 `{critical}`，伪关键边 `{pseudo}`',
    },
    cards=dict(
        one_liner='相同权重分一组做 Kruskal，组内用 Tarjan 找桥',
        complexity='时间 `O(m log m)`，空间 `O(n + m)`',
        problem=['无向连通加权图，`edges[i] = [a, b, w]`。找最小生成树（MST）的两类边',
                 '==关键边==：删掉它 MST 权值变大；==伪关键边==：有的 MST 含它，有的不含，但不是关键边',
                 '本视频：4 个点，边 `[[0,1,1],[1,2,1],[2,3,2],[0,3,2],[1,3,5]]` → `[[0,1], [2,3]]`'],
        quote='不再一条条边进行处理，而是对于权值相同的边一组组来进行处理。',
        quote_src='—— yiduobo 题解原文',
        idea=['边按权重排序，同权重分组。组内某条边两端已连通 → 之前的边更小 → ==完全不需要==',
              '其余边是候选：在「并查集分量缩点」的图上求桥，桥 = ==关键边==，其余 = ==伪关键边==',
              '同一对分量之间的平行边互相可替代，直接记为伪关键边；分类完才合并并查集'],
        summary=['时间 `O(m log m)`：排序为主，每组建图 + Tarjan 总共只扫每条边一次',
                 '易错：同权重的边必须先全部分类、再统一合并并查集，不能边分类边合并',
                 '易错：缩点图的点是 `find(x)` 的代表，不是原来的节点；平行边不能算桥',
                 '原文为 Python 2 写法，`fa = range(n)` 已改为 `fa = list(range(n))`（Python 3 的 range 不能赋值）',
                 '本视频：权重 1 的 `e0 e1` 把 0-1-2 串成链，各自是桥 → 关键；权重 2 的 `e2 e3` 都连向 3 → 互相可替代 → 伪关键；`e4` 权重 5 且 1、3 已连通 → 丢弃'],
    ),
)
