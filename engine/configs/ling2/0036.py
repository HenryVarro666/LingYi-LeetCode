BOARD = [["8", "3", ".", ".", "7", ".", ".", ".", "."],
         ["6", ".", ".", "1", "9", "5", ".", ".", "."],
         [".", "9", "8", ".", ".", ".", ".", "6", "."],
         ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
         ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
         ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
         [".", "6", ".", ".", ".", ".", "2", "8", "."],
         [".", ".", ".", "4", "1", "9", ".", ".", "5"],
         [".", ".", ".", ".", "8", ".", ".", "7", "9"]]

L_FOR_I, L_X, L_CHECK, L_RET_F, L_MARK, L_RET_T = 7, 11, 12, 13, 15, 17


def _cur(S):
    """当前正在处理的格子 (i, j)；刚进入新的一行时为 None"""
    if 'j' not in S or S['_line'] in (L_FOR_I, L_RET_T):
        return None
    return S['i'], S['j']


def _done(S, r, c):
    """(r, c) 这个数字是否已经登记进三张表"""
    if BOARD[r][c] == '.' or 'i' not in S:
        return False
    cur = _cur(S)
    if S['_line'] == L_RET_T:
        return True
    if cur is None:
        return r < S['i']
    if (r, c) == cur:
        return S['_line'] == L_MARK
    return (r, c) < cur


