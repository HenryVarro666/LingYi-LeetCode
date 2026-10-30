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

EDGES = [[0, 1], [1, 2], [1, 3]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = 4
    weight = S.get('weight') or [0] * n
    f = S.get('f')
    now = S['_inner'].get('now') if 'dfs' in str(S.get('_fn', 'dfs')) or True else None
    inner = S['_inner']
    in_dp = 'flag' in inner
    fills, rings, notes = {}, {}, {}
    for v in range(n):
        if weight[v] > 0:
            fills[v] = (28, 84, 52)
        if in_dp and f is not None and any(c is not None for c in f[v]):
            a, b = f[v]
            fa_ = '?' if a is None else a
            fb_ = '?' if b is None else b
            notes[v] = (f'{fa_}|{fb_}', T['orange'])
        elif weight[v] > 0:
            notes[v] = (f'×{weight[v]}', T['green'])
    if in_dp:
        c = inner.get('now')
        if c is not None:
            rings[c] = T['yellow']
    else:
        for name, col in (('x', 'blue'), ('y', 'pink')):
            c = S.get(name)
            if c is not None and c in range(n) and 'trips' in S and 'path' in S:
                rings[c] = T[col]
        c = inner.get('now')
        if c is not None and 'path' in S:
            rings[c] = T['yellow']
    _dtree(cv, T, (x0 + 10, y0, x1 - 10, y1), n, EDGES, '树（×次数 = weight；橙 = f[点] = 不减半|减半）',
           fills, rings, notes, side=True)


CONFIG = dict(
    num=2646, title='最小化旅行的价格总和', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='暴力求 lca 计次 + 树形 DP f[i][0/1]',
    tags=['灵神题单·动态规划', '灵神题单·链表树与回溯', '难度分 2238'],
    code='''
class Solution(object):
    def minimumTotalPrice(self, n, edges, price, trips):

        g = {index : set() for index in range(n)}
        fa = {index : None for index in range(n)}

        for x, y in edges:
            g[x].add(y)
            g[y].add(x)
        
        q = [0]
        head, tail = 0, 1
        while head < tail:
            now = q[head]
            head += 1
            for nxt in g[now]:
                if nxt != fa[now]:
                    q.append(nxt)
                    fa[nxt] = now
                    tail += 1

        weight = [0] * n
        for x, y in trips:
            path = set([x])
            now = x
            while fa[now] is not None:
                now = fa[now]
                path.add(now)
            
            now = y
            while now not in path:
                now = fa[now]
            
            while x != now:
                weight[x] += 1
                x = fa[x]
            
            while y != now:
                weight[y] += 1
                y = fa[y]
        
            weight[now] += 1

        f = [[None] * 2 for _ in range(n)]
        def dfs(now, flag):
            if f[now][flag] is None:
                if flag == 0:
                    f[now][flag] = price[now] * weight[now]
                    for nxt in g[now]:
                        if nxt != fa[now]:
                            dfs(nxt, 0)
                            dfs(nxt, 1)
                            f[now][flag] += min(f[nxt][0], f[nxt][1])
                else:
                    f[now][flag] = price[now] // 2 * weight[now]
                    for nxt in g[now]:
                        if nxt != fa[now]:
                            dfs(nxt, 0)
                            f[now][flag] += f[nxt][0]
            
            return f[now][flag]

        
        dfs(0, 0)
        dfs(0, 1)
        return min(f[0][0], f[0][1])
''',
    call='Solution().minimumTotalPrice(4, [[0,1],[1,2],[1,3]], [2,2,10,6], [[0,3],[2,1]])',
    expect=13,
    views=[
        dict(type='array', var='price', label='price', cell=70, h=135),
        dict(type='array', var='weight', label='weight（每个点被经过的次数）', cell=70, h=135),
        dict(type='custom', draw=_draw, h=290),
        dict(type='calls', h=130),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('now', 'now', 'yellow'), ('flag', 'flag', 'purple'),
           ('f[now][flag]', lambda S: S['f'][S['now']][S['flag']] if 'flag' in S['_inner'] else None, 'green')],
    skip=['for x, y in edges', 'g[x].add(y)', 'g[y].add(x)', 'head += 1', 'tail += 1', 'q.append(nxt)', 'for nxt in g[now]',
          'if nxt != fa[now]', 'q = [0]', 'head, tail = 0, 1', 'while head < tail', 'now = q[head]', 'f = [[None]'],
    captions={
        'g = {index': '邻接表 `g`：每个点一个邻居集合',
        'fa = {index': '`fa[i]`：父亲，先全空',
        'fa[nxt] = now': 'bfs 以 0 为根，定下 `fa[{nxt}] = {now}`',
        'weight = [0] * n': '`weight[i]`：点 i 被所有旅行经过几次',
        'path = set([x])': lambda S, B, r: f'旅行 `{S.x} → {S.y}`：先从起点 `{S.x}` 一路向上走到根，把经过的点记进 `path`',
        'now = x': '从起点出发',
        'now = y': '再从终点 `{y}` 往上走，第一个落在 `path` 里的点就是 ==lca==',
        'while fa[now] is not None': lambda S, B, r: ('还没到根，继续向上' if S.fa[S.now] is not None else '到根了，`path` 记录完毕'),
        'path.add': '`path` 加入 `{now}`',
        'while now not in path': lambda S, B, r: (f'`{S.now}` 不在 `path` 里，继续向上' if S.now not in S.path else f'`{S.now}` 在 `path` 里 → 它就是 lca'),
        'now = fa[now]': '`now` 上移到父亲 `{now}`',
        'while x != now': lambda S, B, r: (f'`x = {S.x}` 还没到 lca `{S.now}` → 这一侧要继续加' if S.x != S.now else '起点这一侧走到 lca 了'),
        'while y != now': lambda S, B, r: (f'`y = {S.y}` 还没到 lca `{S.now}` → 这一侧要继续加' if S.y != S.now else '终点这一侧走到 lca 了'),
        'weight[x] += 1': '`weight[x]` 加一 → `{weight}`',
        'weight[y] += 1': '`weight[y]` 加一 → `{weight}`',
        'x = fa[x]': '`x` 上移到父亲 `{x}`',
        'y = fa[y]': '`y` 上移到父亲 `{y}`',
        'weight[now] += 1': 'lca 自己也经过一次 → `weight = {weight}`',
        'f[now][flag] is None': lambda S, B, r: (f'`f[{S.now}][{S.flag}]` 还没算过 → 现在算' if S.f[S.now][S.flag] is None else f'`f[{S.now}][{S.flag}]` 已经算过 = {S.f[S.now][S.flag]}，直接用（记忆化）'),
        'if flag == 0': lambda S, B, r: ('`flag = 0`：==不减半== `now`' if S.flag == 0 else '`flag = 1`：==减半== `now`'),
        'price[now] * weight[now]': '不减半：费用 = `price × weight` = `{price[now]} × {weight[now]}` = `{f[now][flag]}`',
        'price[now] // 2': '减半：费用 = `price // 2 × weight` = `{f[now][flag]}`',
        'dfs(nxt, 0)': '先算儿子 `{nxt}` 不减半：`f[{nxt}][0]`',
        'dfs(nxt, 1)': '再算儿子 `{nxt}` 减半：`f[{nxt}][1]`',
        'min(f[nxt][0], f[nxt][1])': '`now` 不减半 → 儿子两种都行，取小：`min({f[nxt][0]}, {f[nxt][1]})` → `f[{now}][0] = {f[now][0]}`',
        '+= f[nxt][0]': '`now` 减半 → 儿子必须不减半：加 `f[{nxt}][0] = {f[nxt][0]}` → `f[{now}][1] = {f[now][1]}`',
        'return f[now][flag]': '`f[{now}][{flag}] = {ret}`',
        'dfs(0, 0)': '从根算 `f[0][0]`（根不减半）',
        'dfs(0, 1)': '再算 `f[0][1]`（根减半）',
        'return min(f[0][0]': '答案 = `min(f[0][0], f[0][1])` = `{ret}`',
    },
    max_steps=75,
    cards=dict(
        one_liner='暴力求 lca 数出经过次数，再按「不减半 / 减半」做树形 DP',
        complexity='时间 `O(nm + n)`（每次旅行向上爬），空间 `O(n)`',
        problem=['无根树，每个点有价格；一次旅行的价格 = 路径上点的价格之和',
                 '开始前可把一些==互不相邻==的点价格减半，求所有旅行的最小总价',
                 '示例：`price = [2,2,10,6]`，旅行 `0→3`、`2→1` → `13`'],
        quote='每一次旅程都应该从树中的点x出发，走到x和y的最近公共祖先lca，然后再从lca走到y。……得到lca后，将x到lca再到y的这条路径上所有节点的权重加上1。',
        quote_src='—— yiduobo 题解原文',
        idea=['先 bfs 定根 0，记下每个点的父亲 `fa`',
              '起点一路向上，终点向上遇到的第一个公共点就是 lca，路径点 `weight` +1',
              '`f[i][0]` 不减半、`f[i][1]` 减半：不减半时儿子取 `min`，减半时儿子只能不减半'],
        summary=['时间 `O(nm)`：每次旅行最多爬到根；空间 `O(n)`',
                 '`f[i][1]` 的价格是 `price[i] // 2 * weight[i]`；price 是偶数，整除安全',
                 '原文为 Python 2 写法，`price[now] / 2` 已改为 `price[now] // 2`',
                 '对比灵神：灵神在 dfs 里边找终点边累计 `cnt`，yiduobo 先向上爬找 lca'],
    ),
)
