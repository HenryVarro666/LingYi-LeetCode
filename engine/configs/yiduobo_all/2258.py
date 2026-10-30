GRID = [[0, 0, 1], [0, 2, 2], [0, 0, 0]]


def _gcolor(S, i, j, v):
    if v == 2:
        return 'purple'
    k = i * len(GRID[0]) + j
    fu, pu = S.get('fire_used'), S.get('person_used')
    if fu is not None and k in fu:
        return 'orange'
    if pu is not None and k in pu:
        return 'orange' if not S.get('fire_pos') else 'blue'
    if v == 1:
        return 'orange'
    return None


def _purpose(S):
    if 'fire_pos' not in S:
        return '先判断「立刻出发」能不能逃出；再让火自己走算上界；最后二分等待时间'
    if len(S['fire_pos']) == 0:
        return '这次 BFS 只让火自己走（`person_pos` 传的是火源），用来算火到安全屋的时间'
    return f'这次 BFS：火先烧 `wait_time = {S["wait_time"]}` 分钟，然后每分钟「火走一圈、人走一圈」'


CONFIG = dict(
    num=2258, title='逃离火灾', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='BFS 判可行 + 二分等待时间',
    tags=['网格图', '难度分 2347'],
    code='''
class Solution(object):
    def maximumMinutes(self, grid):
        m = len(grid)
        n = len(grid[0])

        fire_list = []

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    fire_list.append([i, j])
        
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        def bfs(person_pos, fire_pos, wait_time):
            fire_q = fire_pos[:]
            fire_l = 0
            fire_r = len(fire_q)

            fire_used = set()
            for x, y in fire_pos:
                fire_used.add(x * n + y)

            for _ in range(wait_time):
                for nowx, nowy in fire_q[fire_l : fire_r]:
                    for index in range(4):
                        x = nowx + dx[index]
                        y = nowy + dy[index]
                        if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 0 and x * n + y not in fire_used:
                            fire_q.append([x, y])
                            fire_used.add(x * n + y)
            
                fire_l, fire_r = fire_r, len(fire_q)

            if m * n - 1 in fire_used:
                return -1

            person_q = person_pos[:]
            person_l = 0
            person_r = len(person_q)

            person_used = set()
            for x, y in person_pos:
                person_used.add(x * n + y)
            
            step = 0
            while person_l < person_r:
                step += 1
                for nowx, nowy in fire_q[fire_l : fire_r]:
                    for index in range(4):
                        x = nowx + dx[index]
                        y = nowy + dy[index]
                        if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 0 and x * n + y not in fire_used:
                            fire_q.append([x, y])
                            fire_used.add(x * n + y)
                
                fire_l, fire_r = fire_r, len(fire_q)

                for nowx, nowy in person_q[person_l : person_r]:
                    for index in range(4):
                        x = nowx + dx[index]
                        y = nowy + dy[index]
                        if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 0:
                            next_key = x * n + y
                            if next_key == m * n - 1:
                                return step
                            
                            if next_key not in person_used and next_key not in fire_used:
                                person_q.append([x, y])
                                person_used.add(next_key)
                
                person_l, person_r = person_r, len(person_q)

                if m * n - 1 in fire_used:
                    break

            return -1

        g = grid[:]
        if bfs([[0, 0]], fire_list, 0) == -1:
            return -1
        
        fire_time = bfs(fire_list, [], 0)

        if fire_time == -1:
            return 10 ** 9
        
        l = 0
        r = fire_time
        while l < r:
            mid = (l + r + 1) >> 1
            if bfs([[0, 0]], fire_list, mid) != -1:
                l = mid
            else:
                r = mid - 1
        
        return l
''',
    call=f'Solution().maximumMinutes({GRID})',
    expect=1,
    skip=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 68, 69, 70, 71, 72, 73, 74, 75, 77, 79, 80, 82, 83, 85, 87, 88, 95, 97],
    views=[
        dict(type='grid', var='grid', label='grid（橙 = 火，蓝 = 人走过，紫 = 墙）', cell=100, h=270,
             color=_gcolor, values=False),
        dict(type='text', fn=_purpose, size=24, h=100),
        dict(type='array', var=lambda S: list(range(S['fire_time'] + 1)) if S.get('fire_time', -1) >= 0 else None,
             label='二分「原地等待的分钟数」：窗口 = [l, r]，粉箭头 = mid', pointers={'mid': 'pink'}, window=('l', 'r'),
             cell=80, h=190),
    ],
    watch=[('wait_time', 'wait_time', 'orange'), ('step', 'step', 'blue'), ('l', 'l', 'green'), ('r', 'r', 'green'), ('mid', 'mid', 'pink')],
    captions={
        36: lambda S, B, r: ('这次不等待，火自己直接开始扩散' if len(S['fire_pos']) == 0 else
                             f'火先烧 {S["wait_time"]} 分钟（人原地等待）。安全屋 `{S["m"] * S["n"] - 1}` 着火了吗？'
                             + ('==着火了，返回 -1==' if S['m'] * S['n'] - 1 in S['fire_used'] else '没有，人可以出发')),
        49: lambda S, B, r: (f'第 `{S["step"]}` 分钟：火向外扩散一圈' if len(S['fire_pos']) == 0 else
                             f'第 `{S["step"]}` 分钟：==火先走一圈==，再轮到人走一圈（样例 2 说明火要先走）'),
        76: '火先烧到了安全屋 → 跳出循环，这个等待时间不行',
        67: lambda S, B, r: (f'火单独走到安全屋用了 =={S["step"]}== 分钟 → 这就是二分的上界' if len(S['fire_pos']) == 0
                             else f'人在第 =={S["step"]}== 分钟走到安全屋；火即使同时到也算成功，所以先判到达、再判着火'),
        78: lambda S, B, r: ('起点 (0,0) 已经被火烧到，人一步也走不了 → 这个等待时间不可行，返回 -1' if 0 in S['fire_used']
                             else '人被火封死，或火先到安全屋 → 这个等待时间不可行，返回 -1'),
        86: lambda S, B, r: ('火走不到安全屋 → 人想等多久都行，返回 `10^9`' if S['fire_time'] == -1
                             else f'火最终能到安全屋（需要 {S["fire_time"]} 分钟），所以答案有上限'),
        89: '二分「原地等待多久」：下界 `l = 0`（第一次 BFS 已证明立刻出发可行）',
        90: '上界 `r = fire_time` = {r}：等得比火到安全屋还久，肯定来不及',
        92: lambda S, B, r: f'取偏大的中点 `mid = ({S["l"]} + {S["r"]} + 1) >> 1` = =={S["mid"]}==：让火先烧 {S["mid"]} 分钟，试一试',
        94: '等 `{mid}` 分钟还能逃出去 → 等待时间越短越安全，答案至少是 {mid}：`l = {l}`',
        96: '等 `{mid}` 分钟逃不出去 → 更久也不行：`r = mid - 1` = {r}',
        98: '`l = r` 时二分结束，最多能等 =={l}== 分钟',
    },
    max_steps=120,
    cards=dict(
        one_liner='二分原地等待的时间，每次用「火先走、人后走」的 BFS 判断能否逃出',
        complexity='时间 `O(mn log mn)`，空间 `O(mn)`',
        problem=['`grid`：0 草地，1 火，2 墙；人在 (0,0)，要去 (m-1,n-1) 的安全屋',
                 '人每分钟走一步，之后火扩散一圈；问人原地最多能等多少分钟再出发',
                 '到不了返回 -1；怎么等都能到返回 `10^9`；和火==同时到安全屋==也算成功',
                 '示例：`[[0,0,1],[0,2,2],[0,0,0]]` → `1`'],
        quote='一个直观的想法是，耽误的越久，出事的概率就越大，因此可以二分这个耽误的时间mid。二分的初始下界自然是0，而上界就是第二步中计算的火走到安全屋的时间。',
        quote_src='—— yiduobo 题解原文',
        idea=['先不等待 BFS 一次：到不了安全屋 → `-1`',
              '再让火自己 BFS：火到不了安全屋 → 人想等多久都行，`10^9`；到得了就得到上界',
              '最后二分等待时间：火先走 `mid` 分钟，再按「火先走、人后走」判断人能否到达'],
        summary=['时间 `O(mn log mn)`：每次 BFS `O(mn)`，二分约 `log(mn)` 次',
                 '易错：每分钟火先走、人后走；人不能进火烧过的格，火可以进人走过的格',
                 '易错：到达安全屋时先返回再判着火，同时到达算成功',
                 '易错：上界是火到安全屋的时间，不是 `mn`；等待 0 分钟也不行就直接 -1',
                 '原文已是 Python 3 可运行的写法，代码未改'],
    ),
)
