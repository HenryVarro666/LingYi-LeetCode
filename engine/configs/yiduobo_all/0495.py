def _axis(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    ts, d = S['timeSeries'], S['duration']
    if 'start' not in S:
        return
    hi = ts[-1] + d
    cell = min(60, (x1 - x0 - 60) / (hi + 1))
    sx = x0 + 30
    base = y1 - 70
    cv.text((x0 + 18, y0 + 4), '时间轴：灰条 = 每次攻击的中毒区间，蓝条 = 当前合并区间 [start, now]', 22, T['muted'], bold=True)
    cur = S.get('time')
    for k, t in enumerate(ts):
        a, b = t, t + d - 1
        y = y0 + 60 + (k % 2) * 34
        hot = cur == t and S['_line'] in (11, 12)
        cv.rect((sx + a * cell, y, sx + (b + 1) * cell, y + 26), fill=T['orange'] if hot else (90, 98, 110), alpha=255, r=4)
        cv.text((sx + a * cell + 6, y + 13), f'{a}~{b}', 16, T['text'], anchor='lm', mono=True)
    st, nw = S['start'], S['now']
    y = y0 + 150
    cv.rect((sx + st * cell, y, sx + (nw + 1) * cell, y + 46), fill=T['blue'], alpha=210, r=6)
    cv.text((sx + (st + nw + 1) * cell / 2, y + 23), f'[{st}, {nw}]  长 {nw - st + 1}', 22, T['bg'], anchor='mm', bold=True)
    cv.line([(sx, base), (sx + (hi + 1) * cell, base)], T['border'], 2)
    for t in range(hi + 1):
        cv.text((sx + t * cell + cell / 2, base + 6), t, 16, T['dim'], anchor='mt', mono=True)
    cv.text((x0 + 18, y1 - 30), f"已累计 res = {S.get('res', 0)}", 24, T['green'], anchor='lm', bold=True)


CONFIG = dict(
    num=495, title='提莫攻击', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='区间合并 · 一趟扫描',
    code='''
class Solution(object):
    def findPoisonedDuration(self, timeSeries, duration):

        if not timeSeries:
            return 0

        res = 0
        start = timeSeries[0]
        now = timeSeries[0] + duration - 1
        for time in timeSeries[1:]:
            if now < time:
                res += now - start + 1
                start = time
            now = time + duration - 1

        return res + now - start + 1
''',
    call='Solution().findPoisonedDuration([1, 4, 8, 9, 12], 3)',
    expect=13,
    views=[
        dict(type='array', var='timeSeries', pointers={}, h=150, label='timeSeries（攻击时刻）',
             color=lambda S, i, v: 'pink' if S.get('time') == v else None),
        dict(type='custom', draw=_axis, h=400),
    ],
    watch=[('start', 'start', 'blue'), ('now', 'now', 'cyan'), ('time', 'time', 'pink'), ('res', 'res', 'green')],
    captions={
        'if not timeSeries': '没有攻击就没有中毒：空数组直接返回 `0`',
        'start = timeSeries[0]': '第一个区间的左端点 `start = {start}`',
        'now = timeSeries[0]': '第一个区间的右端点 `now = {start} + {duration} - 1 = {now}`：中毒覆盖 `[{start}, {now}]`',
        'for time': lambda S, B, r: ('所有攻击都扫完了，跳出循环' if B.get('time') == S.time and S.time == S.timeSeries[-1] else f'依次看下一次攻击 `time = {S.time}`（区间已按左端点排好序）'),
        'if now < time': lambda S, B, r: (f'`now = {S.now} < time = {S.time}`：新区间从 {S.time} 开始，和上一段==不相交== → 上一段可以结算' if S.now < S.time
                                         else f'`now = {S.now} ≥ time = {S.time}`：新区间的左端点落在上一段里 → ==合并==，不结算'),
        'res += now': '结算上一段：`{B.res} + ({now} - {start} + 1) = {res}`',
        'start = time': '新的一段从 `{time}` 开始：`start = {start}`',
        'now = time': '无论合不合并，右端点都推到 `{time} + {duration} - 1 = {now}`',
        'return res': '别忘了最后一段：`{res} + ({now} - {start} + 1)` = =={ret}==',
    },
    cards=dict(
        one_liner='把每次攻击看成区间，合并重叠后累加长度',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['提莫每次攻击让敌人中毒 `duration` 秒；中毒期间再次攻击，只重置计时、不叠加',
                 '给定升序的攻击时刻 `timeSeries`，求总中毒秒数',
                 '示例：`[1,4]`，`duration=2` → `4`；本视频：`[1,4,8,9,12]`，`duration=3` → `13`'],
        quote='看着题目描述花里胡哨的，但是实际上就是区间合并的问题，而且这里区间已经天然按左边界排好序了，于是只需要一趟扫描。',
        quote_src='—— yiduobo 题解原文',
        idea=['每次攻击对应区间 `[time, time+duration-1]`',
              '新区间左端点 ≤ 上一段右端点：合并，右端点推到新的',
              '否则：结算上一段长度，当前区间成为新的上一段'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '扫描结束后，==最后一段还没结算==，要在 return 里补上',
                 '区间是闭区间 `[time, time+duration-1]`，长度要 `+ 1`',
                 '对比公式法：每次加 `min(间隔, duration)`，本文用的是区间合并'],
    ),
)
