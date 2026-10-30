def _lay(edges):
    n = len(edges) + 1
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)
    depth, kids, seen, q = [0] * n, {i: [] for i in range(n)}, {0}, [0]
    for x in q:
        for y in g[x]:
            if y not in seen:
                seen.add(y)
                depth[y] = depth[x] + 1
                kids[x].append(y)
                q.append(y)
    pos, cnt = {}, [0]
    def go(x):
        if not kids[x]:
            pos[x] = cnt[0]
            cnt[0] += 1
        else:
            for y in kids[x]:
                go(y)
            pos[x] = (pos[kids[x][0]] + pos[kids[x][-1]]) / 2
    go(0)
    return pos, depth, cnt[0], max(depth) + 1, kids


def _tree(cv, T, edges, box, label, fill=None, ring=None, sub=None, title=None, r=26):
    """通用树绘制：label(i)=节点内文字，fill(i)=颜色名或None，ring(i)=描边颜色名，sub(i)=节点下方小字"""
    x0, y0, x1, y1 = box
    pos, depth, w, h, kids = _lay(edges)
    if title:
        cv.text((x0 + 14, y0 + 2), title, 22, T['muted'], bold=True)
        y0 += 36
    dx = min(110, (x1 - x0 - 2 * r - 20) / max(w - 1, 1)) if w > 1 else 0
    dy = min(120, (y1 - y0 - 2 * r - 30) / max(h - 1, 1)) if h > 1 else 0
    sx = (x0 + x1) / 2 - dx * (w - 1) / 2
    P = {i: (sx + pos[i] * dx, y0 + r + 10 + depth[i] * dy) for i in pos}
    for a, b in edges:
        cv.line([P[a], P[b]], T['border'], 3)
    for i, (X, Y) in P.items():
        f = fill(i) if fill else None
        rg = ring(i) if ring else None
        cv.rect((X - r, Y - r, X + r, Y + r), fill=T[f] if f else T['panel2'], outline=T[rg] if rg else T['border'], width=5 if rg else 2, r=r)
        cv.text((X, Y), label(i), 26, T['bg'] if f else T['text'], anchor='mm', bold=True)
        cv.text((X - r - 2, Y - r - 2), i, 16, T['dim'], anchor='rb', mono=True)
        if sub and sub(i):
            cv.text((X + r + 8, Y), sub(i), 20, T['muted'], anchor='lm', bold=True)

EDGES = [[0, 1], [1, 2], [1, 3], [3, 4]]
AMT = [-2, 4, 2, -4, 6]


def _draw(cv, S, B, box, T):
    bt = S.get('bob_time')
    x = S['_inner'].get('x')
    n = len(AMT)
    def sub(i):
        if bt is not None and bt[i] < n:
            return f'bob 第{bt[i]}秒'
        return ''
    def fill(i):
        return 'orange' if (bt is not None and bt[i] < n) else None
    def ring(i):
        return 'yellow' if i == x else None
    _tree(cv, T, EDGES, box, lambda i: AMT[i], fill=fill, ring=ring, sub=sub, r=26,
          title='节点里是 amount；橙 = Bob 走过的路（标注到达时间），黄框 = 当前递归节点')


def _alice(S, B, ret):
    x, at, bt = S.x, S.alice_time, S.bob_time[S.x]
    if at < bt:
        return f'Alice 第 `{at}` 秒到 `{x}`，Bob 第 `{bt}` 秒才到（`{bt}` = n 表示不来）→ Alice 先开门，独享 `{S.amount[x]}`'
    return f'Alice 第 `{at}` 秒到 `{x}`，Bob 第 `{bt}` 秒到：Alice 不是先到，不能独享'


def _alice2(S, B, ret):
    x, at, bt = S.x, S.alice_time, S.bob_time[S.x]
    if at == bt:
        return f'两人同时（第 `{at}` 秒）到 `{x}` → 平分：`tot += {S.amount[x]} // 2`'
    return f'Bob 第 `{bt}` 秒就到过 `{x}`，门已被打开 → 不加不扣'


def _leaf(S, B, ret):
    k = len(S.g[S.x])
    if k == 1:
        return f'`{S.x}` 只有一个邻居 → ==叶子==，Alice 走到头了'
    return f'`{S.x}` 有 {k} 个邻居 → 不是叶子，继续往下走'


