PIECES = ['bishop', 'bishop']
POS = [(3, 3), (1, 1)]
NAMES = ['象A', '象B']
COLS = ['blue', 'pink', 'green', 'purple']


def _end(m):
    x0, y0, dx, dy, st = m
    return x0 + dx * st, y0 + dy * st


def _pos(m, t):
    x0, y0, dx, dy, st = m
    k = min(t, st)
    return x0 + dx * k, y0 + dy * k


def _clash(m1, m2):
    """第一个重叠的 (时刻, 格子)，没有则 None（与 is_valid 一致）"""
    for t in range(1, max(m1[4], m2[4]) + 1):
        a, b = _pos(m1, t), _pos(m2, t)
        if a == b:
            return t, a
    return None


def _mv(m):
    if m[4] == 0:
        return '原地不动'
    return f'往 ({m[2]},{m[3]}) 走 {m[4]} 步到 {_end(m)}'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    i = S.get('i')
    path = S.get('path')
    cv.text((x0 + 18, y0 + 4), '棋盘（箭头 = 已定下的移动，黄 = 正在尝试的移动，红叉 = 冲突）', 22, T['muted'], bold=True)
    cell = min((x1 - x0 - 330) / 8, (y1 - y0 - 100) / 8, 70)
    sx = x0 + 70
    sy = y0 + 72
    for r in range(8):
        for c in range(8):
            X, Y = sx + c * cell, sy + r * cell
            cv.rect((X, Y, X + cell, Y + cell), fill=T['panel2'] if (r + c) % 2 == 0 else (30, 36, 46), outline=T['border'])
    for k in range(8):
        cv.text((sx + k * cell + cell / 2, sy - 6), k + 1, 17, T['dim'], anchor='mb', mono=True)
        cv.text((sx - 8, sy + k * cell + cell / 2), k + 1, 17, T['dim'], anchor='rm', mono=True)

    def ctr(p):
        return sx + (p[1] - 1) * cell + cell / 2, sy + (p[0] - 1) * cell + cell / 2

    cur = S.get('move1') if i is not None and i < len(PIECES) else None
    fixed = [(k, path[k]) for k in range(i or 0) if path and path[k]] if i is not None else []
    for k, m in fixed:
        a, b = ctr((m[0], m[1])), ctr(_end(m))
        if m[4]:
            cv.arrow(a, b, T[COLS[k]], 6, 14)
        cv.rect((b[0] - cell * 0.18, b[1] - cell * 0.18, b[0] + cell * 0.18, b[1] + cell * 0.18), fill=T[COLS[k]], r=4, alpha=140)
    bad = None
    if cur is not None:
        a, b = ctr((cur[0], cur[1])), ctr(_end(cur))
        if cur[4]:
            cv.arrow(a, b, T['yellow'], 5, 14)
        cv.rect((b[0] - cell * 0.22, b[1] - cell * 0.22, b[0] + cell * 0.22, b[1] + cell * 0.22), outline=T['yellow'], width=4, r=5)
        for k, m in fixed:
            cl = _clash(cur, m)
            if cl:
                bad = cl
                break
    for k, p in enumerate(POS):
        X, Y = ctr(p)
        cv.rect((X - cell * 0.36, Y - cell * 0.36, X + cell * 0.36, Y + cell * 0.36), fill=T[COLS[k]], r=cell * 0.2)
        cv.text((X, Y), '象', 24, T['bg'], anchor='mm', bold=True)
    if bad:
        X, Y = ctr(bad[1])
        cv.line([(X - 14, Y - 14), (X + 14, Y + 14)], T['red'], 6)
        cv.line([(X - 14, Y + 14), (X + 14, Y - 14)], T['red'], 6)
    # 右侧：每个棋子已选的移动
    tx = sx + 8 * cell + 36
    cv.text((tx, sy), '已确定的移动', 22, T['muted'], bold=True)
    for k in range(len(PIECES)):
        yy = sy + 40 + k * 70
        cv.rect((tx, yy, tx + 18, yy + 18), fill=T[COLS[k]], r=4)
        txt = '尚未选择'
        if path and any(kk == k for kk, _ in fixed):
            txt = _mv(path[k])
        cv.text((tx + 28, yy - 4), f'{NAMES[k]} {POS[k]}', 22, T['text'], bold=True)
        cv.text((tx + 28, yy + 24), txt, 20, T['text'] if txt != '尚未选择' else T['dim'])
    if cur is not None:
        yy = sy + 40 + 2 * 70
        cv.text((tx, yy), f'正在试：{NAMES[i]}', 22, T['yellow'], bold=True)
        cv.text((tx, yy + 30), _mv(cur).replace('往 ', '方向 ').replace(' 走 ', ' × ').replace(' 步到 ', ' 步 → '), 19, T['yellow'])
        cv.text((tx, yy + 62), '与前面的移动冲突' if bad else '与前面的移动不冲突', 21, T['red'] if bad else T['green'], bold=True)
        if bad:
            cv.text((tx, yy + 92), f'第 {bad[0]} 秒同在 {bad[1]}', 21, T['red'], bold=True)


