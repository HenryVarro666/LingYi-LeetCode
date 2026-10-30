ROOM = [[1, 1], [1, 0]]
R0, C0 = 0, 0
OPEN = sorted((r, c) for r in range(2) for c in range(2) if ROOM[r][c] == 1)

SETUP = f'''
class Robot:
    # 题目给的机器人接口：只能 move / turnLeft / turnRight / clean，看不到地图
    def __init__(self, room, r, c):
        self.room, self.r, self.c, self.d = room, r, c, 0    # d: 0 上 1 右 2 下 3 左
        self.cleaned = set()
    def move(self):
        dr, dc = [(-1, 0), (0, 1), (1, 0), (0, -1)][self.d]
        r, c = self.r + dr, self.c + dc
        if 0 <= r < len(self.room) and 0 <= c < len(self.room[0]) and self.room[r][c] == 1:
            self.r, self.c = r, c
            return True
        return False
    def turnLeft(self):
        self.d = (self.d - 3) % 4
    def turnRight(self):
        self.d = (self.d + 1) % 4
    def clean(self):
        self.cleaned.add((self.r, self.c))

robot = Robot({ROOM}, {R0}, {C0})
'''

DIRS_TXT = ['上', '右', '下', '左']


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    rb = S.get('robot')
    if rb is None:
        return
    vis = S.get('vis') or set()
    nr, nc = len(ROOM), len(ROOM[0])
    cell = min(150, (x1 - x0 - 60) / nc, (y1 - y0 - 150) / nr)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * nc) / 2
    sy = y0 + 70
    cv.text((x0 + 18, y0 + 4), '房间（算法看不见：绿 = 已清扫，红叉 = 探过是墙，青点 = vis 里的相对坐标）', 22, T['muted'], bold=True)
    probed = {(R0 + a, C0 + b) for a, b in vis}
    for r in range(nr):
        for c in range(nc):
            X, Y = sx + c * cell, sy + r * cell
            if ROOM[r][c] == 0:
                cv.rect((X + 4, Y + 4, X + cell - 4, Y + cell - 4), fill=(52, 58, 68), r=10)
                if (r, c) in probed:
                    cv.text((X + cell / 2, Y + cell / 2), '×', 54, T['red'], anchor='mm', bold=True)
                continue
            done = (r, c) in rb.cleaned
            cv.rect((X + 4, Y + 4, X + cell - 4, Y + cell - 4), fill=T['green'] if done else T['panel2'], r=10,
                    outline=T['border'])
            if (r, c) in probed and not done:
                cv.text((X + cell - 14, Y + 12), '·', 40, T['cyan'], anchor='ra', bold=True)
            cv.text((X + 12, Y + cell - 10), f'({r - R0},{c - C0})', 18, T['bg'] if done else T['dim'], anchor='lb', mono=True)
    # 机器人（三角形，尖端朝向）
    cx, cy = sx + rb.c * cell + cell / 2, sy + rb.r * cell + cell / 2
    s = cell * 0.30
    ux, uy = [(0, -1), (1, 0), (0, 1), (-1, 0)][rb.d]
    px, py = -uy, ux
    cv.poly([(cx + ux * s * 1.2, cy + uy * s * 1.2), (cx - ux * s * 0.8 + px * s, cy - uy * s * 0.8 + py * s),
             (cx - ux * s * 0.8 - px * s, cy - uy * s * 0.8 - py * s)], T['orange'])
    cv.text((x0 + 18, sy + nr * cell + 14),
            f"机器人：相对坐标 ({rb.r - R0},{rb.c - C0})，朝{DIRS_TXT[rb.d]}；已清扫 {len(rb.cleaned)} 格；vis 里 {len(vis)} 个坐标",
            26, T['text'], bold=True)


def _moved(S, B):
    return (S.robot.r, S.robot.c) != (B.robot.r, B.robot.c)


