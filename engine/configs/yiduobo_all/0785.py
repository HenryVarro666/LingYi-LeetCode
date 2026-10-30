GRAPH = [[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]
POS = {0: (0.15, 0.15), 1: (0.85, 0.15), 2: (0.85, 0.85), 3: (0.15, 0.85)}
FILL = {None: None, 0: 'green', 1: 'purple'}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g = S.get('graph')
    if not g:
        return
    color = S.get('color') or [None] * len(g)
    side = min(x1 - x0 - 420, y1 - y0 - 70)
    R = 34

    def P(u):
        fx, fy = POS[u]
        return x0 + 70 + fx * side, y0 + 35 + fy * side

    now, nxt = S.get('now'), S['_inner'].get('next')
    cur = (now, nxt) if isinstance(now, int) and isinstance(nxt, int) and nxt in g[now] else None
    for u, vs in enumerate(g):
        for v in vs:
            if u > v:
                continue
            hot = cur is not None and set(cur) == {u, v}
            c = T['muted']
            if hot:
                c = T['red'] if color[u] is not None and color[u] == color[v] else T['yellow']
            cv.line([P(u), P(v)], c, 7 if hot else 3)
    for u in range(len(g)):
        X, Y = P(u)
        f = FILL.get(color[u])
        on = u == now
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=T[f] if f else T['panel2'],
                     outline=T['yellow'] if on else T['border'], width=6 if on else 2)
        cv.text((X, Y), u, 30, T['bg'] if f else T['text'], anchor='mm', bold=True)
    lx = x0 + 70 + side + 110
    items = [('None 无色', None), ('0 左半部', 'green'), ('1 右半部', 'purple')]
    for k, (name, f) in enumerate(items):
        yy = y0 + 50 + k * 50
        cv.d.ellipse((lx, yy, lx + 28, yy + 28), fill=T[f] if f else T['panel2'], outline=T['border'])
        cv.text((lx + 42, yy + 14), name, 22, T['muted'], anchor='lm')
    cv.text((lx, y0 + 50 + 3 * 50 + 4), '黄圈 = 当前点 now', 20, T['dim'])
    cv.text((lx, y0 + 50 + 3 * 50 + 36), '黄边 = now–next，红边 = 同色冲突', 20, T['dim'])


def _same(S, B, ret):
    a, b = B.now, B.next
    ca, cb = B.color[a], B.color[b]
    if ca == cb:
        return f'`color[{b}] == color[{a}] == {ca}`：==相邻两点同色== → 不是二分图'
    if cb is None:
        return f'`{b}` 还无色，不冲突'
    return f'`color[{b}] = {cb}` 与 `color[{a}] = {ca}` 相反 → 跳过 {b}'


CONFIG = dict(
    num=785, title='判断二分图', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='01 染色 · DFS',
    tags=['labuladong', '灵神题单·图论算法', '难度分 1625'],
    code='''
class Solution(object):
    def isBipartite(self, graph):

        n = len(graph)
        color = [None] * n
        for x in range(n):
            if color[x] is None:
                if not self.dfs(x, color, 0, graph):
                    return False

        return True

    def dfs(self, now, color, c, graph):
        color[now] = c
        for next in graph[now]:
            if color[next] == color[now]:
                return False
            if color[next] is None:
                if not self.dfs(next, color, 1 - c, graph):
                    return False
        return True
''',
    call=f'Solution().isBipartite({GRAPH})',
    expect=False,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var=lambda S: ['-' if v is None else v for v in S['color']] if 'color' in S else None,
             label='color（None 无色 / 0 / 1）', cell=80, h=150,
             color=lambda S, i, v: FILL.get(S['color'][i]), pointers={'now': 'yellow'}),
        dict(type='calls', h=170, hide=('color', 'graph')),
    ],
    watch=[('now', 'now', 'yellow'), ('next', lambda S: S['_inner'].get('next')), 'c'],
    captions={
        'n = len(graph)': '{n} 个点，准备对每个点做 01 染色',
        'color = [None] * n': '`color` 全为 `None`：所有点==还没染色==',
        'if color[x] is None': lambda S, B, r: (f'点 {S.x} 无色 → 染成 0，从它开始 dfs' if B.color[S.x] is None
                                                else f'点 {S.x} 已经染过色，跳过'),
        'if not self.dfs(x, color, 0, graph)': '调用 `dfs({x}, color, 0)`',
        'color[now] = c': '`color[{now}] = {c}`：把 {now} 染成 =={c}==',
        'for next in graph[now]': lambda S, B, r: (f'看 {S.now} 的相邻点 `next = {S.next}`'
                                                   if 'next' in S and ('next' not in B or B.next != S.next or B.now != S.now)
                                                   else f'{S.now} 的相邻点都检查完了'),
        'if color[next] == color[now]': _same,
        'return False\n': '出现同色相邻点 → 返回 `False`',
        'if color[next] is None': lambda S, B, r: (f'`{B.next}` 无色 → 染成反色 `1 - {B.c} = {1 - B.c}`，从它继续 dfs'
                                                   if B.color[B.next] is None else f'`{B.next}` 已染色，不用递归'),
        'if not self.dfs(next, color, 1 - c, graph)': '递归 `dfs({B.next}, color, {1 - B.c})`',
        20: lambda S, B, r: '下层返回 `False`，继续向上传递 `False`',
        21: '`dfs({now})`：所有相邻点都不冲突 → 返回 `True`',
        9: '`dfs` 返回 `False` → 这张图==不是二分图==',
    },
    max_steps=60,
    cards=dict(
        one_liner='01 染色：二分图左边全染 0、右边全染 1，相邻点一定异色',
        complexity='时间 `O(n+m)`，空间 `O(n)`',
        problem=['无向图用邻接表 `graph` 给出，`graph[u]` 是 u 的相邻点',
                 '能否把点分成两个集合，使==每条边的两端分属不同集合==？',
                 '示例：`[[1,2,3],[0,2],[0,1,3],[0,2]]` → `false`'],
        quote='将二分图左边的部分全部置为0，将右边的部分全部置为1，那么可以发现，==任意相邻的两点颜色都不一样==。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历每个点，若还没被染色，就染成 0 并从它开始 dfs',
              '相邻点 next 三种情况：==同色 → 不是二分图==；异色 → 跳过；',
              '无色 → 染成 `1 - c`，从 next 继续 dfs'],
        summary=['时间 `O(n+m)`：每个点只染一次色，每条边看两次',
                 '用 `None` 表示无色，颜色用 `0 / 1`，反色就是 `1 - c`',
                 '图可能不连通，外层要对==每个无色的点==都发起 dfs',
                 '本例 0、1、2 两两相邻构成三角形（奇环）→ 必然冲突',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
