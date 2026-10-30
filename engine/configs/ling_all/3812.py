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


N = 7
EDGES = [[0, 1], [1, 2], [2, 3], [3, 4], [3, 5], [1, 6]]
START = '0011000'
TARGET = '0010001'
_xs, _ds, _ch, _nl = _tree_pos(N, EDGES)
_PAR = {c: p for p in _ch for c in _ch[p]}
_EIDX = {}
for _i, (_a, _b) in enumerate(EDGES):
    _EIDX[(_a, _b)] = _i
    _EIDX[(_b, _a)] = _i
_PRE = []


def _walk(x):
    _PRE.append(x)
    for c in _ch[x]:
        _walk(c)


_walk(0)
_R = {}


def _calc(x):
    r = START[x] != TARGET[x]
    for c in _ch[x]:
        if _calc(c):
            r = not r
    _R[x] = r
    return r


_calc(0)


def _anc(x):
    r = set()
    while x != -1:
        r.add(x)
        x = _PAR.get(x, -1)
    return r


def _top(i, x):
    while i != -1 and _PAR.get(i, -1) != x:
        i = _PAR.get(i, -1)
    return i if i != -1 else None


def _state(S, B):
    x = S.get('x')
    if x is None or x < 0 or 'revs' not in S:
        return False, None, set(), set(), 0
    path = _anc(x)
    pre = _PRE.index(x)
    y = S.get('y')
    line = S.get('_line') or 0
    dn = set()
    for i in range(N):
        if i in path:
            continue
        if _PRE.index(i) < pre:
            dn.add(i)
            continue
        c = _top(i, x)
        if c is None or y is None or y not in _ch[x]:
            continue
        p, q = _ch[x].index(c), _ch[x].index(y)
        if p < q or (p == q and (line >= 14 or (line == 12 and B.get('y') == y))):
            dn.add(i)
    return True, x, path, dn, line


def _draw(cv, S, B, box, T):
    live, x, path, dn, line = _state(S, B)

    def f(i):
        d = dict(txt=f'{START[i]}→{TARGET[i]}')
        if START[i] != TARGET[i]:
            d['fill'] = 'pink'
        if live and i == x:
            d['ring'] = 'yellow'
            if line >= 11 and 'rev' in S['_inner']:
                d['bot'] = f'rev={"是" if S["rev"] else "否"}'
                d['botc'] = 'orange' if S['rev'] else 'muted'
        elif live and i in path:
            d['ring'] = 'blue'
        elif live and i in dn:
            d['bot'] = '翻 ↑' if _R[i] else '不翻'
            d['botc'] = 'orange' if _R[i] else 'muted'
        return d

    def e(p, c):
        return 'orange' if live and c in dn and _R[c] else None

    _draw_tree(cv, box, T, N, EDGES, f, edge_fn=e, edge_label=lambda p, c: str(_EIDX[(p, c)]), bot_right=True, txt_size=22,
               title='树（节点 = 初始色→目标色，粉 = 不一致；青字 = 边下标，橙线 = 要翻转）')


def _sum(S, B):
    live, x, path, dn, line = _state(S, B)
    if not live or 'rev' not in S['_inner']:
        return ''
    return (f'节点 `{x}`：`start[{x}] = {START[x]}`，`target[{x}] = {TARGET[x]}` → 先假设 ==rev = {"True" if START[x] != TARGET[x] else "False"}==；'
            f'现在 `rev = {S["rev"]}`（被翻几次就取反几次）')


