SOL = ["534678912", "672195348", "198342567", "859761423", "426853791",
       "713924856", "961537284", "287419635", "345286179"]
BLANKS = [(0, 2), (1, 2), (2, 2), (2, 4), (2, 5)]
BOARD = [list(r) for r in SOL]
for _i, _j in BLANKS:
    BOARD[_i][_j] = '.'


def _choices(S, i, j):
    p = i // 3 * 3 + j // 3
    return [c + 1 for c in range(9) if not S['column'][j][c] and not S['row'][i][c] and not S['matrix'][p][c]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    bd = S.get('board')
    if bd is None or 'column' not in S:
        return
    inner = S.get('_inner', {})
    line = S.get('_line', 0)
    cs = min(46, (y1 - y0 - 50) / 9)
    bx, by = x0 + 24, y0 + 40
    cv.text((bx, y0 + 4), '数独（黄 = 未填，绿 = 已填，粉框 = 正在扫描，蓝框 = 当前选中的最少可填格子）', 19, T['muted'], bold=True)
    for i in range(9):
        for j in range(9):
            X, Y = bx + j * cs, by + i * cs
            blank = (i, j) in BLANKS
            v = bd[i][j]
            fill = T['panel2']
            if blank:
                fill = T['green'] if v != '.' else (90, 78, 30)
            cv.rect((X + 1, Y + 1, X + cs - 1, Y + cs - 1), fill=fill, r=4)
            if v != '.':
                cv.text((X + cs / 2, Y + cs / 2), v, 22, T['bg'] if blank else T['text'], anchor='mm', bold=blank)
            elif line >= 20:
                cv.text((X + cs / 2, Y + cs / 2), len(_choices(S, i, j)), 18, T['yellow'], anchor='mm')
    for t in range(4):
        cv.line([(bx, by + t * 3 * cs), (bx + 9 * cs, by + t * 3 * cs)], T['muted'], 3)
        cv.line([(bx + t * 3 * cs, by), (bx + t * 3 * cs, by + 9 * cs)], T['muted'], 3)
    if line in (36, 37) and 'i' in inner:
        i, j = inner['i'], inner['j']
        X, Y = bx + j * cs, by + i * cs
        cv.rect((X - 2, Y - 2, X + cs + 2, Y + cs + 2), outline=T['pink'], width=4, r=6)
    bst = _best(S)
    r, c = bst if bst else (-1, -1)
    if r is not None and r >= 0:
        X, Y = bx + c * cs, by + r * cs
        cv.rect((X - 4, Y - 4, X + cs + 4, Y + cs + 4), outline=T['blue'], width=4, r=8)
    rx = bx + 9 * cs + 30
    cv.text((rx, by), '空格里的黄字 = 还能填几个数字', 18, T['muted'])
    tgt = None
    if line in (36, 37) and 'i' in inner:
        tgt = (inner['i'], inner['j'])
    elif r is not None and r >= 0:
        tgt = (r, c)
    if tgt:
        i, j = tgt
        p = i // 3 * 3 + j // 3
        yy = by + 40
        cv.text((rx, yy), f'格子 ({i},{j})：True = 数字已被占用', 20, T['muted'], bold=True)
        yy += 32
        for name, arr in ((f'row[{i}]', S['row'][i]), (f'column[{j}]', S['column'][j]), (f'matrix[{p}]', S['matrix'][p])):
            cv.text((rx, yy), name, 18, T['muted'], mono=True)
            yy += 24
            for d in range(9):
                X = rx + d * 30
                on = arr[d]
                cv.rect((X, yy, X + 26, yy + 26), fill=T['orange'] if on else T['panel2'], r=4, outline=T['border'], width=1)
                cv.text((X + 13, yy + 13), d + 1, 16, T['bg'] if on else T['dim'], anchor='mm', bold=True)
            yy += 40
        cv.text((rx, yy), f'可填：{_choices(S, i, j)}', 20, T['green'], bold=True)


def _best(S):
    inner = S.get('_inner', {})
    if S.get('_line') == 37:
        return (inner.get('i'), inner.get('j'))
    r = inner.get('min_choice_row')
    if r is None or r < 0:
        return None
    return (r, inner.get('min_choice_column'))


def _less(S, B, ret):
    i, j, ch, mc = S.i, S.j, S.choice, B.min_choice
    if ch < mc:
        return f'`({i},{j})` 能填 `{ch}` 个数字 < 目前最少的 `{mc}` → ==记为最少格子=='
    return f'`({i},{j})` 能填 `{ch}` 个，不比目前最少的 `{mc}` 少 → 不换'


CONFIG = dict(
    num=37, title='解数独', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='搜索回溯 · 每轮全盘扫描选可填数字最少的格子',
    tags=['labuladong', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def solveSudoku(self, board):

        column = [[False for index in range(9)] for index in range(9)]
        row = [[False for index in range(9)] for index in range(9)]
        matrix = [[False for index in range(9)] for index in range(9)]
        finish_flag = True
        for i, line in enumerate(board):
            for j, num in enumerate(line):
                if num != '.':
                    num = int(num)
                    column[j][num - 1] = True
                    row[i][num - 1] = True
                    matrix_pos = i // 3 * 3 + j // 3
                    matrix[matrix_pos][num - 1] = True

        self.dfs(board, column, row, matrix)

    def dfs(self, board, column, row, matrix):
        min_choice = 10
        min_choice_row = -1
        min_choice_column = -1

        finish_flag = True
        for i, line in enumerate(board):
            for j, num in enumerate(line):
                matrix_pos = i // 3 * 3 + j // 3
                if num == '.':
                    finish_flag = False
                    choice = 0
                    for choice_num in range(9):
                        if not column[j][choice_num] and not row[i][choice_num] and not matrix[matrix_pos][choice_num]:
                            choice += 1
                    if choice == 0:
                        return False
                    if choice < min_choice:
                        min_choice = choice
                        min_choice_row = i
                        min_choice_column = j

        if finish_flag:
            return True

        choice_matrix = min_choice_row // 3 * 3 + min_choice_column // 3
        for choice_num in range(9):
            if not column[min_choice_column][choice_num] and not row[min_choice_row][choice_num] and not matrix[choice_matrix][choice_num]:
                board[min_choice_row][min_choice_column] = str(choice_num + 1)
                column[min_choice_column][choice_num] = True
                row[min_choice_row][choice_num] = True
                matrix[choice_matrix][choice_num] = True
                finish_flag = self.dfs(board, column, row, matrix)
                if finish_flag:
                    return True
                board[min_choice_row][min_choice_column] = '.'
                column[min_choice_column][choice_num] = False
                row[min_choice_row][choice_num] = False
                matrix[choice_matrix][choice_num] = False

        return False
''',
    call=f'board = {BOARD}\nSolution().solveSudoku(board)\n["".join(r) for r in board]',
    expect=SOL,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='calls', h=150, hide=('board', 'column', 'row', 'matrix')),
    ],
    watch=[('min_choice', lambda S: S['_inner'].get('min_choice'), 'blue'),
           ('最少格子', lambda S: _best(S), 'blue'),
           ('choice', lambda S: S['_inner'].get('choice'), 'pink')],
    skip=[4, 5, 6, 24, 44, 53, 8, 9, 10, 11, 12, 13, 14, 15, 21, 22, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 38, 39, 45, 46, 48, 49, 55, 56],
    captions={
        4: '`column[j][d]`：第 `j` 列是否已有数字 `d+1`',
        5: '`row[i][d]`：第 `i` 行是否已有数字 `d+1`',
        6: '`matrix[k][d]`：第 `k` 个小矩阵（`k = i // 3 * 3 + j // 3`）是否已有 `d+1`',
        7: '三个 `9×9` 布尔表 `column / row / matrix`：扫描整个数独，把已有数字标记进去（一步带过）',
        17: '开始搜索：每一轮先扫描整个数独',
        20: lambda S, B, ret: f'新的一轮扫描：`min_choice = 10` 表示还没找到格子（还剩 `{sum(r.count(".") for r in S.board)}` 个空格）',
        24: '`finish_flag = True`：先假设都填满了，遇到空格就置为 False',
        35: '某个空格==一个数字都填不了== → 当前填法是错的，回溯',
        36: _less,
        37: '最少格子更新为 `({i},{j})`，可填 `{min_choice}` 个',
        41: lambda S, B, ret: ('`finish_flag` 仍为 True：==都填满了==，当前填法就是答案' if S.finish_flag
                               else '`finish_flag = False`：还有空格，选最少格子继续填'),
        42: '返回 `True`',
        44: '`({min_choice_row},{min_choice_column})` 在第 `{choice_matrix}` 个小矩阵',
        47: lambda S, B, ret: (f'`({S.min_choice_row},{S.min_choice_column})` 选第一个行、列、矩阵都没占用的数字 → 填 =={S.choice_num + 1}=='),
        50: '标记 `column`、`row`、`matrix` 中数字 `{choice_num + 1}` 已被占用（其他格子的可填数随之减少）',
        51: '继续进行下一轮搜索',
        52: lambda S, B, ret: ('下一轮返回 `True` → 一路返回' if S.finish_flag else '下一轮失败，撤销这个数字'),
        53: '返回 `True`',
        54: '撤销：格子恢复成 `.`，三个标记改回 False',
        59: '所有数字都试过了，回溯',
    },
    max_steps=75,
    cards=dict(
        one_liner='每轮扫描全盘：满了就返回，有格子无数可填就回溯，否则填可选最少的格子',
        complexity='时间：指数级上界（每轮扫描 `O(81×9)`），空间 `O(m)` 递归',
        problem=['`9×9` 数独，`\'.\'` 是空格；每行、每列、每个 `3×3` 宫中 `1~9` 各出现一次',
                 '原地填好 `board`，保证有唯一解',
                 '本视频：示例 1 的解答盘面挖掉 5 个格子'],
        quote='(1)如果都填满了……直接返回。(2)如果存在一个未填充的格子中已经无法填数字进去了……回溯。(3)否则==找出剩下可以填的数字最少的格子==，选择一个数字填进去。',
        quote_src='—— yiduobo 题解原文',
        idea=['`column / row / matrix` 三个 `9×9` 布尔表记录每列、每行、每个小矩阵用过的数字',
              '每一轮重新扫描所有空格，数出可填数字个数，取最少的那个（严格小于才换）',
              '填入后修改三个表，其他格子的可填数自然减少；失败就恢复'],
        summary=['和灵神的最小堆不同：这里==每轮全盘重算==，写法简单，每轮 `O(81×9)`',
                 '`choice == 0` 立即返回 False：提前发现死路',
                 '小矩阵编号 `i // 3 * 3 + j // 3`，范围 `0~8`',
                 '原文为 Python 2 写法，整数除法 `i / 3 * 3 + j / 3` 已改为 `//`；删去了 docstring',
                 '原文提到 Dancing Links 会更快，但实现麻烦，所以用基本的搜索回溯'],
    ),
)
