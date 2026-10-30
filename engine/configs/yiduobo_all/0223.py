def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    A, Bb, C, D, E, F, G, H = (S[k] for k in 'ABCDEFGH')
    xmin, xmax, ymin, ymax = -3, 9, -1, 4
    u = min((x1 - x0 - 120) / (xmax - xmin), (y1 - y0 - 240) / (ymax - ymin))
    ox = x0 + 60 + (x1 - x0 - 120 - u * (xmax - xmin)) / 2
    oy = y1 - 130
    P = lambda x, y: (ox + (x - xmin) * u, oy - (y - ymin) * u)
    cv.text((x0 + 18, y0 + 4), '两个矩形（蓝 = 左边/上面的 A..D，粉 = E..H，绿 = 重叠部分）', 22, T['muted'], bold=True)
    for k in range(xmin, xmax + 1):
        cv.line([P(k, ymin), P(k, ymax)], T['border'], 1)
        cv.text((P(k, ymin)[0], oy + 8), k, 18, T['dim'], anchor='mt', mono=True)
    for k in range(ymin, ymax + 1):
        cv.line([P(xmin, k), P(xmax, k)], T['border'], 1)
        cv.text((P(xmin, k)[0] - 8, P(xmin, k)[1]), k, 18, T['dim'], anchor='rm', mono=True)
    for (a, b, c, d, col) in ((A, Bb, C, D, T['blue']), (E, F, G, H, T['pink'])):
        p, q = P(a, d), P(c, b)
        cv.rect((p[0], p[1], q[0], q[1]), fill=col, alpha=60, outline=col, width=4)
    x, y = S.get('x'), S.get('y')
    if x is not None and y is not None:
        p, q = P(E, H), P(E + x, H - y)
        cv.rect((p[0], p[1], q[0], q[1]), fill=T['green'], alpha=140, outline=T['green'], width=3)
    elif x is not None:
        cv.line([P(E, ymin + .2), P(E + x, ymin + .2)], T['green'], 8)
        cv.text((P(E + x, ymin)[0] + 10, P(E, ymin + .2)[1]), f'重叠水平边长 x = {x}', 22, T['green'], anchor='lm', bold=True)
    if y is not None and x is not None:
        cv.text((x0 + 18, y1 - 100), f'重叠 {x} × {y} = {x * y}', 26, T['green'], bold=True)
    ar = (C - A) * (D - Bb) + (G - E) * (H - F)
    cv.text((x1 - 18, y0 + 40), f'两块面积和 = {(C - A) * (D - Bb)} + {(G - E) * (H - F)} = {ar}', 22, T['muted'], anchor='ra', bold=True)


CONFIG = dict(
    num=223, title='矩形面积', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='总面积减去重叠面积',
    tags=['灵神题单', '数学算法'],
    code='''
class Solution(object):
    def computeArea(self, A, B, C, D, E, F, G, H):

        if A > E:
            A, B, C, D, E, F, G, H = E, F, G, H, A, B, C, D

        if E >= A and E <= C:
            if G < C:
                x = G - E
            else:
                x = C - E
        else:
            x = 0

        if H > D:
            A, B, C, D, E, F, G, H = E, F, G, H, A, B, C, D

        if H <= D and H >= B:
            if F > B:
                y = H - F
            else:
                y = H - B
        else:
            y = 0

        return (C - A) * (D - B) + (G - E) * (H - F) - x * y
''',
    call='sol = Solution()\n[sol.computeArea(-3, 0, 3, 4, 0, -1, 9, 2), sol.computeArea(0, -1, 9, 2, -3, 0, 3, 4)]',
    expect=[45, 45],
    views=[
        dict(type='custom', draw=_draw, h=600),
    ],
    watch=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', ('x', lambda S: S.get('x', '-')), ('y', lambda S: S.get('y', '-'))],
    captions={
        'if A > E': lambda S, B, r: f"先让 A..D 是左边的方形：`A > E` 即 `{S['A']} > {S['E']}` → " + ('==交换两个方形==' if S['A'] > S['E'] else '已经在左边，不换'),
        'A, B, C, D, E, F, G, H = E': '左右颠倒了：把两个方形的坐标整体对调',
        'if E >= A and E <= C': lambda S, B, r: f"右边方形的左边 E 在左方形的横向范围内吗？`{S['A']} <= {S['E']} <= {S['C']}` → " + ('在，才可能重叠' if S['A'] <= S['E'] <= S['C'] else '不在，水平重叠 0'),
        'if G < C': lambda S, B, r: f"右方形的右边 G 也在里面吗？`G < C` 即 `{S['G']} < {S['C']}` → " + ('整个 R2 在 R1 内，边长 G − E' if S['G'] < S['C'] else '不在，只重叠到 C'),
        'x = G - E': '水平重叠边长 `x = G − E` = =={x}==',
        'x = C - E': '水平重叠边长 `x = C − E` = =={x}==',
        'x = 0': '水平方向不相交，`x = 0`，重叠面积必为 0',
        'if H > D': lambda S, B, r: f"再区分上下：让 E..H 是下面的方形。`H > D` 即 `{S['H']} > {S['D']}` → " + ('==交换==' if S['H'] > S['D'] else '已经是下面的，不换'),
        'if H <= D and H >= B': lambda S, B, r: f"下方形的上边 H 在上方形的纵向范围内吗？`{S['B']} <= {S['H']} <= {S['D']}` → " + ('在，才可能重叠' if S['B'] <= S['H'] <= S['D'] else '不在，竖直重叠 0'),
        'if F > B': lambda S, B, r: f"下方形的下边 F 比上方形的下边 B 高吗？`{S['F']} > {S['B']}` → " + ('是，整个在里面，边长 H − F' if S['F'] > S['B'] else '否，重叠到 B'),
        'y = H - F': '竖直重叠边长 `y = H − F` = =={y}==',
        'y = H - B': '竖直重叠边长 `y = H − B` = =={y}==',
        'y = 0': '竖直方向不相交，`y = 0`',
        'return': lambda S, B, r: f"总面积 `{(S['C']-S['A'])*(S['D']-S['B'])} + {(S['G']-S['E'])*(S['H']-S['F'])} − {S['x']}×{S['y']}` = =={r}==",
    },
    cards=dict(
        one_liner='总面积 = 两个方形面积之和 − 重叠面积',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['二维平面上两个边平行坐标轴的矩形，分别给出左下角和右上角',
                 '求它们覆盖的总面积',
                 '示例：`(-3,0,3,4)` 和 `(0,-1,9,2)` → `45`'],
        quote='这个面积S = S(方形1) + S(方形2) - S(重合)，计算两个方形的面积很简单，于是现在题目就变成了如何求重叠部分的面积。',
        quote_src='—— yiduobo 题解原文',
        idea=['先交换，保证 A..D 是左边的方形，再判断水平重叠边长 x',
              '再交换，保证 E..H 是下面的方形，判断竖直重叠边长 y',
              '不重叠时 x 或 y 为 0，减掉 `x*y` 即可'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错点：第二次交换后，A..H 的含义变了，最后求面积用的是交换后的值',
                 '交换只改变谁是 R1，不改变两块面积之和',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
