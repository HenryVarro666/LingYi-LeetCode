def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pts = S['points']
    n = len(pts)
    low = S.get('low')
    cols = S.get('colors')
    if low is None or cols is None or len(cols) != n:
        cols = [0] * n
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    w, h = x1 - x0 - 200, y1 - y0 - 150
    sc = min(w / max(1, max(xs) - min(xs)), h / max(1, max(ys) - min(ys)), 100)
    ox = x0 + 100 + (w - sc * (max(xs) - min(xs))) / 2
    oy = y0 + 80 + (h - sc * (max(ys) - min(ys))) / 2 + sc * (max(ys) - min(ys))

    def P(i):
        return (ox + (pts[i][0] - min(xs)) * sc, oy - (pts[i][1] - min(ys)) * sc)

    cv.text((x0 + 18, y0 + 4), '点的位置（线 = 距离 < low 的"非法点对"，两端必须异色；红 = 冲突）', 22, T['muted'], bold=True)
    if low is not None:
        for i in range(n):
            for j in range(i + 1, n):
                d = abs(pts[i][0] - pts[j][0]) + abs(pts[i][1] - pts[j][1])
                if d < low:
                    bad = cols[i] != 0 and cols[i] == cols[j]
                    a, b = P(i), P(j)
                    cv.line([a, b], T['red'] if bad else T['dim'], 6 if bad else 3)
                    cv.text(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 18), d, 20, T['red'] if bad else T['muted'], anchor='mm', bold=True)
    cur = S.get('x') if 'low' in S else None
    for i in range(n):
        X, Y = P(i)
        fill = T['blue'] if cols[i] == 1 else T['pink'] if cols[i] == -1 else T['panel2']
        ring = cur == i
        cv.rect((X - 26, Y - 26, X + 26, Y + 26), fill=fill, outline=T['yellow'] if ring else T['border'], width=5 if ring else 2, r=26)
        cv.text((X, Y), i, 26, T['bg'] if cols[i] else T['text'], anchor='mm', bold=True)
        cv.text((X, Y + 36), f'({pts[i][0]},{pts[i][1]})', 18, T['dim'], anchor='mt', mono=True)


CONFIG = dict(
    num=3710, title='最大划分因子', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='二分答案 + 二分图染色', tags=['灵神题单·二分算法', '难度分 2135'],
    code='''
class Solution:
    def maxPartitionFactor(self, points: List[List[int]]) -> int:
        if len(points) == 2:
            return 0

        # 原理见 785. 判断二分图
        def check(low: int) -> bool:
            colors = [0] * len(points)

            def dfs(x: int, c: int) -> bool:
                colors[x] = c
                x1, y1 = points[x]
                for y, (x2, y2) in enumerate(points):
                    if y == x or abs(x1 - x2) + abs(y1 - y2) >= low:  # 符合要求
                        continue
                    if colors[y] == c or colors[y] == 0 and not dfs(y, -c):
                        return False  # 不是二分图
                return True

            # 可能有多个连通块
            for i, c in enumerate(colors):
                if c == 0 and not dfs(i, 1):
                    return False
            return True

        max_dis = max(abs(x1 - x2) + abs(y1 - y2)
                      for (x1, y1), (x2, y2) in combinations(points, 2))

        left, right = 0, max_dis + 1
        while left + 1 < right:
            mid = (left + right) // 2
            if check(mid):
                left = mid
            else:
                right = mid
        return left
''',
    call='Solution().maxPartitionFactor([[0,0],[1,1],[2,0],[8,3]])',
    expect=2, max_steps=110,
    skip=['y == x or abs', 'continue', 'x1, y1 = points[x]', 'for y, (x2', 'if len(points) == 2', 'colors = [0]', 'return True', 'for i, c in enumerate', 'combinations', 'return False'],
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', h=70, fn=lambda S: (f"开区间 `({S['left']}, {S['right']})`：`check(left)` 真，`check(right)` 假；现在试 `low = {S['low']}`" if 'low' in S and 'left' in S
                                                  else (f"开区间 `({S['left']}, {S['right']})`" if 'right' in S and 'left' in S else ''))),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('colors', 'colors', 'cyan')],
    captions={
        'max_dis = max': '最大曼哈顿距离 = `{max_dis}`；再加一一定无法满足 → 右开端点',
        'left, right = 0': '开区间 `(0, {right})`：`low = 0` 随意划分一定可行；`low = {right}` 一定不可行',
        'mid = (': '猜划分因子 `low = {mid}`：能否让每组内部的点对距离都 `≥ {mid}`？',
        'colors[x] = c': lambda S, B, r: f'给点 `{B.x}` 染色 `{B.c}`（1 / -1 表示两个组）',
        'if colors[y] == c': lambda S, B, r: (f'`{B.x}` 与 `{B.y}` 距离 `< {B.low}`（非法点对）：不能同组。`{B.y}` 已是同色 `{B.c}` → ==冲突==，不是二分图，`check` 返回 False' if B.colors[B.y] == B.c
                                              else (f'`{B.x}` 与 `{B.y}` 距离 `< {B.low}`（非法点对），`{B.y}` 还没染色 → 染成相反色 `{-B.c}`，递归' if B.colors[B.y] == 0 else f'`{B.x}` 与 `{B.y}` 距离 `< {B.low}`，但 `{B.y}` 已是异色，没问题')),
        'if c == 0 and not dfs(i, 1)': lambda S, B, r: (f'点 `{B.i}` 还没染色：它是新连通块的起点，染成 1 开始 dfs' if B.c == 0 else f'点 `{B.i}` 已染色，跳过'),
        'return left': '`check(left)` 为真的最大 low：==返回 {left}==',
        'if check(mid)': lambda S, B, r: '调用 `check({mid})`：`mid = {mid}` 能不能满足？'.format(mid=S.mid),
        'left = mid': '`check({mid})` 为真：划分因子 ≥ {mid} 可行 → `left = {left}`',
        'right = mid': '`check({mid})` 为假：{mid} 太苛刻 → `right = {right}`',
    },
    cards=dict(
        one_liner='二分划分因子 low；距离小于 low 的点对连边，判断是不是二分图',
        complexity='时间 `O(n² log U)`，空间 `O(n)`',
        problem=['把 `n` 个点分成恰好两个非空的组，划分因子 = 同组点对的最小曼哈顿距离',
                 '求最大的划分因子（`n = 2` 时为 0）',
                 '本视频：`[[0,0],[1,1],[2,0],[8,3]]` → `2`'],
        quote='对于曼哈顿距离 < low 的点对（非法点对），连一条边，我们可以得到一个无向图。我们需要把这些点分成两个集合，每个集合内部不能有边。这和 785. 判断二分图是完全一样的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['「最大化最小值」→ 二分答案：low 越小越宽松，越大越苛刻',
              '给定 low：距离 `< low` 的点对必须拆开 → 连边 → 交替染色判二分图',
              '`check` 为真就 `left = mid`，开区间写法最后返回 `left`'],
        summary=['时间 `O(n² log U)`，`U` 是最大曼哈顿距离；也可对所有距离排序后二分',
                 '易错：`n = 2` 时没有组内点对，要特判返回 0',
                 '图可能有多个连通块，要对每个未染色的点都 dfs 一次',
                 '二分结果一定是某两点的距离（反证：否则 `check(ans+1)` 也为真）',
                 '另一写法：按距离从小到大处理点对，用带权并查集（异或）判矛盾，本视频不展开'],
    ),
)
