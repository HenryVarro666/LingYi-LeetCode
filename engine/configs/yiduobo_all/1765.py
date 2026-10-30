WATER = [[0, 1, 0], [0, 0, 0], [0, 0, 0]]


def _nb(S, B, r):
    x, y = S.x, S.y
    if not (0 <= x < S.m and 0 <= y < S.n):
        return f'邻居 `({x},{y})` 越界 → 跳过'
    if S.res[x][y] != -1:
        return f'邻居 `({x},{y})` 高度已定为 `{S.res[x][y]}` → 跳过'
    return f'邻居 `({x},{y})` 还是 `-1`（没访问过）→ ==第一次到达，高度 = 当前 + 1=='


CONFIG = dict(
    num=1765, title='地图中的最高点', difficulty='Medium', category='网格图',
    author='yiduobo', technique='多源 BFS（从所有水域出发）',
    tags=['灵神题单', '网格图'],
    code='''
class Solution(object):
    def highestPeak(self, isWater):

        m = len(isWater)
        n = len(isWater[0])
        res = [[-1] * n for _ in range(m)]
        q = []
        for i in range(m):
            for j in range(n):
                if isWater[i][j]:
                    q.append([i, j])
                    res[i][j] = 0
        
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        l = 0
        r = len(q)
        while l < r:
            nowx, nowy = q[l]
            l += 1
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x >= 0 and x < m and y >= 0 and y < n and res[x][y] == -1:
                    res[x][y] = res[nowx][nowy] + 1
                    q.append([x, y])
                    r += 1
        
        return res
''',
    call=f'Solution().highestPeak({WATER})',
    expect=[[1, 0, 1], [2, 1, 2], [3, 2, 3]],
    skip=['m = len', 'n = len', 'l = 0', 'r = len', 'dx = [', 'dy = [', 'l += 1', 'for index in range(4)',
          'x = nowx', 'y = nowy', 'q.append([x, y])', 'r += 1', 'for i in range', 'for j in range', 'q = []'],
    views=[
        dict(type='grid', var='res', label='res（-1 = 未访问；绿 = 已定高度；蓝框 = 出队，粉框 = 正在看的邻居）', cell=110, h=400,
             color=lambda S, i, j, v: 'green' if v == 0 else ('cyan' if v > 0 else None),
             cursors=[('nowx', 'nowy', 'blue'), ('x if _line == 24 else None', 'y', 'pink')]),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']] if 'q' in S else None,
             label='q（暗 = 已出队，l 指向下一个出队的）', cell=80, pointers={'l': 'blue'},
             dim=lambda S, i, v: i < S.get('l', 0), h=190),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r')],
    captions={
        'res = [[-1]': '`res` 全部先填 `-1`，表示还没访问',
        'if isWater[i][j]': lambda S, B, r: (f'`({S.i},{S.j})` 是水域 → ==高度必须为 0，作为 BFS 起点==' if S.isWater[S.i][S.j]
                                              else f'`({S.i},{S.j})` 是陆地，先不管'),
        'q.append([i, j])': '水域 `({i},{j})` 入队',
        'res[i][j] = 0': '水域高度固定为 0',
        'while l < r': lambda S, B, r: (f'`l = {B.l} < r = {B.r}`：队列不空，继续' if B.l < B.r
                                        else f'`l == r = {B.r}`：队列空了，所有格子高度都定了'),
        'nowx, nowy = q[l]': '出队 `({nowx},{nowy})`，高度 `{res[nowx][nowy]}`，向四个方向扩展',
        'if x >= 0 and x < m': _nb,
        'res[x][y] = res[nowx][nowy] + 1': '`res[{x}][{y}] = {res[nowx][nowy]} + 1 = {res[x][y]}`：相邻高度差恰好 1，取最大',
        'return res': '返回 `res`：每格的高度就是到最近水域的距离',
    },
    cards=dict(
        one_liner='相邻高度差不超过 1，所以从水域一层层 +1 往外涨',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`isWater[i][j] = 1` 是水域（高度必须为 0），`0` 是陆地',
                 '任意相邻格子高度差 ==至多为 1==，求一种让最高点尽量高的高度矩阵',
                 '本视频：`[[0,1,0],[0,0,0],[0,0,0]]` → `[[1,0,1],[2,1,2],[3,2,3]]`'],
        quote='应该从高度位置等于0的水域开始进行bfs，每次将相邻且未访问过的位置的高度置为当前位置高度加1，这样就能使得最高位置的高度最大。',
        quote_src='—— yiduobo 题解原文',
        idea=['高度差不超过 1，所以每格高度 ≤ 它到最近水域的距离',
              '取等号就能让最高点最大：高度 = 到最近水域的距离',
              '多源 BFS 一层层扩，第一次到达时 `res` 还是 `-1`，直接赋值'],
        summary=['时间 `O(mn)`，每个格子只入队一次',
                 '`res` 初值 `-1` 兼当 visited 标记，不用再开 `used`',
                 '易错：水域要==全部==先入队，再统一 BFS',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
