import math


def _ln(code, sub):
    """1-based line number of the first code line containing sub (leading blank line stripped)"""
    for k, s in enumerate(code.strip('\n').split('\n')):
        if sub in s:
            return k + 1
    return -1


def _gdraw(cv, box, T, pos, E, node_fn, edge_fn, label_fn=None, title='', directed=True, R=30, base=0, above=None):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    w = x1 - x0 - 140
    h = y1 - y0 - 170
    P = [(x0 + 70 + fx * w, y0 + 80 + fy * h) for fx, fy in pos]
    es = set(E)
    for (a, b) in E:
        col, wd = edge_fn(a, b)
        (ax, ay), (bx, by) = P[a], P[b]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        off = 10 if (b, a) in es else 0
        nx, ny = -uy * off, ux * off
        p0 = (ax + ux * R + nx, ay + uy * R + ny)
        p1 = (bx - ux * (R + 2) + nx, by - uy * (R + 2) + ny)
        if directed:
            cv.arrow(p0, p1, col, wd, head=16)
        else:
            cv.line([p0, p1], col, wd)
    for i, (x, y) in enumerate(P):
        fill, tc, ring = node_fn(i)
        cv.rect((x - R, y - R, x + R, y + R), fill=fill, r=R, outline=ring or T['border'], width=5 if ring else 1)
        cv.text((x, y), i + base, 26, tc, anchor='mm', bold=True)
        if label_fn:
            lab = label_fn(i)
            if lab:
                if above and above(i):
                    cv.text((x, y - R - 6), lab[0], 21, lab[1], anchor='mb', bold=True)
                else:
                    cv.text((x, y + R + 8), lab[0], 21, lab[1], anchor='mt', bold=True)


EDGES = [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]
POS = [(0.35, 0.12), (0.8, 0.12), (0.8, 0.88), (0.35, 0.88), (0.0, 0.12)]
CODE = '''
class Solution(object):
    def findRedundantConnection(self, edges):
        
        n = len(edges)
        fa = [index for index in range(n)]

        for edge in edges:
            x, y = edge
            x -= 1
            y -= 1
            if self.find(x, fa) == self.find(y, fa):
                return edge
            
            if fa[x] < fa[y]:
                fa[fa[y]] = fa[x]
            else:
                fa[fa[x]] = fa[y]

    def find(self, x, fa):
        if fa[x] == x:
            return x
        
        tmp = self.find(fa[x], fa)
        fa[x] = tmp
        return tmp
'''
L_RET = _ln(CODE, 'return edge')
L_UNION = (_ln(CODE, 'if fa[x] < fa[y]'), _ln(CODE, 'fa[fa[y]] = fa[x]'), _ln(CODE, 'fa[fa[x]] = fa[y]'))


def _root(fa, x):
    while fa[x] != x:
        x = fa[x]
    return x


def _draw(cv, S, B, box, T):
    edges = S.get('edges') or EDGES
    cur = S.get('edge')
    idx = next((k for k, e in enumerate(edges) if e is cur), None) if cur is not None else None
    line = S.get('_line')
    done_ret = line == L_RET

    def node(i):
        return T['panel2'], T['text'], None

    def ecol(a, b):
        k = edges.index([a + 1, b + 1])
        if idx is None:
            return T['dim'], 3
        if k == idx:
            return (T['red'], 7) if done_ret else (T['yellow'], 6)
        if k < idx:
            return T['green'], 5
        return T['dim'], 3

    def lab(i):
        fa = S.get('fa')
        if fa is None:
            return None
        return (f'fa={fa[i] + 1}', T['muted'])
    E = [(a - 1, b - 1) for a, b in edges]
    _gdraw(cv, box, T, POS, E, node, ecol, lab, '无向图（黄 = 正在加的边，绿 = 已加入的树边，红 = 冗余边，fa = 并查集父节点编号）', directed=False, base=1, above=lambda i: POS[i][1] < 0.5)


