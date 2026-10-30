import math

N0 = 8
CRY = [0]
FF = [0, 2, 3, 4, 5, 6, 7]
FT = [1, 3, 4, 2, 3, 7, 6]
POS = {0: (.12, .17), 1: (.40, .17), 2: (.14, .55), 3: (.48, .55), 4: (.31, .86), 5: (.82, .55), 6: (.66, .17), 7: (.92, .17)}
SCC_COL = ['blue', 'green', 'purple', 'cyan', 'pink', 'orange', 'yellow', 'red']
_CODE_LINES = None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = N0
    inner = S.get('_inner', {})
    u, vv = inner.get('u'), inner.get('v')
    line = S.get('_line')
    cv.text((x0 + 18, y0 + 4), '有向图（◆ = 有水晶；节点下方 dfn/low；同色 = 同一个强连通分量）', 21, T['muted'], bold=True)
    px = lambda p: (x0 + 40 + p[0] * (x1 - x0 - 80), y0 + 80 + p[1] * (y1 - y0 - 160))
    belong = S.get('belong') or [-1] * n
    dfn = S.get('dfn') or [0] * n
    low = S.get('low') or [0] * n
    ins = S.get('in_stack') or [False] * n
    R = 28
    for a, b in zip(FF, FT):
        (ax, ay), (bx, by) = px(POS[a]), px(POS[b])
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        ox, oy = -uy * 8, ux * 8
        col = (80, 90, 104)
        wd = 3
        if belong[a] != -1 and belong[a] == belong[b]:
            col = T[SCC_COL[belong[a] % 8]]
        if a == u and b == vv:
            col, wd = T['yellow'], 6
        cv.arrow((ax + ux * (R + 2) + ox, ay + uy * (R + 2) + oy), (bx - ux * (R + 4) + ox, by - uy * (R + 4) + oy), col, wd, 14)
    cnt_need = []
    if 'ind' in S and 'ctrstals_set' in S and 'x' in S:
        cand = [c for c in range(len(S['ind'])) if c not in S['ctrstals_set'] and S['ind'][c] == 0]
        cnt_need = [c for c in cand if c < S['x'] or (c == S['x'] and S.get('res', 0) > B.get('res', 0))]
    final = 'ind' in S
    for i in range(n):
        X, Y = px(POS[i])
        b = belong[i]
        fill = T['panel2']
        if b != -1:
            c = T[SCC_COL[b % 8]]
            fill = tuple(int(0.35 * k + 0.65 * q) for k, q in zip(c, T['panel2']))
        out = T['border']
        wd = 2
        if ins[i]:
            out, wd = T['orange'], 4
        if i == u:
            out, wd = T['pink'], 6
        if final and S.get('x') is not None and b == S['x'] and S.get('_line') is not None:
            out, wd = T['pink'], 6
        if b in cnt_need:
            out, wd = T['red'], 6
        cv.rect((X - R, Y - R, X + R, Y + R), fill=fill, outline=out, width=wd, r=R)
        cv.text((X, Y), i, 26, T['text'], anchor='mm', bold=True)
        if i in CRY:
            cv.text((X, Y - R - 4), '◆ 水晶', 19, T['yellow'], anchor='mb', bold=True)
        if dfn[i]:
            cv.text((X, Y + R + 4), f'{dfn[i]}/{low[i]}', 20, T['cyan'], anchor='mt', bold=True, mono=True)
        if final and b != -1 and 'ind' in S:
            cv.text((X, Y + R + 28), f"入度 {S['ind'][b]}", 19, T['orange'], anchor='mt', bold=True)
        if b in cnt_need:
            cv.text((X, Y - R - 4 - (24 if i in CRY else 0)), '+1', 24, T['red'], anchor='mb', bold=True)
    if S.get('stack') is not None:
        st = S['stack']
        cv.text((x0 + 18, y1 - 44), 'stack：' + (' '.join(map(str, st)) if st else '（空）'), 24, T['orange'], bold=True)


def _msg(S):
    if 'ind' in S:
        return '缩点后：==入度为 0 且没有水晶==的分量，必须新连一条边'
    if 'belong' in S:
        return 'Tarjan：`dfn` = 访问次序，`low` = 能回到的最早次序；==low == dfn== 就是一个强连通分量的根'
    return '有向图：要让每个点有水晶，或能被带水晶的点走到'


