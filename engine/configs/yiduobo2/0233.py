N0 = 2015
DIG = str(N0)
POS = ['个位', '十位', '百位', '千位', '万位']


def _k(S):
    """当前考察的是第几位（0 = 个位）"""
    p = S.get('pow10')
    return len(str(p)) - 2 if p else 0


def _contrib(k):
    p = 10 ** (k + 1)
    lo = p // 10
    c1 = N0 // p * lo
    tmp = N0 % p
    if tmp < lo:
        c2, kind = 0, '<'
    elif tmp < 2 * lo - 1:
        c2, kind = tmp - lo + 1, 'in'
    else:
        c2, kind = lo, '>='
    return c1, c2, tmp, kind


def _row_state(S):
    line = S.get('_line')
    if 'pow10' not in S or line in (3, 4):
        return 0, None, 0
    k = _k(S)
    if line in (5, 14, 16):
        return k, None, 0
    if line in (6, 7, 9):
        return k, k, 1
    if line == 8:
        return k, k, 2 if S['tmp'] < S['pow10'] // 10 else 1
    if line in (10, 12):
        return k, k, 2
    return k, None, 0


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    done, cur, shown = _row_state(S)
    line = S.get('_line')
    focus = cur
    if focus is None and line == 5 and S.get('pow10', 0) <= N0 * 10:
        focus = _k(S)
    n = len(DIG)
    cv.text((x0 + 18, y0 + 4), f'n = {N0}：高位 x = n // pow10，低位 tmp = n % pow10（含当前这一位）', 22, T['muted'], bold=True)
    cell = 84
    sx = x0 + 40
    sy = y0 + 50
    for t, ch in enumerate(DIG):
        p = n - 1 - t
        fill = T['panel2']
        if focus is not None:
            fill = T['blue'] if p > focus else (T['yellow'] if p == focus else T['pink'])
        cv.rect((sx + t * cell + 4, sy, sx + (t + 1) * cell - 4, sy + cell - 8), fill=fill, r=12)
        cv.text((sx + t * cell + cell / 2, sy + (cell - 8) / 2), ch, 42, T['bg'] if focus is not None else T['text'], anchor='mm', bold=True)
        cv.text((sx + t * cell + cell / 2, sy + cell), POS[p], 17, T['dim'], anchor='mt')
    if focus is not None:
        pw = 10 ** (focus + 1)
        lo, hi = pw // 10, 2 * pw // 10 - 1
        tx = sx + n * cell + 30
        cv.text((tx, sy + 6), f'x = {N0} // {pw} = {N0 // pw}', 24, T['blue'], bold=True, mono=True)
        cv.text((tx, sy + 42), f'tmp = {N0} % {pw} = {N0 % pw}', 24, T['pink'], bold=True, mono=True)
        # 数轴：0 ~ pow10-1，高亮 [lo, hi]
        L, R = x0 + 60, x1 - 60
        ly = sy + cell + 110
        cv.text((x0 + 18, ly - 74), f'tmp 落在哪一段？{POS[focus]}是 1 的低位范围：[{lo}, {hi}]', 22, T['muted'], bold=True)

        def X(v):
            return L + v / max(1, pw - 1) * (R - L)
        cv.line([(L, ly), (R, ly)], T['border'], 4)
        cv.rect((X(lo), ly - 14, max(X(hi), X(lo) + 8), ly + 14), fill=T['green'], r=6, alpha=200)
        for v in sorted({0, lo, hi, pw - 1}):
            cv.text((X(v), ly + 22), v, 18, T['muted'], anchor='mt', mono=True)
        if 'tmp' in S and line in (7, 8, 9, 10, 12) and S.get('pow10') == pw:
            tv = S['tmp']
            cv.tri_down(X(tv), ly - 18, 12, T['yellow'])
            cv.text((X(tv) + 14, ly - 30), f'tmp={tv}', 20, T['yellow'], anchor='lm', bold=True)
    # 贡献表
    ty = y0 + 322
    cols = [('位', 90), ('高位 x·10^(k−1)', 230), ('低位 tmp 的贡献', 330), ('小计', 140)]
    tw = sum(w for _, w in cols)
    tx0 = x0 + (x1 - x0 - tw) / 2
    Xc = tx0
    for name, w in cols:
        cv.text((Xc + w / 2, ty), name, 20, T['muted'], anchor='mt', bold=True)
        Xc += w
    rh = 46
    total = 0
    for r in range(n):
        Y = ty + 32 + r * rh
        c1, c2, tmp, kind = _contrib(r)
        on = r < done or r == cur
        cv.rect((tx0, Y, tx0 + tw, Y + rh - 6), fill=(60, 52, 30) if r == cur else (T['panel2'] if on else T['panel']), r=8,
                outline=T['yellow'] if r == cur else T['border'], width=2 if r == cur else 1)
        vals = [POS[r], '', '', '']
        if r < done or (r == cur and shown >= 1):
            vals[1] = str(c1)
        if r < done or (r == cur and shown >= 2):
            lo = 10 ** r
            vals[2] = {'<': f'0（{tmp} < {lo}）', 'in': f'{c2}（{tmp} − {lo} + 1）', '>=': f'{c2}（{tmp} ≥ {2 * lo - 1}）'}[kind]
        if r < done:
            vals[3] = str(c1 + c2)
            total += c1 + c2
        Xc = tx0
        for (name, w), v in zip(cols, vals):
            cv.text((Xc + w / 2, Y + (rh - 6) / 2), v, 21, T['text'] if on else T['dim'], anchor='mm', bold=True)
            Xc += w
    cv.text((tx0 + tw, ty + 32 + n * rh + 6), f'已完成的位合计 = {total}', 22, T['green'], anchor='ra', bold=True)


