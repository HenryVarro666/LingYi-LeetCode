TRI = [[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]


def _dp():
    n = len(TRI)
    f = [row[:] for row in TRI]
    for i in range(n - 2, -1, -1):
        for j in range(i + 1):
            f[i][j] = min(f[i + 1][j], f[i + 1][j + 1]) + TRI[i][j]
    return f


DP = _dp()


def _progress(S):
    """(i, j) of the last cell already written into f; None before the loop"""
    i, j = S.get('i'), S.get('j')
    if i is None:
        return None
    line = S.get('_line')
    if line == 7:
        return i, j
    if line == 6:  # 刚取出 j，还没写
        return (i, j - 1) if j is not None else (i + 1, 10)
    if line == 5:
        return i + 1, 10
    return 0, 10


def _known(S, r, c):
    p = _progress(S)
    n = len(TRI)
    if r == n - 1:
        return 'f' in S
    if p is None:
        return False
    pi, pj = p
    return r > pi or (r == pi and c <= pj)


def _cell(cv, T, X, Y, cell, v, fill, outline, tcol, width=1):
    cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), fill=fill, r=8, outline=outline, width=width)
    cv.text((X + cell / 2, Y + cell / 2), v, int(cell * 0.4), tcol, anchor='mm', bold=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(TRI)
    cell = 78
    i, j = S.get('i'), S.get('j')
    active = S.get('_line') in (6, 7) and i is not None and j is not None
    gx = [x0 + 40, x0 + (x1 - x0) / 2 + 30]
    cv.text((gx[0], y0 + 4), 'triangle（左对齐）', 24, T['muted'], bold=True)
    cv.text((gx[1], y0 + 4), 'dfs(i,j)：从 (i,j) 走到最后一排的最小和', 24, T['muted'], bold=True)
    top = y0 + 50
    for r in range(n):
        for c in range(r + 1):
            X, Y = gx[0] + c * cell, top + r * cell
            fill, out, tc, w = T['panel2'], T['border'], T['text'], 1
            if active and (r, c) == (i, j):
                fill, tc = T['yellow'], T['bg']
            cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), fill=fill, r=8, outline=out, width=w)
            cv.text((X + cell / 2, Y + cell / 2), TRI[r][c], 30, tc, anchor='mm', bold=True)
            # dp triangle
            X2 = gx[1] + c * cell
            known = _known(S, r, c)
            fill, out, tc, w = T['panel2'], T['border'], T['text'], 1
            if active and (r, c) == (i + 1, j):
                fill, tc = T['pink'], T['bg']
            elif active and (r, c) == (i + 1, j + 1):
                fill, tc = T['blue'], T['bg']
            elif active and (r, c) == (i, j):
                fill, tc, out, w = T['green'], T['bg'], T['yellow'], 3
            cv.rect((X2 + 3, Y + 3, X2 + cell - 3, Y + cell - 3), fill=fill, r=8, outline=out, width=w)
            cv.text((X2 + cell / 2, Y + cell / 2), DP[r][c] if known else '?', 30, tc if known else T['dim'], anchor='mm', bold=True)


def _formula(S):
    if S.get('_line') == 7:
        i, j, f, x = S['i'], S['j'], S['f'], S['x']
        return f'`f[{j}] = min(f[{j}], f[{j + 1}]) + {x}` = =={f[j]}==（下方 / 右下方选小的）'
    return '`f[j] = min(f[j], f[j + 1]) + x`：只依赖正下方和右下方'


def _cap_f(S, B, ret):
    j, x = S.j, S.x
    a, b = B.f[j], B.f[j + 1]
    side = '正下方' if a <= b else '右下方'
    return f'`({S.i},{j}) = {x}`：正下方 `{a}`、右下方 `{b}`，走{side}更小 → `f[{j}] = {min(a, b)} + {x}` = =={S.f[j]}=='


