def _tree_consts(n, edges, sort_ch=False):
    g = [[] for _ in range(n)]
    for e in edges:
        g[e[0]].append(e[1])
        g[e[1]].append(e[0])
    par = [-1] * n
    ch = [[] for _ in range(n)]
    ent, ext, clk = [0] * n, [0] * n, [0]
    dep = [0] * n

    def go(u, p):
        par[u] = p
        ent[u] = clk[0]
        clk[0] += 1
        for v in (sorted(g[u]) if sort_ch else g[u]):
            if v != p:
                ch[u].append(v)
                dep[v] = dep[u] + 1
                go(v, u)
        ext[u] = clk[0]
        clk[0] += 1
    go(0, -1)
    xs, cnt = [0.0] * n, [0]

    def lay(u):
        if not ch[u]:
            xs[u] = cnt[0]
            cnt[0] += 1
        else:
            for v in ch[u]:
                lay(v)
            xs[u] = (xs[ch[u][0]] + xs[ch[u][-1]]) / 2
    lay(0)
    return dict(n=n, ch=ch, par=par, ent=ent, ext=ext, dep=dep, xs=xs, leaves=max(cnt[0], 1), maxd=max(dep))


def _tree_draw(tc, state, label, note=None, live=None, title='', elab=None, width_cap=170):
    """state(S) -> (cur, T): 当前节点 / 时钟（ext[u] <= T 的节点算已完成）；cur=None 表示未开始"""
    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        n, ch, par, ext = tc['n'], tc['ch'], tc['par'], tc['ext']
        cur, tm = state(S, B)
        path = set()
        u = cur
        while u is not None and u >= 0:
            path.add(u)
            u = par[u]
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
        W = x1 - x0 - 120
        dx = min(width_cap, W / max(1, tc['leaves'] - 1)) if tc['leaves'] > 1 else 0
        sx = x0 + 60 + (W - dx * (tc['leaves'] - 1)) / 2
        H = y1 - y0 - 100
        dy = min(120, H / max(1, tc['maxd']))
        R = 24
        P = [(sx + tc['xs'][i] * dx, y0 + 60 + tc['dep'][i] * dy) for i in range(n)]
        for u in range(n):
            for v in ch[u]:
                on = v in path and u in path
                cv.line([P[u], P[v]], T['yellow'] if on else T['border'], 4 if on else 3)
                if elab:
                    mx, my = (P[u][0] + P[v][0]) / 2, (P[u][1] + P[v][1]) / 2
                    cv.text((mx + 12, my), str(elab[(u, v)]), 22, T['orange'], anchor='lm', bold=True)
        for u in range(n):
            x, y = P[u]
            done = tm is not None and ext[u] <= tm
            if u == cur:
                fill, tc_ = T['yellow'], T['bg']
            elif u in path:
                fill, tc_ = T['blue'], T['bg']
            elif done:
                fill, tc_ = T['green'], T['bg']
            else:
                fill, tc_ = T['panel2'], T['text']
            cv.rect((x - R, y - R, x + R, y + R), fill=fill, outline=T['border'], r=R)
            cv.text((x, y), label(u), 24, tc_, anchor='mm', bold=True)
            cv.text((x - R - 4, y - R - 2), str(u), 18, T['dim'], anchor='rb', mono=True)
            if live and u == cur:
                s = live(S, u)
                if s:
                    cv.text((x + R + 8, y), s, 22, T['yellow'], anchor='lm', bold=True)
            elif note and done:
                s = note(u)
                if s:
                    cv.text((x + R + 8, y), s, 22, T['green'], anchor='lm', bold=True)
    return draw


EDGES = [[0, 1, 4], [0, 2, 2], [2, 3, 12], [2, 4, 6]]
K = 2
NN = 5
TC = _tree_consts(NN, EDGES)
ELAB = {(e[0], e[1]): e[2] for e in EDGES}
WT = dict(ELAB)


