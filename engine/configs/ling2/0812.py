_CODE = '''
def det(x1: int, y1: int, x2: int, y2: int) -> int:
    return x1 * y2 - y1 * x2

def convex_hull(points: List[List[int]]) -> List[List[int]]:
    points.sort()

    # 计算下凸包（从左到右）
    q = []
    for p in points:
        while len(q) > 1 and det(q[-1][0] - q[-2][0], q[-1][1] - q[-2][1], p[0] - q[-1][0], p[1] - q[-1][1]) <= 0:
            q.pop()
        q.append(p)

    # 计算上凸包（从右到左）
    down_size = len(q)
    # 注意下凸包的最后一个点，是上凸包的右边第一个点，所以从 n-2 开始遍历
    for i in range(len(points) - 2, -1, -1):
        p = points[i]
        while len(q) > down_size and det(q[-1][0] - q[-2][0], q[-1][1] - q[-2][1], p[0] - q[-1][0], p[1] - q[-1][1]) <= 0:
            q.pop()
        q.append(p)

    # 此时首尾是同一个点 points[0]，需要去掉
    q.pop()
    return q

class Solution:
    def largestTriangleArea(self, points: List[List[int]]) -> float:
        ch = convex_hull(points)

        def area(i: int, j: int, k: int) -> int:
            return det(ch[j][0] - ch[i][0], ch[j][1] - ch[i][1], ch[k][0] - ch[i][0], ch[k][1] - ch[i][1])

        m = len(ch)
        ans = 0
        # 固定三角形的其中一个顶点 ch[i]
        for i in range(m):
            # 同向双指针
            k = i + 2
            for j in range(i + 1, m - 1):
                while k + 1 < m and area(i, j, k) < area(i, j, k + 1):
                    k += 1
                # 循环结束后，ch[k] 距离 ch[i]ch[j] 最远
                ans = max(ans, area(i, j, k))  # 注意这里没有除以 2
        return ans / 2
'''
_LINES = _CODE.strip('\n').split('\n')


def _src(S):
    return _LINES[S['_line'] - 1].strip() if 0 < S['_line'] <= len(_LINES) else ''


def _det(a, b, c):
    """cross of (b-a) x (c-b) for hull turn test"""
    return (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])


def _area(ch, i, j, k):
    return (ch[j][0] - ch[i][0]) * (ch[k][1] - ch[i][1]) - (ch[j][1] - ch[i][1]) * (ch[k][0] - ch[i][0])


