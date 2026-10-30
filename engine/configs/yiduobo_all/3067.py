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
    c = S.get('root')
    inner = S.get('_inner', {})
    cur = inner.get('now') if 'fa' in inner else None
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


CONFIG = dict(
    num=3067, title='在带权树网络中统计可连接服务器对数目', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='枚举中间点 · DFS 数点 · tot 累加', tags=['数学算法', '链表树与回溯', '难度分 1909'],
    code='''
class Solution(object):
    def countPairsOfConnectableServers(self, edges, signalSpeed):

        g = {}
        for x, y, w in edges:
            if x not in g:
                g[x] = {}
            if y not in g:
                g[y] = {}
            g[x][y] = g[y][x] = w
        

        def dfs(now, fa, dis):
            cnt = 0
            if dis % signalSpeed == 0:
                cnt += 1
            for child in g[now]:
                if child != fa:
                    cnt += dfs(child, now, dis + g[now][child])
            
            return cnt

        n = len(edges) + 1
        res = [0] * n
        for root in range(n):
            tot = 0
            for child in g[root]:
                cnt = dfs(child, root, g[root][child])
                res[root] += tot * cnt
                tot += cnt
        
        return res
''',
    call='Solution().countPairsOfConnectableServers(%r, %d)' % (EDGES, SPEED),
    expect=[0, 5, 0, 3, 0],
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var='res', h=150, label='res', pointers={'root': 'blue'}, cell=70),
        dict(type='calls', h=160, hide=('countPairsOfConnectableServers',)),
    ],
    watch=['root', ('tot', 'tot', 'cyan'), ('cnt', 'cnt', 'green')],
    skip=['g = {}', 'for x, y, w in edges', 'if x not in g', 'if y not in g', 'g[x] = {}', 'g[y] = {}', 'g[x][y] = g[y][x] = w',
          'n = len(edges)', 'res = [0] * n', 'cnt = 0', 'cnt += 1'],
    max_steps=68,
    captions={
        'for root in range': '把 `{root}` 当作中间点 `c`（树根）：它的每个邻居是一棵子树',
        'tot = 0': '`tot`：已经数过的子树里，距离是 `{signalSpeed}` 倍数的点的总数，先清零',
        'for child in g[root]': '`root = {root}`：取下一个邻居 `child = {child}`' ,
        'cnt = dfs(child, root, g[root][child])': '从邻居 `{child}` 出发数这棵子树，起始距离是边权 `{g[root][child]}`',
        'res[root] += tot * cnt': '这棵子树 `{cnt}` 个点 × 前面子树 `{tot}` 个点 → `res[{root}]` = =={res[root]}==（只算新子树与旧子树的配对，不重复）',
        'tot += cnt': '把 `{cnt}` 并进 `tot` = =={tot}==，留给后面的子树去配对',
        'if dis % signalSpeed == 0': lambda S, B, r: f'`{S.now}` 到根的距离 `dis = {S.dis}`，`{S.dis} % {S.signalSpeed} = {S.dis % S.signalSpeed}` → ' + ('==是倍数，计 1 个==' if S.dis % S.signalSpeed == 0 else '不是倍数，不计'),
        'cnt += dfs(child, now, dis + g[now][child])': '继续往下：到 `{child}` 的距离 = `{dis} + {g[now][child]}` = {dis + g[now][child]}',
        'return cnt': '以 `{now}` 为根的这部分共有 `{cnt}` 个合格点，返回',
        'return res': '最终 `res = {res}`',
    },
    cards=dict(
        one_liner='根不同子树的点配对：当前子树点数 × tot，再累加 tot',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['无根带权树，给定 `signalSpeed`，`c` 到 `a`、`b` 的距离都是它的倍数',
                 '且 `c→a` 和 `c→b` 两条路径没有公共边，`a < b`',
                 '求每个服务器作 `c` 时的点对数；本视频：`signalSpeed = 3`，`[0,5,0,3,0]`'],
        quote='如果将 c 视为树的根节点，那么 a 和 b 就必须处在不同的子树中。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据规模不大，==逐个枚举中间点 c==，不用预处理',
              '`dfs` 数出 c 的每个孩子子树里，距离是倍数的点数 `cnt`',
              '`tot` 记录已遍历子树的合格点数，`cnt * tot` 累加到 `res[c]`，再 `tot += cnt`，避免重复'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '`dfs` 里 `fa` 防止走回头路；起始距离是 `g[root][child]`',
                 '对比灵神：yiduobo 用字典存图，灵神用邻接表并跳过叶子（只有一个邻居）',
                 '原文是 Python 3 可直接运行的写法，没有改动'],
    ),
)
