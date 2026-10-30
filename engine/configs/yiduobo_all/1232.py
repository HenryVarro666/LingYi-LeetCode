def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    P = [tuple(p) for p in S['coordinates']]
    cv.text((x0 + 18, y0 + 4), '点集：虚线 = 过前两点的直线，黄 = 正在检查的点', 24, T['muted'], bold=True)
    xs = [p[0] for p in P]; ys = [p[1] for p in P]
    lx, hx, ly, hy = min(xs), max(xs), min(ys), max(ys)
    L, R, Tp, Bt = x0 + 70, x1 - 60, y0 + 110, y1 - 60
    def X(v): return L + (v - lx) / max(1, hx - lx) * (R - L)
    def Y(v): return Bt - (v - ly) / max(1, hy - ly) * (Bt - Tp)
    cv.line([(L - 20, Bt + 20), (R + 20, Bt + 20)], T['border'], 2)
    # 过 P0、P1 的直线（延伸到整个 x 范围）
    dx, dy = P[1][0] - P[0][0], P[1][1] - P[0][1]
    if dx != 0:
        ya = P[0][1] + dy * (lx - P[0][0]) / dx
        yb = P[0][1] + dy * (hx - P[0][0]) / dx
        cv.dashed((X(lx), max(Tp - 20, min(Bt + 20, Y(ya)))), (X(hx), max(Tp - 20, min(Bt + 20, Y(yb)))), T['cyan'], 3)
    cur = S.get('index') if 'x2' in S else None
    bad = cur is not None and S['x1'] * S['y2'] != S['x2'] * S['y1']
    for i, (px, py) in enumerate(P):
        c = T['text']
        if i < 2:
            c = T['cyan']
        elif cur is not None and i < cur:
            c = T['green']
        elif cur is not None and i == cur:
            c = T['red'] if bad else T['yellow']
        cv.rect((X(px) - 9, Y(py) - 9, X(px) + 9, Y(py) + 9), fill=c, r=9)
        cv.text((X(px), Y(py) - 16), f'#{i} ({px},{py})', 18, T['dim'], anchor='mb', mono=True)


CONFIG = dict(
    num=1232, title='缀点成线', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='叉积判断共线',
    tags=['灵神题单·数学算法'],
    code='''
class Solution(object):
    def checkStraightLine(self, coordinates):
        x1 = coordinates[1][0] - coordinates[0][0]
        y1 = coordinates[1][1] - coordinates[0][1]
        for index in range(2, len(coordinates)):
            x2 = coordinates[index][0] - coordinates[0][0]
            y2 = coordinates[index][1] - coordinates[0][1]
            if x1 * y2 != x2 * y1:
                return False
        
        return True
''',
    call='Solution().checkStraightLine([[0,0],[2,1],[4,2],[6,3],[8,5]])',
    expect=False,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', fn=lambda S: (f"向量1 `({S['x1']}, {S['y1']})`，向量2 `({S['x2']}, {S['y2']})`；`x1×y2 = {S['x1']*S['y2']}`，`x2×y1 = {S['x2']*S['y1']}`")
             if 'x2' in S else (f"点 0 到点 1 的向量 `({S['x1']}, {S['y1']})`" if 'y1' in S else '')),
    ],
    watch=['index', 'x1', 'y1', 'x2', 'y2'],
    captions={
        'x1 = coordinates[1][0]': '以点 0 为起点，点 1 的 x 方向增量 `x1 = {x1}`',
        'y1 = coordinates[1][1]': '点 1 的 y 方向增量 `y1 = {y1}`：向量 `({x1}, {y1})` 决定了那条直线',
        'for index': lambda S, B, r: ('从第三个点（下标 2）开始，逐个检查它在不在这条直线上' if S.index == 2 else f'下一个点：检查点 {S.index}'),
        'x2 = ': '点 `{index}` 相对点 0 的 x 增量 `x2 = {x2}`',
        'y2 = ': '点 `{index}` 相对点 0 的 y 增量 `y2 = {y2}`',
        'if x1 * y2': lambda S, B, r: (f'叉积判共线：`x1×y2 = {S.x1*S.y2}`，`x2×y1 = {S.x2*S.y1}`，'
                                       + ('==不相等 → 点 ' + str(S.index) + ' 不在直线上，立刻返回 False==' if S.x1*S.y2 != S.x2*S.y1 else '==相等 → 共线，继续下一个点==')),
        'return False': '有一个点偏离直线，整体不可能共线 → `False`',
        'return True': '所有点都在直线上 → `True`',
    },
    cards=dict(
        one_liner='用叉积判共线：两个向量叉积为 0 就在同一条直线上',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定若干点 `coordinates[i] = [x, y]`，判断它们是否都在同一条直线上',
                 '示例：`[[1,2],[2,3],[3,4],[4,5],[5,6],[6,7]]` → `True`',
                 '本视频：`[[0,0],[2,1],[4,2],[6,3],[8,5]]` → `False`'],
        quote='判断共线是经典的计算几何问题，一般是利用叉积来进行判断。',
        quote_src='—— yiduobo 题解原文',
        idea=['点 0、点 1 确定一条直线，方向向量 `(x1, y1)`',
              '第三个点起，每个点相对点 0 的向量 `(x2, y2)`',
              '共线 ⇔ 叉积 `x1*y2 - x2*y1 = 0`，用乘法比较，不用除法（斜率）'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '交叉相乘避免除以 0（竖直线 `x1 = 0` 也能正确判断）',
                 '只需要从下标 2 开始检查；两个点永远共线',
                 '同类题：2280 折线图最少线段数，也是用叉积比较相邻向量'],
    ),
)
