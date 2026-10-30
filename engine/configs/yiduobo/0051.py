def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'right_slash' not in S or 'now' not in S:
        return
    n, now = S['n'], S['now']
    if 'level' not in S and S.get('res') is not None:  # 搜索结束后的转换阶段：画出正在转换的解
        now = S['res']
    col, ls, rs = S['column'], S['left_slash'], S['right_slash']
    lv, idx = S.get('level'), S.get('index')
    m = 2 * n - 1
    cv.text((x0 + 18, y0 + 4), '棋盘（Q = now 里的皇后，× = 被覆盖，蓝框 = (level, index)）', 22, T['muted'], bold=True)
    cs, bx, by = 58, x0 + 34, y0 + 46
    k = len(now)
    for i in range(n):
        cv.text((bx - 10, by + i * cs + cs / 2), i, 18, T['muted'], anchor='rm', mono=True)
        for j in range(n):
            placed = i < k and now[i] == j
            attacked = (not placed) and i >= k and (col[j] or ls[i + j] or rs[i - j + n - 1])
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
    ok = lv is not None and idx is not None and lv < n
    if ok:
        X, Y = bx + idx * cs, by + lv * cs
        cv.rect((X - 1, Y - 1, X + cs + 1, Y + cs + 1), outline=T['blue'], width=4, r=8)
    fx, ac = x0 + 330, 40
    rows = [('column[index]', col, idx if ok else None),
            ('left_slash[index+level]', ls, (idx + lv) if ok else None),
            ('right_slash[level-index+n-1]', rs, (lv - idx + n - 1) if ok else None)]
    yy = y0 + 40
    for name, arr, hi in rows:
        cv.text((fx, yy), name, 19, T['muted'], mono=True, bold=True)
        yy += 26
        for kk, v in enumerate(arr):
            X = fx + kk * (ac + 4)
            cv.rect((X, yy, X + ac, yy + ac), fill=T['orange'] if v else T['panel2'], r=6,
                    outline=T['blue'] if kk == hi else T['border'], width=3 if kk == hi else 1)
            cv.text((X + ac / 2, yy + ac / 2), 'T' if v else '', 20, T['bg'], anchor='mm', bold=True)
            cv.text((X + ac / 2, yy + ac + 2), kk, 15, T['dim'], anchor='mt', mono=True)
        yy += ac + 24


_st = {'fresh': False}  # for pos 是否刚开始一个新的解


def _res_str(S, B, ret):
    _st['fresh'] = True
    return '`res_str` 收集这个解的 `n` 行'


def _for_pos(S, B, ret):
    fresh, _st['fresh'] = _st['fresh'], False
    if 'pos' in S and (fresh or S.pos != B.get('pos')):
        return f'这一行皇后在第 `{S.pos}` 列'
    return '这个解的每一行都画好了'


def _check(S, B, ret):
    lv, i, n = S.level, S.index, S.n
    why = []
    if S.column[i]:
        why.append(f'列 `{i}`')
    if S.left_slash[i + lv]:
        why.append(f'左斜线 `{i + lv}`')
    if S.right_slash[lv - i + n - 1]:
        why.append(f'右斜线 `{lv - i + n - 1}`')
    if why:
        return f'`({lv}, {i})` 被覆盖（' + '、'.join(why) + '）→ ×'
    return f'`({lv}, {i})` 没被覆盖 → ==可以放=='


