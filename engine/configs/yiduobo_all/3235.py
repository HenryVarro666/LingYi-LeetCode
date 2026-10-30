XC, YC = 3, 3
CIRCLES = [[2, 1, 1], [1, 2, 1]]
_PAL = ['cyan', 'orange', 'purple', 'green', 'pink', 'yellow']
_SIDES = ['左边', '上边', '右边', '下边']


def _root(fa, x):
    while fa[x] != x:
        x = fa[x]
    return x


def _draw(cv, S, B, box, T):
    from PIL import Image, ImageDraw
    x0, y0, x1, y1 = box
    X, Y, cs, fa = S.get('xCorner'), S.get('yCorner'), S.get('circles'), S.get('fa')
    if X is None or fa is None or not isinstance(fa, list):
        return
    n = len(cs)
    cv.text((x0 + 18, y0 + 4), '同色 = 同一连通块；黄 = 当前判断的圆 / 边', 22, T['muted'], bold=True)
    lo_x = min([0] + [c[0] - c[2] for c in cs]) - 0.3
    hi_x = max([X] + [c[0] + c[2] for c in cs]) + 0.3
    lo_y = min([0] + [c[1] - c[2] for c in cs]) - 0.3
    hi_y = max([Y] + [c[1] + c[2] for c in cs]) + 0.3
    aw, ah = x1 - x0 - 60, y1 - y0 - 80
    sc = min(aw / (hi_x - lo_x), ah / (hi_y - lo_y))
    ox = x0 + 30 + (aw - sc * (hi_x - lo_x)) / 2
    oy = y0 + 56 + (ah - sc * (hi_y - lo_y)) / 2

    def P(x, y):
        return ox + (x - lo_x) * sc, oy + (hi_y - y) * sc

    roots = [_root(fa, k) for k in range(n + 4)]
    cmap = {}
    for r in sorted(set(roots)):
        if roots.count(r) > 1:
            cmap[r] = _PAL[len(cmap) % len(_PAL)]
    ci = S.get('i') if isinstance(S.get('i'), int) and 0 <= S.get('i', -1) < n else None
    cj = S.get('j') if isinstance(S.get('j'), int) and 0 <= S.get('j', -1) < n else None
    cp = S.get('p') if isinstance(S.get('p'), int) and 0 <= S.get('p', -1) < 4 else None
    ln = S.get('_line', 0)
    # 圆
    for k, (cx, cy, r) in enumerate(cs):
        px, py = P(cx, cy)
        R = r * sc
        col, a = (T[cmap[roots[k]]], 100) if roots[k] in cmap else (T['blue'], 60)
        lay = Image.new('RGBA', (int(2 * R) + 8, int(2 * R) + 8), (0, 0, 0, 0))
        ring = T['yellow'] if (k == ci or (k == cj and ln in (53, 54))) else col
        ImageDraw.Draw(lay).ellipse((3, 3, 2 * R + 4, 2 * R + 4), fill=tuple(col) + (a,), outline=tuple(ring) + (255,), width=6 if ring is not col else 4)
        cv.im.alpha_composite(lay, (int(px - R - 4), int(py - R - 4)))
        cv.text((px, py), f'{k}', 28, T['text'], anchor='mm', bold=True)
        cv.text((px, py + 28), f'({cx},{cy}) r={r}', 17, T['muted'], anchor='mm', mono=True)
    # 四条边：节点 n..n+3 = 左 上 右 下
    pts = [P(0, 0), P(0, Y), P(X, Y), P(X, 0)]
    for q in range(4):
        a_, b_ = pts[q], pts[(q + 1) % 4]
        rt = roots[n + q]
        col = T[cmap[rt]] if rt in cmap else T['dim']
        cv.line([a_, b_], col, 9 if q == cp else 6)
        mx, my = (a_[0] + b_[0]) / 2, (a_[1] + b_[1]) / 2
        dx = {0: -10, 1: 0, 2: 10, 3: 0}[q]
        dy = {0: 0, 1: -8, 2: 0, 3: 8}[q]
        cv.text((mx + dx, my + dy), f'{_SIDES[q]} #{n + q}', 20, T['yellow'] if q == cp else col,
                anchor={0: 'rm', 1: 'mb', 2: 'lm', 3: 'mt'}[q], bold=True)
    for p_ in (pts[0], pts[2]):
        cv.d.ellipse((p_[0] - 8, p_[1] - 8, p_[0] + 8, p_[1] + 8), fill=T['red'])
    # 两圆相交点 A
    if ci is not None and cj is not None and ln in (53, 54):
        a1, b1, r1 = cs[ci]
        a2, b2, r2 = cs[cj]
        if (a1 - a2) ** 2 + (b1 - b2) ** 2 <= (r1 + r2) ** 2:
            ax, ay = (a1 * r2 + a2 * r1) / (r1 + r2), (b1 * r2 + b2 * r1) / (r1 + r2)
            cv.line([P(a1, b1), P(a2, b2)], T['pink'], 3)
            pa = P(ax, ay)
            cv.d.ellipse((pa[0] - 9, pa[1] - 9, pa[0] + 9, pa[1] + 9), fill=T['yellow'], outline=T['bg'], width=2)
            cv.text((pa[0], pa[1] - 16), f'A({ax:g},{ay:g})', 22, T['yellow'], anchor='mb', bold=True)


