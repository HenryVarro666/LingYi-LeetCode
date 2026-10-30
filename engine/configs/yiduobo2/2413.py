INPUTS = [5, 6]


def _dots(cv, T, x, y, n, color, r=22, gap=18, lone_c=None):
    """把 n 个点两两配对画成两行：能配完 = 偶数"""
    cols = (n + 1) // 2
    for c in range(cols):
        if 2 * c + 1 < n:
            px = x + c * (2 * r + gap)
            cv.rect((px - 5, y - 5, px + 2 * r + 5, y + 4 * r + gap + 5), outline=T['muted'], width=2, r=r)
    for k in range(n):
        cx = x + (k // 2) * (2 * r + gap) + r
        cy = y + (k % 2) * (2 * r + gap) + r
        lone = n % 2 == 1 and k == n - 1
        cv.d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(lone_c or T['red']) if lone else color, outline=T['border'])
    return cols * (2 * r + gap)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S.get('n')
    if not isinstance(n, int):
        return
    line = S.get('_line')
    cv.text((x0 + 18, y0 + 4), f'把 n = {n} 个点两两配对：能配完就是偶数', 24, T['muted'], bold=True)
    w = _dots(cv, T, x0 + 60, y0 + 60, n, T['blue'])
    odd = n % 2 == 1
    cv.text((x0 + 60 + w + 20, y0 + 92), f'n % 2 = {n % 2}', 30, T['red'] if odd else T['green'], anchor='lm', bold=True)
    cv.text((x0 + 60 + w + 20, y0 + 132), '落单一个 → 奇数' if odd else '全部配对 → 偶数', 24,
            T['red'] if odd else T['green'], anchor='lm')
    if line not in (4, 6):  # 还没走到 return
        return
    yy = y0 + 230
    cv.line([(x0 + 30, yy - 20), (x1 - 30, yy - 20)], T['border'], 2)
    if line == 4:
        cv.text((x0 + 60, yy), 'n 本身就是 2 的倍数 → 返回 n', 26, T['green'], bold=True)
        _dots(cv, T, x0 + 60, yy + 50, n, T['green'])
        cv.text((x0 + 60, yy + 170), f'答案 = {n}', 34, T['yellow'], bold=True)
    else:
        cv.text((x0 + 60, yy), '复制一份 → 落单的点有了伴：n * 2 一定是偶数', 26, T['green'], bold=True)
        yy += 40
        w1 = _dots(cv, T, x0 + 60, yy + 50, n, T['blue'], lone_c=T['yellow'])
        cv.text((x0 + 60 + w1 + 6, yy + 82), '+', 36, T['muted'], anchor='lm', bold=True)
        w2 = _dots(cv, T, x0 + 60 + w1 + 40, yy + 50, n, T['purple'], lone_c=T['yellow'])
        ya = yy + 50 + 22
        xa, xb = x0 + 60 + w1 - 18 - 22, x0 + 60 + w1 + 40 + w2 - 18 - 22
        cv.arc_arrow((xa, ya - 26), (xb, ya - 26), 40, T['yellow'], width=3)
        cv.text((xb + 40, ya), '← 两个落单的配成一对', 22, T['yellow'], anchor='lm', bold=True)
        cv.text((x0 + 60, yy + 170), f'答案 = {n} × 2 = {n * 2}', 34, T['yellow'], bold=True)


CONFIG = dict(
    num=2413, title='最小偶倍数', difficulty='Easy', category='数学',
    author='yiduobo', technique='判断奇偶 · 分类讨论',
    tags=['List.md'],
    code='''
class Solution(object):
    def smallestEvenMultiple(self, n):
        if n % 2 == 0:
            return n
        else:
            return n * 2
''',
    call='\n'.join([f'a{i} = Solution().smallestEvenMultiple({v})' for i, v in enumerate(INPUTS)]
                   + ['(' + ', '.join(f'a{i}' for i in range(len(INPUTS))) + ')']),
    expect=(10, 6),
    views=[
        dict(type='text', fn=lambda S: f'本视频依次调用：`n = 5`、`n = 6`　当前 `n = {S["n"]}`' if 'n' in S else '', size=28, h=60),
        dict(type='custom', draw=_draw, h=460),
    ],
    watch=[('n', 'n', 'blue'), ('n % 2', 'n % 2', 'orange')],
    captions={
        'if n % 2 == 0': lambda S, B, ret: (
            f'`{S.n} % 2 = {S.n % 2}`：' + ('==偶数== → 走 `return n`' if S.n % 2 == 0 else '==奇数== → 走 `else`')),
        'return n * 2': '`n = {n}` 是奇数，和 2 互质 → 最小偶倍数是 `{n} × 2` = =={ret}==',
        4: '`n = {n}` 是偶数，==自己就是 2 的倍数== → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='奇数乘 2，偶数就是自己',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给你正整数 `n`，返回 `2` 和 `n` 的==最小公倍数==',
                 '示例 1：`n = 5` → `10`',
                 '示例 2：`n = 6` → `6`（数字也是自己的倍数）'],
        quote='比较基础的题目。==当n为奇数时，答案就是n * 2，否则就是n自己==。',
        quote_src='—— yiduobo 题解',
        idea=['答案要同时是 `n` 的倍数和 `2` 的倍数，还要最小',
              '`n` 是偶数：`n` 自己已经是 2 的倍数',
              '`n` 是奇数：`n` 的倍数里第一个偶数是 `2n`'],
        result='`n = 5` → `10`，`n = 6` → `6` ✓',
        after=[dict(heading='为什么奇数乘 2 就是最小的？', lines=[
            '`lcm(2, n) = 2 × n / gcd(2, n)`',
            '`n` 是偶数：`gcd(2, n) = 2` → `lcm = n`',
            '`n` 是奇数：`gcd(2, n) = 1` → `lcm = 2n`',
            '更小的倍数只有 `n` 本身，而它是奇数，不行'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '用 `n % 2 == 0` 判断偶数（也可以 `n & 1 == 0`，注意加括号）',
                 '原文为 Python 2 风格，仅删去文档字符串，代码未改',
                 '对比灵神：把 if/else 压成一行 `(n % 2 + 1) * n`'],
    ),
)
