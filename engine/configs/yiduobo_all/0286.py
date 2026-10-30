INF = 2147483647
ROOMS = [[INF, -1, 0, INF], [INF, INF, INF, -1], [0, -1, INF, INF]]


def _show(S):
    r = S.get('rooms')
    if r is None:
        return None
    return [['∞' if v == 2147483647 else v for v in row] for row in r]


def _color(S, i, j, v):
    if v == 0:
        return 'green'
    if v == '∞':
        return None
    if v == -1:
        return 'purple'
    return 'blue'


def _nb(S, B, r):
    x, y = S.x, S.y
    m, n = B.m, B.n
    if not (0 <= x < m and 0 <= y < n):
        return f'`({x},{y})` 越界'
    a, b = B.rooms[x][y], B.rooms[S.nowx][S.nowy] + 1
    sa = '∞' if a == INF else a
    if a > b:
        return f'从 `({S.nowx},{S.nowy})` 看邻居 `({x},{y})` = `{sa}` > `{b}`→ ==更近=='
    return f'从 `({S.nowx},{S.nowy})` 看邻居 `({x},{y})` = `{sa}` ≤ `{b}`→ 墙或已有更近值'


CONFIG = dict(
    num=286, title='墙与门', difficulty='Medium', category='网格图',
    author='yiduobo', technique='多源 BFS',
    tags=['灵神题单'],
    setup='INF = 2147483647',
    code='''
class Solution(object):
    def wallsAndGates(self, rooms):

        m = len(rooms)
        n = len(rooms[0])

        q = []
        for i in range(m):
            for j in range(n):
                if rooms[i][j] == 0:
                    q.append([i, j])
        
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        head, tail = 0, len(q)
        while head < tail:
            for nowx, nowy in q[head : tail]:
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n and rooms[x][y] > rooms[nowx][nowy] + 1:
                        rooms[x][y] = rooms[nowx][nowy] + 1
                        q.append([x, y])
            
            head, tail = tail, len(q)

        return rooms
''',
    call=f'Solution().wallsAndGates({ROOMS})',
    expect=[[2, -1, 0, 1], [1, 2, 1, -1], [0, -1, 2, 3]],
    skip=['m = len', 'n = len', 'for i in range', 'for j in range', 'dx = [', 'dy = [', 'for index in range(4)',
          'x = nowx', 'y = nowy', 'if rooms[i][j] == 0', 'q = []', 'q.append([x, y])', 'for nowx, nowy'],
    max_steps=90,
    views=[
        dict(type='grid', var=_show, label='rooms（绿 = 门，紫 = 墙，∞ = 未算出，蓝 = 最短距离）', cell=96, h=400,
             color=_color, cursors=[('nowx', 'nowy', 'blue'), ('x if _line in (21, 22, 23) else None', 'y', 'pink')]),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']] if 'q' in S else None,
             label='q（暗 = 已处理的轮次，head 到 tail 是当前这一轮）', cell=70, pointers={'head': 'blue', 'tail': 'pink'},
             dim=lambda S, i, v: i < S.get('head', 0), h=190),
    ],
    watch=[('head', 'head', 'blue'), ('tail', 'tail', 'pink')],
    captions={
        'q.append([i, j])': '发现一扇门 `({i},{j})`，==所有门一起==作为 BFS 的起点入队',
        'head, tail = 0, len(q)': '`head = 0, tail = {tail}`：第一轮 = 所有的门（距离 0）',
        'while head < tail': lambda S, B, r: (f'`head = {B.head} < tail = {B.tail}`：这一轮还有格子，继续' if B.head < B.tail
                                              else f'`head = {B.head} >= tail = {B.tail}`：没有新格子了，BFS 结束'),
        'if x >= 0 and x < m': _nb,
        'rooms[x][y] = rooms[nowx][nowy] + 1': '`rooms[{x}][{y}] = {rooms[nowx][nowy]} + 1` = =={rooms[x][y]}==，入队',
        'head, tail = tail, len(q)': lambda S, B, r: f'这一轮扩展完：下一轮是 `q[{S.head}:{S.tail}]`，共 {S.tail - S.head} 个格子，距离再 +1',
        'return rooms': '所有能到达门的房间都填好了距离，到不了的仍是 INF',
    },
    cards=dict(
        one_liner='把所有门同时入队，一起向外 BFS，首次到达的轮次就是最近距离',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`rooms` 里 `-1` 是墙，`0` 是门，`INF = 2147483647` 是空房间',
                 '给每个空房间填上到最近的门的步数（上下左右），到不了的保持 `INF`',
                 '本视频：3×4 网格，两扇门分别在 `(0,2)` 和 `(2,0)`'],
        quote='从地图上的所有门开始向四周进行bfs，对于某个单元格，其首先被访问到的轮次就是其到达最近的门的距离了。',
        quote_src='—— yiduobo 题解原文',
        idea=['不是对每个房间找门，而是==反过来：从所有门同时出发==',
              '队列初始就放进全部的门，BFS 一轮走一步',
              '`rooms[x][y] > rooms[nowx][nowy] + 1` 既判断是否更近，又兼作 visited（墙 -1 永远不满足）'],
        summary=['时间 `O(mn)`：每个格子最多被更新入队一次',
                 '多源 BFS：初始队列放入全部起点，距离自动取最近的',
                 '墙是 `-1`，条件 `> 当前 + 1` 自然把它排除，门的 0 也不会被覆盖',
                 '代码在 Python 3 下直接可运行，未做修改；`INF` 在 setup 里定义为 2147483647'],
    ),
)
