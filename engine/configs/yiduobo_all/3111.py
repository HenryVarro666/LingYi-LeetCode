def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pts = S['points']
    w = S['w']
    cv.text((x0 + 18, y0 + 4), '横坐标（排序后）：每个矩形盖住一段长度 w 的区间', 24, T['muted'], bold=True)
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
    live = 'p' in S and 'q' in S
    p = S.get('p', 0)
    q = S.get('q', 0)
    # 已完成的矩形：p 之前已经分段
    if 'p' in S:
        i = 0
        k = 0
        cols = [T['cyan'], T['purple']]
        while i < min(p, len(pts)):
            j = i + 1
            while j < len(pts) and pts[j][0] - pts[i][0] <= w:
                j += 1
            if j <= p:
                a = left + (pts[i][0] - lo) * sc
                b = left + (pts[i][0] + w - lo) * sc
                cv.rect((a - 10, base - 110 - 30 * (k % 2), b + 10, base - 20), fill=cols[k % 2], alpha=70, r=8)
                k += 1
            i = j
    if live and p < len(pts):
        a = left + (pts[p][0] - lo) * sc
        b = left + (pts[p][0] + w - lo) * sc
        cv.rect((a - 10, base - 150, b + 10, base - 10), fill=T['yellow'], alpha=60, r=8)
        cv.text((a, base - 160), f'矩形左端 = {pts[p][0]}，右端 = {pts[p][0] + w}', 22, T['yellow'], anchor='lb', bold=True)
    for idx, (x, y) in enumerate(pts):
        X = left + (x - lo) * sc
        col = T['text']
        if 'p' in S:
            if idx < p:
                col = T['green']
            elif idx == p:
                col = T['blue']
            elif idx < q:
                col = T['yellow']
            elif idx == q and q < len(pts):
                col = T['pink']
        cv.circle((X, base - 30 - (idx % 3) * 14), 11, col) if hasattr(cv, 'circle') else cv.rect((X - 9, base - 40 - (idx % 3) * 14, X + 9, base - 22 - (idx % 3) * 14), fill=col, r=9)
    cv.text((x0 + 18, y1 - 50), 'p = 新矩形的起点（蓝），q = 第一个没被盖住的点（粉），黄 = 被盖住，绿 = 已处理', 20, T['muted'])


CONFIG = dict(
    num=3111, title='覆盖所有点的最少矩形数目', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='排序 + 双指针放线段',
    tags=['灵神题单', '贪心与思维', '难度分 1401'],
    code='''
class Solution(object):
    def minRectanglesToCoverPoints(self, points, w):

        points.sort()
        p = 0
        res = 0
        while p < len(points):
            q = p + 1
            while q < len(points) and points[q][0] - points[p][0] <= w:
                q += 1
            
            res += 1
            p = q
        
        return res
''',
    call='Solution().minRectanglesToCoverPoints([[5,1],[1,0],[2,7],[7,3],[3,4],[1,9],[9,2]], 2)',
    expect=3,
    views=[
        dict(type='array', var=lambda S: [pt[0] for pt in S['points']], pointers={'p': 'blue', 'q': 'pink'}, label='排序后各点的横坐标', h=200),
        dict(type='custom', draw=_draw, h=420),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink'), ('res', 'res', 'green')],
    captions={
        'points.sort()': '矩形没有高度限制，只看横坐标：先==从小到大排序==',
        'p = 0': '最左侧的点一定要被盖住：`p = {p}`',
        'res = 0': '`res` 记录矩形个数',
        'q = p + 1': '从 `p` 的下一个点开始，看有哪些点被同一个矩形盖住',
        'while q < len(points) and': lambda S, B, r: (f"`{S.points[S.q][0]} − {S.points[S.p][0]} = {S.points[S.q][0] - S.points[S.p][0]} <= w = {S.w}`：==在矩形内==，继续" if S.q < len(S.points) and S.points[S.q][0] - S.points[S.p][0] <= S.w else (f"`q = {S.q}` 已到末尾，没有更多点" if S.q >= len(S.points) else f"`{S.points[S.q][0]} − {S.points[S.p][0]} = {S.points[S.q][0] - S.points[S.p][0]} > w = {S.w}`：==超出矩形== → 停")),
        'q += 1': '又盖住一个点，`q` → {q}',
        'res += 1': '`p` 到 `q-1` 的点由一个矩形盖住 → `res` = =={res}==',
        'p = q': '下一个矩形从第一个没盖住的点开始：`p` = {p}',
        'return res': '所有点都盖住了，最少 `{res}` 个矩形',
    },
    cards=dict(
        one_liner='矩形不限高，就是一条线上用长 w 的线段盖点',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['平面上有一些点，用宽度不超过 `w` 的矩形覆盖，高度不限',
                 '求覆盖所有点最少需要几个矩形',
                 '示例：横坐标 `1 1 2 3 5 7 9`，`w = 2` → `3`'],
        quote='由于需要覆盖所有点，因此最左侧的线段的左端点就应该放置在最左侧点所处的位置上',
        quote_src='—— yiduobo 题解原文',
        idea=['高度没限制，问题变成一条直线上放线段盖点',
              '先排序，最左侧点必须被盖：线段左端放在它上面',
              '双指针：`p` 是起点，`q` 往右找第一个盖不住的点，再从 `q` 重来'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)`',
                 '`points.sort()` 按横坐标排序（横坐标相同再比纵坐标，不影响结果）',
                 '易错点：条件是 `<= w`，边上的点也算覆盖',
                 '对比灵神：灵神用 `x2` 记录右端点，只遍历一次；这里用 `p`、`q` 双指针划分每一段'],
    ),
)
