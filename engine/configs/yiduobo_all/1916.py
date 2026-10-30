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
TC = _tree_consts(NN, [[PREV[i], i] for i in range(1, NN)], sort_ch=True)
CNT = [0] * NN
WAYS = [0] * NN
for _u in range(NN - 1, -1, -1):
    CNT[_u] = 1 + sum(CNT[c] for c in TC['ch'][_u])
    _w = math.factorial(CNT[_u] - 1)
    for _c in TC['ch'][_u]:
        _w = _w * WAYS[_c] // math.factorial(CNT[_c])
    WAYS[_u] = _w


def _state(S, B=None):
    I = B['_inner'] if S.get('_line') == 35 and B is not None else S['_inner']
    x = I.get('now')
    line = S.get('_line', 0)
    if x is None:
        return None, (10 ** 6 if line >= 18 and 'sons' in S and line < 20 and False else None)
    y, sons = I.get('son'), S['sons']
    kids = TC['ch'][x]
    if line in (32, 33):
        t = TC['ent'][x]
    elif line == 42:
        t = TC['ext'][x]
    elif line == 40:
        t = TC['ext'][kids[-1]] if kids else TC['ent'][x]
    else:
        incl = (line == 34 and B is not None and y is not None and B['_inner'].get('son') == y) or line in (36, 37, 38)
        done = []
        for z in sorted(sons[x]):
            if z == y and not incl:
                break
            done.append(z)
            if z == y:
                break
        t = TC['ext'][done[-1]] if done else TC['ent'][x]
    return x, t


def _live(S, u):
    I = S['_inner']
    if S['_line'] >= 34 and 'tot_cnt' in I:
        return f"cnt={I['tot_cnt']}"
    return ''


def _fml(S):
    I = S['_inner']
    if 'now' not in I or 'tot_cnt' not in I:
        return '`f[now]` = 以 now 为根的建造方案数；`cnt[now]` = 子树节点数'
    return f"`res = (cnt-1)! × ∏ f[k] / cnt[k]!`：现在 `res = {I['res']}`，`tot_cnt = {I['tot_cnt']}`"


