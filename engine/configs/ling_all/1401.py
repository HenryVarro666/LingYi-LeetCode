def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    xc, yc, R = S['xCenter'], S['yCenter'], S['radius']
    rx1, ry1, rx2, ry2 = S['x1'], S['y1'], S['x2'], S['y2']
    px, py = S.get('x'), S.get('y')
    cv.text((x0 + 18, y0 + 4), '圆（蓝）与矩形（灰）：矩形里离圆心最近的点 (x, y)', 24, T['muted'], bold=True)
    # 世界坐标 -> 画布
    wx0, wx1, wy0, wy1 = -2, 4, -2, 2
    top, bot = y0 + 60, y1 - 150
    sc = min((x1 - x0 - 80) / (wx1 - wx0), (bot - top) / (wy1 - wy0))
    ox = x0 + 40 + ((x1 - x0 - 80) - sc * (wx1 - wx0)) / 2
    oy = top + ((bot - top) - sc * (wy1 - wy0)) / 2

    def P(x, y):
        return ox + (x - wx0) * sc, oy + (wy1 - y) * sc

    for gx in range(wx0, wx1 + 1):
        X, _ = P(gx, 0)
        cv.line([(X, P(0, wy1)[1]), (X, P(0, wy0)[1])], T['border'], 1)
        cv.text((X, P(0, wy0)[1] + 6), gx, 18, T['dim'], anchor='mt', mono=True)
    for gy in range(wy0, wy1 + 1):
        _, Y = P(0, gy)
        cv.line([(P(wx0, 0)[0], Y), (P(wx1, 0)[0], Y)], T['border'], 1)
        cv.text((P(wx0, 0)[0] - 8, Y), gy, 18, T['dim'], anchor='rm', mono=True)
    cv.line([(P(0, wy1)[0], P(0, wy1)[1]), (P(0, wy0)[0], P(0, wy0)[1])], T['muted'], 2)
    cv.line([(P(wx0, 0)[0], P(wx0, 0)[1]), (P(wx1, 0)[0], P(wx1, 0)[1])], T['muted'], 2)
    # 矩形
    a, b = P(rx1, ry2), P(rx2, ry1)
    cv.rect((a[0], a[1], b[0], b[1]), fill=T['panel2'], outline=T['muted'], width=3)
    cv.text((a[0] + 8, a[1] + 6), f'矩形 [{rx1},{rx2}]×[{ry1},{ry2}]', 20, T['muted'], bold=True)
    # 圆
    cx, cy = P(xc, yc)
    cv.d.ellipse((cx - R * sc, cy - R * sc, cx + R * sc, cy + R * sc), outline=T['blue'], width=4)
    cv.d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=T['blue'])
    cv.text((cx, cy + R * sc + 8), f'圆心 ({xc},{yc})', 20, T['blue'], anchor='mt', bold=True)
    if px is not None:
        qx, qy = P(px, py if py is not None else yc)
        if py is not None:
            cv.dashed((cx, cy), (qx, qy), T['yellow'], 3)
            cv.d.ellipse((qx - 9, qy - 9, qx + 9, qy + 9), fill=T['yellow'])
            cv.text((qx + 14, qy - 14), f'({px},{py})', 22, T['yellow'], bold=True)
        else:
            # 只定了 x：画一条竖线
            cv.line([(qx, P(0, wy1)[1]), (qx, P(0, wy0)[1])], T['yellow'], 3)
    if px is not None and py is not None:
        d2 = (px - xc) ** 2 + (py - yc) ** 2
        ok = d2 <= R * R
        cv.text(((x0 + x1) / 2, y1 - 110),
                f'd² = ({px}−{xc})² + ({py}−{yc})² = {d2}    radius² = {R * R}', 28,
                T['green'] if ok else T['red'], anchor='mt', bold=True)
        cv.text(((x0 + x1) / 2, y1 - 64), ('d² ≤ radius² → 最近点在圆内，相交' if ok else 'd² > radius² → 最近点也在圆外，不相交'),
                28, T['green'] if ok else T['red'], anchor='mt', bold=True)


CONFIG = dict(
    num=1401, title='圆和矩形是否有重叠', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='矩形内最近点',
    tags=['计算几何', '难度分 1709'],
    code='''
class Solution:
    def checkOverlap(self, radius: int, xCenter: int, yCenter: int, x1: int, y1: int, x2: int, y2: int) -> bool:
        # 找到在矩形中的到圆心 (xCenter, yCenter) 最近的点 (x, y)
        x = max(x1, min(xCenter, x2))
        y = max(y1, min(yCenter, y2))

        # 判断 (x, y) 是否在圆中
        return (x - xCenter) ** 2 + (y - yCenter) ** 2 <= radius ** 2
''',
    call='Solution().checkOverlap(1, 0, 0, 1, -1, 3, 1)',
    expect=True,
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=[('x', 'x', 'yellow'), ('y', 'y', 'yellow'), ('radius', 'radius', 'blue'),
           ('d²', '(x - xCenter) ** 2 + (y - yCenter) ** 2 if "y" in S else "?"', 'orange')],
    captions={
        'x = max': '把 `xCenter = {xCenter}` ==修正==到 `[{x1}, {x2}]` 内：`min({xCenter}, {x2}) = {min(xCenter, x2)}`，再和 `{x1}` 取最大 → `x` = =={x}==（圆心在区间左侧，取左端点 `x1`）',
        'y = max': '`yCenter = {yCenter}` 已经在 `[{y1}, {y2}]` 内，不用修正 → `y` = =={y}==',
        'return': lambda S, B, ret: (f'`d² = ({S.x}−{S.xCenter})² + ({S.y}−{S.yCenter})² = {(S.x - S.xCenter) ** 2 + (S.y - S.yCenter) ** 2}`，'
                                     f'`radius² = {S.radius ** 2}` → 最近点在圆内，==相交==，返回 {ret}'),
    },
    cards=dict(
        after=[dict(heading='反过来：不相交的情况', lines=['示例 2：圆心 `(1,1)`，矩形 `(1,-3)–(2,-1)`', '`x` 取 `1`，`y` 被夹到 `-1`，`d² = 4 > 1`', '最近点都在圆外 → ==不相交==，返回 `false`'])],
        one_liner='先找矩形里离圆心最近的点，再看它在不在圆里',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['圆 `(radius, xCenter, yCenter)`，与坐标轴平行的矩形 `(x1, y1, x2, y2)`',
                 '有公共点（含边界）返回 `true`，否则 `false`',
                 '示例：`radius=1, (0,0), 矩形 (1,-1)–(3,1)` → `true`'],
        quote='找到在矩形中的到圆心 (xCenter, yCenter) 最近的点 (x, y)。判断点 (x, y) 是否在圆中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['矩形里离圆心最近的点，如果都不在圆内，其余点更不在',
              'x 和 y 互不影响：各自把圆心坐标==夹到==区间 `[x1,x2]`、`[y1,y2]` 里',
              '夹法：`max(x1, min(xCenter, x2))`，小了取 `x1`，大了取 `x2`，在里面就不动'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错：夹取要先 `min` 再 `max`，别写反；比较用 `<=`，擦边也算重叠',
                 '全程整数，用距离平方，不需要开根号',
                 '同类：计算几何里「点到线段/矩形的最近点」'],
    ),
)
