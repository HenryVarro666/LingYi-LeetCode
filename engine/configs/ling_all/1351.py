CONFIG = dict(
    num=1351, title='统计有序矩阵中的负数', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='从右上角出发的双指针',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution:
    def countNegatives(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        ans = 0
        i, j = 0, n - 1  # 从右上角开始
        while i < m and j >= 0:  # 还有剩余元素
            if grid[i][j] < 0:
                ans += m - i  # 这一列剩余元素都是负数
                j -= 1
            else:
                i += 1  # 这一行剩余元素全都非负，排除
        return ans
''',
    call='Solution().countNegatives([[4,3,2,-1],[3,2,1,-1],[1,1,-1,-2],[-1,-1,-2,-3]])',
    expect=8,
    views=[
        dict(type='text', fn=lambda S: (f"右上角 `({S['i']}, {S['j']})` 往左下走；已确认的负数 ==`{S['ans']}`== 个" if 'ans' in S and 'i' in S else '')),
        dict(type='grid', var='grid', cursors=[('i', 'j', 'yellow', '(i,j)')], h=420, cell=96,
             color=lambda S, i, j, v: ('pink' if v < 0 else None) if 'ans' in S else None,
             dim=lambda S, i, j, v: ('i' in S and 'j' in S and (i < S['i'] or j > S['j']))),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'm, n = len': '`m = {m}` 行，`n = {n}` 列',
        'i, j = 0': '从右上角 `(0, {j})` 出发：它是所在行最大、所在列最小的数',
        'while i < m': lambda S, B, r: (f'`i = {S.i} < {S.m}` 且 `j = {S.j} >= 0`：还有剩余元素，继续' if (S.i < S.m and S.j >= 0) else f'`i = {S.i}` 或 `j = {S.j}` 越界：没有剩余元素 → 结束'),
        'if grid[i][j] < 0': lambda S, B, r: (f'`grid[{S.i}][{S.j}] = {S.grid[S.i][S.j]} < 0`：它是这一列里最大的剩余数，已经是负数 → 它下面都更小' if S.grid[S.i][S.j] < 0 else f'`grid[{S.i}][{S.j}] = {S.grid[S.i][S.j]} >= 0`：它是这一行里最小的剩余数，已经非负 → 这一行左边都更大'),
        'ans += m - i': '这一列从第 `{i}` 行到底共 `{m} - {i} = {m - i}` 个都是负数：`ans` → =={ans}==',
        'j -= 1': '这一列处理完，排除；`j` 左移到 `{j}`',
        'i += 1': '这一行剩下的全都非负，排除；`i` 下移到 `{i}`',
        'return ans': '一共 `{ans}` 个负数',
    },
    cards=dict(
        one_liner='右上角既是行最大、又是列最小：一次比较就能排除一整行或一整列',
        complexity='时间 `O(m + n)`，空间 `O(1)`',
        problem=['`m*n` 矩阵，每行每列都非严格递减，统计负数个数',
                 '进阶：`O(m + n)`',
                 '本视频：4×4 示例 → `8`'],
        quote='利用 grid 行列有序的性质，我们可以用 O(1) 的时间获取 O(m) 或 O(n) 的信息。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从右上角 `(0, n-1)` 出发：它在行里最大、在列里最小',
              '若它是负数：这一列从它往下全是负数，一次加 `m - i`，`j` 左移',
              '若它非负：这一行从它往左全非负，`i` 下移；每步排除一行或一列'],
        summary=['时间 `O(m + n)`，空间 `O(1)`：每步 `i` 增或 `j` 减',
                 '负数时是加 `m - i`（剩余整列），不是加 1',
                 '也可以从左下角开始，方法类似',
                 '同类题：240 搜索二维矩阵 II'],
    ),
)
