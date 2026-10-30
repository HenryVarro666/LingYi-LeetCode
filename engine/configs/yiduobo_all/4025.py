PERIOD, LIGHTS, ARR = 10, [3, 6, 8], [4, 9, 15, 17, 1, 8]


def _idx(S):
    t = S.get('t')
    if t is None or 'ma' not in S:
        return None
    for k, v in enumerate(S['arrivalTime']):
        if v % S['period'] == t:
            return k
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    p = S['period']
    mx = S.get('ma')
    t = S.get('t')
    ans = S.get('res', 0)
    cv.text((x0 + 18, y0 + 4), f'一个周期 period = {p} 秒（绿 = 最长绿灯 ma，红 = 红灯）', 22, T['muted'], bold=True)
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
        cv.text((x1 - 20, y0 + 4), f'res = {ans}', 28, T['green'], anchor='ra', bold=True)


CONFIG = dict(
    num=4025, title='交通灯的最大等待时间', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='贪心 · 全走绿灯最长的灯',
    tags=['脑筋急转弯'],
    code='''
class Solution(object):
    def minPenalty(self, period, lights, arrivalTime):
        
        res = 0
        ma = max(lights)
        for t in arrivalTime:
            t %= period
            if t >= ma:
                res = max(res, period - t)
        
        return res
''',
    call=f'Solution().minPenalty({PERIOD}, {LIGHTS!r}, {ARR!r})',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var='arrivalTime', label='arrivalTime（黄 = 正在处理的车）', h=210, cell=90,
             color=lambda S, i, v: 'yellow' if i == _idx(S) else None),
    ],
    watch=[('period', 'period', 'blue'), ('ma', 'ma', 'green'), ('t', 't', 'yellow'), ('res', 'res', 'orange')],
    captions={
        'res = 0': '`res` 记录最大的等待时间',
        'ma = max': '多辆车可以共用一盏灯 → 全部走绿灯最长的：`ma = max(lights) = {ma}`',
        'for t in arrivalTime': lambda S, B, r: (f'下一辆车：到达 `{S.t}`' if S.get('t') != B.get('t') else '所有车都遍历完了'),
        't %= period': '到达时刻落在周期的第 `{t}` 秒：`t %= {period}`',
        'if t >= ma': lambda S, B, r: (f'`{S.t} >= ma = {S.ma}`：落在红灯里，==要等==' if S.t >= S.ma else f'`{S.t} < ma = {S.ma}`：落在绿灯里，不用等'),
        'res = max': '等待 `{period} − {t}` = {period - t} 秒，`res` 取较大者 → =={res}==',
        'return res': '最大等待时间的最小值 =={ret}==',
    },
    cards=dict(
        one_liner='车可以共用一盏灯，所以全走绿灯最长的那盏',
        complexity='时间 `O(n + m)`，空间 `O(1)`',
        problem=['所有灯同步循环，一个周期 `period` 秒，绿灯 `lights[i]` 秒，其余是红灯',
                 '车到达后取 `r = t % period`：`r < lights[i]` 不用等，否则等 `period - r`',
                 '求所有车等待时间最大值的最小值。示例：`period=10, lights=[3,6,8], arrivalTime=[4,9,15]` → `1`'],
        quote='由于可以让多辆汽车分配到同一个信号灯，那么为了让等待时间最小，就应该让所有汽车都走绿灯时间持续最长的那个信号灯。',
        quote_src='—— yiduobo 题解原文',
        idea=['多辆车可以共用同一盏灯 → 不存在“抢灯”，每辆车独立选最好的',
              '绿灯最长的那盏灯，对每辆车都是最好的选择',
              '遍历到达时间：`r >= ma` 才要等，用 `period - r` 更新 `res`'],
        summary=['时间 `O(n + m)`，空间 `O(1)`',
                 '`lights` 只用来取最大值 `ma`',
                 '易错：先 `t %= period` 再和 `ma` 比较；`r == ma` 也要等（红灯从第 `ma` 秒开始）',
                 '原文 `class Solution(object)` 是 Python 2 风格，但代码无需修改即可在 Python 3 运行',
                 '对比灵神：思路一致，变量名为 `res` / `ma`，灵神用 `ans` / `mx`'],
    ),
)
