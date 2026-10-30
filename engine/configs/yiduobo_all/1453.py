PTS = [[0, 0], [1, 1], [4, 4]]
R = 2


def _ff(v):
    return '%.2f' % v if abs(v - round(v)) > 1e-9 else '%d' % round(v)


def _centers(S):
    """两个候选圆心；只有「确实是当前这一对飞镖算出来的」才返回"""
    out = []
    if 'center_y2' not in S or 'x1' not in S:
        return out
    for cx, cy in ((S['center_x1'], S['center_y1']), (S['center_x2'], S['center_y2'])):
        ok = all(abs(((px - cx) ** 2 + (py - cy) ** 2) ** 0.5 - R) < 1e-6 for px, py in ((S['x1'], S['y1']), (S['x2'], S['y2'])))
        out.append((cx, cy) if ok else None)
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '飞镖（点）· 钉在靶边上的两个飞镖（粉）→ 两个候选靶心（青 / 橙）', 21, T['muted'], bold=True)
    wx0, wx1, wy0, wy1 = -5, 5, -4, 5
    top, bot = y0 + 90, y1 - 26
    left, right = x0 + 50, x1 - 30
    sc = min((right - left) / (wx1 - wx0), (bot - top) / (wy1 - wy0))
    ox = left + ((right - left) - sc * (wx1 - wx0)) / 2
    oy = top + ((bot - top) - sc * (wy1 - wy0)) / 2

    def P(x, y):
        return ox + (x - wx0) * sc, oy + (wy1 - y) * sc

    for gx in range(wx0, wx1 + 1):
        X = P(gx, 0)[0]
        cv.line([(X, P(0, wy1)[1]), (X, P(0, wy0)[1])], T['border'], 1)
        cv.text((X, P(0, wy0)[1] + 4), gx, 16, T['dim'], anchor='mt', mono=True)
    for gy in range(wy0, wy1 + 1):
        Y = P(0, gy)[1]
        cv.line([(P(wx0, 0)[0], Y), (P(wx1, 0)[0], Y)], T['border'], 1)
        cv.text((P(wx0, 0)[0] - 6, Y), gy, 16, T['dim'], anchor='rm', mono=True)
    cents = _centers(S)
    cols = [T['cyan'], T['orange']]
    for c, col in zip(cents, cols):
        if c:
            X, Y = P(*c)
            cv.d.ellipse((X - R * sc, Y - R * sc, X + R * sc, Y + R * sc), outline=col, width=3)
            cv.d.ellipse((X - 6, Y - 6, X + 6, Y + 6), fill=col)
    pair = [(S['x1'], S['y1']), (S['x2'], S['y2'])] if 'x2' in S else []
    cur = (S['x'], S['y']) if 'x' in S and S.get('_line') in (35, 36, 37, 38) else None
    for px, py in PTS:
        X, Y = P(px, py)
        col = T['pink'] if (px, py) in pair else T['text']
        cv.d.ellipse((X - 9, Y - 9, X + 9, Y + 9), fill=col)
        cv.text((X + 14, Y - 14), f'({px},{py})', 18, col, bold=True)
        if cur == (px, py):
            cv.d.ellipse((X - 16, Y - 16, X + 16, Y + 16), outline=T['yellow'], width=4)
    # 在圆内的飞镖数
    line = S.get('_line', 0)
    if 'cnt1' in S and line >= 33:
        cv.text((x0 + 18, y0 + 34), f"青圈内 cnt1 = {S['cnt1']}", 22, T['cyan'], bold=True)
        cv.text((x0 + 300, y0 + 34), f"橙圈内 cnt2 = {S['cnt2']}", 22, T['orange'], bold=True)
    if 'res' in S:
        cv.text((x1 - 20, y0 + 34), f"目前最多 res = {S['res']}", 22, T['green'], anchor='ra', bold=True)
    if pair and all(c is None for c in cents) and line <= 14 and line >= 13 and 'p_dis' in S:
        pass


def _cap_pdis(S, B, r):
    if S.p_dis > 4 * R * R:
        return f'`p_dis = {S.p_dis}` > 直径平方 `4r² = {4 * R * R}`：两个飞镖离得比靶子直径还远 → 不可能同在靶上'
    return f'`p_dis = {S.p_dis}` ≤ 直径平方 `4r² = {4 * R * R}`：有可能同在靶边上，去求靶心'


