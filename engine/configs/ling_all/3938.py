G = [[4, -2, -3], [-1, -3, -1], [-4, 2, -1]]


def _line_of(S):
    """当前 maxSubArray 正在扫的是哪一行/列：('r', i) / ('c', j) / None"""
    g, nums = S['grid'], S.get('nums')
    if nums is None:
        return None
    for r in range(len(g)):
        if g[r] is nums:
            return ('r', r)
    if 'col' in S:
        for c in range(len(g[0])):
            if [row[c] for row in g] == nums:
                return ('c', c)
    return None


def _gcolor(S, i, j, v):
    ln = _line_of(S)
    if ln is None:
        g = S['grid']
        if S['_line'] == 19 and 0 < i < len(g) - 1 and 0 < j < len(g[0]) - 1:
            return 'yellow'
        return None
    k, idx = ln
    return 'blue' if (k == 'r' and i == idx) or (k == 'c' and j == idx) else None


def _txt(S):
    if 'f' not in S or 'nums' not in S:
        return '答案 = 所有行、所有列里「长度 >= 2 的最大子数组和」（边界上的单格不能算）'
    return f"`f = {S['f']}`（以前一个数结尾的最大和），`ans = {S['ans']}`"


CONFIG = dict(
    num=3938, title='矩阵中最大共享路径和', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='转化成每行每列的最大子数组和（长度>=2）',
    tags=['一、入门 DP', '难度分 2252'],
    code='''
# 手写 max 更快
fmax = lambda a, b: b if b > a else a

class Solution:
    # 53. 最大子数组和（子数组长度 >= 2）
    def maxSubArray(self, nums: list[int]) -> int:
        ans = -inf  # 注意答案可以是负数，不能初始化成 0
        f = nums[0]
        for x in nums[1:]:
            ans = fmax(ans, f + x)  # f+x 保证子数组至少有两个数
            f = fmax(f, 0) + x
        return ans

    def maxScore(self, grid: list[list[int]]) -> int:
        ans = -inf

        # 单独计算子数组长为 1 的情况，此时子数组不能在 grid 的边界上
        if len(grid) > 2 and len(grid[0]) > 2:
            ans = max(max(row[1: -1]) for row in grid[1: -1])

        # 每行的最大子数组和（子数组长度 >= 2）
        for row in grid:
            ans = fmax(ans, self.maxSubArray(row))

        # 每列的最大子数组和（子数组长度 >= 2）
        for col in zip(*grid):
            ans = fmax(ans, self.maxSubArray(list(col)))

        return ans
''',
    call=f'Solution().maxScore({G})',
    expect=3,
    skip=['f = nums[0]', 'for row in grid:', 'for col in zip', 'ans = -inf'],
    views=[
        dict(type='grid', var='grid', label='grid（黄 = 内部单格；蓝 = 正在扫的行/列）', cell=100, h=330, color=_gcolor),
        dict(type='array', var='nums', label='nums（当前这一行/列）', cell=84, h=150),
        dict(type='text', fn=_txt, size=26, h=60),
    ],
    watch=[('x', 'x', 'blue'), ('f', 'f', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = -inf': '答案可能是负数，不能初始化成 0，所以用 `-inf`',
        'if len(grid) > 2': '行列都 > 2 才有内部格子；3 行 3 列，内部只有中间 1 格',
        'ans = max(max(row[1: -1])': '先算长度为 1 的情况：只有==不在边界上==的格子才能单独当共享格 → 内部最大值 `ans = {ans}`',
        'ans = fmax(ans, self.maxSubArray(row))': '`ans = fmax(ans, 这一行的最大子数组和)`：行里长度 >= 2 的最大和与 `ans` 取较大者 → {ans}',
        'ans = fmax(ans, self.maxSubArray(list(col)))': '`ans = fmax(ans, 这一列的最大子数组和)`：列里长度 >= 2 的最大和与 `ans` 取较大者 → {ans}',
        'ans = fmax(ans, f + x)': '`f + x = {f} + {x}` = {f + x}：==至少两个数==的子数组和，更新 `ans` → {ans}',
        'f = fmax(f, 0) + x': '`f = max(f, 0) + x`：前面和为负就丢掉 → `f` = =={f}==',
        'return ans': lambda S, B, r: (f'返回最大和 `{r}`' if 'f' in S and S._line == 12 else f'所有行列取最大，答案 `{r}`'),
    },
    cards=dict(
        one_liner='两条路径的交集一定是一段水平或竖直线段',
        complexity='时间 `O(mn)`，空间 `O(m)` 或 `O(1)`',
        problem=['`m x n` 矩阵，玩家 1 从左上走到右下（右/下），玩家 2 从左下走到右上（右/上）',
                 '两条路径经过的相同格子叫共享格，求共享格之和的最大值',
                 '本视频：`[[4,-2,-3],[-1,-3,-1],[-4,2,-1]]` → `3`'],
        quote='两人的移动路径，可以分别视作一个减函数和一个增函数（非严格）。所以交集要么是水平的一段，要么是垂直的一段。',
        quote_src='—— 灵茶山艾府题解',
        idea=['问题等价于每行每列的最大子数组和（第 53 题）',
              '交点不能在边界上（只能形如卐字），所以边界上的子数组长度至少为 2',
              '先单独算内部单格的最大值，再对每行每列求长度 >= 2 的最大子数组和'],
        summary=['时间 `O(mn)`：每个格子在其行、列各扫一次',
                 '易错：`ans` 初始为 `-inf`，答案可以为负',
                 '长度 >= 2：先 `ans = max(ans, f + x)` 再更新 `f`，顺序不能反',
                 '本视频用 `fmax` 手写 max 的原版代码；题解另有前缀和写法'],
    ),
)
