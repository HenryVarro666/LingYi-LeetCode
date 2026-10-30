def _layout_tree(ch, root):
    pos, cnt = {}, [0]

    def go(u, d):
        kids = ch.get(u, [])
        if not kids:
            x = cnt[0]
            cnt[0] += 1
        else:
            xs = [go(v, d + 1) for v in kids]
            x = (xs[0] + xs[-1]) / 2
        pos[u] = (x, d)
        return x
    go(root, 0)
    return pos, cnt[0]


def _tree_view(ch, root, colors, title, tags=None, wt=None, lab=None):
    """ch: {父: [子...]}；colors(S) -> {节点: 颜色名}；tags(S) -> {节点: 小字}；wt: {子: 边权}"""
    pos, W = _layout_tree(ch, root)
    D = max(d for _, d in pos.values()) + 1

    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
        cell = min(120, (x1 - x0 - 60) / max(W, 1))
        rowh = min(110, (y1 - y0 - 165) / max(D - 1, 1))
        sx = x0 + 30 + ((x1 - x0 - 60) - cell * W) / 2
        r = min(28, cell * 0.36, rowh * 0.42)
        P = {u: (sx + (x + 0.5) * cell, y0 + 80 + d * rowh) for u, (x, d) in pos.items()}
        for u, kids in ch.items():
            for v in kids:
                cv.line([P[u], P[v]], T['border'], 3)
                if wt:
                    left = P[v][0] <= P[u][0] + 1
                    cv.text(((P[u][0] + P[v][0]) / 2 + (-10 if left else 10), (P[u][1] + P[v][1]) / 2 - 6), wt[v], 22, T['orange'],
                            anchor='rm' if left else 'lm', bold=True)
        cm = colors(S) or {}
        tg = (tags(S) if tags else None) or {}
        for u, (X, Y) in P.items():
            c = cm.get(u)
            cv.rect((X - r, Y - r, X + r, Y + r), fill=T[c] if c else T['panel2'], outline=T['border'], width=2, r=r)
            cv.text((X, Y), lab(u) if lab else u, 26, T['bg'] if c else T['text'], anchor='mm', bold=True)
            if u in tg:
                cv.text((X + r + 6, Y + r * 0.5), tg[u], 20, T['muted'], anchor='lm', bold=True)
    return dict(type='custom', draw=draw, h=0)
CH = {0: [1], 1: [2, 3, 4], 2: [5]}
WT = {1: 2, 2: 3, 3: 5, 4: 4, 5: 6}


def _colors(S):
    c = {}
    if 'now' in S:
        c[S['now']] = 'yellow'
        if S.get('fa') is not None:
            c[S['fa']] = 'green'
        return c
    for nm, col in (('low', 'pink'), ('high', 'blue')):
        v = S.get(nm)
        if isinstance(v, int) and 0 <= v < 6:
            c[v] = col
    if not c:
        for nm, col in (('src1', 'blue'), ('src2', 'pink'), ('dest', 'orange')):
            v = S.get(nm)
            if isinstance(v, int) and 0 <= v < 6:
                c[v] = col
    return c


def _tags(S):
    d, lv = S.get('dis'), S.get('level')
    if d is None or lv is None:
        return {}
    return {i: f'dis={d[i]}' for i in range(6) if lv[i] is not None}


def _formula(S):
    if 'src1' in S and 'dest' in S:
        return f"`src1 = {S['src1']}`（蓝），`src2 = {S['src2']}`（粉），`dest = {S['dest']}`（橙）：子树 = 三个点之间的 Y 形"
    return '`f[x]` 依次存 `x` 往上 1、2、4… 步的祖先；`dis[x]` 是到根的带权距离'


