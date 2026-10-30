import math as _m


def _tgraph(cv, T, box, pos, edges, ncol, nsub, ecol, title, R=30, bottom=62, side=None):
    """通用树/图：pos 为 0..1 的相对坐标；nsub 返回 str 或 [str]（画在节点下方）"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    L, Rr, Tp, Bt = x0 + 80, x1 - 80, y0 + 52 + R + (50 if 'a' in (side or {}).values() else 0), y1 - R - bottom
    P = {u: (L + fx * (Rr - L), Tp + fy * (Bt - Tp)) for u, (fx, fy) in pos.items()}
    for u, v in edges:
        c, wd = ecol(u, v)
        cv.line([P[u], P[v]], c, wd)
    for u, (px, py) in P.items():
        fc = ncol(u)
        cv.d.ellipse((px - R, py - R, px + R, py + R), fill=fc, outline=T['border'], width=2)
        cv.text((px, py), u, 28, T['bg'] if fc != T['panel2'] else T['text'], anchor='mm', bold=True)
        s = nsub(u)
        if s is None:
            continue
        sd = (side or {}).get(u, 'b')
        for k, line in enumerate([s] if isinstance(s, str) else s):
            if sd == 'b':
                cv.text((px, py + R + 4 + k * 23), line, 20, T['yellow'], anchor='mt', bold=True, mono=True)
            elif sd == 'a':
                cv.text((px, py - R - 4 - (len(s) - 1 - k) * 23 if not isinstance(s, str) else py - R - 4), line, 20, T['yellow'], anchor='mb', bold=True, mono=True)
            elif sd == 'r':
                cv.text((px + R + 8, py - R - 4 + k * 23), line, 20, T['yellow'], anchor='lm', bold=True, mono=True)
            else:
                cv.text((px - R - 8, py - R - 4 + k * 23), line, 20, T['yellow'], anchor='rm', bold=True, mono=True)
EDGES = [(0, 1), (1, 2), (1, 3), (4, 2)]
GUESSES = [(1, 3), (0, 1), (1, 0), (2, 4)]
K = 3
POS = {0: (0.05, 0.12), 1: (0.34, 0.12), 2: (0.66, 0.12), 4: (0.95, 0.12), 3: (0.34, 1.0)}
SIDE = {0: 'b', 1: 'a', 2: 'b', 4: 'b', 3: 'b'}


def _parents(root):
    adj = {}
    for a, b in EDGES:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    par, seen, q = {root: None}, {root}, [root]
    for u in q:
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                par[v] = u
                q.append(v)
    return par


def _draw_guess(cv, T, box, root, ncol, nsub, ecol, title):
    x0, y0, x1, y1 = box
    par = _parents(root)
    R = 30
    L, Rr, Tp, Bt = x0 + 80, x1 - 80, y0 + 100 + R, y1 - R - 70
    P = {u: (L + fx * (Rr - L), Tp + fy * (Bt - Tp)) for u, (fx, fy) in POS.items()}
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    for u, v in EDGES:
        c, wd = ecol(u, v)
        cv.line([P[u], P[v]], c, wd)
    for u, v in GUESSES:
        (ax, ay), (bx, by) = P[u], P[v]
        d = _m.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / d, (by - ay) / d
        nx, ny = -uy * 13, ux * 13
        ok = par.get(v) == u
        c = T['green'] if ok else T['red']
        cv.arrow((ax + ux * (R + 6) + nx, ay + uy * (R + 6) + ny), (bx - ux * (R + 8) + nx, by - uy * (R + 8) + ny), c, 4 if ok else 2, 14)
    for u, (px, py) in P.items():
        fc = ncol(u)
        cv.d.ellipse((px - R, py - R, px + R, py + R), fill=fc, outline=T['border'], width=2)
        cv.text((px, py), u, 28, T['bg'] if fc != T['panel2'] else T['text'], anchor='mm', bold=True)
        s = nsub(u)
        if s is not None:
            cv.text((px, py - R - 6), s, 22, T['yellow'], anchor='mb', bold=True, mono=True)
    cv.text((x0 + 18, y1 - 34), f'绿箭头 = 以 {root} 为根时猜对（u 是 v 的父节点），红箭头 = 猜错', 20, T['muted'])
def _ctx(S):
    inn = S['_inner']
    if 'now_hit' in inn:
        return 2, inn
    if 'now' in inn:
        return 1, inn
    return 0, inn


def _draw(cv, S, B, box, T):
    ph, inn = _ctx(S)
    now = inn.get('now') if ph else None
    nxt = inn.get('nxt') if ph else None
    root = now if ph == 2 else 0
    if nxt is not None and now is not None and (min(now, nxt), max(now, nxt)) not in {(min(a, b), max(a, b)) for a, b in EDGES}:
        nxt = None
    q = S.get('q') or []

    def ncol(u):
        if u == now:
            return T['blue']
        if u == nxt and ph:
            return T['yellow']
        vis = S.get('vis') or ()
        return T['cyan'] if u in vis and ph else T['panel2']

    def nsub(u):
        if ph == 2:
            for e in q:
                if e[0] == u:
                    return f'hit={e[1]}'
        if ph == 1 and u == 0:
            return f"hit={S.get('hit')}"
        return None

    def ecol(u, v):
        if ph and now is not None and nxt is not None and {u, v} == {now, nxt}:
            return T['yellow'], 6
        return T['border'], 3

    _draw_guess(cv, T, box, root, ncol, nsub, ecol,
                '树 + 猜测（蓝 = now，黄 = nxt，青 = 已入队）')


def _txt(S):
    ph, inn = _ctx(S)
    if ph == 1:
        return f"第一遍 bfs：以 0 为根数猜对 `hit = {S.get('hit')}`"
    if ph == 2:
        return f"第二遍 bfs：`now = {inn['now']}` 为根时命中 `{inn['now_hit']}` 个，目前 `res = {S.get('res')}`（要 `>= {S['k']}`）"
    return '先数以 0 为根的命中数 `hit`，再用 bfs 把根在父子间传递'


CONFIG = dict(
    num=2581, title='统计可能的树根数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='换根 · 两遍 bfs',
    tags=['灵神题单·动态规划', '难度分 2228'],
    code='''
class Solution(object):
    def rootCount(self, edges, guesses, k):

        n = len(edges) + 1
        g = {index : set() for index in range(n)}
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)
        
        guess_dict = {index : set() for index in range(n)}
        for x, y in guesses:
            guess_dict[x].add(y)
        
        hit = 0

        q = [0]
        head, tail = 0, 1
        vis = set([0])
        while head < tail:
            now = q[head]
            head += 1
            for nxt in g[now]:
                if nxt not in vis:
                    if nxt in guess_dict[now]:
                        hit += 1
                    q.append(nxt)
                    vis.add(nxt)
                    tail += 1
        
        res = 0
        if hit >= k:
            res += 1

        q = [[0, hit]]
        vis = set([0])
        head, tail = 0, 1
        while head < tail:
            now, now_hit = q[head]
            head += 1
            for nxt in g[now]:
                if nxt not in vis:
                    vis.add(nxt)
                    nxt_hit = now_hit
                    if nxt in guess_dict[now]:
                        nxt_hit -= 1
                    if now in guess_dict[nxt]:
                        nxt_hit += 1
                    if nxt_hit >= k:
                        res += 1

                    q.append([nxt, nxt_hit])
                    tail += 1
        
        return res
''',
    call='Solution().rootCount([[0,1],[1,2],[1,3],[4,2]], [[1,3],[0,1],[1,0],[2,4]], 3)',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='queue', var='q', label='q（第二遍里是 [节点, 命中数]）', h=110),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'blue'), ('hit', 'hit', 'cyan'),
           ('now_hit', lambda S: S['_inner'].get('now_hit'), 'yellow'), ('res', lambda S: S.get('res'), 'green')],
    skip=['g[x].add(y)', 'g[y].add(x)', 'for x, y in edges', 'guess_dict[x].add(y)', 'for x, y in guesses',
          'head += 1', 'tail += 1', 'head, tail = 0, 1', 'while head < tail', 'for nxt in g[now]', 'n = len(edges)',
          'g = {index', 'guess_dict = {index', 'q.append(', 'vis.add(nxt)'],
    max_steps=80,
    captions={
        'hit = 0': '`hit`：以 0 为根时，猜对的个数。先建好邻接表 `g` 和猜测表 `guess_dict[x]`（x 猜是父亲的那些 y）',
        'q = [0]': '第一遍 bfs 从 0 出发，`vis` 防止走回头路',
        'now = q[head]': '取出队头 `now = {now}`',
        'if nxt not in vis': lambda S, B, r: (f"`{S['nxt']}` 还没访问 → 它是 `{S['now']}` 的孩子" if S['nxt'] not in S['vis'] else f"`{S['nxt']}` 已访问过 → 跳过"),
        'nxt_hit += 1': '猜测里有 `[{nxt},{now}]`：换根后 `{nxt}` 成了 `{now}` 的父亲 → ==命中 +1== = `{nxt_hit}`',
        'hit += 1': '以 0 为根时 `{now}` 是 `{nxt}` 的父亲，且有猜测 `[{now},{nxt}]` → ==命中== `hit = {hit}`',
        'res = 0': '第一遍结束：以 0 为根命中 `hit = {hit}`',
        'if hit >= k': '`{hit} >= {k}` → 0 本身是否算一个可能的根',
        'vis = set([0])': '`vis` 只含起点 0',
        'res += 1': lambda S, B, r: (f"`{S['nxt']}` 也达标：`res = {S['res']}`" if 'nxt_hit' in S['_inner'] else f"`res = {S['res']}`：0 号点算一个"),
        'q = [[0, hit]]': '第二遍 bfs：队列里带上「以该点为根的命中数」，从 `[0, {hit}]` 开始',
        'now, now_hit = q[head]': '取出 `now = {now}`，以它为根命中 `now_hit = {now_hit}`',
        'nxt_hit = now_hit': '把根从 `{now}` 换成邻居 `{nxt}`：先复制 `{now_hit}`，只有边 `({now},{nxt})` 的猜测会变',
        'nxt_hit -= 1': '猜测里有 `[{now},{nxt}]`：换根后 `{now}` 不再是 `{nxt}` 的父亲 → ==命中 −1== = `{nxt_hit}`',
        'if nxt_hit >= k': lambda S, B, r: f"以 `{S['nxt']}` 为根命中 `{S['nxt_hit']}`，" + (f"`>= {S['k']}` → 计入" if S['nxt_hit'] >= S['k'] else f"`< {S['k']}` → 不计"),
        'return res': '可能的树根一共 `{res}` 个',
    },
    cards=dict(
        one_liner='根从父亲换到孩子，只会改变这一条边上的猜测',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['一棵 `n` 个点的树，Bob 猜了一些「u 是 v 的父亲」',
                 '至少猜对 `k` 个的根，一共有几个？',
                 '示例：`k = 3`，`guesses = [[1,3],[0,1],[1,0],[2,4]]` → `3`'],
        quote='将根节点从p移动到q实际上只会影响(p, q)这一组父子对，若之前以p为根节点时命中的猜测数量为p_hit，那么以q为根节点时命中的猜测数量q_hit只需在p_hit的基础上，增加关于边(p, q)的判断就可以计算得到了。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举根再 bfs 数命中要 `O(n^2)`，太慢',
              '换根时把根从 p 移到相邻的孩子 q',
              '之前 p 是 q 父亲的猜测 `[p,q]` 作废，减 1；`[q,p]` 变对，加 1',
              '第一遍 bfs 求 `hit`，第二遍 bfs 沿父子边传递'],
        summary=['两遍 bfs：时间 `O(n+m)`，空间 `O(n+m)`',
                 '队列里存 `[节点, 命中数]`，用 `vis` 避免走回父亲',
                 '别漏掉根 0 自己：`hit >= k` 要先判一次',
                 '对比灵神：他用 DFS 递归 + 哈希表存 `(x,y)`；这里用 bfs + `guess_dict`',
                 '原文可直接在 Python 3 运行，未改动'],
    ),
)
