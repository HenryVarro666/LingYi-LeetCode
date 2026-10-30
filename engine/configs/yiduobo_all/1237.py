SETUP = '''
class CustomFunction:
    def __init__(self, function_id):
        self.function_id = function_id
    def f(self, x, y):
        if self.function_id == 1:
            return x + y
        if self.function_id == 2:
            return x * y
        return x * x + y
'''


def _sq(v):
    return (max(v, 0) / 1000) ** 0.5


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '矩阵：横轴 x（行），纵轴 y（列）；每行只从上一行停下的 y 往下走（开方刻度）', 22, T['muted'], bold=True)
    side = min(x1 - x0 - 120, y1 - y0 - 150)
    ox, oy = x0 + 70 + (x1 - x0 - 120 - side) / 2, y0 + 90
    cv.rect((ox, oy, ox + side, oy + side), fill=T['panel2'], outline=T['border'], r=6)
    for v in (1, 25, 100, 400, 1000):
        cv.text((ox + _sq(v) * side, oy + side + 6), v, 18, T['dim'], anchor='mt', mono=True)
        cv.text((ox - 8, oy + side - _sq(v) * side), v, 18, T['dim'], anchor='rm', mono=True)
    cv.text((ox + side / 2, oy + side + 34), 'x', 22, T['muted'], anchor='mt', bold=True)
    cv.text((ox - 56, oy + side / 2), 'y', 22, T['muted'], anchor='mm', bold=True)
    if 'x' not in S or 'y' not in S:
        return
    x, y = S['x'], S['y']
    X = ox + _sq(x) * side
    Y = oy + side - _sq(y) * side
    if y >= 1:
        cv.rect((ox, oy, ox + side, Y), fill=T['red'], alpha=45)          # y 以上：已被排除
    cv.rect((ox, Y, X, oy + side), fill=T['red'], alpha=45) if y >= 1 else None  # x 以左：已处理的行
    if y >= 1:
        cv.line([(X, Y), (ox + side, Y)], T['pink'], 3)
    for a, b in S.get('res', []):
        px, py = ox + _sq(a) * side, oy + side - _sq(b) * side
        cv.rect((px - 8, py - 8, px + 8, py + 8), fill=T['yellow'], r=8)
    if y >= 1:
        cv.rect((X - 9, Y - 9, X + 9, Y + 9), fill=T['pink'], r=9)
        cv.text((X + 16, Y + 4), f'({x}, {y})', 22, T['pink'], anchor='lt', bold=True)


CONFIG = dict(
    num=1237, title='找出给定方程的正整数解', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='矩阵右下角出发 · y 只减不增',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def findSolution(self, customfunction, z):

        y = 1000
        res = []
        for x in range(1, 1001):
            while y > 0:
                v = customfunction.f(x, y)
                if v <= z:
                    break
                y -= 1
            if y == 0:
                break
            
            if v == z:
                res.append([x, y])
                y -= 1
        
        return res
''',
    setup=SETUP,
    call='Solution().findSolution(CustomFunction(3), 1001)',
    expect=[[x, 1001 - x * x] for x in range(1, 32)],
    max_events=30000,
    max_steps=64,
    views=[
        dict(type='text', fn=lambda S: (f"`f({S['x']}, {S['y']})` = =={S['v']}== 对比 z = 1001" if 'v' in S and 'x' in S and S['y'] >= 1 else ''), size=30),
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), 'v', ('res 个数', 'len(res)', 'green')],
    captions={
        'y = 1000': '`y` 从 1000 开始：矩阵的右下角 `(1, 1000)`',
        'res = []': '`res` 保存所有解',
        'for x in range': '处理第 `{x}` 行：`y` 不回头，接着上一行停下的位置往下走',
        'while y > 0': lambda S, B, r: (f'`y = {S.y} > 0`，这一行还要继续找' if S.y > 0 else '`y = 0`：这一行也没有可行位置，退出内层循环'),
        'v = customfunction.f': '`f({x}, {y}) = {v}`',
        'if v <= z': lambda S, B, r: (f'`{S.v} <= {S.z}` → 成立：到这里 `f` 不大于 z，停止缩小 y' if S.v <= S.z else f'`{S.v} <= {S.z}` → 不成立：`f(x, y)` 还是比 z 大'),
        10: '停下：`y = {y}`，这一行不会再往下了',
        'y -= 1': lambda S, B, r: (f'`f({S.x}, {B.y}) = {S.v} > z`：以它为左下角的矩阵全大于 z，`y` → {S.y}' if S.v > S.z else f'这个 `y` 已记入答案，下一行 `f` 更大，必须用更小的 y：`y` → {S.y}'),
        13: '`y == 0`：跳出外层 for，不再处理后面的行',
        'if y == 0': lambda S, B, r: ('`y == 0`：y 用光了，后面的行也不可能有解 → 结束' if S.y == 0 else f'`y = {S.y}` ≠ 0，继续'),
        'if v == z': lambda S, B, r: (f'`{S.v} == {S.z}` → 成立：找到一组解' if S.v == S.z else f'`{S.v} == {S.z}` → 不成立：`{S.v} < {S.z}`，这一行没有解'),
        'res.append': '记录答案 `[{x}, {y}]`，现在共 `{len(res)}` 组',
        'return res': '返回 `{len(res)}` 组解',
    },
    cards=dict(
        one_liner='把 f 看成矩阵：一行一行往上走，y 只减不增',
        complexity='时间 `O(C)`（C = 1000），空间 `O(1)`',
        problem=['`f(x, y)` 对 x、y 都严格递增，公式未知，只能调用',
                 '求所有 `f(x, y) == z` 的正整数对，x、y 都在 `1~1000`',
                 '本视频：`f = x*x + y`，`z = 1001` → `[1,1000]`、`[2,997]`、…、`[31,40]`'],
        quote='若我们现在知道了f[2, 2] > z，那么对于以位置(2, 2)为左下角，(3, 4)为右上角的矩阵来说，里面的每个元素都大于f[2, 2]。',
        quote_src='—— yiduobo 题解原文',
        idea=['把 f 排成 1000×1000 矩阵，两个方向都递增',
              '从右下角 `(1, 1000)` 出发：先缩小 y 直到 `f(x, y) <= z`',
              '相等就记录；换下一行 x 时，`y` 以上的部分已排除，从原位置接着走',
              '每个 x、y 最多走一遍，所以是线性的'],
        summary=['每个 x 与 y 至多各走 1000 次，时间 `O(C)`',
                 '找到解后要 `y -= 1`：下一行 `f(x+1, y) > z`，不能再用同一个 y',
                 '`if y == 0: break`：y 用完后，之后的行都不可能有解',
                 '原文已是 Python 3 可运行，只删去了开头的接口说明注释字符串',
                 '对比灵神：灵神每步只动 x 或 y 其一，yiduobo 按行把 y 缩到不大于 z'],
    ),
)
