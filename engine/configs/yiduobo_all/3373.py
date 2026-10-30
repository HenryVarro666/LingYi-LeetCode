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

E1 = [[0, 1], [0, 2], [0, 3], [2, 4]]
E2 = [[0, 1], [1, 2], [1, 3]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    inner = S['_inner']
    cur = inner.get('x')
    edges = S.get('edges')
    active = 0
    if edges is not None:
        active = 1 if edges is S.get('edges1') else 2
    mark = S.get('mark')
    mid = (x0 + x1) / 2
    for t, (E, bx, name) in enumerate(((E1, (x0, mid - 6), '第一棵树 edges1'), (E2, (mid + 6, x1), '第二棵树 edges2')), 1):
        pos, depth, w, h, kids = _lay(E)
        done = ('cnt1' in S) if t == 1 else ('cnt2' in S)
        def fill(i, t=t, depth=depth, done=done):
            if done and active != t:
                return 'blue' if depth[i] % 2 == 0 else 'pink'
            if active == t and mark is not None and mark[i] != -1:
                return 'blue' if mark[i] == 0 else 'pink'
            return None
        def ring(i, t=t):
            return 'yellow' if active == t and i == cur else None
        _tree(cv, T, E, (bx[0], y0, bx[1], y1), lambda i: i, fill=fill, ring=ring, title=name, r=26)


def _lvl(S, B, ret):
    return f'进入下一层：颜色 `now` 翻转为 `{S.now}`（蓝 = 0，粉 = 1），这一层是 `q[{S.head}:{S.tail}]`'


CONFIG = dict(
    num=3373, title='连接两棵树后最大目标节点数目 II', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='BFS 按层奇偶分成两部分',
    tags=['灵神题单·链表树与回溯', '难度分 2162'],
    code='''
class Solution(object):
    def maxTargetNodes(self, edges1, edges2):
        
        def calc(edges):
            n = len(edges) + 1
            cnt = [0] * 2
            mark = [-1] * n

            g = {x : set() for x in range(n)}
            for x, y in edges:
                g[x].add(y)
                g[y].add(x)
            
            q = [0]
            vis = set([0])
            mark[0] = 0

            head, tail = 0, 1
            cnt[0] += 1
            now = 0
            while head < tail:
                now = 1 - now
                for x in q[head : tail]:
                    for y in g[x]:
                        if y not in vis:
                            vis.add(y)
                            mark[y] = now
                            q.append(y)
                            cnt[now] += 1
                
                head, tail = tail, len(q)
            
            return [cnt[mark[x]] for x in range(n)]
        
        cnt1 = calc(edges1)
        cnt2 = calc(edges2)
        ma = max(cnt2)
        return [v + ma for v in cnt1]
''',
    call='Solution().maxTargetNodes([[0,1],[0,2],[0,3],[2,4]], [[0,1],[1,2],[1,3]])',
    expect=[5, 6, 6, 6, 5],
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var='q', label='q（BFS 队列）', cell=60, h=110),
        dict(type='array', var='mark', label='mark（-1 = 未染色）', cell=60, h=110),
        dict(type='array', var='cnt', label='cnt（颜色 0 / 颜色 1 的个数）', cell=60, h=110),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'yellow'), ('head', lambda S: S['_inner'].get('head'), 'blue'),
           ('tail', lambda S: S['_inner'].get('tail'), 'pink'), ('cnt1', lambda S: S.get('cnt1'), 'cyan'),
           ('cnt2', lambda S: S.get('cnt2'), 'pink'), ('ma', lambda S: S.get('ma'), 'orange')],
    skip=['n = len(edges) + 1', 'for x, y in edges', 'g[x].add(y)', 'vis = set', 'q = [0]', 'for y in g[x]', 'vis.add(y)', 'q.append(y)', 'cnt = [0] * 2', 'mark = [-1] * n', 'g = {x', 'g[y].add(x)', 'head, tail = 0, 1', 'cnt[0] += 1', 'now = 0', 'for x in q[head'],
    captions={
        'mark[0] = 0': '建好邻接集合后，从 0 号点开始 BFS：`mark[x]` 记 x 到 0 的距离奇偶，0 号点是 `0`，颜色 0 先有 1 个点',
        'cnt[0] += 1': '颜色 0 已有 1 个点（0 号点自己）',
        'now = 0': '`now` 表示当前层的颜色',
        'while head < tail': lambda S, B, r: (f'这一层还有点：`head = {S.head} < tail = {S.tail}`' if S.head < S.tail else f'`head = {S.head}`，`tail = {S.tail}`：没有新点了 → 这棵树染完'),
        'now = 1 - now': _lvl,
        'for x in q[head : tail]': '取出这一层的节点 `{x}`',
        'if y not in vis': lambda S, B, r: (f'从 `{S.x}` 看邻居 `{S.y}`：没访问过 → 它在下一层' if S.y not in B.vis else f'从 `{S.x}` 看邻居 `{S.y}`：已访问（是父亲）→ 跳过'),
        'mark[y] = now': '`mark[{y}] = {now}`：到 0 的距离奇偶 = 层数奇偶',
        'cnt[now] += 1': '颜色 `{now}` 的个数加一：`cnt = {cnt}`',
        'head, tail = tail, len(q)': '这一层处理完：新的一层是 `q[{head}:{tail}]`',
        'return [cnt[mark[x]]': lambda S, B, r: f'每个节点的目标节点数 = 它所属部分的大小：`{r}`',
        'cnt1 = calc': '第一棵树：每个节点的同色节点数 `{cnt1}`',
        'cnt2 = calc': '第二棵树：每个节点所在部分的大小 `{cnt2}`',
        'ma = max(cnt2)': '连到较少的部分，较多的部分就全成目标 → 取最大 `ma = {ma}`',
        'return [v + ma': '`v + ma` 逐个相加，答案 `{ret}`',
    },
    cards=dict(
        one_liner='距离奇偶只看到根的深度奇偶，BFS 分成两部分就行',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['两棵无向树，两点间路径边数为偶数则互为目标节点，自己也算',
                 '第一棵树的每个节点 `i` 连到第二棵树某点，求 `i` 的目标节点数最大值',
                 '本视频示例：`[5,6,6,6,5]`'],
        quote='可以发现，最后这一项dis[lca] * 2对距离的奇偶性没有影响，因此只有当dis[x]和dis[y]同奇偶时，二者互为目标节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['距离 `dis[x] + dis[y] - 2*dis[lca]`，最后一项是偶数 → 只看 `dis[x]`、`dis[y]` 的奇偶',
              'BFS 按层给节点标 0/1，每个节点的目标节点数 = 自己所在部分的大小',
              '第二棵树：连到较少的一类，较多的一类全是目标 → 加上 `max(cnt2)`'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`',
                 '`calc` 返回每个节点所在部分的大小，两棵树复用同一函数',
                 '`max(cnt2)` 对所有 i 相同，只算一次',
                 '对比灵神：灵神用 DFS 里的 `d ^ 1` 染色；yiduobo 用 BFS 一层一层翻转 `now`'],
    ),
)
