def _tidy(children, root=0):
    pos = {}
    cnt = [0]
    md = [0]

    def go(u, d):
        md[0] = max(md[0], d)
        ks = children[u]
        if not ks:
            x = cnt[0]
            cnt[0] += 1
        else:
            for k in ks:
                go(k, d + 1)
            x = (pos[ks[0]][0] + pos[ks[-1]][0]) / 2
        pos[u] = (x, d)
    go(root, 0)
    return pos, max(cnt[0], 1), md[0] + 1


def _children(n, edges):
    g = [[] for _ in range(n)]
    for e in edges:
        g[e[0]].append(e[1])
        g[e[1]].append(e[0])
    ch = [[] for _ in range(n)]
    seen = {0}
    st = [0]
    while st:
        u = st.pop()
        for v in g[u]:
            if v not in seen:
                seen.add(v)
                ch[u].append(v)
                st.append(v)
    for c in ch:
        c.sort()
    return ch


def _draw_tree(cv, box, T, children, edges, node_fn, edge_fn=None, under_fn=None, title=None, rad=23):
    """node_fn(u)->颜色名或None；edge_fn(a,b)->颜色名或None；under_fn(u)->节点下方小字"""
    x0, y0, x1, y1 = box
    if title:
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
        y0 += 44
    pos, w, dep = _tidy(children)
    gx = (x1 - x0 - 80) / max(w - 1, 1) if w > 1 else 0
    gx = min(gx, 170)
    gy = min((y1 - y0 - 90) / max(dep - 1, 1), 120)
    ox = x0 + (x1 - x0 - gx * (w - 1)) / 2
    oy = y0 + 40

    def P(u):
        return (ox + pos[u][0] * gx, oy + pos[u][1] * gy)
    for e in edges:
        a, b = e[0], e[1]
        pa_, pb = P(a), P(b)
        c = edge_fn(a, b) if edge_fn else None
        cv.line([pa_, pb], T[c] if c else T['border'], 7 if c else 3)
        if len(e) > 2:
            mx, my = (pa_[0] + pb[0]) / 2, (pa_[1] + pb[1]) / 2
            lab = str(e[2])
            tw = cv.tlen(lab, 20, True) + 12
            cv.rect((mx - tw / 2, my - 13, mx + tw / 2, my + 13), fill=T['bg'], r=8)
            cv.text((mx, my), lab, 20, T[c] if c else T['muted'], anchor='mm', bold=True, mono=True)
    for u in range(len(children)):
        X, Y = P(u)
        c = node_fn(u)
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=T[c] if c else T['panel2'],
                     outline=T[c] if c else T['border'], width=3)
        cv.text((X, Y), u, 26, T['bg'] if c else T['text'], anchor='mm', bold=True)
        if under_fn:
            s = under_fn(u)
            if s:
                cv.text((X + rad + 8, Y), s, 20, T['cyan'], anchor='lm', bold=True, mono=True)

CODE = '''
class Solution(object):
    def pathExistenceQueries(self, n, nums, maxDiff, queries):
        
        order = [index for index in range(n)]
        order.sort(key=lambda d:nums[d])
        rank = [None] * n
        for r, index in enumerate(order):
            rank[index] = r

        f = [[] for _ in range(n)]

        def update(start, end):
            p = start
            for index in range(start, end + 1):
                while p <= end and nums[order[p]] - nums[order[index]] <= maxDiff:
                    p += 1
                f[index].append(p - 1)

            while f[start][-1] != end:
                for index in range(start, end + 1):
                    mid = f[index][-1]
                    f[index].append(f[mid][-1])

        p = 0
        while p < n:
            q = p + 1
            while q < n and nums[order[q]] - nums[order[q - 1]] <= maxDiff:
                q += 1
            
            update(p, q - 1)
            p = q
        
        res = []
        for x, y in queries:
            x = rank[x]
            y = rank[y]
            if x > y:
                x, y = y, x

            if f[x][-1] < y:
                res.append(-1)
                continue

            res.append(0)
            p = len(f[x]) - 1
            while x < y:
                while p > 0 and f[x][p] >= y:
                    p -= 1
                res[-1] += (1 << p)
                x = f[x][p]
        
        return res
'''
LINE_TXT = {i: l for i, l in enumerate(CODE.strip('\n').split('\n'), 1)}

NUMS = [5, 3, 1, 9, 10, 7, 20]
MAXD = 2
QUERIES = [[2, 4], [0, 6]]


def _ln(sub, nth=0):
    r = [i for i, l in LINE_TXT.items() if sub in l]
    return r[nth] if r else 10 ** 6


