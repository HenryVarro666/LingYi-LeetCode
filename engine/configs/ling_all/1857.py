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
    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
        n = len(colors)
        g = [[] for _ in range(n)]
        deg = [0] * n
        for x, y in edges:
            if x == y:  # 自环
                return -1
            g[x].append(y)
            deg[y] += 1

        ans = visited = 0
        q = deque(i for i, d in enumerate(deg) if d == 0)  # 入度为 0 的点入队
        f = [defaultdict(int) for _ in range(n)]
        while q:
            x = q.popleft()  # x 的所有转移来源都计算完毕，也都更新到 f[x] 中
            visited += 1
            ch = colors[x]
            f[x][ch] += 1
            ans = max(ans, f[x][ch])
            for y in g[x]:
                for ch, c in f[x].items():
                    f[y][ch] = max(f[y][ch], c)  # 刷表法，更新邻居的最大值
                deg[y] -= 1
                if deg[y] == 0:
                    q.append(y)

        return ans if visited == n else -1
'''
LN = _mk(CODE)
COLORS = 'abaca'
NM = [f'{i}:{c}' for i, c in enumerate(COLORS)]
POS = {NM[0]: (0, .5), NM[1]: (.42, 0), NM[2]: (.42, 1), NM[3]: (.72, 1), NM[4]: (1, 1)}
EDGES = [(NM[a], NM[b]) for a, b in [[0, 1], [0, 2], [2, 3], [3, 4]]]


def _fs(d):
    return ' '.join(f'{k}{v}' for k, v in sorted(d.items()) if v)


def _draw(cv, S, B, box, T):
    q, f, deg = S.get('q'), S.get('f'), S.get('deg')
    st, sub, hot = {}, {}, None
    if q is not None and f is not None and deg is not None and len(f) == 5:
        line, x = S['_line'], S.get('x')
        cur = x if (x is not None and LN('x = q.popleft()') <= line <= LN('q.append(y)')) else None
        for i in range(5):
            pend = i == S.get('y') and LN('deg[y] -= 1') <= line <= LN('if deg[y] == 0')
            if deg[i] == 0 and i not in q and not pend:
                st[NM[i]] = 'green'
            if i in q:
                st[NM[i]] = 'cyan'
            sub[NM[i]] = _fs(f[i])
        if cur is not None:
            st[NM[cur]] = 'yellow'
            y = S.get('y')
            if y is not None and line >= LN('for ch, c in') and y in S['g'][cur]:
                hot = (NM[cur], NM[y])
    _gdraw(cv, box, T, POS, EDGES, st, sub, hot, '节点 = 编号:颜色 · 下方 = f（颜色+次数）· 青 在队列 · 黄 刚出队 · 绿 已定', R=36)


def _fx(S):
    f, x = S.get('f'), S.get('x')
    if f is None or x is None or len(f) != 5 or S['_line'] < LN('x = q.popleft()'):
        return ''
    return f'`f[{x}]` = ' + (('{' + ', '.join(f"'{k}': {v}" for k, v in sorted(f[x].items())) + '}') if f[x] else '{}')


CONFIG = dict(
    num=1857, title='有向图中最大颜色值', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='拓扑排序 + 刷表法 DP',
    tags=['图论算法', '难度分 2313'],
    code=CODE,
    call="Solution().largestPathValue('abaca', [[0,1],[0,2],[2,3],[3,4]])",
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=500),
        dict(type='queue', var='q', label='q（入度为 0 的点）', h=130),
        dict(type='text', fn=_fx, h=60),
    ],
    max_steps=80,
    watch=[('x', 'x', 'yellow'), ('y', 'y', 'pink'), ('ans', 'ans', 'green'), ('visited', 'visited', 'cyan')],
    skip=['n = len(colors)', 'for y in g[x]', 'for ch, c in'],
    captions={
        'g = [[]': '邻接表 `g[x]` 存 `x` 能到达的点',
        'deg = [0]': '`deg[y]` 记 `y` 的入度：还有几个点没把结果传给它',
        'g[x].append(y)': '建边 `{x} → {y}`',
        'deg[y] += 1': '`{y}` 的入度加一：`deg[{y}] = {deg[y]}`',
        'ans = visited': '`ans` 记最大颜色值，`visited` 记出过队的点数（判环用）',
        'q = deque': '入度为 0 的点没有来源，先入队：`{list(q)}`',
        'f = [defaultdict': '`f[x][颜色]` = 以 `x` 为终点的路径中，该颜色最多出现几次',
        'while q': lambda S, B, r: (f'队列里还有 `{len(S.q)}` 个点' if S.q else '队列空了，拓扑排序结束'),
        'x = q.popleft()': '`x = {x}` 出队：所有指向它的点都已把结果刷进 `f[{x}]`',
        'visited += 1': '又有一个点出队：`visited = {visited}`',
        'ch = colors[x]': '点 `{x}` 自己的颜色是 `{ch}`',
        'f[x][ch] += 1': '路径多经过了点 `{x}`：`f[{x}][{ch!r}]` 加一 → `{f[x][ch]}`',
        'ans = max': '`ans = max({B.ans}, f[{x}][{ch!r}])` = =={ans}==',
        'f[y][ch] = max': '刷表：把 `f[{x}]` 里颜色 `{ch}` 的 `{c}` 传给邻居 `{y}`：`f[{y}][{ch!r}] = max({B.f[y][ch]}, {c}) = {f[y][ch]}`',
        'deg[y] -= 1': '`{x}` 的结果传完了：`deg[{y}] = {deg[y]}`',
        'if deg[y] == 0': lambda S, B, r: (f'`deg[{S.y}] = 0`：来源都传完了 → 入队' if S.deg[S.y] == 0
                                           else f'`deg[{S.y}] = {S.deg[S.y]}`：还有来源没传完，先不入队'),
        'q.append(y)': '点 `{y}` 的 `f` 已定型，入队',
        'return ans if': lambda S, B, r: (f'`visited = {S.visited}` = `n`：全部出过队，无环 → 答案 =={r}==' if r != -1
                                          else f'`visited = {S.visited}` < `n`：有点入不了队 → 有环，返回 -1'),
    },
    cards=dict(
        one_liner='拓扑序上做 DP：f[x][c] 记终点为 x 时颜色 c 最多几个',
        complexity='时间 `O((n+m)|Σ|)`，空间 `O(m+n|Σ|)`',
        problem=['有向图，`colors[i]` 是节点 `i` 的颜色，路径的颜色值 = 路径上出现最多的颜色的点数',
                 '求所有有效路径的最大颜色值；图中有环则返回 `-1`',
                 '示例：`colors="abaca"`，边 `0→1,0→2,2→3,3→4` → `3`'],
        quote='定义 f[x][i] 表示终点为 x 的路径中，颜色 i 的最大出现次数。为了正确计算转移，必须先把 x 的所有转移来源算出来，也就是按照拓扑序转移。',
        quote_src='—— 灵茶山艾府题解',
        idea=['入度为 0 的点入队；`x` 出队时先给 `f[x][colors[x]]` 加一',
              '刷表法：用 `f[x][i]` 去更新邻居 `f[y][i]` 的最大值，再把 `y` 入度减一',
              '只需取 `f[x][colors[x]]` 的最大值当答案；`visited != n` 说明有环'],
        summary=['时间 `O((n+m)|Σ|)`，空间 `O(m+n|Σ|)`，`|Σ| = 26`',
                 '自环 `x == y` 直接返回 `-1`；其余环靠 `visited == n` 判断',
                 '`f[x][ch] += 1` 要在 `x` 出队时做，保证来源都刷完',
                 '灵神另给了记忆化搜索 + 三色标记法：以起点定义状态，用 0 表示计算中来判环',
                 '同类题：2050 并行课程 III（拓扑序上 DP）'],
    ),
)
