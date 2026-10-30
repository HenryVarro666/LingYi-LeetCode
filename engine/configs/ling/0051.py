def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'diag2' not in S:
        return
    n, q = S['n'], S['queens']
    col, d1, d2 = S['col'], S['diag1'], S['diag2']
    r, c = S.get('r'), S.get('c')
    m = 2 * n - 1
    cv.text((x0 + 18, y0 + 4), '棋盘（Q = 皇后，× = 被攻击，蓝框 = 正在试的 (r, c)）', 22, T['muted'], bold=True)
    cs, bx, by = 58, x0 + 34, y0 + 46
    for i in range(n):
        cv.text((bx - 10, by + i * cs + cs / 2), i, 18, T['muted'], anchor='rm', mono=True)
        for j in range(n):
            placed = r is not None and q[i] == j and (i < r or (i == r and col[j] and d1[i + j] and d2[i - j]))
            attacked = (not placed) and r is not None and i >= r and (col[j] or d1[i + j] or d2[i - j])
            X, Y = bx + j * cs, by + i * cs
            base = T['panel2'] if (i + j) % 2 == 0 else (40, 47, 58)
            fill = T['yellow'] if placed else ((70, 34, 38) if attacked else base)
            cv.rect((X + 2, Y + 2, X + cs - 2, Y + cs - 2), fill=fill, outline=T['border'], width=1, r=6)
            if placed:
                cv.text((X + cs / 2, Y + cs / 2), 'Q', 30, T['bg'], anchor='mm', bold=True)
            elif attacked:
                cv.text((X + cs / 2, Y + cs / 2), '×', 26, T['red'], anchor='mm', bold=True)
    for j in range(n):
        cv.text((bx + j * cs + cs / 2, by + n * cs + 4), j, 18, T['muted'], anchor='mt', mono=True)
    if r is not None and c is not None and r < n:
        X, Y = bx + c * cs, by + r * cs
        cv.rect((X - 1, Y - 1, X + cs + 1, Y + cs + 1), outline=T['blue'], width=4, r=8)
    # 右侧：三个标记数组
    fx, ac = x0 + 330, 40
    rows = [('col[c]', col, list(range(n)), (c if c is not None else None)),
            ('diag1[r+c]  ↗', d1, list(range(m)), (r + c if r is not None and c is not None and r < n else None)),
            ('diag2[r-c]  ↖', d2, [k if k < n else k - m for k in range(m)],
             ((r - c) % m if r is not None and c is not None and r < n else None))]
    yy = y0 + 46
    for name, arr, labels, hi in rows:
        cv.text((fx, yy + ac / 2), name, 20, T['muted'], anchor='lm', mono=True, bold=True)
        ax = fx + 180
        for k, v in enumerate(arr):
            X = ax + k * (ac + 4)
            cv.rect((X, yy, X + ac, yy + ac), fill=T['orange'] if v else T['panel2'], r=6,
                    outline=T['blue'] if k == hi else T['border'], width=3 if k == hi else 1)
            cv.text((X + ac / 2, yy + ac / 2), 'T' if v else '', 20, T['bg'], anchor='mm', bold=True)
            cv.text((X + ac / 2, yy + ac + 4), labels[k], 16, T['dim'], anchor='mt', mono=True)
        yy += ac + 34
    cv.text((fx, yy + 2), 'diag2 的下标 r−c 可以是负数：Python 负下标从数组末尾数', 18, T['dim'])


def _check(S, B, ret):
    r, c = S.r, S.c
    why = []
    if S.col[c]:
        why.append(f'列 `{c}`')
    if S.diag1[r + c]:
        why.append(f'↗`{r + c}`')
    if S.diag2[r - c]:
        why.append(f'↖`{r - c}`')
    if why:
        return f'`({r}, {c})` 被攻击（' + '、'.join(why) + '）→ ×'
    return f'`({r}, {c})` 安全 → ==放皇后=='


