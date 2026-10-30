PTS = [[1,1],[1,3],[3,1],[3,3],[4,1],[4,3]]


def _plot(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pts = S['points']
    cv.text((x0 + 18, y0 + 4), '平面上的点（黄 = 枚举的左下/右上，绿 = 哈希表里找到的另两个角）', 22, T['muted'], bold=True)
    gx0, gy0, gx1, gy1 = x0 + 70, y0 + 60, x1 - 40, y1 - 50
    maxx = max(p[0] for p in PTS) + 1
    maxy = max(p[1] for p in PTS) + 1
    sx = (gx1 - gx0) / maxx
    sy = (gy1 - gy0) / maxy
    s = min(sx, sy)

    def P(x, y):
        return gx0 + x * s, gy1 - y * s
    for xx in range(maxx + 1):
        cv.line([P(xx, 0), P(xx, maxy)], T['border'], 1)
        cv.text((P(xx, 0)[0], gy1 + 6), xx, 18, T['dim'], anchor='mt', mono=True)
    for yy in range(maxy + 1):
        cv.line([P(0, yy), P(maxx, yy)], T['border'], 1)
        cv.text((gx0 - 10, P(0, yy)[1]), yy, 18, T['dim'], anchor='rm', mono=True)
    live = 'x1' in S and 'x2' in S and 'i' in S and 'j' in S and S.get('_line', 0) >= 9
    if live:
        a, b, c, d = S['x1'], S['y1'], S['x2'], S['y2']
        if a != c and b != d:
            ok = (c * 40001 + b) in S['point_set'] and (a * 40001 + d) in S['point_set']
            col = T['green'] if ok else T['red']
            cv.rect((*P(min(a, c), max(b, d)), *P(max(a, c), min(b, d))), fill=col, alpha=45, outline=col, width=3)
    for k, (x, y) in enumerate(pts):
        px, py = P(x, y)
        col = T['text']
        r = 13
        if 'i' in S and 'j' in S and k in (S['i'], S['j']) and S.get('_line', 0) >= 7:
            col = T['yellow']
            r = 17
        cv.rect((px - r, py - r, px + r, py + r), fill=col, r=r)
        cv.text((px + 20, py - 24), f'({x},{y})', 18, T['muted'], mono=True)
    if live:
        a, b, c, d = S['x1'], S['y1'], S['x2'], S['y2']
        if a != c and b != d:
            for (x, y) in ((c, b), (a, d)):
                px, py = P(x, y)
                ex = (x * 40001 + y) in S['point_set']
                cv.rect((px - 20, py - 20, px + 20, py + 20), outline=T['green'] if ex else T['red'], width=4, r=20)


CONFIG = dict(
    num=939, title='最小面积矩形', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='枚举对角 · 哈希表查另两角',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def minAreaRect(self, points):

        point_set = set()
        for x, y in points:
            point_set.add(x * 40001 + y)
        
        res = None
        for i in range(len(points) - 1):
            for j in range(i + 1, len(points)):
                x1, y1 = points[i]
                x2, y2 = points[j]
                if x1 == x2 or y1 == y2:
                    continue
                
                if (x2 * 40001 + y1) in point_set and (x1 * 40001 + y2) in point_set:
                    area = abs(x2 - x1) * abs(y2 - y1)
                    if res is None or res > area:
                        res = area
        if res is None:
            res = 0
        return res
''',
    call='Solution().minAreaRect(%r)' % PTS,
    expect=2,
    views=[
        dict(type='custom', draw=_plot, h=430),
        dict(type='text', h=70, fn=lambda S: (f"对角 (({S['x1']},{S['y1']}), ({S['x2']},{S['y2']}))，另两角 ({S['x1']},{S['y2']}) 与 ({S['x2']},{S['y1']})" if 'x2' in S and S.get('_line', 0) >= 9 else '先把所有点编码成整数放进哈希表')),
        dict(type='set', var='point_set', h=130, fmt=lambda v: f'{v // 40001},{v % 40001}', font=22),
    ],
    watch=['i', 'j', ('res', 'res', 'green'), 'area'],
    captions={
        'point_set.add': '点 `({x},{y})` 编码成 `{x} * 40001 + {y}` 放入集合，之后 O(1) 查某个点在不在',
        'res = None': '`res = None` 表示还没找到任何矩形',
        'for i in range': '`i` 选第一个点，当作矩形的一个对角',
        'for j in range': '`j` 选第二个点，当作另一个对角（只枚举 j > i，每对只看一次）',
        'x1, y1 = points[i]': '第一个对角 `({x1}, {y1})`',
        'x2, y2 = points[j]': '第二个对角 `({x2}, {y2})`',
        'if x1 == x2 or y1 == y2': lambda S, B, r: f'对角 `({S.x1},{S.y1})`、`({S.x2},{S.y2})`：' + ('同一条竖线或横线，撑不出面积 → 跳过' if (S.x1 == S.x2 or S.y1 == S.y2) else 'x、y 都不同 → 可能是矩形的对角'),
        'continue': '这两点在同一条竖线或横线上，不可能是对角，换下一对',
        'in point_set': '另两个角 `({x2},{y1})`、`({x1},{y2})` 是否都在点集里 → =={(x2 * 40001 + y1) in point_set and (x1 * 40001 + y2) in point_set}==',
        'area = abs': '四个角齐了：面积 = `|{x2}-{x1}| × |{y2}-{y1}|` = =={area}==',
        'res is None or res > area': lambda S, B, r: f'`res` 是 {S.res}，新面积 {S.area}：' + ('还没有答案或更小 → 更新' if (B.res is None or B.res > S.area) else '不比已有答案小 → 不更新'),
        'res = area': '最小面积更新为 =={res}==',
        'if res is None:': lambda S, B, r: '一个矩形都没找到 → 答案取 0' if S.res is None else f'`res` 已经是 {S.res}，不是 None，不用兜底',
        'return res': '枚举完所有对角，最小面积为 =={res}==',
    },
    skip=['res = None\n', 'for j in range', 'x1, y1 = points[i]', 'x2, y2 = points[j]', 'continue'],
    max_steps=110,
    cards=dict(
        one_liner='矩形平行坐标轴：定了对角，另两个角就定了',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['给出平面上一些点，矩形的边必须平行于 x 轴、y 轴',
                 '求这些点能组成的矩形的==最小面积==，不存在返回 `0`',
                 '本视频：`[[1,1],[1,3],[3,1],[3,3],[4,1],[4,3]]` → `2`'],
        quote='设左下角为(x1, y1)，右上角为(x2, y2)，那么只有当存在两点(x1, y2)以及(x2, y1)时，才可能构成矩形。',
        quote_src='—— yiduobo 题解原文',
        idea=['边平行坐标轴 → ==两个对角点就唯一确定矩形==',
              '把每个点编码成 `x * 40001 + y` 存进集合，查询另两角只要 O(1)',
              '双重循环枚举对角，两角都在就算面积、取最小'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '易错点：`x1 == x2` 或 `y1 == y2` 时退化成线段，必须跳过',
                 '编码乘数 40001 要大于坐标范围（0 到 40000），否则不同点会撞键',
                 '没有任何矩形时 `res` 仍是 None，要改成 0 再返回',
                 '原文为 Python 2 风格，本题代码无需修改即可在 Python 3 运行'],
    ),
)
