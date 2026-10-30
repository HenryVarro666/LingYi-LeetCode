def _X(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p2[1]) - (p3[0] - p2[0]) * (p2[1] - p1[1])


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pts = S['points']
    line = S.get('_line')
    left = S.get('self.left')
    sp = S.get('sorted_points')
    res = S.get('res')
    cur = S.get('point') if res is not None or sp is None else None
    gx, gy = 5, 5           # 坐标范围 0..4
    cell = min((x1 - x0 - 120) / (gx - 0.5), (y1 - y0 - 120) / (gy - 0.5))
    ox, oy = x0 + 70, y1 - 60
    px = lambda p: (ox + p[0] * cell, oy - p[1] * cell)
    cv.text((x0 + 18, y0 + 4), '点集（绿线 = 栈里的凸包，粉 = 正要加入的点，黄 = 起点 left）', 22, T['muted'], bold=True)
    for k in range(gx):
        X = ox + k * cell
        cv.line([(X, oy), (X, oy - (gy - 1) * cell)], T['border'], 1)
        cv.text((X, oy + 10), k, 18, T['dim'], anchor='mt', mono=True)
    for k in range(gy):
        Y = oy - k * cell
        cv.line([(ox, Y), (ox + (gx - 1) * cell, Y)], T['border'], 1)
        cv.text((ox - 12, Y), k, 18, T['dim'], anchor='rm', mono=True)
    # 起点到各点的射线（排序后）
    if sp is not None and left is not None and (res is None or len(res) <= 1):
        for q in sp:
            cv.dashed(px(left), px(q), T['dim'], 1)
    # 当前凸包
    if res is not None and len(res) > 1:
        cv.line([px(q) for q in res], T['green'], 5)
    if res is not None and cur is not None and len(res) > 0 and cur not in res:
        cv.dashed(px(res[-1]), px(cur), T['pink'], 3)
    order = {}
    if sp is not None:
        for i, q in enumerate(sp):
            order[tuple(q)] = i + 1
    for q in pts:
        X, Y = px(q)
        fill = T['blue']
        if left is not None and q == left:
            fill = T['yellow']
        elif res is not None and q in res:
            fill = T['green']
        if cur is not None and q == cur:
            fill = T['pink']
        r = 17
        cv.d.ellipse((X - r, Y - r, X + r, Y + r), fill=fill, outline=T['bg'], width=3)
        cv.text((X + 24, Y - 6), f'({q[0]},{q[1]})', 20, T['text'], anchor='lm', mono=True)
        if tuple(q) in order and not (left is not None and q == left):
            cv.text((X, Y), order[tuple(q)], 20, T['bg'], anchor='mm', bold=True)


def _stk(S):
    res = S.get('res')
    if res is None:
        return ''
    return '栈 res：' + ' → '.join(f'`({q[0]},{q[1]})`' for q in res)


def _pop(S, B, ret):
    r = S.res
    return (f'`Xmul(res[-1], res[-2], point) > 0`：`{tuple(r[-1])}` 相对 `{tuple(r[-2])}→{tuple(S.point)}` 向内凹（叉积 {_X(r[-1], r[-2], S.point)} > 0）'
            f' → ==弹出 {tuple(r[-1])}==')


def _while(S, B, ret):
    r = S.res
    if len(r) <= 1:
        return '栈里只有起点，没法判断凹凸 → 直接把 `point` 压栈'
    c = _X(r[-1], r[-2], S.point)
    if c > 0:
        return f'叉积 `Xmul = {c}` > 0：栈顶是凹点 → ==继续弹栈=='
    if c == 0:
        return '叉积 `Xmul = 0`：三点==共线==，边上的树也要围住 → 不弹，停止'
    return f'叉积 `Xmul = {c}` < 0：形状为凸 → 栈顶保留，停止弹栈'


