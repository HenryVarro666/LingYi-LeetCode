TRIPS, CAP = [[2, 1, 5], [3, 5, 7], [1, 2, 4]], 3
LO, HI = 0, 8


def _phase(S):
    ln = S.get('_line')
    return 1 if ln in (4, 5, 6, 7) else 2 if ln in (10, 11, 12, 13, 14, 16) else 3 if ln == 18 else 0


def _cur_trip(S):
    if _phase(S) != 1 or 'start' not in S:
        return None
    t = [S['num'], S['start'], S['end']]
    return TRIPS.index(t) if t in TRIPS else None


def _order():
    info = []
    for num, start, end in TRIPS:
        info.append([num, start * 2])
        info.append([num, end * 2 - 1])
    return sorted(info, key=lambda d: d[1])


def _cur_ev(S):
    # 第二趟：正在处理 sorted(info) 中的第几个事件
    if _phase(S) != 2 or 'pos' not in S:
        return None
    for j, (n, p) in enumerate(_order()):
        if p == S['pos'] and n == S['num']:
            return j
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    L, R = x0 + 70, x1 - 40

    def X(v):
        return L + (v - LO) / (HI - LO) * (R - L)

    ph = _phase(S)
    cur = _cur_trip(S)
    cv.text((x0 + 18, y0 + 4), 'trips：[num, start, end]（黄 = 正在拆成两个事件）', 24, T['muted'], bold=True)
    for i, (n, a, b) in enumerate(TRIPS):
        Y = y0 + 44 + i * 42
        done = ph >= 2 or (cur is not None and i < cur) or (i == cur and S.get('_line') == 7)
        fill = T['yellow'] if i == cur else (T['blue'] if done else (60, 66, 76))
        cv.rect((X(a), Y, X(b), Y + 32), fill=fill, r=9)
        cv.text(((X(a) + X(b)) / 2, Y + 16), f'{n} 人 {a}→{b}', 20, T['bg'] if (done or i == cur) else T['text'],
                anchor='mm', bold=True)
    ay = y0 + 44 + len(TRIPS) * 42 + 10
    cv.line([(L, ay), (R, ay)], T['border'], 2)
    for v in range(LO, HI + 1):
        cv.line([(X(v), ay), (X(v), ay + 6)], T['border'], 2)
        cv.text((X(v), ay + 8), v, 18, T['dim'], anchor='mt')
    j = _cur_ev(S)
    if j is not None:
        n, p = _order()[j]
        x = X(p / 2) if p % 2 == 0 else X((p + 1) / 2)
        cv.dashed((x, y0 + 36), (x, ay), T['yellow'], 2)
    # info 事件卡片：起点 ×2（偶数），终点 ×2−1（奇数）
    info = S.get('info')
    ey = ay + 50
    if ph >= 2 or ph == 0 and info and len(info) == 2 * len(TRIPS):
        evs, head = _order(), 'sorted(info, key=pos)：同一地点 end×2−1 < start×2 → ==先下后上=='
    else:
        evs, head = (info or []), 'info：[num, pos]，pos = start×2（上车）或 end×2−1（下车）'
    cv.rich(x0 + 18, ey, head, x1 - x0 - 40, size=22, accent=T['yellow'], max_lines=1)
    if not evs:
        return
    w = min(150, (x1 - x0 - 40) / max(1, len(evs)))
    run = 0
    for k, (n, p) in enumerate(evs):
        up = p % 2 == 0
        run += n if up else -n
        bx = x0 + 20 + k * w
        done = ph == 3 or (j is not None and (k < j or (k == j and S.get('_line') not in (10, 11))))
        is_cur = j is not None and k == j
        fill = T['yellow'] if is_cur else ((40, 45, 53) if done else T['panel2'])
        cv.rect((bx + 4, ey + 44, bx + w - 4, ey + 120), fill=fill, r=10,
                outline=T['green'] if up else T['pink'], width=3)
        tc = T['bg'] if is_cur else T['text']
        cv.text((bx + w / 2, ey + 64), f'[{n}, {p}]', 22, tc, anchor='mm', mono=True, bold=True)
        where = p // 2 if up else (p + 1) // 2
        cv.text((bx + w / 2, ey + 98), f'{"上" if up else "下"} {n} 人 @{where}', 18,
                T['bg'] if is_cur else (T['green'] if up else T['pink']), anchor='mm', bold=True)
        if done and ph >= 2:
            over = run > CAP
            cv.text((bx + w / 2, ey + 130), f'now={run}', 20, T['red'] if over else T['cyan'], anchor='mt', bold=True)
    # 座位：capacity 个格子，now 个有人
    if 'now' in S:
        now = S['now']
        sy = ey + 190
        cv.text((x0 + 18, sy), f'车上座位（capacity = {CAP}）', 22, T['muted'], bold=True)
        for k in range(max(CAP, now)):
            bx = x0 + 40 + k * 86
            over = k >= CAP
            fill = (T['red'] if over else T['cyan']) if k < now else T['panel2']
            cv.rect((bx, sy + 36, bx + 70, sy + 96), fill=fill, r=10, outline=T['red'] if over else T['border'], width=2)
            if k < now:
                cv.text((bx + 35, sy + 66), '人', 24, T['bg'], anchor='mm', bold=True)
        cv.text((x0 + 40 + max(CAP, now) * 86 + 10, sy + 66), f'now = {now}', 26,
                T['red'] if now > CAP else T['cyan'], anchor='lm', bold=True)


