MAZE = [['+', '+', '+', '.', '+'],
        ['+', '.', '.', '.', '+'],
        ['+', '.', '+', '+', '+'],
        ['+', '+', '+', '+', '+']]
ENT = [1, 1]


def _show(S):
    g = S.get('maze')
    if g is None:
        return None
    used = S.get('used') or set()
    n = len(g[0])
    return [[str(i * n + j) if i * n + j in used else c for j, c in enumerate(row)] for i, row in enumerate(g)]


def _color(S, i, j, v):
    g = S.get('maze')
    if g is None:
        return None
    n = len(g[0])
    if i * n + j in (S.get('used') or set()):
        return 'green'
    if g[i][j] == '.' and (i in (0, len(g) - 1) or j in (0, n - 1)):
        return 'orange'
    return None


def _nb(S, B, r):
    x, y, m, n = S.x, S.y, S.m, S.n
    if not (x >= 0 and x < m and y >= 0 and y < n):
        return f'`({x},{y})` 出界 → 跳过'
    if S.maze[x][y] == '+':
        return f'`({x},{y})` 是墙 `+` → 跳过'
    if x * n + y in S.used:
        return f'编号 `{x}×{n}+{y} = {x * n + y}` 已在 `used` 里 → 走过了，跳过'
    return f'`({x},{y})` 是空格且编号 `{x * n + y}` 没出现过 → ==可以走=='


def _edge(S, B, r):
    x, y = S.x, S.y
    if x == 0 or y == 0 or x == S.m - 1 or y == S.n - 1:
        return f'`({x},{y})` 在迷宫边界上 → ==到达出口=='
    return f'`({x},{y})` 不在边界，先入队，下一轮再从它往外扩'


CONFIG = dict(
    num=1926, title='迷宫中离入口最近的出口', difficulty='Medium', category='网格图',
    author='yiduobo', technique='BFS（数组 + l/r 分层）',
    tags=['labuladong', '灵神题单·网格图', '难度分 1638'],
    code='''
class Solution(object):
    def nearestExit(self, maze, entrance):

        m = len(maze)
        n = len(maze[0])

        q = [[entrance[0], entrance[1]]]
        l = 0
        r = 1
        used = set()
        used.add(entrance[0] * n + entrance[1])
        step = 0
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        while l < r:
            step += 1
            for nowx, nowy in q[l : r]:
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n and maze[x][y] != '+' and x * n + y not in used:
                        if x == 0 or y == 0 or x == m - 1 or y == n - 1:
                            return step
                        q.append([x, y])
                        used.add(x * n + y)
            
            l, r = r, len(q)

        return -1
''',
    call=f'Solution().nearestExit({MAZE}, {ENT})',
    expect=3,
    skip=['m = len', 'n = len', 'l = 0', 'r = 1', 'used = set()', 'dx = [', 'dy = [', 'for index in range',
          'x = nowx', 'y = nowy', 'q.append'],
    views=[
        dict(type='grid', var=_show, cell=92, h=400,
             label='maze（绿 = 在 used 里，数字 = 编号 x·n+y；橙 = 出口）',
             color=_color, cursors=[('nowx', 'nowy', 'blue'), ('x', 'y', 'pink')]),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']] if 'q' in S else None,
             label='q（暗 = 之前的轮次；[l, r) 是当前这一轮）', cell=90, h=170,
             pointers={'l': 'blue', 'r': 'pink'},
             dim=lambda S, i, v: i < S.get('l', 0)),
    ],
    watch=[('step', 'step', 'green'), ('l', 'l', 'blue'), ('r', 'r', 'pink'),
           ('used', lambda S: sorted(S['used']) if 'used' in S else None)],
    captions={
        'q = [[entrance': '入口 `({entrance[0]},{entrance[1]})` 入队；`q[l:r]` 是==当前这一轮==的格子',
        'used.add(entrance': '格子 `(x,y)` 编码成 `x * n + y` 放进集合：入口编号 `{entrance[0]}×{n}+{entrance[1]} = {entrance[0] * n + entrance[1]}`',
        'step = 0': '`step` 记录 BFS 的轮次 = 走了几步',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`：这一轮还有格子，继续' if S.l < S.r
                                        else '`l == r`：没有新格子了，BFS 结束'),
        'step += 1': '开始第 =={step}== 轮：这一轮扩展到的格子离入口 {step} 步',
        'for nowx, nowy in': lambda S, B, r: ('这一轮的格子都扩展完了' if 'nowx' in B and (B.nowx, B.nowy) == (S.nowx, S.nowy)
                                             else f'取出 `({S.nowx},{S.nowy})`，按 `dx/dy` 看下、右、上、左'),
        'if x >= 0 and x < m': _nb,
        'if x == 0 or y == 0': _edge,
        'return step': '第 {step} 轮就到达了边界 → 最近出口的距离是 =={step}==',
        'used.add(x * n + y)': '`({x},{y})` 入队，编号 `{x * n + y}` 加入 `used`',
        'l, r = r, len(q)': '这一轮结束：`l, r = {l}, {r}`，新入队的就是下一轮',
        'return -1': 'BFS 完成仍没到边界 → `-1`',
    },
    cards=dict(
        one_liner='从入口一轮轮向外扩，第一次踩到边界就是答案',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['迷宫里 `.` 是空格、`+` 是墙，从 `entrance` 出发每步上下左右走一格',
                 '==边界上的空格是出口==（入口自己不算），求最少步数，没有返回 -1',
                 '本视频：4×5 迷宫，入口 `(1,1)` → `3`'],
        quote='题目要求找出从entrance开始需要走多少步走到迷宫的边界上，==非常典型的bfs问题==。直接从entrance开始bfs，一轮一轮向外扩展直到抵达迷宫边界。',
        quote_src='—— yiduobo 题解原文',
        idea=['队列是普通数组，`q[l:r]` 是当前一轮，扩完令 `l, r = r, len(q)`',
              '访问过的格子用一维编号 `x * n + y` 存进集合 `used`',
              '在扩展邻居时判断边界，所以入口本身不会被当成出口'],
        summary=['时间、空间都是 `O(mn)`：每个格子最多入队一次',
                 '易错：入口在边界上时不能直接返回 0，原文只在==邻居==上判断出口',
                 '易错：入队时就加入 `used`，否则同一格会被多次入队',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
