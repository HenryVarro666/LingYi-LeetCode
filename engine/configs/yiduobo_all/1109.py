BOOK, N = [[1, 2, 10], [2, 3, 20], [2, 5, 25]], 5


def _phase(S):
    ln = S.get('_line')
    if ln in (5, 6, 7, 8):
        return 1
    if ln in (10, 11):
        return 2
    return 3 if ln == 13 else 0


def _cur(S):
    # 第一趟循环正在处理的是哪条预订
    if _phase(S) != 1 or 'start' not in S:
        return None
    t = [S['start'], S['end'], S['num']]
    return BOOK.index(t) if t in BOOK else None


def _final(S):
    # 第二趟：已经变成“最终座位数”的最大下标
    ph = _phase(S)
    if ph == 3:
        return N
    if ph != 2:
        return 0
    return S['index'] if S.get('_line') == 11 else S['index'] - 1


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    res = S.get('res')
    ph = _phase(S)
    cell = min(120, (x1 - x0 - 120) / (N + 1))
    sx = x0 + 60 + ((x1 - x0 - 120) - cell * (N + 1)) / 2

    def X(i):
        return sx + i * cell

    # ① 预订区间
    cv.text((x0 + 18, y0 + 4), 'bookings：[first, last, seats]（黄 = 正在处理）', 24, T['muted'], bold=True)
    cur = _cur(S)
    for k, (a, b, s) in enumerate(BOOK):
        Y = y0 + 46 + k * 50
        done = ph >= 2 or (cur is not None and k < cur) or (cur == k and S.get('_line') in (7, 8))
        fill = T['yellow'] if k == cur else (T['blue'] if done else (60, 66, 76))
        cv.rect((X(a) + 4, Y, X(b) + cell - 4, Y + 38), fill=fill, r=10)
        cv.text(((X(a) + X(b) + cell) / 2, Y + 19), f'航班 {a}~{b} 各 +{s}', 22,
                T['bg'] if (k == cur or done) else T['text'], anchor='mm', bold=True)
    # ② res 数组（差分 → 前缀和）
    top = y0 + 46 + len(BOOK) * 50 + 46
    lab = {0: 'res：差分数组（res[0] 不用）', 1: 'res：f[l] += s，f[r+1] −= s',
           2: 'res：从左往右累加（绿 = 已是最终座位数）', 3: 'res：每个航班的座位总数'}[ph]
    cv.text((x0 + 18, top - 36), lab, 24, T['muted'], bold=True)
    if res is None:
        cv.text((x0 + 18, top + 10), '（尚未创建）', 24, T['dim'])
        return
    bres = B.get('res')
    fin = _final(S)
    ch = min(cell * 0.86, 80)
    for i, v in enumerate(res):
        changed = bres is not None and i < len(bres) and bres[i] != v
        if i == 0:
            fill, tc = (34, 38, 46), T['dim']
        elif ph >= 2 and i <= fin:
            fill, tc = T['green'], T['bg']
        else:
            fill, tc = T['panel2'], T['text']
        cv.rect((X(i) + 4, top, X(i) + cell - 4, top + ch), fill=fill, r=8,
                outline=T['yellow'] if changed else T['border'], width=4 if changed else 1)
        cv.text((X(i) + cell / 2, top + ch / 2), str(v), 30 if len(str(v)) < 4 else 24, tc, anchor='mm', bold=True)
        cv.text((X(i) + cell / 2, top + ch + 6), i, 20, T['dim'], anchor='mt', mono=True)
    # ③ 指针
    py = top + ch + 40
    if ph == 1 and cur is not None:
        a, b, s = BOOK[cur]
        cv.tri_up(X(a) + cell / 2, py, 10, T['green'])
        cv.text((X(a) + cell / 2, py + 16), f'+{s}', 22, T['green'], anchor='mt', bold=True)
        if b < N:
            cv.tri_up(X(b + 1) + cell / 2, py, 10, T['pink'])
            cv.text((X(b + 1) + cell / 2, py + 16), f'−{s}', 22, T['pink'], anchor='mt', bold=True)
        else:
            cv.text((X(N) + cell, py + 16), f'end = n：res[{N + 1}] 越界，无需 −{s}', 22, T['pink'], anchor='ra', bold=True)
    elif ph == 2:
        i = S['index']
        cv.tri_up(X(i) + cell / 2, py, 10, T['yellow'])
        cv.text((X(i) + cell / 2, py + 16), 'index', 22, T['yellow'], anchor='mt', bold=True)
        cv.text((X(i - 1) + cell / 2, py + 16), '+', 26, T['muted'], anchor='mt', bold=True)
    elif ph == 3:
        cv.text(((X(1) + X(N) + cell) / 2, py + 10), f'返回 res[1:] = {res[1:]}', 26, T['green'], anchor='mt', bold=True)


