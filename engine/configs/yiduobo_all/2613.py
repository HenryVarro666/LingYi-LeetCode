def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pts = S.get('points')
    cv.text((x0 + 18, y0 + 4), '点按 x、y 排好序（格内 = 排序后下标，括号 = 原下标）；黄区 = 当前分治范围', 22, T['muted'], bold=True)
    if not pts:
        return
    X0, X1, Y0, Y1 = x0 + 90, x1 - 60, y0 + 70, y1 - 70
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    lx, hx, ly, hy = min(xs) - 0.5, max(xs) + 0.5, min(ys) - 0.5, max(ys) + 0.5
    px = lambda x: X0 + (x - lx) / (hx - lx) * (X1 - X0)
    py = lambda y: Y1 - (y - ly) / (hy - ly) * (Y1 - Y0)
    cv.rect((X0, Y0, X1, Y1), outline=T['border'], width=2, r=6)
    for x in range(int(min(xs)), int(max(xs)) + 1):
        cv.text((px(x), Y1 + 8), x, 20, T['dim'], anchor='mt', mono=True)
    for y in range(int(min(ys)), int(max(ys)) + 1):
        cv.text((X0 - 10, py(y)), y, 20, T['dim'], anchor='rm', mono=True)
    L, R = S.get('left'), S.get('right')
    live = isinstance(L, int) and isinstance(R, int) and 'points' in S and 'mid' in S or (isinstance(L, int) and isinstance(R, int))
    if live:
        rx0, rx1 = px(pts[L][0]) - 30, px(pts[R][0]) + 30
        cv.rect((rx0, Y0 + 2, rx1, Y1 - 2), fill=T['yellow'], alpha=22, r=8)
    md, mx = S.get('min_dis'), S.get('mid_x')
    if live and md is not None and mx is not None:
        cv.rect((px(mx - md), Y0 + 2, px(mx + md), Y1 - 2), fill=T['cyan'], alpha=38)
        cv.dashed((px(mx), Y0), (px(mx), Y1), T['cyan'], 3)
        cv.text((px(mx), Y0 - 4), f'中线 mid_x={mx}，宽 2×{md}', 20, T['cyan'], anchor='mb', bold=True)
    a, b = S.get('p1'), S.get('p2')
    if isinstance(a, int) and isinstance(b, int) and a < len(pts) and b < len(pts):
        cv.line([(px(pts[a][0]), py(pts[a][1])), (px(pts[b][0]), py(pts[b][1]))], T['orange'], 5)
    for i, p in enumerate(pts):
        cx, cy = px(p[0]), py(p[1])
        inr = (not live) or (L <= i <= R)
        best = isinstance(a, int) and isinstance(b, int) and i in (a, b)
        fill = T['orange'] if best else (T['blue'] if inr else T['panel2'])
        cv.rect((cx - 26, cy - 22, cx + 26, cy + 22), fill=fill, r=10, outline=T['border'])
        cv.text((cx, cy - 4), i, 24, T['bg'] if inr or best else T['muted'], anchor='mm', bold=True, mono=True)
        cv.text((cx, cy + 14), f'({p[2]})', 14, T['bg'] if inr or best else T['dim'], anchor='mm', mono=True)


