def _groups(P):
    """segment i = P[i]->P[i+1]; group id per segment (new group when slope changes)"""
    g, pdy, pdx, k = [], 1, 0, 0
    for i in range(len(P) - 1):
        dy, dx = P[i + 1][1] - P[i][1], P[i + 1][0] - P[i][0]
        if dy * pdx != pdy * dx:
            k += 1
            pdy, pdx = dy, dx
        g.append(k)
    return g


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    P = sorted(tuple(p) for p in S['stockPrices'])
    n = len(P)
    cv.text((x0 + 18, y0 + 4), '折线图（排序后）：同色 = 同一线段，黄 = 当前比较', 24, T['muted'], bold=True)
    xs = [p[0] for p in P]; ys = [p[1] for p in P]
    lx, hx, ly, hy = min(xs), max(xs), min(ys), max(ys)
    L, R, Tp, Bt = x0 + 70, x1 - 50, y0 + 120, y1 - 60
    def X(v): return L + (v - lx) / max(1, hx - lx) * (R - L)
    def Y(v): return Bt - (v - ly) / max(1, hy - ly) * (Bt - Tp)
    cv.line([(L - 20, Bt + 20), (R + 20, Bt + 20)], T['border'], 2)
    sorted_ok = all(P[i][0] < P[i + 1][0] for i in range(n - 1))
    cur = _cur(S, P)
    g = _groups(P) if sorted_ok else []
    cols = [T['cyan'], T['orange'], T['purple'], T['pink'], T['green']]
    for i in range(n - 1):
        c = (125, 133, 145)
        if sorted_ok and cur is not None:
            if cur >= n - 1:
                c = cols[g[i] % len(cols)]
            elif i == cur:
                c = T['yellow']
            elif i < cur:
                c = cols[g[i] % len(cols)]
        cv.line([(X(P[i][0]), Y(P[i][1])), (X(P[i + 1][0]), Y(P[i + 1][1]))], c, 6 if c == T['yellow'] else 4)
    for i, (px, py) in enumerate(P):
        cv.rect((X(px) - 7, Y(py) - 7, X(px) + 7, Y(py) + 7), fill=T['text'], r=7)
        cv.text((X(px), Y(py) - 14), f'({px},{py})', 18, T['dim'], anchor='mb', mono=True)

def _cur(S, P):
    if S.get('_line') == 17:
        return len(P) - 1
    if 'qx' in S and 'index' in S:
        return S['index'] - 1
    if 'px' in S:
        return 0
    return None

CONFIG = dict(
    num=2280, title='表示一个折线图的最少线段数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='排序 + 向量叉积判共线',
    tags=['灵神题单·数学算法', '难度分 1681'],
    code='''
class Solution(object):
    def minimumLines(self, stockPrices):
        res = 0
        if len(stockPrices) == 1:
            return 0
        elif len(stockPrices) == 2:
            return 1
        else:
            sorted_info = sorted(stockPrices, key=lambda d:d[0])
            px, py = sorted_info[1][0] - sorted_info[0][0], sorted_info[1][1] - sorted_info[0][1]
            for index in range(2, len(sorted_info)):
                qx, qy = sorted_info[index][0] - sorted_info[index - 1][0], sorted_info[index][1] - sorted_info[index - 1][1]
                if px * qy != py * qx:
                    res += 1
                    px, py = qx, qy
        
        return res + 1
''',
    call='Solution().minimumLines([[4,6],[1,1],[3,5],[6,4],[2,3],[5,5]])',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', fn=lambda S: (f"向量 p=`({S['px']}, {S['py']})`，q=`({S['qx']}, {S['qy']})`；叉积 `px×qy = {S['px']*S['qy']}`，`py×qx = {S['py']*S['qx']}`")
             if 'qx' in S else (f"第一个向量 p=`({S['px']}, {S['py']})`" if 'px' in S else '')),
    ],
    watch=[('res', 'res', 'green'), 'px', 'py', 'qx', 'qy', 'index'],
    captions={
        'len(stockPrices) == 1': '边界：只有一个点，没有线段 → `0`',
        'len(stockPrices) == 2': '边界：两个点，恰好一条线段 → `1`',
        'sorted_info = sorted': '按 x 坐标从小到大排序，相邻点才是折线上的相邻顶点',
        'px, py = sorted_info': '第一、二个点形成的向量 `p = ({px}, {py})`',
        'qx, qy =': '第 `{index-1}`、`{index}` 个点形成的向量 `q = ({qx}, {qy})`',
        'if px * qy': lambda S, B, r: (f'叉积判共线：`px×qy = {S.px*S.qy}`，`py×qx = {S.py*S.qx}`，'
                                       + ('==不相等 → 不共线，折了一下，多一条线段==' if S.px*S.qy != S.py*S.qx else '==相等 → 共线，仍是同一条线段==')),
        'res += 1': '出现拐点，`res` → {res}',
        'px, py = qx, qy': '当前向量成为新的参照：`p = ({px}, {py})`',
        'return res + 1': '`res = {res}` 个拐点，线段数 = 拐点数 + 1 = `{res + 1}`',
    },
    cards=dict(
        one_liner='相邻三点不共线就是一个拐点，线段数 = 拐点数 + 1',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`stockPrices[i] = [day, price]`，相邻点连成折线图',
                 '求表示这条折线所需的 ==最少线段数==',
                 '本视频：`[[4,6],[1,1],[3,5],[6,4],[2,3],[5,5]]` → `3`'],
        quote='如果相邻的三点不在一条直线上，那么就会产生一条折线，于是可以将所有点先按照x坐标从小到大排序，然后一趟遍历，判断相邻的三点是否共线。',
        quote_src='—— yiduobo 题解原文',
        idea=['先处理边界：1 个点 `0` 条，2 个点 `1` 条',
              '一般情况：每个相邻点对是一个向量，比较前后两个向量',
              '叉积 `px*qy - py*qx = 0` 说明共线；不为 0 就是拐点，`res += 1`',
              '最后 `res + 1`：第一条线段还没算进去'],
        summary=['时间 `O(n log n)`，空间 `O(n)`（`sorted` 产生新列表）',
                 '叉积全是整数乘法，没有除法，不会有浮点误差',
                 '==返回 `res + 1`==：`res` 数的是拐点，不是线段',
                 '`px, py` 只在拐点处更新；共线时方向相同，不用改',
                 '对比灵神：灵神用 `1/0` 初始斜率省掉了边界特判；yiduobo 单独判断 1、2 个点'],
    ),
)
