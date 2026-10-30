PTS = [[0, 0], [0, 1], [1, 0], [0, 2]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pts = S.get('points')
    if not pts:
        return
    cv.text((x0 + 18, y0 + 4), '平面上的点（蓝 i，粉 j，绿 k；黄边 = 能构成三角形，灰边 = 候选）', 22, T['muted'], bold=True)
    mx = max(p[0] for p in pts)
    my = max(p[1] for p in pts)
    pad = 100
    sc = min((x1 - x0 - 2 * pad - 120) / mx, (y1 - y0 - 2 * pad - 30) / my)
    ox, oy = x0 + (x1 - x0 - mx * sc) / 2, y1 - pad

    def P(p):
        return (ox + p[0] * sc, oy - p[1] * sc)
    for gx in range(mx + 1):
        cv.line([(ox + gx * sc, oy), (ox + gx * sc, oy - my * sc)], T['border'], 1)
        cv.text((ox + gx * sc, oy + 10), gx, 20, T['dim'], anchor='mt', mono=True)
    for gy in range(my + 1):
        cv.line([(ox, oy - gy * sc), (ox + mx * sc, oy - gy * sc)], T['border'], 1)
        cv.text((ox - 12, oy - gy * sc), gy, 20, T['dim'], anchor='rm', mono=True)
    i, j, k = S.get('i'), S.get('j'), S.get('k')
    live = all(v is not None for v in (i, j, k)) and S.get('k', 99) < len(pts)
    if live:
        tri = [P(pts[i]), P(pts[j]), P(pts[k])]
        ok = 'avg' in S and S.get('_line', 0) >= 13
        col = T['yellow'] if ok else T['muted']
        cv.line([tri[0], tri[1], tri[2], tri[0]], col, 5)
        if 'C' in S and S.get('_line', 0) >= 12:
            for (a, b), nm, c in (((0, 1), 'A', S.get('A')), ((0, 2), 'B', S.get('B')), ((1, 2), 'C', S.get('C'))):
                if c is None:
                    continue
                mxp, myp = (tri[a][0] + tri[b][0]) / 2, (tri[a][1] + tri[b][1]) / 2
                cv.text((mxp + 10, myp - 10), f'{c:.2f}', 24, T['cyan'], anchor='lb', bold=True)
    for n, p in enumerate(pts):
        X, Y = P(p)
        col = T['blue'] if n == i else T['pink'] if n == j else T['green'] if n == k and live else T['text']
        cv.rect((X - 11, Y - 11, X + 11, Y + 11), fill=col, r=11)
        cv.text((X + 16, Y - 16), f'P{n}({p[0]},{p[1]})', 22, col, anchor='lb', mono=True)
    res = S.get('res', 0)
    cv.text((x1 - 24, y0 + 40), f'目前最大面积 res = {res:.3f}', 28, T['green'], anchor='ra', bold=True)


def _ok(S):
    return S.A + S.B > S.C and S.A + S.C > S.B and S.B + S.C > S.A


CONFIG = dict(
    num=812, title='最大三角形面积', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='枚举三点 + 海伦公式',
    tags=['计算几何'],
    code='''
class Solution(object):
    def largestTriangleArea(self, points):

        n = len(points)
        res = 0
        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                for k in range(j + 1, n):
                    A = sqrt((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2)
                    B = sqrt((points[i][0] - points[k][0]) ** 2 + (points[i][1] - points[k][1]) ** 2)
                    C = sqrt((points[j][0] - points[k][0]) ** 2 + (points[j][1] - points[k][1]) ** 2)
                    if A + B > C and A + C > B and B + C > A:
                        avg = (A + B + C) / 2
                        s = sqrt(avg * (avg - A) * (avg - B) * (avg - C))
                        res = max(s, res)
        
        return res
''',
    setup='from math import sqrt',
    call=f'Solution().largestTriangleArea({PTS!r})',
    expect=1.0,
    result_fn=lambda r: round(r, 5),
    views=[
        dict(type='text', fn=lambda S: (f"边长 `A={S['A']:.2f}`　`B={S['B']:.2f}`　`C={S['C']:.2f}`" + (f"　半周长 `avg={S['avg']:.2f}`" if 'avg' in S and S.get('_line', 0) >= 13 else '')) if 'C' in S and S.get('_line', 0) >= 12 else '枚举每一组三个点 `i < j < k`，用三边长算面积', size=26, h=70),
        dict(type='custom', draw=_draw, h=640),
    ],
    watch=['i', 'j', 'k', ('res', 'res', 'green')],
    captions={
        'n = len': '只有 `{n}` 个点，`C({n},3) = {n*(n-1)*(n-2)//6}` 组三点，直接暴力枚举',
        'A = sqrt': lambda S, B, r: f'`A` = 点 {S.i} 到点 {S.j} 的距离 = `{S.A:.2f}`',
        'B = sqrt': lambda S, B, r: f'`B` = 点 {S.i} 到点 {S.k} 的距离 = `{S.B:.2f}`',
        'C = sqrt': lambda S, B, r: f'`C` = 点 {S.j} 到点 {S.k} 的距离 = `{S.C:.2f}`',
        'if A + B > C': lambda S, B, r: (f'三边 `{S.A:.2f}, {S.B:.2f}, {S.C:.2f}`：任意两边之和都大于第三边 → ==能构成三角形==' if _ok(S)
                                       else f'三边 `{S.A:.2f}, {S.B:.2f}, {S.C:.2f}`：有一组两边之和 ==不大于== 第三边 → 三点共线，跳过'),
        'avg =': lambda S, B, r: f'海伦公式先求半周长 `avg = (A+B+C)/2 = {S.avg:.2f}`',
        's = sqrt': lambda S, B, r: f'`s = sqrt(avg(avg-A)(avg-B)(avg-C))` = ==面积 {S.s:.2f}==',
        'res = max': lambda S, B, r: f'`res = max({S.s:.2f}, {B.res:.2f})` = =={S.res:.2f}==',
        'return res': '全部 4 组枚举完，最大面积 `{res}`',
    },
    cards=dict(
        one_liner='点很少，三重循环枚举三个点，海伦公式算面积',
        complexity='时间 `O(n³)`，空间 `O(1)`',
        problem=['`points` 是平面上的点，任取三个不同的点组成三角形，求最大面积',
                 '示例：`[[0,0],[0,1],[1,0],[0,2],[2,0]]` → `2.0`',
                 '本视频：`[[0,0],[0,1],[1,0],[0,2]]` → `1.0`（含一组三点共线）'],
        quote='判断能否形成三角形通常是两边长度之和大于第三边，而知道三条边的长度之和则可以使用海伦公式来求解三角形的面积。由于题目给出的点数量非常少，因此可以直接枚举三个点的所有组合。',
        quote_src='—— yiduobo 题解原文',
        idea=['`i < j < k` 三重循环，每组点恰好枚举一次',
              '先算三条边长 `A`、`B`、`C`，三条都满足“两边之和大于第三边”才是三角形',
              '再用海伦公式：半周长 `avg`，面积 = `sqrt(avg(avg−A)(avg−B)(avg−C))`'],
        summary=['时间 `O(n³)`，n ≤ 50 完全够用',
                 '共线的三点算出来是“退化三角形”，靠 `if` 过滤；浮点误差下不如用叉积 `|x1y2 − x2y1| / 2` 稳',
                 '原文已是 Python 3 可运行写法，代码未改；`sqrt` 来自 `math`，在 setup 里导入',
                 '灵神题解对照：叉积公式不需要开根号；更快的做法是先求凸包再旋转卡壳'],
    ),
)
