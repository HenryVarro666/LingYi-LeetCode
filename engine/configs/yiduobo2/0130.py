BOARD = ['XXXXX',
         'XOOXO',
         'XXXOO',
         'XOXXX']
RESULT = [list('XXXXX'), list('XXXXO'), list('XXXOO'), list('XOXXX')]


def _cell_color(S, i, j, v):
    if v == 'P':
        return 'green'
    if v == 'O':
        return 'green' if 'i' in S else 'blue'
    return None


def _cap_border(side):
    def f(S, B, ret):
        b = B.board
        idx = S.index
        m, n = S.m, S.n
        r, c = {'L': (idx, 0), 'R': (idx, n - 1), 'T': (0, idx), 'B': (m - 1, idx)}[side]
        if b[r][c] == 'O':
            return f'边界格 `({r},{c})` 是 ==O== → 它一定不会被围住：入队，标成 `P`'
        if b[r][c] == 'P':
            return f'边界格 `({r},{c})` 已经标过 P（角上的格子会被检查两次）'
        return f'边界格 `({r},{c})` 是 `X`，跳过'
    return f


def _cap_nb(S, B, ret):
    x, y, nx, ny = S.x, S.y, S.new_x, S.new_y
    m, n = S.m, S.n
    d = {(0, 1): '右', (-1, 0): '上', (0, -1): '左', (1, 0): '下'}[(nx - x, ny - y)]
    if not (0 <= nx < m and 0 <= ny < n):
        return f'{d}边 `({nx},{ny})` 出界'
    v = B.board[nx][ny]
    if v == 'O':
        return f'{d}边 `({nx},{ny})` 是 ==O== 且和边界连通 → 入队，标成 `P`'
    if v == 'P':
        return f'{d}边 `({nx},{ny})` 已经是 P，不重复入队'
    return f'{d}边 `({nx},{ny})` 是 `X`'


def _row_cap(S, B, ret):
    if S.get('i') is None or S.get('i') == B.get('i'):
        return '扫描完毕：==只有 P 恢复成 O==，其余（含被围住的 O）都成了 X'
    i = S.i
    if i == 0:
        return f'最后扫描整个矩阵：`P` → `O`，其它（包括没被标记的 O）→ `X`。先看第 `{i}` 行'
    return f'第 `{i - 1}` 行处理完；接着处理第 `{i}` 行'


