def _fk(S, name):
    f = S.get('f')
    if f is None:
        return None
    k = S.get('now')
    if name == 'now':
        return f[k] if k is not None else f[1]
    return f[S['last']] if 'last' in S else None


def _cur(S):
    inner = S.get('_inner', {})
    return ('i' in inner and 'j' in inner and S.get('_line', 0) >= 20)


def _txt(S):
    if 'f' not in S:
        return ''
    if 'now' not in S:
        return '`f[1][i][j]`：走 1 步就出界的方案数（边上的格子贴边每一面算 1）'
    k = S['k']
    return f"第 `k = {k}` 步：`f[{k % 2}]` 由 `f[{1 - k % 2}]` 的四个邻居相加；目标格 ({S['x']},{S['y']}) 累计 `res = {S['res']}`"


CONFIG = dict(
    num=576, title='出界的路劲数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='f[k][x][y] 恰好第 k 步出界 · 01 滚动数组',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def findPaths(self, m, n, N, i, j):

        if N == 0:
            return 0

        x = i
        y = j
        f = [[[0] * n for _ in range(m)] for _ in range(2)]

        for i in range(m):
            f[1][i][0] += 1
            f[1][i][n - 1] += 1
        for j in range(n):
            f[1][0][j] += 1
            f[1][m - 1][j] += 1

        res = f[1][x][y]
        mod = 10 ** 9 + 7
        for k in range(2, N + 1):
            now = k % 2
            last = 1 - now
            for i in range(m):
                for j in range(n):
                    f[now][i][j] = 0
                    if i > 0:
                        f[now][i][j] += f[last][i - 1][j]
                    if i < m - 1:
                        f[now][i][j] += f[last][i + 1][j]
                    if j > 0:
                        f[now][i][j] += f[last][i][j - 1]
                    if j < n - 1:
                        f[now][i][j] += f[last][i][j + 1]
                    f[now][i][j] %= mod
            res += f[now][x][y]
            res %= mod
        return res
''',
    call='Solution().findPaths(2, 2, 2, 0, 0)',
    expect=6,
    views=[
        dict(type='table', var=lambda S: _fk(S, 'now'), label='本轮 f[now]（恰好第 k 步出界的方案数；蓝框 = 正在算的格子；开头是 f[1]）',
             cell=130, h=210,
             cursors=[(lambda S: S['_inner']['i'] if _cur(S) else None, lambda S: S['_inner']['j'] if _cur(S) else None, 'blue')],
             color=lambda S, i, j, v: 'green' if 'x' in S and (i, j) == (S['x'], S['y']) else None),
        dict(type='table', var=lambda S: _fk(S, 'last'), label='f[last]（上一轮，只读）', cell=130, h=210,
             color=lambda S, i, j, v: 'green' if 'x' in S and (i, j) == (S['x'], S['y']) else None),
        dict(type='text', h=90, size=28, fn=_txt),
    ],
    watch=[('k', 'k', 'blue'), 'now', 'last', ('x,y', '(x, y)', 'green'), ('res', 'res', 'green')],
    captions={
        'if N == 0': '`N = {N}`：一步都不能走，不可能出界 → 先判掉 `N == 0` 返回 0',
        'x = i': '先把起点存进 `x, y`：后面循环会复用 `i, j` 当遍历变量',
        'f = [[[0]': '`f[k % 2]` 两层滚动：`f[k][x][y]` = ==前 k−1 步都在界内、第 k 步才出界==的方案数',
        'f[1][i][0] += 1': '第 `{i}` 行最左格：往左一步就出界，`f[1][{i}][0]` 加 1',
        'f[1][i][n - 1] += 1': '第 `{i}` 行最右格：往右一步出界，`f[1][{i}][{n-1}]` 加 1',
        'f[1][0][j] += 1': '第 0 行第 `{j}` 格：往上一步出界，加 1',
        'f[1][m - 1][j] += 1': '最下行第 `{j}` 格：往下一步出界，加 1',
        'res = f[1][x][y]': '走 1 步出界的方案数 `f[1][{x}][{y}] = {res}`：先计入答案（题目不要求用完所有步数）',
        'for k in range(2, N + 1)': lambda S, B, r: (f'枚举步数 `k = {S.k}`：每一轮的状态只依赖上一轮' if 'k' not in B else f'`k` 已经走完 2…{S.N}，所有步数都累加过了'),
        'now = k % 2': '本轮写 `f[{now}]`，上一轮读 `f[{1 - now}]`（01 滚动数组）',
        'f[now][i][j] = 0': '先清零 `f[{now}][{i}][{j}]`：它里面还是两轮前的旧值',
        'if i > 0': lambda S, B, r: f'`i = {S.i} > 0`：上方有格子 → 从上方走来，加 `f[last][{S.i-1}][{S.j}]`' if S.i > 0 else '`i = 0`：上面已是边界，往上一步就出界，已在上一轮统计过，不加',
        'if i < m - 1': lambda S, B, r: f'`i = {S.i} < m−1`：下方有格子，加 `f[last][{S.i+1}][{S.j}]`' if S.i < S.m - 1 else '`i` 在最下行：没有下邻居，不加',
        'if j > 0': lambda S, B, r: f'`j = {S.j} > 0`：左边有格子，加 `f[last][{S.i}][{S.j-1}]`' if S.j > 0 else '`j = 0`：没有左邻居，不加',
        'if j < n - 1': lambda S, B, r: f'`j = {S.j} < n−1`：右边有格子，加 `f[last][{S.i}][{S.j+1}]`' if S.j < S.n - 1 else '`j` 在最右列：没有右邻居，不加',
        'f[now][i][j] %= mod': '`f[{now}][{i}][{j}] = {f[now][i][j]}`，取模防止溢出',
        'res += f[now][x][y]': '把本轮起点 `({x},{y})` 的 `{f[now][x][y]}` 累加进答案：`res = {res}`',
        'res %= mod': '`res` 取模 → {res}',
        'return res': '所有步数累加完毕，返回 `{res}`',
    },
    cards=dict(
        one_liner='f[k][x][y]：前 k−1 步在界内、第 k 步才出界，逐轮累加',
        complexity='时间 `O(N·m·n)`，空间 `O(m·n)`',
        problem=['`m × n` 网格，球从 `(i, j)` 出发，每步上下左右移一格',
                 '最多移动 `N` 次，求把球移出边界的路径数（对 `10^9+7` 取模）',
                 '示例：`m=2, n=2, N=2, 起点 (0,0)` → `6`',
                 '另一例：`m=1, n=3, N=3, 起点 (0,1)` → `12`'],
        quote='f[k][x][y]表示从x行y列开始，移动k次之后移除界的操作总数。这个状态表示意味着对于f[k][x][y]，其前k - 1步操作都必须保证球在界内，而最后一步操作时才将球移出界外',
        quote_src='—— yiduobo 题解原文',
        idea=['“恰好第 k 步出界”保证不重复；所以每个 `k` 的结果都要累加进答案',
              '`f[k]` 每个格子 = 上下左右四个邻居的 `f[k-1]` 之和（邻居必须在界内）',
              '只依赖上一轮，用 `k % 2` 两层数组滚动'],
        summary=['时间 `O(N·m·n)`，空间 `O(m·n)`',
                 '易错：`i, j` 被循环变量覆盖，所以先存起点 `x, y`',
                 '易错：不是只算第 N 步，要把每轮 `f[now][x][y]` 都加到答案',
                 '每轮都要先清零 `f[now][i][j]`，再累加四个方向',
                 '原文已是 Python 3 可运行写法，代码未改'],
    ),
)
