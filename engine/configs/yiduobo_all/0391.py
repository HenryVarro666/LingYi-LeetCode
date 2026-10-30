def _idx(S):
    rs = S['rectangles']
    if 'x1' in S:
        cur = [S['x1'], S['y1'], S['x2'], S['y2']]
        return rs.index(cur) if cur in rs else 0
    return 0 if 'lx' in S else -1


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    rs = S['rectangles']
    xs = [r[0] for r in rs] + [r[2] for r in rs]
    ys = [r[1] for r in rs] + [r[3] for r in rs]
    mx, my = max(xs), max(ys)
    mnx, mny = min(xs), min(ys)
    cv.text((x0 + 18, y0 + 4), '小矩形（已扫描的填色；点：橙 = 出现奇数次，灰 = 偶数次）', 22, T['muted'], bold=True)
    top, bot = y0 + 56, y1 - 14
    sc = min((bot - top) / (my - mny), (x1 - x0 - 140) / (mx - mnx))
    ox = x0 + ((x1 - x0) - sc * (mx - mnx)) / 2
    X = lambda x: ox + (x - mnx) * sc
    Y = lambda y: bot - (y - mny) * sc
    k = _idx(S)
    cols = ['blue', 'pink', 'green', 'purple', 'cyan', 'yellow', 'orange']
    for i, r in enumerate(rs):
        if i > k:
            cv.rect((X(r[0]), Y(r[3]), X(r[2]), Y(r[1])), outline=T['border'], width=1)
            continue
        cv.rect((X(r[0]), Y(r[3]), X(r[2]), Y(r[1])), fill=T[cols[i % 7]], alpha=110, outline=T[cols[i % 7]], width=3)
        cv.text(((X(r[0]) + X(r[2])) / 2, (Y(r[1]) + Y(r[3])) / 2), f'#{i}', 22, T['text'], anchor='mm', bold=True)
    if 'lx' in S and 'rx' in S:
        a, b = (X(S['lx']), Y(S['ry'])), (X(S['rx']), Y(S['ly']))
        for p, q in (((a[0], a[1]), (b[0], a[1])), ((b[0], a[1]), (b[0], b[1])), ((b[0], b[1]), (a[0], b[1])), ((a[0], b[1]), (a[0], a[1]))):
            cv.dashed(p, q, T['yellow'], 3)
    pc = S.get('point_cnt') or {}
    for (px, py), c in pc.items():
        col = T['orange'] if c % 2 == 1 else T['dim']
        cv.rect((X(px) - 7, Y(py) - 7, X(px) + 7, Y(py) + 7), fill=col, r=7)


def _cnt(S, B, ret):
    n = sum(1 for v in S['point_cnt'].values() if v % 2 == 1)
    return f'出现奇数次的点有 `{n}` 个，`cnt == 4` → =={ret}=='


