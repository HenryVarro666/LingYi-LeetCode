B5 = [[1, 3], [3, 2], [3, 3], [3, 5], [5, 3]]


def _gridv(S):
    g = [[0] * 5 for _ in range(5)]
    for x, y in S['buildings']:
        g[x - 1][y - 1] = 1
    return g


def _col(S, i, j, v):
    if not v:
        return None
    x, y = i + 1, j + 1
    if 'res' in S and 'col' in S and S['_line'] >= 22:
        r, c = S['row'], S['col']
        if x != c[y][0] and x != c[y][1] and y != r[x][0] and y != r[x][1]:
            return 'green'
    return None


CONFIG = dict(
    num=3531, title='统计被覆盖的建筑', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表记录每行每列端点',
    code='''
class Solution(object):
    def countCoveredBuildings(self, n, buildings):
        
        row = {}
        col = {}

        for x, y in buildings:
            if x not in row:
                row[x] = [y, y]
            else:
                row[x][0] = min(row[x][0], y)
                row[x][1] = max(row[x][1], y)
            
            if y not in col:
                col[y] = [x, x]
            else:
                col[y][0] = min(col[y][0], x)
                col[y][1] = max(col[y][1], x)
        
        res = 0
        for x, y in buildings:
            if x != col[y][0] and x != col[y][1] and y != row[x][0] and y != row[x][1]:
                res += 1
        return res
''',
    call=f'Solution().countCoveredBuildings(5, {B5})',
    expect=1,
    skip=['row = {}', 'col = {}', 'res = 0'],
    views=[
        dict(type='grid', var=_gridv, label='城市（行 = x，列 = y；1 = 建筑，绿 = 被覆盖）', cell=60, h=340,
             color=_col, rows=[1, 2, 3, 4, 5], cols=[1, 2, 3, 4, 5], cursors=[('x - 1', 'y - 1', 'yellow')]),
        dict(type='map', var='row', label='row：x → [最小 y, 最大 y]', fmt=lambda k, v: f'{k}: {v}', h=150, font=26),
        dict(type='map', var='col', label='col：y → [最小 x, 最大 x]', fmt=lambda k, v: f'{k}: {v}', h=150, font=26),
    ],
    watch=['x', 'y', ('res', 'res', 'green')],
    captions={
        'for x, y in buildings': lambda S, B, r: ('遍历结束' if 'x' in B and (S.x, S.y) == (B.x, B.y) else f'看建筑 `({S.x}, {S.y})`'),
        'if x not in row': lambda S, B, r: (f'`row` 里还没有 `x = {S.x}` → 新建 `[y, y]`' if S.x not in B.row else f'`row` 里已有 `x = {S.x}` → 更新这一行的端点'),
        'row[x] = [y, y]': '这一行第一次出现，最小和最大 y 都是 `{y}`',
        'row[x][0] = min': '最小 y：`row[{x}][0] = {row[x][0]}`',
        'row[x][1] = max': '最大 y：`row[{x}][1] = {row[x][1]}`',
        'if y not in col': lambda S, B, r: (f'`col` 里还没有 `y = {S.y}` → 新建 `[x, x]`' if S.y not in B.col else f'`col` 里已有 `y = {S.y}` → 更新这一列的端点'),
        'col[y] = [x, x]': '这一列第一次出现，最小和最大 x 都是 `{x}`',
        'col[y][0] = min': '最小 x：`col[{y}][0] = {col[y][0]}`',
        'col[y][1] = max': '最大 x：`col[{y}][1] = {col[y][1]}`',
        'if x != col[y][0]': lambda S, B, r: (
            f'`x = {S.x}` 在 `col[{S.y}] = {S.col[S.y]}`，`y = {S.y}` 在 `row[{S.x}] = {S.row[S.x]}`：'
            + ('==都不是端点，四个方向都有建筑==' if S.x != S.col[S.y][0] and S.x != S.col[S.y][1] and S.y != S.row[S.x][0] and S.y != S.row[S.x][1]
               else '有一个等于端点，那个方向没有建筑')),
        'res += 1': '被覆盖，`res = {res}`',
        'return res': '共 `{res}` 个被覆盖的建筑',
    },
    cards=dict(
        one_liner='哈希表记下每行每列的两端，不在端点上就是被覆盖',
        complexity='时间 `O(m)`，空间 `O(m)`',
        problem=['`n × n` 的城市里有 `m` 个建筑 `(x, y)`',
                 '上下左右四个方向都至少有一个建筑，就算被覆盖',
                 '示例：`n=5, [[1,3],[3,2],[3,3],[3,5],[5,3]]` → `1`'],
        quote='首先对buildings进行一趟遍历，使用两个哈希表row和col分别统计每一行最小和最大的纵坐标，以及每一列最小和最大的横坐标。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟：`row[x]` 存这一行的 `[最小 y, 最大 y]`，`col[y]` 存这一列的 `[最小 x, 最大 x]`',
              '第二趟：对 `(x, y)`，看它是不是处在这些端点之间',
              '这里的写法是判断「不等于端点」，坐标唯一所以等价于严格夹在中间'],
        summary=['时间 `O(m)`，空间 `O(m)`，用字典所以不依赖 `n` 的大小',
                 '易错：`row` 以 x 为键、存 y 的范围，`col` 以 y 为键、存 x 的范围，别混',
                 '第一次出现的行/列要先建 `[v, v]`，再用 `min/max` 更新',
                 '原文为 Python 2 风格，本题只删去了类型说明，代码未改',
                 '对比灵神：灵神用定长数组并手写比较，这里用字典'],
    ),
)
