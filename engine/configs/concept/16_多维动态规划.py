GRID = [[1, 3, 1, 2], [1, 5, 1, 3], [4, 2, 1, 1]]


def _f_color(S, r, c, v):
    if 'i' in S and 'j' in S and S.get('_line') in (7, 10):
        i, j = S['i'], S['j']
        if (r, c) == (i + 1, j) or (r, c) == (i, j + 1):
            return 'yellow'                       # 当前格子依赖的「左」和「上」
    if v != float('inf') and r > 0 and c > 0:
        return 'green'
    return None


def _grid_color(S, r, c, v):
    if 'i' in S and 'j' in S and (r, c) == (S['i'], S['j']):
        return 'pink'
    return None


def _formula(S):
    if 'f' not in S or 'i' not in S or 'j' not in S or 'x' not in S:
        return '`f[i+1][j+1]` = 从左上角走到 `(i, j)` 的最小路径和（多开一行一列存 ∞）'
    i, j, f, x = S['i'], S['j'], S['f'], S['x']
    if i == j == 0:
        return f'起点：`f[1][1] = grid[0][0] = {x}`'
    a, b = f[i + 1][j], f[i][j + 1]
    fa = '∞' if a == float('inf') else a
    fb = '∞' if b == float('inf') else b
    return f'`f[{i + 1}][{j + 1}] = min(左 {fa}, 上 {fb}) + {x}`'


CONFIG = dict(
    num=None, title='多维动态规划 · 通用思想与模板', author='概念讲解', category='多维动态规划',
    technique='通用思想与模板', kind='concept', difficulty='',
    code='''
def min_path_sum(grid):              # 64. 最小路径和
    m, n = len(grid), len(grid[0])
    # f[i+1][j+1] = 从左上角到 (i, j) 的最小路径和
    f = [[inf] * (n + 1) for _ in range(m + 1)]  # 第 0 行 / 列 = 出界
    for i, row in enumerate(grid):   # 从上到下
        for j, x in enumerate(row):  # 从左到右
            if i == j == 0:
                f[1][1] = x          # 起点
            else:                    # 最后一步：从左边来 or 从上边来
                f[i + 1][j + 1] = min(f[i + 1][j], f[i][j + 1]) + x
    return f[m][n]
''',
    call=f'min_path_sum({GRID})',
    expect=8,
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='grid', var='grid', label='grid（粉 = 当前格子）', color=_grid_color, cell=70, h=270),
        dict(type='table', var='f', label='f（表头 = 对应 dfs 的下标；黄 = 依赖的左 / 上，绿 = 已算出）', color=_f_color, cell=70,
             rows=lambda S: ['-1'] + [str(k) for k in range(len(S['f']) - 1)],
             cols=lambda S: ['-1'] + [str(k) for k in range(len(S['f'][0]) - 1)],
             cursors=[(lambda S: S['i'] + 1 if 'i' in S and 'x' in S else None,
                       lambda S: S['j'] + 1 if 'j' in S and 'x' in S else None, 'pink')], h=330),
    ],
    watch=[('i', 'i', 'pink'), ('j', 'j', 'pink'), ('x', 'x')],
    captions={
        'm, n = len': '网格 `{m} × {n}`，只能向右或向下走，求路径上数字之和的最小值',
        'f = [[inf]': '`f` 比 grid 多一行一列：第 0 行、第 0 列是 `∞`，翻译自 ==出界的状态 dfs(-1, j) = ∞==',
        'for i, row': lambda S, B, ret: (f'第 `{S.i}` 行：从上到下填表' if B.get('i') != S.i or 'row' not in B
                                         else '整张表填完'),
        'for j, x': lambda S, B, ret: (f'格子 `({S.i}, {S.j})`，`grid = {S.x}`' if (B.get('i'), B.get('j')) != (S.i, S.j)
                                       or 'x' not in B else f'第 `{S.i}` 行填完'),
        'if i == j == 0': lambda S, B, ret: ('是起点' if S.i == S.j == 0 else
                                             f'最后一步：从左边 `({S.i},{S.j - 1})` 或上边 `({S.i - 1},{S.j})` 走过来（黄色）'),
        'f[1][1] = x': '起点：`f[1][1] = {x}`（翻译自递归边界 `dfs(0, 0) = grid[0][0]`）',
        'f[i + 1][j + 1] = min': lambda S, B, ret: (
            f'`f[{S.i + 1}][{S.j + 1}] = min({_v(S.f[S.i + 1][S.j])}, {_v(S.f[S.i][S.j + 1])}) + {S.x} = {S.f[S.i + 1][S.j + 1]}`'
            + ('：左边是 ∞ → 只能从上面来' if S.j == 0 else ('：上边是 ∞ → 只能从左边来' if S.i == 0 else
               ('：从左边来更小' if S.f[S.i + 1][S.j] < S.f[S.i][S.j + 1] else '：从上边来更小')))),
        'return f[m][n]': '答案 `f[{m}][{n}] = {ret}`：`O(mn)` 个状态，每个 `O(1)`',
    },
    cards=dict(
        one_liner='状态要两个下标才说清：想清楚「最后一步」，按依赖顺序填表',
        complexity='时间 `O(mn)`，空间 `O(mn)`（可压成 `O(n)`）',
        problem_heading='什么时候用？',
        problem=['状态需要两个下标：网格位置 `(i, j)`、两个串的前缀 `(i, j)`',
                 '网格里只能向右 / 向下走，求路径数或最小和',
                 '两个字符串比较：最长公共子序列、编辑距离',
                 '子串 / 区间问题：`f[i][j]` 描述 `s[i..j]`（回文子串）'],
        before=[dict(heading='核心概念：二维状态 + 填表顺序', lines=[
            '定义 `f[i][j]`，看 ==最后一步== 从哪来：左边 / 上边，或两串末尾',
            '多开一行一列放边界（`∞` 或 `0`），省掉 `i == 0`、`j == 0` 的特判',
            '填表顺序 = 依赖关系：依赖左和上，就从上到下、从左到右',
            '只依赖上一行 → 可以压成一维数组']),
        ],
        idea_heading='两位作者怎么说',
        quote='见微知著，==想清楚最后一步发生了什么，就想清楚每一步发生了什么==。',
        quote_src='—— 灵茶山艾府 · 64. 最小路径和',
        idea=['灵神：二维也走「递归 → 记忆化 → 递推」，`f` 多开一行一列存出界的 `∞`',
              'yiduobo 64 直接令 `f[i][j]` 为走到 `(i, j)` 的最小和，分起点 / 首行 / 首列讨论',
              '1143 / 72：两人都盯着 ==两个串的最后一个字符==，相等就一起去掉'],
        summary_heading='本类 Hot100 题目 & 学习顺序',
        summary=['`62` 不同路径：`f[i][j] = f[i-1][j] + f[i][j-1]`（或组合数）',
                 '`64` 最小路径和：`min(左, 上) + grid[i][j]`',
                 '`5` 最长回文子串：中心扩展 / 区间 DP',
                 '`1143` 最长公共子序列：末尾相等 `+1`，否则去掉一个取 max',
                 '`72` 编辑距离：插入、删除、替换三种转移取最小',
                 '易错：多开一行一列时 `f` 下标整体 `+1`，`grid` 下标不变'],
    ),
)


def _v(a):
    return '∞' if a == float('inf') else a
