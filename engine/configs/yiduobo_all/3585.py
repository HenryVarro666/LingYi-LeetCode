def _tidy(children, root=0):
    pos = {}
    cnt = [0]
    md = [0]

    def go(u, d):
        md[0] = max(md[0], d)
        ks = children[u]
        if not ks:
            x = cnt[0]
            cnt[0] += 1
        else:
            for k in ks:
                go(k, d + 1)
            x = (pos[ks[0]][0] + pos[ks[-1]][0]) / 2
        pos[u] = (x, d)
    go(root, 0)
    return pos, max(cnt[0], 1), md[0] + 1


def _children(n, edges):
    g = [[] for _ in range(n)]
    for e in edges:
        g[e[0]].append(e[1])
        g[e[1]].append(e[0])
    ch = [[] for _ in range(n)]
    seen = {0}
    st = [0]
    while st:
        u = st.pop()
        for v in g[u]:
            if v not in seen:
                seen.add(v)
                ch[u].append(v)
                st.append(v)
    for c in ch:
        c.sort()
    return ch


def _draw_tree(cv, box, T, children, edges, node_fn, edge_fn=None, under_fn=None, title=None, rad=23):
    """node_fn(u)->颜色名或None；edge_fn(a,b)->颜色名或None；under_fn(u)->节点下方小字"""
    x0, y0, x1, y1 = box
    if title:
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
        y0 += 44
    pos, w, dep = _tidy(children)
    gx = (x1 - x0 - 80) / max(w - 1, 1) if w > 1 else 0
    gx = min(gx, 170)
    gy = min((y1 - y0 - 90) / max(dep - 1, 1), 120)
    ox = x0 + (x1 - x0 - gx * (w - 1)) / 2
    oy = y0 + 40

    def P(u):
        return (ox + pos[u][0] * gx, oy + pos[u][1] * gy)
    for e in edges:
        a, b = e[0], e[1]
        pa_, pb = P(a), P(b)
        c = edge_fn(a, b) if edge_fn else None
        cv.line([pa_, pb], T[c] if c else T['border'], 7 if c else 3)
        if len(e) > 2:
            mx, my = (pa_[0] + pb[0]) / 2, (pa_[1] + pb[1]) / 2
            lab = str(e[2])
            tw = cv.tlen(lab, 20, True) + 12
            cv.rect((mx - tw / 2, my - 13, mx + tw / 2, my + 13), fill=T['bg'], r=8)
            cv.text((mx, my), lab, 20, T[c] if c else T['muted'], anchor='mm', bold=True, mono=True)
    for u in range(len(children)):
        X, Y = P(u)
        c = node_fn(u)
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=T[c] if c else T['panel2'],
                     outline=T[c] if c else T['border'], width=3)
        cv.text((X, Y), u, 26, T['bg'] if c else T['text'], anchor='mm', bold=True)
        if under_fn:
            s = under_fn(u)
            if s:
                cv.text((X + rad + 8, Y), s, 20, T['cyan'], anchor='lm', bold=True, mono=True)

