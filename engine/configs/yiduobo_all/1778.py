SETUP = '''
HID = [[1, 1, 1, 0],
       [1, 0, 1, 1],
       [1, 1, 0, 2]]   # 0 墙，1 空地，2 终点；机器人从 (1, 0) 出发（对它自己是未知的）


class GridMaster(object):
    def __init__(self):
        self.r, self.c = 1, 0

    def canMove(self, d):
        dr, dc = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}[d]
        r, c = self.r + dr, self.c + dc
        return 0 <= r < 3 and 0 <= c < 4 and HID[r][c] != 0

    def move(self, d):
        dr, dc = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}[d]
        self.r += dr
        self.c += dc

    def isTarget(self):
        return HID[self.r][self.c] == 2
'''
TGT = (1, 3)          # 终点相对起点的坐标
HID_T = (2, 3)        # 终点在隐藏网格里的位置：只有被探到后才在画面上显示 T
ROW0, COL0 = 1, 0     # 起点在隐藏网格里的位置，仅用于把相对坐标摆进 3x4 的画面


def _known(S):
    s = set()
    for k in ('can_reach',):
        if S.get(k) is not None:
            s |= set(S[k])
    q = S.get('q')
    if q:
        s |= {tuple(p) for p in q}
    s.add((0, 0))
    return s


def _mat(S):
    if 'can_reach' not in S:
        return None
    known = _known(S)
    out = []
    for r in range(3):
        row = []
        for c in range(4):
            p = (r - ROW0, c - COL0)
            if p == (0, 0):
                row.append('S')
            elif p in known:
                row.append('T' if HID_T == (r, c) else '·')
            else:
                row.append('?')
        out.append(row)
    return out


def _color(S, i, j, v):
    p = (i - ROW0, j - COL0)
    q = S.get('q')
    if q is not None and S.get('head') is not None and [p[0], p[1]] in q:
        return 'green'
    if v == 'T':
        return 'orange'
    if v == '?':
        return None
    return 'purple' if v == '·' else 'cyan'


def _cur(S):
    if 'nowx' not in S:
        return None
    return S['nowx'] + ROW0 if 'head' not in S else None


def _cury(S):
    return S['nowy'] + COL0 if 'nowx' in S and 'head' not in S else None


def _nb_dfs(S, B, r):
    d = S.do[S.index]
    if not S.master.canMove(d):
        return f'向 `{d}` 走：机器人说 canMove 为 False（墙或边界），不走'
    if (S.x, S.y) in S.can_reach:
        return f'向 `{d}` 走到 `({S.x},{S.y})`：能走但已经探过，不重复'
    return f'向 `{d}` 走到 `({S.x},{S.y})`：能走且没探过 → ==去探索=='


def _nb_bfs(S, B, r):
    if (S.x, S.y) in B.can_reach:
        return f'邻居 `({S.x},{S.y})` 是已探明的路且还没走到 → ==入队，下一层==（同时从 can_reach 删掉当作 visited）'
    return f'邻居 `({S.x},{S.y})` 不在 `can_reach` 里（墙、未知，或已经走到过），不入队'


