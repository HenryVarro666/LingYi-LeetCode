EDGES = [[0, 1, 3], [1, 2, 3], [1, 3, 3], [3, 4, 3]]
SPEED = 3
POS = {0: (0.1, 0.12), 2: (0.1, 0.88), 1: (0.36, 0.5), 3: (0.65, 0.5), 4: (0.92, 0.5)}
_ADJ = {}
for _a, _b, _w in EDGES:
    _ADJ.setdefault(_a, []).append((_b, _w))
    _ADJ.setdefault(_b, []).append((_a, _w))


def _dists(c):
    """从 c 出发：每个点的 (距离, 所在分支的邻居)"""
    d = {c: (0, None)}
    st = [c]
    while st:
        x = st.pop()
        for y, w in _ADJ[x]:
            if y not in d:
                d[y] = (d[x][0] + w, y if x == c else d[x][1])
                st.append(y)
    return d


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '服务器树（边上是权值；蓝 = 中间点 c，绿 = 到 c 的距离是 %d 的倍数）' % SPEED, 22, T['muted'], bold=True)
    w, h = x1 - x0 - 120, y1 - y0 - 140
    P = {k: (x0 + 60 + v[0] * w, y0 + 80 + v[1] * h) for k, v in POS.items()}
    c = S.get('i')
    inner = S.get('_inner', {})
    cur = inner.get('x') if 'fa' in inner else None
    dd = _dists(c) if isinstance(c, int) and c in P else {}
    branch_cols = [T['pink'], T['orange'], T['purple'], T['cyan']]
    nb = [y for y, _ in _ADJ[c]] if dd else []
    for a, b, wt in EDGES:
        (xa, ya), (xb, yb) = P[a], P[b]
        cv.line([(xa, ya), (xb, yb)], T['border'], 4)
        cv.text(((xa + xb) / 2, (ya + yb) / 2 - 14), wt, 22, T['yellow'], anchor='mb', bold=True)
    for k, (px, py) in P.items():
        fill, tc, ring = T['panel2'], T['text'], None
        if dd:
            dist, br = dd[k]
            if k == c:
                fill, tc = T['blue'], T['bg']
            else:
                ring = branch_cols[nb.index(br) % 4]
                if dist % SPEED == 0:
                    fill, tc = T['green'], T['bg']
        r = 30
        if ring:
            cv.d.ellipse((px - r - 5, py - r - 5, px + r + 5, py + r + 5), outline=ring, width=4)
        cv.d.ellipse((px - r, py - r, px + r, py + r), fill=fill, outline=T['border'])
        if k == cur:
            cv.d.ellipse((px - r - 10, py - r - 10, px + r + 10, py + r + 10), outline=T['yellow'], width=5)
        cv.text((px, py), k, 30, tc, anchor='mm', bold=True)
        if dd and k != c:
            cv.text((px, py + r + 10), 'd=%d' % dd[k][0], 20, T['muted'], anchor='mt', mono=True)


def _t(S):
    if 'i' in S and 's' in S and 'fa' not in S.get('_inner', {}):
        return f"中间点 ==%d==：前面各子树共有 `s = %d` 个可连接点" % (S['i'], S['s'])
    return ''


