def _digits(S, key):
    v = S.get(key)
    return list(str(v)) if isinstance(v, int) else None


def _whole(cv, S, B, box, T):
    """把原数字画成一行：蓝 = 还在 x 里（左半），橙 = 已经搬进 rev（右半）"""
    x0, y0, x1, y1 = box
    if not isinstance(S.get('x'), int):
        return
    copying = S['_line'] == 7
    rev = B.get('rev', 0) if copying else S.get('rev', 0)
    left = str(S['x'])
    right = str(rev)[::-1] if rev else ''
    digits = left + right
    cv.text((x0 + 18, y0 + 4), '原来的数字：蓝 = 还在 x 里（左半），橙 = 已搬进 rev（右半）', 24, T['muted'], bold=True)
    cell = 96
    sx = x0 + (x1 - x0 - cell * len(digits)) / 2
    y = y0 + 48
    for k, d in enumerate(digits):
        X = sx + k * cell
        if k < len(left):
            c = T['yellow'] if (copying and k == len(left) - 1) else T['blue']
        else:
            c = T['orange']
        cv.rect((X + 6, y, X + cell - 6, y + 84), fill=c, r=10)
        cv.text((X + cell / 2, y + 42), d, 40, T['bg'], anchor='mm', bold=True)
    if right:
        mx = sx + len(left) * cell
        cv.line([(mx, y - 8), (mx, y + 92)], T['text'], 3)
        cv.text((sx + len(left) * cell / 2, y + 100), f'x = {left}', 22, T['blue'], anchor='mt', bold=True)
        cv.text((mx + len(right) * cell / 2, y + 100), f'倒过来 rev = {rev}', 22, T['orange'], anchor='mt', bold=True)
    elif copying:
        cv.text((sx + len(left) * cell / 2, y + 100), '黄色这一位正在搬进 rev', 22, T['yellow'], anchor='mt', bold=True)


def _cond(S):
    if 'rev' not in S:
        return '特判：负数、或个位为 0 的正数，一定不是回文'
    x, rev = S['x'], S['rev']
    if S['_line'] == 7:
        return f'搬一位：`rev = rev × 10 + x % 10 = {rev}`，下一步再去掉 x 的个位'
    if S['_line'] == 9:
        ok = rev == x or rev == x // 10
        return (f"`rev = {rev}`，`x = {x}`，`x // 10 = {x // 10}` → "
                + ('==回文==' if ok else '==不是回文=='))
    if rev < x // 10:
        return f'`rev = {rev} < x // 10 = {x // 10}`：右半还没搬到一半'
    return f'`rev = {rev} ≥ x // 10 = {x // 10}`：右半已经搬到一半 → 停'


def _sp(S, B, ret):
    x = B.x
    if x < 0:
        return f'`x = {x}` 是==负数==：倒过来读负号在末尾 → 一定不是回文'
    if x > 0 and x % 10 == 0:
        return f'`x = {x}` 个位是 0，但最高位不可能是 0 → ==一定不是回文=='
    return f'`x = {x}`：非负，且个位不是 0 → 特判不成立，开始反转右半'


def _while(S, B, ret):
    rev, x = B.rev, B.x
    if rev < x // 10:
        return f'`rev = {rev} < x // 10 = {x // 10}` → 右半还==没追上==左半，继续搬一位'
    return f'`rev = {rev}` 不小于 `x // 10 = {x // 10}` → ==已处理一半==，退出循环'


def _ret(S, B, ret):
    rev, x = B.rev, B.x
    if rev == x:
        return f'`rev == x == {x}`：==偶数长度==回文，左半 = 右半反转 → `True`'
    if rev == x // 10:
        return f'`rev == x // 10 == {rev}`：==奇数长度==回文，x 末位是正中间那位，不用比 → `True`'
    return f'`rev = {rev}`，`x = {x}`：两种情况都不相等 → `False`'


CONFIG = dict(
    num=9, title='回文数', difficulty='Easy', category='数学',
    author='灵茶山艾府', technique='只反转一半数字',
    tags=['字节30天', '面试经典150'],
    code='''
class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0 or x > 0 and x % 10 == 0:
            return False
        rev = 0
        while rev < x // 10:
            rev = rev * 10 + x % 10
            x //= 10
        return rev == x or rev == x // 10
''',
    call='''Solution().isPalindrome(10)
Solution().isPalindrome(1221)
Solution().isPalindrome(121)''',
    expect=True,
    views=[
        dict(type='text', fn=_cond, size=28),
        dict(type='custom', draw=_whole, h=190),
        dict(type='string', var=lambda S: _digits(S, 'x'), label='x（还没处理的左半部分；黄 = 个位 x % 10）', cell=96,
             color=lambda S, i, v: 'yellow' if 'rev' in S and i == len(str(S['x'])) - 1 and S['_line'] != 9 else None),
        dict(type='string', var=lambda S: _digits(S, 'rev'), label='rev（右半部分反转后拼成的数）', cell=96,
             color=lambda S, i, v: 'orange'),
        dict(type='text', fn=lambda S: '三个输入依次运行：`10` → `1221`（偶数长度）→ `121`（奇数长度）', size=24),
    ],
    watch=[('x', 'x', 'blue'), ('rev', 'rev', 'orange'), ('x // 10', 'x // 10')],
    captions={
        'if x < 0 or': _sp,
        'return False': '特判命中 → 返回 `False`，不用循环',
        'rev = 0': '`rev = 0`：用来存 x ==右半部分反转==后的数',
        'while rev < x // 10': _while,
        'rev = rev * 10': '把 x 的个位 `{B.x % 10}` 接到 rev 末尾：`{B.rev}×10 + {B.x % 10}` = =={rev}==',
        'x //= 10': '去掉 x 的个位：`x` 变成 `{x}`',
        'return rev == x': _ret,
    },
    cards=dict(
        one_liner='只反转右半部分，和左半部分比较',
        complexity='时间 `O(log x)`，空间 `O(1)`',
        problem=['给你一个整数 `x`，判断它是不是==回文数==（正着读和倒着读一样）',
                 '`121` → `true`；`-121` → `false`；`10` → `false`（倒过来是 `01`）',
                 '进阶：不把整数转成字符串'],
        quote='对于回文数来说，只需判断 x 的左半部分是否等于右半部分就行。当 x 是奇数长度回文数时，这个做法比官方题解少循环一次。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x % 10` 取个位，`x //= 10` 去个位；`rev * 10 + 个位` 把它接到 rev 末尾',
              '只要 `rev < x // 10` 就继续搬 → 搬到一半就停',
              '偶数长度：`rev == x`；奇数长度：`rev == x // 10`（x 多出正中间一位）'],
        result='`10` → False，`1221` → True，`121` → True ✓',
        summary=['时间 `O(log x)`：只循环约一半的位数；空间 `O(1)`',
                 '先特判：负数不是回文；==个位是 0 的正数==也不是（`0` 本身是）',
                 '循环条件 `rev < x // 10`：奇数长度时比 `rev < x` 少循环一次',
                 '字符串写法一行：`s == s[::-1]`'],
    ),
)
