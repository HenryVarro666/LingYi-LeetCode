# 示例 3：edges=[[2,4],[0,1],[2,3],[0,2]] -> [4,6,3,5,5]
POS_ = {0: (0.5, 0.10), 1: (0.22, 0.50), 2: (0.78, 0.50), 3: (0.62, 0.90), 4: (0.94, 0.90)}
EDGE_ = [(0, 1), (0, 2), (2, 3), (2, 4)]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    W, H = x1 - x0 - 150, y1 - y0 - 130
    P = {k: (x0 + 75 + v[0] * W, y0 + 65 + v[1] * H) for k, v in POS_.items()}
    inn = S.get('_inner', {})
    cx, cy = inn.get('x'), inn.get('y')
    cv.text((x0 + 18, y0 + 4), '蓝 = 奇数点（进入它要 1），紫 = 偶数点（进入它要 2）；黄框 x，粉框 y', 22, T['muted'], bold=True)
    for a, b in EDGE_:
        hot = (cx, cy) in ((a, b), (b, a))
        cv.line([P[a], P[b]], T['yellow'] if hot else T['border'], 6 if hot else 3)
    sr, ans = S.get('sub_res'), S.get('ans')
    for k, (px, py) in P.items():
        cv.rect((px - 26, py - 26, px + 26, py + 26), fill=T['blue'] if k % 2 else T['purple'], r=26)
        if k == cx:
            cv.rect((px - 34, py - 34, px + 34, py + 34), outline=T['yellow'], width=5, r=34)
        if k == cy:
            cv.rect((px - 34, py - 34, px + 34, py + 34), outline=T['pink'], width=5, r=34)
        cv.text((px, py), k, 30, T['bg'], anchor='mm', bold=True)
        lines = []
        if sr is not None and sr[k] is not None:
            lines.append((f'下 {sr[k][0]}/{sr[k][1]}', T['cyan']))
        if ans is not None and ans[k] != 0:
            lines.append((f'ans={ans[k]}', T['orange']))
        left = k in (1,)
        for i, (s, c) in enumerate(lines):
            cv.text((px - 40 if left else px + 40, py - 14 + i * 28), s, 23, c, anchor='rm' if left else 'lm', bold=True, mono=True)


def c_w(S, B, ret):
    x, y = S['_inner']['x'], S['_inner']['y']
    return f'进入 `{y}` 的边权：{y} 是{"奇" if y % 2 else "偶"}数 → `2 - {y} % 2` = =={S.w}=='


def c_my(S, B, ret):
    x, y = S['_inner']['x'], S['_inner']['y']
    return f'从 `{x}` 经 `{y}` 往下最深 `{S.sub_res[y][0]} + {S.w}` = =={S.max_y}==（`{y}` 的子树深度 + 边权）'


def c_cmp(S, B, ret):
    x, y = S['_inner']['x'], S['_inner']['y']
    return f'`max_y = {S.max_y}` 和当前最大 `{B.max_d}` 比 → ' + ('==更大==' if S.max_y > B.max_d else '不更大')


def c_cmp2(S, B, ret):
    return f'没超过最大 `{S.max_d}`，再和次大 `{S.max_d2}` 比：`{S.max_y} > {S.max_d2}` → ' + ('==更大==，次大要更新' if S.max_y > S.max_d2 else '不更大，丢掉')


def c_big(S, B, ret):
    return f'新的最大 `max_d = {S.max_d}`，原来的最大退居次大 `max_d2 = {S.max_d2}`，最大值走的儿子 `my = {S.my}`'


def c_second(S, B, ret):
    return f'没超过最大，但超过次大 → `max_d2 = {S.max_d2}`（换根时要「绕开最大那个儿子」就靠它）'


def c_ansx(S, B, ret):
    x = S['_inner']['x']
    return f'`ans[{x}] = max(向下最深 {S.max_d}, 向上 {S.from_up})` = =={S.ans[x]}=='


def c_mx(S, B, ret):
    x, y = S['_inner']['x'], S['_inner']['y']
    if y != S.my:
        return f'`{y}` 不是最深的那个儿子 → 站在 `{x}`，不往 `{y}` 走，最远还是 `max_d` = =={S.mx}=='
    return f'`{y}` 正是最深的儿子 → 绕开它，只能用==次大== `max_d2` = =={S.mx}=='


def c_rr(S, B, ret):
    x, y = S['_inner']['x'], S['_inner']['y']
    return (f'传给 `{y}` 的 `from_up = max({S.from_up}, {S.mx}) + {S.w}` = =={max(S.from_up, S.mx) + S.w}=='
            f'（从 {y} 走到 {x} 的边权是 `2 - {x} % 2`）')


