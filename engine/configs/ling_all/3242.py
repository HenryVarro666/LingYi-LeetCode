CONFIG = dict(
    num=3242, title='设计相邻元素求和服务', difficulty='Easy', category='设计',
    author='灵茶山艾府', technique='初始化时预处理 8 个方向',
    tags=[],
    code='''
DIRS = ((-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (-1, 1), (-1, -1), (1, -1))

class NeighborSum:
    def __init__(self, grid: List[List[int]]):
        n = len(grid)
        s = [[0, 0] for _ in range(n * n)]
        for i, row in enumerate(grid):
            for j, v in enumerate(row):
                for k, (dx, dy) in enumerate(DIRS):
                    x, y = i + dx, j + dy
                    if 0 <= x < n and 0 <= y < n:
                        s[v][k // 4] += grid[x][y]
        self.s = s

    def adjacentSum(self, value: int) -> int:
        return self.s[value][0]

    def diagonalSum(self, value: int) -> int:
        return self.s[value][1]
''',
    call='''ns = NeighborSum([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
[ns.adjacentSum(1), ns.adjacentSum(4), ns.diagonalSum(4), ns.diagonalSum(8)]''',
    expect=[6, 16, 16, 4],
    views=[
        dict(type='text', h=70, fn=lambda S: ("`s[v][0]` = 上下左右之和，`s[v][1]` = 四个斜角之和" if 'k' not in S else
            f"元素 =={S.get('v')}==，第 `{S['k']}` 个方向（`k // 4` = {S['k'] // 4}）→ 累加到 `s[{S.get('v')}][{S['k'] // 4}]`")),
        dict(type='grid', var='grid', cursors=[('i', 'j', 'yellow', '(i,j)'), ('x', 'y', 'cyan', '')], h=300),
        dict(type='table', var='s', rows=lambda S: list(range(len(S['s']))), cols=['adj', 'diag'], h=420),
    ],
    watch=['i', 'j', 'v', 'k', 'x', 'y', ('value', 'value', 'green')],
    captions={
        's = [[0, 0]': '`s[v] = [相邻和, 对角和]`，每个元素值 `v` 一行，先全部清零',
        'for k, (dx, dy)': '`k = {k}`：方向 `({dx}, {dy})`，`k < 4` 是上下左右，`k >= 4` 是斜向',
        'if 0 <= x < n': lambda S, B, r: (f'邻居 `({S.x}, {S.y})` 在网格内 → 可以累加' if 0 <= S.x < S.n and 0 <= S.y < S.n
                                          else f'邻居 `({S.x}, {S.y})` 越界 → 跳过，必须判断边界'),
        's[v][k // 4] += ': '`k // 4` = {k // 4}：把邻居 `{grid[x][y]}` 累加到 `s[{v}][{k // 4}]` → =={s[v][k // 4]}==',
        'self.s = s': '预处理完毕：以后每次查询都只是查表',
        'return self.s[value][0]': '`adjacentSum({value})` 直接读表 = =={ret}==，==O(1)==',
        'return self.s[value][1]': '`diagonalSum({value})` 直接读表 = =={ret}==，==O(1)==',
    },
    skip=['x, y = i + dx'],
    max_steps=50,
    cards=dict(
        one_liner='初始化时把每个元素的两种邻居和都算好，查询 O(1)',
        complexity='初始化 `O(n²)`，查询 `O(1)`，空间 `O(n²)`',
        problem=['`n × n` 网格，元素互不相同，范围 `[0, n²-1]`',
                 '`adjacentSum(v)`：上下左右邻居之和；`diagonalSum(v)`：四个斜角邻居之和',
                 '示例：`[[0,1,2],[3,4,5],[6,7,8]]`，`adjacentSum(4) = 16`'],
        quote='用一个大小为 n²×2 的数组 s 预处理元素和，其中 s[v][0] 为 adjacentSum(v) 的结果，s[v][1] 为 diagonalSum(v) 的结果。',
        quote_src='—— 灵茶山艾府题解',
        idea=['8 个偏移向量放一个数组，前 4 个是上下左右，后 4 个是斜向',
              '元素值互不相同、范围正好是 `0..n²-1`，所以可以直接拿值当下标，不用哈希表',
              '用 `k // 4` 区分写入哪一列：0 或 1'],
        summary=['初始化 `O(n²)`，查询 `O(1)`，空间 `O(n²)`',
                 '易错点：邻居要判断 `0 <= x < n and 0 <= y < n`；`s` 按元素值 `v` 索引，不是按坐标',
                 '题解注：也可以在 grid 外面加一圈 0，就不用判断越界'],
    ),
)
