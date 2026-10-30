SETUP = '''
class CustomFunction:
    def __init__(self, function_id):
        self.function_id = function_id
    def f(self, x, y):
        if self.function_id == 1:
            return x + y
        return x * y
'''


def _sq(v):
    return (v / 1000) ** 0.5


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '搜索范围：横坐标 [x, 1000]、纵坐标 [1, y]（坐标轴用开方刻度，方便看清小数）', 22, T['muted'], bold=True)
    side = min(x1 - x0 - 120, y1 - y0 - 150)
    ox, oy = x0 + 70 + (x1 - x0 - 120 - side) / 2, y0 + 90
    cv.rect((ox, oy, ox + side, oy + side), fill=T['panel2'], outline=T['border'], r=6)
    if 'x' not in S or 'y' not in S:
        return
    x, y = S['x'], S['y']
    xl = ox + _sq(min(x, 1000)) * side
    yt = oy + side - _sq(max(y, 0)) * side
    if x <= 1000 and y >= 1:
        cv.rect((xl, yt, ox + side, oy + side), fill=T['blue'], alpha=70)
    for v in (1, 25, 100, 400, 1000):
        cv.text((ox + _sq(v) * side, oy + side + 6), v, 18, T['dim'], anchor='mt', mono=True)
        cv.text((ox - 8, oy + side - _sq(v) * side), v, 18, T['dim'], anchor='rm', mono=True)
    cv.text((ox + side / 2, oy + side + 34), 'x', 22, T['muted'], anchor='mt', bold=True)
    cv.text((ox - 56, oy + side / 2), 'y', 22, T['muted'], anchor='mm', bold=True)
    for a, b in S.get('ans', []):
        px, py = ox + _sq(a) * side, oy + side - _sq(b) * side
        cv.rect((px - 8, py - 8, px + 8, py + 8), fill=T['yellow'], r=8)
    if x <= 1000 and y >= 1:
        px, py = ox + _sq(x) * side, oy + side - _sq(y) * side
        cv.rect((px - 9, py - 9, px + 9, py + 9), fill=T['pink'], r=9)
        cv.text((px + 16, py + 4), f'({x}, {y})', 22, T['pink'], anchor="lt", bold=True)


CONFIG = dict(
    num=1237, title='找出给定方程的正整数解', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='相向双指针（从右上角出发）',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution:
    def findSolution(self, customfunction: 'CustomFunction', z: int) -> List[List[int]]:
        ans = []
        x, y = 1, 1000
        while x <= 1000 and y:
            res = customfunction.f(x, y)
            if res < z:
                x += 1
            elif res > z:
                y -= 1
            else:
                ans.append([x, y])
                x += 1
                y -= 1
        return ans
''',
    setup=SETUP,
    call='Solution().findSolution(CustomFunction(2), 1000)',
    expect=[[1, 1000], [2, 500], [4, 250], [5, 200], [8, 125], [10, 100], [20, 50], [25, 40], [40, 25], [50, 20], [100, 10], [125, 8], [200, 5], [250, 4], [500, 2], [1000, 1]],
    max_events=30000,
    max_steps=64,
    views=[
        dict(type='text', fn=lambda S: (f"`f({S['x']}, {S['y']})` = =={S['res']}== 对比 z = 1000" if 'res' in S and S['x'] <= 1000 and S['y'] >= 1 else ''), size=30),
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), 'res', ('ans', 'ans', 'green')],
    captions={
        'x, y = 1, 1000': '从右上角出发：`x = 1`，`y = 1000`，搜索范围是整个 [1,1000]×[1,1000]',
        'while x <= 1000': lambda S, B, r: ('范围还不为空，继续' if S.x <= 1000 and S.y else '`x > 1000` 或 `y = 0`：搜索范围为空 → 结束'),
        'res = customfunction.f': '`f({x}, {y}) = {res}`，和 `z = {z}` 比较',
        'if res < z': lambda S, B, r: (f'`{S.res} < {S.z}` → 成立：任意 `y\' < {S.y}` 都有 `f(x,y\')` 更小，固定 x 找不到答案' if S.res < S.z else f'`{S.res} < {S.z}` → 不成立'),
        'elif res > z': lambda S, B, r: (f'`{S.res} > {S.z}` → 成立：任意 `x\' > {S.x}` 都有 `f(x\',y)` 更大，固定 y 找不到答案' if S.res > S.z else f'`{S.res} > {S.z}` → 不成立，只剩相等'),
        'x += 1': lambda S, B, r: (f'这一列（x = {B.x}）已排除，`x` → {S.x}，范围缩小' if S.res < S.z else f'`f(x+1,y) > f(x,y) = z`，所以 x 也右移：`x` → {S.x}'),
        'y -= 1': lambda S, B, r: (f'这一行（y = {B.y}）已排除，`y` → {S.y}，范围缩小' if S.res > S.z else f'`f(x,y-1) < z`，所以 y 也下移：`y` → {S.y}'),
        'ans.append': '`f({x}, {y}) == {z}`：记录答案 `[{x}, {y}]`',
        'return ans': '搜完了，一共 `{len(ans)}` 组解',
    },
    cards=dict(
        one_liner='f 单调递增：从右上角出发，每次排除一整行或一整列',
        complexity='时间 `O(C)`（C = 1000），空间 `O(1)`',
        problem=['`f(x, y)` 是未知的单调递增函数，关于 x、y 都严格递增',
                 '找出所有满足 `f(x, y) == z` 的正整数对 `(x, y)`',
                 '示例：`f = x × y`，`z = 1000` → 共 16 组，如 `[1,1000]`、`[2,500]`、…、`[1000,1]`'],
        quote='本题其实和 15. 三数之和 是类似的，都可以使用==相向双指针==解决。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f(x,y) < z`：这一列 y 以下都更小 → `x += 1`',
              '`f(x,y) > z`：这一行 x 以右都更大 → `y -= 1`',
              '`f(x,y) == z`：记录，且两边一起缩 → `x += 1, y -= 1`',
              '示例里 x、y 要走满 1000 格，视频中间做了快进，只看开头和结尾'],
        summary=['每次循环 x 增或 y 减至少一个，循环不超过 `2C` 次',
                 '循环条件是 `x <= 1000 and y`，y 到 0 即停',
                 '相等时 x、y 同时变，是因为 `f(x+1,y) > z`',
                 '同类题：167、15、16、18、611（相向双指针）'],
    ),
)