def _ifv(S, B, ret):
    u, v = S.u, S.v
    if S.dfn[v] == 0:
        return f'边 `{u}→{v}`：`{v}` ==没访问过== → 作为树边递归进去'
    if S.in_stack[v]:
        return f'边 `{u}→{v}`：`{v}` 已访问且 ==还在栈里==（同一个环/分量）→ 用 `dfn[{v}] = {S.dfn[v]}` 更新 `low[{u}]`'
    return f'边 `{u}→{v}`：`{v}` 已访问但 ==已出栈==（属于别的分量）→ 忽略'


def _root(S, B, ret):
    u = S.u
    if S.low[u] == S.dfn[u]:
        return f'`low[{u}] = dfn[{u}] = {S.dfn[u]}`：回不到更早的点 → `{u}` 是==分量的根==，栈里它之上的点同属一个 SCC'
    return f'`low[{u}] = {S.low[u]} < dfn[{u}] = {S.dfn[u]}`：能回到更早的点 → `{u}` 不是根，留在栈里'


def _tot(S, B, ret):
    k = max(S.belong)
    members = [i for i in range(S.n) if S.belong[i] == k]
    return f'弹出完毕：分量 `#{k}` = =={members}==，已有 {k + 1} 个分量'


def _fin(S, B, ret):
    x = S.x
    mem = [i for i in range(S.n) if S.belong[i] == x]
    if x in S.ctrstals_set:
        return f'分量 `#{x}` {mem}：本身有水晶 → 不用加边'
    if S.ind[x] == 0:
        return f'分量 `#{x}` {mem}：==没水晶且入度 0==，没人能把魔力送来 → 需要一条新边'
    return f'分量 `#{x}` {mem}：入度 `{S.ind[x]}`，会被别的分量走到 → 不用加边'


