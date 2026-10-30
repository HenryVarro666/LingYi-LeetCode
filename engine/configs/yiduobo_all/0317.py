GRID = [[1, 0, 1], [0, 2, 0]]


def _cur(S):
    d = S.get('dis')
    return d[-1] if d else None


def _total(S):
    d = S.get('dis')
    if not d or 'res' not in S:
        return None
    m, n = S['m'], S['n']
    out = [[None] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if S['grid'][i][j] != 0:
                out[i][j] = '■'
            elif any(x[i][j] == -1 for x in d):
                out[i][j] = '×'
            else:
                out[i][j] = sum(x[i][j] for x in d)
    return out


def _same(S, B):
    try:
        return B.nowx == S.nowx and B.nowy == S.nowy
    except Exception:
        return False


def _gcolor(S, i, j, v):
    if v == 1:
        return 'orange'
    if v == 2:
        return 'red'
    return None


CONFIG = dict(
    num=317, title='离建筑物最近的距离', difficulty='Hard', category='网格图',
    author='yiduobo', technique='每栋建筑各做一次 BFS，再累加距离',
    tags=['灵神题单', '网格图'],
    code='''
class Solution(object):
    def shortestDistance(self, grid):

        m = len(grid)
        n = len(grid[0])
        
        dis = []

        def bfs(x, y):
            q = [[x, y]]
            dis.append([[-1 for j in range(n)] for i in range(m)])
            head, tail = 0, 1
            vis = set([x * n + y])
            step = 0
            dx = [0, 1, 0, -1]
            dy = [1, 0, -1, 0]

            while head < tail:
                step += 1
                for nowx, nowy in q[head : tail]:
                    for index in range(4):
                        x = nowx + dx[index]
                        y = nowy + dy[index]
                        if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 0 and x * n + y not in vis:
                            vis.add(x * n + y)
                            q.append([x, y])
                            dis[-1][x][y] = step
                
                head, tail = tail, len(q)

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    bfs(i, j)

        res = -1
        for i in range(m):
            for j in range(n):
                tot = 0
                for p in range(len(dis)):
                    if dis[p][i][j] == -1:
                        tot = -1
                        break
                    else:
                        tot += dis[p][i][j]
                
                if tot != -1 and (res == -1 or res > tot):
                    res = tot
        
        return res
''',
    call=f'Solution().shortestDistance({GRID})',
    expect=2,
    skip=['dx = [', 'dy = [', 'for index in range(4)', 'x = nowx', 'y = nowy', 'q = [[x, y]]', 'head, tail = 0, 1',
          'step = 0', 'q.append', 'for i in range(m)', 'for j in range(n)', 'tot = 0'],
    max_steps=76,
    views=[
        dict(type='grid', var='grid', label='grid（橙 = 建筑 1，红 = 障碍 2，蓝框 = 正在 BFS 的建筑/出队格）', cell=90, h=300,
             color=_gcolor, cursors=[('nowx', 'nowy', 'blue')]),
        dict(type='grid', var=_cur, label='dis[-1]：当前这栋建筑到各格的距离（-1 = 没到过）', cell=90, h=300),
        dict(type='grid', var=_total, label='总距离（× = 有建筑到不了，■ = 非空地）', cell=90, h=300,
             cursors=[('i', 'j', 'yellow')]),
    ],
    watch=[('step', 'step', 'blue'), ('head', 'head'), ('tail', 'tail'), ('tot', 'tot', 'yellow'), ('res', 'res', 'green')],
    captions={
        'dis = []': '`dis` 按建筑编号存放：==每栋建筑一张距离表==',
        'if grid[i][j] == 1': lambda S, B, r: (f'`({S.i},{S.j})` 是建筑 → 从这里做一次 BFS' if S.grid[S.i][S.j] == 1
                                               else f'`({S.i},{S.j})` 不是建筑（{S.grid[S.i][S.j]}），跳过'),
        'bfs(i, j)': '对建筑 `({i},{j})` 做 BFS：新建一张距离表，全填 `-1`（还没到过）',
        'vis = set': '起点 `{x * n + y}`（把 `(x,y)` 压成 `x*n+y`）先放进 `vis`，防止走回头路',
        'while head < tail': lambda S, B, r: (f'队列 `[{S.head}:{S.tail}]` 还有 `{S.tail - S.head}` 个格子 → 继续扩下一层' if S.head < S.tail
                                              else '队列空了：这栋建筑能到的格子都量完了'),
        'step += 1': '往外扩一层：这一层的格子离建筑 `{step}` 步',
        'for nowx, nowy in q': lambda S, B, r: (f'这一层的格子都处理完了' if _same(S, B) else f'取出当前层的格子 `({S.nowx},{S.nowy})`，向四个方向扩'),
        'if x >= 0 and x < m': lambda S, B, r: (
            f'`({S.x},{S.y})` 是没到过的空地 → ==可以走==' if (0 <= S.x < S.m and 0 <= S.y < S.n and S.grid[S.x][S.y] == 0 and S.x * S.n + S.y not in S.vis)
            else f'`({S.x},{S.y})` 越界、是建筑/障碍或已到过 → 不走'),
        'vis.add': '标记 `({x},{y})` 已到过',
        'dis[-1][x][y] = step': '`({x},{y})` 离这栋建筑 ==`{step}`== 步：写进 `dis[-1]`',
        'head, tail = tail': '这一层处理完：`[{head}:{tail}]` 是下一层',
        'res = -1': '`res` 记最小总距离，`-1` 表示还没有候选',
        'tot += dis': '累加：`({i},{j})` 到建筑 `{p}` 的距离 `{dis[p][i][j]}`，`tot` = =={tot}==',
        'if dis[p][i][j] == -1': lambda S, B, r: (f'建筑 `{S.p}` 到不了 `({S.i},{S.j})`（`-1`）→ 这格作废' if S.dis[S.p][S.i][S.j] == -1
                                                  else f'建筑 `{S.p}` 能到 `({S.i},{S.j})`，距离 `{S.dis[S.p][S.i][S.j]}`'),
        'tot = -1': '有建筑到不了 → `tot = -1`，不再累加',
        'if tot != -1': lambda S, B, r: (f'`tot = {S.tot}`，比当前 `res = {S.res}` 小 → ==更新答案==' if (S.tot != -1 and (S.res == -1 or S.res > S.tot))
                                         else f'`tot = {S.tot}`：{"作废" if S.tot == -1 else "不比 res 更小"} → 不更新'),
        'return res': '所有格子比完，最小的总距离是 ==`{res}`==',
    },
    cards=dict(
        one_liner='从每栋建筑各 BFS 一遍，把距离加起来，取最小的空地',
        complexity='时间 `O(k × m × n)`（k 为建筑数），空间 `O(k × m × n)`',
        problem=['网格里 `0` 空地、`1` 建筑、`2` 障碍；只能上下左右走，不能穿过建筑和障碍',
                 '在空地上选一块地，使它到==所有建筑==的距离之和最小，到不了就返回 `-1`',
                 '本视频：`[[1,0,1],[0,2,0]]` → `2`（取 `(0,1)`）'],
        quote='本题看上去与之前的296题很像，但是本题的建筑物是无法通过的，而且还可能存在障碍单元格，因此不能使用之前的贪心法。',
        quote_src='—— yiduobo 题解原文',
        idea=['建筑和障碍会挡路，不能用 296 题的曼哈顿距离贪心',
              '原文选「==从每栋建筑出发做 BFS==」：建筑少则 BFS 少，建筑多则地图拥挤、每次 BFS 很短',
              '每次 BFS 的距离存进 `dis`，最后逐格累加，有一个 `-1` 就作废'],
        summary=['时间 `O(k·m·n)`，空间 `O(k·m·n)`',
                 '有一栋建筑到不了的格子，总和作废（`tot = -1`），不能当候选',
                 '`x * n + y` 把二维坐标压成一个整数放进 `vis`',
                 '`res` 初值 `-1`，所以要判断 `res == -1 or res > tot`',
                 '原文是 Python 2 风格的类，代码无需修改'],
    ),
)
