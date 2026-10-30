def _cmp(S):
    if 'i' not in S or 'j' not in S:
        return ''
    i, j, m = S['i'], S['j'], S['matrix']
    a, b = m[i][j], m[i - 1][j - 1]
    return f'`matrix[{i}][{j}] = {a}` 对比左上角 `matrix[{i-1}][{j-1}] = {b}`：' + ('==相等==' if a == b else '==不相等==')


def _color(S, i, j, v):
    if 'i' not in S or 'j' not in S:
        return None
    ci, cj = S['i'], S['j']
    if (i, j) == (ci, cj):
        return 'blue'
    if (i, j) == (ci - 1, cj - 1):
        return 'pink'
    return None


CONFIG = dict(
    num=766, title='托普利茨矩阵', difficulty='Easy', category='网格图',
    author='yiduobo', technique='逐行对比左上角', tags=[],
    code='''
class Solution(object):
    def isToeplitzMatrix(self, matrix):

        m = len(matrix)
        n = len(matrix[0])

        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][j] != matrix[i - 1][j - 1]:
                    return False
        
        return True
''',
    call='Solution().isToeplitzMatrix([[1,2,3,4],[5,1,2,3],[9,5,1,2]])',
    expect=True,
    views=[
        dict(type='grid', var='matrix', color=_color, h=330, cell=90),
        dict(type='text', fn=_cmp, size=30, h=70),
    ],
    watch=['m', 'n', 'i', 'j'],
    skip=['m = len', 'n = len'],
    captions={
        'for i in range(1, m)': '==从第二行开始==，每次只检测一行：`i = {i}`',
        'for j in range(1, n)': '第 0 列是对角线起点无需检测，`j` 从 1 起：现在 `j = {j}`',
        'if matrix[i][j] !=': lambda S, B, r: (f'`{S.matrix[S.i][S.j]}` 和左上角 `{S.matrix[S.i-1][S.j-1]}` 相等 → 同一条对角线上没出问题' if S.matrix[S.i][S.j] == S.matrix[S.i-1][S.j-1] else f'`{S.matrix[S.i][S.j]}` ≠ 左上角 `{S.matrix[S.i-1][S.j-1]}` → 这条对角线不一致'),
        'return False': '有一处不一致，直接返回 `False`',
        'return True': '所有格子都和左上角相等，每条对角线都一致 → `True`',
    },
    cards=dict(
        one_liner='跳出对角线的框框：每个格子只要等于它的左上角',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['若矩阵中每条从左上到右下的对角线上元素都相同，就是托普利茨矩阵',
                 '给定 `m×n` 矩阵，判断是不是',
                 '本视频：`[[1,2,3,4],[5,1,2,3],[9,5,1,2]]` → `True`'],
        quote='那么可以跳出对角线的框框，从第二行开始，每次只检测一行。',
        quote_src='—— yiduobo 题解原文',
        idea=['同一条对角线上相邻两个元素，互为左上、右下',
              '所以只需检查 `matrix[i][j] == matrix[i-1][j-1]`',
              '第 0 行、第 0 列是对角线起点，不用检测'],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '`i`、`j` 都从 1 开始，否则 `i-1`、`j-1` 会越界（或读到负下标）',
                 '发现不等立即返回 `False`',
                 '原文 Python 2 风格，本题代码无需修改即可在 Python 3 运行'],
    ),
)
