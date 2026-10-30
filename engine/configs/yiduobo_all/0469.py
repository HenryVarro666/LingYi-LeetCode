import functools as _ft

PTS = [[0, 0], [0, 10], [10, 10], [10, 0], [5, 5]]


def _cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - b[1]) - (c[0] - b[0]) * (b[1] - a[1])


def _plot(cv, S, B, box, T):
    x0, y0, x1_, y1_ = box
    cv.text((x0 + 18, y0 + 4), '点（黄 = 最左点 left，蓝 = 按极角排序后的编号，粉 = 当前检查的三点）', 22, T['muted'], bold=True)
    gx0, gy0, gx1, gy1 = x0 + 60, y0 + 70, x1_ - 60, y1_ - 50
    xs = [p[0] for p in PTS]
    ys = [p[1] for p in PTS]
    s = min((gx1 - gx0) / (max(xs) - min(xs) + 2), (gy1 - gy0) / (max(ys) - min(ys) + 2))

    def P(x, y):
        return gx0 + (x - min(xs) + 1) * s, gy1 - (y - min(ys) + 1) * s
    for xx in range(min(xs), max(xs) + 1, 5):
        cv.line([P(xx, min(ys) - 1), P(xx, max(ys) + 1)], T['border'], 1)
        cv.text((P(xx, min(ys) - 1)[0], gy1 + 6), xx, 18, T['dim'], anchor='mt', mono=True)
    for yy in range(min(ys), max(ys) + 1, 5):
        cv.line([P(min(xs) - 1, yy), P(max(xs) + 1, yy)], T['border'], 1)
        cv.text((gx0 - 10, P(0, yy)[1]), yy, 18, T['dim'], anchor='rm', mono=True)
    sp = S.get('sorted_points')
    left = S.get('left')
    line = S.get('_line', 0)
    l1, l2 = S.get('last_one'), S.get('last_two')
    pt = S.get('point')
    if sp is not None and left is not None:
        for a, b in zip([left] + sp, sp):
            cv.line([P(*a), P(*b)], T['blue'], 2)
        if len(sp) > 1:
            cv.line([P(*sp[-1]), P(*left)], T['blue'], 2)
    if l1 is not None and l2 is not None and pt is not None and line >= 40:
        c = _cross(l1, l2, pt)
        col = T['red'] if c > 0 else T['green']
        cv.line([P(*l1), P(*l2), P(*pt)], col, 5)
    for q in S['points']:
        px, py = P(*q)
        col, r = T['text'], 13
        if left is not None and q == left:
            col, r = T['yellow'], 17
        elif pt is not None and q in (l1, l2, pt) and line >= 40:
            col, r = T['pink'], 17
        cv.rect((px - r, py - r, px + r, py + r), fill=col, r=r)
        lab = f'({q[0]},{q[1]})'
        if sp is not None and q in sp:
            lab = f'#{sp.index(q) + 1} ' + lab
        cv.text((px + 20, py - 28), lab, 18, T['blue'] if sp is not None and q in sp else T['muted'], mono=True)


def _turn(S):
    l1, l2, pt = S.get('last_one'), S.get('last_two'), S.get('point')
    if l1 is not None and l2 is not None and pt is not None and S.get('_line', 0) >= 40:
        c = _cross(l1, l2, pt)
        return f'叉积 Xmul({l1}, {l2}, {pt}) = {c}  →  ' + ('大于 0：向左拐，有点被丢弃' if c > 0 else '不大于 0：向右拐或共线，凸')
    return '先找最左点，按极角排序，再扫一遍检查是否一直向右拐'


