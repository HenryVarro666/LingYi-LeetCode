def _tree_consts(n, edges, sort_ch=False):
    g = [[] for _ in range(n)]
    for e in edges:
        g[e[0]].append(e[1])
        g[e[1]].append(e[0])
    par = [-1] * n
    ch = [[] for _ in range(n)]
    ent, ext, clk = [0] * n, [0] * n, [0]
    dep = [0] * n

    def go(u, p):
        par[u] = p
        ent[u] = clk[0]
        clk[0] += 1
        for v in (sorted(g[u]) if sort_ch else g[u]):
            if v != p:
                ch[u].append(v)
                dep[v] = dep[u] + 1
                go(v, u)
        ext[u] = clk[0]
        clk[0] += 1
    go(0, -1)
    xs, cnt = [0.0] * n, [0]

    def lay(u):
        if not ch[u]:
            xs[u] = cnt[0]
            cnt[0] += 1
        else:
            for v in ch[u]:
                lay(v)
            xs[u] = (xs[ch[u][0]] + xs[ch[u][-1]]) / 2
    lay(0)
    return dict(n=n, ch=ch, par=par, ent=ent, ext=ext, dep=dep, xs=xs, leaves=max(cnt[0], 1), maxd=max(dep))


def _tree_draw(tc, state, label, note=None, live=None, title='', elab=None, width_cap=170):
    """state(S) -> (cur, T): 当前节点 / 时钟（ext[u] <= T 的节点算已完成）；cur=None 表示未开始"""
    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        n, ch, par, ext = tc['n'], tc['ch'], tc['par'], tc['ext']
        cur, tm = state(S, B)
        path = set()
        u = cur
        while u is not None and u >= 0:
            path.add(u)
            u = par[u]
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
        W = x1 - x0 - 120
        dx = min(width_cap, W / max(1, tc['leaves'] - 1)) if tc['leaves'] > 1 else 0
        sx = x0 + 60 + (W - dx * (tc['leaves'] - 1)) / 2
        H = y1 - y0 - 100
        dy = min(120, H / max(1, tc['maxd']))
        R = 24
        P = [(sx + tc['xs'][i] * dx, y0 + 60 + tc['dep'][i] * dy) for i in range(n)]
        for u in range(n):
            for v in ch[u]:
                on = v in path and u in path
                cv.line([P[u], P[v]], T['yellow'] if on else T['border'], 4 if on else 3)
                if elab:
                    mx, my = (P[u][0] + P[v][0]) / 2, (P[u][1] + P[v][1]) / 2
                    cv.text((mx + 12, my), str(elab[(u, v)]), 22, T['orange'], anchor='lm', bold=True)
        for u in range(n):
            x, y = P[u]
            done = tm is not None and ext[u] <= tm
            if u == cur:
                fill, tc_ = T['yellow'], T['bg']
            elif u in path:
                fill, tc_ = T['blue'], T['bg']
            elif done:
                fill, tc_ = T['green'], T['bg']
            else:
                fill, tc_ = T['panel2'], T['text']
            cv.rect((x - R, y - R, x + R, y + R), fill=fill, outline=T['border'], r=R)
            cv.text((x, y), label(u), 24, tc_, anchor='mm', bold=True)
            cv.text((x - R - 4, y - R - 2), str(u), 18, T['dim'], anchor='rb', mono=True)
            if live and u == cur:
                s = live(S, u)
                if s:
                    cv.text((x + R + 8, y), s, 22, T['yellow'], anchor='lm', bold=True)
            elif note and done:
                s = note(u)
                if s:
                    cv.text((x + R + 8, y), s, 22, T['green'], anchor='lm', bold=True)
    return draw


EDGES = [[0, 1], [1, 2]]
COINS = [10, 10, 3]
K = 5
NN = 3
NJ = 3
G = [[] for _ in range(NN)]
for _a, _b in EDGES:
    G[_a].append(_b)
    G[_b].append(_a)
FP = {}


def _sim(i, j, fa, parent, seen):
    if (i, j) in seen:
        return
    seen.add((i, j))
    FP[(i, j)] = parent
    for c in sorted(G[i]):
        if c != fa:
            _sim(c, j, i, (i, j), seen)
            _sim(c, j + 1, i, (i, j), seen)


