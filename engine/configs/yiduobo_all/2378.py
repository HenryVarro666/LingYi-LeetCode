def _tlay(n, edges, root=0):
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)
    depth, par, order = {root: 0}, {root: -1}, [root]
    for x in order:
        for y in g[x]:
            if y not in depth:
                depth[y], par[y] = depth[x] + 1, x
                order.append(y)
    kids = [[y for y in g[x] if par.get(y) == x] for x in range(n)]
    xs, cnt = {}, [0]

    def go(x):
        if not kids[x]:
            xs[x] = cnt[0]
            cnt[0] += 1
        else:
            for y in kids[x]:
                go(y)
            xs[x] = (xs[kids[x][0]] + xs[kids[x][-1]]) / 2
    go(root)
    return xs, depth, par, cnt[0], max(depth.values()) + 1


def _dtree(cv, T, box, n, edges, title, fills=None, rings=None, notes=None, hot=None, root=0, maxR=28, labels=None, side=False):
    """画一棵一般树。fills: 点->颜色；rings: 点->描边色；notes: 点->(文字,颜色)（点下方）；hot: {(a,b):颜色}；labels: 点->显示文字"""
    x0, y0, x1, y1 = box
    fills, rings, notes, hot, labels = fills or {}, rings or {}, notes or {}, hot or {}, labels or {}
    cv.text((x0 + 8, y0), title, 22, T['muted'], bold=True)
    xs, depth, par, leaves, levels = _tlay(n, edges, root)
    w = x1 - x0 - 50
    top = y0 + 44
    R = max(16, min(maxR, w / leaves / 2.3))
    dy = min(110, (y1 - top - 2 * R - 34) / max(1, levels - 1)) if levels > 1 else 0
    pos = {v: (x0 + 25 + (xs[v] + 0.5) * w / leaves, top + depth[v] * dy + R) for v in range(n)}
    for a, b in edges:
        (ax, ay), (bx, by) = pos[a], pos[b]
        c = hot.get((a, b)) or hot.get((b, a))
        cv.line([(ax, ay), (bx, by)], c or T['border'], 6 if c else 3)
    for v in range(n):
        X, Y = pos[v]
        ring = rings.get(v)
        cv.rect((X - R, Y - R, X + R, Y + R), fill=fills.get(v, T['panel2']), outline=ring or T['border'],
                width=5 if ring else 2, r=R)
        cv.text((X, Y), labels.get(v, v), int(R * 0.95), T['text'], anchor='mm', bold=True)
        if v in notes:
            t, c = notes[v]
            if side:
                cv.text((X + R + 8, Y), t, 20, c, anchor='lm', bold=True, mono=True)
            else:
                cv.text((X, Y + R + 6), t, 20, c, anchor='mt', bold=True, mono=True)
    return pos

EDGE_LIST = [[-1, -1], [0, 5], [0, 10], [2, 6], [2, 4]]
TREE = [[i, p] for i, (p, w) in enumerate(EDGE_LIST) if p != -1]
N = 5


def _draw(cv, S, B, box, T):
    inner = S['_inner']
    cur = inner.get('now')
    f = S.get('f')
    fills, rings, notes, hot = {}, {}, {}, {}
    if f:
        for v in range(N):
            a, b = f[v]
            if a is not None or b is not None:
                notes[v] = (f"{'?' if a is None else a}|{'?' if b is None else b}", T['orange'])
                fills[v] = (28, 84, 52) if (a is not None and b is not None) else T['panel2']
    if cur is not None:
        rings[cur] = T['yellow']
        ch = inner.get('child')
        if ch is not None and S['_line'] >= 21:
            rings[ch] = T['pink']
            hot[(cur, ch)] = T['pink']
    pos = _dtree(cv, T, box, N, TREE, '树（边上数字 = 边权；橙字 = f[点][不选父边]|f[点][选了父边]）', fills, rings, notes, hot=hot, side=True)
    for i, (p, w) in enumerate(EDGE_LIST):
        if p == -1:
            continue
        (ax, ay), (bx, by) = pos[p], pos[i]
        cv.text(((ax + bx) / 2 - 14, (ay + by) / 2 - 4), str(w), 24, T['cyan'], anchor='rm', bold=True, mono=True)


def _cap_if(S, B, r):
    v = S.f[S.now][S.flag]
    if v is None:
        return f"`f[{S.now}][{S.flag}]` 还没算过 → 现在算"
    return f"`f[{S.now}][{S.flag}]` 已经是 `{v}`，直接返回（记忆化）"


