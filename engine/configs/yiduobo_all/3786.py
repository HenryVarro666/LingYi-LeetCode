import math as _m

_PAL = ['blue', 'pink', 'green', 'orange', 'purple', 'cyan']


def _pos(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    depth, order, leaves = {0: 0}, [], [0]
    pos = {}

    def go(u, fa, d):
        kids = [v for v in adj[u] if v != fa]
        if not kids:
            pos[u] = (len(pos_leaf), d)
            pos_leaf.append(u)
            return
        for v in kids:
            go(v, u, d + 1)
        xs = [pos[v][0] for v in kids]
        pos[u] = ((min(xs) + max(xs)) / 2, d)
    pos_leaf = []
    go(0, -1, 0)
    return pos


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n, edges, group = S['n'], S['edges'], S['group']
    pos = _pos(n, edges)
    inner = S.get('_inner', {})
    cur, kid = inner.get('now'), inner.get('nxt')
    width = max(p[0] for p in pos.values()) + 1
    height = max(p[1] for p in pos.values()) + 1
    cw = min(170, (x1 - x0 - 100) / max(width, 1))
    rh = min(95, (y1 - y0 - 130) / max(height - 1, 1))
    ox = x0 + (x1 - x0 - cw * (width - 1)) / 2
    oy = y0 + 80
    P = {u: (ox + p[0] * cw, oy + p[1] * rh) for u, p in pos.items()}
    gs = sorted(set(group))
    col = {g: T[_PAL[i % len(_PAL)]] for i, g in enumerate(gs)}
    cv.text((x0 + 18, y0 + 4), '树（颜色 = 点权，黄环 = now，黄边 = now-nxt）', 22, T['muted'], bold=True)
    for a, b in edges:
        hot = (cur is not None and kid is not None and {a, b} == {cur, kid})
        cv.line([P[a], P[b]], T['yellow'] if hot else T['border'], 7 if hot else 3)
    for u in range(n):
        px, py = P[u]
        r = 30
        if u == cur:
            cv.d.ellipse((px - r - 8, py - r - 8, px + r + 8, py + r + 8), outline=T['yellow'], width=5)
        cv.d.ellipse((px - r, py - r, px + r, py + r), fill=col[group[u]])
        cv.text((px, py), group[u], 30, T['bg'], anchor='mm', bold=True)
        cv.text((px, py + r + 6), f'#{u}', 18, T['dim'], anchor='mt', mono=True)


_DONE = {}


def _mark(S):
    _DONE['k'] = (S.now, S.nxt, S.g)
    a = S.s[S.nxt][S.g] + S.cnt[S.nxt][S.g]
    b = S.cnt[S.now][S.g] - S.cnt[S.nxt][S.g]
    c = S.s[S.now][S.g] - S.s[S.nxt][S.g] - S.cnt[S.nxt][S.g]
    return f'跨子树的点对：新子树的距离和 `{a}` × 之前已合并的个数 `{b}` + 之前已合并的距离和 `{c}` × 新子树个数 `{S.cnt[S.nxt][S.g]}` → `res` = =={S.res}=='


CONFIG = dict(
    num=3786, title='树组的交互代价总和', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='树形 DP：子树点权个数 cnt 与到根距离和 s',
    tags=['灵神题单·贪心与思维', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def interactionCosts(self, n, edges, group):
        
        t = [[] for _ in range(n)]
        s = [{} for _ in range(n)]
        cnt = [{} for _ in range(n)]

        for x, y in edges:
            t[x].append(y)
            t[y].append(x)

        def dfs(now, fa):
            s[now][group[now]] = 0
            cnt[now][group[now]] = 1
            res = 0
            for nxt in t[now]:
                if nxt == fa:
                    continue
                res += dfs(nxt, now)
                for g in s[nxt]:
                    s[now][g] = s[now].get(g, 0) + s[nxt][g] + cnt[nxt][g]
                    cnt[now][g] = cnt[now].get(g, 0) + cnt[nxt][g]
                    res += (s[nxt][g] + cnt[nxt][g]) * (cnt[now].get(g, 0) - cnt[nxt][g]) + cnt[nxt][g] * (s[now][g] - s[nxt][g] - cnt[nxt][g])

            return res
        
        return dfs(0, -1)
''',
    call='Solution().interactionCosts(5, [[0,1],[0,2],[1,3],[1,4]], [1,2,1,1,2])',
    expect=7,
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='map', var=lambda S: S['cnt'][S['_inner']['now']] if S.get('_inner', {}).get('now') is not None else {}, h=110,
             label='cnt[now]：now 子树里每种点权的个数'),
        dict(type='map', var=lambda S: S['s'][S['_inner']['now']] if S.get('_inner', {}).get('now') is not None else {}, h=110,
             label='s[now]：这些点到 now 的距离之和'),
        dict(type='calls', h=200),
    ],
    watch=[('res', 'res', 'green'), 'now', 'nxt', 'g'],
    skip=['t = [[]', 's = [{}', 'cnt = [{}', 'for x, y in edges', 't[x].append', 't[y].append', 'continue', 'res = 0'],
    max_steps=75,
    captions={
        's[now][group[now]] = 0': '到达点 `{now}`，点权 `{group[now]}`：它自己到自己距离为 0 → `s[{now}][{group[now]}] = 0`',
        'cnt[now][group[now]] = 1': '子树里点权 `{group[now]}` 的点有 1 个（自己）→ `cnt[{now}][{group[now]}] = 1`',
        'for nxt in t[now]': lambda S, B, r: (f'`now = {S.now}` 的子树都合并完了' if 'nxt' in B and B.now == S.now and B.nxt == S.nxt else f'看邻居 `nxt = {S.nxt}`'),
        'if nxt == fa': lambda S, B, r: (f'`nxt = {S.nxt}` 是父节点，跳过' if S.nxt == S.fa else f'`nxt = {S.nxt}` 是子节点 → 递归，先算完它的子树内部的路径'),
        'res += dfs(nxt, now)': '递归进入子节点 `{B.nxt}`：先算它子树内部的点对代价，返回后加到 `res`',
        'for g in s[nxt]': lambda S, B, r: (f'子树 `{S.nxt}` 的点权都合并完了' if _DONE.get('k') == (S.now, S.nxt, S.g) else f'合并点权 `g = {S.g}`：子树 `{S.nxt}` 里 `cnt = {S.cnt[S.nxt][S.g]}`，`s = {S.s[S.nxt][S.g]}`'),
        's[now][g] = ': '子树点到 now 要多走一条边：每个点距离 +1 → `s[now][{g}] += s[nxt] + cnt[nxt]` = =={s[now][g]}==',
        'cnt[now][g] = ': '`cnt[now][{g}]` += 子树的个数 → =={cnt[now][g]}==',
        'res += (': lambda S, B, r: _mark(S),
        'return res': '点 `{now}` 的子树里所有同点权点对的代价和 = `{res}`',
        'return dfs(0, -1)': '从 0 号点出发 DFS，它的返回值就是整棵树的答案',
    },
    cards=dict(
        one_liner='自底向上合并子树：记下点权个数和到根的距离和，跨子树点对一次算完',
        complexity='时间 `O(nU)`，空间 `O(nU)`；`U ≤ 20` 为不同点权数',
        problem=['一棵 `n` 个点的树，点有组标签 `group`',
                 '同组两点的交互代价 = 路径边数，求所有同组无序点对的代价之和',
                 '本视频：`n=5`，`group=[1,2,1,1,2]` → `7`'],
        quote='注意到需要计算的是交互代价的总和，那么就可以考虑使用共享法，分别计算每个节点为答案做出的贡献。',
        quote_src='—— yiduobo 题解原文',
        idea=['以 `now` 为根：路径要么只在某棵子树内（递归得到），要么经过 `now`（从一棵子树走到另一棵）',
              '经过 `now` 的点对代价 = 两点各自到 `now` 的距离之和，按「已合并子树」逐棵相加',
              '记 `cnt[x][g]` 为子树 x 中点权 g 的个数，`s[x][g]` 为它们到 x 的距离和，合并时 `s` 要加上 `cnt`（多走一条边）'],
        summary=['时间 `O(nU)`，空间 `O(nU)`',
                 '易错点：子树 `nxt` 的距离要整体 `+cnt[nxt][g]`，才是到 `now` 的距离',
                 '`res` 的更新式先用「已合并子树」的 `cnt/s`，所以要在 `cnt[now]` 更新后用差值取出',
                 '原文已是 Python 3 可运行写法，未作修改',
                 '对比灵神：灵神按边拆分、乘法原理 `a_i·b_i`；yiduobo 按点拆分、合并时累加距离'],
    ),
)
