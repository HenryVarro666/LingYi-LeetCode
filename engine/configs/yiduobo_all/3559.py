def _layout_tree(ch, root):
    pos, cnt = {}, [0]

    def go(u, d):
        kids = ch.get(u, [])
        if not kids:
            x = cnt[0]
            cnt[0] += 1
        else:
            xs = [go(v, d + 1) for v in kids]
            x = (xs[0] + xs[-1]) / 2
        pos[u] = (x, d)
        return x
    go(root, 0)
    return pos, cnt[0]


def _tree_view(ch, root, colors, title, tags=None, wt=None, lab=None):
    """ch: {父: [子...]}；colors(S) -> {节点: 颜色名}；tags(S) -> {节点: 小字}；wt: {子: 边权}"""
    pos, W = _layout_tree(ch, root)
    D = max(d for _, d in pos.values()) + 1

    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
        cell = min(120, (x1 - x0 - 60) / max(W, 1))
        rowh = min(110, (y1 - y0 - 165) / max(D - 1, 1))
        sx = x0 + 30 + ((x1 - x0 - 60) - cell * W) / 2
        r = min(28, cell * 0.36, rowh * 0.42)
        P = {u: (sx + (x + 0.5) * cell, y0 + 80 + d * rowh) for u, (x, d) in pos.items()}
        for u, kids in ch.items():
            for v in kids:
                cv.line([P[u], P[v]], T['border'], 3)
                if wt:
                    left = P[v][0] <= P[u][0] + 1
                    cv.text(((P[u][0] + P[v][0]) / 2 + (-10 if left else 10), (P[u][1] + P[v][1]) / 2 - 6), wt[v], 22, T['orange'],
                            anchor='rm' if left else 'lm', bold=True)
        cm = colors(S) or {}
        tg = (tags(S) if tags else None) or {}
        for u, (X, Y) in P.items():
            c = cm.get(u)
            cv.rect((X - r, Y - r, X + r, Y + r), fill=T[c] if c else T['panel2'], outline=T['border'], width=2, r=r)
            cv.text((X, Y), lab(u) if lab else u, 26, T['bg'] if c else T['text'], anchor='mm', bold=True)
            if u in tg:
                cv.text((X + r + 6, Y + r * 0.5), tg[u], 20, T['muted'], anchor='lm', bold=True)
    return dict(type='custom', draw=draw, h=0)
CH = {1: [2, 3], 3: [4, 5]}


def _colors(S):
    c = {}
    if 'now' in S:
        c[S['now']] = 'yellow'
        if S.get('fa') is not None:
            c[S['fa']] = 'green'
        return c
    for nm, col in (('x', 'blue'), ('y', 'pink'), ('high', 'blue'), ('low', 'pink')):
        v = S.get(nm)
        if isinstance(v, int) and 1 <= v <= 5:
            c[v] = col
    return c


def _tags(S):
    lv = S.get('level')
    if lv is None:
        return {}
    return {i: f'层{lv[i]}' for i in range(1, 6) if lv[i] is not None}


def _formula(S):
    if 'low' in S and 'high' in S and S.get('low') is not None:
        return f"`low = {S['low']}`（层 {S['level'][S['low']]}），`high = {S['high']}`（层 {S['level'][S['high']]}）：先对齐层级，再一起往上"
    return '`f[x][j]` = 节点 `x` 往上第 `2^j` 个祖先；路径边数 `d`，答案 `2^(d-1)`，`d = 0` 时答案 `0`'


