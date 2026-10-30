GRID = [["X", "X", "X", "X", "X"], ["X", "*", "O", "O", "X"], ["X", "O", "X", "O", "X"], ["X", "X", "X", "#", "X"]]


def _color(S, i, j, v):
    if GRID[i][j] == '*':
        return 'yellow'
    if GRID[i][j] == '#':
        return 'green'
    if 'q' in S and [i, j] in S['q']:
        return 'blue'
    return None


def _nb(S, B, r):
    x, y = S.x, S.y
    m, n = B.m, B.n
    if not (0 <= x < m and 0 <= y < n):
        return f'邻居 `({x},{y})` 越界，跳过'
    c = B.grid[x][y]
    if c == '#':
        return f'邻居 `({x},{y})` 是食物 `#` → 返回当前轮次 ==`step = {B.step}`=='
    if c == 'O':
        return f'邻居 `({x},{y})` 是空地 `O`，不是食物 → 继续往下判断'
    return f'邻居 `({x},{y})` 是 `X`（墙或已走过）→ 不是食物，不能走'


CONFIG = dict(
    num=1730, title='获取食物的最短路径', difficulty='Medium', category='网格图',
    author='yiduobo', technique='BFS（按轮次）',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def getFood(self, grid):

        m = len(grid)
        n = len(grid[0])
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '*':
                    sx, sy = i, j
                    grid[i][j] = 'X'
        
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        q = [[sx, sy]]
        head, tail = 0, 1
        step = 0
        while head < tail:
            step += 1
            for nowx, nowy in q[head : tail]:
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n:
                        if grid[x][y] == '#':
                            return step
                    
                        if grid[x][y] == 'O':
                            q.append([x, y])
                            grid[x][y] = 'X'
            
            head, tail = tail, len(q)
        
        return -1
''',
    call=f'Solution().getFood({GRID})',
    expect=4,
    skip=['m = len', 'n = len', 'for i in range', 'for j in range', 'dx = [', 'dy = [', 'for index in range(4)',
          'x = nowx', 'y = nowy', 'q.append', 'sx, sy = i, j', "if grid[i][j] == '*'"],
    max_steps=90,
    views=[
        dict(type='grid', var='grid', label='grid（黄 = 起点 *，绿 = 食物 #，蓝 = 已入队的格子；X = 墙或已走过）', cell=96, h=400,
             color=_color, cursors=[('nowx', 'nowy', 'blue'), ('x if _line in (24, 25, 28, 30) else None', 'y', 'pink')]),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']] if 'q' in S else None,
             label='q（暗 = 已处理的轮次，head 到 tail 是当前这一轮）', cell=80, pointers={'head': 'blue', 'tail': 'pink'},
             dim=lambda S, i, v: i < S.get('head', 0), h=190),
    ],
    watch=[('head', 'head', 'blue'), ('tail', 'tail', 'pink'), ('step', 'step', 'green')],
    captions={
        "grid[i][j] = 'X'": '起点记为 `({sx},{sy})`，并==改成 X==：当作走过的标记，不会再回头',
        'q = [[sx, sy]]': '起点入队，`q[head:tail]` 就是当前这一轮要扩展的格子',
        'head, tail = 0, 1': '`head = 0, tail = 1`：第一轮只有起点',
        'step = 0': '`step` 记 BFS 的轮次，也就是走了几步',
        'while head < tail': lambda S, B, r: (f'`head = {B.head} < tail = {B.tail}`：这一轮还有格子，继续' if B.head < B.tail
                                              else f'`head = {B.head} >= tail = {B.tail}`：没有新格子了 → 走不到食物'),
        'step += 1': '开始新的一轮，`step` → =={step}==：这一轮扩展出的格子都比上一轮多走一步',
        'for nowx, nowy in q[head : tail]': '取出这一轮的格子 `({nowx},{nowy})`，看四个方向',
        'if x >= 0 and x < m': '先判断 `({x},{y})` 是否在网格内',
        "if grid[x][y] == '#'": _nb,
        "if grid[x][y] == 'O'": lambda S, B, r: (f'`({S.x},{S.y})` 是空地 `O` → ==入队==' if B.grid[S.x][S.y] == 'O' else f'`({S.x},{S.y})` 不是空地，不入队'),
        "grid[x][y] = 'X'": '入队时立刻改成 `X`，同一格不会被重复入队',
        'head, tail = tail, len(q)': lambda S, B, r: f'这一轮扩展完：下一轮是 `q[{S.head}:{S.tail}]`，共 {S.tail - S.head} 个格子',
        'return step': '第一次碰到 `#` 的轮次就是最短步数：返回 =={step}==',
        'return -1': '队列扩展完也没碰到 `#` → 返回 `-1`',
    },
    cards=dict(
        one_liner='从 * 出发 BFS，第一次碰到 # 的轮次就是最短路',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['网格里 `*` 是起点，`#` 是食物，`O` 是空地，`X` 是障碍',
                 '每步走上下左右一格，求到任意一个食物的最短步数，走不到返回 `-1`',
                 '本视频：4×5 网格，路径 `(1,1)→(1,2)→(1,3)→(2,3)→(3,3)`，答案 `4`'],
        quote='非常标准的bfs问题。从*所在的位置开始进行bfs，如果能走到#所在的位置，那么bfs的轮次即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['BFS 一轮扩展一圈，`step` 就是轮次',
              '队列用数组 + `head`、`tail`：`q[head:tail]` 是当前轮',
              '入队时就把 `O` 改成 `X`，既当 visited 又省一个数组'],
        summary=['时间 `O(mn)`：每个格子最多入队一次',
                 '先找到 `*` 并把它改成 `X`，否则起点可能被走回来',
                 '碰到 `#` 就直接返回，不需要入队',
                 '队列空了仍没碰到 `#` → `-1`',
                 '代码在 Python 3 下直接可运行，未做修改'],
    ),
)
