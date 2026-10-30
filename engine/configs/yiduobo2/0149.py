PTS = [[1, 1], [2, 2], [3, 3], [3, 1]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '点斜式：过基准点 p 的直线 y − py = k(x − px)（橙 = point1，蓝 = point2）', 22, T['muted'], bold=True)
    lo, hi = 0, 4
    size = min(380, y1 - y0 - 70)
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
    i = S.get('index')
    p1 = S.get('point1')
    p2 = S.get('point2') if 'part1' in S or 'x2' in S else None
    if p1 is not None and p2 is not None and S.get('_line', 0) >= 11 and p2 != p1:
        (bx, by), (cx, cy) = p1, p2
        if cx == bx:
            a, b = P(bx, lo), P(bx, hi)
        else:
            k = (cy - by) / (cx - bx)
            a, b = P(lo, by + k * (lo - bx)), P(hi, by + k * (hi - bx))
            if abs(k) > 1:
                a, b = P(bx + (lo - by) / k, lo), P(bx + (hi - by) / k, hi)
        cv.line([a, b], T['blue'], 3)
    for t, (px, py) in enumerate(PTS):
        X, Y = P(px, py)
        fill = T['panel2']
        if i is not None and t < i:
            fill = (40, 45, 53)
        if p2 is not None and [px, py] == p2 and S.get('_line', 0) >= 11:
            fill = T['blue']
        if p1 is not None and [px, py] == p1:
            fill = T['orange']
        cv.d.ellipse((X - 20, Y - 20, X + 20, Y + 20), fill=fill, outline=T['border'], width=2)
        cv.text((X, Y), t, 20, T['bg'] if fill in (T['blue'], T['orange']) else T['text'], anchor='mm', bold=True)
        lab = f'({px},{py})'
        lw = cv.tlen(lab, 18, mono=True)
        cv.rect((X - lw / 2 - 4, Y + 23, X + lw / 2 + 4, Y + 45), fill=T['bg'], r=4, alpha=220)
        cv.text((X, Y + 34), lab, 18, T['muted'], anchor='mm', mono=True)
    # 右侧：分子分母比较
    rx = ox + size + 50
    if 'part1' in S and 'part2' in S and S.get('_line', 0) >= 15:
        cv.rich(rx, y0 + 52, f'`k = part1 / part2 = {S["part1"]} / {S["part2"]}`', x1 - rx - 10, size=26)
        cv.text((rx, y0 + 100), '只记分子分母（不做除法）', 22, T['muted'])
        key = S.get('key')
        if key is not None and S.get('_line') in (L_CMP, L_ADD):
            ok = S['part1'] * key[1] == S['part2'] * key[0]
            cv.rich(rx, y0 + 150, f'和键 `{key}` 比较：', x1 - rx - 10, size=24)
            cv.rich(rx, y0 + 196, f'`{S["part1"]}×{key[1]}` vs `{S["part2"]}×{key[0]}`', x1 - rx - 10, size=24)
            cv.rich(rx, y0 + 242, '→ ==斜率相同==' if ok else '→ 斜率不同', x1 - rx - 10, size=26)
    sp = S.get('same_point_cnt')
    if sp is not None:
        cv.rich(rx, y1 - 60, f'`same_point_cnt = {sp}`（重合点，含 point1 自己）', x1 - rx - 10, size=22)


CODE = '''
class Solution(object):
    def maxPoints(self, points):
        if len(points) < 3:
            return len(points)

        res = 0
        for index, point1 in enumerate(points):
            x1, y1 = point1
            param_dict = {}
            same_point_cnt = 1
            for point2 in points[index + 1:]:
                x2, y2 = point2

                part1 = y2 - y1
                part2 = x2 - x1

                if part1 == 0 and part2 == 0:
                    same_point_cnt += 1
                    continue


                flag = False
                for key in param_dict:
                    if part1 * key[1] == part2 * key[0]:
                        param_dict[key] += 1
                        flag = True
                        break

                if not flag:
                    param_dict[(part1, part2)] = 1

            if param_dict:
                same_line_cnt = max(param_dict.values())
            else:
                same_line_cnt = 0

            res = max(res, same_line_cnt + same_point_cnt)

        return res
'''
_LINES = CODE.strip('\n').split('\n')


def _ln(sub):
    return [i + 1 for i, s in enumerate(_LINES) if sub in s][0]


L_CMP = _ln('if part1 * key[1] == part2 * key[0]')
L_ADD = _ln('param_dict[key] += 1')


_it = {'n': 0}


def _reset(S, B, ret):
    _it['n'] = 0
    if S.part1 == 0 and S.part2 == 0:
        return '两点重合 → 不参与斜率比较'
    return f'`({S.part1}, {S.part2})` 不是重合点 → 去和已有的斜率逐个比较'


def _for_key(S, B, ret):
    _it['n'] += 1
    keys = list(S.param_dict)
    n = _it['n']
    if not keys:
        return '`param_dict` 还是空的，没有可比较的键'
    if n <= len(keys):
        return f'取出第 {n} 个已有的键 `{keys[n - 1]}`'
    return '已有的键都比较完了，没有斜率相同的'


