TRIPS, CAP = [[2, 1, 5], [1, 2, 4], [3, 5, 7], [2, 6, 8]], 4
LO, HI = 0, 9


def _phase(S):
    ln = S.get('_line')
    return 1 if ln in (3, 4, 5, 6) else 2 if ln in (9, 10, 11, 12) else 3 if ln == 13 else 0


def _cur_trip(S):
    if _phase(S) != 1 or 'num' not in S:
        return None
    t = [S['num'], S['from_'], S['to']]
    return TRIPS.index(t) if t in TRIPS else None


def _prefix(d):
    out, run = [], 0
    for k in sorted(d):
        run += d[k]
        out.append((k, run))
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    L, R = x0 + 70, x1 - 40

    def X(v):
        return L + (v - LO) / (HI - LO) * (R - L)

    ph = _phase(S)
    cur = _cur_trip(S)
    cv.text((x0 + 18, y0 + 4), 'trips：num 人从 from 坐到 to（to 处下车；黄 = 正在处理）', 24, T['muted'], bold=True)
    for i, (n, a, b) in enumerate(TRIPS):
        Y = y0 + 44 + i * 42
        done = ph >= 2 or (cur is not None and i < cur) or (i == cur and S.get('_line') == 6)
        fill = T['yellow'] if i == cur else (T['blue'] if done else (60, 66, 76))
        cv.rect((X(a), Y, X(b), Y + 32), fill=fill, r=9)
        cv.text(((X(a) + X(b)) / 2, Y + 16), f'{n} 人 [{a}, {b})', 20, T['bg'] if (done or i == cur) else T['text'],
                anchor='mm', bold=True)
    ay = y0 + 44 + len(TRIPS) * 42 + 10
    cv.line([(L, ay), (R, ay)], T['border'], 2)
    for v in range(LO, HI + 1):
        cv.line([(X(v), ay), (X(v), ay + 6)], T['border'], 2)
        cv.text((X(v), ay + 8), v, 18, T['dim'], anchor='mt')
    # 差分 d：只在 from / to 这些位置上有值
    d = S.get('d')
    bd = B.get('d') or {}
    dy = ay + 44
    cv.text((x0 + 18, dy + 18), 'd', 24, T['purple'], anchor='lm', bold=True, mono=True)
    k_now = S.get('k') if ph >= 2 else None
    if d:
        for key, v in d.items():
            ch = bd.get(key) != v
            c = T['green'] if v > 0 else (T['pink'] if v < 0 else T['dim'])
            w = 54
            hl = key == k_now
            cv.rect((X(key) - w / 2, dy, X(key) + w / 2, dy + 36), fill=T['yellow'] if hl else T['panel2'], r=8,
                    outline=T['yellow'] if ch else T['border'], width=3 if ch else 1)
            cv.text((X(key), dy + 18), f'{v:+d}' if v else '0', 22, T['bg'] if hl else c, anchor='mm', bold=True)
    # 车上人数（差分的前缀和），只画已经扫过的位置
    gt, gb = dy + 60, y1 - 30
    vmax = max(CAP + 2, 6)

    def Y(v):
        return gb - v / vmax * (gb - gt)

    cv.text((x0 + 18, gt + 2), '车上人数 s', 22, T['muted'], bold=True)
    cv.line([(L, gb), (R, gb)], T['border'], 2)
    cv.dashed((L, Y(CAP)), (R, Y(CAP)), T['red'], 3)
    cv.text((R, Y(CAP) - 6), f'capacity = {CAP}', 20, T['red'], anchor='rb', bold=True)
    if ph >= 2 and d:
        pts = _prefix(d)
        line = S.get('_line')
        upto = k_now if line in (10, 11, 12) else (k_now - 0.5 if k_now is not None else None)
        if ph == 3:
            upto = HI
        shown = [(k, s) for k, s in pts if upto is not None and k <= upto]
        for j, (k, s) in enumerate(shown):
            nk = pts[j + 1][0] if j + 1 < len(pts) else HI
            if j + 1 < len(shown) or ph == 3:
                end = nk
            else:
                end = k + 0.6
            over = s > CAP
            c = T['red'] if over else T['cyan']
            cv.rect((X(k), Y(s), X(end), gb), fill=c, alpha=70)
            cv.line([(X(k), Y(s)), (X(end), Y(s))], c, 4)
            cv.text((X(k) + 6, Y(s) - 4), s, 20, c, anchor='lb', bold=True)
        if k_now is not None and ph == 2:
            cv.dashed((X(k_now), dy + 40), (X(k_now), gb), T['yellow'], 2)


