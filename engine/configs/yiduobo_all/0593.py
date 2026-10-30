def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pts = [S[f'p{i}'] for i in (1, 2, 3, 4)]
    cols = [T['blue'], T['pink'], T['green'], T['orange']]
    u = min((x1 - x0 - 400) / 3.4, (y1 - y0 - 200) / 3.4)
    cx, cy = x0 + 40 + 1.7 * u + 40, (y0 + y1) / 2 + 10
    P = lambda p: (cx + p[0] * u, cy - p[1] * u)
    cv.text((x0 + 18, y0 + 4), '四个点按 p1→p2→p3→p4→p1 连成四边形，看边长和直角', 22, T['muted'], bold=True)
    for k in (-1, 0, 1):
        cv.line([(cx + k * u, cy - 1.7 * u), (cx + k * u, cy + 1.7 * u)], T['border'], 2 if k == 0 else 1)
        cv.line([(cx - 1.7 * u, cy + k * u), (cx + 1.7 * u, cy + k * u)], T['border'], 2 if k == 0 else 1)
    ls = [S.get(f'l{i}') for i in (1, 2, 3, 4)]
    for i in range(4):
        if ls[i] is not None:
            a, b = P(pts[i]), P(pts[(i + 1) % 4])
            cv.line([a, b], T['yellow'], 5)
            m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            ln = S.get(f'len{i + 1}')
            if ln is not None:
                dx, dy = m[0] - cx, m[1] - cy
                nrm = max(1, (dx * dx + dy * dy) ** 0.5)
                cv.text((m[0] + dx / nrm * 40, m[1] + dy / nrm * 30), f'len²={ln}', 20, T['yellow'], anchor='mm', bold=True)
    for i, p in enumerate(pts):
        X, Y = P(p)
        cv.d.ellipse((X - 13, Y - 13, X + 13, Y + 13), fill=cols[i])
        dx, dy = X - cx, Y - cy
        nrm = max(1, (dx * dx + dy * dy) ** 0.5)
        side = abs(dx) > abs(dy)
        cv.text((X + (22 if dx > 0 else -22) if side else X, Y if side else Y + (24 if dy > 0 else -24)), f'p{i + 1}({p[0]},{p[1]})', 22, cols[i], anchor=('lm' if dx > 0 else 'rm') if side else 'mm', bold=True)
    rx = x0 + 40 + 3.4 * u + 80
    ry = y0 + 70
    for i in range(4):
        if ls[i] is not None:
            cv.text((rx, ry + i * 44), f'l{i + 1} = {ls[i]}', 26, T['text'], mono=True)
    if S.get('len1') is not None:
        lens = [S.get(f'len{i}') for i in (1, 2, 3, 4)]
        ok = all(v is not None for v in lens)
        cv.text((rx, ry + 200), '四边长² ' + ' '.join(str(v) for v in lens if v is not None), 24,
                T['green'] if ok and len(set(lens)) == 1 else T['muted'], bold=True)
    if S.get('l4') is not None and S.get('len4') is not None:
        d = [ls[i][0] * ls[(i + 1) % 4][0] + ls[i][1] * ls[(i + 1) % 4][1] for i in range(3)]
        cv.text((rx, ry + 250), '相邻向量点积（0 = 垂直）', 22, T['muted'], bold=True)
        cv.text((rx, ry + 286), ' , '.join(str(v) for v in d), 26, T['green'] if all(v == 0 for v in d) else T['red'], bold=True)