def _cap_for_i(S, B, ret):
    if S.get('i') is not None and (B.get('i') != S.get('i') or 'i' not in B):
        return f'自底向上：处理第 `i = {S.i}` 排（要先算出第 `{S.i + 1}` 排）'
    return '第 0 排也算完了 → 结束'


CONFIG = dict(
    num=120, title='三角形最小路径和', difficulty='Medium', category='多维动态规划',
    author='灵茶山艾府', technique='记忆化搜索 → 递推 → 空间优化',
    tags=['面试经典150'],
    code='''
class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        n = len(triangle)
        f = triangle[-1][:]
        for i in range(n - 2, -1, -1):
            for j, x in enumerate(triangle[i]):
                f[j] = min(f[j], f[j + 1]) + x
        return f[0]
''',
    call=f'Solution().minimumTotal({TRI})',
    expect=11,
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='custom', draw=_draw, h=380),
        dict(type='array', var='f', label='f（一维滚动数组；绿 = 刚写入，蓝 = 右下方，暗 = 已用完）', cell=84, pointers={'j': 'yellow'},
             color=lambda S, k, v: ('green' if k == S['j'] else 'blue' if k == S['j'] + 1 else None) if S.get('_line') == 7 else None,
             dim=lambda S, k, v: S.get('i') is not None and S.get('_line') in (6, 7) and k > S['i'] + 1),
    ],
    watch=['n', ('i', 'i', 'yellow'), ('j', 'j', 'yellow'), 'x'],
    captions={
        'n = len(triangle)': '一共 `n = {n}` 排',
        'f = triangle[-1][:]': '边界：最后一排走不动了，`dfs(n-1, j) = triangle[n-1][j]` → `f` 初始化为最后一排的副本',
        'for i in range': _cap_for_i,
        'for j, x in enumerate': lambda S, B, r: (f'第 {S.i} 排的第 `j = {S.j}` 个数 `x = {S.x}`'
                                                    if B.get('j') != S.get('j') or B.get('i') != S.get('i') else f'第 {S.i} 排处理完'),
        'f[j] = min': _cap_f,
        'return f[0]': '`f[0]` 就是 `dfs(0, 0)`：从顶点出发的最小路径和 =={ret}==（2 + 3 + 5 + 1）',
    },
    cards=dict(
        one_liner='dfs(i,j) = min(下方, 右下方) + 自己；自底向上递推，一维数组滚动',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['给一个三角形 `triangle`，求==自顶向下==的最小路径和',
                 '在第 `i` 排下标 `j` 时，下一步只能走到下一排的 `j` 或 `j + 1`',
                 '示例：`[[2],[3,4],[6,5,7],[4,1,8,3]]` → `11`（2 + 3 + 5 + 1）'],
        quote='定义状态为 ==dfs(i,j)==，表示从 (i,j) 出发，移动到 triangle 最后一排，路径上的元素之和的最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i,j) = min(dfs(i+1,j), dfs(i+1,j+1)) + triangle[i][j]`',
              '边界 `dfs(n-1,j) = triangle[n-1][j]`，答案 `dfs(0,0)`；重复调用 → `@cache`',
              '去掉「递」只留「归」：要先算第 `i+1` 排，所以 ==i 从大到小==枚举',
              '`f[i][j]` 只依赖下一排 → 去掉第一维，`f[j] = min(f[j], f[j+1]) + x`'],
        result='`f[0] = 11`：路径 `2 → 3 → 5 → 1`',
        summary=['时间 `O(n^2)`，空间 `O(n)`（写法二直接在 triangle 上改，`O(1)`）',
                 '易错：`f` 要复制最后一排 `[:]`，否则会改坏输入（虽然本题无影响）',
                 '易错：自顶向下要处理左右边界；自底向上 `j + 1` 永远合法，更简洁',
                 '`i` 必须倒序；`j` 正序即可：`f[j]` 用到的 `f[j+1]` 还是下一排的值'],
    ),
)
