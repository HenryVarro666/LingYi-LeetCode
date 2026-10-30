PTS = [[3, -3], [-1, -2], [-4, 4], [-3, 1], [2, 2], [1, 4]]
LAB = 'abdcab'
LC = {'a': 'pink', 'b': 'blue', 'c': 'green', 'd': 'purple'}


def _cur(S):
    if 'x' in S and 'c' in S and S['_line'] in range(5, 13):
        for i, (p, c) in enumerate(zip(PTS, LAB)):
            if p == [S['x'], S['y']] and c == S['c']:
                return i
    return None


def _plot(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    R = 5
    side = min(x1 - x0 - 60, y1 - y0 - 60)
    cx, cy = (x0 + x1) / 2 - 120, (y0 + y1) / 2 + 10
    u = side / (2 * R)
    P = lambda x, y: (cx + x * u, cy - y * u)
    for k in range(-R + 1, R):
        a, b = P(k, -R + 0.5), P(k, R - 0.5)
        cv.line([a, b], T['border'] if k else T['dim'], 1 if k else 2)
        a, b = P(-R + 0.5, k), P(R - 0.5, k)
        cv.line([a, b], T['border'] if k else T['dim'], 1 if k else 2)
    m2 = S.get('min2')
    fin = m2 is not None and m2 != float('inf')
    if fin:
        q = m2 - 1  # 合法正方形的最大半边长
        if q >= 0:
            (ax, ay), (bx, by) = P(-q, q), P(q, -q)
            cv.rect((ax, ay, bx + 1, by + 1), fill=T['green'], alpha=45)
            for p0, p1 in (((ax, ay), (bx, ay)), ((bx, ay), (bx, by)), ((bx, by), (ax, by)), ((ax, by), (ax, ay))):
                cv.line([p0, p1], T['green'], 3)
        (ax, ay), (bx, by) = P(-m2, m2), P(m2, -m2)
        for p0, p1 in (((ax, ay), (bx, ay)), ((bx, ay), (bx, by)), ((bx, by), (ax, by)), ((ax, by), (ax, ay))):
            cv.dashed(p0, p1, T['red'], 3)
    cur = _cur(S)
    for i, ((x, y), c) in enumerate(zip(PTS, LAB)):
        X, Y = P(x, y)
        col = T[LC[c]]
        if i == cur:
            cv.rect((X - 26, Y - 26, X + 26, Y + 26), outline=T['yellow'], width=5, r=26)
        cv.rect((X - 18, Y - 18, X + 18, Y + 18), fill=col, r=18)
        cv.text((X, Y), c, 24, T['bg'], anchor='mm', bold=True)
        cv.text((X + 24, Y - 22), f'd={max(abs(x), abs(y))}', 20, T['muted'], anchor='lm', mono=True)
    lx = cx + R * u + 20
    cv.text((lx, y0 + 30), '每个点标注切比雪夫距离', 22, T['muted'], bold=True)
    cv.text((lx, y0 + 60), '`d = max(|x|, |y|)`'.strip('`'), 22, T['text'], mono=True)
    cv.line([(lx, y0 + 110), (lx + 40, y0 + 110)], T['red'], 3)
    cv.text((lx + 50, y0 + 110), f"min2 = {m2 if fin else 'inf'}", 22, T['red'], anchor='lm', bold=True)
    cv.text((lx + 50, y0 + 140), '同标签次小距离的最小值', 20, T['muted'], anchor='lm')
    cv.rect((lx, y0 + 180, lx + 40, y0 + 205), fill=T['green'], alpha=90)
    cv.text((lx + 50, y0 + 192), '合法区域 d < min2', 22, T['green'], anchor='lm', bold=True)


def _if(S, B, ret):
    old = B.min_d[S.c] if S.c in B.min_d else float('inf')
    o = 'inf' if old == float('inf') else old
    if old == float('inf'):
        return f'`d = {S.d} < min_d[{S.c!r}] = inf`：第一次见到标签 `{S.c}`，记为最小距离'
    if S.d < old:
        return f'`d = {S.d} < min_d[{S.c!r}] = {o}`：刷新标签 `{S.c}` 的最小距离，==旧最小值降为次小=='
    return f'`d = {S.d} ≥ min_d[{S.c!r}] = {o}`：它不是最小，==可能是次小=='


CONFIG = dict(
    num=3143, title='正方形中的最多点数', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='维护次小距离的最小值',
    tags=['灵神核心路线', '灵神题单·二分算法', '难度分 1697'],
    code='''
class Solution:
    def maxPointsInsideSquare(self, points: List[List[int]], s: str) -> int:
        min_d = defaultdict(lambda: inf)
        min2 = inf
        for (x, y), c in zip(points, s):
            d = max(abs(x), abs(y))
            if d < min_d[c]:
                # d 是目前最小的，那么 min_d[c] 是次小的
                min2 = min(min2, min_d[c])
                min_d[c] = d
            else:
                # d 可能是次小的
                min2 = min(min2, d)
        return sum(d < min2 for d in min_d.values())
''',
    call=f'Solution().maxPointsInsideSquare({PTS}, {LAB!r})',
    expect=2,
    views=[
        dict(type='custom', draw=_plot, h=470),
        dict(type='map', var='min_d', label='min_d：每种标签的最小距离', h=130,
             fmt=lambda k, v: f"'{k}': {'inf' if v == float('inf') else v}"),
    ],
    watch=['x', 'y', 'c', ('d', 'd', 'yellow'), ('min2', 'min2', 'red')],
    captions={
        'min_d = defaultdict': '`min_d[c]`：标签 `c` 的点到原点的==最小==切比雪夫距离',
        'min2 = inf': '`min2`：所有标签「==次小==距离」中的最小值',
        'for (x, y), c': lambda S, B, r: ('所有点处理完毕' if 'c' in B and (B.x, B.y) == (S.x, S.y)
                                         else f'看点 `({S.x}, {S.y})`，标签 `{S.c!r}`'),
        'd = max(': '切比雪夫距离 `d = max(|{x}|, |{y}|) = {d}`：半边长 `≥ {d}` 才能框住它',
        'if d < min_d[c]': _if,
        'min2 = min(min2, min_d[c])': lambda S, B, r: f"`min2 = min({B.min2}, {B.min_d[S.c]}) = {S.min2}`" + (f'：旧最小值 `{B.min_d[S.c]}` 成了次小' if S.min2 != float('inf') else '：旧值是 inf，还没有次小'),
        'min_d[c] = d': '`min_d[{c!r}] = {d}`',
        'min2 = min(min2, d)': lambda S, B, r: f'`min2 = min({B.min2}, {S.d}) = {S.min2}`' + ('：没变，已有更近的「次小」' if S.min2 == B.min2 else f'：半边长到 `{S.min2}` 就会框住两个同标签点'),
        'return sum': '只有 `min_d[c] < min2 = {min2}` 的标签能放进正方形 → =={ret}== 个点',
    },
    cards=dict(
        one_liner='正方形不能碰到任何标签的「次小距离」，取它们的最小值 min2',
        complexity='时间 `O(n + |Σ|)`，空间 `O(|Σ|)`',
        problem=['平面上若干点，`s[i]` 是第 `i` 个点的标签',
                 '中心在原点、边平行坐标轴的正方形内（含边界）==不能有同标签的两点==，求最多包含几个点',
                 '示例：`[[2,2],[-1,-2],[-4,4],[-3,1],[3,-3]], "abdca"` → `2`',
                 '本视频调换顺序并加一个点 `(1,4)` 标签 `b`，答案仍为 `2`'],
        quote='定义 `minD[c]` 为标签为 c 的所有点到 (0,0) 的最小切比雪夫距离……可以在正方形中的点需要满足 ==`minD[c] < min2`==。',
        quote_src='—— 灵茶山艾府题解 · 方法二',
        idea=['点 `(x,y)` 在半边长为 `k` 的正方形内 ⇔ `max(|x|,|y|) ≤ k`',
              '某标签的第二个点一进来就非法 → 半边长必须 `< min2`',
              '无需维护每个标签的次小值，直接维护全局 `min2`'],
        summary=['时间 `O(n + |Σ|)`，空间 `O(|Σ|)`',
                 '`d < min_d[c]` 时被挤下来的旧最小值才是次小，别漏了更新 `min2`',
                 '比较必须是严格 `<`：距离等于 `min2` 的点也会把同标签点带进来',
                 '方法一：二分正方形半边长，check 中用集合判重并直接更新答案，`O(n log U)`'],
    ),
)
