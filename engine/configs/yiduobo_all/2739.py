M0, A0 = 26, 10


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '两个油箱（每格 = 1 升）；已行驶距离 res 在下面', 24, T['muted'], bold=True)
    main, add = S.get('mainTank'), S.get('additionalTank')
    if main is None:
        return
    for row, (name, v, v0, c) in enumerate((('mainTank 主油箱', main, M0 + 5, 'blue'), ('additionalTank 副油箱', add, A0, 'orange'))):
        yy = y0 + 70 + row * 150
        cv.text((x0 + 30, yy), f'{name} = {v}', 28, T[c], bold=True)
        W = x1 - x0 - 60
        cell = min(30, W / v0)
        for k in range(v0):
            X = x0 + 30 + k * cell
            cv.rect((X + 1, yy + 44, X + cell - 1, yy + 84), fill=T[c] if k < v else T['panel2'], outline=T['border'], r=3)
    r, t = S.get('r'), S.get('t')
    if r is not None and t is not None:
        cv.text((x0 + 30, y0 + 340), f'余 r = {r} 升，可转油次数 t = {t}', 28, T['cyan'], bold=True)
    cv.text((x0 + 30, y0 + 410), f"已行驶 res = {S.get('res', 0)} km", 34, T['green'], bold=True)


CONFIG = dict(
    num=2739, title='总行驶距离', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='反复除 5 · 求补给量 t',
    code='''
class Solution(object):
    def distanceTraveled(self, mainTank, additionalTank):

        res = 0
        while mainTank:
            r = mainTank % 5
            t = mainTank // 5
            if t > 0:
                res += t * 50
                t = min(t, additionalTank)
                additionalTank -= t
                mainTank = r + t
            else:
                res += r * 10
                break

        return res
''',
    call=f'Solution().distanceTraveled({M0}, {A0})',
    expect=320,
    views=[dict(type='custom', draw=_draw, h=520)],
    watch=[('mainTank', 'mainTank', 'blue'), ('additionalTank', 'additionalTank', 'orange'), 'r', 't', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计行驶距离',
        'while mainTank': '`mainTank = {mainTank}`，主油箱还有油，继续',
        'r = mainTank % 5': '先分出零头：`r = {mainTank} % 5 = {r}`（不足 5 升的部分）',
        't = mainTank // 5': '`t = {mainTank} // 5 = {t}`：主油箱能触发的补给次数',
        'if t > 0': lambda S, B, r: (f'`t = {S.t} > 0`：能触发补给，先把这些油烧掉再转油' if S.t > 0
                                      else '`t = 0`：再也不会补给，只剩零头'),
        'res += t * 50': '烧掉 `{t} * 5` 升，行驶 `{t} * 50` → `res = {res}`',
        't = min(t, additionalTank)': '想转 `t` 升，但副油箱只有 `{additionalTank}` 升 → `t = {t}`',
        'additionalTank -= t': '副油箱转出 `{t}` 升 → `{additionalTank}`',
        'mainTank = r + t': '主油箱 = 零头 `{r}` + 转来 `{t}` = `{mainTank}`，下一轮继续',
        'res += r * 10': '`t = 0`：剩下 `{r}` 升直接跑完，`res += {r} * 10` → `{res}`',
        'break': '油烧完了，退出循环',
        'return res': '总行驶距离 `{res}` km',
    },
    cards=dict(
        one_liner='反复算补给量 t：烧掉整 5 升，转进 t 升，直到 t = 0',
        complexity='时间 `O(log mainTank)`，空间 `O(1)`',
        problem=['主油箱 `mainTank` 升，副油箱 `additionalTank` 升，每升跑 10 km',
                 '主油箱每用掉 5 升，副油箱有油就转 1 升过去',
                 '示例：`mainTank = 1, additionalTank = 2` → `10`',
                 '本视频：`mainTank = 26, additionalTank = 10` → `320`'],
        quote='不断将主油箱的油量除以5来计算可能获得的补给油量t，若当前的t大于0，那么就尝试从副油箱抽调t的油补到主油箱并更新行驶距离，然后重复此过程，直到某一时刻t等于0为止。',
        quote_src='—— yiduobo 题解原文',
        idea=['`t = mainTank // 5` 就是这一轮最多能得到的补给',
              '实际能转 `min(t, additionalTank)`，主油箱变成 `r + t`',
              '`t` 变成 0 时不会再补给，剩余油量 `* 10` 加进答案'],
        summary=['每轮 `mainTank` 大约缩成 1/4，时间 `O(log mainTank)`',
                 '易错：转油量要取 `min(t, additionalTank)`',
                 '原文为 Python 2 写法，`t = mainTank / 5` 的整数除法已改为 `//`',
                 '对比灵神：灵神循环条件是 `mainTank >= 5`，这里是 `while mainTank` 并在 `t = 0` 时 break'],
    ),
)
