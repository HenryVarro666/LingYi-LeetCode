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
    def minimumTime(self, n: int, relations: List[List[int]], time: List[int]) -> int:
        g = [[] for _ in range(n)]
        deg = [0] * n  # deg[i] 表示 i 的先修课的个数
        for x, y in relations:
            g[x - 1].append(y - 1)  # 建图
            deg[y - 1] += 1

        q = deque(i for i, d in enumerate(deg) if d == 0)  # 没有先修课
        f = [0] * n
        while q:
            x = q.popleft()  # x 出队，意味着 x 的所有先修课都上完了
            f[x] += time[x]  # 加上当前课程的时间，就得到了最终的 f[x]
            for y in g[x]:  # 遍历 x 的邻居 y
                f[y] = max(f[y], f[x])  # 更新 f[y] 的所有先修课程耗时的最大值
                deg[y] -= 1
                if deg[y] == 0:  # y 的先修课已上完
                    q.append(y)
        return max(f)
'''
LN = _mk(CODE)
POS = {'1': (0, 0), '2': (0, .5), '3': (0, 1), '4': (.5, 1), '5': (1, .5)}
TIME = [1, 2, 3, 4, 5]
EDGES = [(str(a), str(b)) for a, b in [[1, 5], [2, 5], [3, 5], [3, 4], [4, 5]]]


def _nxt(S, B):
    if B.get('_line', 0) > LN('for y in g[x]') and S.y == B.get('y'):
        raise ValueError('loop end')
    return f'看 `x = {S.x}` 的后继课 `y = {S.y}`'


def _draw(cv, S, B, box, T):
    q, f, deg = S.get('q'), S.get('f'), S.get('deg')
    st, sub, hot = {}, {}, None
    for k in POS:
        sub[k] = f't={TIME[int(k) - 1]}'
    if q is not None and f is not None and deg is not None and len(f) == 5:
        line, x = S['_line'], S.get('x')
        cur = x if (x is not None and LN('x = q.popleft()') <= line <= LN('q.append(y)')) else None
        for i in range(5):
            k = str(i + 1)
            pend = i == S.get('y') and LN('deg[y] -= 1') <= line <= LN('if deg[y] == 0')
            if deg[i] == 0 and i not in q and not pend:
                st[k] = 'green'
            if i in q:
                st[k] = 'cyan'
            if f[i]:
                sub[k] = f't={TIME[i]} f={f[i]}'
        if cur is not None:
            st[str(cur + 1)] = 'yellow'
            y = S.get('y')
            if y is not None and line >= LN('for y in g[x]') and y in (S.get('g') or [[]] * 5)[cur]:
                hot = (str(cur + 1), str(y + 1))
    _gdraw(cv, box, T, POS, EDGES, st, sub, hot, '节点 = 课号 · t = 耗时 · 青 在队列 q · 黄 刚出队 · 绿 f 已定', R=32)


CONFIG = dict(
    num=2050, title='并行课程 III', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='拓扑排序 · 在拓扑序上 DP',
    tags=['图论算法', '难度分 2084'],
    code=CODE,
    call='Solution().minimumTime(5, [[1,5],[2,5],[3,5],[3,4],[4,5]], [1,2,3,4,5])',
    expect=12,
    views=[
        dict(type='custom', draw=_draw, h=560),
        dict(type='array', var='deg', label='deg（还剩几门先修课没上完）', h=140),
        dict(type='array', var='f', label='f（最早完成月份）', h=140,
             color=lambda S, i, v: 'green' if v else None),
    ],
    skip=['for y in g[x]'],
    watch=[('x', 'x', 'yellow'), ('y', 'y', 'pink')],
    captions={
        'g[x - 1].append': '`{x} → {y}`：先修课 `{x}` 向 `{y}` 连边（下标减 1）',
        'deg[y - 1] += 1': '`{y}` 多了一门先修课：`deg[{y-1}] = {deg[y-1]}`',
        'q = deque': '先修课个数为 0 的课，现在就能开始 → 入队：`{list(q)}`',
        'f = [0] * n': '`f[i]` 先全部清零；入队前它只存「先修课里最晚完成的时间」',
        'while q': lambda S, B, r: (f'队列里还有 `{len(S.q)}` 门课待处理' if S.q else '队列空了：所有课都处理完'),
        'x = q.popleft()': '`x = {x}` 出队：它的先修课都上完了，`f[{x}]` 里已是最晚的先修完成时间 `{f[x]}`',
        'f[x] += time[x]': '加上自己的耗时：`f[{x}] = {B.f[x]} + {time[x]}` = =={f[x]}==，这是它的最终完成月份',
        'f[y] = max': '后继课 `{y+1}` 必须等 `{x+1}` 上完：`f[{y}] = max({B.f[y]}, {f[x]}) = {f[y]}`',
        'deg[y] -= 1': '`{y}` 的先修课少了一门：`deg[{y}] = {deg[y]}`',
        'if deg[y] == 0': lambda S, B, r: (f'`deg[{S.y}] = 0`：先修课都上完 → 入队' if S.deg[S.y] == 0
                                           else f'`deg[{S.y}] = {S.deg[S.y]}`：还有先修课没完成，先不入队'),
        'q.append(y)': '课 `{y+1}` 可以开始了，`f[{y}] = {f[y]}` 已是它的开始时间 → 入队',
        'return max(f)': '最晚完成的那门课决定总时长：`max(f)` = =={ret}==',
    },
    cards=dict(
        one_liner='拓扑序走一遍：完成时间 = 自己耗时 + 先修课里最晚完成的',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['`n` 门课，`relations[j]=[a,b]` 表示课 `a` 必须在课 `b` 之前完成',
                 '`time[i]` 是第 `i+1` 门课的耗时，课程可同时上，求完成所有课的最少月份',
                 '示例：`n=5`，`time=[1,2,3,4,5]` → `12`'],
        quote='设当前节点为 x，我们可以在计算出 f[x] 后，更新 y 的所有先修课程耗时的最大值，这里 x 是 y 的先修课程。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i] = time[i] + max f[j]`（`j` 是 `i` 的先修课）',
              '边算拓扑序边转移：`x` 出队时 `f[x]` 先修部分已齐，补上 `time[x]` 就定型',
              '用 `f[x]` 去刷新后继 `f[y]`（刷表法），入度归零再入队'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`',
                 '出队时才 `f[x] += time[x]`：入队前 `f[y]` 只是先修课的最大值',
                 '课号从 1 开始，建图时要 `x - 1`、`y - 1`',
                 '答案是 `max(f)`，不是最后一个出队的课',
                 '同类题：1857 有向图中最大颜色值（拓扑序上 DP）'],
    ),
)
