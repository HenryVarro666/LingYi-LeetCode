MAZE = [['+', '+', '+', '.', '+'],
        ['+', '.', '.', '.', '+'],
        ['+', '.', '+', '+', '+'],
        ['+', '+', '+', '+', '+']]
ENT = [1, 1]


def _dist():
    m, n = len(MAZE), len(MAZE[0])
    d = {tuple(ENT): 0}
    q = [tuple(ENT)]
    for i, j in q:
        for x, y in (i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j):
            if 0 <= x < m and 0 <= y < n and MAZE[x][y] == '.' and (x, y) not in d:
                d[(x, y)] = d[(i, j)] + 1
                q.append((x, y))
    return d


DIST = _dist()


def _show(S):
    g = S.get('maze')
    if g is None:
        return None
    return [[('起' if [i, j] == ENT else str(DIST.get((i, j), '?'))) if c is None else c
             for j, c in enumerate(row)] for i, row in enumerate(g)]


def _color(S, i, j, v):
    g = S.get('maze')
    if g is None:
        return None
    if g[i][j] is None:
        return 'green'
    if g[i][j] == '+':
        return None
    m, n = len(g), len(g[0])
    if i in (0, m - 1) or j in (0, n - 1):
        return 'orange'
    return None


def _nb(S, B, r):
    x, y, m, n = S.x, S.y, S.m, S.n
    if not (0 <= x < m and 0 <= y < n):
        return f'邻居 `({x},{y})` 出界 → 跳过'
    c = S.maze[x][y]
    if c == '+':
        return f'邻居 `({x},{y})` 是墙 → 跳过'
    if c is None:
        return f'邻居 `({x},{y})` 已被标记成 `None`（访问过）→ ==不重复入队=='
    return f'邻居 `({x},{y})` 是没走过的空格 `.` → 可以走'


def _edge(S, B, r):
    x, y = S.x, S.y
    if x == 0 or y == 0 or x == S.m - 1 or y == S.n - 1:
        return f'`({x},{y})` 在边界上 → ==它就是出口==，第一次碰到就是最近的'
    return f'`({x},{y})` 不在边界上，还不是出口'


CONFIG = dict(
    num=1926, title='迷宫中离入口最近的出口', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='网格图 BFS（双列表）',
    tags=['labuladong', '灵神题单·网格图', '难度分 1638'],
    code='''
class Solution:
    def nearestExit(self, maze: List[List[str]], entrance: List[int]) -> int:
        m, n = len(maze), len(maze[0])
        sx, sy = entrance  # 起点
        maze[sx][sy] = None  # 访问标记
        q = [(sx, sy)]

        ans = 1
        while q:
            tmp = q
            q = []
            for i, j in tmp:
                # 注意起点不算终点，不能在这里判断 (i,j) 是不是终点
                for x, y in (i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j):  # 访问相邻的格子
                    if 0 <= x < m and 0 <= y < n and maze[x][y] == '.':  # 之前没有访问过
                        if x == 0 or y == 0 or x == m - 1 or y == n - 1:  # 到达终点
                            return ans
                        maze[x][y] = None  # 访问标记
                        q.append((x, y))
            ans += 1
        return -1  # 无法到达终点
''',
    call=f'Solution().nearestExit({MAZE}, {ENT})',
    expect=3,
    skip=['m, n = len', 'sx, sy = entrance', 'q = []', 'for x, y in', 'q.append'],
    views=[
        dict(type='grid', var=_show, cell=92, h=400,
             label='maze（绿 = 已访问，数字 = 第几层；橙 = 边界出口；蓝框 = 出队格，粉框 = 邻居）',
             color=_color, cursors=[('i', 'j', 'blue'), ('x', 'y', 'pink')]),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['tmp']] if 'tmp' in S else None,
             label='tmp（这一层的格子）', cell=90, h=145),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']] if 'q' in S else None,
             label='q（下一层的格子）', cell=90, h=145),
    ],
    watch=[('ans', 'ans', 'green'), ('(i,j)', lambda S: (S['i'], S['j']) if 'i' in S else None, 'blue'),
           ('(x,y)', lambda S: (S['x'], S['y']) if 'x' in S else None, 'pink')],
    captions={
        'maze[sx][sy] = None': '起点 `({sx},{sy})` 改成 `None`：==直接改 maze 当访问标记==，省掉 vis 数组',
        'q = [(sx, sy)]': '第 0 层只有起点',
        'ans = 1': '`ans` = 下一层格子离起点的步数，从 1 开始',
        'while q': lambda S, B, r: ('`q` 不空：扩展下一层' if S.q else '`q` 空了：所有能走的格子都走完，没碰到出口'),
        'tmp = q': '取出这一层 `{[tuple(t) for t in tmp]}`，用新列表 `q` 收集下一层',
        'for i, j in tmp': lambda S, B, r: ('这一层的格子都处理完了' if 'i' in B and (B.i, B.j) == (S.i, S.j)
                                            else f'出队 `({S.i},{S.j})`：看它的左、右、上、下四个邻居'),
        'if 0 <= x < m': _nb,
        'if x == 0 or y == 0': _edge,
        'return ans': '走了 =={ans}== 步就到了出口：BFS 按层扩展，第一次到达就是最短',
        "maze[x][y] = None": '==入队前就标记==：`({x},{y})` 记为第 {ans} 层并加入 `q`，保证不会重复入队',
        'ans += 1': '这一层扩展完，`ans` → {ans}',
        'return -1': '无法到达出口，返回 -1',
    },
    cards=dict(
        one_liner='从入口一层层 BFS，第一次踩到边界空格就是最近出口',
        complexity='时间 `O(mn)`，空间 `O(min(m,n))`',
        problem=['迷宫 `maze` 里 `.` 是空格、`+` 是墙，从 `entrance` 出发上下左右走',
                 '==出口 = 边界上的空格==，但入口本身不算出口；求最少步数，到不了返回 -1',
                 '本视频：4×5 迷宫，入口 `(1,1)` → `3`'],
        quote='网格图存在左右横跳的可能，我们要==避免重复访问==之前访问过的格子。为此在格子坐标入队前标记 vis[i][j] = true。',
        quote_src='—— 灵茶山艾府题解',
        idea=['二叉树 BFS 只往下走；网格图会来回走，所以==入队前打标记==',
              '写法二直接把 `maze[i][j]` 改成 `None`，省去 `vis` 数组',
              '起点不算出口：只在==检查邻居时==判断是否到达边界'],
        summary=['时间 `O(mn)`；队列只装一层，空间 `O(min(m,n))`',
                 '易错：不能在出队时判断 `(i,j)` 是不是出口，否则入口在边界时会错误返回',
                 '易错：要在入队时标记，出队时才标记会让同一格重复入队',
                 '写法一用独立的 `vis` 数组，不修改输入，复杂度相同'],
    ),
)
