BOARD = [['.', '.', '.', '.', '.'],
         ['.', '.', 'W', '.', '.'],
         ['B', 'W', 'W', '.', '.'],
         ['.', '.', '.', '.', '.'],
         ['.', '.', '.', '.', '.']]


def _col(S, i, j, v):
    if v == 'B':
        return 'orange'
    if v == 'W':
        return 'cyan'
    return None


def _first(S, B, r):
    if S.x < 0 or S.x >= S.m or S.y < 0 or S.y >= S.n:
        return f'方向 `({S.dx},{S.dy})`：下一格 `({S.x},{S.y})` ==出界== → 换方向'
    c = S.board[S.x][S.y]
    if c == '.':
        return f'方向 `({S.dx},{S.dy})`：下一格 `({S.x},{S.y})` 是空格 → 不成线段，换方向'
    if c == S.color:
        return f'方向 `({S.dx},{S.dy})`：下一格与 `color` 同色 → 线段中间没有异色格，换方向'
    return f'方向 `({S.dx},{S.dy})`：下一格是异色 `{c}` → 继续往前找同色端点'


def _walk(S, B, r):
    if S.x < 0 or S.x >= S.m or S.y < 0 or S.y >= S.n:
        return f'走到 `({S.x},{S.y})`：出界 → 这个方向没有好线段'
    c = S.board[S.x][S.y]
    if c == '.':
        return f'走到 `({S.x},{S.y})`：空格 → 线段断了，换方向'
    if c == S.color:
        return f'走到 `({S.x},{S.y})`：遇到同色 `{c}` → 两端同色、中间全是异色 → ==好线段=='
    return f'走到 `({S.x},{S.y})`：仍是异色 `{c}`，继续'


CONFIG = dict(
    num=1958, title='检查操作是否合法', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='枚举八个方向',
    tags=[],
    code='''
class Solution:
    def checkMove(self, board: List[List[str]], rMove: int, cMove: int, color: str) -> bool:
        m, n = len(board), len(board[0])
        for dx, dy in (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1):
            x, y = rMove + dx, cMove + dy
            if x < 0 or x >= m or y < 0 or y >= n or board[x][y] == '.' or board[x][y] == color:
                continue
            while True:
                x += dx
                y += dy
                if x < 0 or x >= m or y < 0 or y >= n or board[x][y] == '.':
                    break
                if board[x][y] == color:
                    return True
        return False
''',
    call=f"Solution().checkMove({BOARD}, 2, 3, 'B')",
    expect=True,
    views=[
        dict(type='grid', var='board', h=420, cell=96, color=_col,
             cursors=[('rMove', 'cMove', 'yellow', '落子'), ('x', 'y', 'pink', '探')]),
        dict(type='text', fn=lambda S: (f"落子 `({S['rMove']},{S['cMove']})` 涂 `{S['color']}`，当前方向 `({S['dx']},{S['dy']})`" if 'dx' in S else f"落子 `({S['rMove']},{S['cMove']})` 涂 `{S['color']}`")),
    ],
    watch=['dx', 'dy', 'x', 'y', 'color'],
    captions={
        'm, n = len': '棋盘 `{m} × {n}`（题目是 8×8，这里用小棋盘演示）',
        'for dx, dy': '枚举八个方向之一：`(dx, dy) = ({dx}, {dy})`',
        'x, y = rMove': '从落子点往 `({dx},{dy})` 方向迈第一步 → `({x}, {y})`',
        'if x < 0 or x >= m or y < 0 or y >= n or board[x][y] == \'.\' or board[x][y] == color': _first,
        'continue': '第一步不满足 → ==好线段至少 3 格==，这个方向作废，换下一个方向',
        'while True': '第一步是异色，沿同一方向继续走',
        'x += dx': '前进一格：`x` → {x}',
        'y += dy': '前进一格：`y` → {y}',
        'if x < 0 or x >= m or y < 0 or y >= n or board[x][y] == \'.\'': lambda S, B, r: ('走到 `(%d,%d)`：出界或空格 → 线段断了，break' % (S.x, S.y)) if (S.x < 0 or S.x >= S.m or S.y < 0 or S.y >= S.n or S.board[S.x][S.y] == '.') else '`(%d,%d)` 没出界、非空格，继续' % (S.x, S.y),
        'break': '这个方向没有好线段，回到 for 换方向',
        'if board[x][y] == color': _walk,
        'return True': '找到以落子点为端点的好线段 → 返回 ==True==',
        'return False': '八个方向都没有 → 返回 False',
    },
    cards=dict(
        one_liner='八个方向各走一遍：先异色、再一路异色、最后碰到同色',
        complexity='时间 `O(m+n)`，空间 `O(1)`',
        problem=['棋盘上选一个空格涂色 `color`，要求它是某条「好线段」的端点',
                 '好线段：≥3 格，两端同色，中间全是另一种颜色，且无空格',
                 '本视频用 5×5 小棋盘：落子 `(2,3)` 涂黑 `B` → `true`'],
        quote='该方向的下一个格子，不能出界，颜色必须和 color 相反。从下下一个格子开始，在遇到颜色等于 color 的格子之前，不能出界，不能遇到空格子。',
        quote_src='—— 灵茶山艾府题解',
        idea=['好线段形如 `WBBB…BW` 或 `BWWW…WB`，所以把条件拆成两步',
              '第一步必须是异色（保证至少一个中间格）',
              '之后一路异色，直到遇到同色就返回 `True`，遇到空格或出界就换方向'],
        summary=['时间 `O(m+n)`，空间 `O(1)`（只有八个方向，每个方向最多走 8 步）',
                 '易错点：第一步若是同色，线段只有两格，不算好线段',
                 '易错点：中间不能有空格，遇到 `.` 要 break',
                 '灵神还提示可用 `color ^ \'B\' ^ \'W\'` 表示异色（C++/Java 的技巧），Python 里直接比较即可',
                 '思考题：全盘 `O(mn)` 的做法可以按行、列、对角线预处理'],
    ),
)
