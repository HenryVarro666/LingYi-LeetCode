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
DONE = {}


def trk(fn=None, rec=None, reset=False):
    """caption wrapper: remember which nodes have returned (node -> returned value), keyed by this step's innermost-locals object"""
    def cap(S, B, ret):
        if reset:
            DONE.clear()
        if rec is not None:
            kv = rec(S, B, ret)
            if kv is not None:
                DONE[kv[0]] = kv[1]
        SNAP[id(S['_inner'])] = dict(DONE)
        return fn(S, B, ret) if callable(fn) else None
    return cap


def _done(S):
    return SNAP.get(id(S['_inner']), {})


def fill_caps(code, caps):
    """give every other statement line a tracking (default-text) caption"""
    out = dict(caps)
    for l in code.strip('\n').split('\n'):
        s = l.strip()
        if not s or s.startswith(('def ', 'class ', '#')) or any(k in l for k in out):
            continue
        out[s] = trk()
    return out
EDGES = [[0, 1], [0, 2], [1, 3], [1, 4]]
NUMS = [2, 1, 4, 2, 3]


def _draw(cv, S, B, box, T):
    nums = S.get('nums')
    if nums is None:
        return
    done, inner = _done(S), S['_inner']
    cur = inner.get('x')
    fill, sub = {}, {}
    for i in range(len(nums)):
        sub[i] = str(nums[i])
        if i in done:
            v = done[i]
            fill[i] = 'red' if v < 0 else 'green' if v == 0 else 'orange'
            sub[i] += f' → {v}'
    if cur is not None and cur not in done:
        fill[cur] = 'blue'
        sub[cur] += f'  已凑 {inner.get("s")}'
    _draw_tree(cv, box, T, len(nums), EDGES, fill, sub, ring=cur,
               title='树（蓝 = 正在处理，绿 = 返回 0（切一刀），橙 = 返回和，红 = 返回 -1；下方：点权 → 返回值）')


def _info(S):
    t = S.get('target')
    if t is None:
        return ''
    return f'总和 `total = {S.get("total")}`，试 `{S.get("i")}` 个块 → 每块 `target = {t}`'


