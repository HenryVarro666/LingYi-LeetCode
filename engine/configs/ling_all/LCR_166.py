G0 = [[1, 3, 1, 2], [1, 5, 1, 3], [4, 2, 1, 1]]


def _cur(S):
    d = S['_inner']
    return d.get('i'), d.get('j')


def _color(S, i, j, v):
    ci, cj = _cur(S)
    if ci is None:
        return None
    if (i, j) == (ci, cj):
        return 'yellow'
    if S.get('_line') == 10 and i == 0:
        if j == cj:
            return 'blue'
        if j == cj - 1:
            return 'pink'
    return None


def _formula(S):
    d = S['_inner']
    i, j, line = d.get('i'), d.get('j'), S.get('_line')
    f = S.get('f')
    if f is None:
        return '`grid[0]` 直接当 `f` 用：`f[j]` = 当前行第 `j` 列的最大价值和'
    if i is None:
        return '第 0 行：只能从左边来，做前缀和'
    if line == 12:
        return f'`f[{j}] = max(f[{j-1}], f[{j}]) + grid[{i}][{j}]`（左 `f[{j-1}]`，上 = 旧 `f[{j}]`）'
    if line == 11:
        return f'第 0 列：只能从上边来，`f[0] += grid[{i}][0]`'
    return '`f` 就是 `grid[0]`：同一块内存'


def _cap_pre(S, B, ret):
    j = S.j
    return f'第 0 行只能从左边来：`f[{j}] += f[{j-1}]` → ==前缀和== `{S.f[j]}`'


def _cap_col(S, B, ret):
    i = S.i
    return f'新的一行 `i = {i}`：第 0 列只能从上边来，`f[0]` 加上 `grid[{i}][0]` → =={S.f[0]}=='


def _cap_max(S, B, ret):
    i, j = S.i, S.j
    left, up = S.f[j - 1], B.f[j]
    return (f'`({i},{j})`：左边 `f[{j-1}] = {left}`（本行刚算好），上边 `f[{j}] = {up}`（上一行留下的）'
            f' → 取大的 `{max(left, up)}` 加格子 `{S.grid[i][j]}` = =={S.f[j]}==')


CONFIG = dict(
    num='LCR 166', title='珠宝的最高价值', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='网格 DP · 原地滚动（O(1) 空间）',
    code='''
class Solution:
    def jewelleryValue(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        f = grid[0]  # 这里没有拷贝，f 和 grid[0] 都持有同一段内存
        for j in range(1, n):
            f[j] += f[j - 1]
        for i in range(1, m):
            f[0] += grid[i][0]
            for j in range(1, n):
                f[j] = max(f[j - 1], f[j]) + grid[i][j]
        return f[-1]
''',
    call=f'Solution().jewelleryValue({G0})',
    expect=14,
    skip=['for j in range', 'for i in range'],
    views=[
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='grid', var='grid', label='grid（第 0 行 = f：粉 = 左，蓝 = 上；黄 = 要加的 grid[i][j]）', cell=84, h=300, color=_color),
        dict(type='array', var='f', label='f（和 grid[0] 是同一个列表）', cell=84, h=190,
             pointers={'j': 'orange'}),
    ],
    watch=[('i', lambda S: S['_inner'].get('i'), 'yellow'), ('j', lambda S: S['_inner'].get('j'), 'orange'),
           ('f[-1]', 'f[-1]', 'green')],
    captions={
        'm, n = len': '`m = {m}` 行、`n = {n}` 列',
        'f = grid[0]': '`f` 和 `grid[0]` ==是同一个列表==，没有拷贝 → 额外空间 `O(1)`',
        'f[j] += f[j - 1]': _cap_pre,
        'f[0] += grid': _cap_col,
        'f[j] = max': _cap_max,
        'return f[-1]': '`f[-1]` 是最后一列：右下角的最大价值和 =={ret}==',
    },
    cards=dict(
        one_liner='到 (i,j) 的最后一步，要么从左来，要么从上来，取大者',
        complexity='时间 `O(mn)`，空间 `O(1)`（原地改 `grid[0]`）',
        problem=['`frame[i][j]` 是珠宝价值，从左上角出发，==每次只能向右或向下==',
                 '走到右下角停止，求能拿到的最大价值和',
                 '示例：`[[1,3,1],[1,5,1],[4,2,1]]` → `12`',
                 '本视频：`[[1,3,1,2],[1,5,1,3],[4,2,1,1]]` → `14`'],
        quote='直接用 grid[0] 当作 f 数组，可以做到 O(1) 额外空间。……对比上下两份代码，你会发现长为 n+1 的数组写起来是更加简洁的，因为可以避免判断边界条件。',
        quote_src='—— 灵茶山艾府题解 · 空间优化方法三',
        idea=['递归：`dfs(i,j) = max(dfs(i,j-1), dfs(i-1,j)) + grid[i][j]`，出界为 0',
              '1:1 翻译成递推 `f[i][j]`；`f[i]` 只依赖上一行，可压成一维',
              '一维时 `f[j-1]` 是左（本行），旧 `f[j]` 是上（上一行）',
              '`i=0`、`j=0` 要单独算，因为没有开 `n+1` 的哨兵格'],
        result='运行结束，返回 `14`：右下角 `f[-1]` 就是最大价值和',
        after=[dict(heading='原文的几种写法', lines=[
            '递归：`O(2^(m+n))`，会超时',
            '`@cache` 记忆化：`O(mn)` 时间和空间',
            '1:1 翻译成 `(m+1)×(n+1)` 的 `f` 数组，`f[0][*]`、`f[*][0]` 当边界',
            '两个数组滚动 → 一个长 `n+1` 的数组 → 原地修改（本视频）',
        ])],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '易错：原地改 `grid[0]` 会破坏输入，`f[0]`、第 0 行要单独处理',
                 '长为 `n+1` 的数组写法更简洁：不用判断边界',
                 '珠宝价值都大于 0；有 0 或负数时记忆化的初值要改'],
    ),
)
