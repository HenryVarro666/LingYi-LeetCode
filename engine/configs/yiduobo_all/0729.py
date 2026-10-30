BOOKS = [(10, 20), (15, 25), (20, 30), (5, 10), (25, 35)]
TMAX = 40


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '时间轴（半开区间 [start, end)；蓝 = 已存日程，黄框 = 正在比较，绿/红 = 新日程）', 24, T['muted'], bold=True)
    lx0, lx1 = x0 + 50, x1 - 40
    sc = (lx1 - lx0) / TMAX
    base = y1 - 60
    cv.line([(lx0, base), (lx1, base)], T['border'], 3)
    for u in range(0, TMAX + 1, 5):
        cv.line([(lx0 + u * sc, base - 6), (lx0 + u * sc, base + 6)], T['border'], 2)
        cv.text((lx0 + u * sc, base + 12), u, 18, T['dim'], anchor='mt', mono=True)
    cal = S.get('self.canlendar') or []
    ln = S.get('_line')
    cmp = (S.get('now_start'), S.get('now_end')) if ln in (7, 8, 9) and 'now_start' in S else None
    row_h = 44
    top = y0 + 84
    if 'start' in S and cmp is not None and ln in (8, 9):
        a, b = cmp
        lo, hi = max(a, S['start']), min(b, S['end'])
        if lo < hi:
            cv.rect((lx0 + lo * sc, top - 4, lx0 + hi * sc, base - 20), fill=T['red'], alpha=60)
    cv.text((lx0, top - 8), '已存日程 self.canlendar', 20, T['muted'], anchor='lb')
    for k, (a, b) in enumerate(cal):
        y = top + k * (row_h + 8)
        is_cmp = cmp is not None and (a, b) == cmp and ln in (8, 9)
        cv.rect((lx0 + a * sc, y, lx0 + b * sc, y + row_h), fill=T['blue'], alpha=200, r=6,
                outline=T['yellow'] if is_cmp else None, width=4 if is_cmp else 1)
        cv.text((lx0 + (a + b) / 2 * sc, y + row_h / 2), f'[{a}, {b})', 20, T['bg'], anchor='mm', bold=True)
    if 'start' in S and ln is not None and ln >= 7:
        s, e = S['start'], S['end']
        y = base - row_h - 24
        bad = ln == 9
        ok = ln in (11, 12)
        col = T['red'] if bad else (T['green'] if ok else T['orange'])
        cv.rect((lx0 + s * sc, y, lx0 + e * sc, y + row_h), fill=col, alpha=200, r=6)
        cv.text((lx0 + (s + e) / 2 * sc, y + row_h / 2), f'新 [{s}, {e})', 20, T['bg'], anchor='mm', bold=True)


def _if(S, B, ret):
    s, e, a, b = S.start, S.end, S.now_start, S.now_end
    if s < b and e > a:
        return f'`{s} < {b}` 且 `{e} > {a}`：新日程和 `[{a}, {b})` ==相交== → 重复预订'
    why = f'`start = {s} ≥ now_end = {b}`' if s >= b else f'`end = {e} ≤ now_start = {a}`'
    return f'{why}：和 `[{a}, {b})` 不相交，看下一个'


CONFIG = dict(
    num=729, title='我的日程安排表 I', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='朴素枚举判相交',
    tags=['labuladong', '灵神题单·常用数据结构'],
    code='''
class MyCalendar(object):

    def __init__(self):
        self.canlendar = []

    def book(self, start, end):
        for now_start, now_end in self.canlendar:
            if start < now_end and end > now_start:
                return False

        self.canlendar.append([start, end])
        return True
''',
    call=f'''c = MyCalendar()
ans = [c.book(s, e) for s, e in {BOOKS}]
ans''',
    expect=[True, False, True, True, False],
    views=[
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=[('start', 'start', 'orange'), ('end', 'end', 'orange'), ('now_start', 'now_start', 'blue'),
           ('now_end', 'now_end', 'blue'), ('已存', lambda S: len(S.get('self.canlendar') or []), 'green')],
    captions={
        'self.canlendar = []': '用一个数组存所有已经成功的日程',
        'for now_start, now_end in self.canlendar': lambda S, B, r: (
            f'book({S.start}, {S.end})：枚举已有日程 `[{S.now_start}, {S.now_end})`'
            if 'now_start' in S and (B.get('now_start'), B.get('now_end'), B.get('start')) != (S.now_start, S.now_end, S.start)
            else (f'book({S.start}, {S.end})：日程表为空，直接可以加入' if not S['self.canlendar']
                  else '所有已有日程都不相交')),
        'if start < now_end and end > now_start': _if,
        'return False': '出现相交 → 返回 ==False==，不加入日程表',
        'self.canlendar.append([start, end])': '没有相交 → 把 `[{start}, {end}]` 加入日程表',
        'return True': '返回 ==True==',
    },
    cards=dict(
        one_liner='操作次数很少：新日程和已有日程逐个判相交就够了',
        complexity='每次 `book` 时间 `O(n)`，总 `O(n^2)`，空间 `O(n)`',
        problem=['实现 `MyCalendar`：`book(start, end)` 预订半开区间 `[start, end)`',
                 '与已有日程有交叉就返回 `false` 且不加入，否则加入并返回 `true`',
                 '示例：`book(10,20), book(15,25), book(20,30)` → `true, false, true`',
                 '本视频再加 `book(5,10)`、`book(25,35)` → `true, false`'],
        quote='对于新来的start和end，枚举之前已经有的所有start和end，判断是否会出现相交的情况。若出现，那么返回false，否则将新来的start和end加入日程表数组，然后返回true。',
        quote_src='—— yiduobo 题解原文',
        idea=['两个半开区间 `[s, e)`、`[a, b)` 相交 ⇔ `s < b` 且 `e > a`',
              '调用次数不超过 1000，`O(n^2)` 的朴素做法已经足够',
              '只有不和任何日程相交时才加入数组'],
        summary=['每次 `book` 是 `O(n)`，`n` 次总共 `O(n^2)`',
                 '易错：半开区间，`[10,20)` 和 `[20,30)` ==不相交==，所以用严格的 `<`、`>`',
                 '更快的做法：有序结构二分找相邻区间（`O(log n)`），或动态开点线段树',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行'],
    ),
)
