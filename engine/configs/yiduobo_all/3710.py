def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pts = S['points']
    n = len(pts)
    thr = S.get('threshold')
    cols = S.get('color')
    live = thr is not None and cols is not None and len(cols) == n
    if not live:
        cols = [None] * n
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    w, h = x1 - x0 - 200, y1 - y0 - 150
    sc = min(w / max(1, max(xs) - min(xs)), h / max(1, max(ys) - min(ys)), 100)
    ox = x0 + 100 + (w - sc * (max(xs) - min(xs))) / 2
    oy = y0 + 80 + (h - sc * (max(ys) - min(ys))) / 2 + sc * (max(ys) - min(ys))

    def P(i):
        return (ox + (pts[i][0] - min(xs)) * sc, oy - (pts[i][1] - min(ys)) * sc)

    cv.text((x0 + 18, y0 + 4), '点的位置（线 = 距离 < 当前划分因子，两端必须异色；红 = 冲突）', 22, T['muted'], bold=True)
    if live:
        for i in range(n):
            for j in range(i + 1, n):
                d = abs(pts[i][0] - pts[j][0]) + abs(pts[i][1] - pts[j][1])
                if d < thr:
                    bad = cols[i] is not None and cols[i] == cols[j]
                    a, b = P(i), P(j)
                    cv.line([a, b], T['red'] if bad else T['dim'], 6 if bad else 3)
                    cv.text(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 18), d, 20, T['red'] if bad else T['muted'], anchor='mm', bold=True)
    cur = S.get('now') if live else None
    for i in range(n):
        X, Y = P(i)
        c = cols[i]
        fill = T['blue'] if c == 0 else T['pink'] if c == 1 else T['panel2']
        cv.rect((X - 26, Y - 26, X + 26, Y + 26), fill=fill, outline=T['yellow'] if cur == i else T['border'], width=5 if cur == i else 2, r=26)
        cv.text((X, Y), i, 26, T['bg'] if c is not None else T['text'], anchor='mm', bold=True)
        cv.text((X, Y + 36), f'({pts[i][0]},{pts[i][1]})', 18, T['dim'], anchor='mt', mono=True)


CONFIG = dict(
    num=3710, title='最大划分因子', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='二分答案 + 二分图染色', tags=['灵神题单·二分算法', '难度分 2135'],
    code='''
class Solution(object):
    def maxPartitionFactor(self, points):

        n = len(points)
        if n <= 2:
            return 0

        dis = [[0] * n for _ in range(n)]
        ma = 0
        for i in range(n):
            for j in range(i + 1, n):
                dis[i][j] = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
                dis[j][i] = dis[i][j]
                ma = max(ma, dis[i][j])

        def check(now, threshold):
            for nxt in range(n):
                if now == nxt:
                    continue
                if dis[now][nxt] < threshold:
                    if color[nxt] is None:
                        color[nxt] = 1 - color[now]
                        if not check(nxt, threshold):
                            return False
                    elif color[nxt] == color[now]:
                        return False
            
            return True

        left = 0
        right = ma

        while left < right:
            mid = (left + right + 1) // 2
            color = [None] * n
            flag = True
            for i in range(n):
                if color[i] is None:
                    color[i] = 0
                    if not check(i, mid):
                        flag = False
                        break

            if flag:
                left = mid
            else:
                right = mid - 1
        
        return left
''',
    call='Solution().maxPartitionFactor([[0,0],[1,1],[2,0],[8,3]])',
    expect=2, max_steps=110,
    skip=[8, 9, 10, 11, 12, 13, 14, 'if now == nxt', 'continue', 'for nxt in range(n)', 'dis[now][nxt] < threshold', 'return False', 'return True', 'color = [None]', 'flag = True', 'for i in range(n):', 'if n <= 2', 'n = len(points)', 'if not check(', 'break', 'color[i] = 0', 'left = 0'],
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', h=70, fn=lambda S: (f"二分范围 `[{S['left']}, {S['right']}]`（闭区间），试划分因子 `mid = {S['mid']}`" if 'mid' in S else (f"二分范围 `[{S['left']}, {S['right']}]`" if 'right' in S and 'left' in S else ''))),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('color', 'color', 'cyan')],
    captions={
        'right = ma': '先算好所有点对的曼哈顿距离，最大 `ma = {ma}`：二分范围 `[0, {ma}]`',
        'mid = (': '取偏大中点 `mid = ({left} + {right} + 1) // 2 = {mid}`：能否让同组点对的距离都 `≥ {mid}`？',
        'if color[i] is None': lambda S, B, r: (f'点 `{B.i}` 还没染色：新连通块的起点，染成 0 后递归染它的邻居' if B.color[B.i] is None else f'点 `{B.i}` 已染色，跳过'),
        'if color[nxt] is None': lambda S, B, r: f'`{B.now}` 与 `{B.nxt}` 距离 `{B.dis[B.now][B.nxt]} < {B.threshold}`（连边）：' + ('`{}` 无色 → 染成相反色，递归'.format(B.nxt) if B.color[B.nxt] is None else '`{}` 已有颜色'.format(B.nxt)),
        'color[nxt] = 1 - color[now]': '`{nxt}` 染成 `{color[nxt]}`，与 `{now}` 的颜色相反',
        'elif color[nxt] == color[now]': lambda S, B, r: (f'`{B.nxt}` 与 `{B.now}` 同色 `{B.color[B.now]}` → ==冲突==，染色失败' if B.color[B.nxt] == B.color[B.now] else f'`{B.nxt}` 与 `{B.now}` 异色，没问题'),
        'flag = False': '染色失败 → 划分因子 {mid} 不可行，不用再看其他点',
        'if flag': lambda S, B, r: (f'染色成功 → 因子 {S.mid} 可行' if S.flag else f'染色失败 → 因子 {S.mid} 不可行'),
        'left = mid': '可行 → 答案 ≥ {mid}：`left = {left}`',
        'right = mid - 1': '不可行 → 答案 ≤ {mid} − 1：`right = {right}`',
        'return left': '`left = right`：最大划分因子 ==`{left}`==',
    },
    cards=dict(
        one_liner='划分因子越小越好分：二分它，距离更近的点连边后看能否 2-染色',
        complexity='时间 `O(n² log U)`，空间 `O(n²)`',
        problem=['把 `n` 个点分成两个非空的组，划分因子 = 同组内点对最小曼哈顿距离',
                 '求最大的划分因子（点数不超过 2 时为 0）',
                 '本视频：`[[0,0],[1,1],[2,0],[8,3]]` → `2`'],
        quote='划分因子越小，越可能得到可行的划分，因此在这里可以二分答案，将问题转化为对于特定的划分因子mid，能否得到可行的划分。而对于这个问题，则可以使用二分图染色的方式来进行判定。',
        quote_src='—— yiduobo 题解原文',
        idea=['先预处理 `dis[i][j]`，点数 ≤ 500 所以 `O(n²)` 存得下',
              '距离 `< mid` 的点对必须在不同组 → 连边，问图能否 2-染色',
              '染色分三种情况：无色就染反色递归；异色跳过；同色失败。成功就 `left = mid`'],
        summary=['时间 `O(n² log U)`，空间 `O(n²)`（距离矩阵）',
                 '原文已是 Python 3 可运行写法，未改动',
                 '`color` 用 `None` 表示未染色，所以颜色是 0 / 1，不是灵神的 ±1',
                 '闭区间二分：`mid` 取偏大，`+1` 防止死循环',
                 '对比灵神：灵神每次 check 现算距离、返回开区间 `left`；这里预存距离矩阵'],
    ),
)
