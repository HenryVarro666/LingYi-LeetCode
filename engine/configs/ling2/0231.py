NUMS = (16, 12, 1, 0)
W = 6  # 显示的二进制位数


def _bits(cv, T, x, y, val, cell, color, label, sub):
    cv.text((x - 30, y + cell / 2), label, 26, T['text'], anchor='rm', bold=True, mono=True)
    cv.text((x - 30, y + cell / 2 + 30), sub, 20, T['dim'], anchor='rm', mono=True)
    s = format(val, f'0{W}b')
    for i, ch in enumerate(s):
        X = x + i * cell
        one = ch == '1'
        cv.rect((X + 4, y + 4, X + cell - 4, y + cell - 4), fill=T[color] if one else T['panel2'], r=8,
                outline=T['border'], width=1)
        cv.text((X + cell / 2, y + cell / 2), ch, 32, T['bg'] if one else T['dim'], anchor='mm', bold=True, mono=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '二进制视角：n、n − 1、n & (n − 1)', 24, T['muted'], bold=True)
    n = S.get('n')
    if n is None:
        return
    cell = 78
    x = x0 + 300
    if n <= 0:
        cv.text((x0 + 60, y0 + 110), f'n = {n} ≤ 0', 40, T['red'], bold=True, mono=True)
        cv.text((x0 + 60, y0 + 180), '不可能是 2 的幂（2^x 总是正数）', 28, T['text'], bold=True)
        cv.text((x0 + 60, y0 + 230), 'and 短路：后面的 n & (n − 1) 根本不算', 24, T['muted'])
        if n == 0:
            cv.text((x0 + 60, y0 + 310), '注意：0 & (0 − 1) = 0 & (−1) = 0', 26, T['orange'], bold=True, mono=True)
            cv.text((x0 + 60, y0 + 352), '如果漏掉 n > 0，0 会被误判成 2 的幂！', 26, T['orange'], bold=True)
        return
    for i in range(W):
        cv.text((x + i * cell + cell / 2, y0 + 50), f'2^{W - 1 - i}', 18, T['dim'], anchor='mm', mono=True)
    _bits(cv, T, x, y0 + 75, n, cell, 'blue', f'n = {n}', '')
    _bits(cv, T, x, y0 + 175, n - 1, cell, 'purple', f'n − 1 = {n - 1}', '')
    cv.line([(x - 10, y0 + 268), (x + W * cell + 10, y0 + 268)], T['border'], 3)
    r = n & (n - 1)
    _bits(cv, T, x, y0 + 285, r, cell, 'red' if r else 'green', f'n & (n−1) = {r}', '')
    msg = (f'只有一个 1：减一后它变 0、右边全变 1 → 与运算 ==全 0== → 是 2 的幂' if r == 0
           else '至少两个 1：减一碰不到最高位的 1 → 与运算 ==不为 0== → 不是 2 的幂')
    cv.rich(x0 + 30, y0 + 395, msg, x1 - x0 - 60, size=25, accent=T['orange'], max_lines=2)


CONFIG = dict(
    num=231, title='2 的幂', difficulty='Easy', category='技巧',
    author='灵茶山艾府', technique='位运算 · n & (n − 1)',
    tags=['List.md'],
    code='''
class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        return n > 0 and n & (n - 1) == 0
''',
    call=f'''s = Solution()
[s.isPowerOfTwo(x) for x in {NUMS}]''',
    expect=[True, False, True, False],
    views=[
        dict(type='custom', draw=_draw, h=500),
        dict(type='text', h=60, size=26, fn=lambda S: f'依次测试 `n = {", ".join(map(str, NUMS))}`'),
    ],
    watch=[('n', 'n', 'blue'), ('n - 1', 'n - 1', 'purple'), ('n & (n - 1)', 'n & (n - 1)')],
    captions={
        'return n > 0 and': lambda S, B, ret: (
            f'`n = {S.n} > 0`，`{S.n} & {S.n - 1} = {S.n & (S.n - 1)}` → 返回 `{ret}`' + ('：==是== 2 的幂' if ret else '：不是 2 的幂')
            if S.n > 0 else f'`n = {S.n}` 不大于 0 → 直接返回 `False`（短路，不算后半部分）'),
    },
    cards=dict(
        one_liner='2 的幂的二进制只有一个 1：n & (n − 1) 恰好为 0',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给你整数 `n`（可能为负数或 0），判断它是不是 2 的幂',
                 '即是否存在整数 `x` 使 `n == 2^x`',
                 '示例：`1` → `true`，`16` → `true`，`3` → `false`',
                 '进阶：不用循环 / 递归'],
        before=[dict(heading='二进制的样子', lines=[
            '2 的幂形如 `100…0`：`4 = 100`，`8 = 1000`，`16 = 10000`',
            '`8 = 1000`，`8 − 1 = 0111` → `8 & 7 = 0`',
            '`9 = 1001`，`9 − 1 = 1000` → `9 & 8 = 1000 ≠ 0`',
        ])],
        quote='如果 n 是 2 的幂，把 n 减一会使 n 的最高位变成 0，其余位变成 1，所以 n&(n−1) 一定是 0。反之……n 的二进制至少有两个 1。把 n 减一，并不会影响 n 最高位的 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`n > 0` 时：`n & (n − 1) == 0` ⇔ 二进制只有一个 1 ⇔ 是 2 的幂',
              '`n ≤ 0` 一定不是 2 的幂，用 `and` 短路一并处理',
              '一行代码，`O(1)`'],
        result='四个测试：`[True, False, True, False]` ✓',
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错：别漏了 `n > 0`，否则 `n = 0` 时 `0 & -1 = 0` 会误判为 True',
                 'Python 中 `&` 优先级低于 `-`、高于 `==`，`n & (n - 1) == 0` 正好是想要的含义',
                 '`n & (n − 1)` = 去掉最低位的 1，可用来枚举、统计比特 1（如 191 题）'],
    ),
)
