def _tidy(children, root=0):
    pos = {}
    cnt = [0]
    md = [0]

    def go(u, d):
        md[0] = max(md[0], d)
        ks = children[u]
        if not ks:
            x = cnt[0]
            cnt[0] += 1
        else:
            for k in ks:
                go(k, d + 1)
            x = (pos[ks[0]][0] + pos[ks[-1]][0]) / 2
        pos[u] = (x, d)
    go(root, 0)
    return pos, max(cnt[0], 1), md[0] + 1


def _children(n, edges):
    g = [[] for _ in range(n)]
    for e in edges:
        g[e[0]].append(e[1])
        g[e[1]].append(e[0])
    ch = [[] for _ in range(n)]
    seen = {0}
    st = [0]
    while st:
        u = st.pop()
        for v in g[u]:
            if v not in seen:
                seen.add(v)
                ch[u].append(v)
                st.append(v)
    for c in ch:
        c.sort()
    return ch


def _draw_tree(cv, box, T, children, edges, node_fn, edge_fn=None, under_fn=None, title=None, rad=23):
    """node_fn(u)->颜色名或None；edge_fn(a,b)->颜色名或None；under_fn(u)->节点下方小字"""
    x0, y0, x1, y1 = box
    if title:
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
        y0 += 44
    pos, w, dep = _tidy(children)
    gx = (x1 - x0 - 80) / max(w - 1, 1) if w > 1 else 0
    gx = min(gx, 170)
    gy = min((y1 - y0 - 90) / max(dep - 1, 1), 120)
    ox = x0 + (x1 - x0 - gx * (w - 1)) / 2
    oy = y0 + 40

    def P(u):
        return (ox + pos[u][0] * gx, oy + pos[u][1] * gy)
    for e in edges:
        a, b = e[0], e[1]
        pa_, pb = P(a), P(b)
        c = edge_fn(a, b) if edge_fn else None
        cv.line([pa_, pb], T[c] if c else T['border'], 7 if c else 3)
        if len(e) > 2:
            mx, my = (pa_[0] + pb[0]) / 2, (pa_[1] + pb[1]) / 2
            lab = str(e[2])
            tw = cv.tlen(lab, 20, True) + 12
            cv.rect((mx - tw / 2, my - 13, mx + tw / 2, my + 13), fill=T['bg'], r=8)
            cv.text((mx, my), lab, 20, T[c] if c else T['muted'], anchor='mm', bold=True, mono=True)
    for u in range(len(children)):
        X, Y = P(u)
        c = node_fn(u)
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=T[c] if c else T['panel2'],
                     outline=T[c] if c else T['border'], width=3)
        cv.text((X, Y), u, 26, T['bg'] if c else T['text'], anchor='mm', bold=True)
        if under_fn:
            s = under_fn(u)
            if s:
                cv.text((X + rad + 8, Y), s, 20, T['cyan'], anchor='lm', bold=True, mono=True)

CODE = '''
class Solution(object):
    def closestNode(self, n, edges, query):

        global pos
        pos = -1

        f = [None] * 4096
        depth = [None] * n
        first = [None] * n
        g = [[] for _ in range(n)]

        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        def add(node, left, right, pos, now):
            if left == right:
                f[node] = now
                return
            
            if f[node] is None or depth[f[node]] > depth[now]:
                f[node] = now

            mid = (left + right) >> 1
            if pos <= mid:
                add(node + node + 1, left, mid, pos, now)
            else:
                add(node + node + 2, mid + 1, right, pos, now)

        def dfs(now, fa):
            global pos
            pos += 1

            if depth[now] is None:
                if fa is None:
                    depth[now] = 0
                else:
                    depth[now] = depth[fa] + 1
                
                first[now] = pos
            
            add(0, 0, 2047, pos, now)

            for next in g[now]:
                if next != fa:
                    dfs(next, now)
                    pos += 1
                    add(0, 0, 2047, pos, now)

        def get(node, left, right, start, end):
            if left == start and right == end:
                return f[node]
            
            mid = (left + right) >> 1
            if end <= mid:
                return get(node + node + 1, left, mid, start, end)
            elif start > mid:
                return get(node + node + 2, mid + 1, right, start, end)
            else:
                left_res = get(node + node + 1, left, mid, start, mid)
                right_res = get(node + node + 2, mid + 1, right, mid + 1, end)
                if depth[left_res] < depth[right_res]:
                    return left_res
                else:
                    return right_res

        def get_lca(x, y):
            start = first[x]
            end = first[y]
            if start > end:
                start, end = end, start
            
            return get(0, 0, 2047, start, end)

        dfs(0, None)
        res = []
        for start, end, node in query:
            lca_se = get_lca(start, end)
            lca_sn = get_lca(start, node)
            lca_en = get_lca(end, node)
            if lca_se == lca_sn:
                res.append(lca_en)
            elif lca_se == lca_en:
                res.append(lca_sn)
            else:
                res.append(lca_se)
        
        return res
'''
LINE_TXT = {i: l for i, l in enumerate(CODE.strip('\n').split('\n'), 1)}
N = 7
EDGES = [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5], [2, 6]]
QUERY = [[3, 5, 4], [5, 6, 4]]
CH = _children(N, EDGES)
PAR = {c: p for p, cs in enumerate(CH) for c in cs}


