import math

COST = [4, 2, 9, 7, 3, 5]
ROADS = [[0, 1], [0, 2], [1, 2], [2, 3], [3, 4], [3, 5], [4, 5]]
POS = {0: (.10, .22), 1: (.10, .78), 2: (.34, .50), 3: (.62, .50), 4: (.88, .22), 5: (.88, .78)}
BCOL = ['blue', 'green', 'purple', 'cyan', 'pink', 'orange']


def _leaf_seed(nl, cut, cost):
    """块 nl 的割点个数；若恰为 1，返回块里最便宜的非割点"""
    cs = [x for x in nl if x in cut]
    if len(cs) != 1:
        return None
    return min((x for x in nl if x not in cut), key=lambda x: cost[x])


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(COST)
    cv.text((x0 + 18, y0 + 4), '无向图（节点旁 = 夺回成本；下方 dfn/low；同色边 = 同一个双连通分量）', 21, T['muted'], bold=True)
    px = lambda p: (x0 + 50 + p[0] * (x1 - x0 - 100), y0 + 100 + p[1] * (y1 - y0 - 210))
    dfn = S.get('dfn') or [None] * n
    low = S.get('low') or [None] * n
    dcc = S.get('dcc') or []
    cut = S.get('cut_pos') or set()
    inner = S.get('_inner', {})
    now, nxt = inner.get('now'), inner.get('next')
    R = 30
    cur = S.get('node_list')
    ki = None
    if cur is not None:
        for k, nl in enumerate(dcc):
            if nl is cur:
                ki = k
    for a, b in ROADS:
        (ax, ay), (bx, by) = px(POS[a]), px(POS[b])
        col, wd = (80, 90, 104), 3
        for k, nl in enumerate(dcc):
            if a in nl and b in nl:
                col = T[BCOL[k % 6]]
                wd = 5
        if (a, b) in ((now, nxt), (nxt, now)):
            col, wd = T['yellow'], 7
        cv.line([(ax, ay), (bx, by)], col, wd)
    seeds = {}
    if ki is not None:
        for k in range(ki + 1):
            sd = _leaf_seed(dcc[k], cut, COST)
            if sd is not None:
                seeds[sd] = k
    dropped = None
    if S.get('_line') == 71 and seeds:
        dropped = max(seeds, key=lambda x: COST[x])
    for i in range(n):
        X, Y = px(POS[i])
        fill = T['panel2']
        out, wd = T['border'], 2
        if dfn[i] is not None:
            out, wd = (110, 120, 134), 3
        if i in cut:
            out, wd = T['red'], 6
        if now == i:
            out, wd = T['pink'], 6
        if cur is not None and i in cur:
            fill = (60, 52, 80)
        if i in seeds and i != dropped:
            fill = tuple(int(0.55 * k + 0.45 * q) for k, q in zip(T['green'], T['panel2']))
        cv.rect((X - R, Y - R, X + R, Y + R), fill=fill, outline=out, width=wd, r=R)
        cv.text((X, Y), i, 28, T['text'], anchor='mm', bold=True)
        cv.text((X, Y - R - 4), f'成本 {COST[i]}', 20, T['yellow'], anchor='mb', bold=True)
        if i in cut:
            cv.text((X, Y + R + 28), '割点', 20, T['red'], anchor='mt', bold=True)
        if dfn[i] is not None:
            cv.text((X, Y + R + 4), f'{dfn[i]}/{low[i]}', 20, T['cyan'], anchor='mt', bold=True, mono=True)
        if i in seeds:
            cv.text((X + R + 8, Y), '省掉' if i == dropped else '空降', 20, T['orange'] if i == dropped else T['green'], anchor='lm', bold=True)
    if dcc:
        cv.text((x0 + 18, y1 - 40), '双连通分量：' + '  '.join(str(sorted(d)) for d in dcc), 22, T['purple'], bold=True)


def _msg(S):
    if S.get('node_list') is not None or 'ma_cost' in S and 'res' in S:
        return '每个==只含 1 个割点==的块（叶子）要空降一个人，选块内最便宜的非割点'
    if 'dcc' in S:
        return 'Tarjan：`dfn` = 访问次序，`low` = 能回到的最早点；`low[next] >= dfn[now]` → `now` 是割点，弹栈得到一个块'
    return '魔物据点不能被分成多块：==割点要等一侧夺完才能夺=='


