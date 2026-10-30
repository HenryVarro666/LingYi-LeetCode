G0 = [[0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0]]


def _col(S, i, j, v):
    return 'cyan' if v == 1 else None


def _side(name, cond):
    def f(S, B, r):
        i, j, g = S.i, S.j, S.grid
        m, n = len(g), len(g[0])
        if cond(i, j, g, m, n):
            return f'{name}：出界或邻居是水 → ==这条边计入周长==，下一步 `res += 1`'
        return f'{name}：邻居是陆地 → 这条边不计'
    return f


CONFIG = dict(
    num=463, title='岛屿的周长', difficulty='Easy', category='网格图',
    author='yiduobo', technique='逐格检验四条边',
    tags=['灵神核心路线', '灵神题单·网格图'],
    code='''
class Solution(object):
    def islandPerimeter(self, grid):

        res = 0

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 1:
                    if i == 0 or grid[i - 1][j] == 0:
                        res += 1
                    if j == 0 or grid[i][j - 1] == 0:
                        res += 1
                    if i == len(grid) - 1 or grid[i + 1][j] == 0:
                        res += 1
                    if j == len(grid[0]) - 1 or grid[i][j + 1] == 0:
                        res += 1

        return res
''',
    call=f'Solution().islandPerimeter({G0})',
    expect=12,
    skip=['res = 0', 'for i in range', 'for j in range'],
    max_steps=80,
    views=[
        dict(type='grid', var='grid', label='grid（青 = 陆地；黄框 = 当前格子）', cell=96, h=330,
             color=_col, cursors=[('i', 'j', 'yellow')]),
        dict(type='text', fn=lambda S: f"res = =={S['res']}==" if 'res' in S else '', size=34, h=60),
    ],
    watch=['i', 'j', ('res', 'res', 'green')],
    captions={
        'if grid[i][j] == 1': lambda S, B, r: (f'`({S.i},{S.j})` 是陆地 → 检验它的四条边' if S.grid[S.i][S.j] == 1
                                               else f'`({S.i},{S.j})` 是水 → 跳过'),
        'if i == 0': _side('上边', lambda i, j, g, m, n: i == 0 or g[i-1][j] == 0),
        'if j == 0': _side('左边', lambda i, j, g, m, n: j == 0 or g[i][j-1] == 0),
        'if i == len(grid) - 1': _side('下边', lambda i, j, g, m, n: i == m-1 or g[i+1][j] == 0),
        'if j == len(grid[0]) - 1': _side('右边', lambda i, j, g, m, n: j == n-1 or g[i][j+1] == 0),
        'return res': '全部格子检验完，周长 =={res}==',
    },
    cards=dict(
        one_liner='陆地靠水或靠边界的那条边，就计入周长',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`1` 是陆地，`0` 是水域；网格只有一个岛屿，没有湖',
                 '求岛屿的周长',
                 '示例：`[[0,1,0,0],[1,1,1,0],[0,1,0,0]]` → `12`'],
        quote='若其位于最左侧那一列，或者其左侧单元格为水域，那么这块陆地的左边就应该计入到周长当中。',
        quote_src='—— yiduobo 题解原文',
        idea=['对一块陆地，逐个检查左、右、上、下四条边',
              '在边界上，或者另一侧是水域，这条边就算周长',
              '遍历所有单元格，累加即可，不需要搜索'],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '易错：先判断是否在边界，再访问邻居，避免下标越界',
                 '上、左、下、右四条边判断规则完全对称',
                 '原文已是 Python 3 可运行写法，代码未改'],
    ),
)
