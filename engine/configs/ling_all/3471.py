CONFIG = dict(
    num=3471, title='找出最大的几近缺失整数', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='分类讨论 · 只看首尾元素',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution:
    def f(self, nums: List[int], x: int) -> int:
        return -1 if x in nums else x

    def largestInteger(self, nums: List[int], k: int) -> int:
        if k == len(nums):
            return max(nums)
        if k == 1:
            ans = -1
            for x, c in Counter(nums).items():
                if c == 1:
                    ans = max(ans, x)
            return ans
        # nums[0] 不能出现在其他地方，nums[-1] 同理
        return max(self.f(nums[1:], nums[0]), self.f(nums[:-1], nums[-1]))
''',
    call='Solution().largestInteger([3,9,7,2,1,7], 4)',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（只有首尾可能满足）', cell=90),
        dict(type='text', size=28, fn=lambda S: f"`k = {S['k']}`，`len(nums) = {len(S['nums'])}`" if 'k' in S else ''),
    ],
    watch=[('k', 'k', 'blue'), ('x', 'x', 'pink')],
    captions={
        'if k == len': lambda S, B, r: (f'`k = {S.k} == len(nums)`：只有一个子数组，取最大值' if S.k == len(S.nums)
                                        else f'`k = {S.k} ≠ len(nums) = {len(S.nums)}`：不止一个子数组'),
        'if k == 1': lambda S, B, r: ('`k = 1`：数出现一次的最大元素' if S.k == 1 else f'`k = {S.k}`，不是 1 → 属于 1 < k < n'),
        'return -1 if x': lambda S, B, r: (f'`{S.x}` 在 `nums` 其他位置也出现了 → 至少落在两个子数组里 → `-1`' if ret == -1
                                           else f'`{S.x}` 在其他位置没出现过 → 满足要求，返回 `{S.x}`'),
        'return max(self.f': '其他元素至少出现在两个子数组里，只看首尾：先算 `f(nums[1:], {nums[0]})`，再算 `f(nums[:-1], {nums[-1]})`，取较大者',
    },
    cards=dict(
        one_liner='1 < k < n 时，只有首尾两个数可能满足',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`x` 恰好只出现在 `nums` 的一个长为 `k` 的子数组中，称为几近缺失整数',
                 '返回最大的几近缺失整数，没有返回 `-1`',
                 '本视频：`[3,9,7,2,1,7]`，`k=4` → `3`'],
        quote='如果 1<k<n，只有 nums[0] 和 nums[n−1] 是可能满足要求的数，因为其他元素至少出现在两个子数组中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`k = n`：只有一个子数组，所有数都满足，取最大值',
              '`k = 1`：每个元素自成一个子数组，只有出现次数为 1 的满足',
              '`1 < k < n`：中间元素必在两个子数组里，只检查首尾是否在别处出现过'],
        after=[dict(heading='本例怎么算', lines=['首元素 `3`：去掉自己后 `[9,7,2,1,7]` 里没有 3 → 满足', '尾元素 `7`：去掉自己后 `[3,9,7,2,1]` 里还有 7 → 排除（返回 -1）', '`max(3, -1) = 3`'])],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '首尾要检查的是整个数组里有没有==别的位置==的同值，所以用切片去掉自己',
                 '示例中末尾 `7` 在下标 2 也出现，所以排除，答案是 `3`'],
    ),
)
