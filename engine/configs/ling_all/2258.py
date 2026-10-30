GRID = [[0, 0, 0, 0, 0], [0, 2, 0, 0, 0], [0, 1, 2, 0, 2], [0, 2, 0, 0, 0]]


def _gcolor(S, i, j, v):
    if v == 1:
        return 'orange'
    if v == 2:
        return 'purple'
    return None


def _tcolor(S, i, j, v):
    if GRID[i][j] == 2:
        return 'purple'
    if v == 0:
        return 'blue'
    if S.get('x') == i and S.get('y') == j:
        return 'green'
    if v > 0:
        return 'cyan'
    return None


def _txt(S):
    if 'd' in S:
        return (f'人到安全屋 `{S["man_to_house_time"]}` 分钟，火到 `{S["fire_to_house_time"]}` 分钟 → 可等 `d = {S["d"]}` 分钟；'
                f'左 `{S["m1"]}/{S["f1"]}`，上 `{S["m2"]}/{S["f2"]}`（人/火到达时间）')
    if 'fire_to_house_time' in S:
        return f'火到安全屋要 `{S["fire_to_house_time"]}` 分钟，人要 `{S["man_to_house_time"]}` 分钟'
    if 'man_to_house_time' in S:
        return f'人从 (0,0) 到安全屋最快 `{S["man_to_house_time"]}` 分钟（`-1` 表示到不了）'
    return '先分别 BFS：人到每个格子的最短时间，火到每个格子的最短时间'