def _conflicts(S):
    """返回 False 时：和当前格冲突的旧格子"""
    if S['_line'] not in (L_CHECK, L_RET_F):
        return set()
    i, j = S['i'], S['j']
    b = BOARD[i][j]
    out = set()
    for r in range(9):
        for c in range(9):
            if (r, c) < (i, j) and BOARD[r][c] == b and (r == i or c == j or (r // 3, c // 3) == (i // 3, j // 3)):
                out.add((r, c))
    return out


def _mini(cv, T, x, y, cell, title, grid, rows_lab, hi_row, x_col, changed, flag):
    cv.text((x, y), title, 19, T['muted'], bold=True, mono=True)
    y += 29
    for c in range(9):
        cv.text((x + 34 + c * cell + cell / 2, y), c + 1, 13, T['dim'], anchor='mt', mono=True)
    y += 16
    for r in range(9):
        cv.text((x + 28, y + r * cell + cell / 2), rows_lab[r], 13, T['yellow'] if r == hi_row else T['dim'], anchor='rm', mono=True)
        for c in range(9):
            X, Y = x + 34 + c * cell, y + r * cell
            v = grid[r][c]
            fill = T['green'] if v else ((44, 50, 60) if r == hi_row else T['panel2'])
            cv.rect((X + 1, Y + 1, X + cell - 1, Y + cell - 1), fill=fill, r=3)
            if (r, c) in changed:
                cv.rect((X - 1, Y - 1, X + cell + 1, Y + cell + 1), outline=T['yellow'], width=2, r=4)
    if hi_row is not None:
        cv.rect((x + 33, y + hi_row * cell, x + 35 + 9 * cell, y + (hi_row + 1) * cell), outline=T['yellow'], width=2, r=4)
        if x_col is not None:
            X, Y = x + 34 + x_col * cell, y + hi_row * cell
            c = T['red'] if flag else T['pink']
            cv.rect((X - 2, Y - 2, X + cell + 2, Y + cell + 2), outline=c, width=3, r=4)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cur = _cur(S)
    bad = _conflicts(S)
    cell = min(52, (y1 - y0 - 180) / 9, (x1 - x0) * 0.52 / 9)
    bx, by = x0 + 34, y0 + 70
    cv.text((x0 + 18, y0 + 4), 'board（绿 = 已登记，黄 = 当前格，红 = 冲突）', 21, T['muted'], bold=True)
    for k in range(9):
        cv.text((bx + k * cell + cell / 2, by - 6), k, 15, T['dim'], anchor='mb', mono=True)
        cv.text((bx - 8, by + k * cell + cell / 2), k, 15, T['dim'], anchor='rm', mono=True)
    for r in range(9):
        for c in range(9):
            X, Y = bx + c * cell, by + r * cell
            v = BOARD[r][c]
            near = cur is not None and (r == cur[0] or c == cur[1] or (r // 3, c // 3) == (cur[0] // 3, cur[1] // 3))
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
    for k in range(4):   # 宫的粗线
        cv.line([(bx + k * 3 * cell, by), (bx + k * 3 * cell, by + 9 * cell)], T['muted'], 3)
        cv.line([(bx, by + k * 3 * cell), (bx + 9 * cell, by + k * 3 * cell)], T['muted'], 3)
    # 三张表
    x = S.get('x') if cur is not None and S['_line'] in (L_CHECK, L_RET_F, L_MARK) else None
    i, j = cur if cur else (None, None)
    bi = i // 3 * 3 + j // 3 if cur else None
    empty = [[False] * 9 for _ in range(9)]
    flat = [S['sub_box_has'][a][b] for a in range(3) for b in range(3)] if 'sub_box_has' in S else None
    bflat = [B['sub_box_has'][a][b] for a in range(3) for b in range(3)] if 'sub_box_has' in B else (flat or empty)
    mx = bx + 9 * cell + 30
    mcell = min(17, (x1 - mx - 50) / 9, (y1 - y0 - 40 - 3 * 53) / 27)
    my = y0 + 40
    lab = [str(k) for k in range(9)]
    blab = [f'{k // 3},{k % 3}' for k in range(9)]
    for title, g, bg, hi, rl in (('row_has[i][x]', S.get('row_has'), B.get('row_has') or empty, i, lab),
                                 ('col_has[j][x]', S.get('col_has'), B.get('col_has') or empty, j, lab),
                                 ("sub_box_has[i'][j'][x]", flat, bflat, bi, blab)):
        if g is None:
            cv.text((mx, my), title + '（尚未创建）', 19, T['dim'], mono=True)
            my += 53 + 9 * mcell
            continue
        changed = {(r, c) for r in range(9) for c in range(9) if g[r][c] != bg[r][c]}
        flag = x is not None and hi is not None and g[hi][x]
        _mini(cv, T, mx, my, mcell, title, g, rl, hi, x, changed, flag and S['_line'] != L_MARK)
        my += 53 + 9 * mcell
    # 棋盘下方：当前格所在行/列/宫已出现的数字（就是三张表里黄框那一行）
    if cur is not None and 'sub_box_has' in S:
        ty = by + 9 * cell + 22
        rows = ((f'第 {i} 行', S['row_has'][i]), (f'第 {j} 列', S['col_has'][j]),
                (f'宫 ({i // 3},{j // 3})', S['sub_box_has'][i // 3][j // 3]))
        for name, has in rows:
            cv.text((bx, ty), name + ' 已有：', 22, T['muted'], bold=True)
            xx = bx + 150
            if not any(has):
                cv.text((xx, ty), '（无）', 22, T['dim'])
            for d in range(9):
                if has[d]:
                    hot = x is not None and d == x
                    c = T['red'] if hot and S['_line'] != L_MARK else (T['yellow'] if hot else T['green'])
                    cv.text((xx, ty), d + 1, 22, c, bold=True)
                    xx += 26
            ty += 34


def _cap_for_i(S, B, ret):
    if 'i' in B and B.i == S.i:
        return '每一格都检查过'
    tail = '（空格 `.` 直接 `continue`，动画只停在数字上）' if S.i == 0 else ''
    return f'扫描第 `i = {S.i}` 行{tail}'


def _cap_x(S, B, ret):
    tail = '（字符 1~9 转成下标 0~8）' if (S.i, S.j) == (0, 0) else ''
    return f'`board[{S.i}][{S.j}] = \'{S.b}\'` → `x = {S.x}`{tail}'


def _cap_check(S, B, ret):
    i, j, x = S.i, S.j, S.x
    hits = []
    if S.row_has[i][x]:
        hits.append(f'第 {i} 行')
    if S.col_has[j][x]:
        hits.append(f'第 {j} 列')
    if S.sub_box_has[i // 3][j // 3][x]:
        hits.append(f'宫 ({i // 3},{j // 3})')
    if hits:
        return f'数字 `{S.b}` 在{"、".join(hits)}里==已经出现过== → 重复！'
    return f'数字 `{S.b}` 在第 {i} 行、第 {j} 列、宫 `({i // 3},{j // 3})` 里都没出现过 → 合法'


CONFIG = dict(
    num=36, title='有效的数独', difficulty='Medium', category='矩阵',
    author='灵茶山艾府', technique='布尔数组记录行/列/宫的数字',
    tags=['面试经典150'],
    code='''
class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        row_has = [[False] * 9 for _ in range(9)]  # row_has[i][x] 表示 i 行是否有数字 x
        col_has = [[False] * 9 for _ in range(9)]  # col_has[j][x] 表示 j 列是否有数字 x
        sub_box_has = [[[False] * 9 for _ in range(3)] for _ in range(3)]  # sub_box_has[i'][j'][x] 表示 (i',j') 宫是否有数字 x

        for i, row in enumerate(board):
            for j, b in enumerate(row):
                if b == '.':
                    continue
                x = int(b) - 1  # 字符 '1'~'9' 转成数字 0~8
                if row_has[i][x] or col_has[j][x] or sub_box_has[i // 3][j // 3][x]:  # 重复遇到数字 x
                    return False
                # 标记行、列、宫包含数字 x
                row_has[i][x] = col_has[j][x] = sub_box_has[i // 3][j // 3][x] = True

        return True
''',
    call=f'Solution().isValidSudoku({BOARD})',
    expect=False,
    skip=['for j, b in', "if b == '.'", 'continue'],
    views=[
        dict(type='custom', draw=_draw, h=630),
    ],
    watch=[('i', 'i'), ('j', 'j'), ('b', 'b'), ('x', 'x', 'pink')],
    captions={
        'row_has = [[False]': '`row_has[i][x]`：第 i 行有没有数字 x（9 行 × 9 个数字）',
        'col_has = [[False]': '`col_has[j][x]`：第 j 列有没有数字 x',
        'sub_box_has = [[[': "`sub_box_has[i'][j'][x]`：宫 `(i', j')` 有没有 x；`board[i][j]` 在宫 `(i // 3, j // 3)`",
        'for i, row in': _cap_for_i,
        'x = int(b) - 1': _cap_x,
        'if row_has[i][x] or': _cap_check,
        'return False': '左上角的宫里有两个 `8` → 数独==无效==，返回 `False`',
        'row_has[i][x] = col_has': '登记：第 `{i}` 行、第 `{j}` 列、宫 `({i // 3},{j // 3})` 都有了数字 `{b}`',
        'return True': '没有任何重复 → 有效',
    },
    cards=dict(
        one_liner='遍历的同时，用布尔数组标记每行、每列、每宫出现过的数字',
        complexity='时间 `O(n²)`，空间 `O(n²)`，`n = 9`',
        problem=['判断已填入数字的 `9 × 9` 数独是否有效（空格用 `.` 表示）',
                 '数字 1~9 在==每行、每列、每个 3×3 宫==内都只能出现一次',
                 '只检查已填的数字，不要求数独可解',
                 '本视频：示例 2，左上角宫里有两个 `8` → `false`'],
        quote='对于宫，我们可以把 board 视作 3×3 个大小为 3×3 的子矩阵。其中 ==board[i][j] 在 (floor(i/3), floor(j/3)) 这个宫==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['三条规则各配一张布尔表：`row_has[i][x]`、`col_has[j][x]`、`sub_box_has[i\'][j\'][x]`',
              '遇到数字 x 先查三张表：任何一张已经是 `True` → 重复，返回 `False`',
              '否则把三张表的对应位置都标成 `True`，继续遍历'],
        summary=['时间 `O(n²)`、空间 `O(n²)`，`n = 9`',
                 '易错：字符要先转成数字，`int(b) - 1` 把 1~9 映射到下标 0~8',
                 '易错：宫的下标是 `(i // 3, j // 3)`，用整除',
                 '另一种写法：三个哈希集合存 `(i, x)`、`(j, x)`、`(i // 3, j // 3, x)`',
                 '思考题：要把数独填完，见 37. 解数独'],
    ),
)
