# ---- 一般树绘制（custom 视图）：按边集合和根节点分层布局
def gtree(edges, root):
    adj = {}
    for a, b in edges:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    kids, depth = {}, {root: 0}

    def go(v, fa):
        kids[v] = []
        for w in adj.get(v, []):
            if w != fa:
                depth[w] = depth[v] + 1
                kids[v].append(w)
                go(w, v)
    go(root, None)
    xs, cnt = {}, [0]

    def lay(v):
        if not kids[v]:
            xs[v] = cnt[0]
            cnt[0] += 1
        else:
            for w in kids[v]:
                lay(w)
            xs[v] = (xs[kids[v][0]] + xs[kids[v][-1]]) / 2
    lay(root)
    return kids, depth, xs, cnt[0]


def make_tree_draw(edges, root, state_fn, title, elabel=None, arrows=False):
    kids, depth, xs, nleaf = gtree(edges, root)
    maxd = max(depth.values())

    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
        sp = min(120, (x1 - x0 - 60) / max(1, nleaf))
        dy = min(120, (y1 - y0 - 90) / max(1, maxd + 0.6))
        rad = max(16, min(28, sp * 0.36, dy * 0.26))
        sx = x0 + 30 + ((x1 - x0 - 60) - sp * nleaf) / 2
        pos = {v: (sx + sp * (xs[v] + 0.5), y0 + 70 + depth[v] * dy) for v in kids}
        for v in kids:
            for w in kids[v]:
                (ax, ay), (bx, by) = pos[v], pos[w]
                if arrows:
                    cv.arrow((ax, ay + rad), (bx, by - rad), T['border'], 3, 10)
                else:
                    cv.line([(ax, ay + rad), (bx, by - rad)], T['border'], 3)
                if elabel and (v, w) in elabel:
                    mx, my = ax + (bx - ax) * 0.4, ay + (by - ay) * 0.4
                    s = str(elabel[(v, w)])
                    cv.text((mx - 8, my), s, 20, T['orange'], anchor='rm', bold=True)
        for v in kids:
            X, Y = pos[v]
            st = state_fn(S, v) or {}
            fill = T[st['fill']] if st.get('fill') else T['panel2']
            cv.rect((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=T['border'], width=2, r=rad)
            if st.get('ring'):
                cv.rect((X - rad - 5, Y - rad - 5, X + rad + 5, Y + rad + 5), outline=T[st['ring']], width=5, r=rad + 5)
            cv.text((X, Y), st.get('text', v), 24, T['bg'] if st.get('fill') else T['text'], anchor='mm', bold=True)
            if st.get('sub') is not None:
                cv.text((X + rad + 8, Y), st['sub'], 21, T[st.get('subc', 'green')], anchor='lm', bold=True)
            if st.get('tag'):
                cv.text((X - rad - 8, Y - rad), st['tag'], 20, T[st.get('tagc', 'pink')], anchor='rb', bold=True)
    return draw
# ---- end helper

CONV = [[0,1,2],[0,2,3],[1,3,4],[1,4,5],[2,5,2],[4,6,3],[5,7,4]]
EDGES = [(x, y) for x, y, w in CONV]
WT = {(x, y): w for x, y, w in CONV}


def _st(S, v):
    res = S.get('res')
    now = S.get('now')
    done = res is not None and res[v] is not None
    return dict(fill='green' if done else None, ring='yellow' if (now == v and S.get('_line', 0) >= 14) else None,
                sub=f'{res[v]}' if done else None)


CONFIG = dict(
    num=3528, title='单位转换 I', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='BFS 累乘边权',
    tags=['链表树与回溯', '难度分 1580'],
    code='''
class Solution(object):
    def baseUnitConversions(self, conversions):
        
        n = len(conversions) + 1
        g = [[] for _ in range(n)]
        for x, y, w in conversions:
            g[x].append((y, w))
            g[y].append((x, w))
        
        res = [None] * n
        res[0] = 1
        mod = 10 ** 9 + 7
        q = deque()
        q.append(0)
        while q:
            now = q.popleft()
            for nxt, w in g[now]:
                if res[nxt] is None:
                    res[nxt] = res[now] * w % mod
                    q.append(nxt)
        
        return res
''',
    call='Solution().baseUnitConversions(CONV)',
    setup='CONV = [[0,1,2],[0,2,3],[1,3,4],[1,4,5],[2,5,2],[4,6,3],[5,7,4]]',
    expect=[1, 2, 3, 8, 10, 6, 30, 24],
    max_steps=58,
    views=[
        dict(type='custom', draw=make_tree_draw(EDGES, 0, _st, '把 0 当树根（橙色 = 边权 factor，绿 = 已得到 res，右侧数字 = res，黄环 = 正在扩展）', WT), h=330),
        dict(type='array', var='res', label='res[i]（None = 还没到达）', color=lambda S, i, v: 'green' if v is not None else None, h=150),
        dict(type='queue', var='q', label='BFS 队列 q', h=120),
    ],
    watch=[('now', 'now', 'blue'), ('nxt', 'nxt', 'orange'), ('w', 'w', 'pink')],
    captions={
        'g[x].append': '建树：每条边存两个方向，`{x} - {y}`，边权 `{w}`（树是无向的，方向不用管）',
        'g[y].append': '反向也存一份：`{y}` 能看到 `{x}`，边权同为 `{w}`',
        'res[0] = 1': '1 个 0 号单位 = 1 个 0 号单位：根的答案 `res[0] = 1`',
        'q.append(0)': '从根 0 开始 bfs，先入队',
        'while q': lambda S, B, r: f'队列里还有 `{list(S.q)}` → 继续' if S.q else '队列空了，所有节点都已到达 → 结束',
        'now = q.popleft()': '取出队首 `{now}`：它的 `res` 已经算好 = `{res[now]}`，现在去扩展它的邻居',
        'if res[nxt] is None': lambda S, B, r: (f'`res[{S.nxt}]` 还是 None → 第一次到达，这是 {S.now} 的孩子，处理它' if S.res[S.nxt] is None
                                              else f'`res[{S.nxt}]` 已有值 → 它是 {S.now} 的父亲，==不走回头路=='),
        'res[nxt] = res[now]': '`res[{nxt}] = res[{now}] * {w} % mod` = `{B.res[now]} * {w}` = =={res[nxt]}==',
        'q.append(nxt)': '`{nxt}` 入队，等着扩展它自己的孩子',
        'return res': '全部到达，返回 `{res}`',
    },
    cards=dict(
        one_liner='0 是树根，从 0 做 BFS，沿路把边权累乘',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 种单位，`conversions[i] = [source, target, factor]`：1 个 source = factor 个 target',
                 '求 1 个 0 号单位等于多少个 `i` 号单位，对 `10^9+7` 取模',
                 '示例：`[[0,1,2],[1,2,3]]` → `[1,2,6]`'],
        quote='题目相当于给出一颗树，同时题目又保证了从0开始可以转换到其他任意单位，于是可以认为0是这颗树的树根，只需从0开始做bfs，计算0到其他所有节点的距离就行了，这里的距离指的是路径上factor的累乘。',
        quote_src='—— yiduobo 题解原文',
        idea=['n 个点 n-1 条边 + 0 能到所有点 → ==树==，0 就是树根',
              '这里的「距离」不是边数，而是路径上 `factor` 的==乘积==',
              '用 `res[nxt] is None` 判断有没有到过：没到过才是孩子'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '建的是==无向图==（两个方向都存），所以要靠 `res[nxt] is None` 防止走回父亲',
                 '乘完立刻 `% mod`，Python 虽不溢出但大数会变慢',
                 '对比灵神：灵神只建单向边 + DFS 传 `mul`；这里双向建边 + BFS 队列',
                 '原文为 Python 2 写法（`class Solution(object)`），代码无需改动即可在 Python 3 运行'],
    ),
)
