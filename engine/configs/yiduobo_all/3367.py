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
_FH = {}


def _calc(u):
    import heapq as _hq
    hp, s, f, h = [], 0, 0, 0
    for c in TC['ch'][u]:
        _calc(c)
        w = ELAB[(u, c)]
        if _FH[c][0] + w > _FH[c][1]:
            diff = _FH[c][0] + w - _FH[c][1]
            _hq.heappush(hp, diff)
            s += diff
            if len(hp) > K:
                s -= _hq.heappop(hp)
        f += _FH[c][1]
        h += _FH[c][1]
    f += s
    h += s
    if len(hp) == K:
        f -= hp[0]
    _FH[u] = (f, h)


_calc(0)


def _state(S, B=None):
    line = S.get('_line', 0)
    I = B['_inner'] if line == 20 and B is not None else S['_inner']
    x = I.get('now')
    if x is None:
        return None, (10 ** 6 if line >= 38 else None)
    y, g = I.get('child'), S['g']
    kids = TC['ch'][x]
    if line in (14, 15, 36):
        t = TC['ent'][x]
    elif 31 <= line <= 34:
        t = TC['ext'][kids[-1]] if kids else TC['ent'][x]
    else:
        incl = (line == 16 and B is not None and y is not None and B['_inner'].get('child') == y) or 22 <= line <= 29
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
    if S['_line'] >= 16 and 's' in I:
        return f"s={I['s']}"
    return ''


def _fml(S):
    I = S['_inner']
    if 'now' not in I or 'heap' not in I:
        return f'`f`：给父亲留一条边（最多选 k-1 条孩子边）；`h`：最多选 k = {K} 条孩子边'
    return f"堆里是收益最大的几条边 `heap = {sorted(I['heap'])}`，额外收益 `s = {I['s']}`"


