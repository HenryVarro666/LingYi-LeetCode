def _root(S, v):
    fa = S.get('fa')
    if not fa:
        return -1
    while fa[v] != v:
        v = fa[v]
    return v


def _color(S, i, j, v):
    if 'fa' in S:                      # 并查集阶段
        n = len(S['dis'])
        d = S.get('d')
        if d is None or v < d:
            return None
        r = _root(S, i * n + j)
        if r == _root(S, 0):
            return 'blue'
        if r == _root(S, n * n - 1):
            return 'pink'
        return 'green'
    return 'cyan' if v == 0 else None  # BFS 阶段：小偷 = 0


def _dim(S, i, j, v):
    if 'fa' in S:
        return S.get('d') is not None and v < S['d']
    return v < 0


def _union_txt(S):
    if 'fa' not in S or 'd' not in S:
        return ''
    n = len(S['dis'])
    same = _root(S, 0) == _root(S, n * n - 1)
    return f"安全系数 `d = {S['d']}`：`dis ≥ {S['d']}` 的格子（亮）已连成块；左上 ==蓝==、右下 ==粉==，{'==已连通，答案就是 d==' if same else '还没连通'}"


CONFIG = dict(
    num=2812, title='找出最安全路径', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='多源 BFS + 从大到小并查集', tags=['灵神题单·二分算法', '难度分 2154'],
    code='''
class Solution:
    def maximumSafenessFactor(self, grid: List[List[int]]) -> int:
        n = len(grid)
        dis = [[-1] * n for _ in range(n)]
        q = []
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                if x == 1:
                    dis[i][j] = 0
                    q.append((i, j))

        groups = [q]
        # 多源 BFS
        while q:  
            tmp = q
            q = []
            for i, j in tmp:
                for x, y in (i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1):
                    if 0 <= x < n and 0 <= y < n and dis[x][y] < 0:
                        dis[x][y] = len(groups)
                        q.append((x, y))
            groups.append(q)  # 相同 dis 分组记录

        # 并查集模板
        fa = list(range(n * n))
        def find(x: int) -> int:
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        # 从大到小枚举答案
        for d in range(len(groups) - 2, 0, -1):
            for i, j in groups[d]:
                for x, y in (i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1):
                    if 0 <= x < n and 0 <= y < n and dis[x][y] >= d:
                        fa[find(x * n + y)] = find(i * n + j)
            if find(0) == find(n * n - 1):  # 写这里判断更快些
                return d
        return 0
''',
    call='Solution().maximumSafenessFactor([[0,0,1],[0,0,0],[0,0,0]])',
    expect=2, max_steps=130,
    skip=['n = len(grid)', 'groups = [q]', 'tmp = q', 'q = []', 'fa = list(range', 'def find', 'for i, row in enumerate', 'for j, x in enumerate', 'if x == 1', 'for i, j in tmp', 'for x, y in', 'q.append', 'groups.append', 'dis[x][y] < 0', 'fa[x] != x', 'return fa[x]', 'fa[x] = find(fa[x])'],
    views=[
        dict(type='table', var='dis', h=380, cell=96,
             label='dis[i][j]：到最近小偷的距离（青 = 小偷；黄 = 当前格；粉 = 邻居）',
             cursors=[('i', 'j', 'yellow', '(i,j)'), ('x', 'y', 'pink', '邻')],
             color=_color, dim=_dim),
        dict(type='text', h=90, fn=lambda S: _union_txt(S) or (f"`groups` 已有 {len(S['groups'])} 组：第 k 组 = 距离恰为 k 的格子" if 'groups' in S else '')),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), ('d', 'd', 'green'), ('groups', 'len(groups)', 'cyan')],
    captions={
        'dis = [[-1]': '`dis[i][j]` = 到最近小偷的距离，先全设 `-1`（还没算到）。`groups[k]` 将存距离恰为 k 的格子',
        'dis[i][j] = 0': '`({i},{j})` 是小偷：距离 0，==作为 BFS 的起点==入队',
        'groups = [q]': '`groups[0]` = 所有小偷：距离为 0 的一组',
        'while q': lambda S, B, r: (f'这一层有 `{len(S.q)}` 个格子，一起向四周扩一步（扩完存入 `groups`）' if S.q else '队列空了：全图的 `dis` 都算好了'),
        'dis[x][y] = len': '从 `({i},{j})` 扩到邻居 `({x},{y})`：它离小偷 ==`{dis[x][y]}`== 步（比上一层多一步），入队',
        'for d in range': '从大到小试安全系数 `d = {d}`：只用 `dis ≥ {d}` 的格子，起点终点连得上吗？',
        'for i, j in groups[d]': lambda S, B, r: f'加入距离恰为 `{S.d}` 的格子 `({S.i},{S.j})`，和周围 `≥ {S.d}` 的格子相连',
        'if 0 <= x < n and 0 <= y < n and dis[x][y] >= d': lambda S, B, r: (f'邻居 `({S.x},{S.y})` 的 `dis = {S.dis[S.x][S.y]} ≥ {S.d}` → ==合并==' if (0 <= S.x < S.n and 0 <= S.y < S.n and S.dis[S.x][S.y] >= S.d)
                                                                      else f'邻居 `({S.x},{S.y})` 越界或 `dis < {S.d}`，不连'),
        'fa[find(x': '合并：邻居 `({B.x},{B.y})` 所在的块并入 `({i},{j})` 所在的块',
        'if find(0)': lambda S, B, r: ('`(0,0)` 与 `(n-1,n-1)` ==连通== → 安全系数 d 可行；d 从大往小，第一个可行的就是最大值' if r is None and False else
                                      f'`(0,0)` 和 `({S.n - 1},{S.n - 1})` 是否连通？当前 `d = {S.d}`'),
        'return d': '第一次连通时的 `d = {d}` 就是最大安全系数 → ==返回 {d}==',
    },
    cards=dict(
        one_liner='先多源 BFS 算每格离小偷多远，再从大到小用并查集连格子',
        complexity='时间 `O(n²)`（并查集近似 `O(1)`），空间 `O(n²)`',
        problem=['`n×n` 网格，`1` 是小偷。路径安全系数 = 路径上各格到最近小偷的最小曼哈顿距离',
                 '求从 `(0,0)` 到 `(n-1,n-1)` 的最大安全系数',
                 '示例：`[[0,0,1],[0,0,0],[0,0,0]]` → `2`'],
        quote='从大到小枚举安全系数。假设安全系数为 d，那么把所有 dis[i][j] ≥ d 的格子与其四周 ≥ d 的格子用并查集连起来。如果 (0, 0) 和 (n-1, n-1) 连通，那么答案为 d。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dis[i][j]` 用从所有小偷出发的多源 BFS 算出，同时按距离分组存进 `groups`',
              '`d` 从大到小：只把「距离恰为 d」的格子增量加入，和周围 `≥ d` 的格子合并',
              '起点终点第一次连通时，当前 `d` 就是答案'],
        summary=['时间 `O(n²)`（按秩合并后并查集均摊 `O(1)`），空间 `O(n²)`',
                 '`groups` 分组避免每个 `d` 都扫全图，所以是增量合并',
                 '枚举从 `len(groups)-2` 开始：最后一组是空队列；到 1 为止，剩下就是 0',
                 '起点或终点本身有小偷时，要到 `d=0` 才连通，直接返回 0',
                 '另一种做法：二分 `d` + BFS 判断连通（见 yiduobo）'],
    ),
)
