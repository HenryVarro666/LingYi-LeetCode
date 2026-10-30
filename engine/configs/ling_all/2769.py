def _line(S):
    num, t = S['num'], S['t']
    return (f"`num` 一路 +1：`{num} + {t} = {num + t}`；`x` 一路 −1：`x − {t}`；要相遇："
            f"`x − {t} = {num + t}` → `x = {num} + 2×{t}` = =={num + 2 * t}==")


def _nl(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    num, t = S['num'], S['t']
    lo, hi = num - 1, num + 2 * t + 1
    sx = x0 + 60
    w = (x1 - x0 - 120) / (hi - lo)
    ay = y0 + (y1 - y0) / 2
    cv.line([(sx, ay), (x1 - 60, ay)], T['border'], 3)
    for v in range(lo, hi + 1):
        X = sx + (v - lo) * w
        cv.line([(X, ay - 8), (X, ay + 8)], T['dim'], 2)
        cv.text((X, ay + 16), v, 20, T['muted'], anchor='mt', mono=True)
    def pt(v, name, c, dy):
        X = sx + (v - lo) * w
        cv.tri_up(X, ay + 60, 10, c)
        cv.text((X, ay + 76), f'{name}={v}', 24, c, anchor='mt', bold=True)
    pt(num, 'num', T['blue'], 0)
    pt(num + t, 'num+t', T['cyan'], 0)
    pt(num + 2 * t, 'x', T['green'], 0)
    X0, X1, X2 = (sx + (v - lo) * w for v in (num, num + t, num + 2 * t))
    cv.arrow((X0, ay - 40), (X1, ay - 40), T['blue'], 4)
    cv.text(((X0 + X1) / 2, ay - 52), f'num 加 {t} 次', 22, T['blue'], anchor='mb', bold=True)
    cv.arrow((X2, ay - 40), (X1, ay - 40), T['green'], 4)
    cv.text(((X1 + X2) / 2, ay - 52), f'x 减 {t} 次', 22, T['green'], anchor='mb', bold=True)


CONFIG = dict(
    num=2769, title='找出最大的可达成数字', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='数学：x = num + 2t',
    tags=[],
    code='''
class Solution:
    def theMaximumAchievableX(self, num: int, t: int) -> int:
        return num + t * 2
''',
    call='Solution().theMaximumAchievableX(3, 2)',
    expect=7,
    views=[
        dict(type='custom', draw=_nl, h=360),
        dict(type='text', fn=_line, size=30, h=200),
    ],
    watch=[('num', 'num', 'blue'), ('t', 't', 'pink')],
    captions={
        'return num + t * 2': '`num` 只增、`x` 只减，各 `t` 次，在 `num + t` 相遇 → 最大的 `x = num + 2t = {num} + {t * 2}` = =={num + t * 2}==',
    },
    cards=dict(
        one_liner='要 x 最大：num 一路加，x 一路减，在中间碰头',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['每次操作：`x` 加或减 `1`，同时 `num` 可以加或减 `1`',
                 '不超过 `t` 次操作后 `x == num`，求最大的 `x`',
                 '示例：`num=4, t=1` → `6`；`num=3, t=2` → `7`'],
        quote='只对 num 执行增加操作，t 次后变为 num+t。只对 x 执行减少操作，t 次后变为 x-t。由 num+t = x-t 得 x = num+2t。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每次操作让两数的差缩小 2：`x` 减 1、`num` 加 1',
              '最多缩小 `2t`，所以初始差最大是 `2t`',
              '更大的 `x` 在 `t` 次内追不上 `num`'],
        after=[dict(heading='验证示例', lines=['`num=4, t=1`：`4 + 2×1 = 6`，x 减 1 到 5、num 加 1 到 5，相遇', '`num=3, t=2`：`3 + 2×2 = 7`，x 走 7→6→5，num 走 3→4→5，相遇', '再大一点的 x 比如 8：每步最多缩小 2，2 步只能缩小 4，追不上'])],
        summary=['时间 `O(1)`，空间 `O(1)`，一行公式 `num + 2t`',
                 '`x` 和 `num` 同时动：每步差距减 2，不是减 1',
                 '核心是「每步缩小的差距上限」这种极端构造思路'],
    ),
)
