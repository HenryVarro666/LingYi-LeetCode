PTS = [[1, 1], [6, 1]]
RMAX = 4          # 示例里二分到的 mid 不超过 4


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pts = S['points']
    mid = S.get('mid') if 'trans_points' in S or S.get('_line', 0) >= 30 else None
    ln = S.get('_line', 0)
    W = (x1 - x0) / 2
    cols = [T['blue'], T['pink'], T['green'], T['orange']]
    cv.text((x0 + 18, y0 + 4), '原坐标：菱形 = 传播 mid 天', 22, T['muted'], bold=True)
    cv.text((x0 + W + 18, y0 + 4), '旋转 45° 后：菱形变正方形', 22, T['muted'], bold=True)
    # ---- 左：原坐标 ----
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    gx0, gx1, gy0, gy1 = min(xs) - RMAX, max(xs) + RMAX, min(ys) - RMAX, max(ys) + RMAX
    top, bot = y0 + 70, y1 - 30
    sc = min((W - 50) / (gx1 - gx0), (bot - top) / (gy1 - gy0))
    ox, oy = x0 + 25, (top + bot) / 2

    def P(a, b):
        return (ox + (a - gx0) * sc, oy - (b - (gy0 + gy1) / 2) * sc)

    for a in range(gx0, gx1 + 1):
        for b in range(gy0, gy1 + 1):
            px, py = P(a, b)
            cv.rect((px - 2, py - 2, px + 2, py + 2), fill=T['dim'], r=2)
    if mid is not None:
        for k, (a, b) in enumerate(pts):
            c = cols[k % 4]
            q = [P(a - mid, b), P(a, b + mid), P(a + mid, b), P(a, b - mid), P(a - mid, b)]
            cv.line(q, c, 4)
    for k, (a, b) in enumerate(pts):
        px, py = P(a, b)
        cv.rect((px - 9, py - 9, px + 9, py + 9), fill=cols[k % 4], r=9)
        cv.text((px, py - 16), f'({a},{b})', 18, T['text'], anchor='mb', mono=True)
    # ---- 右：旋转后 ----
    U = [(a + b, b - a) for a, b in pts]
    ux0, ux1 = min(u for u, v in U) - RMAX, max(u for u, v in U) + RMAX
    vy0, vy1 = min(v for u, v in U) - RMAX, max(v for u, v in U) + RMAX
    sc2 = min((W - 50) / (ux1 - ux0), (bot - top) / (vy1 - vy0))
    rx, ry = x0 + W + 25, (top + bot) / 2

    def Q(u, v):
        return (rx + (u - ux0) * sc2, ry - (v - (vy0 + vy1) / 2) * sc2)

    if mid is not None:
        for k, (u, v) in enumerate(U):
            c = cols[k % 4]
            q = [Q(u - mid, v - mid), Q(u + mid, v - mid), Q(u + mid, v + mid), Q(u - mid, v + mid), Q(u - mid, v - mid)]
            cv.line(q, c, 4)
    for k, (u, v) in enumerate(U):
        px, py = Q(u, v)
        cv.rect((px - 8, py - 8, px + 8, py + 8), fill=cols[k % 4], r=8)
        cv.text((px, py + 14), f"({u},{v})", 18, T['text'], anchor='mt', mono=True)
    sweeping = ('x_cnt' in S and (47 <= ln <= 69 or 5 <= ln <= 19) and 'x' in S and mid is not None)
    if sweeping:
        sx_ = S['x']
        a_, b_ = Q(sx_, vy0)[0], 0
        cv.line([(a_, top - 10), (a_, bot + 10)], T['yellow'], 4)
        cv.text((a_, bot + 12), f"扫描线 x={sx_}  x_cnt={S['x_cnt']}", 20, T['yellow'], anchor='mt', bold=True)
        if 'y' in S and ln in (5, 17, 19, 67, 69):
            qx, qy = Q(S['x'], S['y'])
            cv.rect((qx - 12, qy - 12, qx + 12, qy + 12), outline=T['yellow'], width=4, r=12)
            ca, cb = (S['x'] - S['y']) / 2, (S['x'] + S['y']) / 2
            px, py = P(ca, cb)
            cv.rect((px - 14, py - 14, px + 14, py + 14), outline=T['yellow'], width=4, r=14)
            cv.text((px, py + 20), f'还原 ≈ ({ca:g},{cb:g})', 18, T['yellow'], anchor='mt', bold=True)


