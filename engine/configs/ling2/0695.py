GRID = [[1, 1, 0],
        [0, 1, 0],
        [1, 0, 0]]


def _gcolor(S, i, j, v):
    if v == 1:
        return 'blue'
    if GRID[i][j] == 1:
        return 'green'   # 原来是陆地，已被标记成 0
    return None


def _nb(S, B, ret):
    x, y, m, n = S.x, S.y, S.m, S.n
    if not (0 <= x < m and 0 <= y < n):
        return f'邻居 `({x},{y})` ==出界== → 不管'
    if B.grid[x][y]:
        return f'邻居 `({x},{y})` 是没访问过的陆地 → 交给下属去统计'
    if GRID[x][y]:
        return f'邻居 `({x},{y})` 已经标记过（0）→ 不重复统计'
    return f'邻居 `({x},{y})` 是水 → 不管'


def _scan(S, B, ret):
    i, j = S.i, S.j
    if S.x:
        return f'`({i},{j})` 是陆地且没访问过 → 从这里==登陆==，DFS 统计整座岛的面积'
    if GRID[i][j]:
        return f'`({i},{j})` 已被标记成 0（属于前面的岛）→ 跳过'
    return f'`({i},{j})` 是水 → 跳过'


CONFIG = dict(
    num=695, title='岛屿的最大面积', difficulty='Medium', category='图论',
    author='灵茶山艾府', technique='网格图 DFS · 返回面积',
    tags=['字节30天', '热题173'],
    code='''
class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        def dfs(i: int, j: int) -> int:
            area = 1  # (i,j) 这个格子
            grid[i][j] = 0  # 标记 (i,j) 访问过
            for x, y in (i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j):  # 左右上下
                if 0 <= x < m and 0 <= y < n and grid[x][y]:
                    # 把统计岛屿面积的任务交给其他人去处理，自己只需累加其他人统计出来的岛屿面积
                    area += dfs(x, y)
            return area
        ans = 0
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                if x:  # 是陆地，且之前没有访问过
                    ans = max(ans, dfs(i, j))
        return ans
''',
    call=f'Solution().maxAreaOfIsland({GRID})',
    expect=3,
    skip=['for x, y in', 'for i, row in', 'for j, x in'],
    views=[
        dict(type='text', fn=lambda S: '蓝 = 未访问陆地　绿 = 已访问（标成 0）　黄框 = `(i,j)`　粉框 = 邻居', size=24),
        dict(type='grid', var='grid', cell=110, h=380, color=_gcolor,
             cursors=[('i', 'j', 'yellow', '(i,j)'), ('x', 'y', 'pink')]),
        dict(type='calls', label='递归调用栈（每层 dfs 负责一片）', h=220),
    ],
    watch=[('当前层 area', 'area', 'cyan'), ('最大面积 ans', 'ans', 'green')],
    captions={
        'm, n = len': '网格 `{m}` 行 `{n}` 列；`1` 是陆地，`0` 是水',
        'area = 1': '登陆 `({i},{j})`：`area = 1`，先算上==自己这一格==',
        'grid[i][j] = 0': '`({i},{j})` 改成 0：==标记访问过==，之后不会被重复统计',
        'if 0 <= x < m': _nb,
        'area += dfs(x, y)': lambda S, B, ret: f'`dfs({B.x},{B.y})`：把那一片的面积==交给下属==统计，自己等着累加',
        'return area': '`({i},{j})` 负责的这一片统计完：向上汇报面积 =={ret}==',
        'ans = 0': '`ans` 记录最大的岛屿面积',
        'if x:': _scan,
        'ans = max(ans, dfs(i, j))': lambda S, B, ret: f'`dfs({B.i},{B.j})` 返回整座岛的面积，再和 `ans = {B.ans}` 取最大',
        'return ans': '所有格子扫描完，最大面积 =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='DFS 登陆一座岛，下属汇报的面积 + 1 就是这一片的面积',
        complexity='时间 `O(mn)`，空间 `O(mn)`（递归栈）',
        problem=['`m × n` 的二进制矩阵 `grid`，上下左右相连的 `1` 组成一座==岛屿==',
                 '岛屿面积 = 岛上 `1` 的个数；返回==最大==的岛屿面积，没有岛返回 0',
                 '本视频：`[[1,1,0],[0,1,0],[1,0,0]]` → 两座岛，面积 3 和 1 → `3`'],
        quote='我们从岛屿的某个位置 (i,j) 登陆，然后一分为四，把统计岛屿面积的任务交给其他人去处理，自己只需累加其他人统计出来的岛屿面积，再加上 1，即 (i,j) 这个格子。',
        quote_src='—— 灵茶山艾府题解',
        idea=['做法同 200. 岛屿数量：DFS 时把访问过的格子改成 0，防止重复',
              '`dfs(i, j)` 返回这一片的面积：`1` + 四个方向下属汇报的面积',
              '遍历每个格子，遇到 1 就 DFS，答案取所有岛面积的最大值'],
        result='两座岛面积分别是 `3` 和 `1` → 返回 `3` ✓',
        summary=['时间 `O(mn)`；空间 `O(mn)`：蛇形岛的递归深度可达 `mn`',
                 '易错：标记要写在递归==之前==，否则相邻格子互相递归，无限循环',
                 '先判断 `0 <= x < m and 0 <= y < n` 再读 `grid[x][y]`（`and` 短路防越界）',
                 '`for j, x in enumerate(row)` 读的是实时值：已标记成 0 的格子会被跳过'],
    ),
)