def _ifn(S, B, ret):
    now, nx = S.now, S.next
    if S.dfn[nx] is None:
        return f'边 `{now}—{nx}`：`{nx}` ==没访问过== → 树边，递归进去'
    return f'边 `{now}—{nx}`：`{nx}` 已访问 → 回边，用 `dfn[{nx}] = {S.dfn[nx]}` 更新 `low[{now}]`'


def _cutq(S, B, ret):
    now, nx = S.now, S.next
    ok = S.low[nx] >= S.dfn[now]
    if ok:
        return f'`low[{nx}] = {S.low[nx]} >= dfn[{now}] = {S.dfn[now]}`：`{nx}` 子树回不到 `{now}` 之上 → 弹出一个==双连通分量=='
    return f'`low[{nx}] = {S.low[nx]} < dfn[{now}] = {S.dfn[now]}`：子树能绕过 `{now}` → 还没形成分量'


def _cutadd(S, B, ret):
    now = S.now
    if now != 0 or S.child_cnt > 1:
        return f'`{now}` 不是根（或根有多个子块）→ ==割点==，去掉它图会分开；`cut_pos = {sorted(S.cut_pos | {now})}`'
    return f'`{now}` 是根且只有一个子块 → 不是割点'


def _dccap(S, B, ret):
    return f'栈弹到 `{S.next}` 为止，再加上 `{S.now}`：新分量 `{sorted(S.dcc[-1])}`'


def _cnt1(S, B, ret):
    nl = S.node_list
    cs = [x for x in nl if x in S.cut_pos]
    if len(cs) == 1:
        sd = _leaf_seed(nl, S.cut_pos, S.cost)
        return f'块 `{sorted(nl)}` 只有 1 个割点 `{cs[0]}` → 叶子块：要空降，选最便宜的非割点 `{sd}`（成本 `{S.cost[sd]}`）'
    return f'块 `{sorted(nl)}` 有 `{len(cs)}` 个割点 → 它会被两侧夺回的据点连起来，==不用空降=='