CODE = '''
class Solution:
    def componentValue(self, nums: List[int], edges: List[List[int]]) -> int:
        g = [[] for _ in nums]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        def dfs(x: int, fa: int) -> int:
            s = nums[x]
            for y in g[x]:
                if y != fa:
                    res = dfs(y, x)
                    if res < 0: return -1
                    s += res
            if s > target: return -1
            return s if s < target else 0

        total = sum(nums)
        for i in range(total // max(nums), 1, -1):
            if total % i == 0:
                target = total // i
                if dfs(0, -1) == 0: return i - 1
        return 0
'''
CAPS = {
    'g = [[]': trk(lambda S, B, r: '先把无向边建成邻接表 `g`', reset=True),
    's = nums[x]': trk(lambda S, B, r: f'进入节点 `{S.x}`：`s` 先装上自己的点权 `{S.s}`'),
    'for y in g[x]': trk(lambda S, B, r: f'遍历 `{S.x}` 的邻居，下一个是 `{S.y}`' + ('（它是父节点，不用回头）' if S.y == S.fa else '（子节点，递归下去）') if S['_inner'].get('y') != B['_inner'].get('y') else f'`{S.x}` 的邻居都处理完了，`s = {S.s}`'),
    'res = dfs(y, x)': trk(lambda S, B, r: f'递归子节点 `{B.y}`：它==返回 -1（不合法）、0（已切下一块）或没装满的和=='),
    'if res < 0: return -1': trk(lambda S, B, r: (f'子树返回 `{B.res}` < 0 → 这个 `target` 不可行，一路返回 `-1`' if r is not None
                                                   else f'子树返回 `{B.res}` ≥ 0（0 = 儿子已自成一块，不占水）→ 并入 `s += res`，`s = {S.s} + {B.res}`' if False else f'子树返回 `{B.res}` ≥ 0（返回 0 表示儿子自成一块）→ 接着 `s += {B.res}`'),
                                 rec=lambda S, B, r: (S.x, -1) if r is not None else None),
    'if s > target': trk(lambda S, B, r: (f'`s = {S.s} > target = {S.target}`：杯子装溢出了 → 返回 `-1`' if r is not None
                                           else f'`s = {S.s} ≤ target = {S.target}`：没超，继续判断'),
                          rec=lambda S, B, r: (S.x, -1) if r is not None else None),
    'return s if s < target else 0': trk(
        lambda S, B, r: (f'`s = {S.s}` 恰好等于 `target = {S.target}` → ==这条边必须删==，返回 `0`' if r == 0
                         else f'`s = {S.s} < target = {S.target}`：杯子还没满，把 `{r}` 交给父节点继续接'),
        rec=lambda S, B, r: (S.x, r)),
    'total = sum(nums)': trk(lambda S, B, r: f'`total = {S.total}`：每块的点权和 = total / 块数'),
    'for i in range': trk(lambda S, B, r: (f'枚举块数 `i = {S.i}`（从 `total // max(nums) = {S.total // max(S.nums)}` 往下，块数越多删边越多）'
                                           if S['_inner'].get('i') != B['_inner'].get('i') else '块数都试完了，没有可行方案')),
    'if total % i': trk(lambda S, B, r: f'`{S.total} % {S.i} = {S.total % S.i}` → ' + ('是因子，每块应为 `total / i`' if S.total % S.i == 0 else '不是因子，==每块点权和不是整数== → 跳过')),
    'target = total // i': trk(lambda S, B, r: f'`target = {S.total} // {S.i} = {S.target}`：每块的点权和', reset=True),
    'if dfs(0, -1) == 0': trk(lambda S, B, r: (f'`dfs(0, -1) = 0`：整棵树恰好切成 `{S.i}` 块 → 删 `{S.i} - 1 = {S.i - 1}` 条边' if r is not None
                                              else f'根返回 `{B.get("res")}`'.replace('None', '') if False else '从根节点 `0` 开始自底向上 DFS，检验是否能切成每块 `target`')),
    'return 0': trk(lambda S, B, r: '所有块数都不行 → 一刀都不能切，返回 `0`'),
}
CONFIG = dict(
    num=2440, title='创建价值相同的连通块', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='枚举块数 + 自底向上 DFS', tags=['灵神题单·链表树与回溯', '难度分 2460'],
    code=CODE,
    call=f'Solution().componentValue({NUMS}, {EDGES})',
    expect=1,
    views=[
        dict(type='custom', draw=_draw, h=390),
        dict(type='text', fn=_info, h=50),
        dict(type='calls', h=150),
    ],
    watch=[('x', lambda S: S['_inner'].get('x'), 'blue'), ('s', lambda S: S['_inner'].get('s')), ('target', 'target', 'green'), ('i', 'i', 'orange')],
    captions=fill_caps(CODE, CAPS),
    skip=['for x, y in edges', 'g[x].append', 'g[y].append', 'if y != fa', 's += res'],
    max_steps=120,
    # result below
    cards=dict(
        one_liner='像用水杯接水：每满 target 就切断，溢出就换块数',
        complexity='时间 `O(n·d(s))`，`d(s)` 为总和的因子数；空间 `O(n)`',
        problem=['无向树，点权 `nums[i]`；删掉若干条边，让所有连通块的点权和 ==相等==',
                 '求最多能删多少条边',
                 '示例：`nums=[6,2,2,2,6]` → `2`；本视频用 5 个节点：`[2,1,4,2,3]` → `1`'],
        quote='如果一条边左右两侧的点权和都是 target 的倍数，那么这条边就可以删除。由于要使删除的边数最多，这条边必须删除。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举块数 `i`（`i` 是 `total` 的因子），则每块和 `target = total / i`',
              'DFS 统计子树和：==超过 target 返回 -1，等于返回 0（切断），不到就继续向上交==',
              '从大到小枚举块数，第一个成功的就是答案 `i - 1`'],
        result='块数 3 不行（子树和 6 超过 4），块数 2 可行：切掉节点 1 的那条边，删 1 条边',
        summary=['时间 `O(n·d(s))`，`d(s)` 最大 240；空间 `O(n)`',
                 '块数上界 `total // max(nums)`：因为每个点权至少是 `max(nums)`',
                 '「接水」类比：每满一杯就换下一杯，所以不会少于 `i` 块也不会多于 `i` 块',
                 '易错：`dfs` 返回 `0` 代表「这条边切断」，不是子树和为 0'],
    ),
)