CONFIG = dict(
    num=469, title='凸多边形', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='凸包扫描 · 检测有无点被丢弃',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def isConvex(self, points):

        def Xmul(p1, p2, p3):
            x1 = p2[0] - p1[0]
            y1 = p2[1] - p1[1]
            x2 = p3[0] - p2[0]
            y2 = p3[1] - p2[1]

            return x1 * y2 - x2 * y1

        def sort_cmp(x, y):
            tmp = Xmul(left, x, y)
            if tmp > 0:
                return -1
            elif tmp < 0:
                return 1
            elif (x[0] - left[0]) ** 2 + (x[1] - left[1]) ** 2 < (y[0] - left[0]) ** 2 + (y[1] - left[1]) ** 2:
                return -1        

            return 1
        
        left = points[0]
        pos = 0
        for index, point in enumerate(points[1:]):
            if point[0] < left[0] or (point[0] == left[0] and point[1] > left[1]):
                left = point
                pos = index + 1
        
        points[0], points[pos] = points[pos], points[0]
        sorted_points = sorted(points[1:], key=functools.cmp_to_key(sort_cmp))

        reverse_pos = len(sorted_points) - 1
        while reverse_pos > 0 and Xmul(left, sorted_points[reverse_pos], sorted_points[reverse_pos - 1]) == 0:
            reverse_pos -= 1

        for index in range(reverse_pos, reverse_pos + (len(sorted_points) - reverse_pos) // 2):
            swap_pos = len(sorted_points) - 1 - index + reverse_pos
            sorted_points[index], sorted_points[swap_pos] = sorted_points[swap_pos], sorted_points[index]

        last_one = left
        last_two = None
        for point in sorted_points:
            if last_two is not None and Xmul(last_one, last_two, point) > 0:
                return False
            last_two, last_one = last_one, point
        
        return True
''',
    setup='import functools',
    call='Solution().isConvex(%r)' % PTS,
    expect=False,
    views=[
        dict(type='custom', draw=_plot, h=420),
        dict(type='text', h=70, fn=_turn),
        dict(type='array', var='sorted_points', h=110, label='sorted_points'),
    ],
    watch=['left', 'pos', 'reverse_pos', ('last_one', 'last_one', 'blue'), ('last_two', 'last_two', 'pink'), 'point'],
    captions={
        'left = points[0]': '先假设 `points[0]` 是最左的点',
        'for index, point in enumerate': '找最左点：`x` 最小，`x` 相同取 `y` 更大的',
        'if point[0] < left[0]': '`{point}` 比当前 left `{left}` 更靠左吗 → {point[0] < B.left[0] or (point[0] == B.left[0] and point[1] > B.left[1])}',
        'left = point': '`left` 换成 `{left}`，记下下标 `pos = {index + 1}`',
        'points[0], points[pos]': '把最左点换到 `points[0]`，剩下的点按极角排序',
        'sorted_points = sorted': '以 `left` 为原点按极角排序（叉积 > 0 排前），共线时近的在前',
        'reverse_pos = len': '排序结果 `{sorted_points}`。最后一条射线上若有多个共线点，要把它们反过来排（近的在后）',
        'while reverse_pos': lambda S, B, r: f'`reverse_pos = {S.reverse_pos}`：向前数与最后一个点和 `left` 共线的点',
        'reverse_pos -= 1': '共线，`reverse_pos` 前移到 {reverse_pos}',
        'for index in range': '翻转最后一段共线点：这里一共 `{(len(sorted_points) - reverse_pos) // 2}` 次交换',
        'swap_pos': '交换位置 `{index}` 和 `{swap_pos}`',
        'last_one = left': '`last_one` 从 `left` 开始，当作扫描的第一条边的起点',
        'last_two = None': '`last_two` 还没有点',
        'for point in sorted_points': '依次取排序后的点 `{point}`',
        'if last_two is not None': lambda S, B, r: ('第一个点：还凑不出两条边，直接记下' if S.last_two is None else
                                                    f'`Xmul({S.last_one}, {S.last_two}, {S.point})` = =={_cross(S.last_one, S.last_two, S.point)}== → ' + ('> 0：向左拐，这个点被丢弃，不是凸包上的点' if _cross(S.last_one, S.last_two, S.point) > 0 else '不大于 0，保持凸')),
        'return False': '有点没在凸包上 → 不是凸多边形，返回 =={ret}==',
        'last_two, last_one': '继续：`last_two = {last_two}`，`last_one = {last_one}`',
        'return True': '所有点都在凸包上 → 返回 =={ret}==',
    },
    skip=['last_two = None', 'last_one = left', 'left = points[0]', 'pos = 0', 'pos = index + 1', 25, 5, 6, 7, 8, 10, 13, 14, 15, 16, 17, 18, 19],
    max_steps=80,
    cards=dict(
        one_liner='套凸包算法：只要有点被丢弃，就不是凸多边形',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给出平面上的一组点，判断这些点能否构成凸多边形',
                 '凸：每个点都在整体的凸包边界上',
                 '本视频：`[[0,0],[0,10],[10,10],[10,0],[5,5]]` → `False`（`(5,5)` 在里面）'],
        quote='在这里可以直接套用凸包的算法，检测是否所有点都没有被丢弃掉。',
        quote_src='—— yiduobo 题解原文',
        idea=['先取==最左点==当原点，其余点按极角（叉积）排序',
              '依次扫描，叉积 `> 0` 说明向左拐，中间那个点会被凸包丢弃',
              '一旦有点被丢弃，立刻返回 `False`；扫完没丢点才是 `True`'],
        summary=['时间 `O(n log n)`，主要是排序；空间 `O(n)`',
                 '易错点：极角相同（共线）的点，最后一条射线上要反转顺序',
                 '最左点相同 x 时取 y 更大的，保证起点唯一',
                 '原文为 Python 2 写法，`sorted(points[1:], sort_cmp)` 已改为 `key=functools.cmp_to_key(sort_cmp)`，整数除法 `/ 2` 已改为 `// 2`（setup 导入 functools）'],
    ),
)
