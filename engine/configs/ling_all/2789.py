CONFIG = dict(
    num=2789, title='合并后数组中的最大元素', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='倒序遍历 · 向左合并',
    tags=['灵神题单', '难度分 1485'],
    code='''
class Solution:
    def maxArrayValue(self, nums: List[int]) -> int:
        s = nums[-1]
        for i in range(len(nums) - 2, -1, -1):
            s = s + nums[i] if nums[i] <= s else nums[i]
        return s
''',
    call='Solution().maxArrayValue([4,30,3,3,9,2,7])',
    expect=34,
    views=[
        dict(type='text', size=34, fn=lambda S: (f"当前合并值 `s = {S['s']}`" + (f"，左边 `nums[{S['i']}] = {S['nums'][S['i']]}`" if 'i' in S else '')) if 's' in S else ''),
        dict(type='array', var='nums', pointers={'i': 'blue'}, h=300,
             color=lambda S, k, v: 'green' if 'i' in S and k > S['i'] and False else None),
    ],
    watch=[('i', 'i', 'blue'), ('s', 's', 'green')],
    captions={
        's = nums[-1]': '从最右边开始向左合并：`s = nums[-1] = {s}`',
        'for i in range': '看左边的 `nums[{i}] = {nums[i]}`，`s = {s}`',
        's = s + nums[i]': lambda S, B, r: (f'`nums[{S.i}] = {S.nums[S.i]} <= s = {B.s}`：能合并 → `s` = =={S.s}==' if S.nums[S.i] <= B.s else f'`nums[{S.i}] = {S.nums[S.i]} > s = {B.s}`：合不了；从 `{S.i}` 开始向左合并更大 → `s` = =={S.s}=='),
        'return s': '最大元素 `{s}`',
    },
    cards=dict(
        one_liner='倒着合并：越合越大，且合不动时就重新从左边开始',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['若 `nums[i] <= nums[i+1]`，可把 `nums[i+1]` 换成两者之和并删掉 `nums[i]`',
                 '操作任意次，求最终数组中的最大元素',
                 '示例：`[2,3,7,9,3]` → `21`；本视频：`[4,30,3,3,9,2,7]` → `34`'],
        quote='如果 nums[i] > sum，无法合并，并且这意味着从 i 开始向左合并可以得到比 sum 更大的元素和，所以直接更新 sum = nums[i]，继续向左合并。',
        quote_src='—— 灵茶山艾府题解',
        idea=['暴力：枚举从每个 `i` 开始向左合并，`O(n^2)`',
              '从 `n-1` 合并到 `j` 停下，说明 `nums[j-1]` 比后面的和还大',
              '所以中间那些起点都不会更优 → 直接从 `j-1` 接着合并，一趟搞定'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '条件是 `nums[i] <= s`（可以相等）',
                 '题解还给了原数组上合并的写法：`nums[i-1] += nums[i]`',
                 '易错：不能正向合并，合并值变大反而更难继续'],
    ),
)
