N = 234


def _done(S):
    """已经剥掉的数位个数（从个位开始）"""
    n = S.get('n')
    if not isinstance(n, int):
        return 0
    return len(str(N)) - (len(str(n)) if n else 0)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S.get('n')
    cv.text((x0 + 18, y0 + 4), '当前的 n：n % 10 取出个位，n //= 10 去掉个位', 24, T['muted'], bold=True)
    if not isinstance(n, int):
        return
    s = str(n) if n else ''
    cell = 110
    sx = x0 + (x1 - x0 - cell * max(1, len(str(N)))) / 2
    y = y0 + 64
    if not s:
        cv.text(((x0 + x1) / 2, y + 50), 'n = 0 → 循环结束', 36, T['green'], anchor='mm', bold=True)
        return
    for i, ch in enumerate(s):
        X = sx + i * cell
        last = i == len(s) - 1
        cv.rect((X + 6, y, X + cell - 6, y + 100), fill=T['orange'] if last else T['panel2'], r=12,
                outline=T['orange'] if last else T['border'], width=2)
        cv.text((X + cell / 2, y + 50), ch, 54, T['bg'] if last else T['text'], anchor='mm', bold=True)
    X = sx + (len(s) - 1) * cell + cell / 2
    cv.text((X, y + 118), f'n % 10 = {n % 10}', 24, T['orange'], anchor='mt', bold=True)
    if len(s) > 1:
        Xl = sx + (len(s) - 1) * cell / 2
        cv.text((Xl, y + 118), f'n // 10 = {n // 10}', 24, T['blue'], anchor='mt', bold=True)
    else:
        cv.text((sx + cell / 2 - 10, y + 156), 'n // 10 = 0', 22, T['blue'], anchor='mt', bold=True)


def _expr(S):
    if 'prod' not in S:
        return ''
    ds = [c for c in str(N)][::-1][:_done(S)]
    p_terms, s_terms = ['1'] + ds, ['0'] + ds
    line = S.get('_line')
    if line in (5, 6):  # prod 已乘上当前个位，n 还没除
        p_terms.append(str(S['n'] % 10))
    if line == 6:  # s 也已加上
        s_terms.append(str(S['n'] % 10))
    pe = f"{' × '.join(p_terms)} = " if len(p_terms) > 1 else ''
    se = f"{' + '.join(s_terms)} = " if len(s_terms) > 1 else ''
    return f"`prod = {pe}{S['prod']}`　　`s = {se}{S['s']}`"


CONFIG = dict(
    num=1281, title='整数的各位积和之差', difficulty='Easy', category='数学',
    author='灵茶山艾府', technique='枚举数位 · 不用字符串',
    tags=['List.md'],
    code='''
class Solution:
    def subtractProductAndSum(self, n: int) -> int:
        prod, s = 1, 0
        while n:
            prod *= n % 10
            s += n % 10
            n //= 10
        return prod - s
''',
    call=f'Solution().subtractProductAndSum({N})',
    expect=15,
    views=[
        dict(type='array', var=lambda S: list(str(N)), label=f'原数 {N} 的各位（绿 = 已统计，橙 = 当前个位）', cell=110, h=170,
             color=lambda S, i, v: ('green' if i >= len(str(N)) - _done(S) else
                                    'orange' if 'prod' in S and S.get('n') and i == len(str(N)) - _done(S) - 1 else None)),
        dict(type='custom', draw=_draw, h=260),
        dict(type='text', fn=_expr, size=30, h=70),
    ],
    watch=[('n', 'n', 'blue'), ('n % 10', 'n % 10', 'orange'), ('prod', 'prod', 'pink'), ('s', 's', 'green')],
    captions={
        'prod, s = 1, 0': '乘积从 ==1== 开始、和从 ==0== 开始（乘法/加法的“单位元”）',
        'while n:': lambda S, B, ret: (f'`n = {B.n} ≠ 0`：还有数位没处理' if B.n else '`n = 0`：所有数位都取完了 → 退出循环'),
        'prod *= n % 10': '个位 `n % 10 = {n % 10}` 乘进去：`prod = {B.prod} × {n % 10} = {prod}`',
        's += n % 10': '个位 `{n % 10}` 加进去：`s = {B.s} + {n % 10} = {s}`',
        'n //= 10': lambda S, B, ret: (f'去掉个位：`n = {B.n} // 10 = {S.n}`，' +
                                       ('下一轮的个位就是原来的十位' if S.n else '数位已经剥光了')),
        'return prod - s': '各位积 `{prod}` − 各位和 `{s}` = =={ret}==',
    },
    cards=dict(
        one_liner='n % 10 取个位、n //= 10 去个位，边剥边算积与和',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['给你整数 `n`，返回「各位数字之积」与「各位数字之和」的差',
                 '示例：`n = 234` → 积 `2×3×4 = 24`，和 `2+3+4 = 9`，答案 `15`',
                 '`1 <= n <= 10^5`'],
        quote='通过 n mod 10=3 得到个位数，然后把 n 更新为 floor(n/10)=12。……遍历的过程中，计算各个数位的乘积以及元素和。',
        quote_src='—— 灵茶山艾府题解（以 n = 123 为例）',
        idea=['==不用转字符串==：`n % 10` 就是个位，`n // 10` 把十位挪到个位',
              '从个位往高位剥，每剥一位同时更新 `prod` 和 `s`',
              '`n` 变成 0 时所有数位都处理完，循环结束'],
        summary=['时间 `O(log n)`：数位个数；空间 `O(1)`',
                 '`prod` 初始化为 ==1==，写成 0 乘出来永远是 0',
                 'Python 要用 `//=` 整除；`/=` 会变成浮点数，循环停不下来',
                 '同类：258 各位相加、2520 统计能整除数字的位数'],
    ),
)
