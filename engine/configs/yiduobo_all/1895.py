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
    cell = 70
    grid = S['grid']
    lx, ly, rx, ry = S.get('lx'), S.get('ly'), S.get('rx'), S.get('ry')
    idx = S.get('index')
    live = rx is not None and ry is not None and line >= 25

    def tint(a, b):
        if not live:
            return None
        if 29 <= line <= 44:           # 逐行核对：当前行高亮，已累加的对角线格子着色
            if a == idx and ly <= b <= ry and 33 <= line:
                return 'pink'
            if lx <= a <= (idx if idx is not None and idx <= rx else rx) and a >= lx:
                if b == ly + a - lx and line >= 37:
                    return 'green'
                if b == ry - a + lx and line >= 37:
                    return 'cyan'
        if line >= 45 and a >= lx and a <= rx and b == idx:
            return 'pink'
        if lx <= a <= rx and ly <= b <= ry:
            return 'blue'
        return None

    px, py = x0 + 24, y0 + 6
    w1, h1 = _mat(cv, T, px, py, grid, cell, 'grid（蓝框 = 当前枚举的正方形）', tint=tint)
    hp, vp = S.get('h_prefix'), S.get('v_prefix')
    if hp is not None and vp is not None:
        def chg(name):
            def f(a, b):
                Bv = B.get(name)
                try:
                    return Bv is not None and Bv[a][b] != S[name][a][b]
                except Exception:
                    return False
            return f
        y2 = py + h1 + 30
        w2, h2 = _mat(cv, T, px, y2, hp, cell, 'h_prefix（每行）', changed=chg('h_prefix'))
        _mat(cv, T, px + w2 + 90, y2, vp, cell, 'v_prefix（每列）', changed=chg('v_prefix'))


def _info(S):
    if 'res' not in S or 'lx' not in S:
        return '先给每行、每列建前缀和，再枚举左上角 `(lx, ly)` 和边长 `l`'
    line = S['_line']
    if line >= 57:
        return '用前缀和求区间和：`prefix[pos][r] − prefix[pos][l−1]`'
    if 'rx' not in S or line < 25:
        return f'枚举左上角 `({S["lx"]}, {S["ly"]})`，目前最大边长 `res = {S["res"]}`'
    t = f'左上角 `({S["lx"]}, {S["ly"]})`，边长 `l = {S["l"]}`，右下角 `({S["rx"]}, {S["ry"]})`'
    if 's' in S:
        t += f'，第一行和 `s = {S["s"]}`'
    return t


