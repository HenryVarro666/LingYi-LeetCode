GRID = [[0, 3, 6], [5, 8, 1], [2, 7, 4]]


def _ycolor(S, i, j, v):
    if 'path' not in S or S['_line'] < 15 or 'dx' not in S:
        return None
    if v == S['i']:
        return 'pink'
    if v == S['i'] - 1:
        return 'blue'
    if v < S['i'] - 1:
        return 'green'
    return None


CONFIG = dict(
    num=2596, title='检查骑士巡视方案', difficulty='Medium', category='模拟',
    author='yiduobo', technique='按步数排序后逐步检查',
    tags=[],
    code='''
class Solution(object):
    def checkValidGrid(self, grid):

        n = len(grid)
        path = [[None, None] for _ in range(n * n)]
        for i in range(n):
            for j in range(n):
                index = grid[i][j]
                path[index][0] = i
                path[index][1] = j

        if path[0][0] != 0 or path[0][1] != 0:
            return False

        for i in range(1, n * n):
            dx = path[i][0] - path[i - 1][0]
            dy = path[i][1] - path[i - 1][1]
            if (abs(dx) == 2 and abs(dy) == 1) or (abs(dx) == 1 and abs(dy) == 2):
                continue
            return False
        
        return True
''',
    call=f'Solution().checkValidGrid({GRID})',
    expect=False,
    skip=['for i in range(n):', 'for j in range(n):', 'index = grid', 'path[index][1]', 'n = len(grid)', 'path = [['],
    views=[
        dict(type='grid', var='grid', label='grid（粉 = 当前这一步的格子，蓝 = 上一步，绿 = 已检查合法）', cell=120, h=400,
             cursors=[('i if _line < 12 else None', 'j', 'yellow')], color=_ycolor),
        dict(type='array', var=lambda S: [f'{a},{b}' if a is not None else '?' for a, b in S['path']] if 'path' in S else None,
             label='path[k] = [行, 列]：按步数 k 排好的坐标（None = 还没填）', cell=96, h=190,
             color=lambda S, i, v: ('pink' if 'dx' in S and S['_line'] >= 15 and i == S['i'] else
                                    'blue' if 'dx' in S and S['_line'] >= 15 and i == S['i'] - 1 else None)),
        dict(type='text', fn=lambda S: (f"`dx = {S['dx']}`，`dy = {S['dy']}`：|dx|、|dy| 要一个是 1、另一个是 2" if 'dx' in S and S['_line'] >= 16 else ''), h=70),
    ],
    watch=['i', 'j', ('dx', 'dx', 'yellow'), ('dy', 'dy', 'yellow')],
    captions={
        'path[index][0] = i': '`grid[{i}][{j}] = {index}`：第 {index} 步在 `({i}, {j})`，记进 `path[{index}]`；数字本身当下标，省掉排序',
        'if path[0][0] != 0': lambda S, B, r: ('起点 `path[0] = {}`：是 `(0, 0)`，合法'.format(S.path[0]) if S.path[0] == [0, 0]
                                                 else '起点 `path[0] = {}` 不是 `(0, 0)` → 不合法'.format(S.path[0])),
        'for i in range(1, n * n)': '第 `{i}` 步：能不能从第 `{i-1}` 步跳过来？（从第 1 步开始检查）',
        'dx = path[i][0]': '横坐标之差 `dx = {path[i][0]} - {path[i-1][0]} = {dx}`',
        'dy = path[i][1]': '纵坐标之差 `dy = {path[i][1]} - {path[i-1][1]} = {dy}`',
        'if (abs(dx) == 2': lambda S, B, r: ('`|dx|={}`、`|dy|={}`：一个 2 一个 1 → 能跳过来，`continue`'.format(abs(S.dx), abs(S.dy))
                                              if sorted((abs(S.dx), abs(S.dy))) == [1, 2] else
                                              '`|dx|={}`、`|dy|={}`：不是 (2,1) 也不是 (1,2) → ==跳不过来=='.format(abs(S.dx), abs(S.dy))),
        'continue': '这一步合法，检查下一步',
        'return False': lambda S, B, r: ('起点不是 `(0, 0)`，返回 `False`' if S._line == 13 else '第 {} 步到不了，直接返回 ==False=='.format(S.i)),
        'return True': '每一步都跳得过来，返回 `True`',
    },
    cards=dict(
        one_liner='先把格子按步数排成一条路径，再逐步检查能不能跳过去',
        complexity='时间 `O(n²)`，空间 `O(n²)`',
        problem=['`n×n` 的棋盘，`grid[i][j]` 是骑士第几步到 `(i, j)`，从左上角出发',
                 '判断整条路线是不是都符合骑士「日」字走法',
                 '示例：`[[0,3,6],[5,8,1],[2,7,4]]` → `false`'],
        quote='首先检测起点是否为(0, 0)。接下来，从下标1开始向后遍历，每次检测当前位置是否能从序列的上一个位置跳跃过来，也就是横坐标之差dx以及纵坐标之差dy中，有一个绝对值为1，另一个绝对值为2。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历整个棋盘，把位置收集到 `path`，==数值当下标==，不用排序',
              '起点 `path[0]` 必须是 `(0, 0)`',
              '从下标 1 起，相邻两个位置的 `|dx|`、`|dy|` 必须是 1 和 2'],
        summary=['时间、空间都是 `O(n²)`',
                 '易错：别忘了检查起点；`dx`、`dy` 要取绝对值',
                 '一旦有一步不合法，立刻返回 `False`',
                 '代码未改，原文已是 Python 3 可运行的写法'],
    ),
)
