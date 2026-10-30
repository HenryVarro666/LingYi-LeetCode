GRID = [[1, 1, 0], [1, 1, 1], [0, 1, 1]]
_CODE = '''
class Solution(object):
    def largest1BorderedSquare(self, grid):

        m = len(grid)
        n = len(grid[0])

        left = [[0] * n for _ in range(m)]
        right = [[0] * n for _ in range(m)]
        up = [[0] * n for _ in range(m)]
        down = [[0] * n for _ in range(m)]

        for i in range(m):
            left[i][0] = grid[i][0]
            for j in range(1, n):
                if grid[i][j] == 1:
                    left[i][j] = left[i][j - 1] + 1
                else:
                    left[i][j] = 0
            
            right[i][n - 1] = grid[i][n - 1]
            for j in range(n - 2, -1, -1):
                if grid[i][j] == 1:
                    right[i][j] = right[i][j + 1] + 1
                else:
                    right[i][j] = 0
        
        for j in range(n):
            up[0][j] = grid[0][j]
            for i in range(1, m):
                if grid[i][j] == 1:
                    up[i][j] = up[i - 1][j] + 1
                else:
                    up[i][j] = 0
            
            down[m - 1][j] = grid[m - 1][j]
            for i in range(m - 2, -1, -1):
                if grid[i][j] == 1:
                    down[i][j] = down[i + 1][j] + 1
                else:
                    down[i][j] = 0

        for res in range(min(m, n), 0, -1):
            for i in range(m - res + 1):
                for j in range(n - res + 1):
                    if right[i][j] >= res and down[i][j] >= res and left[i + res - 1][j + res - 1] >= res and up[i + res - 1][j + res - 1] >= res:
                        return res * res
        
        return 0
'''
_LINES = _CODE.strip('\n').splitlines()
L_SEARCH = next(k for k, s in enumerate(_LINES, 1) if 'if right[i][j] >= res' in s)
L_RET = next(k for k, s in enumerate(_LINES, 1) if 'return res * res' in s)
L_FOR_RES = next(k for k, s in enumerate(_LINES, 1) if 'for res in range' in s)


def _cur_table(S):
    """当前这一行正在写哪张表（left/right/up/down），否则 None"""
    ln = S.get('_line')
    if not ln or ln >= L_FOR_RES:
        return None
    t = _LINES[ln - 1].strip()
    for name in ('left', 'right', 'up', 'down'):
        if t.startswith(name + '['):
            return name
    return None