def _cap_while(S, B, ret):
    p = S.pow10
    if p <= S.n * 10:
        return f'`pow10 = {p} ≤ n × 10 = {S.n * 10}`：考察==第 {_k(S) + 1} 位（{POS[_k(S)]}）==上的 1'
    return f'`pow10 = {p} > n × 10`：最高位也考察完了 → 结束'


def _cap_c1(S, B, ret):
    p = S.pow10
    x, lo = S.n // p, p // 10
    if x == 0:
        return f'高位 `x = {S.n} // {p} = 0`：没有更小的高位 → `+0`'
    return f'高位取 `0 ~ {x - 1}`（{x} 种）时，{POS[_k(S)]}的 1 完整出现 {lo} 次 → `+{x} × {lo} = {x * lo}`'


def _cap_if1(S, B, ret):
    lo = S.pow10 // 10
    if S.tmp >= lo:
        return f'`tmp = {S.tmp} ≥ {lo}`：高位等于 x 的这一段里也会出现 1'
    return f'`tmp = {S.tmp} < {lo}`：这一段{POS[_k(S)]}上==不会出现 1==，贡献 0'


def _cap_if2(S, B, ret):
    lo = S.pow10 // 10
    hi = 2 * S.pow10 // 10 - 1
    if S.tmp < hi:
        return f'`tmp = {S.tmp}` 落在 `[{lo}, {hi}]` 中间'
    return f'`tmp = {S.tmp} ≥ {hi}`：整段 `{lo} ~ {hi}` 都出现了'


CONFIG = dict(
    num=233, title='数字 1 的个数', difficulty='Hard', category='数学',
    author='yiduobo', technique='逐位统计 · 高位 + 低位分段',
    tags=['字节30天'],
    code='''
class Solution(object):
    def countDigitOne(self, n):
        pow10 = 10
        res = 0
        while pow10 <= n * 10:
            res += n // pow10 * (pow10 // 10)
            tmp = n % pow10
            if tmp >= pow10 // 10:
                if tmp < 2 * pow10 // 10 - 1:
                    res += tmp - pow10 // 10 + 1
                else:
                    res += pow10 // 10

            pow10 *= 10

        return res
''',
    call=f'Solution().countDigitOne({N0})',
    expect=1608,
    views=[
        dict(type='custom', draw=_draw, h=640),
    ],
    watch=[('pow10', 'pow10', 'yellow'), ('tmp', 'tmp', 'pink'), ('res', 'res', 'green')],
    captions={
        'pow10 = 10': '`pow10 = 10`：考察第 k 位时 `pow10 = 10^k`，从个位（k = 1）开始',
        'res = 0': '`res` 累加每一位上 1 出现的次数',
        'while pow10 <= n * 10': _cap_while,
        'res += n // pow10': _cap_c1,
        'tmp = n % pow10': '`tmp = {n} % {pow10} = {tmp}`：当前位及更低位构成的数',
        'if tmp >= pow10 // 10': _cap_if1,
        'if tmp < 2 * pow10': _cap_if2,
        'res += tmp - pow10 // 10 + 1': '只出现到 tmp：`{tmp} − {pow10 // 10} + 1 = {tmp - pow10 // 10 + 1}` 个 1 → `res = {res}`',
        'res += pow10 // 10': '完整出现 `{pow10 // 10}` 个 1 → `res = {res}`',
        'pow10 *= 10': lambda S, B, r: f'{POS[_k(S) - 1]}算完，`pow10` → `{S.pow10}`',
        'return res': '`0 ~ {n}` 中数字 1 一共出现 =={ret}== 次',
    },
    cards=dict(
        one_liner='1 的总数 = 每一位上 1 的出现次数之和；高位整段 + 低位看 tmp 落在哪',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['给定整数 `n`，计算所有 ==小于等于 n 的非负整数== 中数字 `1` 出现的个数',
                 '示例：`n = 13` → `6`（1、10、11×2、12、13）',
                 f'本视频：`n = {N0}` → `1608`'],
        quote='于是现在就有了一种做法：对于整数n，从低位开始往高位遍历，==考察当前位上会出现多少个1==。……所有的计算结果加和即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['个位的 1 形如 `x·10 + 1`，十位的 1 形如 `x·100 + (10~19)`……',
              '高位为 `0 ~ x−1` 时，当前位的 1 完整出现 `x` 轮，每轮 `10^(k−1)` 个',
              '高位等于 x 时看低位 `tmp`：小于 `10^(k−1)` → 0；超过 `2·10^(k−1)−1` → 整段',
              '落在中间 → `tmp − 10^(k−1) + 1` 个'],
        result='`res = 202 + 206 + 200 + 1000 = 1608`（个位 + 十位 + 百位 + 千位）',
        after=[dict(heading='原文举例：28XXXX 的千位', lines=[
            '高位 0~27：1000~1999、11000~11999、…、271000~271999',
            '一共 `28 × 10^3 = 28000` 个 1',
            '高位等于 28：280999 → 千位无 1；281999 → 1000 个',
            '281234 → `1234 − 1000 + 1 = 235` 个',
        ])],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '循环条件 `pow10 <= n * 10` 等价于 `10^(k−1) ≤ n`：最高位也要算',
                 '易错：中间段要 `+1`，`tmp` 本身也算',
                 '原文为 Python 2 写法：所有 `/` 整除已改为 `//`，并删去了文档字符串',
                 '对比灵神：灵神拆成 prefix | m | suffix 四种情况，本质相同'],
    ),
)