CONFIG = dict(
    num=51, title='N 皇后', difficulty='Hard', category='回溯',
    author='灵茶山艾府', technique='排列型回溯 · 列号全排列 + 斜线 O(1) 判断',
    code='''
class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        ans = []
        queens = [0] * n  # 皇后放在 (r,queens[r])
        col = [False] * n
        diag1 = [False] * (n * 2 - 1)
        diag2 = [False] * (n * 2 - 1)
        def dfs(r: int) -> None:
            if r == n:
                ans.append(['.' * c + 'Q' + '.' * (n - 1 - c) for c in queens])
                return
            # 在 (r,c) 放皇后
            for c, ok in enumerate(col):
                if not ok and not diag1[r + c] and not diag2[r - c]:  # 判断能否放皇后
                    queens[r] = c  # 直接覆盖，无需恢复现场
                    col[c] = diag1[r + c] = diag2[r - c] = True  # 皇后占用了 c 列和两条斜线
                    dfs(r + 1)
                    col[c] = diag1[r + c] = diag2[r - c] = False  # 恢复现场
        dfs(0)
        return ans
''',
    call='Solution().solveNQueens(4)',
    expect=[['.Q..', '...Q', 'Q...', '..Q.'], ['..Q.', 'Q...', '...Q', '.Q..']],
    views=[
        dict(type='custom', draw=_draw, h=290),
        dict(type='calls', h=248),
        dict(type='stack', var='ans', label='ans（每个方案写成各行皇后的列号）', h=96,
             fmt=lambda b: '[' + ','.join(str(row.index('Q')) for row in b) + ']'),
    ],
    watch=[('r', 'r', 'blue'), ('c', 'c', 'blue'), ('queens', 'queens', 'yellow')],
    skip=['for c, ok in enumerate(col)'],
    captions={
        'queens = [0] * n': '`queens[r]`：第 `r` 行的皇后放在第几列（每行恰好一个）',
        'col = [False] * n': '`col[c]`：第 `c` 列有没有皇后',
        'diag1 = [False]': '`diag1[r+c]`：↗ 方向的斜线，同一条线上 `r+c` 相同，共 `2n-1` 条',
        'diag2 = [False]': '`diag2[r-c]`：↖ 方向的斜线，同一条线上 `r-c` 相同',
        'dfs(0)': '从第 `0` 行开始放',
        'if r == n': lambda S, B, ret: (
            f'`r == n`：`{S.n}` 行都放好了 → ==得到一个方案== `queens = {S.queens}`' if S.r == S.n else
            f'第 `{S.r}` 行：逐列尝试'),
        'ans.append': '把 `queens` 画成棋盘字符串，加入 ans',
        '                return': '返回上一层，继续试别的列',
        'if not ok and not diag1': _check,
        'queens[r] = c': lambda S, B, ret: (f'`queens[{S.r}] = {S.c}`' + ('：==直接覆盖，无需恢复现场==' if not S.ans and S.r < 2 else '（直接覆盖）')),
        'col[c] = diag1[r + c] = diag2[r - c] = True': '占用：列 `{c}`、↗ 斜线 `{r + c}`、↖ 斜线 `{r - c}`',
        'dfs(r + 1)': '递归 `dfs({r})`：去第 `{r}` 行',
        'col[c] = diag1[r + c] = diag2[r - c] = False': '回到第 `{r}` 行，恢复现场：释放列 `{c}` 和两条斜线',
        'return ans': '搜索结束，共 `{len(ret)}` 种放法',
    },
    max_steps=84,
    cards=dict(
        one_liner='每行一个皇后 → 枚举列号的全排列，斜线用 r+c / r−c 判断',
        complexity='时间 `O(n²·n!)`，空间 `O(n)`（不计返回值）',
        problem=['`n×n` 棋盘放 `n` 个皇后，任意两个不能同行、同列、同斜线，返回所有放法',
                 '示例：`n = 4` → `[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]`'],
        quote='由于每行恰好放一个皇后，记录每行的皇后放在哪一列，可以得到一个 `[0,n-1]` 的排列 `queens`……所以我们本质上是在==枚举列号的全排列==。',
        quote_src='—— 灵茶山艾府题解「答疑」',
        idea=['和 46 全排列一样：`col[c]` 就是 `on_path`',
              '↗ 方向行号加列号不变，↖ 方向行号减列号不变',
              '用 `diag1[r+c]`、`diag2[r-c]` 标记，`O(1)` 判断是否被攻击'],
        result='2 种放法全部找到 ✓（第二个方案在快进部分，过程同理）',
        summary=['`O(n²·n!)`：至多 `n!` 个叶子，每个生成棋盘 `O(n²)`；实际 `n=9` 只有 352 种',
                 '`queens` 定长直接覆盖；`col / diag1 / diag2` 必须恢复现场',
                 '`diag2[r - c]` 的下标可能为负，Python 会从数组末尾数，长度 `2n-1` 正好不冲突',
                 '同类：52 N 皇后 II（只数个数）'],
    ),
)
