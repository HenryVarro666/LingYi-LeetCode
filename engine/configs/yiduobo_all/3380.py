PTS = [(1, 1), (1, 3), (3, 1), (3, 3), (2, 2)]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '平面上的点（黄 = 左下角，蓝 = 右下 / 左上，粉 = 右上；绿框 = 当前合法矩形）', 22, T['muted'], bold=True)
    gx0, gx1 = x0 + 90, x1 - 90
    gy0, gy1 = y0 + 70, y1 - 50
    mx, my = 4, 4
    sx, sy = (gx1 - gx0) / mx, (gy1 - gy0) / my

    def P(x, y):
        return gx0 + x * sx, gy1 - y * sy
    for k in range(1, mx + 1):
        cv.line([P(k, 0.4), P(k, my)], T['border'], 1)
        cv.text((P(k, 0)[0], gy1 + 12), k, 20, T['dim'], anchor='mt', mono=True)
    for k in range(1, my + 1):
        cv.line([P(0.4, k), P(mx, k)], T['border'], 1)
        cv.text((gx0 - 30, P(0, k)[1]), k, 20, T['dim'], anchor='mm', mono=True)
    live = S.get('_line', 0) in (51, 52) and 'x2' in S and 'x1' in S
    if live:
        a, b = P(S['x1'], S['y1']), P(S['x2'], S['y2'])
        ok = (S['x2'], S['y2']) in S['cnt'] and S['cnt'][(S['x2'], S['y2'])] - S['cnt'].get((S['x1'], S['y2']), 0) - S['cnt'].get((S['x2'], S['y1']), 0) + S['cnt'].get((S['x1'], S['y1']), 0) == 1
        if True:
            cv.rect((a[0], b[1], b[0], a[1]), outline=T['green'] if ok else T['red'], width=4, r=4)
    for (x, y) in PTS:
        X, Y = P(x, y)
        col = T['muted']
        if live:
            if (x, y) == (S['x1'], S['y1']):
                col = T['yellow']
            elif (x, y) in ((S['x2'], S['y1']), (S['x1'], S['y2'])):
                col = T['blue']
            elif (x, y) == (S['x2'], S['y2']):
                col = T['pink']
        cv.rect((X - 13, Y - 13, X + 13, Y + 13), fill=col, r=13)
        cv.text((X + 18, Y - 20), f'({x},{y})', 18, T['dim'], anchor='lb', mono=True)


