PCOL = {2: 'blue', 3: 'pink', 5: 'green'}
INPUTS = [14, 60]


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
    n = S.get('num')
    if not isinstance(n, int):
        return
    cv.text((x0 + 18, y0 + 4), 'num 的质因数（蓝 = 2，粉 = 3，绿 = 5，红 = 其他）', 24, T['muted'], bold=True)
    if n <= 0:
        return
    fs = _factor(n)
    orig = next((o for o in INPUTS[::-1] if o % n == 0 and all(p in (2, 3, 5) for p in _factor(o // n))), n)
    removed = _factor(orig // n)
    y = y0 + 50
    expr = f'num = {n}' + (' = ' + ' × '.join(map(str, fs)) if len(fs) > 1 else ('（质数）' if fs else ''))
    cv.text((x0 + 24, y), expr, 32, T['text'], bold=True, mono=True)
    y += 58
    cw, ch, gap = 84, 68, 14
    sx = x0 + 24
    for k, p in enumerate(fs):
        X = sx + k * (cw + gap)
        cv.rect((X, y, X + cw, y + ch), fill=T[PCOL.get(p, 'red')], r=12)
        cv.text((X + cw / 2, y + ch / 2), p, 34, T['bg'], anchor='mm', bold=True)
    if not fs:
        cv.rect((sx, y, sx + cw, y + ch), outline=T['green'], width=3, r=12)
        cv.text((sx + cw / 2, y + ch / 2), '1', 34, T['green'], anchor='mm', bold=True)
        cv.text((sx + cw + 20, y + ch / 2), '除得只剩 1：没有别的质因数了', 26, T['green'], anchor='lm', bold=True)
    y += ch + 30
    if removed:
        cv.text((sx, y), f'已经除掉的（原来 num = {orig}）', 22, T['muted'], bold=True)
        for k, p in enumerate(removed):
            X = sx + k * (cw + gap)
            c = T[PCOL.get(p, 'red')]
            cv.rect((X, y + 34, X + cw, y + 34 + ch), outline=c, width=3, r=12)
            cv.text((X + cw / 2, y + 34 + ch / 2), f'÷{p}', 30, c, anchor='mm', bold=True)
    y += 34 + ch + 40
    order = [(6, 2), (8, 3), (10, 5)]
    cv.text((sx, y), '三轮除法：', 24, T['muted'], bold=True)
    ln = S.get('_line')
    X = sx + 130
    for k, (line, p) in enumerate(order):
        on = ln in (line, line + 1)
        done = (ln or 0) > line + 1
        c = T[PCOL[p]]
        cv.rect((X, y - 8, X + 150, y + 38), fill=c if on else T['panel2'], outline=c, width=2, r=10)
        cv.text((X + 75, y + 15), f'除尽 {p}' + (' ✓' if done else ''), 24, T['bg'] if on else c, anchor='mm', bold=True)
        X += 170


def _w(p):
    def f(S, B, ret):
        if B.num % p == 0:
            return f'`{B.num} % {p} == 0` → 还能除以 {p}'
        return f'`{B.num}` 不是 {p} 的倍数 → =={p} 除干净了=='
    return f


def _ret(S, B, ret):
    if ret:
        return f'除完 2、3、5 后 `num == 1` → 只含这三种质因数，==是丑数=='
    return f'除完 2、3、5 后剩下 `num = {S.num}` ≠ 1 → ==还有别的质因数==，不是丑数'


CONFIG = dict(
    num=263, title='丑数', difficulty='Easy', category='数学',
    author='yiduobo', technique='不断除以 2、3、5',
    tags=['List.md'],
    code='''
class Solution(object):
    def isUgly(self, num):
        if num <= 0:
            return False

        while num % 2 == 0:
            num //= 2
        while num % 3 == 0:
            num //= 3
        while num % 5 == 0:
            num //= 5

        return num == 1
''',
    call='''Solution().isUgly(14)
Solution().isUgly(60)''',
    expect=True,
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='text', fn=lambda S: '依次运行两个输入：`14` → `60`', size=24),
    ],
    watch=[('num', 'num', 'blue')],
    captions={
        'if num <= 0': lambda S, B, ret: ('`num ≤ 0` 一定不是丑数' if B.num <= 0 else f'`num = {B.num} > 0` → 开始不断除以 2、3、5'),
        'return False': '返回 `False`',
        'while num % 2 == 0': _w(2),
        'num //= 2': lambda S, B, ret: (f'`num` 除以 2 → `{S.num}`（原文 `num /= 2`，Python 3 要写 `//=`）' if B.num in INPUTS
                                        else f'`num` 除以 2 → `{S.num}`'),
        'while num % 3 == 0': _w(3),
        'num //= 3': '`num` 除以 3 → `{num}`',
        'while num % 5 == 0': _w(5),
        'num //= 5': '`num` 除以 5 → `{num}`',
        'return num == 1': _ret,
    },
    cards=dict(
        one_liner='把 2、3、5 都除干净，剩下 1 就是丑数',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['==丑数==：只包含质因数 `2`、`3`、`5` 的==正==整数',
                 '判断 `num` 是不是丑数（`1` 也算丑数）',
                 '示例：`6` → `true`；`14` → `false`（含质因数 7）；本视频：`14`、`60`'],
        quote='比较基础的题目。首先当num小于等于0时，其一定不是丑数。否则就对num不断除上2、3、5，如果除剩下来的数不为1，那么就不是丑数，否则就是丑数。',
        quote_src='—— yiduobo 题解',
        idea=['先排除 `num ≤ 0`：丑数必须是正整数',
              '三个 while 依次把因子 2、3、5 ==全部除掉==',
              '还剩别的质因数时，结果一定 > 1；只剩 1 说明是丑数'],
        result='`14` → False（剩 7），`60` → True ✓',
        summary=['时间 `O(log n)`：每除一次 num 至少变成一半；空间 `O(1)`',
                 '易错：不判 `num ≤ 0` 的话 `0 % 2 == 0` 会死循环',
                 '对比灵神：灵神只除 3 和 5，最后用 `n & (n − 1) == 0` 判断剩下的是不是 2 的幂',
                 '原文为 Python 2 写法：`num /= 2`（3、5 同）已改为 `//=`，并删去 docstring'],
    ),
)
