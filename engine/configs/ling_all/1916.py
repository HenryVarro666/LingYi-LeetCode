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


PREV = [-1, 0, 0, 1, 2]
NN = len(PREV)
TC = _tree_consts(NN, [[PREV[i], i] for i in range(1, NN)])
SIZE = [0] * NN
for _u in range(NN - 1, -1, -1):
    SIZE[_u] = 1 + sum(SIZE[c] for c in TC['ch'][_u])


def _state(S, B=None):
    I = B['_inner'] if S.get('_line') == 15 and B is not None else S['_inner']
    x = I.get('x')
    line = S.get('_line', 0)
    if x is None:
        return None, (10 ** 6 if line >= 21 else None)
    y, g = I.get('y'), S['g']
    if line == 13:
        t = TC['ent'][x]
    elif line in (16, 17, 18):
        t = TC['ext'][g[x][-1]] if g[x] and line != 18 else (TC['ext'][x] if line == 18 else TC['ent'][x])
    else:
        incl = line == 14 and B is not None and y is not None and B['_inner'].get('y') == y
        done = []
        for z in g[x]:
            if z == y and not incl:
                break
            done.append(z)
            if z == y:
                break
        t = TC['ext'][done[-1]] if done else TC['ent'][x]
    return x, t


def _live(S, u):
    I = S['_inner']
    if S['_line'] >= 14 and 'size' in I:
        return f"size={I['size']}"
    return ''


def _fml(S):
    if 'mul' not in S:
        return '答案 = `n!` ÷ ∏ `size[i]`：分子分母分别算，最后用逆元做除法'
    return f"分子 `fac` = =={S['fac']}==（= {NN}!），分母 `mul` = ∏size = =={S['mul']}=="


CONFIG = dict(
    num=1916, title='统计为蚁群构筑房间的不同顺序', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='树形 DP · n! ÷ ∏子树大小',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2486'],
    code='''
class Solution:
    def waysToBuildRooms(self, prevRoom: List[int]) -> int:
        MOD = 1_000_000_007
        n = len(prevRoom)
        g = [[] for _ in range(n)]
        fac = 1  # 分子
        for i in range(1, n):
            fac = fac * (i + 1) % MOD
            g[prevRoom[i]].append(i)

        mul = 1  # 分母
        def dfs(x: int) -> int:
            size = 1
            for y in g[x]:
                size += dfs(y)
            nonlocal mul
            mul = mul * size % MOD
            return size
        dfs(0)

        return fac * pow(mul, -1, MOD) % MOD
''',
    call='Solution().waysToBuildRooms([-1, 0, 0, 1, 2])',
    expect=6,
    views=[
        dict(type='text', size=26, h=60, fn=_fml),
        dict(type='custom', h=430, draw=_tree_draw(TC, _state, lambda u: str(u), note=lambda u: f'size={SIZE[u]}',
                                                   live=_live, title='房间树：黄 = 当前，蓝 = 递归路径，绿 = 子树大小已算完')),
        dict(type='calls', h=170),
    ],
    watch=[('x', 'x', 'blue'), ('size', 'size', 'orange'), ('fac', 'fac', 'cyan'), ('mul', 'mul', 'green')],
    skip=['MOD = 1_000_000_007', 'n = len(prevRoom)', 'g = [[] for', 'for i in range(1, n)', 'nonlocal mul'],
    captions={
        'fac = 1': '`fac` 做分子：最后要变成 `n!`',
        'fac = fac * (i + 1)': '`fac` 累乘 `{i + 1}`：现在是 `{i + 1}!` = =={fac}==',
        'g[prevRoom[i]].append(i)': '房间 `{i}` 必须在 `{prevRoom[i]}` 之后建 → 挂成 `{prevRoom[i]}` 的儿子',
        'mul = 1': '`mul` 做分母：所有子树大小的乘积',
        'dfs(0)': lambda S, B, r: '从根房间 0 开始 DFS，算每棵子树的大小' if r is None else '树遍历完，分子分母都齐了',
        'size = 1': '先算上自己：`size = 1`',
        'for y in g[x]': lambda S, B, r: (f'儿子都看完了：房间 `{S.x}` 的子树大小 `size = {S.size}`' if 'y' in B and B.y == S.y
                                          else f'`size = {S.size}`；看房间 `{S.x}` 的下一个儿子 `y = {S.y}`'),
        'size += dfs(y)': '进入儿子 `{y}`：它的子树大小会累加进 `size`（现在 `{size}`）',
        'mul = mul * size': '子树 `{x}` 在排列里是一段，必须==以 `{x}` 开头==：合法占 `1/{size}` → `mul` 乘 `{size}`：`{B.mul} × {size}` = =={mul}==',
        'return size': '返回房间 `{x}` 的子树大小 =={size}==',
        'return fac * pow': '答案 = `fac × mul⁻¹ mod p` = `{fac} ÷ {mul}` = =={ret}==（费马小定理求逆元）',
    },
    cards=dict(
        one_liner='把房间按建造顺序标号：合法排列占 n! 的 1/∏size',
        complexity='时间 `O(n + log M)`，空间 `O(n)`',
        problem=['`prevRoom[i]` 表示建房间 `i` 之前必须先建它，房间 0 已建好，求建完所有房间的不同顺序数（模 `10^9+7`）',
                 '关系构成一棵以 0 为根的树',
                 '示例：`prevRoom=[-1,0,0,1,2]` → `6`'],
        quote='所有排列总共有 n! 种，但其中肯定有不合法的……对于每棵子树 i，不以 i 的标记数字开头的排列都是不合法的，所以同样地，要把方案数除以 size[i]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['给节点按建造顺序标 `1..n`，DFS 收集标号得到 `1..n` 的一个排列',
              '合法排列要求每棵子树里最先出现的是子树的根 → 概率 `1/size[i]`',
              '答案 = `n! / ∏ size[i]`，除法用费马小定理的逆元 `pow(mul, -1, MOD)`'],
        summary=['时间 `O(n + log M)`，空间 `O(n)`',
                 '易错：分母要取模后求逆元，不能直接整除；`pow(x, -1, MOD)` 需要 Python 3.8+',
                 '`fac` 从 2 乘到 n（循环里乘 `i + 1`），`dfs` 的 `mul` 用 `nonlocal`',
                 '变形：无向树、对每个根求答案 → 换根 DP（ABC160F）'],
    ),
)
