N = 5
EDGES = [[0, 1], [0, 2], [1, 3], [1, 4]]
STR = 'abcab'
QUERIES = ['query 3 4', 'query 3 2', 'update 1 c', 'query 3 2', 'query 4 2']


def _letters(v):
    s = ''.join(chr(97 + k) for k in range(26) if v >> k & 1)
    return s if s else '空'


def _layout():
    ch = {i: [] for i in range(N)}
    par = {0: -1}
    st = [0]
    seen = {0}
    adj = {i: [] for i in range(N)}
    for a, b in EDGES:
        adj[a].append(b)
        adj[b].append(a)
    order = []

    def go(u, p, d):
        order.append(u)
        for v in adj[u]:
            if v != p:
                par[v] = u
                ch[u].append(v)
                go(v, u, d + 1)
    go(0, -1, 0)
    depth = {0: 0}
    for u in order:
        for v in ch[u]:
            depth[v] = depth[u] + 1
    xs = {}
    cnt = [0]

    def place(u):
        if not ch[u]:
            xs[u] = cnt[0]
            cnt[0] += 1
        else:
            for v in ch[u]:
                place(v)
            xs[u] = (xs[ch[u][0]] + xs[ch[u][-1]]) / 2
    place(0)
    return ch, par, depth, xs, cnt[0]


CH, PAR, DEPTH, XS_, NLEAF = _layout()


def _subtree(u):
    r = [u]
    for v in CH[u]:
        r += _subtree(v)
    return r


def _path(a, b):
    pa = []
    x = a
    while x != -1:
        pa.append(x)
        x = PAR[x]
    pb = []
    x = b
    while x != -1:
        pb.append(x)
        x = PAR[x]
    sa = set(pa)
    l = next(v for v in pb if v in sa)
    return pa[:pa.index(l) + 1] + pb[:pb.index(l)][::-1], l


def _draw_tree(cv, S, B, box, T, chars, par_val, qpair, upd, lca_ok):
    x0, y0, x1, y1 = box
    maxd = max(DEPTH.values())
    W = x1 - x0 - 120
    H = y1 - y0 - 185
    gx = lambda u: x0 + 60 + (XS_[u] / max(1, NLEAF - 1)) * W
    gy = lambda u: y0 + 95 + (DEPTH[u] / max(1, maxd)) * H
    cv.text((x0 + 18, y0 + 4), '树（圆 = 节点字母；下方 = 从根到该点路径上奇数次的字母）', 22, T['muted'], bold=True)
    hot, lca = set(), None
    if qpair:
        pth, l = _path(*qpair)
        hot = set(pth)
        lca = l if lca_ok else None
    sub = set(_subtree(upd)) if upd is not None else set()
    for u in range(N):
        for v in CH[u]:
            on = u in hot and v in hot
            cv.line([(gx(u), gy(u)), (gx(v), gy(v))], T['yellow'] if on else T['border'], 5 if on else 2)
    for u in range(N):
        X, Y = gx(u), gy(u)
        fill = T['blue']
        ring = None
        if u in sub:
            fill = T['purple']
        if u in hot:
            ring = T['yellow']
        if qpair and u in qpair:
            fill = T['pink']
        if lca is not None and u == lca:
            fill = T['green']
        cv.rect((X - 30, Y - 30, X + 30, Y + 30), fill=fill, r=30, outline=ring or T['border'], width=5 if ring else 1)
        cv.text((X, Y), chars[u], 32, T['bg'], anchor='mm', bold=True, mono=True)
        cv.text((X - 38, Y - 30), u, 18, T['dim'], anchor='rb', mono=True)
        if par_val is not None:
            cv.text((X, Y + 36), '{' + _letters(par_val[u]) + '}', 20, T['cyan'], anchor='mt', mono=True)


def _segget(f, n, x):
    p, l, r, res = 0, 0, n - 1, 0
    while True:
        res ^= f[p]
        if l == r:
            return res
        m = (l + r) // 2
        if x <= m:
            p, r = p + p + 1, m
        else:
            p, l = p + p + 2, m + 1


def _info(S):
    q = S.get('q')
    line = S.get('_line') or 0
    return q, line, S.get('u'), S.get('v')


def _draw(cv, S, B, box, T):
    xr = S.get('xor')
    chars = [chr(97 + v.bit_length() - 1) for v in xr] if isinstance(xr, list) and len(xr) == N else list(STR)
    par_val = None
    pre_xor, pos, f = S.get('pre_xor'), S.get('pos'), S.get('f')
    if isinstance(pre_xor, list) and isinstance(pos, list) and isinstance(f, list) and 'order' in S and len(S['order']) == N:
        par_val = [pre_xor[i] ^ _segget(f, N, pos[i]) for i in range(N)]
    q, line, u, v = _info(S)
    qpair = upd = None
    if isinstance(q, str) and isinstance(u, int):
        if q[0] == 'q' and isinstance(v, int) and line >= 109:
            qpair = (u, v)
        elif q[0] == 'u' and line >= 101:
            upd = u
    _draw_tree(cv, S, B, box, T, chars, par_val, qpair, upd, line >= 114 and 'lca' in S)


