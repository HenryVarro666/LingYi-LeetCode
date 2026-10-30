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
EDGES = [[0, 1, 1], [1, 2, 3], [1, 3, 1], [2, 4, 6], [3, 5, 2], [3, 6, 5]]
NUMS = [1, 1, 0, 3, 1, 2, 1]
PARENTS = [-1, 0, 1, 1, 2, 3, 3]
WT = {1: 1, 2: 3, 3: 1, 4: 6, 5: 2, 6: 5}


def _path(x):
    p = []
    while x != -1:
        p.append(x)
        x = PARENTS[x]
    return p[::-1]


def _win(S):
    x = S['_inner'].get('x')
    if x is None:
        return None, [], 0
    return x, _path(x), S['_inner'].get('top_depth', 0)


def _draw(cv, S, B, box, T):
    x, p, st = _win(S)
    cols = [NUMS[i] for i in p[st:]]
    w = set(p[st:])

    def fill(i):
        if i in w:
            return 'yellow' if cols.count(NUMS[i]) >= 2 else 'green'
        return 'orange' if i in p else None
    gtree_draw(cv, box, T, PARENTS, lambda i: NUMS[i], fill, lambda i: 'blue' if i == x else None, None,
               edge=lambda u: 'green' if (u in w and PARENTS[u] in w) else None, edge_label=lambda u: WT[u],
               title='树（圈内 = 颜色；绿 = 窗口，黄 = 窗口里出现两次的颜色，橙 = 被挤出，蓝环 = x）')


def _fm(S):
    x, p, st = _win(S)
    if x is None:
        return f"当前最优 `ans = {S.get('ans')}`（长度, −节点数）"
    d = S['dis']
    return (f"窗口 = 深度 `{st}` ~ `{len(p) - 1}`：长度 `{d[-1]} - {d[st]} = {d[-1] - d[st]}`，节点 `{len(p) - st}` 个；"
            f"`ans = {S.get('ans')}`")


CONFIG = dict(
    num=3486, title='最长特殊路径 II', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='树上滑动窗口 · 多维护一个 last1',
    tags=['链表树与回溯', '难度分 2925'],
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

        def dfs(x: int, fa: int, top_depth: int, last1: int) -> None:
            color = nums[x]
            last2 = last_depth.get(color, 0)
            top_depth = max(top_depth, min(last1, last2))  # 相较 3425 题，维护窗口左端点的逻辑变了

            nonlocal ans
            ans = max(ans, (dis[-1] - dis[top_depth], top_depth - len(dis)))

            last_depth[color] = len(dis)
            for y, w in g[x]:
                if y != fa:
                    dis.append(dis[-1] + w)
                    dfs(y, x, top_depth, max(last1, last2))  # 相较 3425 题，额外维护 last1
                    dis.pop()
            last_depth[color] = last2

        dfs(0, -1, 0, 0)
        return [ans[0], -ans[1]]
''',
    call='Solution().longestSpecialPath([[0,1,1],[1,2,3],[1,3,1],[2,4,6],[3,5,2],[3,6,5]], [1,1,0,3,1,2,1])',
    expect=[9, 3],
    views=[
        dict(type='custom', draw=_draw, h=380),
        dict(type='text', fn=_fm, size=24, h=55),
        dict(type='array', var='dis', label='dis（根到路径上各节点的距离）', cell=60, h=125),
        dict(type='map', var='last_depth', label='last_depth（颜色 → 最近出现的深度 + 1）', h=120),
    ],
    watch=[('x', lambda S: S['_inner'].get('x'), 'blue'), ('top_depth', lambda S: S['_inner'].get('top_depth'), 'green'),
           ('last1', lambda S: S['_inner'].get('last1'), 'pink'), ('ans', 'ans', 'yellow')],
    captions={
        'ans = (-1, 0)': '`ans = (长度, −节点数)`：取反后一次 `max` 就能「长度最大、节点数最少」',
        'dis = [0]': '`dis` 栈：根到路径上每个节点的距离',
        'last2 = ': '到达节点 `x = {x}`，颜色 `{color}` 上次出现在 `last2 = {last2}`；窗口里已有一个重复颜色，它的上一次位置是 `last1 = {last1}`',
        'top_depth = max': '窗口顶端 `max({B.top_depth}, min({last1}, {last2}))` → =={top_depth}==：允许一个颜色重复，所以取两个「上一次位置」里较靠上的那个',
        'ans = max': '窗口长度 `{dis[-1]} - {dis[top_depth]} = {dis[-1] - dis[top_depth]}`，节点数 `{len(dis) - top_depth}` → `ans = {ans}`',
        'if y != fa': '`y = {y}`：{"是父节点，跳过" if y == fa else "是子节点，往下走"}',
        'dis.append': '往下走边长 `{w}`：`dis` 末尾加入 `{dis[-1]}`',
        'dfs(y, x': '递归进入 `{y}`：传下 `top_depth = {top_depth}`，`last1 = max({last1}, {last2}) = {max(last1, last2)}`（更靠下的那个重复位置）',
        'last_depth[color] = last2': '离开 `{x}`：`dis` 弹出，颜色 `{color}` 还原为 `{last2}`，==恢复现场==',
        'dfs(0, -1': '从根出发：`top_depth = 0`，`last1 = 0`（还没有重复颜色）',
        'return [ans': '最长 `{ans[0]}`，最少节点 `{-ans[1]}` → 返回 `{ret}`',
    },
    skip=['color = nums[x]', 'last_depth[color] = len', 'for y, w in g[x]', 'dis.pop()', 'for x, y, w in edges', 'g[x].append', 'g[y].append', 'nonlocal ans'],
    max_steps=100,
    cards=dict(
        one_liner='在 3425 的窗口上多开一个名额：允许一个颜色出现两次',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树，根 `0`，边有长度，节点有颜色值',
                 '特殊路径：自上而下，==最多一个值出现两次==，其余值唯一',
                 '求最长长度，及最长时的最少节点数',
                 '示例：`[9, 3]`（`1→2→4`）'],
        quote='本题允许窗口中的一个元素（颜色）出现两次，我们记录这个颜色在窗口中的更靠上的深度 last1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['新节点的颜色上一次出现在 `last2`；窗口里已有的重复颜色在 `last1`',
              '窗口顶端至少是 `min(last1, last2) + 1`，用 `max` 更新（`last2` 可能在窗口外）',
              '`last2` 更靠下时，它成为新的 `last1` 往下传'],
        result='返回 `[9, 3]`',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`top_depth` 是更新最大值而不是直接替换；传给孩子的是 `max(last1, last2)`',
                 '只比 3425 题多一个参数 `last1`，其余（`dis` 栈、`last_depth`、元组 `ans`）完全一样',
                 '回溯时 `last_depth[color]` 要还原，`dis` 要弹栈'],
    ),
)
