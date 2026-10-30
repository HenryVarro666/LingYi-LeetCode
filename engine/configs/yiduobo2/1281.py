N = 4421


def _done(S):
    n = S.get('n')
    if not isinstance(n, int):
        return 0
    return len(str(N)) - (len(str(n)) if n else 0)


def _rows(S):
    """账本：每一轮分离出的 now、去掉个位后的 n、累计的 x、y（只填到当前行已经算出的部分）"""
    ds = [int(c) for c in str(N)][::-1]
    line, done = S.get('_line'), _done(S)
    full, part, fields = done, None, 0
    if line == 6:
        full, part, fields = done, done, 1
    elif line == 7:
        full, part, fields = done - 1, done - 1, 2
    elif line == 8:
        full, part, fields = done - 1, done - 1, 3
    rows, x, y, n = [], 0, 1, N
    for r in range(len(ds)):
        now = ds[r]
        n //= 10
        x += now
        y *= now
        vals = [now, n, x, y]
        if r < full:
            rows.append(vals)
        elif r == part:
            rows.append(vals[:fields] + [None] * (4 - fields))
    return rows


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '分离每一位的过程（一行 = 一轮 while）', 24, T['muted'], bold=True)
    heads = ['轮', 'now = n % 10', 'n //= 10 后', 'x（和）', 'y（积）']
    cols = [T['muted'], T['orange'], T['blue'], T['green'], T['pink']]
    ws = [70, 230, 200, 170, 170]
    sx = x0 + (x1 - x0 - sum(ws)) / 2
    y = y0 + 54
    X = sx
    for h, w, c in zip(heads, ws, cols):
        cv.text((X + w / 2, y), h, 23, c, anchor='mt', bold=True)
        X += w
    cv.line([(sx, y + 38), (sx + sum(ws), y + 38)], T['border'], 2)
    if 'x' not in S:
        cv.text((sx + 10, y + 64), f'初始：n = {N}，x = 0，y = 1' if 'n' in S else '', 24, T['dim'])
        return
    rows = _rows(S)
    for r, vals in enumerate(rows):
        Y = y + 50 + r * 56
        last = r == len(rows) - 1
        if last:
            cv.rect((sx - 6, Y - 6, sx + sum(ws) + 6, Y + 46), fill=T['panel2'], r=8)
        X = sx
        cells = [r + 1] + vals
        for k, (v, w, c) in enumerate(zip(cells, ws, cols)):
            if v is not None:
                cv.text((X + w / 2, Y + 20), v, 30, c if k else T['dim'], anchor='mm', bold=True)
            X += w


CONFIG = dict(
    num=1281, title='整数的各位积和之差', difficulty='Easy', category='数学',
    author='yiduobo', technique='分离每一位 · 求和求积再作差',
    tags=['List.md'],
    code='''
class Solution(object):
    def subtractProductAndSum(self, n):
        x = 0
        y = 1
        while n:
            now = n % 10
            n //= 10
            x += now
            y *= now

        return y - x
''',
    call=f'Solution().subtractProductAndSum({N})',
    expect=21,
    views=[
        dict(type='array', var=lambda S: list(str(N)), label=f'n = {N}（绿 = 已分离出来的位）', cell=100, h=160,
             color=lambda S, i, v: 'green' if i >= len(str(N)) - _done(S) else None),
        dict(type='custom', draw=_draw, h=360),
    ],
    watch=[('n', 'n', 'blue'), ('now', 'now', 'orange'), ('x', 'x', 'green'), ('y', 'y', 'pink')],
    captions={
        'x = 0': '`x` 记各位之==和==，从 0 开始',
        'y = 1': '`y` 记各位之==积==，必须从 1 开始',
        'while n:': lambda S, B, ret: (f'`n = {B.n}` 还没分离完' if B.n else '`n = 0`：每一位都分离出来了'),
        'now = n % 10': '分离出最低位：`now = {n} % 10 = {now}`',
        'n //= 10': lambda S, B, ret: (f'去掉最低位：`n = {B.n} // 10 = {S.n}`' +
                                       ('（==原文是 `n /= 10`，Python 3 要写 `//=`==）' if B.n == N else '')),
        'x += now': '求和：`x = {B.x} + {now} = {x}`',
        'y *= now': '求积：`y = {B.y} × {now} = {y}`',
        'return y - x': '积 `{y}` − 和 `{x}` = =={ret}==',
    },
    cards=dict(
        one_liner='把 n 的每一位逐个分离出来，分别求和、求积，最后作差',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['给你整数 `n`，返回「各位数字之积」与「各位数字之和」的差',
                 '示例：`n = 4421` → 积 `4×4×2×1 = 32`，和 `4+4+2+1 = 11`，答案 `21`'],
        quote='比较基础的题目，==直接分离每一位，分别求和求积之后作差==即可。',
        quote_src='—— yiduobo 题解',
        idea=['`now = n % 10` 拿到最低位，`n //= 10` 把它去掉',
              '`x` 累加每一位，`y` 累乘每一位',
              '`n` 变成 0 说明每一位都分离完了，返回 `y - x`'],
        summary=['时间 `O(log n)`（位数），空间 `O(1)`',
                 '`y` 初始化为 1 而不是 0',
                 '原文为 Python 2 写法：`n /= 10` 是整除，已改为 `n //= 10`，并删去文档字符串',
                 '若保留 `/=`，Python 3 中 n 会变成小数，结果出错',
                 '对比灵神：先取 `n % 10` 再更新，写法几乎一样；变量名 x/y 对应 s/prod'],
    ),
)
