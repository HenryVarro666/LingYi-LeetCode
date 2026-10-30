ECOL = {1: 'red', 2: 'blue', 3: 'green'}
ENAME = {1: 'Alice 专用', 2: 'Bob 专用', 3: '公共边'}


def _root(par, v):
    while par[v] != v:
        v = par[v]
    return v


def _par(S):
    if 'bob_del' in S and S.get('g') is not None:
        return S['g']
    return S.get('f')


def _draw(cv, S, B, box, T):
    import math
    x0, y0, x1, y1 = box
    n = S['n']
    par = _par(S)
    cx, cy = (x0 + x1) / 2 - 40, (y0 + y1) / 2 + 14
    R = min((x1 - x0) / 2 - 150, (y1 - y0) / 2 - 62)
    pos = {}
    for t in range(n):
        a = -math.pi / 2 + 2 * math.pi * t / n
        pos[t] = (cx + R * math.cos(a), cy + R * math.sin(a))
    cv.text((x0 + 18, y0 + 4), '图（边色：绿 = 公共，红 = Alice，蓝 = Bob；节点底色 = 并查集里同一连通块）', 22, T['muted'], bold=True)
    cur = None
    L = S.get('_line', 0)
    ct = 2 if 'bob_del' in S else (1 if 'alice_del' in S else S.get('t'))
    if 'x' in S and 'y' in S and (10 <= L <= 27 or 32 <= L <= 40 or 46 <= L <= 55):
        cur = (S['x'], S['y'])
    for t, a, b in S['edges']:
        a -= 1
        b -= 1
        (ax, ay), (bx, by) = pos[a], pos[b]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy) or 1
        off = {3: 0, 1: 11, 2: -11}[t]
        ox, oy = -dy / L * off, dx / L * off
        p0, p1 = (ax + ox, ay + oy), (bx + ox, by + oy)
        if cur and {a, b} == set(cur) and t == ct:
            cv.line([p0, p1], T['yellow'], 12)
        cv.line([p0, p1], T[ECOL[t]], 5 if t == 3 else 4)
    palette = ['cyan', 'purple', 'yellow', 'orange']
    roots = {}
    for v in range(n):
        X, Y = pos[v]
        fill = T['panel2']
        if par is not None:
            r = _root(par, v)
            roots.setdefault(r, len(roots))
            fill = T[palette[roots[r] % 4]]
        cv.rect((X - 30, Y - 30, X + 30, Y + 30), fill=fill, outline=T['border'], width=2, r=30)
        cv.text((X, Y), v + 1, 30, T['bg'] if par is not None else T['text'], anchor='mm', bold=True)
    for k, t in enumerate((3, 1, 2)):
        X, Y = x1 - 190, y0 + 40 + k * 34
        cv.rect((X, Y + 8, X + 32, Y + 14), fill=T[ECOL[t]], r=3)
        cv.text((X + 44, Y + 12), ENAME[t], 22, T['text'], anchor='lm')


def _txt(S):
    if 'used_common' not in S:
        return ''
    s = f"公共边留下 `used_common = {S['used_common']}`，已删边 `res = {S.get('res', 0)}`"
    if 'alice_del' in S:
        s += f"；`alice_del = {S['alice_del']}`"
    if 'bob_del' in S:
        s += f"，`bob_del = {S['bob_del']}`"
    return s