CONFIG = dict(
    num=1094, title='拼车', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='差分（哈希表 + 排序）',
    tags=['labuladong', '灵神题单·常用数据结构', '难度分 1441'],
    code='''
class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        d = defaultdict(int)
        for num, from_, to in trips:
            d[from_] += num
            d[to] -= num

        s = 0
        for k in sorted(d):
            s += d[k]
            if s > capacity:
                return False
        return True
''',
    call=f'Solution().carPooling({TRIPS}, {CAP})',
    expect=False,
    views=[
        dict(type='custom', draw=_draw, h=620),
    ],
    watch=[('num', 'num'), ('from_', 'from_'), ('to', 'to'), ('k', 'k', 'yellow'), ('s', 's', 'cyan'),
           ('capacity', 'capacity', 'red')],
    captions={
        'd = defaultdict': '`d`：差分数组。只有 `from` 和 `to` 这些位置会变，用==哈希表==代替长为 1001 的数组',
        'for num, from_, to in trips': lambda S, B, r: (
            '所有行程都处理完：每个行程只改了 d 的两个位置' if 'num' in B and (B.num, B.from_, B.to) == (S.num, S.from_, S.to)
            else f'行程：`{S.num}` 人在 `{S.from_}` 上车、`{S.to}` 下车 → 把 `a[{S.from_}..{S.to - 1}]` 都加 {S.num}'),
        'd[from_] += num': lambda S, B, r: (
            f'区间加的左端：`d[{S.from_}] += {S.num}` → `{S.d[S.from_]}`' +
            (f'（位置 {S.from_} 有 {-B.d[S.from_]} 人下、{S.num} 人上，==差分自动合并==）' if B.d.get(S.from_, 0) < 0 else '')),
        'd[to] -= num': '右端的下一个位置：`d[{to}] -= {num}` → `{d[to]}`（乘客在 {to} ==已下车==，不占座）',
        's = 0': '`s`：从左到右累加差分，就是车开到每个位置时==车上的人数==',
        'for k in sorted(d)': lambda S, B, r: (
            f'按位置从小到大：`k = {S.k}`' if 'k' not in B or B.k != S.k else '所有位置扫完'),
        's += d[k]': lambda S, B, r: (f'`s = {B.s} + {S.d[S.k] if S.d[S.k] >= 0 else f"({S.d[S.k]})"}` = =={S.s}==：'
                                      f'位置 {S.k} 之后车上有 {S.s} 人'),
        'if s > capacity': lambda S, B, r: (f'`{S.s} > {S.capacity}`：==超载==！' if S.s > S.capacity
                                            else f'`{S.s} ≤ {S.capacity}`，没超载，继续'),
        'return False': '有位置超载 → 返回 `False`',
        'return True': '全程没有超载 → 返回 `True`',
    },
    cards=dict(
        one_liner='每个行程 = 区间加 num：差分只改两个点，再按位置累加看是否超载',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`trips[i] = [num, from, to]`：num 名乘客在 from 上车、to 下车（只往东开）',
                 '车有 `capacity` 个座位，==先下后上==；能接送所有乘客返回 `true`',
                 '示例：`[[2,1,5],[3,3,7]], capacity = 4` → `false`',
                 f'本视频：`{TRIPS}`，`capacity = {CAP}` → `false`'],
        before=[dict(heading='差分数组（灵神的例子）', lines=[
            '`a = [1,3,3,5,8]` 两两作差、开头补 `a[0]`：`d = [1,2,0,2,3]`',
            '性质 1：从左到右累加 `d`，就还原出 `a`（类似==求导与积分==）',
            '性质 2：`a[i..j]` 都加 `x` ⇔ `d[i] += x`，`d[j+1] −= x`'])],
        quote='只需要考虑在 from_i 和 to_i 这些位置上的乘客数，==其余位置的乘客是保持不变的==，无需考虑。',
        quote_src='—— 灵茶山艾府题解（第二种写法）',
        idea=['设 `a[i]` = 车开到位置 i 时的人数；行程把 `a[from..to−1]` 都加 num',
              '差分：`d[from] += num`，`d[to] −= num`；用哈希表只存这些位置',
              '`sorted(d)` 从小到大累加得 `s`，一旦 `s > capacity` 就返回 `False`'],
        result='位置 6 处车上有 5 人 > 4，返回 `False`',
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '第一种写法：开长 1001 的数组，`all(s <= capacity for s in accumulate(d))`，`O(n + U)`',
                 '`to` 处是==减==：乘客在 to 下车，`a[to]` 不含他们，自然先下后上',
                 '无需建出 `a`：边累加边判断即可'],
    ),
)
