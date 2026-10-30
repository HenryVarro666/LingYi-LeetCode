import math as _math


def _gdraw(cv, T, box, title, pos, edges, color_of, sub_of=None, ecolor_of=None, R=26):
    """有向图：pos = [(fx, fy)]（0~1 的相对位置），edges = [(a, b)]"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    Wd, Hd = x1 - x0 - 100, y1 - y0 - 110
    P = [(x0 + 50 + fx * Wd, y0 + 60 + fy * Hd) for fx, fy in pos]
    es = set(edges)
    for a, b in edges:
        ec = (ecolor_of(a, b) if ecolor_of else None) or 'dim'
        col = T[ec] if isinstance(ec, str) else ec
        (xa, ya), (xb, yb) = P[a], P[b]
        if a == b:
            cv.arc_arrow((xa - 12, ya - R + 2), (xa + 12, ya - R + 2), 46, col, 3, 11)
            continue
        dx, dy = xb - xa, yb - ya
        L = _math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        off = 9 if (b, a) in es else 0
        nx, ny = -uy * off, ux * off
        cv.arrow((xa + ux * (R + 3) + nx, ya + uy * (R + 3) + ny), (xb - ux * (R + 6) + nx, yb - uy * (R + 6) + ny), col, 3, 12)
    for i, (x, y) in enumerate(P):
        c = color_of(i)
        fill = T[c] if isinstance(c, str) else (c or T['panel2'])
        cv.rect((x - R, y - R, x + R, y + R), fill=fill, outline=T['border'], r=R)
        cv.text((x, y), i, 26, T['bg'] if c else T['muted'], anchor='mm', bold=True)
        if sub_of:
            s = sub_of(i)
            if s:
                cv.text((x, y + R + 6), s, 19, T['text'], anchor='mt', mono=True)
    return P
import math as _math


def _gdraw2(cv, T, box, title, nodes, pos, edges, color_of, sub_of=None, R=26, directed=False):
    """图：nodes = 节点标号列表，pos = {标号: (fx, fy)}，edges = [(a, b)]"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    Wd, Hd = x1 - x0 - 100, y1 - y0 - 120
    P = {i: (x0 + 50 + pos[i][0] * Wd, y0 + 60 + pos[i][1] * Hd) for i in nodes}
    for a, b in edges:
        (xa, ya), (xb, yb) = P[a], P[b]
        L = _math.hypot(xb - xa, yb - ya)
        ux, uy = (xb - xa) / L, (yb - ya) / L
        if directed:
            cv.arrow((xa + ux * (R + 3), ya + uy * (R + 3)), (xb - ux * (R + 6), yb - uy * (R + 6)), T['dim'], 3, 12)
        else:
            cv.line([(xa, ya), (xb, yb)], T['dim'], 4)
    for i in nodes:
        x, y = P[i]
        c = color_of(i)
        fill = T[c] if isinstance(c, str) else (c or T['panel2'])
        cv.rect((x - R, y - R, x + R, y + R), fill=fill, outline=T['border'], r=R)
        cv.text((x, y), i, 26, T['bg'] if c else T['muted'], anchor='mm', bold=True)
        if sub_of:
            s = sub_of(i)
            if s:
                if y < y0 + (y1 - y0) / 2:
                    cv.text((x, y - R - 5), s, 19, T['text'], anchor='mb', mono=True)
                else:
                    cv.text((x, y + R + 6), s, 19, T['text'], anchor='mt', mono=True)
    return P


EDGES = [[1, 2], [2, 3], [3, 4], [4, 1], [2, 5], [5, 6]]
SA, SB = 1, 5
NODES = [1, 2, 3, 4, 5, 6]
POS = {1: (0.0, 0.3), 2: (0.3, 0.3), 3: (0.3, 0.95), 4: (0.0, 0.95), 5: (0.62, 0.3), 6: (0.92, 0.3)}


def _col(S, i):
    if 'chain' not in S:
        return None
    sa, sb = S['startA'], S['startB']
    if 'vis' in S and 'entrance' in S or 'vis' in S:
        if i in S['vis']:
            return 'green'
    if i == S.get('now') and 'dis' in S:
        return 'pink'
    if i == S.get('now') and 'head' in S and 'disA' not in S:
        return 'pink'
    if 'disA' not in S:
        if i in S['chain']:
            return 'orange'
        return None
    if i in S['chain']:
        return 'orange'
    return 'cyan'


def _sub(S, i):
    out = []
    if i == S['startA']:
        out.append('A小力')
    if i == S['startB']:
        out.append('B小扣')
    if 'disA' in S and S['disA'][i] is not None and 'disB' in S and S['disB'][i] is not None:
        out.append(f"{S['disA'][i]}/{S['disB'][i]}")
    return ' '.join(out)