CONFIG = dict(
    num=2613, title='美数对', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='曼哈顿最近点对 · 分治', tags=['常用数据结构', '数学算法'],
    code='''
class Solution(object):
    def beautifulPair(self, nums1, nums2):

        def dis(p1, p2):
            return abs(points[p1][0] - points[p2][0]) + abs(points[p1][1] - points[p2][1])

        def smaller(p1, p2, q1, q2):
            d1 = dis(p1, p2)
            d2 = dis(q1, q2)
            if d1 < d2:
                return True
            if d1 > d2:
                return False

            if min(points[p1][2], points[p2][2]) < min(points[q1][2], points[q2][2]):
                return True
            if min(points[p1][2], points[p2][2]) > min(points[q1][2], points[q2][2]):
                return False
            
            return max(points[p1][2], points[p2][2]) < max(points[q1][2], points[q2][2])

        points = []
        for index, (x, y) in enumerate(zip(nums1, nums2)):
            points.append([x, y, index])
        
        points.sort()
        p1 = p2 = None
        for i in range(1, len(points)):
            if points[i][0] == points[i - 1][0] and points[i][1] == points[i - 1][1]:
                if p1 is None or smaller(i, i - 1, p1, p2):
                    p1, p2 = i, i - 1
        
        if p1 is not None:
            return [min(points[p1][2], points[p2][2]), max(points[p1][2], points[p2][2])]

        def calc(left, right):
            if left == right - 1:
                return left, right

            elif left == right - 2:
                if smaller(left, left + 1, left, left + 2):
                    if smaller(left, left + 1, left + 1, left + 2):
                        return left, left + 1
                    else:
                        return left + 1, left + 2
                elif smaller(left, left + 2, left + 1, left + 2):
                    return left, left + 2
                else:
                    return left + 1, left + 2
                    
            else:
                mid = (left + right) // 2
                left_p1, left_p2 = calc(left, mid)
                right_p1, right_p2 = calc(mid + 1, right)
                if smaller(left_p1, left_p2, right_p1, right_p2):
                    p1, p2 = left_p1, left_p2
                else:
                    p1, p2 = right_p1, right_p2

                min_dis = dis(p1, p2)
                mid_x = (points[mid][0] + points[mid + 1][0]) // 2
                for i in range(mid, left - 1, -1):
                    if mid_x - points[i][0] > min_dis:
                        break
                
                    for j in range(mid + 1, right + 1):
                        if points[j][0] - mid_x > min_dis:
                            break
                        
                        if smaller(i, j, p1, p2):
                            p1, p2 = i, j
                            min_dis = dis(p1, p2)

                return p1, p2

        p1, p2 = calc(0, len(points) - 1)
        return [min(points[p1][2], points[p2][2]), max(points[p1][2], points[p2][2])]
''',
    call='Solution().beautifulPair([1,2,3,4], [2,3,1,3])',
    expect=[0, 1],
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='calls', h=150),
    ],
    watch=['left', 'right', 'mid', 'min_dis', 'mid_x', ('p1', 'p1', 'orange'), ('p2', 'p2', 'orange')],
    skip=['return True', 'return False', 'if d1 > d2', 'd1 = dis', 'd2 = dis', 'points = []', 'points.append', 'p1 = p2 = None'],
    max_steps=110,
    captions={
        'points.sort()': '按 x、再按 y 排序，之后点的下标 0..n-1 就是从左到右的顺序',
        'if points[i][0] == points[i - 1][0]': '排序后坐标完全相同的点相邻 → 距离 0，一定是最优',
        'return [min(points[p1][2]': '返回原下标对（小的在前）`{ret}`',
        'if left == right - 1': lambda S, B, r: f'范围 `[{S.left}, {S.right}]` 只有 2 个点 → 直接是答案' if S.left == S.right - 1 else f'范围 `[{S.left}, {S.right}]` 超过 2 个点',
        'elif left == right - 2': '正好 3 个点：不再分治，两两比较，用 `smaller` 选出最近对',
        'mid = (left + right) // 2': '从中间切开：左半 `[{left}, {mid}]`，右半 `[{mid+1}, {right}]`（原文 `/` 已改 `//`）',
        'left_p1, left_p2 = calc': '递归求左半内部的最近对 → `({left_p1}, {left_p2})`',
        'right_p1, right_p2 = calc': '递归求右半内部的最近对 → `({right_p1}, {right_p2})`',
        'if smaller(left_p1': '比较两侧最近对谁更近（距离相等则比原下标字典序）',
        'if d1 < d2': '`d1 = {d1}`，`d2 = {d2}`：前一对更近 → 直接 True；相等时才继续比原下标',
        'p1, p2 = left_p1': '左侧更优，暂存为当前最近对 `({p1}, {p2})`',
        'p1, p2 = right_p1': '右侧更优，暂存为当前最近对 `({p1}, {p2})`',
        'min_dis = dis(p1, p2)': '当前最小距离 `min_dis` = =={min_dis}==，跨中线的点对只有距离更小才有意义',
        'mid_x = ': '中线 `mid_x` = {mid_x}；只需看离中线不超过 `min_dis` 的点',
        'for i in range(mid, left - 1, -1)': lambda S, B, r: f'左半从中线向左取点 `i = {S.i}`' if 'i' in S else '左半从中线向左扫描',
        'if mid_x - points[i][0] > min_dis': '`{mid_x} - {points[i][0]} = {mid_x - points[i][0]}`，是否比 `min_dis = {min_dis}` 还远？远了就不可能更近 → break',
        'for j in range(mid + 1': '右半从中线向右取点 `j = {j}`',
        'if points[j][0] - mid_x > min_dis': '`{points[j][0]} - {mid_x} = {points[j][0] - mid_x}`，超出 `min_dis = {min_dis}` 就 break',
        'if smaller(i, j, p1, p2)': '跨中线的点对 `({i}, {j})` 比当前最近对更近吗？调用 `smaller` 比距离，距离相同再看原下标',
        'p1, p2 = i, j': '更近！更新最近对 `({p1}, {p2})`',
        'return p1, p2': '这一层的最近对是 `({p1}, {p2})`，返回给上一层',
        'p1, p2 = calc(0, len(points) - 1)': '整个排序后的点集的最近对：下标 `({p1}, {p2})`',
    },
    cards=dict(
        one_liner='排序后分治：左右各求最近对，再只看中线附近的跨线点对',
        complexity='时间 约 `O(n log n)`（本文未做 12 点限制，最坏更慢），空间 `O(n)`',
        problem=['两个等长数组，选下标 `i<j` 使曼哈顿距离 `|nums1[i]-nums1[j]|+|nums2[i]-nums2[j]|` 最小',
                 '距离相同取 `i` 最小，再取 `j` 最小',
                 '示例：`nums1=[1,2,3,2,4]`，`nums2=[2,3,1,2,3]` → `[0,3]`；本视频用 `[1,2,3,4]`、`[2,3,1,3]` → `[0,1]`'],
        quote='将所有位置按x为第一优先级，y为第二优先级排序。接下来按数组划分成左右两个部分，并花一条中线。接下来分别递归求解这两个部分中的最近点对距离，取两侧最短距离的最小值dis，然后从中线向左侧和右侧画一个宽度为2 * dis的矩形，接下来就只考虑矩形内的左右配对就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['先处理重复点：坐标相同距离为 0，直接返回',
              '`calc(left, right)`：≤3 个点暴力，否则左右递归 + 中线带状区检查',
              '`smaller` 同时比较距离和原下标，保证并列时字典序最小'],
        summary=['原文为 Python 2 写法，`(left + right) / 2` 与 `/ 2` 的整数除法已改为 `//`',
                 '`smaller` 的并列规则是易错点：先比距离，再比 `min` 下标，再比 `max` 下标',
                 '中线带内的双重循环靠 `break` 剪枝；作者提到曼哈顿距离每点最多看约 12 个对面点，本题不必实现',
                 '本视频用 4 个点演示，只递归一层'],
    ),
)
