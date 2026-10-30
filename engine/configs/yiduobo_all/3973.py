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
    gx = min(gx, 230)
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
    def distinctPaths(self, n, parent, gates, queries):
        
        g = [[] for _ in range(n)]
        for u, p in enumerate(parent):
            if p != -1:
                g[p].append(u)
        
        q = [0]
        level = [0] * n
        head, tail = 0, 1
        while head < tail:
            for u in q[head : tail]:
                for v in g[u]:
                    level[v] = level[u] + 1
                    q.append(v)
            head, tail = tail, len(q)

        ma_p = 0
        x = 1
        while x <= level[q[-1]]:
            x += x
            ma_p += 1

        anc = [[-1] * ma_p for _ in range(n)]
        f = [[[0] * 4 for _ in range(ma_p)] for _ in range(n)]
        
        mod = 10 ** 9 + 7
        for p in range(ma_p):
            for u in range(n):
                if p == 0:
                    anc[u][p] = parent[u]
                    update = True
                    if parent[u] != -1:
                        for state in range(4):
                            start = (state >> 1) & 1
                            end = state & 1
                            if start == end:
                                f[u][0][state] = gates[u][1 - start]
                            else:
                                f[u][0][state] = gates[u][-1]
                else:
                    v = anc[u][p - 1]
                    if v != -1 and anc[v][p - 1] != -1:
                        anc[u][p] = anc[v][p - 1]
                        for state in range(4):
                            start = (state >> 1) & 1
                            end = state & 1
                            f[u][p][state] = (f[u][p - 1][start << 1] * f[v][p - 1][end] % mod + f[u][p - 1][(start << 1) | 1] * f[v][p - 1][2 | end] % mod) % mod

            p += 1

        res = 0
        mod = 10 ** 9 + 7
        for u, color_u, v, color_v in queries:
            u_red = color_u
            u_blue = 1 - color_u

            v_red = color_v
            v_blue = 1 - color_v
            
            p = ma_p - 1
            while level[u] > level[v]:
                while p > 0 and (anc[u][p] == -1 or level[anc[u][p]] < level[v]):
                    p -= 1

                nxt_u = anc[u][p]
                u_red, u_blue = (u_red * f[u][p][3] % mod + u_blue * f[u][p][1] % mod) % mod, (u_red * f[u][p][2] % mod + u_blue * f[u][p][0] % mod) % mod
                u = nxt_u
            
            p = ma_p - 1
            while level[v] > level[u]:
                while p > 0 and (anc[v][p] == -1 or level[anc[v][p]] < level[u]):
                    p -= 1
                nxt_v = anc[v][p]
                v_red, v_blue = (v_red * f[v][p][3] % mod + v_blue * f[v][p][1] % mod) % mod, (v_red * f[v][p][2] % mod + v_blue * f[v][p][0] % mod) % mod
                v = nxt_v

            p = ma_p - 1
            while u != v:
                while p > 0 and anc[u][p] == anc[v][p]:
                    p -= 1
                nxt_u = anc[u][p]
                u_red, u_blue = (u_red * f[u][p][3] % mod + u_blue * f[u][p][1] % mod) % mod, (u_red * f[u][p][2] % mod + u_blue * f[u][p][0] % mod) % mod
                u = nxt_u
                nxt_v = anc[v][p]
                v_red, v_blue = (v_red * f[v][p][3] % mod + v_blue * f[v][p][1] % mod) % mod, (v_red * f[v][p][2] % mod + v_blue * f[v][p][0] % mod) % mod
                v = nxt_v

            res ^= (u_red + u_blue) * (v_red + v_blue) % mod

        return res
