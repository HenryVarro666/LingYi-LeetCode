PTS = [[1, 1], [1, 2], [3, 2], [3, 3]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pts = PTS
    j = S.get('j')
    mx = max(max(p) for p in pts) + 1
    side = min(x1 - x0 - 120, y1 - y0 - 90)
    ox, oy = x0 + 70, y1 - 50          # 原点（左下）
    k = side / mx
    cv.text((x0 + 18, y0 + 4), '平面上的点（j=1 时横纵坐标互换：x 取 p[1]，y 取 p[0]）', 22, T['muted'], bold=True)
    cv.line([(ox, oy), (ox + mx * k, oy)], T['border'], 2)
    cv.line([(ox, oy), (ox, oy - mx * k)], T['border'], 2)
    for t in range(1, mx):
        cv.text((ox + t * k, oy + 8), t, 18, T['dim'], anchor='mt', mono=True)
        cv.text((ox - 10, oy - t * k), t, 18, T['dim'], anchor='rm', mono=True)

    def P(a, b):   # (x, y) 在 j 视角下 -> 屏幕坐标；j=1 时 x 对应真实 y 轴
        return (ox + a * k, oy - b * k) if not j else (ox + b * k, oy - a * k)

    x = S.get('x')
    # 当前列（x 固定）高亮
    if x is not None and 'min_x' in S and S.get('_line', 0) >= 19:
        a, b = P(x, 0), P(x, mx - 0.3)
        cv.line([a, b], T['yellow'], 3)
    if 'min_x' in S and S['min_x'] != float('inf') and S['max_x'] > 0:
        for v, c in ((S['min_x'], T['cyan']), (S['max_x'], T['orange'])):
            cv.dashed(P(v, 0), P(v, mx - 0.3), c, 3)
    cur = (S.get('p') or [None, None])
    for p in pts:
        X, Y = ox + p[0] * k, oy - p[1] * k
        hot = (j is not None and S.get('_line', 0) < 19 and p == S.get('p'))
        cv.rect((X - 14, Y - 14, X + 14, Y + 14), fill=T['pink'] if hot else T['blue'], r=14)
    if 'max_y' in S and 'min_y' in S and S.get('x') is not None and S['x'] in S['max_y'] and S['x'] in S['min_y'] and S.get('_line', 0) >= 19:
        a, b = P(S['x'], S['min_y'][S['x']]), P(S['x'], S['max_y'][S['x']])
        cv.line([a, b], T['green'], 6)


def _top(S):
    if 'j' not in S:
        return '边平行坐标轴：先看==竖直边==（j=0），再互换横纵坐标看==水平边==（j=1）'
    return f"`j = {S['j']}`：" + ('底边竖直（同一个 x，不同的 y）' if S['j'] == 0 else '底边水平（横纵坐标互换，当作同一个 x）')


CONFIG = dict(
    num=3588, title='找到最大三角形面积', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举底边 · 哈希表记录 minY/maxY',
    tags=[],
    code='''
# 手写 min max 更快
min = lambda a, b: b if b < a else a
max = lambda a, b: b if b > a else a

class Solution:
    def maxArea(self, coords: List[List[int]]) -> int:
        def calc(j: int) -> int:
            min_x, max_x = inf, 0
            min_y = defaultdict(lambda: inf)
            max_y = defaultdict(int)
            for p in coords:
                x, y = p[j], p[1 - j]
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y[x] = min(min_y[x], y)
                max_y[x] = max(max_y[x], y)

            res = 0
            for x, y in min_y.items():
                res = max(res, (max_y[x] - y) * max(max_x - x, x - min_x))
            return res

        return max(calc(0), calc(1)) or -1
''',
    call='Solution().maxArea(%r)' % PTS,
    expect=2,
    skip=['min = lambda', 'max = lambda', 'defaultdict(lambda', 'x, y = p[j]'],
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='custom', draw=_draw, h=330),
        dict(type='map', var='min_y', label='min_y[x]：横坐标 x 上最低的点', fmt=lambda k, v: f'{k}: {v}', h=118, font=26),
        dict(type='map', var='max_y', label='max_y[x]：横坐标 x 上最高的点', fmt=lambda k, v: f'{k}: {v}', h=118, font=26),
        dict(type='text', size=26, h=80, fn=lambda S: (
            f"`res = (max_y[x] − min_y[x]) × max(max_x − x, x − min_x)` 当前 res = =={S['res']}==" if 'res' in S else '')),
    ],
    watch=[('j', 'j', 'blue'), ('x', 'x', 'pink'), ('y', 'y'), ('min_x', 'min_x', 'cyan'), ('max_x', 'max_x', 'orange'), ('res', 'res', 'green')],
    captions={
        'min_x, max_x = inf, 0': '`min_x`、`max_x`：所有点横坐标的最小、最大值，==高==要从它们里选',
        'for p in coords': lambda S, B, r: (f'取点 `p = {S.p}`' if S.get('p') != B.get('p') or 'p' not in B else '所有点扫完了'),
        'x, y = p[j], p[1 - j]': '`j = {j}`：`x = p[{j}] = {x}`，`y = p[{1 - j}] = {y}`',
        'min_x = min(min_x, x)': '更新最小横坐标：`min_x = {min_x}`',
        'max_x = max(max_x, x)': '更新最大横坐标：`max_x = {max_x}`',
        'min_y[x] = min': '横坐标 `{x}` 上最低的点：`min_y[{x}] = {min_y[x]}`',
        'max_y[x] = max': '横坐标 `{x}` 上最高的点：`max_y[{x}] = {max_y[x]}`（底边 = 最高 − 最低）',
        'max_y = defaultdict': '两张哈希表：`min_y[x]`、`max_y[x]` 记录每个横坐标上最低、最高的点（默认值 inf / 0）',
        'res = 0': '`res` 记录底边在竖直方向时，面积乘二的最大值',
        'for x, y in min_y.items()': lambda S, B, r: ('枚举结束' if S.x == B.get('x') and S.y == B.get('y')
                                                      else f'枚举底边所在的横坐标 `x = {S.x}`：`min_y = {S.y}`，`max_y = {S.max_y[S.x]}`'),
        'res = max(res': lambda S, B, r: (f"底边 `{S.max_y[S.x]} − {S.y} = {S.max_y[S.x] - S.y}`，高 `max({S.max_x} − {S.x}, {S.x} − {S.min_x}) = {max(S.max_x - S.x, S.x - S.min_x)}`"
                                          f" → 面积×2 = {(S.max_y[S.x] - S.y) * max(S.max_x - S.x, S.x - S.min_x)}，`res = {S.res}`"),
        'return res': '`j = {j}` 这个方向最大面积的两倍 = =={res}==',
        'return max(calc(0)': lambda S, B, r: ('先算 `calc(0)`（竖直底边），再算 `calc(1)`（水平底边）' if r is None
                                              else f'两个方向取较大者；若为 0（没有合法三角形）则返回 -1 → =={r}=='),
    },
    max_steps=90,
    cards=dict(
        one_liner='枚举底边的 x：底边取最高最低点，高取离两端更远的一侧',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给 `n` 个点，选三个点组成三角形，要求至少有一条边平行于 x 轴或 y 轴',
                 '返回最大面积的==两倍==，没有合法三角形返回 `-1`',
                 '示例：`[[1,1],[1,2],[3,2],[3,3]]` → `2`（底 1，高 2）'],
        quote='假设底边横坐标 x=1，为了最大化三角形面积，我们需要最大化三角形的底边长，以及三角形的高，二者相乘，就是三角形面积乘二的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['底边与 y 轴平行：同一个 `x` 上选最高点和最低点，底 = `max_y[x] − min_y[x]`',
              '高 = 第三个点到这条竖线的距离，取全局 `min_x`/`max_x` 里更远的 → `max(x − min_x, max_x − x)`',
              '底边与 x 轴平行：把每个点的横纵坐标互换，复用同一段逻辑'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`max_x` 初值取 0 没问题（坐标 ≥ 1）；面积不能为 0，所以最后 `or -1`',
                 '写法二用参数 `j` 切换 `x = p[j], y = p[1-j]`，不修改输入；写法一直接交换坐标再调用一次 `calc`',
                 '手写 `min`/`max` 的 lambda 比内置函数更快，视频里不单独演示这两行',
                 '思考题：任选三点的最大三角形面积 → 凸包 + 旋转卡壳'],
    ),
)
