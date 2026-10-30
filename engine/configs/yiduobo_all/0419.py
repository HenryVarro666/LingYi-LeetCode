BOARD = [['X', 'X', '.', 'X'], ['.', '.', '.', 'X'], ['X', '.', '.', 'X']]


def _head(r, c):
    if BOARD[r][c] != 'X':
        return False
    return not ((r > 0 and BOARD[r - 1][c] == 'X') or (c > 0 and BOARD[r][c - 1] == 'X'))


def _color(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return None
    line = S.get('_line')
    before = (r, c) < (i, j) or ((r, c) == (i, j) and line == 12)
    if (r, c) == (i, j):
        return 'yellow' if line != 12 else 'green'
    if before and _head(r, c):
        return 'green'
    return None


def _cap_if(S, B, ret):
    i, j = S.i, S.j
    return f"`board[{i}][{j}] = '{S.board[i][j]}'`" + (' → 是战舰的一格，继续看上、左' if S.board[i][j] == 'X' else ' → 空位，跳过')


def _cap_up(S, B, ret):
    i, j = S.i, S.j
    if S.i > 0 and S.board[i - 1][j] == 'X':
        return f"上面 `board[{i-1}][{j}] = 'X'` → 这是竖直战舰的==中间或底部==，不是标志点，跳过"
    return '上面不是 X（或在第一行）→ 这格不是竖直战舰的中间部分'


def _cap_left(S, B, ret):
    i, j = S.i, S.j
    if S.j > 0 and S.board[i][j - 1] == 'X':
        return f"左边 `board[{i}][{j-1}] = 'X'` → 这是水平战舰的==右侧==，不是标志点，跳过"
    return '左边不是 X（或在第一列）→ 这格不是水平战舰的右侧部分'


CONFIG = dict(
    num=419, title='棋盘上的战舰', difficulty='Medium', category='网格图',
    author='yiduobo', technique='一趟扫描 · 只数战舰的标志点',
    tags=[],
    code='''
class Solution(object):
    def countBattleships(self, board):

        res = 0
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 'X':
                    if i > 0 and board[i - 1][j] == 'X':
                        continue
                    if j > 0 and board[i][j - 1] == 'X':
                        continue
                    res += 1

        return res
''',
    call=f'Solution().countBattleships({BOARD})',
    expect=3,
    skip=['for j in range'],
    views=[
        dict(type='grid', var='board', label='board（黄 = 正在看的格子，绿 = 已数过的战舰标志点）', cell=110, h=420,
             cursors=[('i', 'j', 'yellow', '(i,j)')], color=_color),
        dict(type='text', fn=lambda S: '标志点：==水平战舰的最左格== 或 ==竖直战舰的最上格==，每艘战舰恰好一个', size=24, h=60),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记录战舰数量',
        'for i in range': lambda S, B, r: (f'扫描第 `{S.i}` 行' if B.get('i') != S.i or 'i' not in B else '所有行扫描完毕'),
        "if board[i][j] == 'X'": _cap_if,
        'if i > 0': _cap_up,
        'if j > 0': _cap_left,
        'continue': '不是标志点，这艘战舰早在别处数过了 → 跳过',
        'res += 1': '上面、左边都不是 X → ==这是战舰的标志点==，`res` → =={res}==',
        'return res': '一共 `{res}` 艘战舰',
    },
    cards=dict(
        one_liner='每艘战舰只在最左或最上的那一格数一次',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`m × n` 的棋盘，`X` 是战舰，`.` 是空位',
                 '战舰只能水平或竖直摆放，且两艘战舰之间不相邻',
                 '求战舰数量。要求一趟扫描、不改动 `board`',
                 '本视频：3×4 的棋盘 → `3`'],
        quote='可以将竖直战舰的顶部以及水平战舰的左侧作为标志点。',
        quote_src='—— yiduobo 题解原文',
        idea=['战舰不会相交也不会相邻，所以每艘战舰要么横着、要么竖着',
              '若一格为 X 且左边也是 X，它是横向战舰的后半段，跳过',
              '若一格为 X 且上边也是 X，它是竖向战舰的后半段，跳过；否则就是标志点，计数 +1'],
        summary=['时间 `O(mn)`，空间 `O(1)`，不修改 `board`',
                 '易错：下标要先判 `i > 0`、`j > 0`，再访问 `board[i-1][j]`',
                 '不需要 DFS 或并查集，战舰的形状限制让「标志点」足够',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
