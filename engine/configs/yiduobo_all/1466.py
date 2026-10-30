# ---------- 一般树自绘（custom 视图）：按孩子列表布局，状态由当前步变量推出 ----------
def _tree_pos(CH, root, box, top=46, bottom=34):
    x0, y0, x1, y1 = box
    depth, pos, cnt = {}, {}, [0]

    def go(u, d):
        depth[u] = d
        ks = CH.get(u, [])
        if not ks:
            pos[u] = cnt[0]
            cnt[0] += 1
        else:
            for k in ks:
                go(k, d + 1)
            pos[u] = sum(pos[k] for k in ks) / len(ks)
    go(root, 0)
    nl, md = max(1, cnt[0]), max(depth.values()) + 1
    sp = min(110, (x1 - x0 - 60) / nl)
    dy = min(100, (y1 - y0 - top - bottom) / max(1, md))
    rad = max(16, min(26, sp * 0.36, dy * 0.3))
    sx = x0 + 30 + ((x1 - x0 - 60) - sp * (nl - 1)) / 2
    return {u: (sx + pos[u] * sp, y0 + top + depth[u] * dy + rad) for u in depth}, rad


def _gtree(cv, T, box, CH, root, cur, hl=(), done=(), badge=None, sub=None, title=None, anc=()):
    P, rad = _tree_pos(CH, root, box)
    if title:
        cv.text((box[0] + 18, box[1] + 4), title, 22, T['muted'], bold=True)
    for u, ks in CH.items():
        for k in ks:
            on = k in anc or k == cur
            cv.line([P[u], P[k]], T['yellow'] if on and u in anc or (on and u == cur) else T['border'], 5 if on else 3)
    for u, (X, Y) in P.items():
        fill, outl, w, tc = T['panel2'], T['border'], 2, T['text']
        if u in done:
            fill, tc = T['green'], T['bg']
        if u in hl:
            fill, tc = T['cyan'], T['bg']
        if u in anc:
            outl, w = T['yellow'], 4
        if u == cur:
            outl, w = T['blue'], 5
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=outl, width=w)
        cv.text((X, Y), u, int(rad * 0.95), tc, anchor='mm', bold=True)
        if sub and u in sub:
            cv.text((X + rad + 6, Y - 4), sub[u], 20, T['yellow'], anchor='lm', bold=True, mono=True)
        if badge and u in badge:
            s = badge[u]
            bw = cv.tlen(s, 19, bold=True) + 14
            cv.rect((X - bw / 2, Y + rad + 4, X + bw / 2, Y + rad + 28), fill=T['panel'], outline=T['green'], width=2, r=8)
            cv.text((X, Y + rad + 16), s, 19, T['green'], anchor='mm', bold=True)


def _anc(PAR, u):
    out = []
    while u is not None and PAR.get(u) is not None:
        u = PAR[u]
        out.append(u)
    return out


def _preorder(CH, root):
    out = []

    def go(u):
        out.append(u)
        for k in CH[u]:
            go(k)
    go(root)
    return out


def _subtree(CH, u):
    out = [u]
    for k in CH[u]:
        out += _subtree(CH, k)
    return out

CONN = [[0, 1], [1, 3], [2, 3], [4, 0], [4, 5]]
N = 6
CH = {0: [1, 4], 1: [3], 3: [2], 4: [5], 2: [], 5: []}
PARENT = {1: 0, 4: 0, 3: 1, 2: 3, 5: 4}


def _draw(cv, S, B, box, T):
    used = S.get('used') or [False] * N
    now, nxt = S.get('now'), S.get('next')
    P, rad = _tree_pos(CH, 0, box)
    cv.text((box[0] + 18, box[1] + 4), '城市与单向边（箭头 = 原方向；红 = 需要反向，绿 = 方向已对）', 22, T['muted'], bold=True)
    for x, y in CONN:
        a, b = P[x], P[y]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / L, dy / L
        p0 = (a[0] + ux * (rad + 3), a[1] + uy * (rad + 3))
        p1 = (b[0] - ux * (rad + 5), b[1] - uy * (rad + 5))
        child = y if PARENT.get(y) == x else x
        away = PARENT.get(y) == x          # 原方向背离 0 号城市 → 需要反向
        found = used[child]
        if (now, nxt) in ((x, y), (y, x)) and nxt is not None and not used[nxt] or (found and {now, nxt} == {x, y}):
            col, w = T['yellow'], 6
        elif found:
            col, w = (T['red'], 5) if away else (T['green'], 5)
        else:
            col, w = T['border'], 3
        cv.arrow(p0, p1, col, w, 14)
        if found and away:
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            cv.text((mx + 14, my), '+1', 22, T['red'], anchor='lm', bold=True)
    for u, (X, Y) in P.items():
        fill, outl, w, tc = T['panel2'], T['border'], 2, T['text']
        if used[u]:
            fill, tc = T['green'], T['bg']
        if u == nxt and S.get('_line', 0) >= 0 and not used[u]:
            outl, w = T['pink'], 5
        if u == now:
            outl, w = T['blue'], 5
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=outl, width=w)
        cv.text((X, Y), u, int(rad * 0.95), tc, anchor='mm', bold=True)


