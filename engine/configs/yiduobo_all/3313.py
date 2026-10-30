def _tree_pos(ch, root=0):
    """一般树自动布局：叶子按顺序排开，父亲在孩子中间。返回 {节点: (x 0~1, 深度)}"""
    pos, cnt = {}, [0]
    leaves = sum(1 for _ in _leaves(ch, root))
    def go(u, d):
        kids = ch.get(u, [])
        if not kids:
            pos[u] = ((cnt[0] + 0.5) / leaves, d); cnt[0] += 1
        else:
            for k in kids:
                go(k, d + 1)
            pos[u] = ((pos[kids[0]][0] + pos[kids[-1]][0]) / 2, d)
    go(root, 0)
    return pos


def _leaves(ch, u):
    kids = ch.get(u, [])
    if not kids:
        yield u
    for k in kids:
        yield from _leaves(ch, k)


def _gt_draw(cv, S, B, box, T, ch, pos, edges, node_fn, extra=None, title=''):
    """edges: [(父,子,颜色名或None,虚线)]；node_fn(S,u)->(填充色, 主文字, 副文字)"""
    x0, y0, x1, y1 = box
    maxd = max(d for _, d in pos.values())
    W, H = x1 - x0 - 300, y1 - y0 - 110
    P = {u: (x0 + 110 + px * W, y0 + 70 + (d / max(maxd, 1)) * H) for u, (px, d) in pos.items()}
    if title:
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    for a, b, col, dash in edges:
        pa, pb = P[a], P[b]
        if dash == 'arc':  # 从孩子 b 绕一道弧线指向 a（向左侧鼓出）
            cx, cy = min(pa[0], pb[0]) - 110, (pa[1] + pb[1]) / 2
            pts = [((1 - t) ** 2 * pb[0] + 2 * (1 - t) * t * cx + t * t * pa[0],
                    (1 - t) ** 2 * pb[1] + 2 * (1 - t) * t * cy + t * t * pa[1]) for t in [0.12 + 0.76 * i / 30 for i in range(31)]]
            cv.line(pts, T[col], 5)
            cv.arrow(pts[-3], pts[-1], T[col], 5, 16)
        elif dash:
            cv.dashed(pb, pa, T[col], 4)
        else:
            cv.line([pa, pb], T[col] if col else T['border'], 4 if col else 3)
    R = 24
    for u, (X, Y) in P.items():
        fill, main, sub = node_fn(S, u)
        cv.rect((X - R, Y - R, X + R, Y + R), fill=T[fill] if isinstance(fill, str) else fill, outline=T['border'], r=R, width=2)
        cv.text((X, Y), main, 24, T['text'] if fill == 'panel2' else T['bg'], anchor='mm', bold=True, mono=True)
        if sub:
            cv.text((X + R + 8, Y), sub, 20, T['text'], anchor='lm', bold=True)
    if extra:
        extra(cv, P, T)
    return P
EDGES = [[0, 1], [0, 2], [2, 3]]
CH = {0: [1, 2], 2: [3]}
POS = _tree_pos(CH)
_NOW = lambda S: S['_inner'].get('now')


def _node(S, u):
    I = S['_inner']
    f, far = S.get('f'), S.get('farthest')
    sub = ''
    if f and far and far[u] is not None:
        sub = f'f={f[u]} 最远→{far[u]}'
    if I.get('nxt') == u:
        return 'pink', str(u), sub
    if I.get('now') == u:
        return 'yellow', str(u), sub
    return 'panel2', str(u), sub


def _draw(cv, S, B, box, T):
    edges = [(a, b, None, False) for a, ks in CH.items() for b in ks]
    I = S['_inner']
    now, nxt = I.get('now'), I.get('nxt')
    if now is not None and nxt is not None:
        edges = [(a, b, 'yellow' if {a, b} == {now, nxt} else None, False) for a, b, _, _ in edges]
    _gt_draw(cv, S, B, box, T, CH, POS, edges, _node,
             title='树（黄 = now，粉 = nxt；f = 向下（或扣掉某个方向后）的最远距离，最远→ = 对应的最远点）')


