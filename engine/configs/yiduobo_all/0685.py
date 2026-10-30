import math


def _ln(code, sub):
    """1-based line number of the first code line containing sub (leading blank line stripped)"""
    for k, s in enumerate(code.strip('\n').split('\n')):
        if sub in s:
            return k + 1
    return -1


def _gdraw(cv, box, T, pos, E, node_fn, edge_fn, label_fn=None, title='', directed=True, R=30, base=0, above=None, elabel=None):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    w = x1 - x0 - 140
    h = y1 - y0 - 170
    P = [(x0 + 70 + fx * w, y0 + 80 + fy * h) for fx, fy in pos]
    es = set(E)
    for (a, b) in E:
        col, wd = edge_fn(a, b)
        (ax, ay), (bx, by) = P[a], P[b]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        off = 10 if (b, a) in es else 0
        nx, ny = -uy * off, ux * off
        p0 = (ax + ux * R + nx, ay + uy * R + ny)
        p1 = (bx - ux * (R + 2) + nx, by - uy * (R + 2) + ny)
        if elabel:
            t = elabel(a, b)
            if t:
                mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
                cv.text((mx + nx * 2.2 + 6, my + ny * 2.2 - 4), t, 20, col, anchor='lb', bold=True)
        if directed:
            cv.arrow(p0, p1, col, wd, head=16)
        else:
            cv.line([p0, p1], col, wd)
    for i, (x, y) in enumerate(P):
        fill, tc, ring = node_fn(i)
        cv.rect((x - R, y - R, x + R, y + R), fill=fill, r=R, outline=ring or T['border'], width=5 if ring else 1)
        cv.text((x, y), i + base, 26, tc, anchor='mm', bold=True)
        if label_fn:
            lab = label_fn(i)
            if lab:
                if above and above(i):
                    cv.text((x, y - R - 6), lab[0], 21, lab[1], anchor='mb', bold=True)
                else:
                    cv.text((x, y + R + 8), lab[0], 21, lab[1], anchor='mt', bold=True)


EDGES = [[1, 2], [2, 3], [3, 4], [4, 1], [1, 5]]
POS = [(0.35, 0.12), (0.8, 0.12), (0.8, 0.88), (0.35, 0.88), (0.0, 0.12)]
CODE = '''
class Solution(object):
    def findRedundantDirectedConnection(self, edges):

        edge_dict = {}
        n = len(edges)
        fa = [None] * n
        p = q = None
        for index, edge in enumerate(edges):
            x, y = edge
            x -= 1
            y -= 1
            edge_dict[(x, y)] = index
            if fa[y] is not None:
                p = y
                q = fa[y]
            fa[y] = x

        if p is not None:
            now = q
            while now != p and fa[now] is not None:
                now = fa[now]
            if now == p:
                return [q + 1, p + 1]
            
            now = p
            while fa[now] is not None:
                now = fa[now]
                if now == p:
                    return [fa[p] + 1, p + 1]

            if edge_dict[(q, p)] < edge_dict[(fa[p], p)]:
                return [fa[p] + 1, p + 1]
            else:
                return [q + 1, p + 1]

        p = 0
        used = [False] * n
        used[0] = True

        while True:
            p = fa[p]
            if used[p]:
                break
            used[p] = True

        now = p
        res = None
        while True:
            if res is None or edge_dict[(fa[res], res)] < edge_dict[(fa[now], now)]:
                res = now
            now = fa[now]
            if now == p:
                break

        return [fa[res] + 1, res + 1]
'''
L_P2 = _ln(CODE, 'used = [False]')
L_P3 = _ln(CODE, 'res = None')
L_RET = _ln(CODE, 'return [fa[res] + 1, res + 1]')


def _draw(cv, S, B, box, T):
    fa = S.get('fa') or [None] * 5
    line = S.get('_line', 0)
    used = S.get('used')
    cur = None
    if line >= L_P3 and S.get('now') is not None:
        cur = S['now']
    elif line >= L_P2 and S.get('p') is not None:
        cur = S['p']
    res = S.get('res') if line >= L_P3 else None
    ed = S.get('edge_dict') or {}
    seen = set(ed)

    def node(i):
        ring = T['yellow'] if cur == i else None
        if line >= L_P2 and used and used[i]:
            return T['blue'], T['bg'], ring
        return T['panel2'], T['text'], ring

    def ecol(a, b):
        if (a, b) not in seen:
            return T['dim'], 2
        if line >= L_RET and res is not None and (a, b) == (fa[res], res):
            return T['red'], 7
        if res is not None and (a, b) == (fa[res], res):
            return T['orange'], 6
        if cur is not None and fa[cur] is not None and (a, b) == (fa[cur], cur):
            return T['yellow'], 6
        return (150, 158, 170), 4

    def elab(a, b):
        return f'#{ed[(a, b)]}' if (a, b) in ed else None
    E = [(a - 1, b - 1) for a, b in EDGES]
    _gdraw(cv, box, T, POS, E, node, ecol, None, '黄 = 倒着走到的点，蓝 = 已走过，橙 = 候选，红 = 答案，#k = 出现顺序', base=1, elabel=elab)


def _fmt_edge(k, v):
    return f'({k[0] + 1},{k[1] + 1}) → #{v}'