def _cmp(S, B, ret):
    k = S.key
    if S.part1 * k[1] == S.part2 * k[0]:
        return f'`{S.part1}×{k[1]} = {S.part2}×{k[0]}`：交叉相乘相等 → 和键 `{k}` ==斜率相同=='
    return f'`{S.part1}×{k[1]} ≠ {S.part2}×{k[0]}`：和键 `{k}` 斜率不同，继续比下一个键'


CONFIG = dict(
    num=149, title='直线上最多的点数', difficulty='Hard', category='数学',
    author='yiduobo', technique='点斜式 · 分子分母交叉相乘判斜率',
    tags=['面试经典150'],
    code=CODE,
    call=f'Solution().maxPoints({PTS})',
    expect=3,
    skip=['x1, y1 = point1', 'x2, y2 = point2', 'for point2 in', 'flag = False', 'flag = True', 'break',
          'param_dict = {}', 'same_point_cnt = 1', 'if param_dict:'],
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='map', var='param_dict', label='param_dict：(分子 dy, 分母 dx) → 点数（不含 point1）', h=110,
             fmt=lambda k, v: f'{k}: {v}'),
    ],
    watch=[('index', 'index', 'orange'), ('point2', 'point2', 'blue'), 'part1', 'part2', ('res', 'res', 'green')],
    captions={
        'if len(points) < 3': '`{len(points)}` 个点：少于 3 个点时一定共线，直接返回点数',
        'res = 0': '`res` 记录答案',
        'for index, point1 in enumerate(points)': lambda S, B, ret: (
            f'选基准点 `point1 = {S.point1}`，过它的直线写成==点斜式== `y − {S.point1[1]} = k(x − {S.point1[0]})`'
            + ('；`param_dict` 清空，`same_point_cnt = 1`（含自己）' if S.index == 0 else '')
            if S.get('index') != B.get('index') else '所有基准点枚举完毕'),
        'part1 = y2 - y1': '`point2 = {point2}`：分子 `part1 = {y2} − {y1} = {part1}`',
        'part2 = x2 - x1': lambda S, B, ret: (f'分母 `part2 = {S.x2} − {S.x1} = {S.part2}`'
                                              + ('：==竖直线==，除法会出错，但分子分母照样能存' if S.part2 == 0 else '')),
        'if part1 == 0 and part2 == 0': _reset,
        'for key in param_dict': _for_key,
        L_CMP: _cmp,
        L_ADD: '找到同一条直线：`param_dict[{key}]` → {param_dict[key]}',
        'if not flag': lambda S, B, ret: ('没有找到斜率相同的键 → 新开一个键' if not S.flag else '已经计数过了，不用新开键'),
        'param_dict[(part1, part2)] = 1': '新键 `({part1}, {part2})` 记 1 个点',
        'same_line_cnt = max': '内层结束：最多的那种斜率有 `same_line_cnt = {same_line_cnt}` 个点',
        'same_line_cnt = 0': '`param_dict` 为空（后面没有点了）→ `same_line_cnt = 0`',
        'res = max': '`res = max({B.res}, {same_line_cnt} + {same_point_cnt})` = =={res}==',
        'return res': '返回 =={ret}==',
    },
    max_steps=75,
    cards=dict(
        one_liner='点斜式：固定基准点，用 (分子, 分母) 记斜率，交叉相乘判断是否相同',
        complexity='时间 `O(n³)`（键的线性比较），空间 `O(n)`',
        problem=['`points[i] = [x, y]` 是平面上的点，求最多有多少个点在同一条直线上',
                 '示例：`[[1,1],[2,2],[3,3]]` → `3`',
                 '本视频：`[[1,1],[2,2],[3,3],[3,1]]` → `3`'],
        quote='计算k的时候需要用到除法，可能会出现损失精度的情况。我在这里的处理办法是==直接记录下分子与分母==。这样做还有一个好处就是对于垂直的直线k也是没有意义的，而用分子分母的方式也可以将其记录下来。',
        quote_src='—— yiduobo 题解',
        idea=['点斜式：过基准点 p 的直线 `y − py = k(x − px)`，k 相同就在同一条直线上',
              '键存 `(dy, dx)`；判断 `dy1/dx1 = dy2/dx2` 用交叉相乘 `dy1·dx2 == dx1·dy2`',
              '重合点的 k 没有意义，单独用 `same_point_cnt` 统计'],
        result='过 `(1,1)` 的斜率 1 上还有 2 个点，加上它自己 → `3` ✓',
        summary=['未约分的键 `(1,1)` 和 `(2,2)` 是同一斜率，所以只能逐个键交叉相乘比较',
                 '这使最坏时间变成 `O(n³)`；把 `(dy, dx)` 用 gcd 约分后当键，可以 O(1) 查哈希表',
                 '`same_point_cnt` 处理旧版题目的重复点；现在题目保证点互不相同',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改',
                 '对比灵神：灵神直接用浮点斜率作键（数据范围小，精度够用）'],
    ),
)
