def _tree_pos(n, edges, root=0):
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)
    xs, ds, ch, cnt = {}, {}, {}, [0]

    def go(x, fa, d):
        ds[x] = d
        ch[x] = [y for y in g[x] if y != fa]
        for y in ch[x]:
            go(y, x, d + 1)
        if ch[x]:
            xs[x] = (xs[ch[x][0]] + xs[ch[x][-1]]) / 2
        else:
            xs[x] = cnt[0]
            cnt[0] += 1
    go(root, -1, 0)
    return xs, ds, ch, max(cnt[0], 1)


def _draw_tree(cv, box, T, n, edges, node_fn, title='', edge_fn=None, edge_label=None, bot_right=False, txt_size=28):
    """node_fn(i) -> dict(fill=颜色名或None, txt=节点里的字, top=上方小字, bot=下方小字, ring=颜色名或None)"""
    x0, y0, x1, y1 = box
    xs, ds, ch, nl = _tree_pos(n, edges)
    md = max(ds.values())
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    gx0, gx1 = x0 + 70, x1 - 70
    gy0, gy1 = y0 + 84, y1 - 52
    step = (gx1 - gx0) / max(nl - 1, 1) if nl > 1 else 0
    step = min(step, 150)
    ox = (x0 + x1) / 2 - step * (nl - 1) / 2
    ly = (gy1 - gy0) / max(md, 1)
    ly = min(ly, 140)
    P = {i: (ox + xs[i] * step, gy0 + ds[i] * ly) for i in range(n)}
    for p in range(n):
        for c in ch[p]:
            col = edge_fn(p, c) if edge_fn else None
            cv.line([P[p], P[c]], T[col] if col else T['border'], 6 if col else 3)
            lab = edge_label(p, c) if edge_label else None
            if lab is not None:
                mx, my = (P[p][0] + P[c][0]) / 2, (P[p][1] + P[c][1]) / 2
                right = P[c][0] >= P[p][0]
                cv.text((mx + (10 if right else -10), my), lab, 22, T[col] if col else T['cyan'], anchor='lm' if right else 'rm', bold=True, mono=True)
    R = 27
    for i in range(n):
        X, Y = P[i]
        d = node_fn(i)
        f = d.get('fill')
        ring = d.get('ring')
        if ring:
            cv.d.ellipse((X - R - 6, Y - R - 6, X + R + 6, Y + R + 6), outline=T[ring], width=4)
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=T[f] if f else T['panel2'],
                     outline=T[f] if f else T['muted'], width=2)
        cv.text((X, Y), d.get('txt', i), txt_size, T['dim'] if d.get('dim') else (T['bg'] if f else T['text']), anchor='mm', bold=True)
        if not edge_label:
            cv.text((X - R - 10, Y - R - 4), i, 18, T['dim'], anchor='rb', mono=True)
        if d.get('top'):
            cv.text((X, Y - R - 10), d['top'], 20, T['cyan'], anchor='mb', bold=True)
        if d.get('bot'):
            if bot_right:
                cv.text((X + R + 12, Y), d['bot'], 22, T[d.get('botc', 'green')], anchor='lm', bold=True)
            else:
                cv.text((X, Y + R + 8), d['bot'], 22, T[d.get('botc', 'green')], anchor='mt', bold=True)


N = 7
EDGES = [[0, 1], [1, 2], [2, 3], [3, 4], [3, 5], [1, 6]]
_xs, _ds, _ch, _nl = _tree_pos(N, EDGES)


def _ints(v):
    return [int(c) for c in v] if isinstance(v, str) else list(v)


