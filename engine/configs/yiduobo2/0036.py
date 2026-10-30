# 示例 1 的数独，把 board[1][1] 从 '.' 改成 '3'：第 1 列出现两个 3
BOARD = [["5", "3", ".", ".", "7", ".", ".", ".", "."],
         ["6", "3", ".", "1", "9", "5", ".", ".", "."],
         [".", "9", "8", ".", ".", ".", ".", "6", "."],
         ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
         ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
         ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
         [".", "6", ".", ".", ".", ".", "2", "8", "."],
         [".", ".", ".", "4", "1", "9", ".", ".", "5"],
         [".", ".", ".", ".", "8", ".", ".", "7", "9"]]

L_FOR_I, L_RET_T = 7, 23
PHASE = {10: 0, 11: 0, 12: 0, 14: 1, 15: 1, 16: 1, 18: 2, 19: 2, 20: 2, 21: 2}   # 行号 -> 正在查哪张表
RETS = (11, 15, 20)


def _cur(S):
    if 'j' not in S or S['_line'] in (L_FOR_I, L_RET_T):
        return None
    return S['i'], S['j']


def _done(S, r, c):
    if BOARD[r][c] == '.' or 'i' not in S:
        return False
    cur = _cur(S)
    if S['_line'] == L_RET_T:
        return True
    if cur is None:
        return r < S['i']
    if (r, c) == cur:
        return S['_line'] == 21
    return (r, c) < cur


