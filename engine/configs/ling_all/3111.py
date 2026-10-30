def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pts = S['points']
    w = S['w']
    cv.text((x0 + 18, y0 + 4), '只看横坐标：每个矩形从某个点开始，恰好伸到 x + w', 24, T['muted'], bold=True)
    xs = [p[0] for p in pts]
    lo, hi = min(xs), max(xs)
    left, right = x0 + 60, x1 - 60
    sc = (right - left) / max(1, hi - lo)
    base = y1 - 120
    cv.line([(left - 20, base), (right + 20, base)], T['border'], 2)
    for v in range(lo, hi + 1):
        X = left + (v - lo) * sc
        cv.line([(X, base), (X, base + 8)], T['border'], 2)
        cv.text((X, base + 14), v, 20, T['dim'], anchor='mt', mono=True)
    x2 = S.get('x2', -1)
    cur = S.get('x')
    if 'x2' in S and x2 >= 0:
        # 当前矩形：右端 x2，左端 x2 - w
        a = left + (x2 - w - lo) * sc
        b = left + (x2 - lo) * sc
        cv.rect((a - 10, base - 150, b + 10, base - 10), fill=T['yellow'], alpha=60, r=8)
        cv.text((a, base - 160), f'当前矩形：[{x2 - w}, {x2}]', 22, T['yellow'], anchor='lb', bold=True)
    for idx, (px, py) in enumerate(pts):
        X = left + (px - lo) * sc
        covered = px <= x2
        col = T['green'] if covered else T['text']
        if cur is not None and px == cur and 'x' in S:
            col = T['blue']
        cv.rect((X - 9, base - 40 - (idx % 3) * 14, X + 9, base - 22 - (idx % 3) * 14), fill=col, r=9)
    cv.text((x0 + 18, y1 - 50), '绿 = 已被矩形盖住，蓝 = 当前遍历到的点，黄框 = 当前矩形', 20, T['muted'])


CONFIG = dict(
    num=3111, title='覆盖所有点的最少矩形数目', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='排序 + 右端点 x2',
    tags=['灵神题单', '难度分 1401'],
    code='''
class Solution:
    def minRectanglesToCoverPoints(self, points: List[List[int]], w: int) -> int:
        points.sort(key=lambda p: p[0])
        ans = 0
        x2 = -1
        for x, _ in points:
            if x > x2:
                ans += 1
                x2 = x + w
        return ans
''',
    call='Solution().minRectanglesToCoverPoints([[5,1],[1,0],[2,7],[7,3],[3,4],[1,9],[9,2]], 2)',
    expect=3,
    views=[
        dict(type='array', var=lambda S: [pt[0] for pt in S['points']], label='排序后各点的横坐标', h=180),
        dict(type='custom', draw=_draw, h=420),
    ],
    watch=[('x', 'x', 'blue'), ('x2', 'x2', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'points.sort': '矩形不限高，只需考虑横坐标：按 `x` ==从小到大排序==',
        'ans = 0': '`ans` 记录矩形个数',
        'x2 = -1': '假设左边已有一个矩形，右端 `x2 = -1`（横坐标都非负，一定盖不到）',
        'for x, _': '看下一个点，横坐标 `x = {x}`',
        'if x > x2': lambda S, B, r: (f"`x = {S.x} > x2 = {S.x2}`：没被盖住，==需要新矩形==" if S.x > S.x2 else f"`x = {S.x} <= x2 = {S.x2}`：已被当前矩形盖住，跳过"),
        'ans += 1': '新矩形从 `x` 开始 → `ans` = =={ans}==',
        'x2 = x + w': '矩形越宽盖得越多，所以右端恰好是 `x + w` = =={x2}==',
        'return ans': '遍历结束，最少 `{ans}` 个矩形',
    },
    cards=dict(
        one_liner='高度不限，只看横坐标：排序后，漏出来的点就开新矩形',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['用矩形覆盖所有点，每个矩形宽度不超过 `w`，高度不限',
                 '求最少矩形数',
                 '示例：横坐标 `1 1 2 3 5 7 9`，`w = 2` → `3`'],
        quote='矩形越宽，覆盖的点越多，所以 x2 应该恰好等于 x1+w。',
        quote_src='—— 灵茶山艾府题解',
        idea=['高度没限制 → 只考虑点的横坐标，先排序',
              '初始化 `x2 = -1`，相当于第一个矩形左边已有个矩形',
              '`x > x2` 就开新矩形，`x2 = x + w`'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)`',
                 '`x2` 初始为 `-1`，保证第一个点一定开新矩形',
                 '比较是 `x > x2`：恰好落在边上的点也算覆盖',
                 '只需要按 `p[0]` 排序，纵坐标没用'],
    ),
)
