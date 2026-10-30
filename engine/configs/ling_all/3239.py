def _pair(S, i, j, v):
    g = S['grid']
    m, n = len(g), len(g[0])
    if 'col' in S and 'i' in S:
        k = next((k for k in range(n) if tuple(r[k] for r in g) == tuple(S['col'])), None)
        if j == k and i in (S['i'], m - 1 - S['i']):
            return 'pink'
    elif 'row' in S and 'j' in S:
        r = next((r for r, row in enumerate(g) if row is S['row']), None)
        if i == r and j in (S['j'], n - 1 - S['j']):
            return 'blue'
    return None


CONFIG = dict(
    num=3239, title='最少翻转次数使二进制矩阵回文 I', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='行列分别统计 · 取最小',
    code='''
class Solution:
    def minFlips(self, grid: List[List[int]]) -> int:
        diff_row = 0
        for row in grid:
            for j in range(len(row) // 2):
                if row[j] != row[-1 - j]:
                    diff_row += 1

        diff_col = 0
        for col in zip(*grid):
            for i in range(len(grid) // 2):
                if col[i] != col[-1 - i]:
                    diff_col += 1

        return min(diff_row, diff_col)
''',
    call='Solution().minFlips([[1,0,0,0],[0,1,0,1],[1,0,1,0]])',
    expect=1,
    views=[
        dict(type='grid', var='grid', h=330, cell=70, color=_pair),
        dict(type='text', size=30, h=100,
             fn=lambda S: f"行方向要翻 `diff_row = {S.get('diff_row', 0)}`" + (f"，列方向要翻 `diff_col = {S['diff_col']}`" if 'diff_col' in S else '')),
    ],
    watch=[('diff_row', 'diff_row', 'blue'), ('diff_col', 'diff_col', 'pink'), ('j', 'j', 'cyan'), ('i', 'i', 'orange')],
    captions={
        'diff_row = 0': '`diff_row`：把==所有行==变成回文需要的翻转数',
        'for row in grid': '检查这一行 `row = {row}`',
        'for j in range(len(row) // 2)': '只需比较前一半：`j = {j}` 对应对称位置 `-1-j`',
        'if row[j] != row[-1 - j]': '`row[{j}] = {row[j]}`，`row[{-1 - j}] = {row[-1 - j]}` → {"不同，要翻一个" if row[j] != row[-1 - j] else "相同，不用翻"}',
        'diff_row += 1': '这一对不同，翻转其中一个即可 → `diff_row = {diff_row}`',
        'diff_col = 0': '行算完了：`diff_row = {diff_row}`。接着同样算==所有列==，`diff_col` 从 0 开始',
        'for col in zip(*grid)': '`zip(*grid)` 把列转成元组，这一列 `col = {col}`',
        'for i in range(len(grid) // 2)': '只比较上半部分：`i = {i}` 对应对称位置 `-1-i`',
        'if col[i] != col[-1 - i]': '`col[{i}] = {col[i]}`，`col[{-1 - i}] = {col[-1 - i]}` → {"不同，要翻一个" if col[i] != col[-1 - i] else "相同，不用翻"}',
        'diff_col += 1': '这一对不同，翻转其中一个 → `diff_col = {diff_col}`',
        'return min': '要么全行回文（`{diff_row}` 次），要么全列回文（`{diff_col}` 次），取小 → ==`{ret}`==',
    },
    cards=dict(
        one_liner='行回文和列回文分开算，取代价小的',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['二进制矩阵，可翻转任意格子（0 变 1 或 1 变 0）',
                 '要使==所有行都是回文==，或==所有列都是回文==，求最少翻转次数',
                 '本视频：`3×4` 矩阵 → `1`（翻转一列内的一格）'],
        quote='先计算所有行变成回文最少需要翻转多少次。也就是对于每一行 row，计算这一行变成回文最少需要翻转多少次。',
        quote_src='—— 灵茶山艾府题解',
        idea=['一行变回文：对称位置 `row[j]` 与 `row[n-1-j]` 不同就要翻一次',
              '各行互不影响，把所有行的不同对数累加',
              '列同理（用 `zip(*grid)` 取列），两种情况取最小'],
        summary=['时间 `O(mn)`，空间 `O(1)`（忽略 `zip` 的开销）',
                 '易错：只比较前一半，中间那个格子不用管',
                 '每对不同的位置只翻一个格子，代价为 1',
                 '要么全行要么全列，不能混合，所以是 `min`'],
    ),
)
