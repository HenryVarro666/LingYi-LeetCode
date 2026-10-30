LO, HI = 10, 19
PR = [p for p in range(2, 80) if all(p % d for d in range(2, int(p ** 0.5) + 1))]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = HI - LO + 1
    cell = min(100, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    ys, ch = y0 + 150, cell * 0.9
    cv.text((x0 + 18, y0 + 4), f'数轴 [{LO}, {HI}]（蓝 = 正在检测的 x，粉 = 上一个质数 pre，绿 = 已确认的质数）', 22, T['muted'], bold=True)

    def cx(v):
        return sx + (v - LO) * cell + cell / 2

    live = 'x' in S and 'res' in S
    x = S.get('x') if live else None
    pre = S.get('pre') if live else None
    res = S.get('res') if live else None
    line = S.get('_line', 0)
    # 已经检测完的数：x 之前的数；x 本身在 flag 判定后（第 17 行起）才有结论
    decided = (x if line >= 17 else x - 1) if x is not None else LO - 1
    for v in range(LO, HI + 1):
        X = sx + (v - LO) * cell
        pr = v in PR
        known = v <= decided
        fill = T['panel2']
        if known and pr:
            fill = T['green']
        if x == v:
            fill = T['blue'] if not (known and pr) else T['green']
        if pre == v and known:
            fill = T['pink']
        cv.rect((X + 4, ys, X + cell - 4, ys + ch), fill=fill, r=10, outline=T['blue'] if x == v else T['border'],
                width=5 if x == v else 1)
        txt = T['bg'] if fill != T['panel2'] else (T['text'] if known and not pr else T['dim'])
        cv.text((X + cell / 2, ys + ch / 2), v, 34, txt, anchor='mm', bold=True)
        if known and not pr:
            cv.line([(X + 12, ys + ch - 10), (X + cell - 12, ys + 10)], T['red'], 3)
    if x is not None and LO <= x <= HI:
        cv.tri_up(cx(x), ys + ch + 22, 10, T['blue'])
        cv.text((cx(x), ys + ch + 38), 'x', 24, T['blue'], anchor='mt', bold=True)
    if pre is not None and LO <= pre <= HI:
        cv.tri_up(cx(pre), ys + ch + 22, 10, T['pink'])
        cv.text((cx(pre), ys + ch + 38 + (28 if pre == x else 0)), 'pre', 24, T['pink'], anchor='mt', bold=True)
    if res and res[0] > 0:
        yy = ys - 30
        a, b = res
        cv.line([(cx(a), yy), (cx(b), yy)], T['yellow'], 5)
        cv.line([(cx(a), yy), (cx(a), yy + 18)], T['yellow'], 5)
        cv.line([(cx(b), yy), (cx(b), yy + 18)], T['yellow'], 5)
        cv.text(((cx(a) + cx(b)) / 2, yy - 8), f'res = [{a}, {b}]，间隙 {b - a}', 26, T['yellow'], anchor='mb', bold=True)


def _txt(S):
    if 'x' not in S:
        return ''
    line = S.get('_line', 0)
    if 'y' in S and 'flag' in S and 12 <= line <= 15:
        return f"试除 `{S['x']} % {S['y']} = {S['x'] % S['y']}`（只需试到 `{S['sqrt_x'] - 1}`）"
    if 'flag' in S and line >= 17:
        return f"`{S['x']}` ==是质数== ✓" if S['flag'] else f"`{S['x']}` 是合数"
    return f"检测 `x = {S['x']}`"


CONFIG = dict(
    num=2523, title='范围内最接近的两个质数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='暴力试除 · 找到间隙 1 或 2 就提前结束',
    tags=['灵神题单·数学算法', '难度分 1650'],
    code='''
class Solution(object):
    def closestPrimes(self, left, right):

        pre = None
        res = [-1, -1]
        if left == 1:
            left += 1

        for x in range(left, right + 1):
            sqrt_x = int(sqrt(x)) + 1
            flag = True
            for y in range(2, sqrt_x):
                if x % y == 0:
                    flag = False
                    break

            if flag:
                if pre is not None and (res[0] == -1 or x - pre < res[1] - res[0]):
                    res[0] = pre
                    res[1] = x
                pre = x

            if res[1] - res[0] == 1 or res[1] - res[0] == 2:
                break

        return res
''',
    setup='from math import sqrt',
    call='Solution().closestPrimes(10, 19)',
    expect=[11, 13],
    views=[
        dict(type='text', fn=_txt, size=27, h=60),
        dict(type='custom', draw=_draw, h=420),
    ],
    watch=['left', 'right', ('x', 'x', 'blue'), ('pre', 'pre', 'pink'), ('res', 'res', 'yellow')],
    captions={
        'pre = None': '`pre` 记上一个质数，还没遇到所以是 `None`',
        'res = [-1, -1]': '`res` 是答案，`[-1, -1]` 表示还没找到质数对',
        'if left == 1': lambda S, B, r: ('`left == 1`：1 不是质数，从 2 开始' if S.left == 1 else '`left != 1`，不用调整'),
        'for x in range': '从小到大检测每个数 `x = {x}` 是不是质数',
        'sqrt_x = ': '只需试除到 √x：`int(sqrt({x})) + 1 = {sqrt_x}`，`y` 取 `2 ~ {sqrt_x - 1}`',
        'flag = True': '先假设 `{x}` 是质数',
        'for y in range': lambda S, B, r: ('试除数用完了，没找到因子' if S.y == S.sqrt_x - 1 and B.get('y') == S.y else f'试除数 `y = {S.y}`'),
        'if x % y == 0': lambda S, B, r: (f'`{S.x} % {S.y} == 0`：`{S.y}` 整除 `{S.x}` → 是合数' if S.x % S.y == 0 else f'`{S.x} % {S.y} != 0`：`{S.y}` 不是因子，继续'),
        'flag = False': '找到因子 → `flag = False`',
        'break': lambda S, B, r: ('已知是合数，不用再试了 → break' if S._line == 15 else f'`res` 的间隙 `{S.res[1] - S.res[0]}` 是 1 或 2 → 已经不可能更小，==提前结束=='),
        'if flag': lambda S, B, r: (f'`{S.x}` 是质数 → 看能不能和 `pre` 配对' if S.flag else f'`{S.x}` 是合数，跳过'),
        'if pre is not None and': lambda S, B, r: (
            ('有 `pre` 且还没有答案（`res[0] == -1`）→ 条件成立，记为第一对' if B.res[0] == -1 else
             f'有 `pre`，`{S.x} − {S.pre} = {S.x - S.pre}` < 当前 `{B.res[1] - B.res[0]}` → 更新') if (S.pre is not None and (B.res[0] == -1 or S.x - S.pre < B.res[1] - B.res[0]))
            else ('`pre` 还是 None：`x` 是遇到的第一个质数，没法配对' if S.pre is None else f'`{S.x} − {S.pre}` 不小于当前间隙 → 不更新')),
        'res[0] = pre': '`res[0] = pre = {pre}`',
        'res[1] = x': '`res[1] = x = {x}` → `res = {res}`，间隙 `{res[1] - res[0]}`',
        'pre = x': '更新 `pre = {x}`：它是下一个质数的“左邻居”',
        'if res[1] - res[0]': lambda S, B, r: (f'间隙 `{S.res[1] - S.res[0]}` 是 1 或 2：==不可能更小==，可以直接返回' if S.res[1] - S.res[0] in (1, 2)
                                               else ('还没有质数对，继续往后找' if S.res[0] == -1 else f'间隙 `{S.res[1] - S.res[0]}`，还没到 1 或 2，继续往后找')),
        'return res': '答案：=={ret}==',
    },
    cards=dict(
        one_liner='暴力试除找质数，间隙达到 1 或 2 就收工',
        complexity='最坏 `O(n√n)`，空间 `O(1)`',
        problem=['在 `[left, right]` 内找差最小的两个质数，差相同取 `nums1` 最小的一对',
                 '没有质数对返回 `[-1, -1]`',
                 '示例：`left=10, right=19` → `[11,13]`'],
        quote='实际上使用暴力算法是完全没有问题的。……最终答案如果不是（2， 3）这一组间距为1的质数，那么就很可能是两个连续的奇数构成的，也就是说最终答案为2。',
        quote_src='—— yiduobo 题解原文',
        idea=['不筛质数：逐个 `x` 试除到 √x 判断，记上一个质数 `pre`',
              '遇到新质数就和 `pre` 比间隙，更小才更新',
              '除了 `(2,3)` 间隙是 1，质数都是奇数，间隙至少 2 → 间隙 ≤ 2 就不可能更小，立刻 break'],
        summary=['最坏复杂度 `O(n√n)`，但质数分布密，实际很快就能提前结束',
                 '`left == 1` 要先改成 2：1 不是质数，否则会被当成质数',
                 '更新条件里 `res[0] == -1` 是“还没有第一对”的哨兵',
                 '原文用到 `sqrt` 但没写导入，视频里在 setup 补了 `from math import sqrt`；代码本身未改',
                 '对比灵神：灵神先筛出质数表再二分，yiduobo 直接试除 + 早停'],
    ),
)
