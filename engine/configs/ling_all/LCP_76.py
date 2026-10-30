A0 = ['..R', '..B', '?R?']
NAMES = ['空', 'B', 'R', 'B连', 'R连', '交替B尾', '交替R尾']


def _cols(S):
    cm = S.get('col_mask', S.get('mask'))
    m = S.get('m', 3)
    if cm is None:
        return None
    return [NAMES[(cm >> (3 * k)) & 7] for k in range(m)]


def _txt(S):
    I = S['_inner']
    if 'row_mask' in I:
        cols = _cols(I)
        return f"本行序列：=={NAMES[I['row_mask']]}==　各列序列：`{' | '.join(cols)}`"
    if 'mask' in I:
        return f"进入第 `{I['r']}` 行，各列序列：`{' | '.join(_cols(I))}`"
    return '每行/每列的 RB 序列只有 7 种状态：空、B、R、B连、R连、BR 交替(B 尾)、BR 交替(R 尾)'


def _nxt_cap(S, B, ret):
    I = S['_inner']
    color = 'B' if I['color'] == 0 else 'R'
    rm, cm = S.rm, None
    return None


def _cell(S, i, j, v):
    r = S['_inner'].get('r', S.get('r'))
    c = S['_inner'].get('c')
    if r is None:
        return None
    if i < r:
        return 'green' if v != '.' and v != '?' or True else None
    return None


