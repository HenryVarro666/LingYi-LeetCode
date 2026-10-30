def _deg(S):
    return [sum(r) for r in S['matrix']] if 'matrix' in S else []


def _text(S):
    if 'matrix' not in S:
        return '无向图的邻接矩阵：第 `i` 行有几个 `1`，顶点 `i` 的度就是几'
    return '每行求和：' + '，'.join(f'顶点 {i} → `{sum(r)}`' for i, r in enumerate(S['matrix']))


CONFIG = dict(
    num=3898, title='统计每个顶点的度', difficulty='Easy', category='图论算法',
    author='灵茶山艾府', technique='邻接矩阵按行求和', tags=[],
    code='''
class Solution:
    def findDegrees(self, matrix: List[List[int]]) -> List[int]:
        return list(map(sum, matrix))
''',
    call='[Solution().findDegrees(m) for m in ([[0,1,1,0],[1,0,1,0],[1,1,0,1],[0,0,1,0]], [[0,1,0],[1,0,0],[0,0,0]], [[0]])]',
    expect=[[2, 2, 3, 1], [1, 1, 0], [0]],
    views=[
        dict(type='text', fn=_text, size=28, h=80),
        dict(type='table', var='matrix', rows=lambda S: [f'点{i}' for i in range(len(S['matrix']))],
             cols=lambda S: [f'点{i}' for i in range(len(S['matrix']))],
             color=lambda S, i, j, v: 'green' if v == 1 else None, cell=96, h=380),
        dict(type='array', var=_deg, label='ans[i] = 第 i 行的和 = 顶点 i 的度', cell=96, color=lambda S, i, v: 'yellow', h=190),
    ],
    watch=[],
    captions={
        'return list(map(sum, matrix))': lambda S, B, ret: '顶点 `i` 的度 = `matrix[i]` 里 `1` 的个数 → 每行求和：==' + str(ret) + '==',
    },
    cards=dict(
        one_liner='点 i 的度，就是邻接矩阵第 i 行里 1 的个数',
        complexity='时间 `O(mn)`，空间 `O(1)`（返回值不计入）',
        problem=['`matrix` 是 `n x n` 邻接矩阵，表示无向图',
                 '`matrix[i][j] = 1` 表示顶点 `i` 和 `j` 之间有一条边',
                 '返回每个顶点的度（相连的边数）',
                 '示例：`[[0,1,0],[1,0,0],[0,0,0]]` → `[1,1,0]`'],
        quote='根据题意，点 i 的度等于 matrix[i] 中的 1 的个数。所以统计矩阵每一行的 1 的个数即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['邻接矩阵第 `i` 行记录了 `i` 与所有点的连接情况',
              '元素只有 `0` 和 `1`，所以 `sum(matrix[i])` 就是 `1` 的个数',
              '`map(sum, matrix)` 对每行求和，`list` 收集成答案'],
        after=[dict(heading='演示说明', lines=['代码只有一行，所以每次调用对应一步',
                                             '依次演示 4 个点、3 个点、1 个点的图'])],
        summary=['时间 `O(mn)`：每个元素看一次；这里 `m = n`',
                 '空间 `O(1)`，返回值不计入',
                 '无向图矩阵对称，对角线为 0，所以不用额外处理自环',
                 '`map(sum, matrix)` 惰性，要 `list` 才得到列表'],
    ),
)
