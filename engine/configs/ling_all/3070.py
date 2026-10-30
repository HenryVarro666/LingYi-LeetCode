GRID = [[3, 2, 5], [1, 6, 2], [4, 3, 2]]
K = 15
_P = [[sum(GRID[a][b] for a in range(i + 1) for b in range(j + 1)) for j in range(3)] for i in range(3)]
COUNTED = []   # 按算法顺序，被计入答案的 (i, j)
for _i in range(3):
    for _j in range(3):
        if _P[_i][_j] > K:
            break
        COUNTED.append((_i, _j))
EXPECT = len(COUNTED)


def _ri(S):
    g, row = S.get('grid'), S.get('row')
    return g.index(row) if g is not None and row in g else None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g = S.get('grid')
    if g is None:
        return
    m, n = len(g), len(g[0])
    line = S.get('_line', 0)
    ci = _ri(S) if line <= 12 else None
    cj = S.get('j')
    cs = S.get('col_sum')
    over = S.get('s', 0) > S.get('k', K)
    ended7 = line == 7 and 'j' in B and S.get('j') == B.get('j') and S.get('x') == B.get('x') and S.get('row') == B.get('row')
    on_cell = ci is not None and cj is not None and 7 <= line <= 12 and not ended7
    cv.text((x0 + 18, y0 + 4), 'grid（绿 = 已计入答案；青 / 红框 = 当前左上角到 (i,j) 的子矩阵）', 22, T['muted'], bold=True)
    cell = min(132, (x1 - x0 - 150) / n)
    ch = min(98, cell * 0.8)
    sx = x0 + 100 + ((x1 - x0 - 150) - cell * n) / 2
    sy = y0 + 70
    done = set(COUNTED[:S.get('ans', 0)])
    for j in range(n):
        cv.text((sx + j * cell + cell / 2, sy - 6), f'j={j}', 18, T['dim'], anchor='mb', mono=True)
    for i in range(m):
        hot = ci == i
        cv.text((sx - 14, sy + i * ch + ch / 2), f'i={i}', 20, T['yellow'] if hot else T['dim'], anchor='rm', mono=True, bold=hot)
        for j in range(n):
            X, Y = sx + j * cell, sy + i * ch
            ok = (i, j) in done
            cv.rect((X + 3, Y + 3, X + cell - 3, Y + ch - 3), fill=T['green'] if ok else T['panel2'], r=8,
                    outline=T['yellow'] if (on_cell and (i, j) == (ci, cj)) else T['border'],
                    width=4 if (on_cell and (i, j) == (ci, cj)) else 1)
            cv.text((X + cell / 2, Y + ch / 2), g[i][j], 30, T['bg'] if ok else T['text'], anchor='mm', bold=True)
    if on_cell and 9 <= line <= 11:
        c = T['red'] if over else T['cyan']
        a, b = sx - 2, sy - 2
        cv.rect((a, b, sx + (cj + 1) * cell + 2, sy + (ci + 1) * ch + 2), fill=c, alpha=34, r=10)
        cv.rect((a, b, sx + (cj + 1) * cell + 2, sy + (ci + 1) * ch + 2), outline=c, width=4, r=10)
    # col_sum：每一列从第 0 行加到当前行
    yb = sy + m * ch + 62
    cv.text((x0 + 18, yb - 40), 'col_sum（每一列从第 0 行加到当前行的和）', 22, T['muted'], bold=True)
    if cs is not None:
        bc = B.get('col_sum') or []
        for j in range(n):
            X = sx + j * cell
            used = on_cell and 9 <= line <= 11 and j <= cj
            chg = line == 8 and j < len(bc) and bc[j] != cs[j]
            fill = (T['red'] if over and j == cj else T['cyan']) if used else T['panel2']
            cv.rect((X + 3, yb, X + cell - 3, yb + 76), fill=fill, r=8,
                    outline=T['yellow'] if chg else T['border'], width=4 if chg else 1)
            cv.text((X + cell / 2, yb + 38), cs[j], 30, T['bg'] if used else T['text'], anchor='mm', bold=True)
    if cs is not None and on_cell and line >= 9:
        parts = ' + '.join(str(v) for v in cs[:cj + 1])
        sv = S['s']
        tail = f'= {sv}'
        cmp_ = f"{'>' if over else '≤'} k = {S['k']}"
        cc = T['red'] if over else T['green']
        cv.text((x0 + 22, yb + 104), f's = {parts} {tail}', 28, T['text'], bold=True, mono=True)
        cv.text((x0 + 22, yb + 148), f"{sv} {cmp_}" + ('　→ 不满足，这一行右边都不用看了' if over else '　→ 满足，计入答案'), 26, cc, bold=True)


