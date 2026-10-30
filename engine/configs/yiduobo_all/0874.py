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


_draw = _mk('nowx', 'nowy', 'dpos')


CONFIG = dict(
    num=874, title='模拟行走机器人', difficulty='Medium', category='模拟',
    author='yiduobo', technique='障碍物按行列聚合 + 二分',
    code='''
class Solution(object):
    def robotSim(self, commands, obstacles):

        x_dict = {}
        y_dict = {}
        for x, y in obstacles:
            if x not in x_dict:
                x_dict[x] = []
            if y not in y_dict:
                y_dict[y] = []
            x_dict[x].append(y)
            y_dict[y].append(x)
        
        sorted_x_dict = {}
        sorted_y_dict = {}
        for x in x_dict:
            sorted_x_dict[x] = sorted(x_dict[x])
        for y in y_dict:
            sorted_y_dict[y] = sorted(y_dict[y])
        
        nowx, nowy = 0, 0
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        dpos = 0
        res = 0
        for cmd in commands:
            if cmd == -1:
                dpos = (dpos + 1) % 4
            elif cmd == -2:
                dpos = (dpos + 3) % 4
            else:
                if dpos == 0:
                    delta = self.bisect(sorted_x_dict.get(nowx, []), nowy, True)
                elif dpos == 1:
                    delta = self.bisect(sorted_y_dict.get(nowy, []), nowx, True)
                elif dpos == 2:
                    delta = self.bisect(sorted_x_dict.get(nowx, []), nowy, False)
                else:
                    delta = self.bisect(sorted_y_dict.get(nowy, []), nowx, False)
                if delta is None or delta > cmd:
                    movelen = cmd
                else:
                    movelen = delta - 1
                nowx += dx[dpos] * movelen
                nowy += dy[dpos] * movelen
                res = max(res, nowx ** 2 + nowy ** 2)
        
        return res

    def bisect(self, pos_list, x, bigger_flag):
        if not pos_list:
            return None
        if x >= pos_list[-1]:
            if bigger_flag:
                return None
            elif x == pos_list[-1]:
                if len(pos_list) == 1:
                    return None
                else:
                    return x - pos_list[-2]
            else:
                return x - pos_list[-1]

        l = 0
        r = len(pos_list) - 1
        while l < r:
            mid = (l + r) >> 1
            if pos_list[mid] <= x:
                l = mid + 1
            else:
                r = mid

        if bigger_flag:
            return pos_list[l] - x
        
        if l == 0:
            return None
        
        if x == pos_list[l - 1]:
            if l == 1:
                return None
            else:
                return x - pos_list[l - 2]
        else:
            return x - pos_list[l - 1]
''',
    call='Solution().robotSim([4,-1,4,-2,4], [[2,4]])',
    expect=65,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='map', var='sorted_x_dict', label='sorted_x_dict：x → 该列障碍物的 y（已排序）', fmt=lambda k, v: f'x={k}: {v}', h=100, font=28),
        dict(type='map', var='sorted_y_dict', label='sorted_y_dict：y → 该行障碍物的 x（已排序）', fmt=lambda k, v: f'y={k}: {v}', h=100, font=28),
        dict(type='text', size=28, h=70,
             fn=lambda S: f"当前命令 `cmd = {S['cmd']}`" + (f"，到下一个障碍的距离 `delta = {S['delta']}`" if 'delta' in S else '') if 'cmd' in S else ''),
    ],
    watch=['cmd', 'nowx', 'nowy', 'dpos', 'delta', ('res', 'res', 'green')],
    captions={
        'x_dict[x].append(y)': '障碍 `({x}, {y})`：记入第 `{x}` 列和第 `{y}` 行',
        'sorted_x_dict[x] = sorted': '第 `{x}` 列的障碍排序 → `{sorted_x_dict[x]}`',
        'sorted_y_dict[y] = sorted': '第 `{y}` 行的障碍排序 → `{sorted_y_dict[y]}`',
        'nowx, nowy = 0, 0': '机器人在原点；`dpos` 是方向下标：0 北、1 东、2 南、3 西',
        'if cmd == -1': '`cmd = {cmd}`：{"右转" if cmd == -1 else "不是右转"}',
        'dpos = (dpos + 1) % 4': '右转：`dpos` → `{dpos}`',
        'elif cmd == -2': '`cmd = {cmd}`：{"左转" if cmd == -2 else "前进 cmd 步"}',
        'dpos = (dpos + 3) % 4': '左转：`dpos` → `{dpos}`',
        'delta = self.bisect': '朝 `dpos = {dpos}` 走：在同一行/列的有序障碍里二分，找下一个障碍离我多远',
        'if delta is None': lambda S, B, r: ('没有障碍挡路，或障碍比 cmd 还远 → 走满 `cmd` 步' if (S.delta is None or S.delta > S.cmd)
                                             else f'`delta = {S.delta} <= cmd = {S.cmd}`：障碍挡路 → 只能走到它前一格'),
        'movelen = cmd': '`movelen = {movelen}`',
        'movelen = delta - 1': '`movelen = delta - 1 = {movelen}`：停在障碍前一格',
        'nowx += dx[dpos]': '`nowx += dx[dpos] * {movelen}` → `{nowx}`',
        'nowy += dy[dpos]': '`nowy += dy[dpos] * {movelen}` → `{nowy}`',
        'res = max': '距离² = `{nowx}² + {nowy}²` = {nowx ** 2 + nowy ** 2}，`res = max({B.res}, …) = =={res}==`',
        'if not pos_list': '`pos_list = {pos_list}`：{"这一行/列没有障碍 → 返回 None" if not pos_list else "有障碍，继续"}',
        'return pos_list[l] - x': '下一个障碍在 `{pos_list[l]}`，距离 `{pos_list[l]} - {x} = {ret}`',
        'return res': '最大距离² = =={res}==',
    },
    skip=['sorted_x_dict = {}', 'sorted_y_dict = {}', 'dx = [', 'dy = [', 'dpos = 0', 'res = 0', 'x_dict[x] = []', 'y_dict[y] = []', 'x_dict = {}', 'y_dict = {}'],
    cards=dict(
        one_liner='障碍物按行列分组排序，每条命令二分找到挡路的障碍',
        complexity='时间 `O(m log m + n log m)`，空间 `O(m)`',
        problem=['机器人从 `(0,0)` 朝北出发：`-2` 左转，`-1` 右转，`1..9` 前进若干格',
                 '遇到障碍物就停在它前一格，继续下一条命令',
                 '返回途中离原点最远的欧氏距离的==平方==',
                 '示例：`[4,-1,4,-2,4]`，障碍 `[[2,4]]` → `65`'],
        quote='我在这里选择的做法是先对障碍物按行和列进行聚合，然后分别排序。在每次行走之前，先通过二分找到下一个障碍物的位置，然后判断这次指令是否会碰到该障碍物。',
        quote_src='—— yiduobo 题解原文',
        idea=['原文先说明：最多 4000 条指令，一步步模拟也只有约 36000 次操作，可行',
              '他的做法是更快的：`x_dict[x]` 存同一列所有障碍的 y，`y_dict[y]` 存同一行的 x',
              '前进前在有序列表里二分，得到「下一个障碍离我多远」`delta`',
              '`delta > cmd` 走满，否则只走 `delta - 1` 格'],
        summary=['时间 `O(m log m + n log m)`，空间 `O(m)`',
                 '易错：`bisect` 要区分朝正向还是反向，且站在障碍上时（`x ==` 某障碍）要找更远的那个',
                 '`delta` 为 None 表示这个方向没有挡路的障碍',
                 '对比灵神：灵神一格一格走并查集合，yiduobo 用二分一步到位',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行'],
    ),
)
