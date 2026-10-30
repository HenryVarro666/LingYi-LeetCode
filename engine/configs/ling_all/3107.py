CONFIG = dict(
    num=3107, title='使数组中位数等于 K 的最少操作数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='排序 + 中位数一侧调整', tags=['灵神题单', '难度分 1605'],
    code='''
class Solution:
    def minOperationsToMakeMedianK(self, nums: List[int], k: int) -> int:
        nums.sort()
        m = len(nums) // 2
        ans = 0
        if nums[m] > k:
            for i in range(m, -1, -1):
                if nums[i] <= k:
                    break
                ans += nums[i] - k
        else:
            for i in range(m, len(nums)):
                if nums[i] >= k:
                    break
                ans += k - nums[i]
        return ans
''',
    call='Solution().minOperationsToMakeMedianK([2,5,6,8,5], 7)',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"中位数 nums[{S['m']}] = {S['nums'][S['m']]}，目标 k = {S['k']}" if 'm' in S else f"目标 k = {S['k']}"), size=32),
        dict(type='array', var='nums', label='nums（排序后）', pointers={'m': 'pink', 'i': 'blue'}, h=240,
             color=lambda S, i, v: ('pink' if 'm' in S and i == S['m'] else None)),
        dict(type='text', fn=lambda S: f"累计操作 ans = {S['ans']}" if 'ans' in S else '', size=30),
    ],
    watch=['k', 'm', 'i', ('ans', 'ans', 'green')],
    captions={
        'nums.sort()': '排序后中位数就在下标 `n // 2`：`{nums}`',
        'm = len': '中位数下标 `m = {m}`，`nums[m] = {nums[m]}`',
        'ans = 0': '`ans` 累加每个数的变化量',
        'if nums[m] > k': lambda S, B, r: (f'`nums[m] = {S.nums[S.m]} > k = {S.k}`：中位数偏大 → 只需处理 `[0, m]` 里大于 k 的数，右边本来就 > k' if S.nums[S.m] > S.k
                                           else f'`nums[m] = {S.nums[S.m]} <= k = {S.k}`：中位数偏小 → 只需处理 `[m, n-1]` 里小于 k 的数，左边本来就 < k'),
        'for i in range(m, -1, -1)': '从 `m` 往左看',
        'for i in range(m, len(nums))': '从 `m` 往右看，`i = {i}`',
        'if nums[i] <= k': lambda S, B, r: (f'`nums[{S.i}] = {S.nums[S.i]} <= k = {S.k}`：已满足；有序，更左边的更不用动 → 停' if S.nums[S.i] <= S.k else f'`nums[{S.i}] = {S.nums[S.i]} > k = {S.k}`：偏大，要降到 k'),
        'if nums[i] >= k': lambda S, B, r: (f'`nums[{S.i}] = {S.nums[S.i]} >= k = {S.k}`：已满足；有序，更右边的更不用动 → 停' if S.nums[S.i] >= S.k else f'`nums[{S.i}] = {S.nums[S.i]} < k = {S.k}`：偏小，要升到 k'),
        'break': '后面都已满足，退出循环',
        'ans += nums[i] - k': '`nums[{i}] = {nums[i]}` 降到 `k`：代价 `{nums[i]} - {k} = {nums[i]-k}` → `ans = {ans}`',
        'ans += k - nums[i]': '`nums[{i}] = {nums[i]}` 升到 `k`：代价 `{k} - {nums[i]} = {k-nums[i]}` → `ans = {ans}`',
        'return ans': '总操作数 `{ans}`',
    },
    cards=dict(
        one_liner='排序后，只把中位数一侧「不合格」的数改成 k',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['每次操作可让任一元素 `+1` 或 `-1`，使数组中位数变为 `k`，求最少操作数',
                 '偶数长度时取中间两个数里较大的',
                 '示例：`[2,5,6,8,5], k=7` → `3`'],
        quote='我们需要把中位数左边的数都变成 ≤ k 的，右边的数都变成 ≥ k 的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后中位数是 `nums[m]`，`m = n // 2`',
              '`nums[m] > k`：下标 `[0,m]` 中大于 k 的数改成 k，右侧已经大于 k',
              '否则：下标 `[m,n-1]` 中小于 k 的数改成 k，左侧已经小于 k',
              '累加变化量即答案'],
        summary=['时间 `O(n log n)`，用快速选择可做到期望 `O(n)`',
                 '易错：偶数长度取较大的中间数，所以 `m = n // 2`',
                 '遇到已满足的数就 `break`，因为数组有序',
                 '思考题：10^5 个询问 k，可用前缀和 + 二分'],
    ),
)
