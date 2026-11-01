import math


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '圆盘 a~z（蓝 = now 指针，粉 = 当前字符 char）', 24, T['muted'], bold=True)
    cx, cy = (x0 + x1) / 2, (y0 + 40 + y1) / 2
    R = min((x1 - x0) / 2 - 60, (y1 - y0 - 40) / 2 - 40)
    pts = {}
    for k in range(26):
        a = -math.pi / 2 + 2 * math.pi * k / 26
        pts[k] = (cx + R * math.cos(a), cy + R * math.sin(a))
    cur = ord(S['now']) - 97 if 'now' in S else None
    b = ord(S['char']) - 97 if 'char' in S else None
    if cur is not None and b is not None and cur != b:
        d = abs(b - cur)
        short_cw = (b - cur) % 26
        step = 1 if short_cw <= 13 else -1
        k = cur
        while k != b:
            n = (k + step) % 26
            cv.line([pts[k], pts[n]], T['yellow'], 6)
            k = n
    for k in range(26):
        X, Y = pts[k]
        fill = T['panel2']
        tc = T['muted']
        if k == cur:
            fill, tc = T['blue'], T['bg']
        elif k == b:
            fill, tc = T['pink'], T['bg']
        cv.rect((X - 20, Y - 20, X + 20, Y + 20), fill=fill, outline=T['border'], r=20)
        cv.text((X, Y), chr(97 + k), 26, tc, anchor='mm', bold=True, mono=True)
    if cur is not None and b is not None:
        d = abs(b - cur)
        cv.text((cx, cy - 22), f"`{S['now']}` → `{S['char']}`".replace('`', ''), 34, T['text'], anchor='mm', bold=True)
        cv.text((cx, cy + 22), f"顺/逆 {d} / {26 - d}，取 {min(d, 26 - d)}", 28, T['yellow'], anchor='mm', bold=True)


CONFIG = dict(
    num=1974, title='使用特殊打字机键入单词的最少时间', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟遍历 · 累加环形距离',
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
    call="Solution().minTimeToType('zjpc')",
    expect=34,
    views=[
        dict(type='string', var='word', h=150, label='word'),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('now', 'now', 'blue'), ('char', 'char', 'pink'), 'delta', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计总秒数，从 0 开始',
        'now = ': lambda S, B, r: ("指针一开始在 `a`" if 'char' not in B else f"指针停在 `{S.now}`，下一段从这里算起"),
        'for char in word': lambda S, B, r: (f'接着要键入 `{S.char}`' if S.char != B.get('char') or S.char != S.now else '单词键入完了，循环结束'),
        'delta = abs': '顺时针距离 = 两字符 ASCII 码之差：`|{ord(char)} - {ord(now)}|` = =={delta}==',
        'res += min': '逆时针是 `26 - {delta}` = {26 - delta}，取较小的 ==`{min(delta, 26 - delta)}`==，再 +1 秒键入 → `res` = =={res}==',
        'return res': '全部键入完，总共 `{res}` 秒',
    },
    cards=dict(
        one_liner='相邻字符的圆盘距离，顺时针与逆时针取小，再加键入一步',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['圆盘上有 a~z，指针起初指向 `a`；每秒转一格或键入一个字符',
                 '求键入 `word` 的最少秒数',
                 '示例：`"zjpc"` → `34`'],
        quote='当顺时针移动时，移动的距离就是较大字符的ascii码减去较小字符的ascii码，而逆时针移动的距离，则可以使用26减去顺时针移动的距离来得到。',
        quote_src='—— yiduobo 题解原文',
        idea=['只需计算各字符之间移动的距离，圆盘可顺可逆',
              '一趟遍历：`delta` 与 `26 - delta` 取小，每个字符再 +1 秒键入',
              '注意起点是 `a`，所以 `now` 初始为 `a`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：起点是 `a`；每次移动完要再加 1 步键入',
                 '对比灵神：灵神先记 `len(s)` 再只累加移动，yiduobo 每步 `+1`，结果一样',
                 '原文无需改动，直接可在 Python 3 运行'],
    ),
)