CONFIG = dict(
    num=1094, title='拼车', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='端点排序扫描 · 起点×2、终点×2−1',
    tags=['labuladong', '灵神题单·常用数据结构', '难度分 1441'],
    code='''
class Solution(object):
    def carPooling(self, trips, capacity):

        info = []
        for num, start, end in trips:
            info.append([num, start * 2])
            info.append([num, end * 2 - 1])

        now = 0
        for num, pos in sorted(info, key=lambda d:d[1]):
            if pos % 2 == 0:
                now += num
                if now > capacity:
                    return False
            else:
                now -= num

        return True
''',
    call=f'Solution().carPooling({TRIPS}, {CAP})',
    expect=True,
    views=[
        dict(type='custom', draw=_draw, h=620),
    ],
    watch=['num', ('pos', 'pos', 'yellow'), ('now', 'now', 'cyan'), ('capacity', 'capacity', 'red')],
    captions={
        'info = []': '`info`：把每个行程的起点、终点拆成事件，排序后一趟扫描',
        'for num, start, end in trips': lambda S, B, r: (
            '拆完了，共 {} 个事件'.format(len(S.info)) if 'start' in B and (B.num, B.start, B.end) == (S.num, S.start, S.end)
            else f'行程：`{S.num}` 人从 `{S.start}` 到 `{S.end}`'),
        'info.append([num, start * 2])': '起点 ×2 → `[{num}, {start * 2}]`（==偶数== = 上车）',
        'info.append([num, end * 2 - 1])': lambda S, B, r: (
            f'终点 ×2−1 → `[{S.num}, {S.end * 2 - 1}]`（==奇数== = 下车）' +
            (f'：地点 {S.end} 的上车记作 `{S.end * 2}`，下车比它小 1 → 排序时==先下后上==' if len(S.info) == 2 else '')),
        'now = 0': '`now`：当前车上的人数',
        'for num, pos in sorted': lambda S, B, r: (
            '所有事件都处理完' if 'pos' in B and B.pos == S.pos and B.num == S.num
            else f'按 pos 从小到大：`[{S.num}, {S.pos}]` → 地点 {S.pos // 2 if S.pos % 2 == 0 else (S.pos + 1) // 2} '
                 f'{"上车" if S.pos % 2 == 0 else "下车"}'),
        'if pos % 2 == 0': lambda S, B, r: (f'`{S.pos}` 是偶数 → 起点，有人上车' if S.pos % 2 == 0
                                            else f'`{S.pos}` 是奇数 → 终点，有人下车'),
        'now += num': '上车 {num} 人：`now = {B.now} + {num}` = =={now}==',
        'if now > capacity': lambda S, B, r: (f'`{S.now} > {S.capacity}`：超载！' if S.now > S.capacity
                                              else f'`{S.now} ≤ {S.capacity}`：坐得下' +
                                              ('（==刚好坐满==：2 人先在 5 下车，3 人才上车）' if S.pos == 10 else '')),
        'return False': '超载 → `False`',
        'now -= num': '下车 {num} 人：`now = {B.now} − {num}` = =={now}==（下车不会超载，不用比较）',
        'return True': '全程 `now ≤ capacity` → 返回 `True`',
    },
    cards=dict(
        one_liner='起点、终点排序后一趟扫描；起点×2、终点×2−1 让同一地点先下后上',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`trips[i] = [num, from, to]`：num 名乘客在 from 上车、to 下车，车只往东开',
                 '车上座位 `capacity`；乘客==先下后上==，能接送所有人返回 `true`',
                 '示例：`[[2,1,5],[3,3,7]], capacity = 4` → `false`',
                 f'本视频：`{TRIPS}`，`capacity = {CAP}` → `true`（地点 5 先下 2 人再上 3 人）'],
        quote='由于这里可以先下后上……若某个起点和另一个终点相同，那么在排序时终点的优先级是高于起点的。……可以使用一个小技巧，将==起点乘以2，将终点乘以2然后减去1==',
        quote_src='—— yiduobo 题解原文',
        idea=['把所有起点、终点从小到大排序，`now` 记车上人数',
              '遇到起点 `now += num` 并和 capacity 比较；遇到终点 `now -= num`',
              '同一地点要先处理终点：`end×2−1` 比 `start×2` 小，==奇偶性==还能区分上下车'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错：同一地点若先上后下，本例地点 5 会算成 2+3 = 5 > 3，误判超载',
                 '只在上车时比较 capacity 就够了：下车只会让人数变少',
                 '也可以用差分数组：`d[from] += num`，`d[to] −= num` 再累加（见灵神写法）',
                 '原文为 Python 2 风格（`class Solution(object)`），代码无需改动'],
    ),
)
