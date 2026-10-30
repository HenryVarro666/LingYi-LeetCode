M0, A0 = 26, 10


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '两个油箱（每格 = 1 升）；已行驶距离在下面', 24, T['muted'], bold=True)
    main, add = S.get('mainTank'), S.get('additionalTank')
    if main is None:
        return
    ans = S.get('ans', 0)
    for row, (name, v, v0, c) in enumerate((('mainTank 主油箱', main, M0 + 5, 'blue'), ('additionalTank 副油箱', add, A0, 'orange'))):
        yy = y0 + 70 + row * 150
        cv.text((x0 + 30, yy), f'{name} = {v}', 28, T[c], bold=True)
        W = x1 - x0 - 60
        cell = min(30, W / v0)
        for k in range(v0):
            X = x0 + 30 + k * cell
            cv.rect((X + 1, yy + 44, X + cell - 1, yy + 84), fill=T[c] if k < v else T['panel2'], outline=T['border'], r=3)
    cv.text((x0 + 30, y0 + 380), f'已行驶 ans = {ans} km', 34, T['green'], bold=True)
    cv.text((x0 + 30, y0 + 440), f'每升 10 km；主油箱每耗 5 升，副油箱转 1 升', 24, T['muted'])


CONFIG = dict(
    num=2739, title='总行驶距离', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='快速模拟 · 批量换算',
    code='''
class Solution:
    def distanceTraveled(self, mainTank: int, additionalTank: int) -> int:
        ans = 0
        while mainTank >= 5:
            t = mainTank // 5
            ans += t * 50
            mainTank %= 5
            t = min(t, additionalTank)
            additionalTank -= t
            mainTank += t
        return ans + mainTank * 10
''',
    call=f'Solution().distanceTraveled({M0}, {A0})',
    expect=320,
    views=[dict(type='custom', draw=_draw, h=520)],
    watch=[('mainTank', 'mainTank', 'blue'), ('additionalTank', 'additionalTank', 'orange'), 't', ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 记录已行驶的距离',
        'while mainTank >= 5': lambda S, B, r: (f'`mainTank = {S.mainTank} >= 5`：还能再凑出整 5 升，会触发转油' if S.mainTank >= 5
                                                  else f'`mainTank = {S.mainTank} < 5`：不会再触发转油，退出循环'),
        't = mainTank // 5': '把逐次 `-= 5` 合并：一共会消耗 5 升 `t = {mainTank} // 5 = {t}` 次',
        'ans += t * 50': '这 `{t}` 次共 `{t} * 5` 升，行驶 `{t} * 50` → `ans = {ans}`',
        'mainTank %= 5': '整 5 升都烧掉了，主油箱只剩零头 `mainTank = {mainTank}`',
        't = min(t, additionalTank)': '最多转 `t` 升，但副油箱不够就只能转 `min` → `t = {t}`',
        'additionalTank -= t': '副油箱减去转走的 `{t}` 升 → `{additionalTank}`',
        'mainTank += t': '转来的 `{t}` 升加回主油箱 → `mainTank = {mainTank}`，它可能又凑够 5 升',
        'return': '剩下不足 5 升的油不会再转油，直接 `* 10`：`{ans} + {mainTank} * 10` = =={ret}==',
    },
    cards=dict(
        one_liner='把逐次减 5 合并成一次除法，批量处理',
        complexity='时间 `O(log mainTank)`，空间 `O(1)`',
        problem=['主油箱 `mainTank` 升，副油箱 `additionalTank` 升，每升跑 10 km',
                 '主油箱每用掉 5 升，副油箱有油就转 1 升过去',
                 '示例：`mainTank = 5, additionalTank = 10` → `60`',
                 '本视频：`mainTank = 26, additionalTank = 10` → `320`'],
        quote='把方法一的减法改成除法，统计 -= 5 发生了 t = ⌊mainTank/5⌋ 次。然后再一次性地把 t 升燃料注入主油箱。注意 t 不能超过 additionalTank。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['方法一每次减 5 模拟，`mainTank` 到 10^9 就超时',
              '一次算出会触发 `t` 次转油，==批量==加距离、批量转油',
              '转进来的油可能又够 5 升，所以外面套 `while`'],
        summary=['时间 `O(log mainTank)`：每轮 `mainTank` 至少缩成原来的 1/4',
                 '易错：`t = min(t, additionalTank)`，副油箱可能不够',
                 '方法一是逐次 `-= 5` 模拟，`O(mainTank)`',
                 '方法三一行公式：`(mainTank + min((mainTank-1)//4, additionalTank)) * 10`',
                 '相似题：1518 换水问题'],
    ),
)
