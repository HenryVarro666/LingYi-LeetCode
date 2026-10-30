def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S['n']
    cell = min(150, (x1 - x0 - 60) / n)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * n) / 2
    cv.text((x0 + 18, y0 + 4), f'长为 n={n} 的数字串：每个下标各填一位，互不影响', 24, T['muted'], bold=True)
    ys = y0 + 80
    ch = 230
    for i in range(n):
        X = sx + i * cell
        even = i % 2 == 0
        c = T['blue'] if even else T['pink']
        opts = '0 2 4 6 8' if even else '2 3 5 7'
        cv.rect((X + 6, ys, X + cell - 6, ys + ch), fill=c, alpha=50, outline=c, width=3, r=14)
        cv.text((X + cell / 2, ys + 40), '偶数下标' if even else '奇数下标', 20, c, anchor='mm', bold=True)
        cv.text((X + cell / 2, ys + 105), 5 if even else 4, 64, T['text'], anchor='mm', bold=True)
        cv.text((X + cell / 2, ys + 170), '种' + ('偶数' if even else '质数'), 20, T['muted'], anchor='mm')
        cv.text((X + cell / 2, ys + 200), opts, 18, T['dim'], anchor='mm', mono=True)
        cv.text((X + cell / 2, ys + ch + 10), i, 20, T['dim'], anchor='mt', mono=True)
    ya = ys + ch + 70
    a, b = (n + 1) // 2, n // 2
    cv.text((x0 + 30, ya), f'偶数下标 a = (n+1)//2 = {a} 个 → 5^{a} = {5 ** a}', 28, T['blue'], bold=True)
    cv.text((x0 + 30, ya + 48), f'奇数下标 b = n//2 = {b} 个 → 4^{b} = {4 ** b}', 28, T['pink'], bold=True)
    cv.text((x0 + 30, ya + 96), f'乘法原理：{5 ** a} × {4 ** b} = {5 ** a * 4 ** b}（再对 10^9+7 取模）', 28, T['green'], bold=True)


CONFIG = dict(
    num=1922, title='统计好数字的数目', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='乘法原理 + 快速幂',
    tags=['灵神题单·数学算法', '难度分 1675'],
    code='''
class Solution:
    def countGoodNumbers(self, n: int) -> int:
        MOD = 1_000_000_007
        return pow(5, (n + 1) // 2, MOD) * pow(4, n // 2, MOD) % MOD
''',
    call='Solution().countGoodNumbers(5)',
    expect=2000,
    views=[dict(type='custom', draw=_draw, h=560)],
    watch=['n', 'MOD'],
    captions={
        'MOD =': '答案可能很大，要对 `10^9+7` 取模：`MOD = {MOD}`',
        'return pow': '偶数下标 `a=(n+1)//2={(n+1)//2}` 个，每个 5 种；奇数下标 `b=n//2={n//2}` 个，每个 4 种 → `5^{(n+1)//2} × 4^{n//2}` = =={ret}==（pow 带第三个参数，边乘边取模）',
    },
    cards=dict(
        after=[dict(heading='为什么要快速幂', lines=['`n` 最大 `10^15`，从 1 乘到 n 会超时', '`5^a` 把指数 a 按二进制拆开：每次平方，只需 `O(log a)` 步', '每次乘法后立刻取模，数值不会爆炸', '这题没有「选法」可搜，纯粹是数一数再快速幂'])],
        one_liner='偶数位 5 种、奇数位 4 种，互相独立，直接乘起来',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['偶数下标必须是偶数 `0 2 4 6 8`，奇数下标必须是质数 `2 3 5 7`',
                 '数字串可以有前导 0，求长为 `n` 的好数字串个数，对 `10^9+7` 取模',
                 '示例：`n = 4` → `400`；本视频演示 `n = 5` → `2000`'],
        quote='由于偶数下标和奇数下标互相独立，根据乘法原理，方案数相乘，答案为 5^a 4^b。',
        quote_src='—— 灵茶山艾府题解',
        idea=['下标 0 起算，偶数下标有 `(n+1)//2` 个，奇数下标有 `n//2` 个',
              '每个位置的选择互不影响 → ==乘法原理==，方案数相乘',
              'n 最大 `10^15`，不能循环乘，用快速幂 `pow(x, e, MOD)`'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '偶数下标个数是 `(n+1)//2`（向上取整），别写成 `n//2`',
                 'Python 内置 `pow(底, 指数, 模)` 就是快速幂，且每步取模',
                 '最后两个幂相乘后还要再 `% MOD`'],
    ),
)