CONFIG = dict(
    num=3380, title='用点构造面积最大的矩形 I', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表找邻点 · 二维前缀和判空',
    code='''
class Solution(object):
    def maxRectangleArea(self, xCoord, yCoord):
        
        points = list(zip(xCoord, yCoord))

        cnt = {}
        points.sort()
        for x, y in points:
            cnt[(x, y)] = 1
        
        def calc(points, left, right):
            if left == right:
                return
            
            mid = (left + right) >> 1
            calc(points, left, mid)
            calc(points, mid + 1, right)
            
            i = left
            j = mid + 1
            tmp = []
            while i <= mid or j <= right:
                if i == mid + 1 or (j <= right and points[i][1] > points[j][1]):
                    cnt[(points[j][0], points[j][1])] += i - left
                    tmp.append(points[j][:])
                    j += 1
                else:
                    tmp.append(points[i][:])
                    i += 1

            for index, (x, y) in enumerate(tmp):
                points[index + left] = [x, y]

        calc(points, 0, len(points) - 1)
        
        points.sort()
        up = {}
        for index in range(len(points) - 1):
            if points[index][0] == points[index + 1][0]:
                up[(points[index][0], points[index][1])] = points[index + 1][:]
        
        points.sort(key=lambda d:(d[1], d[0]))
        res = -1
        for index in range(len(points) - 1):
            x1, y1 = points[index]
            if (x1, y1) not in up:
                continue
            if points[index + 1][1] != points[index][1]:
                continue
            x2, y2 = points[index + 1][0], up[(x1, y1)][1]
            if (x2, y2) in cnt and cnt[(x2, y2)] - cnt[(x1, y2)] - cnt[(x2, y1)] + cnt[(x1, y1)] == 1:
                res = max(res, (x2 - x1) * (y2 - y1))
        
        return res
''',
    call='Solution().maxRectangleArea([1,1,3,3,2], [1,3,1,3,2])',
    expect=-1,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='map', var='cnt', fmt=lambda k, v: f'({k[0]},{k[1]}) → {v}', label='cnt：左下方（含自己）的点数', h=170),
        dict(type='map', var='up', fmt=lambda k, v: f'({k[0]},{k[1]}) ↑ ({v[0]},{v[1]})', label='up：同一列正上方最近的点', h=130),
    ],
    watch=['x1', 'y1', 'x2', 'y2', ('res', 'res', 'green')],
    captions={
        'points = list': '把两列坐标拼成点，下面按 x、y 两个维度各处理一遍',
        'cnt[(points[j][0]': '左半边已放好的 `{i - left}` 个点 x 更小、y 不大于它 → 都在它左下方：`cnt[({points[j][0]},{points[j][1]})] += {i - left}` = =={cnt[(points[j][0], points[j][1])]}==',
        'i == mid + 1 or': lambda S, B, r: ('左半边已用完，直接放右半边的点' if S.i == S.mid + 1 else
                                         (f'右边 y = `{S.points[S.j][1]}` 比左边 `{S.points[S.i][1]}` 更小，先放右边（左边剩下的点 y 更大，不在它下方）' if S.j <= S.right and S.points[S.i][1] > S.points[S.j][1]
                                          else f'左边 y = `{S.points[S.i][1]}` 不大于右边 → 先放左边，它不会被右边点统计')),
        'calc(points, 0': '先对 y 归并排序，边合并边统计每个点左下方的点数',
        'up[(points[index][0]': '同一列相邻的两点：`up[({points[index][0]},{points[index][1]})]` = 正上方的点 `({points[index + 1][0]},{points[index + 1][1]})`',
        'x1, y1 = points[index]': '以 `({x1},{y1})` 作矩形左下角（按 y 为主、x 为辅排序）',
        'not in up': lambda S, B, r: (f'`({S.x1},{S.y1})` 正上方没有点 → 构不成矩形，跳过' if (S.x1, S.y1) not in S.up else f'`({S.x1},{S.y1})` 的正上方有点 `{tuple(S.up[(S.x1, S.y1)])}`'),
        '!= points[index][1]': lambda S, B, r: (f'下一个点和它不在同一行（y {S.points[S.index + 1][1]} ≠ {S.points[S.index][1]}）→ 右边没有点，跳过' if S.points[S.index + 1][1] != S.points[S.index][1] else '下一个点就在同一行右侧，当作右下角'),
        'x2, y2 = ': '右下角 x2 = `{x2}`，左上角 y2 = `{y2}` → 右上角 `({x2},{y2})`',
        'if (x2, y2) in cnt': lambda S, B, r: (f"右上角 `({S.x2},{S.y2})` 不存在 → 构不成矩形" if (S.x2, S.y2) not in S.cnt else
                                              f"四角相减：`{S.cnt[(S.x2, S.y2)]} - {S.cnt[(S.x1, S.y2)]} - {S.cnt[(S.x2, S.y1)]} + {S.cnt[(S.x1, S.y1)]}` = =={S.cnt[(S.x2, S.y2)] - S.cnt[(S.x1, S.y2)] - S.cnt[(S.x2, S.y1)] + S.cnt[(S.x1, S.y1)]}==" + (' → 恰为 1，矩形是空的' if S.cnt[(S.x2, S.y2)] - S.cnt[(S.x1, S.y2)] - S.cnt[(S.x2, S.y1)] + S.cnt[(S.x1, S.y1)] == 1 else ' ≠ 1，里面还有别的点，不合法')),
        'res = max': '用面积更新答案：`res` = {res}',
        'return res': lambda S, B, r: f'返回 `{r}`' + ('：唯一的矩形里有 `(2,2)`，不合法' if r == -1 else ''),
    },
    skip=['cnt[(x, y)] = 1', 'for x, y in points', 'tmp.append', 'i += 1', 'j += 1', 'for index, (x, y)', 'points[index + left]',
          'i = left', 'j = mid + 1', 'tmp = []', 'mid = ', 'continue', 'if left == right', 13, 'while i <= mid', 'for index in range', 'if points[index][0] ==', 'calc(points, left, mid)', 'calc(points, mid + 1, right)'],
    max_steps=100,
    cards=dict(
        one_liner='先算每个点左下方有几个点，再用二维前缀和判断矩形里是否空',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给一组互不相同的点，选 4 个点做顶点，组成边平行于坐标轴的矩形',
                 '矩形内部和边界上==不能再有其他点==，求最大面积，没有就返回 `-1`',
                 '示例 2：`[[1,1],[1,3],[3,1],[3,3],[2,2]]` → `-1`（中心点 `(2,2)` 在矩形内）'],
        quote='若矩形的左下角为(x1, y1)，那么左上角的点(x1, y2)只能是x1这一列上刚好位于(x1, y1)上面的那个点。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举左下角：左上角取同列正上方最近的点，右下角取同行右边最近的点，右上角就定了',
              '`cnt[(x,y)]` = 横纵坐标都不超过它的点数，四角相减 = 矩形内点数，恰好等于 1 才是空矩形',
              '`cnt` 用按 x 排序后对 y 归并排序，在合并时顺便数出来'],
        summary=['时间 `O(n log n)`（归并统计 + 排序），空间 `O(n)`',
                 '易错点：四角相减后要把三个角加回，空矩形的条件是结果 `== 1`',
                 '原文是 3382 的写法（传入 xCoord、yCoord），本题 points 拆成两列传入；`zip` 外加 `list`、删去类型说明',
                 '同一个矩形可以由 `up` 和同行右邻点唯一确定，所以不会漏也不会重'],
    ),
)