def _info_text(S):
    q, line, u, v = _info(S)
    if isinstance(q, str) and isinstance(u, int):
        if q[0] == 'u' and 'delta' in S and line >= 103:
            return f'`delta = 新 ^ 旧` = =={_letters(S["delta"])}==：把 `pos[{u}]` 起 `covered[{u}] = {S["covered"][u]}` 个位置都异或它'
        if q[0] == 'q' and 'x' in S and line >= 115 and isinstance(v, int):
            x = S['x']
            return f'路径 {u}→{v} 奇数次的字母：=={_letters(x)}== → ' + ('==能==' if x == 0 or x & (x - 1) == 0 else '不能') + '重排成回文'
    od, ps, cv_ = S.get('order'), S.get('pos'), S.get('covered')
    if isinstance(od, list) and len(od) == N and isinstance(ps, list):
        return f'dfs 序 `order = {od}`；`pos = {ps}`；`covered = {cv_}`'
    return '字母次数的奇偶性 = 一个二进制数；能重排成回文 ⇔ 全 0 或恰好一位为 1'


def _cells_f(S):
    f = S.get('f')
    if not isinstance(f, list):
        return None
    return f[:12]


def _cap_cond(S, B, ret):
    x = S.x
    if x == 0 or x & (x - 1) == 0:
        return f'`x` = {_letters(x)}：' + ('全 0' if x == 0 else '恰好一位为 1') + ' → ==能==，加入 True'
    return f'`x` = {_letters(x)}：多于一位为 1 → ==不能==，加入 False'


