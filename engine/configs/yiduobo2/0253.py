IV = [[0, 30], [5, 10], [10, 20]]


def _cur(S):
    if S.get('_line') in (9, 10, 11, 12, 13, 15) and 't' in S and 'p' in S:
        return (S['t'], S['p'])
    return None


def _applied(S):
    return S.get('_line') in (11, 13, 15)


def _done(S, ev):
    cur = _cur(S)
    if S.get('_line') == 17:
        return True
    if cur is None:
        return False
    return tuple(ev) < cur or (tuple(ev) == cur and _applied(S))


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    lo, hi = 0, 32
    L, R = x0 + 70, x1 - 40

    def X(v):
        return L + (v - lo) / (hi - lo) * (R - L)

    cv.text((x0 + 18, y0 + 4), '会议时间轴（左闭右开；绿 = 正在开）', 24, T['muted'], bold=True)
    sweeping = S.get('_line') in (9, 10, 11, 12, 13, 15, 17) and 'time_points' in S and S.get('t') is not None
    for k, (a, b) in enumerate(IV):
        Y = y0 + 56 + k * 62
        active = sweeping and _done(S, (a, 1)) and not _done(S, (b, 0))
        c = T['green'] if active else (T['dim'] if sweeping and _done(S, (b, 0)) else T['blue'])
        cv.rect((X(a), Y, X(b), Y + 34), fill=c, r=10)
        cv.text((X(a) + 10, Y + 17), f'[{a}, {b})', 20, T['bg'], anchor='lm', bold=True)
    axis_y = y0 + 56 + len(IV) * 62 + 6
    cv.line([(L, axis_y), (R, axis_y)], T['border'], 2)
    for v in range(0, 31, 5):
        cv.line([(X(v), axis_y), (X(v), axis_y + 8)], T['border'], 2)
        cv.text((X(v), axis_y + 12), v, 18, T['dim'], anchor='mt')
    cur = _cur(S)
    if cur is not None and S.get('_line') != 17:
        t, p = cur
        cv.dashed((X(t), y0 + 40), (X(t), axis_y), T['yellow'], 3)
        cv.text((X(t), axis_y + 36), f't = {t}', 22, T['yellow'], anchor='mt', bold=True)
    # 排好序的时间点
    tp = S.get('time_points')
    ey = axis_y + 84
    head = 'sorted(time_points)：[时间, 类型]，0 = 结束，1 = 开始（同一时刻先结束）' if sweeping or S.get('_line') == 17 \
        else 'time_points：[时间, 类型]，0 = 结束，1 = 开始'
    cv.text((x0 + 18, ey), head, 22, T['muted'], bold=True)
    if not tp:
        return
    evs = sorted(tp) if sweeping or S.get('_line') == 17 else tp
    w = min(118, (x1 - x0 - 40) / max(1, len(evs)))
    run = 0
    for k, (t, p) in enumerate(evs):
        run += 1 if p else -1
        if sweeping and _done(S, (t, p)):
            cv.text((x0 + 20 + k * w + w / 2, ey + 112), f'cnt={run}', 20, T['green'], anchor='mt', bold=True)
        bx = x0 + 20 + k * w
        done = sweeping and _done(S, (t, p))
        is_cur = cur is not None and (t, p) == cur
        fill = T['yellow'] if is_cur else (T['panel2'] if not done else (40, 45, 53))
        cv.rect((bx + 4, ey + 40, bx + w - 4, ey + 100), fill=fill, r=10,
                outline=T['green'] if p == 1 else T['pink'], width=3)
        cv.text((bx + w / 2, ey + 58), f'[{t},{p}]', 22, T['bg'] if is_cur else (T['dim'] if done else T['text']), anchor='mm', mono=True, bold=True)
        cv.text((bx + w / 2, ey + 86), '开始' if p else '结束', 18, T['bg'] if is_cur else (T['green'] if p else T['pink']), anchor='mm')


