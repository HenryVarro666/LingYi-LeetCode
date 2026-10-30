def _fin(v):
    return v not in (float('inf'), float('-inf'))


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    P = [(x + y, y - x) for x, y in S['points']]
    cv.text((x0 + 18, y0 + 4), "旋转后的点 (x+y, y−x)：切比雪夫距离 = 横纵坐标差的最大值", 22, T['muted'], bold=True)
    pl, pr, pt, pb = x0 + 190, x1 - 190, y0 + 90, y1 - 80
    xs_ = [p[0] for p in P]
    ys_ = [p[1] for p in P]
    lo_x, hi_x, lo_y, hi_y = min(xs_), max(xs_), min(ys_), max(ys_)

    def X(v):
        return pl + (v - lo_x) / max(1, hi_x - lo_x) * (pr - pl)

    def Y(v):
        return pb - (v - lo_y) / max(1, hi_y - lo_y) * (pb - pt)

    done = 'ans' in S
    cur = S.get('i') if 'i' in S else None
    n_seen = (cur + 1) if (cur is not None and not done) else (len(P) if done else 0)
    # 已经维护好的四条边界
    for key, col, vert in (('max_x1', 'cyan', True), ('min_x1', 'cyan', True), ('max_y1', 'orange', False), ('min_y1', 'orange', False)):
        v = S.get(key)
        if v is not None and _fin(v):
            if vert:
                cv.line([(X(v), pt - 20), (X(v), pb + 20)], T[col], 3)
                cv.text((X(v), pb + 24), f'{key}={v}', 18, T[col], anchor='mt', bold=True)
            else:
                cv.line([(pl - 30, Y(v)), (pr + 30, Y(v))], T[col], 3)
                cv.text((pl - 34, Y(v)), f'{key}={v}', 18, T[col], anchor='rm', bold=True)
    for key, col, vert in (('max_x2', 'cyan', True), ('min_x2', 'cyan', True), ('max_y2', 'orange', False), ('min_y2', 'orange', False)):
        v = S.get(key)
        if v is not None and _fin(v):
            if vert:
                cv.dashed((X(v), pt - 20), (X(v), pb + 20), T[col], 2)
            else:
                cv.dashed((pl - 30, Y(v)), (pr + 30, Y(v)), T[col], 2)
    phase2 = S.get('_line', 0) >= 43
    removed = S.get('i') if phase2 else None
    extremes = {S.get(k) for k in ('max_xi', 'min_xi', 'max_yi', 'min_yi')}
    for k, (px, py) in enumerate(P):
        c = T['text']
        r = 14
        if k == removed:
            c, r = T['pink'], 20
        elif cur is not None and k == cur and not phase2:
            c, r = T['yellow'], 18
        elif k >= n_seen and not phase2:
            c = T['dim']
        cv.rect((X(px) - r, Y(py) - r, X(px) + r, Y(py) + r), fill=c, r=r)
        cv.text((X(px) + 26, Y(py) - 24), f'{k}:({px},{py})', 20, T['muted'], anchor='lm', mono=True)


def _t(S):
    if 'max_x1' not in S:
        return ''
    return (f"x'：最大 {S['max_x1']} 次大 {S['max_x2']} | 最小 {S['min_x1']} 次小 {S['min_x2']}"
            f"　y'：最大 {S['max_y1']} 次大 {S['max_y2']} | 最小 {S['min_y1']} 次小 {S['min_y2']}")


