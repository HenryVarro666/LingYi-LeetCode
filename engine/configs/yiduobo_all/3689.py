CONFIG = dict(
    num=3689, title='最大子数组总值 I', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='取整个数组 k 次',
    tags=['灵神题单', '难度分 1371'],
    code='''
class Solution(object):
    def maxTotalValue(self, nums, k):
        
        return (max(nums) - min(nums)) * k
''',
    call='Solution().maxTotalValue([4,2,5,1], 3)',
    expect=12,
    views=[
        dict(type='array', var='nums', h=240, label='nums（整个数组：上限的最大值与下限的最小值）',
             color=lambda S, i, v: ('green' if v == max(S['nums']) else 'red' if v == min(S['nums']) else None) if 'nums' in S else None),
        dict(type='text', fn=lambda S: f"最大值 `{max(S['nums'])}`，最小值 `{min(S['nums'])}`，差 =={max(S['nums'])-min(S['nums'])}== 取 `{S['k']}` 次" if 'nums' in S else ''),
    ],
    watch=['k', ('max', 'max(nums)', 'green'), ('min', 'min(nums)', 'red')],
    captions={
        'return': '直接取原数组 `{k}` 次：每次值都是 `{max(nums)} - {min(nums)} = {max(nums) - min(nums)}`，总和 =={ret}==',
    },
    cards=dict(
        one_liner='每个子数组都取整个数组，值最大，共取 k 次',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['从 `nums` 里选恰好 `k` 个子数组，可重叠、可重复',
                 '子数组的值是最大值减最小值，求总值最大',
                 '示例：`[4,2,5,1]`，`k = 3` → `12`'],
        quote='直接取原数组，此时的最大值就是原数组的最大值，也就是所有子数组可能取到的最大值的上限，而最小值就是原数组的最小值。',
        quote_src='—— yiduobo 题解原文',
        idea=['想让每个子数组的值最大：最大值尽量大，最小值尽量小',
              '原数组的最大值是上限，最小值是下限，取整个数组同时达到',
              '又能重复取，所以取 k 次，答案 = (最大 − 最小) × k'],
        after=[dict(heading='逐步验证', lines=['示例 `[4,2,5,1]`，`k = 3`', '取 `nums[0..3]`：`5 − 1 = 4`', '再取两次同一个子数组，也是 `4`', '总和 `4 × 3 = 12`'])],
        before=[dict(heading='先看一个小例子', lines=['`nums = [1,3,2]`，`k = 2`', '要让每个子数组的值尽可能大', '原数组的最大值和最小值同时出现在整个数组里', '所以取两次整个数组：`2 + 2 = 4`'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '“上限、下限同时取到”是贪心的依据',
                 '`k` 可以大于子数组种类数，因为允许重复'],
    ),
)
