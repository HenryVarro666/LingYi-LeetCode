LX, LY = 13, 16
R1 = [0, 0, 3, 2]
R2 = [1, 2, 4, 4]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    r1, r2 = S.get('rec1', R1), S.get('rec2', R2)
    ln = S.get('_line')
    which = 'x' if ln == LX else 'y' if ln == LY else None
    ox, oy = x0 + 150, y1 - 120
    u = min((x1 - x0 - 260) / 5, (y1 - y0 - 200) / 5)
    P = lambda x, y: (ox + x * u, oy - y * u)
    cv.text((x0 + 18, y0 + 4), '两个矩形（蓝 = rec1，粉 = rec2），横轴/纵轴各压成线段比较', 22, T['muted'], bold=True)
    for k in range(6):
        cv.line([P(k, 0), P(k, 5)], T['border'], 1)
        cv.line([P(0, k), P(5, k)], T['border'], 1)
        cv.text((P(k, 0)[0], oy + 8), k, 18, T['dim'], anchor='mt', mono=True)
        cv.text((ox - 10, P(0, k)[1]), k, 18, T['dim'], anchor='rm', mono=True)
    for r, c in ((r1, T['blue']), (r2, T['pink'])):
        a, b = P(r[0], r[3]), P(r[2], r[1])
        cv.rect((a[0], a[1], b[0], b[1]), fill=c, alpha=70, outline=c, width=4)
    # x 方向线段
    for (r, c, dy) in ((r1, T['blue'], 40), (r2, T['pink'], 62)):
        hot = which == 'x'
        cv.line([(P(r[0], 0)[0], oy + dy), (P(r[2], 0)[0], oy + dy)], c, 9 if hot else 4)
    for (r, c, dx) in ((r1, T['blue'], 40), (r2, T['pink'], 62)):
        hot = which == 'y'
        cv.line([(ox - dx, P(0, r[1])[1]), (ox - dx, P(0, r[3])[1])], c, 9 if hot else 4)
    if which:
        i = 0 if which == 'x' else 1
        lo, hi = max(r1[i], r2[i]), min(r1[i + 2], r2[i + 2])
        col = T['green'] if lo < hi else T['red']
        if which == 'x':
            cv.line([(P(lo, 0)[0], oy + 84), (P(hi, 0)[0], oy + 84)], col, 9)
            cv.text((P(5, 0)[0] + 20, oy + 84), f'x 交集 [{lo}, {hi}]' + (' 长度>0' if lo < hi else ' 长度≤0'), 22, col, anchor='lm', bold=True)
        else:
            cv.line([(ox - 84, P(0, lo)[1]), (ox - 84, P(0, hi)[1])], col, 9)
            cv.text((ox + 5 * u + 20, P(0, hi)[1]), f'y 交集 [{lo}, {hi}]' + (' 长度>0' if lo < hi else ' 长度≤0'), 22, col, anchor='lm', bold=True)


CONFIG = dict(
    num=836, title='矩形重叠', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='水平/竖直方向分别排除',
    tags=['灵神题单', '数学算法'],
    code='''
class Solution(object):
    def isRectangleOverlap(self, rec1, rec2):

        A, B, C, D = rec1
        E, F, G, H = rec2

        if A == C or B == D:
            return False

        if E == G or F == H:
            return False

        if C <= E or G <= A:
            return False
        
        if D <= F or H <= B:
            return False

        return True
''',
    call='sol = Solution()\n[sol.isRectangleOverlap([0,0,3,2], [1,2,4,4]), sol.isRectangleOverlap([0,0,3,2], [1,1,4,4])]',
    expect=[False, True],
    views=[
        dict(type='custom', draw=_draw, h=600),
    ],
    watch=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
    captions={
        'A, B, C, D = rec1': lambda S, B, r: f"rec1 左下角 `({S['A']}, {S['B']})`，右上角 `({S['C']}, {S['D']})`",
        'E, F, G, H = rec2': lambda S, B, r: f"rec2 左下角 `({S['E']}, {S['F']})`，右上角 `({S['G']}, {S['H']})`",
        'if A == C': '先排除退化：宽或高为 0 的矩形没有面积，不可能重叠',
        'if E == G': 'rec2 同样检查有没有面积',
        'if C <= E': lambda S, B, r: f"水平方向：rec1 在左侧要 `C <= E`（`{S['C']} <= {S['E']}`），在右侧要 `G <= A`（`{S['G']} <= {S['A']}`）→ " + ('==有一个成立，水平分开，不重叠==' if S['C'] <= S['E'] or S['G'] <= S['A'] else '都不成立，水平方向相交'),
        'if D <= F': lambda S, B, r: f"竖直方向：rec1 在下方要 `D <= F`（`{S['D']} <= {S['F']}`），在上方要 `H <= B`（`{S['H']} <= {S['B']}`）→ " + ('==有一个成立，竖直分开（边接触也算），不重叠==' if S['D'] <= S['F'] or S['H'] <= S['B'] else '都不成立，竖直方向相交'),
        'return False': '只是边/角接触或完全分开：==返回 False==',
        'return True': '水平、竖直都相交：==返回 True==',
    },
    cards=dict(
        one_liner='水平、竖直两个维度，哪一维「分开」就不重叠',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['矩形 `[x1, y1, x2, y2]` 是左下角 + 右上角，边平行坐标轴',
                 '相交面积为正才算重叠，仅边或角接触不算',
                 '本视频：`[0,0,3,2]` 与 `[1,2,4,4]`，再看 `[1,1,4,4]`'],
        quote='若rec1与rec2在水平维度上没有重叠，那么rec1可能在rec2的左侧，此时有C <= E，另一种可能是rec1在rec2的右侧，此时有A >= G。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用 A==C 之类排除没有面积的矩形',
              '水平分开：一个在另一个左边或右边；竖直分开：一个在上边或下边',
              '四种「分开」都不满足，两个矩形必然重叠'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错点：比较要带等号，==边接触不算重叠==',
                 '原文为 Python 2 风格，代码无需改动',
                 '对比灵神：他把两个方向压成区间，用 `max < min` 判断'],
    ),
)
