PTS = [[0, 0], [1, 0], [0, 1], [2, 1]]


def _plot(cv, S, B, box, T):
    x0, y0, x1_, y1_ = box
    cv.text((x0 + 18, y0 + 4), '点与已枚举的点对（黄线 = 当前点对，灰线 = 之前的点对）', 22, T['muted'], bold=True)
    gx0, gy0, gx1, gy1 = x0 + 60, y0 + 60, x1_ - 60, y1_ - 50
    maxx = max(p[0] for p in PTS) + 1
    maxy = max(p[1] for p in PTS) + 1
    s = min((gx1 - gx0) / maxx, (gy1 - gy0) / maxy)

    def P(x, y):
        return gx0 + x * s, gy1 - y * s
    for xx in range(maxx + 1):
        cv.line([P(xx, 0), P(xx, maxy)], T['border'], 1)
        cv.text((P(xx, 0)[0], gy1 + 6), xx, 18, T['dim'], anchor='mt', mono=True)
    for yy in range(maxy + 1):
        cv.line([P(0, yy), P(maxx, yy)], T['border'], 1)
        cv.text((gx0 - 10, P(0, yy)[1]), yy, 18, T['dim'], anchor='rm', mono=True)
    pts = S['points']
    i = S.get('i')
    cur = None
    if 'x2' in S and 'x' in S and S.get('_line', 0) >= 7:
        cur = ((S['x'], S['y']), (S['x2'], S['y2']))
    if i is not None and 'x2' in S:
        pass
    # 已枚举的点对：j < i，或 i 相同时 x2,y2 之前的
    if i is not None:
        done = []
        for a in range(i + 1):
            for b in range(a):
                if a < i or (cur and pts[b] != list(cur[1]) and b < pts.index(list(cur[1]))):
                    done.append((pts[a], pts[b]))
        for a, b in done:
            cv.line([P(*a), P(*b)], (90, 98, 110), 2)
    if cur:
        cv.line([P(*cur[0]), P(*cur[1])], T['yellow'], 5)
    for q, (px_, py_) in enumerate(pts):
        px, py = P(px_, py_)
        col, r = T['text'], 13
        if cur and [px_, py_] in ([*cur[0]], [*cur[1]]):
            col, r = T['yellow'], 17
        cv.rect((px - r, py - r, px + r, py + r), fill=col, r=r)
        cv.text((px + 20, py - 28), f'({px_},{py_})', 18, T['muted'], mono=True)


def _end(S, B):
    try:
        return S.g == B.g
    except Exception:
        return False


def _fmt_k(k, v):
    return f'k={k:g}: [' + ', '.join(('%g' % b) for b in v) + ']'


def _fmt_k2(k, v):
    return f'{k}: [' + ', '.join(('%g' % b) for b in v) + ']'


def _line(S):
    if 'x2' in S and 'dx' in S and S.get('_line', 0) >= 11:
        k = S['dy'] / S['dx'] if S['dx'] else inf
        b = (S['y'] * S['dx'] - S['x'] * S['dy']) / S['dx'] if S['dx'] else S['x']
        return f"斜率 k = {S['dy']}/{S['dx']} = {k:g}，截距 b = {b:g}；中点 key = ({S['x'] + S['x2']}, {S['y'] + S['y2']})"
    return '枚举所有点对：按斜率 k 分组存截距，再按中点分组存斜率'


