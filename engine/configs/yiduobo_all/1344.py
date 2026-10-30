def _clock(cv, S, B, box, T):
    import math
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    R = min(x1 - x0, y1 - y0) / 2 - 50
    cy -= 10
    cv.d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=T['border'], width=4)
    for k in range(12):
        a = math.radians(k * 30)
        p = (cx + (R - 8) * math.sin(a), cy - (R - 8) * math.cos(a))
        cv.text(p, 12 if k == 0 else k, 22, T['dim'], anchor='mm', bold=True)
    if 'minutes_angle' in S:
        h, m = S['hour'], S['minutes']
        ha = math.radians(S['hour_angle'])
        ma = math.radians(S['minutes_angle'])
        cv.line([(cx, cy), (cx + R * 0.5 * math.sin(ha), cy - R * 0.5 * math.cos(ha))], T['blue'], 8)
        cv.line([(cx, cy), (cx + R * 0.78 * math.sin(ma), cy - R * 0.78 * math.cos(ma))], T['pink'], 5)
    cv.text((cx, y1 + 22), '蓝 = 时针，粉 = 分针（都从 12 点方向量起）', 22, T['muted'], anchor='mb')


def _fmt(S):
    if 'minutes_angle' in S:
        return f"时针 `{S['hour_angle']:g}°`，分针 `{S['minutes_angle']}°`"
    if 'hour_angle' in S:
        return f"时针与 12 点夹角 `{S['hour_angle']:g}°`"
    return f"时间 `{S['hour']}:{S['minutes']:02d}`"


CONFIG = dict(
    num=1344, title='时钟指针的夹角', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='分别求与 12 点的夹角',
    code='''
class Solution(object):
    def angleClock(self, hour, minutes):

        if hour == 12:
            hour = 0
        
        hour_angle = (hour + minutes / 60.0) * 30
        minutes_angle = minutes * 6
        return min(abs(hour_angle - minutes_angle), 360 - abs(hour_angle - minutes_angle))
''',
    call='Solution().angleClock(3, 30)',
    expect=75,
    views=[
        dict(type='text', size=32, fn=_fmt),
        dict(type='custom', h=440, draw=_clock),
    ],
    watch=['hour', 'minutes', 'hour_angle', 'minutes_angle'],
    captions={
        'if hour == 12': '12 点等于 0 点，`hour = {hour}`，不是 12 就不用改',
        'hour_angle =': '时针不只看整点：分针走了 `{minutes}` 分，时针又多走 `{minutes}/60` 小时 → `({hour} + {minutes}/60) × 30 = =={hour_angle:g}==°`',
        'minutes_angle =': '一圈 360° 分 60 分钟，每分钟 6° → `{minutes} × 6 = =={minutes_angle}==°`',
        'return min': lambda S, B, r: f'两针差 `|{S.hour_angle:g} − {S.minutes_angle}| = {abs(S.hour_angle - S.minutes_angle):g}`；若超过 180 就改用 `360 −` 它，取较小者 → =={r:g}==',
    },
    cards=dict(
        one_liner='先各自量出与 12 点的夹角，再相减取较小角',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给出 `hour` 点 `minutes` 分，求时针和分针的较小夹角（度）',
                 '示例：`hour = 3, minutes = 30` → `75`'],
        quote='将其转化为求解时针与十二点整的夹角hour_angle，然后求解分针与十二点整的夹角minute_angle，那么二者的夹角就是角度之差的绝对值。',
        quote_src='—— yiduobo 题解原文',
        idea=['分针：每分钟 6°，所以 `minutes * 6`',
              '时针：每小时 30°，还要加上分针带来的 `minutes / 60` 小时',
              '差的绝对值若大于 180°，改成 `360 −` 它'],
        summary=['时间、空间都是 `O(1)`',
                 '易错点：`hour == 12` 要当作 0；时针要加上 `minutes / 60` 的偏移',
                 '易错点：夹角大于 180° 时要用 360° 去减',
                 '原文 `minutes / 60.0` 本身就是浮点除法，Python 3 下无需修改，代码未改动'],
    ),
)
