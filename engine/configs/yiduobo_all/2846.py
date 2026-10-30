# 示例树：0-1(3) 0-2(3) 1-3(5) 2-4(3) 2-5(5)
_POS = {0: (0.5, 0.0), 1: (0.25, 0.5), 2: (0.7, 0.5), 3: (0.25, 1.0), 4: (0.55, 1.0), 5: (0.9, 1.0)}
_EDGES = [(0, 1, 3), (0, 2, 3), (1, 3, 5), (2, 4, 3), (2, 5, 5)]
_PAR = {0: None, 1: 0, 2: 0, 3: 1, 4: 2, 5: 2}
_WC = {3: 'cyan', 5: 'orange'}


def _chain(v):
    r = []
    while v is not None:
        r.append(v)
        v = _PAR[v]
    return r


def _fmt(d):
    return '{' + ', '.join(f'权{k}:{c}' for k, c in sorted(d.items()) if c) + '}' if d and any(d.values()) else '{空}'


def _state(S):
    ln = S.get('_line', 0)
    inn = S.get('_inner', S)
    return ln, inn


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    W, H = x1 - x0 - 120, y1 - y0 - 130
    X = lambda v: x0 + 60 + _POS[v][0] * W
    Y = lambda v: y0 + 70 + _POS[v][1] * H
    cv.text((x0 + 18, y0 + 4), '树（边上的数字 = 边权，青 = 3，橙 = 5）', 22, T['muted'], bold=True)
    ln, inn = _state(S)
    depth = S.get('depth')
    seen = {v for v in range(6) if depth and depth[v] is not None}
    cur = inn.get('now') if 'fa' in inn and 'now' in inn else None
    inq = 'res' in S and 'lca' in S and 77 <= ln <= 85
    hit = set()
    marks = {}
    if inq and 'x' in S and 'y' in S:
        x, y, l = S['x'], S['y'], S['lca']
        hit = set(_chain(x)[:_chain(x).index(l) + 1]) | set(_chain(y)[:_chain(y).index(l) + 1]) if x != y else {x}
        marks = {x: 'blue', y: 'pink'}
        marks[l] = 'green'
        cv.text((x1 - 18, y0 + 4), f'询问 ({x}, {y})', 24, T['yellow'], anchor='ra', bold=True)
    for u, v, w in _EDGES:
        on = u in hit and v in hit
        cv.line([(X(u), Y(u)), (X(v), Y(v))], T['yellow'] if on else T['border'], 7 if on else 3)
        cv.text(((X(u) + X(v)) / 2 + 14, (Y(u) + Y(v)) / 2), w, 26, T[_WC[w]], anchor='lm', bold=True)
    for v in _POS:
        c = marks.get(v)
        cx, cy, r = X(v), Y(v), 32
        if c:
            fill = T[c]
        elif v in seen:
            fill = T['panel2']
        else:
            fill = (40, 46, 56)
        cv.rect((cx - r, cy - r, cx + r, cy + r), fill=fill, outline=T['yellow'] if v == cur else T['border'], width=5 if v == cur else 1, r=r)
        cv.text((cx, cy), v, 30, T['bg'] if c else (T['text'] if v in seen else T['dim']), anchor='mm', bold=True)
        if v in seen:
            cv.text((cx, cy + r + 8), f'深度 {depth[v]}', 18, T['dim'], anchor='mt')


def _info(S):
    ln, inn = _state(S)
    if 'cnt' not in S:
        return ''
    if 'path_cnt' in S and 78 <= ln <= 85 and 'x' in S:
        return f'路径边权计数 `path_cnt = {_fmt(S["path_cnt"])}`'
    now = inn.get('now') if 'fa' in inn else None
    if now is not None:
        return f'`cnt[{now}]` = 根到 {now} 的边权计数 `{_fmt(S["cnt"][now])}`'
    return ''


