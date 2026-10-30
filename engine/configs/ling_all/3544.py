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

EDGES = [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5], [2, 6]]
NUMS = [4, -8, -6, 3, 7, -2, 5]
K = 2
N = 7
G = [[] for _ in range(N)]
for _a, _b in EDGES:
    G[_a].append(_b)
    G[_b].append(_a)


def _order():
    out, par = [], {}

    def go(x, fa):
        out.append(x)
        par[x] = fa
        for y in G[x]:
            if y != fa:
                go(y, x)
    go(0, -1)
    return out, par


def _solve():
    res, f = {}, []

    def dfs(x, fa):
        f.append([0, 0])
        s = NUMS[x]
        a0 = a1 = 0
        for y in G[x]:
            if y == fa:
                continue
            sy, y0, y1 = dfs(y, x)
            s += sy
            a0 += y0
            a1 += y1
        r0, r1 = f.pop()
        i0, i1 = r1 - s * 2, r0 + s * 2
        e0, e1 = max(a0, i0), max(a1, i1)
        if len(f) >= K:
            f[-K][0] += e0
            f[-K][1] += e1
        res[x] = (s, e0, e1)
        return s, e0, e1
    dfs(0, -1)
    return res


SOL = _solve()


def _draw(cv, S, B, box, T):
    inner = S['_inner']
    cur = inner.get('x')
    order, par = _order()
    path, done = set(), set()
    if cur is not None:
        v = cur
        while v != -1:
            path.add(v)
            v = par[v]
        done = {v for v in order[:order.index(cur)] if v not in path}
        if S['_line'] == 43:
            done.add(cur)
    fills, rings, notes = {}, {}, {}
    for v in done:
        s, a, b = SOL[v]
        notes[v] = (f'{a}/{b}', T['orange'])
        fills[v] = (28, 84, 52)
    for v in path:
        rings[v] = (150, 120, 40)
    if cur is not None:
        rings[cur] = T['yellow']
    labels = {v: f'{v}' for v in range(N)}
    _dtree(cv, T, box, N, EDGES, '树（点上数字 = nums[i]；橙字 = 已返回的 res0/res1）', fills, rings, notes, labels=labels)
    x0, y0, x1, y1 = box
    # nums 标在节点旁
    xs, depth, _, leaves, levels = _tlay(N, EDGES, 0)
    w = x1 - x0 - 50
    top = y0 + 44
    R = max(16, min(28, w / leaves / 2.3))
    dy = min(110, (y1 - top - 2 * R - 34) / max(1, levels - 1))
    for v in range(N):
        X, Y = x0 + 25 + (xs[v] + 0.5) * w / leaves, top + depth[v] * dy + R
        cv.text((X - R - 4, Y - R + 2), str(NUMS[v]), 20, T['cyan'], anchor='rm', bold=True, mono=True)


