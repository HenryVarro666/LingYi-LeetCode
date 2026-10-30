def _b(x, m):
    return format(x, f'0{m}b')[-m:] if m else ''


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S['n']
    k = S['k']
    line = S.get('_line', 0)
    cv.text((x0 + 18, y0 + 4), f'二进制逐位：n = {n}，n & x = 0 → n 为 1 的位 x 只能填 0', 24, T['muted'], bold=True)
    if 'm' not in S:
        # 还在 sumOfGoodIntegers：展示区间 [low, high]
        low, high = max(n - k, 1), n + k
        cv.text((x0 + 30, y0 + 90), f'n = {n} = {n:b}（二进制）', 34, T['text'], mono=True, bold=True)
        cv.text((x0 + 30, y0 + 160), f'区间 [max(n−k, 1), n+k] = [{low}, {high}]', 34, T['cyan'], mono=True, bold=True)
        cv.text((x0 + 30, y0 + 240), '答案 = calc(high+1) − calc(low)', 34, T['yellow'], mono=True, bold=True)
        cv.text((x0 + 30, y0 + 300), 'calc(h)：所有小于 h 的正整数里，满足 AND n = 0 的数之和', 26, T['muted'])
        return
    m = S['m']
    h = S['high']
    cur = S.get('i')
    rows = [('n', n, T['text']), ('high', h, T['cyan']), ('prefix', S.get('prefix', 0), T['blue']), ('free_mask', S.get('free_mask', 0), T['green'])]
    cell = min(120, (x1 - x0 - 330) / m)
    sx = x0 + 250
    ys = y0 + 110
    rh = 96
    for c in range(m):
        bit = m - 1 - c
        X = sx + c * cell
        cv.text((X + cell / 2, ys - 34), f'第{bit}位', 20, T['dim'], anchor='mm', mono=True)
    if cur is not None and 0 <= cur < m:
        X = sx + (m - 1 - cur) * cell
        cv.rect((X + 2, ys - 6, X + cell - 2, ys + rh * len(rows)), outline=T['yellow'], width=5, r=12)
    for r, (name, val, col) in enumerate(rows):
        y = ys + r * rh
        cv.text((x0 + 30, y + rh / 2 - 10), name, 28, col, anchor='lm', bold=True, mono=True)
        for c in range(m):
            bit = m - 1 - c
            X = sx + c * cell
            v = val >> bit & 1
            fill = T['panel2']
            tc = T['dim']
            if name == 'n' and v:
                fill, tc = T['pink'], T['bg']
            elif name == 'high' and v:
                fill, tc = T['cyan'], T['bg']
            elif name == 'prefix' and v:
                fill, tc = T['blue'], T['bg']
            elif name == 'free_mask' and v:
                fill, tc = T['green'], T['bg']
            cv.rect((X + 8, y + 4, X + cell - 8, y + rh - 22), fill=fill, r=10, outline=T['border'])
            cv.text((X + cell / 2, y + (rh - 18) / 2), str(v), 40, tc, anchor='mm', bold=True, mono=True)
    yb = ys + rh * len(rows) + 14
    cv.text((x0 + 30, yb), f"free_cnt = {S.get('free_cnt', 0)}    res = {S.get('res', 0)}", 28, T['yellow'], bold=True, mono=True)
    cv.text((x0 + 30, yb + 46), '粉 = n 的 1 位（不能填 1）；绿 = 自由位', 22, T['muted'])


def _cap_if_high(S, B, ret):
    i = S.i
    if S.high >> i & 1:
        return f'`high` 第 {i} 位是 ==1==：这一位填 `0` 就比 high 小，后面的位都自由，先把这部分算进来'
    return f'`high` 第 {i} 位是 0：这一位只能填 0（不能超过 high），直接看下一位'


def _cap_pre(S, B, ret):
    return (f'前缀 `prefix = {S.prefix}` 出现在后面 `{S.free_cnt}` 个自由位的每种填法里：'
            f'`{S.prefix} << {S.free_cnt}` = =={S.prefix << S.free_cnt}==，`res` → {S.res}')


def _cap_suf(S, B, ret):
    add = S.free_mask * (1 << S.free_cnt >> 1)
    return (f'每个自由位固定为 1 时，其余 `{max(S.free_cnt - 1, 0)}` 位随便填（`{(1 << S.free_cnt >> 1)}` 种）：'
            f'`{S.free_mask} * {(1 << S.free_cnt >> 1)}` = =={add}==，`res` → {S.res}')