def _cap_for2(S, B, ret):
    if B.get('t') == S.get('t') and B.get('p') == S.get('p') and 't' in B:
        return '所有时间点处理完毕'
    kind = '有会议==开始==' if S.p == 1 else '有会议==结束=='
    extra = '（`[10, 0]` 排在 `[10, 1]` 前面：同一时刻==先结束再开始==）' if S.t == 10 and S.p == 0 else ''
    return f'从小到大扫描：`t = {S.t}`，{kind}{extra}'


CONFIG = dict(
    num=253, title='会议室 II', difficulty='Medium', category='普通数组',
    author='yiduobo', technique='差分 / 扫描线：数同时进行的会议',
    tags=['热题173'],
    code='''
class Solution(object):
    def minMeetingRooms(self, intervals):
        res = cnt = 0
        time_points = []
        for x, y in intervals:
            time_points.append([x, 1])
            time_points.append([y, 0])

        for t, p in sorted(time_points):
            if p == 0:
                cnt -= 1
            else:
                cnt += 1

            res = max(res, cnt)

        return res
''',
    call=f'Solution().minMeetingRooms({IV})',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('t', 't', 'yellow'), 'p', ('cnt', 'cnt', 'green'), ('res', 'res', 'orange')],
    captions={
        'res = cnt = 0': '`cnt`：当前==正在召开==的会议数；`res`：cnt 的最大值，就是需要的会议室数',
        'time_points = []': '把每个区间拆成两个时间点',
        'for x, y in intervals': lambda S, B, r: (f'会议 `[{S.x}, {S.y})`' if (B.get('x'), B.get('y')) != (S.get('x'), S.get('y')) or 'x' not in B
                                                  else '所有会议都拆完了'),
        'time_points.append([x, 1])': '`[{x}, 1]`：时刻 {x} 有会议开始（类型 1）',
        'time_points.append([y, 0])': lambda S, B, r: (f'`[{S.y}, 0]`：时刻 {S.y} 有会议结束（类型 0）——结束标 0，排序时就排在同一时刻的开始前面'
                                                       if len(S.time_points) == 2 else f'`[{S.y}, 0]`：时刻 {S.y} 有会议结束'),
        'for t, p in sorted': _cap_for2,
        'if p == 0': lambda S, B, r: ('`p == 0`：结束事件' if S.p == 0 else '`p == 1`：开始事件'),
        'cnt -= 1': '一场会议结束，腾出一间：`cnt` = {B.cnt} − 1 = =={cnt}==',
        'cnt += 1': '一场会议开始，占用一间：`cnt` = {B.cnt} + 1 = =={cnt}==',
        'res = max': '`res = max({B.res}, {cnt}) = {res}`',
        'return res': '同一时刻最多有 =={ret}== 场会议在开 → 需要 {ret} 间会议室',
    },
    cards=dict(
        one_liner='把会议拆成“开始 +1 / 结束 −1”的时间点，扫描时 cnt 的最大值就是答案',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给一组会议时间 `intervals[i] = [start, end]`（左闭右开）',
                 '求==最少需要多少间会议室==，才能让所有会议都开得了',
                 '示例：`[[0,30],[5,10],[15,20]]` → `2`',
                 '本视频：`[[0,30],[5,10],[10,20]]` → `2`（10 时刻一场结束、一场开始）'],
        quote='使用一个计数器cnt表示当前正在召开的会议，然后从小到大遍历所有的时间点……在计算cnt时如果碰到相同的时间点，则应该==先处理结束的会议，再处理新召开的会议==。',
        quote_src='—— yiduobo 题解原文',
        idea=['问题等价于：==最多有几个区间同时重叠==',
              '开始时间点 `cnt += 1`，结束时间点 `cnt -= 1`（差分），每次用 cnt 更新答案',
              '区间左闭右开：结束标 `0`、开始标 `1`，`sorted` 自动让同一时刻的结束排在前面'],
        result='`res = 2`：最多两场会议同时进行',
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错：同一时刻先结束后开始；若反过来，本例会错误地得到 3',
                 '编码技巧：用 `[t, 0/1]` 让排序顺手处理并列情况，不用写比较函数',
                 '另一种常见写法：按开始时间排序 + 最小堆存结束时间',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