CONFIG = dict(
    num=1956, title='感染K种病毒所需的最短时间', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='二分答案 + 旋转坐标扫描线',
    tags=['灵神题单·数学算法'],
    code='''
class Solution(object):
    def minDayskVariants(self, points, k):

        def check(x, y, mid):
            ori_x = int((x - y) / 2.0)
            ori_y = int((x + y) / 2.0)
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    cnt = 0
                    cx = ori_x + dx
                    cy = ori_y + dy
                    for px, py in points:
                        if abs(cx - px) + abs(cy - py) <= mid:
                            cnt += 1
                    
                    if cnt >= k:
                        return True
            
            return False

        max_dis = 0
        n = len(points)
        for i in range(n - 1):
            for j in range(i + 1, n):
                max_dis = max(max_dis, abs(points[i][0] - points[j][0]) + abs(points[j][0] - points[j][1]))
        
        left = 0
        right = int(max_dis * 0.75) + 1
        while left < right:
            mid = (left + right) // 2
            trans_points = []
            for i in range(n):
                x, y = points[i][0], points[i][1]
                up_y, down_y = y + mid, y - mid
                x1, y1 = x + down_y, down_y - x
                x2, y2 = x + up_y, up_y - x
                trans_points.append([x1, y1, y2, 1])
                trans_points.append([x2, y1, y2, -1])
            
            trans_points.sort(key = lambda d:(d[0], -d[-1]))

            x_cnt = 0
            y1_dict = {}
            y2_dict = {}
            flag = False

            for x, y1, y2, delta in trans_points:
                x_cnt += delta
                if delta == 1:
                    y1_dict[y1] = y1_dict.get(y1, 0) + 1
                    y2_dict[y2] = y2_dict.get(y2, 0) + 1
                else:
                    y1_dict[y1] -= 1
                    y2_dict[y2] -= 1
                
                if x_cnt >= k or (x_cnt == k - 1 and delta == -1):
                    y_list = []
                    for y1 in y1_dict:
                        for freq in range(y1_dict[y1]):
                            y_list.append([y1, 1])
                    for y2 in y2_dict:
                        for freq in range(y2_dict[y2]):
                            y_list.append([y2, -1])

                    y_list.sort(key=lambda d:(d[0], -d[-1]))
                    y_cnt = 0
                    for y, delta in y_list:
                        y_cnt += delta
                        if (y_cnt >= k or (y_cnt == k - 1 and delta == -1)) and check(x, y, mid):
                            flag = True
                            break
                    
                    if flag:
                        break
            
            if flag:
                right = mid
            else:
                left = mid + 1
        
        return left
''',
    call='Solution().minDayskVariants([[1,1],[6,1]], 2)',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"二分天数：left = {S['left']}，right = {S['right']}" + (f"，试 mid = =={S['mid']}==" if 'mid' in S and S.get('_line', 0) >= 30 and S['left'] < S['right'] else '')) if 'left' in S and 'right' in S else '', size=30, h=70),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), 'x_cnt', 'y_cnt'],
    skip=['trans_points.append','x_cnt += delta','if delta == 1','y_cnt += delta','if cnt >= k',70,71,73,74,'for i in range(n - 1)','for j in range(i + 1','for dx','for dy','cnt = 0','cx = ','cy = ','for px, py','if abs(cx','cnt += 1','ori_y =','up_y, down_y','x, y = points','x1, y1 =','x2, y2 =','for i in range(n):','y1_dict[y1] =','y2_dict[y2] =','y1_dict[y1] -=','y2_dict[y2] -=','y1_dict = {}','y2_dict = {}','flag = False','trans_points = []','x_cnt = 0','for y1 in y1_dict','for freq','y_list.append','for y2 in y2_dict','y_list = []','n = len','max_dis = 0','y_cnt = 0'],
    max_steps=70,
    captions={
        'max_dis = max': '先估二分上界：取点对的距离（原文这里第二项写成 `points[j][0] − points[j][1]`，只影响上界估计）→ `max_dis = {max_dis}`',
        'left = 0': '答案天数最小 0，二分的下界 `left = 0`',
        'right = int': '上界取 `max_dis × 0.75` 向上取整 = `{right}`：这么多天一定够',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`：答案还在 `[{S.left}, {S.right}]` 里，继续二分' if S.left < S.right else f'`left = right = {S.left}`：区间收成一点，答案找到'),
        'mid = ': '试 `mid = {mid}` 天：问能不能有一个整点被至少 `k = {k}` 个菱形同时覆盖（天数越大覆盖越广，所以可以二分）',
        'trans_points.sort': '每个菱形旋转 45° 变成正方形，拆成左边（+1）、右边（−1）两个事件，按 x 排序：`{[(e[0], e[-1]) for e in trans_points]}`',
        'for x, y1, y2, delta': lambda S, B, r: ('事件扫完了，没有任何位置被 k 个正方形覆盖 → 这个 mid 不行' if B.get('x') == S.x and B.get('delta') == S.delta and B.get('x_cnt') == S.x_cnt else (f'扫到 `x = {S.x}`：' + ('一个正方形的==左边==，进入它（x_cnt + 1）' if S.delta == 1 else '一个正方形的==右边==，离开它（x_cnt − 1）'))),
        'if x_cnt >= k': lambda S, B, r: (f'`x_cnt = {S.x_cnt}`' + ('，这一列至少被 `k` 个正方形盖住 → 再沿 y 方向找具体位置' if (S.x_cnt >= S.k or (S.x_cnt == S.k - 1 and S.delta == -1)) else f' < `k = {S.k}`，覆盖不够，继续扫')),
        'y_list.sort': '同一列的正方形，把下边（+1）和上边（−1）按 y 排序，再沿 y 方向扫一遍：`{y_list}`',
        'for y, delta in y_list': '扫到 `y = {y}`（旋转坐标 `({x}, {y})`）',
        'if (y_cnt >= k': lambda S, B, r: (f'`y_cnt = {S.y_cnt}`' + (f' ≥ `k`：候选点 `({S.x}, {S.y})` 被 k 个正方形盖住，但可能不是整点 → 调 `check` 还原验证' if (S.y_cnt >= S.k or (S.y_cnt == S.k - 1 and S.delta == -1)) else f' < `k = {S.k}`，覆盖不够，继续')),
        'ori_x =': '`check`：把旋转坐标 `({x}, {y})` 还原成原坐标 `({(x - y) / 2:g}, {(x + y) / 2:g})`（可能不是整点），取整后检查周围 3×3 个整点各被几个菱形覆盖',
        'return True': '周围有整点被至少 `k` 个菱形覆盖 → ==这个 mid 可行==',
        'return False': '周围 9 个整点都不够 `k` 个 → 候选点无效',
        'if flag:': lambda S, B, r: (f'`flag = True`：`{S.mid}` 天可行，答案 ≤ mid' if S.flag else f'`flag = False`：`{S.mid}` 天扫完整个平面也没有被 k 个菱形覆盖的整点，答案 > mid'),
        'right = mid': '`{mid}` 天够用 → 往小里找：`right = {right}`',
        'left = mid + 1': '`{mid}` 天不够 → 答案在右边：`left = {left}`',
        'return left': '区间收成一点：最少 =={ret}== 天',
    },
    cards=dict(
        one_liner='天数越大覆盖越广 → 二分；旋转 45° 把菱形变成正方形',
        complexity='时间 约 `O(log D · n³)`，空间 `O(n)`（n ≤ 50）',
        problem=['平面上有 n 个病毒位置，每天向上下左右扩散一格（覆盖一个菱形）',
                 '求最少几天，使某个==整数点==同时被至少 `k` 种病毒覆盖',
                 '示例：`points=[[1,1],[6,1]]`，`k=2` → `3`'],
        quote='菱形的相交是不太好处理的，因此在这里需要做一次坐标变换，将坐标轴逆时针旋转45度，这样一来所有的菱形就变成了正方形，问题就变成了给出若干个正方形，问是否存在某个整数点被最少k个正方形覆盖。',
        quote_src='—— yiduobo 题解原文',
        idea=['`t` 越大覆盖越大，满足单调 → 二分最小的 `t`',
              '判定：旋转后的正方形做扫描线，先沿 x 找被 ≥ k 个盖住的列，再沿 y 找位置',
              '边界点还原后可能不是整点 → 在原坐标周围 3×3 里逐个验证'],
        summary=['时间约 `O(log D · n³)`，n ≤ 50 所以暴力扫描足够，原文提到最优是扫描线 + 树状数组',
                 '原文为 Python 2 写法，`mid = (left + right) / 2` 已改为 `//`',
                 '`max_dis` 那行第二项下标疑似笔误（应为 `[j][1]`），只影响上界，二分仍能收敛',
                 '易错：检测点在正方形边界上，需向外多查一圈整点',
                 '同类：二分答案 + 判定可行性'],
    ),
)
