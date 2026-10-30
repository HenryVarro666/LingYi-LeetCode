ROWS = 2


def _booked(S):
    return S.get('self.booked')


def _mat(S):
    b = _booked(S) or {}
    return [[(b.get(c + str(r)) or 0) for c in 'ABCD'] for r in range(1, ROWS + 1)]


def _color(S, i, j, v):
    if v == 3:
        return 'orange'
    if v == 1:
        return 'green'
    return None


def _status(S):
    b = S.get('self.booked')
    if b is None or 'self.total' not in S:
        return ''
    return f"已预订 =={len(b)}== 个座位，花费总和 `total` = =={S['self.total']}==（绿 = 1 秒，橙 = 3 秒）"


CONFIG = dict(
    num=4080, title='设计公交车座位预订系统', difficulty='Medium', category='设计',
    author='yiduobo', technique='哈希表记座位 + total 累计', tags=[],
    code='''
class BusBooking(object):

    def __init__(self, n):
        self.booked = {}
        self.total = 0

    def toggle(self, seat):

        if seat in self.booked:
            self.total -= self.booked[seat]
            self.booked.pop(seat)
            return

        p = seat[0]
        if (p == 'A' and 'B' + seat[1:] in self.booked) or (p == 'D' and 'C' + seat[1:] in self.booked):
            t = 3
        else:
            t = 1
        
        self.booked[seat] = t
        self.total += t

    def getTotalTime(self):
        return self.total

    def getMinTime(self):
        return len(self.booked)
''',
    call='''bus = BusBooking(2)
out = []
bus.toggle('B1')
bus.toggle('A1')
out.append(bus.getTotalTime())
out.append(bus.getMinTime())
bus.toggle('B1')
out.append(bus.getTotalTime())
out.append(bus.getMinTime())
bus.toggle('C2')
bus.toggle('D2')
out.append(bus.getTotalTime())
out.append(bus.getMinTime())
out''',
    expect=[4, 2, 3, 1, 7, 3],
    max_steps=90,
    views=[
        dict(type='grid', var=_mat, label='座位表（A、D 靠窗，B、C 靠过道；数字 = 预订花费的秒数）',
             rows=['第1排', '第2排'], cols=['A', 'B', 'C', 'D'], color=_color, h=260, cell=110),
        dict(type='map', var='self.booked', label='booked（座位 → 花费）', fmt=lambda k, v: f'{k} → {v} 秒', h=170, font=30),
        dict(type='text', size=30, h=90, fn=_status),
        dict(type='text', size=30, h=80, fn=lambda S: '各次查询的结果 `out` = ' + str(S['out']) if 'out' in S else ''),
    ],
    watch=[('seat', 'seat', 'blue'), ('t', 't', 'orange'), ('total', 'self.total', 'green'), ('out', 'out', 'pink')],
    captions={
        'self.booked = {}': '`booked`：座位 → 预订时花费的秒数，开始为空',
        'self.total = 0': '`total`：当前所有已订座位的花费之和',
        'if seat in self.booked': '`{seat}` 已经订过了吗？→ {"订过，这次是释放" if seat in self.booked else "没订过，这次是预订"}',
        'self.total -= self.booked[seat]': '释放 `{seat}`：把它当时的花费 `{B.self.booked[seat]}` 从 `total` 减掉 → `{self.total}`',
        'self.booked.pop(seat)': '`{seat}` 从 `booked` 弹出，座位空出来',
        12: '释放完毕，直接返回',
        'p = seat[0]': '取座位字母 `{p}`，看它是不是靠窗的 A / D',
        'if (p ==': '靠窗座位（A、D）要看相邻过道（A 看 B，D 看 C）是否已被订：{"相邻过道已订 → 要 3 秒" if (p == "A" and "B" + seat[1:] in self.booked) or (p == "D" and "C" + seat[1:] in self.booked) else ("过道座位，不受影响，1 秒" if p in "BC" else "相邻过道还空着，1 秒")}',
        't = 3': '相邻过道座位已被订 → 这次花费 `t = 3`',
        't = 1': '过道座位，或相邻过道还空着 → 花费 `t = 1`',
        'self.booked[seat] = t': '花费在预订时就定下来：`booked[{seat}] = {t}`',
        'self.total += t': '`total` 加上 `{t}` → =={self.total}==',
        'return self.total': '`getTotalTime`：直接返回 `total` = =={self.total}==',
        'return len(self.booked)': '`getMinTime`：可以重排成先订靠窗、再订过道，每个都是 1 秒 → 已订个数 =={len(self.booked)}==',
        'out.append': '记录结果：`out` = {out}',
    },
    cards=dict(
        one_liner='哈希表记下每个座位当时花的秒数，total 累加',
        complexity='每个操作 `O(1)`，空间 `O(已订座位数)`',
        problem=['公交车 `n` 排，每排 `A B C D`；`A`、`D` 靠窗，`B`、`C` 靠过道',
                 '订过道座位 1 秒；订靠窗座位，若相邻过道已被订则 3 秒，否则 1 秒',
                 '`toggle` 预订/释放；`getTotalTime` 按实际顺序的总时间；`getMinTime` 最优顺序的总时间',
                 '本视频：`n = 2`，依次 toggle `B1 A1 B1 C2 D2`'],
        quote='综合起来，在这里就只需要使用一个哈希表booked，key是目前已经预订的座位标号，value是花费的时间。同时还需要使用一个变量total记录预订所有座位花费的总时间。',
        quote_src='—— yiduobo 题解原文',
        idea=['座位花费在预订那一刻就定了，之后别人订/退都不影响它',
              '所以用 `booked[座位] = 花费` 存下来，释放时按它减去 `total`',
              '最小总时间：先订靠窗再订过道，每个都只要 1 秒 → 就是已订个数'],
        summary=['`toggle` / `getTotalTime` / `getMinTime` 都是 `O(1)`',
                 '易错：释放座位要减去==当时==的花费，而不是重新算',
                 '相邻关系：`A` 邻 `B`，`D` 邻 `C`，排号相同',
                 '代码原文即 Python 3 可运行，未做修改'],
    ),
)
