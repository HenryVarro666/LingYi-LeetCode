import math as _m


def _geo(sides):
    a, b, c = sides
    x = (a * a + c * c - b * b) / (2 * a)
    y2 = c * c - x * x
    return a, b, c, x, (_m.sqrt(y2) if y2 > 0 else 0.0)


def _ang(sides):
    a, b, c = sides
    cl = lambda v: max(-1.0, min(1.0, v))
    A = _m.degrees(_m.acos(cl((b * b + c * c - a * a) / (2 * b * c))))
    B = _m.degrees(_m.acos(cl((a * a + c * c - b * b) / (2 * a * c))))
    return A, B, 180 - A - B


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    sides = S.get('sides')
    if not sides or len(sides) != 3:
        return
    a, b, c, gx, gy = _geo(sides)
    cv.text((x0 + 18, y0 + 4), '三角形（边长按当前顺序，角 A 对边 a，B 对 b，C 对 c）', 22, T['muted'], bold=True)
    if gy <= 0:
        cv.text(((x0 + x1) / 2, (y0 + y1) / 2), '三点共线，面积为 0', 30, T['red'], anchor='mm', bold=True)
        return
    pad = 110
    sc = min((x1 - x0 - 2 * pad) / max(a, gx, a - gx, 1e-9), (y1 - y0 - 2 * pad) / gy)
    ox = x0 + (x1 - x0) / 2 - (a * sc) / 2
    oy = y1 - pad + 10
    Vb, Vc, Va = (ox, oy), (ox + a * sc, oy), (ox + gx * sc, oy - gy * sc)
    named = 'a' in S
    cv.line([Vb, Vc, Va, Vb], T['border'], 4)
    cv.line([Vb, Vc], T['blue'], 5)
    cv.line([Vc, Va], T['pink'], 5)
    cv.line([Va, Vb], T['green'], 5)
    pa = ((Vb[0] + Vc[0]) / 2, Vb[1] + 14)
    pb = ((Vc[0] + Va[0]) / 2 + 16, (Vc[1] + Va[1]) / 2)
    pc = ((Va[0] + Vb[0]) / 2 - 16, (Va[1] + Vb[1]) / 2)
    cv.text(pa, f'a = {a}' if named else a, 30, T['blue'], anchor='mt', bold=True)
    cv.text(pb, f'b = {b}' if named else b, 30, T['pink'], anchor='lm', bold=True)
    cv.text(pc, f'c = {c}' if named else c, 30, T['green'], anchor='rm', bold=True)
    A, Bd, C = _ang(sides)
    for name, V, col, val, show, dx, dy, anc in (
            ('A', Va, T['blue'], A, 'A' in S, 0, -14, 'mb'), ('B', Vb, T['pink'], Bd, 'B' in S, -14, 4, 'rm'),
            ('C', Vc, T['green'], C, 'B' in S, 14, 4, 'lm')):
        cv.rect((V[0] - 7, V[1] - 7, V[0] + 7, V[1] + 7), fill=col, r=7)
        cv.text((V[0] + dx, V[1] + dy), f'{name} = {val:.2f}°' if show else name, 28, col if show else T['muted'], anchor=anc, bold=True)


CONFIG = dict(
    num=3899, title='三角形的内角度数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='排序 + 余弦定理',
    tags=['计算几何', '难度分 1407'],
    code='''
class Solution:
    def internalAngles(self, sides: List[int]) -> List[float]:
        sides.sort()
        a, b, c = sides
        if a + b <= c:
            return []

        A = degrees(acos((b * b + c * c - a * a) / (b * c * 2)))
        B = degrees(acos((a * a + c * c - b * b) / (a * c * 2)))
        return [A, B, 180 - A - B]  # 小边对小角
''',
    setup='from math import degrees, acos',
    call='Solution().internalAngles([5, 3, 4])',
    expect=[36.86990, 53.13010, 90.0],
    result_fn=lambda r: [round(x, 5) for x in r],
    views=[
        dict(type='array', var='sides', label='sides', h=210, cell=80),
        dict(type='text', fn=lambda S: (f"余弦定理：`cos A = (b² + c² − a²) / 2bc` = =={(S['b']**2 + S['c']**2 - S['a']**2) / (2 * S['b'] * S['c']):.4f}==" if 'a' in S and S['a'] + S['b'] > S['c'] else '先排序，再用 `a + b > c` 判断能否成三角形'), size=26, h=70),
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=['a', 'b', 'c', ('A', 'A', 'blue'), ('B', 'B', 'pink')],
    captions={
        'sides.sort()': '先排序，保证 `a ≤ b ≤ c`：这样 `a + c > b` 和 `b + c > a` 必然成立，只剩一个条件要检查：`{sides}`',
        'a, b, c = sides': '最短边 `a = {a}`，次短 `b = {b}`，最长 `c = {c}`',
        'if a + b <= c': '较短两边之和 `{a} + {b} = {a + b}` {"≤" if a + b <= c else ">"} 最长边 `{c}` → {"==凑不成三角形==，返回空数组" if a + b <= c else "能构成面积为正的三角形"}',
        'A = degrees': '余弦定理：`cos A = (b² + c² − a²) / 2bc` = {(b*b + c*c - a*a) / (b*c*2):.4f}，`acos` 后转成度数：==A = {A:.2f}°==',
        'B = degrees': lambda S, B, r: f'同理 `cos B = (a² + c² − b²) / 2ac` = {(S.a*S.a + S.c*S.c - S.b*S.b) / (S.a*S.c*2):.4f}，==B = {S.B:.2f}°==',
        'return [A': '`C = 180 − A − B = {180 - A - B:.2f}°`，不用再算一次 acos。小边对小角，所以 `A ≤ B ≤ C` 已经有序，不必再排序',
    },
    cards=dict(
        one_liner='先排序判断三边，两个角用余弦定理，第三个角 180 减去',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给长度为 3 的正整数数组 `sides`，判断能否做三角形的三边（面积为正）',
                 '能：返回按 ==非递减== 排序的三个内角（单位：度）；不能：返回 `[]`',
                 '示例：`[3,4,5]` → `[36.87, 53.13, 90]`；`[2,4,2]` → `[]`'],
        quote='由于 a+c>b 和 b+c>a 一定成立，所以只需判断 a+b>c 是否成立。……由于「小边对小角」，所以 A≤B≤C。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后 `a ≤ b ≤ c`，三角形不等式只剩 ==a + b > c== 这一条',
              '余弦定理 `cos A = (b²+c²−a²) / 2bc`，`acos` 得弧度，`degrees` 转成度',
              '只算两个角，==C = 180 − A − B==；小边对小角，结果天然有序'],
        summary=['时间、空间都是 `O(1)`',
                 '判断条件是 `a + b <= c`（等于也不行，面积为 0）',
                 '`sides.sort()` 会原地改输入；本视频传入 `[5,3,4]` 来演示排序',
                 '用 `degrees(acos(...))`，别忘了弧度转角度；最后一个角用 180 减，省一次 acos'],
    ),
)
