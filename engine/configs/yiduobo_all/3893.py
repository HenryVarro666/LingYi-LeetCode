def _ph(S):
    """1 = 第一遍(统计左侧不相交)  2 = 第二遍(右侧)  3 = 汇总"""
    L = S.get('_line', 0)
    if L >= 26:
        return 3
    if L >= 18:
        return 2
    return 1


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    L = S.get('_line', 0)
    n = S['n'] if 'n' in S else 0
    info = S.get('info')
    if not info:
        return
    orig = {i: (a, b) for i, a, b in info}
    tmax = max(b for a, b in orig.values())
    ph = _ph(S)
    cur = S.get('index') if 'index' in S else None
    # 参考线：phase1 用起点 s，phase2 用终点 e
    ref = None
    if ph == 1 and L >= 13 and 's' in S:
        ref = S['s']
    elif ph == 2 and L >= 21 and 'e' in S:
        ref = S['e']
    cv.text((x0 + 18, y0 + 4), '员工的工作区间（横轴 = 时间）', 22, T['muted'], bold=True)
    lx0, lx1 = x0 + 70, x1 - 270
    sc = (lx1 - lx0) / (tmax + 1)
    top = y0 + 44
    rh = 44
    for t in range(tmax + 1):
        X = lx0 + (t + 0.5) * sc
        cv.line([(X, top - 4), (X, top + n * rh)], (40, 46, 56), 1)
        cv.text((X, top + n * rh + 4), t, 16, T['dim'], anchor='mt', mono=True)
    lm, rm = S.get('left_miss'), S.get('right_miss')
    cv.text((lx1 + 30, top - 22), 'left', 18, T['cyan'], anchor='mm', bold=True)
    cv.text((lx1 + 100, top - 22), 'right', 18, T['orange'], anchor='mm', bold=True)
    cv.text((lx1 + 180, top - 22), '团队', 18, T['green'], anchor='mm', bold=True)
    for i in range(n):
        a, b = orig[i]
        Y = top + i * rh
        miss = False
        if ref is not None and i != cur:
            miss = (ph == 1 and b < ref) or (ph == 2 and a > ref)
        fill = T['blue'] if i == cur and ph < 3 else (T['yellow'] if (ph == 3 and i == cur) else (T['red'] if miss else (120, 128, 140)))
        cv.text((lx0 - 14, Y + rh / 2), f'员工{i}', 18, T['text'] if i == cur else T['muted'], anchor='rm', bold=(i == cur))
        cv.rect((lx0 + a * sc + sc / 2, Y + 8, lx0 + b * sc + sc / 2, Y + rh - 8), fill=fill, r=6, alpha=230 if (miss or i == cur) else 160)
        cv.text(((lx0 + a * sc + lx0 + b * sc + sc) / 2, Y + rh / 2), f'[{a},{b}]', 18, T['bg'], anchor='mm', bold=True)
        if lm is not None and (ph >= 2 or (ph == 1 and L >= 16 and cur is not None and i <= cur) or ph == 3 or True):
            pass
        def _done(arr, k):
            return arr is not None and k < len(arr)
        lv = lm[i] if lm is not None and _left_done(S, i) else None
        rv = rm[i] if rm is not None and _right_done(S, i) else None
        if lv is not None:
            cv.text((lx1 + 30, Y + rh / 2), lv, 24, T['cyan'], anchor='mm', bold=True, mono=True)
        if rv is not None:
            cv.text((lx1 + 100, Y + rh / 2), rv, 24, T['orange'], anchor='mm', bold=True, mono=True)
        if lv is not None and rv is not None and ph == 3:
            cv.text((lx1 + 180, Y + rh / 2), n - lv - rv, 26, T['green'], anchor='mm', bold=True, mono=True)
    if ref is not None:
        X = lx0 + ref * sc + sc / 2
        cv.dashed((X, top - 6), (X, top + n * rh), T['yellow'], 3)
        cv.text((X, top - 8), ('s=' if ph == 1 else 'e=') + str(ref), 18, T['yellow'], anchor='mb', bold=True)
    # 两个排好序的数组
    ay = top + n * rh + 50
    cell = 64
    for r, (nm, color, ptr) in enumerate((('endTime', 'cyan', S.get('p') if ph == 1 and L >= 12 else None),
                                          ('startTime', 'orange', S.get('p') if ph == 2 else None))):
        arr = S.get(nm)
        Y = ay + r * 96
        cv.text((x0 + 18, Y + 24), f'{nm}（排序后）', 20, T[color], anchor='lm', bold=True)
        sx = x0 + 230
        for k, v in enumerate(arr):
            X = sx + k * (cell + 6)
            hit = ptr is not None and k == ptr
            counted = ptr is not None and ((ph == 1 and k < ptr) or (ph == 2 and k > ptr))
            cv.rect((X, Y, X + cell, Y + 48), fill=(70, 78, 90) if counted else (36, 42, 52), outline=T['blue'] if hit else None, width=3, r=6)
            cv.text((X + cell / 2, Y + 24), v, 24, T['red'] if counted else T['text'], anchor='mm', bold=True)
        if ptr is not None and 0 <= ptr < len(arr):
            X = sx + ptr * (cell + 6) + cell / 2
            cv.tri_up(X, Y + 54, 9, T['blue'])
            cv.text((X, Y + 66), 'p', 20, T['blue'], anchor='mt', bold=True)
    if ph == 1 and L >= 12:
        cv.text((x0 + 18, ay + 190), '红色 = 已确认与当前员工不相交（p 之前的 endTime）', 18, T['red'])
    elif ph == 2:
        cv.text((x0 + 18, ay + 190), '红色 = 已确认与当前员工不相交（p 之后的 startTime）', 18, T['red'])


