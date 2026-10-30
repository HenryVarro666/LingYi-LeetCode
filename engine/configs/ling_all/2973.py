def _layout_tree(n, edges, root=0):
    g = [[] for _ in range(n)]
    for x, y in edges:
        g[x].append(y)
        g[y].append(x)
    pos, nxt = {}, [0]

    def go(x, fa, d):
        ch = [y for y in g[x] if y != fa]
        if not ch:
            pos[x] = (nxt[0], d)
            nxt[0] += 1
        else:
            for y in ch:
                go(y, x, d + 1)
            pos[x] = (sum(pos[y][0] for y in ch) / len(ch), d)
    go(root, -1, 0)
    return pos, nxt[0], max(d for _, d in pos.values()) + 1


def _draw_tree(cv, box, T, n, edges, fill, sub, ring=None, title='', subcolor='muted', inner=None):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    pos, w, h = _layout_tree(n, edges)
    sp = min(170, (x1 - x0 - 60) / max(1, w))
    R = max(18, min(28, sp * 0.36))
    dy = min(120, (y1 - y0 - 70 - 2 * R - 40) / max(1, h - 1))
    sx = x0 + 30 + ((x1 - x0 - 60) - sp * w) / 2 + sp / 2
    P = {k: (sx + a * sp, y0 + 60 + R + d * dy) for k, (a, d) in pos.items()}
    for a, b in edges:
        (ax, ay), (bx, by) = P[a], P[b]
        if pos[a][1] > pos[b][1]:
            (ax, ay), (bx, by) = (bx, by), (ax, ay)
        cv.line([(ax, ay), (bx, by)], T['dim'], 3)
    for k, (cx, cy) in P.items():
        c = fill.get(k)
        cv.rect((cx - R, cy - R, cx + R, cy + R), fill=T[c] if c else T['panel2'], outline=T['yellow'] if k == ring else T['border'],
                width=5 if k == ring else 3, r=R)
        cv.text((cx, cy), k, 26, T['bg'] if c else T['text'], anchor='mm', bold=True)
        s = sub.get(k)
        if s not in (None, ''):
            tw = cv.tlen(s, 21, bold=True) + 10
            cv.rect((cx - tw / 2, cy + R + 4, cx + tw / 2, cy + R + 32), fill=T['panel'], r=6)
            cv.text((cx, cy + R + 8), s, 21, T[subcolor], anchor='mt', bold=True)


SNAP = {}
DONE = set()


def trk(fn=None, rec=None, reset=False):
    """caption wrapper: remember which nodes have returned, keyed by this step's innermost-locals object"""
    def cap(S, B, ret):
        if reset:
            DONE.clear()
            SNAP.clear()
        if rec is not None:
            DONE.add(rec(S, B))
        SNAP[id(S['_inner'])] = frozenset(DONE)
        return fn(S, B, ret) if callable(fn) else None
    return cap


def _done(S):
    return SNAP.get(id(S['_inner']), frozenset())


def fill_caps(code, caps, reset_key):
    """give every other statement line a tracking (default-text) caption"""
    out = dict(caps)
    for l in code.strip('\n').split('\n'):
        s = l.strip()
        if not s or s.startswith(('def ', 'class ', '#')) or any(k in l for k in out):
            continue
        out[s] = trk()
    return out
EDGES = [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5], [2, 6]]
COST = [1, 4, 2, 3, 5, -8, -9]


def _draw(cv, S, B, box, T):
    cost = S.get('cost')
    if cost is None:
        return
    done, cur, ans = _done(S), S['_inner'].get('x'), S.get('ans')
    fill = {k: 'green' for k in done}
    if cur is not None and cur not in done:
        fill[cur] = 'blue'
    sub = {i: (f'{cost[i]}' + (f' → {ans[i]}' if i in done and ans else '')) for i in range(len(cost))}
    _draw_tree(cv, box, T, len(cost), EDGES, fill, sub, ring=cur,
               title='树（蓝 = 正在处理，绿 = 已返回；下方：开销 → 放置的金币）')


def _alist(S):
    a = S['_inner'].get('a')
    if a is None:
        return ''
    return f'当前节点 `{S["_inner"].get("x")}` 的 `a` = ==[{", ".join(map(str, a))}]==（{len(a)} 个数）'


def _c_max(S, B, ret):
    a = S.a
    return (f'最大三个相乘 `{a[-3]}×{a[-2]}×{a[-1]}` = {a[-3]*a[-2]*a[-1]}；最小两个（可能是负数）乘最大 `{a[0]}×{a[1]}×{a[-1]}` = {a[0]*a[1]*a[-1]}；'
            f'再和 `0` 取 max → 金币 =={S.ans[S.x]}==')


def _c_m(S, B, ret):
    m = len(S.a)
    return f'`m = {m}`：' + ('不少于 3 个节点 → 要算三数之积' if m >= 3 else '子树不足 3 个节点 → 保持 `ans[x] = 1`')


def _c_cut(S, B, ret):
    m = len(B.a)
    if m > 5:
        return f'`m = {m} > 5` → ==只保留最小 2 个和最大 3 个==，其余数字永远用不上'
    return f'`m = {m}` 不超过 5 个，全部保留'