'''
LINE_TXT = {i: l for i, l in enumerate(CODE.strip('\n').split('\n'), 1)}
def _ln(sub, nth=0):
    r = [i for i, l in LINE_TXT.items() if sub in l]
    return r[nth] if r else 10 ** 6


L_Q = _ln('for u, color_u, v, color_v in queries')

N = 4
PARENT = [-1, 0, 0, 1]
GATES = [[1, 1, 1], [2, 1, 1], [1, 2, 1], [1, 1, 2]]
EDGES = [[p, u] for u, p in enumerate(PARENT) if p != -1]
CH = _children(N, EDGES)

SN = ['蓝→蓝', '蓝→红', '红→蓝', '红→红']


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    ln = S.get('_line', 0)
    r = {}
    inq = ln >= L_Q and 'u' in S and 'v' in S and 'u_red' in S
    if inq:
        r[S['u']], r[S['v']] = 'blue', 'pink'
        if S['u'] == S['v']:
            r[S['u']] = 'yellow'
    elif 'u' in S and 'p' in S and ln >= _ln('for p in range(ma_p)') and ln < L_Q:
        r[S['u']] = 'yellow'
    lv = S.get('level')
    mid = y0 + (y1 - y0) * 0.45
    _draw_tree(cv, (x0, y0, x1, mid), T, CH, EDGES, lambda u: r.get(u),
               under_fn=lambda u: (f'层{lv[u]} ' if lv and (lv[u] or u == 0) else '') + f'{GATES[u][0]}·{GATES[u][1]}·{GATES[u][2]}',
               title='树（节点旁：层数 红门·蓝门·白门 的数量；蓝 = alice，粉 = bob）', rad=22)
    anc, f = S.get('anc'), S.get('f')
    if not anc or not f:
        return
    mp = len(anc[0])
    cv.text((x0 + 18, mid + 4), 'anc[u][p]：往上 2^p 步到哪；f[u][p][起点卡→终点卡]：方案数', 22, T['muted'], bold=True)
    ys = mid + 44
    cw = 56
    blk = 70 + cw * 4 + 24
    cur_u, cur_p, cur_s = (S.get('u'), S.get('p'), S.get('state')) if not inq and ln >= _ln('for p in range(ma_p)') else (None, None, None)
    for p in range(mp):
        bx = x0 + 60 + p * blk
        cv.text((bx, ys), f'p = {p}（2^{p} 步）', 20, T['cyan'], bold=True)
        cv.text((bx + 60, ys + 44), 'anc', 17, T['dim'], anchor='mm')
        for s in range(4):
            cv.text((bx + 70 + cw * s + cw / 2, ys + 44), SN[s], 16, T['dim'], anchor='mm')
    rh = (y1 - ys - 72) / max(len(anc), 1)
    rh = min(rh, 46)
    for u in range(len(anc)):
        Y = ys + 72 + u * rh
        cv.text((x0 + 20, Y + rh / 2), f'u={u}', 20, T['yellow'] if u == cur_u else T['text'], anchor='lm', bold=True)
        for p in range(mp):
            bx = x0 + 60 + p * blk
            a = anc[u][p]
            hot = u == cur_u and p == cur_p
            cv.rect((bx + 40, Y + 2, bx + 80, Y + rh - 2), fill=T['panel2'], outline=T['yellow'] if hot else T['border'], r=6, width=3 if hot else 1)
            cv.text((bx + 60, Y + rh / 2), a, 20, T['text'] if a != -1 else T['dim'], anchor='mm', bold=True)
            for s in range(4):
                v = f[u][p][s]
                h2 = hot and s == cur_s
                cv.rect((bx + 90 + cw * s, Y + 2, bx + 90 + cw * s + cw - 4, Y + rh - 2), fill=T['yellow'] if h2 else T['panel2'], outline=T['border'], r=6)
                cv.text((bx + 90 + cw * s + cw / 2 - 2, Y + rh / 2), v, 20, T['bg'] if h2 else (T['text'] if v else T['dim']), anchor='mm', bold=True)


def _cap_if(S, B, ret):
    u = S.u
    return f'`state = {S.state}`（{SN[S.state]}）同色 → 只能走 {u} 号点上这种颜色的门：`gates[{u}][1 − {S.start}] = {S.f[u][0][S.state]}`（红蓝下标与卡色编码相反）'


def _cap_cond(S, B, ret):
    u, p = S.u, S.p
    if S.v == -1:
        return f'`v = anc[{u}][{p-1}] = -1`：走不到 → `anc[{u}][{p}]`、`f` 都没有意义'
    if S.anc[S.v][p - 1] == -1:
        return f'`anc[{S.v}][{p-1}] = -1`：再走 2^{p-1} 步就出树了 → 跳过'
    return f'`v = {S.v}`，再走 2^{p-1} 步到 `{S.anc[S.v][p-1]}` → 有效，开始合并'


def _while_cap(S, B, ret):
    return None


CONFIG = dict(
    num=3973, title='通往最近公共祖先的不同门径', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='树上倍增 + 门卡方案数',
    tags=['会员题'],
    code=CODE,
    call='Solution().distinctPaths(4, [-1,0,0,1], [[1,1,1],[2,1,1],[1,2,1],[1,1,2]], [[3,1,2,0]])',
    expect=21,
    views=[
        dict(type='custom', draw=_draw, h=600),
    ],
    watch=[('u', 'u', 'blue'), ('v', 'v', 'pink'), 'p', 'u_red', 'u_blue', 'v_red', 'v_blue', ('res', 'res', 'green')],
    skip=['g = [[] for', 'for u, p in enumerate(parent)', 'if p != -1:', 'g[p].append', 'q = [0]', 'level = [0]', 'head, tail = 0, 1',
          'while head < tail', 'for u in q[head', 'for v in g[u]', 'q.append(v)', 'head, tail = tail', 'ma_p = 0', 'x = 1', 'while x <= level',
          'x += x', 'ma_p += 1', 'f = [[[0]', 'mod = 10', 'for u in range(n)', 'if p == 0', 'update = True', 'if parent[u] != -1', 'for state in range(4)',
          'start = (state', 'end = state & 1', 'if start == end', 'else:', 'p += 1', 'res = 0', 'v_red = color_v', 'v_blue = 1 - color_v',
          'nxt_u = anc[u][p]', 'nxt_v = anc[v][p]', 'for p in range(ma_p)', 'p = ma_p - 1', 'if v != -1 and anc[v][p - 1] != -1', 'u = nxt_u', 'v = nxt_v', 'p -= 1', 'f[u][p][state] = (', 'while level[v] > level[u]'],
    max_steps=100,
    captions={
        'level[v] = level[u] + 1': '`level[{v}] = level[{u}] + 1 = {level[v]}`：BFS 按层求深度',
        'anc = [[-1]': '最大深度是 {level[q[-1]]}，倍增表需要 `ma_p = {ma_p}` 层：`anc[u][p]` = 往上 2^p 步，`f[u][p][state]` = 方案数',
        'anc[u][p] = parent[u]': '`anc[{u}][0] = parent[{u}] = {parent[u]}`：一步就是父亲',
        'f[u][0][state] = gates[u][1 - start]': _cap_if,
        'f[u][0][state] = gates[u][-1]': lambda S, B, r: f'`state = {S.state}`（{SN[S.state]}）颜色变了 → 只能走白门（走完翻色）：`f[{S.u}][0][{S.state}] = gates[{S.u}][-1] = {S.f[S.u][0][S.state]}`',
        'v = anc[u][p - 1]': lambda S, B, r: f'`v = anc[{S.u}][{S.p - 1}] = {S.v}`：先走 2^{S.p - 1} 步到 v；' + ('v 不存在 → 这一层不用算' if S.v == -1 else (f'再走 2^{S.p - 1} 步 `anc[{S.v}][{S.p - 1}] = -1` 出树 → 这一层不用算' if S.anc[S.v][S.p - 1] == -1 else f'再走 2^{S.p - 1} 步到 `{S.anc[S.v][S.p - 1]}` → 有效')),
        'anc[u][p] = anc[v][p - 1]': '`anc[{u}][{p}] = anc[{v}][{p-1}] = {anc[u][p]}`：再从 v 走 2^{p-1} 步；并用 f 把“经过 v 时持蓝卡 / 持红卡”两种方案相加，填好 `f[{u}][{p}]`',
        'f[u][p][state] = (': '`f[{u}][{p}][{state}]` = 经过 v 时持==蓝卡==的方案 + 持==红卡==的方案 = {f[u][p][state]}',
        'for u, color_u, v, color_v in queries': lambda S, B, r: ('询问都处理完了' if ('u_red' in B and B.u == S.u) else f'询问：alice 从 `{S.u}` 出发持卡 `{S.color_u}`（1 = 红），bob 从 `{S.v}` 出发持卡 `{S.color_v}`'),
        'u_red = color_u': '初始方案数：红卡 → `u_red = 1`',
        'u_blue = 1 - color_u': '`u_red = {u_red}`，`u_blue = {u_blue}`：开始只有一种持卡；bob 同理（持蓝：`v_blue = 1`）',
                'while level[u] > level[v]': lambda S, B, r: (f'`level[{S.u}] = {S.level[S.u]}` > `level[{S.v}] = {S.level[S.v]}`：先把深的 alice 拉到和 bob 同一层' if S.level[S.u] > S.level[S.v] else (f'`level[{S.v}] > level[{S.u}]`：先把深的 bob 往上拉' if False else f'`level[{S.u}] = {S.level[S.u]}` 不比 `level[{S.v}]` 深 → 这一步不用再拉')),
        'while level[v] > level[u]': lambda S, B, r: (f'`level[{S.v}] = {S.level[S.v]}` > `level[{S.u}] = {S.level[S.u]}`：bob 更深，往上拉' if S.level[S.v] > S.level[S.u] else f'两人同层（`level = {S.level[S.u]}`）→ 不用再拉'),
        'while p > 0 and (anc[u][p] == -1': lambda S, B, r: (f'`p = 0`，最小的一步' if S.p == 0 else (f'走 2^{S.p} 步会到 `{S.anc[S.u][S.p]}`，比 bob 的层还浅（或出树）→ 缩小 p（`p -= 1`）' if (S.anc[S.u][S.p] == -1 or S.level[S.anc[S.u][S.p]] < S.level[S.v]) else f'走 2^{S.p} 步到 `{S.anc[S.u][S.p]}`，不会越过 bob 的层 → 可以走')),
        'u_red, u_blue = (u_red * f[u][p][3]': '走 2^{p} 步：alice 到 `{anc[u][p]}`，新 `u_red = {u_red}`，`u_blue = {u_blue}`（按 f[u][p] 合并两种持卡的方案数）',
        'v_red, v_blue = (v_red * f[v][p][3]': '同样走 2^{p} 步：bob 到 `{anc[v][p]}`，新 `v_red = {v_red}`，`v_blue = {v_blue}`',
        'while u != v': lambda S, B, r: (f'`u = {S.u}` != `v = {S.v}`：还没相遇 → 两人一起往上跳' if S.u != S.v else f'`u = v = {S.u}`：相遇在最近公共祖先 ==LCA=='),
        'while p > 0 and anc[u][p] == anc[v][p]': lambda S, B, r: (f'`p = 0`，一步一步走' if S.p == 0 else (f'2^{S.p} 级祖先相同（{S.anc[S.u][S.p]}）：一次跳到会==越过 LCA== → 缩小 p（`p -= 1`）' if S.anc[S.u][S.p] == S.anc[S.v][S.p] else f'2^{S.p} 级祖先不同 → 可以一起跳')),
        'res ^= ': '`({u_red} + {u_blue}) × ({v_red} + {v_blue}) = {res}`：两人独立，乘法原理；所有询问的结果异或',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='树上倍增：anc 记祖先，f 记走 2^p 步后各种持卡颜色的方案数',
        complexity='预处理 `O(n log n)`，每次询问 `O(log n)`',
        problem=['有根树，每个点有红、蓝、白三种门若干扇：红门只让红卡过，蓝门只让蓝卡过，白门任意卡都能过但过后卡要翻色',
                 'alice、bob 各从一个点出发，持红或蓝卡，各自沿父亲往上走到最近公共祖先；同色多扇门算不同方案',
                 '本视频：4 个点，询问 alice 在 3 持红卡，bob 在 2 持蓝卡，方案数 = 7 × 3 = `21`'],
        quote='令f[u][p][state]表示u往上走2^p步，且其实的卡牌颜色和到达终点时的卡牌颜色的组合为state时的合法方案数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`anc[u][p]` 是 u 往上 2^p 步的点，`f[u][p][state]`：起点卡色、终点卡色（两位二进制）对应的方案数',
              '`p = 0`：同色只能走本色门，异色只能走白门；`p > 0`：枚举经过中间点 v 时持红还是持蓝，把两段方案数相乘再相加',
              '询问时先把较深的一方拉到同一层，再一起往上跳到 LCA，沿途不断把“红/蓝”方案数向前推，最后两人相乘'],
        summary=['预处理 `O(n log n)`，每次询问 `O(log n)`；方案数都要对 `10^9+7` 取模',
                 '==gates[u] 的下标 0 是红、1 是蓝==，而卡牌编码 0 = 蓝、1 = 红，所以同色时用 `gates[u][1 - start]`',
                 '一起往上跳时 `p` 要缩到两人的 2^p 级祖先不同，才不会跳过 LCA',
                 '最终答案是所有询问结果的按位异或',
                 '原文为 Python 2 风格，但无需改动即可在 Python 3 运行'],
    ),
)
