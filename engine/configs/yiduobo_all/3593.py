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


def _state(S, B=None):
    x = S.get('now')
    live = x is not None and x >= 0 and 'ma' in S
    if not live:
        return False, None, set(), set(), 0
    path = _anc(x)
    pre = _PRE.index(x)
    y = S.get('nxt')
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
        if p < q or (p == q and (line >= 21 or (line == 16 and B is not None and B.get('nxt') == y))):
            dn.add(i)
    return True, x, path, dn, line


_ADD = {}
for _i in range(N):
    _k = _ch[_i]
    _ADD[_i] = (len(_k) - sum(1 for c in _k if _F[c] == max(_F[d] for d in _k))) if _k else 0


def _res(S):
    live, x, path, dn, line = _state(S)
    if not live:
        return 0
    return sum(_ADD[i] for i in dn) + (_ADD[x] if line >= 30 else 0)


def _draw(cv, S, B, box, T):
    live, x, path, dn, line = _state(S, B)

    def f(i):
        d = dict(txt=COST[i])
        if live and i == x:
            d['fill'] = 'yellow'
            if line >= 31:
                d['bot'] = f'返回 {_F[i]}'
        elif live and i in path:
            d['fill'] = 'blue'
        elif live and i in dn:
            d['fill'] = 'green'
            d['bot'] = f'返回 {_F[i]}'
        return d
    _draw_tree(cv, box, T, N, EDGES, f, title='树（节点里是 cost；黄 = 当前 now，蓝 = 递归路径，绿 = 已折叠成一个叶子并返回路径得分）')


def _sum(S, B):
    x = S.get('now')
    if x is None or x < 0 or 'tot' not in S:
        return ''
    kids = [c for c in _ch[x]]
    return f'节点 `{x}`：已看儿子 `tot = {S["tot"]}` 个，最大得分 `ma = {S["ma"]}`，等于最大的 `cnt = {S["cnt"]}` 个'




CONFIG = dict(
    num=3593, title='使叶子路径成本相等的最小增量', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='叶子折叠进根 · 一趟 DFS',
    tags=['灵神题单', '链表树与回溯', '难度分 1959'],
    code='''
class Solution(object):
    def minIncrease(self, n, edges, cost):
        
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        global res
        res = 0

        def dfs(now, fa):
            ma = 0
            cnt = 0
            tot = 0
            for nxt in g[now]:
                if nxt == fa:
                    continue
                
                v = dfs(nxt, now)
                tot += 1

                if v > ma:
                    ma = v
                    cnt = 0
                if v == ma:
                    cnt += 1
            
            global res
            res += tot - cnt
            return ma + cost[now]
        
        dfs(0, -1)
        return res
''',
    call='Solution().minIncrease(5, [[0,4],[0,1],[1,2],[1,3]], [3,4,1,1,7])',
    expect=1,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=_sum, size=26, h=70),
        dict(type='calls', h=190, hide=('n', 'edges', 'cost')),
    ],
    watch=[('now', 'now', 'yellow'), ('ma', 'ma', 'cyan'), ('cnt', 'cnt', 'orange'), ('tot', 'tot', 'purple'), ('res', lambda S: _res(S), 'green')],
    skip=['g[x].append', 'g[y].append', 'for x, y in edges', 'continue', 'global res'],
    max_steps=90,
    captions={
        'g = [[]': '建邻接表 `g`（循环里把每条边双向加入）',
        'res = 0': '`res` 是全局答案：需要修改的节点数',
        'ma = 0': '进入节点 `{now}`：准备找孩子们路径得分的==最大值 ma==',
        14: '`cnt` 记录有几个孩子的得分等于 `ma`',
        'tot = 0': '`tot` 记录孩子总数',
        'if nxt == fa': lambda S, B, r: (f'`{S.nxt}` 是父亲 → 不能往回走' if S.nxt == S.fa else f'`{S.nxt}` 是孩子 → 先递归算它折叠后的路径得分'),
        'v = dfs': lambda S, B, r: (f'递归进入孩子 `{S.nxt}`：把它子树里的叶子都折叠到 `{S.nxt}` 上' if S['_inner'].get('now') != B['_inner'].get('now')
                                    else f'孩子 `{S.nxt}` 折叠完成，路径得分 `v = {S.v}`'),
        'tot += 1': '孩子数 `tot` = {tot}',
        'if v > ma': lambda S, B, r: (f'`v = {S.v}` > `ma = {S.ma}` → 出现新的最大值，计数要清零重数' if S.v > S.ma
                                      else f'`v = {S.v}` 不大于 `ma = {S.ma}`，最大值不变'),
        'ma = v': '更新最大值 `ma = {ma}`，`cnt` 清零',
        25: '`cnt` 清零：新最大值还没人数过，下一个 if 会把它数成 1',
        'if v == ma': lambda S, B, r: (f'`v = {S.v}` == `ma` → 它取到最大值，下一行 `cnt` 加一' if S.v == S.ma
                                       else f'`v = {S.v}` < `ma = {S.ma}` → 它要被修改成 `ma`，不计入 `cnt`'),
        'cnt += 1': '取到最大值的孩子数 `cnt = {cnt}`',
        'res += tot - cnt': lambda S, B, r: (f'`tot - cnt = {S.tot} - {S.cnt}` = =={S.tot - S.cnt}== 个孩子要修改 → `res` {_res(S) - (S.tot - S.cnt)} → =={_res(S)}=='
                                             if S.tot - S.cnt else f'`tot - cnt = {S.tot} - {S.cnt} = 0`：得分都相同（或没孩子）→ 无需修改，`res` = {_res(S)}'),
        'return ma + cost': '孩子全部补齐为 `ma`，叶子==折叠==进 `{now}`：得分 `{ma} + cost[{now}] = {ma + cost[now]}`，返回给上层',
        'dfs(0, -1)': '从根 `0` 向下做一趟 DFS',
        'return res': '全部折叠完毕，答案 `res = {ret}`',
    },
    cards=dict(
        one_liner='同一根下所有叶子路径得分相同，就把它们折叠进根',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['以 `0` 为根的树，节点 `i` 的成本是 `cost[i]`，路径得分 = 路径上成本之和',
                 '可以给任意节点增加成本，使根到所有叶子的路径得分相等',
                 '求最少要增加成本的节点个数',
                 '示例：`cost=[3,4,1,1,7]`，边 `0-4, 0-1, 1-2, 1-3` → `1`'],
        quote='对于一颗子树，如果从子树根节点到其中所有叶子节点的路径得分都相同，那么接下来就可以直接修改根节点，而不需要修改单个叶子节点。更进一步的，这种情况下就可以视为将这些叶子折叠进了这个根节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['从样例 3 看出：节点 `1` 下两条路径得分都是 8，修改它自己即可',
              '`dfs(now)` 先让每个孩子折叠成一个得分 `v`，找最大值 `ma` 及出现次数 `cnt`',
              '小于 `ma` 的孩子各改一次：`res += 孩子数 - cnt`',
              '然后 `now` 自己也折叠，得分 `ma + cost[now]` 返回上层'],
        summary=['时间 `O(n)`，空间 `O(n)`（递归栈）',
                 '易错：判断叶子靠「没有孩子」，递归里天然得到 `ma = 0`，直接返回 `cost[now]`',
                 '`if v > ma` 里把 `cnt` 清零，紧接着 `if v == ma` 又让 `cnt` 变 1，两个 if 不是 elif',
                 '对比灵神：灵神用 `-1` 假邻居区分根与叶子，并分析了「有递有归」写法；这里用 `tot` 数孩子']),
)
