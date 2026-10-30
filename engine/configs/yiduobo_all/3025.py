def _found(P, i, j):
    """按算法回放：到 (i, j) 为止已计入答案的点对"""
    out = []
    for a in range(len(P) - 1):
        ma = -10 ** 9 - 1
        for b in range(a + 1, len(P)):
            if a > i or (a == i and b > j):
                return out
            if ma < P[b][1] <= P[a][1]:
                ma = P[b][1]
                out.append((a, b))
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    P = S['points']
    cv.text((x0 + 18, y0 + 4), 'points（排序后：横坐标升序、纵坐标降序）  蓝=左上角 i，粉=右下角 j', 24, T['muted'], bold=True)
    mx = max(max(p[0] for p in P), 1)
    my = max(max(p[1] for p in P), 1)
    L, R, Tp, Bt = x0 + 70, x1 - 110, y0 + 90, y1 - 70
    sx = (R - L) / (mx + 1)
    sy = (Bt - Tp) / (my + 1)
    X = lambda x: L + (x + 0.5) * sx
    Y = lambda y: Bt - (y + 0.5) * sy
    cv.line([(L, Bt), (R + 40, Bt)], T['border'], 2)
    cv.line([(L, Bt), (L, Tp - 20)], T['border'], 2)
    for x in range(mx + 1):
        cv.text((X(x), Bt + 8), x, 20, T['dim'], anchor='mt', mono=True)
    for y in range(my + 1):
        cv.text((L - 12, Y(y)), y, 20, T['dim'], anchor='rm', mono=True)
    live = 'i' in S
    i = S.get('i')
    j = S.get('j')
    if live and j is not None and 'ma' in S:
        ln = _found(P, i, j)
    else:
        ln = _found(P, i, -1) if live else []
    for a, b in ln:
        cv.line([(X(P[a][0]), Y(P[a][1])), (X(P[b][0]), Y(P[b][1]))], T['green'], 4)
    if live and j is not None and 'ma' in S and j < len(P) and j > i:
        ax, ay, bx, by = P[i][0], P[i][1], P[j][0], P[j][1]
        cv.rect((min(X(ax), X(bx)), min(Y(ay), Y(by)), max(X(ax), X(bx)), max(Y(ay), Y(by))), fill=T['yellow'], alpha=40)
        cv.dashed((X(ax), Y(ay)), (X(bx), Y(ay)), T['yellow'], 3)
        cv.dashed((X(bx), Y(ay)), (X(bx), Y(by)), T['yellow'], 3)
        cv.dashed((X(bx), Y(by)), (X(ax), Y(by)), T['yellow'], 3)
        cv.dashed((X(ax), Y(by)), (X(ax), Y(ay)), T['yellow'], 3)
    for k, (x, y) in enumerate(P):
        col = T['text']
        if live and k == i:
            col = T['blue']
        elif live and j is not None and k == j and 'ma' in S:
            col = T['pink']
        cv.rect((X(x) - 12, Y(y) - 12, X(x) + 12, Y(y) + 12), fill=col, r=12)
        cv.text((X(x) + 18, Y(y) - 18), f'{k}:({x},{y})', 18, T['muted'], anchor='lb', mono=True)
    if live and 'ma' in S and S['ma'] > -10 ** 9:
        y = Y(S['ma'])
        cv.dashed((L, y), (R, y), T['orange'], 2)
        cv.text((R + 6, y), f"ma={S['ma']}", 20, T['orange'], anchor='lm', bold=True)


def _if(S, B, ret):
    P, i, j, ma = S.points, S.i, S.j, B.get('ma', S.ma)
    yj, yi = P[j][1], P[i][1]
    ok = ma < yj <= yi
    return (f'`{ma if ma > -10**9 else "-inf"} < {yj} <= {yi}` → ==成立==：中间点都挡不住，(点{i}, 点{j}) 合法'
            if ok else
            (f'`y_j = {yj}` 高于 `y_i = {yi}`：j 在 i 上方，不是右下角' if yj > yi else
             f'`y_j = {yj} <= ma = {ma}`：中间有点 y 更高，会落在矩形里 → 不合法'))


CONFIG = dict(
    num=3025, title='人员站位的方案数 I', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='排序 · 暴力枚举 + 维护 ma',
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
    call='Solution().numberOfPairs([[4,1],[1,4],[3,3],[2,2],[5,0]])',
    expect=5,
    views=[dict(type='custom', draw=_draw, h=600)],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ma', 'ma', 'orange'), ('res', 'res', 'green')],
    captions={
        'points.sort': '排序后 `points = {points}`：保证 j<k 时 `x[j] < x[k]` 或 `y[j] > y[k]`，所以 k 不会落进 i、j 的矩形',
        'for i in range': lambda S, B, r: (f'左上角都枚举完了（最后一个点不能当左上角）' if B.get('i') == S.i and 'i' in B else f'枚举左上角 `i = {S.i}`：点 `{S.points[S.i]}`'),
        'ma = -10': '`ma`：i 与 j 之间、纵坐标 ≤ y_i 的点里最高的纵坐标，先设成负无穷',
        'for j in range': lambda S, B, r: (f'`j` 已经枚举到最后一个点：`i = {S.i}` 的所有右下角都看完了'
                                           if B.get('j') == S.j and 'j' in B and B.get('i') == S.i and B.get('_line') != 6 else
                                           f'枚举右下角 `j = {S.j}`：点 `{S.points[S.j]}`'),
        'if ma <': _if,
        'ma = points': '`ma` 更新为 `{ma}`：以后的 j 必须比它更高才不被挡住',
        'res += 1': '找到合法点对，`res` → =={res}==',
        'return res': '一共 `{res}` 对',
    },
    cards=dict(
        one_liner='排好序后，用 ma 记住中间点的最高纵坐标',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['平面上有 `n` 个点，数有多少对 `(A, B)`：A 在 B 左上角（可共线）',
                 '且以 A、B 为对角的矩形（含边界）里没有别的点',
                 '示例：`[[6,2],[4,4],[2,6]]` → `2`'],
        quote='先对所有节点按横坐标升序，纵坐标降序进行排序，这样做的理由是可以保证对于任意一组j < k，其要么满足x[j] < x[k]，要么满足y[j] > y[k]。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序后，i 之后的 j 一定满足 x 不小于 i，只需比较纵坐标',
              '中间点 `i+1..j-1` 的横坐标必在矩形内，只要看纵坐标有没有落在 `(y_j, y_i]`',
              '用 `ma` 记录纵坐标 ≤ y_i 的最大值，`ma < y_j <= y_i` 就合法'],
        summary=['时间 `O(n^2)`，空间 `O(1)`',
                 '排序键 `(x, -y)`：同横坐标时上面的点排前面，保证 A 在 B 左上',
                 '`<= points[i][1]` 取等号：同一水平线上的点对也合法',
                 '`ma` 每个 i 重新初始化；3027 题同样的写法',
                 '原文为 Python 2 风格，在 Python 3 下无需修改，逐字使用'],
    ),
)
