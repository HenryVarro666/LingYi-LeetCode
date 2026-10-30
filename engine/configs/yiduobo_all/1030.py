CONFIG = dict(
    num=1030, title='距离顺序排列矩阵单元格', difficulty='Easy', category='网格图',
    author='yiduobo', technique='从起点 BFS',
    tags=[],
    code='''
class Solution(object):
    def allCellsDistOrder(self, R, C, r0, c0):

        q = [[r0, c0]]
        l = 0
        r = 1
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        used = [[False] * C for _ in range(R)]
        used[r0][c0] = True
        while l < r:
            for nowx, nowy in q[l : r]:
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < R and y >= 0 and y < C and not used[x][y]:
                        used[x][y] = True
                        q.append([x, y])
            
            l, r = r, len(q)
        
        return q
''',
    call='Solution().allCellsDistOrder(3, 4, 1, 1)',
    expect=[[1, 1], [2, 1], [1, 2], [0, 1], [1, 0], [2, 2], [2, 0], [1, 3], [0, 2], [0, 0], [2, 3], [0, 3]],
    views=[
        dict(type='grid', var='used', h=300, cursors=[('nowx', 'nowy', 'yellow', '当前'), ('x', 'y', 'cyan', '邻居')],
             color=lambda S, i, j, v: 'green' if v is True else None, values=False),
        dict(type='array', var='q', h=200, label='q（BFS 队列 = 答案）', cell=96,
             window=('l', 'r - 1'), fmt=lambda v: f'{v[0]},{v[1]}'),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), 'nowx', 'nowy', 'x', 'y'],
    skip=['dx = [', 'dy = [', 'l = 0', 'r = 1', 'for index in range(4)', 'x = nowx', 'y = nowy', 'used = [['],
    max_steps=80,
    captions={
        'q = [[r0, c0]]': '从 `({r0}, {c0})` 出发，它离自己距离 0',
        'used[r0][c0] = True': '起点标记已访问',
        'while l < r': lambda S, B, r: (f'`l={S.l} < r={S.r}`：队列里 `[{S.l}, {S.r})` 这一层距离相同，逐个展开' if S.l < S.r else '这一层没有新点了 → 结束'),
        'for nowx, nowy in q[l : r]': lambda S, B, r: ('本层的点都处理完了' if B.get('nowx') == S.nowx and B.get('nowy') == S.nowy and B.get('l') == S.l else f'取出本层的点 `({S.nowx}, {S.nowy})`'),
        'if x >= 0': lambda S, B, r: (f'邻居 `({S.x}, {S.y})`：' + ('越界，跳过' if not (0 <= S.x < S.R and 0 <= S.y < S.C) else ('已访问，跳过' if B.used[S.x][S.y] else '==没访问过，入队==')) ),
        'used[x][y] = True': '`({x}, {y})` 标记已访问，距离比当前点大 1',
        'q.append': '`({x}, {y})` 入队，`q` 长度 {len(q)}',
        'l, r = r, len(q)': '本层结束：下一层区间 `[{l}, {r})`，距离加 1',
        'return q': '按层展开得到的就是距离从小到大：共 `{len(q)}` 个格子',
    },
    cards=dict(
        one_liner='BFS 第 k 层的格子，离起点的曼哈顿距离恰好是 k',
        complexity='时间 `O(R·C)`，空间 `O(R·C)`',
        problem=['`R × C` 的矩阵，给定起点 `(r0, c0)`',
                 '按到起点的曼哈顿距离从小到大，返回所有格子坐标',
                 '示例：`R=3, C=4, (1,1)` → `[[1,1],[2,1],[1,2],...]`'],
        quote='我们可以从(r0, c0)开始进行bfs，其中第k轮的bfs处理的点距离(r0, c0)的曼哈顿距离恰好为k，因此bfs完成后，最终的bfs队列就是答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['队列用数组 `q` 模拟，`[l, r)` 是当前这一层',
              '每层向四个方向扩展，没访问过的入队',
              '第 k 层处理完，队尾就是第 k+1 层，整个 `q` 自然按距离排好'],
        summary=['时间 `O(R·C)`，空间 `O(R·C)`',
                 '易错点：入队时就标记 `used`，否则同一格会重复入队',
                 '`l, r = r, len(q)` 是切换到下一层的关键',
                 '同距离内的顺序不限，题目允许任意'],
    ),
)
