BOARD = ['XXX', 'OO ', 'O  ']


def _grid(S):
    return [list(r) for r in S['board']]


def _col(S, i, j, v):
    ln = S.get('_line', 0)
    if ln >= 22 and S.get('win_x') is not None:   # 判断三连阶段：整行/整列染色
        k = S.get('i')
        if k is not None and ln in (26, 27, 28, 29) and (i == k or j == k):
            return 'green' if (S['row_x'][k] == 3 and i == k and v == 'X') or (S['col_x'][k] == 3 and j == k and v == 'X') else None
    return 'pink' if v == 'O' else ('blue' if v == 'X' else None)


def _fn(S):
    if 'cnt_x' not in S:
        return '合法局面：X 先手，所以 `X 数 − O 数` 只能是 0 或 1；赢的一方不能再多下'
    s = f"X = =={S['cnt_x']}==，O = =={S['cnt_o']}=="
    if 'delta' in S:
        s += f"，`delta = {S['delta']}`"
    if 'win_x' in S:
        s += f"　X 三连：=={S['win_x']}==，O 三连：=={S['win_o']}=="
    return s


CONFIG = dict(
    num=794, title='有效的井字游戏', difficulty='Medium', category='模拟',
    author='yiduobo', technique='计数 + 判断三连',
    tags=[],
    code='''
class Solution(object):
    def validTicTacToe(self, board):

        cnt_x = cnt_o = 0
        col_x = [0, 0, 0]
        col_o = [0, 0, 0]
        row_x = [0, 0, 0]
        row_o = [0, 0, 0]
        for i in range(3):
            for j in range(3):
                if board[i][j] == 'X':
                    cnt_x += 1
                    row_x[i] += 1
                    col_x[j] += 1
                elif board[i][j] == 'O':
                    cnt_o += 1
                    row_o[i] += 1
                    col_o[j] += 1

        delta = cnt_x - cnt_o
        if delta < 0 or delta > 1:
            return False

        win_x = win_o = False
        for i in range(3):
            if row_x[i] == 3 or col_x[i] == 3:
                win_x = True
            if row_o[i] == 3 or col_o[i] == 3:
                win_o = True
        
        if board[0][0] == board[1][1] == board[2][2]:
            if board[0][0] == 'O':
                win_o = True
            elif board[0][0] == 'X':
                win_x = True
        
        if board[0][2] == board[1][1] == board[2][0]:
            if board[0][2] == 'O':
                win_o = True
            elif board[0][2] == 'X':
                win_x = True

        if win_x and win_o:
            return False

        if delta == 0 and win_x:
            return False

        if delta == 1 and win_o:
            return False

        return True
''',
    call=f'Solution().validTicTacToe({BOARD})',
    expect=False,
    skip=['row_x[i] += 1', 'col_x[j] += 1', 'row_o[i] += 1', 'col_o[j] += 1', 'col_x = [', 'col_o = [', 'row_x = [',
          'row_o = [', 'for i in range', 'for j in range', 'elif board[i][j]', 'if board[i][j] == \'X\''],
    views=[
        dict(type='text', fn=_fn, size=26, h=60),
        dict(type='grid', var=_grid, label='board（蓝 = X，粉 = O）', cell=100, h=360, color=_col,
             cursors=[('i if _line in (9, 10, 11, 12, 13, 14, 15, 16, 17) else None', 'j', 'yellow')]),
        dict(type='array', var=lambda S: S.get('row_x'), label='row_x（每行 X 的个数）', cell=70, h=140),
        dict(type='array', var=lambda S: S.get('col_x'), label='col_x（每列 X 的个数）', cell=70, h=140),
    ],
    watch=[('cnt_x', 'cnt_x', 'blue'), ('cnt_o', 'cnt_o', 'pink'), 'delta', 'win_x', 'win_o'],
    captions={
        'cnt_x = cnt_o = 0': '先统计 X、O 的个数，同时记下每行每列各有几个',
        'cnt_x += 1': '这一格是 `X`：`cnt_x` = {cnt_x}（同时 `row_x[{i}]`、`col_x[{j}]` 各加 1）',
        'cnt_o += 1': '这一格是 `O`：`cnt_o` = {cnt_o}（同时 `row_o[{i}]`、`col_o[{j}]` 各加 1）',
        'delta = cnt_x - cnt_o': '`delta = {cnt_x} − {cnt_o}` = =={delta}==（X 先手，只能是 0 或 1）',
        'if delta < 0 or delta > 1': lambda S, B, r: (f'`delta = {S.delta}` 不在 0~1 → ==数量就不合法==' if S.delta < 0 or S.delta > 1
                                                      else f'`delta = {S.delta}`，数量合法，接着看三连'),
        'win_x = win_o = False': '假设先都没三连，再逐行逐列检查',
        'if row_x[i] == 3 or col_x[i] == 3': lambda S, B, r: (
            f'第 {S.i} 行/列 X 的个数 `{S.row_x[S.i]}`/`{S.col_x[S.i]}`' + ('，有三连 → ==win_x = True==' if S.row_x[S.i] == 3 or S.col_x[S.i] == 3 else '，不够三个')),
        'if row_o[i] == 3 or col_o[i] == 3': lambda S, B, r: (
            f'第 {S.i} 行/列 O 的个数 `{S.row_o[S.i]}`/`{S.col_o[S.i]}`' + ('，有三连 → ==win_o = True==' if S.row_o[S.i] == 3 or S.col_o[S.i] == 3 else '，不够三个')),
        'win_x = True': '这一行（或列）三个都是 X → `win_x = True`',
        'win_o = True': '这一行（或列）三个都是 O → `win_o = True`',
        'if board[0][0] == board[1][1]': '再查主对角线：三格相同才可能三连（==别忘了对角线==）',
        'if board[0][2] == board[1][1]': '再查副对角线',
        'if win_x and win_o': lambda S, B, r: ('X、O 同时三连，不可能 → ==False==' if S.win_x and S.win_o else '没有两边同时三连'),
        'if delta == 0 and win_x': lambda S, B, r: (
            f'`delta = 0`（X、O 一样多，轮到 X 下），可 X 已三连：说明 X 赢了还继续下 → ==不合法=='
            if S.delta == 0 and S.win_x else '不是「X 赢但数量相同」'),
        'if delta == 1 and win_o': lambda S, B, r: (
            'O 已三连，但 X 比 O 多一个：O 赢后 X 又下了 → ==不合法==' if S.delta == 1 and S.win_o else '不是「O 赢但 X 多一个」'),
        'return False': '局面不可能出现 → `False`',
        'return True': '所有检查都通过 → ==合法== `True`',
    },
    cards=dict(
        one_liner='先看数量差，再看谁三连，两者要对得上',
        complexity='时间 `O(1)`（棋盘固定 3×3），空间 `O(1)`',
        problem=['3×3 棋盘，`X` 先手，`O` 后手，空格用 `" "` 表示',
                 '判断它是否是某局合法游戏进行中能出现的局面（有人三连后游戏立刻结束）',
                 '本视频：`["XXX","OO ","O  "]` → `False`'],
        quote='若X达成了三连，且X和O的数量相同，那么不合法。',
        quote_src='—— yiduobo 题解原文',
        idea=['数量：X 比 O 多 0 或 1 个，否则不合法',
              'X 赢 → X 必须多 1 个；O 赢 → 两者必须一样多；不能同时三连',
              '行、列、两条对角线都要查，对角线容易漏'],
        summary=['时间、空间都是 `O(1)`',
                 '易错：忘查对角线；X 5 个 O 4 个时 X 可有两组三连，仍合法',
                 '其他两组三连的情形会被数量条件挡掉，无需单独判断',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行'],
    ),
)
