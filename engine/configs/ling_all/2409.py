from itertools import accumulate as _acc
_DS = list(_acc((31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31), initial=0))
_AA, _LA, _AB, _LB = '08-15', '08-18', '08-16', '08-19'


def _d(s):
    return _DS[int(s[:2]) - 1] + int(s[3:])


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    a1, a2, b1, b2 = _d(_AA), _d(_LA), _d(_AB), _d(_LB)
    lo, hi = min(a1, b1) - 1, max(a2, b2) + 1
    n = hi - lo + 1
    cell = min(120, (x1 - x0 - 150) / n)
    sx = x0 + 120
    cv.text((x0 + 18, y0 + 4), '一年中的第几天（把 "MM-DD" 换成整数后，就是两个闭区间）', 22, T['muted'], bold=True)
    rows = [('Alice', a1, a2, T['blue'], y0 + 90), ('Bob', b1, b2, T['pink'], y0 + 190)]
    for name, l, r, c, y in rows:
        cv.text((x0 + 20, y + 28), name, 26, c, anchor='lm', bold=True)
        cv.rect((sx + (l - lo) * cell + 3, y, sx + (r - lo + 1) * cell - 3, y + 56), fill=c, alpha=200, r=10)
    ya = y0 + 290
    for d in range(lo, hi + 1):
        X = sx + (d - lo) * cell
        cv.rect((X + 2, ya, X + cell - 2, ya + 50), fill=T['panel2'], r=6, outline=T['border'])
        cv.text((X + cell / 2, ya + 25), d, 22, T['text'], anchor='mm', mono=True)
        cv.line([(X + cell / 2, y0 + 82), (X + cell / 2, ya)], T['border'], 1)
    cv.text((x0 + 20, ya + 25), '日期', 24, T['muted'], anchor='lm')
    L = S.get('left')
    R = S.get('right')
    if isinstance(L, int) and isinstance(R, int):
        cv.rect((sx + (L - lo) * cell + 1, y0 + 74, sx + (R - lo + 1) * cell - 1, ya + 60), outline=T['yellow'], width=5, r=12)
        cv.text((sx + (L - lo) * cell, ya + 76), f'left = {L}', 26, T['yellow'], anchor='lt', bold=True)
        cv.text((sx + (R - lo + 1) * cell, ya + 76), f'right = {R}', 26, T['yellow'], anchor='rt', bold=True)
        cv.text((x0 + 20, ya + 140), f'交集长度 right − left + 1 = {R} − {L} + 1 = {R - L + 1}', 30, T['green'], bold=True)


CONFIG = dict(
    num=2409, title='统计共同度过的日子数', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='日期转整数 · 区间交集',
    tags=[],
    code='''
DAYS_SUM = list(accumulate((31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31), initial=0))

def calc_days(date: str) -> int:
    return DAYS_SUM[int(date[:2]) - 1] + int(date[3:])

class Solution:
    def countDaysTogether(self, arriveAlice: str, leaveAlice: str, arriveBob: str, leaveBob: str) -> int:
        left = calc_days(max(arriveAlice, arriveBob))  # 直接比较字符串再计算
        right = calc_days(min(leaveAlice, leaveBob))
        return max(right - left + 1, 0)  # 答案不能为负数
''',
    call=f'Solution().countDaysTogether({_AA!r}, {_LA!r}, {_AB!r}, {_LB!r})',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', h=80, size=28,
             fn=lambda S: (f"`{S['date']}` → 前面月份天数之和 `{_DS[int(S['date'][:2]) - 1]}` + 日 `{int(S['date'][3:])}` = =={_DS[int(S['date'][:2]) - 1] + int(S['date'][3:])}==" if 'date' in S else '')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('date', 'date')],
    captions={
        'return DAYS_SUM': lambda S, B, ret: f"`{S.date}` 是第 =={ret}== 天：前 `{int(S.date[:2]) - 1}` 个月共 `{_DS[int(S.date[:2]) - 1]}` 天，再加上 `{int(S.date[3:])}` 号",
        'left = calc_days': lambda S, B, ret: (f"交集左端点 = 两个到达日期的==较大者==：`max({S.arriveAlice!r}, {S.arriveBob!r})` = `{max(S.arriveAlice, S.arriveBob)!r}`，换算成第 `{S.left}` 天" if 'left' in S
                                              else f"交集左端点 = 两个到达日期的==较大者==：`max({S.arriveAlice!r}, {S.arriveBob!r})` = `{max(S.arriveAlice, S.arriveBob)!r}`，字符串 `MM-DD` 直接比较就是按日期比较"),
        'right = calc_days': lambda S, B, ret: (f"交集右端点 = 两个离开日期的==较小者==：`min({S.leaveAlice!r}, {S.leaveBob!r})` = `{min(S.leaveAlice, S.leaveBob)!r}`，换算成第 `{S.right}` 天" if 'right' in S
                                               else f"交集右端点 = 两个离开日期的==较小者==：`min({S.leaveAlice!r}, {S.leaveBob!r})` = `{min(S.leaveAlice, S.leaveBob)!r}`"),
        'return max(right': '闭区间含两端：`right − left + 1` = `{right} − {left} + 1` = {right - left + 1}；不相交时是负数或 0，所以和 `0` 取 `max` → ==`{ret}`==',
    },
    cards=dict(
        one_liner='日期换成第几天，问题就变成两个闭区间求交集的整数个数',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['Alice、Bob 分别在罗马待 `[arriveAlice, leaveAlice]`、`[arriveBob, leaveBob]`（日期闭区间，格式 `"MM-DD"`，平年）',
                 '求两人同时在罗马的天数',
                 '示例：`08-15~08-18` 与 `08-16~08-19` → `3`'],
        quote='把字符串日期转换成具体在这一年的第几天，也就是一个整数。那么问题变成：给你两个闭区间，求这两个闭区间的交集区间中的整数个数，这等价于交集区间长度加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`DAYS_SUM` 是每月天数的前缀和：`DAYS_SUM[m-1] + d` 就是第几天',
              '交集左端点 = 左端点的最大值，右端点 = 右端点的最小值',
              '`MM-DD` 补零后，字符串字典序就是日期先后，可以先比字符串再转换'],
        summary=['时间、空间都是 `O(1)`',
                 '易错：闭区间要 `+1`；没有交集时 `right − left + 1` 可能为负，要和 `0` 取 `max`',
                 '一年按平年（2 月 28 天）算',
                 '另一种写法：用 `datetime.strptime` 解析，默认 1900 年是平年，再相减取 `.days`'],
    ),
)