def _cap_in(which):
    def f(S, B, r):
        cx, cy = (S.center_x1, S.center_y1) if which == 1 else (S.center_x2, S.center_y2)
        d2 = (S.x - cx) ** 2 + (S.y - cy) ** 2
        ok = d2 <= S.r ** 2 + 0.00001
        return (f'检查飞镖 `({S.x},{S.y})`：到靶心{"一" if which == 1 else "二"}的距离平方 `{_ff(d2)}` '
                + (f'≤ `r² = {S.r ** 2}` → ==在靶内==' if ok else f'> `r² = {S.r ** 2}` → 在靶外'))
    return f


CONFIG = dict(
    num=1453, title='圆形靶内的最大飞镖数量', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='两点定靶心 · 枚举验证',
    tags=['计算几何'],
    setup='from math import sqrt',
    code='''
class Solution(object):
    def numPoints(self, points, r):

        n = len(points)
        res = 1
        for i in range(n - 1):
            for j in range(i + 1, n):
                x1, y1 = points[i]
                x2, y2 = points[j]
                
                p_dis = (x1 - x2) ** 2 + (y1 - y2) ** 2

                if p_dis > 4 * (r ** 2):
                    continue
                else:
                    mid_x = (x1 + x2) / 2.0
                    mid_y = (y1 + y2) / 2.0
                    a = (x2 - x1) * 1.0
                    b = (y2 - y1) * 1.0
                    if b == 0:
                        center_x1 = mid_x
                        center_y1 = mid_y - sqrt(r ** 2 - p_dis / 4.0)
                        center_x2 = mid_x
                        center_y2 = mid_y + sqrt(r ** 2 - p_dis / 4.0)
                    else:
                        tmp = sqrt((r ** 2 - p_dis / 4.0) / (1 + ((a/b) ** 2)))
                        center_x1 = mid_x - tmp
                        center_y1 = a/b * (mid_x - center_x1) + mid_y
                        center_x2 = mid_x + tmp
                        center_y2 = a/b * (mid_x - center_x2) + mid_y
                    

                    cnt1 = cnt2 = 0
                    for x, y in points:
                        if (x - center_x1) ** 2 + (y - center_y1) ** 2 <= r ** 2 + 0.00001:
                            cnt1 += 1
                        if (x - center_x2) ** 2 + (y - center_y2) ** 2 <= r ** 2 + 0.00001:
                            cnt2 += 1

                    res = max(res, cnt1, cnt2)
        
        return res
''',
    call=f'Solution().numPoints({PTS}, {R})',
    expect=2,
    skip=['x1, y1 = points', 'x2, y2 = points', 'mid_x =', 'mid_y =', 'a = (x2', 'b = (y2', 'for x, y in points'],
    max_steps=90,
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=[('i', 'i if "i" in S else "-"', 'pink'), ('j', 'j if "j" in S else "-"', 'pink'),
           ('p_dis', 'p_dis if "p_dis" in S else "-"', 'yellow'),
           ('cnt1', 'cnt1 if "cnt1" in S else "-"', 'cyan'), ('cnt2', 'cnt2 if "cnt2" in S else "-"', 'orange'),
           ('res', 'res', 'green')],
    captions={
        'res = 1': '随便找一个飞镖，把靶子压在它身上就能套住 1 个 → `res = 1`',
        'for i in': lambda S, B, r: ('所有飞镖对都试过了' if 'i' in B and B.i == S.i else f'枚举第一个落在靶==边缘==上的飞镖 `i = {S.i}`'),
        'for j in': lambda S, B, r: ('这个飞镖的所有搭档都试过了' if 'j' in B and B.i == S.i and B.j == S.j and S.j < len(S.points) - 1 else
                                     (f'`j = {S.j}` 是 `i = {S.i}` 的最后一个搭档，之后就没有了' if 'j' in B and B.i == S.i and B.j == S.j else f'再枚举第二个也在靶边上的飞镖 `j = {S.j}`')),
        'x1, y1 = points': '飞镖 A = `({x1}, {y1})`',
        'x2, y2 = points': '飞镖 B = `({x2}, {y2})`',
        'p_dis =': '取飞镖 A=`({x1}, {y1})`、B=`({x2}, {y2})`，距离平方 `p_dis` = =={p_dis}==',
        'if p_dis': _cap_pdis,
        'continue': '直径都不够长，这一对直接跳过',
        'mid_x =': '线段 AB 的中点 x = `{mid_x}`',
        'mid_y =': '中点 y = `{mid_y}`：靶心一定在 AB 的垂直平分线上，且距 A、B 都为 `r`',
        'a = ': '`a = x2 − x1` = {a}',
        'b = ': '`b = y2 − y1` = {b}',
        'if b == 0': lambda S, B, r: (f'AB 中点 `({S.mid_x}, {S.mid_y})`，靶心在它的垂直平分线上；' + ('`b = 0`：AB 水平，平分线是竖线 `x = mid_x`' if S.b == 0 else '`b ≠ 0`：平分线斜着，要解方程')),
        'center_x1 = mid_x\n': '靶心一的 x = 中点 x',
        'center_y1 = mid_y -': '靶心一在中点下方 `sqrt(r² − p_dis/4)` 处 → y = =={center_y1}==',
        'center_x2 = mid_x\n': '靶心二的 x = 中点 x',
        'center_y2 = mid_y +': '靶心二在中点上方同样距离处 → y = =={center_y2}==',
        'tmp = sqrt': lambda S, B, r: f'勾股定理：靶心到中点的水平偏移 `tmp` = =={_ff(S.tmp)}==',
        'center_x1 = mid_x - tmp': lambda S, B, r: f'靶心一 x = `mid_x − tmp` = =={_ff(S.center_x1)}==',
        'center_y1 = a/b': lambda S, B, r: f'再用垂直关系求 y → 靶心一 = `({_ff(S.center_x1)}, {_ff(S.center_y1)})`',
        'center_x2 = mid_x + tmp': lambda S, B, r: f'靶心二 x = `mid_x + tmp` = =={_ff(S.center_x2)}==',
        'center_y2 = a/b': lambda S, B, r: f'靶心二 = `({_ff(S.center_x2)}, {_ff(S.center_y2)})`（与靶心一关于 AB 对称）',
        'cnt1 = cnt2 = 0': '数一数这两个靶子各套住几个飞镖',
        'for x, y in points': lambda S, B, r: ('所有飞镖都数完了' if 'x' in B and B.x == S.x and B.y == S.y else f'检查飞镖 `({S.x}, {S.y})`'),
        'if (x - center_x1)': _cap_in(1),
        'cnt1 += 1': '`cnt1` → =={cnt1}==',
        'if (x - center_x2)': _cap_in(2),
        'cnt2 += 1': '`cnt2` → =={cnt2}==',
        'res = max': lambda S, B, r: f'`res = max({B.res}, {S.cnt1}, {S.cnt2})` = =={S.res}==' + ('，刷新答案' if S.res > B.res else ''),
        'return res': '最多能套住 `{res}` 个飞镖',
    },
    cards=dict(
        after=[dict(heading='特殊情况：两飞镖同一水平线', lines=['`b = y2 − y1 = 0`：AB 水平，垂直平分线是竖线', '靶心的 `x` 就是中点 `mid_x`，只剩 `y = mid_y ± sqrt(r² − p_dis/4)`', '不单独处理的话，`a/b` 会除以 0'])],
        one_liner='最优靶子总能平移到边上卡住两个飞镖：枚举每一对，反推靶心再数点',
        complexity='时间 `O(n³)`，空间 `O(1)`',
        problem=['平面上有若干飞镖 `points`，靶子是半径为 `r` 的圆，位置任意',
                 '求靶子最多能套住（含边界）多少个飞镖',
                 '本视频：`points=[[0,0],[1,1],[4,4]], r=2` → `2`'],
        quote='注意到这里区间合并的结果必然由其中一个或两个区间的边界构成，而这个边界代表的就是对应的飞镖也落在靶子边缘上，于是可以采用一个低配的做法，即枚举飞镖p以及这里另一个落在靶子边缘上的飞镖，通过这两点确定圆的圆心。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想「角度区间」做法：固定一个飞镖在靶边，别的飞镖对应一段圆心角，求最大重叠；但三角函数有精度、还是环形区间，难写',
              '改成低配做法：最优靶子可平移到同时卡住两个飞镖，两点距离 `≤ 2r` 才有解',
              '圆心在 AB 垂直平分线上，联立垂直关系与勾股定理得两个对称靶心，逐个数点；判断时加 `0.00001` 容差'],
        summary=['时间 `O(n³)`：`O(n²)` 对飞镖 × 每对 `O(n)` 数点；空间 `O(1)`',
                 '易错：`b == 0`（AB 水平）要单独处理，否则 `a/b` 除零；`p_dis > 4r²` 要先跳过再开根',
                 '开方有浮点误差，所以比较用 `<= r² + 0.00001`',
                 '原文为 Python 2 风格，`sqrt` 需从 `math` 导入；代码本身未改动（`2.0`、`1.0` 浮点除在 Python 3 下同样成立）',
                 '这里没演示 `res = 1` 的情形：只有一个飞镖或没有合适的对时直接返回 1'],
    ),
)
