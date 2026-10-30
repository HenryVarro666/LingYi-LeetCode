CONFIG = dict(
    num=3107, title='使数组中位数等于 K 的最少操作数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='排序 + 分三种情况', tags=['灵神题单', '贪心与思维', '难度分 1605'],
    code='''
class Solution(object):
    def minOperationsToMakeMedianK(self, nums, k):

        nums.sort()
        n = len(nums)
        
        res = 0

        if nums[n // 2] < k:
            for v in nums[n // 2:]:
                res += max(k - v, 0)
        elif nums[n // 2] > k:
            for v in nums[:n // 2 + 1]:
                res += max(v - k, 0)
        
        return res
''',
    call='Solution().minOperationsToMakeMedianK([2,5,6,8,5,9], 9)',
    expect=4,
    views=[
        dict(type='text', fn=lambda S: (f"nums[n//2] = {S['nums'][S['n']//2]}，目标 k = {S['k']}" if 'n' in S else f"目标 k = {S['k']}"), size=32),
        dict(type='array', var='nums', label='nums（排序后）', h=240,
             color=lambda S, i, v: ('pink' if 'n' in S and i == S['n'] // 2 else None)),
        dict(type='text', fn=lambda S: f"累计代价 res = {S['res']}" if 'res' in S else '', size=30),
    ],
    watch=['k', 'n', 'v', ('res', 'res', 'green')],
    captions={
        'nums.sort()': '先排序，中位数就是 `nums[n // 2]`：`{nums}`',
        'n = len': '`n = {n}`，中位数下标 `n // 2 = {n // 2}`',
        'res = 0': '`res` 累加代价',
        'if nums[n // 2] < k': lambda S, B, r: (f'`nums[{S.n//2}] = {S.nums[S.n//2]} < k = {S.k}`：情况 1，中位数要升到 k；它后面也可能 < k' if S.nums[S.n // 2] < S.k
                                                else f'`nums[{S.n//2}] = {S.nums[S.n//2]} < k = {S.k}` 不成立，看下一种情况'),
        'elif nums[n // 2] > k': lambda S, B, r: (f'`nums[{S.n//2}] = {S.nums[S.n//2]} > k = {S.k}`：情况 2，与情况 1 对称，处理前半部分' if S.nums[S.n // 2] > S.k
                                                  else '等于 k：情况 3，无需操作，答案 0'),
        'for v in nums[n // 2:]': '遍历后半部分，取 `v = {v}`',
        'for v in nums[:n // 2 + 1]': '遍历前半部分（含中位数），取 `v = {v}`',
        'res += max(k - v, 0)': '`max({k} - {v}, 0) = {max(k - v, 0)}`：小于 k 才要抬到 k → `res = {res}`',
        'res += max(v - k, 0)': '`max({v} - {k}, 0) = {max(v - k, 0)}`：大于 k 才要降到 k → `res = {res}`',
        'return res': '最少操作 `{res}`',
    },
    cards=dict(
        one_liner='中位数必须成为 k：把后半部分比 k 小的数全抬到 k',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['每次可把任一数 `+1` 或 `-1`，求让中位数等于 `k` 的最少操作数',
                 '示例：`[2,5,6,8,5], k=7` → `3`',
                 '本视频：`[2,5,6,8,5,9], k=9`（偶数长度）→ `4`'],
        quote='此时只需遍历数组的前半部分，计算将其中所有大于k的整数变为k的代价并累加即可。',
        quote_src='—— yiduobo 题解原文（情况 2）',
        idea=['排序后中位数是 `nums[n // 2]`',
              '情况 1：它小于 k，它必须变成 k，它后面小于 k 的也要变',
              '情况 2：它大于 k，与情况 1 对称，改前半部分',
              '情况 3：等于 k，不用动，答案 0'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '易错：前半部分切片要含中位数，写作 `nums[:n // 2 + 1]`',
                 '用 `max(…, 0)` 一并跳过已满足的数，不用 break',
                 '原文已是 `//`，无需改动'],
    ),
)
