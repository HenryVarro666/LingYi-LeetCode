D4 = ((0, 1), (1, 0), (0, -1), (-1, 0))


def _mk(xn, yn, kn):
    ARROW = ['↑ 北', '→ 东', '↓ 南', '← 西']
    OBS = [(2, 4)]

    def _draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        X0, X1, Y0, Y1 = -1, 4, -1, 9
        nx, ny = X1 - X0 + 1, Y1 - Y0 + 1
        cell = min((x1 - x0 - 40) / nx, (y1 - y0 - 50) / ny, 56)
        sx = x0 + 20 + ((x1 - x0 - 40) - cell * nx) / 2
        sy = y0 + 40
        cv.text((x0 + 18, y0 + 2), '地图（黄 = 机器人，红 = 障碍物，北在上）', 22, T['muted'], bold=True)

        def P(gx, gy):
            return sx + (gx - X0) * cell, sy + (Y1 - gy) * cell
        for gx in range(X0, X1 + 1):
            for gy in range(Y0, Y1 + 1):
                px, py = P(gx, gy)
                cv.rect((px + 1, py + 1, px + cell - 1, py + cell - 1), fill=T['panel2'], outline=T['border'], r=4)
                if gy == 0 or gx == 0:
                    cv.text((px + cell / 2, py + cell / 2), '', 14, T['dim'], anchor='mm')
        px, py = P(0, 0)
        cv.rect((px + 3, py + 3, px + cell - 3, py + cell - 3), outline=T['green'], width=3, r=6)
        cv.text((px + cell / 2, py + cell + 4), '原点', 16, T['green'], anchor='mt')
        for gx, gy in OBS:
            px, py = P(gx, gy)
            cv.rect((px + 4, py + 4, px + cell - 4, py + cell - 4), fill=T['red'], r=6)
            if cell >= 40:
                cv.text((px + cell / 2, py + cell / 2), f'{gx},{gy}', 16, T['bg'], anchor='mm', bold=True)
        if xn in S and yn in S:
            rx, ry = S[xn], S[yn]
            if X0 <= rx <= X1 and Y0 <= ry <= Y1:
                px, py = P(rx, ry)
                cv.rect((px + 5, py + 5, px + cell - 5, py + cell - 5), fill=T['yellow'], r=cell / 2)
                dxy = [(0, -1), (1, 0), (0, 1), (-1, 0)][S[kn] % 4]
                cx, cy = px + cell / 2, py + cell / 2
                cv.arrow((cx - dxy[0] * cell * 0.25, cy - dxy[1] * cell * 0.25), (cx + dxy[0] * cell * 0.32, cy + dxy[1] * cell * 0.32), T['bg'], width=4, head=9)
            cv.text((x1 - 20, y0 + 40), f'位置 ({rx}, {ry})', 26, T['yellow'], anchor='ra', bold=True)
            cv.text((x1 - 20, y0 + 80), f'朝向 {ARROW[S[kn]]}', 26, T['blue'], anchor='ra', bold=True)
            cv.text((x1 - 20, y0 + 120), f'距离² = {rx * rx + ry * ry}', 26, T['green'], anchor='ra', bold=True)
    return _draw


_draw = _mk('x', 'y', 'k')


CONFIG = dict(
    num=874, title='模拟行走机器人', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='方向数组 + 哈希集合模拟',
    code='''
DIRS = (0, 1), (1, 0), (0, -1), (-1, 0)  # 上右下左（顺时针）

class Solution:
    def robotSim(self, commands: List[int], obstacles: List[List[int]]) -> int:
        obstacle_set = set(map(tuple, obstacles))
        ans = x = y = k = 0
        for c in commands:
            if c < 0:
                k = (k + c * 2 + 7) % 4  # c=-2 左转，c=-1 右转
                continue
            while c > 0 and (x + DIRS[k][0], y + DIRS[k][1]) not in obstacle_set:
                x += DIRS[k][0]
                y += DIRS[k][1]
                c -= 1
            ans = max(ans, x * x + y * y)
        return ans
''',
    call='Solution().robotSim([4,-1,4,-2,4], [[2,4]])',
    expect=65,
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='text', size=28, h=70,
             fn=lambda S: f"命令 `{S['commands']}`，当前 `c = {S['c']}`" if 'c' in S else ''),
    ],
    watch=['c', 'x', 'y', 'k', ('ans', 'ans', 'green')],
    captions={
        'obstacle_set = set': '障碍物转成集合 `{obstacle_set}`：判断某坐标是不是障碍物只要 `O(1)`',
        'ans = x = y = k = 0': '从原点出发，`k = 0` 朝北；`ans` 记录到过的最大距离平方',
        'if c < 0': lambda S, B, r: (f'`c = {S.c}` < 0：是转向命令' if S.c < 0 else f'`c = {S.c}`：向前走 `{S.c}` 步'),
        'k = (k + c * 2 + 7)': '`c = {c}`：`(k + c*2 + 7) % 4` → `k = {k}`，朝向 =={["北","东","南","西"][k]}==',
        'while c > 0': lambda S, B, r: ((f'还剩 `{S.c}` 步，下一格 `({S.x + D4[S.k][0]}, {S.y + D4[S.k][1]})` 不是障碍 → 前进')
                                        if S.c > 0 and (S.x + D4[S.k][0], S.y + D4[S.k][1]) not in S.obstacle_set
                                        else ('步数走完，停下' if S.c <= 0 else f'下一格 `({S.x + D4[S.k][0]}, {S.y + D4[S.k][1]})` ==是障碍物== → 原地停下，不走了')),
        'x += DIRS[k][0]': '沿方向 `{((0, 1), (1, 0), (0, -1), (-1, 0))[k]}` 前进一格（`x`、`y` 同时加上方向分量，`c` 减 1）',
        'ans = max': '走完这条命令，距离² = `{x}² + {y}²` = {x * x + y * y}，`ans = max({B.ans}, {x * x + y * y}) = =={ans}==`',
        'return ans': '所有命令执行完，最大距离² = =={ans}==',
    },
    skip=['y += DIRS', 'c -= 1', 'continue'],
    cards=dict(
        one_liner='方向用下标 k 表示，一格一格走，遇到障碍就停',
        complexity='时间 `O(nU + m)`（U = 9），空间 `O(m)`',
        problem=['机器人从 `(0,0)` 朝北出发：`-2` 左转，`-1` 右转，`1..9` 前进若干格',
                 '遇到障碍物就停在它前一格，继续下一条命令',
                 '返回途中离原点最远的欧氏距离的==平方==',
                 '示例：`[4,-1,4,-2,4]`，障碍 `[[2,4]]` → `65`'],
        quote='用一个下标 k 表示当前机器人的方向为 dirs[k]，初始 k=0，表示初始方向为上。右转把 k 增加一，左转把 k 增加三，再模 4。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`DIRS` 是顺时针的上右下左；右转 `k+1`，左转 `k+3`（循环数组）',
              '写法二：`c = -1` 右转、`c = -2` 左转，统一成 `(k + 2c + 7) % 4`',
              '障碍物放进哈希集合，每走一步查下一格是否在集合里'],
        summary=['时间 `O(nU + m)`，空间 `O(m)`',
                 '易错：障碍物坐标要转成 tuple 才能放进集合',
                 '易错：起点有障碍物也能继续走，只检查「下一格」',
                 '只在每条前进命令走完后更新 `ans`，中途停在障碍前同样有效',
                 '写法一用 if/elif 分别处理右转、左转，效果相同'],
    ),
)