CONFIG = dict(
    num=130, title='被围绕的区域', difficulty='Medium', category='图论',
    author='yiduobo', technique='从边界 O 出发 BFS 染色',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def solve(self, board):

        if not board:
            return

        m = len(board)
        n = len(board[0])

        q = []
        for index in range(m):
            if board[index][0] == 'O':
                q.append((index, 0))
                board[index][0] = 'P'
            if board[index][n - 1] == 'O':
                q.append((index, n - 1))
                board[index][n - 1] = 'P'

        for index in range(n):
            if board[0][index] == 'O':
                q.append((0, index))
                board[0][index] = 'P'
            if board[m - 1][index] == 'O':
                q.append((m - 1, index))
                board[m - 1][index] = 'P'

        left = 0
        right = len(q)
        dx = [0, -1, 0, 1]
        dy = [1, 0, -1, 0]
        while left < right:
            x, y = q[left]
            left += 1

            for index in range(4):
                new_x = x + dx[index]
                new_y = y + dy[index]
                if new_x >= 0 and new_x < m and new_y >= 0 and new_y < n and board[new_x][new_y] == 'O':
                    q.append((new_x, new_y))
                    board[new_x][new_y] = 'P'
                    right += 1

        for i in range(m):
            for j in range(n):
                if board[i][j] != 'P':
                    board[i][j] = 'X'
                else:
                    board[i][j] = 'O'
''',
    call=f'''board = [list(r) for r in {BOARD}]
Solution().solve(board)
board''',
    expect=RESULT,
    skip=[4, 13, 16, 21, 24, 27, 29, 30, 33, 35, 36, 37, 39, 41, 44, 45, 46, 47, 48],
    max_steps=80,
    views=[
        dict(type='grid', var='board', label='board（蓝 = O，绿 = P：和边界连通；黄框 = 出队格，粉框 = 邻居）', h=330, cell=78,
             color=_cell_color,
             cursors=[('x if 31 <= _line <= 41 else None', 'y', 'yellow'),
                      ('new_x if _line == 38 else None', 'new_y', 'pink')]),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']] if 'q' in S else None,
             label='q（BFS 队列，left 之前的已出队）', cell=82, pointers={'left': 'blue'},
             dim=lambda S, i, v: 'left' in S and i < S['left']),
        dict(type='text', fn=lambda S: ('思路：边界上的 O 和与它相连的 O ==不会被围住==，先把它们标成 P'
                                        if S.get('_line', 0) < 43 else '最后一趟扫描：P → O，其余 → X'), size=24, h=56),
    ],
    watch=[('m', 'm'), ('n', 'n'), ('(x, y)', '(x, y)', 'yellow'), ('left', 'left', 'blue'), ('right', 'right')],
    captions={
        'm = len(board)': '`m = {m}` 行',
        'n = len(board[0])': '`n = {n}` 列',
        'q = []': '先把==边界上的 O== 全部放进队列 q（用 list 朴素实现队列）',
        11: lambda S, B, r: (f'检查第 `{S.index}` 行的最左、最右两个边界格' if S.index != B.get('index') or 'index' not in B
                             else '左右两条边界检查完毕'),
        12: _cap_border('L'),
        14: '`({index},0)` 入队并标成 `P`',
        15: _cap_border('R'),
        17: '`({index},{n - 1})` 入队并标成 `P`',
        19: lambda S, B, r: (f'检查第 `{S.index}` 列的最上、最下两个边界格' if S.index != B.index
                             else '上下两条边界检查完毕'),
        20: _cap_border('T'),
        22: '`(0,{index})` 入队并标成 `P`',
        23: _cap_border('B'),
        25: '`({m - 1},{index})` 入队并标成 `P`',
        'right = len(q)': '边界上一共 `{right}` 个 O；BFS：`left` 是队首，`right` 是队尾',
        'while left < right': lambda S, B, r: (f'`left = {B.left} < right = {B.right}`：队列非空' if B.left < B.right
                                               else '队列空了：所有和边界连通的 O 都标成了 P'),
        'x, y = q[left]': '取出队首 `({x},{y})`，看它的上下左右',
        38: _cap_nb,
        40: '`({new_x},{new_y})` 标成 P 并入队，`right` + 1',
        43: _row_cap,
    },
    cards=dict(
        one_liner='从边界上的 O 出发染色，没被染到的 O 才是被围住的',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`m × n` 的矩阵由 `X` 和 `O` 组成，把所有==被 X 围住==的 O 区域改成 X（原地修改）',
                 '和边界上的 O 相连的 O ==不算被围住==',
                 '示例：`[[X,X,X,X],[X,O,O,X],[X,X,O,X],[X,O,X,X]]` → 只剩底边的 O',
                 '本视频：4 × 5 的矩阵，左边中间的 `O O` 被围住'],
        quote='种子染色法(floodfill)的某种变形。我们只需要==从边界上的O开始做BFS或者DFS==，找出所有未被标记过的相连的O，将其做好标记。',
        quote_src='—— yiduobo 题解原文',
        idea=['反过来想：先找==不会被围住==的 O —— 它们一定和边界上的 O 连通',
              '边界上的 O 全部入队并改成 `P`，BFS 把相连的 O 也改成 `P`',
              '最后扫描一遍：`P` → `O`，其余全变 `X`'],
        summary=['时间 `O(mn)`：每个格子最多入队一次',
                 '入队时==立刻标 P==，否则同一个格子会被重复入队',
                 '队列用 list + 左右指针实现（原文：性能可能会稍差一些），也可以用 `deque`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