CONFIG = dict(
    num=3383, title='施法所需最低符文数量', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='Tarjan 强连通分量缩点 · 统计入度为 0',
    tags=[],
    code='''
class Solution(object):
    def minRunesToAdd(self, n, crystals, flowFrom, flowTo):
        
        g = [[] for _ in range(n)]
        for x, y in zip(flowFrom, flowTo):
            g[x].append(y)
        
        global t, tot
        t = 0
        tot = 0
        low = [0] * n
        dfn = [0] * n
        stack = []
        in_stack = [False] * n
        belong = [-1] * n

        def tarjan(u):
            global t, tot
            t += 1
            low[u] = t
            dfn[u] = t
            stack.append(u)
            in_stack[u] = True

            for v in g[u]:
                if dfn[v] == 0:
                    tarjan(v)
                    low[u] = min(low[u], low[v])
                elif in_stack[v]:
                    low[u] = min(low[u], dfn[v])
            
            if low[u] == dfn[u]:
                v = -1
                while v != u:
                    v = stack.pop()
                    belong[v] = tot
                    in_stack[v] = False
                tot += 1
        
        for x in range(n):
            if dfn[x] == 0:
                tarjan(x)
        
        new_g = [set() for _ in range(tot)]
        ind = [0] * tot
        for x, y in zip(flowFrom, flowTo):
            if belong[x] != belong[y] and belong[y] not in new_g[belong[x]]:
                new_g[belong[x]].add(belong[y])
                ind[belong[y]] += 1

        ctrstals_set = set()
        for x in crystals:
            ctrstals_set.add(belong[x])

        res = 0
        for x in range(tot):
            if x not in ctrstals_set and ind[x] == 0:
                res += 1

        return res
''',
    call=f'Solution().minRunesToAdd({N0}, {CRY}, {FF}, {FT})',
    expect=2,
    views=[
        dict(type='text', fn=_msg, size=24, h=60),
        dict(type='custom', draw=_draw, h=600),
    ],
    watch=[('t', 't', 'cyan'), ('tot', 'tot', 'green'), ('u', lambda S: S['_inner'].get('u'), 'pink'), ('res', 'res', 'yellow')],
    skip=['g = [[] for', 'for x, y in zip(flowFrom, flowTo):\n', 'g[x].append(y)', 'global t, tot', 't = 0', 'tot = 0', 'low = [0]', 'dfn = [0]',
          'stack = []', 'in_stack = [False]', 'belong = [-1]', '            t += 1', 'low[u] = t', 'dfn[u] = t', 'stack.append(u)', 'for v in g[u]',
          '                    tarjan(v)', 'elif in_stack[v]', 'v = -1', 'while v != u', 'v = stack.pop()', 'belong[v] = tot', 'in_stack[v] = False',
          'for x in range(n)', 'for x in range(tot)', 'if dfn[x] == 0', 'tarjan(x)', 'new_g = [set()', 'for x, y in zip(flowFrom, flowTo)', 'if belong[x] != belong[y]',
          'new_g[belong[x]].add', 'ind[belong[y]] += 1', 'for x in crystals', 'ctrstals_set.add', 'def tarjan'],
    captions={
        'in_stack[u] = True': lambda S, B, r: f'访问 `{S.u}`：`dfn[{S.u}] = low[{S.u}] = {S.dfn[S.u]}`（第 {S.dfn[S.u]} 个到达），入栈',
        'if dfn[v] == 0': _ifv,
        'low[u] = min(low[u], low[v])': lambda S, B, r: f'`{S.v}` 递归返回，子树能回到的最早点传给父亲：`low[{S.u}] = min({B.low[S.u]}, {S.low[S.v]}) = {S.low[S.u]}`',
        'low[u] = min(low[u], dfn[v])': lambda S, B, r: f'`low[{S.u}] = min({B.low[S.u]}, {S.dfn[S.v]}) = {S.low[S.u]}`',
        'if low[u] == dfn[u]': _root,
        'tot += 1': _tot,
        'ind = [0] * tot': '分量个数 `tot = {len(ind)}`；之后遍历所有边，不同分量之间的边累加到目标分量的入度 `ind`',
        'ctrstals_set = set()': lambda S, B, r: f'缩点完成：各分量入度 `ind = {S.ind}`（重复边只算一次，用 `new_g` 去重）',
        'res = 0': lambda S, B, r: f'有水晶的分量：`{sorted(S.ctrstals_set)}`；接下来统计「没水晶且入度为 0」的分量个数',
        'if x not in ctrstals_set': _fin,
        'res += 1': '`res = {res}`：需要从水晶向这个分量连一条新边',
        'return res': '最少需要添加 `{ret}` 条符文',
    },
    max_steps=60,
    cards=dict(
        one_liner='缩点后，入度为 0 且没水晶的分量，各要补一条边',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['`n` 个焦点，部分有魔法水晶；有向符文把魔力从 `flowFrom[i]` 传到 `flowTo[i]`',
                 '要让每个焦点要么有水晶，要么能从别的焦点接到魔力，至少再加几条有向边？',
                 '本视频：`n=8`，水晶在 `0`，边 `0→1, 2→3→4→2, 5→3, 6↔7` → `2`'],
        quote='对于强连通相关的问题，一种常见的处理方法是先对有向图执行一次tarjan算法，找出图中所有的强连通分量，然后将强连通分量收缩成一个单独的点。这样一来，整张图就可以转换成有向无环图。',
        quote_src='—— yiduobo 题解原文',
        idea=['环里的点互相能到，一个分量里==只要有一个点被接上，整个分量都有魔力==',
              '先 Tarjan 求强连通分量并缩点，得到有向无环图（DAG）',
              '入度为 0 又没有水晶的分量，没人能给它送魔力 → 各补一条边，统计个数即可'],
        summary=['时间 `O(n+m)`；Tarjan 用 `dfn`（次序）、`low`（能回到的最早次序）和栈找 SCC',
                 '`low[u] == dfn[u]` 才是 SCC 的根，此时把栈弹到 `u` 为止',
                 '缩点后入度要对重复边去重（`new_g` 用 set），水晶所在的分量不用加边',
                 '对比灵神：灵神先从水晶出发 DFS 标记可达点，只对剩余点跑 Tarjan；yiduobo 直接全图缩点再用水晶集合排除',
                 '原文变量 `t`、`tot` 用 `global` 声明，代码未改动'],
    ),
)