CODE = '''
class Solution(object):
    def findMedian(self, n, edges, queries):
        
        g = [[] for _ in range(n)]
        for u, v, w in edges:
            g[u].append((v, w))
            g[v].append((u, w))
        
        dis = [0] * n
        level = [0] * n
        f = [[] for _ in range(n)]
        def dfs(now, fa, f, dis):
            if fa is not None:
                f[now].append(fa)
                while len(f[f[now][-1]]) >= len(f[now]):
                    f[now].append(f[f[now][-1]][len(f[now]) - 1])
            
            for nxt, w in g[now]:
                if nxt == fa:
                    continue
                dis[nxt] = dis[now] + w
                level[nxt] = level[now] + 1
                dfs(nxt, now, f, dis)
        
        def get_lca(x, y):
            high, low = x, y
            if level[high] > level[low]:
                high, low = low, high

            p = len(f[low]) - 1
            while level[low] != level[high]:
                while p > len(f[low]) - 1 or (p > 0 and level[f[low][p]] < level[high]):
                    p -= 1
                low = f[low][p]
            
            p = len(f[low]) - 1
            while low != high:
                while p > len(f[low]) - 1 or (p > 0 and level[f[low][p]] == level[f[high][p]]):
                    p -= 1
                
                low = f[low][p]
                high = f[high][p]
            
            return low

        dfs(0, None, f, dis)
        
        res = []
        for x, y in queries:
            lca = get_lca(x, y)
            total_dis = dis[x] + dis[y] - dis[lca] * 2
            if (dis[x] - dis[lca]) * 2 >= total_dis:
                d = 0
                while d * 2 < total_dis:
                    p = len(f[x]) - 1
                    while p > 0 and (d + dis[x] - dis[f[x][p]]) * 2 >= total_dis:
                        p -= 1
                    
                    d += dis[x] - dis[f[x][p]]
                    x = f[x][p]
                
                res.append(x)
            
            else:
                d = 0
                while d * 2 < total_dis:
                    p = len(f[y]) - 1
                    while p > 0 and (d + dis[y] - dis[f[y][p]]) * 2 > total_dis:
                        p -= 1
                    
                    if (d + dis[y] - dis[f[y][p]]) * 2 <= total_dis:
                        d += dis[y] - dis[f[y][p]]
                        y = f[y][p]
                    else:
                        break
                
                res.append(y)
        
        return res
'''
LINE_TXT = {i: l for i, l in enumerate(CODE.strip('\n').split('\n'), 1)}

N = 5
EDGES = [[0, 1, 2], [0, 2, 5], [1, 3, 1], [2, 4, 3]]
QUERIES = [[3, 4], [4, 3]]
CH = _children(N, EDGES)
_GL = range([i for i, l in LINE_TXT.items() if 'def get_lca' in l][0], [i for i, l in LINE_TXT.items() if 'return low' in l][0] + 1)


def _node(S):
    inner = S.get('_inner', {})
    roles = {}
    if 'fa' in inner and 'now' in inner:
        roles[inner['now']] = 'yellow'
    elif 'total_dis' in inner or 'lca' in inner:
        roles[inner['x']] = 'blue'
        roles[inner['y']] = 'pink'
        if inner.get('lca') is not None:
            roles[inner['lca']] = 'yellow'
    return lambda u: roles.get(u)


def _draw(cv, S, B, box, T):
    d = S.get('dis')
    _draw_tree(cv, box, T, CH, EDGES, _node(S),
               under_fn=(lambda u: f'dis={d[u]}' if d and u < len(d) and (d[u] or u == 0) else None),
               title='树（黄 = DFS 当前点 / lca，蓝 = x，粉 = y）')


def _fmap(S):
    f = S.get('f')
    return {i: f[i] for i in range(len(f))} if f else None


def _cap_wh(S, B, ret):
    now = S.now
    f = S.f
    if len(f[f[now][-1]]) >= len(f[now]):
        return f'`f[{f[now][-1]}]` 有 {len(f[f[now][-1]])} 项 ≥ `f[{now}]` 的 {len(f[now])} 项 → ==还能再翻倍=='
    return f'`f[{f[now][-1]}]` 只有 {len(f[f[now][-1]])} 项，不够长 → `f[{now}]` 到此为止'


def _cap_pick(S, B, ret):
    return f'`{S.p}` 级大步：走完后 `d` 会到 `{S.d + S.dis[S.x] - S.dis[S.f[S.x][S.p]]}`'


