def xn(x):  # 0 到 x 的异或和（与代码里的 xor_n 相同）
    return (x, 1, x + 1, 0)[x % 4]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'n' not in S or 'start' not in S:
        return
    n, st = S['n'], S['start']
    ln = S.get('_line')
    nums = [st + 2 * i for i in range(n)]
    bits = max(4, max(nums).bit_length())
    cv.text((x0 + 18, y0 + 4), f'nums[i] = start + 2i（n = {n}，start = {st}）', 24, T['muted'], bold=True)
    cols = [('i', x0 + 50), ('nums[i]', x0 + 140), ('二进制', x0 + 290), ('>> 1', x0 + 470), ('最低位', x0 + 600)]
    hy = y0 + 62
    for name, cx in cols:
        cv.text((cx, hy), name, 22, T['muted'], anchor='mm', bold=True)
    hi_shift = ln in (4, 6)
    hi_low = ln in (5, 6)
    rh = 46
    for i, v in enumerate(nums):
        y = hy + 30 + i * rh
        b = format(v, f'0{bits}b')
        cv.rect((x0 + 20, y, x0 + 660, y + rh - 6), fill=T['panel2'], r=8)
        cv.text((cols[0][1], y + (rh - 6) / 2), i, 22, T['dim'], anchor='mm', mono=True)
        cv.text((cols[1][1], y + (rh - 6) / 2), v, 24, T['text'], anchor='mm', mono=True, bold=True)
        bw = cv.tlen(b, 26, mono=True)
        bx = cols[2][1] - bw / 2
        cv.text((bx, y + (rh - 6) / 2), b[:-1], 26, T['cyan'] if hi_shift else T['text'], anchor='lm', mono=True, bold=True)
        cv.text((bx + cv.tlen(b[:-1], 26, mono=True), y + (rh - 6) / 2), b[-1], 26,
                T['orange'] if hi_low else T['text'], anchor='lm', mono=True, bold=True)
        cv.text((cols[3][1], y + (rh - 6) / 2), v >> 1, 24, T['cyan'] if hi_shift else T['dim'], anchor='mm', mono=True, bold=True)
        cv.text((cols[4][1], y + (rh - 6) / 2), v & 1, 24, T['orange'] if hi_low else T['dim'], anchor='mm', mono=True, bold=True)
    # 右侧：0..x 的异或和周期表
    tx, ty = x0 + 700, hy - 12
    cv.text((tx, ty), '0 到 x 的异或和', 22, T['muted'], bold=True)
    a = st // 2
    used = {(a + n - 1) % 4, (a - 1) % 4} if ln == 6 else set()
    for r, (k, s) in enumerate([(0, 'x'), (1, '1'), (2, 'x+1'), (3, '0')]):
        yy = ty + 40 + r * 46
        on = k in used
        cv.rect((tx, yy, tx + 290, yy + 38), fill=T['panel2'], r=8, outline=T['yellow'] if on else T['border'], width=3 if on else 1)
        cv.text((tx + 14, yy + 19), f'x % 4 = {k}  →  {s}', 22, T['yellow'] if on else T['text'], anchor='lm', mono=True)
    yb = hy + 30 + n * rh + 18
    lines = []
    if ln in (4, 6):
        lines.append(f'右移一位后是连续整数 `{a}, {a + 1}, …, {a + n - 1}`（`a = start // 2 = {a}`）')
    if ln in (5, 6):
        bb = n & st & 1
        lines.append(f'最低位：`{n}` 个 `{st & 1}` 异或 → `b = {bb}`（只有 n、start 都是奇数时为 1）')
    if ln == 6:
        hi, lo = xn(a + n - 1), xn(a - 1)
        lines.append(f'`{a}^…^{a + n - 1}` = `xor_n({a + n - 1}) ^ xor_n({a - 1})` = `{hi} ^ {lo}` = `{hi ^ lo}`')
        lines.append(f'答案 = `{hi ^ lo} × 2 + {n & st & 1}` = =={(hi ^ lo) * 2 + (n & st & 1)}==')
    for k, t in enumerate(lines):
        cv.rich(x0 + 22, yb + k * 44, t, x1 - x0 - 44, size=25, accent=T['orange'], max_lines=1)


