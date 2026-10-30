XS = [1, 1, 3, 3, 1, 3]
YS = [1, 3, 1, 3, 2, 2]


def _cells(S):
    pts = S.get('points')
    if pts is None:
        return None
    return [f'{p[0]},{p[1]}' for p in pts]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pts = list(zip(XS, YS))
    ux = sorted(set(XS))
    uy = sorted(set(YS))
    W, H = x1 - x0 - 140, y1 - y0 - 170
    gx = lambda x: x0 + 80 + (ux.index(x) / max(1, len(ux) - 1)) * W
    gy = lambda y: y1 - 60 - (uy.index(y) / max(1, len(uy) - 1)) * H
    cv.text((x0 + 18, y0 + 4), '点旁边的数字 = cnt：横、纵坐标都不超过该点的点数（含自己）', 22, T['muted'], bold=True)
    cnt = S.get('cnt') or {}
    # 候选矩形
    if all(k in S for k in ('x1', 'y1', 'x2', 'y2')) and 'index' in S and S.get('up') is not None:
        a, b, c, d = S['x1'], S['y1'], S['x2'], S['y2']
        if (c, d) in cnt and (a, d) in cnt and (c, b) in cnt:
            ok = cnt[(c, d)] - cnt[(a, d)] - cnt[(c, b)] + cnt[(a, b)] == 1
            col = T['green'] if ok else T['red']
            cv.rect((gx(a), gy(d), gx(c), gy(b)), fill=col, alpha=45, outline=col, width=3)
    for x in ux:
        cv.text((gx(x), y1 - 36), x, 20, T['dim'], anchor='mt', mono=True)
    for y in uy:
        cv.text((x0 + 56, gy(y)), y, 20, T['dim'], anchor='rm', mono=True)
    hot = set()
    if 'x1' in S and 'x2' in S and 'index' in S:
        hot = {(S['x1'], S['y1'])}
        if 'y2' in S:
            hot.add((S['x2'], S['y2']))
    for p in pts:
        X, Y = gx(p[0]), gy(p[1])
        ring = T['yellow'] if p in hot else None
        cv.rect((X - 22, Y - 22, X + 22, Y + 22), fill=T['blue'], r=22, outline=ring or T['border'], width=5 if ring else 1)
        cv.text((X, Y), cnt.get(p, ''), 22, T['bg'], anchor='mm', bold=True, mono=True)


def _cap_merge(S, B, ret):
    i, j = S.i, S.j
    if not (i == S.mid + 1 or (j <= S.right and S.points[i][1] > S.points[j][1])):
        return f'`y_i = {S.points[i][1]} ≤ y_j = {S.points[j][1]}`：左边的点先出列（它对右边 `cnt` 的贡献暂不增加）'
    if i == S.mid + 1:
        return f'左半边用完，右边 `{S.points[j][1]}` 直接出列；左边 `[{S.left}, {S.mid}]` 里 `{i - S.left}` 个点的 y 都不超过它'
    yi, yj = S.points[i][1], S.points[j][1]
    return f'`y_i = {yi} > y_j = {yj}`：左边 `i` 之前的 `{i - S.left}` 个点（x 更小、y 不超过 `{yj}`）都在右点的左下方 → ==cnt 加 {i - S.left}=='


def _cap_cond(S, B, ret):
    d = S.cnt[(S.x2, S.y2)] - S.cnt[(S.x1, S.y2)] - S.cnt[(S.x2, S.y1)] + S.cnt[(S.x1, S.y1)]
    return (f'`cnt[(x2,y2)] − cnt[(x1,y2)] − cnt[(x2,y1)] + cnt[(x1,y1)] = {d}`：'
            + ('==等于 1== → 矩形里除四个角外没有别的点' if d == 1 else '不等于 1 → 里面还有别的点'))