CONFIG = dict(
    num=3070, title='元素和小于等于 k 的子矩阵的数目', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='逐行累加列和 · 超过 k 提前 break',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1499'],
    code='''
class Solution:
    def countSubmatrices(self, grid: List[List[int]], k: int) -> int:
        col_sum = [0] * len(grid[0])
        ans = 0
        for row in grid:
            s = 0
            for j, x in enumerate(row):
                col_sum[j] += x
                s += col_sum[j]
                if s > k:
                    break
                ans += 1
        return ans
''',
    call=f'Solution().countSubmatrices({GRID}, {K})',
    expect=EXPECT,
    views=[
        dict(type='custom', draw=_draw, h=600),
    ],
    watch=[('s', 's', 'cyan'), ('k', 'k', 'red'), ('ans', 'ans', 'green'), ('j', 'j', 'pink')],
    captions={
        'col_sum = [0]': '`col_sum[j]`：第 `j` 列从第 0 行加到当前行的和，一开始全是 0',
        'ans = 0': '`ans` 统计「包含左上角、和 ≤ k」的子矩阵个数',
        'for row in grid': lambda S, B, r: ('所有行都处理完了' if ('row' in B and S.row == B.row)
                                            else '第 `{}` 行：右下角落在这一行的子矩阵，从左往右一个个试'.format(_ri(S))),
        's = 0': '`s` 清零：`s` 只统计==当前行==里「左上角到 `(i,j)`」的子矩阵和',
        'for j, x in enumerate(row)': lambda S, B, r: ('这一行走到头了，没有 break' if ('j' in B and S.j == B.j and S.x == B.x and S.row == B.row)
                                                       else '右下角取 `({}, {})`，新加入的数是 `x = {}`'.format(_ri(S), S.j, S.x)),
        'col_sum[j] += x': '`col_sum[{j}]` += {x} → {col_sum[j]}：现在它是第 {j} 列从第 0 行到当前行的和',
        's += col_sum[j]': lambda S, B, r: ('`s` += `col_sum[{}]` → =={}==：前 {} 列的列和之和，正好是左上角到 `({}, {})` 的子矩阵和'
                                            ).format(S.j, S.s, S.j + 1, _ri(S), S.j),
        'if s > k': lambda S, B, r: ('`s = {} ≤ k = {}`：这个子矩阵合格'.format(S.s, S.k) if S.s <= S.k
                                     else '`s = {} > k = {}`：不合格 → 下一步 break'.format(S.s, S.k)),
        'break': '元素都非负：再往右加列，`s` 只增不减 → 这一行右边的子矩阵全都不合格，直接跳出',
        'ans += 1': lambda S, B, r: '`ans` → =={}==：左上角到 `({}, {})` 这个子矩阵算一个'.format(S.ans, _ri(S), S.j),
        'return ans': '返回 `{ans}`',
    },
    cards=dict(
        one_liner='把二维前缀和拆成「按行累加列和」，s 超过 k 就提前收工',
        complexity='时间 `O(mn)`，空间 `O(n)`',
        problem=['给非负整数矩阵 `grid`（`m×n`）和整数 `k`',
                 '数有多少个「包含左上角 `grid[0][0]`」且元素和 `≤ k` 的子矩阵',
                 '示例：`[[7,6,3],[6,6,1]]`，`k=18` → `4`',
                 f'本视频：3×3 矩阵，`k={K}` → `{EXPECT}`'],
        quote='遍历当前行时，一边更新 colSum[j]，一边累加 colSum[j] 到变量 s 中。如果 s≤k 则把答案加一，否则可以跳出循环（因为矩阵元素都非负）。',
        quote_src='—— 灵茶山艾府题解 · 方法二',
        idea=['左上角固定，子矩阵由右下角 `(i,j)` 决定：数一数有多少个 `s(i,j) ≤ k`',
              '`col_sum[j]` 存第 j 列到当前行的和；前 `j+1` 列的 `col_sum` 相加 = ==子矩阵和==',
              '元素非负，同一行里 `s` 随 `j` 不减 → 一旦超过 `k` 就可以 `break`'],
        summary=['时间 `O(mn)`，空间 `O(n)`',
                 '易错：`s` 每行清零；`col_sum` 不清零，要跨行累加',
                 '`break` 只跳出当前行，下一行仍要从 `j=0` 试起',
                 '依赖「元素非负」；有负数就不能提前 break',
                 '方法一：直接建 `(m+1)×(n+1)` 二维前缀和，空间 `O(mn)`'],
    ),
)
