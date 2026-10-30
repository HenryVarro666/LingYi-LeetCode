PCOL = {2: 'blue', 3: 'pink', 5: 'green'}
INPUTS = [0, 14, 90]


def _factor(v):
    out, p = [], 2
    while p * p <= v:
        while v % p == 0:
            out.append(p)
            v //= p
        p += 1
    if v > 1:
        out.append(v)
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S.get('n')
    if not isinstance(n, int):
        return
    cv.text((x0 + 18, y0 + 4), '把 n 分解质因数（蓝 = 2，粉 = 3，绿 = 5，红 = 其他质因数）', 24, T['muted'], bold=True)
    if n <= 0:
        cv.rich(x0 + 24, y0 + 60, f'`n = {n}` 不是正整数，谈不上质因数', x1 - x0 - 48, size=30)
        return
    fs = _factor(n)
    orig = next((o for o in INPUTS[::-1] if o > 0 and o % n == 0 and all(p in (3, 5) for p in _factor(o // n))), n)
    removed = _factor(orig // n)
    y = y0 + 50
    expr = f'n = {n}' + (' = ' + ' × '.join(map(str, fs)) if len(fs) > 1 else ('（质数）' if fs else '（没有质因数）'))
    cv.text((x0 + 24, y), expr, 32, T['text'], bold=True, mono=True)
    y += 58
    cw, ch, gap = 84, 68, 14
    sx = x0 + 24
    for k, p in enumerate(fs):
        X = sx + k * (cw + gap)
        cv.rect((X, y, X + cw, y + ch), fill=T[PCOL.get(p, 'red')], r=12)
        cv.text((X + cw / 2, y + ch / 2), p, 34, T['bg'], anchor='mm', bold=True)
    if not fs:
        cv.text((sx, y + 20), '空：n = 1 没有任何质因数', 28, T['muted'])
    y += ch + 22
    if removed:
        cv.text((sx, y), f'已经除掉的因子（原来 n = {orig}）', 22, T['muted'], bold=True)
        for k, p in enumerate(removed):
            X = sx + k * (cw + gap)
            c = T[PCOL.get(p, 'red')]
            cv.rect((X, y + 34, X + cw, y + 34 + ch), outline=c, width=3, r=12)
            cv.text((X + cw / 2, y + 34 + ch / 2), f'÷{p}', 30, c, anchor='mm', bold=True)
    y += 34 + ch + 30
    if S['_line'] == 9:
        w = max(4, n.bit_length())
        a, b = f'{n:0{w}b}', f'{n - 1:0{w}b}'
        r = f'{n & (n - 1):0{w}b}'
        cv.text((x0 + 24, y), '最后用位运算判断 n 是不是 2 的幂：', 26, T['muted'], bold=True)
        rows = [(f'n     = {n}', a, T['blue']), (f'n − 1 = {n - 1}', b, T['purple']), ('n & (n − 1)', r, T['green'] if n & (n - 1) == 0 else T['red'])]
        for k, (lab, bits, c) in enumerate(rows):
            yy = y + 44 + k * 54
            cv.text((x0 + 24, yy + 22), lab, 26, T['text'], anchor='lm', mono=True)
            for t, ch in enumerate(bits):
                X = x0 + 300 + t * 52
                cv.rect((X, yy, X + 46, yy + 46), fill=c if ch == '1' else T['panel2'], r=6)
                cv.text((X + 23, yy + 23), ch, 26, T['bg'] if ch == '1' else T['dim'], anchor='mm', bold=True, mono=True)
        cv.line([(x0 + 24, y + 147), (x0 + 300 + w * 52, y + 147)], T['border'], 2)


def _ret(S, B, ret):
    n = S.n
    w = max(2, n.bit_length())
    s = f'只剩 `n = {n}`：`{n:0{w}b} & {n - 1:0{w}b} = {n & (n - 1):0{w}b}`'
    if ret:
        return s + ' = 0 → n 是 ==2 的幂==，只含因子 2 → 丑数 `True`'
    return s + ' ≠ 0 → 不是 2 的幂，==还有别的质因子== → `False`'


def _w(p):
    def f(S, B, ret):
        if B.n % p == 0:
            return f'`{B.n} % {p} == 0` → 还有因子 {p}，继续除'
        return f'`{B.n}` 不是 {p} 的倍数 → ==因子 {p} 去干净了=='
    return f


CONFIG = dict(
    num=263, title='丑数', difficulty='Easy', category='数学',
    author='灵茶山艾府', technique='去掉因子 3、5 + 位运算判 2 的幂',
    tags=['List.md'],
    code='''
class Solution:
    def isUgly(self, n: int) -> bool:
        if n <= 0:
            return False
        while n % 3 == 0:
            n //= 3
        while n % 5 == 0:
            n //= 5
        return n & (n - 1) == 0
''',
    call='''Solution().isUgly(0)
Solution().isUgly(14)
Solution().isUgly(90)''',
    expect=True,
    views=[
        dict(type='custom', draw=_draw, h=560),
        dict(type='text', fn=lambda S: '依次运行三个输入：`0` → `14` → `90`', size=24),
    ],
    watch=[('n', 'n', 'blue'), ('n & (n - 1)', 'n & (n - 1)')],
    captions={
        'if n <= 0': lambda S, B, ret: (f'`n = {B.n} ≤ 0`：丑数必须是==正整数== → 直接 `False`' if B.n <= 0
                                        else f'`n = {B.n}` 是正整数，开始去掉因子 3 和 5'),
        'return False': '不是正整数 → `False`',
        'while n % 3 == 0': _w(3),
        'n //= 3': '`n //= 3` → `{n}`',
        'while n % 5 == 0': _w(5),
        'n //= 5': '`n //= 5` → `{n}`',
        'return n & (n - 1)': _ret,
    },
    cards=dict(
        one_liner='除干净 3 和 5，剩下的必须是 2 的幂',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['==丑数==：只包含质因数 `2`、`3`、`5` 的==正==整数',
                 '判断整数 `n` 是不是丑数（`1` 没有质因数，也算丑数）',
                 '示例：`6` → `true`；`1` → `true`；`14` → `false`（含质因数 7）'],
        before=[dict(heading='n & (n − 1)：2 的幂判断', lines=[
            '`n − 1` 会把 n 最低位的 1 变成 0，它右边的 0 全变成 1',
            '所以 `n & (n − 1)` 就是==去掉 n 的最低位 1==',
            '2 的幂二进制只有一个 1：`8 = 1000`，`8 & 7 = 1000 & 0111 = 0`',
            '`12 = 1100`，`12 & 11 = 1000 ≠ 0` → 不是 2 的幂'])],
        quote='去掉 n 中的因子 3……去掉 n 中的因子 5……最后，n 必须只剩下因子 2，即 n=2^k。用 231. 2 的幂 中的技巧判断。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`n ≤ 0` 不是正整数，直接返回 `false`',
              '不断除以 3、除以 5，直到不再是它们的倍数',
              '只剩因子 2 ⇔ n 是 2 的幂 ⇔ `n & (n − 1) == 0`（`n = 1` 时也成立）'],
        result='`0` → False，`14` → False，`90` → True ✓',
        summary=['时间 `O(log n)`：因子 3 和因子 5 一共 `O(log n)` 个；空间 `O(1)`',
                 '易错：别忘了特判 `n ≤ 0`，否则 `0 % 3 == 0` 会死循环',
                 '用位运算省掉了「不断除以 2」的循环',
                 '`n = 1`：`1 & 0 = 0`，正确返回 `true`'],
    ),
)