CONFIG = dict(
    num=593, title='有效的正方形', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='枚举三种连点顺序 · 边长 + 点积',
    tags=['灵神题单', '数学算法'],
    code='''
class Solution(object):
    def validSquare(self, p1, p2, p3, p4):

        if p1 == p2 or p1 == p3 or p1 == p4 or p2 == p3 or p2 == p4 or p3 == p4:
            return False

        return self.check(p1, p2, p3, p4) or self.check(p1, p2, p4, p3) or self.check(p1, p3, p2, p4)

    def check(self, p1, p2, p3, p4):
        l1 = [p1[0] - p2[0], p1[1] - p2[1]]
        l2 = [p2[0] - p3[0], p2[1] - p3[1]]
        l3 = [p3[0] - p4[0], p3[1] - p4[1]]
        l4 = [p4[0] - p1[0], p4[1] - p1[1]]

        len1 = l1[0] ** 2 + l1[1] ** 2
        len2 = l2[0] ** 2 + l2[1] ** 2
        len3 = l3[0] ** 2 + l3[1] ** 2
        len4 = l4[0] ** 2 + l4[1] ** 2
        if len1 == len2 and len1 == len3 and len1 == len4:
            if l1[0] * l2[0] + l1[1] * l2[1] == 0 and l2[0] * l3[0] + l2[1] * l3[1] == 0 and l3[0] * l4[0] + l3[1] * l4[1] == 0:
                return True

        return False
''',
    call='Solution().validSquare([1,0], [-1,0], [0,1], [0,-1])',
    expect=True,
    views=[
        dict(type='custom', draw=_draw, h=600),
    ],
    watch=['p1', 'p2', 'p3', 'p4'],
    captions={
        'if p1 == p2': '先排除重合的点：有两点重合一定不是正方形',
        'return self.check(p1, p2, p3, p4) or': lambda S, B, r: ('点的先后、顺逆时针不影响，只需试三种连法：1234、1243、1324' if r is None else f'三种连法试完：=={r}==，说明存在一种连法构成正方形'),
        'l1 = ': '边向量 `l1 = p1 − p2` = {l1}',
        'l2 = ': '边向量 `l2 = p2 − p3` = {l2}',
        'l3 = ': '边向量 `l3 = p3 − p4` = {l3}',
        'l4 = ': '边向量 `l4 = p4 − p1` = {l4}',
        'len1 = ': '边长平方 `len1` = {len1}（用平方，避免开方）',
        'len2 = ': '`len2` = {len2}',
        'len3 = ': '`len3` = {len3}',
        'len4 = ': '`len4` = {len4}',
        'if len1 == len2 and': lambda S, B, r: f"四条边长平方 `{S['len1']}, {S['len2']}, {S['len3']}, {S['len4']}` " + ('==全相等==，再检查直角' if len({S['len1'], S['len2'], S['len3'], S['len4']}) == 1 else '不全相等 → 这种连法不是正方形'),
        'if l1[0] * l2[0]': lambda S, B, r: f"相邻边向量点积 `{S['l1'][0]*S['l2'][0]+S['l1'][1]*S['l2'][1]}, {S['l2'][0]*S['l3'][0]+S['l2'][1]*S['l3'][1]}, {S['l3'][0]*S['l4'][0]+S['l3'][1]*S['l4'][1]}`，点积为 0 即垂直 → " + ('==三个直角，加上四边相等=正方形==' if r is None and S['l1'][0]*S['l2'][0]+S['l1'][1]*S['l2'][1]==0 and S['l2'][0]*S['l3'][0]+S['l2'][1]*S['l3'][1]==0 and S['l3'][0]*S['l4'][0]+S['l3'][1]*S['l4'][1]==0 else '有不垂直的角'),
        'return True': '四边相等且是直角：==这种连法是正方形==',
        'return False': '这种连法不行，回到上一层试下一种连法',
    },
    cards=dict(
        one_liner='四边相等且四个直角：试三种连法，边长看平方，直角看点积',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给四个点的坐标（顺序任意），判断能否组成正方形',
                 '正方形可能斜着放，不能只看水平/竖直线',
                 '本视频：`[1,0] [-1,0] [0,1] [0,-1]` → `true`'],
        quote='判断正方形就是要求四条边的长度相等，且形成的是四个直角。在这里，必须要判断直角，因为正方形可能是斜着放的。',
        quote_src='—— yiduobo 题解原文',
        idea=['点重合直接返回 false',
              '四点的顺序理论上有 24 种，去掉轮转和反向后只剩 3 种',
              '每种连法：四条边平方相等 + 相邻向量点积为 0（垂直）'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错点：只看四边相等会把菱形当成正方形，必须再查直角',
                 '边长用平方比较，点积用整数运算，没有浮点误差',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