_sim(0, 0, None, None, set())


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    I = B['_inner'] if S.get('_line') in (23, 24) else S['_inner']
    f = S.get('f')
    cur = (I['now'], I['right_shift']) if 'now' in I and 'right_shift' in I else None
    line = S.get('_line', 0)
    tgt = None
    if cur and 'child' in I and line in (23, 24):
        tgt = (I['child'], cur[1] + (1 if line == 24 else 0))
    path = set()
    u = cur
    while u is not None and u in FP:
        path.add(u)
        u = FP[u]
    cv.text((x0 + 18, y0 + 4), '备忘表 f[now][right_shift]（? = 还是 None，只画前 3 列）', 22, T['muted'], bold=True)
    cw = min(120, (x1 - x0 - 290) / NJ)
    ch_ = min(70, (y1 - y0 - 110) / NN)
    sx, sy = x0 + 260, y0 + 90
    for j in range(NJ):
        cv.text((sx + j * cw + cw / 2, sy - 8), f'shift={j}', 20, T['dim'], anchor='mb', mono=True)
    for i in range(NN):
        cv.text((sx - 12, sy + i * ch_ + ch_ / 2), f'节点{i}（coins={COINS[i]}）', 21, T['muted'], anchor='rm', bold=True)
        for j in range(NJ):
            c = (i, j)
            X, Y = sx + j * cw, sy + i * ch_
            if c not in FP:
                cv.rect((X + 4, Y + 4, X + cw - 4, Y + ch_ - 4), outline=T['border'], r=8)
                continue
            val = f[i][j] if f else None
            if c == cur:
                fill, col = T['yellow'], T['bg']
            elif c in path:
                fill, col = T['blue'], T['bg']
            elif val is not None:
                fill, col = T['green'], T['bg']
            else:
                fill, col = T['panel2'], T['dim']
            cv.rect((X + 4, Y + 4, X + cw - 4, Y + ch_ - 4), fill=fill, outline=T['border'], r=8)
            cv.text((X + cw / 2, Y + ch_ / 2), '?' if val is None else str(val), 28, col, anchor='mm', bold=True)
            if c == tgt:
                cv.rect((X + 1, Y + 1, X + cw - 1, Y + ch_ - 1), outline=T['pink'], width=5, r=10)
    if tgt is not None and f:
        hit = f[tgt[0]][tgt[1]] is not None
        cv.text((x0 + 18, sy + NN * ch_ + 14), f'即将调用 dfs({tgt[0]}, {tgt[1]})（粉框）：' + ('表里已有值 → 直接返回' if hit else '表里还是 None → 要往下算'),
                22, T['pink'], bold=True)


def _opt(S, B):
    I = B['_inner'] if S.get('_line') in (23, 24) else S['_inner']
    if 'now' not in I:
        return '`f[now][right_shift]`：祖先已右移 `right_shift` 次时，`now` 子树的最大积分'
    if 'v1' in I:
        return f"`dfs({I['now']}, {I['right_shift']})`：方案一 `v1 = {I['v1']}`，方案二 `v2 = {I.get('v2', '?')}`"
    return f"`dfs({I['now']}, {I['right_shift']})`"


