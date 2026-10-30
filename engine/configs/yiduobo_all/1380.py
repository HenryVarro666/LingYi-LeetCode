CONFIG = dict(
    num=1380, title='矩阵中的幸运数', difficulty='Easy', category='网格图',
    author='yiduobo', technique='行最小列最大',
    code='''
class Solution(object):
    def luckyNumbers (self, matrix):

        row = []
        m = len(matrix)
        n = len(matrix[0])
        for i in range(m):
            now = 0
            for j in range(1, n):
                if matrix[i][now] > matrix[i][j]:
                    now = j
            row.append(now)
        
        col = []
        for j in range(n):
            now = 0
            for i in range(1, m):
                if matrix[now][j] < matrix[i][j]:
                    now = i
            col.append(now)
        
        res = []
        for i in range(m):
            j = row[i]
            if col[j] == i:
                res.append(matrix[i][j])
        
        return res
''',
    call='Solution().luckyNumbers([[3,7,8],[9,11,13],[15,16,17]])',
    expect=[15],
    views=[
        dict(type='grid', var='matrix', h=330,
             cursors=[('i', 'j', 'yellow', '(i,j)')],
             color=lambda S, i, j, v: ('green' if 'row' in S and 'col' in S and i < len(S['row']) and S['row'][i] == j and j < len(S['col']) and S['col'][j] == i
                                       else 'blue' if 'row' in S and i < len(S['row']) and S['row'][i] == j
                                       else 'pink' if 'col' in S and j < len(S['col']) and S['col'][j] == i else None)),
        dict(type='text', fn=lambda S: '蓝 = 该行最小，粉 = 该列最大，绿 = 两者兼得（幸运数）', size=26, h=60),
    ],
    watch=['i', 'j', 'now', ('row', 'row', 'blue'), ('col', 'col', 'pink'), ('res', 'res', 'green')],
    captions={
        'if matrix[i][now] > matrix[i][j]': '比较 `{matrix[i][now]}`（当前最小）和 `{matrix[i][j]}`：' + '{"更小，换人" if matrix[i][now] > matrix[i][j] else "不更小，保持"}',
        'row.append(now)': '第 `{i}` 行最小值在第 `{now}` 列，记入 `row`：`{row}`',
        'if matrix[now][j] < matrix[i][j]': '比较 `{matrix[now][j]}`（当前最大）和 `{matrix[i][j]}`：' + '{"更大，换人" if matrix[now][j] < matrix[i][j] else "不更大，保持"}',
        'col.append(now)': '第 `{j}` 列最大值在第 `{now}` 行，记入 `col`：`{col}`',
        'j = row[i]': '第 `{i}` 行最小值在第 `{j}` 列',
        'if col[j] == i': lambda S, B, r: (f'`col[{S.j}] = {S.col[S.j]}` == `{S.i}`：这列最大也在本行 → ==幸运数=='
                                           if S.col[S.j] == S.i else f'`col[{S.j}] = {S.col[S.j]}` != `{S.i}`：这列最大在别的行 → 不是'),
        'res.append': '`{matrix[i][j]}` 既是行最小又是列最大，加入答案：`{res}`',
        'return': '幸运数 `{ret}`',
    },
    cards=dict(
        one_liner='先记每行最小在哪列、每列最大在哪行，再对一对',
        complexity='时间 `O(mn)`，空间 `O(m+n)`',
        problem=['矩阵中数字互不相同，找出所有「在所在行最小、同时在所在列最大」的数',
                 '本视频：`[[3,7,8],[9,11,13],[15,16,17]]` → `[15]`'],
        quote='先找出每一行中的最小值位于哪一列，并使用一个数组row记录下来，接下来找出每一列中的最大值位于哪一行，同样是用一个数组col记录下来。',
        quote_src='—— yiduobo 题解原文',
        idea=['数字互不相同 → 每行最小、每列最大都唯一',
              '`row[i]` 记第 i 行最小值的列，`col[j]` 记第 j 列最大值的行',
              '若 `col[row[i]] == i`，说明这个格子两个条件同时满足'],
        summary=['时间 `O(mn)`，空间 `O(m+n)`',
                 '记的是位置（列号/行号）而不是数值，才能直接比对',
                 '依赖「所有数互不相同」，否则最值可能不唯一',
                 '原文为 Python 2 风格，除删去类型文档字符串外无需改动'],
    ),
)
