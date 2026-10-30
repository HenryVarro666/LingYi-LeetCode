PTS = [[1, 5], [1, 3], [2, 4], [3, 2], [4, 6], [5, 1]]


def _ij(S):
    """(i, j)：j 用当前 y2 在 i 之后找（示例里 y 互不相同）"""
    pts = S['points']
    if 'y1' not in S or 'i' not in S:
        return None, None
    i = S['i']
    j = None
    if 'y2' in S:
        for k in range(i + 1, len(pts)):
            if pts[k][1] == S['y2']:
                j = k
    return i, j


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pts = S['points']
    cv.text((x0 + 18, y0 + 4), '点按 x 升序、x 相同时 y 降序（蓝=i，粉=j，黄线=max_y）', 22, T['muted'], bold=True)
    gx0, gx1, gy0, gy1 = x0 + 90, x1 - 190, y0 + 110, y1 - 60
    xs = [p[0] for p in PTS]
    ys = [p[1] for p in PTS]
    X = lambda x: gx0 + (x - min(xs)) / (max(xs) - min(xs)) * (gx1 - gx0)
    Y = lambda y: gy1 - (y - min(ys)) / (max(ys) - min(ys)) * (gy1 - gy0)
    cv.line([(gx0 - 30, gy1 + 30), (gx1 + 20, gy1 + 30)], T['border'], 2)
    cv.line([(gx0 - 30, gy1 + 30), (gx0 - 30, gy0 - 20)], T['border'], 2)
    cv.text((gx1 + 20, gy1 + 34), 'x', 20, T['dim'], anchor='rt')
    cv.text((gx0 - 34, gy0 - 20), 'y', 20, T['dim'], anchor='rb')
    i, j = _ij(S)
    line = S.get('_line')
    fresh = line in (5, 6)   # 刚换了新的 i：max_y / j 还是上一轮的
    if fresh:
        j = None
    if i is not None:
        a = pts[i]
        if not fresh and 'max_y' in S and S['max_y'] > -1e9:
            cv.dashed((X(a[0]), Y(S['max_y'])), (gx1, Y(S['max_y'])), T['yellow'], 3)
            cv.text((gx1 + 8, Y(S['max_y'])), f"max_y={S['max_y']}", 20, T['yellow'], anchor='lm', bold=True)
        if j is not None and line in (7, 8, 9):
            b = pts[j]
            ok = a[1] >= b[1] and b[1] > B.get('max_y', S['max_y']) if line == 7 else (line in (8, 9))
            if ok:
                cv.rect((X(a[0]), Y(a[1]), X(b[0]), Y(b[1])), fill=T['green'], alpha=45, outline=T['green'], width=3)
    for k, (px, py) in enumerate(pts):
        c = T['dim']
        if i is not None and k == i:
            c = T['blue']
        elif j is not None and k == j:
            c = T['pink']
        elif i is not None and j is not None and i < k < j:
            c = T['muted']
        cv.rect((X(px) - 14, Y(py) - 14, X(px) + 14, Y(py) + 14), fill=c, r=14)
        cv.text((X(px), Y(py) - 24), f'({px},{py})', 20, T['text'], anchor='mb', mono=True)


CONFIG = dict(
    num=3027, title='人员站位的方案数 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='排序 + 枚举左上角，维护 max_y',
    tags=['枚举右，维护左', 'CDQ 分治 / 值域分治', '难度分 2020'],
    code='''
class Solution:
    def numberOfPairs(self, points: List[List[int]]) -> int:
        points.sort(key=lambda p: (p[0], -p[1]))  # x 升序，y 降序
        ans = 0
        for i, (_, y1) in enumerate(points):
            max_y = -inf
            for (_, y2) in points[i + 1:]:
                if y1 >= y2 > max_y:
                    max_y = y2
                    ans += 1
                if max_y == y1:  # 优化
                    break
        return ans
''',
    call=f'Solution().numberOfPairs({PTS!r})',
    expect=6,
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='array', var='points', label='points（排序后）', cell=120, pointers={'i': 'blue'}),
    ],
    watch=[('i', 'i', 'blue'), ('y1', 'y1', 'blue'), ('y2', 'y2', 'pink'), ('max_y', 'max_y', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'points.sort': '先排序：x 升序，x 相同时 ==y 降序==；这样 `j > i` 时右下角天然满足 x2 ≥ x1',
        'for i, (_, y1)': '枚举左上角 `points[{i}]`，`y1 = {y1}`',
        'max_y = -inf': '`max_y`：i 与 j 之间所有点中 y 的最大值，从 −inf 开始',
        'for (_, y2)': '枚举右下角，`y2 = {y2}`',
        'if y1 >= y2 > max_y': lambda S, B, r: (
            f'`{S.y1} ≥ {S.y2} > {S.max_y}` 成立：不在 i 上方，且比中间所有点都高 → ==矩形内没有别的点==' if S.y1 >= S.y2 > S.max_y
            else (f'`y2 = {S.y2} > y1 = {S.y1}`：右下角跑到左上角上面了，跳过' if S.y2 > S.y1
                  else f'`y2 = {S.y2} ≤ max_y = {S.max_y}`：中间已有点挡在矩形里，不合法')),
        'max_y = y2': '`max_y` 更新为 `{y2}`：后面的 j 必须比它还高才不被挡住',
        'ans += 1': '找到一对合法的 (i, j)，`ans` = =={ans}==',
        'if max_y == y1': lambda S, B, r: ('`max_y == y1`：已经顶到左上角的高度，后面再没有合法 y2 → ==提前 break=='
                                           if S.max_y == S.y1 else '`max_y` 还没顶到 `y1`，继续往右'),
        'return ans': '返回合法点对数 =={ret}==',
    },
    cards=dict(
        one_liner='排好序后，只需维护"中间点的最大 y"就能 O(1) 判断矩形是否干净',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['给定平面上 `n` 个点，Alice 在矩形左上角，Bob 在右下角',
                 '围栏（含边界）内不能有其他人，问有多少种 (Alice, Bob) 点对',
                 '示例：`[[6,2],[4,4],[2,6]]` → `2`',
                 '本视频：6 个点，其中有两个点横坐标相同'],
        quote='对于下标在闭区间 [i+1,j-1] 中的每个点，纵坐标要么大于 y1，要么小于 y2。……只需维护遍历过的点的纵坐标的最大值 max_y。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先按 x 升序排序，x 相同按 ==y 降序==，于是 `x1 ≤ x2` 自动成立',
              '大于 `y1` 的点直接跳过；其余点只要 `y2 > max_y`，中间就没有点挡住',
              '"O(1) 时间获取 O(n) 信息"：用最大值代替再扫一遍 `[i+1, j-1]`'],
        summary=['时间 `O(n^2)`，空间 `O(1)`',
                 '易错：x 相同时必须 y 降序，否则 `(1,3)→(1,1)` 会漏判中间的 `(1,2)`',
                 '`y1 >= y2` 要带等号：围栏可以是一条线段',
                 '`max_y == y1` 时 break 是优化，不影响答案'],
    ),
)
