CONFIG = dict(
    num=1605, title='给定行和列的和求可行矩阵', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='贪心构造 · 左上角出发去掉行或列',
    tags=['贪心算法', '构造题', '难度分 1868'],
    code='''
class Solution:
    def restoreMatrix(self, rowSum: List[int], colSum: List[int]) -> List[List[int]]:
        m, n = len(rowSum), len(colSum)
        mat = [[0] * n for _ in range(m)]
        i = j = 0  # 从左上角出发
        while i < m and j < n:
            rs, cs = rowSum[i], colSum[j]
            if rs < cs:
                mat[i][j] = rs  # 去掉第 i 行
                colSum[j] -= rs
                i += 1  # 往下走
            else:
                mat[i][j] = cs  # 去掉第 j 列
                rowSum[i] -= cs
                j += 1  # 往右走
        return mat
''',
    call='Solution().restoreMatrix([5,7,10], [8,6,8])',
    expect=[[5, 0, 0], [3, 4, 0], [0, 2, 8]],
    views=[
        dict(type='array', var='rowSum', h=150, label='rowSum（还需要的行和）', pointers={'i': 'blue'}, cell=70,
             dim=lambda S, k, v: k < S.get('i', 0)),
        dict(type='array', var='colSum', h=150, label='colSum（还需要的列和）', pointers={'j': 'pink'}, cell=70,
             dim=lambda S, k, v: k < S.get('j', 0)),
        dict(type='grid', var='mat', h=300, label='mat（蓝框 = 当前位置 (i, j)）', cell=90,
             cursors=[('i if i < m and j < n else None', 'j', 'blue')],
             color=lambda S, i, j, v: 'green' if v else None),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'rs', 'cs'],
    skip=['m, n = len', 'mat = [[0]'],
    max_steps=60,
    captions={
        'i = j = 0': '从左上角 `(0, 0)` 出发：每一步==要么去掉一行，要么去掉一列==',
        'while i < m and j < n': lambda S, B, r: (f'`i = {B.i} < {B.m}` 且 `j = {B.j} < {B.n}`，还有行列没填完' if B.i < B.m and B.j < B.n
                                                  else '行或列走完了，矩阵构造完毕'),
        'rs, cs = rowSum[i], colSum[j]': '这一行还需要 `rs = {rs}`，这一列还需要 `cs = {cs}`',
        'if rs < cs': lambda S, B, r: (f'`rs = {S.rs} < cs = {S.cs}`：行先被填满 → 这格填 `rs`，第 {S.i} 行去掉' if S.rs < S.cs
                                       else f'`rs = {S.rs} ≥ cs = {S.cs}`：列先被填满（或同时）→ 这格填 `cs`，第 {S.j} 列去掉'),
        'mat[i][j] = rs': '`mat[{i}][{j}] = rs = {rs}`：行的需求全部满足，不会超过列的需求',
        'colSum[j] -= rs': '第 {j} 列还剩 `colSum[{j}] = {colSum[j]}` 要后面的行来填',
        'i += 1': '第 {B.i} 行填完了，往下走：`i` → {i}',
        'mat[i][j] = cs': '`mat[{i}][{j}] = cs = {cs}`：列的需求全部满足，不会超过行的需求',
        'rowSum[i] -= cs': '第 {i} 行还剩 `rowSum[{i}] = {rowSum[i]}` 要后面的列来填',
        'j += 1': '第 {B.j} 列填完了，往右走：`j` → {j}',
        'return mat': '行和列都用完了，返回 `mat`',
    },
    cards=dict(
        one_liner='从左上角出发，每次填 min(行需求, 列需求)，去掉满足的行或列',
        complexity='时间 `O(m+n)`（不计建矩阵），空间 `O(1)`',
        problem=['已知每行的和 `rowSum`、每列的和 `colSum`，构造任意一个非负整数矩阵',
                 '题目保证 `sum(rowSum) == sum(colSum)`，至少有一个解',
                 '本视频：`rowSum=[5,7,10]`，`colSum=[8,6,8]`',
                 '→ `[[5,0,0],[3,4,0],[0,2,8]]`'],
        quote='也可以这样理解：从左上角出发，每次要么去掉一行，要么去掉一列。同样根据数学归纳法，可以证明该做法的正确性。',
        quote_src='—— 灵茶山艾府题解',
        idea=['这格填 `min(rs, cs)`：填满的那一行（或列）就此去掉，剩下是更小的子问题',
              '行去掉 → `i` 下移；列去掉 → `j` 右移；总和相等，归纳可证一定能走到终点',
              '灵神还给了更直观的写法：双重循环，每格填 `min(rs, cs)` 并扣掉，思路相同'],
        summary=['时间 `O(m+n)`（不算创建 `m×n` 矩阵），空间 `O(1)`',
                 '易错：`rs < cs` 去掉行；否则（含相等）去掉列，只能二选一',
                 '`rowSum`、`colSum` 被原地修改，当作「剩余需求」使用',
                 '正确性：每步不超需求，且总和相等，数学归纳'],
    ),
)
