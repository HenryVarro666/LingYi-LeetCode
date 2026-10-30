GRID = [[4, 3, 8, 4, 1], [9, 5, 1, 9, 5], [2, 7, 6, 5, 7], [3, 5, 1, 2, 6]]


def _ctr(S):
    """center of the window being examined"""
    if 'x' in S and 'y' in S:
        return S['x'], S['y']
    if 'i' in S and 'j' in S and 'res' in S:
        return S['i'], S['j']
    return None


def _color(S, a, b, v):
    c = _ctr(S)
    if c is None:
        return None
    x, y = c
    if (a, b) == (x, y):
        return 'yellow'
    if 'x' in S and 'nums' in S and (a, b) == (S.get('i'), S.get('j')):
        return 'orange'
    if abs(a - x) <= 1 and abs(b - y) <= 1:
        return 'blue'
    return None


CONFIG = dict(
    num=840, title='矩阵中的幻方', difficulty='Medium', category='网格图',
    author='yiduobo', technique='枚举中心 5 + 逐个检查',
    code='''
class Solution(object):
    def numMagicSquaresInside(self, grid):

        m = len(grid)
        n = len(grid[0])
        res = 0

        for i in range(1, m - 1):
            for j in range(1, n - 1):
                if grid[i][j] == 5:
                    res += self.check(grid, i, j)
        
        return res

    def check(self, grid, x, y):
        nums = set(range(1, 10))
        row = [0] * 3
        col = [0] * 3
        left = right = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if grid[i][j] not in nums:
                    return 0
                nums.remove(grid[i][j])
                
                row[i - x + 1] += grid[i][j]
                col[j - y + 1] += grid[i][j]
                if i + j == x + y:
                    left += grid[i][j]
                if i - j == x - y:
                    right += grid[i][j]
        
        if left != 15 or right != 15:
            return 0
        if row[0] != 15 or row[1] != 15 or row[2] != 15:
            return 0
        if col[0] != 15 or col[1] != 15 or col[2] != 15:
            return 0

        return 1
''',
    call=f'Solution().numMagicSquaresInside({GRID})',
    expect=1,
    skip=['row[i - x + 1]', 'col[j - y + 1]', 'if i + j == x + y', 'if i - j == x - y', 'left += grid', 'right += grid',
          'for j in range(y - 1', 'left = right = 0', 'row = [0]', 'col = [0]'],
    views=[
        dict(type='grid', var='grid', label='grid（蓝框 = 以黄色中心为核心的 3×3，橙 = 正在检查的格子）', cell=96, h=380, color=_color,
             cursors=[(lambda S: (_ctr(S) or (-1, -1))[0], lambda S: (_ctr(S) or (-1, -1))[1], 'yellow')]),
        dict(type='text', size=24, h=60, fn=lambda S: (f"`nums` 还剩：`{sorted(S['nums'])}`" if 'nums' in S and 'x' in S else '')),
        dict(type='text', size=24, h=60, fn=lambda S: (f"`row = {S['row']}`　`col = {S['col']}`　`left = {S['left']}`　`right = {S['right']}`" if 'row' in S and 'left' in S else '')),
    ],
    watch=['res', ('x', 'x', 'yellow'), ('y', 'y', 'yellow'), ('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'm = len': '`m = {m}` 行',
        'n = len': '`n = {n}` 列',
        'res = 0': '`res` 统计幻方个数',
        'for i in range(1': lambda S, B, r: ('所有中心都枚举完了' if B.get('i') == S.i and 'res' in B else f'枚举中心的行 `i = {S.i}`（边缘一圈不可能是中心）'),
        'for j in range(1': lambda S, B, r: ('这一行的中心都看完了' if B.get('j') == S.j and B.get('i') == S.i else f'中心 `({S.i}, {S.j})`，值 `{S.grid[S.i][S.j]}`'),
        'if grid[i][j] == 5': lambda S, B, r: (f'中心 `{S.grid[S.i][S.j]}` ==是 5==：幻方的中心必为 5，进去检查' if S.grid[S.i][S.j] == 5
                                              else f'中心 `{S.grid[S.i][S.j]}` ≠ 5 → 不可能是幻方，跳过'),
        'res += self.check': lambda S, B, r: (f'`check` 返回 `{r}`：' + ('==这个 3×3 是幻方==' if r else '不是幻方') + f'，`res = {S.res}`' if r is not None else '调用 `check(grid, i, j)`，检查这个 3×3'),
        'nums = set': '`nums = {{1..9}}`：每用掉一个数就删掉一个，用来保证 1~9 恰好各一次',
        'for i in range(x - 1': lambda S, B, r: ('9 个格子都检查完了' if B.get('i') == S.i and 'nums' in B and S.i == S.x + 1 and B.get('j') == S.y + 1 else f'检查第 `{S.i}` 行'),
        'if grid[i][j] not in nums': lambda S, B, r: (f'`grid[{S.i}][{S.j}] = {S.grid[S.i][S.j]}` ' + ('不在 `nums` 里：要么超出 1~9，要么重复了 → ==直接返回 0，不是幻方==' if S.grid[S.i][S.j] not in S.nums else '在 `nums` 里，还没用过')),
        'nums.remove': '用掉 `{grid[i][j]}`，从 `nums` 删除；还剩 `{len(nums)}` 个',
        'if left != 15': lambda S, B, r: f'两条对角线：`left = {S.left}`，`right = {S.right}`' + (' → 都是 15' if S.left == 15 and S.right == 15 else ' → 有不是 15 的，返回 0'),
        'if row[0] != 15': lambda S, B, r: f'三行之和 `{S.row}`' + (' → 都是 15' if S.row == [15, 15, 15] else ' → 有不是 15 的，返回 0'),
        'if col[0] != 15': lambda S, B, r: f'三列之和 `{S.col}`' + (' → 都是 15' if S.col == [15, 15, 15] else ' → 有不是 15 的，返回 0'),
        'return 1': '数字恰好 1~9，行、列、两条对角线之和都是 15 → 返回 `1`，调用处 `res += 1`',
        'return res': '共 `{ret}` 个幻方',
    },
    cards=dict(
        one_liner='矩阵很小：枚举每个中心，只检查值为 5 的，逐格验证',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`3×3` 幻方：填入 `1~9` 各一次，每行、每列、两条对角线之和都相等',
                 '数一数 `grid` 里有多少个 `3×3` 子矩阵是幻方',
                 '本视频：`4×5` 的 `grid` → `1`'],
        quote='由于幻方的中心必然为5，因此可以从第1行第1列开始枚举所有值等于5的位置，然后进行下列检测。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举中心 `(i, j)`，从 `1` 到 `m-2` / `n-2`，保证 3×3 不越界',
              '检测一：用集合 `nums` 判断是否恰好用了 1~9',
              '检测二：行、列之和直接累加；对角线用 `i + j == x + y`、`i - j == x - y` 判别'],
        summary=['时间 `O(mn)`，空间 `O(1)`：每个窗口最多检查 9 个格子',
                 '易错：枚举下标要从 `1` 到 `m-2`，因为 `i` 是中心不是左上角',
                 '`grid` 里可能有 0 或 >9 的数，靠 `not in nums` 一并排除',
                 '对角线：`i + j` 相同的是副对角线，`i - j` 相同的是主对角线',
                 '对比灵神：灵神用位掩码一次判 1~9，并证明只需验前两行前两列；这里逐项全验',
                 '原文已是 Python 3 可运行写法，代码无需改动'],
    ),
)
