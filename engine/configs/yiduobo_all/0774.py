ST = [1, 3, 4, 10]
K = 3
E = 0.1 ** 6


def _t(st, j, mid):
    g = st[j] - st[j - 1]
    if g > mid:
        t = int(g / mid)
        if st[j - 1] + mid * t + E >= st[j]:
            t -= 1
        return t
    return 0


def _fmt(v):
    return f'{v:.6g}' if isinstance(v, float) else str(v)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    st = ST
    lo, hi = st[0], st[-1]
    cv.text((x0 + 18, y0 + 4), '数轴：实心 = 原有加油站，空心 = 为了让间距 ≤ mid 新增的', 24, T['muted'], bold=True)
    left, right = x0 + 60, x1 - 60
    unit = (right - left) / (hi - lo)
    base = y0 + (y1 - y0) * 0.55
    X = lambda v: left + (v - lo) * unit
    line = S.get('_line', 0)
    live = 'mid' in S and 'index' in S and 10 <= line <= 17
    cur = S['index'] if live and line >= 11 else None
    cv.line([(left, base), (right, base)], T['border'], 3)
    for j in range(1, len(st)):
        a, b = X(st[j - 1]), X(st[j])
        isc = cur == j
        if isc:
            cv.rect((a, base - 14, b, base + 14), fill=T['yellow'], r=4, alpha=90)
        cv.text(((a + b) / 2, base - 34), st[j] - st[j - 1], 22, T['yellow'] if isc else T['muted'], anchor='mb', bold=True)
        if live and cur is not None and (j < cur or (j == cur and line >= 15) or (j == cur and line == 17)):
            pass
        if live and cur is not None and (j < cur or (j == cur and line >= 15)):
            t = _t(st, j, S['mid'])
            for i in range(1, t + 1):
                px = X(st[j - 1] + S['mid'] * i)
                if px < b - 3:
                    cv.rect((px - 9, base - 9, px + 9, base + 9), outline=T['green'], width=4, r=9)
    for v in st:
        cv.rect((X(v) - 10, base - 10, X(v) + 10, base + 10), fill=T['blue'], r=10)
        cv.text((X(v), base + 20), v, 22, T['text'], anchor='mt', bold=True)
    if live:
        cv.text((x0 + 18, y1 - 60), f"mid = {_fmt(S['mid'])}：每段间距要 <= mid", 26, T['yellow'], bold=True)


def _top(S):
    line = S.get('_line', 0)
    if 'mid' in S and 10 <= line <= 17:
        return f"试 `mid = {_fmt(S['mid'])}`：插几个站才能让每段 `<= mid`？总数 `cnt = {S.get('cnt', 0)}`，限额 `k = {K}`"
    if 'left' not in S:
        return f'`k` 个新站放哪儿？先==二分最大距离 mid==，再数要几个站'
    return f"答案夹在 `({S['left']:.6f}, {S['right']:.6f}]`，宽度 `{S['right'] - S['left']:.2e}`"


def _gap(S, B, ret):
    g = S.stations[S.index] - S.stations[S.index - 1]
    if g > S.mid:
        return f'间距 `{g}` > `mid = {_fmt(S.mid)}` → 这段==要插站=='
    return f'间距 `{g}` <= `mid = {_fmt(S.mid)}` → 不用插'


def _lt(S, B, ret):
    return (f"`t = int({S.stations[S.index] - S.stations[S.index - 1]} / {_fmt(S.mid)}) = {S.t}`：按每段 mid 切，"
            f"先估计要插 {S.t} 个")


def _fix(S, B, ret):
    lo, hi = S.stations[S.index - 1], S.stations[S.index]
    if lo + S.mid * S.t + E >= hi:
        return f'`{lo} + mid×{S.t} + E >= {hi}`：刚好整除（浮点误差内），==最后一个站会和右端点重合== → 要 `t -= 1`'
    return f'`{lo} + mid×{S.t} + E < {hi}`：切出的 {S.t} 个站都落在段内 → `t` 不变'