CONFIG = dict(
    num='LCP 54', title='夺回据点', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='Tarjan 点双连通分量 · 叶子块各空降一人',
    tags=[],
    code='''
class Solution(object):
    def minimumCost(self, cost, roads):

        n = len(cost)
        if n == 1:
            return cost[0]
        
        g = {}
        for x, y in roads:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)
        
        cut_pos = set()
        dfn = [None] * n
        low = [None] * n
        dcc = []
        stack = []

        global cnt
        cnt = 0

        def dfs(now):
            global cnt
            cnt += 1
            dfn[now] = low[now] = cnt
            stack.append(now)
            child_cnt = 0
            for next in g.get(now, set()):
                if dfn[next] is None:
                    dfs(next)
                    low[now] = min(low[now], low[next])
                    if low[next] >= dfn[now]:
                        child_cnt += 1
                        if now != 0 or child_cnt > 1:
                            cut_pos.add(now)
                        
                        dcc.append([])
                        while stack[-1] != next:
                            dcc[-1].append(stack[-1])
                            stack.pop()
                        dcc[-1].append(next)
                        stack.pop()
                        dcc[-1].append(now)
                    
                else:
                    low[now] = min(low[now], dfn[next])
        
        dfs(0)

        if len(dcc) == 1:
            return min(cost)

        ma_cost = 0
        res = 0
        for node_list in dcc:
            cnt = 0
            min_cost = None
            for now in node_list:
                if now in cut_pos:
                    cnt += 1
                elif min_cost is None or cost[now] < min_cost:
                    min_cost = cost[now]
            if cnt == 1:
                res += min_cost
                ma_cost = max(ma_cost, min_cost)

        return res - ma_cost
''',
    call=f'Solution().minimumCost({COST}, {ROADS})',
    expect=2,
    views=[
        dict(type='text', fn=_msg, size=24, h=60),
        dict(type='custom', draw=_draw, h=600),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'pink'), ('cut_pos', 'cut_pos', 'red'), ('res', 'res', 'green'), ('ma_cost', 'ma_cost', 'yellow')],
    skip=['n = len(cost)', 'if n == 1', 'for x, y in roads', 'if x not in g', 'if y not in g', 'g[x] = set()', 'g[y] = set()', 'g[x].add(y)', 'g[y].add(x)',
          'dfn = [None]', 'low = [None]', 'dcc = []', 'stack = []', 'global cnt', 'cnt = 0', 'cnt += 1', 'stack.append(now)', 'child_cnt = 0',
          'for next in g.get', '                    dfs(next)', 'child_cnt += 1', 'dcc.append([])', 'while stack[-1] != next', 'dcc[-1].append(stack[-1])',
          'stack.pop()', 'dcc[-1].append(next)', 'else:', 'def dfs', 'ma_cost = 0', 'for node_list in dcc', 'min_cost = None', 'for now in node_list',
          'if now in cut_pos', 'elif min_cost is None', 'min_cost = cost[now]', 'ma_cost = max', 'g = {}', 'if dfn[next] is None', 'res = 0', 'cut_pos.add(now)'],
    captions={
        'cut_pos = set()': '先建邻接表 `g`（无向边两头都存）。再准备 Tarjan 要用的：`cut_pos` 割点集合、`dfn/low`、`dcc` 分量列表、`stack`',
        'dfs(0)': '从据点 `0` 开始 Tarjan（dfs 一趟求出所有割点和双连通分量）',
        'dfn[now] = low[now] = cnt': '访问 `{now}`（沿树边进来）：`dfn = low = {dfn[now]}`，入栈，然后逐个看它的邻居',
        'low[now] = min(low[now], low[next])': lambda S, B, r: f'`{S.next}` 返回：`low[{S.now}] = min({B.low[S.now]}, {S.low[S.next]}) = {S.low[S.now]}`',
        'if low[next] >= dfn[now]': _cutq,
        'if now != 0 or child_cnt > 1': _cutadd,
        'dcc[-1].append(now)': _dccap,
        'low[now] = min(low[now], dfn[next])': lambda S, B, r: f'边 `{S.now}—{S.next}`：`{S.next}` 已访问（回边或父边）→ `low[{S.now}] = min({B.low[S.now]}, dfn[{S.next}] = {S.dfn[S.next]}) = {S.low[S.now]}`',
        'if len(dcc) == 1': lambda S, B, r: f'共 `{len(S.dcc)}` 个分量；割点 `{sorted(S.cut_pos)}`。只有 1 个分量时直接取最小成本，这里不是',
        'if cnt == 1': _cnt1,
        'res += min_cost': '`res = {B.res} + {min_cost} = {res}`：这个叶子块空降最便宜的非割点',
        'return res - ma_cost': '最贵的那个叶子块可以==省掉空降==：它的另一侧夺完后，割点会带着小队过来。`{res} − {ma_cost}` = `{ret}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='割点要等一侧夺完才能夺：叶子块各空降一人，最贵的那个省掉',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['`n` 个据点被魔物占领，`roads` 是无向道路，`cost[i]` 是夺回据点 `i` 的成本',
                 '夺回过程中，魔物占着的据点==不能被分割成多个连通块==；已夺回据点的相邻据点可顺势夺回',
                 '求夺回全部据点的最小总成本。本视频：`cost=[4,2,9,7,3,5]`，7 条边'],
        quote='如果将连通分量进行缩点操作，最后将会得到一颗树，其中仅有一个割点的连通分量为树的叶子节点，而其他的则为非叶子节点。对于这颗树来说，可以占据任意叶子节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['割点的某一侧没夺完之前，不能先夺割点，否则魔物会被分成两块',
              '缩点后是一棵树：==只含 1 个割点的块 = 叶子块==，每个叶子块都要空降一人，选块内最便宜的非割点',
              '最后可放弃空降成本最大的那个叶子块：其余块夺完后，割点能把小队带过来'],
        summary=['Tarjan 一趟求出割点和点双连通分量；时间 `O(n+m)`',
                 '空降只选非割点（割点要最后夺）；只有 1 个割点的块才需要空降',
                 '答案 = 所有叶子块最小非割点成本之和 − 其中最大的一个',
                 '特判：`n == 1` 返回 `cost[0]`；只有 1 个分量时返回 `min(cost)`',
                 '原文用 `global cnt` 记 dfn 序号，代码未改动；本题官方无灵神题解，此为 yiduobo 思路'],
    ),
)