CONFIG = dict(
    num=3625, title='统计梯形的数目 II', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='斜率分组 · 减去平行四边形',
    tags=['灵神题单', '难度分 2643'],
    code='''
class Solution:
    def countTrapezoids(self, points: List[List[int]]) -> int:
        groups = defaultdict(list)  # 斜率 -> [截距]
        groups2 = defaultdict(list)  # 中点 -> [斜率]

        for i, (x, y) in enumerate(points):
            for x2, y2 in points[:i]:
                dy = y - y2
                dx = x - x2
                k = dy / dx if dx else inf
                b = (y * dx - x * dy) / dx if dx else x
                groups[k].append(b)
                groups2[(x + x2, y + y2)].append(k)

        ans = 0
        for g in groups.values():
            if len(g) == 1:
                continue
            s = 0
            for c in Counter(g).values():
                ans += s * c
                s += c

        for g in groups2.values():
            if len(g) == 1:
                continue
            s = 0
            for c in Counter(g).values():
                ans -= s * c  # 平行四边形会统计两次，减去多统计的一次
                s += c

        return ans
''',
    call='Solution().countTrapezoids(%r)' % PTS,
    expect=1,
    views=[
        dict(type='custom', draw=_plot, h=330),
        dict(type='text', h=70, fn=_line),
        dict(type='map', var='groups', h=150, fmt=_fmt_k, font=22),
        dict(type='map', var='groups2', h=150, fmt=_fmt_k2, font=22),
    ],
    watch=['i', ('k', 'k', 'blue'), ('b', 'b', 'pink'), 's', ('ans', 'ans', 'green')],
    captions={
        'groups = defaultdict': '`groups`：斜率相同的线段放一组，值里存==截距==，同斜率不同截距才是平行线',
        'groups2 = defaultdict': '`groups2`：按==中点==分组，值里存斜率，用来数平行四边形',
        'for i, (x, y)': '枚举右端点 `({x}, {y})`，左边的点用 `points[:i]`，每个点对只枚举一次',
        'dy =': '`dy = {y} - {y2} = {dy}`',
        'dx =': '`dx = {x} - {x2} = {dx}`',
        'k = dy / dx': '点对 `({x},{y})`-`({x2},{y2})`：斜率 `k = {dy}/{dx}` = =={k}==（竖线 `dx = 0` 记为 inf）',
        'b = (y': '截距 `b = (y·dx − x·dy)/dx` = =={b}==；竖线时 `b = x`，用来区分不同的竖线',
        'groups[k].append': '斜率 {k} 这组加入截距 {b}：这一组里两两可以当梯形的上下底',
        'groups2[(x': '中点（和）`({x + x2}, {y + y2})` 这组加入斜率 {k}：中点相同的两条对角线 = 平行四边形',
        16: lambda S, B, r: ('枚举完所有斜率组' if _end(S, B) else f'斜率组 `{S.g}`：' + ('只有 1 条线段，凑不成一对平行边 → 跳过' if len(S.g) == 1 else f'有 {len(S.g)} 条线段，可以选两条')),
        20: '`c` = 这个截距上的线段数（同截距共线，不能同时选）',
        21: '和前面截距不同的 `{s}` 条线段配对：`ans += {s} × {c}` → =={ans}==',
        24: lambda S, B, r: ('枚举完所有中点组' if _end(S, B) else f'中点组，斜率列表 `{S.g}`：' + ('只有 1 条对角线，凑不成平行四边形 → 跳过' if len(S.g) == 1 else '同一中点有多条线段，可能是平行四边形')),
        28: '`c` = 这个斜率上的线段数（共线的对角线不能同时选）',
        29: '平行四边形有两对平行边，第一轮数了两次，这里减去一次：`ans -= {s} × {c}` → =={ans}==',
        'return ans': '梯形个数 =={ans}==',
    },
    skip=[3, 4, 7, 8, 9, 15, 17, 18, 19, 22, 25, 26, 27, 30],
    max_steps=80,
    cards=dict(
        one_liner='平行边按斜率+截距分组数梯形，再减去多数的平行四边形',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['给出平面上的点，求任选四个点能组成的==梯形==个数',
                 '梯形：凸四边形，至少有一对平行边',
                 '本视频：`[[0,0],[1,0],[0,1],[2,1]]` → `1`'],
        quote='把斜率相同的直线放在同一组，可以从中选择一对平行边，作为梯形的顶边和底边。不能选两条重合的边，所以还要按照截距分组。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举所有点对，算==斜率 k 和截距 b==，同斜率不同截距 = 一对平行边',
              '平行四边形有两对平行边，被数了两次',
              '平行四边形的==对角线中点重合==：按中点分组再减一次'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`',
                 '易错点：同斜率同截距是共线，不能当上下底；竖线（`dx = 0`）斜率记为 `inf`，截距记为 `x`',
                 '中点用 `(x+x2, y+y2)` 避免小数；中点相同的组内还要按斜率分，共线的两条对角线不算',
                 '优化前用哈希表套哈希表；本版先存列表，长度为 1 的组直接跳过，更快',
                 '梯形个数 = 平行边对数 − 平行四边形个数'],
    ),
)
