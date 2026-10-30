GRID = [['.', 'X', 'Y'], ['Y', '.', '.']]   # 每一行互不相同，便于用 index 反查行号


def _valid():
    """按行优先顺序，所有「X、Y 一样多且至少一个 X」的右下角"""
    out = []
    for a in range(len(GRID)):
        for b in range(len(GRID[0])):
            x = sum(GRID[i][j] == 'X' for i in range(a + 1) for j in range(b + 1))
            y = sum(GRID[i][j] == 'Y' for i in range(a + 1) for j in range(b + 1))
            if x == y > 0:
                out.append((a, b))
    return out


VALID = _valid()


def _ij(S):
    if 'row' not in S or 'grid' not in S:
        return None, None
    i = S['grid'].index(S['row'])
    ln = S['_line']
    j = S['j'] if ln >= 7 and ln <= 13 and 'j' in S else None
    return i, j


def _rect_j(S):
    """s0 / s1 此刻累计到第几列（含）"""
    i, j = _ij(S)
    if i is None or j is None:
        return -1
    return j if S['_line'] >= 10 else j - 1


def _gcolor(S, a, b, v):
    if (a, b) in VALID[:S.get('ans', 0)]:
        return 'green'
    i, j = _ij(S)
    if i is None or j is None:
        return None
    if a <= i and b <= _rect_j(S):
        return 'blue'
    return None


def _ccolor(S, r, j, v):
    i, jj = _ij(S)
    if jj is None:
        return None
    if j == jj and S['_line'] in (9, 10, 11):
        return 'yellow'
    if j <= _rect_j(S):
        return 'blue'
    return None


def _cc(S):
    cc = S['col_cnt']
    return [[c[0] for c in cc], [c[1] for c in cc]]


def _text(S):
    i, j = _ij(S)
    if 'col_cnt' not in S:
        return '子矩阵必须包含 `grid[0][0]` → 只数「左上角固定在 (0,0)」的矩阵，右下角 `(i, j)` 随便选'
    if i is None:
        return '`col_cnt[j]` 记第 `j` 列到当前行为止的 X、Y 个数；`s0`、`s1` 是它们的横向累加'
    ln = S['_line']
    if ln in (7, 8, 9):
        return f"看格子 `({i},{j}) = '{GRID[i][j]}'`，先更新它所在列的计数"
    rj = _rect_j(S)
    return f"子矩阵 `(0,0)–({i},{j})`：X 共 `{S['s0']}` 个，Y 共 `{S['s1']}` 个" + ('' if ln != 12 else '　→ 相等且大于 0 才算')


def _cap_for_row(S, B, r):
    if 'row' in B and B.row == S.row:
        return '所有行都处理完了'
    return f'下一行：第 `{S.grid.index(S.row)}` 行。`col_cnt` 保留，列里继续往下累加'


def _cap_for_j(S, B, r):
    if 'j' in B and B.j == S.j and B.c == S.c:
        return '这一行扫完了'
    return f"从左往右：`(j={S.j}, c='{S.c}')`，枚举右下角 `({S.grid.index(S.row)}, {S.j})`"


def _cap_if_c(S, B, r):
    if S.c == '.':
        return "`c = '.'`：空格子，不影响 X、Y 的个数"
    return f"`c = '{S.c}'`：是 X 或 Y，要给第 `{S.j}` 列计数"


def _cap_cnt(S, B, r):
    k = ord(S.c) & 1
    return (f"`ord('{S.c}') & 1 = {k}`：X 的最低位是 0，Y 是 1，==不用判断是哪个字母=="
            f" → `col_cnt[{S.j}]` = `{S.col_cnt[S.j]}`")


def _cap_cmp(S, B, r):
    if S.s0 == S.s1 and S.s0 > 0:
        return f'`s0 = s1 = {S.s0} > 0`：X、Y 一样多且至少一个 X → ==合法=='
    if S.s0 == S.s1:
        return '`s0 = s1 = 0`：虽然相等，但一个 X 都没有 → ==不算=='
    return f'`s0 = {S.s0} ≠ s1 = {S.s1}` → 不合法'


