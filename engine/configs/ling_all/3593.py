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
EDGES = [[0, 4], [0, 1], [1, 2], [1, 3]]
COST = [3, 4, 1, 1, 7]
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
    _F[x] = COST[x] + max([_calc(c) for c in _ch[x]] or [0])
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

    def f(i):
        d = dict(txt=COST[i])
        if live and i == x:
            d['fill'] = 'yellow'
            if line >= 23:
                d['bot'] = f'返回 {_F[i]}'
        elif live and i in path:
            d['fill'] = 'blue'
        elif live and done(i):
            d['fill'] = 'green'
            d['bot'] = f'返回 {_F[i]}'
        return d
    _draw_tree(cv, box, T, N, EDGES, f, title='树（节点里是 cost；黄 = 当前 x，蓝 = 递归路径，绿 = 已返回「根到该子树叶子」最大路径和）')


def _sum(S, B):
    x = S.get('x')
    if x is None or x < 0 or 'max_s' not in S:
        return ''
    kids = [c for c in _ch[x]]
    return f'节点 `{x}`：已看儿子 → 最大路径和 `max_s = {S["max_s"]}`，`cnt = {S["cnt"]}` 个儿子取到最大；儿子共 `{len(kids)}` 个'




CONFIG = dict(
    num=3593, title='使叶子路径成本相等的最小增量', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='自底向上 DFS · 最大值计数',
    tags=['灵神题单', '链表树与回溯', '难度分 1959'],
    code='''
class Solution:
    def minIncrease(self, n: int, edges: List[List[int]], cost: List[int]) -> int:
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)
        g[0].append(-1)

        def dfs(x: int, fa: int) -> int:
            max_s = cnt = 0
            for y in g[x]:
                if y == fa:
                    continue
                mx = dfs(y, x)
                if mx > max_s:
                    max_s = mx
                    cnt = 1
                elif mx == max_s:
                    cnt += 1

            nonlocal ans
            ans += len(g[x]) - 1 - cnt
            return max_s + cost[x]

        ans = 0
        dfs(0, -1)
        return ans
''',
    call='Solution().minIncrease(5, [[0,4],[0,1],[1,2],[1,3]], [3,4,1,1,7])',
    expect=1,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=_sum, size=26, h=70),
        dict(type='calls', h=190, hide=('n', 'edges', 'cost')),
    ],
    watch=[('x', 'x', 'yellow'), ('max_s', 'max_s', 'cyan'), ('cnt', 'cnt', 'orange'), ('ans', 'ans', 'green')],
    skip=['g[x].append', 'g[y].append', 'for x, y in edges', 'continue'],
    max_steps=90,
    captions={
        'g = [[]': '建邻接表：`g[x]` 是 x 的所有邻居（两条 append 加双向边）',
        'g[0].append(-1)': '给根 `0` 加一个假邻居 `-1`：这样根至少有 2 个邻居，不会被误当成叶子',
        'max_s = cnt = 0': '进入节点 `{x}`：准备统计儿子们返回的==最大路径和==，以及取到最大的个数',
        'if y == fa': lambda S, B, r: (f'`{S.y}` 是父节点 → 跳过，不往回走' if S.y == S.fa else f'`{S.y}` 是儿子 → 递归求它的路径和'),
        'mx = dfs': lambda S, B, r: (f'递归进入儿子 `{S.y}`：去求它那棵子树的最大路径和' if S['_inner'].get('x') != B['_inner'].get('x')
                                     else f'儿子 `{S.y}` 返回「它子树里最大路径和」`mx = {S.mx}`'),
        'if mx > max_s': lambda S, B, r: (f'`mx = {S.mx}` > `max_s = {S.max_s}` → 出现更大的路径和' if S.mx > S.max_s
                                           else f'`mx = {S.mx}` 没超过 `max_s = {S.max_s}`，看看是否相等'),
        'max_s = mx': '最大值更新：`max_s = {max_s}`',
        'cnt = 1': '新的最大值只有 `1` 个儿子取到：`cnt = 1`',
        'elif mx == max_s': lambda S, B, r: (f'`mx = {S.mx}` == `max_s` → 又多一个取到最大值的儿子' if S.mx == S.max_s
                                              else f'`mx = {S.mx}` < `max_s = {S.max_s}` → 它比最大值小，之后要靠 `cost` 增量补齐'),
        'cnt += 1': '`cnt` 加 1，现在有 `{cnt}` 个儿子取到最大值 `{max_s}`',
        'ans += ': lambda S, B, r: (f'节点 {S.x} 有 `{len(S.g[S.x]) - 1}` 个儿子，`{S.cnt}` 个已是最大值，其余 `{len(S.g[S.x]) - 1 - S.cnt}` 个要加成本：`ans` {B.ans} → =={S.ans}=='
                                    if len(S.g[S.x]) - 1 - S.cnt else f'儿子数 `{len(S.g[S.x]) - 1}`，全部已取到最大（或没有儿子）→ 不用修改，`ans` 仍为 {S.ans}'),
        'return max_s + cost': '路径和都补齐成 `max_s` 后，==整棵子树视作一个叶子==：返回 `{max_s} + cost[{x}] = {max_s + cost[x]}`',
        'dfs(0, -1)': '从根 `0` 开始自底向上 DFS',
        'ans = 0': '`ans` 统计需要增大成本的节点数',
        'return ans': '最少需要修改 `{ans}` 个节点',
    },
    cards=dict(
        one_liner='子树里所有叶子路径补齐后，就当成一个叶子',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['树以 `0` 为根，每个节点有成本 `cost[i]`，路径得分 = 路径上成本之和',
                 '只能给节点 ==增加== 成本，使根到所有叶子的路径得分相等',
                 '求需要增加成本的节点数最少是多少',
                 '示例：`cost=[3,4,1,1,7]`，边 `0-4, 0-1, 1-2, 1-3` → `1`'],
        quote='如果后面要增大这些路径和，只需增大 cost[x]，就可以统一增大这些条路径和。这样我们可以视作子树 x 只有一个叶子，且路径和为 4。',
        quote_src='—— 灵茶山艾府题解',
        idea=['成本只能增不能减：子树内路径和要补齐到该子树的==最大值==',
              '`dfs(x)` 返回子树 x 的最大路径和；儿子里有 `cnt` 个取到最大，其余 `儿子数 - cnt` 个都要各加一次',
              '补齐后改 `cost[x]` 就能整体抬高，所以子树等价于一个叶子，往上继续算'],
        summary=['时间 `O(n)`，空间 `O(n)`（递归栈）',
                 '易错：根节点只有一个邻居时会被误当叶子，所以 `g[0].append(-1)`',
                 '`ans += 儿子数 - cnt`：`len(g[x]) - 1` 才是儿子数（减去父亲）',
                 '写法二自底向上，不必再带 `path_sum`；写法一是「有递有归」，把路径和当参数传下去']),
)
