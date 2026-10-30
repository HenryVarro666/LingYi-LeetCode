def _can(v, x, y):
    return any((v - a * x) >= 0 and (v - a * x) % y == 0 for a in range(v // x + 1))


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    x, y = S['primeOne'], S['primeTwo']
    ans = x * y - x - y if S.get('_line') is not None and S.get('_line') >= 4 else None
    N = 30
    cols = 6
    cell = min(110, (x1 - x0 - 60) / cols)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * cols) / 2
    cv.text((x0 + 18, y0 + 4), f'1 ~ {N}：能写成 `a×{x} + b×{y}`（a, b ≥ 0）的数标绿，不能的标红'.replace('`', ''), 22, T['muted'], bold=True)
    ch = cell * 0.72
    for v in range(1, N + 1):
        r, c = divmod(v - 1, cols)
        X, Y = sx + c * cell, y0 + 50 + r * (ch + 8)
        ok = _can(v, x, y)
        fill = T['green'] if ok else T['red']
        hit = ans is not None and v == ans
        cv.rect((X + 3, Y, X + cell - 3, Y + ch), fill=fill, alpha=70 if not hit else 255, outline=T['yellow'] if hit else None, width=5, r=10)
        cv.text((X + cell / 2, Y + ch / 2), v, 30, T['bg'] if hit else T['text'], anchor='mm', bold=True, mono=True)
    yb = y0 + 50 + 5 * (ch + 8) + 14
    last_bad = max(v for v in range(1, N + 1) if not _can(v, x, y))
    if ans is not None:
        cv.text((x0 + 18, yb), f'最大的红色数字 = {last_bad} = {x}×{y} − {x} − {y}', 30, T['yellow'], bold=True)
    else:
        cv.text((x0 + 18, yb), f'x = {x}，y = {y}（互质）：找最大的红色数字', 28, T['text'], bold=True)


CONFIG = dict(
    num=2979, title='最贵的无法购买的商品', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='结论 xy − x − y',
    tags=['灵神题单', '数学算法'],
    code='''
class Solution(object):
    def mostExpensiveItem(self, primeOne, primeTwo):

        return primeOne * primeTwo - primeOne - primeTwo
''',
    call='Solution().mostExpensiveItem(5, 7)',
    expect=23,
    views=[
        dict(type='custom', draw=_draw, h=620),
    ],
    watch=[('primeOne', 'primeOne', 'blue'), ('primeTwo', 'primeTwo', 'pink')],
    captions={
        'return primeOne': '`x×y − x − y = {primeOne}×{primeTwo} − {primeOne} − {primeTwo}` = =={ret}==：{ret} 是最大的凑不出的价格，比它大的都能凑出',
    },
    cards=dict(
        one_liner='两个互质面值，凑不出的最大数是 `xy − x − y`',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['商店只有两种面值的商品价格 `primeOne`、`primeTwo`（都是质数，互不相同）',
                 '求最大的整数 `v`，使得 `a×x + b×y = v` 没有非负整数解 (a, b)',
                 '示例：`primeOne = 5, primeTwo = 7` → `23`'],
        quote='这里的v就等于xy - x - y，下面给出一种比较简单的证明方法。',
        quote_src='—— yiduobo 题解原文',
        idea=['设 `x = primeOne, y = primeTwo`，要找最大的 `v`，使 `ax + by = v` 没有非负解',
              '答案==直接一行公式==：`xy − x − y`，题解的重点是证明它',
              '分两步：先证明 `v` 不可能更大，再证明 `xy − x − y` 确实凑不出'],
        before=[dict(heading='证明 ①：v 不会超过 xy − x − y', lines=[
            '假设 `v + x` 能写成 `cx + dy`（c, d ≥ 0）',
            '若 `c ≥ 1`：`(c−1)x + dy = v`，v 就能凑出，矛盾 → ==c 只能是 0==，即 `dy = v + x`',
            '若 `d ≥ x`：令 `t = d − x`，得 `(y−1)x + ty = v`，又能凑出，矛盾 → ==d 小于 x==',
            '所以 `d ≤ x−1`，`v = dy − x ≤ (x−1)y − x = xy − x − y`'])],
        after=[dict(heading='证明 ②：xy − x − y 确实凑不出', lines=[
            '假设有非负 (a, b) 使 `ax + by = xy − x − y`',
            '移项合并：`(a+1)x = (x−b−1)y`，两边非零且都是 `y` 的倍数',
            '`x, y` 互质 → `a + 1 = ky`（k ≥ 1），代回得 `(k−1)xy = −(b+1)y`',
            '左边 ≥ 0，右边 < 0，矛盾 → 凑不出。结合 ①，答案就是 `xy − x − y`'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '前提：两个面值==互质==（题目保证是不同质数），否则公式不成立',
                 '这是「钱币问题 / Frobenius 数」：`xy − x − y` 之后的数全都能凑出',
                 '原文本就是 Python 3 可运行的写法，未修改'],
    ),
)