CONFIG = dict(
    num=3841, title='查询树上回文路径', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='状压奇偶 + dfs 序区间异或（线段树）+ 欧拉序 ST 求 LCA',
    tags=['常用数据结构', '链表树与回溯', '难度分 2384'],
    code='''
class Solution(object):
    def palindromePath(self, n, edges, s, queries):
        
        def dfs(now, pre, fa, level, order, pos, covered, pre_xor):
            if pre == -1:
                level[now] = 0
                pre_xor[now] = xor[now]
            else:
                level[now] = level[pre] + 1
                fa[now] = pre
                pre_xor[now] = pre_xor[pre] ^ xor[now]

            order.append(now)
            pos[now] = len(order) - 1

            for nxt in g[now]:
                if nxt == pre:
                    continue
                dfs(nxt, now, fa, level, order, pos, covered, pre_xor)
            
            covered[now] = len(order) - pos[now]
        
        def update(p, left, right, start, end, delta, f):
            if left == start and right == end:
                f[p] ^= delta
                return

            mid = (left + right) // 2
            if end <= mid:
                update(p + p + 1, left, mid, start, end, delta, f)
            elif start >= mid + 1:
                update(p + p + 2, mid + 1, right, start, end, delta, f)
            else:
                update(p + p + 1, left, mid, start, mid, delta, f)
                update(p + p + 2, mid + 1, right, mid + 1, end, delta, f)

        def get(p, left, right, x):
            if left == right:
                return f[p]
            
            mid = (left + right) // 2
            if x <= mid:
                return f[p] ^ get(p + p + 1, left, mid, x)
            else:
                return f[p] ^ get(p + p + 2, mid + 1, right, x)

        def get_lca(u, v):
            if pos[u] > pos[v]:
                u, v = v, u
            
            left = pos[u] + 1
            right = pos[v]

            p = L
            mi = None
            while left <= right:
                while p > 0 and left + (1 << p) - 1 > right:
                    p -= 1
                if mi is None or level[mi] > level[st[left][p]]:
                    mi = st[left][p]
                left += (1 << p)
            
            return fa[mi]
                
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)
        
        fa = [-1] * n
        level = [0] * n
        covered = [0] * n
        pos = [0] * n
        order = []
        pre_xor = [0] * n
        xor = [1 << (ord(c) - 97) for c in s]

        dfs(0, -1, fa, level, order, pos, covered, pre_xor)
        
        f = [0] * (n * 4)

        L = 1
        while (1 << L) <= n:
            L += 1
        
        st = [[None] * L for _ in range(n)]
        for p in range(L):
            for index in range(n):
                if p == 0:
                    st[index][p] = order[index]
                elif index + (1 << p) - 1 < n:
                    if level[st[index][p - 1]] < level[st[index + (1 << (p - 1))][p - 1]]:
                        st[index][p] = st[index][p - 1]
                    else:
                        st[index][p] = st[index + (1 << (p - 1))][p - 1]

        res = []
        for q in queries:
            if q[0] == 'u':
                u, c = q.split()[1:]
                u = int(u)
                v = 1 << (ord(c) - 97)
                delta = v ^ xor[u]
                update(0, 0, n - 1, pos[u], pos[u] + covered[u] - 1, delta, f)
                xor[u] = v
            else:
                u, v = q.split()[1:]
                u = int(u)
                v = int(v)
                if u == v:
                    res.append(True)
                else:
                    lca = get_lca(u, v)
                    x = get(0, 0, n - 1, pos[u]) ^ get(0, 0, n - 1, pos[v]) ^ pre_xor[u] ^ pre_xor[v] ^ xor[lca]
                    if x == 0 or (x & (x - 1)) == 0:
                        res.append(True)
                    else:
                        res.append(False)
        
        return res
''',
    call=f'Solution().palindromePath({N}, {EDGES}, {STR!r}, {QUERIES})',
    expect=[True, False, True, False],
    skip=[4, 5, 6, 8, 9, 10, 13, 16, 17, 18, 19,
          24, 25, 26, 28, 29, 30, 31, 32, 33, 34, 35, 38, 39, 41, 42, 43, 44, 45,
          48, 49, 51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 63,
          65, 66, 67, 68, 70, 71, 72, 73, 74, 75, 82, 83, 84, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95,
          97, 98, 99, 101, 102, 106, 108, 109, 111, 112, 117],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=_info_text, size=24, h=100),
        dict(type='array', var=_cells_f, label='f：线段树节点上的“整段异或”（只记修改）', h=140, cell=64),
    ],
    watch=[('u', 'u', 'pink'), ('v', 'v', 'orange'), ('lca', 'lca', 'green'), ('res', 'res', 'blue')],
    captions={
        7: '根的 `pre_xor` = 自己字母的二进制数',
        11: '`pre_xor[{now}] = pre_xor[{pre}] ^ xor[{now}]`：根到 {now} 的字母奇偶性',
        14: '`pos[{now}] = {pos[now]}`：{now} 在 dfs 序里的位置（先序，首次访问）',
        21: '`covered[{now}] = {covered[now]}`：子树 {now} 占 dfs 序 `[{pos[now]}, {pos[now] + covered[now] - 1}]`，子树 = 一段连续区间',
        76: '`xor[i]`：节点 i 的字母对应的二进制数（第 k 位 = 字母 k）',
        78: 'dfs 一次：算 `level / fa / order / pos / covered / pre_xor`',
        80: '`f`：线段树，==只存区间修改的异或==，初始全 0；单点求值时层层异或',
        100: lambda S, B, r: (f'处理 `"{S.q}"`：==update==' if S.q[0] == 'u' else f'处理 `"{S.q}"`：==query==，判断路径能否重排成回文'),
        103: '`delta = v ^ xor[{u}]` = =={delta}==：擦掉旧字母、换上新字母',
        104: '子树 {u} = 区间 `[{pos[u]}, {pos[u] + covered[u] - 1}]`：整段异或 `delta`（线段树区间修改不下放）',
        105: '`xor[{u}]` 记下新字母',
        107: lambda S, B, r: ('拆出 `u, c`' if S.q[0] == 'u' else f'拆出 `u, v`：路径 {S.q.split()[1]} → {S.q.split()[2]}'),
        110: lambda S, B, r: (f'`u == v`：只有一个点，必然回文' if S.u == S.v else f'`u != v`：要先求 LCA'),
        113: '`lca = get_lca({u}, {v}) = {lca}`：欧拉序区间里深度最小的点的父亲（ST 表查最小深度）',
        114: '`x = 线段树修改值[{u}] ^ 线段树修改值[{v}] ^ pre_xor[{u}] ^ pre_xor[{v}] ^ xor[{lca}]`：lca 及以上的部分都抵消了，补回 `xor[lca]`',
        115: _cap_cond,
        116: '`res = {res}`',
        118: '`res = {res}`',
        120: '全部处理完，返回 `{ret}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='dfs 序把子树变成区间：修改 = 区间异或，查询 = 单点异或',
        complexity='时间 `O((n+q) log n)`，空间 `O(n log n)`',
        problem=['无向树，每个节点一个小写字母；`update u c` 改字母，`query u v` 判断 u→v 路径上的字母能否==重新排列成回文==',
                 '返回每个 query 的布尔值',
                 '本视频：`n=5`，字母 `abcab`，5 个操作 → `[True, False, True, False]`'],
        quote='可以借助dfs序实现，理由是以u为根节点的子树中的所有节点，在dfs序中恰好是连续的一段，也就是说此时的修改变成了对于一个连续区间的修改。',
        quote_src='—— yiduobo 题解原文',
        idea=['回文 ⇔ 出现奇数次的字母至多一个 ⇔ 26 位二进制数为 `0` 或 2 的幂',
              '路径 u→v = `pre_xor[u] ^ pre_xor[v] ^ xor[lca]`；修改点 u 会改变整棵子树的 `pre_xor`',
              'dfs 序上子树是一段区间 → 线段树「区间异或、单点查询」；LCA 用欧拉序 + ST 表'],
        summary=['时间 `O((n+q) log n)`，空间 `O(n log n)`',
                 '易错：修改要异或 `新 ^ 旧`，而不是直接异或新字母',
                 '易错：LCA = dfs 序 `[pos[u]+1, pos[v]]` 里深度最小节点的==父亲==；`u == v` 单独判断',
                 '线段树不需要下放标记：单点求值时把路径上每个节点的值异或起来',
                 '对比灵神：灵神用倍增求 LCA、差分树状数组做区间异或；yiduobo 用 ST 表 + 线段树',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
