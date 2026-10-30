CONFIG = dict(
    num=883, title='三维形体投影面积', difficulty='Easy', category='网格图',
    author='yiduobo', technique='俯视 + 每行/每列取最大值',
    tags=[],
    code='''
class Solution(object):
    def projectionArea(self, grid):

        m = len(grid)
        n = len(grid[0])
        max_row = [0] * m
        max_col = [0] * n
        res = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] > 0:
                    res += 1
                    max_row[i] = max(max_row[i], grid[i][j])
                    max_col[j] = max(max_col[j], grid[i][j])
        
        return res + sum(max_col) + sum(max_row)
''',
    call='Solution().projectionArea([[1,2,0],[3,0,4]])',
    expect=19,
    views=[
        dict(type='grid', var='grid', cursors=[('i', 'j', 'yellow', '(i,j)')], h=300,
             color=lambda S, i, j, v: None if v > 0 else 'dim'),
        dict(type='array', var='max_row', pointers={'i': 'blue'}, label='max_row（每行最高）', h=130),
        dict(type='array', var='max_col', pointers={'j': 'pink'}, label='max_col（每列最高）', h=130),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('res（俯视）', 'res', 'green')],
    captions={
        'max_row = [0]': '`max_row[i]`：第 `i` 行从侧面看的投影高度，先全部记 0',
        'max_col = [0]': '`max_col[j]`：第 `j` 列从前面看的投影高度，先全部记 0',
        'res = 0': '`res` 统计俯视图面积，即非 0 格子的个数',
        'if grid[i][j] > 0': '`grid[{i}][{j}] = {grid[i][j]}` > 0？→ {"有立方体，会投影" if grid[i][j] > 0 else "是空格，不投影"}',
        'res += 1': '这个格子从上往下看有投影：`res` → =={res}==',
        'max_row[i] = max': '行最大：`max({B.max_row[i]}, {grid[i][j]})` → `max_row[{i}] = {max_row[i]}`',
        'max_col[j] = max': '列最大：`max({B.max_col[j]}, {grid[i][j]})` → `max_col[{j}] = {max_col[j]}`',
        'return res': '俯视 `{res}` + 前后 `sum(max_col) = {sum(max_col)}` + 左右 `sum(max_row) = {sum(max_row)}` = =={ret}==',
    },
    cards=dict(
        one_liner='三个方向各算一次：俯视数格子，侧视取每行/每列最高',
        complexity='时间 `O(m*n)`，空间 `O(m+n)`',
        problem=['`n×n` 网格，`grid[i][j]` 表示该格摞了几个 `1×1×1` 立方体',
                 '求形体在 xy、yz、zx 三个平面上的投影面积之和',
                 '本视频：`[[1,2,0],[3,0,4]]`（2×3，原题为方阵）→ `19`'],
        quote='从上面来看，所有高度非0的格子都会形成投影，因此对于grid中所有非0值，都应该将答案加上1',
        quote_src='—— yiduobo 题解原文',
        idea=['俯视：每个非 0 格子贡献 `1`',
              '左右看：每一行只看最高的那摞 → 加 `max_row`',
              '前后看：每一列只看最高的那摞 → 加 `max_col`'],
        summary=['时间 `O(m*n)`，空间 `O(m+n)`',
                 '易错：俯视统计的是==非 0 格子数==，不是高度之和',
                 '侧视看的是行/列的==最大值==，被挡住的矮摞不计',
                 '原文代码已是 Python 3 写法，未做修改'],
    ),
)
