NS = (3, 4, 5, 7, 8)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'n' not in S:
        return
    n = S['n']
    r = n % 4
    cv.text((x0 + 18, y0 + 4), f'n = {n} 颗石头：从右往左每 4 颗分成一组', 24, T['muted'], bold=True)
    R = 26
    gap, ggap = 64, 40
    groups = n // 4
    total = n * gap + (groups + (1 if r else 0) - 1) * ggap
    sx = x0 + max(30, (x1 - x0 - total) / 2)
    cy = y0 + 120
    X = sx
    k = 0
    if r:
        cv.rect((X - 12, cy - R - 16, X + r * gap - gap + 2 * R + 12, cy + R + 16), outline=T['yellow'], width=3, r=14)
        cv.text((X + (r * gap - gap + 2 * R) / 2, cy + R + 26), f'先手先拿走 {r} 颗', 22, T['yellow'], anchor='mt', bold=True)
        for _ in range(r):
            cv.d.ellipse((X, cy - R, X + 2 * R, cy + R), fill=T['yellow'])
            X += gap
            k += 1
        X += ggap
    for g in range(groups):
        cv.rect((X - 12, cy - R - 16, X + 3 * gap + 2 * R + 12, cy + R + 16), outline=T['border'], width=2, r=14)
        for j in range(4):
            c = T['blue'] if j == 0 else T['pink']
            cv.d.ellipse((X, cy - R, X + 2 * R, cy + R), fill=c if g == 0 else T['panel2'], outline=T['border'], width=2)
            X += gap
        X += ggap
    Y = cy + 110
    if groups:
        cv.text((x0 + 40, Y), '一组 4 颗 = 一轮：一方拿 a 颗（1~3），另一方就拿 4 − a 颗，正好凑满 4', 23, T['text'])
        cv.text((x0 + 40, Y + 40), '（第一组示意：蓝 = 对手拿 1 颗，粉 = 我补 3 颗）', 21, T['muted'])
    if n < 4:
        msg = f'n = {n} < 4：先手==一次拿光==，直接获胜'
        c = T['green']
    elif r:
        msg = f'n % 4 = {r} ≠ 0：先手拿走 {r} 颗，剩下 4 的倍数，相当于==先后手互换== → 先手必胜'
        c = T['green']
    else:
        msg = 'n % 4 = 0：先手怎么拿，后手都补到 4 → 最后一颗总被后手拿走，==先手必败=='
        c = T['red']
    cv.rich(x0 + 40, Y + 96, msg, x1 - x0 - 80, size=26, color=c, accent=T['orange'])
    cur = NS.index(n)
    Y3 = y1 - 66
    cv.text((x0 + 18, Y3 - 38), '本视频依次调用 canWinNim(n)', 22, T['muted'], bold=True)
    X = x0 + 40
    for k, v in enumerate(NS):
        res = 'true' if v % 4 else 'false'
        txt = f'{v} → {res}' if k <= cur else f'{v} → ?'
        w = cv.tlen(txt, 26, True, True) + 36
        cv.rect((X, Y3, X + w, Y3 + 50), fill=T['blue'] if k == cur else T['panel2'], r=10, outline=T['border'])
        cv.text((X + w / 2, Y3 + 25), txt, 26, T['bg'] if k == cur else (T['text'] if k < cur else T['dim']),
                anchor='mm', bold=True, mono=True)
        X += w + 16


CONFIG = dict(
    num=292, title='Nim游戏', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='每轮凑满 4 颗',
    tags=['labuladong', '灵神题单·数学算法'],
    code='''
class Solution(object):
    def canWinNim(self, n):
        return n % 4 != 0
''',
    call=f'[Solution().canWinNim(x) for x in {NS}]',
    expect=[True, False, True, True, False],
    views=[dict(type='custom', draw=_draw, h=600)],
    watch=[('n', 'n', 'blue'), ('n % 4', lambda S: S['n'] % 4 if 'n' in S else None, 'orange')],
    captions={
        'return n % 4': lambda S, B, r: (
            f'`n = {S.n}`：`{S.n} % 4 = {S.n % 4}` ≠ 0 → 先拿 {S.n % 4} 颗，把 4 的倍数留给对手 → =={r}=='
            if r else f'`n = {S.n}` 是 4 的倍数 → 后手每轮补到 4，先手必败 → =={r}=='),
    },
    cards=dict(
        one_liner='每次只能拿 1~3 颗：对手拿 a 颗我就拿 4 − a 颗，每轮凑满 4',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['桌上有 `n` 颗石头，你和朋友轮流拿，==你先手==，每次拿 1~3 颗',
                 '拿走最后一颗石头的人获胜；双方都用最优策略，问你能否获胜',
                 '示例：`n = 4` → `false`（不管拿几颗，对手都能拿走最后一颗）；`n = 1` → `true`',
                 f'本视频依次计算 `n = {list(NS)}`'],
        quote='注意到每次只能拿1-3颗石头，那么==后手总是能根据先手拿的石头数量将这一轮的总数补充到4==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n` 是 4 的倍数：后手每轮补到 4，最后一颗一定是后手拿的 → 后手必胜',
              '`n` 不是 4 的倍数：先手先拿 `n % 4` 颗，剩下 4 的倍数',
              '这相当于==先后手互换==，先手变成了“补到 4”的那一方 → 先手必胜'],
        summary=['时间 `O(1)`，空间 `O(1)`，一行 `return n % 4 != 0`',
                 '关键：找到一个“每轮总数固定”的配对策略（1~3 颗 → 补到 4）',
                 '推广：每次拿 1~m 颗时，答案是 `n % (m + 1) != 0`',
                 '更一般的博弈要用 SG 函数，本题是最简单的一种形式',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
