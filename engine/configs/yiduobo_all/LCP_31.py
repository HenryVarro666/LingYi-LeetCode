MAZE = [['.#.'], ['.#.'], ['.#.']]


def _vcells(S):
    if 'f' not in S:
        return None
    F = S['f']
    t, m, n = len(F), len(F[0]), len(F[0][0])
    return [[''.join(str(s) for s in range(4) if any(F[tt][i][j][s] is False for tt in range(t))) for j in range(n)] for i in range(m)]


CONFIG = dict(
    num='LCP 31', title='变换的迷宫', difficulty='Hard', category='网格图',
    author='yiduobo', technique='记忆化搜索 · 卷轴二进制状态 + 永久卷轴挂机',
    tags=['灵神题单', '综合应用'],
    code='''
class Solution(object):
    def escapeMaze(self, maze):

        t = len(maze)
        m = len(maze[0])
        n = len(maze[0][0])
        
        f = [[[[None] * 4 for k in range(n)] for j in range(m)] for i in range(t)]

        dx = [1, 0, -1, 0, 0]
        dy = [0, 1, 0, -1, 0]

        def dfs(nowt, nowx, nowy, nows, f):
            if f[nowt][nowx][nowy][nows] is None:
                if nowx == m - 1 and nowy == n - 1:
                    return True

                f[nowt][nowx][nowy][nows] = False

                if nowt == t - 1:
                    return False
                
                
                for index in range(5):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n:
                        if maze[nowt + 1][x][y] == '.':
                            if dfs(nowt + 1, x, y, nows, f):
                                return True
                        else:
                            if nows == 0 or nows == 2:
                                if dfs(nowt + 1, x, y, nows + 1, f):
                                    return True
                
                            if nows < 2:
                                for nextt in range(nowt + 1, t):
                                    if dfs(nextt, x, y, nows + 2, f):
                                        return True
            
            return False
        
        

        return dfs(0, 0, 0, 0, f)
''',
    call=f'Solution().escapeMaze({MAZE})',
    expect=True,
    views=[
        dict(type='grid', var=lambda S: list(S['maze'][S['nowt']]) if 'nowt' in S else None,
             label='maze[nowt]（红 = 陷阱，蓝框 = 当前位置，粉框 = 想去的格子）', cell=96, h=230,
             cursors=[('nowx', 'nowy', 'blue'), ('x if _line in (24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34) else None', 'y', 'pink')],
             color=lambda S, i, j, v: 'red' if v == '#' else None),
        dict(type='grid', var=_vcells, label='f：各位置已搜过（False）的卷轴状态 nows（跨所有时刻合并）', cell=96, h=180),
        dict(type='text', fn=lambda S: (f"`nows = {S['nows']}`：二进制 `{S['nows']:02b}`，临时卷轴 ==" + ('已用' if S['nows'] & 1 else '未用') + "==，永久卷轴 ==" + ('已用' if S['nows'] & 2 else '未用') + '==') if 'nows' in S else '', size=24, h=70),
        dict(type='calls', h=250, hide=('f',)),
    ],
    watch=['nowt', 'nowx', 'nowy', ('nows', 'nows', 'yellow')],
    skip=['dx = [', 'dy = [', 'x = nowx + dx', 'm = len', 'n = len'],
    max_steps=140,
    captions={
        't = len(maze)': '`t = {t}`：迷宫一共 {t} 个时刻；`m × n` = `{m} × {n}`（行 × 列）',
        'f = [[[[None]': '`f[时刻][x][y][状态]`：None = 没搜过，False = 搜过（走不通）；状态 `nows` 是两位二进制',
        'return dfs(0, 0, 0, 0, f)': lambda S, B, r: ('从时刻 0、起点 (0,0)、两张卷轴都没用出发' if r is None else f'搜索结果：`{r}`'),
        'f[nowt][nowx][nowy][nows] is None': lambda S, B, r: (
            f'状态 `(t={S.nowt}, ({S.nowx},{S.nowy}), nows={S.nows})` 没搜过 → 继续' if S.f[S.nowt][S.nowx][S.nowy][S.nows] is None
            else f'状态 `(t={S.nowt}, ({S.nowx},{S.nowy}), nows={S.nows})` 已经搜过 → 直接返回 False'),
        'nowx == m - 1 and nowy == n - 1': lambda S, B, r: ('走到右下角出口 → 返回 True' if S.nowx == S.m - 1 and S.nowy == S.n - 1 else '还没到出口'),
        'f[nowt][nowx][nowy][nows] = False': '先标记「搜过」（若能成功会一路返回 True）',
        'nowt == t - 1': lambda S, B, r: ('最后一个时刻了还没到出口 → 返回 False' if S.nowt == S.t - 1 else f'`nowt = {S.nowt}`，时间还没用完，继续行动'),
        'for index in range(5)': '方向 `{index}`：下、右、上、左、原地挂机，共 5 个选择',
        'y = nowy + dy': '想去 `({x},{y})`',
        'x >= 0 and x < m': lambda S, B, r: (f'`({S.x},{S.y})` 在迷宫内' if 0 <= S.x < S.m and 0 <= S.y < S.n else f'`({S.x},{S.y})` 出界，换下一个选择'),
        "maze[nowt + 1][x][y] == '.'": lambda S, B, r: (f'下一时刻 `maze[{S.nowt+1}]` 里 `({S.x},{S.y})` 是空地 → 直接走' if S.maze[S.nowt + 1][S.x][S.y] == '.' else f'下一时刻 `({S.x},{S.y})` 是陷阱 → 需要卷轴'),
        'nows == 0 or nows == 2': lambda S, B, r: ('临时卷轴还没用过（`nows` 是 0 或 2）→ 可以用临时卷轴' if B.nows in (0, 2) else '临时卷轴已经用过 → 不能再用'),
        'dfs(nowt + 1, x, y, nows, f)': '空地直接走：时间 +1，状态不变',
        'dfs(nowt + 1, x, y, nows + 1, f)': '用临时卷轴：`nows + 1`，只管这一时刻，时间 +1',
        'nows < 2': '永久卷轴还没用过 → 可以用永久卷轴',
        'dfs(nextt, x, y, nows + 2, f)': '用永久卷轴：`nows + 2`，并枚举到达时刻 `nextt`（在那个格子挂机等待）',
        'return True': '一路返回 True：找到了出路',
        'return False': '这个状态走不通 → 返回 False',
    },
    cards=dict(
        one_liner='记忆化搜索，永久卷轴等价于「在那个格子挂机」',
        complexity='时间 `O(t·m·n·4·t)`，空间 `O(t·m·n)`',
        problem=['`maze[t]` 是第 t 时刻的迷宫，`.` 空地，`#` 陷阱，出口在右下角',
                 '每个时刻可上下左右走或原地停留；有一张临时卷轴、一张永久卷轴',
                 '问能否在时间结束前不踩陷阱到达出口',
                 '本视频：`[[".#."],[".#."],[".#."]]` → `True`'],
        quote='使用永久卷轴相当于提供了一种待在(cx, cy)一直挂机的选项，这样一来就没有必要在状态中储存(cx, cy)了，而是在使用永久卷轴的这一回合处理掉后续一直待在(cx, cy)挂机的情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想最直观的状态 `f[t][x][y][state][cx][cy]`，太大',
              '永久卷轴的作用只是「以后回到 (cx,cy) 也安全」，而没有收集道具的需求',
              '回到那里的过程可以改成一直待在那里挂机，所以不用记 (cx,cy)',
              '状态只剩两位二进制：低位临时卷轴，高位永久卷轴'],
        summary=['记忆化搜索，状态 `t·m·n·4`',
                 '用永久卷轴时要枚举 `nextt`：站在该格挂机到哪个时刻再出发',
                 '易错：临时卷轴只管一个时刻，所以只让 `nows + 1` 传到下一层',
                 '原文为 Python 2 风格，代码无需改动（已是 Python 3 可运行）'],
    ),
)
