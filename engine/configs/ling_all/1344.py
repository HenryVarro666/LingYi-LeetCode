CONFIG = dict(
    num=1344, title='时钟指针的夹角', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='公式 · 避免浮点运算',
    code='''
class Solution:
    def angleClock(self, hour: int, minutes: int) -> float:
        d = abs(hour * 60 - minutes * 11)
        return min(d, 720 - d) / 2
''',
    call='Solution().angleClock(4, 50)',
    expect=155,
    views=[
        dict(type='text', size=34, fn=lambda S: f"`2d = |60×{S['hour']} − 11×{S['minutes']}|` = =={S['d']}==" if 'd' in S else f"时间 `{S['hour']}:{S['minutes']:02d}`"),
        dict(type='text', size=30, fn=lambda S: f"较小角 `min({S['d']}, 720 − {S['d']}) / 2`" if 'd' in S else ''),
        dict(type='custom', h=420, draw=lambda cv, S, B, box, T: _clock(cv, S, box, T)),
    ],
    watch=['hour', 'minutes', ('d', 'd', 'green')],
    captions={
        'd = abs': '`2d = |60×{hour} − 11×{minutes}|` = =={d}==（`d` 是夹角的 2 倍，全程是整数）',
        'return min': lambda S, B, r: f'夹角可能超过 180，较小角取 `min(2d, 720 − 2d)` = `min({S.d}, {720 - S.d})` = `{min(S.d, 720 - S.d)}`，最后只除一次 2 → =={r}==',
    },
    cards=dict(
        one_liner='把夹角乘 2，整个公式只剩整数运算',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给出 `hour` 点 `minutes` 分，求时针和分针的较小夹角（度）',
                 '示例：`hour = 4, minutes = 50` → `155`'],
        quote='先计算 2d = |60×hour − 11×minutes|，以及 min(2d, 720° − 2d)，最后再除以 2，这样只会执行一次浮点运算。',
        quote_src='—— 灵茶山艾府题解（写法二）',
        before=[dict(heading='先把角度算清楚', lines=['一圈 `360°` 有 `60` 个刻度，分针每分钟 `6°`', '一圈 `12` 小时，时针每小时 `30°`，每分钟还会再走 `0.5°`', '所以分针在 `6·minutes`，时针在 `30·hour + 0.5·minutes`'])],
        idea=['分针每分钟转 `6°`，时针每分钟转 `0.5°`，每小时转 `30°`',
              '夹角 `d = |30·hour − 5.5·minutes|`，可能大于 `180°`，要取 `min(d, 360 − d)`',
              '两边乘 2 去掉 `5.5`：`2d = |60·hour − 11·minutes|`'],
        summary=['时间、空间都是 `O(1)`',
                 '易错点：夹角可能大于 180°，要取 `min(d, 360 − d)`',
                 '本题 `hour ≤ 12`，`d ≤ 360`，不用先对 12 取模',
                 '写法一是 `d = abs(hour*30 - minutes*5.5)` 再 `min(d, 360-d)`，带浮点数；本视频演示写法二'],
    ),
)

def _clock(cv, S, box, T):
    import math
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    R = min(x1 - x0, y1 - y0) / 2 - 50
    cv.d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=T['border'], width=4)
    for k in range(12):
        a = math.radians(k * 30)
        p = (cx + (R - 8) * math.sin(a), cy - (R - 8) * math.cos(a))
        cv.text(p, 12 if k == 0 else k, 22, T['dim'], anchor='mm', bold=True)
    h, m = S['hour'], S['minutes']
    ha = math.radians(30 * h + 0.5 * m)
    ma = math.radians(6 * m)
    cv.line([(cx, cy), (cx + R * 0.5 * math.sin(ha), cy - R * 0.5 * math.cos(ha))], T['blue'], 8)
    cv.line([(cx, cy), (cx + R * 0.78 * math.sin(ma), cy - R * 0.78 * math.cos(ma))], T['pink'], 5)
    cv.text((cx, y1 + 10), '蓝 = 时针，粉 = 分针', 22, T['muted'], anchor='mb')
