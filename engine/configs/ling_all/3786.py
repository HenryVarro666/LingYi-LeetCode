import math as _m

_PAL = ['blue', 'pink', 'green', 'orange', 'purple', 'cyan']


def _pos(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    depth, order, leaves = {0: 0}, [], [0]
    pos = {}

    def go(u, fa, d):
        kids = [v for v in adj[u] if v != fa]
        if not kids:
            pos[u] = (len(pos_leaf), d)
            pos_leaf.append(u)
            return
        for v in kids:
            go(v, u, d + 1)
        xs = [pos[v][0] for v in kids]
        pos[u] = ((min(xs) + max(xs)) / 2, d)
    pos_leaf = []
    go(0, -1, 0)
    return pos


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n, edges, group = S['n'], S['edges'], S['group']
    pos = _pos(n, edges)
    inner = S.get('_inner', {})
    cur, kid = inner.get('x'), inner.get('y')
    width = max(p[0] for p in pos.values()) + 1
    height = max(p[1] for p in pos.values()) + 1
    cw = min(170, (x1 - x0 - 100) / max(width, 1))
    rh = min(95, (y1 - y0 - 130) / max(height - 1, 1))
    ox = x0 + (x1 - x0 - cw * (width - 1)) / 2
    oy = y0 + 80
    P = {u: (ox + p[0] * cw, oy + p[1] * rh) for u, p in pos.items()}
    gs = sorted(set(group))
    col = {g: T[_PAL[i % len(_PAL)]] for i, g in enumerate(gs)}
    cv.text((x0 + 18, y0 + 4), '树（颜色 = 点权 group，黄环 = 正在处理的点，黄边 = 刚统计完的边）', 22, T['muted'], bold=True)
    for a, b in edges:
        hot = (cur is not None and kid is not None and {a, b} == {cur, kid})
        cv.line([P[a], P[b]], T['yellow'] if hot else T['border'], 7 if hot else 3)
    for u in range(n):
        px, py = P[u]
        r = 30
        if u == cur:
            cv.d.ellipse((px - r - 8, py - r - 8, px + r + 8, py + r + 8), outline=T['yellow'], width=5)
        cv.d.ellipse((px - r, py - r, px + r, py + r), fill=col[group[u]])
        cv.text((px, py), group[u], 30, T['bg'], anchor='mm', bold=True)
        cv.text((px, py + r + 6), f'#{u}', 18, T['dim'], anchor='mt', mono=True)


CONFIG = dict(
    num=3786, title='树组的交互代价总和', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='贡献法：枚举每条边 + 子树点权计数',
    tags=['灵神题单·贪心与思维', '灵神题单·链表树与回溯'],
    code='''
class Solution:
    def interactionCosts(self, n: int, edges: List[List[int]], group: List[int]) -> int:
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        total_cnt = Counter(group)
        ans = 0

        def dfs(x: int, fa: int) -> Dict[int, int]:
            nonlocal ans
            cnt_x = defaultdict(int)
            cnt_x[group[x]] = 1
            for y in g[x]:
                if y == fa:
                    continue
                cnt_y = dfs(y, x)
                for i, c in cnt_y.items():
                    ans += c * (total_cnt[i] - c)
                    cnt_x[i] += c
            return cnt_x

        dfs(0, -1)
        return ans
''',
    call='Solution().interactionCosts(5, [[0,1],[0,2],[1,3],[1,4]], [1,2,1,1,2])',
    expect=7,
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='map', var='total_cnt', h=110, label='total_cnt：整棵树每种点权的个数'),
        dict(type='map', var=lambda S: dict(S['_inner'].get('cnt_x', {})) if S.get('_inner') else {}, h=110, label='cnt_x：当前点子树里每种点权的个数'),
        dict(type='calls', h=200),
    ],
    watch=[('ans', 'ans', 'green'), 'x', 'y'],
    skip=['g = [[]', 'for x, y in edges', 'g[x].append(y)', 'g[y].append(x)', 'nonlocal ans', 'continue', 'cnt_x = defaultdict'],
    max_steps=75,
    captions={
        'total_cnt = Counter': '先统计整棵树每种点权的个数 `total_cnt = {dict(total_cnt)}`，后面要用它算「另一侧」',
        'ans = 0': '`ans` 累加每条边的贡献',
        'cnt_x[group[x]] = 1': '点 `{x}` 的点权是 `{group[x]}`，它自己这棵（子）树里该点权出现 1 次',
        'for y in g[x]': lambda S, B, r: (f'`x = {S.x}` 的邻居都看完了' if 'y' in B and 'x' in B and B.x == S.x and B.y == S.y else f'看邻居 `y = {S.y}`'),
        'if y == fa': lambda S, B, r: (f'`y = {S.y}` 是父节点，跳过，避免走回头路' if S.y == S.fa else f'`y = {S.y}` 不是父节点 → 是子节点，递归下去'),
        'cnt_y = dfs(y, x)': '递归得到子树 `{y}` 里各点权的个数：`cnt_y = {dict(cnt_y)}`',
        'for i, c in cnt_y.items()': lambda S, B, r: (f'边 `{S.x}-{S.y}` 的点权都枚举完了' if 'i' in B and B.i == S.i and B.c == S.c else f'切断边 `{S.x}-{S.y}`：枚举点权 `i = {S.i}`，子树一侧有 `c = {S.c}` 个'),
        'ans += c': '边 `{x}-{y}` 的贡献：点权 {i} 的点对 = `{c} × (total_cnt[{i}] − {c})` = `{c} × {total_cnt[i] - c}`（另一侧个数）→ `ans` = =={ans}==',
        'cnt_x[i] += c': '把子树的计数并进 `cnt_x`：`cnt_x[{i}]` = {cnt_x[i]}',
        'return cnt_x': '点 `{x}` 的子树统计完，把 `cnt_x = {dict(cnt_x)}` 交给父节点',
        'dfs(0, -1)': '从 0 号点出发 DFS，`fa = -1` 表示没有父节点',
        'return ans': '每条边的贡献加完 → 返回 `{ans}`',
    },
    cards=dict(
        one_liner='不去数点对，而是数每条边被多少个同点权点对经过',
        complexity='时间 `O(nU)`，空间 `O(nU)`；`U = max(group) ≤ 20`',
        problem=['一棵 `n` 个点的树，每个点有点权 `group[i]`',
                 '点权相同的一对点，交互代价 = 两点路径上的边数；求所有这样点对的代价之和',
                 '本视频：`n=5`，`group=[1,2,1,1,2]` → `7`'],
        quote='考虑每条边 x-y 对答案的贡献，问题变成：有多少个相同点权的点对，之间的最短路径经过 x-y？……根据乘法原理，有 a_i·b_i 个点权都为 i 的点对。',
        quote_src='—— 灵茶山艾府题解',
        idea=['提示：要的是所有相同点权组的代价总和（不是分组算），通常用贡献法',
              '切断一条边，树分成 A、B 两块；点权 `i` 在两块里各有 `a_i`、`b_i` 个，经过这条边的点对有 `a_i·b_i` 个',
              '先统计 `total_cnt`，DFS 求子树计数 `a`，另一侧 `b = total − a`'],
        after=[dict(heading='另一种写法', lines=[
            '写法二：把「枚举点权 `target`」写在 DFS 外面，DFS 只返回一个整数，空间 `O(n)`',
            '虚树做法：与 `U` 无关，时间 `O(n log n)`，需要最近公共祖先'])],
        summary=['时间 `O(nU)`，空间 `O(nU)`（递归栈里每层一个计数表）',
                 '易错点：另一侧个数 `b = total_cnt[i] − c`，别忘了用整棵树的计数相减',
                 '`if y == fa: continue` 防止 DFS 走回父节点',
                 '同类题：§5.5 贡献法专题（907、2104、2281）'],
    ),
)