def _in(c, p):
    return (c[0] - p[0]) ** 2 + (c[1] - p[1]) ** 2 <= c[2] ** 2


def _touch(c, p1, p2):
    if _in(c, p1) or _in(c, p2):
        return True
    same = 0 if p1[0] == p2[0] else 1
    other = 1 - same
    if p1[same] < c[same] - c[2] or p1[same] > c[same] + c[2]:
        return False
    if max(p1[other], p2[other]) < c[other] or min(p1[other], p2[other]) > c[other]:
        return False
    return True


def _inrec(c1, c2, X, Y):
    return c1[0] * c2[2] + c2[0] * c1[2] < X * (c1[2] + c2[2]) and c1[1] * c2[2] + c2[1] * c1[2] < Y * (c1[2] + c2[2])


def _cc(c1, c2):
    return (c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 <= (c1[2] + c2[2]) ** 2


def _edge(S, B, r):
    i, p, X, Y = S.i, S.p, S.xCorner, S.yCorner
    pts = [(0, 0), (0, Y), (X, Y), (X, 0)]
    c = S.circles[i]
    t = _touch(c, pts[p], pts[(p + 1) % 4])
    nm = ['左边', '上边', '右边', '下边'][p]
    return (f'圆 `{i}` 与矩形{nm}（节点 `{S.n + p}`）相交 / 包含吗？端点在圆内，或圆心到边的垂线 ≤ 半径且垂足落在边上 → '
            + ('==相交==，下一步合并' if t else '不相交'))


def _pair(S, B, r):
    c1, c2 = S.circles[S.i], S.circles[S.j]
    if not _cc(c1, c2):
        return f'圆 `{S.i}` 与圆 `{S.j}`：圆心距² `{(c1[0]-c2[0])**2 + (c1[1]-c2[1])**2}` > 半径和² `{(c1[2]+c2[2])**2}` → 不相交'
    ok = _inrec(c1, c2, S.xCorner, S.yCorner)
    ax = (c1[0] * c2[2] + c2[0] * c1[2]) / (c1[2] + c2[2])
    ay = (c1[1] * c2[2] + c2[1] * c1[2]) / (c1[2] + c2[2])
    return (f'圆 `{S.i}`、`{S.j}` 相交；按半径比切分圆心连线，点 A = `({ax:g}, {ay:g})`，'
            + ('在矩形内 → ==这座桥有效，合并==' if ok else '在矩形外 → 不算阻断，不合并'))


def _final(S, B, r):
    n = S.n
    pairs = {55: (0, 2, '左边', '右边'), 57: (1, 3, '上边', '下边'), 59: (0, 3, '左边', '下边'), 61: (1, 2, '上边', '右边')}
    a, b, na, nb = pairs[S['_line']]
    fa = S.fa

    def rt(x):
        while fa[x] != x:
            x = fa[x]
        return x
    same = rt(n + a) == rt(n + b)
    return f'{na} 与 {nb} 在同一个连通块吗？' + ('==是 → 有一堵墙把它们连起来，不可达 → 返回 False==' if same else '不在 → 这一组没被阻断')


CONFIG = dict(
    num=3235, title='判断矩形的两个角落是否可达', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='并查集 · 圆与矩形四边连通',
    tags=['七、并查集', '§7.2 进阶', '数学算法', '五、计算几何', '§5.2 圆'],
    code='''
class Solution(object):
    def canReachCorner(self, xCorner, yCorner, circles):
        def find(fa, x):
            if fa[x] != x:
                fa[x] = find(fa, fa[x])
            return fa[x]
        def union(fa, x, y):
            fa_x = find(fa, x)
            fa_y = find(fa, y)
            if fa_x != fa_y:
                fa[fa_x] = fa_y
        def dis(p1, p2):
            return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
        def in_circle(circle, p):
            return dis((circle[0], circle[1]), p) <= circle[2] ** 2
        def rec_cross(circle, p1, p2):
            in1 = in_circle(circle, p1)
            in2 = in_circle(circle, p2)
            
            if in1 or in2:
                return True
            
            if p1[0] == p2[0]:
                same = 0
            else:
                same = 1
            
            other = 1 - same
            
            if p1[same] < circle[same] - circle[2] or p1[same] > circle[same] + circle[2]:
                return False
            
            if max(p1[other], p2[other]) < circle[other] or min(p1[other], p2[other]) > circle[other]:
                return False
            return True
        def circle_cross(circle1, circle2):
            return dis((circle1[0], circle1[1]), (circle2[0], circle2[1])) <= (circle1[2] + circle2[2]) ** 2
        def cross_in_rec(circle1, circle2, xCorner, yCorner):
            if circle1[0] * circle2[2] + circle2[0] * circle1[2] >= xCorner * (circle1[2] + circle2[2]):
                return False
            if circle1[1] * circle2[2] + circle2[1] * circle1[2] >= yCorner * (circle1[2] + circle2[2]):
                return False
            return True
        n = len(circles)
        fa = [index for index in range(n + 4)]
        rec_points = [(0, 0), (0, yCorner), (xCorner, yCorner), (xCorner, 0)]
        for i in range(n):
            for p in range(4):
                if rec_cross(circles[i], rec_points[p], rec_points[(p + 1) % 4]):
                    union(fa, i, n + p)
            
            for j in range(i + 1, n):
                if circle_cross(circles[i], circles[j]) and cross_in_rec(circles[i], circles[j], xCorner, yCorner):
                    union(fa, i, j)
        if find(fa, n) == find(fa, n + 2):
            return False
        if find(fa, n + 1) == find(fa, n + 3):
            return False
        if find(fa, n) == find(fa, n + 3):
            return False
        if find(fa, n + 1) == find(fa, n + 2):
            return False
        
        return True
''',
    call=f'Solution().canReachCorner({XC}, {YC}, {CIRCLES})',
    expect=False,
    views=[
        dict(type='custom', draw=_draw, h=500),
        dict(type='array', var='fa', label='fa：0..n-1 是圆，n = 左边，n+1 = 上边，n+2 = 右边，n+3 = 下边', cell=80, h=150),
    ],
    watch=[('i', 'i', 'blue'), ('p', 'p', 'cyan'), ('j', 'j', 'pink')],
    skip=[k for k in range(3, 44) if k != 11],
    captions={
        44: '`n` 个圆，再加矩形的 4 条边，共 `n + 4` 个点',
        45: '并查集初始：`0..n-1` 是圆，`n` 左边、`n+1` 上边、`n+2` 右边、`n+3` 下边，各自成一块',
        46: '矩形四个顶点，依次连成 左 / 上 / 右 / 下 四条边',
        47: '枚举圆 `i`：先看它与哪几条矩形边相交，再看它与后面哪些圆相交',
        49: _edge,
        50: '圆 `{i}` 碰到这条边 → 合并圆 `{i}` 与边节点 `{n + p}`',
        11: '合并：`fa[{fa_x}] = {fa_y}`，两块变成一块',
        52: '再依次看它与编号更大的圆（两圆只需判断一次）',
        48: '依次看矩形的四条边：左 / 上 / 右 / 下（`p = 0..3`）',
        53: _pair,
        54: '桥有效：合并圆 `{i}` 与圆 `{j}`',
        55: _final, 57: _final, 59: _final, 61: _final,
        56: '左边和右边连通，路被竖直堵死 → `False`',
        58: '上边和下边连通，路被横向堵死 → `False`',
        60: '左边和下边连通，起点被围在左下角 → `False`',
        62: '上边和右边连通，终点被围在右上角 → `False`',
        63: '四组都没连通：没有任何一堵墙 → 路径存在，返回 `True`',
    },
    cards=dict(
        one_liner='圆和矩形四边当成点，用并查集看哪些边被圆「连通」了',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['矩形左下角在原点，右上角 `(xCorner, yCorner)`，平面里有若干圆',
                 '要找一条 `(0,0)` 到右上角的路径：只在起终点碰矩形边界，不碰 / 不进任何圆',
                 '本视频：`X = Y = 3`，`circles = [[2,1,1],[1,2,1]]` → `False`'],
        quote='直接找出这样的路径是非常困难的，从样例一就可以发现，可行路径可以是歪歪扭扭的，因此在这里就应该反过来思考，判断可行路径是否被完全阻断了。',
        quote_src='—— yiduobo 题解原文',
        idea=['堵死的四种情形：上下连通、左右连通、左下连通（围住起点）、上右连通（围住终点）',
              '把矩形四条边和所有圆都当成并查集里的点；圆碰边、圆碰圆就合并',
              '圆与边相交：端点在圆内，或圆心到边所在直线的垂线 ≤ 半径且垂足在边上',
              '两圆相交还要看交点是否在矩形内：用半径比切分圆心连线，得到点 A'],
        summary=['时间 `O(n^2)`，两两枚举圆；空间 `O(n)`',
                 '圆与圆「相交」只判断圆心距² ≤ 半径和²，不开方',
                 '易错：两圆交在矩形外不算阻断，要用 `x1*r2 + x2*r1 < X*(r1+r2)` 检验点 A',
                 '四组检验缺一不可：左右、上下、左下、上右',
                 '视频里 `rec_cross` 等辅助函数的内部细节被折叠，只演示每一步判断的结论',
                 '对比灵神：灵神 DFS 从上 / 左出发找右 / 下；这里用并查集一次检验四组'],
    ),
)