def _draw(cv, S, B, box, T):
    sa, sb = S['startA'], S['startB']
    _gdraw2(cv, T, box, '无向图（橙 = 链，青 = 环，绿 = 小扣能先到的点；标注 = 小力步数/小扣步数）', NODES, POS,
            [tuple(e) for e in S['edges']], lambda i: _col(S, i), sub_of=lambda i: _sub(S, i))


def _cap_peel(S, B, r):
    return f'邻居 `{S.next}` 少了一条边，度 → {S.d[S.next]}'


CONFIG = dict(
    num='LCP 21', title='追逐游戏', difficulty='', category='图论算法',
    author='yiduobo', technique='拓扑剪链找环 + 双 BFS',
    tags=['灵神题单·图论算法', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def chaseGame(self, edges, startA, startB):

        g = {}
        d = {}
        n = len(edges)
        for x, y in edges:
            d[x] = d.get(x, 0) + 1
            d[y] = d.get(y, 0) + 1
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)
        
        if startB in g[startA]:
            return 1
        
        q = []
        chain = set()
        for index in range(1, n + 1):
            if d[index] == 1:
                q.append(index)
                chain.add(index)
        
        head, tail = 0, len(q)
        while head < tail:
            now = q[head]
            head += 1
            for next in g[now]:
                d[next] -= 1
                if d[next] == 1:
                    q.append(next)
                    tail += 1
                    chain.add(next)
        
        def bfs(start, dis):
            dis[start] = 0
            q = [start]
            head, tail = 0, 1
            while head < tail:
                now = q[head]
                head += 1
                for next in g[now]:
                    if dis[next] is None:
                        dis[next] = dis[now] + 1
                        q.append(next)
                        tail += 1
        
        disA = [None] * (n + 1)
        bfs(startA, disA)
        disB = [None] * (n + 1)
        bfs(startB, disB)

        if n - len(chain) > 3:
            entrance = None
            b_to_circle = None
            for index in range(1, n + 1):
                if index not in chain and (b_to_circle is None or b_to_circle > disB[index]):
                    b_to_circle = disB[index]
                    entrance = index
            
            if disA[entrance] > b_to_circle + 1:
                return -1
        
        q = [startB]
        head, tail = 0, 1
        vis = set([startB])
        while head < tail:
            now = q[head]
            head += 1
            for next in g[now]:
                if disA[next] - 1 > disB[next] and next not in vis:
                    q.append(next)
                    vis.add(next)
                    tail += 1
        
        res = 0
        for index in vis:
            res = max(res, disA[index])
        return res
''',
    call='Solution().chaseGame(EDGES, 1, 5)',
    setup='EDGES = [[1, 2], [2, 3], [3, 4], [4, 1], [2, 5], [5, 6]]',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=250),
        dict(type='array', var='disA', h=140, label='disA[i]：小力到 i 的最少步数（下标从 1 起）'),
        dict(type='array', var='disB', h=140, label='disB[i]：小扣到 i 的最少步数'),
    ],
    watch=[('head', 'head', 'blue'), ('tail', 'tail', 'pink'), 'entrance', 'b_to_circle', ('res', 'res', 'green')],
    skip=['d[x] = d.get', 'd[y] = d.get', 'if x not in g', 'g[x] = set()', 'if y not in g', 'g[y] = set()', 'g[x].add(y)', 'g[y].add(x)',
          'n = len(edges)', 'g = {}', 'd = {}', 'q = []', 'chain = set()', 'q.append(index)', 'chain.add(index)', 'for index in range(1, n + 1):',
          'head += 1', 'for next in g[now]', 'q.append(next)', 'tail += 1', 'chain.add(next)', 'dis[start] = 0', 'q = [start]', 'head, tail = 0, 1',
          'def bfs', 'while head < tail', 'entrance = None', 'b_to_circle = None', 'b_to_circle = disB[index]', 'res = 0', 'if dis[next] is None', 'vis.add(next)', 'q = [startB]', 'for index in vis'],
    max_steps=75,
    captions={
        'for x, y in edges': '读入边 `{x}-{y}`：两端度数 +1，互相加进邻接表 `g`',
        'if startB in g[startA]': '小力先手：如果小扣就在隔壁，==第一步就抓到==，返回 1',
        'if d[index] == 1': lambda S, B, r: (f'`d[{S.index}] = 1`：只连着一个点 → 是==链的末端==，先入队' if S.d[S.index] == 1 else f'`d[{S.index}] = {S.d[S.index]}`：在环上或在环的接口处，先不动'),
        'head, tail = 0, len(q)': '链的末端入队：`q = {q}`。下面像拓扑排序一样一层层把链==剪掉==，剩下的就是环',
        'd[next] -= 1': _cap_peel,
        'if d[next] == 1': lambda S, B, r: (f'`d[{S.next}]` 变成 1 → 它也成了链的末端，入队' if S.d[S.next] == 1 else f'`d[{S.next}] = {S.d[S.next]}` ≠ 1：还在环上或还有别的分支，不入队'),
        'disA = [None] * (n + 1)': '剪完了。环 = 没进过 `chain` 的点：`{sorted(set(range(1, n + 1)) - chain)}`，环长 `{n - len(chain)}`',
        'bfs(startA, disA)': '从小力 `{startA}` 出发 BFS，算出小力到每个点的最少步数 `disA`',
        'bfs(startB, disB)': '再从小扣 `{startB}` 出发 BFS，算出 `disB`',
        'now = q[head]': lambda S, B, r: (f'BFS 取出 `{S.now}`，给它的邻居标上 `dis[{S.now}] + 1`' if 'dis' in S else
                                          (f'取出链上的点 `{S.now}`，把它从图里剪掉（邻居度数各减 1）' if 'disA' not in S else f'小扣扩展到 `{S.now}`：看它的邻居能不能去')),
        'dis[next] = dis[now] + 1': 'BFS 距离：`dis[{next}] = dis[{now}] + 1` = {dis[next]}',
        'if n - len(chain) > 3': lambda S, B, r: (f'环长 `{S.n - len(S.chain)}` > 3：小扣有机会在环上和小力绕圈（环长 ≤ 3 时，小力一上环就和环上所有点相邻）' if S.n - len(S.chain) > 3
                                                  else f'环长 `{S.n - len(S.chain)}` ≤ 3：绕不了圈，小力一定追得上'),
        'if index not in chain and': lambda S, B, r: (f'`{S.index}` 在环上，小扣到它要 `{S.disB[S.index]}` 步' + ('，比之前更近 → 更新入口' if (B.b_to_circle is None or B.b_to_circle > S.disB[S.index]) else '，不比之前近')) if S.index not in S.chain else f'`{S.index}` 在链上，不是入口',
        'entrance = index': '小扣最快上环的点 `entrance = {entrance}`，需要 `{b_to_circle}` 步',
        'if disA[entrance] > b_to_circle + 1': lambda S, B, r: (f'小力到入口要 `{S.disA[S.entrance]}` 步，小扣只要 `{S.b_to_circle}` 步：小力慢超过 1 步 → 小扣先上环绕圈，==永远追不上，返回 -1=='
                                                              if S.disA[S.entrance] > S.b_to_circle + 1 else
                                                              f'小力 `{S.disA[S.entrance]}` 步 ≤ 小扣 `{S.b_to_circle}` + 1：小力先守住入口，小扣上不了环 → 能追上'),
        'vis = set([startB])': '现在小扣想跑远：从 `{startB}` 出发 BFS，只走“小力比小扣晚到 ≥ 2 步”的点（`disA - 1 > disB`）',
        'if disA[next] - 1 > disB[next]': lambda S, B, r: (f'邻居 `{S.next}`：小力 `{S.disA[S.next]}` 步到，小扣 `{S.disB[S.next]}` 步到 → ' + ('小扣早到 ≥ 2 步，==能去==' if (S.disA[S.next] - 1 > S.disB[S.next] and S.next not in B.vis) else ('已经去过' if S.next in B.vis and S.disA[S.next] - 1 > S.disB[S.next] else '小力不晚于小扣 +1 步，去了会被抓，不能去'))),
        
        'res = max(res, disA[index])': '小扣能到 `{sorted(vis)}`，取小力最晚到的：`res = max({B.res}, disA[{index}]) = {res}`',
        'return res': '小力最少要 =={ret}== 回合才能抓到小扣',
    },
    cards=dict(
        one_liner='先剪掉链找出环，用小力、小扣到各点的距离判断能否抓到',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 个点 `n` 条边的连通图（每个点编号 1..n），小力在 `startA`，小扣在 `startB`',
                 '小力先手，每回合两人依次行动，小力走到小扣所在点就抓到；两人都最优',
                 '求小力最少几回合抓到小扣，抓不到返回 `-1`；本视频样例答案 `3`'],
        quote='已知n个点，n - 1条边的连通图是一颗树，那么在数中增加一条边，得到的将会是一个环，以及与环相邻的若干条链。形象点来说，就是类似于简笔画的太阳。',
        quote_src='—— yiduobo 题解原文',
        idea=['图 = 一个环 + 挂在环上的链；==环长 > 3== 且小扣能先到环的入口，就能绕圈躲一辈子（-1）',
              '链的末端度数为 1：像拓扑排序一样一层层删，没删到的点就是环',
              '否则小扣尽量跑远：只能去“小力比他晚到 ≥ 2 步”的点，答案取其中小力到得最晚的'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`disA[entrance] > b_to_circle + 1` 才判 `-1`，差 1 步还是能守住入口',
                 '环长 `≤ 3` 时不会无限追：小力上环后和环上所有点相邻',
                 '开头 `startB in g[startA]` 要先判：一步就抓到',
                 '原文已是 Python 3 可运行的写法，未做任何修改'],
    ),
)