CONFIG = dict(
    num=2846, title='边权重均等查询', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='欧拉序 LCA + 根到点边权计数相减',
    tags=['灵神题单·常用数据结构', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def minOperationsQueries(self, n, edges, queries):
        g = {}
        for x, y, v in edges:
            if x not in g:
                g[x] = {}
            if y not in g:
                g[y] = {}
            g[x][y] = g[y][x] = v
        
        global pos
        pos = -1
        f = [None] * 65536
        depth = [None] * n
        first = [None] * n
        cnt = [{} for _ in range(n)]
        def add(node, left, right, pos, now):
            if left == right:
                f[node] = now
                return
            
            if f[node] is None or depth[f[node]] > depth[now]:
                f[node] = now
            mid = (left + right) >> 1
            if pos <= mid:
                add(node + node + 1, left, mid, pos, now)
            else:
                add(node + node + 2, mid + 1, right, pos, now)
        def dfs(now, fa):
            global pos
            pos += 1
            if depth[now] is None:
                if fa is None:
                    depth[now] = 0
                else:
                    depth[now] = depth[fa] + 1
                
                first[now] = pos
            
            add(0, 0, 32767, pos, now)
            for next in g.get(now, {}):
                if next != fa:
                    cnt[next] = cnt[now].copy()
                    cnt[next][g[now][next]] = cnt[next].get(g[now][next], 0) + 1
                    dfs(next, now)
                    pos += 1
                    add(0, 0, 32767, pos, now)
        def get(node, left, right, start, end):
            if left == start and right == end:
                return f[node]
            
            mid = (left + right) >> 1
            if end <= mid:
                return get(node + node + 1, left, mid, start, end)
            elif start > mid:
                return get(node + node + 2, mid + 1, right, start, end)
            else:
                left_res = get(node + node + 1, left, mid, start, mid)
                right_res = get(node + node + 2, mid + 1, right, mid + 1, end)
                if depth[left_res] < depth[right_res]:
                    return left_res
                else:
                    return right_res
        def get_lca(x, y):
            start = first[x]
            end = first[y]
            if start > end:
                start, end = end, start
            
            return get(0, 0, 32767, start, end)
        dfs(0, None)
        res = []
        for x, y in queries:
            if x == y:
                res.append(0)
                continue
            lca = get_lca(x, y)
            path_cnt = {}
            for v in cnt[x]:
                path_cnt[v] = cnt[x][v]
            for v in cnt[y]:
                path_cnt[v] = path_cnt.get(v, 0) + cnt[y][v]
            for v in cnt[lca]:
                path_cnt[v] -= cnt[lca][v] * 2
            res.append(depth[x] + depth[y] - depth[lca] * 2 - max(path_cnt.values()))
        
        return res
''',
    call='Solution().minOperationsQueries(6, [[0,1,3],[0,2,3],[1,3,5],[2,4,3],[2,5,5]], [[3,4],[4,5]])',
    expect=[1, 1],
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', fn=_info),
        dict(type='array', var='depth', label='depth', h=130, cell=70),
    ],
    watch=[('now', 'now', 'yellow'), ('x', lambda S: S['x'] if S.get('_line', 0) >= 73 else '-', 'blue'), ('y', lambda S: S['y'] if S.get('_line', 0) >= 73 else '-', 'pink'), ('lca', lambda S: S['lca'] if S.get('_line', 0) >= 78 and 'lca' in S else '-', 'green'), ('res', 'res', 'orange')],
    captions={
        'pos = -1': '`pos` 是欧拉序的当前位置：进入一个点、从子树回来都算一格',
        'f = [None] * 65536': '`f` 是线段树：每个区间存「欧拉序里深度最小的点」，区间最小 = 这段的 ==lca==',
        'first = [None]': '`first[v]`：点 v 在欧拉序里第一次出现的位置',
        'cnt = [{}': '`cnt[v]`：==根到 v 的路径==上每种边权出现几次（哈希表）',
        'pos += 1': lambda S, B, r: (f'进入点 `{S.now}`，欧拉序位置 `pos = {S.pos}`' if S.get('_line') == 31 else f'从子树 `{S.next}` 回到 `{S.now}`，又记一格：`pos = {S.pos}`'),
        'if depth[now] is None': lambda S, B, r: ('第一次到 `{}`：要记深度和 `first`'.format(S.now) if S.depth[S.now] is None else f'`{S.now}` 已经来过'),
        'depth[now] = 0': '进入根 `0`：深度 0',
        'depth[now] = depth[fa] + 1': '进入点 `{now}`：`depth[{now}] = depth[{fa}] + 1 = {depth[now]}`',
        'first[now] = pos': '`first[{now}] = {first[now]}`：点 {now} 首次出现在欧拉序第 {first[now]} 格（回溯时 `pos` 也会再加一格）',
        'for next in g.get': '遍历 `{now}` 的邻居',
        'if next != fa': lambda S, B, r: (f'邻居 `{S.next}` 是父亲 → 不回头' if S.next == S.fa else f'邻居 `{S.next}` 是孩子 → 往下走'),
        'cnt[next] = cnt[now].copy()': '孩子 `{next}` 先继承 `{now}` 的计数',
        'cnt[next][g[now][next]] =': '孩子 `{next}` 复制 `{now}` 的计数，再把边 `{now}-{next}` 的权 `{g[now][next]}` 计一次 → `cnt[{next}] = {cnt[next]}`',
        'dfs(next, now)': '递归进入孩子 `{next}`',
        'dfs(0, None)': '从根 0 开始 DFS：一路建欧拉序、深度和 `cnt`',
        'for x, y in queries': lambda S, B, r: (f'询问 `({S.x}, {S.y})`' if S.get('_line') == 73 and S.get('res') is not None and len(S.res) < 2 else '询问处理完了'),
        'if x == y': lambda S, B, r: ('`x == y`：路径长 0，答案 0' if S.x == S.y else f'询问 `({S.x}, {S.y})`：两点不同，要找 lca'),
        'lca = get_lca(x, y)': '求 lca：欧拉序区间 `[first[{x}], first[{y}]]` 里==深度最小==的点（线段树区间查询）',
        'path_cnt = {}': '==lca== 是点 `{lca}`；`path_cnt` 清空，准备累加路径上的边权',
        'for v in cnt[x]': '加上 `cnt[{x}]`（根到 x）',
        'path_cnt[v] = cnt[x][v]': '`path_cnt[{v}] = {path_cnt[v]}`',
        'for v in cnt[y]': '再加上 `cnt[{y}]`（根到 y）',
        'path_cnt[v] = path_cnt.get': '`path_cnt[{v}] = {path_cnt[v]}`',
        'for v in cnt[lca]': '根到 lca 这段被算了两次 → 减去 `2 × cnt[{lca}]`',
        'path_cnt[v] -= ': '`path_cnt[{v}]` 减 `2 × {cnt[lca][v]}` → {path_cnt[v]}',
        'res.append(depth[x]': lambda S, B, r: f'路径长 `{S.depth[S.x]} + {S.depth[S.y]} - 2×{S.depth[S.lca]} = {S.depth[S.x] + S.depth[S.y] - 2 * S.depth[S.lca]}`，最多的边权占 `{max(S.path_cnt.values())}` 条 → ==改 {S.res[-1]} 条==',
        'return res': '返回 `{res}`',
    },
    skip=[31, 32, 33, 41, 42, 43, 46, 79, 81, 83, 3, 4, 5, 6, 7, 8, 9, 11, 13, 14, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 40, 47, 49, 50, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63, 65, 66, 67, 68, 70, 72, 74, 75, 76],
    max_steps=80,
    cards=dict(
        one_liner='欧拉序求 lca，根到点的边权计数相减得路径计数',
        complexity='时间 `O(n·U + q·(log n + U))`，空间 `O(n·U)`，`U = 26`',
        problem=['树上每条边有权（1..26）；询问 `(x, y)`：改最少的边，让 `x` 到 `y` 路径上边权全相等',
                 '答案 = 路径长 - 路径上出现最多的边权条数',
                 '示例：6 个点的树，`[[3,4],[4,5]]` → `[1, 1]`'],
        quote='受到计算路径长度方法的启发，注意到本题中边权的取值范围只有26种，那么就可以对每个节点使用一个哈希表记录根节点到当前节点路径中每种边权出现的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['lca 偷懒用欧拉序 + 线段树：`first[x]..first[y]` 区间里深度最小的点',
              'DFS 时 `cnt[孩子]` = `cnt[父亲]` 复制后再加这条边的权',
              '路径计数 = `cnt[x] + cnt[y] - 2·cnt[lca]`，取最大值即可'],
        summary=['路径长 `depth[x] + depth[y] - 2·depth[lca]`，减去最多边权的条数',
                 '易错：`x == y` 时路径为空，`max` 会报错，要先特判返回 0',
                 '原文是 Python 2 风格，本题代码无需改动，直接可在 Python 3 运行',
                 '对比灵神：灵神用倍增维护 2^i 步路径的计数；yiduobo 用根到点的前缀计数相减（求最大值不适用）'],
    ),
)