def _res(u, kk=K):
    nc_sum, inc = 0, []
    for c in TC['ch'][u]:
        nc, cc = _res(c)
        nc_sum += nc
        d = cc + WT[(u, c)] - nc
        if d > 0:
            inc.append(d)
    inc.sort(reverse=True)
    return nc_sum + sum(inc[:kk]), nc_sum + sum(inc[:kk - 1])


def _state(S, B=None):
    line = S.get('_line', 0)
    I = B['_inner'] if line == 18 and B is not None else S['_inner']
    x = I.get('x')
    if x is None:
        return None, (10 ** 6 if line >= 25 else None)
    y, g = I.get('y'), S['g']
    kids = TC['ch'][x]
    if line in (13, 14):
        t = TC['ent'][x]
    elif line == 24:
        t = TC['ext'][x]
    elif line == 22:
        t = TC['ext'][kids[-1]] if kids else TC['ent'][x]
    else:
        incl = (line == 15 and B is not None and y is not None and B['_inner'].get('y') == y) or line in (19, 20, 21)
        done = []
        for z, _w in g[x]:
            if z == y and not incl:
                break
            if z in kids:
                done.append(z)
            if z == y:
                break
        t = TC['ext'][done[-1]] if done else TC['ent'][x]
    return x, t


def _live(S, u):
    I = S['_inner']
    if S['_line'] >= 15 and 'not_choose' in I:
        return f"nc={I['not_choose']}"
    return ''


def _fml(S):
    I = S['_inner']
    if 'x' not in I or 'inc' not in I:
        return f'每个点最多保留 `k = {K}` 条边；`dfs` 返回 `(至多选 k 条, 至多选 k-1 条)`'
    return f"不选的基础和 `not_choose = {I.get('not_choose', 0)}`，候选增量 `inc = {I['inc']}`"