CONFIG = dict(
    num=774, title='最小化去加油站的最大距离', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='实数二分 · 判定加几个站',
    tags=['灵神题单·二分算法', 'VIP 题'],
    code='''
class Solution(object):
    def minmaxGasDist(self, stations, k):

        left = 0.0
        right = 10 ** 8
        E = 0.1 ** 6

        while left < right - E:
            mid = (left + right) / 2
            cnt = 0
            for index in range(1, len(stations)):
                if stations[index] - stations[index - 1] > mid:
                    t = int((stations[index] - stations[index - 1]) / mid)
                    if stations[index - 1] + mid * t + E >= stations[index]:
                        t -= 1
                    
                    cnt += t

            if cnt <= k:
                right = mid
            else:
                left = mid
        
        return left
''',
    call=f'Solution().minmaxGasDist({ST}, {K})',
    expect=2.0,
    result_fn=lambda r: round(r, 3),
    views=[
        dict(type='text', fn=_top, size=26, h=100),
        dict(type='custom', draw=_draw, h=330),
    ],
    watch=[('left', 'round(left, 6)', 'green'), ('right', 'round(right, 6)', 'red'), ('mid', 'round(mid, 6)', 'yellow'),
           ('cnt', 'cnt', 'cyan'), ('k', 'k', 'orange')],
    skip=['E = 0.1', 'cnt = 0', 'for index in range'],
    max_steps=48,
    captions={
        'left = 0.0': '`left = 0.0`：最大距离的下界',
        'right = 10': '`right = 10^8`：先给个足够大的上界（实数二分，不能用整数加减 1）',
        'while left < right - E': lambda S, B, r: (f'`right - left` 还 > E = 1e-6，继续二分' if S.left < S.right - E
                                                    else f'`right - left <= 1e-6` → ==精度够了==，停'),
        'mid = (left': '`mid = (left + right) / 2 = {round(mid, 6)}`：==实数二分取中点，不取整==',
        'if stations[index]': _gap,
        't = int': _lt,
        'if stations[index - 1] + mid': _fix,
        't -= 1': '`t = {t}`：少插一个，终点本来就是站',
        'cnt += t': '这段要插 `{t}` 个 → `cnt = {cnt}`',
        'if cnt <= k': lambda S, B, r: (f'`cnt = {S.cnt} <= k = {S.k}`：新站够用 → 答案 ==不超过 mid=='
                                        if S.cnt <= S.k else f'`cnt = {S.cnt} > k = {S.k}`：新站不够 → 答案 ==大于 mid=='),
        'right = mid': '`mid` 够用 → `right = {round(right, 6)}`',
        'left = mid': '`mid` 不够用 → `left = {round(left, 6)}`',
        'return left': '`right - left <= 1e-6`，返回 `left ≈ {round(ret, 6)}`',
    },
    cards=dict(
        after=[dict(heading='视频里快进了什么', lines=[
            '`right` 从 `10^8` 开始，前约 24 次 `mid` 都比最大间距 `6` 大',
            '这时一个站都不用插，`cnt = 0`，`right` 只是不断减半',
            '`mid` 降到 `6` 以下，才出现 ==cnt > k== 让 `left` 往右挪',
            '最后一次迭代的完整过程在动画末尾']),
        ],
        one_liner='k 很大不能逐个放站 → 二分「最大距离」，数需要几个站',
        complexity='时间 `O(n log(U/E))`，空间 `O(1)`',
        problem=['`stations` 是一条直线上已有的加油站位置，要再新增 `k` 个站（位置可以是实数）',
                 '目标：让相邻两站之间的==最大距离==尽量小，返回这个最小值',
                 '本视频：`stations = [1,3,4,10], k = 3` → `2.0`（答案允许误差 1e-6）'],
        quote='新增的加油站越多，最大距离必然就越小，那么在这里就可以二分这个最大距离mid。对于当前的mid，遍历所有初始的加油站位置，计算在相邻加油站之间需要新增多少个加油站才能使得最大距离不超过mid。',
        quote_src='—— yiduobo 题解原文',
        idea=['逐个放站的复杂度与 `k` 挂钩；改成判定「mid 够不够」就和 `k` 无关了',
              '一段长 `g`，要让每段 `<= mid`，需要插 `ceil(g / mid) - 1` 个站',
              '实数二分：`right - left < 1e-6` 就停，不再用严格的大小比较'],
        summary=['时间 `O(n log(U/E))`，空间 `O(1)`',
                 '实数二分的终止条件是精度 `E = 1e-6`，不是 `left + 1 < right`',
                 '`t = int(g / mid)` 在刚好整除时会多算 1 个，所以要 `+ E` 比较后 `t -= 1`',
                 '原文已是 Python 3 可运行（`/` 本来就要浮点除法），没有改动',
                 '返回值是近似值，视频里按 3 位小数校验'],
    ),
)