def _plane(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pts = S.get('points')
    if not pts:
        return
    src = _src(S)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    lo_x, hi_x, lo_y, hi_y = min(xs), max(xs), min(ys), max(ys)
    sc = min((x1 - x0 - 200) / max(1, hi_x - lo_x), (y1 - y0 - 110) / max(1, hi_y - lo_y))
    ox = x0 + 70 + ((x1 - x0 - 200) - sc * (hi_x - lo_x)) / 2
    oy = y1 - 50

    def P(p):
        return (ox + (p[0] - lo_x) * sc, oy - (p[1] - lo_y) * sc)

    for gx in range(lo_x, hi_x + 1):
        cv.line([P((gx, lo_y)), P((gx, hi_y))], T['panel2'], 1)
        cv.text((P((gx, lo_y))[0], oy + 10), gx, 18, T['dim'], anchor='mt', mono=True)
    for gy in range(lo_y, hi_y + 1):
        cv.line([P((lo_x, gy)), P((hi_x, gy))], T['panel2'], 1)
        cv.text((ox - 14, P((lo_x, gy))[1]), gy, 18, T['dim'], anchor='rm', mono=True)
    ch = S.get('ch')
    if ch is not None:
        cv.text((x0 + 18, y0 + 4), '凸包 ch（绿）· 当前三角形 ch[i] ch[j] ch[k]（蓝），虚线 = 候选 k+1', 22, T['muted'], bold=True)
        m = len(ch)
        cv.line([P(ch[t]) for t in range(m)] + [P(ch[0])], T['green'], 3)
        if src.startswith('return ans'):
            best = max(((a, b, c) for a in range(m) for b in range(a + 1, m) for c in range(b + 1, m)),
                       key=lambda t: abs(_area(ch, *t)))
            tri = [P(ch[t]) for t in best]
            cv.poly(tri, T['green'] + (90,))
            cx = sum(p[0] for p in tri) / 3
            cy = sum(p[1] for p in tri) / 3
            cv.text((cx, cy), f'面积 {abs(_area(ch, *best)) / 2}', 30, T['text'], anchor='mm', bold=True)
        elif all(isinstance(S.get(v), int) for v in 'ijk') and S['k'] < m and S['j'] < m:
            i, j, k = S['i'], S['j'], S['k']
            tri = [P(ch[i]), P(ch[j]), P(ch[k])]
            cv.poly(tri, T['blue'] + (70,))
            cv.line(tri + [tri[0]], T['blue'], 3)
            if src.startswith('while k + 1') and k + 1 < m:
                c2 = P(ch[k + 1])
                cv.dashed(P(ch[j]), c2, T['orange'], 3)
                cv.dashed(P(ch[i]), c2, T['orange'], 3)
        for t, p in enumerate(ch):
            X, Y = P(p)
            name = ''.join(v for v in 'ijk' if isinstance(S.get(v), int) and S.get(v) == t and not src.startswith('return ans'))
            cv.text((X + 14, Y - 14), f'ch[{t}]' + (f' {name}' if name else ''), 22, T['yellow'] if name else T['green'], anchor='lb', bold=True)
    else:
        cv.text((x0 + 18, y0 + 4), 'Andrew 单调链：q（绿）保持左转，黄 = 当前点 p，橙虚线 = 待检查的拐弯', 22, T['muted'], bold=True)
        q = S.get('q') or []
        if len(q) >= 2:
            cv.line([P(p) for p in q], T['green'], 4)
        p = S.get('p')
        if p is not None and q and src.startswith('while') and len(q) >= 2:
            cv.dashed(P(q[-1]), P(p), T['orange'], 3)
    for p in pts:
        X, Y = P(p)
        inq = ch is None and p in (S.get('q') or [])
        onhull = ch is not None and p in ch
        cur = ch is None and S.get('p') == p
        c = T['yellow'] if cur else T['green'] if (inq or onhull) else T['muted']
        cv.rect((X - 11, Y - 11, X + 11, Y + 11), fill=c, r=11)
        cv.text((X + 14, Y + 6), f'({p[0]},{p[1]})', 20, T['text'] if (inq or onhull or cur) else T['muted'], anchor='lt', mono=True)


def _hull_w(lim_name):
    def f(S, B, ret):
        q, p = B.q, B.p
        lim = 1 if lim_name == '1' else B.down_size
        if len(q) <= lim:
            return (f'`q` 只有 {len(q)} 个点，不用检查' if lim_name == '1'
                    else '上凸包部分还没有点，不用检查') + f' → 直接加入 `{p}`'
        d = _det(q[-2], q[-1], p)
        if d <= 0:
            return f'`{q[-2]}→{q[-1]}→{p}` 叉积 `{d} ≤ 0`：==右拐或共线== → `{q[-1]}` 不在凸包上，弹出'
        return f'`{q[-2]}→{q[-1]}→{p}` 叉积 `{d} > 0`：==左转==，保留'
    return f


def _cal_w(S, B, ret):
    i, j, k, m, ch = B.i, B.j, B.k, B.m, B.ch
    if k + 1 >= m:
        return f'`k + 1 = {k + 1}` 越界 → 停下，`ch[{k}]` 就是最远点'
    a, b = _area(ch, i, j, k), _area(ch, i, j, k + 1)
    if a < b:
        return f'`area(i,j,k) = {a} < area(i,j,k+1) = {b}`：`ch[{k + 1}]` 离边 `ch[{i}]ch[{j}]` 更远 → `k` 右移'
    return f'`area(i,j,k) = {a} ≥ area(i,j,k+1) = {b}`：面积不再变大 → `ch[{k}]` 最远，停'


def _ans(S, B, ret):
    a = _area(B.ch, B.i, B.j, B.k)
    return f'`area({B.i},{B.j},{B.k}) = {a}`（平行四边形面积）：`ans = max({B.ans}, {a}) = {max(B.ans, a)}`'


def _info(S):
    q = S.get('q')
    if S.get('ch') is not None:
        return f"凸包 `ch = {S['ch']}`，`m = {len(S['ch'])}`"
    if q is None:
        return '先把点按 `(x, y)` 排序，再求凸包'
    part = '上凸包（从右到左）' if 'down_size' in S else '下凸包（从左到右）'
    return f'{part}：`q = {q}`'


CONFIG = dict(
    num=812, title='最大三角形面积', difficulty='Easy', category='数学',
    author='灵茶山艾府', technique='凸包 + 旋转卡壳（同向双指针）',
    tags=['字节3个月', '字节6个月'],
    code=_CODE,
    call='Solution().largestTriangleArea([[0,0],[3,0],[4,2],[1,3],[1,1]])',
    expect=5.0,
    skip=['return x1 * y2 - y1 * x2', 'return det(ch[j][0]'],
    max_steps=75,
    views=[
        dict(type='custom', draw=_plane, h=560),
        dict(type='text', fn=_info, size=26, h=60),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('k', 'k', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'points.sort()': '按 `(x, y)` 排序：Andrew 算法先从左到右求==下凸包==',
        'q = []': '`q` 当作栈，存当前凸包上的点',
        'for p in points': lambda S, B, r: f'下一个点 `p = {S.p}`' if 'p' in S else '下凸包扫描完',
        'while len(q) > 1': _hull_w('1'),
        'while len(q) > down_size': _hull_w('d'),
        11: lambda S, B, r: f'弹出 `{B.q[-1]}`',
        20: lambda S, B, r: f'弹出 `{B.q[-1]}`',
        24: lambda S, B, r: f'首尾都是 `points[0] = {B.q[-1]}`，弹出重复的那个',
        'q.append(p)': '`{p}` 入栈：`q = {q}`',
        'down_size = len(q)': '下凸包有 `{down_size}` 个点，上凸包的弹栈不能动它们',
        'for i in range(len(points) - 2': lambda S, B, r: f'从右往左求==上凸包==：`i = {S.i}`',
        'p = points[i]': '`p = points[{i}] = {p}`',
        'ch = convex_hull': '面积最大的三角形，==三个顶点都在凸包上== → 先求凸包',
        'm = len(ch)': '凸包有 `m = {m}` 个顶点',
        'ans = 0': '`ans` 记录最大的==两倍面积==（叉积）',
        'for i in range(m)': lambda S, B, r: f'固定顶点 `ch[{S.i}] = {S.ch[S.i]}`',
        'k = i + 2': '同向双指针：`k` 从 `i + 2 = {k}` 开始，只增不减',
        'for j in range(i + 1': lambda S, B, r: f'第二个顶点 `ch[{S.j}] = {S.ch[S.j]}`',
        'while k + 1 < m': _cal_w,
        'k += 1': '`k` → {k}',
        'ans = max(ans': _ans,
        'return ans / 2': '叉积是平行四边形面积，==最后才除以 2==：`{ans} / 2 = {ans / 2}`',
        'return q': '凸包顶点（逆时针）：`{q}`',
    },
    cards=dict(
        one_liner='最大三角形的三个顶点都在凸包上：凸包 + 旋转卡壳',
        complexity='时间 `O(n log n)`（排序），空间 `O(n)`',
        problem=['给 `n` 个平面点，从中任取三个点组成三角形，返回最大面积（误差 `10⁻⁵` 内算对）',
                 '示例：`[[0,0],[0,1],[1,0],[0,2],[2,0]]` → `2.0`',
                 '本视频：`[[0,0],[3,0],[4,2],[1,3],[1,1]]` → `5.0`'],
        quote='三角形的高越长越好，所以第三个顶点相比在凸包内部，在凸包上更好（更远）。所以==面积最大的三角形，三个顶点都在凸包上==。',
        quote_src='—— 灵茶山艾府题解「方法二」',
        idea=['面积 = 叉积绝对值的一半：`|x1·y2 − y1·x2| / 2`，全程用整数，最后再除以 2',
              '求凸包（Andrew 单调链），枚举顶点 `i`',
              '`j` 增大时，离 `ch[i]ch[j]` 最远的 `k` 也增大 → ==同向双指针=='],
        result='最大三角形面积 `10 / 2 = 5.0`',
        summary=['时间 `O(n log n)`：排序 + 凸包 `O(n)` + 旋转卡壳 `O(m²)`；空间 `O(n)`',
                 '易错：叉积 `≤ 0` 才弹出（共线点也去掉）；上凸包弹栈不能低于 `down_size`',
                 '首尾都是 `points[0]`，最后要 `q.pop()` 去重',
                 '方法一：`combinations` 暴力枚举三点，`O(n³)`，本题 `n ≤ 50` 也能过',
                 '前置题：587. 安装栅栏'],
    ),
)