def _ln(sub, nth=0):
    r = [i for i, l in LINE_TXT.items() if sub in l]
    return r[nth] if r else 10 ** 6


def _euler():
    g = [[] for _ in range(N)]
    for x, y in EDGES:
        g[x].append(y)
        g[y].append(x)
    out = []

    def go(u, fa):
        out.append(u)
        for v in g[u]:
            if v != fa:
                go(v, u)
                out.append(u)
    go(0, None)
    return out


EUL = _euler()


def _path(a, b):
    up = [a]
    while up[-1] in PAR:
        up.append(PAR[up[-1]])
    seen = set(up)
    down = [b]
    while down[-1] not in seen:
        down.append(PAR[down[-1]])
    return up[:up.index(down[-1]) + 1] + down[:-1][::-1]


_A = _ln('def add')
_G1, _G2 = _ln('def get(') , _ln('return get(0, 0, 2047, start, end)')
_SKIP = list(range(_A, _ln('def dfs'))) + list(range(_G1, _G2 + 1)) + list(range(_ln('global pos'), _ln('def add'))) + [_ln('global pos', 1)]


def _qi(S):
    res = S.get('res')
    if res is None:
        return None
    ln = S.get('_line', 0)
    k = len(res) - (1 if 'res.append' in LINE_TXT.get(ln, '') else 0)
    return k if 0 <= k < len(QUERY) and ln >= _ln('for start, end, node in query') else None