CONFIG = dict(
    num='LCP 76', title='魔法棋盘', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='轮廓线 DP（7 种序列状态 + 记忆化）',
    tags=['灵神题单·动态规划', '灵神题单·常用数据结构'],
    code='''
TRANS = (
    # (当前序列末尾添加 B 之后的状态，当前序列末尾添加 R 之后的状态)
    (1, 2),   # 0: 空
    (3, 6),   # 1: 一个 B
    (5, 4),   # 2: 一个 R
    (3, -1),  # 3: 连续多个 B
    (-1, 4),  # 4: 连续多个 R
    (-1, 6),  # 5: BR 交替，且以 B 结尾
    (5, -1),  # 6: BR 交替，且以 R 结尾
)

class Solution:
    def getSchemeCount(self, n: int, m: int, a: List[str]) -> int:
        if n < m:  # 保证 n >= m
            a = [list(col) for col in zip(*a)]
            n, m = m, n
        @cache
        def DFS(r: int, mask: int) -> int:
            if r == n:  # 找到 1 个合法方案
                return 1
            # 写一个暴搜，生成所有的合法状态
            def dfs(c: int, row_mask: int, col_mask: int) -> int:
                if c == m:  # 方案合法
                    return DFS(r + 1, col_mask)  # 枚举下一行
                def nxt(color: int) -> int:
                    rm = TRANS[row_mask][color]  # 新的 rowMask
                    if rm < 0: return 0  # 非法
                    c3 = c * 3
                    cm = TRANS[(col_mask >> c3) & 7][color]  # 新的 colMask 的第 c 列
                    if cm < 0: return 0 # 非法
                    cm = col_mask & ~(7 << c3) | (cm << c3)  # 修改 colMask 的第 c 列
                    return dfs(c + 1, rm, cm)
                b = a[r][c]
                if b == 'B': return nxt(0)
                if b == 'R': return nxt(1)
                if b == '.': return dfs(c + 1, row_mask, col_mask)
                return dfs(c + 1, row_mask, col_mask) + nxt(0) + nxt(1)
            return dfs(0, 0, mask)
        return DFS(0, 0)
''',
    call=f'Solution().getSchemeCount(3, 3, {A0})',
    expect=5,
    views=[
        dict(type='grid', var=lambda S: A0, label='chessboard（黄 = 当前格；暗 = 已决定的行）', cell=100, h=300,
             cursors=[(lambda S: S['_inner'].get('r', S.get('r')) if 'c' in S['_inner'] else None,
                       lambda S: S['_inner'].get('c'), 'yellow')]),
        dict(type='text', size=26, h=70, fn=_txt),
        dict(type='calls', h=230, hide=('a',)),
    ],
    watch=[('r', lambda S: S['_inner'].get('r', S.get('r')), 'blue'), ('c', lambda S: S['_inner'].get('c'), 'yellow'),
           ('row_mask', lambda S: S['_inner'].get('row_mask'), 'pink'), ('col_mask', lambda S: S['_inner'].get('col_mask'), 'green')],
    skip=['if n < m', 'a = [list', 'n, m = m, n', 'def ', 'TRANS = (', 'c3 = c * 3'],
    captions={
        'return DFS(0, 0)': '从第 0 行出发，各列序列都是「空」：`DFS(0, 0)`',
        'if r == n': lambda S, B, r: ('`r == n`：所有行都放好了 → ==找到 1 个合法方案==' if S.r == S.n else f'`r = {S.r} < n`：还要放第 `{S.r}` 行'),
        'return dfs(0, 0, mask)': '暴搜第 `{r}` 行每一格放什么：`dfs(0, 0, mask)`',
        'if c == m': lambda S, B, r: (f'`c == m`：这一行放完且合法 → 带着新的各列状态去 `DFS({S.r + 1}, ...)`' if S.c == S.m else f'第 `{S.r}` 行第 `{S.c}` 列'),
        'rm = TRANS[row_mask][color]': lambda S, B, r: (f'本行末尾加 {"B" if S.color == 0 else "R"}：`{NAMES[S.row_mask]}` → '
                                                       + (f'`{NAMES[S.rm]}`' if S.rm >= 0 else '==非法（出现共鸣）==')),
        'if rm < 0': lambda S, B, r: ('本行序列非法 → 这种放法不要，返回 0' if S.rm < 0 else '本行序列合法，再看这一列'),
        'cm = TRANS[(col_mask >> c3) & 7][color]': lambda S, B, r: (f'这一列末尾加 {"B" if S.color == 0 else "R"}：`{NAMES[(S.col_mask >> S.c3) & 7]}` → '
                                                                   + (f'`{NAMES[S.cm]}`' if S.cm >= 0 else '==非法==')),
        'if cm < 0': lambda S, B, r: ('这一列序列非法 → 返回 0' if S.cm < 0 else '行、列都合法 → 继续放下一格'),
        'cm = col_mask & ~': lambda S, B, r: f'只改 `col_mask` 里第 `{S.c}` 列的 3 个比特，其余列不变：各列变成 `{" | ".join(_cols({"col_mask": S.cm, "m": S.m}))}`',
        'return dfs(c + 1, rm, cm)': '这一格放好了，往右走一格，继续决定下一列',
        'b = a[r][c]': '看棋盘这一格 `a[{r}][{c}] = {b!r}`，决定怎么放',
        "if b == 'B'": lambda S, B, r: ('是 `B` → 只能放黑棋' if S.b == 'B' else '不是 `B`，看下一个条件'),
        "if b == 'R'": lambda S, B, r: ('是 `R` → 只能放红棋' if S.b == 'R' else '不是 `R`，看下一个条件'),
        "if b == '.'": lambda S, B, r: ('是 `.` → 确定为空，序列不变，直接下一列' if S.b == '.' else '不是 `.`，只剩 `?` 了'),
        "return dfs(c + 1, row_mask, col_mask) + nxt(0)": '`?` 待定：==空、放 B、放 R== 三种情况都试，方案数相加',
    },
    max_steps=70,
    cards=dict(
        one_liner='每行每列的 RB 序列只有 7 种状态，逐行记忆化 + 行内暴搜',
        complexity='时间 `O(n·21^m)`（m ≤ 5），空间 `O(n·8^m)`',
        problem=['`n × m` 棋盘，格子是 `.` 空、`B` 黑、`R` 红、`?` 待定',
                 '同行/同列两颗异色棋子，中间恰好只隔一颗棋子 → 产生共鸣（中间可有空位）',
                 '把所有 `?` 填成 空/黑/红，使得任意两子都==不共鸣==，求方案数',
                 '本视频：`["..R","..B","?R?"]` → `5`'],
        quote='对于一行或者一列的 RB 序列，有以下 7 种情况：空；只有一个 B；只有一个 R；连续多个 B；连续多个 R；BR 交替，且以 B 结尾；BR 交替，且以 R 结尾。',
        quote_src='—— 灵茶山艾府题解',
        idea=['序列末尾追加 B/R，状态按 `TRANS` 表转换，`-1` 表示出现共鸣',
              '7 种状态用 3 个比特存，所有列合在一起就是 `mask`，`DFS(r, mask)` 记忆化',
              '行内再写一个暴搜 `dfs(c, row_mask, col_mask)`，枚举这一行怎么放，放完得到下一行的 `mask`'],
        result='所有 `?` 的填法里，合法的共 5 种 ✓',
        summary=['时间 `O(n·21^m)`：状态 `n·7^m` 个，每个状态暴搜 `3^m`',
                 '`n < m` 时先转置，保证 `m ≤ 5`',
                 '易错：单个 B/R 要独立成状态，它既能变连续、也能变交替',
                 '异色棋子之间可以有空位，所以「空」不改变序列状态',
                 '题解还附有视频：力扣杯 2023 春个人赛第五题'],
    ),
)
