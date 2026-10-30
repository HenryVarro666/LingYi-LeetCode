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


EDGES = [[0, 1], [1, 2]]
COINS = [10, 10, 3]
K = 5
NN = 3
G = [[] for _ in range(NN)]
for _a, _b in EDGES:
    G[_a].append(_b)
    G[_b].append(_a)
FP, ENT, EXT, VAL, _clk = {}, {}, {}, {}, [0]


def _sim(i, j, fa, parent):
    if (i, j) in VAL:
        return VAL[(i, j)]
    FP[(i, j)] = parent
    ENT[(i, j)] = _clk[0]
    _clk[0] += 1
    r1 = (COINS[i] >> j) - K
    r2 = COINS[i] >> (j + 1)
    for c in G[i]:
        if c != fa:
            r1 += _sim(c, j, i, (i, j))
            if j < 13:
                r2 += _sim(c, j + 1, i, (i, j))
    EXT[(i, j)] = _clk[0]
    _clk[0] += 1
    VAL[(i, j)] = max(r1, r2)
    return VAL[(i, j)]


_sim(0, 0, -1, None)
NJ = 3


def _kids(cur):
    return [c for c in FP if FP[c] == cur]


def _state(S, B):
    I = B['_inner'] if S.get('_line') in (14, 16) else S['_inner']
    if 'i' not in I:
        return None, (10 ** 6 if S.get('_line', 0) >= 19 else None), None
    i, j, line = I['i'], I['j'], S['_line']
    cur = (i, j)
    tgt = None
    if line in (10, 11):
        t = ENT[cur]
    elif line == 17:
        t = EXT[cur]
    else:
        ch = I.get('ch')
        exit_ = line == 12 and ch is not None and B['_inner'].get('ch') == ch
        calls = []
        for c in G[i]:
            if c == I['fa']:
                continue
            if c == ch and not exit_:
                if line in (15, 16):
                    calls.append((c, j))
                if line == 14:
                    tgt = (c, j)
                if line == 16:
                    tgt = (c, j + 1)
                break
            calls += [(c, j), (c, j + 1)]
        ks = [c for c in calls if FP.get(c) == cur]
        t = EXT[ks[-1]] if ks else ENT[cur]
    return cur, t, tgt


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cur, tm, tgt = _state(S, B)
    path = set()
    u = cur
    while u is not None:
        path.add(u)
        u = FP[u]
    cv.text((x0 + 18, y0 + 4), 'dfs(i, j) 的结果表（j = 祖先已右移的次数）', 22, T['muted'], bold=True)
    cw = min(120, (x1 - x0 - 290) / NJ)
    ch_ = min(70, (y1 - y0 - 110) / NN)
    sx, sy = x0 + 260, y0 + 90
    for j in range(NJ):
        cv.text((sx + j * cw + cw / 2, sy - 8), f'j={j}', 22, T['dim'], anchor='mb', mono=True)
    for i in range(NN):
        cv.text((sx - 12, sy + i * ch_ + ch_ / 2), f'节点{i}（coins={COINS[i]}）', 21, T['muted'], anchor='rm', bold=True)
        for j in range(NJ):
            c = (i, j)
            X, Y = sx + j * cw, sy + i * ch_
            if c not in FP:
                cv.rect((X + 4, Y + 4, X + cw - 4, Y + ch_ - 4), outline=T['border'], r=8)
                continue
            done = tm is not None and EXT[c] <= tm
            if c == cur:
                fill, col = T['yellow'], T['bg']
            elif c in path:
                fill, col = T['blue'], T['bg']
            elif done:
                fill, col = T['green'], T['bg']
            else:
                fill, col = T['panel2'], T['dim']
            cv.rect((X + 4, Y + 4, X + cw - 4, Y + ch_ - 4), fill=fill, outline=T['border'], r=8)
            cv.text((X + cw / 2, Y + ch_ / 2), str(VAL[c]) if (done or c == cur and tm is not None and EXT[c] <= tm) else '?', 28, col, anchor='mm', bold=True)
            if c == tgt:
                cv.rect((X + 1, Y + 1, X + cw - 1, Y + ch_ - 1), outline=T['pink'], width=5, r=10)
    if tgt is not None:
        hit = FP[tgt] != cur
        cv.text((x0 + 18, sy + NN * ch_ + 14), f'即将调用 dfs({tgt[0]}, {tgt[1]})（粉框）：' + ('已在表里 → ==命中缓存==，直接取值' if hit else '第一次遇到，要往下算').replace('==', ''),
                22, T['pink'], bold=True)


def _opt(S, B):
    I = B['_inner'] if S.get('_line') in (14, 16) else S['_inner']
    if 'i' not in I:
        return '`dfs(i, j)`：子树里每个点的金币已被右移 `j` 次时的最大积分'
    return f"`dfs({I['i']}, {I['j']})`：不右移 `res1 = {I.get('res1', '?')}`，右移 `res2 = {I.get('res2', '?')}`"


def _callcap(S, B, r, jj):
    I = B['_inner']
    c = (I['ch'], I['j'] + jj)
    hit = FP[c] != (I['i'], I['j'])
    return c, hit


def _cap14(S, B, r):
    c, hit = _callcap(S, B, r, 0)
    return (f'不右移：加上 `dfs({c[0]}, {c[1]})`' + ('，这个状态==已经算过==，命中缓存直接用' if hit else '，第一次遇到 → 进入递归'))


