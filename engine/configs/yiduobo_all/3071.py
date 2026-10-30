def _inY(i, j, n):
    if i <= n // 2:
        return i == j or i == n - 1 - j
    return j == n // 2


CONFIG = dict(
    num=3071, title='在矩阵上写出字母 Y 所需的最少操作次数', difficulty='Medium', category='模拟',
    author='yiduobo', technique='统计 Y 内外频次 + 枚举两种数字', tags=[],
    code='''
class Solution(object):
    def minimumOperationsToWriteY(self, grid):

        freq_y = [0] * 3
        freq_other = [0] * 3

        n = len(grid)
        for i in range(n):
            for j in range(n):
                if i <= n // 2:
                    if i == j or i == n - 1 - j:
                        freq_y[grid[i][j]] += 1
                    else:
                        freq_other[grid[i][j]] += 1
                else:
                    if j == n // 2:
                        freq_y[grid[i][j]] += 1
                    else:
                        freq_other[grid[i][j]] += 1
        
        res = n * n
        y_size = n + n // 2
        for y in range(3):
            for other in range(3):
                if y == other:
                    continue
                res = min(res, y_size - freq_y[y] + n * n - y_size - freq_other[other])
        
        return res
''',
    call='Solution().minimumOperationsToWriteY([[1,2,2],[1,1,0],[0,1,0]])',
    expect=3,
    max_steps=90,
    views=[
        dict(type='grid', var='grid', h=330, cell=70, label='grid（蓝 = 属于 Y，黄框 = 当前格）',
             cursors=[('i', 'j', 'yellow', '(i,j)')],
             color=lambda S, i, j, v: 'blue' if _inY(i, j, len(S['grid'])) else None),
        dict(type='array', var='freq_y', h=150, label='freq_y：Y 上各数字出现次数', cell=70),
        dict(type='array', var='freq_other', h=150, label='freq_other：其他位置各数字出现次数', cell=70),
    ],
    watch=['i', 'j', 'y', 'other', ('res', 'res', 'green')],
    captions={
        'freq_y = [0]': '`freq_y[v]`：数字 `v` 在 Y 上出现几次',
        'freq_other = [0]': '`freq_other[v]`：数字 `v` 在其他位置出现几次',
        'n = len': '`n = {n}`',
        'for i in range(n)': '逐行扫描：第 `{i}` 行',
        'for j in range(n)': '看格子 `({i}, {j})`，数字 `{grid[i][j]}`',
        'if i <= n // 2': '`i = {i}` {"<= n//2：上半部分，Y 是两条对角线" if i <= n // 2 else "> n//2：下半部分，Y 只剩中间竖线"}',
        'if i == j or': '`i == j`（左对角线）或 `i == n-1-j`（右对角线）？{"==是，在 Y 上==" if (i == j or i == n - 1 - j) else "否，不在 Y 上"}',
        'if j == n // 2': '是中间竖线（`j == {n//2}`）吗？{"==是，在 Y 上==" if j == n // 2 else "否，不在 Y 上"}',
        'freq_y[grid[i][j]] += 1': '数字 `{grid[i][j]}` 在 Y 上 → `freq_y = {freq_y}`',
        'freq_other[grid[i][j]] += 1': '数字 `{grid[i][j]}` 在 Y 外 → `freq_other = {freq_other}`',
        'res = n * n': '`res` 初值取最坏情况：所有格子都改，`{n*n}`',
        'y_size = ': 'Y 的格子数 = 上半部分 `n` 个（V 形，每列一个）+ 下半竖线 `n//2` 个 = ==`{y_size}`==',
        'for y in range(3)': '枚举 Y 最终写成数字 `y = {y}`',
        'for other in range(3)': '枚举其他位置最终写成 `other = {other}`',
        'if y == other': '`y = {y}`，`other = {other}`：{"==相同，不允许，跳过==" if y == other else "不同，可行"}',
        'continue': 'Y 内外必须不同，换下一种',
        'res = min': 'Y 要改 `{y_size} − {freq_y[y]}` 个，其他要改 `{n*n-y_size} − {freq_other[other]}` 个，合计 {y_size - freq_y[y] + n*n - y_size - freq_other[other]} → `res = {res}`',
        'return res': '最少操作次数 `{res}`',
    },
    cards=dict(
        one_liner='枚举 Y 和其他位置各写什么数字，缺多少改多少',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['`n x n` 矩阵（`n` 为奇数），值为 0/1/2；Y 由两条对角线和中间竖线组成',
                 '要求 Y 内值全相同、Y 外值全相同，且两者不同；每次操作改一格',
                 '示例：`[[1,2,2],[1,1,0],[0,1,0]]` → `3`'],
        quote='一趟遍历，统计每种数字在Y上出现的次数以及在其他位置上出现的次数，接下来只需枚举最终构造的Y上的数字以及其他位置上的数字，然后分别计算填充Y和其他位置需要多少次操作即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['上半部分 `i <= n//2`：两条对角线；下半部分：中间竖线 `j == n//2`',
              'Y 的格子数 `y_size = n + n//2`，其余是 `n*n - y_size`',
              '某区域写成数字 `d` 的操作数 = 区域格数 − 该区域里 `d` 的个数'],
        summary=['时间 `O(n^2)`，空间 `O(1)`',
                 '`y_size = n + n//2`：V 形每列一个共 `n`，竖线下半 `n//2`',
                 '易错：`y == other` 必须跳过',
                 '原文为 Python 2 风格，其中 `n // 2` 本就是整数除法，代码未改动'],
    ),
)
