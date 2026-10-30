# 示例树：0-1(1) 0-4(2) 1-2(1) 1-3(2) 4-5(2)
_POS = {0: (0.5, 0.0), 1: (0.25, 0.5), 4: (0.75, 0.5), 2: (0.1, 1.0), 3: (0.4, 1.0), 5: (0.75, 1.0)}
_EDGES = [(0, 1, 1), (0, 4, 2), (1, 2, 1), (1, 3, 2), (4, 5, 2)]
_WC = {1: 'cyan', 2: 'orange'}


def _anc(par, v):
    r = []
    while v != -1:
        r.append(v)
        v = par[v]
    return r


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    W, H = x1 - x0 - 120, y1 - y0 - 150
    X = lambda v: x0 + 60 + _POS[v][0] * W
    Y = lambda v: y0 + 70 + _POS[v][1] * H
    cv.text((x0 + 18, y0 + 4), '树（边上的数字 = 边权，青 = 1，橙 = 2）', 22, T['muted'], bold=True)
    depth = S.get('depth')
    ln = S.get('_line', 0)
    q = S.get('queries')
    qa = qb = None
    idx = len(S['ans']) - (1 if ln == 54 else 0) if 'ans' in S else None
    if idx is not None and q is not None and 0 <= idx < len(q) and 30 <= ln <= 54:
        qa, qb = q[idx]
    hit = set()
    if qa is not None and ln >= 52:
        pa = S['pa']
        A, Bn = _anc([r[0] for r in pa], qa), _anc([r[0] for r in pa], qb)
        common = [v for v in A if v in Bn][0]
        hit = set(A[:A.index(common) + 1]) | set(Bn[:Bn.index(common) + 1])
    for u, v, w in _EDGES:
        on = u in hit and v in hit
        cv.line([(X(u), Y(u)), (X(v), Y(v))], T['yellow'] if on else T['border'], 7 if on else 3)
        cv.text(((X(u) + X(v)) / 2 + 14, (Y(u) + Y(v)) / 2), w, 26, T[_WC[w]], anchor='lm', bold=True)
    cur = {}
    if 'x' in S and 'y' in S and qa is not None:
        cur = {S['x']: 'blue', S['y']: 'pink'}
        if 'lca' in S and ln >= 52:
            cur[S['lca']] = 'green'
    for v, (px, py) in _POS.items():
        c = cur.get(v)
        cx, cy = X(v), Y(v)
        r = 32
        cv.rect((cx - r, cy - r, cx + r, cy + r), fill=T[c] if c else T['panel2'], outline=T['border'], r=r)
        cv.text((cx, cy), v, 30, T['bg'] if c else T['text'], anchor='mm', bold=True)
        if depth and depth[v] is not None and any(depth) or v == 0:
            cv.text((cx, cy + r + 8), f'深度 {depth[v]}' if depth else '', 18, T['dim'], anchor='mt')
    if qa is not None:
        cv.text((x1 - 18, y0 + 4), f'询问 ({qa}, {qb})', 24, T['yellow'], anchor='ra', bold=True)


def _cw_txt(S):
    cw = S.get('cw')
    if cw is None or not (30 <= S.get('_line', 0) <= 54):
        return ''
    items = [f'权{k + 1}:{c}' for k, c in enumerate(cw) if c]
    return f'路径上边权计数 `cw = {{{", ".join(items) if items else "空"}}}`　路径长 `path_len = {S.get("path_len", "?")}`'