CONFIG = dict(
    num=3367, title='移除边之后的权重最大和', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='树形 DP + 贪心（增量排序）',
    tags=['灵神题单·动态规划', '难度分 2602'],
    code='''
class Solution:
    def maximizeSumOfWeights(self, edges: List[List[int]], k: int) -> int:
        g = [[] for _ in range(len(edges) + 1)]
        for x, y, wt in edges:
            g[x].append((y, wt))
            g[y].append((x, wt))

        # 优化
        if all(len(to) <= k for to in g):
            return sum(e[2] for e in edges)

        def dfs(x: int, fa: int) -> Tuple[int, int]:
            not_choose = 0
            inc = []
            for y, wt in g[x]:
                if y == fa:
                    continue
                nc, c = dfs(y, x)
                not_choose += nc  # 先都不选
                if (d := c + wt - nc) > 0:
                    inc.append(d)
            inc.sort(reverse=True)
            # 再选增量最大的 k 个或者 k-1 个
            return not_choose + sum(inc[:k]), not_choose + sum(inc[:k - 1])
        return dfs(0, -1)[0]  # not_choose >= choose
''',
    call='Solution().maximizeSumOfWeights(EDGES, K)',
    setup='EDGES = [[0, 1, 4], [0, 2, 2], [2, 3, 12], [2, 4, 6]]\nK = 2',
    expect=22,
    views=[
        dict(type='text', size=24, h=60, fn=_fml),
        dict(type='custom', h=380, draw=_tree_draw(TC, _state, lambda u: str(u), note=lambda u: f'{_res(u)}', live=_live, elab=ELAB,
                                                   title='树：橙色 = 边权，旁注 = dfs 返回的 (至多选 k 条, 至多选 k-1 条)')),
        dict(type='array', var='inc', label='inc（选这条边的增量，非正数不进来）', cell=70, h=140),
        dict(type='calls', h=150),
    ],
    watch=[('x', 'x', 'blue'), ('not_choose', 'not_choose', 'cyan'), ('nc', 'nc', 'orange'), ('c', 'c', 'green'), ('d', 'd', 'pink')],
    skip=['g = [[] for', 'for x, y, wt in edges', 'g[x].append', 'g[y].append', 'continue'],
    max_steps=90,
    captions={
        'if all(len(to) <= k': lambda S, B, r: (f'优化：所有点度数 ≤ k = {K} 才能一条边都不删；这里最大度数是 `{max(len(t) for t in S.g)}` → 不满足，要真的做 DP'
                                                 if max(len(t) for t in S.g) > K else '所有点度数都 ≤ k：一条边都不用删，直接返回边权和'),
        'return sum(e[2]': '度数都不超过 k：直接返回所有边权之和',
        'not_choose = 0': '`not_choose`：假设 `x` 连往儿子的边==全都不选==，各儿子子树（至多选 k 条）的最优和',
        'inc = []': '`inc` 记录改成“选”这条边之后，总和==增加多少==',
        'for y, wt in g[x]': lambda S, B, r: (f'儿子都看完了：`not_choose = {S.not_choose}`，`inc = {S.inc}`' if 'y' in B and B.y == S.y
                                              else f'看 `x = {S.x}` 的下一条边：`y = {S.y}`，边权 `wt = {S.wt}`'),
        'if y == fa': lambda S, B, r: (f'`y = {S.y}` 是父节点，跳过' if S.y == S.fa else f'`y = {S.y}` 是儿子，继续往下'),
        'nc, c = dfs(y, x)': '进入儿子 `{y}`：返回 `(nc, c)` = 它子树里 与 `x` 的边==不选 / 选==时的最优和',
        'not_choose += nc': '先都不选：`not_choose` 加上 `nc = {nc}` → =={not_choose}==',
        'if (d := c + wt - nc) > 0': lambda S, B, r: (f'选边 `{S.x}-{S.y}` 的增量 `d = c + wt - nc = {S.c} + {S.wt} - {S.nc}` = `{S.d}` > 0 → ==值得选==，放进 `inc`'
                                                       if S.d > 0 else f'增量 `d = {S.c} + {S.wt} - {S.nc}` = `{S.d}` ≤ 0 → 选了反而亏，不进 `inc`'),
        'inc.append(d)': '`inc` 追加 `{d}` → `{inc}`',
        'inc.sort': '增量==从大到小==排序：优先选增量最大的边（贪心，同「老鼠和奶酪」）',
        'return not_choose + sum(inc[:k])': '`x` 最多选 `k = {k}` 条：`{not_choose} + {sum(inc[:k])}` = =={ret[0]}==；给父亲留一条边名额，只能选 `k-1` 条：=={ret[1]}==',
        'return dfs(0, -1)[0]': lambda S, B, r: '从根 0 开始；答案取 `not_choose ≥ choose` 的第一个值' if r is None else f'答案 = `dfs(0, -1)[0]` = =={r}=='
    },
    cards=dict(
        one_liner='选或不选一条边：用「增量」排序，选最大的 k 个',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['无向带权树，删掉若干条边，使每个点至多与 `k` 个点相连',
                 '求剩下边权之和的最大值',
                 '示例：`edges=[[0,1,4],[0,2,2],[2,3,12],[2,4,6]], k=2` → `22`'],
        quote='考虑节点 x 和它的儿子 y 的这条边（x-y）选或不选：不选，那么在节点 y 及其儿子的边中，至多选 k 条边；选，那么在节点 y 及其儿子的边中，至多选 k-1 条边。',
        quote_src='—— 灵茶山艾府题解',
        idea=['特殊情形：链 + `k=1` 就是「打家劫舍」，所以一定是 DP',
              '`dfs(y)` 返回 `(nc, c)`：与父亲的边不选 / 选时，`y` 子树的最大和',
              '先假设儿子的边都不选，再按增量 `c + wt − nc` 从大到小，选前 `k`（或 `k−1`）个'],
        summary=['时间 `O(n log n)`（瓶颈是排序），空间 `O(n)`',
                 '易错：增量 `≤ 0` 的边不要放进 `inc`；给父亲的边要留出一个名额（`k-1`）',
                 '优化：所有点度数 `≤ k` 时直接返回边权和',
                 '这里的贪心和 2611. 老鼠和奶酪一模一样'],
    ),
)