def _axis(cv, box, T, order, hl, arcs, note=None):
    """order: 排序后各点的节点编号；hl: {rank: 颜色名}；arcs: [(from_rank, to_rank, 颜色名, 虚线?)]"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '数轴：圆内 = nums 的值，下方 = 原节点号，#k = 排序后的编号', 22, T['muted'], bold=True)
    vals = [NUMS[j] for j in order]
    lo, hi = min(vals), max(vals)
    base = y0 + 120
    pxs = []
    for p, v in enumerate(vals):
        pxs.append(x0 + 50 + p / max(len(vals) - 1, 1) * (x1 - x0 - 100))
    cv.line([(x0 + 30, base), (x1 - 30, base)], T['border'], 3)
    for a, b, c, dsh in arcs:
        if a == b or not (0 <= a < len(vals)) or not (0 <= b < len(vals)):
            continue
        pa_, pb = (pxs[a], base - 24), (pxs[b], base - 24)
        lift = 30 + abs(pxs[a] - pxs[b]) * 0.1
        cv.arc_arrow(pa_, pb, lift, T[c], width=4)
    for p, v in enumerate(vals):
        c = hl.get(p)
        X = pxs[p]
        cv.d.ellipse((X - 22, base - 22, X + 22, base + 22), fill=T[c] if c else T['panel2'], outline=T[c] if c else T['border'], width=3)
        cv.text((X, base), v, 24, T['bg'] if c else T['text'], anchor='mm', bold=True)
        cv.text((X, base + 34), f'节点 {order[p]}', 18, T['dim'], anchor='mt')
        cv.text((X, base + 62), f'#{p}', 20, T['yellow'] if c else T['muted'], anchor='mt', bold=True, mono=True)
    if note:
        cv.text((x0 + 18, base + 112), note, 22, T['cyan'], anchor='lm', bold=True)
NUMS = [5, 3, 1, 7, 9, 20]
QUERIES = [[2, 4], [0, 5]]
L_X = _ln('x = rank[x]')
L_Y = _ln('y = rank[y]')
L_Q = _ln('for x, y in queries')
L_UPD_CALL = _ln('update(p, q - 1)')


def _draw(cv, S, B, box, T):
    order = S.get('order')
    f = S.get('f')
    if order is None or f is None:
        return
    line = S.get('_line', 0)
    inner = S.get('_inner', {})
    hl, arcs, note = {}, [], None
    n = len(order)
    if 'start' in inner and 'end' in inner:
        idx = inner.get('index')
        if idx is not None:
            hl[idx] = 'yellow'
        if inner.get('mid') is not None and line > _ln('mid = f[index][-1]') - 1 and line >= _ln('mid = f[index][-1]'):
            hl[inner['mid']] = 'cyan'
        elif inner.get('p') is not None and inner['p'] < n and line < _ln('while f[start][-1] != end'):
            hl[inner['p']] = 'cyan'
        arcs = [(q, f[q][-1], 'purple', False) for q in range(n) if f[q]]
        note = f"区间 [{inner['start']}, {inner['end']}]：紫色箭头 = 当前最远一步 / 倍增后的最远跳点"
    elif line >= L_Q and 'x' in S and 'y' in S:
        rank = S['rank']
        x, y = S['x'], S['y']
        if line < L_X:
            x = rank[x]
        if line < L_Y:
            y = rank[y]
        hl[x], hl[y] = 'blue', 'pink'
        p = S.get('p')
        if p is not None and 0 <= x < n and p < len(f[x]) and line > _ln('p = len(f[x]) - 1') - 1:
            arcs = [(x, f[x][p], 'blue', False)]
        note = f"蓝 = x（向右跳），粉 = y（目标）" + (f"；已走 {S['res'][-1]} 步" if S.get('res') and line > _ln('res.append(0)') else '')
    elif 'p' in S and 'q' in S:
        for t in range(S['p'], min(S['q'], n)):
            hl[t] = 'green'
        note = f"绿色 = 一个连通块：相邻差 <= {MAXD} 就连在一起"
    _axis(cv, box, T, order, hl, arcs, note)


def _fmap(S):
    f = S.get('f')
    return {i: f[i] for i in range(len(f))} if f else None


CONFIG = dict(
    num=3534, title='针对图的路径存在性查询 II', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='排序 + 分块 + 倍增',
    tags=['难度分 2507'],
    code=CODE,
    call='Solution().pathExistenceQueries(6, [5,3,1,7,9,20], 2, [[2,4],[0,5]])',
    expect=[4, -1],
    views=[
        dict(type='custom', draw=_draw, h=290),
        dict(type='array', var='order', label='order：排序后第 r 个点的原下标', cell=56, h=120),
        dict(type='map', var=_fmap, label='f[x]：x 向右走 1, 2, 4… 步最远到的编号', fmt=lambda k, v: f'f[{k}] = {v}', h=230),
    ],
    watch=['x', 'y', 'p', ('res', 'res', 'green')],
    skip=['order = [index', 'rank = [None]', 'for r, index in enumerate(order)', 'rank[index] = r', 'f = [[] for', 'p = start',
          'q = p + 1', 'p = q', 'for index in range', 'mid = f[index][-1]', 'if x > y', 'res = []', 'p += 1', 'q += 1', 'continue', 'while x < y', 'p -= 1', 'p = 0'],
    max_steps=100,
    captions={
        'order.sort': '把下标按 `nums` 排序：`order` 是排序后第 r 个点的原下标，`rank` 是反过来的映射',
        'while p <= end and': lambda S, B, r: (f'`{S.nums[S.order[S.p]] if S.p <= S.end else "越界"}` − `{S.nums[S.order[S.index]]}` 仍 <= maxDiff，指针 p 后移' if S.p <= S.end and S.nums[S.order[S.p]] - S.nums[S.order[S.index]] <= S.maxDiff else f'`p = {S.p}` 够不着了（或到区间尾），停'),
        'f[index].append(p - 1)': '`f[{index}]` 加入 `{p - 1}`：编号 {index} 走 1 步最远到 {p - 1}',
        'while f[start][-1] != end': lambda S, B, r: (f'`f[{S.start}][-1] = {S.f[S.start][-1]}` != 区间尾 {S.end}：还没一步到尾 → 再倍增一轮' if S.f[S.start][-1] != S.end else f'`f[{S.start}][-1] = {S.end}` 已到区间尾，倍增结束'),
        'f[index].append(f[mid][-1])': '`f[{index}]` 追加：先到 `{mid}`，再用 `f[{mid}]` 最远的一步 → `{f[index][-1]}`（步数翻倍）',
        'while p < n': lambda S, B, r: (f'`p = {S.p}` < n：从 {S.p} 开始找下一个连通块' if S.p < S.n else '所有连通块都处理完了'),
        'while q < n and': '相邻两点差 `<= maxDiff = {maxDiff}` 就属于同一块：块尾 `q` = {q}',
        'update(p, q - 1)': '对块 `[{p}, {q - 1}]` 建倍增表 `f`',
        'for x, y in queries': lambda S, B, r: ('询问都处理完了' if (S.x == B.x and S.y == B.y) else f'处理询问：节点 `{S.x}` 到节点 `{S.y}`'),
        'x = rank[x]': '节点号映射成排序后的编号：`x = {x}`',
        'y = rank[y]': '`y = {y}`',
        'if f[x][-1] < y': lambda S, B, r: (f'`f[{S.x}][-1] = {S.f[S.x][-1]}` < y = {S.y}：x 向右最远也到不了 y → ==不连通== -1' if S.f[S.x][-1] < S.y else f'`f[{S.x}][-1] = {S.f[S.x][-1]}` >= y = {S.y}：能到，开始算步数'),
        'res.append(-1)': '答案 -1',
        'res.append(0)': '先记步数 0，再往右跳',
        'p = len(f[x]) - 1': '从最大的一步试起：`p = {p}`（走 2^p 步）',
        'while x < y': lambda S, B, r: (f'`x = {S.x}` < `y = {S.y}`：还没到 → 继续跳' if S.x < S.y else f'`x = {S.x}` 到达 y，这个询问结束'),
        'while p > 0 and f[x][p] >= y': lambda S, B, r: ('`p = 0`，最小的一步' if S.p == 0 else f'2^{S.p} 步会到 `{S.f[S.x][S.p]}`' + (' >= y：跳过头了 → 换小一档（p 减 1）' if S.f[S.x][S.p] >= S.y else ' < y：不过头 → 可以跳')),
        'p -= 1': '步子太大，换小一档：`p = {p}`',
        'res[-1] += (1 << p)': '累计步数 `+= 2^{p}` → {res[-1]}',
        'x = f[x][p]': '`x` 跳到 {x}',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='先分成连通块，再用倍增表 f 把一步步的走法折叠起来',
        complexity='时间 `O((n+q) log n)`，空间 `O(n log n)`',
        problem=['`|nums[i]−nums[j]| <= maxDiff` 的两点之间有边；每次询问求 `u` 到 `v` 的最短边数，不连通返回 -1',
                 '示例：`nums=[5,3,1,9,10]`，`maxDiff=2`，询问 `[0,2]` → `2`，`[2,3]` → `-1`',
                 '本视频：`nums=[5,3,1,7,9,20]`，询问 `[2,4]` 与 `[0,5]`，答案 `[4,-1]`'],
        quote='从x出发的每一步都应该尽量远的向后走，……这个行走的过程是O(n)的，需要想办法进行优化。',
        quote_src='—— yiduobo 题解原文',
        idea=['nums 无序 → 先排序，用 `order`/`rank` 在“原下标”和“排序后下标”之间换算',
              '排序后相邻差 `<= maxDiff` 的连成一块；每块里用滑动窗口算出每个点一步最远走到哪，再倍增折叠成 `f[x]`',
              '询问：x、y 不在同一块就是 -1；否则从大到小试 `f[x][p]`，只跳不过头的步，累加 `2^p`'],
        summary=['时间 `O((n+q) log n)`，空间 `O(n log n)`；`f[x]` 是不等长的列表，每块到块尾就停止倍增',
                 '连通性靠 `f[x][-1] < y` 判断：x 向右最远走不到 y 就是 -1',
                 '==跳的条件是 `f[x][p] < y`==（不过头），所以 `while p > 0 and f[x][p] >= y` 要缩小 p',
                 '对比灵神：灵神从右端 r 往左跳并统一用 `pa[x][i]` 表，yiduobo 从左端 x 往右跳并先分块'],
    ),
)
