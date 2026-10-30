import math as _m
R0, CX, CY = 2.0, 1.0, 1.0


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '圆（半径 2，圆心 (1, 1)）（画成以圆心为原点）：虚线 = 半径 r，黄点 = 生成的点', 21, T['muted'], bold=True)
    side = min(x1 - x0 - 40, y1 - y0 - 60)
    sc = side / (2 * R0 * 1.12)
    cx, cy = (x0 + x1) / 2, y0 + 40 + side / 2
    n = 90
    cv.line([(cx + R0 * sc * _m.cos(2 * _m.pi * k / n), cy - R0 * sc * _m.sin(2 * _m.pi * k / n)) for k in range(n + 1)], T['blue'], 4)
    cv.line([(cx - R0 * sc * 1.08, cy), (cx + R0 * sc * 1.08, cy)], T['border'], 1)
    cv.line([(cx, cy - R0 * sc * 1.08), (cx, cy + R0 * sc * 1.08)], T['border'], 1)
    cv.text((cx + 8, cy + 6), '圆心', 18, T['dim'], anchor='lt')
    for p in (S.get('pts') or []):
        px, py = cx + (p[0] - CX) * sc, cy - (p[1] - CY) * sc
        cv.rect((px - 8, py - 8, px + 8, py + 8), fill=T['muted'], r=8)
    li = S.get('_inner') or {}
    if 'r' in li and 'theta' in li:
        r, th = li['r'], li['theta']
        px, py = cx + r * _m.cos(th) * sc, cy - r * _m.sin(th) * sc
        cv.dashed((cx, cy), (px, py), T['pink'], 3)
        cv.rect((px - 11, py - 11, px + 11, py + 11), fill=T['yellow'], r=11)
        cv.text((px + 16, py - 16), f'r={r:.2f}, θ={_m.degrees(th):.0f}°', 20, T['yellow'], anchor='lb', bold=True)
    elif 'r' in li:
        cv.dashed((cx, cy), (cx + li['r'] * sc, cy), T['pink'], 3)
        cv.text((cx + li['r'] * sc / 2, cy - 8), f"r={li['r']:.2f}", 20, T['pink'], anchor='mb', bold=True)


CONFIG = dict(
    num=478, title='在圆内随机生成点', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='极坐标 + 开方修正半径',
    tags=['随机化'],
    code='''
import math
import random

class Solution(object):

    def __init__(self, radius, x_center, y_center):
        self.radius = radius
        self.x_center = x_center
        self.y_center = y_center

    def randPoint(self):
        r = self.radius * math.sqrt(random.random())
        theta = 2 * math.pi * random.random()
        return [r * math.cos(theta) + self.x_center, r * math.sin(theta) + self.y_center]
''',
    setup='import random\nrandom.seed(1)',
    call='''s = Solution(2.0, 1.0, 1.0)
pts = []
pts.append(s.randPoint())
pts.append(s.randPoint())
pts.append(s.randPoint())
[[round(v, 3) for v in p] for p in pts]''',
    expect=[[1.421, 0.4], [0.944, 2.747], [-0.337, 1.439]],
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', h=70, size=28, fn=lambda S: ('`r = R × sqrt(随机数)`：面积与 r^2 成正比，所以要开方' if 'theta' not in (S.get('_inner') or {}) else '角度均匀随机，再转回直角坐标：`x = r·cosθ + 圆心x`')),
        dict(type='calls', label='正在执行', h=90),
    ],
    watch=['r', 'theta'],
    skip=['import math', 'import random'],
    captions={
        'self.radius = radius': '记下半径 `{radius}`',
        'self.x_center = x_center': '记下圆心 `({x_center}, {y_center})`',
        'self.y_center = y_center': '圆心记好了，后面生成的点要平移到这个圆心',
        'r = self.radius * math.sqrt(random.random())': '半径不能直接均匀取：外圈周长大、点更多。取 `R × sqrt(U)`，`r = {r:.3f}`',
        'theta = 2 * math.pi * random.random()': '角度各方向等概率，`θ = 2π × 随机数` = `{theta:.3f}` 弧度',
        'return [r * math.cos': lambda S, B, ret: '极坐标转直角坐标并平移：点 = (`{:.3f}`, `{:.3f}`)'.format(ret[0], ret[1]),
    },
    max_steps=60,
    cards=dict(
        one_liner='不用拒绝采样：极坐标，半径取 R·sqrt(随机数)',
        complexity='每次 `randPoint` 时间 `O(1)`，空间 `O(1)`',
        problem=['给定圆的半径和圆心 `(x_center, y_center)`',
                 '`randPoint()` 在圆内==均匀==随机返回一个点 `[x, y]`',
                 '示例：半径 2，圆心 (1, 1)'],
        quote='对于r，则相对复杂一些。……就可以得到累积分布函数F(p\') = r\'^2/r^2，于是就有r\' = r * sqrt(F(p\'))。',
        quote_src='—— yiduobo 题解',
        idea=['第一反应是拒绝采样：在正方形里随机，落在圆外就重来',
              '极坐标：角度 `θ` 等概率，`θ = 2π × 随机数`',
              '半径 `r` 不能均匀：半径 r\' 的圆环周长 ∝ r\'，概率密度 `2r\'/r^2`，积分得 `r\' = r × sqrt(U)`'],
        summary=['`O(1)` 时间，无需重试；拒绝采样期望重试 `4/π` 次',
                 '易错：半径直接用 `R × 随机数` 会让点挤在圆心附近',
                 '易错：最后要加上圆心坐标做平移',
                 '原文写 `sqrt` 但只 import 了 math，已改为 `math.sqrt`',
                 '同类随机题：381、497、710'],
    ),
)
