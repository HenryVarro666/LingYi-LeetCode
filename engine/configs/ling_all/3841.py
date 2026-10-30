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


def _info(S):
    op = S.get('op')
    line = S.get('_line') or 0
    x, y = S.get('x'), S.get('y')
    return op, line, x, y


def _draw(cv, S, B, box, T):
    t = S.get('t')
    chars = [chr(97 + v) for v in t] if isinstance(t, list) and len(t) == N else list(STR)
    g, f = S.get('g'), S.get('f')
    par_val = None
    if hasattr(g, 'path_xor_from_root') and hasattr(f, 'pre'):
        par_val = [g.path_xor_from_root[i] ^ f.pre(g.tin[i]) for i in range(N)]
    op, line, x, y = _info(S)
    qpair = upd = None
    if isinstance(op, str) and isinstance(x, int):
        if op[0] == 'q' and isinstance(y, int) and line >= 119:
            qpair = (x, y)
        elif op[0] == 'u' and line >= 111:
            upd = x
    _draw_tree(cv, S, B, box, T, chars, par_val, qpair, upd, line >= 121 and 'lca' in S)


def _formula(S):
    op, line, x, y = _info(S)
    if isinstance(op, str) and isinstance(x, int):
        if op[0] == 'u' and 'val' in S and line >= 113:
            return f'`val = (1<<旧) ^ (1<<新)` = =={_letters(S["val"])}==：子树 {x} 里所有节点的路径奇偶性都异或它'
        if op[0] == 'q' and 'lca' in S and line >= 121 and 'res' in S and isinstance(y, int):
            r = S['res']
            return f'路径 {x}→{y} 奇数次的字母：=={_letters(r)}==，`res & (res-1) == 0` → ' + ('==是回文==' if r & (r - 1) == 0 else '不是回文')
    return '字母次数的奇偶性 = 一个二进制数；能重排成回文 ⇔ 至多一位为 1（`0` 或 `2^k`）'


def _cap_lca(S, B, ret):
    return f'`lca({S.x}, {S.y}) = {S.lca}`：路径 x→y 经过的最高点'


def _cap_res(S, B, ret):
    x, y, l = S.x, S.y, S.lca
    return (f'`XOR[{x}] ^ XOR[{y}]`：lca={l} 及以上的部分都抵消了（lca 自己也被消掉）→ 再异或 `1 << t[{l}]` 补回来 → '
            f'奇数次字母 =={_letters(S.res)}==')


def _cap_ans(S, B, ret):
    r = S.res
    if r & (r - 1) == 0:
        return f'`res` = {_letters(r)}：至多一位为 1 → ==能重排成回文==，`True`'
    return f'`res` = {_letters(r)}：有 ==多于一位== 为 1 → 不能，`False`'


