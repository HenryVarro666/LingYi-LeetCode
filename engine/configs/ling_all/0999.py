BOARD = [list(r) for r in ['........', '...p....', '...p....', 'pp.R.pB.', '........', '...B....', '...p....', '........']]


def _dname(dx, dy):
    return {(0, -1): '左', (0, 1): '右', (-1, 0): '上', (1, 0): '下'}.get((dx, dy), '')


def _color(S, i, j, v):
    if v == 'R':
        return 'blue'
    if v == 'p':
        return 'pink'
    if v == 'B':
        return 'purple'
    return None


def _stop(S, B, r):
    x, y = S.x, S.y
    d = _dname(S.dx, S.dy)
    if not (0 <= x < 8 and 0 <= y < 8):
        return f'往{d}走到 `({x},{y})`：==出界==，这个方向到头了'
    c = S.board[x][y]
    if c == '.':
        return f'往{d}走到 `({x},{y})` 是空格 → 车可以继续往{d}'
    return f'往{d}走到 `({x},{y})` 是 `{c}`，不是空格 → ==被挡住==，停下'


def _end(S, B, r):
    x, y = S.x, S.y
    if not (0 <= x < 8 and 0 <= y < 8):
        return f'停在界外，这个方向没有卒 → `ans` 不变 = {S.ans}'
    c = S.board[x][y]
    if c == 'p':
        return f'挡住车的是卒 `p`（`({x},{y})`）→ 车能吃到它，`ans` = =={S.ans + 1}=='
    return f'挡住车的是象 `B`（`({x},{y})`）→ 自己人，吃不到，`ans` 不变 = {S.ans}'


CONFIG = dict(
    num=999, title='可以被一步捕获的棋子数', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='枚举四个方向 · 走到被挡',
    tags=[],
    code='''
class Solution:
    def numRookCaptures(self, board: List[List[str]]) -> int:
        SIZE = 8
        for i, row in enumerate(board):
            for j, c in enumerate(row):
                if c == 'R':
                    x0, y0 = i, j
        ans = 0
        for dx, dy in (0, -1), (0, 1), (-1, 0), (1, 0):
            x, y = x0 + dx, y0 + dy
            while 0 <= x < SIZE and 0 <= y < SIZE and board[x][y] == '.':
                x += dx
                y += dy
            if 0 <= x < SIZE and 0 <= y < SIZE and board[x][y] == 'p':
                ans += 1
        return ans
''',
    call=f'Solution().numRookCaptures({BOARD})',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: ('白车 `R` 在 `(%d,%d)`：往 ==%s== 走，遇到 `B` 或界外就停；停在 `p` 才算吃到' % (S['x0'], S['y0'], _dname(S['dx'], S['dy']))) if 'dx' in S else ('先扫一遍棋盘找到白车 `R`（蓝）；`p` 粉色，`B` 紫色' if 'x0' not in S else '车在 `(%d,%d)`，接下来往四个方向走' % (S['x0'], S['y0']))),
        dict(type='grid', var='board', cursors=[('x', 'y', 'yellow', '(x,y)')], color=_color, h=520, cell=62),
    ],
    watch=[('x0', 'x0', 'blue'), ('y0', 'y0', 'blue'), 'dx', 'dy', 'x', 'y', ('ans', 'ans', 'green')],
    skip=['for j, c in enumerate', "if c == 'R'", 'for i, row', 'SIZE = 8'],
    captions={
        'x0, y0 = i, j': '找到白车 `R`：位置 `(x0, y0) = ({x0}, {y0})`',
        'ans = 0': '`ans` 记录车能吃到的卒数，初始为 0',
        'for dx, dy in': '换一个方向：`(dx, dy) = ({dx}, {dy})`',
        'x, y = x0 + dx': '从车旁边的第一格出发：`(x, y) = ({x}, {y})`',
        'while 0 <=': _stop,
        'x += dx': '空格不挡路，往前进一格：`x += dx` → {x}',
        'y += dy': '`y += dy` → {y}，来到 `({x}, {y})`，回头再判断这一格',
        "board[x][y] == 'p'": _end,
        'ans += 1': '吃到一个卒：`ans` = =={ans}==',
        'return ans': '四个方向都走完，车能吃到 `{ans}` 个卒',
    },
    cards=dict(
        one_liner='找到车，往四个方向一格一格走，停在卒上就 +1',
        complexity='时间 `O(L^2)`（L=8），空间 `O(1)`',
        problem=['`8×8` 棋盘上只有一个白车 `R`，还有白象 `B`、黑卒 `p`，`.` 是空格',
                 '车能上下左右移动，不能穿过其他棋子；一步内能吃掉的卒有几个？',
                 '示例：车在第 3 行，左右上方各有一个卒可吃，下方被象挡住 → `3`'],
        quote='枚举往左右上下四个方向移动。一步一步走，只要没有出界且是空方块，就继续走。如果移动到卒（p）的位置，答案加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先遍历棋盘，找到车的位置 `(x0, y0)`',
              '四个方向向量 `(dx, dy)` 逐个试，一步步走过空格',
              '停下时如果正好在棋盘内且是 `p`，答案加一；是 `B` 或出界则不加'],
        summary=['时间 `O(L^2)`：找车 `L^2`，四个方向各最多走 `L` 步',
                 '易错：停下后要先判出界，再看 `board[x][y]`，否则越界',
                 '易错：象 `B` 也会挡路，但吃不到它',
                 '模板：四方向向量 + 走到不满足条件为止，网格模拟常用'],
    ),
)
