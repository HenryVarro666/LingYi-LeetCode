import math


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '圆盘 a~z（蓝 = cur 指针，粉 = 要键入的 b）', 24, T['muted'], bold=True)
    cx, cy = (x0 + x1) / 2, (y0 + 40 + y1) / 2
    R = min((x1 - x0) / 2 - 60, (y1 - y0 - 40) / 2 - 40)
    pts = {}
    for k in range(26):
        a = -math.pi / 2 + 2 * math.pi * k / 26
        pts[k] = (cx + R * math.cos(a), cy + R * math.sin(a))
    cur = ord(S['cur']) - 97 if 'cur' in S else None
    b = ord(S['b']) - 97 if 'b' in S else None
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
        cv.text((cx, cy - 22), f"`{S['cur']}` → `{S['b']}`".replace('`', ''), 34, T['text'], anchor='mm', bold=True)
        cv.text((cx, cy + 22), f"顺/逆 {d} / {26 - d}，取 {min(d, 26 - d)}", 28, T['yellow'], anchor='mm', bold=True)


CONFIG = dict(
    num=1974, title='使用特殊打字机键入单词的最少时间', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='环形最短距离 · 模拟（Go 原文转写）',
    code='''
class Solution:
    def minTimeToType(self, s: str) -> int:
        cur = 'a'
        ans = len(s)
        for b in s:
            d = ord(b) - ord(cur)
            if d < 0:
                d = -d
            ans += min(d, 26 - d)
            cur = b
        return ans
''',
    call="Solution().minTimeToType('bza')",
    expect=7,
    views=[
        dict(type='string', var='s', h=150, label='word（要键入的字母）'),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('cur', 'cur', 'blue'), ('b', 'b', 'pink'), 'd', ('ans', 'ans', 'green')],
    captions={
        'ans = len(s)': '每个字母都要键入 1 秒，先记 `ans = len(s) = {ans}`，之后只加指针移动的秒数',
        'cur = ': lambda S, B, r: ("指针初始指向 `a`" if S.get('cur') == 'a' and 'b' not in B else f"指针移到 `{S.cur}`，键入完成，下一个字母从这里出发"),
        'for b in s': lambda S, B, r: (f'下一个要键入的字母 `b = {S.b}`' if S.get('b') != B.get('b') or S.b != S.cur else f'字母都处理完了，循环结束'),
        'd = ord(b)': '`{b}` 和 `{B.cur}` 的字母表距离：`ord(b) - ord(cur)` = {d}',
        'd = -d': '距离取绝对值：`d` = =={d}==',
        'ans += min': '圆盘首尾相连：顺时针 `{d}`、逆时针 `26 - {d}` = {26-d}，取小的 ==`{min(d, 26-d)}`==；`ans` = {ans}',
        'return ans': '总共 `{ans}` 秒',
    },
    cards=dict(
        one_liner='圆盘上两字母之间走顺时针或逆时针，取较短的一边',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['圆盘上有 a~z，指针起初指向 `a`，每秒可转动一格或键入当前字母',
                 '求键入单词 `word` 的最少秒数',
                 '示例：`"bza"` → `7`'],
        quote='ans += min(d, 26-d)',
        quote_src='—— 灵茶山艾府题解代码（Go）',
        idea=['每个字母必须键入一次：先记 `len(s)` 秒',
              '相邻两个字母距离 `d`：顺时针 `d`，逆时针 `26-d`，取小的',
              '键入后指针停在该字母，更新 `cur`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（原文自带的 `min` 辅助函数直接用内置 `min`）',
                 '时间 `O(n)`，空间 `O(1)`',
                 '易错点：指针从 `a` 出发；别忘了加键入的 `len(s)` 秒；逆时针是 `26-d`'],
    ),
)
