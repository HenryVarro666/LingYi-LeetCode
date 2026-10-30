TX, TY = 3, 2
OBS = [[5, 2], [1, 2], [2, 2]]
CMD = 'URR'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    NX, NY = 7, 4
    cell = min(110, (x1 - x0 - 120) / NX, (y1 - y0 - 150) / NY)
    ox = x0 + 70 + ((x1 - x0 - 120) - cell * NX) / 2
    oy = y1 - 70
    P = lambda a, b: (ox + a * cell, oy - b * cell)
    cv.text((x0 + 18, y0 + 4), '坐标平面：蓝点 = 一个周期走过的格子，浅蓝 = 重复的周期，红 = 陷阱，黄 = 终点', 22, T['muted'], bold=True)
    for a in range(NX):
        for b in range(NY):
            px, py = P(a, b)
            cv.rect((px - cell / 2 + 3, py - cell / 2 + 3, px + cell / 2 - 3, py + cell / 2 - 3), fill=T['panel2'], r=8)
        cv.text((P(a, 0)[0], oy + cell / 2 + 6), a, 20, T['dim'], anchor='mt', mono=True)
    for b in range(NY):
        cv.text((ox - cell / 2 - 8, P(0, b)[1]), b, 20, T['dim'], anchor='rm', mono=True)
    pts = S.get('points_on_path') or []
    done = 'nowx' in S and S.get('_line', 0) >= 11
    base = [(0, 0)] + [tuple(p) for p in pts]
    if done and pts:
        ex, ey = pts[-1]
        for k in (1, 2):
            for (a, b) in base:
                a2, b2 = a + ex * k, b + ey * k
                if a2 < NX and b2 < NY:
                    px, py = P(a2, b2)
                    cv.rect((px - cell / 2 + 10, py - cell / 2 + 10, px + cell / 2 - 10, py + cell / 2 - 10), fill=T['cyan'], alpha=70, r=10)
    for i, (a, b) in enumerate(base):
        px, py = P(a, b)
        cv.rect((px - cell / 2 + 6, py - cell / 2 + 6, px + cell / 2 - 6, py + cell / 2 - 6), fill=T['blue'] if i else T['green'], r=10)
        cv.text((px, py), '起' if i == 0 else i, 26, T['bg'], anchor='mm', bold=True)
    if not pts:
        cv.rect((P(0, 0)[0] - cell / 2 + 6, P(0, 0)[1] - cell / 2 + 6, P(0, 0)[0] + cell / 2 - 6, P(0, 0)[1] + cell / 2 - 6), fill=T['green'], r=10)
    for a, b in OBS:
        if a < NX and b < NY:
            px, py = P(a, b)
            cv.rect((px - cell / 2 + 3, py - cell / 2 + 3, px + cell / 2 - 3, py + cell / 2 - 3), outline=T['red'], width=4, r=10)
            cv.text((px, py + cell / 2 - 12), f'({a},{b})', 16, T['red'], anchor='mb', mono=True, bold=True)
    px, py = P(TX, TY)
    cv.rect((px - cell / 2 + 3, py - cell / 2 + 3, px + cell / 2 - 3, py + cell / 2 - 3), outline=T['yellow'], width=5, r=10)
    cv.text((px, py - cell / 2 + 10), '终点', 18, T['yellow'], anchor='mt', bold=True)
    I = S.get('_inner', {})
    if 'pre_round' in I:
        cx, cy = I['x'], I['y']
        if cx < NX and cy < NY:
            px, py = P(cx, cy)
            cv.rect((px - cell / 2, py - cell / 2, px + cell / 2, py + cell / 2), outline=T['pink'], width=6, r=12)
            cv.text((x0 + 18, y0 + 40), f'粉框 = 正在检查 ({cx},{cy})；橙框 = 走完 {I["pre_round"]} 个整周期的位置', 24, T['pink'], bold=True)
        nx_, ny_ = I.get('nowx'), I.get('nowy')
        if nx_ is not None and nx_ < NX and ny_ < NY:
            px, py = P(nx_, ny_)
            cv.rect((px - cell / 2 + 14, py - cell / 2 + 14, px + cell / 2 - 14, py + cell / 2 - 14), outline=T['orange'], width=4, r=8)


def _cap_check(S, B, r):
    I = S['_inner']
    return (f'目标 `({I["x"]}, {I["y"]})`：每周期前进 `({S["points_on_path"][-1][0]}, {S["points_on_path"][-1][1]})`，'
            f'x、y 方向分别最多完整走 `{I["x"]}//{S["points_on_path"][-1][0]}`、`{I["y"]}//{S["points_on_path"][-1][1]}` 个周期，取较小 → ==`{I["pre_round"]}` 个周期==')