CONFIG = dict(
    num=489, title='扫地机器人', difficulty='Hard', category='网格图',
    author='yiduobo', technique='DFS 探索未知地图 · 相对坐标 + 手动回溯',
    tags=['灵神题单·网格图', '灵神题单·贪心与思维'],
    setup=SETUP,
    code='''
#class Robot(object):
#
#
#

class Solution(object):
    def cleanRoom(self, robot):

        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]
        vis = set([(0, 0)])
        robot.clean()

        def dfs(nowx, nowy, nowd):
            for index in range(4):
                d = (nowd + index) % 4
                x = nowx + dx[d]
                y = nowy + dy[d]
                if index > 0:
                    robot.turnRight()
                if (x, y) not in vis:
                    vis.add((x, y))
                    if robot.move():
                        robot.clean()
                        dfs(x, y, d)
                        robot.turnRight()
                        robot.turnRight()
                        robot.move()                            
                        robot.turnRight()
                        robot.turnRight()
            robot.turnRight()

        dfs(0, 0, 0)
''',
    call='Solution().cleanRoom(robot)\nsorted(robot.cleaned)',
    expect=OPEN,
    skip=['dx = [', 'dy = [', 'y = nowy', 'for index in range(4)', 'd = (nowd', 'x = nowx', 'vis.add', 'if index > 0'],
    max_steps=100,
    views=[dict(type='custom', draw=_draw, h=380),
           dict(type='calls', h=210)],
    watch=[('(nowx, nowy)', '(nowx, nowy) if "nowx" in dir() else None', 'blue'),
           ('index', 'index if "index" in dir() else None', 'pink'), ('d', 'd if "d" in dir() else None', 'cyan')],
    captions={
        11: '`vis` 记录探过的==相对坐标==：起点当作 `(0,0)`，朝上',
        12: '先清扫起点。机器人看不到地图，所以只能靠相对坐标记路',
        33: '从 `(0,0)`、朝向 `0`（上）开始 dfs',
        20: lambda S, B, r: f'`index = {S.index}`：机器人==右转一次==，朝{DIRS_TXT[S.robot.d]}，正对相对坐标 `({S.x},{S.y})`',
        21: lambda S, B, r: (f'`index = {B.index}`：朝{DIRS_TXT[B.d]}，目标 `({B.x},{B.y})` ==没探过== → 试着走'
                             if (B.x, B.y) not in B.vis else f'`index = {B.index}`：朝{DIRS_TXT[B.d]}，目标 `({B.x},{B.y})` 已在 `vis` → 跳过，不重复走'),
        23: lambda S, B, r: (f'`move()` ==成功==：前进到相对坐标 `({B.x},{B.y})`' if _moved(S, B)
                             else f'`move()` 失败：前面是墙。`({B.x},{B.y})` 已记入 `vis`，以后不再试'),
        24: '到了新格子，清扫它',
        25: '以新位置 `({x},{y})`、朝向 `{d}` ==递归探索==，等它回来再退回',
        26: '`dfs` 回来了：要退回 `({nowx},{nowy})`，先右转（共转两次才能掉头）',
        27: '第二次右转：现在==背对==刚才的来路',
        28: '`move()`：沿来路退一步，回到 `({nowx},{nowy})`',
        29: '再右转',
        30: '又右转：连转两次，朝向复原成进入这个方向时的样子',
        31: '四个方向转完后机器人共右转了 3 次，再右转一次 → ==朝向回正==，递归返回给上一层时方向不变',
    },
    cards=dict(
        one_liner='没有地图：靠相对坐标记路，走出去再手动走回来',
        complexity='时间 `O(格子数)`，空间 `O(格子数)`',
        problem=['房间里有墙，机器人只能 `move`、`turnRight`、`turnLeft`、`clean`，==看不到地图==',
                 '`move()` 撞墙返回 `False`；要把每个能到的格子都清扫一遍',
                 '本视频：2×2 房间（右下是墙），机器人起点在左上、朝上'],
        quote='本题没有给出地图，但是要求对地图进行一次遍历，那么最直观的做法就是dfs。不妨设机器人一开始位于坐标(0, 0），接下来根据机器人的行动计算当前的相对坐标。',
        quote_src='—— yiduobo 题解原文',
        idea=['起点当作 `(0,0)`、朝上，用 `vis` 集合记录相对坐标去重',
              '顺时针 `dx、dy` 枚举四个方向：右转 `index` 次后朝向 `d`，能走就 `move`',
              '机器人不能“返回”：dfs 回来后要==转 180° → 前进一步 → 再转 180°==，退回原格并恢复朝向'],
        summary=['时间 `O(N)`、空间 `O(N)`，`N` 为可达格子数（每个坐标只试一次）',
                 '`vis.add` 要在 `move()` 之前：撞墙的坐标也要记，否则会反复撞',
                 '易错：回溯要先转两次、退一步、再转两次；四个方向枚举完还要再右转一次回正',
                 '题目的 `Robot` 接口在 `setup` 里用一个小房间模拟；原文代码未改，开头几行是 LeetCode 的注释模板'],
    ),
)
