N = 6
LEAD = [[1, 2], [1, 6], [2, 3], [2, 5], [1, 4]]
OPS = [[1, 1, 500], [2, 2, 50], [3, 1], [2, 6, 15], [3, 1]]


def _prefix(arr, i):
    r = 0
    while i > 0:
        r += arr[i]
        i -= i & -i
    return r


def _values(S):
    """当前每个 dfs 序位置上节点的真实值 = delta 的前缀和（f 是 delta 的树状数组）"""
    f = S.get('f')
    if f is None:
        return None
    return [_prefix(f, i) for i in range(1, N + 1)]


def _node_at(S):
    order = S.get('order') or []
    v = _values(S)
    return order, v


def _rng(S):
    node = S.get('node')
    sp, ep = S.get('start_pos'), S.get('end_pos')
    if node is None or sp is None or ep is None or not sp[node]:
        return None
    return sp[node], ep[node]


def _order_cells(S):
    return ['-'] + list(S.get('order') or [])


def _val_cells(S):
    v = _values(S)
    return ['-'] + (v if v is not None else [])


def _wl(S):
    r = _rng(S)
    return r[0] if r else None


def _wr(S):
    r = _rng(S)
    return r[1] if r else None


def _fmt_op(S, B, ret):
    op = S.op
    node = S.node
    sp, ep = S.start_pos[node], S.end_pos[node]
    if op[0] == 1:
        return f'操作 1：节点 `{node}` 加 `{op[2]}` → 只改 dfs 序位置 `{sp}`，即区间 `[{sp}, {sp}]`'
    if op[0] == 2:
        return f'操作 2：节点 `{node}` 的子树加 `{op[2]}` → 区间 `[{sp}, {ep}]` 整段加'
    return f'操作 3：查节点 `{node}` 的子树和 → 区间 `[{sp}, {ep}]` 的区间和'


