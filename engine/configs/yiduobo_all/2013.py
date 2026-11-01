N = 7  # 画 0..6 的坐标范围


def _pts(S):
    col = S.get('self.point_dict')
    out = {}
    if col is not None:
        for x, c in col.items():
            for y, v in c.items():
                if v and 0 <= x < N and 0 <= y < N:
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
    live = 'res' in S and 'y2' in S and 'x' in S and 'y' in S
    cand = set()
    if live:
        x, y, y2 = S['x'], S['y'], S['y2']
        d = abs(y - y2)
        cv.line([pos(x, y), pos(x, y2)], T['yellow'], 4)
        if S['_line'] in (22, 23):
            cand = {(x - d, y), (x - d, y2)}
        elif S['_line'] in (25, 26):
            cand = {(x + d, y), (x + d, y2)}
    q = (S['x'], S['y']) if 'res' in S and 'x' in S else None
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
    author='yiduobo', technique='哈希表计数 · 枚举同列的点定边长',
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
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), 'y2', ('res', 'res', 'green')],
    captions={
        'self.point_dict = {}': '`point_dict[x][y]`：横坐标 x、纵坐标 y 的位置上有几个点',
        8: lambda S, B, r: ('`x` 这一列还没有点 → 要先建一个空字典' if S.x not in S['self.point_dict'] else '`x` 这一列已经有点了'),
        14: lambda S, B, r: ('查询点这一列有点，继续' if S.x in S['self.point_dict'] else '查询点这一列没有点'),
        'self.point_dict[x] = {}': '新建第 `{x}` 列的字典',
        'self.point_dict[x][y] = ': '坐标 `({x}, {y})` 的点数 → `{self.point_dict[x][y]}`',
        'for y2 in self.point_dict[x]': lambda S, B, r: (f'枚举和查询点同一列的点：`y2 = {S.y2}`，边长就是 `|y - y2|`' if 'y2' in S and S.y2 != B.get('y2') else '同一列的点枚举完了'),
        'if y2 == y': lambda S, B, r: (f'`y2 = {S.y2}` 就是查询点自己的位置，边长为 0 → 跳过' if S.y2 == S.y else f'`y2 = {S.y2}` ≠ `y = {S.y}`：边长 `|{S.y} - {S.y2}|` = =={abs(S.y - S.y2)}=='),
        'if x - abs(y - y2) in self.point_dict': '正方形在左边：另一列是 `x - 边长` = `{x - abs(y - y2)}`，那一列有点吗？',
        'res += self.point_dict[x][y2] * self.point_dict[x - abs': '左边：`({x}, {y2})` 有 `{self.point_dict[x][y2]}` 个 × `({x - abs(y - y2)}, {y})` × `({x - abs(y - y2)}, {y2})` → `res` = =={res}==',
        'if x + abs(y - y2) in self.point_dict': '正方形在右边：另一列是 `x + 边长` = `{x + abs(y - y2)}`，那一列有点吗？',
        'res += self.point_dict[x][y2] * self.point_dict[x + abs': '右边：三个角的个数相乘 → `res` = =={res}==',
        'return res': '查询点能构成的正方形数：`{res}`',
        'return 0': '查询点所在的列没有任何点，不可能构成正方形 → `0`',
    },
    cards=dict(
        one_liner='以同列的点定边长，正方形只会向左或向右长出去',
        complexity='`add` 为 `O(1)`，`count` 为 `O(同一列的点数)`',
        problem=['点不断加入（可重复），每次查询：选三个已有的点和查询点组成面积为正的轴对齐正方形，求方案数',
                 '本视频：加入 `(1,5) (4,2) (1,2)`，查 `(4,5)` → `1`；再查 `(6,3)` → `0`；再加 `(4,2)`，查 `(4,5)` → `2`'],
        quote='可以枚举与该点的横坐标相同的点，其坐标可以写作(x, y2)。这两个点纵坐标之差就是正方形的边长，即abs(y - y2)。',
        quote_src='—— yiduobo 题解原文',
        idea=['`point_dict[x][y]` 记录每个坐标上的点数',
              '查询 `(x, y)`：枚举同一列的点 `(x, y2)`，边长 `|y - y2|`',
              '另外两个点在 `x - 边长` 或 `x + 边长` 那一列，纵坐标仍是 `y`、`y2`；三个角的个数相乘'],
        summary=['`add` 为 `O(1)`，`count` 为 `O(同一列点数)`',
                 '易错点：`y2 == y` 要跳过（边长为 0）；左右两侧都要查，重复的点靠乘法计入',
                 '对比灵神：灵神枚举同一行、查上下两侧；yiduobo 枚举同一列、查左右两侧，二者对称',
                 '原文无需改动，直接可在 Python 3 运行；视频里坐标缩小到 0~6'],
    ),
)
