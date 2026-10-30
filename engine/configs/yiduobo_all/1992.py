LAND = [[1, 0, 0], [0, 1, 1], [0, 1, 1]]


def _cell(S, i, j, v):
    if 'used' not in S or 'n' not in S:
        return None
    if v == 1 and i * S['n'] + j in S['used']:
        return 'green'
    return None


def _nb(S, B, r):
    x, y = S.x, S.y
    if not (x >= 0 and x < S.m and y >= 0 and y < S.n):
        return f'邻居 `({x},{y})` 越界 → 跳过'
    if x * S.n + y in S.used:
        return f'邻居 `({x},{y})` 已在 `used` 里 → 跳过，不重复入队'
    if S.land[x][y] != 1:
        return f'邻居 `({x},{y})` 是森林（0）→ 不是农场，跳过'
    return f'邻居 `({x},{y})` 是没访问过的农场 → ==入队=='


def _q(S):
    q = S.get('q')
    return [f'{a},{b}' for a, b in q] if q else None


CONFIG = dict(
    num=1992, title='找到所有的农场组', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='floodfill BFS · 队首队尾即矩形两角',
    tags=['灵神题单·贪心与思维', '难度分 1539'],
    code='''
class Solution(object):
    def findFarmland(self, land):

        m = len(land)
        n = len(land[0])

        res = []
        used = set()
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        for i in range(m):
            for j in range(n):
                if land[i][j] == 1 and i * n + j not in used:
                    q = [[i, j]]
                    used.add(i * n + j)
                    l = 0
                    r = 1
                    while l < r:
                        for nowx, nowy in q[l : r]:
                            for index in range(4):
                                x = nowx + dx[index]
                                y = nowy + dy[index]
                                if x >= 0 and x < m and y >= 0 and y < n and x * n + y not in used and land[x][y] == 1:
                                    used.add(x * n + y)
                                    q.append([x, y])
                    
                        l, r = r, len(q)
                    
                    res.append([q[0][0], q[0][1], q[-1][0], q[-1][1]])
        
        return res
''',
    call=f'Solution().findFarmland({LAND})',
    expect=[[0, 0, 0, 0], [1, 1, 2, 2]],
    skip=['m = len', 'n = len', 'res = []', 'used = set', 'dx = [', 'dy = [', 'l = 0', 'r = 1',
          'for index in range(4)', 'x = nowx', 'y = nowy', 'used.add(x * n + y)', 'for j in range(n)'],
    max_steps=60,
    views=[
        dict(type='grid', var='land', label='land（绿 = 已访问的农场；蓝框 = 当前格子，粉框 = 正在看的邻居）', cell=90, h=330,
             color=_cell, cursors=[('i', 'j', 'yellow'), ('nowx', 'nowy', 'blue'),
                                   ('x if _line in (23, 25) else None', 'y', 'pink')]),
        dict(type='array', var=_q, label='q（当前农场组的 BFS 队列：首 = 左上角，尾 = 右下角）', cell=80,
             pointers={'l': 'blue'}, dim=lambda S, i, v: i < S.get('l', 0), h=170),
        dict(type='text', h=70, size=30,
             fn=lambda S: ('农场组 = 队首 `' + str(S['q'][0]) + '` + 队尾 `' + str(S['q'][-1]) + '`') if S.get('q') else '还没找到新的农场组'),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), ('l', 'l', 'blue'), ('r', 'r'), ('res', 'res', 'green')],
    captions={
        'for i in range(m)': '按行扫描整张地图，寻找一块==还没访问过==的农场当起点',
        'if land[i][j] == 1': lambda S, B, r: (
            f'`({S.i},{S.j})` 是农场且不在 `used` → ==新农场组的左上角==，从这里开 BFS'
            if S.land[S.i][S.j] == 1 and S.i * S.n + S.j not in S.used
            else (f'`({S.i},{S.j})` 是森林，跳过' if S.land[S.i][S.j] != 1 else f'`({S.i},{S.j})` 已被某个农场组访问过，跳过')),
        'q = [[i, j]]': '起点入队：因为从左上角出发，==队首一定是矩形的左上角==',
        'used.add(i * n + j)': '把二维坐标压成一维 `i * n + j` 放进 `used`，防止重复访问',
        'while l < r': lambda S, B, r: (f'`l = {B.l} < r = {B.r}`：这一层还有格子要扩展' if B.l < B.r
                                        else f'`l == r`：队列扩展完了，这个农场组 BFS 结束'),
        'for nowx, nowy in q[l : r]': '取出当前这一层 `q[l:r]` 的格子，逐个向四个方向扩展',
        'if x >= 0 and x < m': _nb,
        'q.append': '`({x},{y})` 入队，队尾更新为 `{q[-1]}`',
        'l, r = r, len(q)': '进入下一层：`l = {l}`，`r = {r}`（队列总长）',
        'res.append': lambda S, B, r: (f'BFS 先到左上角、最后到右下角：队首 `{S.q[0]}`，队尾 `{S.q[-1]}` → '
                                       f'==农场组 {S.res[-1]}=='),
        'return res': '地图扫完，一共 `{len(res)}` 个农场组：`{res}`',
    },
    cards=dict(
        one_liner='农场组是矩形：BFS 起点是左上角，终点必是右下角，队首队尾就是答案',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`m x n` 二进制矩阵：`1` 是农场，`0` 是森林',
                 '农场连成互不相邻的==矩形农场组==，求每组左上角、右下角坐标',
                 '示例：`[[1,0,0],[0,1,1],[0,1,1]]` → `[[0,0,0,0],[1,1,2,2]]`',
                 '本视频：3 x 3 的地图，2 个农场组（示例 1）'],
        quote='对每一块农场组的bfs都是从农场组的左上角开始，而bfs必然于农场组的右下角结束，这也就意味着==队列首尾的位置恰好就是题目要找的答案==。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目保证农场组是矩形且互不相邻 → 经典 floodfill',
              '按行扫描遇到没访问的 `1`，它一定是某个矩形的==左上角==',
              '用数组 + `l`、`r` 做按层 BFS，访问过的格子压成 `i*n+j` 记进 `used`',
              'BFS 的最后一个入队格子就是==右下角==，不用再单独找边界'],
        summary=['时间 `O(mn)`：每个格子最多入队一次',
                 '易错：队首是 `q[0]`，队尾是 `q[-1]`，写成 `q[l]` 就错了',
                 '不用 `used` 会重复把同一个农场组再 BFS 一遍',
                 '对比灵神：灵神只判断「左、上都不是 1」找左上角，再向右、向下延伸找右下角',
                 '原文已是 Python 3 可运行写法，代码未改'],
    ),
)
