M = [[1, 2, -1], [4, -1, 6], [7, 8, 9]]


def _col(S, i, j, v):
    if 'j' in S and j == S['j']:
        return 'blue'
    return None


CONFIG = dict(
    num=3033, title='修改矩阵', difficulty='Easy', category='网格图',
    author='yiduobo', technique='按列两趟遍历',
    tags=[],
    code='''
class Solution(object):
    def modifiedMatrix(self, matrix):

        m = len(matrix)
        n = len(matrix[0])

        for j in range(n):
            ma = -1
            for i in range(m):
                ma = max(ma, matrix[i][j])
            
            for i in range(m):
                if matrix[i][j] == -1:
                    matrix[i][j] = ma
        
        return matrix
''',
    call=f'Solution().modifiedMatrix({M})',
    expect=[[1, 2, 9], [4, 8, 6], [7, 8, 9]],
    skip=['m = len', 'n = len', 'for i in range(m)'],
    views=[
        dict(type='grid', var='matrix', label='matrix（蓝 = 当前列，黄框 = 当前行 i）', cell=100, h=360, color=_col,
             cursors=[('i if _line >= 10 else None', 'j', 'yellow')]),
        dict(type='text', fn=lambda S: f"本列已看到的最大值 `ma` = =={S['ma']}==" if 'ma' in S and S['_line'] >= 8 else ''),
    ],
    watch=[('j', 'j', 'blue'), ('i', 'i', 'yellow'), ('ma', 'ma', 'green')],
    captions={
        7: lambda S, B, r: ('所有列都处理完了' if getattr(B, 'j', None) == S.j else f'按列遍历：`j = {S.j}`'),
        'ma = -1': '这一列的最大值先记成 `-1`（每列至少有一个非负数，会被更新）',
        'ma = max(ma': '`ma = max({B.ma}, matrix[{i}][{j}]={matrix[i][j]})` = =={ma}==',
        'if matrix[i][j] == -1': lambda S, B, r: (f'`matrix[{B.i}][{B.j}] = {B.matrix[B.i][B.j]}`' + (' ==是 -1，要替换==' if B.matrix[B.i][B.j] == -1 else '，不是 -1，不动')),
        'matrix[i][j] = ma': '第二趟：`matrix[{i}][{j}]` 改成列最大值 `{ma}`',
        'return matrix': '所有列处理完，返回 `matrix`',
    },
    cards=dict(
        one_liner='每列扫两趟：第一趟找最大值，第二趟替换 -1',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['把矩阵里每个 `-1` 换成它==所在列的最大元素==',
                 '示例：`[[1,2,-1],[4,-1,6],[7,8,9]]` → `[[1,2,9],[4,8,6],[7,8,9]]`'],
        quote='按列遍历整个矩阵，对于当前列，先按行遍历获取列中的最大值ma，接下来再将列中值为-1的数修改成ma即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['外层 `j` 枚举列，内层 `i` 枚举行',
              '第一趟：`ma` 从 `-1` 起，逐行取 `max`',
              '第二趟：碰到 `-1` 就写成 `ma`'],
        summary=['时间 `O(mn)`（每格看两次），空间 `O(1)`',
                 '易错：必须分两趟，边找最大值边替换会拿到不完整的最大值',
                 '`ma` 初值 `-1` 可行，因为每列保证有非负数',
                 '原文为 Python 2 风格，仅删去类型说明，代码未改'],
    ),
)