CONFIG = dict(
    num=685, title='冗余连接 II', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='入度分类 · 沿入边找环',
    tags=['灵神题单·图论算法', '灵神题单·常用数据结构'],
    code=CODE,
    call=f'Solution().findRedundantDirectedConnection({EDGES})',
    expect=[4, 1],
    skip=['n = len(edges)', 'x -= 1', 'while True', 'used[0] = True'],
    max_steps=100,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='fa', label='fa[y] = 指向 y 的点（入边起点，下标 = 点 − 1）', h=125, cell=66, pointers={'p': 'pink', 'now': 'yellow'}),
        dict(type='map', var='edge_dict', label='edge_dict：边 → 出现顺序', h=100, fmt=_fmt_edge, font=22),
    ],
    watch=[('p', 'p', 'pink'), ('now', 'now', 'yellow'), ('res', 'res', 'green')],
    captions={
        'edge_dict = {}': '`edge_dict` 记录每条边的出现顺序，最后要在环上挑==最晚出现==的边',
        'fa = [None]': '`fa[y]` 记录 y 的入边起点；`p`、`q` 留给入度为 2 的点',
        'p = q = None': '`p`、`q` 先置空',
        'for index, edge in enumerate': lambda S, B, r: ('所有边的入边都记完了，没有点的入度为 2' if S.get('edge') == B.get('edge') and S.get('index') == B.get('index')
                                                        else f'看第 `{S.index}` 条边 `{S.edge}`'),
        'x, y = edge': '这条边从点 `{x}` 指向点 `{y}`（题目里点从 1 开始）',
        'y -= 1': '点编号减一变成下标：边 `{x} → {y}`',
        'edge_dict[(x, y)]': '记下边 `({x}, {y})` 是第 `{index}` 条',
        'if fa[y] is not None': lambda S, B, r: ('点 `%d` 已经有入边 → 入度为 2' % S.y if S.fa[S.y] is not None
                                                  else '点 `%d` 还没有入边，正常' % S.y),
        'p = y': '入度为 2 的点 `p = {p}`',
        'q = fa[y]': '它的第一条入边起点 `q = {q}`',
        'fa[y] = x': '`fa[{y}] = {x}`：记下 `{y}` 的入边来自 `{x}`',
        'if p is not None': lambda S, B, r: ('有入度为 2 的点 → 情况 1' if S.p is not None
                                              else '没有入度为 2 的点：所有点入度都是 1 → ==情况 2==，图里只有一个环'),
        'p = 0': '情况 2：从点 0 出发，沿入边倒着走，先找到一个环上的点',
        'used = [False]': '`used` 标记倒着走时到过的点',
        'p = fa[p]': '沿入边倒退一步：`p = {p}`',
        'if used[p]': lambda S, B, r: (f'点 `{S.p}` 以前走过 → 绕了一圈，它在环上' if S.used[S.p]
                                       else f'点 `{S.p}` 第一次到，继续倒退'),
        'used[p] = True': '标记点 `{p}` 已走过',
        'break': lambda S, B, r: ('环走完了，退出循环' if S.get('res') is not None else f'停下：`p = {S.p}` 在环上'),
        'now = p': '从环上的点 `{p}` 出发，沿入边走一整圈',
        'res = None': '`res` 记录环上最晚出现的那条边的终点',
        'if res is None or edge_dict': lambda S, B, r: (
            '还没有候选 → 当前边先当候选' if S.res is None or B.get('res') is None and S.res is None else
            ('当前边 `(%d→%d)` 编号 %d，比候选编号 %d 更晚 → 更新' % (S.fa[S.now] + 1, S.now + 1, S.edge_dict[(S.fa[S.now], S.now)], S.edge_dict[(S.fa[S.res], S.res)])
             if S.edge_dict[(S.fa[S.res], S.res)] < S.edge_dict[(S.fa[S.now], S.now)]
             else '当前边 `(%d→%d)` 编号 %d，不比候选 %d 晚 → 不换' % (S.fa[S.now] + 1, S.now + 1, S.edge_dict[(S.fa[S.now], S.now)], S.edge_dict[(S.fa[S.res], S.res)]))),
        'res = now': '候选边变成 `{fa[res]+1} → {res+1}`',
        'now = fa[now]': '继续沿入边倒着走：`now = {now}`',
        'if now == p': lambda S, B, r: ('走回了起点 → 环走完了' if S.now == S.p else '还没走回 `p`，继续'),
        'return [fa[res] + 1, res + 1]': '环上最晚出现的边是 `{fa[res]+1} → {res+1}`，返回 =={ret}==',
    },
    cards=dict(
        one_liner='先按入度分情况，再沿入边倒着找环，删环上最晚的边',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['有向图原本是一棵==有根树==（根入度 0，其余点入度 1），现在多了一条边',
                 '返回一条删去后能恢复成有根树的边；多个答案时返回==最后出现==的',
                 '示例：`[[1,2],[2,3],[3,4],[4,1],[1,5]]` → `[4,1]`'],
        quote='对于一颗树而言，其根节点的入度为0，而其余所有的节点的入度为1，出度则没有限制。',
        quote_src='—— yiduobo 题解原文',
        idea=['情况 1：某点入度为 2，两条入边 e1、e2 必删其一：有一条在环上删它，否则删较晚的',
              '情况 2：所有点入度都是 1：图里有且只有一个环，删环上最晚出现的边',
              '找环：每个点记录入边起点 `fa`，沿 `fa` 倒着走；本视频演示情况 2'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '先判断有没有入度为 2 的点：它决定走哪条分支',
                 '情况 2 里先倒着走到一个环上的点，再绕一圈挑编号最大的边',
                 '本视频只演示情况 2；情况 1 的两个子情况在代码前半段，示例未触发',
                 '对比 684：无向图用并查集，有向图要看入度'],
    ),
)
