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
    author='灵茶山艾府', technique='枚举两矩形 + 最优性剪枝', tags=[],
    code='''
class Solution:
    def largestSquareArea(self, bottomLeft: List[List[int]], topRight: List[List[int]]) -> int:
        max_side = 0
        for i, ((bx, by), (tx, ty)) in enumerate(zip(bottomLeft, topRight)):
            if tx - bx <= max_side or ty - by <= max_side:
                continue  # 最优性剪枝：max_side 不可能变大
            for j in range(i):
                bx2, by2 = bottomLeft[j]
                tx2, ty2 = topRight[j]
                width = min(tx, tx2) - max(bx, bx2)  # 右上横坐标 - 左下横坐标
                height = min(ty, ty2) - max(by, by2)  # 右上纵坐标 - 左下纵坐标
                side = min(width, height)
                max_side = max(max_side, side)
        return max_side ** 2
''',
    call='Solution().largestSquareArea(%r, %r)' % (BL, TR),
    expect=4,
    views=[
        dict(type='text', fn=lambda S: (f"交集：宽 `{S['width']}`，高 `{S['height']}` → 边长 ==min=={'' if 'side' not in S else ' = ' + str(S['side'])}" if 'height' in S and S['_line'] >= 10 else f"`max_side = {S['max_side']}`" if 'max_side' in S else '')),
        dict(type='custom', draw=_mk_draw(BL, TR, 'i', 'j', 7, 11), h=520),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'width', 'height', ('max_side', 'max_side', 'green')],
    captions={
        'max_side = 0': '`max_side` 记录目前能放下的最大正方形边长',
        'if tx - bx <= max_side': '矩形 `{i}` 宽 `{tx-bx}`、高 `{ty-by}`，当前 `max_side = {max_side}`：有一边 ≤ max_side 吗？{"==是，剪枝==" if (tx-bx<=max_side or ty-by<=max_side) else "否，要枚举"}',
        'continue': '它的边长不够，交集只会更小 → ==max_side 不可能变大==，跳过内层循环',
        'for j in range': '内层只枚举 `j < i` 的矩形，每一对只看一次',
        'bx2, by2': '取出矩形 `{j}` 的左下角 `({bx2}, {by2})`',
        'tx2, ty2': '取出矩形 `{j}` 的右上角 `({tx2}, {ty2})`',
        'width = ': '交集宽 = 右上横坐标取小 − 左下横坐标取大 = `min({tx},{tx2}) - max({bx},{bx2})` = =={width}==',
        'height = ': '交集高 = `min({ty},{ty2}) - max({by},{by2})` = =={height}==',
        'side = min': '能放下的最大正方形边长 = `min(宽, 高)` = =={side}==（负数说明没交集）',
        'max_side = max': '`max_side = max({B.max_side}, {side}) = {max_side}`',
        'return max_side': '返回边长的平方：`{max_side} ** 2` = =={ret}==',
    },
    cards=dict(
        one_liner='两两枚举矩形，交集还是矩形，取长宽较小者',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['`n` 个与坐标轴平行的矩形，选两个取交集，求交集里能放下的最大正方形面积',
                 '没有任何交集则返回 `0`',
                 '示例：`[[1,1],[2,2],[3,1]]` 与 `[[3,3],[4,4],[6,6]]` → `1`'],
        quote='如果两个矩形有交集，那么交集也是矩形。求出这个交集矩形的左下角和右上角，就可以算出交集矩形的长和宽。',
        quote_src='—— 灵茶山艾府题解',
        idea=['左下角取两者的最大值，右上角取两者的最小值',
              '长和宽的较小值就是正方形边长 `side`，最后平方',
              '优化：外层矩形自己的长或宽 `<= max_side` 时，内层不用跑'],
        summary=['时间 `O(n^2)`，空间 `O(1)`',
                 '易错：`width`、`height` 为负说明没有交集，`max_side` 初值 0 会自动过滤',
                 '答案是面积，别忘了最后 `** 2`',
                 '题解还给了无剪枝的优化前写法，逻辑相同'],
    ),
)
