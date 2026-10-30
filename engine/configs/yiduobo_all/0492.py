CONFIG = dict(
    num=492, title='构造矩形', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='从 sqrt 往下枚举因数',
    code='''
class Solution(object):
    def constructRectangle(self, area):

        W = int(sqrt(area))
        while area % W != 0:
            W -= 1
        return [area // W, W]
''',
    setup='from math import sqrt',
    call='Solution().constructRectangle(28)',
    expect=[7, 4],
    views=[
        dict(type='text', size=34, fn=lambda S: (f"面积 `{S['area']}` = 长 `{S['area'] // S['W']}` × 宽 `{S['W']}`" + (' ==整除，找到了==' if S['area'] % S['W'] == 0 else f"　余数 `{S['area'] % S['W']}` ≠ 0")) if 'W' in S and S['W'] > 0 else f"目标面积 `{S['area']}`"),
        dict(type='text', size=26, fn=lambda S: f"`sqrt({S['area']})` ≈ {S['area'] ** 0.5:.2f}，W 从 `{int(S['area'] ** 0.5)}` 开始往下找" if 'W' in S else ''),
        dict(type='custom', h=330, draw=lambda cv, S, B, box, T: _rect(cv, S, box, T)),
    ],
    watch=[('area', 'area', 'blue'), ('W', 'W', 'pink'), ('area % W', 'area % W', 'yellow')],
    captions={
        'W = int': '`W = int(sqrt({area})) = {W}`：宽不能超过长，所以从 ==sqrt== 开始，这时长宽最接近',
        'while area % W': lambda S, B, r: (f'`{S.area} % {S.W} = {S.area % S.W}` ≠ 0 → 不能整除，这个宽凑不出矩形' if S.area % S.W else f'`{S.area} % {S.W} = 0` → 能整除，==长宽找到了==，退出循环'),
        'W -= 1': '宽减 1 再试：`W` → {W}（越往下，长宽差越大，所以第一个成功的就最接近）',
        'return': '长 `{area} // {W} = {area // W}`，宽 `{W}` → ==返回 [{area // W}, {W}]==',
    },
    cards=dict(
        one_liner='从 sqrt(area) 往下枚举，第一个整除的 W 就是答案',
        complexity='时间 `O(sqrt(area))`，空间 `O(1)`',
        problem=['给定面积 `area`，设计长 `L`、宽 `W` 的矩形，满足 `L × W = area` 且 `L ≥ W`',
                 '长宽差要尽可能小，返回 `[L, W]`',
                 '示例：`area = 4` → `[2, 2]`；本视频：`28` → `[7, 4]`'],
        quote='为了使得W小于等于L且W和L尽可能接近，那么应该从sqrt(area)开始，逐个往下枚举W。当area模W为0时，L为area/W，此时的W和L即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['`W ≤ L` 说明 `W ≤ sqrt(area)`，所以起点是 `int(sqrt(area))`',
              '往下枚举 W：W 越大，长宽越接近',
              '第一个满足 `area % W == 0` 的 W 就是最优'],
        summary=['时间 `O(sqrt(area))`，空间 `O(1)`',
                 '`W = 1` 一定能整除，所以循环必定终止',
                 '原文为 Python 2 写法，`area / W` 已改为 `area // W`（整数除法）',
                 '原文用了 `sqrt` 但没写 import，这里在 setup 里补了 `from math import sqrt`'],
    ),
)


def _rect(cv, S, box, T):
    x0, y0, x1, y1 = box
    if 'W' not in S or S['W'] <= 0:
        return
    area, W = S['area'], S['W']
    L = area / W
    ok = area % W == 0
    unit = min((x1 - x0 - 80) / max(L, 8), (y1 - y0 - 60) / max(W, 1), 56)
    w, h = L * unit, W * unit
    ox, oy = (x0 + x1) / 2 - w / 2, y0 + 20
    cv.rect((ox, oy, ox + w, oy + h), fill=T['green'] if ok else T['border'], alpha=150 if ok else 255, r=6)
    cv.text(((x0 + x1) / 2, oy + h + 8), f'长 {L:g}  ×  宽 {W}' + ('' if ok else '（不是整数，凑不出）'), 24, T['text'] if ok else T['muted'], anchor='mt', bold=True)