CONFIG = dict(
    num=3841, title='查询树上回文路径', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='状压奇偶 + LCA + 差分树状数组（异或）',
    tags=['常用数据结构', '链表树与回溯', '难度分 2384'],
    code='''
# 模板来自我的题单 https://leetcode.cn/circle/discuss/mOr1u6/
class FenwickTree:
    def __init__(self, n: int):
        self.tree = [0] * (n + 1)  # 使用下标 1 到 n

    # a[i] ^= val
    # 1 <= i <= n
    # 时间复杂度 O(log n)
    def update(self, i: int, val: int) -> None:
        t = self.tree
        while i < len(t):
            t[i] ^= val
            i += i & -i

    # 计算前缀异或和 a[1] ^ ... ^ a[i]
    # 1 <= i <= n
    # 时间复杂度 O(log n)
    def pre(self, i: int) -> int:
        t = self.tree
        res = 0
        while i > 0:
            res ^= t[i]
            i &= i - 1
        return res

# 模板来自我的题单 https://leetcode.cn/circle/discuss/K0n2gO/
class LcaBinaryLifting:
    def __init__(self, edges: List[List[int]], s: List[int]):
        n = len(edges) + 1
        m = n.bit_length()
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        depth = [0] * n
        pa = [[-1] * n for _ in range(m)]
        tin = [0] * n  # DFS 时间戳
        tout = [0] * n
        clock = 0
        path_xor_from_root = [0] * n  # 从根开始的路径的字母出现次数的奇偶性
        path_xor_from_root[0] = 1 << s[0]

        def dfs(x: int, fa: int) -> None:
            pa[0][x] = fa
            nonlocal clock
            clock += 1
            tin[x] = clock
            for y in g[x]:
                if y != fa:
                    depth[y] = depth[x] + 1
                    path_xor_from_root[y] = path_xor_from_root[x] ^ (1 << s[y])
                    dfs(y, x)
            tout[x] = clock

        dfs(0, -1)

        for i in range(m - 1):
            for x in range(n):
                if (p := pa[i][x]) != -1:
                    pa[i + 1][x] = pa[i][p]

        self.depth = depth
        self.pa = pa
        self.tin = tin
        self.tout = tout
        self.path_xor_from_root = path_xor_from_root

    # 返回 node 的第 k 个祖先节点
    # 如果不存在，返回 -1
    def get_kth_ancestor(self, node: int, k: int) -> int:
        pa = self.pa
        for i in range(k.bit_length()):
            if k >> i & 1:
                node = pa[i][node]
                if node < 0:
                    return -1
        return node

    # 返回 x 和 y 的最近公共祖先
    def get_lca(self, x: int, y: int) -> int:
        if self.depth[x] > self.depth[y]:
            x, y = y, x
        # 使 y 和 x 在同一深度
        y = self.get_kth_ancestor(y, self.depth[y] - self.depth[x])
        if y == x:
            return x
        pa = self.pa
        for i in range(len(pa) - 1, -1, -1):
            px, py = pa[i][x], pa[i][y]
            if px != py:
                x, y = px, py  # 同时往上跳 2**i 步
        return pa[0][x]

class Solution:
    def palindromePath(self, n: int, edges: list[list[int]], s: str, queries: list[str]) -> list[bool]:
        ord_a = ord('a')
        t = [ord(ch) - ord_a for ch in s]  # 映射成 [0, 25] 中的整数

        g = LcaBinaryLifting(edges, t)
        tin = g.tin
        tout = g.tout
        path_xor_from_root = g.path_xor_from_root

        f = FenwickTree(n)  # 注意树状数组是异或运算
        ans = []

        for q in queries:
            op, x, y = q.split()
            x = int(x)
            if op[0] == 'u':
                c = ord(y) - ord_a
                val = (1 << t[x]) ^ (1 << c)  # 擦除旧的，换上新的
                t[x] = c
                # 子树 x 全部异或 val，转换成对区间 [tin[x], tout[x]] 的差分更新
                f.update(tin[x], val)
                f.update(tout[x] + 1, val)
            else:
                y = int(y)
                lca = g.get_lca(x, y)
                res = path_xor_from_root[x] ^ path_xor_from_root[y] ^ f.pre(tin[x]) ^ f.pre(tin[y]) ^ (1 << t[lca])
                ans.append(res & (res - 1) == 0)  # 至多一个字母的出现次数是奇数

        return ans
''',
    call=f'Solution().palindromePath({N}, {EDGES}, {STR!r}, {QUERIES})',
    expect=[True, False, True, False],
    skip=[72, 106, 3, 4, 10, 11, 12, 13, 19, 20, 21, 22, 23, 24,
          29, 30, 31, 32, 33, 34, 36, 37, 38, 39, 40, 41, 42, 45, 46, 47, 49, 50, 51, 53,
          58, 59, 60, 61, 63, 64, 65, 66, 67, 73, 74, 75, 76, 77, 78, 82, 83, 86, 87, 88, 89, 90, 91, 92,
          97, 101, 102, 103, 106, 108, 110, 111, 112, 118, 119],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=_formula, size=26, h=90),
        dict(type='array', var='f.tree', label='f.tree：差分树状数组（只存“区间更新”的异或，下标 1..n）', h=150, cell=80),
    ],
    watch=[('x', 'x', 'pink'), ('y', 'y', 'orange'), ('lca', 'lca', 'green'), ('ans', 'ans', 'blue')],
    captions={
        48: '`tin[{x}] = {clock}`：进入时间戳；子树 = 区间 `[tin, tout]`',
        52: '`path_xor_from_root[{y}]`：从根 0 到 {y} 的字母奇偶性（父亲的异或自己的字母）',
        54: '`tout[{x}] = {clock}`：子树 {x} 的时间戳区间为 `[{tin[x]}, {tout[x]}]`',
        56: 'DFS 一次：求每个点的 `tin/tout` 和「根到它」的字母奇偶性 `path_xor_from_root`',
        85: '先把较深的点往上提到同一深度（倍增求第 k 个祖先）',
        93: '两点的父亲相同 → 父亲就是 ==LCA==：`{pa[0][x]}`',
        98: '字母映射成 0~25：`t = {t}`',
        100: '预处理：`tin/tout`、倍增数组 `pa`、`path_xor_from_root`',
        105: '`f`：差分树状数组，==异或==运算；保存的是更新带来的修改，不含初始值',
        106: '`ans` 收集每个 query 的答案',
        109: lambda S, B, r: (f'处理 `"{S.q}"`：==update== —— 改节点 {S.x} 的字母为 `{S.y}`' if S.op[0] == 'u'
                              else f'处理 `"{S.q}"`：==query== —— 路径 {S.x}→{S.y} 能否重排成回文'),
        113: '`val = (1<<旧) ^ (1<<新)` = =={val}==（二进制）：擦掉旧字母、换上新字母',
        114: '`t[{x}] = {t[x]}`：记下新字母',
        116: '`f.update(tin[{x}], val)`：差分，区间 `[tin, tout]` 的起点异或 val',
        117: '`f.update(tout[{x}] + 1, val)`：终点后一位再异或一次 val 抵消 → ==只影响子树 {x}==',
        120: _cap_lca,
        121: _cap_res,
        122: _cap_ans,
        124: '全部处理完，返回 `{ret}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='异或前缀 + LCA 抵消，修改变成子树区间异或',
        complexity='时间 `O((n+q) log n)`，空间 `O(n log n)`',
        problem=['无向树，每个节点一个小写字母；`update u c` 改字母，`query u v` 问 u→v 路径上的字母能否==重排成回文==',
                 '返回每个 query 的布尔答案',
                 '本视频：`n=5`，节点字母 `abcab`，5 个操作 → `[True, False, True, False]`'],
        quote='用二进制数表示路径中的字母出现次数的奇偶性。如果二进制数是 0 或者 2^k，那么至多有一个字母的出现次数是奇数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['回文 ⇔ 至多一个字母出现奇数次 ⇔ 奇偶性二进制数 `res` 满足 `res & (res-1) == 0`',
              '路径 x→y 的奇偶性 = `XOR[x] ^ XOR[y] ^ (1 << s[lca])`，lca 被抵消了，要补回来',
              '改 `s[x]` 只影响子树 x 的 `XOR[i]`：子树 = DFS 时间戳区间，==区间异或、单点查询==用差分树状数组'],
        summary=['时间 `O((n+q) log n)`：LCA 倍增 + 树状数组；空间 `O(n log n)`',
                 '易错：lca 要再异或一次自己的字母；update 的区间终点要用 `tout + 1`',
                 '易错：树状数组只记录“更新”，初始的 `path_xor_from_root` 要另外异或上',
                 '树状数组换成异或：`update` 用 `^=`，`pre` 用 `^`，区间更新 = 两端各异或一次',
                 '前置题：2791 树中可以形成回文的路径数；3515 带权树中的最短路径（同样的 tin/tout + 差分树状数组）'],
    ),
)