def cap_ret(S, B, ret):
    a, n, b = S.a, S.n, S.b
    hi, lo = xn(a + n - 1), xn(a - 1)
    tail = '（`a - 1 = -1`，Python 里 `-1 % 4 = 3` → 0，正好是空异或和）' if a == 0 else ''
    return f'`(xor_n({a + n - 1}) ^ xor_n({a - 1})) * 2 + b = ({hi} ^ {lo}) * 2 + {b}` = =={ret}=={tail}'


CONFIG = dict(
    num=1486, title='数组异或操作', difficulty='Easy', category='技巧',
    author='灵茶山艾府', technique='O(1) 数学公式 · 拆出最低位 + 前缀异或',
    tags=['List.md'],
    code='''
class Solution:
    def xorOperation(self, n: int, start: int) -> int:
        xor_n = lambda n: (n, 1, n + 1, 0)[n % 4]
        a = start // 2
        b = n & start & 1  # 都为奇数才是 1
        return (xor_n(a + n - 1) ^ xor_n(a - 1)) * 2 + b
''',
    call='''s = Solution()
[s.xorOperation(5, 3), s.xorOperation(4, 6)]''',
    expect=[3, 8],
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='text', fn=lambda S: (f"本次调用：`xorOperation(n = {S['n']}, start = {S['start']})`" if 'n' in S else ''),
             size=26, h=50),
    ],
    watch=[('n', 'n'), ('start', 'start'), ('a', 'a', 'cyan'), ('b', 'b', 'orange')],
    captions={
        'xor_n = lambda': lambda S, B, ret: (f'`xorOperation({S.n}, {S.start})`：`xor_n(x)` 是 `0^1^…^x`，'
                                             f'按 `x % 4` 周期为 4，`O(1)` 算出'),
        'a = start // 2': '所有数==右移一位==：`start + 2i` 变成 `a + i`，`a = {start} // 2 = {a}`',
        'b = n & start & 1': lambda S, B, ret: (
            f'最低位：start 是奇数 → 每个数最低位都是 `1`，`{S.n}` 个 1 是{"奇" if S.n & 1 else "偶"}数个 → `b = {S.b}`'
            if S.start & 1 else f'最低位：start 是偶数 → 每个数最低位都是 `0` → `b = 0`'),
        'return (xor_n': cap_ret,
    },
    cards=dict(
        one_liner='最低位单独算，其余位右移后变成连续整数的异或和，用前缀异或 O(1) 求',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`nums[i] = start + 2*i`（`0 <= i < n`），返回 `nums` 所有元素的==异或和==',
                 '示例：`n = 5, start = 0` → `[0,2,4,6,8]` → `8`',
                 '示例：`n = 4, start = 3` → `[3,5,7,9]` → `8`'],
        before=[dict(heading='0 到 x 的异或和', lines=[
            '偶数 `x` 和 `x+1` 只差最低位：`x ^ (x+1) = 1`',
            '所以从 0 开始==每 4 个数异或和为 0==：`0^1^2^3 = 0`，`4^5^6^7 = 0`……',
            '按 `x % 4` 分类：`x`、`1`、`x+1`、`0`',
            '`a ^ … ^ (a+n-1)` = `xor_n(a+n-1) ^ xor_n(a-1)`：`0..a-1` 出现两次，抵消'])],
        quote='设 `a = floor(start/2)`，`b` 为异或和的最低位。==只有 n 和 start 都为奇数时 b=1==，其余情况 b=0。那么异或和等于 `(a^(a+1)^…^(a+n-1))·2 + b`。',
        quote_src='—— 灵茶山艾府题解「合二为一」',
        idea=['`start + 2i` 的最低位都和 `start` 相同：奇数个 1 异或得 1，偶数个得 0',
              '其余比特位：右移一位后是 `a, a+1, …, a+n-1`，==连续整数==',
              '连续整数的异或和 = 两个前缀异或和再异或，类比前缀和相减'],
        result='两次调用：`(5, 3)` → `3`（`3^5^7^9^11`），`(4, 6)` → `8`（`6^8^10^12`）✓',
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '方法一（暴力）：逐个异或 `start + 2 * i`，`O(n)`，==刚开始刷题掌握它即可==',
                 '易错：`start` 为奇数时别忘了把最低位 `b` 加回来',
                 '`a = 0` 时 `xor_n(-1)`：Python 中 `-1 % 4 = 3` → `0`，无需特判',
                 '同类：异或的前缀性质，见 1310 子数组异或查询'],
    ),
)
