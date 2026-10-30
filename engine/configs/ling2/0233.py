N0 = 2103
DIG = str(N0)
POS = ['个位', '十位', '百位', '千位', '万位']


def _contrib(i):
    p = 10 ** i
    mp, M, ms = N0 // (p * 10), N0 // p % 10, N0 % p
    c2 = p if M > 1 else (ms + 1 if M == 1 else 0)
    return mp * p, c2, M


def _pos(S):
    p = S.get('pow10')
    return len(str(p)) - 1 if p else 0


def _row_state(S):
    """返回 (已完成的行数, 当前行 i, 当前行已显示到第几项: 0/1/2)"""
    line = S.get('_line')
    i = _pos(S)
    if line in (None, 3, 4) or 'pow10' not in S:
        return 0, None, 0
    if line in (6, 24, 26):
        return i, None, 0
    if line in (7, 8):
        return i, i, 0
    if line in (12, 14, 21):
        return i, i, 1
    if line == 18:
        return i, i, 2 if S.get('M') == 0 else 1
    if line in (17, 22):
        return i, i, 2
    return i, None, 0


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    done, cur, shown = _row_state(S)
    line = S.get('_line')
    i = _pos(S) if 'pow10' in S else None
    focus = cur if cur is not None else (i if line == 6 and i is not None and 10 ** i <= N0 else None)
    k = len(DIG)
    cv.text((x0 + 18, y0 + 4), f'n = {N0} 拆成  prefix | m | suffix（m = 当前统计的这一位）', 22, T['muted'], bold=True)
    cell = 96
    sx = x0 + (x1 - x0 - cell * k) / 2
    sy = y0 + 64
    for t, ch in enumerate(DIG):
        p = k - 1 - t  # 这一位的 10 的幂次
        fill = T['panel2']
        if focus is not None:
            fill = T['yellow'] if p == focus else (T['blue'] if p > focus else T['pink'])
        cv.rect((sx + t * cell + 4, sy, sx + (t + 1) * cell - 4, sy + cell - 8), fill=fill, r=12)
        cv.text((sx + t * cell + cell / 2, sy + (cell - 8) / 2), ch, 48, T['bg'] if focus is not None else T['text'], anchor='mm', bold=True)
        cv.text((sx + t * cell + cell / 2, sy + cell + 2), POS[p], 18, T['dim'], anchor='mt')
    if focus is not None:
        mp, M, ms = N0 // (10 ** focus * 10), N0 // 10 ** focus % 10, N0 % 10 ** focus
        ly = sy + cell + 36
        items = [('prefix ≤ max_prefix = ' + str(mp), T['blue']), ('M = ' + str(M), T['yellow']),
                 ('suffix ≤ max_suffix = ' + (str(ms) if focus else '（无）'), T['pink'])]
        lx = x0 + 30
        for s, c in items:
            cv.rect((lx, ly + 2, lx + 16, ly + 18), fill=c, r=3)
            cv.text((lx + 24, ly + 10), s, 21, c, anchor='lm', bold=True)
            lx += cv.tlen(s, 21, bold=True) + 64
    # 贡献表
    ty = sy + cell + 92
    cols = [('位', 90), ('情况一 max_prefix·10^i', 300), ('情况二/三/四', 300), ('小计', 150)]
    tx = x0 + (x1 - x0 - sum(w for _, w in cols)) / 2
    X = tx
    for name, w in cols:
        cv.text((X + w / 2, ty), name, 20, T['muted'], anchor='mt', bold=True)
        X += w
    rh = 46
    total = 0
    for r in range(k):
        Y = ty + 32 + r * rh
        c1, c2, M = _contrib(r)
        on = r < done or r == cur
        fill = (60, 52, 30) if r == cur else T['panel2']
        cv.rect((tx, Y, tx + sum(w for _, w in cols), Y + rh - 6), fill=fill if on else T['panel'], r=8,
                outline=T['yellow'] if r == cur else T['border'], width=2 if r == cur else 1)
        vals = [POS[r], '', '', '']
        if r < done or (r == cur and shown >= 1):
            vals[1] = f'{c1}'
        if r < done or (r == cur and shown >= 2):
            tag = '二' if M > 1 else ('三' if M == 1 else '四')
            vals[2] = f'{c2}（情况{tag}）'
        if r < done:
            vals[3] = f'{c1 + c2}'
            total += c1 + c2
        X = tx
        for (name, w), v in zip(cols, vals):
            cv.text((X + w / 2, Y + (rh - 6) / 2), v, 22, T['text'] if on else T['dim'], anchor='mm', bold=True, mono=v[:1].isdigit())
            X += w
    cv.text((tx + sum(w for _, w in cols), ty + 32 + k * rh + 6), f'已完成的位合计 = {total}', 22, T['green'], anchor='ra', bold=True)


def _cap_while(S, B, ret):
    if S.pow10 <= S.n:
        return f'`pow10 = {S.pow10} ≤ {S.n}`：统计==所有数的{POS[_pos(S)]}==上一共出现多少个 1'
    return f'`pow10 = {S.pow10} > {S.n}`：每一位都统计完了'