CONFIG = dict(
    num=3102, title='最小化曼哈顿距离', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='切比雪夫距离 · 维护最值与次值',
    tags=['灵神题单·数学算法', '难度分 2216'],
    code='''
class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        max_x1 = max_x2 = max_y1 = max_y2 = -inf
        min_x1 = min_x2 = min_y1 = min_y2 = inf
        max_xi = min_xi = max_yi = min_yi = 0

        for i, (x, y) in enumerate(points):
            x, y = x + y, y - x

            # x 最大次大
            if x > max_x1:
                max_x2 = max_x1
                max_x1 = x
                max_xi = i
            elif x > max_x2:
                max_x2 = x

            # x 最小次小
            if x < min_x1:
                min_x2 = min_x1
                min_x1 = x
                min_xi = i
            elif x < min_x2:
                min_x2 = x

            # y 最大次大
            if y > max_y1:
                max_y2 = max_y1
                max_y1 = y
                max_yi = i
            elif y > max_y2:
                max_y2 = y

            # y 最小次小
            if y < min_y1:
                min_y2 = min_y1
                min_y1 = y
                min_yi = i
            elif y < min_y2:
                min_y2 = y

        ans = inf
        for i in max_xi, min_xi, max_yi, min_yi:
            dx = (max_x2 if i == max_xi else max_x1) - (min_x2 if i == min_xi else min_x1)
            dy = (max_y2 if i == max_yi else max_y1) - (min_y2 if i == min_yi else min_y1)
            ans = min(ans, max(dx, dy))
        return ans
''',
    call='Solution().minimumDistance([[3,10],[5,15],[10,2],[4,4]])',
    expect=12,
    views=[
        dict(type='text', fn=_t, size=22, h=60),
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', fn=lambda S: (f"删点 {S['i']}：dx = {S['dx']}，dy = {S['dy']}" if 'dx' in S and 'ans' in S and S['_line'] >= 50 else ''), size=30, h=60),
    ],
    watch=[('i', 'i', 'yellow'), ('ans', 'ans', 'green'), 'max_xi', 'min_xi', 'max_yi', 'min_yi'],
    skip=['max_xi = min_xi', 'max_x1 = max_x2', 'min_x1 = min_x2', 'max_x2 = max_x1', 'min_x2 = min_x1', 'max_y2 = max_y1', 'min_y2 = min_y1', 'max_xi = i', 'min_xi = i', 'max_yi = i', 'min_yi = i'],
    max_steps=64,
    captions={
        'ans = inf': '前面的遍历结束：四个极值点的下标已记下。只有它们被删，答案才可能变',
        'for i, (x, y)': '枚举第 `{i}` 个点，坐标 `({x}, {y})`',
        'x, y = x + y': '切比雪夫坐标：`(x+y, y−x)` = `({x}, {y})`，曼哈顿距离 = 横纵差的较大者',
        'if x > max_x1': lambda S, B, r: (f'`x = {S.x}` > 最大 `{B.max_x1}` → 成为新的最大，原最大降为次大' if S.x > B.max_x1 else f'`x = {S.x}` 不超过最大 `{B.max_x1}`，再和次大比'),
        'elif x > max_x2': lambda S, B, r: (f'`x = {S.x}` > 次大 `{B.max_x2}` → 成为新的次大' if S.x > B.max_x2 else f'`x = {S.x}` 不超过次大 `{B.max_x2}`，不用动'),
        'if x < min_x1': lambda S, B, r: (f'`x = {S.x}` < 最小 `{B.min_x1}` → 成为新的最小，原最小降为次小' if S.x < B.min_x1 else f'`x = {S.x}` 不小于最小 `{B.min_x1}`，再和次小比'),
        'elif x < min_x2': lambda S, B, r: (f'`x = {S.x}` < 次小 `{B.min_x2}` → 成为新的次小' if S.x < B.min_x2 else f'`x = {S.x}` 不小于次小 `{B.min_x2}`，不用动'),
        'if y > max_y1': lambda S, B, r: (f'`y = {S.y}` > 最大 `{B.max_y1}` → 成为新的最大，原最大降为次大' if S.y > B.max_y1 else f'`y = {S.y}` 不超过最大 `{B.max_y1}`，再和次大比'),
        'elif y > max_y2': lambda S, B, r: (f'`y = {S.y}` > 次大 `{B.max_y2}` → 成为新的次大' if S.y > B.max_y2 else f'`y = {S.y}` 不超过次大 `{B.max_y2}`，不用动'),
        'if y < min_y1': lambda S, B, r: (f'`y = {S.y}` < 最小 `{B.min_y1}` → 成为新的最小，原最小降为次小' if S.y < B.min_y1 else f'`y = {S.y}` 不小于最小 `{B.min_y1}`，再和次小比'),
        'elif y < min_y2': lambda S, B, r: (f'`y = {S.y}` < 次小 `{B.min_y2}` → 成为新的次小' if S.y < B.min_y2 else f'`y = {S.y}` 不小于次小 `{B.min_y2}`，不用动'),
        'max_x1 = x': '次大改为旧最大 `{max_x2}`，最大改为 `{max_x1}`；顺手记下它是第 `{i}` 个点（`max_xi`）',
        'min_x1 = x': '次小改为旧最小 `{min_x2}`，最小改为 `{min_x1}`；记下第 `{i}` 个点（`min_xi`）',
        'max_y1 = y': '次大改为旧最大 `{max_y2}`，最大改为 `{max_y1}`；记下第 `{i}` 个点（`max_yi`）',
        'min_y1 = y': '次小改为旧最小 `{min_y2}`，最小改为 `{min_y1}`；记下第 `{i}` 个点（`min_yi`）',
        'for i in max_xi': lambda S, B, r: (f'只需考虑删这 4 个点：`{S.max_xi}, {S.min_xi}, {S.max_yi}, {S.min_yi}`（别的点删了也没用），现在删点 `{S.i}`' if S.i != B.i else '4 个候选点都试完了'),
        'dx = ': '删点 `{i}` 后 x 方向极差：`{dx}`（若它是最大/最小就改用次大/次小）',
        'dy = ': '删点 `{i}` 后 y 方向极差：`{dy}`',
        'ans = min': '删点 `{i}` 后最大距离 = `max({dx}, {dy})` = {max(dx, dy)}；`ans = min({B.ans}, {max(dx, dy)})` = =={ans}==',
        'return ans': '四种删法里最好的：=={ret}==',
    },
    cards=dict(
        one_liner='曼哈顿距离旋转 45° 变成切比雪夫距离，只看四个极值点',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['删掉恰好一个点，使剩下点两两曼哈顿距离的==最大值最小==',
                 '示例：`[[3,10],[5,15],[10,2],[4,4]]` → `12`'],
        quote='所以要求任意两点曼哈顿距离的最大值，……我们只需要计算任意两个 (x′,y′) 切比雪夫距离的最大值，即横纵坐标差的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`|x1−x2|+|y1−y2| = max(|x1′−x2′|, |y1′−y2′|)`，其中 `(x′,y′)=(x+y, y−x)`',
              '最大距离 = `max(max x′ − min x′, max y′ − min y′)`',
              '删点只会影响最值，所以维护最大次大、最小次小，再==只试 4 个极值点=='],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '最大次大可能相同、最小次小可能相同，用 `>`/`<` 严格比较即可保证次值正确',
                 '另两种写法：有序集合 `O(n log n)`；nlargest/nsmallest 后遍历全部点',
                 '同类：1131 绝对值表达式的最大值、1330 翻转子数组'],
    ),
)
