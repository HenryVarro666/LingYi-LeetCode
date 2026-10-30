N = 4
DISLIKES = [[1, 2], [1, 3], [2, 4]]
POS = {0: (0.15, 0.15), 1: (0.85, 0.15), 2: (0.15, 0.85), 3: (0.85, 0.85)}
FILL = {0: None, 1: 'red', -1: 'blue'}
_X = lambda S: S['_inner'].get('x')


def _cur_edge(S):
    x, y = S['_inner'].get('x'), S['_inner'].get('y')
    if 'graph' in S and isinstance(x, int) and isinstance(y, int) and y in S['graph'][x]:
        return (x, y)
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g = S.get('graph') or S.get('g')
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
        on = u == S['_inner'].get('x')
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
    cv.text((lx, y0 + 50 + 3 * 50 + 68), '节点编号 = 人的编号 − 1', 20, T['dim'])


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
    num=886, title='可能的二分法', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='建图 + 判断二分图（交替染色）',
    tags=['labuladong', '灵神题单·图论算法', '难度分 1795'],
    code='''
class Solution:
    # 785. 判断二分图
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
        
    def possibleBipartition(self, n: int, dislikes: List[List[int]]) -> bool:
        # 构建图
        g = [[] for _ in range(n)]
        for x, y in dislikes:
            x -= 1  # 节点编号改成从 0 开始
            y -= 1
            g[x].append(y)
            g[y].append(x)
        return self.isBipartite(g)
''',
    call=f'Solution().possibleBipartition({N}, {DISLIKES})',
    expect=True,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='colors', label='colors（1 红 / -1 蓝 / 0 未访问）', cell=80, h=150,
             color=lambda S, i, v: FILL.get(v), pointers={_X: 'yellow'}, pointer_labels={_X: 'x'}),
        dict(type='calls', h=170, hide=('graph', 'dislikes')),
    ],
    watch=[('x', _X, 'yellow'), ('y', lambda S: S['_inner'].get('y')), 'c', 'g'],
    captions={
        'g = [[] for _ in range(n)]': '把讨厌关系看成==无向边==：先建 `n = {n}` 个空邻接表',
        'for x, y in dislikes': lambda S, B, r: (f'取讨厌关系 `[{S.x}, {S.y}]`：{S.x} 和 {S.y} 之间连一条边' if 'x' not in B or (B.x, B.y) != (S.x, S.y)
                                                 else '所有讨厌关系都连好边了'),
        'x -= 1': '节点编号改成从 0 开始：`x` → {x}，`y` → {y - 1}',
        'g[x].append(y)': '`g[{x}]` 加入 {y}',
        'g[y].append(x)': '`g[{y}]` 加入 {x}：无向图要==两个方向都加==',
        'return self.isBipartite(g)': lambda S, B, r: ('建图完成 → 每条边两端必须分到不同组 = ==判断二分图==（785 题）' if r is None
                                                       else f'`isBipartite` 返回 `{r}` → 可以分成两组'),
        'colors = [0] * len': '`colors` 全是 0：所有人==都还没分组==',
        'colors[x] = c': lambda S, B, r: f'`colors[{S.x}] = {S.c}`：把 {S.x} 染成==' + ('红色' if S.c == 1 else '蓝色') + '==（分到' + ('第一组' if S.c == 1 else '第二组') + '）',
        'for y in graph[x]': lambda S, B, r: (f'看 {S.x} 讨厌的人 `y = {S.y}`' if 'y' in S and ('y' not in B or B.y != S.y or B.x != S.x)
                                             else f'{S.x} 的邻居都检查完了'),
        'if colors[y] == c or': _if,
        '            return True': '`dfs({x}, {c})`：{x} 的邻居都没有冲突 → 返回 `True`',
        'if c == 0 and not dfs(i, 1)': _main,
        24: '每个连通块都能交替染色 → ==是二分图==，返回 `True`',
    },
    skip=['# 取相反数', 'y -= 1', 'for i, c in enumerate'],
    max_steps=70,
    cards=dict(
        one_liner='讨厌关系连边，能分成两组 ⇔ 这张图是二分图',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['`n` 个人分成两组（大小任意），`[a, b]` 表示 a、b ==不能在同一组==',
                 '能分成功返回 `true`，否则 `false`',
                 '示例：`n = 4, dislikes = [[1,2],[1,3],[2,4]]` → `true`（`[1,4]` 和 `[2,3]`）'],
        quote='我们需要把这些点分成两组，每组内部不能有边（否则违背要求）。换句话说，==每条边的两个端点，一定来自不同组==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['在 `a_i` 和 `b_i` 之间连一条边，得到一个无向图',
              '“每条边两端不同组”正是二分图的定义 → ==和 785 题完全一样==',
              '直接复用 785 的交替染色：`1` 红、`-1` 蓝，递归传 `-c`'],
        summary=['时间 `O(n+m)`，`m` 是 `dislikes` 的长度；空间 `O(n+m)` 存图',
                 '易错：人的编号从 1 开始，建图前要==先减 1==',
                 '无向图建边要 `g[x]` 和 `g[y]` ==两边都加==',
                 '图可能不连通，主循环对每个未染色的点都要发起一次 dfs',
                 '同类：785. 判断二分图、1129. 颜色交替的最短路径'],
    ),
)
