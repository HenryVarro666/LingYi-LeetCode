def _dep(S, i, j, v):
    if (i, j) == (S['i'], S['j'] + 1):
        return 'blue'      # 上：f[i][j+1]
    if (i, j) == (S['i'] + 1, S['j']):
        return 'pink'      # 左：f[i+1][j]
    if (i, j) == (0, 1):
        return 'orange'    # 虚拟起点
    return None


def _formula(S):
    if 'j' not in S:
        return '`f[i+1][j+1] = f[i][j+1]`（上）` + f[i+1][j]`（左）'
    i, j, f = S['i'], S['j'], S['f']
    up, left = f[i][j + 1], f[i + 1][j]
    return f'f[{i + 1}][{j + 1}] = 上 f[{i}][{j + 1}] + 左 f[{i + 1}][{j}] = {up} + {left} = =={up + left}=='


def _cap_cell(S, B, ret):
    i, j, f = S.i, S.j, S.f
    up, left, v = f[i][j + 1], f[i + 1][j], f[i + 1][j + 1]
    if (i, j) == (0, 0):
        return f'起点 `(0,0)`：上面是虚拟起点 `f[0][1] = 1`，左边出界为 0 → `1 + 0 = 1`，对应 `dfs(0,0) = 1`'
    if i == 0:
        if j > 1:
            return f'第一行同理：只能从左边来 → `{v}`'
        return f'第一行：上面出界（0 条路），==只能从左边来== → `{up} + {left} = {v}`'
    if j == 0:
        return f'新的一行 `i = {i}`。第一列：左边出界（0 条路），==只能从上面来== → `{up} + {left} = {v}`'
    return f'到 `({i},{j})` 的最后一步：从上面来 `{up}` 条 + 从左边来 `{left}` 条，互斥 → 加法原理 = =={v}=='


CONFIG = dict(
    num=62, title='不同路径', difficulty='Medium', category='多维动态规划',
    author='灵茶山艾府', technique='网格图 DP：记忆化搜索 → 递推',
    code='''
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        f = [[0] * (n + 1) for _ in range(m + 1)]
        f[0][1] = 1
        for i in range(m):
            for j in range(n):
                f[i + 1][j + 1] = f[i][j + 1] + f[i + 1][j]
        return f[m][n]
''',
    call='Solution().uniquePaths(3, 4)',
    expect=10,
    skip=['f = [[0] * (n + 1)', 'for i in range(m)', 'for j in range(n)'],
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='table', var='f', label='f[i+1][j+1] = 从 (0,0) 走到 (i,j) 的路径数（表头是原网格坐标）',
             rows=lambda S: ['i=-1', 'i=0', 'i=1', 'i=2'], cols=lambda S: ['j=-1', 'j=0', 'j=1', 'j=2', 'j=3'],
             cursors=[('m', 'n', 'green'), ('i + 1', 'j + 1', 'yellow')],
             color=_dep, cell=108, h=574),
    ],
    watch=['i', 'j', ('上 f[i][j+1]', 'f[i][j + 1]', 'blue'), ('左 f[i+1][j]', 'f[i + 1][j]', 'pink'),
           ('f[m][n]', 'f[m][n]', 'green')],
    captions={
        'f[0][1] = 1': 'f 表多开一行一列，全是 0（出界 = 0 条路）；再令 `f[0][1] = 1`：把 `(-1,0)` ==当起点，第一步只能往下走==',
        'f[i + 1][j + 1] =': _cap_cell,
        'return f[m][n]': '`f[m][n]` 翻译自递归入口 `dfs(m-1, n-1)`：答案 =={ret}==',
    },
    cards=dict(
        one_liner='想清楚最后一步从哪来：上面 + 左边',
        complexity='时间 `O(mn)`，空间 `O(mn)`（可优化到 `O(n)`）',
        problem=['机器人在 `m × n` 网格左上角，==每次只能向下或向右==走一步',
                 '问走到右下角共有多少条不同路径',
                 '示例：`m = 3, n = 4` → `10`（下面就演示它）'],
        quote='想一想，==最后一步==发生了什么？……这些问题都是==和原问题相似的、规模更小的子问题==，可以用递归解决。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i,j)` = 从 `(0,0)` 走到 `(i,j)` 的路径数；最后一步来自上或左',
              '`dfs(i,j) = dfs(i-1,j) + dfs(i,j-1)`；出界为 0，`dfs(0,0) = 1`',
              '入参相同的调用大量重复 → `@cache` 记忆化，每个状态只算一次',
              '去掉「递」只留「归」：`f[i+1][j+1]` ==就是== `dfs(i,j)`，+1 给出界状态留位置'],
        after=[dict(heading='从记忆化搜索到递推', lines=[
            '记忆化：`dfs(m-1,n-1)` 往回递归，边界 `dfs(-1,j) = dfs(i,-1) = 0`',
            '递推：f 第 0 行 / 第 0 列就是这些出界状态，全为 0',
            '原文先写 `if i == j == 0: f[1][1] = 1` 特判',
            '再改成 `f[0][1] = 1`，`f[1][1]` ==也能用同一个式子算==',
        ])],
        summary=['时间 `O(mn)`、空间 `O(mn)`；只用一行 `f[j+1] += f[j]` 可降到 `O(n)`',
                 '易错：f 要开 `(m+1) × (n+1)`，下标整体 +1，返回 `f[m][n]`',
                 '另一种方法：组合数学，共走 `m+n-2` 步选 `m-1` 步向下 → `comb(m+n-2, m-1)`',
                 '进阶：有障碍物 → 63. 不同路径 II'],
    ),
)