CONFIG = dict(
    num=3559, title='给边赋权值的方案数 II', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='倍增 LCA + 快速幂 2^(d-1)',
    tags=['链表树与回溯', '难度分 2146'],
    code='''
class Solution(object):
    def assignEdgeWeights(self, edges, queries):
        
        n = len(edges) + 1
        g = [[] for _ in range(n + 1)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        f = [[] for _ in range(n + 1)]
        level = [None] * (n + 1)

        def dfs(now, fa, f, depth):
            level[now] = depth
            if fa is not None:
                f[now].append(fa)
                p = fa
                while len(f[p]) >= len(f[now]):
                    f[now].append(f[p][len(f[now]) - 1])
                    p = f[now][-1]
            
            for nxt in g[now]:
                if nxt != fa:
                    dfs(nxt, now, f, depth + 1)

        def get_lca(x, y):
            if level[x] > level[y]:
                low, high = x, y
            else:
                low, high = y, x
            
            p = len(f[low]) - 1
            while level[low] != level[high]:
                while p >= len(f[low]) or level[f[low][p]] < level[high]:
                    p -= 1
                low = f[low][p]

            p = len(f[low]) - 1
            while low != high:
                while p >= len(f[low]) or (p > 0 and f[low][p] == f[high][p]):
                    p -= 1
                low = f[low][p]
                high = f[high][p]
            
            return low
        
        def quick_pow(p):
            if p == 0:
                return 1
            if p == 1:
                return 2
            
            v = quick_pow(p // 2)
            v = v * v % mod
            if p & 1:
                v = v * 2 % mod
            return v

        dfs(1, None, f, 0)
        mod = 10 ** 9 + 7
        res = []
        for x, y in queries:
            lca = get_lca(x, y)
            length = level[x] + level[y] - level[lca] - level[lca]
            if length == 0:
                res.append(0)
            else:
                res.append(quick_pow(length - 1))
        
        return res
''',
    call='Solution().assignEdgeWeights([[1, 2], [1, 3], [3, 4], [3, 5]], [[1, 4], [3, 4], [2, 5]])',
    expect=[2, 1, 4],
    views=[
        dict(type='text', fn=_formula, size=24, h=60),
        dict(_tree_view(CH, 1, _colors, '树（黄 = 正在处理的节点，绿 = 它的父亲；蓝 = 浅的那个，粉 = 深的那个）', tags=_tags), h=400),
        dict(type='table', var='f', label='f[x]：x 往上走 1、2、4…步到的节点（行 = 节点 x，第 0 行没用）', rows=list(range(6)),
             cell=56, h=300),
    ],
    watch=['now', 'fa', 'x', 'y', 'low', 'high', 'p'],
    max_steps=90,
    skip=['for x, y in edges', 'g[x].append', 'g[y].append', 'for nxt in g[now]', 'if nxt != fa', 'p = fa', 'for x, y in queries',
          'if length == 0', 'else:', 'res = []', 'mod = 10', 'p = f[now][-1]', 'p -= 1', 'f = [[] for', 'level = [None]', 'if p == 0', 'if p == 1', 'while level[low] != level[high]', 'if fa is not None'],
    captions={
        'n = len(edges) + 1': '`n = {n}` 个节点，编号 1 到 n',
        'g = [[] for': '邻接表 `g` 建好（无向边两头都存）',
        'f = [[] for': '`f[x]` 依次存 `x` 的第 1、2、4、8… 个祖先',
        'level = [None]': '`level[x]`：`x` 的深度',
        'dfs(1, None, f, 0)': '从根 `1` 出发 DFS，同时填 `level` 和 `f`',
        'level[now] = depth': '`level[{now}] = {depth}`',
        'if fa is not None': lambda S, B, ret: ('不是根：有父亲 `{}`，开始填 `f[{}]`'.format(S.fa, S.now) if S.fa is not None else '根节点没有祖先，`f[1]` 留空'),
        'f[now].append(fa)': '`f[{now}][0] = {fa}`：走 1 步 = 父亲',
        'while len(f[p]) >= len(f[now])': lambda S, B, ret: (f'`p = {S.p}` 还有第 {len(S.f[S.now])} 档祖先 → 可以继续翻倍' if len(S.f[S.p]) >= len(S.f[S.now])
                                                            else f'`p = {S.p}` 没有那么高的祖先了 → `f[{S.now}]` 填完'),
        'f[now].append(f[p][len(f[now]) - 1])': '2^j 步的祖先 `p` 再走 2^j 步：`f[{now}]` 变成 `{f[now]}`',
        'p = f[now][-1]': '`p` 换成刚加入的最远祖先 `{p}`',
        'dfs(1': '',
        'lca = get_lca(x, y)': '询问 `({x}, {y})`：先求最近公共祖先',
        'if level[x] > level[y]': lambda S, B, ret: f'`level[{S.x}] = {S.level[S.x]}`，`level[{S.y}] = {S.level[S.y]}`：分出深的 `low` 和浅的 `high`',
        'low, high = x, y': '`x` 更深：`low = {low}`，`high = {high}`',
        'low, high = y, x': '`y` 更深或同层：`low = {low}`，`high = {high}`',
 'p = len(f[low]) - 1': lambda S, B, ret: ('`low` 已经等于 `high`，不用再往上找' if S.p < 0 else f'从 `low` 最大的一档 `p = {S.p}` 开始试'),
        'while level[low] != level[high]': lambda S, B, ret: ('层级不同：`low` 还要往上' if S.level[S.low] != S.level[S.high] else '`low` 与 `high` 同一层了'),
        'while p >= len(f[low]) or level[f[low][p]] < level[high]': lambda S, B, ret: ('这一档不能用（没有这么高，或者会跳到 `high` 上方）：`p` 减小' if (S.p >= len(S.f[S.low]) or S.level[S.f[S.low][S.p]] < S.level[S.high])
                                                                                     else f'第 `{S.p}` 档合适：跳完仍不高于 `high` 的层级'),
        'p -= 1': '`p` 降到 {p}',
        'low = f[low][p]': '`low` 跳 `2^{p}` 步 → =={low}==',
        'while low != high': lambda S, B, ret: ('同层但不是同一点：一起往上找汇合处' if S.low != S.high else '`low == high`：找到最近公共祖先'),
        'while p >= len(f[low]) or (p > 0 and f[low][p] == f[high][p])': lambda S, B, ret: ('这一档不能跳（没有这么高，或者两边已汇合，会跳过头）：`p` 减小' if (S.p >= len(S.f[S.low]) or (S.p > 0 and S.f[S.low][S.p] == S.f[S.high][S.p]))
                                                                                              else f'第 `{S.p}` 档：两边祖先不同，还没汇合，可以跳'),
        'high = f[high][p]': '`high` 也跳 `2^{p}` 步 → `low = {low}`，`high = {high}`',
        'return low': '最近公共祖先 = ==`{ret}`==',
        'length = level[x]': '距离 = `{level[x]} + {level[y]} - 2 * {level[lca]}` = =={length}== 条边',
        'res.append(0)': '`x == y`：路径没有边，答案 `0`',
        'res.append(quick_pow(length - 1))': '路径 `{length}` 条边 → 答案 `2^({length} - 1)`，交给快速幂',
        'if p == 0': lambda S, B, ret: ('`2^0 = 1`：递归的底' if S.p == 0 else '`p != 0`，继续看'),
        'if p == 1': lambda S, B, ret: ('`2^1 = 2`：递归的底' if S.p == 1 else '`p != 1`，折半递归'),
        'v = quick_pow(p // 2)': '快速幂：先算 `2^({p} // 2)`',
        'v = v * v % mod': '平方：`v` = =={v}==',
        'if p & 1': lambda S, B, ret: ('`p` 是奇数：还要再乘一个 2' if S.p & 1 else '`p` 是偶数：不用再乘'),
        'v = v * 2 % mod': '再乘 2：`v` = =={v}==',
        'return v': '`2^p` = ==`{ret}`==',
        'return res': '三个询问的答案：==`{ret}`==',
    },
    cards=dict(
        one_liner='路径 d 条边，奇数代价共 2^(d-1) 种；d 用 LCA 倍增求',
        complexity='预处理 `O(n log n)`，每个询问 `O(log n)`',
        problem=['无向树，节点 `1..n`，根是 `1`；每条边权值设为 `1` 或 `2`',
                 '每个询问 `[u, v]`：`u` 到 `v` 路径总代价为==奇数==的方案数（取模）',
                 '示例：`[[1,2],[1,3],[3,4],[3,5]]`，查询 `[[1,4],[3,4],[2,5]]` → `[2,1,4]`'],
        quote='上一题的加强版……也是先计算两点之间边的数量cnt，然后计算cnt的赋值方案数。……赋值方案数为2^(cnt - 1)。需要特别注意的是，本题中的u和v可能相同，这种情况下的答案为0。',
        quote_src='—— yiduobo 题解原文',
        idea=['两点间边数 = 各自到 LCA 的距离之和：`level[x] + level[y] - 2 * level[lca]`',
              'LCA 用倍增：`f[x][j]` 是往上走 `2^j` 步的节点，DFS 时顺手填好',
              '求 LCA 分两步：先把深的拉到同一层，再从大步到小步一起往上跳',
              '`cnt` 条边的方案数 `2^(cnt-1)`，用快速幂计算'],
        summary=['预处理 `O(n log n)`，每次询问 `O(log n)`',
                 '易错：`u == v` 时没有边，答案 `0`',
                 '两点汇合时 `f[low][p] == f[high][p]` 不能跳，否则跳过头',
                 '原文已经是 Python 3 可运行的写法（用的已是 `//`），代码未改动',
                 '对比灵神：灵神用 `n.bit_length()` 开定长表，并预处理 `POW2`；这里 `f[x]` 是变长列表，按需快速幂'],
    ),
)
