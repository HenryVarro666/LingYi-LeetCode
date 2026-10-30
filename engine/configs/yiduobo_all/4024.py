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
    i = S.get('index')
    live = 'min_dis' in S
    md = S.get('min_dis')
    ans = S.get('res', -1)
    if live and md is not None:
        pts = [P(tx - md, ty), P(tx, ty + md), P(tx + md, ty), P(tx, ty - md), P(tx - md, ty)]
        cv.line(pts, T['green'], 3)
    cx, cy = P(tx, ty)
    cv.rect((cx - 11, cy - 11, cx + 11, cy + 11), fill=T['pink'], r=3)
    cv.text((cx + 16, cy - 8), f'target ({tx},{ty})', 20, T['pink'], anchor='lm', bold=True)
    for k, (x, y, r) in enumerate(drones):
        d = abs(tx - x) + abs(ty - y)
        seen = i is not None and (k < i or (k == i and 'd' in S))
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
    author='yiduobo', technique='一趟遍历 · res = -1 判空',
    tags=[],
    code='''
class Solution(object):
    def nearestDrone(self, drones, target):
        
        res = -1
        min_dis = None
        for index, (x, y, r) in enumerate(drones):
            d = abs(x - target[0]) + abs(y - target[1])
            if d <= r and (res == -1 or min_dis > d):
                res = index
                min_dis = d
        
        return res
''',
    call=f'Solution().nearestDrone({DR!r}, {TG!r})',
    expect=4,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='array', var=lambda S: [f'{a},{b},{c}' for a, b, c in S['drones']], label='drones[i] = [x, y, range]', h=215, cell=118,
             pointers={'index': 'yellow'}),
    ],
    watch=[('index', 'index', 'yellow'), ('d', 'd', 'blue'), ('r', 'r', 'orange'), ('min_dis', 'min_dis', 'green'), ('res', 'res', 'green')],
    captions={
        'res = -1': '`res = -1`：用 -1 表示==还没找到==可用的无人机',
        'min_dis = None': '`min_dis = None`：第一架可用的无人机来了直接收下',
        'for index, (x, y, r)': lambda S, B, rt: (f'第 `{S.index}` 台：`({S.x}, {S.y})`，range = `{S.r}`' if S.get('index') != B.get('index') else '遍历结束'),
        'd = abs': '距离 `|{x}−{target[0]}| + |{y}−{target[1]}|` = =={d}==',
        'if d <= r and': lambda S, B, rt: (
            f'`d = {S.d}`，`range = {S.r}`：' + (f'`{S.d} > {S.r}` ==够不着==，跳过' if S.d > S.r else
            ('够得着，而且 `res == -1`：还没有答案，==直接收下==' if S.res == -1 else
             (f'够得着，`{S.min_dis} > {S.d}` 比当前更近 → ==更新==' if S.min_dis > S.d else
              (f'够得着，但并列（都是 {S.d}）：`>` 不成立，保留小下标' if S.min_dis == S.d else f'够得着，但 `{S.d}` 比当前最近 `{S.min_dis}` 远，不换'))))),
        'res = index': '`res` 更新为 `{res}`',
        'min_dis = d': '`min_dis` 更新为 `{min_dis}`',
        'return res': '最近的可用无人机下标 =={ret}==',
    },
    cards=dict(
        one_liner='遍历一趟：够得着才比较，用 res == -1 判断第一个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每台无人机有坐标和飞行范围，曼哈顿距离不超过范围才能到达目标',
                 '找可到达且距离最小的无人机下标，并列取最小下标，都不行返回 `-1`',
                 '示例：`drones=[[2,1,5],[4,4,5],[6,6,8]], target=[5,5]` → `1`'],
        quote='对于第index台无人机，先通过abs(x[index] - tx) + abs(y[index] - ty)计算当前无人机到目标的距离d。若d小于等于这台无人机的range[index]，就使用d以及index更新答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['按顺序遍历，先算距离 `d`，不超过 `range` 才有资格',
              '`res == -1` 表示还没有答案：第一台可用的直接收下，不需要初始化成无穷大',
              '之后只有 `min_dis > d`（严格更近）才更新，并列时下标小的先到、保留'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`min_dis` 初始是 `None`，靠 `res == -1` 短路，避免 `None > d` 比较',
                 '更新条件是 `min_dis > d`，严格大于，并列不换，天然取最小下标',
                 '原文 `class Solution(object)` 是 Python 2 风格，但代码在 Python 3 下无需修改',
                 '对比灵神：灵神用 `inf` 做初值省掉判空，yiduobo 用 `res == -1`'],
    ),
)