def _cap16(S, B, r):
    c, hit = _callcap(S, B, r, 1)
    return (f'右移：加上 `dfs({c[0]}, {c[1]})`（儿子被再右移一次）' + ('，==命中缓存==，直接用' if hit else '，第一次遇到 → 进入递归'))


CONFIG = dict(
    num=2920, title='收集所有金币可获得的最大积分', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='树形 DP · 记忆化搜索（带右移次数）',
    tags=['灵神题单·动态规划', '难度分 2351'],
    code='''
class Solution:
    def maximumPoints(self, edges: List[List[int]], coins: List[int], k: int) -> int:
        g = [[] for _ in coins]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        @cache  # 缓存装饰器，避免重复计算 dfs 的结果（记忆化）
        def dfs(i: int, j: int, fa: int) -> int:
            res1 = (coins[i] >> j) - k
            res2 = coins[i] >> (j + 1)
            for ch in g[i]:
                if ch != fa:
                    res1 += dfs(ch, j, i)  # 不右移
                    if j < 13:  # j+1 >= 14 相当于 res2 += 0，无需递归
                        res2 += dfs(ch, j + 1, i)  # 右移
            return max(res1, res2)

        return dfs(0, 0, -1)
''',
    call='Solution().maximumPoints(EDGES, COINS, K)',
    setup='EDGES = [[0, 1], [1, 2]]\nCOINS = [10, 10, 3]\nK = 5',
    expect=11,
    views=[
        dict(type='text', size=24, h=60, fn=_opt),
        dict(type='custom', h=400, draw=_draw),
        dict(type='calls', h=170),
        dict(type='array', var='coins', label='coins（蓝箭头 = 当前节点 i）', cell=70, h=130, pointers={'i': 'blue'}),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'cyan'), ('res1', 'res1', 'orange'), ('res2', 'res2', 'green')],
    skip=['g = [[] for', 'g[x].append(y)', 'g[y].append(x)', 'for x, y in edges'],
    max_steps=90,
    captions={
        'res1 = (coins[i] >> j) - k': '不右移：当前金币已被右移 `j = {j}` 次 → `{coins[i]} >> {j}` 再减 `k`：`res1 = {res1}`',
        'res2 = coins[i] >> (j + 1)': '右移：`floor(coins/2)` 就是 `>> 1`，右移可叠加 → `coins[{i}] >> {j + 1}` = `res2 = {res2}`',
        'for ch in g[i]': lambda S, B, r: (f'邻居都处理完：`res1 = {S.res1}`，`res2 = {S.res2}`' if 'ch' in B and B.ch == S.ch
                                          else f'看 `i = {S.i}` 的邻居 `ch = {S.ch}`'),
        'if ch != fa': lambda S, B, r: (f'`ch = {S.ch}` 是父节点，跳过' if S.ch == S.fa else f'`ch = {S.ch}` 是儿子，两种选择都要往下算'),
        'res1 += dfs(ch, j, i)': _cap14,
        'if j < 13': lambda S, B, r: (f'`res1 = {S.res1}`；`j = {S.j} < 13` → 还要算右移的分支' if S.j < 13 else '`j + 1 >= 14`：金币全变 0，右移分支不用递归'),
        'res2 += dfs(ch, j + 1, i)': _cap16,
        'return max(res1, res2)': '两种选择取大：`max({res1}, {res2})` = ==`{ret}`==，结果填进 `dfs({i}, {j})`',
        'return dfs(0, 0, -1)': lambda S, B, r: '从根节点、右移 0 次开始：`dfs(0, 0, -1)`' if r is None else f'答案 = `dfs(0, 0)` = =={r}==',
    },
    cards=dict(
        one_liner='记下祖先一共右移了几次：状态 `dfs(i, j)`',
        complexity='时间 `O(n log U)`，空间 `O(n log U)`',
        problem=['每个节点二选一收金币：得 `coins[i] - k`，或得 `floor(coins[i]/2)` 且子树金币全部减半',
                 '祖先先收，求收完所有节点的最大积分',
                 '示例：`edges=[[0,1],[1,2]], coins=[10,10,3], k=5` → `11`'],
        quote='右移运算是可以叠加的，即 (x >> 1) >> 1 等于 x >> 2。我们可以在递归的过程中，额外记录从根节点递归到当前节点的过程中，一共执行了多少次右移。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i, j)`：`i` 子树的金币已被右移 `j` 次，最多得多少分',
              '选或不选：不右移得 `(coins[i] >> j) - k`；右移得 `coins[i] >> (j+1)`，儿子的 `j` 也加 1',
              '`coins ≤ 10^4` 最多右移 14 次就变 0，所以 `j` 到 13 就不再递归'],
        after=[dict(heading='另一种写法：递推', lines=['题解方法二：每个节点返回长为 14 的数组 `f[j]`', '自底向上累加儿子数组，思路与记忆化搜索 1:1 对应'])],
        summary=['时间 `O(n log U)`，`U = max(coins)`，空间 `O(n log U)`',
                 '`@cache` 记忆化：同一个 `(i, j, fa)` 只算一次（表里同一格被多次取用）',
                 '易错：右移分支要把儿子的 `j` 也加 1；`j = 13` 之后 `res2` 的子树贡献为 0',
                 '相似题：337. 打家劫舍 III'],
    ),
)
