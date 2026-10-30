def _digits(S, key):
    v = S.get(key)
    return list(str(v)) if isinstance(v, int) else None


def _whole(cv, S, B, box, T):
    """原数字一行：蓝 = 还在 x 里（前半），绿 = 已翻转进 y（后半）"""
    x0, y0, x1, y1 = box
    if not isinstance(S.get('x'), int):
        return
    copying = S['_line'] == 12
    y = B.get('y', 0) if copying else S.get('y', 0)
    left = str(S['x'])
    right = str(y)[::-1] if y else ''
    digits = left + right
    cv.text((x0 + 18, y0 + 4), '原来的数字：蓝 = 还在 x 里（前半），绿 = 已翻转进 y（后半）', 24, T['muted'], bold=True)
    cell = 92
    sx = x0 + (x1 - x0 - cell * len(digits)) / 2
    yy = y0 + 48
    for k, d in enumerate(digits):
        X = sx + k * cell
        if k < len(left):
            c = T['yellow'] if (copying and k == len(left) - 1) else T['blue']
        else:
            c = T['green']
        cv.rect((X + 6, yy, X + cell - 6, yy + 80), fill=c, r=10)
        cv.text((X + cell / 2, yy + 40), d, 38, T['bg'], anchor='mm', bold=True)
    if right:
        mx = sx + len(left) * cell
        cv.line([(mx, yy - 8), (mx, yy + 88)], T['text'], 3)
        cv.text((sx + len(left) * cell / 2, yy + 96), f'x = {left}', 22, T['blue'], anchor='mt', bold=True)
        cv.text((mx + len(right) * cell / 2, yy + 96), f'y = {y}', 22, T['green'], anchor='mt', bold=True)


def _top(S):
    if 'y' not in S:
        return '先处理特殊情况：负数、0、以 0 结尾的数'
    x, y = S['x'], S['y']
    if S['_line'] == 12:
        return f'翻转一位：`y = y × 10 + x % 10 = {y}`，下一步 x 去掉个位'
    if S['_line'] >= 15:
        return f'`x = {x}`，`y = {y}`，`y // 10 = {y // 10}`'
    if x > y:
        return f'`x = {x} > y = {y}`：后半还没翻转完'
    return f'`x = {x} ≤ y = {y}`：==翻转到一半了=='


def _while(S, B, ret):
    x, y = B.x, B.y
    if x > y:
        return f'`x = {x} > y = {y}` → 翻转的后半还没追上，继续'
    if len(str(y)) > len(str(x)):
        return f'`x = {x}` 不再大于 `y = {y}` → ==翻转过半==：奇数长度，y 多带了正中间那位'
    return f'`x = {x}` 不再大于 `y = {y}` → ==正好翻转了一半=='


def _cmp(S, B, ret):
    x, y = S.x, S.y
    if x == y:
        return f'`x == y == {x}`：==偶数长度==，前半 = 后半翻转 → 是回文'
    if x == y // 10:
        return f'`x = {x} == y // 10 = {y // 10}`：==奇数长度==，较大的 y 整除 10 去掉中间位再比 → 是回文'
    return f'`x = {x}`，`y = {y}`：两种比较都不相等 → 不是回文'


CONFIG = dict(
    num=9, title='回文数', difficulty='Easy', category='数学',
    author='yiduobo', technique='整数翻转一半',
    tags=['字节30天', '面试经典150'],
    code='''
class Solution(object):
    def isPalindrome(self, x):
        if x < 0:
            return False
        if x == 0:
            return True
        if x % 10 == 0:
            return False

        y = 0
        while x > y:
            y = y * 10 + x % 10
            x //= 10

        if x == y or x == y // 10:
            return True

        return False
''',
    call='''Solution().isPalindrome(0)
Solution().isPalindrome(1221)
Solution().isPalindrome(12321)''',
    expect=True,
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='custom', draw=_whole, h=180),
        dict(type='string', var=lambda S: _digits(S, 'x'), label='x（黄 = 下一个要翻转的个位 x % 10）', cell=92,
             color=lambda S, i, v: 'yellow' if 'y' in S and i == len(str(S['x'])) - 1 and S['_line'] < 15 else None),
        dict(type='string', var=lambda S: _digits(S, 'y'), label='y（x 的后半部分翻转后得到的数）', cell=92,
             color=lambda S, i, v: 'green'),
        dict(type='text', fn=lambda S: '依次运行三个输入：`0` → `1221`（偶数长度）→ `12321`（奇数长度）', size=24),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'green'), ('y // 10', 'y // 10')],
    captions={
        'if x < 0': lambda S, B, ret: (f'`x = {B.x}` 是负数 → 一定不是回文' if B.x < 0 else f'`x = {B.x}` 不是负数'),
        'if x == 0': lambda S, B, ret: ('`x == 0`：==0 是符合要求的== → 直接返回 `True`' if B.x == 0 else f'`x = {B.x}` 不是 0'),
        'return True': lambda S, B, ret: ('`0` 本身就是回文数 → `True`' if 'y' not in S else '是回文数 → `True`'),
        'if x % 10 == 0': lambda S, B, ret: (f'`x = {B.x}` 以 0 结尾 → 不可能是回文' if B.x % 10 == 0
                                             else f'`x = {B.x}` 不以 0 结尾 → 按整数翻转的做法继续'),
        'y = 0': '`y` 存 x ==后半部分翻转==后的数，从 0 开始',
        'while x > y': _while,
        'y = y * 10': '取 x 的个位 `{B.x % 10}` 接到 y 后面：`{B.y}×10 + {B.x % 10}` = =={y}==',
        'x //= 10': lambda S, B, ret: (f'x 去掉个位（原文 `x /= 10`，Python 3 要写 `//=`）：`x` → `{S.x}`' if S.y < 10
                                       else f'x 去掉个位：`x` → `{S.x}`'),
        'if x == y or': _cmp,
        'return False': '不是回文 → `False`',
    },
    cards=dict(
        one_liner='把后半部分翻转，翻转到一半就和前半比较',
        complexity='时间 `O(log x)`，空间 `O(1)`',
        problem=['给你一个整数 `x`，判断它是不是==回文数==（正着读和倒着读一样）',
                 '`121` → `true`；`-121` → `false`；`10` → `false`（倒过来是 `01`）'],
        quote='对于其他的情况，都可以按整数翻转的做法，翻转后n / 2位之后比较与前n / 2位是否一样。需要注意的是这里的n如果是奇数，那么需要将较大的数整除10之后再进行比较。',
        quote_src='—— yiduobo 题解',
        idea=['特判三种：==负数==不是；==0== 是；==以 0 结尾==的其他数都不是',
              '`while x > y`：不断把 x 的个位挪到 y 末尾，直到 y 不小于 x',
              '偶数长度比 `x == y`；奇数长度 y 多了中间一位，比 `x == y // 10`'],
        result='`0` → True，`1221` → True，`12321` → True ✓',
        summary=['时间 `O(log x)`：只翻转一半的位数；空间 `O(1)`',
                 '易错：以 0 结尾的正数要先排除，否则 `10` 会被误判（翻转后 y 丢了 0）',
                 '对比灵神：灵神用 `rev < x // 10` 当条件，奇数长度时少循环一次',
                 '原文为 Python 2 写法：`x /= 10`、`y / 10` 已改为 `//`，并删去 docstring'],
    ),
)
