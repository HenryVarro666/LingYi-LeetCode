def _mk_draw(bl, tr, ik, jk, jmin, imin):
    def _draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), '矩形（蓝 = 外层 i，粉 = 内层 j，黄 = 交集）', 24, T['muted'], bold=True)
        mx = max(max(t) for t in tr) + 1
        W = x1 - x0 - 80
        H = y1 - y0 - 110
        sc = min(W, H) / mx
        ox, oy = x0 + 50, y1 - 30

        def P(x, y):
            return (ox + x * sc, oy - y * sc)
        for k in range(mx + 1):
            cv.line([P(k, 0), P(k, mx)], T['border'], 1)
            cv.line([P(0, k), P(mx, k)], T['border'], 1)
            cv.text((P(k, 0)[0], oy + 4), k, 18, T['dim'], anchor='mt', mono=True)
            cv.text((ox - 8, P(0, k)[1]), k, 18, T['dim'], anchor='rm', mono=True)
        i = S.get(ik)
        j = S.get(jk) if S.get('_line', 99) >= jmin else None
        for k in range(len(bl)):
            a, b = P(bl[k][0], tr[k][1]), P(tr[k][0], bl[k][1])
            c = T['blue'] if k == i else T['pink'] if k == j else T['dim']
            cv.rect((a[0], a[1], b[0], b[1]), outline=c, width=4 if k in (i, j) else 2)
            cv.text((a[0] + 8, a[1] + 6), k, 22, c, anchor='la', bold=True)
        if i is not None and j is not None and j < len(bl):
            lx, ly = max(bl[i][0], bl[j][0]), max(bl[i][1], bl[j][1])
            rx, ry = min(tr[i][0], tr[j][0]), min(tr[i][1], tr[j][1])
            if rx > lx and ry > ly and S.get('_line', 99) >= imin:
                a, b = P(lx, ry), P(rx, ly)
                cv.rect((a[0], a[1], b[0], b[1]), fill=T['yellow'], alpha=110)
    return _draw


BL = [[1, 1], [2, 2], [3, 1], [2, 2]]
TR = [[4, 4], [5, 5], [6, 6], [3, 3]]

CONFIG = dict(
    num=3047, title='求交集区域内的最大正方形面积', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='两两枚举 + 线段重叠', tags=[],
    code='''
class Solution(object):
    def largestSquareArea(self, bottomLeft, topRight):

        n = len(bottomLeft)
        res = 0
        for i in range(n - 1):
            for j in range(i + 1, n):
                x = max(0, min(topRight[i][0], topRight[j][0]) - max(bottomLeft[i][0], bottomLeft[j][0]))
                y = max(0, min(topRight[i][1], topRight[j][1]) - max(bottomLeft[i][1], bottomLeft[j][1]))
                res = max(res, min(x, y) ** 2)
        
        return res
''',
    call='Solution().largestSquareArea(%r, %r)' % (BL, TR),
    expect=4,
    views=[
        dict(type='text', fn=lambda S: (f"横向重叠 `x = {S['x']}`，纵向重叠 `y = {S['y']}`" if 'y' in S and S['_line'] >= 8 else f"`res = {S['res']}`" if 'res' in S else '')),
        dict(type='custom', draw=_mk_draw(BL, TR, 'i', 'j', 7, 9), h=520),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'x', 'y', ('res', 'res', 'green')],
    captions={
        'n = len': '共 `{n}` 个矩形，数据不大 → 直接两两枚举',
        'res = 0': '`res` 保存最大的正方形面积',
        'for i in range': '`i` 取 0 ~ n-2，和后面的 `j` 配成一对',
        'for j in range': '`j` 从 `i + 1` 取到末尾，和 `i = {i}` 配对；每一对只枚举一次',
        'x = max': '先看横向：两条线段重叠长度 = 终点较小值 − 起点较大值 = `min({topRight[i][0]},{topRight[j][0]}) - max({bottomLeft[i][0]},{bottomLeft[j][0]})`，外面套 `max(0, …)` → =={x}==',
        'y = max': '再看纵向：同理重叠长度 = =={y}==（不相交就取 0）',
        'res = max': '正方形边长 = `min({x}, {y})`，面积 `{min(x,y)**2}` → `res = max({B.res}, {min(x,y)**2}) = {res}`',
        'return res': '返回最大面积 `{res}`',
    },
    cards=dict(
        one_liner='矩形平行坐标轴：横纵各算线段重叠，取小者',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['`n` 个与坐标轴平行的矩形，选两个取交集，求交集里能放下的最大正方形面积',
                 '没有任何交集则返回 `0`',
                 '示例：`[[1,1],[2,2],[3,1]]` 与 `[[3,3],[4,4],[6,6]]` → `1`'],
        quote='矩形的摆放是平行于坐标轴的，因此可以分别从横纵坐标两个方面分别考虑，取这两个方向交集的较小值即为相交部分的正方形边长。',
        quote_src='—— yiduobo 题解原文',
        idea=['问题变成：给两条线段，求重叠部分的长度',
              '重叠长度 = ==终点的较小值 − 起点的较大值==',
              '横、纵各算一次，取较小的当边长'],
        summary=['时间 `O(n^2)`，空间 `O(1)`',
                 '`max(0, …)` 防止不相交时得到负数再平方变成正数',
                 '易错：先取 `min(x, y)` 再平方，不是先平方',
                 '原文为 Python 2 风格，仅 class 写法不同，代码未改动'],
    ),
)