CONFIG = dict(
    num=3544, title='子树反转和', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='树形 DP · 刷表法 O(n)',
    tags=['灵神题单·动态规划', '难度分 2545'],
    code='''
max = lambda a, b: b if b > a else a  # 手写 max 效率更高

class Solution:
    def subtreeInversionSum(self, edges: List[List[int]], nums: List[int], k: int) -> int:
        n = len(nums)
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        f = []

        def dfs(x: int, fa: int) -> Tuple[int, int, int]:
            f.append([0, 0])  # 用于刷表

            s = nums[x]  # 子树和
            not_inv0 = not_inv1 = 0  # 不反转 x 时的额外增量（0 表示上面反转了偶数次，1 表示上面反转了奇数次）
            for y in g[x]:
                if y == fa:
                    continue
                sy, y0, y1 = dfs(y, x)
                s += sy
                # 不反转 x，反转次数的奇偶性不变
                not_inv0 += y0
                not_inv1 += y1

            sub_res0, sub_res1 = f.pop()  # 被刷表后的结果

            # 反转 x
            # x 上面反转了偶数次，反转 x 会带来 -2 倍子树和的增量，且对于 x 的 k 级后代来说，上面反转了奇数次（所以是 sub_res1）
            inv0 = sub_res1 - s * 2
            # x 上面反转了奇数次，反转 x 会带来 2 倍子树和的增量，且对于 x 的 k 级后代来说，上面反转了偶数次（所以是 sub_res0）
            inv1 = sub_res0 + s * 2

            res0 = max(not_inv0, inv0)
            res1 = max(not_inv1, inv1)

            # 刷表法：更新 x 的 k 级祖先的状态
            if len(f) >= k:
                f[-k][0] += res0
                f[-k][1] += res1

            return s, res0, res1

        s, res0, _ = dfs(0, -1)
        return s + res0  # 对于根节点来说，上面一定反转了偶数次（0 次）
''',
    call='Solution().subtreeInversionSum([[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]], [4,-8,-6,3,7,-2,5], 2)',
    expect=27,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='stack', var='f', label='f（刷表缓冲：每层 [偶, 奇] 累计，栈顶 = 当前点）', fmt=lambda p: f'[{p[0]}, {p[1]}]', h=120),
        dict(type='calls', h=170),
    ],
    watch=[('x', lambda S: S['_inner'].get('x'), 'yellow'), ('s', lambda S: S['_inner'].get('s'), 'cyan'),
           ('not_inv0', lambda S: S['_inner'].get('not_inv0')), ('not_inv1', lambda S: S['_inner'].get('not_inv1')),
           ('res0', lambda S: S['_inner'].get('res0'), 'green'), ('res1', lambda S: S['_inner'].get('res1'), 'green')],
    skip=['for x, y in edges', 'g[x].append(y)', 'g[y].append(x)', 'if y == fa', 'continue', 'for y in g[x]', 'n = len(nums)', 'g = [[] for'],
    captions={
        'f = []': '`f`：刷表用的栈，每进入一个点压一格 `[偶, 奇]`',
        'f.append([0, 0])': '进入 `{x}`：压一格，等它的 `k` 级后代来「刷表」',
        's = nums[x]': '子树和 `s` 先从自己 `{s}` 开始',
        'not_inv0 = not_inv1': '不反转 `x` 的增量先清零',
        'sy, y0, y1 = dfs(y, x)': '去儿子 `{y}`：拿回它的子树和与两种奇偶下的最大增量',
        's += sy': '子树和 `s = {s}`',
        'not_inv0 += y0': '不反转 `x` → 儿子上面的奇偶性不变：累加 `y0`，`not_inv0 = {not_inv0}`',
        'not_inv1 += y1': '同理累加 `y1`，`not_inv1 = {not_inv1}`',
        'sub_res0, sub_res1 = f.pop()': '弹出 `x` 这格：`k` 级后代已刷进来 `[{sub_res0}, {sub_res1}]`',
        'inv0 = sub_res1': '上面偶数次，反转 `x`：立刻 `-2s = {-2 * s}`，后代奇数次 → `inv0 = {inv0}`',
        'inv1 = sub_res0': '上面奇数次，反转 `x`：立刻 `+2s = {2 * s}`，后代偶数次 → `inv1 = {inv1}`',
        'res0 = max': '偶数次：`max(不反转 {not_inv0}, 反转 {inv0})` = ==`{res0}`==',
        'res1 = max': '奇数次：`max(不反转 {not_inv1}, 反转 {inv1})` = ==`{res1}`==',
        'if len(f) >= k': lambda S, B, r: (f'栈里还有 `{len(S.f)}` 层 ≥ `k = {S.k}`：`x` 有 k 级祖先' if len(S.f) >= S.k else f'栈里只有 `{len(S.f)}` 层 < `k = {S.k}`：没有 k 级祖先'),
        'f[-k][0] += res0': '刷表：把 `res0 = {res0}` 加到 `k` 级祖先那格的偶数位',
        'f[-k][1] += res1': '刷表：`res1 = {res1}` 加到奇数位',
        'return s, res0, res1': '`{x}` 返回：子树和 `{s}`，增量 `{res0}` / `{res1}`',
        's, res0, _ = dfs(0, -1)': '从根 `0` 出发 dfs：根上面没有反转（偶数次）',
        'return s + res0': '总和 `{s}` + 最大增量 `{res0}` = ==`{ret}`==',
    },
    max_steps=64,
    cards=dict(
        one_liner='先算原总和，再算反转能「多出」多少',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['以 `0` 为根的树，反转一个点 = 它整棵子树的值 ×(−1)',
                 '两个反转点若互为祖先后代，距离必须 `≥ k`',
                 '求反转后点权和的最大值',
                 '示例：`k = 2`，`nums = [4,-8,-6,3,7,-2,5]` → `27`'],
        quote='反转 x，问题变成 x 的 k 级后代的最大增量。……站在 x 的视角计算，很不方便；但如果站在 z 的视角，去更新 x，就很好算了（每个 z 至多有一个 k 级祖先 x）。',
        quote_src='—— 灵茶山艾府题解（树上刷表法）',
        idea=['算增量：`dfs(x)` 返回子树和 `s` 与上面反转偶/奇次时的最大增量 `res0/res1`',
              '不反转 `x`：直接累加儿子；反转 `x`：增量 `∓2s`，再加上 `x` 的 ==k 级后代==',
              '用栈 `f` 刷表：每个点算完后，把结果加到它的 k 级祖先那一格'],
        summary=['时间 `O(n)`，空间 `O(n)`；方法一「多维 DP」是 `O(nk)`',
                 '反转 `x` 不能从儿子转移（儿子可能也反转，违反距离 `k`），所以要用 k 级后代',
                 '`len(f) >= k` 才有 k 级祖先；根上面反转了 0 次（偶数）',
                 '写法一（记忆化 `dfs(x, cd, mul)`）和写法二（递推）本视频不演示']
    ),
)
