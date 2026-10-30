# 示例 2：roads 与 seats（布局用的静态树，和 call 保持一致）
ROADS = [[3, 1], [3, 2], [1, 0], [0, 4], [0, 5], [4, 6]]
SEATS = 2
G = {i: [] for i in range(len(ROADS) + 1)}
for _x, _y in ROADS:
    G[_x].append(_y)
    G[_y].append(_x)
CH, PAR = {}, {0: -1}


def _build(x, fa):
    CH[x] = [y for y in G[x] if y != fa]
    for y in CH[x]:
        PAR[y] = x
        _build(y, x)


_build(0, -1)
POS, _leaf = {}, [0]


def _place(x, d):
    if not CH[x]:
        POS[x] = (_leaf[0], d)
        _leaf[0] += 1
    else:
        for y in CH[x]:
            _place(y, d + 1)
        POS[x] = (sum(POS[y][0] for y in CH[x]) / len(CH[x]), d)


_place(0, 0)
NLEAF = _leaf[0]
MAXD = max(d for _, d in POS.values()) + 1
SIZE, PRE = {}, {}


def _meta(x):
    PRE[x] = len(PRE)
    SIZE[x] = 1 + sum(_meta(y) for y in CH[x])
    return SIZE[x]


_meta(0)


def track(fn):
    return fn if callable(fn) else (lambda S, B, r: fn)


def _done(n, cur, line, y, same):
    """dfs(n) 是否已经返回（由当前所在节点、行号和循环变量 y 推出）"""
    if cur is None:
        return line is not None and line >= 19   # 全部返回
    if n == cur:
        return line == 17
    anc, a = [], PAR[n]
    while a >= 0:
        anc.append(a)
        a = PAR[a]
    if cur in anc:                       # n 在 cur 的子树里
        if line >= 14:
            return True
        c = ([n] + anc)[anc.index(cur)]   # cur 的哪个孩子管着 n
        if y not in CH[cur]:
            return False
        i, j = CH[cur].index(c), CH[cur].index(y)
        return i < j or (i == j and line == 11 and same)
    a = cur
    while a >= 0:
        if a == n:                       # n 是 cur 的祖先，还没返回
            return False
        a = PAR[a]
    return PRE[n] < PRE[cur]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '城市树（首都 0 为根；黄 = 递归路径，蓝 = 当前节点，绿 = 已算出子树大小）', 22, T['muted'], bold=True)
    sp = min(130, (x1 - x0 - 80) / max(1, NLEAF))
    dy = min(100, (y1 - y0 - 120) / max(1, MAXD - 1))
    sx = x0 + 40 + ((x1 - x0 - 80) - sp * (NLEAF - 1)) / 2
    rad = 25

    def P(n):
        return sx + POS[n][0] * sp, y0 + 80 + POS[n][1] * dy
    cur = S['_inner'].get('x') if 'x' in S['_inner'] else None
    line = S.get('_line')
    same = bool(B) and B['_inner'].get('y') == S['_inner'].get('y') and B['_inner'].get('x') == cur
    DONE = {n: SIZE[n] for n in CH if _done(n, cur, line, S['_inner'].get('y'), same)}
    path = set()
    a = cur
    while a is not None and a >= 0:
        path.add(a)
        a = PAR[a]
    for n in CH:
        for c in CH[n]:
            cv.line([P(n), P(c)], T['border'], 3)
            if c in DONE:
                cost = (DONE[c] - 1) // SEATS + 1
                mx, my = (P(n)[0] + P(c)[0]) / 2, (P(n)[1] + P(c)[1]) / 2
                t = f'+{cost} 升'
                w = cv.tlen(t, 19, bold=True) + 14
                cv.rect((mx - w / 2, my - 14, mx + w / 2, my + 14), fill=T['panel'], outline=T['orange'], width=2, r=8)
                cv.text((mx, my), t, 19, T['orange'], anchor='mm', bold=True)
    for n in CH:
        X, Y = P(n)
        fill = T['green'] if n in DONE else T['panel2']
        outline = T['yellow'] if n in path else T['border']
        if n == cur:
            fill, outline = T['blue'], T['blue']
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=outline, width=4)
        cv.text((X, Y), n, 26, T['bg'] if n in DONE or n == cur else T['text'], anchor='mm', bold=True)
        if n in DONE:
            cv.text((X + rad + 8, Y), f'size={DONE[n]}', 19, T['green'], anchor='lm', bold=True)


