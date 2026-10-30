DR = [[2, 1, 5], [4, 4, 5], [6, 6, 8], [-3, 2, 4], [5, 6, 1], [1, 5, 6]]
TG = [5, 5]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    drones = S['drones']
    tx, ty = TG
    X0, X1, Y0, Y1 = -5, 9, -1, 9
    W, H = x1 - x0 - 60, y1 - y0 - 80
    cell = min(W / (X1 - X0), H / (Y1 - Y0))
    ox = x0 + 30 + (W - cell * (X1 - X0)) / 2
    oy = y0 + 56 + (H - cell * (Y1 - Y0)) / 2 + cell * (Y1 - Y0)

    def P(x, y):
        return (ox + (x - X0) * cell, oy - (y - Y0) * cell)

    cv.text((x0 + 18, y0 + 4), '平面图（黄 = 正在看，绿 = 当前最优，蓝 = 够得着但不是最近，灰 = 够不着）', 22, T['muted'], bold=True)
    for gx in range(X0, X1 + 1):
        cv.line([P(gx, Y0), P(gx, Y1)], T['border'], 1)
    for gy in range(Y0, Y1 + 1):
        cv.line([P(X0, gy), P(X1, gy)], T['border'], 1)
    i = S.get('i')
    live = 'min_dis' in S
    md = S.get('min_dis', float('inf'))
    ans = S.get('ans', -1)
    if live and md != float('inf'):
        pts = [P(tx - md, ty), P(tx, ty + md), P(tx + md, ty), P(tx, ty - md), P(tx - md, ty)]
        cv.line(pts, T['green'], 3)
    cx, cy = P(tx, ty)
    cv.rect((cx - 11, cy - 11, cx + 11, cy + 11), fill=T['pink'], r=3)
    cv.text((cx + 16, cy - 8), f'target ({tx},{ty})', 20, T['pink'], anchor='lm', bold=True)
    for k, (x, y, r) in enumerate(drones):
        d = abs(tx - x) + abs(ty - y)
        seen = i is not None and (k < i or (k == i and 'dis' in S))
        c = T['dim']
        if seen and d <= r:
            c = T['blue']
        if k == ans:
            c = T['green']
        if k == i:
            c = T['yellow']
        px, py = P(x, y)
        if k == i:
            cv.dashed((px, py), (cx, cy), T['yellow'], 3)
        cv.rect((px - 12, py - 12, px + 12, py + 12), fill=c, r=12)
        cv.text((px, py - 18), f'{k}', 22, c if seen or k == i else T['muted'], anchor='mb', bold=True)
        if k == i:
            cv.text((px + 18, py + 10), f'r={r}', 20, T['yellow'], anchor='lm', bold=True)


CONFIG = dict(
    num=4024, title='最近的可用无人机', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='一次遍历模拟',
    tags=[],
    code='''
class Solution:
    def nearestDrone(self, drones: list[list[int]], target: list[int]) -> int:
        tx, ty = target
        min_dis = inf
        ans = -1
        for i, (x, y, r) in enumerate(drones):
            dis = abs(tx - x) + abs(ty - y)
            if dis <= r and dis < min_dis:
                min_dis = dis
                ans = i
        return ans
''',
    call=f'Solution().nearestDrone({DR!r}, {TG!r})',
    expect=4,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='array', var=lambda S: [f'{a},{b},{c}' for a, b, c in S['drones']], label='drones[i] = [x, y, range]', h=215, cell=118,
             pointers={'i': 'yellow'}),
    ],
    watch=[('i', 'i', 'yellow'), 'dis', ('r', 'r', 'orange'), ('min_dis', 'min_dis', 'green'), ('ans', 'ans', 'green')],
    captions={
        'tx, ty = target': '目标在 `({tx}, {ty})`',
        'min_dis = inf': '`min_dis` 记录目前最近的距离，初始为无穷大',
        'ans = -1': '`ans = -1`：没有无人机够得着就返回 -1',
        'for i, (x, y, r)': lambda S, B, rt: (f'看第 `{S.i}` 架：位置 `({S.x}, {S.y})`，飞行范围 `{S.r}`' if S.get('i') != B.get('i') else '所有无人机都看完了'),
        'dis = abs': '曼哈顿距离 `|{tx - x}| + |{ty - y}|` = =={dis}==',
        'if dis <= r and dis < min_dis': lambda S, B, rt: (
            f'`dis = {S.dis}`，`r = {S.r}`：' + (f'==够不着== `{S.dis} > {S.r}`，跳过' if S.dis > S.r else
            (f'够得着，且 `{S.dis} < {S.min_dis}` 更近 → ==更新==' if S.dis < S.min_dis else
             (f'够得着，但和当前最近并列（都是 {S.dis}）：`<` 不成立，==不换==，保住小下标' if S.dis == S.min_dis else f'够得着，但 `{S.dis}` 比当前最近的 `{S.min_dis}` 远，不换')))),
        'min_dis = dis': '最近距离更新为 `{min_dis}`',
        'ans = i': '答案下标更新为 `{ans}`',
        'return ans': '最近的可用无人机下标 =={ret}==',
    },
    cards=dict(
        one_liner='按题意模拟：够得着才比较，严格更近才更新',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`drones[i] = [x, y, range]`，曼哈顿距离 `<= range` 才能到达 `target`',
                 '返回能到达且距离最小的无人机下标，并列取最小下标，没有则 `-1`',
                 '示例：`drones=[[2,1,5],[4,4,5],[6,6,8]], target=[5,5]` → `1`'],
        quote='按题意模拟即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['遍历每架无人机，算曼哈顿距离 `abs(tx - x) + abs(ty - y)`',
              '条件 `dis <= r and dis < min_dis`：既够得着，又==严格==更近',
              '严格小于，距离相同就不更新，自然保留最小下标'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：是 `dis <= r`（可等于）和 `dis < min_dis`（必须严格小于）',
                 '`min_dis` 初始 `inf`，这样第一架够得着的一定能进来',
                 '本视频用 6 架无人机演示：下标 1、2 距离并列为 2，保留下标 1，最后被下标 4（距离 1）取代'],
    ),
)
