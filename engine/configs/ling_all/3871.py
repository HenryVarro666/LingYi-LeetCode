N0 = 1234567


def _done(S, low):
    # ans 已包含 low 这一项：ans 至少等于前面各项 + 本项
    n, tot, l = S['n'], 0, 1000
    while l <= low:
        tot += n - l + 1
        l *= 1000
    return S['ans'] >= tot


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S['n']
    low = S.get('low')
    line = S.get('_line', 0)
    digits = f'{n:,}'
    cv.text((x0 + 18, y0 + 4), f'n = {n}：从右往左，第 k 个逗号出现在 [1000^k, n] 的每个数里', 24, T['muted'], bold=True)
    cw = 62
    tw = len(digits) * cw
    sx = x0 + ((x1 - x0) - tw) / 2
    ys = y0 + 70
    ncomma = digits.count(',')
    cur_k = None
    if low is not None:
        k, v = 1, 1000
        while v < low:
            v *= 1000
            k += 1
        cur_k = k if v == low else None
    # 逗号从右数第 j 个
    cnt = 0
    for idx in range(len(digits) - 1, -1, -1):
        ch = digits[idx]
        X = sx + idx * cw
        if ch == ',':
            cnt += 1
            col = T['text']
            if cur_k == cnt:
                col = T['yellow']
                cv.rect((X + 4, ys - 6, X + cw - 4, ys + 84), fill=T['yellow'], alpha=60, r=10)
            elif cur_k is not None and cnt < cur_k or (cur_k is None and low is not None and cnt <= ncomma and 1000 ** cnt < low):
                col = T['green']
            cv.text((X + cw / 2, ys + 40), ',', 66, col, anchor='mm', bold=True, mono=True)
            cv.text((X + cw / 2, ys + 100), f'#{cnt}', 20, col, anchor='mt', bold=True)
        else:
            cv.text((X + cw / 2, ys + 40), ch, 66, T['text'], anchor='mm', bold=True, mono=True)
    # 每个逗号的贡献条
    yb = ys + 170
    cv.text((x0 + 18, yb - 40), '每个逗号出现的数：[low, n] 占 [1, n] 的比例（条长）和个数', 22, T['muted'], bold=True)
    bx0, bx1 = x0 + 90, x1 - 260
    k, v = 1, 1000
    rows = []
    while v <= n:
        rows.append((k, v))
        k += 1
        v *= 1000
    for k, v in rows:
        y = yb + (k - 1) * 90
        started = low is not None and (v < low or v == low)
        counted = low is not None and (v < low or (v == low and line >= 8 and _done(S, v)))
        col = T['green'] if counted else (T['yellow'] if v == low else T['panel2'])
        cv.text((x0 + 18, y + 24), f'#{k}', 26, T['text'], anchor='lm', bold=True)
        cv.rect((bx0, y + 6, bx1, y + 42), fill=T['panel2'], r=8, outline=T['border'])
        if started:
            xs = bx0 + (bx1 - bx0) * (v - 1) / n
            cv.rect((xs, y + 6, bx1, y + 42), fill=col, r=8, alpha=230)
        cv.text((bx0, y + 46), f'low = 10^{3 * k}', 18, T['dim'], anchor='lt', mono=True)
        if counted:
            cv.text((bx1 + 14, y + 24), f'{n - v + 1}', 26, col, anchor='lm', bold=True, mono=True)
    tot = S.get('ans', 0)
    cv.text((x1 - 14, y1 - 10), f'ans = {tot}', 30, T['green'], anchor='rb', bold=True, mono=True)


CONFIG = dict(
    num=3871, title='统计范围内的逗号 II', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='贡献法：数每个逗号出现在几个数里',
    tags=['灵神题单·动态规划', '灵神题单·贪心与思维', '难度分 1381'],
    code='''
class Solution:
    def countCommas(self, n: int) -> int:
        ans = 0
        # 从低到高，枚举逗号的位置
        low = 1000
        while low <= n:
            # [low, n] 中的每个数都在这个位置上有一个逗号
            ans += n - low + 1
            low *= 1000
        return ans
''',
    call=f'Solution().countCommas({N0})',
    expect=1468136,
    views=[
        dict(type='custom', draw=_draw, h=560),
        dict(type='text', h=60, size=26,
             fn=lambda S: (f"本轮：`n - low + 1` = `{S['n']} - {S['low']} + 1` = =={S['n'] - S['low'] + 1}==" if 'low' in S and S['low'] <= S['n'] and S.get('_line', 0) in (8, 9)
                           else ('`low > n`：更高位的逗号没有数能用到，结束' if S.get('low', 0) > S['n'] else ''))),
    ],
    watch=[('n', 'n', 'blue'), ('low', 'low', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 累计逗号总数；不逐个数去数，而是==站在逗号的角度==数',
        'low = 1000': '最右边的逗号从 `1000` 起才会出现：`low = {low}`',
        'while low <= n': lambda S, B, r: (f'`low = {S.low} <= n = {S.n}`：[low, n] 非空，这个位置的逗号要数' if S.low <= S.n
                                           else f'`low = {S.low} > n = {S.n}`：更高位的逗号一个也用不上 → 结束'),
        'ans += n - low + 1': '[{low}, {n}] 每个数都有这个逗号：`{n} - {low} + 1` = =={n - low + 1}==，`ans` → {ans}',
        'low *= 1000': '下一个逗号要再多三位才出现：`low` → =={low}==',
        'return ans': '所有逗号位置累加完毕，一共 `{ans}` 个逗号',
    },
    cards=dict(
        one_liner='横看成岭侧成峰：数每个逗号出现在几个数里',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['把 `1..n` 都写成千分位格式（`1,000`、`1,000,000`），问一共写了多少个逗号',
                 '`n` 最大 `10^15`，不能逐个数去数',
                 '示例：`n = 1002` → `3`；`n = 998` → `0`；本视频 `n = 1234567`'],
        quote='最右边的逗号，出现在 [10^3, n] 的每个整数中。这有 n-10^3+1 个。',
        quote_src='—— 灵茶山艾府题解',
        idea=['换个角度：不数「每个数有几个逗号」，而数「每个逗号出现在几个数里」',
              '第 k 个逗号出现在 `[1000^k, n]` 的每个数中，共 `n - 1000^k + 1` 个',
              '`low` 每次乘 1000，累加到超过 `n` 为止'],
        summary=['时间 `O(log n)`：`low` 每轮乘 1000，最多 5 轮',
                 '循环条件是 `low <= n`；`n < 1000` 时一轮也不进，答案 0',
                 '题解还给了等比数列求和的 `O(1)` 公式：`k(n+1) - (10^(3k+3) - 1000)/999`',
                 '同类思路：贡献法，换成「每个元素被几个答案用到」'],
    ),
)
