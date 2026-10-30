N0 = 127
LAYER_COL = ['blue', 'pink', 'purple', 'cyan']


def _v5(x):
    c = 0
    while x % 5 == 0:
        x //= 5
        c += 1
    return c


def _log5(p):
    k = 0
    while p > 1:
        p //= 5
        k += 1
    return k


def _state(S):
    """(已计入的层数, 当前层, 当前层是否刚计入)"""
    line = S.get('_line')
    fp = S.get('five_pow')
    if fp is None:
        return 0, None, False
    k = _log5(fp)
    if line == 6:
        return k - 1, k, True
    if line == 7:
        return k - 1, None, False
    if line == 9:
        return 9, None, False
    return k - 1, k, False


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    done, cur, just = _state(S)
    fp = S.get('five_pow')
    xs = list(range(5, N0 + 1, 5))
    cv.text((x0 + 18, y0 + 4), f'1 ~ {N0} 中能整除 5 的数：每个方块 = 它提供的一个因子 5', 22, T['muted'], bold=True)
    # five_pow 进度条
    cx = x0 + 30
    for k, p in enumerate([5, 25, 125, 625], 1):
        lab = f'{p}：{N0 // p} 个' if p <= N0 else f'{p} > {N0}'
        w = cv.tlen(lab, 24, bold=True) + 36
        on = fp == p
        fill = T[LAYER_COL[k - 1]] if k <= done else (T['yellow'] if on else T['panel2'])
        cv.rect((cx, y0 + 56, cx + w, y0 + 106), fill=fill, r=12, outline=T['yellow'] if on else T['border'], width=3 if on else 1)
        cv.text((cx + w / 2, y0 + 81), lab, 24, T['bg'] if (k <= done or on) else T['dim'], anchor='mm', bold=True)
        if k < 4:
            cv.text((cx + w + 18, y0 + 81), '→', 24, T['muted'], anchor='mm')
        cx += w + 36
    cw = (x1 - x0 - 40) / len(xs)
    sq = min(cw - 6, 46)
    base = y1 - 130
    for idx, x in enumerate(xs):
        X = x0 + 20 + idx * cw + cw / 2
        hit = cur is not None and fp and x % fp == 0
        for k in range(1, _v5(x) + 1):
            Y = base - k * (sq + 6)
            if k <= done:
                fill, out, w = T[LAYER_COL[k - 1]], None, 1
            elif cur == k and just:
                fill, out, w = T['yellow'], None, 1
            elif cur == k:
                fill, out, w = T['panel2'], T['yellow'], 3
            else:
                fill, out, w = T['panel2'], T['border'], 1
            cv.rect((X - sq / 2, Y, X + sq / 2, Y + sq), fill=fill, outline=out, width=w, r=6)
        cv.text((X, base + 6), x, 15 if x >= 100 else 17, T['yellow'] if hit else T['muted'], anchor='mt', mono=True,
                bold=bool(hit))
    if fp and cur is not None:
        c = N0 // fp
        cv.text(((x0 + x1) / 2, base + 46), f'能整除 five_pow = {fp} 的数（黄色数字）：{N0} // {fp} = {c} 个',
                24, T['yellow'], anchor='mt', bold=True)
    if 'res' in S:
        cv.text(((x0 + x1) / 2, base + 86), f"已累加的方块数 = res = {S['res']}", 24, T['green'], anchor='mt', bold=True)


def _cap_add(S, B, ret):
    fp = S.five_pow
    k = _log5(fp)
    c = N0 // fp
    if k == 1:
        return f'所有能整除 5 的数都提供一个因子 5：`{N0} // 5 = {c}` → `res = {S.res}`'
    return (f'能整除 {fp} 的数前面已算过 {k - 1} 个 5，这里==只需再算一个==：'
            f'`{N0} // {fp} = {c}` → `res = {S.res}`')


CONFIG = dict(
    num=172, title='阶乘后的零', difficulty='Medium', category='数学',
    author='yiduobo', technique='数因子 5 · 5 的幂次逐个累加',
    tags=['字节30天', '面试经典150'],
    code='''
class Solution(object):
    def trailingZeroes(self, n):
        res = 0
        five_pow = 5
        while n >= five_pow:
            res += n // five_pow
            five_pow *= 5

        return res
''',
    call=f'Solution().trailingZeroes({N0})',
    expect=31,
    views=[
        dict(type='custom', draw=_draw, h=600),
    ],
    watch=['n', ('five_pow', 'five_pow', 'yellow'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 统计 `{n}!` 中有多少个因子 5（5 比 2 少，每个 5 都能配一个 2 成 10）',
        'five_pow = 5': '`five_pow` 依次取 5 的幂：5、25、125……',
        'while n >= five_pow': lambda S, B, ret: (
            f'`n = {S.n} ≥ five_pow = {S.five_pow}` → 还有数能整除 {S.five_pow}' if S.n >= S.five_pow
            else f'`n = {S.n} < five_pow = {S.five_pow}`：没有数能整除它了 → 结束'),
        'res += n // five_pow': _cap_add,
        'five_pow *= 5': '`five_pow` 乘 5 → `{five_pow}`，考察下一个幂次',
        'return res': f'`{N0}!` 末尾有 =={{ret}}== 个 0：`25 + 5 + 1`',
    },
    cards=dict(
        one_liner='末尾的 0 来自 2×5；能整除 5、25、125… 的数，各再提供一个因子 5',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['给定整数 `n`，返回 `n!` 结果中==尾随零==的数量',
                 '示例：`n = 5` → `5! = 120` → `1`；`n = 3` → `3! = 6` → `0`',
                 f'本视频：`n = {N0}` → `31`'],
        quote='所有能整除25的数都可以提供两个因子5。但是需要注意能整除25必然能整除5，……==在这里只需要再计算一个因子5==。',
        quote_src='—— yiduobo 题解原文',
        idea=['末尾的 0 由因子 2 与因子 5 相乘得到，5 比 2 少 → 只数因子 5',
              '能整除 5 的数各算一个；能整除 25 的==再==算一个；125 再算一个……',
              '1 到 n 中能整除 `k` 的数有 `n // k` 个：找最大的 `p` 使 `pk ≤ n`'],
        result=f'`res = 25 + 5 + 1 = 31`：`{N0}!` 末尾有 31 个 0',
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '循环条件 `n >= five_pow`：five_pow 超过 n 后再除都是 0',
                 '易错：只算 `n // 5` 会漏掉 25、125 里多出来的因子 5',
                 '原文为 Python 2 写法：`n / five_pow` 已改为整除 `n // five_pow`，并删去了文档字符串',
                 '对比灵神：灵神反复 `n //= 5` 再累加，不用维护 five_pow'],
    ),
)