CONFIG = dict(
    num='LCP 03', title='机器人大冒险', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='模拟一个周期 · 枚举周期内位置',
    tags=[],
    code='''
class Solution(object):
    def robot(self, command, obstacles, x, y):

        points_on_path = []
        nowx = nowy = 0
        for com in command:
            if com == 'U':
                nowy += 1
            else:
                nowx += 1
            points_on_path.append([nowx, nowy])

        def check(x, y):
            pre_round = min(x // points_on_path[-1][0], y // points_on_path[-1][1])
            nowx = points_on_path[-1][0] * pre_round
            nowy = points_on_path[-1][1] * pre_round
            if nowx == x and nowy == y:
                return True
            for dx, dy in points_on_path:
                if nowx + dx == x and nowy + dy == y:
                    return True
            return False

        if not check(x, y):
            return False

        for ox, oy in obstacles:
            if ox > x or oy > y:
                continue
            if check(ox, oy):
                return False
        
        return True
''',
    call=f'Solution().robot("{CMD}", {OBS}, {TX}, {TY})',
    expect=False,
    skip=['nowx = nowy = 0', 'points_on_path = []', 'nowx = points', 'nowy = points'],
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', fn=lambda S: (f"一个周期（`{CMD}`）后的增量：`dx = {S['points_on_path'][-1][0]}`，`dy = {S['points_on_path'][-1][1]}`"
                                       if S.get('points_on_path') and S.get('_line', 0) >= 11 else '先模拟一遍指令，记录走过的位置'), size=28),
    ],
    watch=[('command', lambda S: S.get('command')), ('nowx', lambda S: S.get('nowx')), ('nowy', lambda S: S.get('nowy'))],
    captions={
        'points_on_path = []': '`points_on_path` 记录一个周期里走过的每个位置',
        'for com in command': '取下一条指令',
        "if com == 'U'": '指令 `{com}`：`U` 向上走一格，`R` 向右走一格',
        'nowy += 1': '向上：`nowy` → {nowy}',
        'nowx += 1': '向右：`nowx` → {nowx}',
        'points_on_path.append': '记下这个位置 `({nowx}, {nowy})`；循环结束后最后一项就是==一个周期的总增量==',
        'pre_round = min': _cap_check,
        'nowx = points_on_path': '`k` 个周期后机器人在 `({nowx}, …)`',
        'nowy = points_on_path': '`k` 个周期后机器人在 `({nowx}, {nowy})`',
        'if nowx == x and nowy == y': '整周期正好落在目标上？`({nowx}, {nowy})` vs `({x}, {y})` → {"是" if nowx == x and nowy == y else "否"}',
        'for dx, dy in': '再枚举第 `k+1` 个周期里的每个位置 `+({dx}, {dy})`',
        'if nowx + dx == x': '`({nowx + dx}, {nowy + dy})` 是 `({x}, {y})` 吗？→ {"是，能走到" if nowx + dx == x and nowy + dy == y else "不是"}',
        'return True': lambda S, B, r: ('机器人能走到这个位置' if S.get('_inner', {}).get('pre_round') is not None else '终点可达、也没踩到陷阱 → `True`'),
        'return False': lambda S, B, r: ('周期内所有位置都试过，走不到这里' if S.get('_inner', {}).get('pre_round') is not None
                                         else '终点走不到或踩中陷阱 → `False`'),
        'if not check(x, y)': '先检查终点能不能走到：能走到才有必要看陷阱',
        'for ox, oy in obstacles': '逐个看陷阱 `({ox}, {oy})`',
        'if ox > x or oy > y': '陷阱 `({ox}, {oy})` 的横或纵坐标超过终点 `({x}, {y})` 吗？{"是 → 机器人只会往上、往右，到不了它，跳过" if ox > x or oy > y else "否 → 可能踩到，要检查"}',
        'continue': '这个陷阱在终点之外，不用检查',
        'if check(ox, oy)': '陷阱 `({ox}, {oy})` 能走到吗？→ {"能走到，机器人会踩到" if check(ox, oy) else "走不到，安全"}',
    },
    cards=dict(
        one_liner='指令周而复始：只模拟一个周期，再算要走几个整周期',
        complexity='时间 `O(len(command) + len(obstacles) × len(command))`，空间 `O(len(command))`',
        problem=['机器人从 `(0,0)` 出发，指令 `U` 向上、`R` 向右，无限循环',
                 '路上有若干陷阱，问能否到达终点 `(x, y)` 且不踩到陷阱',
                 '本视频：`command="URR"`，陷阱 `[[5,2],[1,2],[2,2]]`，终点 `(3,2)` → `False`'],
        quote='题目中的机器人总是复读同一段指令，不妨先模拟一个周期，就可以得到在一个周期中走到的所有格子，以及最终再横纵坐标上有多少增量。',
        quote_src='—— yiduobo 题解原文',
        idea=['能走到 `(X, Y)` ⇔ 走了 `k` 个整周期后，再在下一周期里走到：`dx*k + path_x[i] = X`',
              '`k` 取 `min(X//dx, Y//dy)`，再枚举周期内的每个位置',
              '先看终点能不能到；再看陷阱，横或纵坐标超过终点的陷阱可以直接忽略'],
        summary=['时间约 `O(陷阱数 × 指令长度)`，坐标再大也不用逐步模拟',
                 '易错点：`k` 取 x、y 两个方向的较小值，才不会走过头',
                 '易错点：陷阱超过终点就不用管（机器人永远不回头）',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '提示：`command` 全是 `U` 或全是 `R` 时除数会为 0，示例数据不涉及'],
    ),
)
