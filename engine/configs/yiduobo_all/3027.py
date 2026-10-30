PTS = [[1, 5], [1, 3], [2, 4], [3, 2], [4, 6], [5, 1]]


def _ij(S):
    if 'i' not in S:
        return None, None
    return S['i'], S.get('j')


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pts = S['points']
    cv.text((x0 + 18, y0 + 4), '点按 x 升序、x 相同时 y 降序（蓝=i，粉=j，黄线=ma）', 22, T['muted'], bold=True)
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
    fresh = line in (6, 7)   # 刚换了新的 i：ma / j 还是上一轮的
    if fresh:
        j = None
    if i is not None:
        a = pts[i]
        if not fresh and 'ma' in S and S['ma'] > -10 ** 9 - 1:
            cv.dashed((X(a[0]), Y(S['ma'])), (gx1, Y(S['ma'])), T['yellow'], 3)
            cv.text((gx1 + 8, Y(S['ma'])), f"ma={S['ma']}", 20, T['yellow'], anchor='lm', bold=True)
        if j is not None and line in (8, 9, 10):
            b = pts[j]
            ok = a[1] >= b[1] and b[1] > B.get('ma', S['ma']) if line == 8 else (line in (9, 10))
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
    author='yiduobo', technique='排序 + 暴力枚举，ma 记录中间最高点',
    tags=['枚举右，维护左', 'CDQ 分治 / 值域分治', '难度分 2020'],
    code='''
class Solution(object):
    def numberOfPairs(self, points):

        points.sort(key=lambda d: (d[0], -d[1]))
        res = 0
        for i in range(len(points) - 1):
            ma = -10 ** 9 - 1
            for j in range(i + 1, len(points)):
                if ma < points[j][1] <= points[i][1]:
                    ma = points[j][1]
                    res += 1
        
        return res
''',
    call=f'Solution().numberOfPairs({PTS!r})',
    expect=6, max_steps=50,
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='array', var='points', label='points（排序后）', cell=120, pointers={'i': 'blue', 'j': 'pink'}),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ma', 'ma', 'yellow'), ('res', 'res', 'green')],
    captions={
        'points.sort': '先按 x 升序、y 降序排：任意 `j < k`，要么 `x[j] < x[k]`，要么 `y[j] > y[k]`',
        'res = 0': '`res` 统计合法点对',
        'for i in range': '`points[{i}]` 当左上角 i',
        'ma = -10': '`ma`：已扫过的点里，y 不超过 `points[i]` 的最大纵坐标；先设成极小值',
        'for j in range': '`points[{j}]` 当右下角 j，只需看 `i+1..j-1` 的点会不会落进矩形',
        'if ma < points[j][1]': lambda S, B, r: (
            f'`{S.ma} < {S.points[S.j][1]} <= {S.points[S.i][1]}` 成立：比中间点都高、又不超过 i → ==矩形内无其他点=='
            if S.ma < S.points[S.j][1] <= S.points[S.i][1]
            else (f'`{S.points[S.j][1]}` 比 i 的 `{S.points[S.i][1]}` 还高：右下角跑到左上角上面了，不合法'
                  if S.points[S.j][1] > S.points[S.i][1]
                  else f'`{S.points[S.j][1]} <= ma = {S.ma}`：前面有个点 y 更高，落在矩形里，不合法')),
        'ma = points[j][1]': '`ma` 更新为 `{ma}`，后面的 j 要比它还高才行',
        'res += 1': '得到一对合法站位，`res` = =={res}==',
        'return res': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='排序保证横向天然合法，只需检查纵向有没有点挡在中间',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['`n` 个点，Alice 在矩形左上角、Bob 在右下角',
                 '围栏内部和边缘不能有别人，求合法 (Alice, Bob) 对数',
                 '示例：`[[6,2],[4,4],[2,6]]` → `2`',
                 '本视频：6 个点，两个点横坐标相同'],
        quote='先对所有节点按横坐标升序，纵坐标降序进行排序，这样做的理由是可以保证对于任意一组j < k，其要么满足x[j] < x[k]，要么满足y[j] > y[k]。',
        quote_src='—— yiduobo 题解原文',
        idea=['原文先想到 CDQ 式的"多维比较"，但这题允许 `O(n^2)`，排序后暴力枚举就够',
              '排序后 `i < j < k` 时，k 绝不会落在 i、j 围成的矩形里',
              '中间点的 x 一定在范围内，只用看纵坐标：用 `ma` 记中间点里不超过 i 的最大 y'],
        summary=['时间 `O(n^2)`，空间 `O(1)`',
                 '`ma < y_j <= y_i`：右边带等号，因为围栏可以是线段',
                 '`ma` 初值 `-10**9-1` 比所有纵坐标都小',
                 '原文外层是 `range(len(points) - 1)`，最后一个点不用当左上角',
                 '对比灵神：灵神多一步 `max_y == y1` 提前 break；yiduobo 不剪枝'],
    ),
)
