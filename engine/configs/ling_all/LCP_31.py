MAZE = [['.#.'], ['.#.'], ['.#.']]


def _vcells(S):
    if 'vis' not in S:
        return None
    k, n, m = len(S['vis']), len(S['vis'][0]), len(S['vis'][0][0])
    return [[''.join(str(s) for s in range(6) if any(S['vis'][t][i][j][s] for t in range(k))) for j in range(m)] for i in range(n)]


CONFIG = dict(
    num='LCP 31', title='变换的迷宫', difficulty='Hard', category='网格图',
    author='灵茶山艾府', technique='记忆化 DFS：时间 + 位置 + 卷轴状态（Go 原文转写）',
    tags=['灵神题单', '综合应用'],
    code='''
dir4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

class Solution:
    def escapeMaze(self, g: List[List[str]]) -> bool:
        k, n, m = len(g), len(g[0]), len(g[0][0])
        vis = [[[[False] * 6 for _ in range(m)] for _ in range(n)] for _ in range(k)]
        # s 的最低位：是否使用了临时消除术
        # s 的其余位：0-未使用永久消除术，1-当前正位于永久消除的位置，2-已使用永久消除术
        def f(t, x, y, s):
            if x < 0 or x >= n or y < 0 or y >= m or t + n - 1 - x + m - 1 - y >= k or vis[t][x][y][s]:
                return False
            if x == n - 1 and y == m - 1:
                return True
            vis[t][x][y][s] = True
            if s >> 1 == 1:
                for dx, dy in dir4:
                    if f(t + 1, x + dx, y + dy, s ^ 6):  # 跳出永久消除的位置
                        return True
                return f(t + 1, x, y, s)
            if s >> 1 == 0 and g[t][x][y] == '#' and f(t, x, y, s | 2):  # 尝试使用永久消除术
                return True
            # 使用永久消除术已无法走到终点，遇到障碍只能使用临时消除术
            if g[t][x][y] == '#':
                if s & 1 == 1:
                    return False
                s |= 1
            for dx, dy in dir4:
                if f(t + 1, x + dx, y + dy, s):
                    return True
            return f(t + 1, x, y, s)
        return f(0, 0, 0, 0)
''',
    call=f'Solution().escapeMaze({MAZE})',
    expect=True,
    views=[
        dict(type='grid', var=lambda S: list(S['g'][S['t']]) if 't' in S else None,
             label='g[t]：时刻 t 的迷宫（红 = 陷阱，蓝框 = 当前位置，右下角是出口）', cell=96, h=230,
             cursors=[('x', 'y', 'blue')], color=lambda S, i, j, v: 'red' if v == '#' else None),
        dict(type='grid', var=_vcells, label='vis：各位置访问过的状态 s（跨所有时刻合并）', cell=96, h=190,
             values=True),
        dict(type='text', fn=lambda S: (f"`s = {S['s']}`：临时消除术 ==" + ('已用' if S['s'] & 1 else '未用') + "==，永久消除术 ==" + ('已用' if S['s'] >> 1 == 2 else '正位于该位置' if S['s'] >> 1 == 1 else '未用') + '==') if 's' in S else '', size=24, h=70),
        dict(type='calls', h=250),
    ],
    watch=['t', 'x', 'y', ('s', 's', 'yellow')],
    captions={
        'k, n, m = len(g)': '`k = {k}` 个时刻，迷宫 `{n}×{m}`',
        'vis = [[[[False]': '`vis[t][x][y][s]`：时刻 t、在 (x,y)、卷轴状态 s 是否搜过，防止重复搜',
        'return f(0, 0, 0, 0)': lambda S, B, r: ('从时刻 0、起点 (0,0)、没用过卷轴出发' if r is None else f'整个搜索的结果：`{r}`'),
        'x < 0 or x >= n': lambda S, B, r: (
            f'`({S.x},{S.y})` 出界 → 不行' if not (0 <= S.x < S.n and 0 <= S.y < S.m)
            else f'`t + 到出口的最短距离 = {S.t + S.n - 1 - S.x + S.m - 1 - S.y} >= k = {S.k}`：时间来不及 → 剪枝' if S.t + S.n - 1 - S.x + S.m - 1 - S.y >= S.k
            else f'这个状态 `vis[{S.t}][{S.x}][{S.y}][{S.s}]` 搜过了 → 不用再搜' if S.vis[S.t][S.x][S.y][S.s]
            else f'状态 `(t={S.t}, x={S.x}, y={S.y}, s={S.s})` 合法，继续'),
        'x == n - 1 and y == m - 1': lambda S, B, r: ('到达出口 `(n-1, m-1)` → 成功' if S.x == S.n - 1 and S.y == S.m - 1 else '还没到出口'),
        'vis[t][x][y][s] = True': '标记这个状态搜过',
        's >> 1 == 1:': lambda S, B, r: ('`s >> 1 == 1`：正站在永久消除的位置上 → 这里永远是空地，可以一直待着，或者走出去' if S.s >> 1 == 1 else '`s >> 1 != 1`：不在永久消除位置，继续正常走'),
        'f(t + 1, x + dx, y + dy, s ^ 6)': '从永久位置走向 `({B.x+B.dx},{B.y+B.dy})`，`s ^ 6` 变成「已使用永久消除术」，时间 +1',
        'return f(t + 1, x, y, s)': lambda S, B, r: ('原地停留一个时刻，时间 `t + 1`' if r is None else f'原地停留分支返回 `{r}`'),
        'g[t][x][y] == \'#\' and f(t, x, y, s | 2)': lambda S, B, r: (
            '当前格是陷阱且没用过永久消除术 → 试试永久消除术：`s | 2`，时间不动' if B.g[B.t][B.x][B.y] == '#' and B.s >> 1 == 0
            else '当前格是空地，不需要永久消除术'),
        'if g[t][x][y] == \'#\':': lambda S, B, r: (
            f'`g[{S.t}][{S.x}][{S.y}] = #` 是陷阱：永久术那条路走不通，只能用临时消除术' if S.g[S.t][S.x][S.y] == '#'
            else f'`g[{S.t}][{S.x}][{S.y}] = .` 空地，不用任何卷轴'),
        'if s & 1 == 1': lambda S, B, r: ('临时消除术已经用过了，没法再过陷阱 → 返回 False' if S.s & 1 == 1 else '临时消除术还没用 → 可以用'),
        's |= 1': '用掉临时消除术：`s = {s}`',
        'f(t + 1, x + dx, y + dy, s):': '走到邻居 `({B.x+B.dx},{B.y+B.dy})`，时间 `{B.t} + 1`',
        'return True': '找到出口，一路返回 True',
        'return False': '这个状态走不通，返回 False 回溯',
    },
    max_steps=100,
    cards=dict(
        one_liner='用位掩码记「两张卷轴」状态，永久卷轴当作原地挂机',
        complexity='时间 `O(k·n·m·6)`，空间 `O(k·n·m·6)`',
        problem=['`maze[t]` 是第 t 时刻的迷宫，`.` 空地，`#` 陷阱，出口在 `(n-1,m-1)`',
                 '每步可上下左右走或停留；有一张临时消除术（只管下一时刻）和一张永久消除术',
                 '问能否在时间结束前不经过陷阱到达出口',
                 '本视频：`[[".#."],[".#."],[".#."]]` → `True`'],
        quote='s 的最低位：是否使用了临时消除术；s 的其余位：0-未使用永久消除术，1-当前正位于永久消除的位置，2-已使用永久消除术',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['状态 `(t, x, y, s)` 做记忆化 DFS，`s` 记两张卷轴的用法',
              '永久消除术把该格永远变空地；把它当成可以「原地一直待着」的状态 `s>>1==1`',
              '遇到陷阱：先试永久消除术（时间不动），再用临时消除术',
              '`t + 到出口的最短距离 >= k` 直接剪枝'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间、空间 `O(k·n·m·6)`',
                 '易错：永久消除后离开该格要 `s ^ 6`，把「位于」变为「已使用」',
                 '易错：临时消除术只管一个时刻，所以 `s |= 1` 后只传给下一层',
                 '关键技巧：永久卷轴不必记位置，只需「回到该格」可用原地等待代替'],
    ),
)
