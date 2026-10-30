B5 = [[1, 3], [3, 2], [3, 3], [3, 5], [5, 3]]


def _gridv(S):
    n = S.get('n')
    if n is None:
        return None
    g = [[0] * n for _ in range(n)]
    for x, y in S['buildings']:
        g[x - 1][y - 1] = 1
    return g


def _col(S, i, j, v):
    if not v:
        return None
    x, y = i + 1, j + 1
    if 'ans' in S and S['_line'] >= 17:
        if S['row_min'][y] < x < S['row_max'][y] and S['col_min'][x] < y < S['col_max'][x]:
            return 'green'
    return None


CONFIG = dict(
    num=3531, title='统计被覆盖的建筑', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='记录每行每列的最小最大值',
    code='''
class Solution:
    def countCoveredBuildings(self, n: int, buildings: List[List[int]]) -> int:
        row_min = [n + 1] * (n + 1)
        row_max = [0] * (n + 1)
        col_min = [n + 1] * (n + 1)
        col_max = [0] * (n + 1)

        for x, y in buildings:
            # 手写 min max 更快
            if x < row_min[y]: row_min[y] = x
            if x > row_max[y]: row_max[y] = x
            if y < col_min[x]: col_min[x] = y
            if y > col_max[x]: col_max[x] = y

        ans = 0
        for x, y in buildings:
            if row_min[y] < x < row_max[y] and col_min[x] < y < col_max[x]:
                ans += 1
        return ans
''',
    call=f'Solution().countCoveredBuildings(5, {B5})',
    expect=1,
    skip=['row_max = [0]', 'col_max = [0]', 'ans = 0'],
    views=[
        dict(type='grid', var=_gridv, label='城市（行 = x，列 = y；1 = 建筑，绿 = 被覆盖）', cell=56, h=330,
             color=_col, rows=[1, 2, 3, 4, 5], cols=[1, 2, 3, 4, 5],
             cursors=[('x - 1', 'y - 1', 'yellow')]),
        dict(type='table', var=lambda S: [S['row_min'], S['row_max'], S['col_min'], S['col_max']] if 'col_max' in S else None,
             label='r小/r大 = row_min/row_max[y]，c小/c大 = col_min/col_max[x]（表头 = 下标）', cell=64, h=260,
             rows=['r小', 'r大', 'c小', 'c大'], cols=[0, 1, 2, 3, 4, 5]),
    ],
    watch=['x', 'y', ('ans', 'ans', 'green')],
    captions={
        'row_min = [n + 1]': '`row_min` 初值设成 `n + 1`，保证任何 x 都能把它压小',
        'col_min = [n + 1]': '`col_min` 同理，初值 `n + 1`',
        'for x, y in buildings': lambda S, B, r: ('遍历结束' if 'x' in B and (S.x, S.y) == (B.x, B.y) else f'看建筑 `({S.x}, {S.y})`'),
        'if x < row_min[y]': '`x = {x}` 比 `row_min[{y}] = {B.row_min[y]}` 小？{"是，更新最小值" if x < B.row_min[y] else "否，不变"}',
        'if x > row_max[y]': '`x = {x}` 比 `row_max[{y}] = {B.row_max[y]}` 大？{"是，更新最大值" if x > B.row_max[y] else "否，不变"}',
        'if y < col_min[x]': '`y = {y}` 比 `col_min[{x}] = {B.col_min[x]}` 小？{"是，更新最小值" if y < B.col_min[x] else "否，不变"}',
        'if y > col_max[x]': '`y = {y}` 比 `col_max[{x}] = {B.col_max[x]}` 大？{"是，更新最大值" if y > B.col_max[x] else "否，不变"}',
        'if row_min[y] < x < row_max[y]': lambda S, B, r: (
            f'`{S.row_min[S.y]} < {S.x} < {S.row_max[S.y]}` 且 `{S.col_min[S.x]} < {S.y} < {S.col_max[S.x]}`：'
            + ('==严格夹在中间，四个方向都有建筑==' if S.row_min[S.y] < S.x < S.row_max[S.y] and S.col_min[S.x] < S.y < S.col_max[S.x]
               else '等于端点说明某个方向没有建筑，不算')),
        'ans += 1': '被覆盖，`ans = {ans}`',
        'return ans': '共 `{ans}` 个被覆盖的建筑',
    },
    cards=dict(
        one_liner='记下每行每列的两端，严格在两端之间就是被覆盖',
        complexity='时间 `O(n+m)`，空间 `O(n)`',
        problem=['`n × n` 的城市里有一些建筑 `[x, y]`，坐标唯一',
                 '某建筑的上下左右四个方向都至少有一个建筑，就算被覆盖',
                 '示例：`n=5, [[1,3],[3,2],[3,3],[3,5],[5,3]]` → `1`'],
        quote='如果一个点不在同一行的最左边也不在最右边，那么这个点左右都有点；如果一个点不在同一列的最上边也不在最下边，那么这个点上下都有点。',
        quote_src='—— 灵茶山艾府题解',
        idea=['同一行的最左、最右点，一边没有邻居；其余点两边都有',
              '第一遍扫描：记录每行、每列的最小和最大坐标',
              '第二遍扫描：坐标==严格==夹在最小最大值之间才计数'],
        summary=['时间 `O(n+m)`，空间 `O(n)`，`m` 为建筑数',
                 '易错：必须是严格不等号，等于端点说明那一侧没有建筑',
                 '数组初值 `n+1` / `0` 要在范围外，才能被首个建筑更新',
                 '代码里手写 `if` 代替 `min/max`，常数更小'],
    ),
)
