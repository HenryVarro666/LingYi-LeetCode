BOMBS = [[0, 0, 5], [4, 0, 3], [7, 0, 4], [4, 6, 1]]
COLS = ['blue', 'pink', 'green', 'purple']


def _draw(cv, S, B, box, T):
    import math
    x0, y0, x1, y1 = box
    g = S.get('g')
    if g is None:
        return
    n = len(BOMBS)
    minx = min(x - r for x, y, r in BOMBS)
    maxx = max(x + r for x, y, r in BOMBS)
    miny = min(y - r for x, y, r in BOMBS)
    maxy = max(y + r for x, y, r in BOMBS)
    pad = 24
    hh = y1 - y0 - 2 * pad - 60
    sc = min((x1 - x0 - 2 * pad) / (maxx - minx), hh / (maxy - miny))
    ox = x0 + pad + ((x1 - x0 - 2 * pad) - sc * (maxx - minx)) / 2
    oy = y0 + 30 + pad + (hh - sc * (maxy - miny)) / 2

    def P(k):
        return ox + (BOMBS[k][0] - minx) * sc, oy + (maxy - BOMBS[k][1]) * sc

    used = S.get('used') or set()
    start = S.get('index') if 'q' in S else None
    now = S.get('now') if 'q' in S else None
    nxt = S.get('next') if 'q' in S else None
    cv.text((x0 + 16, y0 + 8), '炸弹平面（圆 = 爆炸范围，箭头 = 能引爆）', 20, T['dim'])
    for k, (x, y, r) in enumerate(BOMBS):
        X, Y = P(k)
        cv.d.ellipse((X - r * sc, Y - r * sc, X + r * sc, Y + r * sc), outline=T[COLS[k]], width=2)
    for i in range(n):
        for j in g.get(i, ()):
            (ax, ay), (bx, by) = P(i), P(j)
            d = math.hypot(bx - ax, by - ay)
            ux, uy = (bx - ax) / d, (by - ay) / d
            hot = now == i and nxt == j
            cv.arrow((ax + ux * 22 - uy * 8, ay + uy * 22 + ux * 8), (bx - ux * 26 - uy * 8, by - uy * 26 + ux * 8),
                     T['yellow'] if hot else T['muted'], 5 if hot else 3, 14)
    for k in range(n):
        X, Y = P(k)
        inu = k in used
        ring = T['yellow'] if k == now else (T['blue'] if k == start else None)
        cv.d.ellipse((X - 20, Y - 20, X + 20, Y + 20), fill=T['green'] if inu else T[COLS[k]], outline=ring,
                     width=5 if ring else 1)
        cv.text((X, Y), k, 24, T['bg'], anchor='mm', bold=True)
    cv.text((x0 + 16, y1 - 22), '绿 = 本轮已引爆（used），蓝圈 = 起点，黄圈 = 正在扩展的 now', 18, T['dim'], anchor='lm')


def _pr(S, B, ret):
    nx = S.next
    if nx in B.used:
        return f'`{nx}` 已经在 `used` 里 → 这轮已经引爆过，跳过'
    return f'`{nx}` 不在 `used` 里 → 新引爆的炸弹，加入 used 和队列'


