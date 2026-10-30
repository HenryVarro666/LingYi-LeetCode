def _mat(cv, T, x, y, M, cell, label, changed=None, tint=None, outline=None, labelcol=None):
    """画一个小矩阵，返回 (宽, 高)。tint(i,j)->颜色名或 None；changed(i,j)->bool"""
    R = len(M)
    C = max([len(r) for r in M] + [1])
    cv.text((x, y), label, 22, labelcol or T['muted'], bold=True)
    y0 = y + 34
    for i in range(R):
        for j in range(len(M[i])):
            v = M[i][j]
            X, Y = x + j * cell, y0 + i * cell
            c = tint(i, j) if tint else None
            fill = T[c] if c else T['panel2']
            ch = changed(i, j) if changed else False
            cv.rect((X + 2, Y + 2, X + cell - 2, Y + cell - 2), fill=fill, r=6,
                    outline=T['yellow'] if ch else T['border'], width=4 if ch else 1)
            if isinstance(v, bool):
                v = 'T' if v else 'F'
            cv.text((X + cell / 2, Y + cell / 2), v, 26, T['bg'] if c else T['text'], anchor='mm', bold=True)
    return C * cell, R * cell + 34


GRID = [[1, 2, 2], [3, 2, 2]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    line = S.get('_line', 0)
    cell = 54
    grid = S['grid']
    k, i, j = S.get('k'), S.get('i'), S.get('j')

    def tint_grid(a, b):
        if k is None or i is None or j is None or line < 20:
            return None
        if 20 <= line <= 29:   # 第一段：k 行的窗口向右滑，比较第 j-1 列与第 j 列的列和
            if i - k <= a <= i - 1:
                if b == j:
                    return 'blue'
                if b == j - 1:
                    return 'pink'
            return None
        if line >= 31 and 'sum_row' in S:  # 第二段：k×k 窗口
            if i - k <= a <= i - 1 and j - k <= b <= j - 1:
                return 'green' if line >= 40 else 'blue'
        return None

    def chg(name):
        def f(a, b):
            Bv = B.get(name)
            try:
                return Bv is not None and Bv[a][b] != S[name][a][b]
            except Exception:
                return False
        return f

    px = x0 + 24
    py = y0 + 6
    w1, h1 = _mat(cv, T, px, py, grid, cell, 'grid', tint=tint_grid)
    rs = S.get('row_sum')
    if rs:
        w2, _ = _mat(cv, T, px + w1 + 40, py, rs, cell, 'row_sum →', changed=chg('row_sum'))
        cs = S['col_sum']
        _mat(cv, T, px + w1 + w2 + 80, py, cs, cell, 'col_sum ↓', changed=chg('col_sum'))
        y2 = py + h1 + 110
        ds, an = S['diag_sum'], S['anti_sum']
        w3, h3 = _mat(cv, T, px, y2, ds, cell, 'diag_sum ↘', changed=chg('diag_sum'))
        w4, _ = _mat(cv, T, px + w3 + 40, y2, an, cell, 'anti_sum ↙', changed=chg('anti_sum'))
        sc = S.get('is_same_col_sum')
        if sc:
            _mat(cv, T, px + w3 + w4 + 70, y2, sc, cell, 'is_same_col_sum',
                 tint=lambda a, b: 'green' if sc[a][b] else None, changed=chg('is_same_col_sum'))


def _info(S):
    if 'k' not in S:
        return '先建四种前缀和，再从大到小枚举边长 `k`'
    line = S['_line']
    k = S['k']
    if 20 <= line <= 29:
        return f'`k = {k}`：窗口向右滑，`same_cnt = {S.get("same_cnt")}`（连续列和相同的列数）'
    if line >= 31 and 'sum_row' in S:
        return f'`k = {k}`：窗口向下滑，`sum_row = {S["sum_row"]}`，`same_cnt = {S.get("same_cnt")}`（连续行和相同的行数）'
    return f'`k = {k}`'


CONFIG = dict(
    num=1895, title='最大的幻方', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='四种前缀和 + 滑动窗口计数',
    tags=['前缀和', '进阶', '难度分 1781'],
    code='''
class Solution:
    def largestMagicSquare(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        row_sum = [[0] * (n + 1) for _ in range(m)]       # → 前缀和
        col_sum = [[0] * n for _ in range(m + 1)]         # ↓ 前缀和
        diag_sum = [[0] * (n + 1) for _ in range(m + 1)]  # ↘ 前缀和
        anti_sum = [[0] * (n + 1) for _ in range(m + 1)]  # ↙ 前缀和

        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                row_sum[i][j + 1] = row_sum[i][j] + x
                col_sum[i + 1][j] = col_sum[i][j] + x
                diag_sum[i + 1][j + 1] = diag_sum[i][j] + x
                anti_sum[i + 1][j] = anti_sum[i][j + 1] + x

        # is_same_col_sum[i][j] 表示右下角为 (i, j) 的子矩形，每列元素和是否都相等
        is_same_col_sum = [[False] * n for _ in range(m)]

        for k in range(min(m, n), 1, -1):
            for i in range(k, m + 1):
                # 想象有一个 k×k 的窗口在向右滑动
                same_cnt = 1
                for j in range(1, n):
                    if col_sum[i][j] - col_sum[i - k][j] == col_sum[i][j - 1] - col_sum[i - k][j - 1]:
                        same_cnt += 1
                    else:
                        same_cnt = 1
                    # 连续 k 列元素和是否都一样
                    is_same_col_sum[i - 1][j] = same_cnt >= k

            for j in range(k, n + 1):
                # 想象有一个 k×k 的窗口在向下滑动
                sum_row = row_sum[0][j] - row_sum[0][j - k]
                same_cnt = 1
                for i in range(2, m + 1):
                    row_s = row_sum[i - 1][j] - row_sum[i - 1][j - k]
                    if row_s == sum_row:
                        same_cnt += 1
                        if (same_cnt >= k and  # 连续 k 行元素和都一样
                            is_same_col_sum[i - 1][j - 1] and  # 连续 k 列元素和都一样
                            col_sum[i][j - 1] - col_sum[i - k][j - 1] == sum_row and  # 列和 = 行和
                            diag_sum[i][j] - diag_sum[i - k][j - k] == sum_row and  # 主对角线和 = 行和
                            anti_sum[i][j - k] - anti_sum[i - k][j] == sum_row):  # 反对角线和 = 行和
                            return k
                    else:
                        sum_row = row_s
                        same_cnt = 1

        return 1
''',
    call=f'Solution().largestMagicSquare({GRID!r})',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=560),
        dict(type='text', h=70, size=28, fn=_info),
    ],
    skip=[12, 13, 14],
    max_steps=80,
    watch=[('k', 'k', 'blue'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('same_cnt', 'same_cnt', 'yellow'), ('sum_row', 'sum_row', 'green')],
    captions={
        'row_sum = ': '`row_sum[i][j]`：第 `i` 行前 `j` 个数之和（→）',
        'col_sum = ': '`col_sum[i][j]`：第 `j` 列前 `i` 个数之和（↓）',
        'diag_sum = ': '`diag_sum`：沿 ↘ 方向累加，用来一次算出主对角线和',
        'anti_sum = ': '`anti_sum`：沿 ↙ 方向累加，用来一次算出反对角线和',
        'row_sum[i][j + 1] = ': '格子 `({i}, {j})` = {x}：四种前缀和各加一格（行 {row_sum[i][j + 1]}、列 {col_sum[i + 1][j]}、↘ {diag_sum[i + 1][j + 1]}、↙ {anti_sum[i + 1][j]}）',
        'is_same_col_sum = ': '`is_same_col_sum[i][j]`：右下角为 `(i, j)` 的窗口，列和是否都相等',
        'for k in range': '从大到小枚举边长 `k = {k}`（不能二分：某个 `k` 成立，不代表更大或更小的 `k` 成立）',
        22: '计数器 `same_cnt` 从 1 开始：连续有多少列的和相同',
        34: '`same_cnt` 从 1 开始：连续有多少行的和相同',
        'if col_sum[i][j] - col_sum': lambda S, B, r: (
            f'比较第 `{S.j}` 列和 `{S.col_sum[S.i][S.j] - S.col_sum[S.i - S.k][S.j]}` 与第 `{S.j - 1}` 列和 '
            f'`{S.col_sum[S.i][S.j - 1] - S.col_sum[S.i - S.k][S.j - 1]}`：'
            + ('相同' if S.col_sum[S.i][S.j] - S.col_sum[S.i - S.k][S.j] == S.col_sum[S.i][S.j - 1] - S.col_sum[S.i - S.k][S.j - 1] else '不同')),
        25: '又一列的列和相同，`same_cnt` → =={same_cnt}==',
        38: '又一行的行和相同，`same_cnt` → =={same_cnt}==',
        27: '和不同，连续被打断，`same_cnt` 重置为 1',
        47: '`same_cnt` 重置为 1：从这一行重新数',
        'is_same_col_sum[i - 1][j] =': '`same_cnt = {same_cnt} >= k = {k}`？→ =={is_same_col_sum[i - 1][j]}==：连续 `k` 列的列和是否都一样',
        'sum_row = row_sum[0]': '窗口在第 `{j - k}`~`{j - 1}` 列，从最上面一行开始：`sum_row` = =={sum_row}==',
        'row_s = ': '窗口下一行的行和 `row_s` = =={row_s}==',
        'if row_s == sum_row': '`row_s = {row_s}` 与 `sum_row = {sum_row}`：' + '{"相同，连续行数 +1" if row_s == sum_row else "不同，从这一行重新开始"}',
        39: '`same_cnt = {same_cnt}`：连续 `k = {k}` 行的行和是否都相同？达到 `k` 才继续检查其余四项',
        40: '连续 `k` 列的列和是否都一样：`is_same_col_sum[{i - 1}][{j - 1}]` = =={is_same_col_sum[i - 1][j - 1]}==',
        41: '列和 `{col_sum[i][j - 1] - col_sum[i - k][j - 1]}` 是否等于行和 `{sum_row}`',
        42: '主对角线和 `{diag_sum[i][j] - diag_sum[i - k][j - k]}` 是否等于行和 `{sum_row}`',
        43: '反对角线和 `{anti_sum[i][j - k] - anti_sum[i - k][j]}` 是否等于行和 `{sum_row}`',
        'return k': '找到最大的幻方，边长 `{k}`',
        'sum_row = row_s': '行和变了，以新的行和为准，重新数',
        'return 1': '`1x1` 一定是幻方',
    },
    cards=dict(
        one_liner='四种前缀和 + 滑动窗口计数：从大到小找第一个幻方',
        complexity='时间 `O(mn·min(m,n))`，空间 `O(mn)`',
        problem=['`k x k` 方阵每一行、每一列和两条对角线之和都相等，就是幻方',
                 '求 `m x n` 矩阵里最大幻方的边长',
                 '示例：`[[5,1,3,1],[9,3,3,1],[1,3,3,8]]` → `2`'],
        quote='本题不能二分答案。「每行每列的元素和都相等」是一个非常刁钻的要求，可能中间的某个 k 满足要求，k 大一点或小一点都无法让每行每列的元素和都相等。',
        quote_src='—— 灵茶山艾府题解',
        idea=['行、列、↘、↙ 四种前缀和，任意连续线段的和都是 `O(1)`',
              '从大到小枚举 `k`：窗口向下滑动，用 `same_cnt` 数连续几行和相同',
              '列同理，提前算出 `is_same_col_sum`；最后只要再核对列和、两条对角线'],
        after=[dict(heading='另一种写法', lines=['方法一：三重循环枚举 `k, i, j`，逐行逐列用 `all(...)` 检查，`O(mn·min(m,n)^2)`',
                                                  '本视频演示的是方法二：用计数器把检查行和列降到 `O(1)`'])],
        summary=['时间 `O(mn·min(m,n))`，空间 `O(mn)`',
                 '前缀和多开一圈，子数组恰为前缀时不用特判',
                 '`k = 1` 一定是幻方，所以 `k` 只枚举到 2，最后 `return 1`',
                 '同类题：1878 菱形和（斜线前缀和）'],
    ),
)
