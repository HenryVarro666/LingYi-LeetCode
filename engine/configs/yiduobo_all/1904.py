def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    s, e = S.get('start'), S.get('end')
    cv.text((x0 + 18, y0 + 4), '时间轴（分钟，每格 = 一刻钟）：绿 = 完整对局', 24, T['muted'], bold=True)
    if s is None or e is None:
        return
    lo = s // 15 * 15
    hi = (e + 14) // 15 * 15
    n = max(1, (hi - lo) // 15)
    w = (x1 - x0 - 60) / n
    base = y0 + 190
    for j in range(n):
        a = lo + 15 * j
        X = x0 + 30 + j * w
        ok = a >= s and a + 15 <= e
        cv.rect((X + 2, base - 60, X + w - 2, base), fill=T['green'] if ok else (60, 66, 76), r=6, alpha=200 if ok else 255)
        cv.text((X, base + 8), f'{a // 60 % 24:02d}:{a % 60:02d}', 15, T['dim'], anchor='mt', mono=True)
    for v, name, c in ((s, 'start', T['blue']), (e, 'end', T['pink'])):
        X = x0 + 30 + (v - lo) / 15 * w
        cv.line([(X, base - 90), (X, base + 4)], c, 4)
        if name == 'end' and abs(e - s) < 60:
            cv.text((X + 8, base + 40), f'{name}={v}', 20, c, anchor='lt', bold=True)
        else:
            cv.text((X + (14 if X < x0 + 120 else 0), base - 96), f'{name}={v}', 20, c, anchor='lb' if X < x0 + 120 else 'mb', bold=True)


CONFIG = dict(
    num=1904, title='你完成的完整对局数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='转成分钟 · 起点向上、终点向下取整 · 跨天拆两段',
    tags=[],
    code='''
class Solution(object):
    def numberOfRounds(self, loginTime, logoutTime):

        login_hour, login_minute = loginTime.split(':')
        start = int(login_hour) * 60 + int(login_minute)
        logout_hour, logout_minute = logoutTime.split(':')
        end = int(logout_hour) * 60 + int(logout_minute)
        if start <= end:
            return self.calc(start, end)
        else:
            return self.calc(start, 1440) + self.calc(0, end)
    
    def calc(self, start, end):
        if start % 15 != 0:
            start = start // 15 * 15 + 15
        end = end // 15 * 15
        return max(0, (end - start) // 15)
''',
    call='Solution().numberOfRounds("23:50", "00:40")',
    expect=2,
    views=[dict(type='custom', draw=_draw, h=330),
           dict(type='text', size=30, h=100, fn=lambda S: (
               f"从 `{S['start']}` 到 `{S['end']}` 分钟" if 'start' in S and 'end' in S else ''))],
    watch=['loginTime', 'logoutTime', ('start', 'start', 'blue'), ('end', 'end', 'pink')],
    captions={
        'login_hour, login_minute': '拆开 `{loginTime}`：小时 `{login_hour}`，分钟 `{login_minute}`',
        'start = int': '统一成分钟：`start = {start}`',
        'logout_hour, logout_minute': '拆开 `{logoutTime}`：小时 `{logout_hour}`，分钟 `{logout_minute}`',
        'end = int': '统一成分钟：`end = {end}`',
        'if start <= end': lambda S, B, r: (f'`{S.start} <= {S.end}`：同一天内，直接算 `start → end`' if S.start <= S.end
                                            else f'`{S.start} > {S.end}`：跨过午夜 → ==拆成两段：`start → 1440` 和 `0 → end`=='),
        'return self.calc(start, end)': '同一天：答案 = `calc({B.start}, {B.end})`，交给 calc 去算',
        'return self.calc(start, 1440)': '通宵：答案 = `calc({B.start}, 1440) + calc(0, {B.end})`，两段分别交给 calc 算再相加',
        'if start % 15': lambda S, B, r: (f'`{S.start} % 15 != 0`：起点不在整刻钟上 → 要==向上取整==到下一个整点' if S.start % 15
                                          else f'`{S.start} % 15 == 0`：起点正好在整刻钟上，不用动'),
        'start = start // 15': '向上取整：`start // 15 * 15 + 15` = =={start}==（原文 `/` 为 Python 2 整除）',
        'end = end // 15': '终点向下取整：`end // 15 * 15` = =={end}==',
        'return max(0': lambda S, B, r: f'`({S.end} − {S.start}) // 15 = {(S.end - S.start) // 15}`' + ('，是负数 → `max(0, …)` 兜成 0' if S.end < S.start else f'，这一段有 =={r}== 局')
    },
    cards=dict(
        one_liner='起点向上取整、终点向下取整，跨天就拆成两段',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['每刻钟开一局，每局 15 分钟，数完整打完的局数',
                 '登录 `loginTime`、登出 `logoutTime`，登出早于登录表示通宵',
                 '本视频：`23:50 → 00:40` → `2`'],
        quote='起始时间就应该除以15向上取整，而结束时间则应该除以15向下取整。如果使用这种计算方式，有一个需要特别注意的地方是当出现起始时和结束时间在同一个十五分钟内……会得到-1这样奇怪的答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把小时换成分钟，单位统一',
              '起点 `< ` 终点：一天内一段；否则拆成「起点到 24:00」和「0:00 到终点」两段',
              '每一段：起点向上、终点向下取整到刻钟，再除以 15；负数用 `max(0, ...)` 兜底'],
        summary=['原文为 Python 2 写法，`calc` 里的整数除法 `/` 已改为 `//`',
                 '时间 `O(1)`，空间 `O(1)`',
                 '易错点：起点已在整刻钟时不能再 +15；同一刻钟内进出差值为负，要取 0',
                 '对比灵神：灵神只向下取整终点，靠整除自然处理起点；yiduobo 两端都显式取整'],
    ),
)