CONFIG = dict(
    num=51, title='N 皇后', difficulty='Hard', category='回溯',
    author='yiduobo', technique='按行搜索回溯 · 列 / 左斜线 / 右斜线覆盖标记',
    code='''
class Solution(object):
    def solveNQueens(self, n):
        res_list = []

        column = [False] * n
        left_slash = [False] * (n + n - 1)
        right_slash = [False] * (n + n - 1)

        now = []

        self.dfs(n, 0, now, column, left_slash, right_slash, res_list)

        res_str_list = []
        for res in res_list:
            res_str = []
            for pos in res:
                res_str.append('.' * pos + 'Q' + '.' * (n - 1 - pos))
            res_str_list.append(res_str)
        return res_str_list

    def dfs(self, n, level, now, column, left_slash, right_slash, res_list):
        if n == level:
            res_list.append(now[:])
            return

        for index in range(n):
            if not (column[index] or left_slash[index + level] or right_slash[level - index + n - 1]):
                now.append(index)
                column[index] = True
                left_slash[index + level] = True
                right_slash[level - index + n - 1] = True
                self.dfs(n, level + 1, now, column, left_slash, right_slash, res_list)
                right_slash[level - index + n - 1] = False
                left_slash[index + level] = False
                column[index] = False
                now.pop()
''',
    call='Solution().solveNQueens(4)',
    expect=[['.Q..', '...Q', 'Q...', '..Q.'], ['..Q.', 'Q...', '...Q', '.Q..']],
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='calls', h=226),
        dict(type='stack', var='res_list', label='res_list（每行皇后所在的列）', h=96),
    ],
    watch=[('level', 'level', 'blue'), ('index', 'index', 'blue'), ('now', 'now', 'yellow'), ('res_str', 'res_str', 'green')],
    skip=['for index in range(n)', 'column[index] = True', 'left_slash[index + level] = True',
          'right_slash[level - index + n - 1] = False', 'left_slash[index + level] = False'],
    captions={
        'column = [False] * n': '`column[j]`：第 `j` 列是否被覆盖',
        'left_slash = [False]': '左斜线上 `i + j` 相等，`n×n` 棋盘共 `2n-1` 条',
        'right_slash = [False]': '右斜线上 `i - j` 相等，可能小于 0 → 统一==加上 n-1==，也是 `2n-1` 条',
        'now = []': '`now[i]`：第 `i` 行皇后放在哪一列',
        'self.dfs(n, 0, now': '按行搜索：从第 `0` 行开始',
        'if n == level': lambda S, B, ret: (
            f'`level == n`：每一行都放好了 → 一个解 `{S.now}`' if S.level == S.n else
            f'第 `{S.level}` 行：枚举放哪一列'),
        'res_list.append(now[:])': '复制 now 记入 `res_list`：`{res_list[-1]}`',
        '            return': '返回上一行，继续枚举',
        'if not (column[index]': _check,
        'now.append(index)': '第 `{level}` 行放第 `{index}` 列：`now = {now}`',
        'right_slash[level - index + n - 1] = True': lambda S, B, ret: (
            f'覆盖：列 `{S.index}`、左斜线 `{S.index + S.level}`、右斜线 `{S.level - S.index + S.n - 1}`'
            + ('（这三行合并成一步显示）' if S.level == 0 and S.index == 0 else '')),
        'self.dfs(n, level + 1': '搜索下一行：`level = {level}`',
        'column[index] = False': '回到第 `{level}` 行：撤销三个覆盖标记',
        'now.pop()': '弹出 `{B.now[-1]}`，第 `{level}` 行换下一个位置',
        'res_str_list = []': '搜索结束，把每个解（列号列表）转成棋盘字符串',
        'for res in res_list': lambda S, B, ret: (
            f'取一个解 `res = {S.res}`' if S.get('res') != B.get('res') else '全部转换完'),
        'res_str = []': _res_str,
        'for pos in res': _for_pos,
        "res_str.append('.' * pos": "`'.' * {pos} + 'Q' + '.' * {n - 1 - pos}` = `'{res_str[-1]}'`",
        'res_str_list.append(res_str)': '一个棋盘画好了',
        'return res_str_list': '返回全部 `{len(ret)}` 个棋盘',
    },
    max_steps=88,
    cards=dict(
        one_liner='按行放皇后，用列 / 左斜线 / 右斜线三个数组记录覆盖',
        complexity='时间 `O(n·n!)` 量级（实际远小于），空间 `O(n)`',
        problem=['`n×n` 棋盘放 `n` 个皇后，任意两个不能同行、同列、同斜线，返回所有放法',
                 '示例：`n = 4` → `[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]`'],
        quote='第 i 行第 j 列的棋子，覆盖掉了第 i 行，第 j 列，以及一条左斜线和一条右斜线。同一左斜线满足 ==i + j 相等==，同一右斜线满足 ==i - j 相等==，需要统一加上 n - 1。',
        quote_src='—— yiduobo 题解',
        idea=['按行搜索，每行只放一个 → 行冲突天然避免',
              '放下皇后：同时标记 `column`、`left_slash`、`right_slash` 三个数组',
              '回来时按相反顺序撤销三个标记，并 `now.pop()`'],
        result='找到 2 个解 ✓（第二个解在快进部分，过程同理）',
        summary=['按行放、列不重复 → 本质是列号的排列，至多 `n!` 个叶子',
                 '`n×n` 棋盘有 `2n-1` 条左斜线和 `2n-1` 条右斜线',
                 '右斜线下标 `level - index` 可能为负，要加 `n-1` 平移',
                 '原文说 51 和 52 题本质一样：52 只需把 `res_list.append` 换成计数',
                 '原文为 Python 2 风格，仅删去 docstring；演示时把连续三行标记合并成一步'],
    ),
)