CONFIG = dict(
    num=3585, title='树中找到带权中位节点', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='倍增求 LCA · 按距离往上走',
    tags=['难度分 2429'],
    code=CODE,
    call='Solution().findMedian(5, [[0,1,2],[0,2,5],[1,3,1],[2,4,3]], [[3,4],[4,3]])',
    expect=[2, 0],
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var='dis', label='dis（根到各点的距离）', cell=60, h=150),
        dict(type='map', var=_fmap, label='f[i]：i 往上走 2^0, 2^1, … 步到的点', fmt=lambda k, v: f'f[{k}] = {v}', h=250),
    ],
    watch=['x', 'y', 'lca', 'total_dis', ('d', 'd', 'cyan'), ('res', 'res', 'green')],
    skip=['g = [[] for', 'for u, v, w in edges', 'g[u].append', 'g[v].append', 'dis = [0]', 'level = [0]', 'f = [[] for',
          'level[nxt] = ', 'for nxt, w in g[now]', 'd = 0', 'if nxt == fa', 'continue', 'if fa is not None', 'res = []', 'def dfs'] + list(_GL),
    max_steps=100,
    captions={
        'dfs(0, None, f, dis)': '从根 0 出发 DFS：沿途记下 `f[now]`（往上走 1、2、4… 步的祖先）、`level`、`dis`',
        'f[now].append(fa)': '`f[{now}]` 先放进父亲 `{fa}`：往上走 2^0 步',
        'while len(f[f[now][-1]])': _cap_wh,
        'f[now].append(f[f[now][-1]]': lambda S, B, r: f'`f[{S.now}]` 追加 `{S.f[S.now][-1]}`：走 2^{len(S.f[S.now]) - 1} 步 = 先走 2^{len(S.f[S.now]) - 2} 步，再走 2^{len(S.f[S.now]) - 2} 步',
        'dis[nxt] = dis[now] + w': '`dis[{nxt}] = {dis[now]} + {w} = {dis[nxt]}`：到根距离 = 父亲的距离 + 边权（`level` 同理 +1）',
        'lca = get_lca(x, y)': '倍增求 x、y 的 `lca`：先把深的一方跳到同一层，再一起往上跳',
        'total_dis = ': '`lca = {lca}`，`total_dis = {dis[x]} + {dis[y]} − 2×{dis[lca]} = {total_dis}`：x 到 y 的路径总长',
        'if (dis[x] - dis[lca]) * 2 >= total_dis': lambda S, B, r: (
            f'`(dis[x]−dis[lca])×2 = {(S.dis[S.x]-S.dis[S.lca])*2}` ' + ('>=' if (S.dis[S.x]-S.dis[S.lca])*2 >= S.total_dis else '<') +
            f' `total_dis = {S.total_dis}` → 答案在 ==x 到 lca== 这一段，从 x 往上走' if (S.dis[S.x]-S.dis[S.lca])*2 >= S.total_dis else
            f'`(dis[x]−dis[lca])×2 = {(S.dis[S.x]-S.dis[S.lca])*2}` < `total_dis = {S.total_dis}` → 答案在 ==y 到 lca== 这一段，从 y 往上走'),
        'while d * 2 < total_dis': lambda S, B, r: (f'`d×2 = {S.d * 2}` < `total_dis = {S.total_dis}`，还没走够一半 → 继续' if S.d * 2 < S.total_dis else f'`d×2 = {S.d * 2}` >= `total_dis = {S.total_dis}`：走够一半 → 停'),
        'p = len(f[x]) - 1': '从最大的一步试起：`p = {p}`',
        'p = len(f[y]) - 1': '从最大的一步试起：`p = {p}`',
        'while p > 0 and (d + dis[x] - dis[f[x][p]]) * 2 >= total_dis': lambda S, B, r: (
            '`p = 0`，已是最小的一步，不能再缩' if S.p == 0 else
            f'走 2^{S.p} 步 `d` 会到 {S.d + S.dis[S.x] - S.dis[S.f[S.x][S.p]]}，×2 ' + ('>=' if (S.d + S.dis[S.x] - S.dis[S.f[S.x][S.p]]) * 2 >= S.total_dis else '<') + f' 总长 {S.total_dis}' +
            (' → ==够一半了，换小步==' if (S.d + S.dis[S.x] - S.dis[S.f[S.x][S.p]]) * 2 >= S.total_dis else ' → 这步可以走')),
        'p -= 1': '步子太大，换小一档：`p = {p}`',
        'while p > 0 and (d + dis[y] - dis[f[y][p]]) * 2 > total_dis': lambda S, B, r: (
            '`p = 0`，已是最小的一步，不能再缩' if S.p == 0 else
            f'走 2^{S.p} 步 `d` 会到 {S.d + S.dis[S.y] - S.dis[S.f[S.y][S.p]]}，×2 ' + ('>' if (S.d + S.dis[S.y] - S.dis[S.f[S.y][S.p]]) * 2 > S.total_dis else '<=') + f' 总长 {S.total_dis}' +
            (' → ==超过一半，换小步==' if (S.d + S.dis[S.y] - S.dis[S.f[S.y][S.p]]) * 2 > S.total_dis else ' → 这步可以走')),
        'd += dis[x] - dis[f[x][p]]': '走这一步：`d` → {d}',
        'x = f[x][p]': '`x` 跳到 {x}',
        'if (d + dis[y] - dis[f[y][p]]) * 2 <= total_dis': lambda S, B, r: f'走完 `d` = {S.d + S.dis[S.y] - S.dis[S.f[S.y][S.p]]}，×2 = {(S.d + S.dis[S.y] - S.dis[S.f[S.y][S.p]]) * 2}，' + ('<= 总长 → ==可以走==' if (S.d + S.dis[S.y] - S.dis[S.f[S.y][S.p]]) * 2 <= S.total_dis else '> 总长 → 走过头了'),
        'd += dis[y] - dis[f[y][p]]': '走这一步：`d` → {d}',
        'y = f[y][p]': '`y` 跳到 {y}',
        'break': '再走就超过一半：停在 `y`，它==离 x 刚好 ≥ 一半==，就是答案',
        'res.append(x)': '答案 `{x}`：第一个离 x ≥ 一半的点',
        'res.append(y)': '答案 `{y}`',
    },
    cards=dict(
        one_liner='倍增表 f[x] 记下往上走 1、2、4… 步的点，按距离一步步走',
        complexity='时间 `O((n+q) log n)`，空间 `O(n log n)`',
        problem=['无向带权树，根为 0；询问 `(u, v)`：求 u 到 v 路径上第一个“离 u 的边权和 ≥ 路径总权值一半”的点',
                 '示例：`edges=[[0,1,2],[0,2,5],[1,3,1],[2,4,3]]`，询问 `[3,4]` → `2`',
                 '本视频：询问 `[3,4]` 与 `[4,3]`，答案 `[2,0]`'],
        quote='从u开始走时，累加的距离必须大于等于total_dis的一半，但是从v开始走时，累加的距离必须刚好小于total_dis的一半。',
        quote_src='—— yiduobo 题解原文',
        idea=['先倍增求 `lca`，`total_dis = dis[u] + dis[v] − 2·dis[lca]`',
              'u 到 lca 的距离 ×2 ≥ 总长：答案在 u 这边，从 u 往上走到刚好够一半',
              '否则在 v 这边：从 v 往上走，只走==不超过一半==的步，停下的点就是答案'],
        summary=['时间 `O((n+q) log n)`，空间 `O(n log n)`；`f[x][k]` 是 x 往上走 2^k 步的点，长度不一',
                 '==两边的比较符号不同==：从 u 走要 `>=` 一半，从 v 走要 `<=` 一半后停',
                 '大步试不过就换小步 `p -= 1`，每次 d 增加的步长递减，所以一次询问 `O(log n)`',
                 '对比灵神：灵神把“至少”转成“至多 half−1 再多跳一步”，yiduobo 分两边写不同的走法'],
    ),
)