def _draw(cv, S, B, box, T):
    if 'd' not in S:
        st, tg, d, res = _ints('0011000'), _ints('0010001'), [1, 3, 2, 3, 1, 1, 1], []
        live = False
    else:
        st, tg, d, res = _ints(S['start']), _ints(S['target']), S['d'], S.get('res', [])
        live = True
    inner = S.get('_inner', {})
    x = S.get('x') if live and S.get('_line', 0) >= 24 and 'head' in S and inner.get('x') is not None else None
    y = inner.get('y') if x is not None else None

    def f(i):
        d_ = dict(txt=f'{st[i]}→{tg[i]}')
        gone = live and d[i] == 0
        if st[i] != tg[i] and not gone:
            d_['fill'] = 'pink'
        if gone:
            d_['dim'] = True
        if i == x:
            d_['ring'] = 'yellow'
        elif i == y:
            d_['ring'] = 'blue'
        if live and not gone:
            d_['bot'] = f'度{d[i]}'
            d_['botc'] = 'cyan' if d[i] == 1 else 'muted'
        return d_

    def e(p, c):
        k = _EIDX[(p, c)]
        if k in res:
            return 'orange'
        if live and (d[p] == 0 or d[c] == 0):
            return 'dim'
        return None

    _draw_tree(cv, box, T, N, EDGES, f, edge_fn=e, edge_label=lambda p, c: str(_EIDX[(p, c)]), bot_right=True, txt_size=22,
               title='树（粉 = 色不一致；度 = 剩余度数；橙线 = 翻转的边；暗 = 已摘掉）')


_EIDX = {}
for _i, (_a, _b) in enumerate(EDGES):
    _EIDX[(_a, _b)] = _i
    _EIDX[(_b, _a)] = _i


