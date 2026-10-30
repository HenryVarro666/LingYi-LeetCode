CALLS = [(5, 3), (3, 0)]
ORIG = dict(CALLS)  # n -> 原始 start（代码里 start 会被右移覆盖，画表时要用原值）


def ps(x):  # 与代码中的 prefix_s 相同
    return (x, 1, x ^ 1, 0)[x % 4]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'n' not in S:
        return
    n = S['n']
    st0 = ORIG.get(n, S['start'])
    ln = S.get('_line')
    shifted = 'end' in S or ln == 8
    nums = [st0 + 2 * i for i in range(n)]
    bits = max(4, max(nums).bit_length())
    cv.text((x0 + 18, y0 + 4), f'nums[i] = start + 2 * i（n = {n}，start = {st0}）', 24, T['muted'], bold=True)
    cols = [('nums[i]', x0 + 90), ('二进制', x0 + 240), ('>> 1', x0 + 410), ('最后一位', x0 + 560)]
    hy = y0 + 62
    for name, cx in cols:
        cv.text((cx, hy), name, 22, T['muted'], anchor='mm', bold=True)
    rh = 46
    low_on = ln in (3, 4, 6) or 'suffix' in S
    for i, v in enumerate(nums):
        y = hy + 30 + i * rh
        b = format(v, f'0{bits}b')
        cv.rect((x0 + 20, y, x0 + 640, y + rh - 6), fill=T['panel2'], r=8)
        cy = y + (rh - 6) / 2
        cv.text((cols[0][1], cy), v, 24, T['text'], anchor='mm', mono=True, bold=True)
        bw = cv.tlen(b, 26, mono=True)
        bx = cols[1][1] - bw / 2
        cv.text((bx, cy), b[:-1], 26, T['cyan'] if shifted else T['text'], anchor='lm', mono=True, bold=True)
        cv.text((bx + cv.tlen(b[:-1], 26, mono=True), cy), b[-1], 26, T['orange'] if low_on else T['text'],
                anchor='lm', mono=True, bold=True)
        cv.text((cols[2][1], cy), v >> 1, 24, T['cyan'] if shifted else T['dim'], anchor='mm', mono=True, bold=True)
        cv.text((cols[3][1], cy), v & 1, 24, T['orange'] if low_on else T['dim'], anchor='mm', mono=True, bold=True)
    # 右侧：prefix_s 的四种情况
    tx, ty = x0 + 680, hy - 12
    cv.text((tx, ty), 'prefix_s(x) = 0^1^…^x', 22, T['muted'], bold=True)
    inner = S.get('_inner', {})
    cur = inner.get('x') if 18 <= (ln or 0) <= 25 else None
    for r, (k, s) in enumerate([(0, 'x'), (1, '1'), (2, 'x ^ 1'), (3, '0')]):
        yy = ty + 40 + r * 46
        on = cur is not None and cur % 4 == k
        cv.rect((tx, yy, tx + 310, yy + 38), fill=T['panel2'], r=8, outline=T['yellow'] if on else T['border'],
                width=3 if on else 1)
        cv.text((tx + 14, yy + 19), f'x % 4 = {k}  →  {s}', 22, T['yellow'] if on else T['text'], anchor='lm', mono=True)
    if cur is not None:
        cv.text((tx, ty + 40 + 4 * 46 + 8), f'当前 x = {cur}', 22, T['yellow'], bold=True)
    yb = hy + 30 + n * rh + 24
    lines = []
    if 'suffix' in S:
        lines.append(f'最后一位 `suffix = {S["suffix"]}`（n、start 都为奇数时才是 1）')
    if 'end' in S:
        lines.append(f"右移后是 `start' = {S['start']}` 到 `end = {S['end']}` 的连续整数")
    if 'res' in S:
        lines.append(f"`res = {S['res']}`" + ("（start' = 0，不用再异或前缀）" if S['start'] == 0 and ln in (12, 15) else ''))
    for k, t in enumerate(lines):
        cv.rich(x0 + 22, yb + k * 44, t, x1 - x0 - 44, size=25, accent=T['orange'], max_lines=1)


def cap_suffix_if(S, B, ret):
    n, s = S.n, S.start
    if n & 1 and s & 1:
        return f'`n = {n}`、`start = {s}` 都是奇数：奇数个最后一位 1 异或 → 答案最后一位是 1'
    if s & 1:
        return f'`start = {s}` 是奇数但 `n = {n}` 是偶数：偶数个 1 异或为 0'
    return f'`start = {s}` 是偶数：所有数最后一位都是 0 → 答案最后一位是 0'


def cap_pref(k):
    def f(S, B, ret):
        x = S.x
        if x % 4 == k:
            return f'`x = {x}`，`x % 4 = {k}` ✓'
        if k == 0:
            return f'`prefix_s({x})`：按 `x % 4` 分四种情况，`{x} % 4 = {x % 4}`，不是 0'
        return f'`x % 4 = {x % 4}`，不是 {k}'
    return f