CODE = '''
class Solution(object):
    def minReorder(self, n, connections):

        g = {}
        for x, y in connections:
            if x not in g:
                g[x] = {}
            if y not in g:
                g[y] = {}
            g[x][y] = 1
            g[y][x] = 0
        
        q = [0]
        l = 0
        r = 1
        used = [False] * n
        used[0] = True
        res = 0
        while l < r:
            now = q[l]
            l += 1
            for next in g[now]:
                if not used[next]:
                    res += g[now][next]
                    q.append(next)
                    used[next] = True
                    r += 1
        
        return res
'''

CONFIG = dict(
    num=1466, title='重新规划路线', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='无向建图 + 从 0 号 BFS，数背离 0 的边',
    tags=['链表树与回溯'],
    code=CODE,
    call='Solution().minReorder(6, [[0,1],[1,3],[2,3],[4,0],[4,5]])',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=370),
        dict(type='array', var='q', label='队列 q（l = 队头，r = 队尾后一位）', cell=64, h=150, pointers={'l': 'blue', 'r': 'pink'}),
        dict(type='array', var='used', label='used[i]：i 号城市是否已访问', cell=64, h=120),
    ],
    watch=[('now', 'now', 'blue'), ('next', 'next', 'pink'), ('l', 'l', 'cyan'), ('r', 'r', 'yellow'), ('res', 'res', 'green')],
    captions={
        'g = {}': '`g[x][y]` 记录无向边的原始方向：==1 = 原图里有 x→y，0 = 只是反方向==',
        'g[x][y] = 1': '原图的边 `{x}→{y}`：正向记 `g[{x}][{y}] = 1`',
        'g[y][x] = 0': '反过来 `{y}→{x}` 只是为了能走通，记 `0`',
        'q = [0]': '题目要求所有城市都能到达 0 号：从 `0` 出发做 BFS',
        'used = [False]': '`used` 防止走回头路（树里每个点只被发现一次）',
        'used[0] = True': '`0` 号城市标记为已访问',
        'res = 0': '`res` 统计需要反向的边数',
        'while l < r': lambda S, B, r: ('队列非空，继续' if S['l'] < S['r'] else '队列空了，所有城市都访问过'),
        'now = q[l]': '取出队头 `now = {now}`',
        'for next in g[now]': lambda S, B, r: (f"枚举与 `{S['now']}` 相连的城市 `{S['next']}`" if S['next'] != B.get('next') or B.get('now') != S['now'] else f"`{S['now']}` 的邻居都看完了"),
        'if not used[next]': lambda S, B, r: (f"`{S['next']}` 还没访问过 → 是从 `{S['now']}` 走出去的新城市" if not S['used'][S['next']] else f"`{S['next']}` 已经访问过（是来时的路） → 跳过"),
        'res += g[now][next]': lambda S, B, r: (f"原图有 `{S['now']}→{S['next']}`，方向背离 0 → ==必须反向==，`res += 1` → {S['res']}" if S['g'][S['now']][S['next']] == 1 else f"原图是 `{S['next']}→{S['now']}`，已经指向 0 的方向 → 不用改，`res += 0`"),
        'q.append(next)': '`{next}` 入队，之后再从它继续往外走',
        'used[next] = True': '标记 `{next}` 已访问',
        'return res': '一共要反向 `{res}` 条边',
    },
    skip=['if x not in g', 'g[x] = {}', 'if y not in g', 'g[y] = {}', 'l = 0', 'r = 1', 'l += 1', 'r += 1'],
    max_steps=100,
    cards=dict(
        one_liner='把有向边当无向边，从 0 号 BFS：沿原方向走出去的边都要反向',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 个城市，`n-1` 条单向道路，构成一棵树',
                 '要让每个城市都能走到 0 号城市，求最少需要改变方向的道路数',
                 '示例：`n = 6`，`connections = [[0,1],[1,3],[2,3],[4,0],[4,5]]` → `3`'],
        quote='由于题目保证了地图是一棵树，那么如果先不考虑图中边的方向，是一定可以从0号城市出发访问到图中其他城市的，于是可以从0号城市开始进行bfs，只需将bfs过程中的正向边反过来就能保证可以从各个城市都可以访问到0号城市了。',
        quote_src='—— yiduobo 题解原文',
        idea=['重新建图：单向边变无向边，但 `g[x][y]` 记住原方向（1 = 原边，0 = 反向边）',
              '从 `0` 向外 BFS：走到 `next` 时，若是原边 `now→next`，方向背离 0，==必须反向==',
              '若走的是反向边（原图是 `next→now`），已经指向 0 方向，不用改'],
        result='BFS 结束，`res = 3`',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '树里恰有 `n-1` 条边，每条边只会在 BFS 发现新点时被统计一次',
                 '易错：只统计「原方向背离 0」的边，别把所有边都数上',
                 '原文已是 Python 3 可运行的写法（变量 `next` 遮住内置函数，但没有用到），未改动'],
    ),
)
