def _queens(S):
    """本写法不存 queens 数组：从 col / diag1 / diag2 三个标记数组反推已放好的皇后（第 i 行在第 q[i] 列）"""
    n, col, d1, d2 = S['n'], S['col'], S['diag1'], S['diag2']
    cols = [c for c in range(n) if col[c]]
    k = len(cols)
    want1 = {i for i, v in enumerate(d1) if v}
    want2 = {i for i, v in enumerate(d2) if v}
    m = 2 * n - 1
    for p in permutations(cols):
        if {i + p[i] for i in range(k)} == want1 and {(i - p[i]) % m for i in range(k)} == want2:
            return list(p)
    return []


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'diag2' not in S:
        return
    n = S['n']
    col, d1, d2 = S['col'], S['diag1'], S['diag2']
    inner = S.get('_inner', {})
    r, c = inner.get('r'), inner.get('c')
    q = _queens(S)
    k = len(q)
    m = 2 * n - 1
    cv.text((x0 + 18, y0 + 4), f'棋盘（Q = 已放的皇后，× = 被攻击，蓝框 = 正在试的格子）   方案数 ans = {S.get("ans", 0)}',
            22, T['muted'], bold=True)
    cs, bx, by = 58, x0 + 34, y0 + 46
    for i in range(n):
        cv.text((bx - 10, by + i * cs + cs / 2), i, 18, T['muted'], anchor='rm', mono=True)
        for j in range(n):
            placed = i < k and q[i] == j
            attacked = (not placed) and i >= k and (col[j] or d1[i + j] or d2[i - j])
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
    trying = r is not None and c is not None and r < n and S.get('_line') in (13, 14, 15, 16)
    if trying:
        X, Y = bx + c * cs, by + r * cs
        cv.rect((X - 1, Y - 1, X + cs + 1, Y + cs + 1), outline=T['blue'], width=4, r=8)
    fx, ac = x0 + 330, 40
    rows = [('col[c]', col, list(range(n)), c if trying else None),
            ('diag1[r+c]  ↗', d1, list(range(m)), (r + c) if trying else None),
            ('diag2[r-c]  ↖', d2, [t if t < n else t - m for t in range(m)], ((r - c) % m) if trying else None)]
    yy = y0 + 46
    for name, arr, labels, hi in rows:
        cv.text((fx, yy + ac / 2), name, 20, T['muted'], anchor='lm', mono=True, bold=True)
        ax = fx + 180
        for t, v in enumerate(arr):
            X = ax + t * (ac + 4)
            cv.rect((X, yy, X + ac, yy + ac), fill=T['orange'] if v else T['panel2'], r=6,
                    outline=T['blue'] if t == hi else T['border'], width=3 if t == hi else 1)
            cv.text((X + ac / 2, yy + ac / 2), 'T' if v else '', 20, T['bg'], anchor='mm', bold=True)
            cv.text((X + ac / 2, yy + ac + 4), labels[t], 16, T['dim'], anchor='mt', mono=True)
        yy += ac + 34
    cv.text((fx, yy + 2), '只数个数，不存棋盘：三个布尔数组就是全部状态', 18, T['dim'])


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
        return f'`({r}, {c})` 被攻击（' + '、'.join(why) + '）→ 跳过'
    return f'`({r}, {c})` 列和两条斜线都空着 → ==可以放=='


def _if_end(S, B, ret):
    r = S.r
    if r == S.n:
        return f'`r == n = {S.n}`：每一行都放下了皇后 → ==找到一个合法方案=='
    return f'来到第 `{r}` 行：枚举这一行的皇后放在哪一列'


