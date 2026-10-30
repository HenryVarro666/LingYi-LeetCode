PTS = [[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]


def _prep():
    n = len(PTS)
    es = []
    for i in range(n - 1):
        for j in range(i + 1, n):
            es.append([i, j, abs(PTS[i][0] - PTS[j][0]) + abs(PTS[i][1] - PTS[j][1])])
    es = sorted(es, key=lambda d: d[2])
    fa = list(range(n))

    def find(x):
        while fa[x] != x:
            x = fa[x]
        return x
    ok = []
    for x, y, l in es:
        a, b = find(x), find(y)
        ok.append(a != b)
        if a != b:
            fa[max(a, b)] = min(a, b)
    return es, ok


SORTED, TAKEN = _prep()


def _k(S):
    """当前 kruskal 枚举到的边在 SORTED 中的下标"""
    if 'res' not in S or 'l' not in S or not isinstance(S.get('x'), int):
        return None
    for k, (a, b, l) in enumerate(SORTED):
        if (a, b) == (S['x'], S['y']):
            return k
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '平面上的点（绿边 = 已选入生成树，黄边 = 正在考虑，红虚线 = 成环舍弃）', 21, T['muted'], bold=True)
    mx = max(p[0] for p in PTS)
    my = max(p[1] for p in PTS)
    pw, ph = (x1 - x0 - 160), (y1 - y0 - 110)
    sc = min(pw / mx, ph / my) * 0.95
    ox = x0 + 80 + (pw - mx * sc) / 2
    oy = y1 - 40

    def P(i):
        return ox + PTS[i][0] * sc, oy - PTS[i][1] * sc

    k = _k(S)
    if k is not None:
        cur_done = S['_line'] != 12  # 12 行（for）只是取出了这条边
        for t in range(k + (1 if cur_done else 0)):
            a, b, l = SORTED[t]
            if t == k:
                continue
            if TAKEN[t]:
                cv.line([P(a), P(b)], T['green'], 6)
            else:
                cv.dashed(P(a), P(b), T['red'], 2)
        a, b, l = SORTED[k]
        cv.line([P(a), P(b)], T['yellow'], 6)
        (ax, ay), (bx, by) = P(a), P(b)
        cv.text(((ax + bx) / 2, (ay + by) / 2 - 8), f'{l}', 24, T['yellow'], anchor='mb', bold=True)
    elif 'res' in S and 'l' in S:   # 循环结束
        for t, (a, b, l) in enumerate(SORTED):
            if TAKEN[t]:
                cv.line([P(a), P(b)], T['green'], 6)
    elif S.get('edges'):
        for a, b, l in S['edges']:
            cv.line([P(a), P(b)], T['border'], 2)
        a, b, l = S['edges'][-1]
        cv.line([P(a), P(b)], T['yellow'], 4)
    R = 24
    for i, (px, py) in enumerate(PTS):
        X, Y = P(i)
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=T['blue'], outline=T['border'], width=2)
        cv.text((X, Y), i, 24, T['bg'], anchor='mm', bold=True)
        cv.text((X + R + 6, Y + 4), f'({px},{py})', 18, T['dim'], anchor='la')


def _edge_fmt(e):
    return f'{e[0]}-{e[1]}:{e[2]}'


def _for(S, B, ret):
    k = _k(S)
    if k is None or ('x' in B and (B.x, B.y) == (S.x, S.y)):
        return '所有边都枚举完了'
    a, b, l = SORTED[k]
    return f'按长度从小到大取边 `{a}-{b}`，长度 `{l}`'


def _if(S, B, ret):
    if S.fa_x != S.fa_y:
        return f'`{S.x}` 的根 {S.fa_x} ≠ `{S.y}` 的根 {S.fa_y}：两点==不连通== → 选这条边'
    return f'`{S.x}`、`{S.y}` 的根都是 {S.fa_x}：已经连通，再选会==成环== → 跳过'


