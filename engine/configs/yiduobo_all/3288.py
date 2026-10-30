C0 = [[3, 1], [2, 2], [0, 0], [5, 3], [1, 1], [5, 4], [6, 5], [4, 4]]
K0 = 1
KP = C0[K0]


def _status(p):
    x, y = p
    if (x, y) == tuple(KP):
        return 'k'
    if (x < KP[0] and y < KP[1]) or (x > KP[0] and y > KP[1]):
        return 'cand'
    return 'out'


def _cur(S):
    ln = S.get('_line', 0)
    if S.get('x') is not None and S.get('y') is not None and (6 <= ln <= 10 or 18 <= ln <= 30):
        return (S['x'], S['y'])
    return None


def _inpts(S):
    return 'points' in S and 12 <= S.get('_line', 0) <= 32


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pts = [tuple(p) for p in (S['points'] if _inpts(S) else S['coordinates'])]
    cur = _cur(S)
    cv.text((x0 + 18, y0 + 4), '平面上的点（黄 = coordinates[k]，绿 = left，蓝 = right，灰 = 排除）', 22, T['muted'], bold=True)
    cw, ch = 62, 36
    gx0, gy0 = x0 + 70, y0 + 50
    W, H = 7 * cw, 6 * ch
    cv.rect((gx0, gy0 + H - KP[1] * ch, gx0 + KP[0] * cw, gy0 + H), fill=T['green'], alpha=40)
    cv.rect((gx0 + (KP[0] + 1) * cw, gy0, gx0 + W, gy0 + H - (KP[1] + 1) * ch), fill=T['blue'], alpha=40)
    cv.line([(gx0, gy0 + H), (gx0 + W, gy0 + H)], T['border'], 2)
    cv.line([(gx0, gy0), (gx0, gy0 + H)], T['border'], 2)
    for i in range(7):
        cv.text((gx0 + i * cw + cw / 2, gy0 + H + 6), i, 18, T['dim'], anchor='mt', mono=True)
    for j in range(6):
        cv.text((gx0 - 8, gy0 + H - j * ch - ch / 2), j, 18, T['dim'], anchor='rm', mono=True)
    cv.text((gx0 + W + 10, gy0 + H), 'x', 20, T['dim'], anchor='lb')
    cv.text((gx0, gy0 - 22), 'y', 20, T['dim'], anchor='lb')
    order = {p: i for i, p in enumerate(pts)}
    done = set()
    if _inpts(S):
        if cur is not None and cur in order:
            done = set(pts[:order[cur]])
        elif S.get('_line', 0) in (30, 32):
            done = set(pts)
    for p in [tuple(q) for q in S['coordinates']]:
        px, py = p
        cx, cy = gx0 + px * cw + cw / 2, gy0 + H - py * ch - ch / 2
        st = _status(p)
        fill = T['yellow'] if st == 'k' else (T['green'] if st == 'cand' and p[0] < KP[0] else (T['blue'] if st == 'cand' else (70, 76, 86)))
        if p == cur:
            fill = T['pink']
        cv.rect((cx - 17, cy - 17, cx + 17, cy + 17), fill=fill, r=17, outline=T['text'] if p in done else None, width=3)
    # 排序后的序列
    ys = y0 + 50 + H + 56
    cv.text((x0 + 18, ys - 30), ('points（排序后：x 升序，x 相同 y 降序）' if _inpts(S) else 'coordinates（原顺序，一趟遍历分成 left / right）'), 22, T['muted'], bold=True)
    n = max(1, len(pts))
    cell = min(112, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    for i, p in enumerate(pts):
        X = sx + i * cell
        st = _status(p)
        fill = T['yellow'] if st == 'k' else (T['panel2'] if st == 'cand' else (46, 52, 62))
        cv.rect((X + 3, ys, X + cell - 3, ys + 60), fill=fill, r=8, outline=T['pink'] if p == cur else T['border'], width=5 if p == cur else 1)
        col = T['bg'] if st == 'k' else (T['text'] if st == 'cand' else T['dim'])
        cv.text((X + cell / 2, ys + 30), f'({p[0]},{p[1]})', 22, col, anchor='mm', bold=True, mono=True)


CONFIG = dict(
    num=3288, title='最长上升路径的长度', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='以 k 为界拆成两半 · 各做二维 LIS',
    tags=['灵神题单·动态规划', '难度分 2450'],
    code='''
class Solution(object):
    def maxPathLength(self, coordinates, k):

        left = []
        right = []
        for x, y in coordinates:
            if x < coordinates[k][0] and y < coordinates[k][1]:
                left.append([x, y])
            elif x > coordinates[k][0] and y > coordinates[k][1]:
                right.append([x, y])

        def calc(points):
            if not points:
                return 0

            points.sort(key=lambda d:(d[0], -d[1]))
            f = [points[0][1]]
            for x, y in points[1:]:
                if y > f[-1]:
                    f.append(y)
                else:
                    lo = 0
                    hi = len(f) - 1
                    while lo < hi:
                        mid = (lo + hi) // 2
                        if y > f[mid]:
                            lo = mid + 1
                        else:
                            hi = mid
                    f[lo] = y

            return len(f)

        return calc(left) + 1 + calc(right)
''',
    call=f'Solution().maxPathLength({C0!r}, {K0})',
    expect=5,
    max_steps=80,
    skip=['left = []', 'right = []'],
    views=[
        dict(type='custom', draw=_draw, h=440),
        dict(type='array', var='f', label='f：长度 i+1 的上升序列的最小结尾 y', h=180, cell=90,
             pointers={'lo if 22 <= _line <= 30 else None': 'blue', 'hi if 23 <= _line <= 29 else None': 'pink',
                       'mid if 25 <= _line <= 29 else None': 'yellow'},
             color=lambda S, i, v: 'yellow' if S.get('lo') is not None and i == S['lo'] and S.get('_line') == 30 else None),
    ],
    watch=[('len(left)', 'len(left)', 'green'), ('len(right)', 'len(right)', 'blue'), ('(x,y)', '(x, y)', 'pink'), ('lo', 'lo', 'blue'), ('hi', 'hi', 'pink')],
    captions={
        'for x, y in coordinates': lambda S, B, r: (f'一趟遍历：看点 `({S.x}, {S.y})`，和 `coordinates[k] = ({S.coordinates[S.k][0]}, {S.coordinates[S.k][1]})` 比' if S.get('x') != B.get('x') or S.get('y') != B.get('y') else '遍历结束：left、right 分好了'),
        'if x < coordinates[k][0]': lambda S, B, r: (f'`x = {S.x} < {S.coordinates[S.k][0]}` 且 `y = {S.y} < {S.coordinates[S.k][1]}` → 在左下，==进 left==' if S.x < S.coordinates[S.k][0] and S.y < S.coordinates[S.k][1]
                                                   else f'`({S.x}, {S.y})` 不在左下，看是不是右上'),
        'left.append': '`left` 加入 `({x}, {y})` → 共 {len(left)} 个',
        'elif x > coordinates[k][0]': lambda S, B, r: (f'`x = {S.x} > {S.coordinates[S.k][0]}` 且 `y = {S.y} > {S.coordinates[S.k][1]}` → 在右上，==进 right==' if S.x > S.coordinates[S.k][0] and S.y > S.coordinates[S.k][1]
                                                     else f'`({S.x}, {S.y})` 左右都不沾边（或就是 k 本身）→ ==舍弃=='),
        'right.append': '`right` 加入 `({x}, {y})` → 共 {len(right)} 个',
        'if not points': lambda S, B, r: ('`points` 为空，没有点可选' if not S.points else f'`points` 有 {len(S.points)} 个点，开始算二维 LIS'),
        'return 0': '空集合，长度 0',
        'points.sort': '`x` 升序排好后，二维问题变成 y 序列的 LIS；`x` 相同时 `y` ==降序==，避免同 x 的两点被连起来',
        'f = [points[0][1]]': '先放第一个点的 `y = {points[0][1]}`',
        'for x, y in points[1:]': lambda S, B, r: (f'下一个点 `({S.x}, {S.y})`' if S.get('x') != B.get('x') or S.get('y') != B.get('y') else '这一批点处理完了'),
        'if y > f[-1]': lambda S, B, r: (f'`y = {S.y} > f[-1] = {S.f[-1]}` → 能接在最长序列后面，==直接追加==' if S.y > S.f[-1]
                                         else f'`y = {S.y} ≤ f[-1] = {S.f[-1]}` → 接不上末尾，二分找第一个 `≥ y` 的位置'),
        'f.append(y)': '`f` 追加 `{y}` → {f}',
        'lo = 0': '二分区间 `[lo, hi]`',
        'hi = len(f) - 1': '`hi = {hi}`',
        'while lo < hi': lambda S, B, r: (f'`lo = {S.lo} < hi = {S.hi}`，继续' if S.lo < S.hi else f'`lo = hi = {S.lo}`：找到了位置'),
        'mid = (lo + hi) // 2': '`mid = ({lo} + {hi}) // 2 = {mid}`',
        'if y > f[mid]': lambda S, B, r: (f'`y = {S.y} > f[{S.mid}] = {S.f[S.mid]}` → 还要往右' if S.y > S.f[S.mid]
                                          else f'`y = {S.y} ≤ f[{S.mid}] = {S.f[S.mid]}` → 往左收缩'),
        'lo = mid + 1': '`lo` → {lo}',
        'hi = mid': '`hi` → {hi}',
        'f[lo] = y': lambda S, B, r: (f'`f[{S.lo}] = {B.f[S.lo]}` 换成 `{S.y}`：长度不变，结尾更小 → {S.f}' if B.f[S.lo] != S.y
                         else f'`f[{S.lo}]` 本来就是 `{S.y}`，y 相等不算严格上升，覆盖后不变 → {S.f}'),
        'return len(f)': '这一半的最长上升序列长度 = =={ret}==',
        'return calc(left)': '先算 `calc(left)`，加上 k 点自己的 `1`，再算 `calc(right)`',
    },
    cards=dict(
        result='`calc(left) + 1 + calc(right) = 2 + 1 + 2 = 5`',
        one_liner='以 k 点切开：左下一半、右上一半，各求一次 LIS',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['点序列要求 `x`、`y` 都严格递增，且必须包含 `coordinates[k]`',
                 '求这样的最长上升路径的长度',
                 '示例：`[[3,1],[2,2],[4,1],[0,0],[5,3]]`，`k=1` → `3`',
                 '本视频用 8 个点，`k=1` → `5`'],
        quote='以coordinates[k]为界切分这个上升序列，可以得到一个由满足x[i] < x[k]且y[i] < y[k]的点组成的最长上升序列，以及另一个由满足x[i] > x[k]且y[i] > y[k]的点组成的最长上升序列。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历，把左下的点放进 `left`，右上的放进 `right`，其余点直接扔掉',
              '对每一半：先按 `x` 升序排，再对 `y` 求最长上升子序列',
              '`x` 相同时 `y` 降序，同一个 `x` 的点就不会被连成上升序列',
              '答案 = `calc(left) + 1 + calc(right)`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：同 `x` 必须 `y` 降序；两边都要严格大于/小于 k 点',
                 '`calc` 里的二分找第一个 `≥ y` 的位置，对应严格上升',
                 '多维有序问题：先排序固定一维，再处理剩下的维度',
                 '对比灵神：灵神不拆两个列表，直接把两类点混在一起做一次 LIS',
                 '原文需要改动的地方：无，Python 3 直接可运行'],
    ),
)