CONFIG = dict(
    num=1486, title='数组异或操作', difficulty='Easy', category='技巧',
    author='yiduobo', technique='确定最后一位 + 前缀异或 prefix_s',
    tags=['List.md'],
    code='''
class Solution(object):
    def xorOperation(self, n, start):
        if n & 1 and start & 1:
            suffix = 1
        else:
            suffix = 0

        start >>= 1
        end = start + n - 1

        res = self.prefix_s(end)
        if start > 0:
            res ^= self.prefix_s(start - 1)

        return (res << 1) + suffix

    def prefix_s(self, x):
        if x % 4 == 0:
            return x
        elif x % 4 == 1:
            return 1
        elif x % 4 == 2:
            return x ^ 1
        else:
            return 0
''',
    call=f'''s = Solution()
[s.xorOperation(n, start) for n, start in {CALLS!r}]''',
    expect=[3, 6],
    views=[
        dict(type='custom', draw=_draw, h=480),
        dict(type='calls', h=145),
    ],
    watch=[('n', 'n'), ('start', 'start'), ('suffix', 'suffix', 'orange'), ('end', 'end', 'cyan'), ('res', 'res', 'green')],
    captions={
        'if n & 1 and start & 1': cap_suffix_if,
        'suffix = 1': '`suffix = 1`',
        'suffix = 0': '`suffix = 0`',
        'start >>= 1': "去掉最后一位：`start' = start >> 1 = {start}`，`nums[i] >> 1` 就是 `start' + i`",
        'end = start + n - 1': "要算的是 `{start} ^ {start + 1} ^ … ^ {end}`：==连续整数的异或==",
        'res = self.prefix_s(end)': '前缀异或：先算 `prefix_s({end})` = `0 ^ 1 ^ … ^ {end}`',
        'if start > 0': lambda S, B, ret: (f"`start' = {S.start} > 0` → 还要异或掉 `prefix_s({S.start - 1})`" if S.start > 0
                                           else "`start' = 0`：前缀本来就从 0 开始，==不需要再异或== `prefix_s(-1)`"),
        'res ^= self.prefix_s': lambda S, B, ret: f"`res = prefix_s({B.end}) ^ prefix_s({B.start - 1})`：`0..{B.start - 1}` 出现两次，抵消",
        'return (res << 1) + suffix': '`res = {res}` 左移一位再加上最后一位：`({res} << 1) + {suffix}` = =={ret}==',
        'if x % 4 == 0': cap_pref(0),
        'elif x % 4 == 1': cap_pref(1),
        'elif x % 4 == 2': cap_pref(2),
        'return x ^ 1': '`x = 4k+2`：`0..x-1` 两两一组共奇数组 → 异或为 1，再 `^ x` → `{ret}`',
        'return x': '`x = 4k`：`0..x-1` 两两一组共偶数组 → 异或为 0，再 `^ x` → `{ret}`',
        'return 1': '`x = 4k+1`：`0..x` 两两一组共奇数组，每组异或为 1 → `1`',
        'return 0': '`x = 4k+3`：`0..x` 两两一组共偶数组 → `0`',
    },
    cards=dict(
        one_liner='先确定答案的最后一位，其余位变成连续整数的异或，用前缀异或 O(1) 求',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`nums[i] = start + 2*i`（`0 <= i < n`），返回 `nums` 所有元素的==异或和==',
                 '示例：`n = 5, start = 0` → `[0,2,4,6,8]` → `8`',
                 '本视频跑两组：`(5, 3)` 和 `(3, 0)`'],
        before=[dict(heading='yiduobo：prefix_s 的四种情况', lines=[
            '偶数 `x` 一定形如 `XX…X0`，`x+1` 形如 `XX…X1` → `x ^ (x+1) = 1`',
            '`i = 4k`：`0..i-1` 分成 `2k` 组 → 0，再 `^ i` → `i`',
            '`i = 4k+1` → `1`；`i = 4k+2` → `1 ^ i`；`i = 4k+3` → `0`'])],
        quote='若start和n都为奇数时，答案的最后一位为1，否则最后一位为0。确定了最后一位之后……==无需再考虑最后一位了==。',
        quote_src='—— yiduobo 知乎题解',
        idea=['`res = ((nums[0]>>1) ^ … ^ (nums[n-1]>>1)) << 1) + suffix`',
              "`nums[i] >> 1 = start' + i` 是连续整数 → 用两个前缀异或相消",
              "原文特别提醒：`start' = 0` 时不需要再异或 `prefix_s[start'-1]`"],
        result='两组都对：`(5, 3)` → `3^5^7^9^11 = 3`，`(3, 0)` → `0^2^4 = 6` ✓',
        summary=['时间 `O(1)`，空间 `O(1)`；数据范围小时直接循环暴力也可以',
                 '关键：拆成「最后一位」和「其余位」两部分分别算',
                 "易错：`start' = 0` 时 `start' - 1 = -1`，原文用 `if start > 0` 跳过",
                 '原文为 Python 2 风格：删去了文档字符串，逻辑未改',
                 '对比灵神：思路相同，他用 `(n, 1, n+1, 0)[n % 4]` 一行写出 `xor_n`'],
    ),
)