CONFIG = dict(
    num=2258, title='逃离火灾', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='两次 BFS + 直接计算',
    tags=['网格图', '难度分 2347'],
    code='''
class Solution:
    def maximumMinutes(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])

        # 返回三个数，分别表示到达安全屋/安全屋左边/安全屋上边的最短时间
        def bfs(q: List[Tuple[int, int]]) -> (int, int, int):
            time = [[-1] * n for _ in range(m)]  # -1 表示未访问
            for i, j in q:
                time[i][j] = 0
            t = 1
            while q:  # 每次循环向外扩展一圈
                tmp = q
                q = []
                for i, j in tmp:
                    for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):  # 上下左右
                        if 0 <= x < m and 0 <= y < n and grid[x][y] == 0 and time[x][y] < 0:
                            time[x][y] = t
                            q.append((x, y))
                t += 1
            return time[-1][-1], time[-1][-2], time[-2][-1]

        man_to_house_time, m1, m2 = bfs([(0, 0)])
        if man_to_house_time < 0:  # 人无法到安全屋
            return -1

        fire_pos = [(i, j) for i, row in enumerate(grid) for j, x in enumerate(row) if x == 1]
        fire_to_house_time, f1, f2 = bfs(fire_pos)
        if fire_to_house_time < 0:  # 火无法到安全屋
            return 10 ** 9

        d = fire_to_house_time - man_to_house_time
        if d < 0:  # 火比人先到安全屋
            return -1

        if m1 != -1 and m1 + d < f1 or \\
           m2 != -1 and m2 + d < f2:  # 安全屋左边或上边的其中一个格子人比火先到
            return d  # 图中第一种情况
        return d - 1  # 图中第二种情况
''',
    call=f'Solution().maximumMinutes({GRID})',
    expect=2,
    skip=['m, n = len', 'for i, j in tmp', 'for x, y in', 'if 0 <= x < m', 'tmp = q', 'q = []', 'q.append', 't += 1',
          't = 1', 'while q', 'for i, j in q', 'fire_pos = [', 'return time[-1]', 'm2 != -1 and m2 + d < f2'],
    views=[
        dict(type='grid', var='grid', label='grid（橙 = 火，紫 = 墙；人在左上，安全屋在右下）', cell=96, h=250,
             color=_gcolor, values=False),
        dict(type='grid', var='time', label='time：当前这次 BFS 的到达时间（-1 = 没到过；蓝 = 起点，绿 = 刚扩到）', cell=96, h=250,
             color=_tcolor),
        dict(type='text', fn=_txt, size=24, h=120),
    ],
    watch=[('t', 't', 'blue'), ('man', 'man_to_house_time', 'blue'), ('fire', 'fire_to_house_time', 'orange'), ('d', 'd', 'green')],
    captions={
        'time = [[-1]': '新建 `time` 表，`-1` 表示还没到过；BFS 一圈一圈向外扩，每圈 +1 分钟',
        'time[i][j] = 0': '起点 `({i},{j})` 的时间记为 0（人从 (0,0) 出发，火从所有着火格同时出发）',
        'time[x][y] = t': lambda S, B, r: (f'火扩到 `({S["x"]},{S["y"]})`（草地、没烧到过）→ 火的最短到达时间 =={S["t"]}==' if 'man_to_house_time' in S
                                           else f'人走到 `({S["x"]},{S["y"]})`（草地、没到过）→ 人的最短到达时间 =={S["t"]}==（BFS 先到的一定最短）'),
        'man_to_house_time, m1, m2': ('人的 BFS 结束：到安全屋 `{man_to_house_time}`，到安全屋左边 `{m1}`，到上边 `{m2}` 分钟'),
        'if man_to_house_time < 0': lambda S, B, r: ('人到不了安全屋 → 怎么等都没用，返回 -1' if S['man_to_house_time'] < 0
                                                     else f'人能到安全屋（{S["man_to_house_time"]} 分钟），继续看火'),
        'fire_to_house_time, f1, f2': '火的 BFS 结束：到安全屋 `{fire_to_house_time}`，到左边 `{f1}`，到上边 `{f2}` 分钟',
        'if fire_to_house_time < 0': lambda S, B, r: ('火到不了安全屋、人能到 → 人和火被隔开，可以永远等 → 返回 `10^9`'
                                                      if S['fire_to_house_time'] < 0 else f'火 {S["fire_to_house_time"]} 分钟能到安全屋，要算最多能等多久'),
        'd = fire_to_house_time': '`d = {fire_to_house_time} - {man_to_house_time}` = =={d}==：人最多可以先等 d 分钟，让自己和火==同时==到安全屋',
        'if d < 0': lambda S, B, r: ('`d < 0`：火比人先到安全屋 → 返回 -1' if S['d'] < 0 else f'`d = {S["d"]} ≥ 0`：人不会比火晚到，可以等'),
        'm1 != -1 and m1 + d < f1': ('==关键细节==：人和火可以同时到安全屋，但不能同时到它旁边的格子（那样火会跟着烧到人）。'
                                     '检查左边：`m1 + d = {m1 + d if m1 != -1 else \'无路\'}` vs 火 `f1 = {f1}`；上边：`m2 = {m2}`（-1 表示是墙，走不过来）'),
        'return d  #': '左边或上边至少有一个格子人严格先到 → 能等满 `d` 分钟，返回 `{d}`',
        'return d - 1': ('两个相邻格子人都没有严格先到（左边 `{m1}+{d}` = {m1 + d} 不小于火的 `{f1}`，上边是墙）→ 少等 1 分钟，返回 `d - 1` = =={d - 1}=='),
    },
    cards=dict(
        one_liner='两次 BFS 求最短时间，再比较人和火到安全屋的时间差',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`grid`：0 草地，1 火，2 墙；人在 (0,0)，要去 (m-1,n-1) 的安全屋',
                 '人每分钟走一步，之后火扩散一圈；问人在原地最多能等多少分钟再出发',
                 '到不了返回 -1；怎么等都能到返回 `10^9`；人和火==同时到安全屋==不算被烧',
                 '示例：`4×5` 的网格（火在左下，安全屋在右下），答案 `2`'],
        quote='设人在 t1 分钟到达 C，火在 t2 分钟到达 C。如果人比火先到达 C，即 t1 < t2，那么不会出现中途火把人烧到的情况。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['人比火先到某格，路上就不会被烧到 → 人可以多等 `t2 - t1 - 1` 分钟',
              '安全屋是特例：同时到也算安全，所以先算 `d = 火时间 - 人时间`',
              '但人到安全屋的上一格（左边或上边）必须==严格==先于火，否则只能等 `d - 1`'],
        summary=['时间 `O(mn)`：人和火各做一次 BFS，没有二分',
                 '易错：只有安全屋允许同时到达，它的左边和上边不允许',
                 '易错：BFS 要三个值（安全屋、左边、上边），邻格是墙时为 -1',
                 '方法一是二分答案：每次先让火扩散 t 分钟，再模拟人逃跑，`O(mn log mn)`，上界取 `mn`'],
    ),
)
