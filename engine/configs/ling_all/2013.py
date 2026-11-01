N = 7  # 画 0..6 的坐标范围


def _pts(S):
    col = S.get('self.col')
    out = {}
    if col is not None:
        for x, c in enumerate(col[:N]):
            for y, v in c.items():
                if v and 0 <= y < N:
                    out[(x, y)] = v
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '点（数字 = 重复个数，蓝 = 查询点，黄框 = 要查的角）', 22, T['muted'], bold=True)
    cell = min(80, (x1 - x0 - 90) / N, (y1 - y0 - 110) / N)
    gx, gy = x0 + 60, y0 + 50
    base = gy + cell * (N - 1)
    pos = lambda x, y: (gx + x * cell, base - y * cell)
    for i in range(N):
        cv.line([pos(0, i), pos(N - 1, i)], T['border'], 1)
        cv.line([pos(i, 0), pos(i, N - 1)], T['border'], 1)
        cv.text((gx + i * cell, base + 14), i, 18, T['dim'], anchor='mt', mono=True)
        cv.text((gx - 14, base - i * cell), i, 18, T['dim'], anchor='rm', mono=True)
    pts = _pts(S)
    live = 'ans' in S and 'x' in S and 'y' in S and 'x2' in S and 'd' in S
    cand = set()
    if live and S.get('d') is not None:
        x, y, x2, d = S['x'], S['y'], S['x2'], S['d']
        if S['_line'] == 17:
            cand = {(x, y - d), (x2, y - d)}
        elif S['_line'] == 18:
            cand = {(x, y + d), (x2, y + d)}
        cv.line([pos(x, y), pos(x2, y)], T['yellow'], 4)
    q = (S['x'], S['y']) if 'ans' in S and 'x' in S else None
    for (px, py), v in pts.items():
        X, Y = pos(px, py)
        c = T['cyan'] if (px, py) == q else T['green']
        cv.rect((X - 17, Y - 17, X + 17, Y + 17), fill=c, r=17)
        cv.text((X, Y), v, 22, T['bg'], anchor='mm', bold=True)
    for (px, py) in cand:
        if 0 <= px < N and 0 <= py < N:
            X, Y = pos(px, py)
            cv.rect((X - 22, Y - 22, X + 22, Y + 22), outline=T['yellow'], width=4, r=22)
    if q and q not in pts:
        X, Y = pos(*q)
        cv.rect((X - 17, Y - 17, X + 17, Y + 17), outline=T['cyan'], width=4, r=17)


CONFIG = dict(
    num=2013, title='检测正方形', difficulty='Medium', category='设计',
    author='灵茶山艾府', technique='哈希表 · 枚举同行的点当对角线邻点（Go 原文转写）',
    code='''
class DetectSquares:
    def __init__(self):
        self.row = [[] for _ in range(1001)]
        self.col = [Counter() for _ in range(1001)]

    def add(self, point: List[int]) -> None:
        x, y = point[0], point[1]
        self.row[y].append(x)
        self.col[x][y] += 1

    def count(self, point: List[int]) -> int:
        x, y = point[0], point[1]
        ans = 0
        for x2 in self.row[y]:
            if x2 != x:
                d = abs(x2 - x)  # 横向距离
                ans += self.col[x][y - d] * self.col[x2][y - d]  # 将 x-x2 当作正方形顶边两个点，计算正方形底边两点的组合方案
                ans += self.col[x][y + d] * self.col[x2][y + d]  # 将 x-x2 当作正方形底边两个点，计算正方形顶边两点的组合方案
        return ans
''',
    call='''d = DetectSquares()
out = []
d.add([1, 5])
d.add([4, 2])
d.add([1, 2])
out.append(d.count([4, 5]))
out.append(d.count([6, 3]))
d.add([4, 2])
out.append(d.count([4, 5]))
out''',
    expect=[1, 0, 2],
    max_steps=90,
    snap_maxlen=8,
    views=[dict(type='custom', draw=_draw, h=560)],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), 'x2', 'd', ('ans', 'ans', 'green')],
    captions={
        'self.row = ': '`row[y]` 记录纵坐标为 y 的所有点的横坐标（有重复就多记几次）',
        'self.col = ': '`col[x][y]` 记录坐标 `(x, y)` 上点的个数',
        'self.row[y].append': '点 `({x}, {y})` 加入第 `{y}` 行的列表',
        'self.col[x][y] += 1': '坐标 `({x}, {y})` 的点数 → `{self.col[x][y]}`',
        'ans = 0': lambda S, B, r: f'查询点 `({S.x}, {S.y})`，`ans = 0`',
        'for x2 in self.row[y]': lambda S, B, r: (f'枚举和查询点同一行的点：`x2 = {S.x2}`' if 'x2' in S and S.x2 != B.get('x2') else '同一行的点枚举完了'),
        'if x2 != x': lambda S, B, r: (f'`x2 = {S.x2}` ≠ `x = {S.x}`：和查询点不重合，可当正方形的一条边' if S.x2 != S.x else f'`x2 = {S.x2}` 就是查询点自己的列 → 边长为 0，跳过'),
        'd = abs': '横向距离 `d = |{x2} - {x}|` = =={d}==，也就是正方形边长',
        'self.col[x][y - d]': '这条边当顶边，底边在 `y - d = {y - d}`：`col[{x}][{y - d}] × col[{x2}][{y - d}]` = `{self.col[x][y - d]} × {self.col[x2][y - d]}` → `ans` = =={ans}==',
        'self.col[x][y + d]': '这条边当底边，顶边在 `y + d = {y + d}`：`col[{x}][{y + d}] × col[{x2}][{y + d}]` = `{self.col[x][y + d]} × {self.col[x2][y + d]}` → `ans` = =={ans}==',
        'return ans': '查询点能构成的正方形数：`{ans}`',
    },
    cards=dict(
        one_liner='查询点定一条水平边，边长定了，上下两侧各查一次',
        complexity='`add` 为 `O(1)`，`count` 为 `O(同一行的点数)`',
        problem=['点不断加入（可重复），每次查询：选三个已有的点和查询点组成面积为正的轴对齐正方形，求方案数',
                 '本视频：加入 `(1,5) (4,2) (1,2)`，查 `(4,5)` → `1`；再查 `(6,3)` → `0`；再加 `(4,2)`，查 `(4,5)` → `2`'],
        quote='将 x-x2 当作正方形顶边两个点，计算正方形底边两点的组合方案',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['`row[y]` 存每一行的点，`col[x][y]` 存坐标上有几个点',
              '查询 `(x, y)`：枚举同一行的点 `x2`，横向距离 `d` 就是边长',
              '正方形在这条边的上方或下方：`col[x][y±d] × col[x2][y±d]`，乘法原理算重复点'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（Go 用全局数组，这里放在 `self` 上；`map[int]int` 用 `Counter`，读不存在的键得 0 且不插入）',
                 '`count` 复杂度 `O(同一行点数)`，空间 `O(点数)`',
                 '易错点：`x2 != x` 排除边长为 0；重复的点要靠乘法计入',
                 '视频里坐标缩小到 0~6，原题范围是 0~1000（所以数组长 1001）'],
    ),
)
