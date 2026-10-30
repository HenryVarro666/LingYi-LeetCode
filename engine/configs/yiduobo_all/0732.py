def _tl(S):
    tl = S.get('self.time_list')
    return [(str(v), 'green' if v % 2 == 0 else 'pink') for v in sorted(tl)] if tl else []


def _chips(title, items_fn, hl_fn):
    """画一排事件小方块：items_fn(S) -> [(文字, 颜色名)]，hl_fn(S, i, item) -> 是否高亮"""
    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 24, T['muted'], bold=True)
        items = items_fn(S)
        if not items:
            cv.text((x0 + 18, y0 + 60), '（空）', 24, T['dim'])
            return
        per = max(1, int((x1 - x0 - 40) // 120))
        for i, (txt, col) in enumerate(items):
            r, c = divmod(i, per)
            X = x0 + 24 + c * 120
            Y = y0 + 60 + r * 90
            cv.rect((X, Y, X + 108, Y + 70), fill=T[col], r=8, alpha=200)
            if hl_fn(S, i, (txt, col)):
                cv.rect((X - 4, Y - 4, X + 112, Y + 74), outline=T['yellow'], width=4, r=10)
            cv.text((X + 54, Y + 35), txt, 26, T['bg'], anchor='mm', bold=True)
    return draw


CONFIG = dict(
    num=732, title='我的日程安排表 III', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='事件排序 + 扫描线',
    tags=['灵神题单'],
    code='''
class MyCalendarThree(object):

    def __init__(self):
        self.time_list = []        

    def book(self, start, end):
        self.time_list.append(start * 2)
        self.time_list.append(end * 2 - 1)

        res = cnt = 0
        for time_point in sorted(self.time_list):
            if time_point & 1:
                cnt -= 1
            else:
                cnt += 1
                res = max(res, cnt)
        
        return res
''',
    call='''c = MyCalendarThree()
out = [c.book(10, 20), c.book(50, 60), c.book(10, 40), c.book(5, 15)]
out''',
    expect=[1, 1, 2, 3],
    views=[
        dict(type='custom', h=330, draw=_chips('sorted(time_list)：绿 = 开始(×2，偶数)，粉 = 结束(×2−1，奇数)',
             lambda S: _tl(S),
             lambda S, i, it: 'time_point' in S and it[0] == str(S['time_point']))),
        dict(type='text', fn=lambda S: (f"扫到 `{S['time_point']}`（{'结束' if S['time_point'] & 1 else '开始'}）：同时进行 `cnt = {S['cnt']}`，最大 `res = {S['res']}`" if 'time_point' in S and 'cnt' in S else (f"本次预订 `[{S['start']}, {S['end']})`" if 'start' in S else ''))),
    ],
    watch=['cnt', ('res', 'res', 'green'), 'time_point'],
    skip=['for time_point'],
    max_steps=110,
    captions={
        'self.time_list = []': '用 `time_list` 存所有预订的开始、结束时间点',
        'self.time_list.append(start * 2)': '开始时间乘 2：`{start} × 2 = {start*2}`（偶数）',
        'self.time_list.append(end * 2 - 1)': '结束时间乘 2 再减 1：`{end} × 2 − 1 = {end*2-1}`（奇数）→ ==区间是左闭右开==，结束点排在同一时刻的开始点之前',
        'res = cnt = 0': '每次预订都重新排序、从头扫一遍',
        'for time_point in sorted': '按时间从小到大处理事件 `{time_point}`',
        'if time_point & 1': lambda S, B, r: (f'`{S.time_point}` 是奇数 → 一个预订结束' if S.time_point & 1 else f'`{S.time_point}` 是偶数 → 一个预订开始'),
        'cnt -= 1': '结束：同时进行的预订 `cnt` → {cnt}',
        'cnt += 1': '开始：同时进行的预订 `cnt` → {cnt}',
        'res = max': '`res = max({B.res}, {cnt}) = {res}`：记录最大重叠（最大 k 次预订）',
        'return res': lambda S, B, r: f'本次预订后，最大 k 次预订 = =={r}==',
    },
    cards=dict(
        one_liner='把开始、结束拆成事件排序，扫描求最大重叠',
        complexity='每次 `book`：时间 `O(n log n)`，空间 `O(n)`',
        problem=['`book(start, end)` 预订半开区间 `[start, end)`',
                 '返回当前所有预订中，==同时重叠次数的最大值== `k`',
                 '示例：`book(10,20)`、`(50,60)`、`(10,40)`、`(5,15)` → `1, 1, 2, 3`'],
        quote='每一次预定都将开始时间与结束时间加入 time_list 中，排序后从头到尾扫描进行统计。同样可以使用乘 2 以及乘 2 减 1 的方式来简化判断。',
        quote_src='—— yiduobo 题解原文',
        idea=['开始 `×2`（偶数），结束 `×2−1`（奇数）：一个数就同时编码了“时间 + 类型”',
              '同一时刻，结束点（奇）比开始点（偶）小一位 → 先结束再开始，区间首尾相接不算重叠',
              '扫描：偶数 `cnt += 1` 并更新最大值，奇数 `cnt -= 1`'],
        summary=['每次 `book` 排序 `O(n log n)`，n 很小时足够；更快可用差分字典或线段树',
                 '结束点写成 `end*2-1` 而不是 `end*2`，是为了半开区间不重叠',
                 '只在 `cnt += 1` 时更新 `res` 即可',
                 '原文为 Python 2 风格，代码无需改动',
                 '和 731（日程安排表 II）同一算法'],
    ),
)
