MAT = [[1, 0, 0, 0], [0, 0, 1, 0], [1, 0, 0, 1]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    line = S.get('_line', 0)
    second = 'res' in S
    title = ('第一趟：累加每行、每列的和' if not second else '第二趟：值为 1 且行和、列和都为 1 → 特殊位置')
    cv.text((x0 + 18, y0 + 4), title, 24, T['muted'], bold=True)
    m, n = len(MAT), len(MAT[0])
    cell = 92
    gx, gy = x0 + 150, y0 + 70
    i, j = S.get('i'), S.get('j')
    sr, sc = S.get('s_row'), S.get('s_col')
    found = set()
    if second and i is not None:
        for a in range(m):
            for b in range(n):
                if (a, b) <= (i, j) and MAT[a][b] == 1 and sum(MAT[a]) == 1 and sum(r[b] for r in MAT) == 1:
                    if (a, b) < (i, j) or line == 17:
                        found.add((a, b))
    for a in range(m):
        cv.text((gx - 20, gy + a * cell + cell / 2), f'行 {a}', 20, T['dim'], anchor='rm')
        for b in range(n):
            X, Y = gx + b * cell, gy + a * cell
            v = MAT[a][b]
            fill = T['green'] if (a, b) in found else (T['panel2'] if v == 0 else (70, 78, 92))
            cv.rect((X + 5, Y + 5, X + cell - 5, Y + cell - 5), fill=fill, r=8, outline=T['border'], width=1)
            cv.text((X + cell / 2, Y + cell / 2), v, 32, T['bg'] if (a, b) in found else (T['text'] if v else T['dim']),
                    anchor='mm', bold=True, mono=True)
    if i is not None and j is not None and 0 <= i < m and 0 <= j < n and line in (10, 11, 16, 17):
        X, Y = gx + j * cell, gy + i * cell
        cv.rect((X, Y, X + cell, Y + cell), outline=T['yellow'], width=4, r=10)
    # s_row（右侧一列）和 s_col（下方一行）
    rx = gx + n * cell + 30
    cv.text((rx + cell / 2, gy - 10), 's_row', 20, T['purple'], anchor='mb', bold=True, mono=True)
    by = gy + m * cell + 30
    cv.text((gx - 20, by + cell / 2), 's_col', 20, T['cyan'], anchor='rm', bold=True, mono=True)
    hi_r = i if (i is not None and line in (10, 11, 16, 17)) else None
    hi_c = j if (j is not None and line in (10, 11, 16, 17)) else None
    if sr is not None:
        bsr = B.get('s_row')
        for a in range(m):
            Y = gy + a * cell
            ch = bsr is not None and bsr[a] != sr[a]
            ok = second and sr[a] == 1
            cv.rect((rx + 5, Y + 5, rx + cell - 5, Y + cell - 5), fill=(50, 44, 70) if a == hi_r else T['panel'], r=8,
                    outline=T['yellow'] if ch else T['purple'], width=3 if ch else 2)
            cv.text((rx + cell / 2, Y + cell / 2), sr[a], 30, T['green'] if ok else T['text'], anchor='mm', bold=True, mono=True)
    if sc is not None:
        bsc = B.get('s_col')
        for b in range(n):
            X = gx + b * cell
            ch = bsc is not None and bsc[b] != sc[b]
            ok = second and sc[b] == 1
            cv.rect((X + 5, by + 5, X + cell - 5, by + cell - 5), fill=(30, 60, 66) if b == hi_c else T['panel'], r=8,
                    outline=T['yellow'] if ch else T['cyan'], width=3 if ch else 2)
            cv.text((X + cell / 2, by + cell / 2), sc[b], 30, T['green'] if ok else T['text'], anchor='mm', bold=True, mono=True)


def _cap_if(S, B, ret):
    i, j = S.i, S.j
    v, r, c = S.mat[i][j], S.s_row[i], S.s_col[j]
    if v != 1:
        return f'`mat[{i}][{j}] = 0`：不是 1，跳过'
    if r != 1:
        return f'`mat[{i}][{j}] = 1`，但第 `{i}` 行和 `s_row[{i}] = {r}` ≠ 1 → 这一行还有别的 1'
    if c != 1:
        return f'`mat[{i}][{j}] = 1`，`s_row[{i}] = 1`，但第 `{j}` 列和 `s_col[{j}] = {c}` ≠ 1 → 这一列还有别的 1'
    return f'`mat[{i}][{j}] = 1`，`s_row[{i}] = 1`，`s_col[{j}] = 1` → ==特殊位置=='


CONFIG = dict(
    num=1582, title='二进制矩阵中的特殊位置', difficulty='Easy', category='矩阵',
    author='yiduobo', technique='先统计行和、列和，再逐格判断',
    tags=['字节30天'],
    code='''
class Solution(object):
    def numSpecial(self, mat):
        m = len(mat)
        n = len(mat[0])

        s_row = [0] * m
        s_col = [0] * n
        for i in range(m):
            for j in range(n):
                s_row[i] += mat[i][j]
                s_col[j] += mat[i][j]

        res = 0
        for i in range(m):
            for j in range(n):
                if mat[i][j] == 1 and s_row[i] == 1 and s_col[j] == 1:
                    res += 1

        return res
''',
    call=f'Solution().numSpecial({MAT})',
    expect=1,
    skip=['for i in range(m)', 'for j in range(n)', 's_row[i] += mat[i][j]', 'n = len(mat[0])', 's_row = [0] * m'],
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), ('res', 'res', 'green')],
    captions={
        'm = len(mat)': '`m = {m}` 行，`n = {len(mat[0])}` 列',
        's_col = [0] * n': '`s_row[i]` 记第 i 行的和，`s_col[j]` 记第 j 列的和，先全 0',
        's_col[j] += mat[i][j]': lambda S, B, ret: (f'`mat[{S.i}][{S.j}] = {S.mat[S.i][S.j]}`：同时加到 `s_row[{S.i}]` 和 `s_col[{S.j}]`'
                                                    + ('' if S.mat[S.i][S.j] else '（加 0 不变）')),
        'res = 0': '行和、列和都统计好了；`res` 计数',
        'if mat[i][j] == 1 and': _cap_if,
        'res += 1': '找到特殊位置 `({i}, {j})`：`res` → {res}',
        'return res': '返回 `{ret}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='特殊位置所在的行和、列和必然都是 1',
        complexity='时间 `O(mn)`，空间 `O(m + n)`',
        problem=['给你 `m × n` 的 01 矩阵 `mat`，统计==特殊位置==的个数',
                 '特殊位置 `(i, j)`：`mat[i][j] == 1`，且第 i 行、第 j 列==其余元素都是 0==',
                 f'示例：`[[1,0,0],[0,0,1],[1,0,0]]` → `1`；本视频 `{MAT}` → `1`'],
        quote='对于特殊位置而言，其所在的行和列上的数字之和必然都是1，因此可以先一趟遍历，计算矩阵中各行各列之和，然后再一趟遍历，若当前位置上的值为1，且其所在行和列的和都是1，那么该位置就是特殊位置了。',
        quote_src='—— yiduobo 题解',
        idea=['第一趟：每个格子同时累加到它的行和 `s_row[i]`、列和 `s_col[j]`',
              '第二趟：`mat[i][j] == 1` 且 `s_row[i] == 1` 且 `s_col[j] == 1` → 计数',
              '三个条件缺一不可：本例里 `(0,0)` 败在列，`(2,3)` 败在行'],
        summary=['时间 `O(mn)`，空间 `O(m + n)`',
                 '易错：只看行和、列和不够，还要求==当前格子本身是 1==',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神只给行和为 1 的行算一次列和，`O(1)` 额外空间'],
    ),
)
