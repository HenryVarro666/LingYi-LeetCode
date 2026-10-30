MAT = [[0, 0, 0, 1], [1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 1, 0]]


def _special():
    m, n = len(MAT), len(MAT[0])
    return {(i, j) for i in range(m) for j in range(n)
            if MAT[i][j] == 1 and sum(MAT[i]) == 1 and sum(MAT[r][j] for r in range(m)) == 1}


def _ri(S):
    row, mat = S.get('row'), S.get('mat')
    if row is None or mat is None:
        return None
    for i, r in enumerate(mat):
        if r is row:
            return i
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'mat（黄 = 当前行，青 = 要检查的第 j 列，绿 = 找到的特殊位置）', 22, T['muted'], bold=True)
    m, n = len(MAT), len(MAT[0])
    cell = 96
    gx = x0 + 150
    gy = y0 + 70
    ri = _ri(S)
    line = S.get('_line', 0)
    j = S.get('j') if line >= 7 else None
    if ri is not None:
        cv.rect((gx - 6, gy + ri * cell - 2, gx + n * cell + 6, gy + (ri + 1) * cell + 2), fill=T['yellow'], alpha=50, r=10)
        cv.rect((gx - 6, gy + ri * cell - 2, gx + n * cell + 6, gy + (ri + 1) * cell + 2), outline=T['yellow'], width=3, r=10)
    if j is not None and ri is not None and line in (7, 9, 10):
        cv.rect((gx + j * cell - 2, gy - 6, gx + (j + 1) * cell + 2, gy + m * cell + 6), fill=T['cyan'], alpha=50, r=10)
        cv.rect((gx + j * cell - 2, gy - 6, gx + (j + 1) * cell + 2, gy + m * cell + 6), outline=T['cyan'], width=3, r=10)
    sp = _special()
    done = set()
    for (a, b) in sp:
        if ri is None:
            if line == 11 or 'ans' in S and S['ans'] == len(sp):
                done.add((a, b))
        elif a < ri or (a == ri and line == 10):
            done.add((a, b))
    for i in range(m):
        for jj in range(n):
            X, Y = gx + jj * cell, gy + i * cell
            v = MAT[i][jj]
            fill = T['green'] if (i, jj) in done else (T['panel2'] if v == 0 else (70, 78, 92))
            cv.rect((X + 5, Y + 5, X + cell - 5, Y + cell - 5), fill=fill, r=8, outline=T['border'], width=1)
            cv.text((X + cell / 2, Y + cell / 2), v, 34, T['bg'] if (i, jj) in done else (T['text'] if v else T['dim']),
                    anchor='mm', bold=True, mono=True)
        cv.text((gx - 20, gy + i * cell + cell / 2), f'行 {i}', 20, T['dim'], anchor='rm')
    for jj in range(n):
        cv.text((gx + jj * cell + cell / 2, gy - 12), f'列 {jj}', 18, T['dim'], anchor='mb')
    # 行和 / 列和
    sx = gx + n * cell + 40
    cv.text((sx, gy - 12), 'sum(row)', 18, T['yellow'], anchor='lb', bold=True, mono=True)
    if ri is not None:
        s = sum(MAT[ri])
        cv.text((sx + 10, gy + ri * cell + cell / 2), f'= {s}', 30, T['green'] if s == 1 else T['red'], anchor='lm', bold=True, mono=True)
    if j is not None and ri is not None and line in (9, 10):
        cs = sum(MAT[r][j] for r in range(m))
        cv.text((gx + j * cell + cell / 2, gy + m * cell + 14), f'列和 = {cs}', 24, T['green'] if cs == 1 else T['red'],
                anchor='mt', bold=True)


def _cap_sum(S, B, ret):
    s = sum(S.row)
    if s != 1:
        return f'第 `{_ri(S)}` 行 `{S.row}` 的和是 `{s}` ≠ 1：这一行==不止一个 1==（或没有 1），不可能有特殊位置'
    return f'第 `{_ri(S)}` 行 `{S.row}` 的和恰好是 `1`：只有一个 1，再看它所在的列'


def _cap_col(S, B, ret):
    cs = sum(r[S.j] for r in S.mat)
    if cs == 1:
        return f'第 `{S.j}` 列的和 = `1`：这一列也只有这个 1 → ==特殊位置== `({_ri(S)}, {S.j})`'
    return f'第 `{S.j}` 列的和 = `{cs}` ≠ 1：这一列还有别的 1，不是特殊位置'


CONFIG = dict(
    num=1582, title='二进制矩阵中的特殊位置', difficulty='Easy', category='矩阵',
    author='灵茶山艾府', technique='逐行检查：行和为 1 再查列和',
    tags=['字节30天'],
    code='''
class Solution:
    def numSpecial(self, mat: List[List[int]]) -> int:
        ans = 0
        for row in mat:
            if sum(row) != 1:
                continue
            j = row.index(1)
            # 计算 j 列的元素和，必须恰好是 1
            if sum(row[j] for row in mat) == 1:
                ans += 1
        return ans
''',
    call=f'Solution().numSpecial({MAT})',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=[('row', 'row', 'yellow'), ('j', 'j', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 统计特殊位置的个数',
        4: lambda S, B, ret: (f'看第 `{_ri(S)}` 行：`{S.row}`' if S.get('row') is not B.get('row') and _ri(S) is not None
                                             and (B.get('row') is None or _ri(B) != _ri(S)) else '所有行都检查完了'),
        'if sum(row) != 1': _cap_sum,
        'continue': '跳过这一行',
        'j = row.index(1)': '唯一的 1 在第 `j = {j}` 列',
        'if sum(row[j] for row in mat) == 1': _cap_col,
        'ans += 1': '找到一个特殊位置：`ans` → {ans}',
        'return ans': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='一行只有一个 1，并且它所在的列也只有一个 1',
        complexity='时间 `O(m(n + m))`，空间 `O(1)`',
        problem=['给你 `m × n` 的 01 矩阵 `mat`，统计==特殊位置==的个数',
                 '特殊位置 `(i, j)`：`mat[i][j] == 1`，且第 i 行、第 j 列==其余元素都是 0==',
                 '示例：`[[1,0,0],[0,0,1],[1,0,0]]` → `1`；本视频的 4×4 矩阵 → `2`'],
        quote='对于矩阵的每一行，如果这一行只有一个 1，那么遍历 1 所在的那一列，如果也只有一个 1，则把答案加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['01 矩阵里“只有一个 1” ⇔ ==和恰好为 1==',
              '先看行和：不为 1 直接跳过（这一行不可能有特殊位置）',
              '行和为 1 时用 `row.index(1)` 找到列号，再算这一列的和'],
        summary=['时间 `O(m(n + m))`：每行求和 `O(n)`，必要时再求一列 `O(m)`；空间 `O(1)`',
                 '易错：行和为 1 才有资格，此时这一行==恰好一个==候选位置，不会重复计数',
                 '题解还给了“中途退出循环”的优化写法：发现第二个 1 就 break'],
    ),
)
