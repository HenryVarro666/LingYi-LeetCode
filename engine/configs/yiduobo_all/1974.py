def _ring(cv, S, B, box, T):
    import math
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 6
    R = min(x1 - x0, y1 - y0) / 2 - 40
    letters = 'abcdefghijklmnopqrstuvwxyz'
    now = S.get('now')
    char = S.get('char')

    def pos(k, r):
        a = -math.pi / 2 + 2 * math.pi * k / 26
        return cx + r * math.cos(a), cy + r * math.sin(a)
    done = set()
    w = S.get('word', '')
    for k, ch in enumerate(letters):
        px, py = pos(k, R)
        fill = None
        if now == ch:
            fill = T['yellow']
        elif char == ch and char != now:
            fill = T['pink']
        cv.rect((px - 22, py - 22, px + 22, py + 22), fill=fill or (40, 46, 56), r=22)
        cv.text((px, py), ch, 26, T['bg'] if fill else T['text'], anchor='mm', bold=True)
    if now is not None and char is not None and char != now:
        i, j = ord(now) - 97, ord(char) - 97
        d = abs(j - i)
        cv.text((cx, cy - 12), f'{now} → {char}', 34, T['text'], anchor='mm', bold=True)
        cv.text((cx, cy + 30), f'顺时针 {d}，逆时针 {26 - d}', 24, T['muted'], anchor='mm')
    elif now is not None:
        cv.text((cx, cy), f'指针在 {now}', 34, T['text'], anchor='mm', bold=True)


CONFIG = dict(
    num=1974, title='使用特殊打字机键入单词的最少时间', difficulty='Easy', category='字符串',
    author='yiduobo', technique='环形距离累加',
    tags=[],
    code='''
class Solution(object):
    def minTimeToType(self, word):

        res = 0
        now = 'a'
        for char in word:
            delta = abs(ord(char) - ord(now))
            res += min(delta, 26 - delta) + 1
            now = char
        
        return res
''',
    call="Solution().minTimeToType('bza')",
    expect=7,
    views=[
        dict(type='custom', draw=_ring, h=470),
        dict(type='string', var='word', label='word', cell=100, h=170,
             color=lambda S, i, v: None),
    ],
    watch=[('now', 'now', 'yellow'), ('char', 'char', 'pink'), 'delta', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计总秒数',
        "now = 'a'": '指针一开始指向 `a`：`now = a`',
        'for char in word': '下一个要打的字母 `char = {char}`，指针当前在 `{now}`',
        'delta = abs': '顺时针走的距离 = ASCII 差：`|{ord(char)} − {ord(now)}|` = =={delta}==',
        'res += min': '顺时针 `{delta}`，逆时针 `26 − {delta} = {26 - delta}`，取小的 `{min(delta, 26 - delta)}`，再加 1 秒键入：`res` {B.res} → =={res}==',
        'now = char': '指针停在 `{char}`，下一轮从这里出发',
        'return res': '总共 `{res}` 秒',
    },
    cards=dict(
        one_liner='相邻字母在圆盘上的距离，顺逆时针取较小，再加 1 秒键入',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['圆盘上有 `a`–`z`，指针初始在 `a`，每秒可顺/逆时针转一格，或键入当前字母',
                 '求键入 `word` 的最少秒数',
                 '示例：`word = "bza"` → `7`'],
        quote='当顺时针移动时，移动的距离就是较大字符的ascii码减去较小字符的ascii码，而逆时针移动的距离，则可以使用26减去顺时针移动的距离来得到。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个字母的位置只和前一个字母有关，逐对累加',
              '`delta = |ord(char) − ord(now)|` 是一个方向的距离，另一个方向是 `26 − delta`',
              '别忘了每个字母还要 1 秒键入，起点是 `a`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：起点是 `a`，不是 `word[0]`',
                 '易错点：每个字母都要 `+1` 键入',
                 '原文是 Python 2 风格，本题代码在 Python 3 下无需改动'],
    ),
)