def _conflicts(S):
    ln = S['_line']
    cur = _cur(S)
    if cur is None or ln not in (10, 11, 14, 15, 19, 20):
        return set()
    i, j = cur
    b = BOARD[i][j]
    ph = PHASE[ln]
    out = set()
    for r in range(9):
        for c in range(9):
            if (r, c) < (i, j) and BOARD[r][c] == b:
                if (ph == 0 and c == j) or (ph == 1 and r == i) or (ph == 2 and (r // 3, c // 3) == (i // 3, j // 3)):
                    out.add((r, c))
    return out


def _mini(cv, T, x, y, cell, title, grid, hi_row, x_col, changed, state, active):
    cv.text((x, y), title, 19, T['text'] if active else T['muted'], bold=True, mono=True)
    y += 29
    for c in range(9):
        cv.text((x + 34 + c * cell + cell / 2, y), c + 1, 13, T['dim'], anchor='mt', mono=True)
    y += 16
    for r in range(9):
        cv.text((x + 28, y + r * cell + cell / 2), r, 13, T['yellow'] if r == hi_row else T['dim'], anchor='rm', mono=True)
        for c in range(9):
            X, Y = x + 34 + c * cell, y + r * cell
            fill = T['green'] if grid[r][c] else ((44, 50, 60) if r == hi_row else T['panel2'])
            cv.rect((X + 1, Y + 1, X + cell - 1, Y + cell - 1), fill=fill, r=3)
            if (r, c) in changed:
                cv.rect((X - 1, Y - 1, X + cell + 1, Y + cell + 1), outline=T['yellow'], width=2, r=4)
    if hi_row is not None:
        cv.rect((x + 33, y + hi_row * cell, x + 35 + 9 * cell, y + (hi_row + 1) * cell), outline=T['yellow'], width=2, r=4)
        if active and x_col is not None:
            X, Y = x + 34 + x_col * cell, y + hi_row * cell
            cv.rect((X - 2, Y - 2, X + cell + 2, Y + cell + 2), outline=T['red'] if state == 'bad' else T['pink'], width=3, r=4)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cur = _cur(S)
    bad = _conflicts(S)
    ln = S['_line']
    cell = min(52, (y1 - y0 - 180) / 9, (x1 - x0) * 0.52 / 9)
    bx, by = x0 + 34, y0 + 70
    cv.text((x0 + 18, y0 + 4), 'board（绿 = 已登记，黄 = 当前格，红 = 冲突）', 21, T['muted'], bold=True)
    for k in range(9):
        cv.text((bx + k * cell + cell / 2, by - 6), k, 15, T['dim'], anchor='mb', mono=True)
        cv.text((bx - 8, by + k * cell + cell / 2), k, 15, T['dim'], anchor='rm', mono=True)
    ph = PHASE.get(ln)
    for r in range(9):
        for c in range(9):
            X, Y = bx + c * cell, by + r * cell
            v = BOARD[r][c]
            near = cur is not None and ((ph == 0 and c == cur[1]) or (ph == 1 and r == cur[0]) or
                                        (ph == 2 and (r // 3, c // 3) == (cur[0] // 3, cur[1] // 3)))
            if cur == (r, c):
                fill = T['red'] if bad else T['yellow']
            elif (r, c) in bad:
                fill = T['red']
            elif _done(S, r, c):
                fill = (46, 110, 64)
            elif near:
                fill = (70, 62, 34)
            else:
                fill = T['panel2']
            cv.rect((X + 1, Y + 1, X + cell - 1, Y + cell - 1), fill=fill, r=4)
            if v != '.':
                cv.text((X + cell / 2, Y + cell / 2), v, int(cell * 0.55), T['bg'] if fill in (T['yellow'], T['red']) else T['text'],
                        anchor='mm', bold=True)
    for k in range(4):
        cv.line([(bx + k * 3 * cell, by), (bx + k * 3 * cell, by + 9 * cell)], T['muted'], 3)
        cv.line([(bx, by + k * 3 * cell), (bx + 9 * cell, by + k * 3 * cell)], T['muted'], 3)
    # 小宫编号 0~8（matrix_pos = i // 3 * 3 + j // 3）
    for k in range(9):
        cv.text((bx + (k % 3) * 3 * cell + 5, by + (k // 3) * 3 * cell + 3), k, 14, T['cyan'], bold=True)
    empty = [[False] * 9 for _ in range(9)]
    xd = int(S['num']) - 1 if cur is not None else None
    i, j = cur if cur else (None, None)
    mp = i // 3 * 3 + j // 3 if cur else None
    mx = bx + 9 * cell + 30
    mcell = min(17, (x1 - mx - 50) / 9, (y1 - y0 - 40 - 3 * 53) / 27)
    my = y0 + 40
    for k, (title, name, hi) in enumerate((('column[j][x]', 'column', j), ('row[i][x]', 'row', i), ('matrix[pos][x]', 'matrix', mp))):
        g = S.get(name)
        if g is None:
            cv.text((mx, my), title + '（尚未创建）', 19, T['dim'], mono=True)
            my += 53 + 9 * mcell
            continue
        bg = B.get(name) or empty
        changed = {(r, c) for r in range(9) for c in range(9) if g[r][c] != bg[r][c]}
        state = 'bad' if ln in RETS and PHASE[ln] == k else ''
        if ln in (10, 14, 19) and PHASE[ln] == k and hi is not None and g[hi][xd]:
            state = 'bad'
        _mini(cv, T, mx, my, mcell, title, g, hi, xd, changed, state, ph == k)
        my += 53 + 9 * mcell
    if cur is not None:
        ty = by + 9 * cell + 24
        cv.text((bx, ty), f"num = '{S['num']}' → 下标 int(num) - 1 = {xd}", 22, T['pink'], bold=True)
        cv.text((bx, ty + 36), f'所在小矩阵 = {i} // 3 * 3 + {j} // 3 = {mp}', 22, T['cyan'], bold=True)


def _cap_for_i(S, B, ret):
    if 'i' in B and B.i == S.i:
        return '所有格子都没冲突'
    tail = '（空格跳过，动画只停在数字上）' if S.i == 0 else ''
    return f'扫描第 `i = {S.i}` 行{tail}'


def _cap_check(name, idx_expr):
    def f(S, B, ret):
        idx = eval(idx_expr, {}, dict(S))
        hit = S[name][idx][int(S.num) - 1]
        where = {'column': f'第 {S.j} 列', 'row': f'第 {S.i} 行', 'matrix': f'第 {idx} 个小矩阵'}[name]
        head = f'`board[{S.i}][{S.j}] = {S.num}`：' if name == 'column' else ''
        if hit:
            return f'{head}{where}==已经出现过== `{S.num}` → 不能再填，冲突！'
        return f'{head}{where}还没有 `{S.num}`，可以'
    return f


CONFIG = dict(
    num=36, title='有效的数独', difficulty='Medium', category='矩阵',
    author='yiduobo', technique='行/列/小矩阵三张填充表',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def isValidSudoku(self, board):
        column = [[False for index in range(9)] for index in range(9)]
        row = [[False for index in range(9)] for index in range(9)]
        matrix = [[False for index in range(9)] for index in range(9)]

        for i, line in enumerate(board):
            for j, num in enumerate(line):
                if num != '.':
                    if column[j][int(num) - 1]:
                        return False
                    column[j][int(num) - 1] = True

                    if row[i][int(num) - 1]:
                        return False
                    row[i][int(num) - 1] = True

                    matrix_pos = i // 3 * 3 + j // 3
                    if matrix[matrix_pos][int(num) - 1]:
                        return False
                    matrix[matrix_pos][int(num) - 1] = True

        return True
''',
    call=f'Solution().isValidSudoku({BOARD})',
    expect=False,
    skip=['for j, num in', "if num != '.'"],
    views=[
        dict(type='custom', draw=_draw, h=630),
    ],
    watch=[('i', 'i'), ('j', 'j'), ('num', 'num', 'pink'), ('matrix_pos', 'matrix_pos', 'cyan')],
    captions={
        'column = [[False': '`column[n][x - 1]`：第 n 列是否已经出现过 x',
        'row = [[False': '`row[m][x - 1]`：第 m 行是否已经出现过 x',
        'matrix = [[False': '`matrix[k][x - 1]`：第 k 个小矩阵是否出现过 x（n 行、n 列、n 个小矩阵）',
        'for i, line in': _cap_for_i,
        'if column[j]': _cap_check('column', 'j'),
        'column[j][int(num) - 1] = True': '`column[{j}][{int(num) - 1}] = True`：第 {j} 列出现过 `{num}` 了',
        'if row[i]': _cap_check('row', 'i'),
        'row[i][int(num) - 1] = True': '`row[{i}][{int(num) - 1}] = True`：第 {i} 行出现过 `{num}` 了',
        'matrix_pos = ': lambda S, B, r: (f'所在小矩阵 `k = {S.i} // 3 * 3 + {S.j} // 3 = {S.matrix_pos}`'
                                          + ('（原文写 `/`，Python 3 要用==整除== `//`）' if 'matrix_pos' not in B else '')),
        'if matrix[matrix_pos]': _cap_check('matrix', 'matrix_pos'),
        'matrix[matrix_pos][int(num) - 1] = True': '`matrix[{matrix_pos}][{int(num) - 1}] = True`：小矩阵 {matrix_pos} 出现过 `{num}` 了',
        11: '第 1 列已有一个 `3`，又来一个 `3` → 先前在这一列填过了，返回 `False`',
        15: '这一行先前填过同样的数字，返回 `False`',
        20: '这个小矩阵先前填过同样的数字，返回 `False`',
        'return True': '每个格子都没有和之前冲突 → 返回 `True`',
    },
    cards=dict(
        one_liner='n×n 数独正好有 n 行、n 列、n 个小矩阵，各用一张表记录填过哪些数',
        complexity='时间 `O(n²)`，空间 `O(n²)`，`n = 9`',
        problem=['判断已填入数字的 `9 × 9` 数独是否有效（空格用 `.` 表示）',
                 '数字 1~9 在==每行、每列、每个 3×3 小矩阵==内都只能出现一次',
                 '本视频：示例 1 中把 `board[1][1]` 改成 `3` → 第 1 列有两个 3 → `false`'],
        quote='一个n*n的数独一定是==n行，n列，n个小矩阵==的，且其中填写的数字正好是1到n。那么可以维护三个n*n的二维list，分别表示行、列以及小矩阵中数字的填充情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['第 m 行第 n 列的数 x：置 `row[m][x-1]`、`column[n][x-1]` 为 True',
              '小矩阵编号 `k = m / 3 * 3 + n / 3`（整除），置 `matrix[k][x-1]` 为 True',
              '要置 True 的地方==已经是 True== → 先前填过 x，返回 False'],
        summary=['时间 `O(n²)`，空间 `O(n²)`',
                 '原文为 Python 2 写法：`i / 3 * 3 + j / 3` 中的 `/` 已改为 `//`（否则得到小数下标），并删去 docstring',
                 '技巧：把二维的「宫」压成一维编号 `0~8`，三张表都是 9×9',
                 '原文提到：转成精确覆盖问题用 Dancing Links 效率更高（37 题解数独）',
                 '对比灵神：思路相同，灵神用 3×3×9 的三维数组存宫，并在一行里同时查三张表'],
    ),
)
