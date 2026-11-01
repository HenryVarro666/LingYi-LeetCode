def _tl(S, s_key, e_key):
    return S.get(s_key), S.get(e_key)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    s, t = S.get('s'), S.get('t')
    cv.text((x0 + 18, y0 + 4), '时间轴（分钟，每格 = 一刻钟）：绿 = 完整对局', 24, T['muted'], bold=True)
    if s is None or t is None:
        return
    lo = s // 15 * 15
    hi = (t + 14) // 15 * 15
    n = (hi - lo) // 15
    w = (x1 - x0 - 60) / n
    base = y0 + 190
    full = (t - t % 15)
    for j in range(n):
        a = lo + 15 * j
        X = x0 + 30 + j * w
        ok = a >= s and a + 15 <= t
        counted = ok and a + 15 <= full
        cv.rect((X + 2, base - 60, X + w - 2, base), fill=T['green'] if counted else (60, 66, 76), r=6, alpha=200 if counted else 255)
        cv.text((X, base + 8), f'{a // 60 % 24:02d}:{a % 60:02d}', 15, T['dim'], anchor='mt', mono=True)
    for v, name, c in ((s, 'start s', T['blue']), (t, 'finish t', T['pink'])):
        X = x0 + 30 + (v - lo) / 15 * w
        cv.line([(X, base - 90), (X, base + 4)], c, 4)
        cv.text((X, base - 96), f'{name}={v}', 20, c, anchor='mb', bold=True)
    X = x0 + 30 + (full - lo) / 15 * w
    cv.dashed((X, base - 80), (X, base + 4), T['yellow'], 3)
    cv.text((X, base + 40), f't - t%15 = {full}', 20, T['yellow'], anchor='mt', bold=True)


CONFIG = dict(
    num=1904, title='你完成的完整对局数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='结束时间向下取整到刻钟（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def numberOfRounds(self, startTime: str, finishTime: str) -> int:
        h1, m1 = map(int, startTime.split(':'))
        h2, m2 = map(int, finishTime.split(':'))
        if startTime > finishTime: h2 += 24  # 玩了个通宵
        s, t = h1 * 60 + m1, h2 * 60 + m2
        return int((t - t % 15 - s) / 15)
''',
    call='Solution().numberOfRounds("22:10", "01:50")',
    expect=14,
    views=[dict(type='custom', draw=_draw, h=330),
           dict(type='text', size=30, h=100, fn=lambda S: (
               f"`({S['t']} − {S['t'] % 15} − {S['s']}) / 15` = =={int((S['t'] - S['t'] % 15 - S['s']) / 15)}==" if 's' in S else ''))],
    watch=['startTime', 'finishTime', ('h2', 'h2', 'pink'), ('s', 's', 'blue'), ('t', 't', 'pink')],
    captions={
        'h1, m1': '把 `{startTime}` 拆成小时 `{h1}` 和分钟 `{m1}`',
        'h2, m2': '把 `{finishTime}` 拆成小时 `{h2}` 和分钟 `{m2}`',
        'if startTime > finishTime': lambda S, B, r: (
            f'字符串比较 `"{S.startTime}" > "{S.finishTime}"` → ==玩了个通宵==，结束时间加 24 小时：`h2` = {S.h2}'
            if S.startTime > S.finishTime else '开始不晚于结束，同一天内，不用加 24 小时'),
        's, t =': '都换成分钟：`s = {s}`，`t = {t}`',
        'return': '`t - t%15` = {t - t % 15}：结束时间向下取整到刻钟，不足一刻钟的丢掉；`s` 不处理，整除时自然向上取整。再减 `s` 除以 15：=={ret}== 局（Go 整除向零取整，故用 `int(x / 15)`）',
    },
    cards=dict(
        one_liner='结束时间向下取整到刻钟，开始时间不动，再整除 15',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['每刻钟（:00/:15/:30/:45）开一局，每局 15 分钟',
                 '进入 `startTime`、退出 `finishTime`，数完整打完的局数',
                 '结束早于开始表示通宵。示例：`22:10 → 01:50` → `14`'],
        quote='将结束时间取到最近的刻钟，而开始时间不作处理。这样可以利用整除运算的性质，去掉不足一刻钟的部分，同时避免计算出 -1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`t - t%15` 把结束时间落到整刻钟，不足的半局丢掉',
              '`(t - t%15 - s) / 15` 的整除自动把开始时间向上取整到下一刻钟',
              '字符串 `"HH:MM"` 可以直接比大小，`startTime > finishTime` 就是跨天'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python：`Sscanf` 对应 `split(\':\')` + `map(int, ...)`',
                 'Go 的整数除法向零取整，Python 的 `//` 向下取整，所以写成 `int(x / 15)`；分子为 -1 时得 0，而不是 -1',
                 '时间 `O(1)`，空间 `O(1)`',
                 '易错点：同一刻钟内进出，分子可能是负数，不能当成 -1 局'],
    ),
)
