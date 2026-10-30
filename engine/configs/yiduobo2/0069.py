import math


def _seq(x, upto):
    """从 x 出发的牛顿迭代序列，直到等于当前 x1"""
    out = [x]
    v = x
    for _ in range(40):
        if abs(v - upto) < 1e-12:
            break
        v = (v + x / v) / 2
        out.append(v)
    return out


def _plot(cv, S, B, box, T):
    x0b, y0b, x1b, y1b = box
    X = S.get('x')
    cv.text((x0b + 18, y0b + 4), '曲线 f(p) = p² − x：蓝点 = 当前 (x0, f(x0))，粉线 = 切线，绿点 = 真正的根 √x', 22, T['muted'], bold=True)
    if not isinstance(X, float) or 'x0' not in S:
        cv.text((x0b + 18, y0b + 60), '（x 变成浮点数之后开始画图）' if isinstance(X, int) and X >= 2 else '', 24, T['dim'])
        return
    x0 = S['x0']
    x1 = S.get('x1')
    root = math.sqrt(X)
    # ---- 上：自适应放大的抛物线
    L, R = x0b + 60, x1b - 40
    top, bot = y0b + 50, y0b + 330
    P = max(x0 * 1.08, root * 1.3)
    f = lambda p: p * p - X  # noqa: E731
    ylo, yhi = f(0), f(P)

    def px(p):
        return L + p / P * (R - L)

    def py(v):
        return bot - (v - ylo) / (yhi - ylo) * (bot - top)
    cv.line([(L, py(0)), (R, py(0))], T['border'], 2)
    cv.line([(L, top), (L, bot)], T['border'], 2)
    pts = [(px(P * k / 80), py(f(P * k / 80))) for k in range(81)]
    cv.line(pts, T['text'], 3)
    cv.d.ellipse((px(root) - 8, py(0) - 8, px(root) + 8, py(0) + 8), fill=T['green'])
    cv.text((px(root), py(0) + 12), f'√x≈{root:.2f}', 20, T['green'], anchor='mt', bold=True)
    if x1 is not None:
        cv.line([(px(x0), py(f(x0))), (px(x1), py(0))], T['pink'], 4)
        cv.d.ellipse((px(x1) - 7, py(0) - 7, px(x1) + 7, py(0) + 7), fill=T['pink'])
        cv.text((px(x1), py(0) - 14), f'x1={x1:.2f}', 20, T['pink'], anchor='mb', bold=True)
    cv.dashed((px(x0), py(f(x0))), (px(x0), py(0)), T['blue'], 2)
    cv.d.ellipse((px(x0) - 9, py(f(x0)) - 9, px(x0) + 9, py(f(x0)) + 9), fill=T['blue'])
    cv.text((px(x0) - 12, py(f(x0))), f'x0={x0:.2f}', 20, T['blue'], anchor='rm', bold=True)
    cv.text((R, bot + 4), f'p 轴（0 ~ {P:.1f}，随 x0 自动放大）', 18, T['dim'], anchor='rt')
    # ---- 下：固定比例的数轴，记录每一次跳跃
    yl = y0b + 430
    cv.text((x0b + 18, yl - 60), f'数轴 0 ~ {X:g}：每次迭代都跳得离 √x 更近', 22, T['muted'], bold=True)
    NL, NR = x0b + 50, x1b - 50

    def nx(p):
        return NL + p / X * (NR - NL)
    cv.line([(NL, yl), (NR, yl)], T['border'], 3)
    for t in (0, X / 2, X):
        cv.text((nx(t), yl + 12), f'{t:g}', 18, T['dim'], anchor='mt')
    cv.tri_up(nx(root), yl + 4, 8, T['green'])
    seq = _seq(X, x1 if x1 is not None else x0)
    for k in range(1, len(seq)):
        a, b = seq[k - 1], seq[k]
        last = k == len(seq) - 1
        cv.arc_arrow((nx(a), yl - 4), (nx(b), yl - 4), 26 + 70 * (a - b) / X, T['pink'] if last else T['dim'], 3 if last else 2)
    for k, v in enumerate(seq):
        c = T['pink'] if k == len(seq) - 1 else T['muted']
        cv.d.ellipse((nx(v) - 6, yl - 6, nx(v) + 6, yl + 6), fill=c)


