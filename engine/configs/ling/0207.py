POS = {0: (0.10, 0.48), 1: (0.36, 0.13), 2: (0.62, 0.48), 3: (0.36, 0.86), 4: (0.70, 0.86)}
FILL = {0: None, 1: 'yellow', 2: 'green'}


def draw_graph(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g = S.get('g')
    if not g:
        return
    colors = S.get('colors') or [0] * len(g)
    W, H, R = (x1 - x0) * 0.55, (y1 - y0) - 60, 28

    def P(u):
        fx, fy = POS[u]
        return x0 + 60 + fx * W, y0 + 30 + fy * H

    cur = None
    if isinstance(S.get('x'), int) and isinstance(S.get('y'), int) and S['y'] in g[S['x']]:
        cur = (S['x'], S['y'])
    for u, vs in enumerate(g):
        for v in vs:
            (ax, ay), (bx, by) = P(u), P(v)
            dx, dy = bx - ax, by - ay
            L = max(1.0, (dx * dx + dy * dy) ** 0.5)
            ux, uy = dx / L, dy / L
            hot = cur == (u, v)
            c = T['yellow'] if hot else T['muted']
            if hot and colors[v] == 1:
                c = T['red']
            if u in g[v]:  # 双向边：各自往一侧偏移
                ox, oy = -uy * 9, ux * 9
            else:
                ox = oy = 0
            cv.arrow((ax + ux * R + ox, ay + uy * R + oy), (bx - ux * (R + 4) + ox, by - uy * (R + 4) + oy),
                     c, 5 if hot else 3, 14)
    for u in range(len(g)):
        X, Y = P(u)
        f = FILL.get(colors[u])
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=T[f] if f else T['panel2'],
                     outline=T['text'] if u == S.get('x') else T['border'], width=4 if u == S.get('x') else 2)
        cv.text((X, Y), u, 28, T['bg'] if f else T['text'], anchor='mm', bold=True)
    lx = x0 + 60 + W + 50
    for k, (name, f) in enumerate([('0 未访问', None), ('1 访问中（在递归栈里）', 'yellow'), ('2 访问完毕（无环）', 'green')]):
        yy = y0 + 40 + k * 46
        cv.d.ellipse((lx, yy, lx + 26, yy + 26), fill=T[f] if f else T['panel2'], outline=T['border'])
        cv.text((lx + 38, yy + 13), name, 21, T['muted'], anchor='lm')
    cv.text((lx, y0 + 40 + 3 * 46 + 6), '白圈 = 当前 x；黄边 = 正在看的边', 19, T['dim'], anchor='la')


def _edge(S, B, ret):
    if 'a' in B and (B.a, B.b) == (S.a, S.b):
        return '建图完成'
    pre = '建图，`g[b]` 存“学完 b 才能学的课”。' if 'a' not in B else ''
    return pre + f'`[{S.a}, {S.b}]`：学 {S.a} 前要先学 {S.b} → 有向边 `{S.b} → {S.a}`'


def _for(S, B, ret):
    if 'y' not in S or not S.g[S.x]:
        return f'`g[{S.x}]` 为空：{S.x} 没有后继课程'
    if 'y' not in B or B.y != S.y:
        return f'看 {S.x} 的邻居 `y = {S.y}`'
    return f'{S.x} 的邻居都看完了'


def _check(S, B, ret):
    y, c = B.y, B.colors[B.y]
    if c == 1:
        return f'`colors[{y}] == 1`：{y} 还在递归栈里（正在访问中）→ ==循环依赖，找到环！=='
    if c == 0:
        return f'`colors[{y}] == 0`：没访问过 {y} → 递归 `dfs({y})` 获取信息'
    return f'`colors[{y}] == 2`：{y} 已完全访问，==重复访问只会重蹈覆辙==，跳过（这不是环）'


def _main(S, B, ret):
    if 'i' in B and B.i == S.i:
        return '所有节点都检查完'
    return f'主循环：节点 `{S.i}`，颜色 `{S.c}`'


