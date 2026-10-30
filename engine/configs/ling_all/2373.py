def _c(S, i, j, v):
    if 'i' not in S or 'j' not in S:
        return None
    if S['i'] <= i <= S['i'] + 2 and S['j'] <= j <= S['j'] + 2 and not (i == S['i'] and j == S['j']):
        return 'blue'
    return None


CONFIG = dict(
    num=2373, title='矩阵中的局部最大值', difficulty='Easy', category='网格图',
    author='灵茶山艾府', technique='原地保存最大值',
    tags=[],
    code='''
class Solution:
    def largestLocal(self, grid: List[List[int]]) -> List[List[int]]:
        n = len(grid)
        for i in range(n - 2):
            for j in range(n - 2):
                grid[i][j] = max(max(row[j:j + 3]) for row in grid[i:i + 3])
            del grid[i][-2:]
        del grid[-2:]  # 不要 return grid[:-2] 那样会有额外的拷贝
        return grid
''',
    call='Solution().largestLocal([[9,9,8,1],[5,6,2,6],[8,2,6,4],[6,2,2,2]])',
    expect=[[9, 9], [8, 6]],
    views=[
        dict(type='grid', var='grid', label='grid（蓝 = 当前 3×3 窗口，黄 = 左上角，写入最大值）', cell=110, h=470,
             color=_c, cursors=[('i', 'j', 'yellow')]),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'n'],
    captions={
        'n = len': '`n = {n}`，结果是 `{n-2} × {n-2}` 的矩阵',
        'for i in range': '`i = {i}`：处理第 `{i}` 行起头的窗口',
        'for j in range': '`j = {j}`：窗口左上角是 `({i},{j})`',
        'grid[i][j] = max': '`grid[{i}][{j}]` 开始的 3×3 里最大值是 =={grid[i][j]}==，直接写回左上角（左上角之后不会再被别的窗口读到）',
        'del grid[i][-2:]': '第 `{i}` 行算完，砍掉右边没用的 2 列',
        'del grid[-2:]': '最后 2 行没用了，原地删掉，不额外拷贝',
        'return grid': '返回原地改好的 `grid`',
    },
    cards=dict(
        one_liner='把 3×3 的最大值就地存到它的左上角',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['`n × n` 矩阵 `grid`，求每个 3×3 子矩阵的最大值',
                 '结果是 `(n-2) × (n-2)` 的矩阵',
                 '示例：`[[9,9,8,1],[5,6,2,6],[8,2,6,4],[6,2,2,2]]` → `[[9,9],[8,6]]`'],
        quote='把最大值直接保存在 3×3 矩阵的左上角，这样无需创建返回矩阵。',
        quote_src='—— 灵茶山艾府题解',
        idea=['窗口 `(i,j)` 只会读右下方，写左上角后不影响后面的窗口',
              '每行算完删掉最后 2 列，最后删掉最后 2 行',
              '全程原地，不创建返回矩阵'],
        summary=['时间 `O(n^2)`，空间 `O(1)`',
                 '易错：不能 `return grid[:-2]`，那样会多拷贝一份',
                 '思考题：窗口很大时可用二维单调队列'],
    ),
)