CONFIG = dict(
    num=3954, title='区间内的兼容数字之和 I', difficulty='Easy', category='动态规划',
    author='灵茶山艾府', technique='贡献法：逐位拆出 < high 的合法数之和',
    tags=['灵神题单·动态规划'],
    code='''
class Solution:
    # 计算小于 high 的正整数中，AND n 等于 0 的数之和
    def calc(self, high: int, n: int) -> int:
        m = high.bit_length()
        free_mask = ((1 << m) - 1) & ~n
        free_cnt = free_mask.bit_count()
        res = prefix = 0

        for i in range(m - 1, -1, -1):
            if n >> i & 1 == 0:
                free_cnt -= 1
                free_mask ^= 1 << i

            if high >> i & 1:
                # 这一位填 0
                res += prefix << free_cnt  # 前缀的贡献：后面 free_cnt 个位置，0 和 1 随便填
                res += free_mask * (1 << free_cnt >> 1)  # 后缀的贡献：每个 free 位置固定为 1 时，其余 free_cnt-1 个位置 0 和 1 随便填

                # 这一位填 1，继续计算
                if n >> i & 1:  # 这一位不能填 1
                    break
                prefix |= 1 << i

        return res

    def sumOfGoodIntegers(self, n: int, k: int) -> int:
        low = max(n - k, 1)
        high = n + k
        return self.calc(high + 1, n) - self.calc(low, n)
''',
    call='Solution().sumOfGoodIntegers(2, 3)',
    expect=10,
    skip=['m = high.bit_length', 'res = prefix = 0'],
    views=[
        dict(type='custom', draw=_draw, h=500),
    ],
    watch=[('i', 'i', 'yellow'), ('high', 'high', 'cyan'), ('free_cnt', 'free_cnt', 'green'), ('prefix', 'prefix', 'blue'), ('res', 'res', 'orange')],
    captions={
        'free_mask = ((1 << m)': '`n` 为 1 的位 `x` 只能填 0；其余位是自由位：`free_mask` = =={free_mask:b}==（二进制）',
        'free_cnt = free_mask': '自由位有 `{free_cnt}` 个',
        'if n >> i & 1 == 0': lambda S, B, r: (f'`n` 第 {S.i} 位是 0 → 这一位属于自由位，但现在轮到它被决定，不再算「后面的自由位」'
                                               if S.n >> S.i & 1 == 0 else f'`n` 第 {S.i} 位是 1 → 它本来就不是自由位，`x` 这一位只能填 0'),
        'free_cnt -= 1': '后面的自由位少了一个：`free_cnt` → =={free_cnt}==',
        'free_mask ^= 1 << i': '把第 {i} 位从 `free_mask` 去掉：`free_mask` → =={free_mask:b}==（二进制）',
        'if high >> i & 1': _cap_if_high,
        'res += prefix <<': _cap_pre,
        'res += free_mask *': _cap_suf,
        'if n >> i & 1:': lambda S, B, r: (f'`n` 第 {S.i} 位是 1，`x` 不能在这一位填 1 → 再往下就不可能顶着 high 走了，==break=='
                                           if S.n >> S.i & 1 else f'`n` 第 {S.i} 位是 0，可以填 1，继续顶着 `high` 往下'),
        'prefix |= 1 << i': '这一位填 1 并且继续贴着 `high`：`prefix` → =={prefix}==',
        'return res': '`calc` 返回 `{res}`：小于 high 的合法数之和',
        'low = max(n - k, 1)': '下界不能小于 1（要求正整数）：`low` = {low}',
        'high = n + k': '上界 `high` = {high}',
        'return self.calc(high + 1, n)': '答案 = `calc(high+1)` − `calc(low)`：小于 high+1 的合法数之和，减去小于 low 的',
    },
    cards=dict(
        result='`calc(6) − calc(1) = 10 − 0 = 10`',
        one_liner='逐位拆开 < high 的数，每一位的贡献一次算清',
        complexity='时间 `O(log(n+k))`，空间 `O(1)`',
        problem=['正整数 `x` 兼容：`abs(n - x) <= k` 且 `n & x == 0`',
                 '求所有兼容整数之和',
                 '示例：`n = 2, k = 3` → `1 + 4 + 5 = 10`'],
        quote='如果 n 的第 i 位是 1，那么 x 的第 i 位不能填 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先把答案变成 `calc(high+1) − calc(low)`，`calc(h)` 求小于 h 的合法数之和',
              '从高到低看 `high` 的每个 1：这一位填 0，后面自由位随便填',
              '用「贡献法」：前缀贡献 `prefix << free_cnt`，每个自由位固定为 1 时再乘剩余填法数'],
        summary=['时间 `O(log(n+k))`，空间 `O(1)`',
                 '`calc` 求的是 ==小于== high，所以传 `high + 1`；下界传 `low`',
                 '`n` 为 1 的位不能填 1：遇到 `n` 和 `high` 同时为 1 就 break',
                 '本题数据很小（≤100），灵神方法一暴力枚举 `[max(n-k,1), n+k]` 也能过；方法二是上下界数位 DP',
                 '这里选的是最后的优化写法，同模板可做更大数据范围的同类题'],
    ),
)
