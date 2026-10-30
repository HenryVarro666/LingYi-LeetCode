def _tree_pos(n, edges, root=0):
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)
    xs, ds, ch, cnt = {}, {}, {}, [0]

    def go(x, fa, d):
        ds[x] = d
        ch[x] = [y for y in g[x] if y != fa]
        for y in ch[x]:
            go(y, x, d + 1)
        if ch[x]:
            xs[x] = (xs[ch[x][0]] + xs[ch[x][-1]]) / 2
        else:
            xs[x] = cnt[0]
            cnt[0] += 1
    go(root, -1, 0)
    return xs, ds, ch, max(cnt[0], 1)


def _draw_tree(cv, box, T, n, edges, node_fn, title='', edge_fn=None, edge_label=None, bot_right=False, txt_size=28):
    """node_fn(i) -> dict(fill=颜色名或None, txt=节点里的字, top=上方小字, bot=下方小字, ring=颜色名或None)"""
    x0, y0, x1, y1 = box
    xs, ds, ch, nl = _tree_pos(n, edges)
    md = max(ds.values())
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    gx0, gx1 = x0 + 70, x1 - 70
    gy0, gy1 = y0 + 84, y1 - 52
    step = (gx1 - gx0) / max(nl - 1, 1) if nl > 1 else 0
    step = min(step, 150)
    ox = (x0 + x1) / 2 - step * (nl - 1) / 2
    ly = (gy1 - gy0) / max(md, 1)
    ly = min(ly, 140)
    P = {i: (ox + xs[i] * step, gy0 + ds[i] * ly) for i in range(n)}
    for p in range(n):
        for c in ch[p]:
            col = edge_fn(p, c) if edge_fn else None
            cv.line([P[p], P[c]], T[col] if col else T['border'], 6 if col else 3)
            lab = edge_label(p, c) if edge_label else None
            if lab is not None:
                mx, my = (P[p][0] + P[c][0]) / 2, (P[p][1] + P[c][1]) / 2
                right = P[c][0] >= P[p][0]
                cv.text((mx + (10 if right else -10), my), lab, 22, T[col] if col else T['cyan'], anchor='lm' if right else 'rm', bold=True, mono=True)
    R = 27
    for i in range(n):
        X, Y = P[i]
        d = node_fn(i)
        f = d.get('fill')
        ring = d.get('ring')
        if ring:
            cv.d.ellipse((X - R - 6, Y - R - 6, X + R + 6, Y + R + 6), outline=T[ring], width=4)
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=T[f] if f else T['panel2'],
                     outline=T[f] if f else T['muted'], width=2)
        cv.text((X, Y), d.get('txt', i), txt_size, T['dim'] if d.get('dim') else (T['bg'] if f else T['text']), anchor='mm', bold=True)
        if not edge_label:
            cv.text((X - R - 10, Y - R - 4), i, 18, T['dim'], anchor='rb', mono=True)
        if d.get('top'):
            cv.text((X, Y - R - 10), d['top'], 20, T['cyan'], anchor='mb', bold=True)
        if d.get('bot'):
            if bot_right:
                cv.text((X + R + 12, Y), d['bot'], 22, T[d.get('botc', 'green')], anchor='lm', bold=True)
            else:
                cv.text((X, Y + R + 8), d['bot'], 22, T[d.get('botc', 'green')], anchor='mt', bold=True)


N = 5
EDGES = [[0, 2], [1, 2], [1, 3], [2, 4]]
VAL = [1, 8, 1, 4, 4]
K = 6
_xs, _ds, _ch, _nl = _tree_pos(N, EDGES)
_PAR = {c: p for p in _ch for c in _ch[p]}
_PRE = []


def _walk(x):
    _PRE.append(x)
    for c in _ch[x]:
        _walk(c)


_walk(0)
_F = {}


def _calc(x):
    _F[x] = VAL[x] + sum(_calc(c) for c in _ch[x])
    return _F[x]


_calc(0)


def _anc(x):
    r = set()
    while x != -1:
        r.add(x)
        x = _PAR.get(x, -1)
    return r


def _top(i, x):
    """i 在 x 的哪个儿子子树里（不在则 None）"""
    while i != -1 and _PAR.get(i, -1) != x:
        i = _PAR.get(i, -1)
    return i if i != -1 else None


def _draw(cv, S, B, box, T):
    x = S.get('x')
    live = x is not None and x >= 0 and 'ans' in S
    path = _anc(x) if live else set()
    pre = _PRE.index(x) if live else -1
    y = S.get('y')
    line = S.get('_line') or 0

    def done(i):
        if i in path:
            return False
        if _PRE.index(i) < pre:
            return True
        c = _top(i, x)
        if c is None or y is None or y not in _ch[x]:
            return False
        a, b = _ch[x].index(c), _ch[x].index(y)
        return a < b or (a == b and (line >= 15 or (line == 11 and B.get('y') == y)))

    fin = set(i for i in range(N) if live and (done(i) or (i == x and line >= 16)))

    def f(i):
        d = dict(txt=VAL[i])
        if i in fin:
            cut = _F[i] % K == 0
            d['fill'] = 'green' if cut else None
            d['bot'] = f'和 {_F[i]}' + (' 可删' if cut else '')
            d['botc'] = 'green' if cut else 'orange'
        if live and i == x:
            d['ring'] = 'yellow'
            if i not in fin:
                d['fill'] = 'yellow'
        elif live and i in path:
            d['ring'] = 'blue'
        return d

    def e(p, c):
        return 'red' if c in fin and _F[c] % K == 0 else None
    _draw_tree(cv, box, T, N, EDGES, f, edge_fn=e, title=f'树（点权，k={K}；黄环 = 当前，蓝环 = 路径，绿 = 和可被 k 整除，红线 = 删边）')