def _cap_c1(S, B, ret):
    mp, p = S.max_prefix, S.pow10
    if mp == 0:
        return '情况一：`max_prefix = 0`，prefix 没有更小的取法 → `+0`'
    return (f'情况一 prefix < {mp}：prefix 有 `{mp}` 种，m 填 1，suffix 随便填 `{p}` 种'
            f' → `+{mp} × {p} = {mp * p}`')


CONFIG = dict(
    num=233, title='数字 1 的个数', difficulty='Hard', category='数学',
    author='灵茶山艾府', technique='贡献法 · 逐位分类讨论',
    tags=['字节30天'],
    code='''
class Solution:
    def countDigitOne(self, n: int) -> int:
        ans = 0
        pow10 = 1

        while pow10 <= n:
            max_prefix = n // (pow10 * 10)
            M = n // pow10 % 10

            # 1. prefix < max_prefix 时，低位不受约束
            # m 填 1，suffix 随便填
            ans += max_prefix * pow10

            if M > 1:
                # 2. prefix = max_prefix 且 M > 1
                # m 填 1，suffix 随便填
                ans += pow10
            elif M == 1:
                # 3. prefix = max_prefix 且 M = 1
                # m 填 1，suffix 可以填 [0, max_suffix] 中的任意整数
                max_suffix = n % pow10
                ans += max_suffix + 1

            pow10 *= 10

        return ans
''',
    call=f'Solution().countDigitOne({N0})',
    expect=1625,
    views=[
        dict(type='custom', draw=_draw, h=640),
    ],
    watch=[('pow10', 'pow10', 'yellow'), ('max_prefix', 'max_prefix', 'blue'), ('M', 'M', 'yellow'),
           ('max_suffix', 'max_suffix', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans`：`0 ~ n` 所有整数中，数字 1 出现的总次数',
        'pow10 = 1': '横看成岭侧成峰：不枚举每个数，而是==逐位==统计这一位是 1 的数有多少个',
        'while pow10 <= n': _cap_while,
        'max_prefix = n //': lambda S, B, r: f'm 是{POS[_pos(S)]}：`max_prefix = {S.n} // {S.pow10 * 10} = {S.max_prefix}`',
        'M = n // pow10': lambda S, B, r: f'`M = {S.n} // {S.pow10} % 10 = {S.M}`：prefix 取到最大时，m 最多是 `{S.M}`',
        'ans += max_prefix * pow10': _cap_c1,
        'if M > 1': lambda S, B, r: (f'prefix = max_prefix：`M = {S.M} > 1` → 情况二' if S.M > 1 else f'`M = {S.M}`，不大于 1'),
        'ans += pow10': '情况二：m 填 1 小于 M，suffix 仍可随便填 `{pow10}` 种 → `ans = {ans}`',
        'elif M == 1': lambda S, B, r: ('`M = 1` → 情况三：m 填 1 后 suffix 受限' if S.M == 1
                                         else '`M = 0` → 情况四：m 只能填 0，==贡献为 0=='),
        'max_suffix = n % pow10': '`max_suffix = {n} % {pow10} = {max_suffix}`：suffix 最大只能到它',
        'ans += max_suffix + 1': '情况三：suffix 可填 `0 ~ {max_suffix}`，共 `{max_suffix + 1}` 种 → `ans = {ans}`',
        'pow10 *= 10': lambda S, B, r: f'{POS[_pos(S) - 1]}统计完，`pow10` → `{S.pow10}`，看更高一位',
        'return ans': '`0 ~ {n}` 中数字 1 一共出现 =={ret}== 次',
    },
    cards=dict(
        one_liner='横看成岭侧成峰：逐位统计「这一位是 1」的数有多少个',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['给定整数 `n`，计算所有 ==小于等于 n 的非负整数== 中数字 `1` 出现的个数',
                 '示例：`n = 13` → `6`（1、10、11×2、12、13）',
                 f'本视频：`n = {N0}` → `1625`'],
        quote='把整数 x 拆分成三段：prefix | m | suffix。……枚举 suffix 的长度 i。对于一个固定的 i，==有多少个整数可以让 m 等于 1==？',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['情况一 prefix < max_prefix：m 填 1，suffix 随便填 → `max_prefix · 10^i`',
              'prefix = max_prefix 时看 `M`：`M > 1` → `+10^i`（情况二）',
              '`M = 1` → suffix 只能填 `0 ~ max_suffix` → `+max_suffix + 1`（情况三）',
              '`M = 0` → m 填不了 1，贡献 0（情况四）'],
        result='`ans = 211 + 210 + 204 + 1000 = 1625`（个位 + 十位 + 百位 + 千位）',
        after=[dict(heading='方法一：数位 DP', lines=[
            '原文还给了数位 DP：`dfs(i, cnt1, is_limit)` 逐位填数字',
            '`is_limit` 表示是否受 n 约束：受约束时这一位最多填 `s[i]`',
            '写法二用贡献法：当前位填 1 时，这个 1 出现在 `sub_cnt` 个数中',
            '数位 DP 是通用模板；本题的数学公式只需 `O(log n)`',
        ])],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '易错：情况一的 prefix 范围是 `0 ~ max_prefix − 1`，共 `max_prefix` 种',
                 '易错：`M = 1` 时 suffix 只能到 `max_suffix`，要 `+1` 算上 0',
                 '贡献法：换个角度，按「位」而不是按「数」统计',
                 '专题：数位 DP 题单、思维题单的「贡献法」'],
    ),
)
