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


EDGES = [[0, 1], [0, 2], [0, 3], [2, 4], [4, 5]]
VALUES = [5, 2, 5, 2, 1, 1]
TC = _tree_consts(6, EDGES, sort_ch=True)


def _res(u):
    kids = TC['ch'][u]
    tv = sum(_res(c)[0] for c in kids)
    ts = sum(_res(c)[1] for c in kids)
    if ts == 0:
        return 0, VALUES[u]
    return max(tv + VALUES[u], ts), ts + VALUES[u]


def _state(S, B=None):
    I = B['_inner'] if S.get('_line') == 17 and B is not None else S['_inner']
    x = I.get('now')
    if x is None:
        return None, (10 ** 6 if S.get('_line', 0) >= 26 else None)
    line, y = S['_line'], I.get('child')
    kids = TC['ch'][x]
    if line in (11, 12):
        t = TC['ent'][x]
    elif line in (22, 24):
        t = TC['ext'][x]
    elif line == 21:
        t = TC['ext'][kids[-1]] if kids else TC['ent'][x]
    else:
        incl = (line == 14 and B is not None and y is not None and B['_inner'].get('child') == y) or line in (18, 19)
        done = []
        for z in sorted(S['g'][x]):
            if z == y and not incl:
                break
            if z in kids:
                done.append(z)
            if z == y:
                break
        t = TC['ext'][done[-1]] if done else TC['ent'][x]
    return x, t


def _live(S, u):
    I = S['_inner']
    if S['_line'] >= 14 and 'tot_s' in I:
        return f"tot_v={I['tot_v']} tot_s={I['tot_s']}"
    return ''


def _opt(S):
    I = S['_inner']
    if 'now' not in I or 'tot_s' not in I:
        return '`dfs` 返回 `(最大合法取值, 子树节点值之和)`'
    x, tv, ts = I['now'], I['tot_v'], I['tot_s']
    if S['_line'] in (21, 22, 24) and S['_line'] >= 21:
        if ts == 0:
            return f"节点 {x} 是叶子（`tot_s = 0`）：必须保留它 → 最大合法取值 ==0=="
        return f"留下 {VALUES[x]}：取 `tot_s` = {ts}；拿走 {VALUES[x]}：`tot_v + values` = {tv} + {VALUES[x]} = {tv + VALUES[x]}"
    return f"累加儿子们的 `(v, s)`：`tot_v = {tv}`，`tot_s = {ts}`"


CONFIG = dict(
    num=2925, title='在树上执行操作以后得到的最大分数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='树形 DP · 保留根 / 取走根',
    tags=['灵神题单·动态规划', '难度分 1940'],
    code='''
class Solution(object):
    def maximumScoreAfterOperations(self, edges, values):

        n = len(edges) + 1
        g = {index : set() for index in range(n)}
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)

        def dfs(now, fa):
            tot_v = 0
            tot_s = 0

            for child in g[now]:
                if child == fa:
                    continue
                v, s = dfs(child, now)
                tot_s += s
                tot_v += v

            if tot_s == 0:
                return 0, values[now]
            else:
                return max(tot_v + values[now], tot_s), tot_s + values[now]
        
        return dfs(0, None)[0]
''',
    call='Solution().maximumScoreAfterOperations(EDGES, VALUES)',
    setup='EDGES = [[0, 1], [0, 2], [0, 3], [2, 4], [4, 5]]\nVALUES = [5, 2, 5, 2, 1, 1]',
    expect=11,
    views=[
        dict(type='text', size=24, h=60, fn=_opt),
        dict(type='custom', h=470, draw=_tree_draw(TC, _state, lambda u: str(VALUES[u]), note=lambda u: f'{_res(u)}',
                                                   live=_live, title='树：圆内 = values，旁注 = 返回的 (v, s)')),
        dict(type='calls', h=150),
        dict(type='array', var='values', label='values', cell=64, h=130, pointers={'now': 'blue'}),
    ],
    watch=[('now', 'now', 'blue'), ('tot_v', 'tot_v', 'orange'), ('tot_s', 'tot_s', 'cyan'), 'v', 's'],
    skip=['n = len(edges)', 'g = {index', 'for x, y in edges', 'g[x].add(y)', 'g[y].add(x)', 'continue'],
    captions={
        'tot_v = 0': '`tot_v`：儿子们==合法最大取值==之和（儿子根值可能没取）',
        'tot_s = 0': '`tot_s`：儿子们子树==全部节点值==之和',
        'for child in g[now]': lambda S, B, r: (f'儿子都处理完：`tot_v = {S.tot_v}`，`tot_s = {S.tot_s}`' if 'child' in B and B.child == S.child
                                                else f'看 `now = {S.now}` 的邻居 `child = {S.child}`'),
        'if child == fa': lambda S, B, r: (f'`child = {S.child}` 是父节点，跳过' if S.child == S.fa else f'`child = {S.child}` 是儿子，往下递归'),
        'v, s = dfs(child, now)': '递归求儿子 `{child}` 子树的 `(v, s)`：最大合法取值、节点值之和',
        'tot_s += s': '儿子返回 `s = {s}`：`tot_s` → =={tot_s}==',
        'tot_v += v': '儿子返回 `v = {v}`：`tot_v` → =={tot_v}==',
        'if tot_s == 0': lambda S, B, r: (f'`tot_s = 0`：没有儿子 → 叶子' if S.tot_s == 0
                                         else f'`tot_s = {S.tot_s} ≠ 0`：有儿子，比较两种方案'),
        'return 0, values[now]': '叶子必须保留：最大合法取值 ==0==，节点值之和 `{values[now]}`',
        'return max(tot_v': '保留根：取 `tot_s = {tot_s}`；取走根：`tot_v + values[{now}] = {tot_v + values[now]}` → 取大 ==`{ret[0]}`==，和 = `{ret[1]}`',
        'return dfs(0, None)': lambda S, B, r: ('从根 `dfs(0, None)` 开始，答案取返回值的第一个数' if r is None else f'根节点返回的第一个数就是答案 ==`{r}`=='),
    },
    cards=dict(
        one_liner='每棵子树二选一：留下根值，或取走根值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['树上每个节点有正值，可取走节点的值（取走后清零）',
                 '要求取走后，根到每个叶子的路径上不能“值全被取走”',
                 '示例一：`values=[5,2,5,2,1,1]` → `11`'],
        quote='对于一颗子树，可以选择保留其根节点值，这种情况下，由于树中节点值都是正数，因此就应该将子树中其他的节点值全部取走；另一种选择则是取走根节点值，那么之后的合法性保证则需要下放到当前子树的子树中进行。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个节点返回两个数：`v` = 合法最大取值，`s` = 子树节点值之和',
              '留下根：其余全取，得 `tot_s`；取走根：儿子们各自合法，得 `tot_v + values[now]`',
              '叶子 `tot_s = 0`：必须留下，`v = 0`'],
        summary=['时间 `O(n)`，空间 `O(n)`（递归深度）',
                 '易错：叶子靠 `tot_s == 0` 判断，所以值必须是正数（本题 ≥ 1）',
                 '对比灵神：灵神算“最少丢多少”，yiduobo 直接算“最多取多少”，两种方向等价',
                 '原文为 Python 2 写法，在 Python 3 下无需修改即可运行'],
    ),
)
