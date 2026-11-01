TOYS = [[1, 3, 2], [2, 6, 1]]
CIRCLES = [[3, 3], [1, 0], [3, 1]]
R0 = 4


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '平面图（橙 = 玩具，白点 = 圈心，黄 = 当前玩具，粉环 = 正在试的圈）', 22, T['muted'], bold=True)
    gx0, gy0, gx1, gy1 = x0 + 50, y0 + 50, x1 - 30, y1 - 40
    W, H = 11.0, 11.0
    sc = min((gx1 - gx0) / W, (gy1 - gy0) / H)
    ox = gx0 + ((gx1 - gx0) - sc * W) / 2
    oy = gy1 - ((gy1 - gy0) - sc * H) / 2

    def P(x, y):
        return ox + x * sc, oy - y * sc

    for k in range(0, 11):
        X, Y = P(k, 0)
        cv.line([P(k, 0), P(k, 10)], T['border'], 1)
        cv.line([P(0, k), P(10, k)], T['border'], 1)
        cv.text((X, Y + 6), k, 16, T['dim'], anchor='mt', mono=True)
        cv.text((P(0, k)[0] - 8, P(0, k)[1]), k, 16, T['dim'], anchor='rm', mono=True)
    cur = S.get('t') if 't' in S else None
    for t in TOYS:
        px, py = P(t[0], t[1])
        rr = t[2] * sc
        is_cur = cur is not None and t == cur
        cv.rect((px - rr, py - rr, px + rr, py + rr), fill=T['yellow'] if is_cur else T['orange'], alpha=150 if is_cur else 70,
                outline=T['yellow'] if is_cur else T['orange'], width=3, r=rr)
    ring = S.get('_line') in CHECK_LINES and 'cy' in S and 'cx' in S
    for c in CIRCLES:
        px, py = P(c[0], c[1])
        cv.rect((px - 6, py - 6, px + 6, py + 6), fill=T['text'], r=6)
    if ring:
        px, py = P(S['cx'], S['cy'])
        rr = R0 * sc
        cv.rect((px - rr, py - rr, px + rr, py + rr), outline=T['pink'], width=4, r=rr)
        cv.rect((px - 9, py - 9, px + 9, py + 9), outline=T['pink'], width=4, r=9)


def _grp(S):
    a = S.get('a')
    if not a:
        return '按横坐标分组：（还没分）'
    return '按横坐标分组 `a`：' + '  '.join(f'x={g[0]}:{g[1]}' for g in a)


CHECK_LINES = (25, 26, 30, 31)

