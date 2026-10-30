PTS = [[1, 1], [1, 2], [3, 2], [3, 3]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    mx = max(max(p) for p in PTS) + 1
    side = min(x1 - x0 - 120, y1 - y0 - 90)
    ox, oy = x0 + 70, y1 - 50
    k = side / mx
    cv.text((x0 + 18, y0 + 4), '平面上的点（黄 = 当前点，青/橙虚线 = 最小/最大坐标）', 22, T['muted'], bold=True)
    cv.line([(ox, oy), (ox + mx * k, oy)], T['border'], 2)
    cv.line([(ox, oy), (ox, oy - mx * k)], T['border'], 2)
    for t in range(1, mx):
        cv.text((ox + t * k, oy + 8), t, 18, T['dim'], anchor='mt', mono=True)
        cv.text((ox - 10, oy - t * k), t, 18, T['dim'], anchor='rm', mono=True)
    line = S.get('_line', 0)
    seen = []
    if 'x' in S and 'y' in S and line <= 30:
        pos = [i for i, p in enumerate(PTS) if p == [S['x'], S['y']]]
        seen = PTS[:pos[0] + 1] if pos else []
    if S.get('max_x') is not None and S.get('min_x') is not None:
        for v, c in ((S['min_x'], T['cyan']), (S['max_x'], T['orange'])):
            cv.dashed((ox + v * k, oy), (ox + v * k, oy - (mx - 0.3) * k), c, 3)
    if S.get('max_y') is not None and S.get('min_y') is not None:
        for v, c in ((S['min_y'], T['cyan']), (S['max_y'], T['orange'])):
            cv.dashed((ox, oy - v * k), (ox + (mx - 0.3) * k, oy - v * k), c, 3)
    # 第一段：已知每列的最高最低点连线
    if 33 <= line <= 34 and 'x' in S and S['x'] in S['max_in_col']:
        x = S['x']
        cv.line([(ox + x * k, oy - S['min_in_col'][x] * k), (ox + x * k, oy - S['max_in_col'][x] * k)], T['green'], 6)
    if line >= 35 and 'y' in S and S['y'] in S['max_in_row']:
        y = S['y']
        cv.line([(ox + S['min_in_row'][y] * k, oy - y * k), (ox + S['max_in_row'][y] * k, oy - y * k)], T['green'], 6)
    for p in PTS:
        X, Y = ox + p[0] * k, oy - p[1] * k
        hot = line <= 30 and 'x' in S and p == [S['x'], S['y']]
        cv.rect((X - 14, Y - 14, X + 14, Y + 14), fill=T['yellow'] if hot else T['blue'], r=14)


CONFIG = dict(
    num=3588, title='找到最大三角形面积', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表 · 每行每列的最远两点',
    tags=[],
    code='''
class Solution(object):
    def maxArea(self, coords):
        
        max_x = None
        min_x = None
        max_y = None
        min_y = None

        max_in_row = {}
        min_in_row = {}
        max_in_col = {}
        min_in_col = {}

        for x, y in coords:
            if max_x is None or x > max_x:
                max_x = x
            if min_x is None or x < min_x:
                min_x = x
            if max_y is None or y > max_y:
                max_y = y
            if min_y is None or y < min_y:
                min_y = y
            if x not in max_in_col or max_in_col[x] < y:
                max_in_col[x] = y
            if x not in min_in_col or min_in_col[x] > y:
                min_in_col[x] = y
            if y not in max_in_row or max_in_row[y] < x:
                max_in_row[y] = x
            if y not in min_in_row or min_in_row[y] > x:
                min_in_row[y] = x
        
        res = 0
        for x in max_in_col:
            res = max(res, (max_in_col[x] - min_in_col[x]) * max((max_x - x), (x - min_x)))
        for y in max_in_row:
            res = max(res, (max_in_row[y] - min_in_row[y]) * max((max_y - y), (y - min_y)))
        if res == 0:
            res = -1
        return res
''',
    call='Solution().maxArea(%r)' % PTS,
    expect=2,
    skip=['min_x = None', 'max_y = None', 'min_y = None', 'min_in_row = {}', 'max_in_col = {}', 'min_in_col = {}'],
    views=[
        dict(type='text', size=26, h=90, fn=lambda S: (
            f"当前点 `({S['x']}, {S['y']})`　x 范围 `{S['min_x']}~{S['max_x']}`，y 范围 `{S['min_y']}~{S['max_y']}`" if 'x' in S and S.get('min_x') is not None and S.get('min_y') is not None
            else '遍历所有点，记下每列/每行最远的两个点，以及全局的坐标范围')),
        dict(type='custom', draw=_draw, h=340),
        dict(type='map', label='每一列（同 x）：最低 y ~ 最高 y　（min_in_col / max_in_col）', h=130, font=26,
             var=lambda S: {k: (S['min_in_col'].get(k, '?'), v) for k, v in S['max_in_col'].items()} if S.get('max_in_col') is not None and S.get('min_in_col') is not None else None,
             fmt=lambda k, v: f'x={k}: y {v[0]}~{v[1]}'),
        dict(type='map', label='每一行（同 y）：最左 x ~ 最右 x　（min_in_row / max_in_row）', h=130, font=26,
             var=lambda S: {k: (S['min_in_row'].get(k, '?'), v) for k, v in S['max_in_row'].items()} if S.get('max_in_row') is not None and S.get('min_in_row') is not None else None,
             fmt=lambda k, v: f'y={k}: x {v[0]}~{v[1]}'),
    ],
    watch=[('x', 'x', 'pink'), ('y', 'y', 'blue'), ('min_x', 'min_x', 'cyan'), ('max_x', 'max_x', 'orange'), ('min_y', 'min_y', 'cyan'), ('max_y', 'max_y', 'orange'), ('res', 'res', 'green')],
    captions={
        'max_x = None': '`max_x/min_x/max_y/min_y`：所有点横、纵坐标的范围，用来求“高”',
        'max_in_row = {}': '四张哈希表：每一==列==（同 x）最低/最高的 y，每一==行==（同 y）最左/最右的 x，用来求“底”',
        'for x, y in coords': lambda S, B, r: (f'取点 `({S.x}, {S.y})`' if S.get('x') != B.get('x') or S.get('y') != B.get('y') or 'x' not in B else '所有点都统计完了'),
        'if max_x is None': lambda S, B, r: (f'`x = {S.x}` 比当前 `max_x = {S.max_x}` 大（或还没有）→ ==更新=='
                                              if S.max_x is None or S.x > S.max_x else f'`x = {S.x}` 没超过 `max_x = {S.max_x}`，不更新'),
        'if min_x is None': lambda S, B, r: (f'`x = {S.x}` 比当前 `min_x = {S.min_x}` 小（或还没有）→ ==更新=='
                                              if S.min_x is None or S.x < S.min_x else f'`x = {S.x}` 没小于 `min_x = {S.min_x}`，不更新'),
        'if max_y is None': lambda S, B, r: (f'`y = {S.y}` 比当前 `max_y = {S.max_y}` 大（或还没有）→ ==更新=='
                                              if S.max_y is None or S.y > S.max_y else f'`y = {S.y}` 没超过 `max_y = {S.max_y}`，不更新'),
        'if min_y is None': lambda S, B, r: (f'`y = {S.y}` 比当前 `min_y = {S.min_y}` 小（或还没有）→ ==更新=='
                                              if S.min_y is None or S.y < S.min_y else f'`y = {S.y}` 没小于 `min_y = {S.min_y}`，不更新'),
        'max_x = x': '`max_x` → {max_x}',
        'min_x = x': '`min_x` → {min_x}',
        'max_y = y': '`max_y` → {max_y}',
        'min_y = y': '`min_y` → {min_y}',
        'if x not in max_in_col': lambda S, B, r: ('第 `{}` 列还没有记录，或这个点更高 → ==更新这列的最高点==' if S.x not in B.max_in_col or B.max_in_col[S.x] < S.y else '这一列已有更高的点，不更新').format(S.x),
        'if x not in min_in_col': lambda S, B, r: ('第 `{}` 列还没有记录，或这个点更低 → ==更新这列的最低点==' if S.x not in B.min_in_col or B.min_in_col[S.x] > S.y else '这一列已有更低的点，不更新').format(S.x),
        'if y not in max_in_row': lambda S, B, r: ('第 `{}` 行还没有记录，或这个点更靠右 → ==更新这行的最右点==' if S.y not in B.max_in_row or B.max_in_row[S.y] < S.x else '这一行已有更靠右的点，不更新').format(S.y),
        'if y not in min_in_row': lambda S, B, r: ('第 `{}` 行还没有记录，或这个点更靠左 → ==更新这行的最左点==' if S.y not in B.min_in_row or B.min_in_row[S.y] > S.x else '这一行已有更靠左的点，不更新').format(S.y),
        'max_in_col[x] = y': '`max_in_col[{x}] = {max_in_col[x]}`',
        'min_in_col[x] = y': '`min_in_col[{x}] = {min_in_col[x]}`',
        'max_in_row[y] = x': '`max_in_row[{y}] = {max_in_row[y]}`',
        'min_in_row[y] = x': '`min_in_row[{y}] = {min_in_row[y]}`',
        'res = 0': '`res` 记录最大的“底 × 高”（即面积的两倍）',
        'for x in max_in_col': lambda S, B, r: ('竖直方向的底枚举完了' if S.x == B.get('x') else f'枚举底边所在的列 `x = {S.x}`'),
        'res = max(res, (max_in_col': lambda S, B, r: (f"底 `{S.max_in_col[S.x]} − {S.min_in_col[S.x]} = {S.max_in_col[S.x] - S.min_in_col[S.x]}`，高 `max({S.max_x} − {S.x}, {S.x} − {S.min_x}) = {max(S.max_x - S.x, S.x - S.min_x)}`"
                                                        f" → `res = {S.res}`"),
        'for y in max_in_row': lambda S, B, r: ('水平方向的底枚举完了' if S.y == B.get('y') else f'枚举底边所在的行 `y = {S.y}`'),
        'res = max(res, (max_in_row': lambda S, B, r: (f"底 `{S.max_in_row[S.y]} − {S.min_in_row[S.y]} = {S.max_in_row[S.y] - S.min_in_row[S.y]}`，高 `max({S.max_y} − {S.y}, {S.y} − {S.min_y}) = {max(S.max_y - S.y, S.y - S.min_y)}`"
                                                        f" → `res = {S.res}`"),
        'if res == 0': lambda S, B, r: ('`res == 0`：面积不能为 0，没有合法三角形 → 改成 -1' if S.res == 0 else f'`res = {S.res}` 不为 0，存在合法三角形'),
        'return res': '最大三角形面积的两倍 = =={res}==',
    },
    max_steps=120,
    cards=dict(
        one_liner='底在同一行或同一列，取最远两点；高取离两端更远的一侧',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给 `n` 个点，选三个点组成三角形，至少一条边平行于 x 轴或 y 轴',
                 '返回最大面积的==两倍==，不存在合法三角形返回 `-1`',
                 '示例：`[[1,1],[1,2],[3,2],[3,3]]` → `2`'],
        quote='为了使得面积尽量大，就应该让底和高都尽量大。……应该取横坐标为x的点中，纵坐标最小和最大的点对。而对于高的计算，则只取决于第三个点与x之差，因此只需取所有点中横坐标最小和最大的点。',
        quote_src='—— yiduobo 题解原文',
        idea=['三角形有两点横坐标相同（竖直底），第三个点横坐标必须不同',
              '底：这一列 `y` 最小和最大的两点；高：离这一列最远的 `min_x` 或 `max_x`',
              '横纵坐标对称：同时统计“列”和“行”，两个方向分别算一遍',
              '一次遍历建好四张哈希表，再各枚举一遍，最后乘二'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：底为 0（这一列只有一个点）时面积为 0，不算三角形；最后 `res == 0` 要改成 `-1`',
                 '`max_x` 等初值用 `None`，是为了第一个点也走统一的比较逻辑',
                 '对比灵神：灵神把“交换横纵坐标”写成一个函数调用两次；yiduobo 直接同时维护行、列两套哈希表'],
    ),
)