def _while(S, B, ret):
    d = abs(B.x0 - B.x1)
    if d >= 1:
        return f'`|x0 − x1| = {d:.3f} ≥ 1` → 整数部分还可能变，继续作切线'
    return f'`|x0 − x1| = {d:.3f} < 1` → ==整数部分已经确定==，停止迭代'


CONFIG = dict(
    num=69, title='x 的平方根', difficulty='Easy', category='二分查找',
    author='yiduobo', technique='牛顿迭代法',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution(object):
    def mySqrt(self, x):
        if x < 2:
            return x

        x *= 1.0
        x0 = x
        x1 = (x0 + x / x0) / 2

        while abs(x0 - x1) >= 1:
            x0 = x1
            x1 = (x0 + x / x0) / 2

        return int(x1)
''',
    call='''Solution().mySqrt(0)
Solution().mySqrt(50)''',
    expect=7,
    views=[
        dict(type='text', fn=lambda S: (f"`x1 = (x0 + x / x0) / 2` = =={S['x1']:.4f}==" if 'x1' in S else
                                        '牛顿迭代：不断作切线逼近 `p² − x = 0` 的根'), size=28),
        dict(type='custom', draw=_plot, h=560),
    ],
    watch=[('x', 'x'), ('x0', lambda S: round(S['x0'], 4), 'blue'), ('x1', lambda S: round(S['x1'], 4), 'pink'),
           ('|x0 − x1|', lambda S: round(abs(S['x0'] - S['x1']), 4))],
    captions={
        'if x < 2': lambda S, B, ret: (f'`x = {B.x} < 2`：0 和 1 的平方根就是自己；而且 x = 0 时后面 `x / x0` 会==除以 0==' if B.x < 2
                                       else f'`x = {B.x} ≥ 2` → 用牛顿迭代求 `p² − {B.x} = 0` 的根'),
        'return x': '直接返回 `{ret}`',
        'x *= 1.0': '`x *= 1.0` 把 x 变成浮点数 → 后面的 `/` 都是==浮点除法==',
        7: '从 `x0 = x = {x0:g}` 出发：在根的右边，切线会一路往左逼近',
        'x1 = (x0 + x / x0) / 2': '在 `x0 = {x0:.3f}` 处作切线（斜率 `2·x0`），交 x 轴于 `(x0 + x / x0) / 2` = =={x1:.3f}==',
        'while abs(x0 - x1) >= 1': _while,
        11: '`x0` 挪到上一条切线的交点 `{x0:.3f}`，继续',
        'return int(x1)': '`int({x1:.4f})` 舍去小数 → =={ret}==',
    },
    cards=dict(
        one_liner='在曲线 p² − x 上不断作切线，交点一步步逼近 √x',
        complexity='时间 `O(log x)`，空间 `O(1)`',
        problem=['给你非负整数 `x`，返回它的==算术平方根==，只保留整数部分',
                 '不允许用 `pow(x, 0.5)` 或 `x ** 0.5`',
                 '示例：`x = 8` → `2`；本视频：`x = 0` → `0`，`x = 50` → `7`'],
        quote='对于曲线y=f(p)上的一个点(p, f(p))做切线，切线与x轴相交的点(0, p1)一定是更接近于f(p) = 0的解的，于是可以不断做切线来逼近最终的答案。',
        quote_src='—— yiduobo 题解',
        idea=['取 `f(p) = p² − x`，它的正根就是 `√x`；在 `q` 处切线斜率为 `2q`',
              '切线交 x 轴于 `(x + q²) / 2q`，也就是 `(q + x / q) / 2` → 把 q 迭代成它',
              '某次迭代 q 的变化不超过 1 时，整数部分已经找到 → 直接返回'],
        result='`x = 50`：`50 → 25.5 → 13.73 → 8.69 → 7.22 → 7.07`，取整得 `7` ✓',
        summary=['时间 `O(log x)`：牛顿法离根很远时每次约减半，接近根后二次收敛',
                 '`x < 2` 要特判：`x = 0` 时 `x / x0` 会除以 0',
                 '原文 `x *= 1.0` 之后都是浮点运算，`/` 本就是浮点除法，Python 3 不用改；只删去了 docstring',
                 '对比灵神：灵神开区间二分，全程整数；牛顿法收敛更快，但要注意浮点精度'],
    ),
)
