def _col(S, i, j, v):
    if 'vis' in S and 'mid' in S:                 # 二分阶段的 BFS
        if S['vis'][i][j]:
            return 'blue'
        return 'green' if v is not None and v >= S['mid'] else None
    return 'cyan' if v == 0 else None


def _dim(S, i, j, v):
    if 'vis' in S and 'mid' in S:
        return v is None or v < S['mid']
    return v is None


def _txt(S):
    if 'mid' in S and 'vis' in S:
        return f"试安全系数 `mid = {S['mid']}`：亮格 = `thief_dis ≥ {S['mid']}`；==蓝== = 从 `(0,0)` 已走到的格子"
    if 'right' in S and 'left' in S:
        return f"二分范围 `[{S['left']}, {S['right']}]`：上界 = 起点、终点安全系数的较小值"
    return '先从所有小偷出发 BFS，算每格离最近小偷的距离（青 = 小偷）'


CONFIG = dict(
    num=2812, title='找出最安全路径', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='多源 BFS + 二分 + BFS 判通', tags=['灵神题单·二分算法', '难度分 2154'],
    code='''
class Solution(object):
    def maximumSafenessFactor(self, grid):

        m = len(grid)
        n = len(grid[0])
        thief_dis = [[None] * n for _ in range(m)]

        q = []
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    q.append([i, j])
                    thief_dis[i][j] = 0
        
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        head, tail = 0, len(q)
        while head < tail:
            for nowx, nowy in q[head : tail]:
                for d in range(4):
                    x = nowx + dx[d]
                    y = nowy + dy[d]
                    if x >= 0 and x < m and y >= 0 and y < n and thief_dis[x][y] is None:
                        thief_dis[x][y] = thief_dis[nowx][nowy] + 1
                        q.append([x, y])
            
            head, tail = tail, len(q)
        

        left = 0
        right = min(thief_dis[0][0], thief_dis[m - 1][n - 1])
        while left < right:
            mid = (left + right + 1) // 2
            q = [[0, 0]]
            vis = [[False] * n for _ in range(m)]
            head, tail = 0, 1
            while head < tail:
                nowx, nowy = q[head]
                head += 1
                for d in range(4):
                    x = nowx + dx[d]
                    y = nowy + dy[d]
                    if x >= 0 and x < m and y >= 0 and y < n and thief_dis[x][y] >= mid and not vis[x][y]:
                        vis[x][y] = True
                        q.append([x, y])
                        tail += 1
                
                if vis[m - 1][n - 1]:
                    break
            
            if vis[m - 1][n - 1]:
                left = mid
            else:
                right = mid - 1
        
        return left
''',
    call='Solution().maximumSafenessFactor([[0,0,1],[0,0,0],[0,0,0]])',
    expect=2, max_steps=130,
    skip=['m = len(grid)', 'n = len(grid[0])', 'thief_dis = [[None]', 'q = []', 'for i in range(m)', 'for j in range(n)', 'if grid[i][j] == 1', 'dx = ', 'dy = ',
          'head, tail = 0, len(q)', 'for nowx, nowy in q[head', 'for d in range(4)', 'x = nowx', 'y = nowy', 'q.append', 'tail += 1', 'head += 1',
          'while head < tail', 'q = [[0, 0]]', 'vis = [[False]', 'head, tail = 0, 1', 'nowx, nowy = q[head]', 'is None:', 'head, tail = tail', 'thief_dis[x][y] >= mid', 48],
    views=[
        dict(type='table', var='thief_dis', h=380, cell=96,
             label='thief_dis[x][y]：到最近小偷的距离',
             cursors=[('nowx', 'nowy', 'yellow', '当前'), ('x', 'y', 'pink', '邻')],
             color=_col, dim=_dim),
        dict(type='text', h=90, fn=_txt),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow')],
    captions={
        'thief_dis[x][y] = thief_dis[nowx][nowy] + 1': '`({nowx},{nowy})` 的邻居 `({x},{y})`：距离 = ==`{thief_dis[x][y]}`==（比当前格多一步）',
        'left = 0': '二分安全系数：下界 `left = 0`（总是可行）',
        'right = min': '上界 = `min(起点, 终点的安全系数)` = ==`{right}`==：再大连起点或终点本身都不合格',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`：继续二分' if S.left < S.right else f'`left = right = {S.left}`：夹到答案'),
        'mid = (': '取偏大中点 `mid = ({left} + {right} + 1) // 2 = {mid}`，==+1== 防死循环；然后从 `(0,0)` BFS，只走 `thief_dis ≥ {mid}` 的格子',
        'vis[x][y] = True': '邻居 `({x},{y})` 的 `thief_dis = {thief_dis[x][y]} ≥ {mid}`，且没走过 → 标记走到，入队',
        'break': '终点已经走到 → 这一轮 BFS 提前结束',
        'if vis[m - 1][n - 1]:': lambda S, B, r: (f'终点 `({S.m-1},{S.n-1})` 走到了：安全系数 {S.mid} 可行' if S.vis[S.m-1][S.n-1] else f'终点没走到：只用 `thief_dis ≥ {S.mid}` 的格子到不了 → {S.mid} 不可行'),
        'left = mid': '终点走得到 → 安全系数 {mid} 可行：`left = {left}`',
        'right = mid - 1': '终点走不到 → {mid} 太高：`right = {right}`',
        'return left': '最大可行的安全系数 ==`{left}`==',
    },
    cards=dict(
        one_liner='安全系数越大越难走：二分它，再 BFS 看走不走得通',
        complexity='时间 `O(mn log(m+n))`，空间 `O(mn)`',
        problem=['网格里 `1` 是小偷，路径安全系数 = 路径上各格到最近小偷距离的最小值',
                 '求 `(0,0)` 到 `(m-1,n-1)` 的最大安全系数',
                 '示例：`[[0,0,1],[0,0,0],[0,0,0]]` → `2`'],
        quote='越安全的路径越难找，那么在这里就可以通过二分最终的安全系数，然后判断是否存在一条所有单元格的安全系数都大于等于mid的路径。',
        quote_src='—— yiduobo 题解原文',
        idea=['先从所有小偷同时 BFS，得到每格的 `thief_dis`',
              '上界取起点、终点 `thief_dis` 的较小值，保证二分到的 `mid` 对起点终点都合法',
              '对 `mid` 从 `(0,0)` 再 BFS，只走 `thief_dis ≥ mid` 的格子，走到终点就 `left = mid`'],
        summary=['时间 `O(mn · log(m+n))`，空间 `O(mn)`',
                 '原文为 Python 2 写法，`mid = (left + right + 1) / 2` 已改为 `//`；其余照搬',
                 '第一次 BFS 用 `head/tail` 一层一层扩，不需要额外的距离数组',
                 '起点被扩进队列时不检查它自己，所以上界必须先取 `min` 保证它合法',
                 '对比灵神：灵神从大到小用并查集增量合并，不用二分'],
    ),
)
