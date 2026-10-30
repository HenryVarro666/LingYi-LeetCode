PTS = [[1, 1], [2, 2], [1, 3], [3, 3], [4, 4]]


def _ks(k):
    if k == float('inf'):
        return '∞'
    return f'{k:g}'


def _cur_j(S):
    """内层循环当前的点在 points 里的下标（点互不相同）"""
    if 'x2' not in S or 'i' not in S:
        return None
    try:
        j = PTS.index([S['x2'], S['y2']])
    except ValueError:
        return None
    return j if j > S['i'] else None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '平面上的点（橙 = 基准点 points[i]，蓝 = 当前点，绿 = 与当前点同斜率的点）', 22, T['muted'], bold=True)
    lo, hi = 0, 5
    size = min(x1 - x0 - 120, y1 - y0 - 70)
    ox = x0 + 60
    oy = y0 + 48 + size

    def P(x, y):
        return ox + (x - lo) / (hi - lo) * size, oy - (y - lo) / (hi - lo) * size

    for t in range(lo, hi + 1):
        X, Y = P(t, t)
        cv.line([(X, oy), (X, oy - size)], T['panel2'], 1)
        cv.line([(ox, Y), (ox + size, Y)], T['panel2'], 1)
        cv.text((X, oy + 6), t, 18, T['dim'], anchor='mt', mono=True)
        if t:
            cv.text((ox - 8, Y), t, 18, T['dim'], anchor='rm', mono=True)
    cv.line([(ox, oy), (ox + size, oy)], T['border'], 2)
    cv.line([(ox, oy), (ox, oy - size)], T['border'], 2)
    i = S.get('i')
    j = _cur_j(S)
    same = set()
    if i is not None and j is not None:
        bx, by = PTS[i]
        cx, cy = PTS[j]
        # 画出整条直线（裁剪到画布内）
        if cx == bx:
            a, b = P(bx, lo), P(bx, hi)
        else:
            k = (cy - by) / (cx - bx)
            a, b = P(lo, by + k * (lo - bx)), P(hi, by + k * (hi - bx))
            if abs(k) > 1:
                a, b = P(bx + (lo - by) / k, lo), P(bx + (hi - by) / k, hi)
        cv.line([a, b], T['blue'], 3)
        for t in range(i + 1, j + 1):
            tx, ty = PTS[t]
            if (ty - by) * (cx - bx) == (cy - by) * (tx - bx):
                same.add(t)
    for t, (px, py) in enumerate(PTS):
        X, Y = P(px, py)
        fill = T['panel2']
        if i is not None and t < i:
            fill = (40, 45, 53)
        if t in same:
            fill = T['green']
        if t == j:
            fill = T['blue']
        if t == i:
            fill = T['orange']
        cv.d.ellipse((X - 20, Y - 20, X + 20, Y + 20), fill=fill, outline=T['border'], width=2)
        cv.text((X, Y), t, 20, T['bg'] if fill not in (T['panel2'], (40, 45, 53)) else T['text'], anchor='mm', bold=True)
        lab = f'({px},{py})'
        lw = cv.tlen(lab, 18, mono=True)
        cv.rect((X - lw / 2 - 4, Y + 23, X + lw / 2 + 4, Y + 45), fill=T['bg'], r=4, alpha=220)
        cv.text((X, Y + 34), lab, 18, T['muted'], anchor='mm', mono=True)
    # 右侧：以基准点为原点的新坐标表
    rx = ox + size + 50
    if i is None:
        return
    bx, by = PTS[i]
    cv.text((rx, y0 + 52), f'以 points[{i}] = ({bx},{by}) 为原点', 24, T['orange'], bold=True)
    for hx, ht in ((0, '点'), (120, '新坐标'), (260, '斜率 k')):
        cv.text((rx + hx, y0 + 90), ht, 20, T['muted'])
    yy = y0 + 124
    if i == len(PTS) - 1:
        cv.text((rx, yy), '（后面没有点了）', 22, T['dim'])
    for t in range(i + 1, len(PTS)):
        tx, ty = PTS[t]
        dx, dy = tx - bx, ty - by
        if j is None or t > j:
            c = T['dim']
            ks = '?'
        else:
            c = T['blue'] if t == j else (T['green'] if t in same else T['text'])
            ks = _ks(dy / dx if dx else float('inf'))
        cv.text((rx, yy), f'{t}:({tx},{ty})', 22, c, mono=True)
        cv.text((rx + 120, yy), f'({dx},{dy})', 22, c, mono=True)
        cv.text((rx + 260, yy), ks, 22, c, mono=True, bold=True)
        yy += 40


