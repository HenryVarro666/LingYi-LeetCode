EDGES = [[0, 1], [1, 2], [2, 0], [2, 3]]
POS = {0: (0.18, 0.22), 1: (0.18, 0.78), 2: (0.5, 0.5), 3: (0.85, 0.5)}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '图（红虚线 = 暂时删掉的边 x-y，绿 = BFS 已到达，粉 = 目标 y）', 22, T['muted'], bold=True)
    W, H = x1 - x0 - 80, y1 - y0 - 90

    def P(i):
        return (x0 + 40 + POS[i][0] * W, y0 + 60 + POS[i][1] * H)
    x, y = S.get('x'), S.get('y')
    g = S.get('g')
    d = S.get('d') if isinstance(S.get('d'), dict) else {}
    removed = g is not None and x is not None and y is not None and y not in g[x]
    for a, b in EDGES:
        if removed and {a, b} == {x, y}:
            cv.dashed(P(a), P(b), T['red'], 5)
        else:
            cv.line([P(a), P(b)], T['border'], 4)
    for i in POS:
        px, py = P(i)
        fill, tc = T['panel2'], T['muted']
        if i in d:
            fill, tc = T['green'], T['bg']
        if i == x and removed:
            fill, tc = T['cyan'], T['bg']
        if i == y and removed:
            fill, tc = T['pink'], T['bg']
        cv.rect((px - 34, py - 34, px + 34, py + 34), fill=fill, r=34, outline=T['border'], width=2)
        cv.text((px, py), i, 34, tc, anchor='mm', bold=True)
        if i in d:
            cv.text((px + 40, py - 44), f'd={d[i]}', 22, T['green'], anchor='lm', bold=True)


CONFIG = dict(
    num=2608, title='图中的最短环', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='枚举每条边：删边后 BFS 求 x 到 y', tags=['灵神题单', '广度优先搜索', '难度分 1904'],
    code='''
class Solution:
    def findShortestCycle(self, n, edges):

        g = {x : set() for x in range(n)}
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)

        res = 1001
        for x, y in edges:
            g[x].remove(y)
            g[y].remove(x)

            q = [x]
            d = {}
            d[x] = 0
            head, tail = 0, 1
            while head < tail:
                for now in q[head : tail]:
                    for nxt in g[now]:
                        if nxt not in d:
                            d[nxt] = d[now] + 1
                            q.append(nxt)
                
                head, tail = tail, len(q)
                if y in d:
                    res = min(res, d[y] + 1)
                    break

            g[x].add(y)
            g[y].add(x)
        
        if res == 1001:
            res = -1
        return res
''',
    call='Solution().findShortestCycle(4, EDGES)',
    setup=f'EDGES = {EDGES}',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var=lambda S: S['q'] if 'd' in S and 'q' in S else None, label='队列 q（BFS 从 x 出发）', window=('head', 'tail - 1'), h=150),
        dict(type='map', var=lambda S: S['d'] if isinstance(S.get('d'), dict) else None, label='d：x 到各点的距离（删边后）', fmt=lambda k, v: f'{k}: {v}', font=26, h=100),
    ],
    watch=['x', 'y', 'now', 'nxt', ('res', 'res', 'green')],
    captions={
        'g[x].remove(y)': '先把边 `{x}-{y}` 从图里删掉：之后若 {x} 还能走到 {y}，路径 + 这条边 = 环',
        'g[y].remove(x)': '无向图，两个方向都要删',
        'q = [x]': '从 `x = {x}` 出发做 BFS，目标是 `y = {y}`',
        'if nxt not in d': '`{nxt}` 到过吗？{nxt in d}：==没到过才记距离入队==',
        'd[nxt] = ': '`d[{nxt}] = d[{now}] + 1 = {d[nxt]}`',
        'head, tail = tail': '一层走完，下一层是新入队的 `q[{head}:{tail}]`',
        'if y in d': '这一层之后 `y` 到了吗？{y in d}。BFS 按层走，==第一次到就是最短==',
        'res = min': '删边后最短路 `d[{y}] = {d[y]}`，加上被删的边：环长 `{d[y]} + 1` = =={d[y]+1}==，`res = {res}`',
        30: '这条边处理完，把它加回图里（两个方向），再换下一条边',
        'if res == 1001': '`res` 还是 1001 才说明每条边都不在环上、要返回 -1；这里 `res = {res}`，有环',
        'return res': '最短环长 `{res}`',
    },
    skip=[6, 7, 'for x, y in edges', 'res = 1001', 'd = {}', 'd[x] = 0', 'g = {x'],
    max_steps=60,
    cards=dict(
        one_liner='枚举每条边：删掉它，看两端还能不能绕回去',
        complexity='时间 `O(m·(n+m))`，空间 `O(n + m)`',
        problem=['无向图，求最短环的长度，没有环返回 `-1`',
                 '数据规模小：`n, m ≤ 1000`',
                 '示例：`n=4`，边 `0-1, 1-2, 2-0, 2-3` → `3`'],
        quote='可以枚举每一条边，计算包含这条边的最短的环的长度。对于一条连接节点x和节点y的边，可以先将其从图中删去，然后从x出发，通过bfs寻找到达y的最短路。',
        quote_src='—— yiduobo 题解',
        idea=['无向图不像有向图好处理，但规模小，可以==逐边枚举==',
              '删掉边 x-y，从 x 做 BFS 找 y：最短路 + 被删的边 = 包含这条边的最短环',
              '所有边的结果取最小；BFS 层层推进，`y` 一出现就可以 `break`'],
        summary=['时间 `O(m·(n+m))`：m 条边各做一次 BFS',
                 '==每条边处理完要加回图中==，否则后面的边会少算',
                 '`res` 初值 1001 比任何可能的环都大，最后判断是否改过',
                 '原文为 Python 2 写法，本题无需改动，可直接在 Python 3 运行'],
    ),
)