def _sum(S, B):
    x = S.get('x')
    if x is None or x < 0 or 's' not in S:
        return ''
    r = S['s'] % K
    if (S.get('_line') or 0) < 15:
        return f'节点 `{x}`：子树和累计中，当前 `s = {S["s"]}`'
    return f'节点 `{x}` 的子树和 `s = {S["s"]}`，`s % k = {S["s"]} % {K} = {r}`' + (' → ==可删==' if r == 0 else ' → 不能删')


CONFIG = dict(
    num=2872, title='可以被 K 整除连通块的最大数目', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='自底向上 DFS · 子树和',
    tags=['灵神题单', '链表树与回溯', '难度分 1968'],
    code='''
class Solution:
    def maxKDivisibleComponents(self, n: int, edges: List[List[int]], values: List[int], k: int) -> int:
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        # 返回子树 x 的点权和
        def dfs(x: int, fa: int) -> int:
            s = values[x]
            for y in g[x]:
                if y != fa:  # 避免访问父节点
                    # 加上子树 y 的点权和，得到子树 x 的点权和
                    s += dfs(y, x)  
            nonlocal ans
            ans += s % k == 0
            return s

        ans = 0
        dfs(0, -1)
        return ans
''',
    call='Solution().maxKDivisibleComponents(5, [[0,2],[1,2],[1,3],[2,4]], [1,8,1,4,4], 6)',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=440),
        dict(type='text', fn=_sum, size=26, h=70),
        dict(type='calls', h=130, hide=('n', 'edges', 'values')),
    ],
    watch=[('x', 'x', 'yellow'), ('s', 's', 'cyan'), ('k', 'k', 'purple'), ('ans', 'ans', 'green')],
    skip=['g[x].append', 'g[y].append', 'for x, y in edges', 'nonlocal'],
    max_steps=90,
    captions={
        'g = [[]': '建邻接表 `g`：每条边双向加入',
        'ans = 0': '`ans` 统计「可以删除的边」的个数；根到它「不存在的父节点」那条边也算上，所以连通块数 = `ans`',
        'dfs(0, -1)': '任选一个点（这里是 `0`）当根，DFS 求每棵子树的点权和',
        's = values[x]': '进入节点 `{x}`：子树和先从自己的点权 `values[{x}] = {values[x]}` 开始',
        'for y in g[x]': lambda S, B, r: (f'取第一个邻居 `y = {S.y}`' if 'y' not in B['_inner'] else
                                          ((f'儿子的和已加入：`s = {S.s}`；' if B['_inner'].get('y') != B['_inner'].get('fa') else '')
                                           + (f'再看下一个邻居 `y = {S.y}`' if S.y != B.y else f'邻居都看完了，子树 {S.x} 的点权和就是 `s = {S.s}`'))),
        'if y != fa': lambda S, B, r: (f'`{S.y}` 是父节点 → 不回头' if S.y == S.fa else f'`{S.y}` 是儿子 → 递归求子树 {S.y} 的点权和'),
        's += dfs': '递归进入儿子 `{y}`：返回它的子树点权和，累加到 `s`',
        'ans += s % k': lambda S, B, r: (f'子树 {S.x} 的和 `s = {S.s}`，`{S.s} % {S.k} == 0` → 它是 k 的倍数：==这条边可以删==，`ans` = {S.ans}' if S.s % S.k == 0
                                        else f'子树 {S.x} 的和 `s = {S.s}`，`{S.s} % {S.k} = {S.s % S.k}` ≠ 0 → 不能删，`ans` 不变 = {S.ans}'),
        'return s': '把子树和 `{s}` 返回给父节点，让它继续累加',
        'return ans': '一共 `{ans}` 个连通块：删掉 {ans - 1} 条边，再加上根所在的最后一块',
    },
    cards=dict(
        one_liner='子树点权和是 k 的倍数，这条边就能删',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树，每个节点有点权 `values[i]`，点权总和是 `k` 的倍数',
                 '可以删若干条边，得到的每个连通块点权和都要被 `k` 整除',
                 '求连通块个数的最大值',
                 '示例：`values=[1,8,1,4,4]`，`k=6` → `2`'],
        quote='如果 x+y 不是 k 的倍数，那么 x 和 y 不全是 k 的倍数……所以当且仅当这两个连通块的点权和都是 k 的倍数，这条边才能删除。……换句话说，只要有能删除的边，就删除。',
        quote_src='—— 灵茶山艾府题解',
        idea=['整棵树的和是 `k` 的倍数，所以删一条边后只需看==一侧==的和',
              '从根 DFS：子树 `x` 的点权和 `s` 是 `k` 的倍数 → 删掉 `x` 到父亲的边',
              '连通块数 = 删边数 + 1；把根的「虚拟父边」也算一次，答案恰好是 `ans`'],
        summary=['时间 `O(n)`，空间 `O(n)`（递归栈）',
                 '贪心成立的理由：能删就删，再分割不会破坏整除性',
                 '`ans += s % k == 0` 是布尔加法，根节点的和必然是 `k` 的倍数，所以会多算一条「虚拟边」',
                 '相似题：2440 创建价值相同的连通块']),
)
