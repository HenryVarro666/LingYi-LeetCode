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
TC = _tree_consts(6, EDGES)


def _loss(u):
    kids = TC['ch'][u]
    if not kids:
        return VALUES[u]
    return min(VALUES[u], sum(_loss(v) for v in kids))


def _state(S, B=None):
    I = B['_inner'] if S.get('_line') == 16 and B is not None else S['_inner']
    x = I.get('x')
    if x is None:
        return None, (10 ** 6 if S.get('_line', 0) >= 18 else None)
    line, y, g = S['_line'], I.get('y'), S['g']
    kids = TC['ch'][x]
    if line == 11:
        t = TC['ent'][x]
    elif line in (12, 17):
        t = TC['ext'][x]
    else:
        incl = line == 14 and B is not None and y is not None and B['_inner'].get('y') == y
        done = []
        for z in g[x]:
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
    if S['_line'] >= 14 and 'loss' in I:
        return f"loss={I['loss']}"
    return ''


CONFIG = dict(
    num=2925, title='在树上执行操作以后得到的最大分数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='树形 DP · 正难则反',
    tags=['灵神题单·动态规划', '难度分 1940'],
    code='''
class Solution:
    def maximumScoreAfterOperations(self, edges: List[List[int]], values: List[int]) -> int:
        g = [[] for _ in values]
        g[0].append(-1)  # 避免误把根节点当作叶子
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        # dfs(x, fa) 计算以 x 为根的子树是健康时，失去的最小分数
        def dfs(x: int, fa: int) -> int:
            if len(g[x]) == 1:  # x 是叶子
                return values[x]
            loss = 0  # 第二种情况
            for y in g[x]:
                if y != fa:
                    loss += dfs(y, x)  # 计算以 y 为根的子树是健康时，失去的最小分数
            return min(values[x], loss)  # 两种情况取最小值
        return sum(values) - dfs(0, -1)
''',
    call='Solution().maximumScoreAfterOperations(EDGES, VALUES)',
    setup='EDGES = [[0, 1], [0, 2], [0, 3], [2, 4], [4, 5]]\nVALUES = [5, 2, 5, 2, 1, 1]',
    expect=11,
    views=[
        dict(type='text', size=26, h=60, fn=lambda S: (
            f"总分 `sum(values)` = =={sum(VALUES)}==，减去最小损失" if 'x' not in S['_inner']
            else f"节点 `{S['_inner']['x']}`：要么丢掉自己 `{VALUES[S['_inner']['x']]}`，要么让儿子们各自健康")),
        dict(type='custom', h=470, draw=_tree_draw(TC, _state, lambda u: str(VALUES[u]), note=lambda u: f'损失 {_loss(u)}',
                                                   live=_live, title='树：圆内 = values，黄 = 当前，蓝 = 递归路径，绿 = 已算完')),
        dict(type='calls', h=170),
        dict(type='array', var='values', label='values', cell=64, h=130, pointers={'x': 'blue'}),
    ],
    watch=[('x', 'x', 'blue'), ('loss', 'loss', 'orange')],
    skip=['g = [[] for', 'g[x].append(y)', 'g[y].append(x)', 'for x, y in edges'],
    captions={
        'g[0].append(-1)': '给根节点 0 补一条假边 `0-(-1)`：这样根的度数至少 2，不会被当成叶子',
        'if len(g[x]) == 1': lambda S, B, r: (f'`g[{S.x}]` 只有 1 个邻居 → ==叶子==，必须失去它的分数' if len(S.g[S.x]) == 1
                                              else f'`g[{S.x}]` 有 {len(S.g[S.x])} 个邻居 → 不是叶子，两种情况取小'),
        'return values[x]': '叶子不能拿：路径和必须非 0，叶子又是路径最后一个点 → 返回 `values[{x}]` = =={values[x]}==',
        'loss = 0': '第二种情况：==保留== `values[x]`，那就要让每个儿子子树自己健康，损失累加到 `loss`',
        'for y in g[x]': lambda S, B, r: (f'邻居都看完了，`loss = {S.loss}`：保留 `values[{S.x}]` 的代价' if B.get('y') == S.y and 'y' in B else f'`loss = {S.loss}`；看 `x = {S.x}` 的下一个邻居 `y = {S.y}`'),
        'if y != fa': lambda S, B, r: (f'`y = {S.y}` 是父节点 `fa`，跳过' if S.y == S.fa else f'`y = {S.y}` 是儿子，递归算它的最小损失'),
        'loss += dfs(y, x)': '进入儿子 `{y}`：求它的子树健康时==最小损失==，再累加进 `loss`（现在 `{loss}`）',
        'return min(values[x], loss)': '情况一：丢 `values[{x}] = {values[x]}`（子孙全拿）；情况二：`loss = {loss}` → 取小 ==`{ret}`==',
        'return sum(values)': '答案 = `sum(values) - dfs(0, -1)` = `{sum(values)} - {sum(values) - ret}` = =={ret}==',
    },
    cards=dict(
        one_liner='正难则反：先全拿，再算最少要丢多少',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['树的每个节点有值，操作 = 拿走一个节点的值并把它清零',
                 '要求：根到每个叶子的路径和都 `≠ 0`（健康），求最大得分',
                 '示例：`values=[5,2,5,2,1,1]` → `11`'],
        quote='正难则反，先把所有 values[i] 加到答案中，然后考虑哪些 values[i] 不能选（撤销，不加入答案）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(x)`：让 `x` 子树健康，==最少==丢多少分',
              '选或不选：丢掉 `values[x]`（子孙随便拿），或保留它并让每个儿子子树健康',
              '两种情况取小；叶子只能丢自己。答案 = 总和 − `dfs(0)`'],
        summary=['时间 `O(n)`，空间 `O(n)`（递归深度最坏 n）',
                 '易错：根节点只有一个儿子时度数为 1，所以要补假边 `0 → -1`',
                 '叶子判断用 `len(g[x]) == 1`；递归时跳过父节点 `fa`',
                 '相似题：337. 打家劫舍 III（同样是选或不选的树形 DP）'],
    ),
)
