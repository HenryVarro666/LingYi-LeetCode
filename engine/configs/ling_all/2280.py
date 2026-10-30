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
    P = [tuple(p) for p in S['stockPrices']]
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
    if 'x1' in S and 'x2' in S:
        return next((i for i in range(len(P) - 1) if P[i][0] == S['x1']), None)
    if 'x1' not in S and 'ans' in S and S.get('_line', 0) and S['_line'] >= 6:
        return len(P) - 1
    return None

CONFIG = dict(
    num=2280, title='表示一个折线图的最少线段数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='排序 + 斜率相乘比较',
    tags=['灵神题单·数学算法', '难度分 1681'],
    code='''
class Solution:
    def minimumLines(self, stockPrices: List[List[int]]) -> int:
        stockPrices.sort(key=lambda x: x[0])  # 按照 day 排序
        ans, pre_dy, pre_dx = 0, 1, 0
        for (x1, y1), (x2, y2) in pairwise(stockPrices):
            dy, dx = y2 - y1, x2 - x1
            if dy * pre_dx != pre_dy * dx:  # 与上一条线段的斜率不同
                ans += 1
                pre_dy, pre_dx = dy, dx
        return ans
''',
    call='Solution().minimumLines([[1,7],[2,6],[3,5],[4,4],[5,4],[6,3],[7,2],[8,1]])',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', fn=lambda S: (f"新线段 `dy={S['dy']}, dx={S['dx']}`；上一条 `pre_dy={S['pre_dy']}, pre_dx={S['pre_dx']}`；"
                                         f"`{S['dy']}×{S['pre_dx']} = {S['dy']*S['pre_dx']}`，`{S['pre_dy']}×{S['dx']} = {S['pre_dy']*S['dx']}`")
             if 'dy' in S else '初始斜率设为 `1/0`（竖直），第一条线段一定算新线段'),
    ],
    watch=[('ans', 'ans', 'green'), 'pre_dy', 'pre_dx', 'dy', 'dx'],
    captions={
        'stockPrices.sort': '先按 `day` 排序：输入可能乱序，相邻点才是折线的相邻顶点',
        'ans, pre_dy, pre_dx': '假设第一天之前的斜率是 `1/0`（竖直）：任何真实线段都与它不同，首段自动计数',
        'dy, dx =': '这一段的增量：`dy = {dy}`，`dx = {dx}`',
        'if dy * pre_dx': lambda S, B, r: (f'交叉相乘比斜率：`{S.dy}×{S.pre_dx} = {S.dy*S.pre_dx}`，`{S.pre_dy}×{S.dx} = {S.pre_dy*S.dx}`，'
                                           + ('==不相等 → 斜率变了，要一条新线段==' if S.dy*S.pre_dx != S.pre_dy*S.dx else '==相等 → 斜率相同，接在上一条线段后面==')
                                           + '。不用除法，避免浮点误差'),
        'ans += 1': '斜率变了，需要新线段：`ans` → {ans}',
        'pre_dy, pre_dx = dy, dx': '把「上一条斜率」更新为这一段：`{pre_dy}/{pre_dx}`',
        'return ans': '所有相邻线段都比完了，最少 `{ans}` 条',
    },
    cards=dict(
        one_liner='按 day 排序，相邻线段斜率变了就多一条线',
        complexity='时间 `O(n log n)`（排序），空间 `O(1)`',
        problem=['`stockPrices[i] = [day, price]`，相邻点连成折线图',
                 '求表示这条折线所需的 ==最少线段数==（共线的点可合并）',
                 '示例：`[[1,7],[2,6],[3,5],[4,4],[5,4],[6,3],[7,2],[8,1]]` → `3`'],
        quote='按照 day 排序后，如果相邻两条线段的斜率不同，那么必然需要一条新的线段。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后只看相邻线段：斜率一样就合并，不一样就 `ans += 1`',
              '假定第一天之前斜率是 `1/0`，省掉「第一条线段」的特判',
              '斜率 `dy/dx` 用交叉相乘 `dy*pre_dx != pre_dy*dx` 比较，==不用除法=='],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '除法算斜率有浮点误差：两个斜率可相差 `10^-18`，会被舍入成同一个数；改乘法全是整数',
                 '==必须先按 day 排序==，输入顺序不保证',
                 '只有一个点时没有线段，循环不执行，答案 `0`'],
    ),
)
