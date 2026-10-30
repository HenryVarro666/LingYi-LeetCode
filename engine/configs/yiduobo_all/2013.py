XMAX, YMAX = 6, 5


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pd = S.get('self.point_dict') or {}
    cv.text((x0 + 18, y0 + 4), '平面上的点（粉圈 = 查询点，橙 = (x, y2)，虚线 = 候选正方形）', 22, T['muted'], bold=True)
    cell = min((x1 - x0 - 120) / (XMAX + 1), (y1 - y0 - 110) / (YMAX + 1))
    ox, oy = x0 + 70, y1 - 50

    def P(a, b):
        return ox + a * cell, oy - b * cell
    for a in range(XMAX + 1):
        X, _ = P(a, 0)
        cv.line([(X, oy + 8), (X, oy - YMAX * cell - 8)], T['border'], 1)
        cv.text((X, oy + 14), a, 18, T['dim'], anchor='mt', mono=True)
    for b in range(YMAX + 1):
        _, Y = P(0, b)
        cv.line([(ox - 8, Y), (ox + XMAX * cell + 8, Y)], T['border'], 1)
        cv.text((ox - 16, Y), b, 18, T['dim'], anchor='rm', mono=True)
    live = 'y2' in S and 'res' in S and 'x' in S and 'y' in S
    qx = S.get('x') if 'res' in S or S.get('_line') is not None else None
    qy = S.get('y')
    # 候选正方形（虚线）
    if live:
        x, y, y2 = S['x'], S['y'], S['y2']
        d = abs(y - y2)
        for sx in (x - d, x + d):
            if sx in pd:
                a = [P(x, y), P(sx, y), P(sx, y2), P(x, y2)]
                for k in range(4):
                    cv.dashed(a[k], a[(k + 1) % 4], T['yellow'], 3)
    for a, col in pd.items():
        for b, c in col.items():
            X, Y = P(a, b)
            fill = T['cyan']
            if live and a == S['x'] and b == S['y2']:
                fill = T['orange']
            cv.rect((X - 20, Y - 20, X + 20, Y + 20), fill=fill, r=20)
            cv.text((X, Y), c, 24, T['bg'], anchor='mm', bold=True)
    if live or ('point' in S and 'res' in S):
        a, b = (S['x'], S['y']) if 'x' in S else (S['point'][0], S['point'][1])
        X, Y = P(a, b)
        cv.rect((X - 22, Y - 22, X + 22, Y + 22), outline=T['pink'], width=5, r=22)
        cv.text((X, Y - 30), f'({a},{b})', 20, T['pink'], anchor='mb', bold=True)


def _sq(S, B, r):
    x, y, y2 = S.x, S.y, S.y2
    d = abs(y - y2)
    return f'边长 `|{y} − {y2}|` = `{d}`'


def _side(sign):
    def f(S, B, r):
        x, y, y2 = S.x, S.y, S.y2
        d = abs(y - y2)
        sx = x + sign * d
        pd = S['self.point_dict']
        name = '右边' if sign > 0 else '左边'
        if sx not in pd:
            return f'{name}的竖线 `x = {sx}` 上没有点 → 这一侧凑不成正方形'
        a, b = pd[sx].get(y, 0), pd[sx].get(y2, 0)
        return f'{name} `x = {sx}`：`({sx},{y})` 有 {a} 个，`({sx},{y2})` 有 {b} 个 → 乘起来 `{pd[x][y2]}×{a}×{b}` = =={pd[x][y2] * a * b}=='
    return f