def _book(S, B, r):
    if 'start' in B and (B.start, B.end, B.num) == (S.start, S.end, S.num):
        return '所有预订都只改了两个端点；接下来一趟累加还原每个航班的座位数'
    return f'预订 `[{S.start}, {S.end}, {S.num}]`：航班 {S.start}~{S.end} 每个都订了 {S.num} 个座位'


CONFIG = dict(
    num=1109, title='航班预订统计', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='差分数组 · 公交车上下车',
    tags=['labuladong', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def corpFlightBookings(self, bookings, n):

        res = [0] * (n + 1)
        for start, end, num in bookings:
            res[start] += num
            if end < n:
                res[end + 1] -= num

        for index in range(2, n + 1):
            res[index] += res[index - 1]

        return res[1:]
''',
    call=f'Solution().corpFlightBookings({BOOK}, {N})',
    expect=[10, 55, 45, 25, 25],
    views=[
        dict(type='custom', draw=_draw, h=500),
        dict(type='text', h=110, size=26, fn=lambda S: (
            '公交车视角：`res[t]` = 第 t 分钟上下车的==净人数=='
            if S.get('_line') in (4, 5, 6, 7, 8) else
            '车上人数 = `res[1] + … + res[t]`：沿时间轴累加，就是==每个航班的座位数==')),
    ],
    watch=['start', 'end', 'num', ('index', 'index', 'yellow')],
    captions={
        'res = [0]': '`res` 长 `n + 1 = {n + 1}`：下标就是航班编号 1~{n}，`res[0]` 空着不用',
        'for start, end, num': _book,
        'res[start] += num': '第 {start} 分钟有 {num} 人==上车==：`res[{start}] += {num}` → {res[start]}',
        'if end < n': lambda S, B, r: (f'`end = {S.end} < n`：第 {S.end + 1} 分钟这 {S.num} 人要下车' if S.end < S.n
                                       else f'`end = {S.end} = n`：坐到最后一个航班，`res[{S.end + 1}]` 越界，==不用减=='),
        'res[end + 1] -= num': '第 {end + 1} 分钟 {num} 人==下车==：`res[{end + 1}] -= {num}` → {res[end + 1]}',
        'for index in range': lambda S, B, r: (
            f'扫描时间轴：`index = {S.index}`（`res[1]` 本身就是第 1 个航班的答案）' if 'index' not in B
            else ('累加完毕' if B.index == S.index else f'`index = {S.index}`：继续沿时间轴累加')),
        'res[index] += res[index - 1]': '航班 {index} 的座位数 = 上一个航班的 `{res[index - 1]}` + 本处变化 `{B.res[index]}` = =={res[index]}==',
        'return res[1:]': '去掉不用的 `res[0]`，返回 `{ret}`',
    },
    cards=dict(
        one_liner='区间加 s 只改两个端点：f[l] += s，f[r+1] −= s，最后一趟累加',
        complexity='时间 `O(n + m)`，空间 `O(1)`（不算返回值）',
        problem=['有 `n` 个航班，编号 1~n；`bookings[i] = [first, last, seats]`',
                 '表示从 first 到 last（含）的==每个航班==都预订了 seats 个座位',
                 '返回长为 n 的数组：每个航班预订的座位总数',
                 f'示例：`{BOOK}, n = {N}` → `[10,55,45,25,25]`'],
        quote='有一辆公交车……表示有s个人在第l分钟上车，在第r + 1分钟下车……我们需要将==f[l]加上s，将f[r + 1]减去s==，那么在处理now时，扫描整个时间轴，每次将now加上对应的f即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['把航班编号看成时间：预订 `[l, r, s]` = s 人第 l 分钟上车、第 r+1 分钟下车',
              '车上人数 `now`：遇到上车加 s，遇到下车减 s',
              '`f[t]` 记第 t 分钟上下车的净人数，扫一遍时间轴累加，就是每一刻的人数'],
        summary=['时间 `O(n + m)`（m 为预订数），额外空间 `O(1)`',
                 '`end == n` 时 `end + 1` 越界：原文用 `if end < n` 跳过（也可开 `n + 2` 长）',
                 '下标 0 空着，航班编号直接当下标；累加从 `index = 2` 开始',
                 '经典==静态区间加==问题，同类题：1094 拼车、2381 字母移位 II',
                 '原文为 Python 2 风格（`class Solution(object)`），代码无需改动'],
    ),
)