def _left_done(S, i):
    """left_miss[i] 已经被写入"""
    L = S.get('_line', 0)
    if L >= 18:
        return True
    if L < 13 or 'index' not in S:
        return False
    order = [t[0] for t in S['info']]
    return order.index(i) < order.index(S['index']) or (order.index(i) == order.index(S['index']) and L == 16)


def _right_done(S, i):
    L = S.get('_line', 0)
    if L >= 25:
        return True
    if L < 21 or 'index' not in S:
        return False
    order = [t[0] for t in S['info']][::-1]
    return order.index(i) < order.index(S['index']) or (order.index(i) == order.index(S['index']) and L == 24)


def _txt(S):
    ph = _ph(S)
    if 'left_miss' not in S:
        return '员工 i 能互动的人数 = n − 它左边不相交的 − 它右边不相交的'
    if ph == 1:
        return '`left_miss[i]` = 终止时间 < 我的起点 的区间数 = 排序后的 endTime 里 `p` 之前的个数'
    if ph == 2:
        return '`right_miss[i]` = 起始时间 > 我的终点 的区间数 = `n − 1 − p`'
    if 'index' in S:
        i = S['index']
        return f'员工 {i}：`n − left_miss − right_miss = {S["n"]} − {S["left_miss"][i]} − {S["right_miss"][i]}`'
    return ''