CONFIG = dict(
    num=3812, title='翻转树上最少边', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='自底向上 DFS · 先定叶子的边',
    tags=['灵神题单', '链表树与回溯', '难度分 2179'],
    code='''
class Solution:
    def minimumFlips(self, n: int, edges: List[List[int]], start: str, target: str) -> List[int]:
        g = [[] for _ in range(n)]
        for i, (x, y) in enumerate(edges):
            g[x].append((y, i))
            g[y].append((x, i))

        revs = [False] * (n - 1)
        # 返回是否需要翻转 x-fa 这条边
        def dfs(x: int, fa: int) -> bool:
            rev = start[x] != target[x]  # x-fa 是否要翻转
            for y, i in g[x]:
                if y != fa and dfs(y, x):
                    revs[i] = True  # 需要翻转 y-x
                    rev = not rev  # x 被翻转了
            return rev

        if dfs(0, -1):  # 只剩下一个根节点需要翻转，无法操作
            return [-1]

        return [i for i, rev in enumerate(revs) if rev]
''',
    call="Solution().minimumFlips(7, [[0,1],[1,2],[2,3],[3,4],[3,5],[1,6]], '0011000', '0010001')",
    expect=[1, 2, 5],
    views=[
        dict(type='custom', draw=_draw, h=540),
        dict(type='array', var='revs', label='revs[i]：边 i 是否要翻转', cell=60, h=100, pointers={}, color=lambda S, i, v: 'orange' if v else None),
        dict(type='calls', h=110, hide=('n', 'edges', 'start', 'target', 'revs')),
    ],
    watch=[('x', 'x', 'yellow'), ('fa', 'fa', 'blue'), ('rev', 'rev', 'orange')],
    skip=['g[x].append', 'g[y].append', 'for i, (x, y) in enumerate'],
    max_steps=100,
    captions={
        'g = [[]': '建邻接表：`g[x]` 里存 `(邻居, 边下标)`，两条 append 把边双向加入',
        'revs = [False]': '`revs[i]` 标记第 `i` 条边要不要翻转，共 `n-1` 条边',
        'rev = start[x]': lambda S, B, r: (f'进入节点 `{S.x}`：`start = {S.start[S.x]}`，`target = {S.target[S.x]}` → `rev = {S.rev}`'
                                           + ('，颜色不对，==需要被翻转一次==' if S.rev else '，颜色已对，暂时不用翻')),
        'for y, i in g[x]': lambda S, B, r: (f'看第一条边：邻居 `y = {S.y}`，边下标 `i = {S.i}`' if 'y' not in B['_inner'] else
                                             (f'下一条边：邻居 `y = {S.y}`，边下标 `i = {S.i}`' if S.y != B.y or S.i != B.i
                                              else f'邻居都看完了，节点 {S.x} 最终 `rev = {S.rev}`')),
        'if y != fa and dfs': lambda S, B, r: (f'`{S.y}` 是父节点 → 这条边由上层决定，不回头' if S.y == S.fa else f'`{S.y}` 是儿子 → 先递归处理子树，问它「{B.y}-{B.x} 这条边要不要翻」'),
        'revs[i] = True': '儿子 `{y}` 说要翻：==必须翻 {y}-{x} 这条边（下标 {i}）==，否则儿子子树颜色永远不对',
        'rev = not rev': '翻这条边会同时翻转 `x = {x}`：`rev` 取反 → =={rev}==',
        'return rev': lambda S, B, r: ((f'返回 `rev = {S.rev}`：节点 {S.x} 现在' + ('仍与目标不同 → 上层要翻 ' + f'{S.x}-{S.fa}' + ' 这条边' if S.rev else '已与目标相同 → 上层不能翻这条边'))
                                       if S.fa != -1 else (f'根 `0` 返回 `{S.rev}`：' + ('根颜色仍不对，却没有边可翻 → 无解' if S.rev else '根颜色也对了 → 有解'))),
        'if dfs(0, -1)': '从根 `0` 出发自底向上：返回 True 表示「根也颜色不对」，那就无解',
        'return [-1]': '无解：`[-1]`',
        'return [i for': '从左到右收集 `revs` 为真的下标 → `{ret}`（自然升序，不用排序）',
    },
    cards=dict(
        one_liner='叶子的边必翻或必不翻，剥掉叶子再往上推',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树，每个点有颜色 `start[x]`，目标颜色 `target[x]`（0/1）',
                 '一次操作选一条边，把它的两个端点颜色都翻转',
                 '求操作次数最少的边下标集合（升序）；无解返回 `[-1]`',
                 '示例 2：`start=0011000`，`target=0010001` → `[1,2,5]`'],
        quote='如果叶子 x 的 start[x] != target[x]，那么与 x 相连的这条边，一定要翻转……如果叶子 x 的 start[x] = target[x]，……与 x 相连的这条边，一定不能翻转。',
        quote_src='—— 灵茶山艾府题解',
        idea=['叶子只连一条边：颜色不对就必须翻它，对了就绝不能翻',
              '处理完叶子把它剥掉（剥洋葱），父亲的颜色已被确定，问题变小',
              '自底向上 DFS：`dfs(x, fa)` 返回「`x-fa` 这条边是否要翻」；被翻一次就让 `rev` 取反'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`dfs(0, -1)` 为真说明只剩根颜色不对，没有边可翻 → `[-1]`',
                 '写法一用列表 `ans` 追加后 `sort`，`O(n log n)`；这里用布尔数组 `revs` 按下标收集，免排序',
                 '也可以用拓扑排序，从度为 1 的叶子开始剥']),
)
