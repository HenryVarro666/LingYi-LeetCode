M = [[0, 1, 1, 1], [1, 1, 1, 1], [0, 1, 1, 1]]


def _fcol(S, i, j, v):
    if 'f' not in S:
        return None
    return 'green' if v >= 2 else None


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or 'f' not in S:
        return '`f[i][j]` = 以 `(i,j)` 为右下角的全 1 正方形最大边长'
    f = S['f']
    if S['matrix'][i][j] == 1 and i and j:
        return f'`min(f[{i-1}][{j}], f[{i}][{j-1}], f[{i-1}][{j-1}]) + 1` = `min({f[i-1][j]}, {f[i][j-1]}, {f[i-1][j-1]}) + 1`'
    return f'`f[{i}][{j}]` = {f[i][j]}，累计 `res` = {S["res"]}'


CONFIG = dict(
    num=1277, title='统计全为 1 的正方形子矩阵', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='二维 DP：以 (i,j) 为右下角的最大边长',
    tags=['单调栈'],
    code='''
class Solution(object):
    def countSquares(self, matrix):

        m = len(matrix)
        n = len(matrix[0])
        f = [[0] * n for _ in range(m)]
        res = 0
        for i in range(m):
            for j in range(n):
                if i == 0:
                    f[i][j] = matrix[i][j]
                elif j == 0:
                    f[i][j] = matrix[i][j]
                elif matrix[i][j] == 1:
                    f[i][j] = min(f[i - 1][j], f[i][j - 1], f[i - 1][j - 1]) + 1

                res += f[i][j]
        
        return res
''',
    call=f'Solution().countSquares({M})',
    expect=15,
    skip=['m = len', 'n = len', 'f = [[0]', 'res = 0'],
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='grid', var='f', label='f（黄 = 当前格；绿 = 边长不小于 2）', cell=110, h=330,
             color=_fcol, cursors=[('i', 'j', 'yellow')]),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('res', 'res', 'green')],
    captions={
        'if i == 0': lambda S, B, r: ('第一行 `i == 0`：正方形只能是单格，`f` 直接取 `matrix[0][%d]`' % S.j if S.i == 0
                                      else '`i = %d`，不在第一行' % S.i),
        'elif j == 0': lambda S, B, r: ('第一列 `j == 0`：正方形只能是单格，`f` 直接取 `matrix[%d][0]`' % S.i if S.j == 0
                                        else '`j = %d`，不在第一列' % S.j),
        'elif matrix[i][j] == 1': lambda S, B, r: (
            f'`matrix[{S.i}][{S.j}] = 1` → ==用 f 的三个邻居推出边长==' if S.matrix[S.i][S.j] == 1
            else f'`matrix[{S.i}][{S.j}] = 0`：不能当右下角，`f` 保持 0'),
        'f[i - 1][j], f[i][j - 1]': '右侧边由 `f[{i-1}][{j}]` 决定，下边由 `f[{i}][{j-1}]` 决定，左上角还要看 `f[{i-1}][{j-1}]`，取最小再 +1 = =={f[i][j]}==',
        'res += f[i][j]': '把 `f[{i}][{j}] = {f[i][j]}` 累加进答案：`res` = {res}',
        'return res': '所有 `f` 之和 = ==`{res}`==',
    },
    cards=dict(
        one_liner='f[i][j] 是右下角最大边长，累加所有 f 就是答案',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['0/1 矩阵，统计全为 1 的==正方形子矩阵==个数',
                 '示例：`[[0,1,1,1],[1,1,1,1],[0,1,1,1]]` → `15`',
                 '本视频使用的就是这个示例'],
        quote='若matrix[i][j]为1，且i和j都大于0，那么我们可以从f[i - 1][j]、f[i][j - 1]以及f[i - 1][j - 1]中推断出f[i][j]。',
        quote_src='—— yiduobo 题解原文',
        idea=['`matrix[i][j]` 为 0：`f = 0`；第一行第一列：`f` 就是它自己',
              '其余为 1 的格子：右侧边看上方、下边看左方，左上角再看左上',
              '`f[i][j] = min(上, 左, 左上) + 1`，遍历时累加到 `res`'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '三个邻居缺一不可：左上角决定正方形内部是否全 1',
                 '第一行和第一列单独处理，避免下标 -1',
                 '对比灵神：灵神给的 DP 在 f 上加一圈 0 并原地修改，yiduobo 显式分情况'],
    ),
)
