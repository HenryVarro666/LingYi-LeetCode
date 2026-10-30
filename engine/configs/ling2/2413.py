INPUTS = [5, 6]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S.get('n')
    if not isinstance(n, int):
        return
    cv.text((x0 + 18, y0 + 4), f'n = {n} 的倍数（绿 = 偶数，2 的倍数）', 24, T['muted'], bold=True)
    cell, gap = 150, 24
    k = 4
    sx = x0 + (x1 - x0 - (k * cell + (k - 1) * gap)) / 2
    y = y0 + 60
    ans = (n % 2 + 1) * n
    for i in range(1, k + 1):
        X = sx + (i - 1) * (cell + gap)
        v = i * n
        even = v % 2 == 0
        best = v == ans
        cv.rect((X, y, X + cell, y + 96), fill=T['green'] if even else T['panel2'], r=14,
                outline=T['yellow'] if best else T['border'], width=5 if best else 2)
        cv.text((X + cell / 2, y + 48), v, 44, T['bg'] if even else T['text'], anchor='mm', bold=True)
        cv.text((X + cell / 2, y + 110), f'{i} × {n}', 22, T['muted'], anchor='mt', mono=True)
        if best:
            cv.text((X + cell / 2, y + 146), '最小偶倍数', 24, T['yellow'], anchor='mt', bold=True)
    yy = y + 210
    cv.line([(x0 + 30, yy - 14), (x1 - 30, yy - 14)], T['border'], 2)
    par = '奇数' if n % 2 else '偶数'
    cv.rich(x0 + 40, yy, f'`n % 2 = {n % 2}`：n 是==' + par + '==', x1 - x0 - 80, size=30)
    cv.rich(x0 + 40, yy + 56, f'`(n % 2 + 1) * n = ({n % 2} + 1) × {n}` = =={ans}==', x1 - x0 - 80, size=30)
    cv.rich(x0 + 40, yy + 112, '奇数 → 乘 2；偶数 → 乘 1（就是自己）', x1 - x0 - 80, size=26, color=T['muted'])


def _table(S):
    n = S.get('n')
    if not isinstance(n, int):
        return ''
    k = INPUTS.index(n)
    parts = [f'`n = {v}` → `{(v % 2 + 1) * v}`' for v in INPUTS[:k + 1]]
    return '本视频跑两个示例：' + '，'.join(parts)


CONFIG = dict(
    num=2413, title='最小偶倍数', difficulty='Easy', category='数学',
    author='灵茶山艾府', technique='分类讨论 · 一行公式',
    tags=['List.md'],
    code='''
class Solution:
    def smallestEvenMultiple(self, n: int) -> int:
        return (n % 2 + 1) * n
''',
    call='\n'.join([f'a{i} = Solution().smallestEvenMultiple({v})' for i, v in enumerate(INPUTS)]
                   + ['(' + ', '.join(f'a{i}' for i in range(len(INPUTS))) + ')']),
    expect=(10, 6),
    views=[
        dict(type='text', fn=_table, size=28, h=60),
        dict(type='custom', draw=_draw, h=440),
    ],
    watch=[('n', 'n', 'blue'), ('n % 2', 'n % 2', 'orange')],
    captions={
        'return (n % 2 + 1) * n': lambda S, B, ret: (
            f'`n = {S.n}` 是奇数：`n % 2 + 1 = 2`，答案 `2n` = =={ret}=='
            if S.n % 2 else
            f'`n = {S.n}` 是偶数：`n % 2 + 1 = 1`，==它自己就是 2 的倍数==，答案 =={ret}=='),
    },
    cards=dict(
        one_liner='n 是奇数答案就是 2n，n 是偶数答案就是 n',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给你正整数 `n`，返回 `2` 和 `n` 的==最小公倍数==',
                 '示例 1：`n = 5` → `10`',
                 '示例 2：`n = 6` → `6`（数字也是自己的倍数）'],
        quote='根据题意，当 n 为奇数时，答案为 2n，当 n 为偶数时，答案为 n。因此答案为 ==(n mod 2 + 1)·n==',
        quote_src='—— 灵茶山艾府题解',
        idea=['偶数 n 本身就是 2 的倍数 → 答案 `n`',
              '奇数 n 和 2 互质 → 最小公倍数是 `2n`',
              '`n % 2` 奇数为 1、偶数为 0，加 1 正好是要乘的倍数'],
        result='`n = 5` → `10`，`n = 6` → `6` ✓',
        after=[dict(heading='写法二：位运算', lines=[
            '`return n << (n & 1)`',
            '`n & 1` 取最低位：奇数为 1、偶数为 0',
            '奇数左移一位 = 乘 2；偶数左移 0 位 = 不变',
            '例：`5 = 101` → `1010 = 10`；`6 = 110` 不动'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '把「分类讨论」压成一个表达式：`(n % 2 + 1) * n`',
                 '一般情况：`lcm(a, b) = a * b // gcd(a, b)`',
                 '注意运算优先级：`n % 2 + 1` 要加括号'],
    ),
)
