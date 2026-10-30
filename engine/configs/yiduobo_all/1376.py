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

MANAGER = [2, 2, -1, 2, 2, 4, 4]
INFORM = [0, 0, 3, 0, 2, 0, 0]
HEAD = 2
N = len(MANAGER)
CH = {i: [] for i in range(N)}
for _i, _m in enumerate(MANAGER):
    if _m >= 0:
        CH[_m].append(_i)


def _draw(cv, S, B, box, T):
    q = S.get('q') or []
    f = S.get('f') or [0] * N
    l = S.get('l', 0)
    now = S.get('now') if 'l' in S and l > 0 else None
    nxt = S.get('next')
    seen = set(q)
    done = set(q[:max(0, l - 1)]) if l else set()
    badge = {u: f'f={f[u]}' for u in seen}
    _gtree(cv, T, box, CH, HEAD, now, hl={nxt} if nxt is not None and 'g' in S and nxt in S['g'].get(now, ()) else (),
           done=done, badge=badge, sub={u: f'+{INFORM[u]}' for u in range(N)},
           title='员工树（节点旁 +t = informTime；绿框 f = 根到该点的时间；蓝 = now，青 = next）')


CODE = '''
class Solution(object):
    def numOfMinutes(self, n, headID, manager, informTime):

        g = {x : set() for x in range(n)}
        q = []
        f = [0] * n
        for index, x in enumerate(manager):
            if x == -1:
                q.append(index)
            else:
                g[x].add(index)
        
        l = 0
        r = 1
        while l < r:
            now = q[l]
            l += 1
            for next in g[now]:
                f[next] = f[now] + informTime[now]
                q.append(next)
                r += 1
        
        return max(f)
'''

CONFIG = dict(
    num=1376, title='通知所有员工所需的时间', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='建图 + BFS 求根到各点距离',
    tags=['链表树与回溯', '难度分 1561'],
    code=CODE,
    call='Solution().numOfMinutes(7, 2, [2,2,-1,2,2,4,4], [0,0,3,0,2,0,0])',
    expect=5,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var='q', label='队列 q（l = 队头，r = 队尾后一位）', cell=64, h=140,
             pointers={'l': 'blue', 'r': 'pink'}),
        dict(type='array', var='f', label='f[x]：从根走到 x 的时间', cell=64, h=130),
    ],
    watch=[('now', 'now', 'blue'), ('next', 'next', 'pink'), ('l', 'l', 'cyan'), ('r', 'r', 'yellow'), ('max(f)', lambda S: max(S['f']) if 'f' in S else None, 'green')],
    captions={
        'g = {x': '把「负责人 → 下属」看成有向边，`g[x]` 是 x 的下属集合',
        'f = [0]': '`f[x]` 记录根到 `x` 的距离，边 `fa→x` 的长度是 `informTime[fa]`',
        'if x == -1': lambda S, B, r: (f"`manager[{S['index']}] = -1` → `{S['index']}` 是总负责人，当作 BFS 的起点" if S['x'] == -1 else f"`{S['x']}` 是 `{S['index']}` 的负责人，不是根，等下加边"),
        'q.append(index)': '总负责人 `{index}` 入队，作为 BFS 的起点',
        'g[x].add(index)': '`{index}` 挂在 `g[{x}]` 下：`g[{x}] = {g[x]}`',
        'l = 0': '`l`、`r` 是手写队列的头尾：`q[l:r]` 是还没处理的节点',
        'while l < r': lambda S, B, r: ('队列非空，继续' if S['l'] < S['r'] else '队列空了，所有员工都走到了'),
        'now = q[l]': '取出队头 `now = {now}`，它的 `f[now] = {f[now]}`',
        'for next in g[now]': lambda S, B, r: (f"枚举 `{S['now']}` 的下属 `{S['next']}`" if S['next'] != B.get('next') or B.get('now') != S['now'] else f"`{S['now']}` 的下属都枚举完了，回到 while"),
        'f[next] = f[now] + informTime[now]': '==x 只能从 fa[x] 走过来==：`f[{next}] = f[{now}] + informTime[{now}] = {f[now]} + {informTime[now]} = {f[next]}`',
        'q.append(next)': '`{next}` 入队，之后再通知它的下属',
        'r += 1': '队尾后移：`r = {r}`',
        'return max(f)': '最远的节点就是最晚收到通知的人：`max(f) = {ret}`',
    },
    skip=['l = 0', 'r = 1', 'for index, x in enumerate', 'l += 1'],
    max_steps=90,
    cards=dict(
        one_liner='把上下级看成带权有向图：从根 BFS，求到每个人的距离，取最大',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 名员工，`manager[i]` 是 `i` 的直属负责人，`headID` 是总负责人',
                 '`informTime[i]` 是 `i` 通知所有直属下属所需的分钟数',
                 '求所有员工都收到通知的最少分钟数',
                 '本视频：`headID = 2`，答案 `5`'],
        quote='对于点i出发的边，其边长就是informTime[i]。接下来我们从根开始进行一趟bfs，计算从根节点开始到每个节点的距离，然后取其中的最大值作为答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['把树看成有向连通图：从 `i` 指向下属的边，边长 `informTime[i]`',
              '设 `f[x]` 为根到 `x` 的距离，`x` 只能由父亲走来：`f[x] = f[fa[x]] + informTime[fa[x]]`',
              '手写队列 `q[l:r]` 做 BFS，访问完所有节点后取 `max(f)`'],
        result='BFS 结束，`f = [3, 3, 0, 3, 3, 5, 5]` → `max(f) = 5`',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '树里每个点只有一个父亲，所以 BFS 不需要 `visited`',
                 '根的 `f` 是 0：「自己知道」不花时间，`informTime` 算在发出通知的那条边上',
                 '对比灵神：灵神用 DFS 递归累加 `path_sum`；yiduobo 用 BFS 递推 `f[x]`，两者是同一条公式',
                 '原文已是 Python 3 可运行的写法，未改动'],
    ),
)