CONFIG = dict(
    num=391, title='完美矩形', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='面积和 + 顶点奇偶计数',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def isRectangleCover(self, rectangles):

        lx, ly, rx, ry = rectangles[0]
        sum_area = (rx - lx) * (ry - ly)
        
        point_cnt = {}
        point_cnt[(lx, ly)] = 1
        point_cnt[(lx, ry)] = 1
        point_cnt[(rx, ly)] = 1
        point_cnt[(rx, ry)] = 1

        for x1, y1, x2, y2 in rectangles[1:]:
            if x1 < lx or y1 < ly:
                lx = x1
                ly = y1
            if x2 > rx or y2 > ry:
                rx = x2
                ry = y2
            sum_area += (y2 - y1) * (x2 - x1)
            point_cnt[(x1, y1)] = point_cnt.get((x1, y1), 0) + 1
            point_cnt[(x1, y2)] = point_cnt.get((x1, y2), 0) + 1
            point_cnt[(x2, y1)] = point_cnt.get((x2, y1), 0) + 1
            point_cnt[(x2, y2)] = point_cnt.get((x2, y2), 0) + 1

        if (ry - ly) * (rx - lx) != sum_area:
            return False
        if point_cnt.get((lx, ly), 0) != 1 or point_cnt.get((lx, ry), 0) != 1 or point_cnt.get((rx, ly), 0) != 1 or point_cnt.get((rx, ry), 0) != 1:
            return False
        cnt = 0
        for key in point_cnt:
            if point_cnt[key] % 2 == 1:
                cnt += 1
        return cnt == 4
''',
    call='Solution().isRectangleCover([[1,1,3,3],[3,1,4,2],[3,2,4,4],[1,3,2,4],[2,3,3,4]])',
    expect=True,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='map', var='point_cnt', fmt=lambda k, v: f'{k}:{v}', font=20, h=210, label='point_cnt：每个顶点被多少个小矩形用到'),
    ],
    watch=[('lx,ly', '(lx, ly)', 'blue'), ('rx,ry', '(rx, ry)', 'pink'), ('sum_area', 'sum_area', 'green'), ('cnt', 'cnt', 'orange')],
    skip=['point_cnt[(x1, y1)] =', 'point_cnt[(x1, y2)]', 'point_cnt[(x2, y1)]', 'point_cnt[(rx, ly)] = 1', 'point_cnt[(lx, ry)] = 1', 'for key in point_cnt'],
    captions={
        'lx, ly, rx, ry = rectangles[0]': '先拿第一个矩形：左下 `({lx}, {ly})`，右上 `({rx}, {ry})`',
        'sum_area = (rx': '面积和先记下第一个矩形的面积：`sum_area` = =={sum_area}==',
        'point_cnt[(lx, ly)] = 1': '第一个矩形的四个角各记 1 次（左下、左上、右下、右上）',
        'point_cnt[(rx, ry)] = 1': '四个角记完，`point_cnt` = `{point_cnt}`',
        'for x1, y1, x2, y2': '{"所有矩形都扫完了" if B.get("x1") == x1 and B.get("y1") == y1 and B.get("x2") == x2 and B.get("y2") == y2 and B.get("sum_area") == sum_area else f"取下一个矩形 `({x1},{y1})–({x2},{y2})`"}',
        'if x1 < lx or y1 < ly': '这个矩形的左下角 `({x1},{y1})` 比当前左下角 `({B.lx},{B.ly})` 更靠左下吗？{"是，更新" if (x1 < B.lx or y1 < B.ly) else "不是，保持"}',
        'lx = x1': '整体左下角更新：`lx` → {lx}',
        'ly = y1': '整体左下角更新：`ly` → {ly}',
        'if x2 > rx or y2 > ry': '这个矩形的右上角 `({x2},{y2})` 比当前右上角 `({rx},{ry})` 更靠右上吗？{"是，更新" if (x2 > B.rx or y2 > B.ry) else "不是，保持"}',
        'rx = x2': '整体右上角更新：`rx` → {rx}',
        'ry = y2': '整体右上角更新：`ry` → {ry}',
        'sum_area += ': '累加面积：`+ {(y2-y1)} × {(x2-x1)}` → `sum_area` = =={sum_area}==',
        'point_cnt[(x2, y2)] =': '这个矩形四个角的次数各 +1：左下 `({x1},{y1})` 现在 {point_cnt[(x1, y1)]} 次，右上 `({x2},{y2})` 现在 {point_cnt[(x2, y2)]} 次（共 {len(point_cnt)} 个点）',
        '(ry - ly) * (rx - lx) != sum_area': '外框面积 `({ry}-{ly})×({rx}-{lx}) = {(ry-ly)*(rx-lx)}`，小矩形面积和 `{sum_area}`：{"不相等，有缝隙或重叠 → False" if (ry-ly)*(rx-lx) != sum_area else "相等，继续检查顶点"}',
        'if point_cnt.get((lx, ly)': '外框四个角必须各只出现 1 次，否则有别的矩形压在角上：{"有问题 → False" if (point_cnt.get((lx, ly), 0) != 1 or point_cnt.get((lx, ry), 0) != 1 or point_cnt.get((rx, ly), 0) != 1 or point_cnt.get((rx, ry), 0) != 1) else "四角都只出现 1 次，通过"}',
        'cnt = 0': '再数一数出现==奇数次==的顶点个数',
        'for key in point_cnt': '看顶点 `{key}`，被 `{point_cnt[key]}` 个矩形共用',
        'if point_cnt[key] % 2 == 1': '顶点 `{key}` 被 `{point_cnt[key]}` 个矩形共用，余数 `{point_cnt[key] % 2}`：{"奇数次，是外框的角 → cnt + 1" if point_cnt[key] % 2 == 1 else "偶数次，内部共享的点，跳过"}',
        'cnt += 1': '`cnt` → {cnt}',
        'return cnt == 4': '奇数次的点正好 `{cnt}` 个，应为 4（只剩外框四角）→ =={ret}==',
    },
    cards=dict(
        one_liner='面积对得上，且只有四个外框角出现奇数次',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给若干轴对齐的小矩形 `[x1,y1,x2,y2]`（左下、右上）',
                 '判断它们能否==恰好、不重叠、无缝隙==拼成一个大矩形',
                 '本视频：5 个小矩形 → `True`'],
        quote='如果拼出来的矩形是完美矩形，那么除了完美矩形的四个角只属于某一个矩形之外，其他矩形四个角上的点必然是偶数个矩形共享的。',
        quote_src='—— yiduobo 题解原文',
        idea=['先一趟扫描：找外框左下 / 右上，累加小矩形面积，统计每个顶点出现次数',
              '条件一：小矩形面积和 == 外框面积（排除缝隙与多余部分）',
              '条件二：外框四角只出现 1 次，其余顶点都是偶数次（排除重叠错位）'],
        summary=['时间 `O(n)`，空间 `O(n)`（`point_cnt` 最多 `4n` 个点）',
                 '两个条件==缺一不可==：只有面积相等，重叠 + 缝隙可能互相抵消',
                 '最后数奇数次的点：只有外框四角才满足，所以 `cnt == 4`',
                 '原文在 Python 3 下可直接运行，没有改动；作者自称这是“比较 trick 的方法”，没有用线段相交判断'],
    ),
)
