G = [[1, 2], [3, 4]]


def _cmp(di, dj, nm):
    def f(S, B, r):
        a = S.grid[S.i][S.j]
        b = S.grid[S.i + di][S.j + dj]
        if a > b:
            return f'比{nm}邻居高（`{a} > {b}`）→ 露出高出的一截 `{a} - {b}` = =={a - b}=='
        return f'不比{nm}邻居高（`{a} <= {b}`）→ 这一面被邻居挡住，贡献 ==0=='
    return f

CONFIG = dict(
    num=892, title='三维形体的表面积', difficulty='Easy', category='网格图',
    author='yiduobo', technique='逐格逐方向累加',
    tags=['灵神核心路线', '灵神题单·网格图'],
    code='''
class Solution(object):
    def surfaceArea(self, grid):

        res = 0
        m = len(grid)
        n = len(grid[0])

        for i in range(m):
            for j in range(n):
                if grid[i][j] > 0:
                    res += 2

                if i == 0:
                    res += grid[i][j]
                elif grid[i][j] > grid[i - 1][j]:
                    res += grid[i][j] - grid[i - 1][j]
                
                if i == m - 1:
                    res += grid[i][j]
                elif grid[i][j] > grid[i + 1][j]:
                    res += grid[i][j] - grid[i + 1][j]
                
                if j == 0:
                    res += grid[i][j]
                elif grid[i][j] > grid[i][j - 1]:
                    res += grid[i][j] - grid[i][j - 1]
                
                if j == n - 1:
                    res += grid[i][j]
                elif grid[i][j] > grid[i][j + 1]:
                    res += grid[i][j] - grid[i][j + 1]
        
        return res
''',
    call=f'Solution().surfaceArea({G})',
    expect=34,
    skip=['m = len', 'n = len'],
    views=[
        dict(type='grid', var='grid', label='grid[i][j] = 这一格叠了几个方块（黄框 = 当前格）', cell=110, h=330,
             cursors=[('i', 'j', 'yellow', '(i,j)')]),
        dict(type='text', size=30, h=70, fn=lambda S: f"累计表面积 `res` = =={S['res']}==" if 'res' in S else ''),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 0': '表面积从 0 开始累加，逐格、逐方向判断能贡献多少',
        'if grid[i][j] > 0': lambda S, B, r: (f'`grid[{S.i}][{S.j}] = {S.grid[S.i][S.j]} > 0`：上、下两个面各露出 1，共 =={2}==' if S.grid[S.i][S.j] > 0
                                              else '高度为 0，没有方块，上下都不贡献'),
        'if i == 0': lambda S, B, r: ('第 0 行：上侧没有邻居，整面墙都露出，贡献 `grid[i][j]` = =={}=='.format(S.grid[S.i][S.j]) if S.i == 0
                                      else f'`grid[{S.i}][{S.j}] = {S.grid[S.i][S.j]}`，上邻居高 `{S.grid[S.i-1][S.j]}`'),
        'grid[i][j] > grid[i - 1][j]': _cmp(-1, 0, '上'),
        'if i == m - 1': lambda S, B, r: ('最后一行：下侧没有邻居，整面墙露出，贡献 `grid[i][j]` = =={}=='.format(S.grid[S.i][S.j]) if S.i == S.m - 1
                                          else f'不是最后一行，要和下邻居 `{S.grid[S.i+1][S.j]}` 比'),
        'grid[i][j] > grid[i + 1][j]': _cmp(1, 0, '下'),
        'if j == 0': lambda S, B, r: ('第 0 列：左侧没有邻居，整面墙露出，贡献 `grid[i][j]` = =={}=='.format(S.grid[S.i][S.j]) if S.j == 0
                                      else f'不是第 0 列，要和左邻居 `{S.grid[S.i][S.j-1]}` 比'),
        'grid[i][j] > grid[i][j - 1]': _cmp(0, -1, '左'),
        'if j == n - 1': lambda S, B, r: ('最后一列：右侧没有邻居，整面墙露出，贡献 `grid[i][j]` = =={}=='.format(S.grid[S.i][S.j]) if S.j == S.n - 1
                                          else f'不是最后一列，要和右邻居 `{S.grid[S.i][S.j+1]}` 比'),
        'grid[i][j] > grid[i][j + 1]': _cmp(0, 1, '右'),
        'return res': '六个方向都累加完，表面积 =={res}==',
    },
    cards=dict(
        one_liner='每格每个方向，只数“比邻居高出来”的那一截墙',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`grid[i][j]` 表示该位置叠了几个 `1×1×1` 的方块',
                 '求整个立体形状的==表面积==（含底面、含中间镂空处的内壁）',
                 '示例：`[[1,2],[3,4]]` → `34`'],
        quote='这次是判断每个格子的每个方向是否会提供表面积。对于上方和下方，若当前格子上高度不为0，那么将分别提供1的表面积。',
        quote_src='—— yiduobo 题解原文',
        idea=['上下两面：只要这格有方块，各贡献 `1`，合计 `2`',
              '前后左右四面：在边界，整面墙露出，贡献 `grid[i][j]`',
              '不在边界：比邻居高才露出，贡献高度差，否则为 `0`',
              '镂空处的内壁同样算：邻居更矮的一侧会被数到'],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '易错：下标 `i+1`、`j+1` 要先判断是否到边界，再取邻居',
                 '只数高度差，不会把相邻方块之间被遮住的面重复计入',
                 '原文已是 Python 3 可运行写法，代码未改'],
    ),
)