CONFIG = dict(
    num=3067, title='在带权树网络中统计可连接服务器对数目', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举中间点 · DFS 数子树 · 乘法原理', tags=['数学算法', '链表树与回溯', '难度分 1909'],
    code='''
# 更快的写法见【Python3 写法二】
class Solution:
    def countPairsOfConnectableServers(self, edges: List[List[int]], signalSpeed: int) -> List[int]:
        n = len(edges) + 1
        g = [[] for _ in range(n)]
        for x, y, wt in edges:
            g[x].append((y, wt))
            g[y].append((x, wt))

        def dfs(x: int, fa: int, s: int) -> int:
            cnt = 0 if s % signalSpeed else 1
            for y, wt in g[x]:
                if y != fa:
                    cnt += dfs(y, x, s + wt)
            return cnt

        ans = [0] * n
        for i, gi in enumerate(g):
            if len(gi) == 1:
                continue
            s = 0
            for y, wt in gi:
                cnt = dfs(y, i, wt)
                ans[i] += cnt * s
                s += cnt
        return ans
''',
    call='Solution().countPairsOfConnectableServers(%r, %d)' % (EDGES, SPEED),
    expect=[0, 5, 0, 3, 0],
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var='ans', h=150, label='ans', pointers={'i': 'blue'}, cell=70),
        dict(type='calls', h=160, hide=('countPairsOfConnectableServers',)),
    ],
    watch=['i', ('s', 's', 'cyan'), ('cnt', 'cnt', 'green')],
    skip=['n = len(edges)', 'for x, y, wt in edges', 'g = [[]', 'g[x].append', 'g[y].append', 'ans = [0]'],
    max_steps=68,
    captions={
        'for i, gi in enumerate(g)': '枚举中间点 `c = {i}`：把它当作树根，邻居有 `{len(gi)}` 个，各自是一棵子树',
        'if len(gi) == 1': lambda S, B, r: (f'`{S.i}` 只有一个邻居（叶子）：两点路径必有公共边 → 答案 0，跳过' if len(S.gi) == 1 else f'`{S.i}` 有 `{len(S.gi)}` 个邻居，可以分到不同子树 → 需要计算'),
        's = 0': '`s`：已处理的几棵子树里，距离是 `signalSpeed` 倍数的点数（先清零）',
        'cnt = dfs(y, i, wt)': '进入邻居 `{y}` 的子树，数出里面距 `{i}` 是 `{signalSpeed}` 倍数的点',
        'ans[i] += cnt * s': '乘法原理：这棵子树的 `{cnt}` 个点 × 之前子树的 `{s}` 个点（不同子树，路径无公共边）→ `ans[{i}]` = =={ans[i]}==',
        's += cnt': '把这棵子树的 `{cnt}` 个点并入 `s` → =={s}==，留给后面的子树去配对',
        'cnt = 0 if s % signalSpeed else 1': '到 `c` 的距离 `s = {s}`，`{s} % {signalSpeed} = {s % signalSpeed}` → ' + '距离是倍数才算 1 个',
        'cnt += dfs(y, x, s + wt)': '往下走到 `{y}`：距离变成 `{s} + {wt} = {s + wt}`，`fa = {x}` 防止走回头路',
        'return cnt': '这棵子树（以 `{x}` 为根）里共有 `{cnt}` 个合格点，返回给上一层',
        'return ans': '每个点作中间点的可连接点对数：`{ans}`',
    },
    cards=dict(
        one_liner='枚举中间点 c，不同子树里的“距离倍数点”两两配对',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['无根带权树，`n` 个服务器，给定 `signalSpeed`',
                 '`a`、`b` 通过 `c` 可连接：`c` 到两点距离都是 `signalSpeed` 的倍数，且两条路径无公共边',
                 '求每个 `c` 的可连接点对数；示例：本视频：`signalSpeed = 3`，`[0,5,0,3,0]`'],
        quote='枚举服务器 c，作为树的根，按照下图计算。优化：如果 c 只有一个邻居，则答案为 0，不调用 dfs。',
        quote_src='—— 灵茶山艾府题解',
        idea=['以 `c` 为根：两点路径无公共边 ⇔ 它们在 ==不同的子树==',
              '`dfs` 数出每棵子树里到 `c` 距离是倍数的点数 `cnt`',
              '依次处理子树：`ans[c] += cnt * s`，再 `s += cnt`，这样每对只算一次'],
        summary=['时间 `O(n^2)`：每个中间点最多遍历整棵树；空间 `O(n)`',
                 '易错：`dfs(y, i, wt)` 的初始距离是边权 `wt`，不是 0',
                 '易错：先 `ans[i] += cnt * s` 再 `s += cnt`，顺序反了会多算',
                 '叶子只有一个邻居，直接跳过；另有 `@cache` 加取模的写法二'],
    ),
)