CONFIG = dict(
    num=1778, title='未知网格中的最短路径', difficulty='Medium', category='网格图',
    author='yiduobo', technique='DFS 探图 + BFS 最短路',
    tags=['灵神题单'],
    setup=SETUP,
    code='''
#class GridMaster(object):
#
#
#

class Solution(object):
    def findShortestPath(self, master):

        can_reach = set()
        can_reach.add((0, 0))

        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]
        do = ['U', 'D', 'L', 'R']

        global tx, ty
        tx = ty = None

        def dfs(nowx, nowy):
            global tx, ty
            if master.isTarget():
                tx, ty = nowx, nowy

            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if master.canMove(do[index]) and (x, y) not in can_reach:
                    can_reach.add((x, y))
                    master.move(do[index])
                    dfs(x, y)
                    master.move(do[index ^ 1])
        
        dfs(0, 0)
        
        if tx is None:
            return -1
        
        q = [[0, 0]]
        head, tail = 0, 1
        res = 0
        while head < tail:
            res += 1
            for nowx, nowy in q[head : tail]:
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if (x, y) in can_reach:
                        can_reach.remove((x, y))
                        q.append([x, y])
            
            head, tail = tail, len(q)
            if (tx, ty) not in can_reach:
                break
        
        return res
''',
    call='Solution().findShortestPath(GridMaster())',
    expect=6,
    skip=['can_reach = set()', 'dx = [', 'dy = [', 'do = [', 'global tx', 'for index in range(4)', 'x = nowx', 'y = nowy',
          'can_reach.add((0, 0))', 'tx = ty = None', 'q.append([x, y])', 'can_reach.add((x, y))'],
    max_steps=60,
    views=[
        dict(type='grid', var=_mat, label='相对起点的地图（· = 已探明；T = 终点；蓝框 = 机器人；绿 = BFS 已到达）', cell=110, h=360,
             color=_color, cursors=[(_cur, _cury, 'blue')]),
        dict(type='array', var=lambda S: ([f'{a},{b}' for a, b in S['q']] if 'q' in S else None),
             label='q（BFS 队列，按层推进）', cell=80, h=150),
        dict(type='text', h=90, size=28,
             fn=lambda S: (f'机器人真实位置在 `({S["master"].r},{S["master"].c})`，程序只知道相对起点的坐标 `({S["nowx"]},{S["nowy"]})`'
                           if 'nowx' in S and 'head' not in S else
                           ('地图探完了：从 `(0, 0)` 开始 BFS，终点在 `(%s, %s)`' % (S.get('tx'), S.get('ty')) if 'q' in S
                            else '机器人什么都看不见，只能 `canMove` 试探、`move` 移动'))),
    ],
    watch=[('nowx', 'nowx', 'blue'), ('nowy', 'nowy', 'blue'), ('tx', 'tx', 'orange'), ('ty', 'ty', 'orange'),
           ('res', 'res', 'green')],
    captions={
        'dfs(0, 0)': '把起点记作 `(0, 0)`，开始 DFS 探索整张图',
        'if master.isTarget()': lambda S, B, r: (f'当前格 `({S.nowx},{S.nowy})` 就是终点 → ==记下 tx, ty=='
                                                  if S.master.isTarget() else f'`({S.nowx},{S.nowy})` 不是终点，继续探'),
        'tx, ty = nowx, nowy': '`tx, ty` 记下终点的相对坐标 `({nowx},{nowy})`',
        'if master.canMove': _nb_dfs,
        'master.move(do[index])': '机器人真的朝 `{do[index]}` 走一步，位置要和 `(x, y)` 同步',
        'dfs(x, y)': '进入 `({x},{y})`，继续向四个方向试探',
        'master.move(do[index ^ 1])': '这一格探完：朝反方向 `{do[index ^ 1]}` 走回来（`index ^ 1` 恰好是反方向），机器人回到 `({nowx},{nowy})`',
        'if tx is None': '`tx` 不是 None：DFS 途中遇到过终点，可以到达 → 继续求最短路',
        'q = [[0, 0]]': '地图已知。从起点 `(0, 0)` 做 BFS，队列初始只有起点',
        'head, tail = 0, 1': '`q[head:tail]` 是当前这一层的格子',
        'while head < tail': '开始新的一轮，`res` 就是起点到当前这一层的步数',
        'res += 1': '这一轮要走一步，`res = {res}`',
        'if (x, y) in can_reach': _nb_bfs,
        'can_reach.remove': '`({x},{y})` 从 `can_reach` 删掉，等于标记为 visited',
        'head, tail = tail': '本层处理完，下一层是 `q[{head}:{tail}]`，共 {tail - head} 个格子',
        'if (tx, ty) not in can_reach': lambda S, B, r: (
            f'终点 `{TGT}` 已被走到（已从 can_reach 删掉）→ 最短路就是 `res = {S.res}` 步，停止'
            if TGT not in S.can_reach else f'终点 `{TGT}` 还没走到，继续下一层'),
        'return res': '起点到终点的最短步数 `{res}`',
    },
    cards=dict(
        one_liner='先 DFS 把未知地图探完，再在已知地图上 BFS',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['隐藏的网格里有一个机器人，看不到地图和自己的位置',
                 '只能调用 `canMove(d)`、`move(d)`、`isTarget()`',
                 '求从起点走到终点的最少步数，到不了返回 `-1`',
                 '本视频：3×4 的隐藏网格，终点在右下角 → `6`'],
        quote='由于题目中的地图一开始是未知的，那么就必须想办法将整个地图探开，才有最短路径这一说。',
        quote_src='—— yiduobo 题解原文',
        idea=['设起点为 `(0, 0)`，DFS 的同时记录每个走到的相对坐标',
              '走过去要 `move`，探完要朝反方向走回来：`index ^ 1`',
              '图探完后，用 `can_reach` 当 visited 做 BFS，终点出队的层数就是答案'],
        summary=['时间 `O(mn)`，空间 `O(mn)`：每格 DFS 一次、BFS 一次',
                 '易错：DFS 回溯时机器人必须真的走回来，否则位置和坐标对不上',
                 '易错：没遇到终点要返回 `-1`，不能直接去 BFS',
                 '`tx, ty` 用 `global` 在嵌套函数里修改；原文代码是 Python 3 可运行的写法，未做修改',
                 '本题是交互题，视频里的 `GridMaster` 是按题意补的最小实现'],
    ),
)
