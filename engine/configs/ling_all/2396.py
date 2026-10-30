def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = 9
    cv.text((x0 + 18, y0 + 4), f'n = {n}：逐个进制看 n 的写法（b 取 2 到 n−2）', 24, T['muted'], bold=True)

    def conv(x, b):
        ds = []
        while x:
            ds.append(x % b)
            x //= b
        return ds[::-1]

    rows = list(range(2, n - 1))
    cell = 64
    y = y0 + 56
    for b in rows:
        ds = conv(n, b)
        pal = ds == ds[::-1]
        cv.text((x0 + 30, y + cell / 2), f'b={b}', 24, T['muted'], anchor='lm', mono=True)
        for k, d in enumerate(ds):
            X = x0 + 130 + k * (cell + 6)
            cv.rect((X, y, X + cell, y + cell - 6), fill=T['green'] if pal else T['pink'], r=8)
            cv.text((X + cell / 2, y + (cell - 6) / 2), d, 28, T['bg'], anchor='mm', bold=True)
        cv.text((x0 + 130 + 5 * (cell + 6), y + cell / 2), '回文' if pal else '不是回文', 24, T['green'] if pal else T['pink'], anchor='lm', bold=True)
        y += cell + 4
    cv.text((x0 + 30, y + 14), 'b = n−2 时 n = 1×(n−2) + 2，写成 12，永远不是回文', 24, T['orange'], bold=True)


CONFIG = dict(
    num=2396, title='严格回文的数字', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='脑筋急转弯 · 带余除法',
    tags=['灵神题单·数学算法', '灵神题单·贪心与思维', '难度分 1329'],
    code='''
class Solution:
    def isStrictlyPalindromic(self, n: int) -> bool:
        return False
''',
    call='Solution().isStrictlyPalindromic(9)',
    expect=False,
    views=[dict(type='custom', draw=_draw, h=560)],
    watch=[('n', 'n', 'blue')],
    captions={
        'return False': '不用枚举进制：取 `b = n - 2`，`n = 1×(n-2) + 2`，写出来是 ==12==，不是回文 → 直接 ==返回 False==',
    },
    cards=dict(
        one_liner='b = n−2 时 n 恒为 “12”，所以答案永远是 False',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`n` 在 `2 ~ n-2` 的所有进制下都是回文，才叫严格回文',
                 '问 `n` 是否严格回文，`4 <= n <= 10^5`',
                 '示例：`n = 9` → `false`（3 进制是 100）'],
        quote='取 `b=n-2`，那么当 `n>4` 时，上式的 `q=1`，`r=2`，也就是说 `n` 在 `n-2` 进制下的数值为 `12`，不是回文数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['带余除法 `n = q·b + r`；`b = n-2` 时 `q = 1`、`r = 2`',
              '两位数 `1 2` 首尾不同，一定不是回文',
              '`n = 4` 只看 2 进制：`100`，也不是回文'],
        after=[dict(heading='为什么 n = 4 要单独说', lines=['`n > 4` 时 `n-2 > 2`，所以 `q = 1`、`r = 2` 才成立', '`n = 4` 时 `b` 只能取 `2`，`n-2 = 2` 进制下 `q = 2`，`r = 0`', '写出来是 `100`，首位 1 末位 0，同样不是回文', '两种情况合起来：任何输入都返回 `False`'])],
        summary=['时间 `O(1)`：不用真的转进制',
                 '上联 `return true`（石子游戏），下联 `return false`（本题），横批脑筋急转弯',
                 '易错点：别写模拟，`n` 到 `10^5` 也没必要']),
)
