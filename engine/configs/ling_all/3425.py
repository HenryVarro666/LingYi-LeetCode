# ---- 通用的一般树画法：按 parents 数组布局，节点带颜色/外圈/下标注
def _gt_layout(parents):
    n = len(parents)
    ch = [[] for _ in range(n)]
    for i in range(1, n):
        ch[parents[i]].append(i)
    depth, xs, cnt = [0] * n, [0.0] * n, [0]

    def go(u, d):
        depth[u] = d
        if not ch[u]:
            xs[u] = cnt[0]
            cnt[0] += 1
        else:
            for v in ch[u]:
                go(v, d + 1)
            xs[u] = (xs[ch[u][0]] + xs[ch[u][-1]]) / 2
    go(0, 0)
    return ch, depth, xs, max(cnt[0], 1), max(depth) + 1


def gtree_draw(cv, box, T, parents, label, fill=None, ring=None, under=None, edge=None, edge_label=None, title=''):
    x0, y0, x1, y1 = box
    n = len(parents)
    ch, depth, xs, nleaf, nd = _gt_layout(parents)
    if title:
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    sp = min(130, (x1 - x0 - 80) / max(1, nleaf))
    dy = min(120, (y1 - y0 - 125) / max(1, nd - 1))
    rad = max(18, min(30, sp * 0.36, dy * 0.3))
    sx = x0 + (x1 - x0 - sp * (nleaf - 1)) / 2
    P = {u: (sx + xs[u] * sp, y0 + 80 + depth[u] * dy) for u in range(n)}
    for u in range(1, n):
        a, b = P[parents[u]], P[u]
        ec = edge(u) if edge else None
        cv.line([a, b], T[ec] if ec else T['border'], 6 if ec else 3)
        if edge_label:
            s = edge_label(u)
            if s is not None:
                mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
                w = cv.tlen(str(s), 18, bold=True) + 10
                cv.rect((mx - w / 2, my - 12, mx + w / 2, my + 12), fill=T['bg'], r=6)
                cv.text((mx, my), str(s), 18, T['muted'], anchor='mm', bold=True)
    for u in range(n):
        X, Y = P[u]
        f = fill(u) if fill else None
        rc = ring(u) if ring else None
        if rc:
            cv.rect((X - rad - 6, Y - rad - 6, X + rad + 6, Y + rad + 6), outline=T[rc], width=5, r=rad + 6)
        cv.rect((X - rad, Y - rad, X + rad, Y + rad), fill=T[f] if f else T['panel2'], outline=T['border'], r=rad)
        cv.text((X, Y), str(label(u)), 26, T['bg'] if f else T['text'], anchor='mm', bold=True)
        cv.text((X + rad + 6, Y - rad * 0.4), f'#{u}', 15, T['dim'], anchor='lm', mono=True)
        if under:
            s = under(u)
            if s:
                cv.text((X, Y + rad + 8), s, 19, T['green'], anchor='mt', bold=True)
    return P
EDGES = [[0, 1, 2], [1, 2, 3], [1, 3, 5], [1, 4, 4], [2, 5, 6]]
NUMS = [2, 1, 2, 1, 3, 1]
PARENTS = [-1, 0, 1, 1, 1, 2]
WT = {2: 3, 1: 2, 3: 5, 4: 4, 5: 6}   # 子节点 -> 到父亲的边长


def _path(x):
    p = []
    while x != -1:
        p.append(x)
        x = PARENTS[x]
    return p[::-1]   # 根 -> x


def _win(S):
    x = S['_inner'].get('x')
    if x is None:
        return None, [], set()
    p = _path(x)
    td = S['_inner'].get('top_depth', 0)
    return x, p, set(p[td:])


def _draw(cv, S, B, box, T):
    x, p, w = _win(S)

    def fill(i):
        if i in w:
            return 'green'
        return 'orange' if i in p else None
    gtree_draw(cv, box, T, PARENTS, lambda i: NUMS[i], fill, lambda i: 'blue' if i == x else None, None,
               edge=lambda u: 'green' if (u in w and PARENTS[u] in w) else None, edge_label=lambda u: WT[u],
               title='树（圈内 = 颜色值 nums[i]，边上 = 长度；绿 = 当前窗口，橙 = 窗口上方的祖先，蓝环 = x）')


def _fm(S):
    x, p, w = _win(S)
    if x is None:
        return f"当前最优 `ans = {S.get('ans')}`（长度, −节点数）"
    td = S['_inner'].get('top_depth', 0)
    d = S['dis']
    return (f"窗口 = 深度 `{td}` ~ `{len(p) - 1}`：长度 `dis[-1] - dis[{td}] = {d[-1]} - {d[td]} = {d[-1] - d[td]}`，"
            f"节点 `{len(p) - td}` 个；`ans = {S.get('ans')}`")


