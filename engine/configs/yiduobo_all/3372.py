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

E1 = [[0, 1], [1, 2], [2, 3]]
E2 = [[0, 1]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    mid = (x0 + x1) / 2
    res = S.get('res')
    act = 0 if res is None else (1 if len(res) == 4 else 2)
    for ti, (n, E, ox, title) in enumerate([(4, E1, x0, '第一棵树：最多 k 轮 bfs'),
                                              (2, E2, mid, '第二棵树：最多 k−1 轮 bfs')]):
        fills, rings, notes = {}, {}, {}
        if act == ti + 1 and 'vis' in S and 'start' in S:
            for v in S['vis']:
                fills[v] = (28, 84, 52)
            fills[S['start']] = (40, 84, 140)
            q, h, t = S.get('q', []), S.get('head', 0), S.get('tail', 0)
            for v in q[h:t]:
                rings[v] = T['yellow']
            x = S.get('x')
            if x is not None and S['_line'] in (21, 22, 23, 24):
                rings[x] = T['pink']
        if act == ti + 1 and res:
            for v, c in enumerate(res):
                if c:
                    notes[v] = (f'={c}', T['orange'])
        _dtree(cv, T, (ox + 10, y0, ox + (x1 - x0) / 2 - 10, y1 - 70), n, E, title, fills, rings, notes, side=True)
    if act and 'rnd' in S:
        cv.text((x0 + 10, y1 - 64), f"起点 start = {S.get('start')}，已走 rnd = {S['rnd']} 轮，已发现 {len(S.get('vis', []))} 个点", 22, T['text'], anchor='lb', bold=True)
    if 'cnt1' in S:
        cv.text((x0 + 10, y1 - 34), f"cnt1 = {S['cnt1']}" + (f"　cnt2 = {S['cnt2']}" if 'cnt2' in S else ''), 22, T['orange'], anchor='lb', bold=True)
    cv.text((x0 + 10, y1 - 6), '蓝 = 起点  绿 = 已发现  黄圈 = 本轮新发现的一层  橙字 = 各起点的结果', 20, T['muted'], anchor='lb')


CONFIG = dict(
    num=3372, title='连接两棵树后最大目标节点数目 I', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='逐点 BFS 数点 · 第二棵树取最大',
    tags=['灵神题单·动态规划', '灵神题单·链表树与回溯', '难度分 1927'],
    code='''
class Solution(object):
    def maxTargetNodes(self, edges1, edges2, k):
        
        def calc(edge, k):
            n = len(edge) + 1
            if k < 0:
                return [0] * n
            elif k == 0:
                return [1] * n

            res = [0] * n

            g = {x : set() for x in range(n)}
            for x, y in edge:
                g[x].add(y)
                g[y].add(x)
            
            for start in range(n):
                q = [start]
                vis = set([start])
                head, tail = 0, 1
                rnd = 0
                while head < tail and rnd < k:
                    rnd += 1
                    for x in q[head : tail]:
                        for y in g[x]:
                            if y not in vis:
                                vis.add(y)
                                q.append(y)
                    
                    head, tail = tail, len(q)
                
                res[start] = tail
            
            return res

        cnt1 = calc(edges1, k)
        cnt2 = calc(edges2, k - 1)
        ma = max(cnt2)
        return [v + ma for v in cnt1]
''',
    call='Solution().maxTargetNodes([[0,1],[1,2],[2,3]], [[0,1]], 2)',
    expect=[5, 6, 6, 5],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='text', h=50, size=26, fn=lambda S: '`tail` = 已发现的点数，每轮 bfs 把边界往外推一层' if 'tail' in S else ''),
    ],
    watch=[('start', 'start', 'blue'), ('rnd', 'rnd', 'yellow'), ('head', 'head'), ('tail', 'tail', 'green'),
           ('res', 'res', 'orange'), ('ma', 'ma', 'pink')],
    skip=['n = len(edge)', 'for x, y in edge', 'g[x].add(y)', 'g[y].add(x)', 'q = [start]', 'vis = set', 'rnd = 0',
          'head, tail = 0, 1', 'for y in g[x]', 'q.append(y)'],
    captions={
        'if k < 0': lambda S, B, r: ('`k < 0`：连不到任何点，全是 0' if S.k < 0 else '`k ≥ 0`：往下算'),
        'elif k == 0': lambda S, B, r: ('`k = 0`：只剩自己，每个点都是 1' if S.k == 0 else '`k > 0`：需要 bfs'),
        'res = [0] * n': '`res[i]`：起点 i 在 `k` 步内能到的点数',
        'g = {x': '建邻接表：每个点存一个邻居集合',
        'for start in range': lambda S, B, r: (f'枚举起点 `start = {S.start}`，以它为中心做 bfs' if ('start' not in B or S.start != B.start) else '所有起点都算完了'),
        'while head < tail': lambda S, B, r: (f'`rnd = {S.rnd} < k = {S.k}` 且这一层有点 → 再推一层' if (S.head < S.tail and S.rnd < S.k)
                                                else (f'`rnd = {S.rnd}` 已到 `k`，停止' if S.rnd >= S.k else '没有新点了，停止')),
        'rnd += 1': '往外走一步：`rnd = {rnd}`',
        'for x in q[head : tail]': lambda S, B, r: (f'取出这一层的点 `{S.x}`，看它的邻居' if ('x' not in B or S.x != B.x) else '这一层的点都处理完了'),
        'if y not in vis': lambda S, B, r: (f'邻居 `{S.y}` 没来过 → 新发现' if S.y not in B.vis else f'邻居 `{S.y}` 已来过（父亲方向），跳过'),
        'vis.add(y)': '`{y}` 标记已来过',
        'head, tail = tail, len(q)': '下一层 = 刚加入的点：`[{head}, {tail})`，`tail` = 已发现总数 `{tail}`',
        'res[start] = tail': '起点 `{start}` 在 `k` 步内能到 `{tail}` 个点 → `res = {res}`',
        'return res': '这棵树每个点的结果：`{res}`',
        'cnt1 = calc': '第一棵树：每个点最多 `k = {k}` 步内有多少点 → `cnt1 = {cnt1}`',
        'cnt2 = calc': '第二棵树：新边占一步，所以只走 `k − 1` 步 → `cnt2 = {cnt2}`',
        'ma = max(cnt2)': '连接点选 cnt2 最大的：==`ma = {ma}`==',
        'return [v + ma': '`answer[i] = cnt1[i] + ma` → `{ret}`',
    },
    max_steps=64,
    cards=dict(
        one_liner='两棵树互不影响：各自 bfs 数点，再把最大值加起来',
        complexity='时间 `O(n² + m²)`（每个点 bfs 一次），空间 `O(n + m)`',
        problem=['两棵无向树，从第一棵树选一点和第二棵树一点连一条边',
                 '`u` 到 `v` 路径边数 `≤ k`，`u` 就是 `v` 的目标节点',
                 '对第一棵树每个点 `i`，求连边后目标节点数的最大值',
                 '本视频：第一棵 `0-1-2-3`，第二棵 `0-1`，`k = 2` → `[5,6,6,5]`'],
        quote='无论如何添加边，第一棵树中节点间的距离是固定的。……i 在第二棵树中的目标节点，实际上也认为是 j 在第二棵树中距离为 k - 1 的目标节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['新边不会成环，所以==第一棵树内部的距离不变==：对每个点 bfs 最多 `k` 轮数点，得 `cnt1`',
              '连到第二棵树的 `j` 后，要多走一条边，所以数 `j` 周围 `k−1` 步内的点，得 `cnt2`',
              '每个 `i` 都连到 `cnt2` 最大的 `j`：答案 = `cnt1[i] + max(cnt2)`'],
        result='运行结束，返回 `[5, 6, 6, 5]`：`cnt1 = [3,4,4,3]`，`ma = 2`',
        summary=['时间 `O(n² + m²)`：n、m ≤ 1000，每点一次 bfs 足够',
                 '`k < 0` 全 0、`k == 0` 全 1 要单独处理（`k = 0` 时第二棵树 `k−1 < 0`）',
                 '`tail` 就是已发现的点数；用 `head, tail` 切出 bfs 的一层',
                 '原文是 Python 2 风格写法，但在 Python 3 下无需改动，代码照搬'],
    ),
)