CONFIG = dict(
    num=3212, title='统计 X 和 Y 频数相等的子矩阵数量', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='二维前缀和 · 只维护每列的计数',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1673'],
    code='''
class Solution:
    def numberOfSubmatrices(self, grid: List[List[str]]) -> int:
        col_cnt = [[0, 0] for _ in grid[0]]
        ans = 0
        for row in grid:
            s0 = s1 = 0
            for j, c in enumerate(row):
                if c != '.':
                    col_cnt[j][ord(c) & 1] += 1
                s0 += col_cnt[j][0]
                s1 += col_cnt[j][1]
                if s0 == s1 > 0:
                    ans += 1
        return ans
''',
    call=f'Solution().numberOfSubmatrices({GRID})',
    expect=2,
    views=[
        dict(type='text', fn=_text, size=26, h=70),
        dict(type='grid', var='grid', label='grid（黄框 = 当前格 (i,j)，蓝 = 正在统计的子矩阵，绿 = 已算进答案的右下角）', cell=96, h=330,
             color=_gcolor, cursors=[(lambda S: _ij(S)[0], lambda S: _ij(S)[1], 'yellow')]),
        dict(type='table', var=_cc, label='col_cnt（第 j 列到当前行的个数；黄 = 刚更新的列）', cell=84, h=210,
             rows=['X', 'Y'], cols=lambda S: list(range(len(S['col_cnt']))), color=_ccolor),
    ],
    watch=[('j', 'j', 'yellow'), ('c', 'c'), ('s0', 's0', 'blue'), ('s1', 's1', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'col_cnt = [[0, 0]': '`col_cnt[j] = [X 个数, Y 个数]`：第 `j` 列==到当前行为止==的计数，初始全 0',
        'ans = 0': '`ans` 统计合法的子矩阵（右下角 `(i, j)`，左上角固定 `(0,0)`）',
        'for row in grid': _cap_for_row,
        's0 = s1 = 0': '每行重新开始：`s0`、`s1` 累加本行从第 0 列到当前列的 `col_cnt`',
        'for j, c in enumerate(row)': _cap_for_j,
        "if c != '.'": _cap_if_c,
        'col_cnt[j][ord(c) & 1] += 1': _cap_cnt,
        's0 += col_cnt[j][0]': lambda S, B, r: f'加上第 `{S.j}` 列的 X 个数 `{S.col_cnt[S.j][0]}` → `s0 = {S.s0}`：`(0,0)–({_ij(S)[0]},{S.j})` 里 X 的总数',
        's1 += col_cnt[j][1]': lambda S, B, r: f'加上第 `{S.j}` 列的 Y 个数 `{S.col_cnt[S.j][1]}` → `s1 = {S.s1}`：同一个子矩阵里 Y 的总数',
        'if s0 == s1 > 0': _cap_cmp,
        'ans += 1': lambda S, B, r: f'`ans` → =={S.ans}==：`(0,0)–({_ij(S)[0]},{S.j})` 这个子矩阵合法',
        'return ans': '所有右下角都看过了，答案 =={ret}==',
    },
    cards=dict(
        one_liner='子矩阵含左上角 → 只数前缀矩阵；用每列的计数一路累加',
        complexity='时间 `O(mn)`，空间 `O(n)`',
        problem=['`grid[i][j]` 是 `X`、`Y` 或 `.`，数有多少子矩阵满足',
                 '包含 `grid[0][0]`、`X` 和 `Y` 个数相等、至少含一个 `X`',
                 '示例：`[["X","Y","."],["Y",".","."]]` → `3`',
                 '本视频用 `[".XY","Y.."]`（`.` 是空格子）→ `2`'],
        quote='遍历每一行，同时用一个长为 n×2 的数组 colCnt 维护每一列的 X 和 Y 的个数。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['子矩阵一定是左上角 `(0,0)`、右下角 `(i,j)` 的前缀矩阵',
              '`col_cnt[j]` 记第 `j` 列到当前行的 X、Y 个数；本行从左往右累加成 `s0`、`s1`',
              '`ord(c) & 1`：X 是 0，Y 是 1，直接当下标，不用 if 判断字母'],
        summary=['时间 `O(mn)`，空间 `O(n)`；方法一用二维前缀和 `s[i+1][j+1]`，空间 `O(mn)`',
                 '易错：`s0 == s1 > 0`，两者都为 0（全是 `.`）不能算',
                 '`s0`、`s1` 每一行都要清零，`col_cnt` 不能清零',
                 '思考题：不要求含左上角 → 枚举上下边界化成一维（363 题思路）'],
    ),
)