CONFIG = dict(
    num=3425, title='最长特殊路径', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='树上滑动窗口 · lastDepth',
    tags=['链表树与回溯', '难度分 2435'],
    code='''
class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        g = [[] for _ in nums]
        for x, y, w in edges:
            g[x].append((y, w))
            g[y].append((x, w))

        ans = (-1, 0)
        dis = [0]
        last_depth = {}  # 颜色 -> 该颜色最近一次出现的深度 +1，注意这里已经 +1 了

        def dfs(x: int, fa: int, top_depth: int) -> None:
            color = nums[x]
            old_depth = last_depth.get(color, 0)
            top_depth = max(top_depth, old_depth)

            nonlocal ans
            # 把 len(dis) - top_depth 取反，这样 max 算的是最小值
            ans = max(ans, (dis[-1] - dis[top_depth], top_depth - len(dis)))

            last_depth[color] = len(dis)
            for y, w in g[x]:
                if y != fa:  # 避免访问父节点
                    dis.append(dis[-1] + w)
                    dfs(y, x, top_depth)
                    dis.pop()  # 恢复现场
            last_depth[color] = old_depth  # 恢复现场

        dfs(0, -1, 0)
        return [ans[0], -ans[1]]
''',
    call='Solution().longestSpecialPath([[0,1,2],[1,2,3],[1,3,5],[1,4,4],[2,5,6]], [2,1,2,1,3,1])',
    expect=[6, 2],
    views=[
        dict(type='custom', draw=_draw, h=380),
        dict(type='text', fn=_fm, size=24, h=55),
        dict(type='array', var='dis', label='dis（根到路径上各节点的距离）', cell=60, h=125),
        dict(type='map', var='last_depth', label='last_depth（颜色 → 最近出现的深度 + 1）', h=120),
    ],
    watch=[('x', lambda S: S['_inner'].get('x'), 'blue'), ('top_depth', lambda S: S['_inner'].get('top_depth'), 'green'),
           ('ans', 'ans', 'yellow')],
    captions={
        'g = [[]': '建邻接表：`g[x]` 存相邻节点和边长',
        'ans = (-1, 0)': '`ans = (长度, −节点数)`：节点数取反，这样 `max` 同时做到==长度最大、节点数最少==',
        'dis = [0]': '`dis` 是栈：根到路径上每个节点的距离，根是 `0`',
        'last_depth = {}': '`last_depth` 记录每种颜色最近一次出现的深度（已 +1）',
        'color = nums[x]': '到达节点 `x = {x}`，颜色 `{color}`',
        'old_depth =': '颜色 `{color}` 上次出现的深度 + 1 = `{old_depth}`（`0` 表示路径上没出现过）',
        'top_depth = max': '窗口顶端 `max({B.top_depth}, {old_depth})` → =={top_depth}==：重复颜色必须被挤出窗口',
        'ans = max': '窗口长度 `{dis[-1]} - {dis[top_depth]} = {dis[-1] - dis[top_depth]}`，节点数 `{len(dis) - top_depth}` → `ans = {ans}`',
        'last_depth[color] = len': '记下颜色 `{color}` 现在出现在深度 `{len(dis) - 1}`（存 `{len(dis)}`）',
        'if y != fa': '`y = {y}`：{"是父节点，跳过，避免走回头路" if y == fa else "是子节点，往下走"}',
        'dis.append': '往下走边长 `{w}`：`dis` 末尾加入 `{dis[-1]}`',
        'dfs(y, x': '递归进入 `{y}`，把当前 `top_depth = {top_depth}` 传下去',
                'last_depth[color] = old_depth': '离开节点 `{x}`：`dis` 弹出末尾，颜色 `{color}` 恢复成 `{old_depth}`，==恢复现场==，不影响兄弟子树',
        'dfs(0, -1, 0)': '从根 `0` 出发，窗口顶端在深度 `0`',
        'return [ans': '最长 `{ans[0]}`，节点数 `{-ans[1]}` → 返回 `{ret}`',
    },
    skip=['for y, w in g[x]', 'dis.pop()', 'for x, y, w in edges', 'g[x].append', 'g[y].append', 'nonlocal ans'],
    max_steps=100,
    cards=dict(
        one_liner='枚举路径最下面的节点，维护最上面的深度：树上的滑动窗口',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树，根 `0`，边有长度，节点有值（颜色）',
                 '特殊路径：自上而下、节点值互不相同',
                 '求最长特殊路径的长度，及最长路径中的最少节点数',
                 '示例答案 `[6,2]`：`2→5` 和 `0→1→4` 长度都是 6'],
        quote='在树上滑窗，我们可以枚举路径最下面的节点（类似子数组右端点），同时维护路径最上面的节点（类似子数组左端点）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['链 = 数组，就是「无重复字符的最长子串」',
              '`last_depth[颜色]` 记录颜色最近出现的深度，窗口顶端取最大值',
              '`dis` 栈存根到各节点的距离，窗口长度 = 栈顶 − `dis[top_depth]`'],
        result='返回 `[6, 2]`',
        summary=['时间 `O(n)`：每个节点访问一次；空间 `O(n)`',
                 '易错：`last_depth` 存的是深度 +1；离开节点要恢复现场',
                 '`ans` 用元组且节点数取反，一次 `max` 同时比较长度和节点数',
                 '只维护深度而不是节点，避免了「扫帚形」树上的 `O(n^2)`'],
    ),
)
