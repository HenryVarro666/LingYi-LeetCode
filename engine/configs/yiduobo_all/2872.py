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


def _state(S, B=None):
    x = S.get('now')
    if x is None or x < 0 or 's' not in S:
        return False, None, set(), set(), 0
    path = _anc(x)
    pre = _PRE.index(x)
    y = S.get('child')
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
        if p < q or (p == q and (line >= 19 or (line == 15 and B is not None and B.get('child') == y))):
            dn.add(i)
    return True, x, path, dn, line


def _cut(i):
    return i != 0 and _F[i] % K == 0


TOTAL = sum(1 for i in range(N) if _cut(i))


def _res(S):
    live, x, path, dn, line = _state(S)
    if not live:
        return TOTAL if (S.get('_line') or 0) >= 27 else 0
    y = S.get('child')
    r = sum(1 for i in dn if _cut(i))
    if line == 19 and y in dn and _cut(y):
        r -= 1
    return r


def _draw(cv, S, B, box, T):
    live, x, path, dn, line = _state(S, B)
    fin = set(dn) | ({x} if live and line >= 24 else set())

    def f(i):
        d = dict(txt=VAL[i])
        if i in fin:
            cut = i in dn and _cut(i)
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
        return 'red' if c in dn and _cut(c) else None
    _draw_tree(cv, box, T, N, EDGES, f, edge_fn=e, title=f'树（点权，k={K}；黄环 = 当前，蓝环 = 路径，绿 = 和可被 k 整除，红线 = 删边）')


def _sum(S, B):
    live, x, path, dn, line = _state(S)
    if not live:
        return ''
    if line in (19, 20) and 'v' in S:
        return f'孩子 `{S["child"]}` 的子树和 `v = {S["v"]}`，`v % k = {S["v"]} % {K} = {S["v"] % K}`' + (' → ==这条边可删==' if S['v'] % K == 0 else ' → 不能删')
    if line >= 24:
        return f'节点 `{x}` 的子树和 = `s + values[{x}] = {S["s"]} + {VAL[x]} = {S["s"] + VAL[x]}`'
    return f'节点 `{x}`：各孩子的子树和累计 `s = {S["s"]}`（自己的点权最后才加）'


CONFIG = dict(
    num=2872, title='可以被 K 整除连通块的最大数目', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='反证法 · 删边 · 子树和',
    tags=['灵神题单', '链表树与回溯', '难度分 1968'],
    code='''
class Solution(object):
    def maxKDivisibleComponents(self, n, edges, values, k):

        g = {x : set() for x in range(n)}
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)

        global res
        res = 0

        def dfs(now, fa):
            global res
            s = 0
            for child in g[now]:
                if child == fa:
                    continue
                v = dfs(child, now)
                if v % k == 0:
                    res += 1
                
                s += v

            return s + values[now]
        
        dfs(0, -1)
        return res + 1
''',
    call='Solution().maxKDivisibleComponents(5, [[0,2],[1,2],[1,3],[2,4]], [1,8,1,4,4], 6)',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=440),
        dict(type='text', fn=_sum, size=26, h=70),
        dict(type='calls', h=130, hide=('n', 'edges', 'values', 'k')),
    ],
    watch=[('now', 'now', 'yellow'), ('s', 's', 'cyan'), ('res', lambda S: _res(S), 'green')],
    skip=['g[x].add', 'g[y].add', 'for x, y in edges', 'global res', 's += v', 'continue'],
    max_steps=90,
    captions={
        'g = {x': '用集合建邻接表：每条边双向加入',
        'res = 0': '`res` 统计删掉的边数；最后连通块数 = 删边数 + 1',
        'dfs(0, -1)': '从根 `0` 向下递归：先处理孩子，再回来判断边能不能删',
        's = 0': '进入节点 `{now}`：`s` 先累计各孩子的子树和（自己的点权最后再加）',
        'for child in g[now]': lambda S, B, r: (
            ('孩子的子树和已并入：`s += v` → ' + f'`s = {S.s}`；' if 'child' in B['_inner'] and B['_inner']['child'] != B['_inner'].get('fa') else '')
            + (f'邻居都看完，孩子们的子树和 `s = {S.s}`' if 'child' in B['_inner'] and S.child == B.child else f'枚举邻居 `child = {S.child}`')),
        'if child == fa': lambda S, B, r: (f'`{S.child}` 是父亲，跳过' if S.child == S.fa else f'`{S.child}` 是孩子 → 递归求它的子树和 `v`'),
        'v = dfs': lambda S, B, r: (f'递归进入孩子 `{S.child}`：求以它为根的子树节点值之和 `v`' if S['_inner'].get('now') != B['_inner'].get('now')
                                    else f'子树和 `v = {S.v}`'),
        'if v % k == 0': lambda S, B, r: (f'`v % k = {S.v} % {S.k} = 0`：这一侧是 k 的倍数，另一侧也必是（总和是 k 的倍数）→ ==边可以删==' if S.v % S.k == 0
                                          else f'`v % k = {S.v} % {S.k} = {S.v % S.k}` ≠ 0 → 这条边不能删'),
        'res += 1': lambda S, B, r: f'删掉 `{S.now}` 与孩子 `{S.child}` 之间的边：`res` = =={_res(S)}==',
        'return s + values': '孩子们的和 `{s}` 加上自己的点权 `{values[now]}`，子树和 =={s + values[now]}== 返回上层',
        'return res + 1': lambda S, B, r: f'删掉的边数 `res = {r - 1}`，连通块数 = 删边数 + 1 = =={r}==',
    },
    cards=dict(
        one_liner='一条边两侧的和都是 k 的倍数，这条边就该删',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树，节点有点权 `values[i]`，总和是 `k` 的倍数',
                 '删去若干条边，让每个连通块的点权和都能被 `k` 整除',
                 '要连通块尽量多，等价于==删尽量多的边==',
                 '示例：`values=[1,8,1,4,4]`，`k=6` → `2`'],
        quote='若某条边两侧的节点值之和都是k的倍数，那么这条边就可以被删掉。在这里可以尝试使用反证法来证明这个结论。',
        quote_src='—— yiduobo 题解原文',
        idea=['反证：若最优解里某连通块跨过这条边，它在两侧的部分都是若干个 k 的倍数之差，也是 k 的倍数，还能继续切开',
              '所以只需判断每条边：孩子子树的和 `v` 是否被 `k` 整除（另一侧自动整除）',
              '`dfs` 返回子树和；孩子的 `v % k == 0` 就 `res += 1`，最后答案 `res + 1`'],
        summary=['时间 `O(n)`，空间 `O(n)`（递归栈）',
                 '这里 `res` 只统计真实存在的边，所以最后要 `+ 1`；灵神把根的「虚拟父边」也计入，省去这个加一',
                 '返回值 `s + values[now]` 是整棵子树的和，边的判断放在父节点里做',
                 '用 `global res` 在嵌套函数里累加；这里的 `g` 用集合存邻居']),
)
