CODE = '''
class Solution(object):
    def maxStability(self, n, edges, k):
        
        edges.sort(key=lambda d:(d[-1], d[-2]), reverse=True)
        res = None
        fa = [index for index in range(n)]
        can_update = []
        cnt = 0

        def find(x, fa):
            if fa[x] != x:
                fa[x] = find(fa[x], fa)
            return fa[x]

        for u, v, s, must in edges:
            fa_u = find(u, fa)
            fa_v = find(v, fa)
            if fa_u == fa_v:
                if must == 1:
                    return -1
            else:
                cnt += 1
                if cnt >= n:
                    return -1

                fa[fa_u] = fa_v
                if must == 1:
                    res = s
                else:
                    can_update.append(s)
        
                if cnt == n - 1 and must == 0:
                    break
        
        if cnt < n - 1:
            return -1
        
        can_update.reverse()
        for index in range(min(k, len(can_update))):
            can_update[index] *= 2
        
        if can_update:
            other_min = min(can_update)
            if res is None or res > other_min:
                res = other_min
        
        return res
'''
_LINES = CODE.strip('\n').split('\n')


def _ln(sub, nth=0):
    return [i + 1 for i, t in enumerate(_LINES) if sub in t][nth]


L_IF = _ln('if fa_u == fa_v')
L_REV = _ln('can_update.reverse()')
L_EDGES = _ln('for u, v, s, must in edges')
L_SORT = _ln('edges.sort')
PAL = ['cyan', 'orange', 'pink', 'green', 'purple', 'yellow']


def _sim(S):
    edges, n = S['edges'], S['n']
    fa = list(range(n))

    def fd(a):
        while fa[a] != a:
            a = fa[a]
        return a

    line = S['_line']
    cur = [S['u'], S['v'], S['s'], S['must']] if 'u' in S else None
    idx = next((i for i, e in enumerate(edges) if list(e) == cur), None) if cur else None
    if line <= L_EDGES:
        idx, upto = None, 0
    else:
        upto = idx + (1 if line >= L_IF else 0) if idx is not None else 0
    chosen, rej = [], set()
    for i in range(min(upto, len(edges))):
        a, b = fd(edges[i][0]), fd(edges[i][1])
        if a != b:
            fa[a] = b
            chosen.append(i)
        else:
            rej.add(i)
    return idx, set(chosen), chosen, rej, [fd(v) for v in range(n)]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n, edges, k = S['n'], S['edges'], S['k']
    idx, chosen, order, rej, roots = _sim(S)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 10
    rx, ry = min(300, (x1 - x0) / 2 - 90), min(165, (y1 - y0) / 2 - 95)
    pos = [(cx - rx, cy - ry), (cx + rx, cy - ry), (cx + rx, cy + ry), (cx - rx, cy + ry)]
    cv.text((x0 + 18, y0 + 4), '图（紫 = 必选边，绿 = 已选进生成树，红虚线 = 成环舍弃，黄框 = 当前边）', 22, T['muted'], bold=True)
    up = set()
    if S['_line'] >= L_REV:
        soft = [i for i in order if not edges[i][3]]
        m = min(k, len(soft))
        up = set(soft[len(soft) - m:]) if m else set()
    for i, e in enumerate(edges):
        a, b, s, mu = e
        p, q = pos[a], pos[b]
        if mu and i in chosen:
            col, w = T['purple'], 9
        elif i in chosen:
            col, w = T['green'], 8
        elif i in rej:
            col, w = T['red'], 3
        else:
            col, w = (T['purple'] if mu else (90, 98, 110)), (5 if mu else 3)
        if i in rej:
            cv.dashed(p, q, col, w)
        else:
            cv.line([p, q], col, w)
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        if (a, b) == (0, 2):
            mx, my = p[0] + (q[0] - p[0]) * 0.32, p[1] + (q[1] - p[1]) * 0.32
        lab = f'{s}→{2 * s}' if i in up else str(s)
        wd = cv.tlen(lab, 26, True) + 20
        cv.rect((mx - wd / 2, my - 18, mx + wd / 2, my + 18), fill=T['panel2'], outline=T['yellow'] if i == idx else col, width=4 if i == idx else 2, r=10)
        cv.text((mx, my), lab, 26, T['orange'] if i in up else T['text'], anchor='mm', bold=True)
    cmap = {}
    for r_ in roots:
        cmap.setdefault(r_, T[PAL[len(cmap) % len(PAL)]])
    for v in range(n):
        X, Y = pos[v]
        cv.rect((X - 34, Y - 34, X + 34, Y + 34), fill=cmap[roots[v]], r=34)
        cv.text((X, Y), v, 34, T['bg'], anchor='mm', bold=True)
    cv.text((cx, y1 - 16), f'同色 = 同一连通块，当前 {len(cmap)} 个；已选 {len(chosen)} / {n - 1} 条边', 22, T['muted'], anchor='mm', bold=True)


def _txt(S):
    line = S['_line']
    if line <= L_SORT:
        return '边 `[u, v, 强度, must]`：先把 must=1 的边排前面，其余按强度从大到小'
    if line < L_REV:
        return f"Kruskal 逐条加边：`cnt = {S['cnt']}`（要 {S['n'] - 1} 条），`res = {S['res']}`（must 边的最后一条强度）"
    return f"升级后的可选边 `can_update = {S['can_update']}`，`res = {S['res']}`"


