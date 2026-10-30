import math


def _ln(code, sub):
    """1-based line number of the first code line containing sub (leading blank line stripped)"""
    for k, s in enumerate(code.strip('\n').split('\n')):
        if sub in s:
            return k + 1
    return -1


def _gdraw(cv, box, T, pos, E, node_fn, edge_fn, label_fn=None, title='', directed=True, R=30, base=0, node_w=None):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    w = x1 - x0 - 140
    h = y1 - y0 - 150
    P = [(x0 + 70 + fx * w, y0 + 60 + fy * h) for fx, fy in pos]
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
                cv.text((x, y + R + 8), lab[0], 21, lab[1], anchor='mt', bold=True)


EDGES = [3, 3, 4, 2, 3, 6, 5, 8, -1]
POS = [(0.0, 0.1), (0.0, 0.85), (0.5, 0.1), (0.25, 0.48), (0.5, 0.85), (0.78, 0.1), (1.0, 0.1), (0.78, 0.85), (1.0, 0.85)]
CODE = '''
class Solution:
    def longestCycle(self, edges: List[int]) -> int:
        n = len(edges)
        ans = -1
        cur_time = 1  # 当前时间
        vis_time = [0] * n  # 首次访问 x 的时间
        for x in range(n):
            start_time = cur_time  # 本轮循环的开始时间
            while x != -1 and vis_time[x] == 0:  # 没有访问过 x
                vis_time[x] = cur_time  # 记录访问 x 的时间
                cur_time += 1
                x = edges[x]  # 访问下一个节点
            if x != -1 and vis_time[x] >= start_time:  # x 在本轮循环中访问了两次，说明 x 在环上
                ans = max(ans, cur_time - vis_time[x])  # 前后两次访问 x 的时间差，即为环长
        return ans  # 如果没有找到环，返回的是 ans 的初始值 -1
'''
L_ANS = _ln(CODE, 'ans = max')


def _draw(cv, S, B, box, T):
    vt = S.get('vis_time')
    st = S.get('start_time')
    x = S.get('x')
    cyc = set()
    if vt and S.get('_line') == L_ANS and x is not None and x != -1:
        cyc = {i for i, t in enumerate(vt) if t and vis_lo(vt, x) <= t < S['cur_time']}

    def node(i):
        if i in cyc:
            return T['green'], T['bg'], None
        ring = T['yellow'] if (x == i and S.get('_line') != L_ANS) else None
        t = vt[i] if vt else 0
        if t == 0:
            return T['panel2'], T['muted'], ring
        if st is not None and t >= st:
            return T['blue'], T['bg'], ring
        return (70, 76, 86), T['text'], ring

    def edge(a, b):
        if vt and vt[a] and vt[b] and a in cyc and b in cyc:
            return T['green'], 5
        if vt and vt[a] and st is not None and vt[a] >= st:
            return T['blue'], 4
        return T['dim'], 3

    def lab(i):
        if vt and vt[i]:
            return (f't={vt[i]}', T['cyan'] if (cyc and i in cyc) else T['muted'])
        return None
    E = [(i, e) for i, e in enumerate(EDGES) if e != -1]
    _gdraw(cv, box, T, POS, E, node, edge, lab, '黄圈 = 当前点，蓝 = 本轮，灰 = 前几轮，绿 = 环，t = 访问时间')


def vis_lo(vt, x):
    return vt[x]


CONFIG = dict(
    num=2360, title='图中的最长环', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='时间戳 · 内向基环树',
    tags=['灵神题单·图论算法', '难度分 1897'],
    code=CODE,
    call=f'Solution().longestCycle({EDGES})',
    expect=3,
    skip=['n = len(edges)', 'cur_time += 1'],
    max_steps=80,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='array', var='edges', label='edges（下标 = 起点，值 = 终点，-1 = 没有出边）', h=130, cell=70,
             pointers={'x': 'yellow'}, index=True),
        dict(type='array', var='vis_time', label='vis_time（0 = 没访问过）', h=130, cell=70),
    ],
    watch=[('x', 'x', 'yellow'), ('start_time', 'start_time', 'blue'), ('cur_time', 'cur_time', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = -1': '先假设没有环：`ans = -1`',
        'cur_time = 1': '计时器从 1 开始，每访问一个新点就加一',
        'vis_time = [0]': '`vis_time[x]` 记录 x 的首次访问时间，0 表示还没访问',
        'for x in range': lambda S, B, r: ('所有点都作为起点试过了' if S.x == len(S.edges) - 1 and S.x == B.get('x') else f'从点 `{S.x}` 出发开始新的一轮'),
        'start_time = cur_time': '`start_time = {start_time}`：记下本轮的开始时间，用来区分“本轮访问”和“以前访问”',
        'while x != -1': lambda S, B, r: (f'点 `{S.x}` 没访问过 → 继续走' if S.x != -1 and S.vis_time[S.x] == 0
                                          else ('走到死路（-1），停下' if S.x == -1
                                                else f'点 `{S.x}` 已经访问过（时间 {S.vis_time[S.x]}）→ 停下')),
        'vis_time[x] = cur_time': '访问点 `{x}`，记录时间 `vis_time[{x}] = {cur_time}`，计时器随后加一',
        'x = edges[x]': '顺着出边走到下一个点：`x = {x}`',
        'if x != -1 and vis_time[x] >= start_time': lambda S, B, r: (
            '走到了死路，本轮没有环' if S.x == -1 else
            (f'`vis_time[{S.x}] = {S.vis_time[S.x]} >= start_time = {S.start_time}`：点 {S.x} ==本轮访问了两次==，它一定在环上'
             if S.vis_time[S.x] >= S.start_time else
             f'`vis_time[{S.x}] = {S.vis_time[S.x]} < start_time = {S.start_time}`：撞上以前的路径，这个连通块的环早就算过了')),
        'ans = max': '环长 = 两次访问的时间差：`{B.cur_time} - {vis_time[x]} = {cur_time - vis_time[x]}`，`ans` → =={ans}==',
        'return ans': '没有环时 `ans` 仍是初始值 -1；这里答案是 =={ret}==',
    },
    cards=dict(
        one_liner='跑操场计时：第二次回到同一点，时间差就是环长',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['有向图 `n` 个点，每个点==至多一条出边==，`edges[i]` 是 i 的终点（-1 表示没有）',
                 '返回图中==最长的环==的长度，没有环返回 `-1`',
                 '示例：`[3,3,4,2,3]` → `3`（环 `3→2→4→3`）。本视频的图多加了几个点，答案同样是 3'],
        quote='如果每访问一个节点，计时器就加一，那么 t2 - t1 就是跑道长度，即环长。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每个点首次访问时记下时间 `vis_time[x]`，计时器全局递增',
              '从 i 出发一路走，==走到本轮自己访问过的点==，说明绕了一圈：环长 = 时间差',
              '走到以前轮次访问过的点：环要么已经算过，要么根本没有'],
        summary=['时间 `O(n)`：二重循环，但每个点只记录一次访问时间',
                 '用 `vis_time[x] >= start_time` 区分“本轮”和“旧轮”，不用另开 visited',
                 '题目保证每个连通块至多一个环，时间差才等于环长；一般图的最长环是 NP-hard',
                 '同类题：2876 有向图访问计数、2608 图中的最短环（题单 §2.3 基环树）'],
    ),
)