CONFIG = dict(
    num=1579, title='保证图可完全遍历', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='并查集 · 先公共边再各自边',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Solution(object):
    def maxNumEdgesToRemove(self, n, edges):

        alice_edge = []
        bob_edge = []
        f = list(range(n))

        res = 0
        used_common = 0
        for t, x, y in edges:
            x -= 1
            y -= 1
            if t == 1:
                alice_edge.append([x, y])
            elif t == 2:
                bob_edge.append([x, y])
            else:
                fa_x = self.find(x, f)
                fa_y = self.find(y, f)
                if fa_x == fa_y:
                    res += 1
                else:
                    used_common += 1
                    if fa_x < fa_y:
                        f[fa_y] = fa_x
                    else:
                        f[fa_x] = fa_y

        g = f[:]

        alice_del = 0
        for x, y in alice_edge:
            fa_x = self.find(x, f)
            fa_y = self.find(y, f)
            if fa_x == fa_y:
                alice_del += 1
            elif fa_x < fa_y:
                f[fa_y] = fa_x
            else:
                f[fa_x] = fa_y
        
        if alice_del != len(alice_edge) - (n - 1 - used_common):
            return -1
        
        bob_del = 0
        for x, y in bob_edge:
            fa_x = self.find(x, g)
            fa_y = self.find(y, g)
            if fa_x == fa_y:
                bob_del += 1
            elif fa_x < fa_y:
                g[fa_y] = fa_x
            else:
                g[fa_x] = fa_y
        
        if bob_del != len(bob_edge) - (n - 1 - used_common):
            return -1
        
        return res + alice_del + bob_del

    def find(self, now, fa):
        if fa[now] != now:
            fa[now] = self.find(fa[now], fa)
        return fa[now]
''',
    call='Solution().maxNumEdgesToRemove(4, [[3,1,2],[3,2,3],[1,1,3],[1,2,4],[1,1,2],[2,3,4]])',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=320),
        dict(type='array', var=lambda S: S['f'], label='f（并查集，Alice 用）', h=135, index=False),
        dict(type='array', var=lambda S: S['g'] if 'bob_del' in S else S['f'], label='g（并查集，Bob 用：公共边之后的快照）', h=135, index=False),
        dict(type='text', fn=_txt, h=50, size=24),
    ],
    watch=[('t', 't', 'yellow'), ('x', 'x', 'blue'), ('y', 'y', 'pink'), ('res', 'res', 'green')],
    captions={
        'f = list(range(n))': '并查集 `f`：一开始每个点自成一块；==注意下标从 0 开始==，所以边端点要减 1',
        'res = 0': '`res` = 能删掉的边数；`used_common` = 真正留下的公共边数',
        'if t == 1': lambda S, B, r: f'这条边类型 `t = {S.t}`：' + {1: '只有 ==Alice== 能走，先存起来', 2: '只有 ==Bob== 能走，先存起来', 3: '==公共边==，两人都能走，优先处理'}[S.t],
        'alice_edge.append': 'Alice 边 `({x+1}, {y+1})` 先存着',
        'bob_edge.append': 'Bob 边 `({x+1}, {y+1})` 先存着',
        'bob_edge = []': '两个列表分别存 Alice、Bob 的专用边，公共边当场处理',
        'if fa_x == fa_y': lambda S, B, r: (f'点 `{S.x+1}` 的根是 `{S.fa_x+1}`，点 `{S.y+1}` 的根是 `{S.fa_y+1}`：'
                                             + ('==同一块，这条边多余==' if S.fa_x == S.fa_y else '不同块，这条边有用，要留')),
        'res += 1': '公共边成环，==删掉==：`res = {res}`',
        'used_common += 1': '公共边有用，保留：`used_common = {used_common}`',
        'f[fa_y] = fa_x': '合并：根小的做父亲，`f[{fa_y}] = {fa_x}`',
        'f[fa_x] = fa_y': '合并：根小的做父亲，`f[{fa_x}] = {fa_y}`',
        'g = f[:]': '==复制一份并查集==：`g` 留给 Bob，只含公共边；`f` 继续给 Alice 加边',
        'alice_del = 0': '`alice_del` 统计 Alice 的多余边',
        'for x, y in alice_edge': lambda S, B, r: ('Alice 的专用边处理完了' if (getattr(B, 'x', None), getattr(B, 'y', None)) == (S.x, S.y) else f'取 Alice 的边 `({S.x+1}, {S.y+1})`，在「公共边」的基础上继续加'),
        'elif fa_x < fa_y': '不同块，这条边要留：把两块合并，根小的做父亲',
        'g[fa_y] = fa_x': '合并（Bob 的并查集）：`g[{fa_y}] = {fa_x}`',
        'g[fa_x] = fa_y': '合并（Bob 的并查集）：`g[{fa_x}] = {fa_y}`',
        'alice_del != len': lambda S, B, r: (
            f'Alice 应保留 `n-1-used_common = {S.n-1-S.used_common}` 条专用边才能连通；实际保留 `{len(S.alice_edge)-S.alice_del}` 条 → '
            + ('==匹配，Alice 能连通==' if S.alice_del == len(S.alice_edge) - (S.n - 1 - S.used_common) else '==不匹配 → 无法连通，返回 -1==')),
        'bob_del = 0': '`bob_del` 统计 Bob 的多余边（用的是 `g`）',
        'for x, y in bob_edge': lambda S, B, r: ('Bob 的专用边处理完了' if (getattr(B, 'x', None), getattr(B, 'y', None)) == (S.x, S.y) else f'取 Bob 的边 `({S.x+1}, {S.y+1})`，在 `g`（只含公共边）上加'),
        'bob_del != len': lambda S, B, r: (
            f'Bob 应保留 `{S.n-1-S.used_common}` 条专用边；实际保留 `{len(S.bob_edge)-S.bob_del}` 条 → '
            + ('==匹配，Bob 也能连通==' if S.bob_del == len(S.bob_edge) - (S.n - 1 - S.used_common) else '==不匹配 → 返回 -1==')),
        'return res + alice_del': '三类多余边相加：`{res} + {alice_del} + {bob_del}` = =={ret}==',
    },
    skip=['alice_edge = []', 'fa[now]', 'x -= 1', 'y -= 1', 'elif t == 2', 'else:', 'self.find(x', 'self.find(y', 'used_common = 0'],
    max_steps=110,
    cards=dict(
        one_liner='公共边先用并查集建起来，再分别给 Alice、Bob 补边',
        complexity='时间 `O(m·α(n))`，空间 `O(n+m)`',
        problem=['`n` 个点，三类边：1 = 仅 Alice、2 = 仅 Bob、3 = 两人都能走',
                 '最多能删掉多少条边，使 Alice 和 Bob 都还能遍历整张图？',
                 '做不到则返回 `-1`',
                 '示例：`n=4, edges=[[3,1,2],[3,2,3],[1,1,3],[1,2,4],[1,1,2],[2,3,4]]` → `2`'],
        quote='一个自然的想法是先尽可能使用绿色边来连通各个节点。……先假设图中没有边，然后利用并查集来将边加入到图中，这个方法相比起来实现会简单得多。',
        quote_src='—— yiduobo 题解原文',
        idea=['各自连通只需要一棵生成树，共 `n-1` 条边；公共边能同时算进两棵树，越多越好',
              '先用并查集加公共边：成环的删掉（`res`），有用的保留（`used_common`）',
              '再在公共边的基础上，Alice、Bob 各自加专用边，成环的又是多余边；最后检查两人是否都连通'],
        summary=['时间 `O(m·α(n))`，空间 `O(n+m)`',
                 '易错：Bob 用的是公共边之后的快照 `g = f[:]`，不能和 Alice 共用同一份并查集',
                 '连通判断：专用边保留数必须刚好等于 `n-1-used_common`，否则返回 `-1`',
                 '原文为 Python 2 写法，`f = range(n)` 已改为 `f = list(range(n))`（Python 3 的 range 不可赋值）',
                 '同类：最小生成树 / 并查集判环（Kruskal）'],
    ),
)
