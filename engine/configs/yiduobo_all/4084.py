GRID = [list('RRDLL'), list('DLLUD'), list('RRRDU'), list('LLLLU')]

ARROW = {'L': '←', 'R': '→', 'U': '↑', 'D': '↓'}


def _col(S, i, j, v):
    if 'vis' not in S:
        return None
    if (i, j) == (S['x'], S['y']):
        return 'yellow'
    if (i, j) in S['vis']:
        return 'green'
    return None


def _chk(S, B, r):
    nx, ny = S.nxt_x, S.nxt_y
    if nx < 0 or nx >= S.m or ny < 0 or ny >= S.n:
        return f'下一格 `({nx},{ny})` ==越界== → 停止，答案是当前格 `({S.x},{S.y})`'
    if (nx, ny) in S.vis:
        return f'下一格 `({nx},{ny})` ==已访问过== → 停止，答案是当前格 `({S.x},{S.y})`'
    return f'下一格 `({nx},{ny})` 在界内且没访问过 → 可以走'


CONFIG = dict(
    num=4084, title='有向网格中的最后访问单元格', difficulty='Medium', category='模拟',
    author='yiduobo', technique='哈希表标记 + 直接模拟',
    code='''
class Solution(object):
    def lastVisitedCell(self, grid):
        
        m = len(grid)
        n = len(grid[0])
        x, y = 0, 0
        
        dx = {'R': 0, 'L': 0, 'U': -1, 'D': 1}
        dy = {'R': 1, 'L': -1, 'U': 0, 'D': 0}
        vis = set([(0, 0)])
        while True:
            d = grid[x][y]
            nxt_x, nxt_y = x + dx[d], y + dy[d]
            if nxt_x < 0 or nxt_x >= m or nxt_y < 0 or nxt_y >= n or (nxt_x, nxt_y) in vis:
                break

            x, y = nxt_x, nxt_y
            vis.add((x, y))
        
        return x, y
''',
    call=f'Solution().lastVisitedCell({GRID})',
    expect=(3, 0),
    skip=['m = len', 'n = len', 'dx = {', 'dy = {', 'while True', 'd = grid'],
    views=[
        dict(type='grid', var='grid', label='grid（黄 = 当前所在格，绿 = 已访问）', cell=100, h=440,
             color=_col, cursors=[('x', 'y', 'yellow')]),
        dict(type='set', var='vis', label='vis（已访问的格子）', fmt=lambda p: f'{p[0]},{p[1]}', h=240),
    ],
    watch=[('x,y', '(x, y)', 'yellow'), ('d', 'd', 'blue'), ('下一格', '(nxt_x, nxt_y)', 'pink')],
    captions={
        'x, y = 0, 0': '从 `(0, 0)` 出发',
        'vis = set': '出发格算已访问：`vis = {{(0, 0)}}`',
        'nxt_x, nxt_y =': '`({x},{y})` 的指令是 `{d}` → 下一格 `({nxt_x},{nxt_y})`',
        'if nxt_x < 0': _chk,
        'break': '不能走了，这一步不执行，循环结束',
        'x, y = nxt_x, nxt_y': '真正走过去：`({x},{y})`',
        'vis.add': '`({x},{y})` 记入 `vis`，之后再进入就算重复',
        'return x, y': '最后访问的格子是 `({x},{y})`',
    },
    cards=dict(
        one_liner='按格子里的箭头一路走，撞墙或走回头路就停',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`m × n` 的网格，每格是 `L R U D` 之一，表示往哪个方向走一格',
                 '从 `(0,0)` 出发（已访问），每步按当前格的字符移动',
                 '若下一步越界或进入已访问的格子，停止且这一步不执行',
                 '返回最后访问的格子坐标'],
        quote='使用一个哈希表vis记录已经访问过的单元格，然后按照题意不断模拟移动即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`dx`、`dy` 两个字典把字符翻译成行列偏移',
              '每次先算出下一格，检查越界或已访问，再决定是否移动',
              '移动后立刻加入 `vis`，所以走回头路会被拦下'],
        summary=['时间 `O(mn)`：每个格子最多访问一次，之后必然停止',
                 '先检查再移动：停下时 `x, y` 仍是最后一个合法格子',
                 '返回的是元组 `(x, y)`，行在前、列在后',
                 '原文为 Python 2 风格，代码未改'],
    ),
)