CONFIG = dict(
    num=684, title='冗余连接', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='并查集 · 找第一条成环的边',
    tags=['灵神题单·图论算法', '灵神题单·常用数据结构'],
    code=CODE,
    call=f'Solution().findRedundantConnection({EDGES})',
    expect=[1, 4],
    skip=['n = len(edges)', 'x -= 1'],
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var='fa', label='fa（下标 = 点编号 − 1，值 = 父节点下标）', h=130, cell=70, pointers={'x': 'blue', 'y': 'pink'}),
        dict(type='calls', h=170),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('edge', 'edge', 'yellow')],
    captions={
        'fa = [index': '`fa[x]` 是 x 的祖先，开始时每个点自己是自己的祖先：`{fa}`',
        'for edge in edges': '按顺序枚举每条边：`{edge}`',
        'x, y = edge': '这条边连接点 `{edge[0]}` 与 `{edge[1]}`',
        'y -= 1': '点编号从 1 开始，减一变成下标：`x = {x}`，`y = {y}`',
        'if self.find(x, fa) == self.find(y, fa)': lambda S, B, r: (
            f'`find({S.x}) = {_root(S.fa, S.x)}`，`find({S.y}) = {_root(S.fa, S.y)}`：' + (
                '祖先相同 → 两点已经通过别的边连通，这条边就是==冗余边==' if _root(S.fa, S.x) == _root(S.fa, S.y)
                else '祖先不同 → 这条边安全，继续合并')),
        'return edge': '返回 `{edge}`：加上它就成环了',
        'if fa[x] < fa[y]': '`fa[{x}] = {fa[x]}`，`fa[{y}] = {fa[y]}`：把==较大的祖先==指向较小的',
        'fa[fa[y]] = fa[x]': '合并：让 `fa[{B.fa[y]}]` 指向 `{B.fa[x]}`，`fa` → `{fa}`',
        'fa[fa[x]] = fa[y]': '合并：让 `fa[{B.fa[x]}]` 指向 `{B.fa[y]}`，`fa` → `{fa}`',
        'if fa[x] == x': lambda S, B, r: (f'`fa[{S.x}] = {S.fa[S.x]}` 就是自己 → 找到祖先 {S.x}' if S.fa[S.x] == S.x
                                          else f'`fa[{S.x}] = {S.fa[S.x]}` 不是自己 → 继续往上找'),
        'return x': '祖先是 `{x}`',
        'tmp = self.find': '往上找到祖先 `{tmp}`',
        'fa[x] = tmp': '路径压缩：`fa[{x}]` 直接指向祖先 `{tmp}`',
        'return tmp': '把祖先 `{tmp}` 返回给上一层',
    },
    cards=dict(
        one_liner='并查集：两端祖先相同的那条边，就是多余的',
        complexity='时间 `O(n·α(n))`，空间 `O(n)`',
        problem=['无向图原本是一棵树（`n` 个点 `n-1` 条边），现在多加了一条边，变成 `n` 条边、恰好有一个环',
                 '找出一条可以删去的边，使剩下的图是树；有多个答案时返回==最后出现==的那条',
                 '示例：`[[1,2],[2,3],[3,4],[1,4],[1,5]]` → `[1,4]`'],
        quote='若此时fa[x]等于fa[y]，说明二者已经通过别的边连接在一起了，因此当前边就是最终的答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['`fa[x]` 记录 x 的祖先，按顺序一条条加边',
              '两端祖先不同：合并，==较大的祖先指向较小的==',
              '两端祖先相同：之前已经连通，这条边再加就成环，直接返回'],
        summary=['时间近似 `O(n)`，空间 `O(n)`；`find` 带路径压缩',
                 '点编号从 1 开始，进并查集前要减一，返回时用原始的 `edge`',
                 '题目只有一个环，所以第一条让两端已连通的边，就是最后出现的可删边',
                 '同类题：685 冗余连接 II（有向图，要分入度情况）'],
    ),
)