CONFIG = dict(
    num=1916, title='统计为蚁群构筑房间的不同顺序', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='树形 DP · 子树方案数 × 多重集排列',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2486'],
    code='''
class Solution(object):
    def waysToBuildRooms(self, prevRoom):

        n = len(prevRoom)
        mod = 10 ** 9 + 7

        fac = [1]
        inv_fac = [1]
        for num in range(1, n + 1):
            fac.append(fac[-1] * num % mod)
            inv_fac.append(self.quickPow(fac[-1], mod - 2, mod))
        
        sons = {index : set() for index in range(n)}
        for index, fa in enumerate(prevRoom):
            if index > 0:
                sons[fa].add(index)
        
        return self.dfs(0, sons, fac, inv_fac, mod)[0]
    
    def quickPow(self, base, p, mod):
        if p == 1:
            return base
        
        res = self.quickPow(base, p // 2, mod)
        res = res * res % mod
        if p % 2 == 1:
            res = res * base % mod
        
        return res

    def dfs(self, now, sons, fac, inv_fac, mod):
        res = 1
        tot_cnt = 1
        for son in sons[now]:
            ways, cnt = self.dfs(son, sons, fac, inv_fac, mod)
            res = res * ways % mod
            res = res * inv_fac[cnt] % mod
            tot_cnt += cnt
        
        res = res * fac[tot_cnt - 1] % mod

        return res, tot_cnt
''',
    call='Solution().waysToBuildRooms([-1, 0, 0, 1, 2])',
    setup='import math',
    expect=6,
    views=[
        dict(type='text', size=24, h=60, fn=_fml),
        dict(type='custom', h=380, draw=_tree_draw(TC, _state, lambda u: str(u), note=lambda u: f'({WAYS[u]}, {CNT[u]})',
                                                   live=_live, title='房间树：旁注 = dfs 返回的 (方案数, 子树节点数)')),
        dict(type='array', var='fac', label='fac[i] = i!（取模后）', cell=70, h=130),
        dict(type='calls', h=150, hide=('self', 'sons', 'fac', 'inv_fac', 'mod')),
    ],
    watch=[('now', 'now', 'blue'), ('res', 'res', 'orange'), ('tot_cnt', 'tot_cnt', 'cyan'), ('ways', 'ways', 'green'), ('cnt', 'cnt', 'pink')],
    skip=[21, 22, 24, 25, 26, 27, 29, 'n = len(prevRoom)', 'mod = 10 ** 9', 'for num in range', 'sons = {index', 'for index, fa', 'if index > 0'],
    max_steps=100,
    captions={
        'fac = [1]': '`fac[i]` 存 `i!` 对 `mod` 取模的结果',
        'inv_fac = [1]': '`inv_fac[i]` 存 `i!` 的乘法逆元，用来做除法',
        10: '`fac[{num}] = {num}!` = =={fac[-1]}==',
        11: '用快速幂 + 费马小定理求 `{num}!` 的逆元：`{num}!^(mod-2)`（模逆元很大，不展开）',
        'sons[fa].add': '房间 `{index}` 要在 `{fa}` 之后建 → 记为 `{fa}` 的儿子',
        'return self.dfs(0': lambda S, B, r: '从根 0 开始，`dfs` 返回 `(方案数, 节点数)`，答案取第一个' if r is None else f'根的方案数 = =={r}==',
        'res = 1': '`res` 从 1 开始，会累乘各儿子的方案数',
        'tot_cnt = 1': '`tot_cnt` 先算上 `now` 自己',
        'for son in sons[now]': lambda S, B, r: (f'儿子都处理完：`tot_cnt = {S.tot_cnt}`，子树共 {S.tot_cnt} 个节点' if 'son' in B and B.son == S.son
                                                 else f'看 `now = {S.now}` 的下一个儿子 `son = {S.son}`'),
        'ways, cnt = self.dfs': '递归求儿子 `{son}` 的 `(ways, cnt)`：它子树的方案数、节点数',
        'res = res * ways': '乘上儿子的方案数：`res = {res}`',
        'res = res * inv_fac[cnt]': '儿子的 `cnt = {cnt}` 个位置内部顺序已由 `ways` 决定 → 除以 `{cnt}!`（乘逆元，取模后的数看着很怪）：`res = {res}`',
        'tot_cnt += cnt': '节点数累加：`tot_cnt = {tot_cnt}`',
        'res = res * fac[tot_cnt - 1]': '除根外还有 `{tot_cnt - 1}` 个节点，先当成 `{tot_cnt - 1}!` 种排列 → `res = {res}`',
        'return res, tot_cnt': '节点 `{now}`：方案数 =={res}==，子树节点数 `{tot_cnt}`',
    },
    cards=dict(
        one_liner='子树里的节点插进排列：乘 `(cnt-1)!`，再除以每个儿子的 `cnt!` 乘 `f`',
        complexity='时间 `O(n log mod)`，空间 `O(n)`',
        problem=['`prevRoom[i]` 表示建房间 `i` 之前要先建它，房间 0 已建好，求建完所有房间的不同顺序数（模 `10^9+7`）',
                 '关系是一棵以 0 为根的树',
                 '示例：`prevRoom=[-1,0,0,1,2]` → `6`'],
        quote='对于这(cnt[now] - 1)！种方案，都可以视为一个排列……不考虑形态的话，这cnt[k]个位置一共可以提供cnt[k]！种构造方案，但是由于构造有先后顺序，因此实际上合法的构造只有f[k]种，于是此时就应该除以cnt[k]！，再乘以f[k]。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[now]`：以 `now` 为根的子树的建造方案数；`cnt[now]`：子树节点数',
              '除了 `now` 先建，其余 `cnt-1` 个节点任意排：`(cnt-1)!` 种',
              '每个儿子子树占 `cnt[k]` 个位置，内部只有 `f[k]` 种合法 → 乘 `f[k]` 除 `cnt[k]!`'],
        summary=['时间 `O(n log mod)`（每个阶乘求一次逆元），空间 `O(n)`',
                 '阶乘要边算边取模；除法用费马小定理求逆元（快速幂）',
                 '原文为 Python 2 写法，快速幂里的 `p / 2` 已改为 `p // 2`（整数除法）',
                 '对比灵神：灵神一个公式 `n! / ∏size` 搞定；yiduobo 逐层算 `f` 和 `cnt`，思路等价',
                 '本视频跳过了 `quickPow` 内部的递归，只展示 `dfs`'],
    ),
)
