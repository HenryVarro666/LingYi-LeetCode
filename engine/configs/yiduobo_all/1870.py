import math

DIST = [1, 3, 2]
HOUR = 2.7
TOP = 10 ** 7


def _x(v, a, b):
    return a + (b - a) * math.log10(max(v, 1)) / 7


def _axis(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    a, b = x0 + 60, x1 - 60
    y = (y0 + y1) / 2 + 10
    cv.text((x0 + 18, y0 + 4), '速度二分区间 [l, r]（对数刻度 1 ~ 10^7）', 22, T['muted'], bold=True)
    cv.line([(a, y), (b, y)], T['border'], 3)
    for e in range(8):
        X = _x(10 ** e, a, b)
        cv.line([(X, y - 8), (X, y + 8)], T['dim'], 2)
        cv.text((X, y + 14), '1' if e == 0 else f'10^{e}', 18, T['dim'], anchor='mt', mono=True)
    if 'r' not in S:
        return
    l, r = S['l'], S['r']
    xl, xr = _x(l, a, b), _x(r, a, b)
    cv.rect((xl - 3, y - 16, max(xr, xl + 6) + 3, y + 4), fill=T['green'], alpha=120, r=4)
    cv.tri_down(xl, y - 20, 10, T['blue'])
    sl, sr = f'l={l}', f'r={r}'
    cl = min(max(xl, x0 + 12 + 6 * len(sl)), x1 - 12 - 6 * len(sl))
    cr = min(max(xr, x0 + 12 + 6 * len(sr)), x1 - 12 - 6 * len(sr))
    cv.text((cl, y - 58), sl, 20, T['blue'], anchor='mb', bold=True)
    cv.tri_down(xr, y - 20, 10, T['pink'])
    cv.text((cr, y - 34), sr, 20, T['pink'], anchor='mb', bold=True)
    if 'mid' in S and l <= S['mid'] <= r and S['_line'] not in (9, 23):
        xm = _x(S['mid'], a, b)
        cv.tri_up(xm, y + 40, 10, T['yellow'])
        sm = f"mid={S['mid']}"
        cm = min(max(xm, x0 + 12 + 6 * len(sm)), x1 - 12 - 6 * len(sm))
        cv.text((cm, y + 54), sm, 20, T['yellow'], anchor='mt', bold=True)


def _times(S):
    if 'mid' not in S or S['_line'] not in (17, 18):
        return []
    m = S['mid']
    return [str(d // m + (1 if d % m else 0)) for d in DIST[:-1]] + [f'{DIST[-1]}/{m}']


def _top(S):
    if 'r' not in S:
        return '速度越快到得越早 → ==二分答案==，下界 1，上界 `10^7`'
    if 'mid' in S and S['_line'] in (17, 18):
        ok = S['cnt'] <= HOUR
        return f"速度 `{S['mid']}`：总耗时 `{S['cnt']:.4g}` {'≤' if ok else '>'} `hour = {HOUR}` → {'==可以放慢==' if ok else '==必须提速=='}"
    if S['l'] < S['r']:
        return f"答案在 `[{S['l']}, {S['r']}]` 里，还剩 `{S['r'] - S['l'] + 1}` 个候选"
    return f"`l == r = {S['l']}`：最小时速"


def _if(S, B, ret):
    if S.cnt <= S.hour:
        return f'耗时 `{S.cnt:.4g} ≤ {S.hour}`：速度 {S.mid} 来得及，==可能可以放慢== → `r = mid`'
    return f'耗时 `{S.cnt:.4g} > {S.hour}`：速度 {S.mid} 迟到，==必须提速== → `l = mid + 1`'


def _each(S, B, ret):
    m = S.mid
    ts = [d // m + (1 if d % m else 0) for d in S.dist[:-1]]
    return f'前 n−1 站向上取整：`{" + ".join(map(str, ts))}`；最后一站 `{S.dist[-1]}/{m}` 不取整 → `cnt = {S.cnt:.4g}`'


CONFIG = dict(
    num=1870, title='准时到达的列车最小时速', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分答案 · 上界 10^7',
    tags=['灵神核心路线', '灵神题单·二分算法', '难度分 1676'],
    code='''
class Solution(object):
    def minSpeedOnTime(self, dist, hour):

        if len(dist) - 1 >= hour:
            return -1

        l = 1
        r = 10 ** 7
        while l < r:
            mid = (l + r) >> 1
            cnt = 0.0
            for d in dist[:-1]:
                cnt += d // mid
                if d % mid != 0:
                    cnt += 1

            cnt += float(dist[-1]) / mid
            if cnt <= hour:
                r = mid
            else:
                l = mid + 1
        
        return l
''',
    call=f'Solution().minSpeedOnTime({DIST}, {HOUR})',
    expect=3,
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='custom', draw=_axis, h=230),
        dict(type='array', var='dist', label='dist：每站距离', cell=110, h=170),
        dict(type='array', var=_times, label='速度 mid 下每站耗时（前 n−1 站向上取整，最后一站不取整）', cell=110,
             index=False, h=170, color=lambda S, i, v: 'cyan'),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow'), ('cnt', 'cnt', 'green'), 'hour'],
    skip=['cnt = 0.0', 'for d in', 'cnt += d // mid', 'if d % mid', 'cnt += 1'],
    max_steps=40,
    captions={
        'if len(dist) - 1 >= hour': lambda S, B, r: (f'`n − 1 = {len(S.dist) - 1} < hour = {S.hour}`：前 n−1 站至少各 1 小时，还有余量'
                                                      if len(S.dist) - 1 < S.hour else '前 n−1 站至少要 n−1 小时 → 不可能准时'),
        'l = 1': '下界 `l = 1`',
        'r = 10 ** 7': '上界 `r = 10^7`：题目保证答案不超过它',
        'while l < r': lambda S, B, r: (f'`[{S.l}, {S.r}]` 不为空，继续二分' if S.l < S.r else f'`l == r = {S.l}`，结束'),
        'mid = (l + r)': '试速度 `mid = ({l} + {r}) >> 1 = {mid}`',
        'cnt += float': _each,
        'if cnt <= hour': _if,
        'r = mid': '`r = {r}`',
        'l = mid + 1': '`l = {l}`',
        'return l': '最小时速 =={ret}==',
    },
    cards=dict(
        one_liner='速度越快到得越早：在 [1, 10^7] 上二分速度',
        complexity='时间 `O(n log 10^7)`，空间 `O(1)`',
        problem=['按顺序坐 `n` 趟列车，第 i 趟距离 `dist[i]`，列车==只在整点发车==',
                 '求 `hour` 小时内到达的==最小正整数时速==，做不到返回 `-1`',
                 '示例：`[1,3,2], hour = 2.7` → `3`；`hour = 1.9` → `-1`'],
        quote='需要注意的是，在这里==前n - 1站的时间需要向上取整，但最后一站的时间不需要==。计算出总耗时后，若耗时小于等于hour，那么说明当前速度可能可以适当放慢。',
        quote_src='—— yiduobo 题解原文',
        idea=['上下界直接取 `[1, 10^7]`（题目保证答案不超过 10^7）',
              '前 n−1 站：`d // mid`，有余数再 `+1`，就是向上取整（等整点）',
              '最后一站到了就算，直接 `dist[-1] / mid`，再和 `hour` 比'],
        summary=['时间 `O(n log 10^7)`，空间 `O(1)`',
                 '先判 `n − 1 >= hour`：前 n−1 站至少各 1 小时，不可能准时',
                 '易错：最后一站不要向上取整',
                 '原文为 Python 2 写法，`d / mid` 已改为 `d // mid`（整数除法）',
                 '灵神把 hour×100 化成整数比较，避开浮点；这里直接用浮点 `cnt <= hour`'],
    ),
)