CONFIG = dict(
    num=2013, title='检测正方形', difficulty='Medium', category='设计',
    author='yiduobo', technique='两层哈希表 · 枚举同竖线的点',
    tags=['哈希表'],
    code='''
class DetectSquares(object):

    def __init__(self):
        self.point_dict = {}

    def add(self, point):
        x, y = point
        if x not in self.point_dict:
            self.point_dict[x] = {}
        self.point_dict[x][y] = self.point_dict[x].get(y, 0) + 1

    def count(self, point):
        x, y = point
        if x not in self.point_dict:
            return 0

        res = 0
        for y2 in self.point_dict[x]:
            if y2 == y:
                continue

            if x - abs(y - y2) in self.point_dict:
                res += self.point_dict[x][y2] * self.point_dict[x - abs(y - y2)].get(y, 0) * self.point_dict[x - abs(y - y2)].get(y2, 0)
            
            if x + abs(y - y2) in self.point_dict:
                res += self.point_dict[x][y2] * self.point_dict[x + abs(y - y2)].get(y, 0) * self.point_dict[x + abs(y - y2)].get(y2, 0)
        
        return res
''',
    call='''d = DetectSquares()
out = []
d.add([1, 3])
d.add([3, 1])
d.add([1, 1])
out.append(d.count([3, 3]))
out.append(d.count([3, 4]))
d.add([3, 1])
out.append(d.count([3, 3]))
out''',
    expect=[1, 0, 2],
    views=[
        dict(type='custom', draw=_draw, h=480),
        dict(type='map', var='self.point_dict', label='point_dict：x → {y: 个数}', fmt=lambda k, v: f'x={k}: {v}', h=115, font=26),
        dict(type='calls', label='正在执行', h=95),
    ],
    watch=['point', 'x', 'y', 'y2', ('res', 'res', 'green')],
    captions={
        'self.point_dict = {}': '`point_dict`：先按横坐标 `x` 分组，里面 `y → 该坐标点的个数`',
        'x, y = point': '取出坐标 `x = {x}`，`y = {y}`',
        8: lambda S, B, r: (f'`x = {S.x}` 是新的横坐标 → 先开一个空字典' if S.x not in S['self.point_dict']
                            else f'`x = {S.x}` 这条竖线已经有点了'),
        14: lambda S, B, r: (f'`x = {S.x}` 这条竖线上没有任何点 → 凑不成正方形，返回 0' if S.x not in S['self.point_dict']
                             else f'竖线 `x = {S.x}` 上有点，可以枚举'),
        9: '开一个空字典，用来装这个 `x` 上各个 `y` 的个数',
        10: '==add==：`({x},{y})` 的个数 +1 → `{self.point_dict[x][y]}`（重复点也计数）',
        'return 0': '返回 `0`',
        'res = 0': '==count=={point}：累计方案数 `res = 0`',
        'for y2 in self.point_dict[x]': '枚举同一竖线上的点 `({x}, {y2})`：它和查询点是正方形的一条竖边',
        'if y2 == y': lambda S, B, r: (f'`y2 = {S.y2}` 就是查询点自己的纵坐标 → 边长为 0，跳过' if S.y2 == S.y
                                       else f'`y2 = {S.y2} ≠ {S.y}`：{_sq(S, B, r)}'),
        'continue': '跳过',
        'if x - abs(y - y2) in self.point_dict': lambda S, B, r: (lambda sx: f'向左凑正方形：看 `x − 边长 = {sx}` 这条竖线' + ('，有点 → 去数个数' if sx in S['self.point_dict'] else '，没有点 → 跳过'))(S.x - abs(S.y - S.y2)),
        'if x + abs(y - y2) in self.point_dict': lambda S, B, r: (lambda sx: f'向右凑正方形：看 `x + 边长 = {sx}` 这条竖线' + ('，有点 → 去数个数' if sx in S['self.point_dict'] else '，没有点 → 跳过'))(S.x + abs(S.y - S.y2)),
        'res += self.point_dict[x][y2] * self.point_dict[x - abs': lambda S, B, r: _side(-1)(S, B, r) + f'；`res = {S.res}`',
        'res += self.point_dict[x][y2] * self.point_dict[x + abs': lambda S, B, r: _side(1)(S, B, r) + f'；`res = {S.res}`',
        'return res': '`count` 返回 `{res}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='固定查询点所在竖线，枚举另一端点，左右各找一条竖边',
        complexity='`add` 为 `O(1)`，`count` 为 `O(同一竖线上不同点数)`',
        problem=['点流：`add([x, y])` 加点（可重复），`count([x, y])` 统计与它构成面积为正的轴对齐正方形的方案数',
                 '示例：加 `(3,10)(11,2)(3,2)`，`count(11,10)` → `1`',
                 '本视频：加 `(1,3)(3,1)(1,1)`，`count(3,3)` → `1`，`count(3,4)` → `0`，再加一个 `(3,1)` 后 `count(3,3)` → `2`'],
        quote='可以枚举与该点的横坐标相同的点，其坐标可以写作(x, y2)。这两个点纵坐标之差就是正方形的边长，即abs(y - y2)。',
        quote_src='—— yiduobo 题解原文',
        idea=['轴对齐 → 查询点 `(x, y)` 与同竖线的点 `(x, y2)` 决定边长 `d = |y − y2|`',
              '另外两个点只能在 `x − d` 或 `x + d` 这条竖线上：`(x±d, y)` 和 `(x±d, y2)`',
              '哈希表存每个坐标的点数，三个点的个数相乘就是方案数（重复点各算各的）'],
        summary=['`add` `O(1)`；`count` 枚举同一竖线上的点，至多 `O(1000)`',
                 '易错：`y2 == y` 要跳过，面积必须为正',
                 '易错：重复点要计数，`d` 的两侧都要算，方案数是三个个数的==乘积==',
                 '原文已是 Python 3 可运行写法，未改动'],
    ),
)