CONFIG = dict(
    num=3382, title='用点构造面积最大的矩形 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='归并排序求二维偏序 + 二维前缀和容斥',
    tags=['常用数据结构'],
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
    call=f'Solution().maxRectangleArea({XS}, {YS})',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var=_cells, label='points（x,y；归并时按 y 从小到大排；框 = 当前归并区间）', h=170, cell=88,
             pointers={'i': 'blue', 'j': 'pink'}, window=('left', 'right')),
        dict(type='map', var='cnt', label='cnt[(x, y)]', fmt=lambda k, v: f'{k[0]},{k[1]}: {v}', h=130, font=24),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('res', 'res', 'green')],
    skip=[8, 17, 12, 13, 15, 19, 20, 21, 22, 25, 26, 28, 29, 31, 32, 38, 39, 40, 44, 45, 47, 49],
    captions={
        4: '`points` 先整理成 `(x, y)` 列表',
        6: '`cnt[(x, y)]`：横、纵坐标都不超过 `(x, y)` 的点数（先都记成 1：自己）',
        7: '先按 x（再按 y）排序，这样 x 已经有序，只需再对 y 做归并',
        9: '`cnt[({x}, {y})] = 1`',
        16: '递归：先把左半边排好；右半边同理（左半边的点 x 都不大于右半边）',
        23: _cap_merge,
        24: '右边点 `{points[j]}` 的 `cnt` += `{i - left}` → ==`{cnt[(points[j][0], points[j][1])]}`==',
        34: '分治：x 已有序，对 y 归并排序，边排边统计每个点左下方的点数 `cnt`',
        36: '重新按 x、再按 y 排序（归并后 `points` 是乱的）',
        37: '`up[(x, y)]`：同一列上紧挨着的上一个点（y 更大）',
        40: '`up[({points[index][0]}, {points[index][1]})] = {points[index + 1]}`：同一列上紧挨着的上面的点',
        42: '改成先按 y、再按 x 排序：同一行的点相邻，相邻点 = 右边紧挨着的点',
        43: '`res = -1`：找不到矩形就返回 -1',
        46: lambda S, B, r: (f'`({S.x1},{S.y1})` 的正上方没有点 → 当不了左下角，跳过' if (S.x1, S.y1) not in S.up
                              else f'`({S.x1},{S.y1})` 正上方是 `{S.up[(S.x1, S.y1)]}`，可以当左下角'),
        48: lambda S, B, r: (f'下一个点 y = `{S.points[S.index + 1][1]}` 不在同一行 → 右边没有紧挨的点，跳过' if S.points[S.index + 1][1] != S.points[S.index][1]
                              else f'下一个点 `{S.points[S.index + 1]}` 在同一行，是右下角'),
        50: '右上角 `(x2, y2) = ({x2}, {y2})`：x 取右下角的，y 取左上角的',
        51: _cap_cond,
        52: '矩形空：面积 `({x2} − {x1}) × ({y2} − {y1})` → `res = {res}`',
        54: '最大面积 = =={ret}==',
    },
    max_steps=110,
    cards=dict(
        one_liner='cnt 容斥：四个角的 cnt 加减后等于 1，矩形里就没有别的点',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['平面上有 `n` 个点，选 4 个点作为轴平行矩形的顶点',
                 '矩形内部不能有其他点，求最大面积，没有则 `-1`',
                 '本视频：`x=[1,1,3,3,1,3]`，`y=[1,3,1,3,2,2]` → `2`'],
        quote='cnt[(x2, y2)] - cnt[(x1, y2)] - cnt[(x2, y1)] + cnt[(x1, y1)] = 1',
        quote_src='—— yiduobo 题解原文',
        idea=['左下角 `(x1,y1)` 的正上方点、正右方点只能是紧挨着的那个，所以枚举左下角就得到矩形',
              '矩形内点数用二维前缀和：`cnt` 是“横纵坐标都不超过它”的点数，四角容斥',
              '`cnt` 用归并排序算：按 x 排好后，对 y 归并，右半边每个点统计左半边有几个 y 不超过它的'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，`zip(...)` 返回迭代器，已改为 `list(zip(...))`',
                 '易错：容斥后“=1”而不是 4，因为另外三个角在公式里被减掉了又加回来',
                 '易错：归并时 y 相同要先取左边，保证“不超过”也算进去',
                 '对比灵神：灵神用树状数组一边扫描一边数点，yiduobo 用归并分治离线求 `cnt`'],
    ),
)