CONFIG = dict(
    num=587, title='安装栅栏', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='格拉汉姆扫描 · 叉积 + 栈',
    tags=['灵神题单·数学算法'],
    code='''
class Solution(object):

    def Xmul(self, p1, p2, p3):
        x1 = p2[0] - p1[0]
        y1 = p2[1] - p1[1]
        x2 = p3[0] - p2[0]
        y2 = p3[1] - p2[1]

        return x1 * y2 - x2 * y1

    def sort_cmp(self, x, y):
        tmp = self.Xmul(self.left, x, y)
        if tmp > 0:
            return -1
        elif tmp < 0:
            return 1
        elif (x[0] - self.left[0]) ** 2 + (x[1] - self.left[1]) ** 2 < (y[0] - self.left[0]) ** 2 + (y[1] - self.left[1]) ** 2:
            return -1        

        return 1

    def outerTrees(self, points):

        if len(points) < 3:
            return points

        self.left = points[0]
        pos = 0
        for index, point in enumerate(points[1:]):
            if point[0] < self.left[0] or (point[0] == self.left[0] and point[1] < self.left[1]):
                self.left = point
                pos = index + 1
        
        points[0], points[pos] = points[pos], points[0]
        sorted_points = sorted(points[1:], key=functools.cmp_to_key(self.sort_cmp))

        reverse_pos = len(sorted_points) - 1
        while reverse_pos > 0 and self.Xmul(self.left, sorted_points[reverse_pos], sorted_points[reverse_pos - 1]) == 0:
            reverse_pos -= 1

        for index in range(reverse_pos, reverse_pos + (len(sorted_points) - reverse_pos) // 2):
            swap_pos = len(sorted_points) - 1 - index + reverse_pos
            sorted_points[index], sorted_points[swap_pos] = sorted_points[swap_pos], sorted_points[index]

        res = [self.left]
        for point in sorted_points:
            while len(res) >1 and self.Xmul(res[-1], res[-2], point) > 0:
                res.pop()
            
            res.append(point)

        return res
''',
    call='Solution().outerTrees([[3,3],[2,2],[2,0],[1,1],[2,4],[4,2]])',
    expect=[[1, 1], [2, 0], [4, 2], [3, 3], [2, 4]],
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='text', fn=_stk, h=60),
    ],
    watch=[('left', 'self.left', 'yellow'), 'pos', ('point', 'point', 'pink'), ('reverse_pos', 'reverse_pos', 'cyan')],
    skip=['x1 = ', 'y1 = ', 'x2 = ', 'y2 = ', 'return x1', 'tmp = self.Xmul', 'if tmp', 'elif tmp', 'elif (x[0]', 'return -1', 'return 1', 'def ', 'if len(points) < 3', 'return points'],
    captions={
        'self.left = points[0]': '先假设 `points[0]` 是最左边的点',
        'if point[0] < self.left[0]': '`{point}` 比当前 left `{self.left}` 更靠左（横坐标相同则更靠下）？',
        'self.left = point': '更新起点 `left = {self.left}`，记下位置 `pos = {pos}`',
        'points[0], points[pos]': '把起点换到 `points[0]`：起点就是凸包的第一个点',
        'for index, point in enumerate': lambda S, B, r: ('所有点都比过了：left 就是最左（再最下）的点' if B.get('point') == S.point and B.get('index') == S.index
                                                           else f'取下一个点 `point = {S.point}`（下标 {S.index + 1}）'),
        'sorted(points[1:]': '其余点按和 left 连线的极角逆时针排序，同一条线上近的在前（排完后画面里的编号就是顺序）',
        'reverse_pos = len': '最后一条射线上的点要==从远到近==，否则凸包会漏边。先从末尾找出这条线的起点',
        'while reverse_pos > 0': lambda S, B, r: (f'`sorted_points[{S.reverse_pos}]` 与前一个点和 left 共线 → 它们在同一条线上，`reverse_pos` 前移'
                                                 if _X(S.self.left, S.sorted_points[S.reverse_pos], S.sorted_points[S.reverse_pos - 1]) == 0
                                                 else f'不共线：最后一条射线从 `sorted_points[{S.reverse_pos}]` 开始'),
        'reverse_pos -= 1': '`reverse_pos` → {reverse_pos}',
        'for index in range(reverse_pos': lambda S, B, r: ('最后一条射线上只有 1 个点，不用反转' if len(S.sorted_points) - S.reverse_pos < 2
                                                          else '把 `[reverse_pos:]` 这一段反转，让最后一条线上的点由远到近'),
        'swap_pos': '交换 `sorted_points[{index}]` 与 `sorted_points[{swap_pos}]`',
        'res = [self.left]': '栈 `res` 从起点开始，接下来按顺序尝试加入每个点',
        'for point in sorted_points': lambda S, B, r: ('所有点都处理完了' if S.res[-1] == S.point and len(S.res) > 1 and B.res[-1] == S.point
                                                       else f'取下一个点 `point = {S.point}`'),
        'while len(res) >1': _while,
        'res.pop()': lambda S, B, r: f'==弹出凹点 {tuple(B.res[-1])}==：它在新边的内侧，不在凸包上',
        'res.append(point)': '`point` 压栈：现在 `res` 长度 `{len(res)}`',
        'return res': '栈里剩下的就是凸包上的所有点（共线点也保留）',
    },
    cards=dict(
        one_liner='极角排序后用栈扫描：遇到凹点就弹出',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给出树的坐标 `points`，用最短的绳子把所有树围起来',
                 '返回绳子上（含边上）所有树的坐标，顺序任意',
                 '示例：`[[1,1],[2,2],[2,0],[2,4],[3,3],[4,2]]` → 五个外圈点'],
        quote='将其他的点，按其到left的连线按逆时针进行排序。位于同一条线上的点则按到left的距离从近到远排序，其中最后一条线上的点则反过来按从远到近排序。',
        quote_src='—— yiduobo 题解原文',
        idea=['起点取==最左（再最下）==的点，它一定在凸包上',
              '其余点绕起点逆时针排好，依次入栈；新点和栈顶两点成==凹==形，栈顶就不该留下 → 弹出',
              '排序和判凹凸都用==向量叉积==：`x1*y2 - x2*y1` 的正负就是转向'],
        summary=['时间 `O(n log n)`（排序），栈扫描 `O(n)`；空间 `O(n)`',
                 '叉积 ==等于 0 的共线点要保留==（题目要求边上的树也算），所以弹栈条件是 `> 0`',
                 '最后一条射线上的点要反转成由远到近，否则这条边上的点会漏掉',
                 '原文为 Python 2 写法，`sorted(..., cmp)` 已改为 `key=functools.cmp_to_key(...)`，`/ 2` 已改为 `// 2`'],
    ),
)