CONFIG = dict(
    num=3812, title='翻转树上最少边', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='拓扑排序式剥叶子',
    tags=['灵神题单', '链表树与回溯', '难度分 2179'],
    code='''
class Solution(object):
    def minimumFlips(self, n, edges, start, target):
        
        start = [int(x) for x in start]
        target = [int(x) for x in target]

        g = [[] for _ in range(n)]
        d = [0] * n

        for index, (x, y) in enumerate(edges):
            g[x].append((y, index))
            g[y].append((x, index))
            d[x] += 1
            d[y] += 1
        
        q = []
        for x in range(n):
            if d[x] == 1:
                q.append(x)
        
        head, tail = 0, len(q)
        res = []
        for _ in range(n - 2):
            x = q[head]
            head += 1
            d[x] -= 1
            for y, index in g[x]:
                if d[y] > 1:
                    d[y] -= 1
                    if start[x] != target[x]:
                        res.append(index)
                        start[y] ^= 1
                    if d[y] == 1:
                        q.append(y)
        
        x = q[head]
        for y, index in g[x]:
            if d[y] == 1:
                if (start[x] == target[x] and start[y] != target[y]) or (start[x] != target[x] and start[y] == target[y]):
                    return [-1]
                if start[x] != target[x]:
                    res.append(index)
                break
        
        return sorted(res)
''',
    call="Solution().minimumFlips(7, [[0,1],[1,2],[2,3],[3,4],[3,5],[1,6]], '0011000', '0010001')",
    expect=[1, 2, 5],
    views=[
        dict(type='custom', draw=_draw, h=430),
        dict(type='array', var='q', label='q：待剥的叶子队列（蓝箭头 = head）', cell=60, h=140, pointers={'head': 'blue'}),
        dict(type='array', var='res', label='res：已决定翻转的边下标', cell=60, h=140),
    ],
    watch=[('x', 'x', 'yellow'), ('head', 'head', 'blue'), ('res', 'res', 'orange')],
    skip=['g[x].append', 'g[y].append', 'd[x] += 1', 'd[y] += 1', 'for index, (x, y) in enumerate', 'for x in range(n)', 'q.append(x)', 'for _ in range(n - 2)',
          'target = [int', 'if d[x] == 1'],
    max_steps=110,
    captions={
        'start = [int': '把字符串转成 0/1 列表（后面要对 `start[y]` 做异或翻转）',
        'g = [[]': '邻接表 `g[x]` 存 `(邻居, 边下标)`',
        'd = [0]': '`d[x]` 记录节点 x 当前的度数',
        'q = []': '`q` 存所有叶子（度为 1 的节点），类似拓扑排序的初始队列',
        'head, tail': '遍历完毕：叶子 `q = {q}` 已入队，`head = 0` 指向队头',
        'res = []': '`res` 收集要翻转的边下标',
        24: '取出队头叶子 `x = {x}`（它只连着一条未删除的边）',
        36: '循环结束，树只剩两个节点：`x = {x}` 和它唯一未删除的邻居',
        'head += 1': '队头指针后移，`head = {head}`',
        'd[x] -= 1': '把叶子 `{x}` 从树上摘掉：`d[{x}]` 变成 `{d[x]}`，它那条边的另一端要 -1',
        'for y, index in g[x]': lambda S, B, r: (f'看邻居 `y = {S.y}`，边下标 `index = {S.index}`' if (S.y, S.index) != (B.y, B.index) or 'y' not in B['_inner'] else '邻居看完，回到外层循环'),
        'if d[y] > 1': lambda S, B, r: (f'`d[{S.y}] = {B.d[S.y]} > 1` → `{S.y}` 还在树上，这条边是叶子 {S.x} 唯一的边' if B.d[S.y] > 1
                                        else f'`d[{S.y}] = {B.d[S.y]}` 不大于 1 → `{S.y}` 已被摘掉（这是已删除的边），跳过'),
        'd[y] -= 1': '边已确定、被删除：`d[{y}]` 减一 → {d[y]}',
        30: lambda S, B, r: (f'`start[{S.x}] = {S.start[S.x]}` ≠ `target[{S.x}] = {S.target[S.x]}` → 叶子颜色不对，==这条边必须翻==' if S.start[S.x] != S.target[S.x]
                                                     else f'`start[{S.x}] = target[{S.x}] = {S.start[S.x]}` → 叶子颜色已对，==这条边不能翻=='),
        'res.append(index)': '记下要翻的边 `{index}`：`res = {res}`',
        'start[y] ^= 1': '翻边会同时翻转另一端：`start[{y}]` 异或 1 → {start[y]}',
        33: lambda S, B, r: (f'`d[{S.y}] = 1` → `{S.y}` 也变成叶子，加入队列' if S.d[S.y] == 1 else f'`d[{S.y}] = {S.d[S.y]}` 还不是叶子'),
        38: lambda S, B, r: (f'`d[{S.y}] = {S.d[S.y]}`：它就是剩下的另一个节点，两点一边' if S.d[S.y] == 1 else f'`d[{S.y}] = {S.d[S.y]}`：已被摘掉的节点，跳过'),
        39: lambda S, B, r: (f'剩下的边 {S.x}-{S.y}：翻一次两端同时变；`x` {"对" if S.start[S.x] == S.target[S.x] else "错"}、`y` {"对" if S.start[S.y] == S.target[S.y] else "错"}'
                              + (' → 一对一错，翻不平 → ==无解==' if (S.start[S.x] == S.target[S.x]) != (S.start[S.y] == S.target[S.y]) else ' → 同对同错，有解')),
        41: lambda S, B, r: ('两端都不对 → ==翻这条边==' if S.start[S.x] != S.target[S.x] else '两端都对 → ==不翻=='),
        'break': '只剩这一条边，处理完退出',
        'q.append(y)': '`{y}` 入队：`q = {q}`',
        'return [-1]': '剩下两个点、一条边：翻一次会同时改两端，但两端对错不一致 → 无解 `[-1]`',
        'return sorted': '边下标升序：返回 `{ret}`',
    },
    cards=dict(
        one_liner='一次摘一个叶子：它颜色对不对，唯一的边就翻不翻',
        complexity='时间 `O(n log n)`（排序），空间 `O(n)`',
        problem=['无向树，每个节点有颜色 `start[x]`，目标 `target[x]`（0/1）',
                 '一次操作选一条边，两个端点颜色一起翻转',
                 '求最少操作的边下标（升序）；做不到返回 `[-1]`',
                 '示例 2：`start=0011000`，`target=0010001` → `[1,2,5]`'],
        quote='对于任意一个度为1的节点，其对应的start和target相同，那么与连接该节点的唯一一条边就不能被标记，反之则必须被标记。……这个过程与拓扑排序很相似。',
        quote_src='—— yiduobo 题解原文',
        idea=['树至少有两个度为 1 的节点（度数和 `2(n-1)` 推出）',
              '每摘一个叶子，它的边就定下来；翻边时把另一端的 `start` 也异或 1',
              '像拓扑排序：另一端度数降到 1 就入队，共摘 `n-2` 个，最后剩一条边单独判断'],
        summary=['时间 `O(n)` 建图 + 剥叶子，排序 `O(n log n)`；空间 `O(n)`',
                 '循环只做 `n - 2` 次，剩下两个节点、一条边用最后一段单独判断',
                 '`if d[y] > 1` 用来区分「还在树上」和「已被摘掉」的邻居',
                 '对比灵神：灵神用 DFS 在回溯时判断，不需要显式维护度数和队列']),
)