CONFIG = dict(
    num=2378, title='选择边来最大化树的得分', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='树形 DP · f[点][父边是否被选]',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def maxScore(self, edges):

        n = len(edges)

        g = [[] for _ in range(n)]

        for index, (p, w) in enumerate(edges):
            if p != -1:
                g[p].append([index, w])
        
        f = [[None] * 2 for _ in range(n)]

        def dfs(now, flag):
            if f[now][flag] is None:
                f[now][flag] = 0
                max_delta = 0
                for child, w in g[now]:
                    v = max(0, dfs(child, False))
                    f[now][flag] += v
                    if not flag:
                        delta = max(0, dfs(child, True)) + w - v
                        max_delta = max(max_delta, delta)
                
                if not flag:
                    f[now][flag] += max_delta
            
            return f[now][flag]
                

        return dfs(0, False)
''',
    call='Solution().maxScore([[-1,-1],[0,5],[0,10],[2,6],[2,4]])',
    expect=11,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='calls', h=200),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'yellow'), ('flag', lambda S: S['_inner'].get('flag'), 'purple'),
           ('child', lambda S: S['_inner'].get('child'), 'pink'), ('w', lambda S: S['_inner'].get('w'), 'cyan'),
           ('v', lambda S: S['_inner'].get('v')), ('max_delta', lambda S: S['_inner'].get('max_delta'), 'orange'),
           ('f[now][flag]', lambda S: S['f'][S['_inner']['now']][S['_inner']['flag']] if 'flag' in S['_inner'] else None, 'green')],
    skip=['n = len(edges)', 'g = [[]', 'for index, (p, w)', 'if p != -1', 'g[p].append', 'f = [[None]'],
    captions={
        'if f[now][flag] is None': _cap_if,
        'f[now][flag] = 0': '`flag = {flag}`：{"`now` 与父亲的边已被选，儿子的边都不能选" if flag else "`now` 与父亲的边没选，儿子的边还可以选一条"}；得分先记 0',
        'max_delta = 0': '`max_delta`：改选一条儿子边最多能多得多少，先记 0',
        'for child, w in g[now]': lambda S, B, r: (f'看 `{S.now}` 的儿子 `{S.child}`（边权 `{S.w}`）' if ('child' not in B or (S.child, S.w) != (B.child, B.w)) else f'`{S.now}` 的儿子都看完了'),
        'v = max(0, dfs(child, False))': '先算儿子 `{B.child}` 的子树：这条边 `{B.now}–{B.child}` 不选',
        'f[now][flag] += v': '儿子子树最多 `v = {v}` 分；先默认儿子边都不选 → `{f[now][flag]}`',
        'if not flag': lambda S, B, r: ('`flag = False`：父边没选，`now` 可以挑一条儿子边' if not S.flag else '`flag = True`：父边已选，儿子边都不能选'),
        'delta = max(0, dfs(child, True))': '假设改选 `{B.now}–{B.child}`：儿子要按「父边已选」重算 `f[{B.child}][True]`',
        'max_delta = max(max_delta, delta)': '改选这条边的增量 `delta = {delta}`（`f[child][True] + w − v`）→ `max_delta = {max_delta}`',
        'f[now][flag] += max_delta': '加上最大增量：`f[{now}][False] = {f[now][flag]}`',
        'return f[now][flag]': '`f[{now}][{flag}] = {ret}`',
        'return dfs(0, False)': lambda S, B, r: ('根没有父边：从 `dfs(0, False)` 开始' if r is None else f'答案 `{r}`'),
    },
    max_steps=58,
    cards=dict(
        one_liner='f[点][父边选没选]：选了父边，儿子边就全不能选',
        complexity='时间 `O(n)`（每个状态算一次），空间 `O(n)`',
        problem=['加权树，`edges[i] = [父亲, 边权]`，根的 `edges[0] = [-1, -1]`',
                 '选一些边，使得任意两条被选的边==不相邻==（不共用端点）',
                 '求被选边的权值和最大值（可以一条都不选）',
                 '示例：`[[-1,-1],[0,5],[0,10],[2,6],[2,4]]` → `11`（选 0–1 和 2–3）'],
        quote='令f[node][flag]表示对于以node为根节点的子树，若其根节点node与node的根节点的边被选择的情况为flag时，子树中最大的得分是多少。',
        quote_src='—— yiduobo 题解原文',
        idea=['`flag = True`：`now` 与父亲的边已选 → 儿子边都不能选，儿子取 `f[child][False]` 之和',
              '`flag = False`：可以不选任何儿子边（同上），也可以==改选恰好一条==儿子边',
              '改选 `now–child`：该儿子换成 `f[child][True] + w`，比原来多出 `delta`，取最大的一个'],
        summary=['时间 `O(n)`，空间 `O(n)`；`f` 数组做记忆化，每个状态只算一次',
                 '最多改选一条儿子边：因为选两条会在 `now` 处相邻',
                 '`max(0, …)`：子树得分不会为负（可以什么都不选）；边权可能为负，所以 `delta` 里也要和 0 比',
                 '原文在 Python 3 下无需修改，代码照搬']
    ),
)
