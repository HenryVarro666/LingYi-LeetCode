GRAPH = [[1, 3], [0, 2], [1, 3], [0, 2]]
POS = {0: (0.15, 0.15), 1: (0.85, 0.15), 2: (0.85, 0.85), 3: (0.15, 0.85)}
FILL = {0: None, 1: 'red', -1: 'blue'}


def _cur_edge(S):
    x, y = S.get('x'), S.get('y')
    if isinstance(x, int) and isinstance(y, int) and y in S['graph'][x]:
        return (x, y)
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g = S.get('graph')
    if not g:
        return
    colors = S.get('colors') or [0] * len(g)
    side = min(x1 - x0 - 420, y1 - y0 - 70)
    R = 34

    def P(u):
        fx, fy = POS[u]
        return x0 + 70 + fx * side, y0 + 35 + fy * side

    cur = _cur_edge(S)
    for u, vs in enumerate(g):
        for v in vs:
            if u > v:
                continue
            hot = cur is not None and set(cur) == {u, v}
            c = T['muted']
            if hot:
                c = T['red'] if colors[u] == colors[v] != 0 else T['yellow']
            cv.line([P(u), P(v)], c, 7 if hot else 3)
    for u in range(len(g)):
        X, Y = P(u)
        f = FILL.get(colors[u])
        on = u == S.get('x')
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=T[f] if f else T['panel2'],
                     outline=T['yellow'] if on else T['border'], width=6 if on else 2)
        cv.text((X, Y), u, 30, T['bg'] if f else T['text'], anchor='mm', bold=True)
    lx = x0 + 70 + side + 110
    items = [('0 未访问', None), ('1 红色', 'red'), ('-1 蓝色', 'blue')]
    for k, (name, f) in enumerate(items):
        yy = y0 + 50 + k * 50
        cv.d.ellipse((lx, yy, lx + 28, yy + 28), fill=T[f] if f else T['panel2'], outline=T['border'])
        cv.text((lx + 42, yy + 14), name, 22, T['muted'], anchor='lm')
    cv.text((lx, y0 + 50 + 3 * 50 + 4), '黄圈 = 当前节点 x', 20, T['dim'])
    cv.text((lx, y0 + 50 + 3 * 50 + 36), '黄边 = 正在看的边 x–y', 20, T['dim'])


def _if(S, B, ret):
    x, y, c = B.x, B.y, B.c
    cy = B.colors[y]
    if cy == c:
        return f'`colors[{y}] == c = {c}`：邻居和 {x} ==同色== → 不是二分图'
    if cy == 0:
        return f'`colors[{y}] == 0`：{y} 未访问 → 递归 `dfs({y}, {-c})`，==取相反数==交替染色'
    return f'`colors[{y}] = {cy}` 与 `c = {c}` 相反，这条边没问题，看下一个邻居'


def _main(S, B, ret):
    if B.colors[S.i] == 0:
        return f'节点 {S.i} 还没染色 → 新连通块，从它开始 `dfs({S.i}, 1)`'
    return f'节点 {S.i} 已染色（颜色 `{S.colors[S.i]}`），属于已处理的连通块，跳过'


CONFIG = dict(
    num=785, title='判断二分图', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='DFS 交替染色',
    tags=['labuladong', '灵神题单·图论算法', '难度分 1625'],
    code='''
class Solution:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        # colors[i] = 0  表示未访问节点 i
        # colors[i] = 1  表示节点 i 为红色
        # colors[i] = -1 表示节点 i 为蓝色
        colors = [0] * len(graph)

        def dfs(x: int, c: int) -> bool:
            colors[x] = c  # 节点 x 染成颜色 c
            for y in graph[x]:
                # 邻居 y 的颜色与 x 的相同，说明不是二分图，返回 False
                # 或者继续递归，发现不是二分图，返回 False
                if colors[y] == c or \\
                   colors[y] == 0 and not dfs(y, -c):  # 取相反数，实现交替染色
                    return False
            return True

        # 可能有多个连通块
        for i, c in enumerate(colors):
            if c == 0 and not dfs(i, 1):
                # 从节点 i 开始递归，发现 i 所在连通块不是二分图
                return False
        return True
''',
    call=f'Solution().isBipartite({GRAPH})',
    expect=True,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='colors', label='colors（1 红 / -1 蓝 / 0 未访问）', cell=80, h=150,
             color=lambda S, i, v: FILL.get(v), pointers={'x': 'yellow'}),
        dict(type='calls', h=170),
    ],
    watch=[('x', 'x', 'yellow'), 'y', 'c'],
    captions={
        'colors = [0] * len': '`colors` 全是 0：所有节点==都未访问==',
        'colors[x] = c': lambda S, B, r: f'`colors[{S.x}] = {S.c}`：把 {S.x} 染成==' + ('红色' if S.c == 1 else '蓝色') + '==',
        'for y in graph[x]': lambda S, B, r: (f'看 {S.x} 的邻居 `y = {S.y}`' if 'y' in S and ('y' not in B or B.y != S.y or B.x != S.x)
                                             else f'{S.x} 的邻居都检查完了'),
        'if colors[y] == c or': _if,
        'return False\n': '发现冲突，返回 `False`',
        '            return True': '`dfs({x}, {c})`：{x} 的邻居都没有冲突 → 返回 `True`',
        'if c == 0 and not dfs(i, 1)': _main,
        '        return True': '每个连通块都能交替染色 → ==是二分图==，返回 `True`',
    },
    skip=[14, 19],
    max_steps=60,
    cards=dict(
        one_liner='相邻节点颜色必须不同：从未染色的点出发，红蓝交替染下去',
        complexity='时间 `O(n+m)`，空间 `O(n)`',
        problem=['无向图用邻接表 `graph` 给出，`graph[u]` 是 u 的邻居',
                 '能否把节点分成 A、B 两组，==每条边的两端分属不同组==？',
                 '示例：`[[1,3],[0,2],[1,3],[0,2]]` → `true`（`{0,2}` 和 `{1,3}`）'],
        quote='邻居 y 的颜色与 x 的相同，说明不是二分图，返回 False；或者继续递归，发现不是二分图，返回 False。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['二分图 ⇔ 能用两种颜色染色，使==每条边两端颜色不同==',
              '颜色用 `1` / `-1` 表示，递归时传 `-c`，==取相反数就是换色==',
              '邻居同色 → 冲突；邻居未染色 → 递归染成相反色'],
        summary=['时间 `O(n+m)`：染过色的节点不会再递归，每个节点只访问一次',
                 '图可能不连通：主循环要从==每个未染色的节点==各发起一次 dfs',
                 '`or` / `and` 的短路：邻居已是相反色时什么都不做',
                 '用 `0` 表示未访问，所以颜色选 `1` 和 `-1` 而不是 `0` 和 `1`',
                 '同类题：886. 可能的二分法（建图后直接调用本题）'],
    ),
)