CONFIG = dict(
    num=207, title='课程表', difficulty='Medium', category='图论',
    author='灵茶山艾府', technique='DFS 三色标记法（判环）',
    code='''
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        g = [[] for _ in range(numCourses)]
        for a, b in prerequisites:
            g[b].append(a)

        colors = [0] * numCourses
        # 返回 True 表示找到了环
        def dfs(x: int) -> bool:
            colors[x] = 1  # x 正在访问中
            for y in g[x]:
                # 情况一：colors[y] == 1，表示发生循环依赖，找到了环
                # 情况二：colors[y] == 0，没有访问过 y，继续递归 y 获取信息
                # 情况三：colors[y] == 2，重复访问 y 只会重蹈覆辙，和之前一样无法找到环，跳过
                if colors[y] == 1 or colors[y] == 0 and dfs(y):
                    return True  # 找到了环
            colors[x] = 2  # x 完全访问完毕，从 x 出发无法找到环
            return False  # 没有找到环

        for i, c in enumerate(colors):
            if c == 0 and dfs(i):
                return False  # 有环
        return True  # 没有环
''',
    call='Solution().canFinish(5, [[1, 0], [2, 1], [2, 0], [3, 0], [4, 3], [3, 4]])',
    expect=False,
    views=[
        dict(type='custom', draw=draw_graph, h=300),
        dict(type='map', var=lambda S: dict(enumerate(S['g'])), label='g（邻接表：g[b] 里是 b 指向的课）',
             fmt=lambda k, v: f'{k} → {v}', h=130),
        dict(type='array', var='colors', label='colors（0 未访问 / 1 访问中 / 2 访问完毕）',
             color=lambda S, i, v: FILL.get(v), cell=76,
             pointers={'x': 'yellow'}),
    ],
    watch=[('x', 'x', 'yellow'), 'y', 'colors'],
    skip=['g = [[] for _ in range'],
    captions={
        'for a, b in prerequisites': _edge,
        'g[b].append(a)': '`g[{b}]` 加入 `{a}`',
        'colors = [0]': '`colors` 全部为 0：所有课程==尚未访问==',
        'colors[x] = 1': '`colors[{x}] = 1`：{x} ==正在访问中==，`dfs({x})` 尚未结束',
        'for y in g[x]': _for,
        'if colors[y] == 1 or': _check,
        'return True  # 找到了环': '`dfs({x})` 返回 `True`：找到了环，一路向上传递',
        'colors[x] = 2': '`colors[{x}] = 2`：{x} ==完全访问完毕==，从 {x} 出发无法找到环',
        'return False  # 没有找到环': '`dfs({x})` 返回 `False`：没有找到环',
        'for i, c in enumerate': _main,
        'if c == 0 and dfs(i)': lambda S, B, ret: (f'节点 {B.i} 未访问 → 从它开始 `dfs({B.i})`' if B.c == 0
                                                   else f'节点 {B.i} 已访问过，跳过'),
        'return False  # 有环': '`dfs` 找到了环 → 循环依赖，==不可能学完所有课程==，返回 `False`',
        'return True  # 没有环': '所有节点都没有找到环 → 返回 `True`',
    },
    max_steps=70,
    cards=dict(
        one_liner='课程依赖是有向图，能学完 ⇔ 图中没有环',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['`[a, b]` 表示学 `a` 之前必须先学 `b`，判断能否学完所有课程',
                 '题意：给你一个有向图（边 `b → a`），==判断图中是否有环==',
                 '本视频示例：5 门课，边 `0→1→2`、`0→2`、`0→3`、`3⇄4` → ==False=='],
        quote='如果在递归过程中，发现下一个节点在递归栈中（正在访问中），则找到了环。',
        quote_src='—— 灵茶山艾府题解',
        idea=['三种颜色：`0` 未访问，`1` 正在访问（`dfs(x)` 尚未结束），`2` 访问完毕',
              '==误区==：只用“访问过/没访问过”两种状态不行，例如 `0→1→2` 之后再走 `0→2`，2 访问过但不是环',
              '颜色 `2` 还说明从它出发找不到环，再遇到直接跳过'],
        summary=['时间 `O(n+m)`：每个节点至多递归一次，每条边至多遍历一次',
                 '==颜色 1 的节点恰好就是当前递归栈==，指向它的边就是“回边”，即环',
                 '`colors[x] = 2` 要在遍历完所有邻居之后再标记',
                 '注意 `dfs` 返回 True 表示==有环==，主函数要取反',
                 '相似题：802. 找到最终的安全状态'],
    ),
)