CONFIG = dict(
    num=2846, title='边权重均等查询', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='树上倍增 + 边权计数',
    tags=['灵神题单·常用数据结构', '灵神题单·链表树与回溯'],
    code='''
class Solution:
    def minOperationsQueries(self, n: int, edges: List[List[int]], queries: List[List[int]]) -> List[int]:
        g = [[] for _ in range(n)]
        for x, y, w in edges:
            g[x].append((y, w - 1))
            g[y].append((x, w - 1))
        m = n.bit_length()
        pa = [[-1] * m for _ in range(n)]
        cnt = [[[0] * 26 for _ in range(m)] for _ in range(n)]
        depth = [0] * n
        def dfs(x: int, fa: int) -> None:
            pa[x][0] = fa
            for y, w in g[x]:
                if y != fa:
                    cnt[y][0][w] = 1
                    depth[y] = depth[x] + 1
                    dfs(y, x)
        dfs(0, -1)
        # 倍增模板
        for i in range(m - 1):
            for x in range(n):
                p = pa[x][i]
                if p != -1:
                    pp = pa[p][i]
                    pa[x][i + 1] = pp
                    for j, (c1, c2) in enumerate(zip(cnt[x][i], cnt[p][i])):
                        cnt[x][i + 1][j] = c1 + c2
        ans = []
        for x, y in queries:
            path_len = depth[x] + depth[y]  # 最后减去 depth[lca] * 2
            cw = [0] * 26
            if depth[x] > depth[y]:
                x, y = y, x
            # 使 y 和 x 在同一深度
            k = depth[y] - depth[x]
            for i in range(k.bit_length()):
                if (k >> i) & 1:  # k 二进制从低到高第 i 位是 1
                    p = pa[y][i]
                    for j, c in enumerate(cnt[y][i]):
                        cw[j] += c
                    y = p
            if y != x:
                for i in range(m - 1, -1, -1):
                    px, py = pa[x][i], pa[y][i]
                    if px != py:
                        for j, (c1, c2) in enumerate(zip(cnt[x][i], cnt[y][i])):
                            cw[j] += c1 + c2
                        x, y = px, py  # 同时上跳 2^i 步
                for j, (c1, c2) in enumerate(zip(cnt[x][0], cnt[y][0])):
                    cw[j] += c1 + c2
                x = pa[x][0]
            lca = x
            path_len -= depth[lca] * 2
            ans.append(path_len - max(cw))
        return ans
''',
    call='Solution().minOperationsQueries(6, [[0,1,1],[0,4,2],[1,2,1],[1,3,2],[4,5,2]], [[2,5],[3,4]])',
    expect=[2, 1],
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', fn=_cw_txt),
        dict(type='array', var='depth', label='depth', h=130, cell=70),
    ],
    watch=['m', ('x', 'x', 'blue'), ('y', 'y', 'pink'), ('k', 'k', 'yellow'), ('lca', 'lca', 'green'), ('ans', 'ans', 'orange')],
    captions={
        'g = [[]': '建邻接表：`g[x]` 存 `(邻居, 边权 - 1)`，边权 1..26 映射到下标 0..25',
        'm = n.bit_length()': '`m = n.bit_length() = {m}`：最多往上跳 `2^(m-1)` 步，倍增表有 `m` 列',
        'pa = [[-1]': '`pa[x][i]`：`x` 的第 `2^i` 个祖先；`cnt[x][i][j]`：这段路径上边权 `j+1` 的个数',
        'cnt[y][0][w] = 1': '点 `{y}` 到父亲 `{x}` 的边权是 `{w + 1}` → `cnt[{y}][0]` 里权 {w + 1} 计 1；深度 `depth[{y}] = {depth[x] + 1}`',
        'dfs(0, -1)': '从根 0 出发 DFS：填好 `pa[·][0]`、`cnt[·][0]`、`depth`',
        'for i in range(m - 1)': '倍增：已知 `2^{i}` 级祖先，推 `2^{i+1}` 级（`i = {i}`）',
        'pa[x][i + 1] = pp': '`pa[{x}][{i + 1}] = pa[{p}][{i}] = {pp}`；同时 `cnt[{x}][{i + 1}] = cnt[{x}][{i}] + cnt[{p}][{i}]`（两段边权计数相加）',
        'for x, y in queries': lambda S, B, r: (f'询问 `({S.x}, {S.y})`：求路径上最多的边权有几条' if len(S.ans) < len(S.queries) else '询问都处理完了'),
        'path_len = depth': '路径长 = `depth[x] + depth[y] - 2·depth[lca]`；先记 `{path_len}`，等找到 lca 再减',
        'if depth[x] > depth[y]': lambda S, B, r: (f'`depth[x] = {S.depth[S.x]}` > `depth[y] = {S.depth[S.y]}` → 交换，保证 `y` 更深' if S.depth[S.x] > S.depth[S.y]
                                                    else f'`depth[x] = {S.depth[S.x]} ≤ depth[y] = {S.depth[S.y]}`：`y` 已经不浅于 `x`'),
        'k = depth[y] - depth[x]': lambda S, B, r: (f'`y` 比 `x` 深 `k = {S.k}` 层，要先把 `y` 上跳 `k` 步对齐（`k` 的每个二进制 1 位跳一次）' if S.k else '`k = 0`：两点深度相同，不用对齐'),
        'if (k >> i) & 1': lambda S, B, r: (f'`k` 的第 {S.i} 位是 1 → 上跳 `2^{S.i}` 步' if (S.k >> S.i) & 1 else f'`k` 的第 {S.i} 位是 0 → 不跳'),
        'p = pa[y][i]': '`y = {y}` 上跳 `2^{i}` 步到 `{p}`，途中的边权计数加进 `cw`',
        41: '`y` → {y}；这段的边权计数已加进 `cw`',
        'if y != x': lambda S, B, r: ('`y == x`：对齐后重合，`x` 就是 lca' if S.y == S.x else f'对齐后 `y = {S.y} ≠ x = {S.x}`：还要一起往上找 lca'),
        'px, py = pa[x][i], pa[y][i]': '试同时上跳 `2^{i}` 步：`px = {px}`，`py = {py}`',
        'if px != py': lambda S, B, r: (f'`{S.px} ≠ {S.py}`：还没到 lca（或越过了根）→ 可以跳' if S.px != S.py else f'`px = py = {S.px}`：跳过头了（那是 lca 或更高）→ 不跳'),
        'x, y = px, py': '`px ≠ py` → 两边同时上跳 `2^{i}` 步：`x = {x}`，`y = {y}`；两段边权计数都加进 `cw`',
        'x = pa[x][0]': '`x` 与 `y` 的父亲相同 → 再各走一步（边权已加）：`lca = x = {x}`',
        'path_len -= depth[lca] * 2': '路径长 `path_len = {path_len}`',
        'ans.append': '路径长 `{path_len}`（= depth[a] + depth[b] - 2·depth[lca]）减出现最多的边权条数 `{max(cw)}` = ==改 {path_len - max(cw)} 条==',
        'return ans': '返回 `{ans}`',
    },
    skip=['cw = [0] * 26', 'path_len -= depth', 'for i in range(k.bit_length())', 'for i in range(m - 1, -1, -1)', 'x, y = y, x', 'depth[y] = depth[x] + 1', 'lca = x', 'for x, y, w in edges', 'g[x].append', 'g[y].append', 'depth = [0] * n', 'pa[x][0] = fa', 'for y, w in g[x]', 'if y != fa', 'dfs(y, x)',
          'for x in range(n)', 'p = pa[x][i]', 'if p != -1', 'pp = pa[p][i]', 'for j, ', 'cnt[x][i + 1][j]', 'cw[j] +=', 'continue', 'ans = []'],
    max_steps=80,
    cards=dict(
        one_liner='倍增求 lca 的同时，把路径上每种边权的条数一起带上',
        complexity='时间 `O((n + q)·U·log n)`，空间 `O(n·U·log n)`，`U = 26`',
        problem=['一棵树，每条边有权 `w`（1..26）；每次询问 `(a, b)`，一次操作可把任意一条边改成任意权',
                 '求让路径上所有边权相等的最少操作次数；示例：6 个点的树，`[[2,5],[3,4]]` → `[2, 1]`'],
        quote='由于 1≤w≤26，我们可以在倍增的同时，维护从节点 x 到 x 的第 2^i 个祖先节点这条路径上的每种边权的个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['答案 = 路径长 - 路径上出现最多的边权的条数',
              '`cnt[x][i]` 是长度 26 的数组：`x` 往上 `2^i` 步这段里每种权各多少条，倍增时两段直接相加',
              '询问时先上跳对齐深度，再从大到小同时上跳找 lca，沿途把计数累加进 `cw`'],
        summary=['路径长 `depth[a] + depth[b] - 2·depth[lca]`，这里 lca 最后才知道，所以先加后减',
                 '易错：同时上跳结束后 `x`、`y` 还差一条边，要再把 `cnt[·][0]` 加进去，再取父亲；边权用 `w - 1` 做下标'],
    ),
)
