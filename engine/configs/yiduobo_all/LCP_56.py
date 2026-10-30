MAT = ['>v<v', 'vv^<', 'v^<>']


def _col(S, i, j, v):
    if 'vis' not in S:
        return None
    return 'green' if S['vis'][i][j] else None


def _pend(S):
    if 'q' not in S:
        return None
    return [f'{a},{b}' for a, b in S['q']]


CONFIG = dict(
    num='LCP 56', title='信物传送', difficulty='未知', category='网格图',
    author='yiduobo', technique='分层 BFS（每轮施法一次）',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def conveyorBelt(self, matrix, start, end):

        m = len(matrix)
        n = len(matrix[0])

        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]
        direct_mapping = {'^': 0, '>': 1, 'v': 2, '<': 3}

        vis = [[False] * n for _ in range(m)]
        vis[start[0]][start[1]] = True
        head = 0
        tail = 1
        q = [start]
        res = 0        

        while True:
            tmp = head
            while head < tail:
                nowx, nowy = q[head]
                head += 1

                x = nowx + dx[direct_mapping[matrix[nowx][nowy]]]
                y = nowy + dy[direct_mapping[matrix[nowx][nowy]]]
                if x >= 0 and x < m and y >= 0 and y < n and not vis[x][y]:
                    q.append([x, y])
                    vis[x][y] = True
                    tail += 1
        
            if vis[end[0]][end[1]]:
                return res
        
            head = tmp

            res += 1

            for nowx, nowy in q[head : tail]:
                for index in range(4):
                    if index != direct_mapping[matrix[nowx][nowy]]:
                        x = nowx + dx[index]
                        y = nowy + dy[index]
                        if x >= 0 and x < m and y >= 0 and y < n and not vis[x][y]:
                            q.append([x, y])
                            vis[x][y] = True
            
            head, tail = tail, len(q)
''',
    call=f'Solution().conveyorBelt({MAT}, [0, 0], [2, 3])',
    expect=2,
    skip=['m = len', 'n = len', 'dx = [', 'dy = [', 'direct_mapping = {', 'tmp = head', 'head += 1', 'tail += 1',
          'q.append', 'for index in range(4)', 'x = nowx', 'y = nowy', 'vis = [[', 'head = 0', 'tail = 1', 'res = 0'],
    views=[
        dict(type='text', size=22, fn=lambda S: f"已施法 ==`{S['res']}`== 次；绿色 = 到过的格子；蓝框 = 正在处理，粉框 = 下一个到达的格子" if 'res' in S else ''),
        dict(type='grid', var='matrix', cell=110, h=400,
             label='matrix',
             color=_col,
             cursors=[('start[0]', 'start[1]', 'cyan', '起点'), ('end[0]', 'end[1]', 'orange', '终点'),
                      ('nowx', 'nowy', 'blue'), ('x if _line in (26, 28, 43, 45) else None', 'y', 'pink')]),
        dict(type='array', var=_pend, label='q（head 指向下一个要处理的，tail 之前是本轮已入队的）', cell=70, h=190,
             pointers={'head': 'blue', 'tail': 'pink'}),
    ],
    max_steps=58,
    watch=[('head', 'head', 'blue'), ('tail', 'tail', 'pink'), ('res', 'res', 'green')],
    captions={
        'q = [start]': '起点入队：`q = [start]`，==起点本身不用施法==',
        'while head < tail': lambda S, B, r: (f'`head = {B.head} < tail = {B.tail}`：这一轮还有格子要顺着传送带走' if B.head < B.tail
                                              else f'`head == tail = {B.tail}`：不施法能到的格子都走完了'),
        'nowx, nowy = q[head]': '取出 `({nowx},{nowy})`，它的传送带是 `{matrix[nowx][nowy]}`，只能顺着走一步',
        'x = nowx': '顺着传送带走到 `({x},{y})`',
        26: lambda S, B, r: (f'`({S.x},{S.y})` 在界内且没到过 → ==顺着传送带免费到达，入队==' if (0 <= S.x < B.m and 0 <= S.y < B.n and not B.vis[S.x][S.y])
                             else f'`({S.x},{S.y})` 越界或已到过 → 不扩展'),
        28: '`({x},{y})` 标记为已到达（这一轮不花施法次数）',
        43: lambda S, B, r: (f'`({S.x},{S.y})` 在界内且没到过 → ==施法转向后到达，入队（花的是本轮这 1 次施法）==' if (0 <= S.x < B.m and 0 <= S.y < B.n and not B.vis[S.x][S.y])
                             else f'`({S.x},{S.y})` 越界或已到过 → 不扩展'),
        45: '`({x},{y})` 标记为已到达（施法扩展出的新位置，下一轮从这里继续 BFS）',
        'if vis[end[0]][end[1]]': lambda S, B, r: (f'终点已到达 → 直接返回施法次数 `{B.res}`' if B.vis[B.end[0]][B.end[1]]
                                                    else '终点还没到 → 需要再施法一次，把传送带转向'),
        'head = tmp': '`head` 退回本轮起点：下面要对==本轮所有新到格子==各施一次法',
        'res += 1': '施法次数 `res` → =={res}==（这一轮的所有扩展都花这一次）',
        'for nowx, nowy in q[head : tail]': '枚举本轮到过的格子 `({nowx},{nowy})`：把它的传送带转向，往另外 3 个方向各走一步',
        40: lambda S, B, r: (
            f'方向 `{S.index}` ≠ 原传送带方向 → 转向后可以走' if S.index != B.direct_mapping[B.matrix[S.nowx][S.nowy]]
            else f'方向 `{S.index}` 是原传送带方向 → 不用转向，上一轮已经走过了'),
        'head, tail = tail, len(q)': '下一轮只处理==刚才施法新扩展出来的格子==：`head = {head}`，`tail = {tail}`',
    },
    cards=dict(
        one_liner='先白嫖顺着传送带能到的格子，再花一次施法扩展一圈',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['网格里每格是一条传送带 `^ > v <`，踩上去会被传到相邻格',
                 '可以花 1 次施法把某格传送带改成任意方向',
                 '问从 `start` 到 `end` 最少要施法几次（题库未给题面，按 yiduobo 文章与原题理解）',
                 '本视频：3×4 网格，起点 `(0,0)`，终点 `(2,3)`'],
        quote='每一轮的bfs都只需要考虑上一轮施法新扩展出来的位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['从当前可达点 BFS：只顺着传送带走，==不花施法==',
              '到不了终点就施法：把这些点的传送带改成其余 3 个方向，扩展一步，`res += 1`',
              '循环：BFS → 判断终点 → 施法扩展，直到终点被访问'],
        summary=['时间 `O(mn)`：每个格子只入队一次，`vis` 去重',
                 '施法次数 = 分层 BFS 的层数，这是 0-1 BFS 的另一种写法',
                 '易错：`head = tmp` 要退回本轮起点，施法扩展的是本轮所有新点，不是下一轮的点',
                 '易错：`head, tail = tail, len(q)` 之后下一轮只处理新增的点'],
    ),
)