CONFIG = dict(
    num='LCP 05', title='发 LeetCoin', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='dfs 序 + 双树状数组（区间加、区间求和）',
    tags=['常用数据结构', '链表树与回溯'],
    code='''
class Solution(object):
    def bonus(self, n, leadership, operations):

        mod = 10 ** 9 + 7
        fa = {}
        childs = {}

        for x, y in leadership:
            if x not in childs:
                childs[x] = []
            childs[x].append(y)
            fa[y] = x
        
        root = 0
        for node in range(1, n + 1):
            if node not in fa:
                root = node
                break

        def dfs(now, order, start_pos, end_pos):
            order.append(now)
            start_pos[now] = len(order)
            if now in childs:
                for next in childs[now]:
                    dfs(next, order, start_pos, end_pos)
            end_pos[now] = len(order)

        def add(arr, now, delta):
            if delta >= mod:
                delta %= mod
            elif delta < 0:
                delta = -((-delta) % mod) + mod
            while now <= n:
                arr[now] += delta
                if arr[now] >= mod:
                    arr[now] -= mod
                now += now & -now
        
        def get(arr, now):
            res = 0
            while now > 0:
                res += arr[now]
                if res >= mod:
                    res -= mod
                elif res < 0:
                    res += mod
                now -= now & -now
            return res
        
        order = []
        start_pos = [0] * (n + 1)
        end_pos = [0] * (n + 1)

        dfs(root, order, start_pos, end_pos)

        f = [0] * (n + 1)
        g = [0] * (n + 1)
        res = []

        for op in operations:
            if op[0] == 1:
                node = op[1]
                coin = op[2]
                add(f, start_pos[node], coin)
                add(g, start_pos[node], (start_pos[node] - 1) * coin)
                add(f, start_pos[node] + 1, -coin)
                add(g, start_pos[node] + 1, -start_pos[node] * coin)
            elif op[0] == 2:
                node = op[1]
                coin = op[2]
                add(f, start_pos[node], coin)
                add(g, start_pos[node], (start_pos[node] - 1) * coin)
                add(f, end_pos[node] + 1, -coin)
                add(g, end_pos[node] + 1, -end_pos[node] * coin)
            else:
                node = op[1]
                prefix_sum_f = get(f, end_pos[node]) * end_pos[node] % mod
                prefix_sum_f -= get(f, start_pos[node] - 1) * (start_pos[node] - 1) % mod
                if prefix_sum_f < 0:
                    prefix_sum_f += mod
                
                prefix_sum_g = get(g, end_pos[node]) - get(g, start_pos[node] - 1)
                if prefix_sum_g < 0:
                    prefix_sum_g += mod

                res.append(prefix_sum_f - prefix_sum_g)
                if res[-1] < 0:
                    res[-1] += mod

        return res
''',
    call=f'Solution().bonus({N}, {LEAD}, {OPS})',
    expect=[650, 665],
    skip=[50, 5, 6, 8, 9, 10, 12, 14, 15, 16, 17, 18, 21, 23, 24, 29, 30, 31, 32, 33, 34, 35, 36, 37, 40, 41, 42, 43, 44, 45, 46, 47, 48, 51, 52, 60, 63, 68, 70, 79, 80, 83, 84],
    views=[
        dict(type='array', var=_order_cells, label='dfs 序 order（位置从 1 数；框 = 当前节点的子树区间）', h=150, cell=80,
             window=(_wl, _wr)),
        dict(type='array', var=_val_cells, label='每个位置的真实值 = delta 的前缀和（树状数组 f 还原出来的）', h=150, cell=80,
             window=(_wl, _wr)),
        dict(type='array', var='f', label='f：delta 的树状数组', h=130, cell=80),
        dict(type='array', var='g', label='g：(i-1)·delta[i] 的树状数组', h=130, cell=80),
    ],
    watch=[('node', 'node', 'blue'), ('coin', 'coin', 'orange'), ('res', 'res', 'green')],
    captions={
        4: '结果对 `mod = 10^9+7` 取模',
        3: '先把 `leadership` 整理成 `childs[上级] = [下属…]`，并记 `fa`（没有上级的就是根）',
        11: '`childs[{x}]` 加入下属 `{y}`',
        20: '定义 dfs：只记==首次访问==的时间戳 `start_pos`，和子树最后一个位置 `end_pos`',
        22: '访问 `{now}`：加进 `order`，`start_pos[{now}] = {start_pos[now]}`（dfs 序里的位置，从 1 数）',
        26: lambda S, B, r: f'`{S.now}` 的子树都访问完：`end_pos[{S.now}] = {S.end_pos[S.now]}`，子树 = 区间 `[{S.start_pos[S.now]}, {S.end_pos[S.now]}]`',
        25: '递归进入下一个孩子，先把它的整棵子树编完号',
        54: '开始 dfs：以后==子树操作 = 区间操作==',
        56: '`f`：delta（差分）的树状数组，下标从 1 开始',
        57: '`g`：`(i-1) * delta[i]` 的树状数组，和 `f` 同步更新',
        58: '`res` 收集每次操作 3 的答案',
        61: '取下一个操作 `{op}`：`op[0]` 是类型（1 点加 / 2 子树加 / 3 查子树和）',
        62: _fmt_op,
        69: _fmt_op,
        76: _fmt_op,
        64: '`f[{start_pos[node]}] += {coin}`：delta 差分，从位置 `{start_pos[node]}` 起所有值 `+{coin}`',
        65: '`g` 同步加 `(位置-1)·coin = {(start_pos[node]-1)*coin}`',
        66: '`f[{start_pos[node]+1}] -= {coin}`：从下一位起取消，所以只影响一个点',
        67: '`g` 同步减 `位置·coin = {start_pos[node]*coin}`',
        71: '`f[{start_pos[node]}] += {coin}`：子树起点处整体 `+{coin}`',
        72: '`g` 同步加 `(位置-1)·coin = {(start_pos[node]-1)*coin}`',
        73: '`f[{end_pos[node]+1}] -= {coin}`：子树结束后取消',
        74: '`g` 同步减 `末位·coin = {end_pos[node]*coin}`',
        77: '`get(f, 末位={end_pos[node]})` × 末位 = ==前缀 [1, {end_pos[node]}] 的 f 部分== = `{prefix_sum_f}`',
        78: '再减去前缀 `[1, {start_pos[node]-1}]` 的 f 部分 → `prefix_sum_f = {prefix_sum_f}`',
        82: '`g` 部分：两个前缀之差 = `{prefix_sum_g}`',
        86: '区间和 = `prefix_sum_f − prefix_sum_g = {prefix_sum_f} − {prefix_sum_g}`，记入答案（取模后可能出现负数）',
        87: '`res[-1] = {res[-1]}`：负数要补 `mod`',
        88: '补 `mod` → `res[-1] = {res[-1]}`',
        90: '全部操作处理完，返回 `{ret}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='子树 = dfs 序上的一段区间：区间加、区间求和',
        complexity='时间 `O((n+q)·log n)`，空间 `O(n)`',
        problem=['一棵上下级树，三种操作：节点加 `coin`、整棵子树加 `coin`、查子树节点值之和',
                 '返回每次操作 3 的结果（对 `10^9+7` 取模）',
                 '本视频：`n = 6`，5 次操作 → `[650, 665]`'],
        quote='受到这个启发，就想到使用dfs序来将树结构转化为线性结构。……对于子树的操作就变成了区间操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['dfs 得到首次访问的位置 `start_pos` 和子树末尾 `end_pos`',
              '区间加用差分 delta；区间求和要 `Σ value`，拆成 `suf·x − Σ(i-1)·delta[i]`',
              '两个树状数组：`f` 维护 delta，`g` 维护 `(i-1)·delta[i]`'],
        summary=['时间 `O((n+q)·log n)`，空间 `O(n)`',
                 '易错：操作 1 是区间 `[x, x]`，要在 `x` 加、`x+1` 减',
                 '易错：`g` 里存的是 `(位置 - 1) * delta`，查询用 `前缀 × 下标 - g 前缀`',
                 '取模：减法后要补回 `mod`，不要出现负数',
                 '此为「区间加 + 区间求和」的树状数组模板'],
    ),
)
