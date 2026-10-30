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
class Solution:
    def pathExistenceQueries(self, n: int, nums: List[int], maxDiff: int, queries: List[List[int]]) -> List[int]:
        idx = sorted(range(n), key=lambda i: nums[i])

        # rank[i] 表示 nums[i] 是 nums 中的第几小，或者说节点 i 在 idx 中的下标
        rank = [0] * n
        for i, j in enumerate(idx):
            rank[j] = i

        # 双指针，从第 i 小的数开始，向左一步，最远能跳到第 left 小的数
        mx = n.bit_length()
        pa = [[0] * mx for _ in range(n)]
        left = 0
        for i, j in enumerate(idx):
            while nums[j] - nums[idx[left]] > maxDiff:
                left += 1
            pa[i][0] = left

        # 倍增
        for i in range(mx - 1):
            for x in range(n):
                p = pa[x][i]
                pa[x][i + 1] = pa[p][i]

        ans = []
        for l, r in queries:
            if l == r:  # 不用跳
                ans.append(0)
                continue
            l, r = rank[l], rank[r]
            if l > r:  # 保证 l 在 r 左边
                l, r = r, l
            # 从 r 开始，向左跳到 l
            res = 0
            for k in range(mx - 1, -1, -1):
                if pa[r][k] > l:
                    res |= 1 << k
                    r = pa[r][k]
            ans.append(-1 if pa[r][0] > l else res + 1)  # 再跳一步就能到 l
        return ans
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
L_BUILD = _ln('left = 0')
L_DBL = _ln('for i in range(mx - 1)')
L_Q = _ln('for l, r in queries')
L_CONV = _ln('l, r = rank[l], rank[r]')
L_FORK = _ln('for k in range(mx - 1, -1, -1)')
L_RANKLOOP, L_PALOOP = _ln('for i, j in enumerate(idx)', 0), _ln('for i, j in enumerate(idx)', 1)


def _draw(cv, S, B, box, T):
    idx = S.get('idx')
    if idx is None:
        return
    line = S.get('_line', 0)
    pa = S.get('pa')
    hl, arcs, note = {}, [], None
    if L_BUILD <= line < L_DBL and 'left' in S and 'i' in S and S['i'] < len(idx):
        i, left = S['i'], S['left']
        hl[i], hl[left] = 'yellow', 'cyan'
        done = i + 1 if line >= L_PALOOP + 3 else i
        arcs = [(p, pa[p][0], 'purple', False) for p in range(done)]
        note = f"`当前` nums = {NUMS[idx[i]]}，最左够得着的是 {NUMS[idx[left]]}（差 {NUMS[idx[i]] - NUMS[idx[left]]}，maxDiff = {MAXD}）".replace('`当前` ', '')
    elif L_DBL <= line < L_Q and 'x' in S and 'i' in S:
        i, x = S['i'], S['x']
        hl[x] = 'yellow'
        if S.get('p') is not None:
            hl[S['p']] = 'cyan'
        arcs = [(q, pa[q][i], 'purple', False) for q in range(len(idx))]
        note = f'紫色箭头 = 每个点往左跳 2^{i} 步最远到哪里'
    elif line >= L_Q and 'l' in S and 'r' in S:
        rank = S['rank']
        l, r = S['l'], S['r']
        if line < L_CONV:
            l, r = rank[l], rank[r]
        hl[l], hl[r] = 'blue', 'pink'
        k = S.get('k')
        if line >= L_FORK and k is not None and 0 <= r < len(pa):
            arcs = [(r, pa[r][k], 'pink', False)]
        if S.get('res') is not None and line >= L_FORK:
            note = f"已经跳了 res = {S['res']} 步；粉 = r（从右往左跳），蓝 = l（目标）"
    _axis(cv, box, T, idx, hl, arcs, note)


def _cap_while(S, B, ret):
    d = S.nums[S.j] - S.nums[S.idx[S.left]]
    if d > S.maxDiff:
        return f'`{S.nums[S.j]} − {S.nums[S.idx[S.left]]} = {d}` > {S.maxDiff}，够不着 → left 右移'
    return f'`{S.nums[S.j]} − {S.nums[S.idx[S.left]]} = {d}` <= {S.maxDiff}，够得着 → 停'


def _cap_if(S, B, ret):
    v = S.pa[S.r][S.k]
    if v > S.l:
        return f'试 2^{S.k} 步：`pa[{S.r}][{S.k}] = {v}` > l = {S.l}：跳 2^{S.k} 步还没越过 l → ==可以跳=='
    return f'试 2^{S.k} 步：`pa[{S.r}][{S.k}] = {v}` <= l = {S.l}：会跳到 l 或越过 → 不跳'