def _c_trunc(S, B, ret):
    return f'`a = a[:2] + a[-3:]`：丢掉中间的数，只剩 5 个 → =={S.a}=='


CODE = '''
class Solution:
    def placedCoins(self, edges: List[List[int]], cost: List[int]) -> List[int]:
        n = len(cost)
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        ans = [1] * n
        def dfs(x: int, fa: int) -> List[int]:
            a = [cost[x]]
            for y in g[x]:
                if y != fa:
                    a.extend(dfs(y, x))
            a.sort()
            m = len(a)
            if m >= 3:
                ans[x] = max(a[-3] * a[-2] * a[-1], a[0] * a[1] * a[-1], 0)
            if m > 5:
                a = a[:2] + a[-3:]
            return a
        dfs(0, -1)
        return ans
'''
CAPS = {
    'n = len(cost)': trk(lambda S, B, r: f'`n = {S.n}` 个节点', reset=True),
    'g = [[]': trk(lambda S, B, r: '先把无向边建成邻接表 `g`'),
    'ans = [1] * n': trk(lambda S, B, r: '先全放 1 个金币：==子树不足 3 个节点就是 1 枚=='),
    'a = [cost[x]]': trk(lambda S, B, r: f'进入节点 `{S.x}`：`a` 先放自己的开销 `{S.cost[S.x]}`'),
    'for y in g[x]': trk(lambda S, B, r: f'遍历 `{S.x}` 的邻居，下一个是 `{S.y}`' if S['_inner'].get('y') != B['_inner'].get('y') else f'`{S.x}` 的邻居都处理完了 → 汇总 `a`'),
    'if y != fa': trk(lambda S, B, r: f'邻居 `{S.y}` ' + (f'是父节点 `{S.fa}` → 跳过，只往下走' if S.y == S.fa else f'不是父节点 → 是子节点，递归进去')),
    'a.extend(dfs': trk(lambda S, B, r: f'递归子节点 `{B.y}`：它会==只返回最多 5 个数==，并入 `a`'),
    'a.sort()': trk(lambda S, B, r: f'把 `a` 排序（它已含自己和所有儿子子树返回的数）→ =={S.a}=='),
    'm = len(a)': trk(lambda S, B, r: f'`m = {S.m}`'),
    'if m >= 3': trk(_c_m),
    'ans[x] = max': trk(_c_max),
    'if m > 5': trk(_c_cut),
    'a = a[:2]': trk(_c_trunc),
    'return ans': trk(lambda S, B, r: f'每个节点的金币数 `{r}`'),
    'dfs(0, -1)': trk(lambda S, B, r: '从根节点 `0` 开始自底向上 DFS'),
    'return a': trk(lambda S, B, r: f'节点 `{S.x}` 完成，向上返回 `{r}`（至多 5 个数）', rec=lambda S, B: S.x),
}
CONFIG = dict(
    num=2973, title='树中每个节点放置的金币数目', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='自底向上 DFS · 只传 5 个数', tags=['灵神题单·链表树与回溯', '难度分 2277'],
    code=CODE,
    call=f'Solution().placedCoins({EDGES}, {COST})',
    expect=[360, 60, 144, 1, 1, 1, 1],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='text', fn=_alist, h=50),
        dict(type='calls', h=150),
    ],
    watch=[('x', lambda S: S['_inner'].get('x'), 'blue'), ('m', lambda S: S['_inner'].get('m')), ('ans', 'ans', 'green')],
    captions=fill_caps(CODE, CAPS, 'n = len'),
    skip=['for x, y in edges', 'g[x].append', 'g[y].append', 'm = len(a)'],
    max_steps=120,
    cards=dict(
        one_liner='三数之积最大值，只需要最小 2 个和最大 3 个',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['无向树，根为 `0`，节点 `i` 的开销为 `cost[i]`',
                 '子树 ==不足 3 个节点== 放 1 个金币；否则放「子树内 3 个不同节点开销乘积的最大值」，负数则放 0',
                 '示例：本视频用 7 个节点的小树'],
        quote='每棵子树只需要返回它最小的 2 个 cost 值和最大的 3 个 cost 值就行，其余数字可以舍弃。',
        quote_src='—— 灵茶山艾府题解',
        idea=['三数之积最大：要么是最大的三个数，要么是 ==最小的两个（负数）× 最大的一个==',
              '所以每棵子树只需向上传 ==5 个数==，其余没用',
              '当前节点：自己的 cost + 各儿子返回的数 → 排序 → 算答案 → 再截断成 5 个'],
        summary=['时间 `O(n log n)`（瓶颈在排序），手动维护最小 2 个、最大 3 个可到 `O(n)`',
                 '易错：乘积为负要和 `0` 取 max；子树 `m < 3` 时保持默认的 `1`',
                 '截断 `a[:2] + a[-3:]` 要在 `m > 5` 时才做，否则会重复取同一个数',
                 '同类题：自底向上 DFS，儿子向父亲返回「够用的信息」'],
    ),
)
