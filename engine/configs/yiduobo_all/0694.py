GRID = [[1, 1, 0, 0, 0], [1, 0, 0, 1, 1], [0, 0, 0, 1, 0], [1, 1, 0, 0, 0]]
ORIG = [row[:] for row in GRID]
ARROW = '→↓←↑'


def _path_arr(S):
    p = S.get('path')
    return None if p is None else list(p)


def _fmt_p(v):
    return ARROW[v] + '' if v < 4 else '回' + ARROW[v - 4]


def _color(S, i, j, v):
    if 'grid' not in S:
        return None
    if ORIG[i][j] == 1 and v == 0:
        return 'green'
    return None


def _nb(S, B, r):
    x, y = S.x, S.y
    if not (0 <= x < S.m and 0 <= y < S.n):
        return f'方向 {S.index} 走到 `({x},{y})` 越界，换下一个方向'
    if S.grid[x][y] == 1:
        return f'方向 {S.index}（{ARROW[S.index]}）走到 `({x},{y})`：是没走过的陆地 → ==走过去=='
    return f'方向 {S.index}（{ARROW[S.index]}）走到 `({x},{y})`：水或已走过，不走'


def _paths(S):
    ps = S.get('path_set')
    return None if ps is None else sorted(ps)


CONFIG = dict(
    num=694, title='不同岛屿的数量', difficulty='Medium', category='网格图',
    author='yiduobo', technique='DFS 序列化岛屿形状',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def numDistinctIslands(self, grid):

        vis = set()
        path_set = set()

        m = len(grid)
        n = len(grid[0])

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        def dfs(nowx, nowy):
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if 0 <= x < m and 0 <= y < n and grid[x][y] == 1:
                    grid[x][y] = 0
                    path.append(index)
                    dfs(x, y)
                    path.append(index + 4)

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    grid[i][j] = 0
                    path = []
                    dfs(i, j)
                    path_set.add(''.join([str(x) for x in path]))

        return len(path_set)
''',
    call=f'Solution().numDistinctIslands({GRID})',
    expect=2,
    skip=['vis = set()', 'path_set = set()', 'm = len', 'n = len', 'dx = [', 'dy = [', 'for i in range(m)',
          'for j in range(n)', 'for index in range(4)', 'x = nowx', 'y = nowy'],
    views=[
        dict(type='grid', var='grid', label='grid（绿 = 已被 DFS 走过的陆地；蓝框 = 当前格；粉框 = 正在看的邻居）', cell=100, h=400,
             color=_color, cursors=[('nowx', 'nowy', 'blue'),
                                    ('x if _line == 17 else None', 'y', 'pink'),
                                    ('i if _line in (25, 26, 27, 28) else None', 'j', 'yellow')]),
        dict(type='array', var=_path_arr, label='path（0~3 = 向 右/下/左/上 前进，4~7 = 对应方向的回溯）', cell=64, h=170),
        dict(type='set', var=lambda S: S.get('path_set'), label='path_set（已出现的岛屿形状）', fmt=lambda x: x, font=30, h=150),
    ],
    max_steps=56,
    watch=[('i', 'i'), ('j', 'j'), ('nowx', 'nowx', 'blue'), ('nowy', 'nowy', 'blue'), ('len(path_set)', 'len(path_set)', 'green')],
    captions={
        'grid[x][y] == 1': _nb,
        'grid[x][y] = 0': '`({x},{y})` 标成 0：既当 ==visited==，也避免重复进入',
        'path.append(index)': '记下这一步的前进方向 `{index}`（{ARROW[index]}），再递归进去',
        'dfs(x, y)': '进入 `({x},{y})`，继续向四个方向探',
        'path.append(index + 4)': '这一层探完回到上一格：补一个 `{index+4}` 作为==回溯标记==，保证序列唯一',
        'path = []': '发现新岛屿的起点 `({i},{j})`：清空 `path`，从这里开始记录行走过程',
        'path_set.add': lambda S, B, r: f'整座岛走完，序列 `{"".join(str(c) for c in S.path)}` 加入集合；集合大小 ==`{len(S.path_set)}`==',
        'return len': '集合里有 `{len(path_set)}` 种不同的序列 → 答案 `{len(path_set)}`',
    },
    cards=dict(
        one_liner='把岛屿的 DFS 行走序列当作形状指纹，放进集合去重',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`grid` 中 1 是陆地，上下左右相连的 1 构成岛屿',
                 '两座岛==能通过平移重合==才算相同，求不同岛屿的数量',
                 '示例：`[[1,1,0,0,0],[1,0,0,1,1],[0,0,0,1,0],[1,1,0,0,0]]`',
                 '→ `2`（两个 L 形相同，另一个是横条）'],
        quote='如果使用dfs，则可以通过dfs序的方式得到唯一的生成序列，是更符合题目需求的。这里的dfs指的是从当前格子向哪个方向进行了移动。',
        quote_src='—— yiduobo 题解原文',
        idea=['按行优先找到岛屿的第一个格子作基准，从它出发 DFS',
              '每向某方向走一步记 `0~3`，探完返回记 `index+4`',
              '序列相同 == 行走过程相同 == 岛屿形状相同，转成字符串入集合'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '易错：必须记录回溯标记，否则 `右下` 和 `下右` 之类不同形状可能得到相同序列',
                 '不用坐标差编码，避开了两位数坐标带来的拼接歧义',
                 '原文代码是 Python 3 可运行的写法，未做修改；`vis` 变量原文定义了但没用到'],
    ),
)