CONFIG = dict(
    num=2467, title='树上最大得分和路径', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='两次 DFS',
    tags=['灵神题单·链表树与回溯', '难度分 2053'],
    code='''
class Solution:
    def mostProfitablePath(self, edges: List[List[int]], bob: int, amount: List[int]) -> int:
        n = len(edges) + 1
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)  # 建树

        bob_time = [n] * n  # bobTime[x] 表示 bob 访问节点 x 的时间
        def dfs_bob(x: int, fa: int, t: int) -> bool:
            if x == 0:
                bob_time[x] = t
                return True
            for y in g[x]:
                if y != fa and dfs_bob(y, x, t + 1):
                    bob_time[x] = t  # 只有可以到达 0 才标记访问时间
                    return True
            return False
        dfs_bob(bob, -1, 0)

        g[0].append(-1)  # 防止把根节点当作叶子
        ans = -inf
        def dfs_alice(x: int, fa: int, alice_time: int, tot: int) -> None:
            if alice_time < bob_time[x]:
                tot += amount[x]
            elif alice_time == bob_time[x]:
                tot += amount[x] // 2
            if len(g[x]) == 1:  # 叶子
                nonlocal ans
                ans = max(ans, tot)  # 更新答案
                return
            for y in g[x]:
                if y != fa:
                    dfs_alice(y, x, alice_time + 1, tot)
        dfs_alice(0, -1, 0, 0)
        return ans
''',
    call='Solution().mostProfitablePath([[0,1],[1,2],[1,3],[3,4]], 3, [-2,4,2,-4,6])',
    expect=6,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='array', var='bob_time', label='bob_time（== n 表示 Bob 不经过）', cell=64, h=120),
        dict(type='calls', h=170),
    ],
    watch=['bob', ('x', lambda S: S['_inner'].get('x'), 'yellow'), ('t', lambda S: S['_inner'].get('t'), 'orange'),
           ('alice_time', lambda S: S['_inner'].get('alice_time'), 'blue'), ('tot', lambda S: S['_inner'].get('tot'), 'cyan'), ('ans', 'ans', 'green')],
    skip=['for x, y in edges', 'g[x].append(y)'],
    captions={
        'bob_time = [n] * n': '先默认 Bob 到每个点的时间是 `n`（==永远不会先到==），再 DFS 求真正的时间',
        'if x == 0:': lambda S, B, r: (f'`x = {S.x}`：走到根节点 0 了，记下到达时间 `t`' if S.x == 0 else f'`x = {S.x}`，还不是根节点 0，继续找'),
        'bob_time[x] = t  #': '这条路通到 0：`bob_time[{x}] = {t}`，Bob 第 `{t}` 秒到这里',
        'dfs_bob(y, x, t + 1)': '往邻居 `{y}` 走，时间 +1；==只有最终能到 0 的路径才会被标记==',
        'dfs_bob(bob, -1, 0)': 'Bob 从自己所在的节点出发，第 `0` 秒',
        'g[0].append(-1)': '给根节点 0 加一个假邻居 -1：这样 0 的度数至少是 2，==不会被当成叶子==',
        'if alice_time < bob_time[x]': _alice,
        'elif alice_time == bob_time[x]': _alice2,
        'tot += amount[x]': '`tot` 变成 {tot}',
        'if len(g[x]) == 1': _leaf,
        'ans = max(ans, tot)': '叶子上结算：`ans = max({B.ans}, {tot}) = {ans}`',
        'dfs_alice(y, x, alice_time + 1': 'Alice 走到孩子 `{y}`（`y != fa` 防止走回头路），时间 +1，`tot` 带下去',
        'dfs_alice(0, -1, 0, 0)': 'Alice 从根节点 0 出发，第 `0` 秒，初始得分 `0`',
        'return ans': 'Alice 的最大净得分是 `{ans}`',
    },
    cards=dict(
        one_liner='先算 Bob 到每个点的时间，再让 Alice 一路 DFS 到叶子',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树，根是 0；Alice 从 0 往叶子走，Bob 从 `bob` 往 0 走，每秒一步',
                 '先到的人开门拿分/扣分；==同时到则平分==；已被打开的门不再算分',
                 '求 Alice 走到某个叶子能得到的最大得分。示例：`bob = 3` → `6`'],
        quote='DFS，求出 bob 到 0 的路径上，Bob 经过每个点的时间 bobTime。DFS，从 0 到每个叶节点，按照题目要求累加 amount，在叶子节点上更新答案的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['第一次 DFS：从 `bob` 出发找 0，==只有能到 0 的路径才标记 `bob_time`==',
              '第二次 DFS：Alice 带着时间和得分往下走：比 Bob 早 → 全拿；同时 → 一半；晚 → 0',
              '到叶子就更新答案；给 0 加假邻居 -1，避免把根当叶子'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`bob_time` 默认 `n`：保证 Alice 对 Bob 没走过的点永远 ==alice_time < bob_time==',
                 '叶子 = 度数为 1；根节点要 `g[0].append(-1)` 才不会被误判',
                 '`amount` 是偶数，所以 `// 2` 没有精度问题'],
    ),
)
