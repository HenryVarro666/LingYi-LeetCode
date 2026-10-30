import math as _m


def _gdraw(cv, box, T, pos, edges, state, sub=None, hot=None, title='', R=30, fs=26):
    """有向图：pos={名字:(fx,fy)}，edges=[(a,b)]，state={名字:颜色名或None}，sub={名字:下方小字}，hot=高亮边 (a,b)"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    half = {k: max(R, (cv.tlen(k, fs, bold=True) + 30) / 2) for k in pos}
    mx = max(half.values())
    w, h = x1 - x0 - 2 * mx - 40, y1 - y0 - 2 * R - 100
    P = {k: (x0 + 20 + mx + fx * w, y0 + 50 + R + fy * h) for k, (fx, fy) in pos.items()}

    def edge_pt(k, ux, uy, pad):
        a, b = half[k] + pad, R + pad
        t = 1 / _m.sqrt((ux / a) ** 2 + (uy / b) ** 2)
        return t

    for a, b in edges:
        if a not in P or b not in P:
            continue
        (ax, ay), (bx, by) = P[a], P[b]
        d = _m.hypot(bx - ax, by - ay) or 1
        ux, uy = (bx - ax) / d, (by - ay) / d
        ta, tb = edge_pt(a, ux, uy, 3), edge_pt(b, ux, uy, 6)
        on = hot is not None and (a, b) == tuple(hot)
        cv.arrow((ax + ux * ta, ay + uy * ta), (bx - ux * tb, by - uy * tb),
                 T['yellow'] if on else T['dim'], width=6 if on else 3, head=16 if on else 13)
    for k, (cx, cy) in P.items():
        c = state.get(k)
        fill = T[c] if c else T['panel2']
        cv.rect((cx - half[k], cy - R, cx + half[k], cy + R), fill=fill, outline=T['border'], width=3, r=R)
        cv.text((cx, cy), k, fs, T['bg'] if c else T['text'], anchor='mm', bold=True)
        if sub and sub.get(k) not in (None, ''):
            cv.text((cx, cy + R + 6), sub[k], 22, T['muted'], anchor='mt', bold=True)


def _mk(CODE):
    lines = CODE.strip('\n').split('\n')
    return lambda s: next(i + 1 for i, l in enumerate(lines) if s in l)

CODE = '''
class Solution:
    def closestMeetingNode(self, edges: List[int], x: int, y: int) -> int:
        ans = n = len(edges)
        vis_x = [False] * n
        vis_y = [False] * n

        while not vis_x[x] or not vis_y[y]:  # x 或 y 没有访问过
            vis_x[x] = vis_y[y] = True  # 标记访问过

            if vis_y[x]:  # 我吹过你吹过的晚风
                ans = x
            if vis_x[y]:
                ans = min(ans, y)  # 如果有多个答案，返回最小的节点编号
            if ans < n:
                return ans

            if edges[x] >= 0:
                x = edges[x]  # 继续走
            if edges[y] >= 0:
                y = edges[y]  # 继续走

        return -1
'''
LN = _mk(CODE)
EDGE_LIST = [1, 2, 3, 4, -1, 3]
NM = [str(i) for i in range(6)]
POS = {'0': (0, .1), '1': (.25, .1), '2': (.5, .1), '3': (.75, .1), '4': (1, .1), '5': (.75, .95)}
EDGES = [(NM[i], NM[e]) for i, e in enumerate(EDGE_LIST) if e >= 0]


def _draw(cv, S, B, box, T):
    vx, vy = S.get('vis_x'), S.get('vis_y')
    st, sub = {}, {}
    x, y = S.get('x'), S.get('y')
    if vx is not None and vy is not None:
        for i in range(6):
            if vx[i] and vy[i]:
                st[NM[i]] = 'purple'
            elif vx[i]:
                st[NM[i]] = 'blue'
            elif vy[i]:
                st[NM[i]] = 'pink'
        ans = S.get('ans')
        if ans is not None and ans < 6:
            st[NM[ans]] = 'green'
    if x is not None and y is not None and 'ans' in S:
        for i in range(6):
            tag = ('x' if i == x else '') + (' ' if i == x == y else '') + ('y' if i == y else '')
            if tag:
                sub[NM[i]] = tag
    _gdraw(cv, box, T, POS, EDGES, st, sub, None, '蓝 x 走过 · 粉 y 走过 · 紫 两人都走过 · 绿 答案', R=34)


CONFIG = dict(
    num=2359, title='找到离给定两个节点最近的节点', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='两人同时走 · 我吹过你吹过的晚风',
    tags=['难度分 1715'],
    code=CODE,
    call='Solution().closestMeetingNode([1,2,3,4,-1,3], 0, 5)',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='array', var='vis_x', label='vis_x（x 走过的点）', pointers={'x': 'blue'}, cell=64, h=150,
             color=lambda S, i, v: 'blue' if v else None),
        dict(type='array', var='vis_y', label='vis_y（y 走过的点）', pointers={'y': 'pink'}, cell=64, h=150,
             color=lambda S, i, v: 'pink' if v else None),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('ans', 'ans', 'green')],
    skip=['vis_x = [False]', 'vis_y = [False]'],
    captions={
        'ans = n': '`ans = n = {n}`：`n` 比任何节点编号都大，表示「还没找到」',
        'while not vis_x': lambda S, B, r: (f'`x = {S.x}`、`y = {S.y}` 至少一个还有新路可走，继续' if (not S.vis_x[S.x] or not S.vis_y[S.y])
                                            else '两人都只能走已经走过的路，不会再有新答案 → 结束'),
        'vis_x[x] = vis_y[y]': '`x` 站在 `{x}`，`y` 站在 `{y}`：各自留下脚印',
        'if vis_y[x]': lambda S, B, r: (f'`vis_y[{S.x}]` 为真：`y` 以前来过 `{S.x}` → `x` 踩到了 `y` 的脚印' if S.vis_y[S.x]
                                        else f'`vis_y[{S.x}]` 为假：`y` 没来过 `{S.x}`'),
        'ans = x': '`{x}` 是两人都到过的点，先记下 `ans = {ans}`',
        'if vis_x[y]': lambda S, B, r: (f'`vis_x[{S.y}]` 为真：`x` 以前来过 `{S.y}` → `y` 踩到了 `x` 的脚印' if S.vis_x[S.y]
                                        else f'`vis_x[{S.y}]` 为假：`x` 没来过 `{S.y}`'),
        'ans = min': '两人同时撞上时取编号小的：`ans = min({B.ans}, {y}) = {ans}`',
        'if ans < n': lambda S, B, r: (f'`ans = {S.ans}` < `n`：找到了，先踩到的人走得最少，直接返回' if S.ans < S.n
                                       else '`ans = n`：还没有交汇点，继续走'),
        'if edges[x] >= 0': lambda S, B, r: (f'`edges[{S.x}] = {S.edges[S.x]}`：`x` 有路可走' if S.edges[S.x] >= 0
                                             else f'`edges[{S.x}] = -1`：`x` 是死路，留在原地'),
        'x = edges[x]': '`x` 沿着边走到 `{x}`',
        'if edges[y] >= 0': lambda S, B, r: (f'`edges[{S.y}] = {S.edges[S.y]}`：`y` 有路可走' if S.edges[S.y] >= 0
                                             else f'`edges[{S.y}] = -1`：`y` 是死路，留在原地'),
        'y = edges[y]': '`y` 沿着边走到 `{y}`',
        'return ans': '答案 =={ret}==：两人最先在这里相遇',
        'return -1': '两人都只剩走过的路，没有共同可达点 → `-1`',
    },
    cards=dict(
        one_liner='两个人同时出发，谁先踩到对方的脚印，那里就是答案',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`edges[i]` 是节点 `i` 的唯一出边（`-1` 表示没有），图可能有环',
                 '求从 `node1`、`node2` 都能到的节点，使两者距离的较大值最小；并列取编号小的',
                 '示例：`edges=[1,2,3,4,-1,3]`，`node1=0`，`node2=5` → `3`'],
        quote='如果某个时刻，x 到达 y 走过的路，即 vis_y[x] 为 true，那么当前 x 所在节点，就是两人都可以到达的节点，且距离最近。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把两个节点当成两个人，每次各走一步，并用 `vis_x`、`vis_y` 留脚印',
              '一人踩到另一人的脚印，说明这里两人都能到，且是最先到的',
              '同一时刻两人互相踩到，取编号较小的；两人都走不动就返回 `-1`'],
        summary=['时间 `O(n)`，空间 `O(n)`：每轮至少标记一个新点',
                 '先 `x` 后 `y` 判断，同时命中时用 `min` 取小编号',
                 '死路时 `x`、`y` 原地不动，循环条件靠脚印终止',
                 '灵神另给了方法一：各跑一遍最短路 `dis1`、`dis2`，再枚举取 `max` 最小的点',
                 '思考题：多个起点 / 多次询问可以用基环树上的倍增或 LCA 来做'],
    ),
)
