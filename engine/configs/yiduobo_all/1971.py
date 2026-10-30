POS = {0: (0.08, 0.50), 1: (0.28, 0.20), 2: (0.28, 0.80), 3: (0.50, 0.50), 4: (0.72, 0.50), 5: (0.90, 0.25), 6: (0.90, 0.80)}
EDGES = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (5, 6)]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '无向图（绿 = 起点，红 = 终点，蓝 = 已访问，蓝环 = now，粉环 = 正在看的 next）', 21, T['muted'], bold=True)
    W, H = x1 - x0 - 80, y1 - y0 - 100
    P = {k: (x0 + 40 + W * a, y0 + 64 + H * b) for k, (a, b) in POS.items()}
    for a, b in EDGES:
        cv.line([P[a], P[b]], T['border'], 4)
    used = S.get('used') or set()
    src, dst = S.get('source'), S.get('destination')
    now, nx = S.get('now'), S.get('next')
    nx = nx if isinstance(nx, int) else None
    inloop = 22 <= S.get('_line', 0) <= 27
    for k, (px, py) in P.items():
        fill = T['panel2']
        if k in used:
            fill = T['blue']
        if k == src:
            fill = T['green']
        if k == dst:
            fill = T['red'] if k not in used or k == dst else fill
        cv.rect((px - 34, py - 34, px + 34, py + 34), fill=fill, outline=T['border'], r=34)
        cv.text((px, py), k, 34, T['bg'] if fill != T['panel2'] else T['muted'], anchor='mm', bold=True)
        if k == now and 'l' in S and S['l'] > 0:
            cv.rect((px - 42, py - 42, px + 42, py + 42), outline=T['blue'], width=5, r=42)
        if k == nx and inloop and now is not None:
            cv.rect((px - 50, py - 50, px + 50, py + 50), outline=T['pink'], width=5, r=50)


CONFIG = dict(
    num=1971, title='寻找图中是否存在路径', difficulty='Easy', category='图论算法',
    author='yiduobo', technique='邻接表 + BFS', tags=['灵神题单·图论算法'],
    code='''
class Solution(object):
    def validPath(self, n, edges, source, destination):

        if source == destination:
            return True

        g = {x : set() for x in range(n)}
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)
        
        q = [source]
        l = 0
        r = 1
        used = set()
        used.add(source)

        while l < r:
            now = q[l]
            l += 1
            for next in g[now]:
                if next not in used:
                    if next == destination:
                        return True
                    used.add(next)
                    q.append(next)
                    r += 1

        return False
''',
    call='Solution().validPath(7, [[0,1],[0,2],[1,3],[2,3],[3,4],[5,6]], 0, 4)',
    expect=True,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var=lambda S: S.get('q'), label='q（BFS 队列，l 指向下一个出队的）', cell=90, h=200,
             pointers={'l': 'blue'}, dim=lambda S, i, v: i < S.get('l', 0)),
        dict(type='set', var='used', label='used（已访问的点）', h=110),
    ],
    watch=['source', 'destination', 'now', ('next', lambda S: S['next'] if isinstance(S.get('next'), int) else '-')],
    captions={
        'if source == destination': '起点就是终点吗？`{source} == {destination}` → 不是，要找路',
        'g = {x': '用字典存邻接表：`g[x]` 是和 x 相连的点集合',
        'g[x].add(y)': '无向边：`{x}` 记下 `{y}`',
        'g[y].add(x)': '反过来 `{y}` 也记下 `{x}`，两个方向都要加',
        'q = [source]': 'BFS 从起点出发：队列里先放 `{source}`',
        'used.add(source)': '起点标记为已访问，避免走回头路',
        'while l < r': lambda S, B, r: ('队列里还有点 → 继续往外扩' if S.l < S.r else '队列空了，所有能到的点都试过 → 到不了'),
        'now = q[l]': '出队：取出 `now = {now}`，看它能去哪',
        'if next not in used': lambda S, B, r: (f'`{S.next}` 没访问过 → 要处理' if S.next not in S.used else f'`{S.next}` 已访问过 → 跳过'),
        'if next == destination': lambda S, B, r: (f'`{S.next}` 就是终点 `{S.destination}`！' if S.next == S.destination else f'`{S.next}` 不是终点 `{S.destination}`，继续'),
        'return True': lambda S, B, r: ('找到终点 `{}`，起点能到终点 → ==True==' .format(S.get('destination'))),
        'used.add(next)': '`{next}` 标记已访问，==入队前就标记==，防止重复入队',
        'q.append(next)': '`{next}` 入队，之后从它继续扩展',
        'return False': '队列空了还没碰到终点 → ==False==',
    },
    skip=['l += 1', 'r += 1', 'l = 0', 'r = 1', 'used = set()'],
    cards=dict(
        one_liner='从起点 BFS，一层层扩展，碰到终点就返回 True',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['无向图有 `n` 个点（编号 0 到 n-1）和若干条边，给定起点 `source` 和终点 `destination`',
                 '判断能否从起点沿着边走到终点（题目原文未收录，按 LeetCode 1971 题意）',
                 '本视频：`n=7`，终点 `4`，从 `0` 出发 → `True`'],
        quote='比较基础的题目，有各式各样的方法。我在这里采用的是从start开始进行bfs，判断能否走到end。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用字典 + 集合建出邻接表，无向边要加两个方向',
              '队列 `q` 放待扩展的点，`used` 记录访问过的点',
              '每次出队一个点，把没访问过的邻居入队；邻居是终点就直接返回'],
        summary=['时间 `O(n + m)`，每个点和每条边最多处理一次',
                 '`source == destination` 要先特判，直接 `True`',
                 '入队时就标记 `used`，避免同一个点多次入队',
                 '队列用列表 + 头指针 `l`，`r` 是队尾；原文已是 Python 3 可运行写法'],
    ),
)
