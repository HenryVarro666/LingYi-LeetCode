CONFIG = dict(
    num=3904, title='最小稳定下标 II', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解 · 后缀最小值数组 + 前缀最大值变量',
    tags=['灵神题单', '动态规划', '难度分 1352'],
    code='''
class Solution:
    def firstStableIndex(self, nums: list[int], k: int) -> int:
        n = len(nums)
        suf_min = [0] * n  # 后缀最小值
        suf_min[-1] = nums[-1]
        for i in range(n - 2, -1, -1):
            suf_min[i] = min(suf_min[i + 1], nums[i])

        pre_max = 0  # 前缀最大值
        for i, x in enumerate(nums):
            pre_max = max(pre_max, x)
            if pre_max - suf_min[i] <= k:
                return i
        return -1
''',
    call='Solution().firstStableIndex([5,0,1,4,6,7], 3)',
    expect=3,
    views=[
        dict(type='text', size=26, fn=lambda S: (f"下标 `{S['i']}`：不稳定值 = `{S['pre_max']} − {S['suf_min'][S['i']]}` = =={S['pre_max'] - S['suf_min'][S['i']]}==（k = {S['k']}）"
                                                 if 'pre_max' in S and 'x' in S and S['_line'] >= 9 else '先倒序算出每个后缀的最小值')),
        dict(type='array', var='nums', label='nums', pointers={'i': 'blue'}, h=200,
             color=lambda S, i, v: 'green' if 'pre_max' in S and 'x' in S and S['_line'] >= 9 and i <= S['i'] else None),
        dict(type='array', var='suf_min', label='suf_min[i]：后缀 [i, n-1] 的最小值', pointers={'i': 'pink'}, h=200,
             color=lambda S, i, v: 'cyan' if 'pre_max' not in S and i >= S['i'] else None),
    ],
    watch=['i', 'k', ('pre_max', 'pre_max', 'orange')],
    captions={
        'suf_min = [0]': '准备数组 `suf_min`，`suf_min[i]` 表示 `nums[i:]` 的最小值',
        'suf_min[-1]': '最后一个后缀只有 `nums[-1]`，最小值就是 =={nums[-1]}==',
        'suf_min[i] =': '倒序：`suf_min[{i}] = min(suf_min[{i+1}], nums[{i}]) = =={suf_min[i]}==`',
        'pre_max = 0': '`pre_max` 维护前缀最大值；`nums[i] >= 0`，所以初始 0 没问题',
        'for i, x': '正序枚举 `i`，`x = nums[{i}] = {x}`',
        'pre_max = max': '`pre_max = max({B.pre_max}, {x})` = =={pre_max}==：现在是 `nums[0..{i}]` 的最大值',
        'if pre_max': '不稳定值 `{pre_max} - {suf_min[i]} = {pre_max - suf_min[i]}`，和 `k = {k}` 比 → {"==稳定==，就是第一个" if pre_max - suf_min[i] <= k else "太大，继续往右"}',
        'return i': '第一个稳定下标是 =={i}==',
        'return -1': '都不稳定，返回 `-1`',
    },
    cards=dict(
        one_liner='前缀最大值 − 后缀最小值，第一个 ≤ k 的下标',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['不稳定值 = `max(nums[0..i]) - min(nums[i..n-1])`，不超过 `k` 的下标叫稳定下标',
                 '求最小的稳定下标，没有返回 `-1`',
                 '示例：`nums=[5,0,1,4], k=3` → `3`；本视频用 `[5,0,1,4,6,7]`'],
        quote='倒序遍历 nums，可以求出每个后缀 [i,n-1] 的最小值 sufMin[i]。答案为第一个满足 preMax[i] - sufMin[i] <= k 的下标 i。',
        quote_src='—— 灵茶山艾府题解',
        idea=['倒着扫一遍，把每个后缀的最小值存进 `suf_min`',
              '正着扫的同时用一个变量维护前缀最大值，不必再开数组',
              '遇到第一个满足条件的 `i` 立即返回'],
        summary=['时间 `O(n)`，空间 `O(n)`（`suf_min`）',
                 '前缀最大值边扫边算，`pre_max` 更新后才是 `[0,i]` 的最大值，别用旧值',
                 '前后缀分解：同类题见灵神动态规划题单「前后缀分解」专题'],
    ),
)