def _cap_ans(S, B, ret):
    if S.pa[S.r][0] > S.l:
        return f'再跳一步 `pa[{S.r}][0] = {S.pa[S.r][0]}` 仍在 l = {S.l} 右边 → 到不了，答案 ==-1=='
    return f'再跳一步就到 l：答案 `res + 1 = {S.res + 1}`'


CONFIG = dict(
    num=3534, title='针对图的路径存在性查询 II', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='排序 + 双指针 + 倍增',
    tags=['难度分 2507'],
    code=CODE,
    call='Solution().pathExistenceQueries(7, [5,3,1,9,10,7,20], 2, [[2,4],[0,6]])',
    expect=[5, -1],
    views=[
        dict(type='custom', draw=_draw, h=290),
        dict(type='array', var='idx', label='idx：按 nums 排序后的节点号', cell=56, h=120),
        dict(type='table', var='pa', label='pa[i][k]：编号 i 向左跳 2^k 步最远到的编号', cell=40, h=230),
    ],
    watch=['left', 'l', 'r', 'res', ('ans', 'ans', 'green')],
    skip=['mx = n.bit_length()', 'pa = [[0] * mx', 'left = 0', 'rank = [0] * n', 'for x in range(n)', 'p = pa[x][i]', 'ans = []',
          L_RANKLOOP, L_PALOOP, 'if l == r', 'rank[j] = i', 'for i in range(mx - 1)', 'if l > r', 'res = 0', 'for k in range(mx - 1, -1, -1)', 'res |= 1 << k', 'left += 1'],
    max_steps=100,
    captions={
        'idx = sorted': '把节点按 `nums` 从小到大排：`idx = {idx}`，相当于在数轴上从左到右==重新编号==（`rank` 是反向映射）',
        'rank[j] = i': '`rank[{j}] = {i}`：节点 {j} 是第 {i} 小，编号 {i}',
        'while nums[j]': _cap_while,
        'left += 1': '`left` 右移到 {left}',
        'pa[i][0] = left': '`pa[{i}][0] = {left}`：编号 {i} 一步最远能跳到编号 {left}',
        'pa[x][i + 1] = pa[p][i]': '`pa[{x}][{i+1}] = pa[{p}][{i}] = {pa[x][i+1]}`：先到 {p}，再跳一次',
        'l, r = rank[l], rank[r]': '节点号映射成数轴上的编号：`l = {l}`，`r = {r}`',
        'if l > r': '保证 l 在 r 左边：`l = {l}`，`r = {r}`',
        'res = 0': '从 r 开始向左跳，`res` 记录已跳的步数',
        'for k in range(mx - 1, -1, -1)': '从大到小试跳 2^{k} 步',
        'if pa[r][k] > l': _cap_if,
        'res |= 1 << k': '真跳：`res += 2^{k}` → {res}',
        'r = pa[r][k]': '真跳：`res += 2^{k}` → {res}，`r` 跳到编号 {r}',
        'ans.append(-1 if': _cap_ans,
    },
    cards=dict(
        one_liner='每步都尽量远地往左跳，倍增数跳了几步',
        complexity='时间 `O((n+q) log n)`，空间 `O(n log n)`',
        problem=['`|nums[i]−nums[j]| <= maxDiff` 的两点之间有边；每次询问求 `u` 到 `v` 的最短边数，不连通返回 -1',
                 '示例：`nums=[5,3,1,9,10]`，`maxDiff=2`，询问 `[0,2]` → `2`，`[2,3]` → `-1`',
                 '本视频：`nums=[5,3,1,9,10,7,20]`，询问 `[2,4]`（1 → 10）与 `[0,6]`，答案 `[5,-1]`'],
        quote='每一步都尽量远地向左跳就行。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把 nums 当作数轴上的点，==排序后重新编号==，用 `rank` 把节点号映射成编号',
              '双指针算出每个编号一步最远向左跳到哪：`pa[i][0] = left`',
              '倍增：`pa[x][i+1] = pa[pa[x][i]][i]`；询问时从大到小试 2^k 步，能跳（仍在 l 右侧）就跳，最后再补一步'],
        summary=['时间 `O((n+q) log n)`，空间 `O(n log n)`',
                 '==跳的条件是 `pa[r][k] > l`==（还没到 l），循环结束后再判断一步能否到 l',
                 '`l == r` 要特判成 0；`l > r` 要交换；跳不到就是 -1',
                 '`mx = n.bit_length()` 保证 2^mx > n，步数不会溢出'],
    ),
)