CONFIG = dict(
    num=3313, title='查找树中最后标记的节点', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='换根 DP · 最远点及次远点',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def lastMarkedNodes(self, edges):

        n = len(edges) + 1

        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        f = [0] * n
        farthest = [None] * n

        def dfs(now, fa):
            farthest[now] = now
            for nxt in g[now]:
                if nxt == fa:
                    continue
                dfs(nxt, now)
                if f[nxt] + 1 > f[now]:
                    f[now] = f[nxt] + 1
                    farthest[now] = farthest[nxt]

        dfs(0, -1)
        
        res = [0] * n

        def calc(now, fa):

            first_dis = second_dis = 0
            first_far = second_far = 0
            for nxt in g[now]:
                cost = f[nxt] + 1
                if cost > first_dis:
                    first_dis, second_dis = cost, first_dis
                    first_far, second_far = farthest[nxt], first_far
                elif cost > second_dis:
                    second_dis = cost
                    second_far = farthest[nxt]

            res[now] = first_far
            f[now] = first_dis
            farthest[now] = first_far

            for nxt in g[now]:
                if nxt == fa:
                    continue
                cost = f[nxt] + 1
                if cost == first_dis and farthest[nxt] == first_far:
                    f[now] = second_dis
                    farthest[now] = second_far
                    calc(nxt, now)
                    f[now] = first_dis
                    farthest[now] = first_far
                else:
                    calc(nxt, now)

        calc(0, -1)
        return res
''',
    call='Solution().lastMarkedNodes([[0,1],[0,2],[2,3]])',
    expect=[3, 3, 1, 1],
    views=[
        dict(type='custom', draw=_draw, h=285),
        dict(type='array', var='f', label='f（第一趟：向下最远距离；第二趟：以它为根的全树最远距离）', cell=56, h=105),
        dict(type='array', var='farthest', label='farthest（对应的最远点）', cell=56, h=105),
        dict(type='array', var='res', label='res（答案：每个点出发的最后被标记点）', cell=56, h=105),
        dict(type='calls', h=100),
    ],
    watch=[('now', "now if 'now' in _inner else ''", 'yellow'), ('first', "(first_dis, first_far) if 'first_far' in _inner else ''", 'green'),
           ('second', "(second_dis, second_far) if 'second_far' in _inner else ''", 'orange')],
    skip=[21, 35, 38, 41, 42, 50, 53, 'for nxt in g[now]', 'continue', 'if nxt == fa', 'first_dis = second_dis = 0', 'first_far = second_far = 0', 'cost = f[nxt] + 1', 'for x, y in edges', 'g[x].append', 'g[y].append', 'n = len(edges)', 'g = [[]', 'f = [0] * n', 'farthest = [None]', 'res = [0] * n'],
    max_steps=100,
    captions={
        15: '`{now}` 先假设最远点是自己：`farthest[{now}] = {now}`，`f[{now}] = 0`',
        19: '先递归孩子 `{nxt}`，等它「向下」的最远距离算好',
        20: lambda S, B, r: (f'孩子 `{S.nxt}` 方向的距离 `f[{S.nxt}] + 1 = {S.f[S.nxt] + 1}`，当前 `f[{S.now}] = {S.f[S.now]}`'
                             + ('，==更远== → 换成这个孩子' if S.f[S.nxt] + 1 > S.f[S.now] else '，不更远 → 不变')),
        22: '更新 `f[{now}] = {f[now]}`，最远点同步换成孩子的最远点 `farthest[{now}] = {farthest[now]}`（==距离和最远点一起维护==）',
        58: '第二趟 `calc`：`f` 要改成「以该点为根、整棵树的最远」，要把向上的方向也算进来',
        34: lambda S, B, r: (f'`{S.now}` 的邻居 `{S.nxt}` 方向' + ('（向上，用父亲换根后的值）' if S.nxt == S.fa else '（向下）') + f'，最远距离 `cost = {S.cost}`'
                             + (f'，比最远 `{S.first_dis}` 还远 → 成为最远方向' if S.cost > S.first_dis else f'，不比最远 `{S.first_dis}` 远 → 再和次远比')),
        36: '最远方向变成 `{nxt}`：`first = ({first_dis}, {first_far})`；原来的最远降为次远 `second = ({second_dis}, {second_far})`',
        37: '`cost = {cost}` 和次远 `{second_dis}` 比：{"更远" if cost > second_dis else "不更远"}',
        39: '`{nxt}` 方向成为次远：`second = ({second_dis}, {second_far})`',
        43: '`{now}` 的答案 = 最远点 `{first_far}`，`res[{now}] = {res[now]}`；`f`、`farthest` 改成含向上方向的全树最远 `({f[now]}, {farthest[now]})`',
        49: lambda S, B, r: ((f'`{S.nxt}` 方向正是 `{S.now}` 的最远方向（距离和最远点都相同）→ 孩子往上走不能再用 `{S.now}` 的最远' if S.cost == S.first_dis and S.farthest[S.nxt] == S.first_far
                              else f'`{S.nxt}` 不在最远方向上 → 孩子往上走可以直接用 `{S.now}` 的最远 `({S.first_dis}, {S.first_far})`')),
        51: '临时把 `{now}` 的最远换成次远 `({f[now]}, {farthest[now]})`，再递归 `{nxt}`',
        52: '递归 `{B.nxt}`：它往上看到的 `{B.now}` 只剩次远 `({B.f[B.now]}, {B.farthest[B.now]})`，不会绕回自己',
        56: '递归 `{B.nxt}`：它往上看到的 `{B.now}` 保持最远 `({B.f[B.now]}, {B.farthest[B.now]})`',
        54: '递归回来，还原 `{now}`：`f[{now}] = {f[now]}`，`farthest[{now}] = {farthest[now]}`',
        59: '`res = {ret}`：每个点出发，最后被标记的点',
    },
    cards=dict(
        one_liner='换根：每个点的最远点 = 向下最远 与 向上最远 的较大者',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['树有 `n` 个点，从某点开始，每秒标记所有与已标记点相邻的点',
                 '问：从每个点 `i` 开始，==最后一个被标记==的点是哪个（并列任选）',
                 '等价于：求每个点距离最远的点。示例：`[[0,1],[0,2],[2,3]]`'],
        quote='本题中每一轮都需要标记相邻节点，那么问题实际上就是问对于树中的每个节点，与这个节点距离最远的节点是哪一个。',
        quote_src='—— yiduobo 题解原文',
        idea=['和 3241 一样的换根：第一趟 dfs 算==向下==的最远距离 `f` 和最远点 `farthest`',
              '第二趟 calc：每个点记==最远、次远==两个方向（含向上的方向）',
              '往最远方向的孩子走时，孩子向上的最远要换成「次远」，否则会绕回自己'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：除了距离，还要同步维护==最远点==是谁（`farthest`）',
                 '易错点：往最远孩子递归前，临时把 `f[now]` 换成次远，递归后要==还原==',
                 '判断孩子是否在最远方向，要距离和最远点同时相等',
                 '原文是 Python 2 风格 `class Solution(object)`，在 Python 3 中可直接运行，未改动'],
    ),
)
