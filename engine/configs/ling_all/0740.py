def _txt(S):
    if 'f1' not in S or 'f0' not in S:
        return '`a[v]` = nums 中等于 `v` 的元素之和；再对 `a` 做打家劫舍'
    if S.get('_line') == 6:
        return f'`f0` = 选到前一个的最优，`f1` = 当前最优；这一格 `x = {S["x"]}`：`max({S["f1"]}, {S["f0"]} + {S["x"]})`'
    return f'`f0 = {S["f0"]}`，`f1 = {S["f1"]}`'


CONFIG = dict(
    num=740, title='删除并获得点数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='值域数组 + 打家劫舍',
    tags=['灵神核心路线', '灵神题单·动态规划'],
    code='''
class Solution:
    # 198. 打家劫舍
    def rob(self, nums: List[int]) -> int:
        f0 = f1 = 0
        for x in nums:
            f0, f1 = f1, max(f1, f0 + x)
        return f1

    def deleteAndEarn(self, nums: List[int]) -> int:
        a = [0] * (max(nums) + 1)
        for x in nums:
            a[x] += x  # 统计等于 x 的元素之和
        return self.rob(a)
''',
    call='Solution().deleteAndEarn([2,2,3,3,3,4])',
    expect=9,
    views=[
        dict(type='array', var='nums', label='输入 nums（在 rob 里是值域数组 a）', h=170, cell=90),
        dict(type='array', var=lambda S: S.get('a'), label='值域数组 a（下标 = 数值，格子 = 该数值的元素之和）', h=190, cell=90,
             color=lambda S, i, v: 'green' if v and S.get('_line') == 12 and i == S.get('x') else None),
        dict(type='text', fn=_txt, size=26, h=80),
    ],
    watch=['x', ('f0', 'f0', 'blue'), ('f1', 'f1', 'green')],
    captions={
        'a = [0] * (max(nums) + 1)': '值域数组：下标 `0..{max(nums)}`，`a[v]` 先全部置 0',
        'for x in nums': '轮到 `x = {x}`',
        'a[x] += x': '遇到 `x = {x}`：`a[{x}]` 累加成 =={a[x]}==；选 `{x}` 就要把它们全选',
        'f0, f1 = f1, max': '`max(不选 {B.f1}，选 {B.f0} + {x})` → `f1 = {f1}`；`f0` 变成旧 `f1 = {f0}`',
        'return f1': '最优总点数 = =={ret}==',
        'return self.rob(a)': '值域数组 `a` 交给打家劫舍：相邻数值不能同时选',
    },
    cards=dict(
        one_liner='选了 x 就得全选 x；相邻数值不能都选，化成打家劫舍',
        complexity='时间 `O(n+U)`，空间 `O(U)`（U 为最大值）',
        problem=['选 `nums[i]` 得 `nums[i]` 分，同时删光所有 `nums[i]±1`',
                 '求最多能得多少分',
                 '示例：`[2,2,3,3,3,4]` → `9`（把三个 3 全选）'],
        quote='所以如果要选 3，所有的 3 都要选。这种「相邻数字不能都选」联想到 198. 打家劫舍。',
        quote_src='—— 灵茶山艾府题解',
        idea=['选了一个 3，2 和 4 都没了，剩下的 3 还能继续选',
              '转成值域数组 `a[i]` = 等于 `i` 的元素之和，如 `[0,0,4,9,4]`',
              '对 `a` 跑一遍打家劫舍，滚动变量 `f0, f1` 即可'],
        summary=['时间 `O(n+U)`，空间 `O(U)`',
                 '`a` 长度要开 `max(nums) + 1`，下标才对得上数值',
                 '值域更大（到 10^9）时，只对出现过的数排序做 DP，即 3186 题'],
    ),
)