CONFIG = dict(
    num=1584, title='连接所有点的最小费用', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='枚举点对建边 + Kruskal',
    tags=['labuladong', '灵神题单·图论算法'],
    code='''
class Solution(object):
    def minCostConnectPoints(self, points):

        n = len(points)
        edges = []
        for i in range(n - 1):
            for j in range(i + 1, n):
                edges.append([i, j, abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])])

        fa = list(range(n))
        res = 0
        for x, y, l in sorted(edges, key=lambda d:d[2]):
            fa_x = self.find(x, fa)
            fa_y = self.find(y, fa)
            if fa_x != fa_y:
                if fa_x < fa_y:
                    fa[fa_y] = fa_x
                else:
                    fa[fa_x] = fa_y
                res += l

        return res

    def find(self, now, fa):
        if fa[now] != now:
            fa[now] = self.find(fa[now], fa)
        return fa[now]
''',
    call=f'Solution().minCostConnectPoints({PTS})',
    expect=20,
    views=[
        dict(type='custom', draw=_draw, h=430),
        dict(type='array', var='fa', label='fa（并查集：fa[i] 是 i 的父亲）', cell=80, h=150,
             color=lambda S, i, v: 'green' if v != i else None),
    ],
    watch=[('边', lambda S: f"{S['x']}-{S['y']}" if isinstance(S.get('x'), int) and 'l' in S else None, 'yellow'),
           'l', 'fa_x', 'fa_y', ('res', 'res', 'green')],
    skip=['for j in range(i + 1, n)', 'for i in range(n - 1)', 'if fa[now] != now', 'fa[now] = self.find', 'return fa[now]',
          'fa_x = self.find', 'fa_y = self.find', 'n = len(points)', 'if fa_x < fa_y'],
    captions={
        'edges = []': '点数不多：直接==两两枚举点对==，算曼哈顿距离当边权',
        'edges.append': lambda S, B, r: f'边 `{S.i}-{S.j}`：`|{S.points[S.i][0]}-{S.points[S.j][0]}| + |{S.points[S.i][1]}-{S.points[S.j][1]}|` = `{S.edges[-1][2]}`',
        'fa = list(range(n))': '共 `{len(edges)}` 条边。并查集初始化：每个点==自成一个集合==',
        'res = 0': '`res`：最小生成树的总长度',
        'for x, y, l in sorted': _for,
        'if fa_x != fa_y': _if,
        'fa[fa_y] = fa_x': '合并：`fa[{fa_y}] = {fa_x}`（编号小的根当父亲）',
        'fa[fa_x] = fa_y': '合并：`fa[{fa_x}] = {fa_y}`（编号小的根当父亲）',
        'res += l': '`res` += `{l}` → =={res}==',
        'return res': '所有点连通，最小费用 =={res}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='两两建边，按长度排序，Kruskal 贪心选不成环的最短边',
        complexity='时间 `O(n² log n)`，空间 `O(n²)`',
        problem=['平面上 `n` 个点，连接两点的费用是==曼哈顿距离== `|xi-xj| + |yi-yj|`',
                 '求让所有点连通的最小总费用（即最小生成树）',
                 '示例：`[[0,0],[2,2],[3,10],[5,2],[7,0]]` → `20`'],
        quote='由于题目中的点数规模不大，因此可以直接==两两枚举点对，计算距离形成边==……得到边之后，使用kurskal算法求解最小生成树即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['边数 `O(n²)`，排序后从短到长枚举',
              '用并查集判断两端是否已连通：==不连通就选==，连通就跳过（否则成环）',
              '作者提到：三角形里最长边一定用不上，可以几何优化，但这里没做'],
        summary=['时间 `O(n² log n)`：瓶颈是给 `n²/2` 条边排序',
                 '并查集 `find` 带路径压缩，合并时让编号小的根当父亲',
                 '稠密图也可以用 `O(n²)` 的 Prim，不用显式建边',
                 '原文为 Python 2 写法，`fa = range(n)` 已改为 `fa = list(range(n))`（Python 3 的 range 不能赋值）'],
    ),
)