def _all(S, B, r):
    i, m = S.i, S.move1
    for k in range(i):
        cl = _clash(m, S.path[k])
        if cl:
            return (f'`{NAMES[i]}` 这个移动和 `{NAMES[k]}` 在第 =={cl[0]}== 秒同时到 `{cl[1]}` → ==重叠，无效==，换下一个移动')
    if i == 0:
        return f'第一个棋子前面没人，`{NAMES[i]}` {_mv(m)} 直接有效'
    return f'`{NAMES[i]}` {_mv(m)}：和前面的棋子逐秒比较，没有同时占同一格 → ==有效=='


CONFIG = dict(
    num=2056, title='棋盘上有效移动组合的数目', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='预处理合法移动 + 回溯枚举',
    tags=['灵神题单·常用数据结构', '灵神题单·链表树与回溯', '难度分 2611'],
    code='''
class Solution:
    # 计算位于 (x0,y0) 的棋子在 dirs 这些方向上的所有合法移动
    def generate_moves(self, x0: int, y0: int, dirs: List[Tuple[int, int]]) -> List[Tuple[int, int, int, int, int]]:
        SIZE = 8
        moves = [(x0, y0, 0, 0, 0)]  # 原地不动
        for dx, dy in dirs:
            # 往 (dx,dy) 方向走 1,2,3,... 步
            x, y = x0 + dx, y0 + dy
            step = 1
            while 0 < x <= SIZE and 0 < y <= SIZE:
                moves.append((x0, y0, dx, dy, step))
                x += dx
                y += dy
                step += 1
        return moves

    # 判断两个移动是否合法，即不存在同一时刻两个棋子重叠的情况
    def is_valid(self, move1: Tuple[int, int, int, int, int], move2: Tuple[int, int, int, int, int]) -> bool:
        x1, y1, dx1, dy1, step1 = move1
        x2, y2, dx2, dy2, step2 = move2
        for i in range(max(step1, step2)):
            # 每一秒走一步
            if i < step1:
                x1 += dx1
                y1 += dy1
            if i < step2:
                x2 += dx2
                y2 += dy2
            if x1 == x2 and y1 == y2:  # 重叠
                return False
        return True

    def countCombinations(self, pieces: List[str], positions: List[List[int]]) -> int:
        rook_dirs = (-1, 0), (1, 0), (0, -1), (0, 1)  # 上下左右
        bishop_dirs = (1, 1), (-1, 1), (-1, -1), (1, -1)  # 斜向
        piece_dirs = {'r': rook_dirs, 'b': bishop_dirs, 'q': rook_dirs + bishop_dirs}
        # 预处理所有合法移动
        all_moves = [self.generate_moves(x, y, piece_dirs[piece[0]])
                     for piece, (x, y) in zip(pieces, positions)]

        n = len(pieces)
        path = [None] * n  # 注意 path 的长度是固定的
        ans = 0
        def dfs(i: int) -> None:
            if i == n:
                nonlocal ans
                ans += 1
                return
            # 枚举当前棋子的所有合法移动
            for move1 in all_moves[i]:
                # 判断合法移动 move1 是否有效
                if all(self.is_valid(move1, move2) for move2 in path[:i]):
                    path[i] = move1  # 直接覆盖，无需恢复现场
                    dfs(i + 1)  # 枚举后续棋子的所有合法移动组合
        dfs(0)
        return ans
''',
    call="Solution().countCombinations(['bishop', 'bishop'], [[3, 3], [1, 1]])",
    expect=60,
    skip=['SIZE = 8', 'for dx, dy in dirs', 'x, y = x0 + dx', 'step = 1', 'while 0 < x', 'moves.append', 'x += dx', 'y += dy',
          'step += 1', 'x1, y1, dx1', 'x2, y2, dx2', 'for i in range(max', 'if i < step', 'x1 += dx1', 'y1 += dy1',
          'x2 += dx2', 'y2 += dy2', 'if x1 == x2', 'return False', 'return True', 'rook_dirs =', 'bishop_dirs =',
          'piece_dirs =', 'n = len(pieces)', 'ans = 0', 'path = [None]', 'nonlocal ans', 'def dfs', 'if i == n', 'path[i] = move1', 48, 39, 'moves = [(x0', 'return moves'],
    max_steps=42,
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='calls', h=120),
    ],
    watch=['i', ('ans', 'ans', 'green')],
    captions={
        'all_moves = [': lambda S, B, r: f'预处理：每个棋子的合法移动 = 原地不动 + 每个方向走 1,2,3… 步；象A 共 `{len(S.all_moves[0])}` 种，象B 共 `{len(S.all_moves[1])}` 种',
        'for move1 in all_moves[i]': lambda S, B, r: (f'{NAMES[S.i]}的合法移动都试完了，回到上一层' if B.get('move1') == S.move1 and B.get('i') == S.i
                                                  else f'枚举第 `{S.i}` 个棋子（{NAMES[S.i]}）的合法移动：`{_mv(S.move1)}`'),
        'if all(': _all,
        'dfs(i + 1)': lambda S, B, r: (f'有效 → 记为 `path[{B.i}]`（长度固定，直接覆盖，无需恢复现场），再去枚举{NAMES[B.i + 1]}的合法移动' if B.i + 1 < len(PIECES)
                                      else f'有效 → 记为 `path[{B.i}]`，所有棋子都选好了'),
        'ans += 1': '所有棋子都选好移动且从未重叠 → 又找到一个有效组合，`ans` = =={ans}==',
        'dfs(0)': '从第 0 个棋子开始回溯',
        'return ans': '所有组合枚举完，有效组合共 =={ret}== 个',
    },
    cards=dict(
        one_liner='先列出每个棋子所有合法移动，再回溯逐个挑，冲突就剪枝',
        complexity='时间 `O(n L M^n)`，空间 `O(n M)`',
        problem=['8×8 棋盘上有最多 4 个棋子（车 / 后 / 象），每个棋子选一个方向和步数，==同时==每秒走一步',
                 '任意时刻两个棋子占同一格就==无效==；可以原地不动',
                 '示例：`["rook"]` `[[1,1]]` → `15`；本视频用两个象 `(3,3)`、`(1,1)` → `60`'],
        quote='写一个回溯，暴力枚举每个棋子的每个合法移动，如果这些棋子没有重叠在一起，则答案加一。……如果当前棋子的当前这个合法移动，与前面的棋子冲突，那么不往下递归，枚举当前棋子的下一个合法移动。',
        quote_src='—— 灵茶山艾府题解',
        idea=['合法移动 = (起点, 方向 `dx,dy`, 步数 `step`)，原地不动是 `step = 0`',
              '回溯第 `i` 个棋子：试它的每个移动，先和 `path[:i]` 逐个用 `is_valid` 检查',
              '`is_valid` 模拟每一秒：两个棋子各走一步，位置相同就重叠；走完的棋子停在终点',
              '有冲突就跳过（剪枝），没冲突才记入 `path[i]` 并递归'],
        summary=['时间 `O(n L M^n)`：`M` 是单个棋子的移动数（至多约 28），`n ≤ 4`',
                 '易错：棋子到终点后==仍然占着那一格==，会挡住别人（所以循环用 `max(step1, step2)`）',
                 '交换位置不算重叠：两格相邻时只检查整数秒的位置即可',
                 '`path` 长度固定，递归时直接覆盖，不用回溯恢复',
                 '视频里 `is_valid` 的逐秒模拟没有逐行展示，红叉标出了第一次重叠的秒和格子'],
    ),
)
