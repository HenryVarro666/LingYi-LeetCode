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



def _draw(cv, S, B, box, T):
    inner = S['_inner']
    cur = inner.get('now')
    in_dp = 'rev' in inner
    s = S.get('s')
    f = S.get('f')
    anc = S.get('k_level_anc')
    kids = S.get('k_level_childs')
    fills, rings, notes = {}, {}, {}
    if cur is not None:
        rings[cur] = T['yellow']
    if in_dp:
        if kids and cur is not None:
            for v in kids[cur]:
                fills[v] = (70, 52, 110)
        if f:
            for v in range(N):
                a, b = f[v]
                if a is not None or b is not None:
                    notes[v] = (f"{'?' if a is None else a}|{'?' if b is None else b}", T['orange'])
    else:
        if s:
            for v in range(N):
                if s[v]:
                    notes[v] = (f's={s[v]}', T['cyan'])
        if anc and cur is not None and anc[cur] is not None:
            rings[anc[cur]] = T['purple']
    _dtree(cv, T, box, N, EDGES, '树（左上 = nums；橙 = f[点][0]|f[点][1]；紫 = k 层后代）' if in_dp else '树（左上 = nums；蓝字 = 子树和 s；紫圈 = k 层祖先）',
           fills, rings, notes, labels={v: f'{v}' for v in range(N)})
    x0, y0, x1, y1 = box
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
    author='yiduobo', technique='树形 DP · 只在可反转处跳到 k 层后代',
    tags=['灵神题单·动态规划', '难度分 2545'],
    code='''
class Solution(object):
    def subtreeInversionSum(self, edges, nums, k):
        
        n = len(edges) + 1
        g = [[] for _ in range(n)]
        fa = [None] * n
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        k_level_anc = [None] * n
        last = {}
        s = [0] * n

        def dfs(now, pre, depth):
            v = nums[now]
            if depth >= k:
                k_level_anc[now] = last[depth - k]
            last[depth] = now
            fa[now] = pre

            for nxt in g[now]:
                if nxt != pre:
                    dfs(nxt, now, depth + 1)
                    v += s[nxt]
            s[now] = v
        
        dfs(0, None, 0)
        
        k_level_childs = [[] for _ in range(n)]
        for index in range(n):
            if k_level_anc[index] is not None:
                k_level_childs[k_level_anc[index]].append(index)
        

        f = [[None] * 2 for _ in range(n)]
        def calc(now, rev, f):
            if f[now][rev] is None:
                f[now][rev] = nums[now]
                if rev == 1:
                    f[now][rev] = -nums[now]
                
                for nxt in g[now]:
                    if nxt != fa[now]:
                        f[now][rev] += calc(nxt, rev, f)
                

                x = s[now]
                v = 0
                for k_nxt in k_level_childs[now]:
                    x -= s[k_nxt]
                    v += calc(k_nxt, rev ^ 1, f)
                
                if rev == 0:
                    x = -x
                
                f[now][rev] = max(f[now][rev], x + v)
            
            return f[now][rev]
        
        return calc(0, 0, f)
''',
    call='Solution().subtreeInversionSum([[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]], [4,-8,-6,3,7,-2,5], 2)',
    expect=27,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='calls', h=200, hide=('f', 'edges', 'nums')),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'yellow'), ('rev', lambda S: S['_inner'].get('rev'), 'purple'),
           ('x', lambda S: S['_inner'].get('x'), 'cyan'), ('v', lambda S: S['_inner'].get('v'), 'pink'),
           ('f[now][rev]', lambda S: S['f'][S['_inner']['now']][S['_inner']['rev']] if 'rev' in S['_inner'] else None, 'green')],
    skip=['for x, y in edges', 'g[x].append(y)', 'g[y].append(x)', 'for nxt in g[now]', 'if nxt != pre', 'if nxt != fa[now]', 'n = len(edges)', 'g = [[] for',
          'fa = [None]', 'last = {}', 'k_level_childs = [[]', 'for index in range(n)', 'f = [[None]',
          'fa[now] = pre', 'last[depth] = now', 'if depth >= k', 'dfs(nxt, now', 'v += s[nxt]', 'if k_level_anc[index] is not None',
          'v = 0', 'for k_nxt in', 'if rev == 1'],
    captions={
        'k_level_anc = [None]': '`k_level_anc[i]`：往上数 `k` 层的祖先，先全空',
        's = [0] * n': '`s[i]`：以 `i` 为根的子树和',
        'v = nums[now]': '进入 `{now}`（深度 `{depth}`）：`v` 从自己 `{v}` 开始',
        'if depth >= k': lambda S, B, r: (f'深度 `{S.depth} ≥ k = {S.k}`：上面有 k 层祖先' if S.depth >= S.k else f'深度 `{S.depth} < k = {S.k}`：没有 k 层祖先'),
        'k_level_anc[now] = last': '`last[{depth - k}]` 是最近访问的深度 `{depth - k}` 的点 = `{now}` 的 k 层祖先 → `{k_level_anc[now]}`',
        'last[depth] = now': '记下深度 `{depth}` 最近访问的是 `{now}`',
        'fa[now] = pre': '`fa[{now}] = {pre}`',
        'dfs(nxt, now, depth + 1)': '去儿子 `{nxt}`',
        'v += s[nxt]': '子树和加上儿子的 `s[{nxt}] = {s[nxt]}` → `v = {v}`',
        's[now] = v': '`s[{now}] = {v}`：子树和算完',
        'dfs(0, None, 0)': '先 dfs 一趟：算子树和 `s`、k 层祖先',
        'k_level_childs[k_level_anc[index]]': '把 `{index}` 登记为 `{k_level_anc[index]}` 的 k 层后代',
        'return calc(0, 0, f)': lambda S, B, ret: ('从根 `0`、没有被反转（`rev = 0`）开始 `calc`' if ret is None else f'答案 `{ret}`'),
        'if f[now][rev] is None': lambda S, B, r: (f"`f[{S.now}][{S.rev}]` 没算过 → 现在算" if S.f[S.now][S.rev] is None else f"`f[{S.now}][{S.rev}]` 已有 `{S.f[S.now][S.rev]}`，直接返回（记忆化）"),
        'f[now][rev] = nums[now]': '不反转 `{now}`：先取自己的值 `{nums[now]}`',
        'f[now][rev] = -nums[now]': '`rev = 1`：上面反转过，自己变成 `{-nums[now]}`',
        'if rev == 1': lambda S, B, r: ('`rev = 1`：上面反转了奇数次' if S.rev == 1 else '`rev = 0`：上面没反转'),
        'f[now][rev] += calc(nxt, rev, f)': '不反转 → 照常往下：算儿子 `{nxt}` 的 `f[{nxt}][{rev}]`，再加进来',
        'x = s[now]': '反转 `{now}`：先取整棵子树和 `{x}`',
        'v = 0': '`v` 累计 k 层后代的结果',
        'x -= s[k_nxt]': '减去 k 层后代 `{k_nxt}` 的子树和 `{s[k_nxt]}`：这些点和 `{now}` 之间不能再反转 → `x = {x}`',
        'v += calc(k_nxt, rev ^ 1, f)': '从 k 层后代 `{k_nxt}` 继续算（`rev ^ 1`：状态翻转），结果累加进 `v`',
        'if rev == 0': lambda S, B, r: ('`rev = 0`：反转后整段变号，`x = -x`' if S.rev == 0 else '`rev = 1`：再反转一次变回原值，`x` 不变'),
        'x = -x': '`x = {x}`',
        'f[now][rev] = max': '取 `max(不反转 {B.f[now][rev]}, 反转 {x} + {v})` → ==`{f[now][rev]}`==',
        'return f[now][rev]': '`f[{now}][{rev}] = {ret}`',
    },
    max_steps=66,
    cards=dict(
        one_liner='反转 now 后，往下 k−1 层都不能反转：直接用子树和一笔算掉',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['以 `0` 为根的树，反转一个点 = 它整棵子树的值 ×(−1)',
                 '被反转点往下 `k−1` 层不能再反转，更深层可以',
                 '求反转后点权和的最大值',
                 '示例：`k = 2`，`nums = [4,-8,-6,3,7,-2,5]` → `27`'],
        quote='如果翻转节点now，那么从now的下一层开始往下的k - 1层节点都不能反转，而now与这些节点的节点值之和，则可以通过以now为根节点的子树中所有节点值之和，减去以now往下k层的所有节点为根节点的子树中所有节点之和计算得到。',
        quote_src='—— yiduobo 题解原文',
        idea=['朴素 DP 要记「距上次反转的距离」，多一维 `dis`',
              '改成：反转 `now` 后直接跳到它的 ==k 层后代==，中间那些层不能动，值之和 = `s[now]` − 各 k 层后代的 `s`',
              '`f[now][rev]`：`rev` 表示上面是否反转过（反转过则这段值取负）'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`k_level_anc` 用 `last[depth-k]` 求：深度 `depth-k` 最近访问的点就是 k 层祖先',
                 '`rev = 0` 时反转 → `x = -x`；`rev = 1` 时再反转变回原值',
                 '原文为 Python 2 风格，在 Python 3 下无需修改，代码照搬']
    ),
)
