GRID = [[0, 3, 6], [5, 8, 1], [2, 7, 4]]


def _ccolor(S, i, j, v):
    if 'pos' not in S or S['_line'] < 9 or 'x' not in S:
        return None
    k = S['grid'][S['i']][S['j']]
    if v < k:
        return 'green'
    return None


CONFIG = dict(
    num=2596, title='检查骑士巡视方案', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='记录坐标 + 相邻两步模拟',
    tags=[],
    code='''
class Solution:
    def checkValidGrid(self, grid: List[List[int]]) -> bool:
        pos = [0] * (len(grid) ** 2)
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                pos[x] = (i, j)  # 记录坐标
        if pos[0] != (0, 0):  # 必须从左上角出发
            return False
        for (i, j), (x, y) in pairwise(pos):
            dx, dy = abs(x - i), abs(y - j)  # 移动距离
            if (dx != 2 or dy != 1) and (dx != 1 or dy != 2):  # 不合法
                return False
        return True
''',
    call=f'Solution().checkValidGrid({GRID})',
    expect=False,
    skip=['for i, row in enumerate', 'for j, x in enumerate'],
    views=[
        dict(type='grid', var='grid', label='grid（格子里的数 = 第几步；蓝 = 这步的起点，粉 = 终点，绿 = 已走合法的格子）', cell=120, h=400,
             cursors=[('i if _line >= 9 else None', 'j', 'blue'), ('x if _line >= 9 else None', 'y', 'pink')],
             color=_ccolor),
        dict(type='array', var=lambda S: [f'{a},{b}' if p != 0 else '?' for p in S['pos'] for a, b in [p if p != 0 else (0, 0)]] if 'pos' in S else None,
             label='pos[k] = 第 k 步所在的格子 (行,列)', cell=96, h=190),
        dict(type='text', fn=lambda S: (f"移动距离 `dx = {S['dx']}`，`dy = {S['dy']}`：{'是日字' if sorted((S['dx'], S['dy'])) == [1, 2] else '==不是日字=='}"
                                        if 'dx' in S and S['_line'] >= 10 else ''), h=70),
    ],
    watch=['i', 'j', 'x', 'y', ('dx', 'dx', 'yellow'), ('dy', 'dy', 'yellow')],
    captions={
        'pos = [0] *': '准备 `pos`：`pos[k]` 放「第 k 步」的坐标，共 `n²` 个',
        'pos[x] = (i, j)': '扫表：`grid[{i}][{j}] = {x}`，第 {x} 步在 `({i}, {j})` → `pos[{x}] = ({i}, {j})`，按走的顺序排好',
        'if pos[0] != (0, 0)': lambda S, B, r: ('`pos[0] = {}`：从左上角 `(0, 0)` 出发，合法'.format(S.pos[0]) if S.pos[0] == (0, 0)
                                                 else '`pos[0] = {}` 不是左上角，直接不合法'.format(S.pos[0])),
        'return False': lambda S, B, r: ('起点不对，返回 `False`' if S._line == 8 else '这一步不是「日」字，骑士走不了，返回 ==False=='),
        'for (i, j), (x, y)': '看相邻两步：从 `({i}, {j})` 走到 `({x}, {y})`',
        'dx, dy = abs': '行差 `dx = |{x} - {i}| = {dx}`，列差 `dy = |{y} - {j}| = {dy}`',
        'if (dx != 2': lambda S, B, r: ('`({},{})`：一个是 2 另一个是 1，是合法的「日」字走法'.format(S.dx, S.dy) if sorted((S.dx, S.dy)) == [1, 2]
                                         else '`({},{})` 不是 (2,1) 也不是 (1,2) → ==不合法=='.format(S.dx, S.dy)),
        'return True': '所有相邻两步都合法，返回 `True`',
    },
    cards=dict(
        one_liner='把每一步的坐标按顺序排好，逐对检查是不是「日」字',
        complexity='时间 `O(n²)`，空间 `O(n²)`',
        problem=['`n×n` 棋盘，`grid[r][c]` 表示骑士第几步到 `(r, c)`，要求从左上角出发、走遍每格一次',
                 '每一步必须是国际象棋骑士的走法：一个方向 2 格、另一个方向 1 格',
                 '示例：`[[0,3,6],[5,8,1],[2,7,4]]` → `false`（第 7 步到第 8 步走不了）'],
        quote='按题意模拟。代码实现时，可以把每个值的坐标记录到一个数组中，方便判断。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`pos[x] = (i, j)`：把「第几步」当下标，坐标当值，省掉排序',
              '先看 `pos[0]` 是不是 `(0, 0)`',
              '`pairwise(pos)` 取相邻两步，`dx, dy` 必须是 `(2,1)` 或 `(1,2)`'],
        summary=['时间、空间都是 `O(n²)`',
                 '易错：别漏了起点必须是左上角 `(0, 0)` 的判断',
                 '日字判断：`(dx != 2 or dy != 1) and (dx != 1 or dy != 2)` 才是不合法',
                 '`pairwise` 来自 `itertools`，每次给出相邻两项'],
    ),
)