CONFIG = dict(
    num=52, title='N 皇后 II', difficulty='Hard', category='回溯',
    author='灵茶山艾府', technique='排列型回溯 · 只计数不存方案',
    tags=['面试经典150'],
    code='''
class Solution:
    def totalNQueens(self, n: int) -> int:
        ans = 0
        col = [False] * n
        diag1 = [False] * (n * 2 - 1)
        diag2 = [False] * (n * 2 - 1)
        def dfs(r: int) -> None:
            if r == n:
                nonlocal ans
                ans += 1  # 找到一个合法方案
                return
            for c, ok in enumerate(col):
                if not ok and not diag1[r + c] and not diag2[r - c]:
                    col[c] = diag1[r + c] = diag2[r - c] = True
                    dfs(r + 1)
                    col[c] = diag1[r + c] = diag2[r - c] = False  # 恢复现场
        dfs(0)
        return ans
''',
    call='Solution().totalNQueens(4)',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='calls', h=300),
    ],
    watch=[('r', lambda S: S['_inner'].get('r'), 'blue'), ('c', lambda S: S['_inner'].get('c'), 'blue'),
           ('ans', 'ans', 'green')],
    skip=['for c, ok in enumerate(col)'],
    captions={
        'ans = 0': '`ans` 只记录方案个数——这题==不用生成棋盘==',
        'col = [False] * n': '`col[c]`：第 `c` 列是否已有皇后（相当于全排列里的 `on_path`）',
        'diag1 = [False]': '`diag1[r+c]`：↗ 斜线上 `r+c` 相同，共 `2n-1` 条',
        'diag2 = [False]': '`diag2[r-c]`：↖ 斜线上 `r-c` 相同，也是 `2n-1` 条',
        'dfs(0)': '从第 `0` 行开始，每行放一个皇后',
        'if r == n': _if_end,
        'ans += 1': '找到一个合法方案：`ans` → =={ans}==',
        '                return': '计数完毕，返回上一层继续试别的列',
        'if not ok and not diag1': _check,
        'col[c] = diag1[r + c] = diag2[r - c] = True': lambda S, B, ret: (
            f"放下皇后 `({S.r}, {S.c})`：占用列 `{S.c}`、"
            f"↗ `{S.r + S.c}`、↖ `{S.r - S.c}`"),
        'dfs(r + 1)': lambda S, B, ret: f"递归 `dfs({S.r})`：去下一行",
        'col[c] = diag1[r + c] = diag2[r - c] = False': lambda S, B, ret: (
            f"回到第 `{S.r}` 行，==恢复现场==：拿走 `({S.r}, {S.c})` 的皇后，试下一列"),
        'return ans': '整棵搜索树走完：`{n}` 皇后共有 =={ret}== 种放法',
    },
    max_steps=75,
    cards=dict(
        one_liner='和 51 题同一套排列型回溯，到达第 n 行时只做 ans += 1',
        complexity='时间 `O(n·n!)`，空间 `O(n)`',
        problem=['`n×n` 棋盘放 `n` 个皇后，任意两个不能==同行、同列、同一条斜线==',
                 '只要返回==不同放法的数量==',
                 '示例：`n = 4` → `2`；`n = 1` → `1`'],
        quote='对于全排列的枚举……搜索树的节点个数为 `floor(e·n!)`……每个非叶节点需要 `O(n)` 的时间遍历数组，所以时间复杂度为 `O(n·n!)`。',
        quote_src='—— 灵茶山艾府题解「复杂度分析」',
        idea=['每行恰好一个皇后 → 本质是==枚举列号的全排列==（排列型回溯）',
              '同一条 ↗ 斜线 `r+c` 相同，同一条 ↖ 斜线 `r-c` 相同，用布尔数组 `O(1)` 判断',
              '递归到 `r == n` 说明 n 行都放好了：`ans += 1`，不必拼棋盘'],
        result='两种放法都数到了：返回 `2` ✓（第二种在快进部分，过程同理）',
        summary=['`O(n·n!)` 只是上界：`n = 9` 时只有 352 种方案，远小于 `9! = 362880`',
                 '`ans` 定义在外层，内层要 `nonlocal ans` 才能累加',
                 '`col / diag1 / diag2` 递归返回后==必须恢复现场==',
                 '`diag2[r - c]` 下标可能为负，Python 从末尾数，长度 `2n-1` 恰好不冲突',
                 '对比 51 题：去掉 `queens` 数组和拼棋盘，只计数'],
    ),
)
