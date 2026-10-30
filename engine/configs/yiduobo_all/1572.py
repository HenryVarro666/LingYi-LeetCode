def _cell(S, i, j, v):
    if 'n' not in S:
        return None
    n = S['n']
    if j == i or j == n - i - 1:
        k = S.get('i', -1)
        if i < k or (i == k and S['_line'] >= 8):
            return 'green'
        return 'cyan'
    return None


CONFIG = dict(
    num=1572, title='矩阵对角线元素的和', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='逐行取两条对角线',
    code='''
class Solution(object):
    def diagonalSum(self, mat):

        n = len(mat)
        res = 0
        for i in range(n):
            res += mat[i][i]
            res += mat[i][n - i - 1]

        if n & 1:
            res -= mat[n // 2][n // 2]
        
        return res
''',
    call='Solution().diagonalSum([[1,2,3,4,5],[6,7,8,9,1],[2,3,4,5,6],[7,8,9,1,2],[3,4,5,6,7]])',
    expect=45,
    views=[
        dict(type='grid', var='mat', label='mat（青 = 两条对角线上的格子，绿 = 已加进 res，黄框 = 这一步取的格子）', cell=96, h=420,
             color=_cell, cursors=[('i', 'i', 'blue'), ('i', 'n - i - 1 if _line == 8 else None', 'pink')]),
        dict(type='text', h=70, size=30,
             fn=lambda S: f"第 `{S['i']}` 行：左对角线列 `{S['i']}`，右对角线列 `{S['n'] - S['i'] - 1}`" if 'i' in S and 'n' in S else ''),
    ],
    watch=[('i', 'i', 'blue'), ('n', 'n'), ('res', 'res', 'green')],
    captions={
        'n = len': '`n = {n}`：方阵的行数，也是列数',
        'res = 0': '`res` 累计对角线元素和',
        'for i in range': lambda S, B, r: (f'处理第 `{S.i}` 行' if S.i != B.get('i', -1) or B.get('i') is None else '所有行都加完了，for 结束'),
        'res += mat[i][i]': '左对角线：第 `{i}` 行取第 `{i}` 列 `mat[{i}][{i}] = {mat[i][i]}` → `res` = {res}',
        'res += mat[i][n - i - 1]': '右对角线：第 `{i}` 行取第 `n-i-1 = {n-i-1}` 列 `mat[{i}][{n-i-1}] = {mat[i][n-i-1]}` → `res` = {res}',
        'if n & 1': lambda S, B, r: (f"`n = {S.n}` 是奇数：两条对角线交于正中心，中心元素被加了两次" if S.n & 1
                                      else f"`n = {S.n}` 是偶数：两条对角线不相交，不用处理"),
        'res -= mat[': '中心元素 `mat[{n//2}][{n//2}] = {mat[n//2][n//2]}` 多算了一次 → 减掉，`res` = =={res}==',
        'return res': '对角线元素总和 `{res}`',
    },
    cards=dict(
        one_liner='每行取两个数：第 i 列和第 n-i-1 列',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给一个 `n × n` 的方阵 `mat`，返回两条对角线上元素的和',
                 '两条对角线交点上的元素只算一次',
                 '示例：`[[1,2,3],[4,5,6],[7,8,9]]` → `25`；本视频用 5×5 方阵'],
        quote='对于第i行，其左对角线上的元素位于第i列，而右对角线上的元素则位于第n - i - 1列，其中n为矩阵的总行数。',
        quote_src='—— yiduobo 题解原文',
        idea=['只遍历 `n` 行，每行直接按下标取两个数，不用扫整个矩阵',
              'n 为奇数时，第 `n//2` 行的两个下标相同，==中心元素被加了两次==',
              '先照加不误，最后再减一次中心元素'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：奇数阶才需要减中心；`n & 1` 判断奇偶',
                 '中心下标是 `n // 2`，行列都一样',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
