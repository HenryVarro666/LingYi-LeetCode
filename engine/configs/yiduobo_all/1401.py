def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    xc, yc, R = S['x_center'], S['y_center'], S['radius']
    rx1, ry1, rx2, ry2 = S['x1'], S['y1'], S['x2'], S['y2']
    px, py = S.get('x'), S.get('y')
    cv.text((x0 + 18, y0 + 4), '圆（蓝）与矩形（灰）：按三种情况选出的点 (x, y)', 24, T['muted'], bold=True)
    # 世界坐标 -> 画布
    wx0, wx1, wy0, wy1 = -1, 3, -3, 2
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
    author='yiduobo', technique='分情况选最近点',
    tags=['计算几何', '难度分 1709'],
    code='''
class Solution(object):
    def checkOverlap(self, radius, x_center, y_center, x1, y1, x2, y2):

        if x2 < x_center:
            x = x2
        elif x1 > x_center:
            x = x1
        else:
            x = x_center

        if y2 < y_center:
            y = y2
        elif y1 > y_center:
            y = y1
        else:
            y = y_center

        return (x - x_center) ** 2 + (y - y_center) ** 2 <= radius * radius
''',
    call='Solution().checkOverlap(1, 1, 1, 1, -3, 2, -1)',
    expect=False,
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=[('x', 'x', 'yellow'), ('y', 'y', 'yellow'), ('radius', 'radius', 'blue'),
           ('d²', '(x - x_center) ** 2 + (y - y_center) ** 2 if "y" in S else "?"', 'orange')],
    captions={
        'if x2 < x_center': '矩形右边 `x2 = {x2}` 在圆心 `{x_center}` 左边吗？{"是，圆心在矩形右侧" if x2 < x_center else "不是，继续看左边"}',
        'x = x2': '圆心在右 → 取右端 `x2`，`x` = =={x}==',
        'elif x1 > x_center': '矩形左边 `x1 = {x1}` 在圆心 `{x_center}` 右边吗？{"是，圆心在矩形左侧" if x1 > x_center else "不是，圆心夹在 x1 和 x2 之间"}',
        'x = x1': '圆心在左 → 取左端 `x1`，`x` = =={x}==',
        'x = x_center': '`{x1} ≤ {x_center} ≤ {x2}`：直接取圆心的 `x`，平方项为 0 → `x` = =={x}==',
        'if y2 < y_center': '矩形上边 `y2 = {y2}` 比圆心 `{y_center}` 低吗？{"是，圆心在矩形上方" if y2 < y_center else "不是，继续看下边"}',
        'y = y2': '圆心在上方 → 取上边 `y2`，`y` = =={y}==',
        'elif y1 > y_center': '矩形下边 `y1 = {y1}` 比圆心 `{y_center}` 高吗？{"是，圆心在矩形下方" if y1 > y_center else "不是，圆心夹在 y1 和 y2 之间"}',
        'y = y1': '圆心在下方 → 取下边 `y1`，`y` = =={y}==',
        'y = y_center': '圆心的 `y` 已在 `[{y1}, {y2}]` 内 → `y` = =={y}==',
        'return': lambda S, B, ret: (f'`d² = ({S.x}−{S.x_center})² + ({S.y}−{S.y_center})² = {(S.x - S.x_center) ** 2 + (S.y - S.y_center) ** 2}`，'
                                     f'`radius² = {S.radius * S.radius}` → 最近点也在圆外，==不相交==，返回 {ret}'),
    },
    cards=dict(
        one_liner='圆里有个点同时在矩形里，那就选最靠近圆心的那个',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['圆 `(radius, x_center, y_center)`，矩形左下 `(x1,y1)`、右上 `(x2,y2)`',
                 '圆和矩形有公共点（含边界）返回 `true`',
                 '示例：圆心 `(1,1)` 半径 `1`，矩形 `(1,-3)–(2,-1)` → `false`'],
        quote='我们希望那两个非负项越小越好，也就是当x越接近x_center，y越接近y_center时，不等式越有可能成立。',
        quote_src='—— yiduobo 题解原文',
        idea=['重叠 = 存在点 `(x,y)` 满足圆不等式，同时 `x1≤x≤x2`、`y1≤y≤y2`',
              '圆不等式是两个平方项之和，越小越容易成立 → `x`、`y` 尽量靠近圆心',
              '对 `x` 分三种情况：圆心在左取 `x1`，在右取 `x2`，在中间取 `x_center`；`y` 同理'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错：三种情况别漏掉「圆心在区间内」，此时平方项直接为 0',
                 '最后用 `<=`，擦边相切也算重叠',
                 '原文为 Python 2 风格，这里只用到整数运算，代码未改动',
                 '对比灵神：灵神一行 `max(x1, min(x, x2))` 夹取，yiduobo 用 if/elif 分情况'],
    ),
)