CONFIG = dict(
    num=3553, title='包含要求路径的最小带权子图 II', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='倍增 LCA + 分情况讨论两条路径重叠',
    tags=['链表树与回溯', '难度分 2411'],
    code='''
class Solution(object):
    def minimumWeight(self, edges, queries):
        
        n = len(edges) + 1
        f = [[] for _ in range(n)]
        level = [None] * n
        dis = [0] * n

        g = [[] for _ in range(n)]
        for x, y, w in edges:
            g[x].append((y, w))
            g[y].append((x, w))
        
        def dfs(now, fa, f, depth):
            level[now] = depth
            if fa is not None:
                f[now].append(fa)
                p = fa
                while len(f[p]) >= len(f[now]):
                    f[now].append(f[p][len(f[now]) - 1])
                    p = f[now][-1]
            
            for nxt, w in g[now]:
                if nxt != fa:
                    dis[nxt] = dis[now] + w
                    dfs(nxt, now, f, depth + 1)

        def get_lca(x, y):
            if level[x] > level[y]:
                low, high = x, y
            else:
                low, high = y, x
            
            p = len(f[low]) - 1
            while level[low] != level[high]:
                while p >= len(f[low]) or level[f[low][p]] < level[high]:
                    p -= 1
                low = f[low][p]

            p = len(f[low]) - 1
            while low != high:
                while p >= len(f[low]) or (p > 0 and f[low][p] == f[high][p]):
                    p -= 1
                low = f[low][p]
                high = f[high][p]
            
            return low

        dfs(0, None, f, 0)
        res = []
        for src1, src2, dest in queries:
            lca1 = get_lca(src1, dest)
            lca2 = get_lca(src2, dest)
            if lca1 != lca2:
                res.append(dis[src1] + dis[src2] - dis[lca1] - dis[lca2])
                if level[lca1] < level[lca2]:
                    res[-1] += dis[dest] - dis[lca1]
                else:
                    res[-1] += dis[dest] - dis[lca2]

            else:
                lca12 = get_lca(src1, src2)
                res.append(dis[src1] + dis[src2] - dis[lca12] - dis[lca12] + dis[lca12] - dis[lca1] + dis[dest] - dis[lca1])

        return res
''',
    call='Solution().minimumWeight([[0,1,2],[1,2,3],[1,3,5],[1,4,4],[2,5,6]], [[2,3,4]])',
    expect=[12],
    views=[
        dict(type='text', fn=_formula, size=24, h=60),
        dict(_tree_view(CH, 0, _colors, '树（边上是权重；黄 = 正在处理，绿 = 父亲；蓝/粉 = 浅/深）', tags=_tags, wt=WT), h=520),
        dict(type='table', var='f', label='f[x]：x 往上走 1、2、4…步到的节点', rows=list(range(6)), cell=44, h=290),
    ],
    watch=['now', 'fa', 'x', 'y', 'low', 'high', 'p'],
    max_steps=84,
    skip=['for x, y, w in edges', 'g[x].append', 'g[y].append', 'for nxt, w in g[now]', 'if nxt != fa', 'p = fa',
          'p = f[now][-1]', 'p -= 1', 'f = [[] for', 'level = [None]', 'while level[low] != level[high]', 'if fa is not None',
          'res = []', 'for src1, src2, dest in queries', 'g = [[] for', 'dis = [0]', 'level[now] = depth', 'low, high = x, y', 'low, high = y, x'],
    captions={
        'n = len(edges) + 1': '`n = {n}` 个节点；边已按两头存进邻接表 `g`',
        'dfs(0, None, f, 0)': '从根 `0` 出发 DFS：填 `level`（层）、`dis`（到根距离）、`f`（倍增表）',
        'level[now] = depth': '`level[{now}] = {depth}`',
        'f[now].append(fa)': '`f[{now}][0] = {fa}`：走 1 步 = 父亲',
        'while len(f[p]) >= len(f[now])': lambda S, B, ret: (f'`p = {S.p}` 还有第 {len(S.f[S.now])} 档祖先 → 继续翻倍' if len(S.f[S.p]) >= len(S.f[S.now])
                                                            else f'`p = {S.p}` 没有更高的祖先了 → `f[{S.now}]` 填完'),
        'f[now].append(f[p][len(f[now]) - 1])': '`f[{now}]` 变成 `{f[now]}`：近的祖先 `p` 再走同样的步数',
        'dis[nxt] = dis[now] + w': '`dis[{nxt}] = {dis[now]} + {w}` = =={dis[nxt]}==',
        'lca1 = get_lca(src1, dest)': '`lca1` = `src1 = {src1}` 与 `dest = {dest}` 的最近公共祖先',
        'lca2 = get_lca(src2, dest)': '`lca2` = `src2 = {src2}` 与 `dest = {dest}` 的最近公共祖先；`lca1 = {lca1}`',
        'if lca1 != lca2': lambda S, B, ret: (f'`lca1 = {S.lca1}`，`lca2 = {S.lca2}`：两个 LCA 不同 → 一个是另一个的祖先' if S.lca1 != S.lca2
                                              else f'`lca1 = lca2 = {S.lca1}`：两条路径在同一点汇入 `dest` 的祖先链 → 要去掉重叠'),
        'lca12 = get_lca(src1, src2)': '`lca12` = `src1` 与 `src2` 的最近公共祖先：它们先在这里合流',
        'res.append(dis[src1] + dis[src2] - dis[lca12]': '总权重 = `src1→lca12` + `src2→lca12` + `lca12→lca1` + `lca1→dest` = ==`{res[-1]}`==',
        'res.append(dis[src1] + dis[src2] - dis[lca1]': '两段互不重叠的路径，加上较浅的 LCA 到 `dest`：==`{res[-1]}`==',
        'if level[x] > level[y]': lambda S, B, ret: f'`level[{S.x}] = {S.level[S.x]}`，`level[{S.y}] = {S.level[S.y]}`：深的当 `low`，浅的当 `high`（同层随便）',
        'low, high = x, y': '`low = {low}`，`high = {high}`',
        'low, high = y, x': '`low = {low}`，`high = {high}`（同层时随便）',
        'p = len(f[low]) - 1': lambda S, B, ret: ('`low` 已是根，不用再找' if S.p < 0 else f'从 `low` 最大的一档 `p = {S.p}` 开始试'),
        'while p >= len(f[low]) or level[f[low][p]] < level[high]': lambda S, B, ret: ('这一档不能用（太高，或者会跳到 `high` 上方）→ `p` 减小' if (S.p >= len(S.f[S.low]) or S.level[S.f[S.low][S.p]] < S.level[S.high])
                                                                                     else f'第 `{S.p}` 档可以用'),
        'low = f[low][p]': lambda S, B, ret: (f'`low` 跳 `2^{S.p}` 步 → =={S.low}==' if S.level[S.low] == S.level[S.high] or True else ''),
        'while low != high': lambda S, B, ret: ('同层但不是同一点：一起往上找汇合处' if S.low != S.high else '`low == high`：找到最近公共祖先'),
        'while p >= len(f[low]) or (p > 0 and f[low][p] == f[high][p])': lambda S, B, ret: ('这一档不能跳（太高，或者两边已汇合，会跳过头）→ `p` 减小' if (S.p >= len(S.f[S.low]) or (S.p > 0 and S.f[S.low][S.p] == S.f[S.high][S.p]))
                                                                                              else f'第 `{S.p}` 档：两边祖先不同，可以跳'),
        'high = f[high][p]': '`high` 也跳：`low = {low}`，`high = {high}`',
        'return low': '最近公共祖先 = ==`{ret}`==',
        'return res': '最小子树权重：==`{ret}`==',
    },
    cards=dict(
        one_liner='先求两个 LCA，再分「同一点 / 祖孙」两种情况去重',
        complexity='预处理 `O(n log n)`，每个询问 `O(log n)`',
        problem=['无向带权树，节点 `0..n-1`；询问 `[src1, src2, dest]`',
                 '选一棵子树，使 `src1`、`src2` 都能到达 `dest`，求==最小总权重==',
                 '示例：`edges=[[0,1,2],[1,2,3],[1,3,5],[1,4,4],[2,5,6]]`，查 `[2,3,4]` → `12`'],
        quote='lca1和lca2要么是同一个节点，要么是互为祖孙的两个节点。理由也很简单，因为lca1和lca2都是dest的祖先节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['子树只需包含 `src1→dest`、`src2→dest` 两条最短路，重叠部分只算一次',
              '`lca1 == lca2`：`src1`、`src2` 先在 `lca12` 合流，再一起走到 `dest`',
              '`lca1 != lca2`：较深的那个 LCA 到 `dest` 是较浅的子路径，只算较浅的一段',
              '距离用 `dis[x]` 之差；LCA 用 `f[x][j]` 倍增，DFS 时顺手填表'],
        summary=['预处理 `O(n log n)`，每个询问 `O(log n)`',
                 '易错：两个 LCA 相同和不同必须分开处理，重叠的边不能算两次',
                 '求 LCA：先拉到同层，再从大步到小步一起往上跳，相同时不能跳（会跳过头）',
                 '原文已经是 Python 3 可运行的写法，代码未做改动',
                 '对比灵神：灵神用「三点两两距离和 ÷ 2」一行搞定，不用分情况；这里是手工分类讨论'],
    ),
)