def _mini(cv, T, x, y, cell, mat, title, tcol, hot=None, cols=None, fs=22):
    cv.text((x, y - 6), title, 22, tcol, anchor='lb', bold=True)
    for i, row in enumerate(mat):
        for j, v in enumerate(row):
            X, Y = x + j * cell, y + i * cell
            fill, tc = T['panel2'], T['text']
            if cols and (i, j) in cols:
                fill, tc = T[cols[(i, j)]], T['bg']
            cv.rect((X + 2, Y + 2, X + cell - 2, Y + cell - 2), fill=fill, r=6,
                    outline=T['yellow'] if hot == (i, j) else T['border'], width=4 if hot == (i, j) else 1)
            cv.text((X + cell / 2, Y + cell / 2), v, fs, tc, anchor='mm', bold=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g = S['grid']
    m, n = len(g), len(g[0])
    ln = S.get('_line', 0)
    cur = _cur_table(S)
    searching = 'res' in S and 'i' in S and 'j' in S and L_SEARCH <= ln <= L_RET
    # ---- 左上：grid
    cell = 84
    gx = x0 + 40
    gy = y0 + 60
    cols = {}
    hot = None
    if searching:
        r, a, b = S['res'], S['i'], S['j']
        ok = ln == L_RET
        for p in range(r):
            for (u, v) in ((a, b + p), (a + r - 1, b + p), (a + p, b), (a + p, b + r - 1)):
                cols[(u, v)] = 'green' if ok else ('pink' if g[u][v] == 0 else 'blue')
    elif cur and 'i' in S and 'j' in S:
        hot = (S['i'], S['j'])
    _mini(cv, T, gx, gy, cell, g, 'grid（蓝 = 正在检查的边框，粉 = 边上有 0，绿 = 找到）', T['muted'], hot=hot, cols=cols, fs=30)
    # ---- 右上：说明
    tx = gx + n * cell + 50
    if searching:
        r, a, b = S['res'], S['i'], S['j']
        ci, cj = a + r - 1, b + r - 1
        rows = [(f'右下角 `({ci},{cj})`' if False else f'右下角 ({ci},{cj})', T['muted']),
                (f"right[{a}][{b}] = {S['right'][a][b]}", T['blue']),
                (f"down[{a}][{b}] = {S['down'][a][b]}", T['cyan']),
                (f"left[{ci}][{cj}] = {S['left'][ci][cj]}", T['pink']),
                (f"up[{ci}][{cj}] = {S['up'][ci][cj]}", T['orange'])]
        cv.text((tx, gy), f'边长 res = {r}，左上角 ({a},{b})', 26, T['text'], bold=True)
        cv.text((tx, gy + 40), '四个方向的连续 1 都要 ≥ res：', 22, T['muted'])
        for k, (s, c) in enumerate(rows[1:]):
            okk = int(s.split('= ')[1]) >= r
            cv.text((tx, gy + 86 + k * 40), s + ('  ✓' if False else ('  达标' if okk else '  不够')), 26, c if okk else T['red'], bold=True, mono=True)
    else:
        cv.text((tx, gy), '先预处理：每个格子向四个方向', 24, T['muted'])
        cv.text((tx, gy + 36), '延伸出去连续 1 的个数', 24, T['muted'])
        if cur:
            cv.text((tx, gy + 96), f'正在填 {cur} 表', 28, T['yellow'], bold=True)
    # ---- 下：四张表
    cs = 58
    gap = (x1 - x0 - 40 - 4 * 3 * cs) / 3
    ty = y0 + 60 + m * cell + 90
    names = [('left', T['pink']), ('right', T['blue']), ('up', T['orange']), ('down', T['cyan'])]
    for k, (nm, c) in enumerate(names):
        tab = S[nm]
        cc = {}
        hh = None
        if searching:
            r, a, b = S['res'], S['i'], S['j']
            if nm in ('right', 'down'):
                hh = (a, b)
            else:
                hh = (a + r - 1, b + r - 1)
        elif nm == cur and 'i' in S and 'j' in S:
            hh = (S['i'], S['j'])
        _mini(cv, T, x0 + 20 + k * (3 * cs + gap), ty, cs, tab, nm + (' →' if nm == 'right' else ' ←' if nm == 'left' else ' ↑' if nm == 'up' else ' ↓'), c, hot=hh, fs=24)


CONFIG = dict(
    num=1139, title='最大的以 1 为边界的正方形', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='四方向连续 1 预处理 · 枚举边长',
    tags=[],
    code=_CODE,
    call=f'Solution().largest1BorderedSquare({GRID})',
    expect=4,
    skip=['for i in range(m):', 'for j in range(n):', 'for j in range(1, n)', 'for j in range(n - 2', 'for i in range(1, m)',
          'for i in range(m - 2', 'for i in range(m - res + 1)', 'for j in range(n - res + 1)', 'if grid[i][j] == 1:', 'm = len', 'n = len', 'left = [[', 'right = [[', 'up = [[', 'down = [['],
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=[('res', 'res', 'blue'), ('i', 'i', 'pink'), ('j', 'j', 'pink')],
    captions={
        'left[i][0] = grid[i][0]': '第 `{i}` 行最左边的格子，向左只有它自己：`left[{i}][0] = {left[i][0]}`',
        'left[i][j] = left[i][j - 1] + 1': '`grid[{i}][{j}]` 是 1 → 向左连续 1 的个数 = 左邻居的 + 1 = =={left[i][j]}==',
        'left[i][j] = 0': '`grid[{i}][{j}]` 是 0 → 连续 1 断了，`left[{i}][{j}] = 0`',
        'right[i][n - 1] = grid[i][n - 1]': '第 `{i}` 行最右边的格子：`right[{i}][{n-1}] = {right[i][n-1]}`，下面从右往左填',
        'right[i][j] = right[i][j + 1] + 1': '`grid[{i}][{j}]` 是 1 → `right[{i}][{j}]` = 右邻居的 + 1 = =={right[i][j]}==',
        'right[i][j] = 0': '`grid[{i}][{j}]` 是 0 → `right[{i}][{j}] = 0`',
        'up[0][j] = grid[0][j]': '第 `{j}` 列最上面的格子：`up[0][{j}] = {up[0][j]}`',
        'up[i][j] = up[i - 1][j] + 1': '`grid[{i}][{j}]` 是 1 → 向上连续 1 的个数 = 上邻居的 + 1 = =={up[i][j]}==',
        'up[i][j] = 0': '`grid[{i}][{j}]` 是 0 → `up[{i}][{j}] = 0`',
        'down[m - 1][j] = grid[m - 1][j]': '第 `{j}` 列最下面的格子：`down[{m-1}][{j}] = {down[m-1][j]}`，下面从下往上填',
        'down[i][j] = down[i + 1][j] + 1': '`grid[{i}][{j}]` 是 1 → `down[{i}][{j}]` = 下邻居的 + 1 = =={down[i][j]}==',
        'down[i][j] = 0': '`grid[{i}][{j}]` 是 0 → `down[{i}][{j}] = 0`',
        'for res in range': lambda S, B, r: ('预处理完成。直接枚举边长：从大到小，先试最大的 `res = %d`' % S.res if 'i' not in B or 'res' not in B
                                              else f'边长 `{B.res}` 找不到 → 缩小到 `res = {S.res}`'),
        'if right[i][j] >= res': lambda S, B, r: (
            f'左上角 `({S.i},{S.j})` 边长 `{S.res}`：向右 `{S.right[S.i][S.j]}`、向下 `{S.down[S.i][S.j]}`；右下角向左 `{S.left[S.i + S.res - 1][S.j + S.res - 1]}`、向上 `{S.up[S.i + S.res - 1][S.j + S.res - 1]}`'
            + (' → 四个都 ≥ res，==边框全是 1==' if min(S.right[S.i][S.j], S.down[S.i][S.j], S.left[S.i + S.res - 1][S.j + S.res - 1], S.up[S.i + S.res - 1][S.j + S.res - 1]) >= S.res
               else ' → 有一个不够，换下一个位置')),
        'return res * res': '边长 `{res}` 的正方形边框全是 1 → 面积 `{res} × {res}` = =={ret}==',
        'return 0': '没有任何边框全是 1 的正方形 → `0`',
    },
    cards=dict(
        one_liner='预处理四个方向的连续 1，再枚举边长和左上角，O(1) 验证边框',
        complexity='时间 `O(n^3)`，空间 `O(n^2)`（n 取行列较大者）',
        problem=['`0/1` 网格，找==边框全是 1== 的最大正方形，返回面积',
                 '里面可以有 0，只看四条边',
                 '示例：`[[1,1,1],[1,0,1],[1,1,1]]` → `9`',
                 '本视频：`[[1,1,0],[1,1,1],[0,1,1]]` → `4`'],
        quote='可以在O(n^2)的时间复杂度预处理出从每个点开始向上、下、左、右这四个方向上延伸的连续1的长度。',
        quote_src='—— yiduobo 题解原文',
        idea=['`left/right/up/down[i][j]`：从 `(i,j)` 往该方向连续 1 的个数，遇到 0 就清零',
              '正方形的左上角往右、往下要 ≥ 边长，右下角往左、往上也要 ≥ 边长',
              '原文说理论上可用单调栈优化到 `O(n^2)`，但 n ≤ 100，直接枚举边长更省事'],
        summary=['时间 `O(n^3)`：边长 × 左上角位置，每次检查 `O(1)`；预处理 `O(n^2)`',
                 '易错：右下角是 `(i+res-1, j+res-1)`，不是 `(i+res, j+res)`',
                 '易错：检查左上角用 `right/down`，右下角用 `left/up`，方向别写反',
                 '代码原样保留（原文已是 Python 3 可运行写法），只删去了类型说明文档字符串',
                 '对比灵神：灵神用行列前缀和统计边上 1 的个数；这里用连续 1 的长度'],
    ),
)
