PERIOD, LIGHTS, ARR = 10, [3, 6, 8], [4, 9, 15, 17, 1, 8]


def _idx(S):
    t = S.get('t')
    if t is None or 'mx' not in S:
        return None
    for k, v in enumerate(S['arrivalTime']):
        if v % S['period'] == t:
            return k
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    p = S['period']
    mx = S.get('mx')
    t = S.get('t')
    ans = S.get('ans', 0)
    cv.text((x0 + 18, y0 + 4), f'一个周期 period = {p} 秒（绿 = 最长绿灯 mx，红 = 红灯）', 22, T['muted'], bold=True)
    sx, W = x0 + 40, x1 - x0 - 80
    cell = W / p
    ys, ch = y0 + 90, 70
    for k in range(p):
        green = mx is not None and k < mx
        c = T['green'] if green else (T['red'] if mx is not None else T['panel2'])
        cv.rect((sx + k * cell + 2, ys, sx + (k + 1) * cell - 2, ys + ch), fill=c, alpha=170, r=6)
        cv.text((sx + k * cell + cell / 2, ys + ch + 8), k, 20, T['dim'], anchor='mt', mono=True)
    if mx is not None:
        cv.text((sx + mx * cell / 2, ys + ch + 50), f'绿灯 0..{mx - 1}', 22, T['green'], anchor='mm', bold=True)
        if mx < p:
            cv.text((sx + (mx + p) * cell / 2, ys + ch + 50), f'红灯 {mx}..{p - 1}', 22, T['red'], anchor='mm', bold=True)
    if t is not None and mx is not None and 0 <= t < p:
        X = sx + t * cell + cell / 2
        cv.tri_down(X, ys - 4, 12, T['yellow'])
        cv.text((X, ys - 22), f't = {t}', 24, T['yellow'], anchor='mb', bold=True)
        if t >= mx:
            cv.arrow((X, ys + ch + 92), (sx + p * cell, ys + ch + 92), T['orange'], 4)
            cv.text(((X + sx + p * cell) / 2, ys + ch + 100), f'等 {p - t} 秒', 24, T['orange'], anchor='mt', bold=True)
        else:
            cv.text((X, ys + ch + 92), '绿灯，直接过', 22, T['green'], anchor='mt', bold=True)
    if mx is not None:
        cv.text((x1 - 20, y0 + 4), f'ans = {ans}', 28, T['green'], anchor='ra', bold=True)


CONFIG = dict(
    num=4025, title='交通灯的最大等待时间', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='脑筋急转弯 · 全选最长绿灯',
    tags=['脑筋急转弯'],
    code='''
class Solution:
    def minPenalty(self, period: int, lights: list[int], arrivalTime: list[int]) -> int:
        mx = max(lights)
        ans = 0
        for t in arrivalTime:
            t %= period
            if t >= mx:
                ans = max(ans, period - t)
        return ans
''',
    call=f'Solution().minPenalty({PERIOD}, {LIGHTS!r}, {ARR!r})',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var='arrivalTime', label='arrivalTime（黄 = 正在处理的车）', h=210, cell=90,
             color=lambda S, i, v: 'yellow' if i == _idx(S) else None),
    ],
    watch=[('period', 'period', 'blue'), ('mx', 'mx', 'green'), ('t', 't', 'yellow'), ('ans', 'ans', 'orange')],
    captions={
        'mx = max': '所有车都走绿灯最长的那盏：`mx = max(lights) = {mx}`，==红灯最短==',
        'ans = 0': '`ans` 记录最大等待时间',
        'for t in arrivalTime': lambda S, B, r: (f'下一辆车，到达时间 `{S.t}`' if S.get('t') != B.get('t') else '所有车都看完了'),
        't %= period': '`t` 在周期里的位置：`t %= {period}` → =={t}==',
        'if t >= mx': lambda S, B, r: (f'`t = {S.t} >= mx = {S.mx}`：==红灯==，要等' if S.t >= S.mx else f'`t = {S.t} < mx = {S.mx}`：正好绿灯，等待 0'),
        'ans = max': '要等 `{period} − {t}` = {period - t} 秒；`ans = max({B.ans}, {period - t})` = =={ans}==',
        'return ans': '最小的最大等待 =={ret}==',
    },
    cards=dict(
        one_liner='所有车都去绿灯最长的那盏灯，红灯最短',
        complexity='时间 `O(n + m)`，空间 `O(1)`',
        problem=['所有灯同步，周期 `period` 秒，第 `i` 盏灯前 `lights[i]` 秒绿、其余红',
                 '车在 `t` 到达，`r = t % period`；`r < lights[i]` 不用等，否则等 `period - r`',
                 '给每辆车分配一盏灯，使最长等待最小。示例：`period=10, lights=[3,6,8], arrivalTime=[4,9,15]` → `1`'],
        quote='把所有汽车分配到持续时间为 m = max(lights) 的信号灯是最优的，红灯最短。',
        quote_src='—— 灵茶山艾府题解',
        idea=['同一盏灯可以放任意多辆车，所以==每辆车都可以选绿灯最长的灯==',
              '绿灯最长 → 红灯 `[mx, period)` 最短，任何一辆车等的时间都不会更长',
              '只需遍历车：`r >= mx` 才要等，取 `period - r` 的最大值'],
        summary=['时间 `O(n + m)`，空间 `O(1)`',
                 '易错：先对 `period` 取模再和 `mx` 比；等待时间是 `period - r`，不是 `mx - r`',
                 '`lights` 只用到最大值，其他灯没用',
                 '同类：脑筋急转弯——先证明选哪个最优，再模拟'],
    ),
)
