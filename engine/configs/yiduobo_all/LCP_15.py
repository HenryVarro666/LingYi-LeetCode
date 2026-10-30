def _X(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pts = S['points']
    res = S.get('res') or []
    rest = S.get('rest')
    p = S.get('p')
    ch = S.get('choose')
    idx = S.get('index')
    line = S.get('_line')
    xs = [q[0] for q in pts]
    ys = [q[1] for q in pts]
    mx, my = max(xs) + 1, max(ys) + 1
    cell = min((x1 - x0 - 140) / mx, (y1 - y0 - 130) / my)
    ox, oy = x0 + 80, y1 - 60
    px = lambda i: (ox + pts[i][0] * cell, oy - pts[i][1] * cell)
    cv.text((x0 + 18, y0 + 4), '绿=已走路线 黄=当前位置p 粉=候选choose 橙环=index', 20, T['muted'], bold=True)
    for k in range(mx + 1):
        X = ox + k * cell
        cv.line([(X, oy), (X, oy - my * cell)], T['border'], 1)
        cv.text((X, oy + 10), k, 18, T['dim'], anchor='mt', mono=True)
    for k in range(my + 1):
        Y = oy - k * cell
        cv.line([(ox, Y), (ox + mx * cell, Y)], T['border'], 1)
        cv.text((ox - 12, Y), k, 18, T['dim'], anchor='rm', mono=True)
    for a, b in zip(res, res[1:]):
        cv.arrow(px(a), px(b), T['green'], 4)
    if p is not None and ch is not None and ch != p:
        cv.dashed(px(p), px(ch), T['pink'], 3)
    if p is not None and idx is not None and rest is not None and idx in rest and line == 25 and idx != ch:
        cv.dashed(px(p), px(idx), T['orange'], 2)
    for i in range(len(pts)):
        X, Y = px(i)
        fill = T['blue']
        if i in res:
            fill = T['green']
        if i == p:
            fill = T['yellow']
        if ch is not None and i == ch and i in (rest or ()):
            fill = T['pink']
        r = 18
        cv.d.ellipse((X - r, Y - r, X + r, Y + r), fill=fill, outline=T['bg'], width=3)
        if idx is not None and i == idx and rest is not None and i in rest and line == 25:
            cv.d.ellipse((X - r - 7, Y - r - 7, X + r + 7, Y + r + 7), outline=T['orange'], width=4)
        cv.text((X, Y), i, 22, T['bg'], anchor='mm', bold=True)
        cv.text((X, Y - 28), f'({pts[i][0]},{pts[i][1]})', 16, T['muted'], anchor='mm', mono=True)


def _dirs(S):
    d = S.get('d')
    if 'direction' not in S:
        return ''
    n = len(S['direction'])
    k = len(S.get('res') or []) - 1
    out = []
    for i, c in enumerate(S['direction']):
        out.append(f'==`{c}`==' if (d is not None and i == k and False) else f'`{c}`')
    cur = f"　当前要转的方向：=={d}==" if d and len(S.get('res') or []) <= n else ''
    path = ' → '.join(str(i) for i in (S.get('res') or []))
    return f"转向 {' '.join(out)}{cur}　路线：{path}"


def _cmp(S, B, r):
    if S.choose is None:
        return f'还没有候选，先把 `index = {S.index}` 当作 `choose`'
    c = _X(S.points[S.choose], S.points[S.p], S.points[S.index])
    c2 = c * S.delta
    side = '右' if c > 0 else ('左' if c < 0 else '正后方')
    if c2 > 0:
        return (f'叉积 `X = {c}`：点 {S.index} 在 `p→choose` 的=={side}侧==，比点 {S.choose} 更靠{side} → ==换成它==')
    return f'叉积 `X = {c}`：点 {S.index} 没有比点 {S.choose} 更靠{"右" if S.delta > 0 else "左"} → 保持'


CONFIG = dict(
    num='LCP 15', title='游乐园的迷宫', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='贪心选最外侧点 · 叉积判左右',
    tags=['灵神题单·数学算法'],
    code='''
class Solution(object):
    def visitOrder(self, points, direction):

        n = len(points)
        rest = set(range(n))
        p = 0
        for index in range(1, len(points)):
            if points[index][0] < points[p][0] or (points[index][0] == points[p][0] and points[index][1] < points[p][1]):
                p = index
        
        rest.remove(p)
        res = [p]

        def X(p1, p2, p3):
            return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])

        for d in direction:
            if d == 'L':
                delta = 1
            else:
                delta = -1
            
            choose = None
            for index in rest:
                if choose is None or X(points[choose], points[p], points[index]) * delta > 0:
                    choose = index
            
            res.append(choose)
            rest.remove(choose)
            p = choose
        
        res.extend(list(rest))
        return res
''',
    call='Solution().visitOrder([[1,1],[1,4],[3,2],[2,1],[3,5]], "LRL")',
    expect=[0, 3, 1, 2, 4],
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', fn=_dirs, h=60),
    ],
    watch=[('p', 'p', 'yellow'), ('d', 'd', 'cyan'), ('choose', 'choose', 'pink'), ('index', 'index', 'orange'), ('rest', 'sorted(rest)', 'blue')],
    skip=['def X', 'return (p2[0]', 'n = len(points)', 'rest = set'],
    captions={
        'p = 0': '`p` 记录起点的编号，先假设是 0 号点',
        'if points[index][0] < points[p][0]': '点 {index} 比当前起点 {p} 更靠左（横坐标相同则更靠下）？',
        'p = index': '起点换成点 {index}',
        'rest.remove(p)': '起点出发，从待选集合 `rest` 里拿掉它；`res = [p]` 是路线',
        'for d in direction': lambda S, B, r: ('所有转向都安排完了' if len(S.res) > len(S.direction) else f'要拐的方向 `d = {S.d}`'),
        'delta = 1': '要向左拐：下一站应选==最右侧==的点，给后面的左拐留足空间（`delta = 1`）',
        'delta = -1': '要向右拐：下一站应选==最左侧==的点（`delta = -1`）',
        'choose = None': '本轮重新选下一站：还没有候选',
        'for index in rest': lambda S, B, r: ('剩下的点都比较完了' if B.get('index') == S.index
                                              else f'逐个看剩下的点 `index = {S.index}`'),
        'if choose is None': _cmp,
        'choose = index': '候选改为点 {choose}',
        'res.append(choose)': '本轮最外侧的点是 {choose}，加入路线 → `res = {res}`',
        'rest.remove(choose)': '点 {choose} 已经走过，从 `rest` 移除',
        'p = choose': '站到点 {p}，下一轮从这里出发',
        'res.extend': '最后只剩一个点，没有方向要求，直接接在路线末尾',
        'return res': '路线 `{res}`：每个转向都满足',
    },
    cards=dict(
        one_liner='要左拐就先去最右边的点，要右拐就先去最左边的点',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['给出平面上 `n` 个点和长为 `n-2` 的转向串 `direction`（`L` 左 / `R` 右）',
                 '找一条经过所有点的路线，第 `i` 次拐弯方向与 `direction[i]` 一致',
                 '本视频：`[[1,1],[1,4],[3,2],[2,1],[3,5]]`，`"LRL"`'],
        quote='若接下来需要向左转，那么就提前走到剩下点中最右侧的那个点，反之，则走到剩下点中最左侧的那个点。',
        quote_src='—— yiduobo 题解原文',
        idea=['起点取最左（再最下）的点：其余点都在它的右边，后面方向好判断',
              '把剩下的点都留在==拐弯的那一侧==，之后连续同向拐弯也有点可用',
              '判断「更右 / 更左」用叉积：`X(choose, p, index)` 的正负就是 index 在 `p→choose` 的哪一侧'],
        summary=['时间 `O(n^2)`：共 `n-2` 轮，每轮扫一遍 `rest`；空间 `O(n)`',
                 '作者坦言只有构造方案、没有严格证明；贪心的直觉是「把点留在转弯的内侧」',
                 '叉积符号与左右的对应别记反：`delta * X > 0` 时换候选',
                 '最后剩下的一个点不需要方向，直接 `extend`',
                 '原文已是 Python 3 可运行，没有改动'],
    ),
)
