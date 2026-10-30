PTS = [[1, 2], [2, 1], [1, 0], [0, 1]]


def _plot(cv, S, B, box, T):
    x0, y0, x1_, y1_ = box
    pts = S['points']
    cv.text((x0 + 18, y0 + 4), '点（黄 = i、k，粉 = 直角顶点 j，绿 = 推出的第四点）', 22, T['muted'], bold=True)
    gx0, gy0, gx1, gy1 = x0 + 70, y0 + 60, x1_ - 40, y1_ - 50
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
    line = S.get('_line', 0)
    i, j, k = S.get('i'), S.get('j'), S.get('k')
    n = len(pts)
    ok_k = k is not None and i is not None and j is not None and k != i and k != j and line >= 14
    if ok_k:
        pi, pj, pk = pts[i], pts[j], pts[k]
        dot = (pj[0] - pi[0]) * (pj[0] - pk[0]) + (pj[1] - pi[1]) * (pj[1] - pk[1])
        col = T['green'] if dot == 0 else T['red']
        cv.arrow(P(*pj), P(*pi), col, 4)
        cv.arrow(P(*pj), P(*pk), col, 4)
        if dot == 0:
            fx, fy = pi[0] + pk[0] - pj[0], pi[1] + pk[1] - pj[1]
            cv.line([P(*pi), P(fx, fy), P(*pk)], T['green'], 3)
            hit = (fx * 40001 + fy) in S['point_set']
            px, py = P(fx, fy)
            cv.rect((px - 20, py - 20, px + 20, py + 20), outline=T['green'] if hit else T['red'], width=4, r=20)
            cv.text((px + 24, py + 30), f'第四点 ({fx},{fy})', 18, T['green'] if hit else T['red'], mono=True)
    for q, (x, y) in enumerate(pts):
        px, py = P(x, y)
        col, r = T['text'], 13
        if ok_k or (i is not None and line >= 11):
            if q == j and line >= 11:
                col, r = T['pink'], 17
            elif q in (i, k if ok_k else -1):
                col, r = T['yellow'], 17
        cv.rect((px - r, py - r, px + r, py + r), fill=col, r=r)
        cv.text((px + 20, py - 28), f'{q}:({x},{y})', 18, T['muted'], mono=True)


def _vec(S):
    if 'x2' in S and S.get('k') is not None and S.get('_line', 0) >= 16:
        return f"v1 = ({S['x1']}, {S['y1']})，v2 = ({S['x2']}, {S['y2']})，点积 = ({S['x1']})×({S['x2']}) + ({S['y1']})×({S['y2']}) = {S['x1']*S['x2']+S['y1']*S['y2']}"
    return '枚举三个点 i、j、k：j 当直角顶点，看 ji 与 jk 是否垂直'


CONFIG = dict(
    num=963, title='最小面积矩形 II', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='向量点积判直角 · 对角线中点找第四点',
    tags=['灵神题单'],
    setup='from math import sqrt',
    code='''
class Solution(object):
    def minAreaFreeRect(self, points):

        n = len(points)

        point_set = set()
        for x, y in points:
            point_set.add(x * 40001 + y)

        res = None
        for i in range(n):
            for j in range(n):
                if i != j:
                    x1 = points[j][0] - points[i][0]
                    y1 = points[j][1] - points[i][1]
                    for k in range(n):
                        if i != k and j != k:
                            x2 = points[j][0] - points[k][0]
                            y2 = points[j][1] - points[k][1]
                            if x1 * x2 + y1 * y2 == 0:
                                x = points[i][0] + points[k][0] - points[j][0]
                                y = points[i][1] + points[k][1] - points[j][1]
                                if x * 40001 + y in point_set:
                                    area = sqrt(x1 ** 2 + y1 ** 2) * sqrt(x2 ** 2 + y2 ** 2)
                                    if res is None or res > area:
                                        res = area
        if res is None:
            res = 0
            
        return res
''',
    call='Solution().minAreaFreeRect(%r)' % PTS,
    expect=2.0000000000000004,
    views=[
        dict(type='custom', draw=_plot, h=430),
        dict(type='text', h=80, fn=_vec),
        dict(type='set', var='point_set', h=90, fmt=lambda v: f'{v // 40001},{v % 40001}', font=22),
    ],
    watch=['i', 'j', 'k', ('res', 'res', 'green')],
    captions={
        'n = len': '共 `n = {n}` 个点',
        'point_set.add': '点 `({x},{y})` 编码后放入集合',
        'res = None': '`res = None`：还没有找到矩形',
        'for i in range': '`i` 选矩形的一个顶点，接着枚举 `j`（直角顶点）和 `k`（第三个顶点），三者必须两两不同',
        'if x1 * x2': lambda S, B, r: f'`i,j,k = {S.i},{S.j},{S.k}`：点积 `{S.x1}×{S.x2} + {S.y1}×{S.y2}` = =={S.x1 * S.x2 + S.y1 * S.y2}== → ' + ('垂直' if S.x1 * S.x2 + S.y1 * S.y2 == 0 else '不垂直'),
        'if x * 40001': '第四点 = `i + k − j` = `({x},{y})`，在点集里 → =={x * 40001 + y in point_set}==',
        'area = sqrt': '面积 = |v1| × |v2| = `√{x1 ** 2 + y1 ** 2} × √{x2 ** 2 + y2 ** 2}` = =={area}==',
        'res is None or res > area': lambda S, B, r: f'`res` = {S.res}，新面积 {S.area}：' + ('更小 → 更新' if (B.res is None or B.res > S.area) else '不更小 → 不更新'),
        'res = area': '最小面积更新为 =={res}==',
        'if res is None:': lambda S, B, r: '一个矩形都没找到 → 答案取 0' if S.res is None else f'`res` 不是 None，直接返回',
        'return res': '最小面积 =={res}==（边长带根号，是浮点数）',
    },
    skip=[7, 4, 10, 11, 12, 22, 13, 14, 15, 16, 17, 18, 19, 21],
    max_steps=75,
    cards=dict(
        one_liner='三点定矩形：点积判直角，中点公式补第四点',
        complexity='时间 `O(n^3)`，空间 `O(n)`',
        problem=['给出平面上一些点，矩形的边==不一定==平行于坐标轴',
                 '求能组成的矩形的最小面积，不存在返回 `0`',
                 '本视频：`[[1,2],[2,1],[1,0],[0,1]]` → `2.0`（正方形，边长 √2）'],
        quote='只要v1·v2等于0，就说明cos(v1, v2) = 0，也就是说v1和v2夹角的cos等于0，即二者的夹角为90度，就可以得到v1和v2垂直了。',
        quote_src='—— yiduobo 题解原文',
        idea=['矩形斜着放也行 → 至少枚举 ==三个点== 才能定下矩形',
              '`j` 当直角顶点，点积为 0 说明 `ji 垂直 jk`',
              '对角线互相平分：第四点 = `i + k − j`，再去哈希表里查'],
        summary=['时间 `O(n^3)`，空间 `O(n)`',
                 '易错点：`i`、`j`、`k` 必须两两不同，否则向量为零，点积恒为 0',
                 '面积是两条边长相乘，带根号，结果为浮点数',
                 '同一个矩形会从多个直角顶点被重复枚举，取最小不受影响',
                 '原文为 Python 2 风格，本题代码无需修改；`sqrt` 在 setup 里从 math 导入'],
    ),
)