CONFIG = dict(
    num=3600, title='升级后最大生成树稳定性', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='必选边优先 + Kruskal + 翻倍最小的 k 条',
    tags=['二分算法', '图论算法', '难度分 2301'],
    code=CODE,
    call='Solution().maxStability(4, [[0,1,8,1],[2,3,3,0],[1,2,5,0],[0,3,2,0],[0,2,4,0]], 1)',
    expect=5,
    max_steps=70,
    skip=['def find', 'if fa[x] != x', 'fa[x] = find(fa[x], fa)', 'return fa[x]'],
    views=[
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=['u', 'v', 's', 'must', 'cnt', ('res', 'res', 'green'), 'can_update', 'k'],
    captions={
        _ln('edges.sort'): '`(must, s)` 倒序：==must=1 的边排最前==，其余强度从大到小',
        _ln('res = None'): '`res`：记录最后加入的 must 边的强度',
        _ln('fa = ['): '并查集 `fa`，用来判环',
        _ln('can_update = []'): '`can_update`：生成树里可升级边的强度',
        _ln('cnt = 0'): '`cnt`：树里已有几条边',
        L_EDGES: lambda S, B, r: (f'取边 `({S.u}, {S.v})` 强度 `{S.s}`，must = `{S.must}`' if not (B.get('u') == S.u and B.get('v') == S.v) else '边处理完了'),
        _ln('fa_u = find'): '找 `u = {u}` 所在连通块的代表元',
        _ln('fa_v = find'): '找 `v = {v}` 所在连通块的代表元',
        L_IF: lambda S, B, r: (f'`{S.fa_u} == {S.fa_v}`：已连通，加这条边会成环' if S.fa_u == S.fa_v else f'`{S.fa_u} != {S.fa_v}`：不同连通块，可以加'),
        _ln('if must == 1', 0): lambda S, B, r: ('必选边成环 → 无解 `-1`' if S.must == 1 else '可选边成环 → 直接跳过'),
        _ln('cnt += 1'): '树里多了一条边：`cnt = {cnt}`',
        _ln('fa[fa_u] = fa_v'): '合并两个连通块',
        _ln('if must == 1', 1): lambda S, B, r: ('必选边：`res = {}`（must 边按强度倒序，最后一条最小）'.format(S.s) if S.must == 1 else '可选边：放进 `can_update`'),
        _ln('res = s'): '`res = {res}`：目前 must 边里最小的强度',
        _ln('can_update.append'): '`can_update = {can_update}`（强度从大到小）',
        _ln('if cnt == n - 1'): lambda S, B, r: (f'`cnt = {S.cnt} = n - 1`，且是可选边 → 树完成，break' if (S.cnt == S.n - 1 and S.must == 0) else f'`cnt = {S.cnt}`，还没凑够 `n-1 = {S.n - 1}` 条'),
        _ln('if cnt < n - 1'): lambda S, B, r: ('边不够，图不连通 → -1' if S.cnt < S.n - 1 else '`cnt = n - 1`，生成树完整'),
        L_REV: '反转：现在 `can_update` ==从小到大==，最小的排前面 → `{can_update}`',
        _ln('for index in range'): lambda S, B, r: (f'升级最小的 `min(k, len) = {min(S.k, len(S.can_update))}` 条' if 'index' not in S else f'第 `{S.index}` 条：强度 ×2'),
        _ln('can_update[index] *= 2'): '`can_update[{index}]` ×2 → `{can_update}`',
        _ln('if can_update:'): '可升级边里最小的强度才会拖后腿',
        _ln('other_min = min'): '`other_min = {other_min}`（升级后可选边的最小强度）',
        _ln('if res is None'): lambda S, B, r: (f'`res = {S.res}` 比 `other_min = {S.other_min}` 大 → 取较小者' if (S.res is None or S.res > S.other_min) else f'`res = {S.res}` 已经不超过 `other_min`'),
        _ln('res = other_min'): '`res = {res}`',
        _ln('return res'): '稳定性取两者较小值：`{res}`',
    },
    cards=dict(
        one_liner='must 边先进树，Kruskal 凑满，再把最小的 k 条可选边翻倍',
        complexity='时间 `O(m log m)`，空间 `O(n)`',
        problem=['`n` 个点，边 `[u, v, s, must]`：`must=1` 必须选，不能升级',
                 '最多 `k` 次升级，把可选边强度翻倍，求生成树最小边权的最大值',
                 '本视频：`n=4`，5 条边，`k=1` → `5`'],
        quote='按照题目的要求，必须先把must为1的边都加入到树中，若在这个过程中出现了环，那么直接返回-1。……为了使得最小的边权最大，就应该将可以修改的边中边权最小的k条边翻倍。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序时 must 边在前：先加必选边，成环就 -1',
              '其余边按 Kruskal 从大到小加，用并查集判环',
              '记下 must 边的最小强度 `res`，可选边反转后翻倍前 `k` 个，再取最小'],
        summary=['时间 `O(m log m)`，空间 `O(n)`',
                 '原文是 Python 2 风格但无需改动，直接可在 Python 3 运行',
                 '易错：`cnt == n-1` 后要 break；最后还要判 `cnt < n-1`（不连通）',
                 '对比灵神：灵神用两个并查集提前判环和连通，yiduobo 合在一次遍历里',
                 '`res` 只取最后一条 must 边，因为 must 边已按强度倒序'],
    ),
)