CONFIG = dict(
    num=2477, title='到达首都的最少油耗', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='自底向上 DFS · 贡献法',
    tags=['贪心与思维', '链表树与回溯', '难度分 2012'],
    code='''
class Solution:
    def minimumFuelCost(self, roads: List[List[int]], seats: int) -> int:
        g = [[] for _ in range(len(roads) + 1)]
        for x, y in roads:
            g[x].append(y)  # 记录每个点的邻居
            g[y].append(x)

        ans = 0
        def dfs(x: int, fa: int) -> int:
            size = 1
            for y in g[x]:
                if y != fa:  # 递归子节点，不能递归父节点
                    size += dfs(y, x)  # 统计子树大小
            if x:  # x 不是根节点
                nonlocal ans
                ans += (size - 1) // seats + 1  # ceil(size/seats)
            return size
        dfs(0, -1)
        return ans
''',
    call='Solution().minimumFuelCost([[3,1],[3,2],[1,0],[0,4],[0,5],[4,6]], 2)',
    expect=7,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='calls', h=190),
    ],
    watch=[('x', lambda S: S['_inner'].get('x'), 'blue'), ('size', lambda S: S['_inner'].get('size'), 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'g = [[] for': '建邻接表 `g`：城市 `0..n-1`，每个城市一个邻居列表',
        'g[x].append(y)': '无向边 `{x}—{y}`：`g[{x}]` 记下 `{y}`，下一行再让 `g[{y}]` 记下 `{x}`（两个方向都要记）',
        'ans = 0': '`ans` 累计所有「边」上的油耗',
        'size = 1': track(lambda S, B, r: f'进入节点 `{S.x}`：子树大小先算上它自己，`size = 1`'),
        'for y in g[x]': track(lambda S, B, r: (f'枚举 `{S.x}` 的邻居 `y = {S.y}`' if S['_inner'].get('y') is not None and B['_inner'].get('y') != S['_inner'].get('y') or B['_inner'].get('y') is None else f'`{S.x}` 的邻居都看完了')),
        'if y != fa': track(lambda S, B, r: (f'`{S.y}` 是父节点 `fa = {S.fa}` → 不能往回走，跳过' if S.y == S.fa else f'`{S.y}` 是 `{S.x}` 的子节点 → 递归进去，统计它的子树大小')),
        'size += dfs': track(lambda S, B, r: f'递归子节点 `{S.y}`：它会把自己子树的大小返回来，加到 `size` 上'),
        'if x:': track(lambda S, B, r: (f'`{S.x}` 不是首都 → 这个子树的 `{S.size}` 个代表要从 `{S.x}` 走到父亲' if S.x else '`x = 0` 是首都，没有父亲，不用再往上走')),
        'ans += ': track(lambda S, B, r: f'这条边：`{S.size}` 个人，每车 `{S.seats}` 座 → 至少 `ceil({S.size}/{S.seats})` = `(size−1)//seats+1` = =={(S.size - 1) // S.seats + 1}== 辆车 → `ans = {B.ans} + {S.ans - B.ans}` = =={S.ans}=='),
        'return size': track(lambda S, B, r: f'子树 `{S.x}` 的大小 `{r}` 返回给父亲，父亲的 `size` 会加上它'),
        'dfs(0, -1)': '从首都 0 出发，`fa = -1` 表示没有父节点',
        'return ans': '每条边的油耗之和：`{ans}` 升',
    },
    skip=['nonlocal ans', 'g[y].append(x)', 'size += dfs'],
    max_steps=60,
    cards=dict(
        one_liner='每条边上要几辆车，取决于边下面的子树有几个人',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 个城市组成一棵树，0 号是首都，每个城市一名代表',
                 '每个城市有一辆 `seats` 座的车，代表们可以换乘，相邻城市一辆车耗 1 升',
                 '求所有代表到达首都的最少油耗',
                 '本视频：`roads=[[3,1],[3,2],[1,0],[0,4],[0,5],[4,6]]`，`seats=2` → `7`'],
        quote='ans += (size - 1) // seats + 1  # ceil(size/seats)',
        quote_src='—— 灵茶山艾府题解代码',
        idea=['换乘免费，所以每条边上的人都先拼满车：边 `x→父` 上走过 `size` 个人',
              '这条边至少要 `ceil(size / seats)` 辆车，每辆车耗 1 升',
              '把所有边的车数相加 = 答案：==贡献法==（和 979 同类）',
              '`size` 就是以 `x` 为根的子树大小，自底向上 DFS 统计'],
        result='运行结束，返回 `7`：六条边的油耗相加',
        summary=['时间 `O(n)`，空间 `O(n)`：每个节点访问一次，递归栈最深 `O(n)`',
                 '`dfs(y, x)`：用 `fa` 避免走回父节点；`if x:` 排除首都（它没有往上的边）',
                 '`(size - 1) // seats + 1` 是整数上取整，不要写成 `size // seats`',
                 '同类：979 在二叉树中分配硬币（也是数每条边的贡献）'],
    ),
)