CONFIG = dict(
    num='LCP 42', title='玩具套圈', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='排序分组 二分找圈（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def circleGame(self, toys: List[List[int]], circles: List[List[int]], r0: int) -> int:
        ans = 0
        circles.sort(key=lambda p: (p[0], p[1]))

        # 将横坐标相同的圈分为一组
        a, y = [], -1
        for p in circles:
            if len(a) == 0 or p[0] > a[-1][0]:
                a.append([p[0], [p[1]]])
                y = -1
            elif p[1] > y:  # 去重
                a[-1][1].append(p[1])
                y = p[1]

        for t in toys:
            x, y, r = t[0], t[1], t[2]
            if r > r0:
                continue
            i = bisect_left(a, x + r - r0, key=lambda g: g[0])
            while i < len(a) and a[i][0] - r0 <= x - r:
                cx, ys = a[i][0], a[i][1]
                j = bisect_left(ys, y)
                if j < len(ys):
                    cy = ys[j]
                    if (x - cx) * (x - cx) + (y - cy) * (y - cy) <= (r0 - r) * (r0 - r):
                        ans += 1
                        break
                if j > 0:
                    cy = ys[j - 1]
                    if (x - cx) * (x - cx) + (y - cy) * (y - cy) <= (r0 - r) * (r0 - r):
                        ans += 1
                        break
                i += 1
        return ans
''',
    call='Solution().circleGame([[1,3,2],[2,6,1]], [[3,3],[1,0],[3,1]], 4)',
    expect=1,
    skip=['y = p[1]', 'x, y, r = t[0]', 'cx, ys = a[i][0]', 'i += 1', 'ans = 0', 'a, y = [], -1'],
    views=[
        dict(type='text', fn=_grp),
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=['r0', ('x', 'x', 'yellow'), ('y', 'y', 'yellow'), ('r', 'r', 'yellow'), ('i', 'i', 'blue'), ('j', 'j', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'circles.sort': '圈按 `(x, y)` 排序：`{circles}`，相同横坐标的会挨在一起',
        'if len(a) == 0 or p[0] > a[-1][0]': lambda S, B, r_: (f'`p = {S.p}`' + (' 的横坐标比最后一组大（或还没有组）→ ==开一个新组==' if (not S.a or S.p[0] > S.a[-1][0]) else ' 的横坐标和最后一组相同 → 不开新组')),
        'a.append([p[0], [p[1]]])': '新开一组：横坐标 `{p[0]}`，纵坐标列表 `[{p[1]}]` → `a = {a}`',
        'elif p[1] > y': '横坐标相同，纵坐标比组内上一个大 `({p[1]} > {y})` 才加入（去重）',
        'a[-1][1].append(p[1])': '同一组再加一个纵坐标：`a = {a}`',
        'for t in toys': lambda S, B, r_: ('所有玩具都枚举完了' if 't' in B and B['t'] == S.t else f'枚举玩具 `t = {S.t}`：坐标 `({S.t[0]}, {S.t[1]})`，半径 `{S.t[2]}`'),
        'if r > r0': lambda S, B, r_: (f'玩具半径 `{S.r}` > 圈半径 `{S.r0}`：任何圈都套不住，跳过' if S.r > S.r0 else f'玩具半径 `{S.r}` <= 圈半径 `{S.r0}`：有可能被套住'),
        'i = bisect_left': '圈的最右端 `cx + r0` 必须 >= 玩具最右端 `x + r`：二分得到第一个满足的组 `i = {i}`',
        'while i < len(a)': lambda S, B, r_: (f'第 `{S.i}` 组横坐标 `{S.a[S.i][0]}`：最左端 `{S.a[S.i][0] - S.r0}` <= 玩具最左端 `{S.x - S.r}` → ==这一组可能套住== ' if S.i < len(S.a) and S.a[S.i][0] - S.r0 <= S.x - S.r else '再往右的组，圈的左端已超过玩具左端 → 没有更多候选，换下一个玩具'),
        'j = bisect_left(ys, y)': '在这一组的纵坐标 `{ys}` 里二分：第一个 `>= {y}` 的位置 `j = {j}`',
        'if j < len(ys)': lambda S, B, r_: (f'`j = {S.j} < {len(S.ys)}`：有一个不小于玩具纵坐标的圈（正上方最近的）' if S.j < len(S.ys) else f'`j = {S.j}`：没有比玩具更高的圈'),
        'cy = ys[j]': '取上方最近的圈：`cy = {cy}`',
        'cy = ys[j - 1]': '取下方最近的圈：`cy = {cy}`',
        'if (x - cx)': lambda S, B, r_: (f'圆心距平方 `{(S.x - S.cx) ** 2 + (S.y - S.cy) ** 2}` ' + ('<=' if (S.x - S.cx) ** 2 + (S.y - S.cy) ** 2 <= (S.r0 - S.r) ** 2 else '>') + f' `(r0 - r)^2 = {(S.r0 - S.r) ** 2}` → ' + ('==套住了==' if (S.x - S.cx) ** 2 + (S.y - S.cy) ** 2 <= (S.r0 - S.r) ** 2 else '套不住')),
        'ans += 1': '这个玩具被套中，`ans` → {ans}',
        'break': '已经有圈套中它了，不必再找（多个圈只算一个）',
        'if j > 0': lambda S, B, r_: (f'`j = {S.j} > 0`：有一个比玩具低的圈（正下方最近的）' if S.j > 0 else '`j = 0`：没有更低的圈'),
        'return ans': '所有玩具都看完了，套中 `{ans}` 个',
    },
    cards=dict(
        one_liner='半径很小：二分出能套住玩具的几列圈，每列再二分最近的上下两个',
        complexity='时间 `O(n log m)`（半径小，每个玩具只看常数列），空间 `O(m)`',
        problem=['玩具 `[x, y, r]`，圈的半径都是 `r0`，圈心 `[x, y]`',
                 '玩具被某个圈完整盖住就算套中，被多个圈套中只算一个',
                 '本视频：2 个玩具、3 个圈、`r0 = 4`，答案 `1`'],
        quote='注意到半径很小，我们可以枚举每个玩具，并暴力枚举该玩具周围是否有可以套住该玩具的圈。',
        quote_src='—— 灵茶山艾府题解',
        idea=['圈排序后，横坐标相同的分成一组，组内纵坐标去重',
              '能套住玩具的圈，横坐标只可能落在一小段里 → 二分出起点，往右扫',
              '每组只要看纵坐标最接近玩具的上下两个圈'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python；`sort.Slice` 写成 `circles.sort(key=...)`，`sort.Search` 写成 `bisect_left(..., key=...)`，`for ; cond; i++` 写成 `while` + `i += 1`',
                 '套住条件：`r <= r0` 且圆心距平方 `<= (r0 - r)^2`',
                 '一个玩具找到一个圈就 `break`，保证不重复计数',
                 '半径 `<= 10` 才让扫描的列数是常数'],
    ),
)