CONFIG = dict(
    num=2101, title='引爆最多的炸弹', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='两两判断建有向图 · 枚举起点 BFS',
    tags=['灵神题单', '图论算法', '难度分 1880'],
    code='''
class Solution(object):
    def maximumDetonation(self, bombs):

        n = len(bombs)
        g = {index : set() for index in range(n)}
        for i in range(n - 1):
            for j in range(i + 1, n):
                x1, y1, r1 = bombs[i]
                x2, y2, r2 = bombs[j]
                pow_d = (x1 -x2) ** 2 + (y1 - y2) ** 2
                if pow_d <= r1 * r1:
                    g[i].add(j)
                if pow_d <= r2 * r2:
                    g[j].add(i)
        
        res = 0
        for index in range(n):
            q = [index]
            used = set([index])
            l = 0
            r = 1
            while l < r:
                now = q[l]
                l += 1
                for next in g[now]:
                    if next not in used:
                        used.add(next)
                        q.append(next)
                        r += 1
            
            res = max(res, len(q))
        
        return res
''',
    call=f'Solution().maximumDetonation({BOMBS})',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='queue', var='q', label='q（BFS 队列）', h=130),
        dict(type='text', fn=lambda S: f"`res` = =={S['res']}==（本轮已引爆 `{len(S['q'])}` 个）" if 'res' in S and 'q' in S else '', h=70),
    ],
    watch=[('index', 'index', 'blue'), ('now', lambda S: S.get('now'), 'yellow'), ('res', 'res', 'green')],
    skip=['n = len', 'for i in range(n - 1)', 'for j in range(i + 1', 'x1, y1, r1 =', 'x2, y2, r2 =', 'l = 0', 'r = 1',
          'l += 1', 'r += 1', 'for next in g[now]', 'q = [index]', 'for index in range(n)', 'while l < r', 'used.add'],
    max_steps=90,
    captions={
        'g = {index': '`g[i]` = 炸弹 i 能直接引爆的炸弹集合（先全是空集合）',
        'pow_d =': '`({x1}−{x2})² + ({y1}−{y2})²` = =={pow_d}==：炸弹 {i}、{j} 圆心距离的平方',
        'if pow_d <= r1 * r1': lambda S, B, ret: (f'`{S.pow_d} ≤ r1² = {S.r1 * S.r1}` → {S.i} 能引爆 {S.j}' if S.pow_d <= S.r1 * S.r1
                                                  else f'`{S.pow_d} > r1² = {S.r1 * S.r1}` → {S.i} 引爆不了 {S.j}'),
        'g[i].add(j)': '建边 `{i} → {j}`：`g[{i}] = {g[i]}`',
        'if pow_d <= r2 * r2': lambda S, B, ret: (f'`{S.pow_d} ≤ r2² = {S.r2 * S.r2}` → {S.j} 能引爆 {S.i}' if S.pow_d <= S.r2 * S.r2
                                                  else f'`{S.pow_d} > r2² = {S.r2 * S.r2}` → {S.j} 引爆不了 {S.i}'),
        'g[j].add(i)': '建边 `{j} → {i}`：`g[{j}] = {g[j]}`',
        'res = 0': '`res = 0`：记录引爆一个炸弹后，最多能引爆几个',
        'used = set': '引爆炸弹 `{index}`：`used` 记录这轮引爆过的炸弹',
        'now = q[l]': '取队头 `now = {now}`：它爆炸，看它能引爆谁',
        'if next not in used': _pr,
        'q.append(next)': '`{next}` 被引爆，入队后它也会继续引爆别的：`q = {q}`',
        'res = max': '从炸弹 `{index}` 出发共引爆 `{len(q)}` 个 → `res = max({B.res}, {len(q)})` = =={res}==',
        'return res': '最多能引爆 `{ret}` 个炸弹',
    },
    cards=dict(
        one_liner='引爆关系是有向图：对每个炸弹 BFS，数能到达几个',
        complexity='时间 `O(n³)`，空间 `O(n²)`',
        problem=['炸弹 `[x, y, r]`：引爆一个炸弹，圆内的炸弹也会爆炸，并继续连锁',
                 '选一个炸弹引爆，最多能引爆多少个？',
                 '本视频：4 个炸弹，`0→1→2` 连锁，3 号孤立，答案 `3`'],
        quote='一个炸弹x可以引爆另一个炸弹y的条件是x和y之间的距离小于等于x的爆炸范围，那么就可以通过两两枚举所有的炸弹对，判断炸弹之间是否能互相引爆。',
        quote_src='—— yiduobo 题解原文',
        idea=['两两枚举 `(i, j)`：圆心距离² 和各自的半径² 比一比，==两个方向分别判断==',
              '结果是有向图：炸弹 → 它能直接引爆的炸弹',
              '枚举起点 BFS 数访问个数，取最大。原文还提到 tarjan 缩点 + 拓扑 DP 的 `O(n²)` 做法'],
        summary=['时间 `O(n³)`（n 个起点，每次 BFS 最坏 `O(n²)`），空间 `O(n²)`',
                 '==比较平方，不要开根号==，避免浮点误差',
                 '`i→j` 和 `j→i` 要分别用 r1、r2 判断：半径不同，关系不对称',
                 '`used` 防止重复入队；起点自己也算 1 个',
                 '对比灵神：灵神用位集合 Floyd 求传递闭包，yiduobo 对每个起点 BFS'],
    ),
)