CONFIG = dict(
    num=3241, title='标记所有节点需要的时间', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='换根 DP · 最大/次大',
    tags=['灵神题单', '动态规划', '难度分 2522'],
    code='''
# 手写 max 更快
max = lambda a, b: b if b > a else a

class Solution:
    def timeTaken(self, edges: List[List[int]]) -> List[int]:
        n = len(edges) + 1
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        # sub_res[x] 保存子树 x 的最大深度，次大深度，以及最大深度要往哪个儿子走
        sub_res = [None] * n
        # 计算 sub_res[x]
        def dfs(x: int, fa: int) -> None:
            max_d = max_d2 = my = 0
            for y in g[x]:
                if y == fa:
                    continue
                dfs(y, x)
                w = 2 - y % 2  # 从 x 到 y 的边权
                max_y = sub_res[y][0] + w  # 从 x 出发，往 y 方向的最大深度
                if max_y > max_d:
                    max_d2 = max_d
                    max_d = max_y
                    my = y
                elif max_y > max_d2:
                    max_d2 = max_y
            sub_res[x] = (max_d, max_d2, my)
        dfs(0, -1)

        # ans[x] 表示当 x 是树根时，整棵树的最大深度
        ans = [0] * n
        # 计算 ans[x]
        def reroot(x: int, fa: int, from_up: int) -> None:
            max_d, max_d2, my = sub_res[x]
            ans[x] = max(max_d, from_up)
            for y in g[x]:
                if y == fa:
                    continue
                # 站在 x 的角度，不往 y 走，能走多远？
                # 要么往上走（from_up），要么往除了 y 的其余子树走（mx），二者取最大值
                mx = max_d if y != my else max_d2
                w = 2 - x % 2  # 从 y 到 x 的边权
                reroot(y, x, max(from_up, mx) + w)  # 对于 y 来说，加上从 y 到 x 的边权
        reroot(0, -1, 0)
        return ans
''',
    call='Solution().timeTaken([[2,4],[0,1],[2,3],[0,2]])',
    expect=[4, 6, 3, 5, 5],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='calls', h=150),
    ],
    watch=['x', 'y', 'w', 'max_y', 'max_d', 'max_d2', 'my', 'from_up', 'mx'],
    skip=['g = [[]', 'g[x].append', 'g[y].append', 'for x, y in edges', 'max = lambda', 'n = len(edges)', 'if y == fa', 'continue', 'for y in g[x]', 'max_d2 = max_d', 'max_d = max_y', 'max_d, max_d2, my = sub_res[x]', 'sub_res = [None]', 'ans = [0]'],
    captions={
        'w = 2 - y': c_w,
        'max_y = sub_res': c_my,
        23: c_cmp,
        27: c_cmp2,
        'max_d = max_d2 = my = 0': '先假设还没看任何儿子：最深、次深都是 `0`，`my` 暂无',
        'dfs(y, x)': '先递归算出儿子 `{y}` 的子树信息，再回来合并',
        'w = 2 - x': '从 `{y}` 走到 `{x}` 的边权看终点 `{x}`：`w = 2 - {x} % 2` = =={w}==；下一步传给 `{y}` 的 `from_up = max({from_up}, {mx}) + {w}` = =={max(from_up, mx) + w}==',
        'my = y': c_big,
        'max_d2 = max_y': c_second,
        'sub_res[x] = (': lambda S, B, r: f'子树 `{S["_inner"]["x"]}` 记下三样：最深 `{S.max_d}`、次深 `{S.max_d2}`、最深往 `{S.my}` 走',
        'dfs(0, -1)': '第一次 DFS：以 0 为根，每个点记「向下的最深/次深」',
        'reroot(0, -1, 0)': '第二次 DFS：换根，`from_up` 是「先向上走再拐弯」能走的最远距离，根的 `from_up = 0`',
        'ans[x] = max': c_ansx,
        'mx = max_d if': c_mx,
        'reroot(y, x, max': c_rr,

        'return ans': '每个点作为起点的最晚标记时间都算好了',
    },
    cards=dict(
        one_liner='标记时间 = 以起点为根的树高（边权看终点奇偶），换根时靠次大值绕开自己',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树，在 0 时刻标记点 `i`，奇数点晚 1 个时刻、偶数点晚 2 个时刻被相邻点传染',
                 '对每个起点，求标记完整棵树的时刻',
                 '示例：`edges=[[2,4],[0,1],[2,3],[0,2]]` → `[4,6,3,5,5]`'],
        quote='本题相当于对每个节点，计算以该节点为根时，树的高度（最大深度）。其中从 x→y 的有向边的边权为 2 − y mod 2。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先转成：边权 `x→y` 取决于终点 `y`，奇 1 偶 2，答案 = 以起点为根的最大深度',
              '第一次 DFS 记每个点向下的最大深度、次大深度，以及最大深度走哪个儿子 `my`',
              '换根：`from_up` 往下传；若 `y` 恰是最深儿子，就改用次大值，不能走回自己'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`x→y` 与 `y→x` 边权不同（看终点奇偶），向上传 `from_up` 时用 `2 - x % 2`',
                 '这是「第二类换根 DP」：除了最大值还要维护==次大值==',
                 '相似题：CF1822F Gardening Friends'],
    ),
)