CONFIG = dict(
    num=2920, title='收集所有金币可获得的最大积分', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='树形 DP · f[now][right_shift] 备忘表',
    tags=['灵神题单·动态规划', '难度分 2351'],
    code='''
class Solution(object):
    def maximumPoints(self, edges, coins, k):

        n = len(edges) + 1
        g = {index : set() for index in range(n)}
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)

        f = [[None] * 14 for _ in range(n)]

        def dfs(now, right_shift, fa):
            if right_shift == 14:
                return 0

            if f[now][right_shift] is None:
                v1 = (coins[now] >> right_shift) - k
                v2 = coins[now] >> (right_shift + 1)
                for child in g[now]:
                    if child == fa:
                        continue
                    
                    v1 += dfs(child, right_shift, now)
                    v2 += dfs(child, right_shift + 1, now)
            
                f[now][right_shift] = max(v1, v2)
            
            return f[now][right_shift]
        
        return dfs(0, 0, None)
''',
    call='Solution().maximumPoints(EDGES, COINS, K)',
    setup='EDGES = [[0, 1], [1, 2]]\nCOINS = [10, 10, 3]\nK = 5',
    expect=11,
    views=[
        dict(type='text', size=24, h=60, fn=_opt),
        dict(type='custom', h=400, draw=_draw),
        dict(type='calls', h=170),
        dict(type='array', var='coins', label='coins（蓝箭头 = 当前节点 now）', cell=70, h=130, pointers={'now': 'blue'}),
    ],
    watch=[('now', 'now', 'blue'), ('right_shift', 'right_shift', 'cyan'), ('v1', 'v1', 'orange'), ('v2', 'v2', 'green')],
    skip=['n = len(edges)', 'g = {index', 'for x, y in edges', 'g[x].add(y)', 'g[y].add(x)', 'continue', 'if child == fa', 'f = [[None]'],
    max_steps=100,
    captions={
        'if right_shift == 14': lambda S, B, r: ('右移 14 次：所有金币都成 0，积分必为 0 → 直接返回' if S.right_shift == 14
                                                 else f'`right_shift = {S.right_shift}` < 14，还要算'),
        'if f[now][right_shift] is None': lambda S, B, r: (f'`f[{S.now}][{S.right_shift}]` 还是 None → ==没算过==，现在算' if S.f[S.now][S.right_shift] is None
                                                           else f'`f[{S.now}][{S.right_shift}] = {S.f[S.now][S.right_shift]}` 已经算过 → 跳过计算直接返回'),
        'v1 = (coins[now]': '方案一：当前节点得 `(coins >> {right_shift}) - k` = `{coins[now]} >> {right_shift}` 再减 `{k}` → `v1 = {v1}`',
        'v2 = coins[now]': '方案二：得 `coins[now] >> {right_shift + 1}`，孩子要多右移一次 → `v2 = {v2}`',
        'for child in g[now]': lambda S, B, r: (f'孩子都处理完：`v1 = {S.v1}`，`v2 = {S.v2}`' if 'child' in B and B.child == S.child
                                               else f'`child = {S.child}` 是父节点，跳过' if S.child == S.fa else f'看 `now = {S.now}` 的孩子 `child = {S.child}`，两个方案都要累加'),
        'if child == fa': lambda S, B, r: (f'`child = {S.child}` 是父节点，跳过' if S.child == S.fa else f'`child = {S.child}` 是孩子，两个方案都要往下累加'),
        'v1 += dfs(child, right_shift, now)': '方案一：孩子保持 `right_shift = {B.right_shift}`，累加 `f[{B.child}][{B.right_shift}]`',
        'v2 += dfs(child, right_shift + 1, now)': '方案二：孩子 `right_shift = {B.right_shift + 1}`，累加 `f[{B.child}][{B.right_shift + 1}]`',
        'f[now][right_shift] = max': '取较大者写入备忘表：`f[{now}][{right_shift}] = max({v1}, {v2})` = =={f[now][right_shift]}==',
        'return f[now][right_shift]': '返回 `f[{now}][{right_shift}]` = =={ret}==',
        'return dfs(0, 0, None)': lambda S, B, r: '从根节点、右移 0 次开始' if r is None else f'答案 = `f[0][0]` = =={r}==',
    },
    cards=dict(
        one_liner='用 `f[now][right_shift]` 记住子树在“祖先已右移若干次”下的最优积分',
        complexity='时间 `O(n log U)`，空间 `O(n log U)`',
        problem=['每个节点二选一收金币：得 `coins[i] - k`，或得 `floor(coins[i]/2)` 且子树金币全部减半',
                 '求收完所有节点的最大积分',
                 '示例：`edges=[[0,1],[1,2]], coins=[10,10,3], k=5` → `11`'],
        quote='注意到除以二向下取整实际上相当于右移操作，那么在这里就可以使用f[now][right_shift]表示以now为根节点的子树，其中now的祖先节点已经执行了right_shift次右移操作时，子树中可以得到的最大积分。',
        quote_src='—— yiduobo 题解原文',
        idea=['`coins ≤ 10000`，右移 14 次必为 0，所以 `right_shift == 14` 直接返回 0',
              '方案一：本节点得 `(coins >> shift) - k`，孩子 shift 不变',
              '方案二：本节点得 `coins >> (shift+1)`，孩子 shift 加 1；两者取大'],
        summary=['时间 `O(n log U)`，空间 `O(n log U)`（备忘表 `n × 14`）',
                 '`f[now][right_shift]` 只在值为 None 时才计算，避免重复递归',
                 '易错：右移 14 次的分支要在函数开头返回 0，否则 `f` 会越界',
                 '对比灵神：灵神用 `@cache` 且 `j < 13` 提前剪枝；yiduobo 手写备忘表并在入口判断 14',
                 '原文为 Python 2 风格，在 Python 3 下无需修改即可运行'],
    ),
)
