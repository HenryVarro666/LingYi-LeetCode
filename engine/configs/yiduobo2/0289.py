BOARD = [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]
CELL_NAME = {0: '死', 1: '活', 2: '活→死', 3: '死→活'}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'board（蓝框 = 当前格，紫框 = 它的邻居）', 24, T['muted'], bold=True)
    bd = S.get('board')
    if bd is None:
        return
    R, C = len(bd), len(bd[0])
    cell = min(96, (y1 - y0 - 70) / R)
    sx = x0 + 60
    sy = y0 + 52
    i, j = S.get('i'), S.get('j')
    first = 'death' in S  # 第一趟（统计邻居）还是第二趟
    for r in range(R):
        for c in range(C):
            v = bd[r][c]
            X, Y = sx + c * cell, sy + r * cell
            fill = {0: T['panel2'], 1: T['green'], 2: T['orange'], 3: T['cyan']}[v]
            changed = B.get('board') is not None and B['board'][r][c] != v
            cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), fill=fill, r=10,
                    outline=T['yellow'] if changed else T['border'], width=3 if changed else 1)
            cv.text((X + cell / 2, Y + cell / 2), v, 30, T['bg'] if v else T['dim'], anchor='mm', bold=True)
    if isinstance(i, int) and isinstance(j, int) and first and S.get('_line') in CELL_LINES:
        # 3×3 邻域
        r0, r1 = max(0, i - 1), min(R - 1, i + 1)
        c0, c1 = max(0, j - 1), min(C - 1, j + 1)
        cv.rect((sx + c0 * cell - 2, sy + r0 * cell - 2, sx + (c1 + 1) * cell + 2, sy + (r1 + 1) * cell + 2),
                outline=T['purple'], width=3, r=12)
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                if (r, c) != (i, j) and bd[r][c] in (1, 2):
                    cv.d.ellipse((sx + c * cell + cell - 22, sy + r * cell + 8, sx + c * cell + cell - 10, sy + r * cell + 20),
                                 fill=T['yellow'])
    if isinstance(i, int) and isinstance(j, int):
        X, Y = sx + j * cell, sy + i * cell
        cv.rect((X - 1, Y - 1, X + cell + 1, Y + cell + 1), outline=T['blue'], width=5, r=12)
    # 右侧：原始棋盘 → 目标棋盘
    gx = sx + C * cell + 70
    small = min(44, cell * 0.5)
    ty = sy + 40
    cv.text((gx, ty - 8), '原来的样子', 20, T['muted'], anchor='lb', bold=True)
    for r in range(R):
        for c in range(C):
            v = BOARD[r][c]
            X, Y = gx + c * small, ty + r * small
            cv.rect((X + 2, Y + 2, X + small - 2, Y + small - 2), fill=T['green'] if v else T['panel2'], r=6, outline=T['border'])
    lx = gx + C * small + 50
    cv.text((lx, ty - 8), '图例', 20, T['muted'], anchor='lb', bold=True)
    for k, (v, txt) in enumerate([(0, '0 死'), (1, '1 活'), (2, '2 活→死'), (3, '3 死→活')]):
        fill = {0: T['panel2'], 1: T['green'], 2: T['orange'], 3: T['cyan']}[v]
        Y = ty + k * 40
        cv.rect((lx, Y, lx + 30, Y + 30), fill=fill, r=6, outline=T['border'])
        cv.text((lx + 40, Y + 15), txt, 21, T['text'], anchor='lm')
    cv.text((gx, ty + R * small + 26), '黄点 = 被算作“原来活着”的邻居（1 或 2）', 19, T['yellow'], anchor='lt')


def _text(S):
    i, j = S.get('i'), S.get('j')
    if 'live' not in S or not isinstance(i, int):
        return '规则：活细胞邻居 `< 2` 或 `> 3` 就死；死细胞邻居恰好 `3` 个就复活'
    if 'death' in S and S.get('_line') in CELL_LINES:
        v = BOARD[i][j]
        return f"`({i},{j})` 原来{'活' if v else '死'}，邻居中原来活着的 `live = {S['live']}`"
    return '第二趟：`2 → 0`、`3 → 1`，其余不变'


def _cell_cap(S, B, ret):
    i, j, live, bd = S.i, S.j, S.live, S.board
    marks = {bd[r][c] for r in range(max(0, i - 1), min(len(bd), i + 2))
             for c in range(max(0, j - 1), min(len(bd[0]), j + 2)) if (r, c) != (i, j)}
    note = []
    if 2 in marks:
        note.append('`2` 原来是活的，照样算')
    if 3 in marks:
        note.append('`3` 原来是死的，不算')
    tail = f'（{"，".join(note)}）' if note else ''
    kind = '死' if B.board[i][j] == 0 else '活'
    return f'`({i},{j})` 是{kind}细胞，周围原来活着的 `live = {live}`{tail}'