CONFIG = dict(
    num=3367, title='移除边之后的权重最大和', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='树形 DP · 大小为 k 的小根堆',
    tags=['灵神题单·动态规划', '难度分 2602'],
    code='''
class Solution(object):
    def maximizeSumOfWeights(self, edges, k):
        
        n = len(edges) + 1
        g = {x : [] for x in range(n)}
        for x, y, w in edges:
            g[x].append((y, w))
            g[y].append((x, w))

        f = [0] * n
        h = [0] * n

        def dfs(now, fa):
            heap = []
            s = 0
            for child, weight in g[now]:
                if child == fa:
                    continue

                dfs(child, now)

                if f[child] + weight > h[child]:
                    diff = f[child] + weight - h[child]
                    heapq.heappush(heap, diff)
                    s += diff
                    if len(heap) > k:
                        s -= heapq.heappop(heap)
                f[now] += h[child]
                h[now] += h[child]

            f[now] += s
            h[now] += s
            if len(heap) == k:
                f[now] -= heap[0]
        
        dfs(0, -1)

        return h[0]
''',
    call='Solution().maximizeSumOfWeights(EDGES, K)',
    setup='EDGES = [[0, 1, 4], [0, 2, 2], [2, 3, 12], [2, 4, 6]]\nK = 2',
    expect=22,
    views=[
        dict(type='text', size=24, h=55, fn=_fml),
        dict(type='custom', h=340, draw=_tree_draw(TC, _state, lambda u: str(u), note=lambda u: f'f={_FH[u][0]} h={_FH[u][1]}', live=_live, elab=ELAB,
                                                   title='树：橙色 = 边权，旁注 = 算完的 f、h')),
        dict(type='array', var='heap', label='heap（小根堆，最多 k 个 diff）', cell=64, h=110),
        dict(type='array', var='f', label='f（选父边：孩子边至多 k-1 条）', cell=64, h=110, pointers={'now': 'blue'}),
        dict(type='array', var='h', label='h（不选父边：孩子边至多 k 条）', cell=64, h=110, pointers={'now': 'blue'}),
    ],
    watch=[('now', 'now', 'blue'), ('child', 'child', 'cyan'), ('s', 's', 'orange'), ('diff', 'diff', 'pink')],
    skip=['n = len(edges)', 'g = {x', 'for x, y, w in edges', 'g[x].append', 'g[y].append', 'continue', 'if child == fa'],
    max_steps=100,
    captions={
        'f = [0] * n': '`f[now]`：`now` 与父亲的边==要选==时，子树边权和的最大值（`now` 只能再选 k-1 条孩子边）',
        'h = [0] * n': '`h[now]`：与父亲的边==不选==时，子树边权和的最大值（`now` 可选 k 条孩子边）',
        'heap = []': '小根堆：只留收益最大的 k 条孩子边的 `diff`',
        's = 0': '`s`：堆里这些 `diff` 之和（额外收益）',
        'for child, weight in g[now]': lambda S, B, r: (f'孩子都处理完：`s = {S.s}`，堆 `{sorted(S.heap)}`' if 'child' in B and B.child == S.child
                                                        else (f'`child = {S.child}` 是父节点，跳过' if S.child == S.fa
                                                              else f'看 `now = {S.now}` 的孩子 `child = {S.child}`，边权 `{S.weight}`')),
        'dfs(child, now)': '先递归算孩子 `{child}`，得到它的 `f`、`h`',
        'if f[child] + weight > h[child]': lambda S, B, r: (f'保留这条边：`f[{S.child}] + weight = {S.f[S.child]} + {S.weight} = {S.f[S.child] + S.weight}` > `h[{S.child}] = {S.h[S.child]}` → ==值得保留=='
                                                            if S.f[S.child] + S.weight > S.h[S.child]
                                                            else f'`f[{S.child}] + weight = {S.f[S.child] + S.weight}` ≤ `h[{S.child}] = {S.h[S.child]}` → 保留了反而亏，且还占名额，不保留'),
        'diff = ': '保留的收益 `diff = f + weight − h` = =={diff}==',
        'heapq.heappush': '`diff` 入堆：`{sorted(heap)}`',
        's += diff': '先当作选了：`s = {s}`',
        'if len(heap) > k': lambda S, B, r: (f'堆里 {len(S.heap)} 个 > k = {S.k} → 名额不够，要去掉收益最小的' if len(S.heap) > S.k
                                             else f'堆里 {len(S.heap)} 个 ≤ k = {S.k}，名额够'),
        's -= heapq.heappop': '弹出堆顶最小的 `diff`，撤销它：`s = {s}`',
        'f[now] += h[child]': '不论保留与否，先加上孩子不选父边的 `h[{child}] = {h[child]}`：`f[{now}] = {f[now]}`',
        'h[now] += h[child]': '`h[{now}]` 同样先加上 `h[{child}]`：`{h[now]}`',
        'f[now] += s': '补上额外收益 `s = {s}`：保留的边用 `f[孩子] + weight` 取代 `h[孩子]` → `f[{now}] = {f[now]}`',
        'h[now] += s': '`h[{now}]` 也补上 `s`：`{h[now]}`',
        'if len(heap) == k': lambda S, B, r: (f'堆满了 `{len(S.heap)} = k`：`f` 只能选 k-1 条孩子边，要去掉一条' if len(S.heap) == S.k
                                              else f'堆里 {len(S.heap)} 个 < k，`f` 还有名额，不用减'),
        'f[now] -= heap[0]': '去掉最小的 `diff = {heap[0]}`：`f[{now}] = {f[now]}`',
        'dfs(0, -1)': '从根 0 开始 `dfs`，结果都存在 `f`、`h` 里',
        'return h[0]': '根没有父边，答案就是 `h[0]` = =={ret}==',
    },
    cards=dict(
        one_liner='每个点留收益最大的 k 条边：用大小为 k 的小根堆挑',
        complexity='时间 `O(n log k)`，空间 `O(n)`',
        problem=['无向带权树，删掉若干条边，使每个点至多与 `k` 个点相连',
                 '求剩下边权之和的最大值',
                 '示例：`edges=[[0,1,4],[0,2,2],[2,3,12],[2,4,6]], k=2` → `22`'],
        quote='若f[child] + weight > h[child]，就可以尝试保留weight这条边……记保留的收益diff = f[child] + weight - h[child]，那么在这里就应该选取其中diff最大的k条边。这是一个经典的top k问题，那么在这里就可以使用一个大小为k的堆。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[now]`：与父亲的边选上，`now` 孩子边至多 k-1 条；`h[now]`：不选，至多 k 条',
              '先让所有孩子取 `h[child]`，再看保留某条边能多赚 `diff`',
              '堆只留最大的 k 个 `diff`；`h` 加上全部，`f` 少算最小的一个'],
        summary=['时间 `O(n log k)`，空间 `O(n)`',
                 '易错：`f` 要比 `h` 少用一条名额，所以堆满 k 个时 `f` 要减去堆顶',
                 '`diff ≤ 0` 的边保留反而更差，直接不考虑',
                 '对比灵神：灵神把 `diff` 全放进列表排序取前 k / k-1 个；yiduobo 用小根堆维护 top k',
                 '原文为 Python 2 风格，在 Python 3 下无需修改即可运行'],
    ),
)