def _roles(S):
    r = {}
    ln = S.get('_line', 0)
    qi = _qi(S)
    if 'fa' in S and 'now' in S and ln < _ln('for start, end, node in query') and ln >= _ln('def dfs'):
        r[S['now']] = 'yellow'
    elif qi is not None:
        st, en, nd = QUERY[qi]
        r[nd], r[st], r[en] = 'orange', 'blue', 'pink'
        for name in ('lca_se', 'lca_sn', 'lca_en'):
            if ln > _ln(name + ' = get_lca') and S.get(name) is not None and S[name] not in r:
                pass
        if ln > _ln('lca_se = get_lca') and S.get('lca_se') is not None:
            r[S['lca_se']] = 'yellow'
        if 'res.append' in LINE_TXT.get(ln, '') and S.get('res'):
            r[S['res'][-1]] = 'green'
    return r


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    r = _roles(S)
    inner = S
    pe = set()
    qi = _qi(S)
    if qi is not None:
        P = _path(QUERY[qi][0], QUERY[qi][1])
        pe = {frozenset(e) for e in zip(P, P[1:])}
    first = S.get('first')
    mid = y0 + (y1 - y0) * 0.66
    _draw_tree(cv, (x0, y0, x1, mid), T, CH, EDGES, lambda u: r.get(u),
               edge_fn=lambda a, b: 'blue' if frozenset((a, b)) in pe else None,
               under_fn=(lambda u: f'd={S["depth"][u]}' if S.get('depth') and S['depth'][u] is not None else None),
               title='树（蓝粉 = 路径 start→end，橙 = node，黄 = lca / DFS 当前点，绿 = 答案）')
    # 欧拉序
    n = len(EUL)
    cell = min(64, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    ys = mid + 40
    cv.text((x0 + 18, mid + 6), '欧拉序（进入或回溯到一个点就记一次）', 22, T['muted'], bold=True)
    pos = len(EUL) - 1
    if 'now' in inner and 'fa' in inner and S.get('_line', 0) < _ln('for start, end, node in query'):
        occ = [i for i, u in enumerate(EUL) if u == inner['now']]
        ln = S.get('_line', 0)
        nx = inner.get('next')
        ci = CH[inner['now']].index(nx) if nx in CH[inner['now']] else 0
        if ln >= _ln('pos += 1', 1):
            pos = occ[ci + 1]
        elif ln >= _ln('dfs(next, now)'):
            pos = occ[ci]
        else:
            pos = occ[0]
    elif 'start' not in inner and 'res' not in S:
        pos = -1
    for i, u in enumerate(EUL):
        X = sx + i * cell
        done = i <= pos
        c = r.get(u) if (done and 'now' in inner and i == pos) else None
        cv.rect((X + 2, ys + 22, X + cell - 2, ys + 22 + cell * 0.8), fill=T['yellow'] if (i == pos and 'now' in inner) else (T['panel2'] if done else None), outline=T['border'], r=6)
        if done:
            cv.text((X + cell / 2, ys + 22 + cell * 0.4), u, 24, T['bg'] if (i == pos and 'now' in inner) else T['text'], anchor='mm', bold=True)
        cv.text((X + cell / 2, ys + 22 + cell * 0.8 + 4), i, 16, T['dim'], anchor='mt', mono=True)


CONFIG = dict(
    num=2277, title='树中最接近路径的节点', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='欧拉序 + 线段树求 LCA',
    tags=['会员题'],
    code=CODE,
    call='Solution().closestNode(7, [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]], [[3,5,4],[5,6,4]])',
    expect=[1, 2],
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=['lca_se', 'lca_sn', 'lca_en', ('res', 'res', 'green')],
    skip=_SKIP + ['pos = -1', 'f = [None]', 'depth = [None]', 'first = [None]', 'g = [[] for', 'for x, y in edges', 'g[x].append', 'g[y].append',
                  'res = []', 'for next in g[now]', 'if next != fa', 'if depth[now] is None', 'if fa is None', 'else:'],
    max_steps=100,
    captions={
        'dfs(0, None)': '从根 0 开始 DFS，记下==欧拉序==：每次进入或回溯到一个节点，就把它记在下一个位置（同时写进线段树）',
        'depth[now] = 0': '根节点深度 0',
        'depth[now] = depth[fa] + 1': '`depth[{now}] = depth[{fa}] + 1 = {depth[now]}`',
        'first[now] = pos': '`first[{now}]` = 节点 {now} 在欧拉序里==第一次出现==的位置',
        'add(0, 0, 2047, pos, now)': lambda S, B, r: f'把 `{S.now}` 写进线段树的第 pos 位（线段树每个区间存==深度最小==的点）',
        'dfs(next, now)': '去孩子 `{next}`',
        _ln('pos += 1', 0): '进入 `{now}`：欧拉序下标前进一位',
        _ln('pos += 1', 1): '从孩子回溯到 `{now}`：欧拉序再记一次 {now}',
        'lca_se = get_lca(start, end)': lambda S, B, r: f'`lca_se` = start、end 的 LCA：欧拉序 first 之间深度最小的点（线段树区间最小值）',
        'lca_sn = get_lca(start, node)': '`lca_sn` = start 与 node 的 LCA',
        'lca_en = get_lca(end, node)': '`lca_en` = end 与 node 的 LCA',
        'if lca_se == lca_sn': lambda S, B, r: (f'`lca_se = {S.lca_se}` == `lca_sn = {S.lca_sn}`：node 在 end 那一侧（或在 lca_se 的外面）→ 答案是 `lca_en`' if S.lca_se == S.lca_sn else f'`lca_se = {S.lca_se}` != `lca_sn = {S.lca_sn}`：node 与 start 汇合得更深（或在 lca_se 外面），继续比 lca_en'),
        'elif lca_se == lca_en': lambda S, B, r: (f'`lca_se = {S.lca_se}` == `lca_en = {S.lca_en}`：node 挂在 start 那一侧 → 答案是 `lca_sn`' if S.lca_se == S.lca_en else f'`lca_en = {S.lca_en}` 也不等于 lca_se：node 落在别的子树或外面 → 答案就是 `lca_se`'),
        'res.append(lca_en)': '答案 `{lca_en}`：node 往上走，最先碰到路径的点',
        'res.append(lca_sn)': '答案 `{lca_sn}`：node 往上走，最先碰到路径的点',
        'res.append(lca_se)': '答案 `{lca_se}`：整条路径的最高点 lca_se 离 node 最近',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='三个 LCA 两两比一比，就知道 node 离路径最近的点是谁',
        complexity='预处理 `O(n)`，每次询问 `O(log n)`',
        problem=['无向树，`n` 个点；每个询问 `[start, end, node]`：求 start 到 end 的路径上，离 node 最近的那个点',
                 '示例：`edges=[[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]]`',
                 '询问 `[3,5,4]` → `1`，`[5,6,4]` → `2`'],
        quote='首先，start到end的路径是经典的lca问题，……对于node，其所处位置有三种情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['记 `lca_se` = start 与 end 的 LCA，路径 = start→lca_se→end 两条树链',
              '`lca_sn`、`lca_en` 分别是 node 与两端的 LCA：node 在哪一侧，答案就是对应那个 LCA；都不在时答案 = `lca_se`',
              '求 LCA 用欧拉序 + 线段树：两点 first 位置之间，深度最小的点就是 LCA'],
        summary=['预处理 `O(n)` 个欧拉序位置，每次 LCA 查询 `O(log n)`',
                 '三种情况：`lca_se == lca_sn` → `lca_en`；`lca_se == lca_en` → `lca_sn`；否则 `lca_se`',
                 '题目数据小，也可以对每个询问直接 BFS（原文提到的暴力解法）',
                 '线段树 `f` 固定开 4096 个位置，欧拉序长度是 `2n−1`，要保证不超过 2048'],
    ),
)
