def _text(S):
    if 'matrix' not in S:
        return '第 `i` 行就是顶点 `i` 的连接情况，行和就是度'
    return '行和：' + '，'.join(f'`matrix[{i}]` = {sum(r)}' for i, r in enumerate(S['matrix']))


CONFIG = dict(
    num=3898, title='统计每个顶点的度', difficulty='Easy', category='图论算法',
    author='yiduobo', technique='遍历每一行求和', tags=[],
    code='''
class Solution(object):
    def findDegrees(self, matrix):
        
        return [sum(row) for row in matrix]
''',
    call='[Solution().findDegrees(m) for m in ([[0,1,1],[1,0,1],[1,1,0]], [[0,1,0,0,0],[1,0,1,1,0],[0,1,0,0,0],[0,1,0,0,0],[0,0,0,0,0]], [[0]])]',
    expect=[[2, 2, 2], [1, 3, 1, 1, 0], [0]],
    views=[
        dict(type='text', fn=_text, size=28, h=80),
        dict(type='table', var='matrix', rows=lambda S: [f'点{i}' for i in range(len(S['matrix']))],
             cols=lambda S: [f'点{i}' for i in range(len(S['matrix']))],
             color=lambda S, i, j, v: 'cyan' if v == 1 else None, cell=96, h=400),
        dict(type='array', var=lambda S: [sum(r) for r in S['matrix']] if 'matrix' in S else [],
             label='每行之和 = 每个顶点的度', cell=96, color=lambda S, i, v: 'green', h=190),
    ],
    watch=[],
    captions={
        'return [sum(row) for row in matrix]': lambda S, B, ret: '`matrix[i]` 里的 `1` 就是 `i` 连出去的边，每行求和得到度：==' + str(ret) + '==',
    },
    cards=dict(
        one_liner='matrix[i] 里 1 的数量，就是顶点 i 的度',
        complexity='时间 `O(n^2)`，空间 `O(n)`（结果数组）',
        problem=['`n * n` 的 `matrix` 表示一个无向图',
                 '`matrix[i][j]` 为 `1`：`i` 和 `j` 之间有边',
                 '返回长度为 `n` 的数组，`ans[i]` 是顶点 `i` 的度',
                 '本视频演示 3 个点、5 个点（星形）、1 个点'],
        quote='对于第i个顶点，matrix[i]表达就是i的连接情况，更具体的，其中1的数量就是i与其他节点连边的数量，即i的度。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历 `matrix` 的每一行 `row`',
              '行内全是 `0/1`，`sum(row)` 就是 `1` 的数量',
              '列表推导一行写完：`[sum(row) for row in matrix]`'],
        after=[dict(heading='演示说明', lines=['列表推导式在引擎里合并成一步，每次调用一步',
                                             '星形图中间点度为 `3`，孤立点度为 `0`'])],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '星形图的中心点度最大，孤立点的度为 `0`',
                 '图是无向的，矩阵对称，按行求和或按列求和结果一样',
                 '原文为 Python 2 风格（class Solution(object)），代码无需修改'],
    ),
)
