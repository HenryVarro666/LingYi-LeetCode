# 示例 2：roads 与 seats（布局用的静态树，和 call 保持一致）
ROADS = [[3, 1], [3, 2], [1, 0], [0, 4], [0, 5], [4, 6]]
SEATS = 2
G = {i: [] for i in range(len(ROADS) + 1)}
for _x, _y in ROADS:
    G[_x].append(_y)
    G[_y].append(_x)
CH, PAR = {}, {0: -1}


def _build(x, fa):
    CH[x] = [y for y in sorted(G[x]) if y != fa]
    for y in CH[x]:
        PAR[y] = x
        _build(y, x)


_build(0, -1)
POS, _leaf = {}, [0]


def _place(x, d):
    if not CH[x]:
        POS[x] = (_leaf[0], d)
        _leaf[0] += 1
    else:
        for y in CH[x]:
            _place(y, d + 1)
        POS[x] = (sum(POS[y][0] for y in CH[x]) / len(CH[x]), d)


_place(0, 0)
NLEAF = _leaf[0]
MAXD = max(d for _, d in POS.values()) + 1
SIZE, PRE, COST = {}, {}, {}


def _meta(x):
    PRE[x] = len(PRE)
    SIZE[x] = 1 + sum(_meta(y) for y in CH[x])
    COST[x] = sum(COST[y] + (SIZE[y] - 1) // SEATS + 1 for y in CH[x])
    return SIZE[x]


_meta(0)


def track(fn):
    return fn if callable(fn) else (lambda S, B, r: fn)


def _done(n, cur, line, ch, same):
    """dfs(n) 是否已经返回（由当前所在节点、行号和循环变量 child 推出）"""
    if cur is None:
        return line is not None and line >= 26
    if n == cur:
        return line == 24
    anc, a = [], PAR[n]
    while a >= 0:
        anc.append(a)
        a = PAR[a]
    if cur in anc:                       # n 在 cur 的子树里
        if line >= 24:
            return True
        c = ([n] + anc)[anc.index(cur)]   # cur 的哪个孩子管着 n
        if ch not in CH[cur]:
            return False
        i, j = CH[cur].index(c), CH[cur].index(ch)
        return i < j or (i == j and (line in (21, 22) or (line == 17 and same)))
    a = cur
    while a >= 0:
        if a == n:
            return False
        a = PAR[a]
    return PRE[n] < PRE[cur]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '城市树（首都 0 为根；黄 = 递归路径，蓝 = 当前节点，绿 = 已返回 (cnt, cost)）', 22, T['muted'], bold=True)
    sp = min(130, (x1 - x0 - 80) / max(1, NLEAF))
    dy = min(100, (y1 - y0 - 120) / max(1, MAXD - 1))
    sx = x0 + 40 + ((x1 - x0 - 80) - sp * (NLEAF - 1)) / 2
    rad = 25

    def P(n):
        return sx + POS[n][0] * sp, y0 + 80 + POS[n][1] * dy
    cur = S['_inner'].get('now') if 'now' in S['_inner'] else None
    line = S.get('_line')
    same = bool(B) and B['_inner'].get('child') == S['_inner'].get('child') and B['_inner'].get('now') == cur
    DONE = {n for n in CH if _done(n, cur, line, S['_inner'].get('child'), same)}
    path = set()
    a = cur
    while a is not None and a >= 0:
        path.add(a)
        a = PAR[a]
    for n in CH:
        for c in CH[n]:
            cv.line([P(n), P(c)], T['border'], 3)
            if c in DONE:
                cost = (SIZE[c] - 1) // SEATS + 1
                mx, my = (P(n)[0] + P(c)[0]) / 2, (P(n)[1] + P(c)[1]) / 2
                t = f'+{cost} 升'
                w = cv.tlen(t, 19, bold=True) + 14
                cv.rect((mx - w / 2, my - 14, mx + w / 2, my + 14), fill=T['panel'], outline=T['orange'], width=2, r=8)
                cv.text((mx, my), t, 19, T['orange'], anchor='mm', bold=True)
    for n in CH:
        X, Y = P(n)
        fill = T['green'] if n in DONE else T['panel2']
        outline = T['yellow'] if n in path else T['border']
        if n == cur:
            fill, outline = T['blue'], T['blue']
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=outline, width=4)
        cv.text((X, Y), n, 26, T['bg'] if n in DONE or n == cur else T['text'], anchor='mm', bold=True)
        if n in DONE:
            cv.text((X + rad + 8, Y - 11), f'cnt={SIZE[n]}', 18, T['green'], anchor='lm', bold=True)
            cv.text((X + rad + 8, Y + 11), f'cost={COST[n]}', 18, T['green'], anchor='lm', bold=True)


