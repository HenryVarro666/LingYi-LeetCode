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

E1 = [[0, 1], [0, 2], [2, 3], [2, 4]]
E2 = [[0, 1], [0, 2], [1, 3], [1, 4]]


def _pre(edges):
    pos, depth, w, h, kids = _lay(edges)
    out = []
    def go(x):
        out.append(x)
        for y in kids[x]:
            go(y)
    go(0)
    return out, depth


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    inner = S['_inner']
    x = inner.get('x')
    if 'edges' in S:
        active = 1 if S['edges'] is S.get('edges1') else 2
    elif 'ans' in S:
        active = 1
    else:
        active = 0
    done2 = 'cnt2' in S and active != 2
    done1 = 'cnt1' in S and active != 1 and 'ans' in S
    ans = S.get('ans')
    mid = (x0 + x1) / 2
    for t, (E, bx, name) in enumerate(((E1, (x0, x0 + (x1 - x0) / 2 - 6), '第一棵树 edges1'), (E2, (mid + 6, x1), '第二棵树 edges2')), 1):
        order, depth = _pre(E)
        if active == t and x is not None and x in order:
            seen = set(order[:order.index(x) + 1])
        elif (t == 2 and done2) or (t == 1 and done1):
            seen = set(order)
        else:
            seen = set()
        def fill(i, depth=depth, seen=seen):
            return ('blue' if depth[i] % 2 == 0 else 'pink') if i in seen else None
        def ring(i, t=t):
            return 'yellow' if active == t and i == x else None
        def sub(i, t=t, seen=seen):
            if t == 1 and ans is not None and i in seen and active == 1 and 'cnt1' in S:
                return f'ans={ans[i]}'
            return ''
        _tree(cv, T, E, (bx[0], y0, bx[1], y1), lambda i: i, fill=fill, ring=ring, sub=sub, title=name, r=26)


def _dfs_cnt(S, B, ret):
    return f'访问 `{S.x}`：它到 0 的距离奇偶是 `{S.d}`，`cnt[{S.d}] += 1` → `{S.cnt}`'


CONFIG = dict(
    num=3373, title='连接两棵树后最大目标节点数目 II', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='树的奇偶染色（二分图）',
    tags=['灵神题单·链表树与回溯', '难度分 2162'],
    code='''
class Solution:
    def count(self, edges: List[List[int]]) -> Tuple[List[List[int]], List[int]]:
        g = [[] for _ in range(len(edges) + 1)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        cnt = [0, 0]
        def dfs(x: int, fa: int, d: int) -> None:
            cnt[d] += 1
            for y in g[x]:
                if y != fa:
                    dfs(y, x, d ^ 1)
        dfs(0, -1, 0)
        return g, cnt

    def maxTargetNodes(self, edges1: List[List[int]], edges2: List[List[int]]) -> List[int]:
        _, cnt2 = self.count(edges2)
        max2 = max(cnt2)

        g, cnt1 = self.count(edges1)
        ans = [max2] * len(g)
        def dfs(x: int, fa: int, d: int) -> None:
            ans[x] += cnt1[d]
            for y in g[x]:
                if y != fa:
                    dfs(y, x, d ^ 1)
        dfs(0, -1, 0)
        return ans
''',
    call='Solution().maxTargetNodes([[0,1],[0,2],[2,3],[2,4]], [[0,1],[0,2],[1,3],[1,4]])',
    expect=[6, 5, 5, 6, 6],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='cnt', label='cnt（偶数层 / 奇数层 的节点数）', cell=70, h=120),
        dict(type='array', var='ans', label='ans', cell=64, h=120),
        dict(type='calls', h=170),
    ],
    watch=[('x', lambda S: S['_inner'].get('x'), 'yellow'), ('d', lambda S: S['_inner'].get('d'), 'blue'),
           ('cnt2', lambda S: S.get('cnt2'), 'pink'), ('max2', lambda S: S.get('max2'), 'orange'), ('cnt1', lambda S: S.get('cnt1'), 'cyan')],
    skip=['for x, y in edges', 'g[x].append(y)', 'g[y].append(x)', 'for y in g[x]', 'if y != fa'],
    captions={
        'g = [[] for': '建树：邻接表，每条边两个方向都加',
        'cnt = [0, 0]': '`cnt[0]`、`cnt[1]`：到根距离为偶数 / 奇数的节点个数（==相当于棋盘黑白染色==）',
        'cnt[d] += 1': _dfs_cnt,
        'dfs(y, x, d ^ 1)': '走到孩子 `{y}`：每走一步，颜色翻转（`d ^ 1`）',
        'dfs(0, -1, 0)': '从节点 0 开始 DFS，0 号点算颜色 `0`',
        'return g, cnt': '这棵树染色完成：`cnt = {cnt}`',
        '_, cnt2 = self.count(edges2)': '第二棵树：偶数层 `{cnt2[0]}` 个、奇数层 `{cnt2[1]}` 个',
        'max2 = max(cnt2)': '节点 i 连到第二棵树==较少的一类==，另一类（较多的）全成目标节点 → `max2 = {max2}`',
        'g, cnt1 = self.count(edges1)': '第一棵树：偶数层 `{cnt1[0]}` 个、奇数层 `{cnt1[1]}` 个',
        'ans = [max2] * len(g)': '每个节点先拿第二棵树的 `max2 = {max2}`',
        'ans[x] += cnt1[d]': '节点 `{x}` 的颜色是 `{d}`，同色节点共 `cnt1[{d}] = {cnt1[d]}` 个 → `ans[{x}] = {ans[x]}`',
        'return ans': '答案：`{ans}`',
    },
    cards=dict(
        one_liner='树是二分图：偶数步只会走到同色节点',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['两棵无向树，路径边数为偶数的两个点互为「目标节点」，自己也算',
                 '对第一棵树每个节点 `i`，连一条边到第二棵树的任意节点，求 `i` 的目标节点数最大值',
                 '每次查询独立。示例：`[6,5,5,6,6]`'],
        quote='对于一棵树，我们把这棵树的所有节点染成黑色或者白色：黑色节点的所有邻居都是白色，白色节点的所有邻居都是黑色。这个想法来自国际象棋的棋盘。',
        quote_src='—— 灵茶山艾府题解',
        idea=['染色后，走偶数步 = 到同色节点：第一棵树里节点 `i` 的目标节点 = ==同色节点数==',
              '连到第二棵树后多走一步：连到较少的一类，较多的一类就成了目标 → 加 `max2`',
              '所以 `ans[i] = 同色数 + max(cnt2)`，两次 DFS 染色即可'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`',
                 '第二棵树只取 `max(cnt2)`，与 `i` 无关',
                 '题目保证 `n, m ≥ 2`；若都是 1 个节点需要特判',
                 '同类题：二分图染色、棋盘奇偶性'],
    ),
)