CONFIG = dict(
    num=3893, title='最大重叠区间团队规模', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='反向计数 · 排序后单调指针',
    tags=['题单·二分算法'],
    code='''
class Solution(object):
    def maximumTeamSize(self, startTime, endTime):
        
        n = len(startTime)

        info = [(index, startTime[index], endTime[index]) for index in range(n)]
        startTime.sort()
        endTime.sort()
        
        info.sort(key=lambda d:d[1])
        left_miss = [0] * n
        p = 0
        for index, s, _ in info:
            while p < n and endTime[p] < s:
                p += 1
            left_miss[index] = p
        
        info.sort(key=lambda d:d[2])
        right_miss = [0] * n
        p = n - 1
        for index, _, e in info[::-1]:
            while p >= 0 and startTime[p] > e:
                p -= 1
            right_miss[index] = n - 1 - p
        
        res = 0
        for index in range(n):
            res = max(res, n - left_miss[index] - right_miss[index])
        return res
''',
    call='Solution().maximumTeamSize([1,2,6,3,8], [4,6,7,5,10])',
    expect=4,
    views=[
        dict(type='custom', draw=_draw, h=700),
        dict(type='text', h=70, size=26, fn=_txt),
    ],
    watch=[('n', 'n'), ('index', 'index', 'pink'), ('p', 'p', 'blue'), ('res', 'res', 'green')],
    skip=['left_miss = [0]', 'right_miss = [0]', 'res = 0', 'endTime.sort()'],
    captions={
        'n = len': '`n = {n}` 个员工',
        'info = [': '`info` 把编号、起点、终点绑在一起：排序之后还能知道是谁',
        'startTime.sort()': '`startTime` 和 `endTime` ==各自独立排序==：只用来数个数，不管是谁的区间',
        'info.sort(key=lambda d:d[1])': '`info` 按起点排序：起点递增时，“终止时间 < 起点”的个数只增不减',
        'p = 0': '`p` 指向 endTime：它之前的都比当前起点早结束',
        'for index, s, _ in info': lambda S, B, r: (f'员工 `{S.index}`：起点 `s = {S.s}`' if 'index' not in B or S.index != B.index or S.s != B.s
                                                    else '左侧统计完毕'),
        'while p < n and endTime[p] < s': lambda S, B, r: (
            f'`endTime[{S.p}] = {S.endTime[S.p]} < {S.s}`：这个区间在 s 之前就结束了，不相交 → `p` 右移' if S.p < S.n and S.endTime[S.p] < S.s
            else (f'`p = {S.p}` 到头了，所有终止时间都 < {S.s}' if S.p >= S.n
                  else f'`endTime[{S.p}] = {S.endTime[S.p]} ≥ {S.s}`：从这里起都和 s 有交集 → 停')),
        'p += 1': '`p = {p}`：已有 {p} 个区间在 {s} 之前结束',
        'left_miss[index] = p': '员工 `{index}`：左边不相交的区间共 `p = {p}` 个 → `left_miss[{index}] = {p}`',
        'info.sort(key=lambda d:d[2])': '换成按终点排序，倒着遍历：终点递减时，“起点 > 终点”的个数只增不减',
        'p = n - 1': '`p` 从 startTime 末尾开始：它之后的起点都比当前终点晚',
        'for index, _, e in info[::-1]': lambda S, B, r: (f'员工 `{S.index}`（倒序）：终点 `e = {S.e}`' if 'e' not in B or 'index' not in B or S.e != B.e or S.index != B.index
                                                         else '右侧统计完毕'),
        'while p >= 0 and startTime[p] > e': lambda S, B, r: (
            f'`startTime[{S.p}] = {S.startTime[S.p]} > {S.e}`：这个区间在 e 之后才开始，不相交 → `p` 左移' if S.p >= 0 and S.startTime[S.p] > S.e
            else (f'`p = -1`：所有起点都 > {S.e}' if S.p < 0
                  else f'`startTime[{S.p}] = {S.startTime[S.p]} ≤ {S.e}`：这些都和 e 有交集 → 停')),
        'p -= 1': '`p = {p}`',
        'right_miss[index] = n - 1 - p': '员工 `{index}`：`p` 之后共 `n − 1 − p = {n - 1 - p}` 个起点晚于 {e} → `right_miss[{index}] = {n - 1 - p}`',
        'for index in range(n)': lambda S, B, r: ('汇总：每个员工能带多大的团队' if 'res' not in B or S.index != B.index else '全部算完'),
        'res = max': lambda S, B, r: (f'员工 `{S.index}`：`{S.n} − {S.left_miss[S.index]} − {S.right_miss[S.index]} = '
                                      f'{S.n - S.left_miss[S.index] - S.right_miss[S.index]}`，`res` = =={S.res}=='),
        'return res': '最大团队规模 `{res}`',
    },
    max_steps=80,
    cards=dict(
        one_liner='直接数相交很麻烦，反过来数不相交的',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每个员工有工作区间 `[start, end]`，有公共时间点就能互动',
                 '团队有效：至少有一人能和队里所有人互动。求有效团队最大规模',
                 '本视频：`start=[1,2,6,3,8]`，`end=[4,6,7,5,10]` → `4`'],
        quote='直接判断区间是否相交其实是相对麻烦的，不妨反过来计算，判断对于每个员工，有多少其他员工的时间区间与该员工的时间区间不重叠。',
        quote_src='—— yiduobo 题解原文',
        idea=['对 `[s, e]`：终止时间 `< s` 的区间在左边不相交，起始时间 `> e` 的区间在右边不相交',
              '把 `startTime`、`endTime` 各自排序，用单调指针 `p` 数出这两类区间的个数',
              '以某人为中心，团队规模 = `n − left_miss − right_miss`，取最大'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：左边用 `endTime[p] < s`，右边用 `startTime[p] > e`，端点相等算相交',
                 '左右两类不相交的区间不会重复：一个区间不可能同时在左边和右边',
                 '`startTime/endTime` 排序后与 `info` 里的原值分开存放，`info` 保留员工编号',
                 '原文为 Python 2 风格，本题代码无需改动，直接可运行'],
    ),
)