CONFIG = dict(
    num=1895, title='最大的幻方', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='枚举左上角和边长 · 行列前缀和',
    tags=['前缀和', '进阶', '难度分 1781'],
    code='''
class Solution(object):
    def largestMagicSquare(self, grid):

        m = len(grid)
        n = len(grid[0])

        h_prefix = [[] for _ in range(m)]
        v_prefix = [[] for _ in range(n)]

        for i in range(m):
            for j in range(n):
                h_prefix[i].append(grid[i][j])
                if j > 0:
                    h_prefix[i][-1] += h_prefix[i][-2]
                
                v_prefix[j].append(grid[i][j])
                if i > 0:
                    v_prefix[j][-1] += v_prefix[j][-2]
        
        res = 1
        for lx in range(m):
            for ly in range(n):
                for l in range(2, min(m - lx, n - ly) + 1):
                    rx = lx + l - 1
                    ry = ly + l - 1
                    l_cross = grid[lx][ly]
                    r_cross = grid[lx][ry]

                    s = self.get_s(h_prefix, lx, ly, ry)

                    flag = True
                    for index in range(lx + 1, rx + 1):
                        if s != self.get_s(h_prefix, index, ly, ry):
                            flag = False
                            break
                        
                        l_cross += grid[index][ly + index - lx]
                        r_cross += grid[index][ry - index + lx]

                    if not flag:
                        continue

                    if l_cross != s or r_cross != s:
                        continue
                    
                    flag = True
                    for index in range(ly, ry + 1):
                        if s != self.get_s(v_prefix, index, lx, rx):
                            flag = False
                            break
                    
                    if flag:
                        res = max(res, l)
        
        return res

    def get_s(self, prefix, pos, l, r):
        res = prefix[pos][r]
        if l > 0:
            res -= prefix[pos][l - 1]
        
        return res
''',
    call=f'Solution().largestMagicSquare({GRID!r})',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='text', h=70, size=26, fn=_info),
    ],
    watch=[('lx', 'lx', 'blue'), ('ly', 'ly', 'pink'), ('s', 's', 'cyan'), ('l_cross', 'l_cross', 'green'), ('r_cross', 'r_cross', 'cyan')],
    skip=[13, 17, 25, 31, 58, 59, 60, 62],
    max_steps=80,
    captions={
        7: '`h_prefix[i]`：第 `i` 行的前缀和',
        8: '`v_prefix[j]`：第 `j` 列的前缀和',
        12: '格子 `({i}, {j})` = {grid[i][j]}：先放进行前缀和',
        14: '行前缀：累加左边一格 → `h_prefix[{i}]` = {h_prefix[i]}',
        16: '同一个格子放进列前缀和',
        18: '列前缀：累加上边一格 → `v_prefix[{j}]` = {v_prefix[j]}',
        20: '`res` 先取 1：`1 x 1` 一定是幻方',
        23: lambda S, B, r: f'边长 `l` 从 2 枚举到 `min(m−lx, n−ly) = {min(len(S.grid) - S.lx, len(S.grid[0]) - S.ly)}`',
        24: '右下角 `rx = {rx}`，`ry = {ry}`',
        26: '主对角线先放左上角：`l_cross = {l_cross}`',
        27: '副对角线先放右上角：`r_cross = {r_cross}`',
        29: '算第一行这一段（列 `{ly}`~`{ry}`）的和 `s`：其余行、列、对角线都要等于它',
        33: lambda S, B, r: f'第 `{S.index}` 行这段的和 `{sum(S.grid[S.index][S.ly:S.ry + 1])}` 与 `s = {S.s}`：' + ('相等，继续' if sum(S.grid[S.index][S.ly:S.ry + 1]) == S.s else '不等 → 这个正方形不行'),
        34: '行和不一致：`flag = False`，不用再看',
        37: '主对角线在第 `{index}` 行的格子 `grid[{index}][{ly + index - lx}]`：`l_cross` → {l_cross}',
        38: '副对角线在第 `{index}` 行的格子 `grid[{index}][{ry - index + lx}]`：`r_cross` → {r_cross}',
        40: lambda S, B, r: '行和都不对，换下一个正方形' if not S.flag else '各行的和都等于 `s`，继续查对角线和列',
        43: lambda S, B, r: (f'`l_cross = {S.l_cross}`，`r_cross = {S.r_cross}`，`s = {S.s}`：' + ('两条对角线都等于 `s`' if S.l_cross == S.s and S.r_cross == S.s else '对角线不等 → 不行')),
        46: '最后核对每一列：列和也要等于 `s`',
        48: lambda S, B, r: f'第 `{S.index}` 列这段的和 `{sum(S.grid[a][S.index] for a in range(S.lx, S.rx + 1))}` 与 `s = {S.s}`：' + ('相等' if sum(S.grid[a][S.index] for a in range(S.lx, S.rx + 1)) == S.s else '不等'),
        52: lambda S, B, r: '行、列、对角线全部等于 `s`：是幻方' if S.flag else '有一列不等，不是幻方',
        53: '是幻方，`res = max(res, {l})` → =={res}==',
        55: '所有正方形枚举完，最大边长 =={res}==',
        58: '取这一行（列）的前缀和 `prefix[{pos}][{r}]` = {res}',
        60: '左端点不是 0，减去 `prefix[{pos}][{l - 1}]` → 区间和 = {res}',
        62: '区间和 =={res}==',
    },
    cards=dict(
        one_liner='数据只有 50：枚举左上角和边长，逐行逐列核对',
        complexity='时间 `O(mn·min(m,n)^2)`，空间 `O(mn)`',
        problem=['每行、每列、两条对角线之和都相等的 `k x k` 方阵叫幻方',
                 '求矩阵里最大幻方的边长，`1 x 1` 一定是幻方',
                 '示例：`[[5,1,3,1],[9,3,3,1],[1,3,3,8]]` → `2`'],
        quote='没有什么特别好的想法，不过由于题目的数据规模并不大，因此可以选择枚举幻方的左上角(lx, ly)以及边长l，然后通过(lx, ly)以及l计算出(rx, ry)。',
        quote_src='—— yiduobo 题解原文',
        idea=['给每一行、每一列各维护一个前缀和，任意区间和 `O(1)`',
              '枚举左上角和边长，第一行的和记为 `s`，其余行的和要等于 `s`',
              '对角线在逐行核对时顺便累加；最后再核对每一列'],
        summary=['时间 `O(mn·min(m,n)^2)`，规模 50 完全够用',
                 '`res` 初值为 1：单个格子一定是幻方',
                 '行不合格就 `break` 并 `continue`，不会白查列',
                 '对比灵神：灵神用四种前缀和并从大到小找，找到就返回；这里全部枚举取最大'],
    ),
)