def _l3_cap(S, B, ret):
    if S.live == 3:
        return f'`live == 3`：死细胞周围恰好 3 个活细胞 → ==复活=='
    return f'`live = {S.live}` ≠ 3 → 继续保持死亡'


def _l23_cap(S, B, ret):
    l = S.live
    if l < 2:
        return f'`live = {l} < 2`：太孤单 → ==死去=='
    if l > 3:
        return f'`live = {l} > 3`：太拥挤 → ==死去=='
    return f'`live = {l}` 在 [2, 3] 内 → 继续存活'


CODE = '''
class Solution(object):
    def gameOfLife(self, board):
        dx = [-1, -1, -1, 0, 0, 1, 1, 1]
        dy = [-1, 0, 1, -1, 1, -1, 0, 1]

        for i in range(len(board)):
            for j in range(len(board[0])):
                death = live = 0
                for index in range(8):
                    x = i + dx[index]
                    y = j + dy[index]
                    if x < 0 or x == len(board) or y < 0 or y == len(board[0]):
                        continue

                    if board[x][y] == 0 or board[x][y] == 3:
                        death += 1
                    else:
                        live += 1

                if board[i][j] == 0:
                    if live == 3:
                        board[i][j] = 3
                else:
                    if live < 2 or live > 3:
                        board[i][j] = 2

        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] >= 2:
                    board[i][j] -= 2
'''
_LINES = CODE.strip('\n').split('\n')
CELL_LINES = {k + 1 for k, l in enumerate(_LINES)
              if any(t in l for t in ('if board[i][j] == 0', 'if live == 3', 'board[i][j] = 3', 'if live < 2',
                                      'board[i][j] = 2'))}

CONFIG = dict(
    num=289, title='生命游戏', difficulty='Medium', category='矩阵',
    author='yiduobo', technique='原地标记 · 2 = 死去，3 = 复活',
    tags=['面试经典150'],
    code=CODE,
    call=f'''board = {BOARD!r}
Solution().gameOfLife(board)
board''',
    expect=[[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]],
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', fn=_text, size=27, h=70),
        dict(type='text', fn=lambda S: '数邻居：`0` 或 `3` 算原来是死的，`1` 或 `2` 算原来是活的', size=24, h=60),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'blue'), ('live', 'live', 'yellow'), ('death', 'death')],
    skip=['for i in range(len(board))', 'for j in range(len(board[0]))', 'death = live = 0', 'for index in range(8)',
          'x = i + dx', 'y = j + dy', 'if x < 0', 'continue', 'if board[x][y] == 0', 'death += 1', 'live += 1',
          'if board[i][j] >= 2'],
    captions={
        'dx = [': '`dx`、`dy`：8 个邻居方向的偏移量',
        'dy = [': '接下来逐格统计 8 个邻居，越界的跳过',
        'if board[i][j] == 0': _cell_cap,
        'if live == 3': _l3_cap,
        'board[i][j] = 3': '不能直接改成 1（会影响后面的格子）→ 标记为 ==3==：本轮复活',
        'if live < 2 or live > 3': _l23_cap,
        'board[i][j] = 2': '标记为 ==2==：本轮死去；后面的格子仍把它当活细胞数',
        'board[i][j] -= 2': '第二趟：`({i},{j})` 的 `{B.board[i][j]}` 减 2 → `{board[i][j]}`',
    },
    max_steps=50,
    cards=dict(
        one_liner='用 2 表示“这轮死去”，3 表示“这轮复活”，原地更新不丢信息',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`m×n` 网格，1 = 活细胞，0 = 死细胞；每个细胞看周围 ==8 个==邻居',
                 '活细胞：邻居 `< 2` 或 `> 3` 个活的就死；死细胞：恰好 `3` 个活邻居就复活',
                 '所有细胞==同时==更新，要求原地完成',
                 '示例：`[[0,1,0],[0,0,1],[1,1,1],[0,0,0]]` → `[[0,0,0],[1,0,1],[0,1,1],[0,1,0]]`'],
        quote='注意到这里的状态只有0和1两种，于是一个自然的想法就是使用额外的状态标记……我在这里==使用的是2表示细胞在这一次操作中死去，3表示细胞在这一次操作中复活==。',
        quote_src='—— yiduobo 题解原文',
        idea=['原地更新的难点：邻居可能已经被改过状态',
              '新增两种状态：`2`（原来活、将死），`3`（原来死、将活）→ 原始状态仍可读出',
              '扫完一遍后，把所有 `≥ 2` 的值减 2 即可'],
        summary=['时间 `O(mn)`（每格看 8 个邻居），空间 `O(1)`',
                 '数邻居时 `0/3` 算死、`1/2` 算活：==按原始状态==统计',
                 '易错：不能直接改成 0/1，否则后面的格子会数错',
                 '原文为 Python 2 风格：只删去了类型说明文档字符串，代码未改'],
    ),
)
