G = [[0, 1, 0], [0, 1, 0]]


def _col(S, i, j, v):
    u = S.get('used')
    if not u:
        return None
    if u[i][j]:
        return 'green' if v == 0 else 'orange'
    return 'red' if v == 1 else None


def _why(S, B, want):
    x, y = S.x, S.y
    if not (0 <= x < S.m and 0 <= y < S.n):
        return f'邻居 `({x},{y})` 越界，跳过'
    if B.used[x][y]:
        return f'邻居 `({x},{y})` 已经走过 / 拆过，跳过'
    v = S.grid[x][y]
    if v == want:
        return (f'邻居 `({x},{y})` 是没走过的空格 → ==入队并标记==' if want == 0
                else f'邻居 `({x},{y})` 是没拆过的障碍 → ==穿过去，作为下一轮的起点==')
    return (f'邻居 `({x},{y})` 是障碍：这一轮不拆，先不走' if want == 0 else f'邻居 `({x},{y})` 是空格，上一轮已处理，跳过')


CONFIG = dict(
    num=2290, title='到达角落需要移除障碍物的最小数目', difficulty='Hard', category='网格图',
    author='yiduobo', technique='按移除数分轮的 BFS',
    tags=['灵神题单', '网格图', '难度分 2138'],
    code='''
class Solution(object):
    def minimumObstacles(self, grid):

        m = len(grid)
        n = len(grid[0])
        used = [[False] * n for _ in range(m)]
        used[0][0] = True

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        def bfs(q, used):
            l, r = 0, len(q)
            while l < r:
                nowx, nowy = q[l]
                l += 1
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n and not used[x][y] and grid[x][y] == 0:
                        q.append([x, y])
                        r += 1
                        used[x][y] = True
        
        q = [[0, 0]]
        res = 0
        while not used[m - 1][n - 1]:
            bfs(q, used)
            if not used[m - 1][n - 1]:
                res += 1
                next_q = []
                for nowx, nowy in q:
                    for index in range(4):
                        x = nowx + dx[index]
                        y = nowy + dy[index]
                        if x >= 0 and x < m and y >= 0 and y < n and not used[x][y] and grid[x][y] == 1:
                            next_q.append([x, y])
                            used[x][y] = True
                
                q = next_q[:]
        
        return res
''',
    call=f'Solution().minimumObstacles({G})',
    expect=1,
    skip=['m = len', 'n = len', 'dx = [', 'dy = [', 'x = nowx', 'y = nowy', 'used = [[', 'used[0][0] = True',
          'for index in range(4)', 'def bfs', 'l += 1', 'r += 1', 'q.append', 'next_q.append', 'next_q = []'],
    views=[
        dict(type='grid', var='grid', label='grid（绿 = 已走空格；橙 = 已拆障碍；红 = 未拆障碍）', cell=100, h=300,
             color=_col, cursors=[('nowx', 'nowy', 'blue'), ('x if x is not None and _line in (19, 20, 21, 22, 23, 24, 25, 38, 39, 40, 41, 42, 43, 44) else None', 'y', 'pink')]),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']] if 'q' in S else None,
             label='q（当前这一轮的前沿格子）', cell=80, h=170),
    ],
    watch=[('res（已拆障碍数）', 'res', 'green'), ('nowx', 'nowx', 'blue'), ('nowy', 'nowy', 'blue')],
    captions={
        'q = [[0, 0]]': '前沿队列从起点出发：`q = [[0, 0]]`',
        'res = 0': '`res` = 当前允许移除的障碍物数，==从 0 开始逐轮加 1==',
        'while not used[m - 1][n - 1]': lambda S, B, r: ('终点还没走到，继续' if not B.used[B.m - 1][B.n - 1] else '终点已经走到了，结束'),
        'bfs(q, used)': '先不拆任何新障碍，从前沿 BFS 扩展：只走==空格==',
        'l, r = 0, len(q)': '本次 BFS 的队列是 `q`，`l` 队首、`r` 队尾',
        'while l < r': lambda S, B, r: ('队列没处理完' if S.l < S.r else 'BFS 扩展完毕：空格能走的都走到了'),
        'nowx, nowy = q[l]': '出队 `({nowx},{nowy})`，看四个邻居',
        20: lambda S, B, r: _why(S, B, 0),
        36: lambda S, B, r: _why(S, B, 1),
        'used[x][y] = True': lambda S, B, r: (f'标记 `used[{S.x}][{S.y}]`：空格并入可走区域' if S.grid[S.x][S.y] == 0 else f'标记 `used[{S.x}][{S.y}]`：拆掉这个障碍，成为下一轮的前沿'),
        'if not used[m - 1][n - 1]': lambda S, B, r: ('走完空格还没到终点 → ==必须多拆一个障碍物==' if not B.used[B.m - 1][B.n - 1] else '已经到终点了'),
        'res += 1': '多允许拆 1 个：`res = {res}`',
        'for nowx, nowy in q': '只看==上一轮前沿== `q` 里的格子，旁边的障碍才是新的候选（旧的在之前轮次处理过了）',
        
        'q = next_q[:]': '下一轮的前沿 = 刚拆开的障碍格：`{q}`',
        'return res': '一共拆了 `{res}` 个障碍物',
    },
    max_steps=120,
    cards=dict(
        one_liner='拆 0 个能走到哪，拆 1 个能走到哪……按拆除数一圈圈外扩',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['网格里 `0` 是空格，`1` 是可以移除的障碍物，四方向移动',
                 '从左上角走到右下角，最少要移除多少个障碍物',
                 '示例：`[[0,1,1],[1,1,0],[1,1,0]]` → `2`',
                 '本视频：`[[0,1,0],[0,1,0]]` → `1`'],
        quote='可以先从左上角开始进行bfs，找出不移除障碍物时的可活动范围。若不能到达地图右下角，则可以从1开始逐个增加可移除障碍物的数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['移除一个障碍物 ≈ 穿墙走到障碍物的格子上',
              '拆 k 个时的可达范围 = 拆 k−1 个的范围 + 再穿过一个相邻障碍后能 BFS 到的范围',
              '每轮只需检查上一轮新增前沿的相邻障碍，旧的早处理过了'],
        summary=['时间 `O(mn)`：每个格子只会被标记一次',
                 '`res` 就是轮数：每多一轮多拆一个障碍物',
                 '易错：下一轮只能从==新拆开的障碍格==出发 BFS，不是整片已走区域',
                 '原文为 Python 2 风格，但在 Python 3 下无需修改，代码原样运行',
                 '对比灵神：灵神用双端队列做 0-1 BFS，一遍搞定；这里是分轮 BFS'],
    ),
)
