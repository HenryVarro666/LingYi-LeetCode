M = [[1, 2, -1], [4, -1, 6], [7, 8, 9]]


def _col(S, i, j, v):
    if 'j' not in S:
        return None
    if S['_line'] in (5, 6, 7) and S.get('row') is S['matrix'][i] and j == S['j']:
        return 'yellow'
    return 'blue' if j == S['j'] else None


CONFIG = dict(
    num=3033, title='修改矩阵', difficulty='Easy', category='网格图',
    author='灵茶山艾府', technique='逐列求最大值再替换',
    tags=[],
    code='''
class Solution:
    def modifiedMatrix(self, matrix: List[List[int]]) -> List[List[int]]:
        for j in range(len(matrix[0])):
            mx = max(row[j] for row in matrix)
            for row in matrix:
                if row[j] == -1:
                    row[j] = mx
        return matrix
''',
    call=f'Solution().modifiedMatrix({M})',
    expect=[[1, 2, 9], [4, 8, 6], [7, 8, 9]],
    views=[
        dict(type='grid', var='matrix', label='matrix（蓝 = 当前列，黄 = 正在看的 row[j]）', cell=100, h=360, color=_col),
        dict(type='text', fn=lambda S: f"第 `{S['j']}` 列最大值 `mx` = =={S['mx']}==" if 'mx' in S and 'j' in S and S['_line'] >= 4 else ''),
    ],
    watch=[('j', 'j', 'blue'), ('mx', 'mx', 'green')],
    captions={
        3: lambda S, B, r: ('所有列都处理完了' if getattr(B, 'j', None) == S.j else f'从左到右处理每一列：`j = {S.j}`'),
        'mx = max': '先扫一遍这一列，最大值 `mx` = =={mx}==（至少有一个非负数，所以不会是 -1）',
        5: lambda S, B, r: ('这一列的行都看完了' if getattr(B, 'row', None) == S.row else f'取下一行 `row = {S.row}`，看它第 `{S.j}` 个数'),
        'if row[j] == -1': lambda S, B, r: (f'这一行 `row[{B.j}] = {B.row[B.j]}`' + (' ==是 -1，要替换==' if B.row[B.j] == -1 else '，不是 -1，保留')),
        'row[j] = mx': '把 -1 换成本列最大值 `{mx}`（`row` 就是 `matrix` 里的行，原地修改）',
        'return matrix': '每一列都处理完，返回原地修改后的 `matrix`',
    },
    cards=dict(
        one_liner='一列一列来：先求列最大值，再把 -1 替换掉',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['矩阵 `matrix` 中的 `-1` 要替换成==所在列的最大元素==',
                 '示例：`[[1,2,-1],[4,-1,6],[7,8,9]]`',
                 '→ `[[1,2,9],[4,8,6],[7,8,9]]`'],
        quote='从左到右，遍历每一列。先计算出列的最大值 mx，再更新列中的 -1 为 mx。',
        quote_src='—— 灵茶山艾府题解',
        idea=['按列遍历：外层枚举 `j`，内层遍历每一行 `row`',
              '先 `max(row[j] for row in matrix)` 得到本列最大值',
              '再扫一遍，遇到 `-1` 就改成 `mx`，原地修改所以空间 `O(1)`'],
        summary=['时间 `O(mn)`，空间 `O(1)`（不算返回值）',
                 '易错：必须==先求完整列最大值==再替换，替换时 `mx` 已经定好，不会受 -1 影响',
                 '题目保证每列至少有一个非负数，所以 `mx` 不会是 -1'],
    ),
)