def _k_cap(S, B, ret):
    if S.dx:
        return f'斜率 `k = dy / dx = {S.dy} / {S.dx} = {_ks(S.k)}`'
    return '`dx = 0`：==竖直线==，斜率不存在，记为 `inf`（不能做除法）'


CONFIG = dict(
    num=149, title='直线上最多的点数', difficulty='Hard', category='数学',
    author='灵茶山艾府', technique='枚举基准点 + 哈希表统计斜率',
    tags=['面试经典150'],
    code='''
class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        ans = 0
        for i, (x, y) in enumerate(points):  # 假设直线一定经过 points[i]
            cnt = defaultdict(int)
            for x2, y2 in points[i + 1:]:
                dx, dy = x2 - x, y2 - y
                k = dy / dx if dx else inf
                cnt[k] += 1
                ans = max(ans, cnt[k])  # 这里没有算上 (x,y) 这个点，最后再加一
        return ans + 1
''',
    call=f'Solution().maxPoints({PTS})',
    expect=4,
    skip=['for x2, y2 in points'],
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='map', var='cnt', label='cnt：斜率 → 点数（不含基准点）', h=110,
             fmt=lambda k, v: f'k={_ks(k)}: {v}'),
    ],
    watch=[('i', 'i', 'orange'), ('(x2,y2)', lambda S: (S['x2'], S['y2']), 'blue'), 'dx', 'dy',
           ('k', 'k'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans`：过某个基准点、==斜率相同==的最多点数（先不算基准点）',
        'for i, (x, y) in enumerate(points)': lambda S, B, ret: (
            f'假设直线一定经过 `points[{S.i}] = ({S.x},{S.y})`，把它当作==坐标原点=='
            if S.get('i') != B.get('i') else '所有基准点都枚举完了'),
        'cnt = defaultdict(int)': lambda S, B, ret: ('换了基准点，斜率计数 `cnt` 清空；内层只枚举==下标更大==的点'
                                                     if S.i < len(S.points) - 1 else '后面没有下标更大的点了，内层循环不执行'),
        'dx, dy = x2 - x, y2 - y': '当前点 `({x2},{y2})` 的新坐标：`({x2}−{x}, {y2}−{y}) = ({dx}, {dy})`',
        'k = dy / dx if dx else inf': _k_cap,
        'cnt[k] += 1': lambda S, B, ret: (f'斜率 `{_ks(S.k)}` 的点数 +1 → `{S.cnt[S.k]}`'
                                          + ('：这些点和基准点==在同一条直线上==' if S.cnt[S.k] > 1 else '')),
        'ans = max': lambda S, B, ret: (f'`ans = max({B.ans}, {S.cnt[S.k]})` = =={S.ans}==' if S.ans > B.ans
                                        else f'`cnt[k] = {S.cnt[S.k]}` 没超过 `ans = {S.ans}`，不变'),
        'return ans + 1': '最后加上基准点自己：`{B.ans} + 1` = =={ret}==',
    },
    cards=dict(
        one_liner='固定直线经过的一个点，斜率相同的点就在同一条直线上',
        complexity='时间 `O(n²)`，空间 `O(n)`',
        problem=['`points[i] = [x, y]` 是平面上的点（互不相同），求==最多有多少个点在同一条直线上==',
                 '示例：`[[1,1],[2,2],[3,3]]` → `3`',
                 '本视频：`[[1,1],[2,2],[1,3],[3,3],[4,4]]` → `4`'],
        quote='把 points[i] = (x,y) 当作坐标原点（所以直线一定经过坐标原点）……==斜率相同的点，一定在同一条直线上==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['用哈希表统计斜率的出现次数，最大次数 + 1（加上基准点）就是过该点的答案',
              '竖直线 `dx = 0` 的斜率记为 `inf`',
              '内层只枚举 `[i+1, n-1]`：一条直线上下标最小的点做基准时，就能数到整条线'],
        result='过 `points[0] = (1,1)` 的斜率 1 有 3 个点，再加上它自己 → `4` ✓',
        summary=['时间 `O(n²)`：两重循环；空间 `O(n)`：哈希表',
                 '本题坐标范围只有 `2·10^4`，==浮点数斜率不会出错==',
                 '坐标达到约 `6.7·10^7` 时，两个很接近的分数可能被舍入成同一个浮点数',
                 '更稳妥：用约分后的 `(dy, dx)` 二元组作为键'],
    ),
)
