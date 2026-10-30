CONFIG = dict(
    num=3239, title='最少翻转次数使二进制矩阵回文 I', difficulty='Medium', category='网格图',
    author='yiduobo', technique='双指针 · 逐行逐列统计',
    code='''
class Solution(object):
    def minFlips(self, grid):

        res = None
        m = len(grid)
        n = len(grid[0])

        cnt = 0
        for i in range(m):
            left, right = 0, n - 1
            while left < right:
                if grid[i][left] != grid[i][right]:
                    cnt += 1
                left += 1
                right -= 1
            
        res = cnt

        cnt = 0
        for j in range(n):
            top, bottom = 0, m - 1
            while top < bottom:
                if grid[top][j] != grid[bottom][j]:
                    cnt += 1
                top += 1
                bottom -= 1

        res = min(res, cnt)
        return res
''',
    call='Solution().minFlips([[1,0,0,0],[0,1,0,1],[1,0,1,0]])',
    expect=1,
    views=[
        dict(type='grid', var='grid', h=330, cell=70,
             cursors=[('i', 'left', 'blue', 'L'), ('i', 'right', 'pink', 'R')]),
        dict(type='text', size=30, h=100,
             fn=lambda S: f"行代价 `res = {S.get('res')}`，当前累计 `cnt = {S.get('cnt', 0)}`"),
    ],
    watch=[('cnt', 'cnt', 'green'), ('res', 'res', 'orange'), ('left', 'left', 'blue'), ('right', 'right', 'pink')],
    captions={
        'res = None': '`res` 最后保存较小的那个代价',
        'cnt = 0': '`cnt` 清零，开始统计新一轮的翻转数',
        'left, right = 0, n - 1': '第 `{i}` 行：左右指针从两端出发 `left = 0`，`right = {right}`',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`，继续向中间比较' if S.left < S.right
                                               else f'指针相遇，这一行比完了'),
        'if grid[i][left] != grid[i][right]': '`grid[{i}][{left}] = {grid[i][left]}`，`grid[{i}][{right}] = {grid[i][right]}` → {"不同，需翻转一次" if grid[i][left] != grid[i][right] else "相同"}',
        'left += 1': '`left` → {left}',
        'right -= 1': '`right` → {right}',
        'res = cnt': '所有行变回文的代价：`res = {res}`',
        'top, bottom = 0, m - 1': '第 `{j}` 列：上下指针从两端出发 `top = 0`，`bottom = {bottom}`',
        'while top < bottom': lambda S, B, r: (f'`top = {S.top} < bottom = {S.bottom}`，继续向中间比较' if S.top < S.bottom
                                               else '指针相遇，这一列比完了'),
        'if grid[top][j] != grid[bottom][j]': '`grid[{top}][{j}] = {grid[top][j]}`，`grid[{bottom}][{j}] = {grid[bottom][j]}` → {"不同，需翻转一次" if grid[top][j] != grid[bottom][j] else "相同"}',
        'cnt += 1': '不同，翻一次：`cnt` → {cnt}',
        'top += 1': '`top` → {top}',
        'bottom -= 1': '`bottom` → {bottom}',
        'res = min': '取较小：`min(行代价, 列代价)` → ==`res = {res}`==',
        'return res': '最少翻转 `{res}` 次',
    },
    cards=dict(
        one_liner='分别算「全行回文」「全列回文」的代价，取小',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['二进制矩阵，每次可翻转任意一个格子',
                 '要使所有行回文，或所有列回文，求最少翻转次数',
                 '本视频：`3×4` 矩阵 → `1`（翻转一列内的一格）'],
        quote='对于将所有行变成回文需要的代价，可以遍历grid的每一行，对于当前行，从左右两侧向中间遍历，若对称位置上的值不相同，那么就需要进行一次修改。',
        quote_src='—— yiduobo 题解原文',
        idea=['行、列两种目标各算一个总代价',
              '每行用左右指针往中间走，对称位置不同就计一次',
              '每列同样用上下指针，最后取较小值'],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '易错：`cnt` 算完行后必须清零再算列',
                 '`while left < right` 保证中间格不比较',
                 '原文为 Python 2 风格，代码无需改动',
                 '对比灵神：灵神用 `row[-1-j]` 与 `zip(*grid)`；yiduobo 手写双指针'],
    ),
)
