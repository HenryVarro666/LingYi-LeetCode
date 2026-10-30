def _dep(S, i, j, v):
    if (i, j) == (S['i'] + 1, S['j']):
        return 'pink'      # 左：f[i+1][j]
    if (i, j) == (S['i'], S['j'] + 1):
        return 'blue'      # 上：f[i][j+1]
    if (i, j) == (0, 1):
        return 'orange'    # f[0][1] = 0
    return None


def _formula(S):
    if 'x' not in S:
        return '`f[i+1][j+1] = min(f[i+1][j]`（左）`, f[i][j+1]`（上）`) + x`'
    i, j, f, x = S['i'], S['j'], S['f'], S['x']
    left, up = f[i + 1][j], f[i][j + 1]
    fm = lambda v: '∞' if v == inf else str(v)
    return f'f[{i + 1}][{j + 1}] = min(左 {fm(left)}, 上 {fm(up)}) + x {x} = =={min(left, up) + x}=='


def _cap_cell(S, B, ret):
    i, j, f, x = S.i, S.j, S.f, S.x
    left, up, v = f[i + 1][j], f[i][j + 1], f[i + 1][j + 1]
    if (i, j) == (0, 0):
        return f'起点：左边出界是 ∞，上面是 `f[0][1] = 0` → `min = 0`，再加 `x = {x}` → `{v}`，就是 `grid[0][0]`'
    if i == 0:
        if j > 1:
            return f'第一行同理，只能从左边来：`{left} + {x} = {v}`'
        return f'第一行：上面出界是 ==∞==，min 不会选它 → 只能从左边来：`{left} + {x} = {v}`'
    if j == 0:
        return f'新的一行 `row = {S.row}`。第一列：左边出界是 ==∞== → 只能从上面来：`{up} + {x} = {v}`'
    side = '左边' if left <= up else '上面'
    return f'最后一步从左来 `{left}`、从上来 `{up}`，取小的（{side}）再加 `x = {x}` → =={v}=='


CONFIG = dict(
    num=64, title='最小路径和', difficulty='Medium', category='多维动态规划',
    author='灵茶山艾府', technique='网格图 DP：记忆化搜索 → 递推',
    code='''
class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        f = [[inf] * (n + 1) for _ in range(m + 1)]
        f[0][1] = 0
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                f[i + 1][j + 1] = min(f[i + 1][j], f[i][j + 1]) + x
        return f[m][n]
''',
    call='Solution().minPathSum([[1,3,1],[1,5,1],[4,2,1]])',
    expect=7,
    skip=['f = [[inf]', 'for i, row in enumerate(grid)', 'for j, x in enumerate(row)'],
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='grid', var='grid', label='grid（黄框 = 当前格 x）', cursors=[('i', 'j', 'yellow')], cell=60, h=215),
        dict(type='table', var='f', label='f[i+1][j+1] = dfs(i,j)：左上角到 (i,j) 的最小路径和',
             rows=lambda S: ['i=-1', 'i=0', 'i=1', 'i=2'], cols=lambda S: ['j=-1', 'j=0', 'j=1', 'j=2'],
             cursors=[('m', 'n', 'green'), ('i + 1', 'j + 1', 'yellow')], color=_dep, cell=76, h=358),
    ],
    watch=['i', 'j', 'x', ('左 f[i+1][j]', 'f[i + 1][j]', 'pink'), ('上 f[i][j+1]', 'f[i][j + 1]', 'blue')],
    captions={
        'm, n = len(grid)': '网格 `m = {m}` 行、`n = {n}` 列',
        'f[0][1] = 0': 'f 多开一行一列，全设为 ==∞==：出界不合法，`min` 永远不会选它；再令 `f[0][1] = 0`，`f[1][1]` 就不用特判',
        'f[i + 1][j + 1] =': _cap_cell,
        'return f[m][n]': '`f[m][n]` 翻译自递归入口 `dfs(m-1, n-1)`：最小路径和 =={ret}==（`1→3→1→1→1`）',
    },
    cards=dict(
        one_liner='想清楚最后一步：从左边来，还是从上边来？',
        complexity='时间 `O(mn)`，空间 `O(mn)`（可优化到 `O(n)` / `O(1)`）',
        problem=['`m × n` 网格 `grid` 里都是非负整数，==每次只能向下或向右==走一步',
                 '求从左上角到右下角，路径上数字总和的最小值',
                 '示例：`[[1,3,1],[1,5,1],[4,2,1]]` → `7`（`1→3→1→1→1`）'],
        quote='==见微知著，想清楚最后一步发生了什么，就想清楚每一步发生了什么。==',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i,j)` = 左上角到 `(i,j)` 的最小价值和；最后一步来自左边或上边',
              '`dfs(i,j) = min(dfs(i,j-1), dfs(i-1,j)) + grid[i][j]`',
              '边界：出界返回 ==∞==（不合法，`min` 不会选），`dfs(0,0) = grid[0][0]`',
              '`dfs(2,2)` 先左再上、先上再左都会调用 `dfs(1,1)` → `@cache` 记忆化',
              '去掉「递」只留「归」：`f[i+1][j+1]` 就是 `dfs(i,j)`'],
        after=[dict(heading='答疑（原文）', lines=[
            '问：看上去 dfs 是从右下往左上算的？',
            '答：加法发生在递归==「归」==的时候，所以计算顺序其实是从左上到右下',
            '问：为什么 `grid[i][j]` 的下标不用 +1？',
            '答：只是在 f 的最左、最上插了一排状态，==只改和 f 有关的下标==',
        ])],
        summary=['空间优化：一维 `f[j+1] = min(f[j], f[j+1]) + x`，空间 `O(n)`',
                 '易错：f 初始化 `inf` 而不是 `0`，否则出界会被当成合法路径',
                 '空间优化版也不能令 `f[0] = 0`：`i > 1` 时 `f[i][0]` 必须是 ∞',
                 '原文还给了直接复用 `grid[0]` 的 `O(1)` 额外空间写法'],
    ),
)
