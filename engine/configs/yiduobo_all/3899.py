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
            ('A', Va, T['blue'], A, 'cosC' in S, 0, -14, 'mb'), ('B', Vb, T['pink'], Bd, 'cosC' in S, -14, 4, 'rm'),
            ('C', Vc, T['green'], C, 'cosC' in S, 14, 4, 'lm')):
        cv.rect((V[0] - 7, V[1] - 7, V[0] + 7, V[1] + 7), fill=col, r=7)
        cv.text((V[0] + dx, V[1] + dy), f'{name} = {val:.2f}°' if show else name, 28, col if show else T['muted'], anchor=anc, bold=True)


CONFIG = dict(
    num=3899, title='三角形的内角度数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='三边判定 + 余弦定理',
    tags=['计算几何', '难度分 1407'],
    code='''
class Solution(object):
    def internalAngles(self, sides):
        
        a, b, c = sides
        if a + b <= c or a + c <= b or b + c <= a:
            return []
        
        cosA = (b ** 2 + c ** 2 - a ** 2) / 2.0 / b / c
        cosB = (a ** 2 + c ** 2 - b ** 2) / 2.0 / a / c
        cosC = (a ** 2 + b ** 2 - c ** 2) / 2.0 / a / b
        return sorted([acos(cosA) / pi * 180, acos(cosB) / pi * 180, acos(cosC) / pi * 180])
''',
    setup='from math import acos, pi',
    call='Solution().internalAngles([5, 3, 4])',
    expect=[36.86990, 53.13010, 90.0],
    result_fn=lambda r: [round(x, 5) for x in r],
    views=[
        dict(type='array', var='sides', label='sides', h=210, cell=80),
        dict(type='text', fn=lambda S: ('　'.join(f"`{k} = {S[k]:.4f}`" for k in ('cosA', 'cosB', 'cosC') if k in S) or ('三条边：`a + b > c`、`a + c > b`、`b + c > a` 全部成立才行' if 'a' in S else '')), size=26, h=70),
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=['a', 'b', 'c', ('cosA', 'cosA', 'blue'), ('cosB', 'cosB', 'pink'), ('cosC', 'cosC', 'green')],
    captions={
        'a, b, c = sides': '三边直接取出：`a = {a}`，`b = {b}`，`c = {c}`（没有排序，所以三个不等式都要判断）',
        'if a + b <= c': lambda S, B, r: (f'两边之和：`{S.a}+{S.b}={S.a+S.b}` vs `{S.c}`；`{S.a}+{S.c}={S.a+S.c}` vs `{S.b}`；`{S.b}+{S.c}={S.b+S.c}` vs `{S.a}` → '
                       + ('有一个 ==不大于== 第三边，返回空数组' if (S.a + S.b <= S.c or S.a + S.c <= S.b or S.b + S.c <= S.a) else '三个都成立，能构成三角形')),
        'cosA =': '余弦定理：`cosA = (b² + c² − a²) / 2bc` = =={cosA:.4f}==（边 a=5 对着直角，所以是 0）。`2.0` 让除法保持浮点',
        'cosB =': '`cosB = (a² + c² − b²) / 2ac` = =={cosB:.4f}==',
        'cosC =': '`cosC = (a² + b² − c²) / 2ab` = =={cosC:.4f}==',
        'return sorted': '三个 `acos` 都转成度：`{acos(cosA) / pi * 180:.2f}°`、`{acos(cosB) / pi * 180:.2f}°`、`{acos(cosC) / pi * 180:.2f}°`，最后 `sorted` 排成非递减',
    },
    cards=dict(
        one_liner='三边都用余弦定理算一遍，最后统一排序',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给长度为 3 的正整数数组 `sides`，判断能否做三角形的三边（面积为正）',
         '能：返回按 ==非递减== 排序的三个内角（单位：度）；不能：返回 `[]`',
         '示例：`[3,4,5]` → `[36.87, 53.13, 90]`；`[2,4,2]` → `[]`'],
        quote='题目要求先判断能否形成三角形，可以直接通过两边之和是否大于第三边来进行判断。若可以，则可以利用余弦定理，计算出每个角的cos值，然后计算acos，再转化为角度即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['不排序，所以 ==三个== 不等式都写出来：任意两边之和必须大于第三边',
              '三个角各用一次余弦定理，得到 `cosA`、`cosB`、`cosC`',
              '`acos` 得弧度，`/ pi * 180` 转成度，再 `sorted` 满足“非递减”'],
        summary=['时间、空间都是 `O(1)`',
         '三角形判定用 `<=`：两边之和等于第三边时三点共线，面积为 0',
         '原文为 Python 2 写法，已调整：`2.0` 保证浮点除法，Python 3 下行为不变；仅 `from math import acos, pi` 放在 setup',
         '对比灵神：灵神先排序，只判断 `a + b > c`，且第三个角用 180 减；这里三个角都用 acos 算'],
    ),
)
