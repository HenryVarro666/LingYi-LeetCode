CONFIG = dict(
    num=2661, title='找出叠涂元素', difficulty='Medium', category='网格图',
    author='yiduobo', technique='行列计数 · 位置预处理', tags=[],
    code='''
class Solution(object):
    def firstCompleteIndex(self, arr, mat):

        k = len(arr)
        row = [None] * (k + 1)
        col = [None] * (k + 1)

        m = len(mat)
        n = len(mat[0])
        filled_row = [0] * m
        filled_col = [0] * n

        for i in range(m):
            for j in range(n):
                row[mat[i][j]] = i
                col[mat[i][j]] = j
        
        for index, v in enumerate(arr):
            filled_row[row[v]] += 1
            filled_col[col[v]] += 1
            if filled_row[row[v]] == n or filled_col[col[v]] == m:
                return index
''',
    call='Solution().firstCompleteIndex([2,8,7,4,1,3,5,6,9], [[3,2,5],[1,4,6],[8,7,9]])',
    expect=3,
    views=[
        dict(type='array', var='arr', label='arr（涂色顺序）', pointers={'index': 'blue'}, h=200,
             color=lambda S, i, v: 'green' if 'index' in S and i <= S['index'] else None),
        dict(type='grid', var='mat', label='mat（绿色 = 已涂）', h=300,
             color=lambda S, i, j, v: 'green' if 'index' in S and v in S['arr'][:S['index'] + 1] else None,
             cursors=[(lambda S: S['row'][S['v']] if 'v' in S else None, lambda S: S['col'][S['v']] if 'v' in S else None, 'yellow', '')]),
        dict(type='text', size=28, fn=lambda S: f"每行已涂 `filled_row = {S['filled_row']}`（满 {S['n']} 个算整行）" if 'filled_row' in S and 'n' in S else ''),
        dict(type='text', size=28, fn=lambda S: f"每列已涂 `filled_col = {S['filled_col']}`（满 {S['m']} 个算整列）" if 'filled_col' in S and 'm' in S else ''),
    ],
    watch=['index', 'v', 'filled_row', 'filled_col'],
    captions={
        'k = len(arr)': '`arr` 里有 `k = {k}` 个数，每个数恰好出现一次',
        'row = [None]': '`row[x]` 记录数 `x` 在 `mat` 里的行号',
        'col = [None]': '`col[x]` 记录数 `x` 在 `mat` 里的列号',
        'filled_row = [0]': '`filled_row[i]` = 第 `i` 行已涂的个数，满 `n = {n}` 个算整行涂满',
        'filled_col = [0]': '`filled_col[j]` = 第 `j` 列已涂的个数，满 `m = {m}` 个算整列涂满',
        'row[mat[i][j]] = i': '预处理：数 `{mat[i][j]}` 在第 `{i}` 行',
        'col[mat[i][j]] = j': '预处理：数 `{mat[i][j]}` 在第 `{j}` 列，之后 O(1) 查位置',
        'for index, v in enumerate(arr)': '按顺序涂第 `{index}` 个数 `v = {v}`，它在 `({row[v]}, {col[v]})`',
        'filled_row[row[v]] += 1': '第 `{row[v]}` 行多涂了一个：`filled_row` = {filled_row}',
        'filled_col[col[v]] += 1': '第 `{col[v]}` 列多涂了一个：`filled_col` = {filled_col}',
        'if filled_row[row[v]] == n': lambda S, B, r: (f"第 {S.row[S.v]} 行已涂 {S.filled_row[S.row[S.v]]}/{S.n}，第 {S.col[S.v]} 列已涂 {S.filled_col[S.col[S.v]]}/{S.m} → " + ('有一行或一列涂满，当前下标就是答案' if (S.filled_row[S.row[S.v]] == S.n or S.filled_col[S.col[S.v]] == S.m) else '都没涂满，继续')),
        'return index': '涂满了：第一次满行/满列出现在下标 `{index}`，返回 =={index}==',
    },
    cards=dict(
        one_liner='给每行每列记个数，涂到某行或某列满了就停',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`arr` 是 `1..m·n` 的一个排列，`mat` 也是 `m×n` 个互不相同的数',
                 '按 `arr` 的顺序给 `mat` 里对应的格子涂色',
                 '返回第一次出现整行或整列被涂满的 `arr` 下标',
                 '示例：本视频 `3×3` 的矩阵 → `3`'],
        quote='对每一行和每一列都使用一个变量记录该行和该列的已经被填充的数的个数，接下来就只需要对arr进行一趟遍历，每次更新其所在行列对应变量的值。',
        quote_src='—— yiduobo 题解原文',
        idea=['先扫一遍 `mat`，用 `row`、`col` 记下每个数的位置',
              '再按 `arr` 顺序涂：该数所在行、列的计数各加 1',
              '行计数 `== n` 或列计数 `== m` 就是整行/整列涂满，返回下标'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '易错点：行满是 `== n`（列数），列满是 `== m`（行数），别写反',
                 '本题代码在 Python 3 下无需修改'],
    ),
)