CONFIG = dict(
    num=2477, title='到达首都的最少油耗', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='自底向上递归 · 返回 (人数, 油耗)',
    tags=['贪心与思维', '链表树与回溯', '难度分 2012'],
    code='''
class Solution(object):
    def minimumFuelCost(self, roads, seats):

        g = {}
        for x, y in roads:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)

        def dfs(now, fa):
            tot_cnt = 1
            tot_cost = 0

            for child in g.get(now, set()):
                if child == fa:
                    continue
                child_cnt, child_cost = dfs(child, now)
                tot_cnt += child_cnt
                tot_cost += child_cost + (child_cnt - 1) // seats + 1

            return tot_cnt, tot_cost

        return dfs(0, -1)[1]
''',
    call='Solution().minimumFuelCost([[3,1],[3,2],[1,0],[0,4],[0,5],[4,6]], 2)',
    expect=7,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='calls', h=190),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'blue'), ('tot_cnt', lambda S: S['_inner'].get('tot_cnt'), 'yellow'),
           ('tot_cost', lambda S: S['_inner'].get('tot_cost'), 'green')],
    captions={
        'g = {}': '`g` 邻接表：城市 → 邻居集合',
        'g[x].add(y)': '边 `{x}—{y}`：`g[{x}]` 加入 `{y}`，下一行 `g[{y}]` 加入 `{x}`（无向边两头都记）',
        'tot_cnt = 1': '进入城市 `{now}`：`tot_cnt = 1`（自己的代表）',
        'tot_cost = 0': '`tot_cost = 0`：以 `{now}` 为根的子树里，代表们汇合到 `{now}` 的油耗',
        'for child in g.get': lambda S, B, r: (f'枚举 `{S.now}` 的邻居 `child = {S.child}`' if S['_inner'].get('child') is not None and (B['_inner'].get('child') != S['_inner'].get('child') or B['_inner'].get('now') != S['_inner'].get('now')) else f'`{S.now}` 的邻居都看完了'),
        'if child == fa': lambda S, B, r: (f'`{S.child}` 就是父亲 `fa = {S.fa}` → 不往回走' if S.child == S.fa else f'`{S.child}` 是 `{S.now}` 的子节点 → 递归进去'),
        'continue': '跳过父亲',
        'child_cnt, child_cost = dfs': '递归子节点 `{child}`：返回它的子树人数和汇合到 `{child}` 的油耗',
        'tot_cnt += child_cnt': '子树 `{child}` 有 `{child_cnt}` 个代表 → `tot_cnt` = {tot_cnt}',
        'tot_cost += child_cost': '`tot_cost` += `{child_cost} + ({child_cnt}−1)//{seats} + 1` = {B.tot_cost} + {child_cost} + =={(child_cnt - 1) // seats + 1}== → {tot_cost}（后者是 `{child_cnt}` 人从 `{child}` 到 `{now}` 的车数）',
        'return tot_cnt, tot_cost': '城市 `{now}` 的子树：`{tot_cnt}` 个代表、汇合油耗 `{tot_cost}`，返回给父亲',
        'return dfs(0, -1)[1]': '从首都 0 出发（`fa = -1` 表示没有父亲），最后取返回值的第二项：总油耗',
    },
    skip=['g[y].add(x)', 'if x not in g', 'if y not in g', 'g[x] = set()', 'g[y] = set()'],
    max_steps=60,
    cards=dict(
        one_liner='每次只坐一站，到站和别的子树的人汇合再拼车',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 个城市组成一棵树，0 号是首都，每个城市一名代表',
                 '每个城市有一辆 `seats` 座的车，代表们可以换乘，相邻城市一辆车耗 1 升',
                 '求所有代表到达首都的最少油耗',
                 '本视频：`roads=[[3,1],[3,2],[1,0],[0,4],[0,5],[4,6]]`，`seats=2` → `7`'],
        quote='由于题目中的换乘没有任何代价，且拼车的油耗必然是小于等于单独搭车的，因此每次乘车都应该尽量拼车，同时每次都只坐一站。',
        quote_src='—— yiduobo 题解原文',
        idea=['`dfs(now, fa)` 返回两个值：子树代表总数 `tot_cnt`、汇合到 `now` 的油耗 `tot_cost`',
              '累加每个孩子：`tot_cost += child_cost + ceil(child_cnt / seats)`',
              '`child_cnt` 个人从孩子坐一站到 `now`，需要 `(child_cnt − 1)//seats + 1` 辆车',
              '从首都 0 开始递归，返回值的第二项就是答案'],
        result='运行结束，返回 `7`：首都子树的总油耗',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：向上取整写成 `(cnt − 1)//seats + 1`，不能直接 `cnt // seats`',
                 '`g.get(now, set())`：只有一个城市（`roads` 为空）时 `g` 里没有 0，要给默认值',
                 '对比灵神：灵神用外部变量 `ans` 累加每条边；yiduobo 把油耗放在返回值里层层累加',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（含删去 `:type` 说明）'],
    ),
)
