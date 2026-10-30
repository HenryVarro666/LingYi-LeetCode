CONFIG = dict(
    num=1005, title='K 次取反后最大化的数组和', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='排序 · 优先改最小的负数',
    tags=['贪心与思维', '难度分 1275'],
    code='''
class Solution:
    def largestSumAfterKNegations(self, nums: List[int], k: int) -> int:
        nums.sort()  # 从小到大排序

        for i, x in enumerate(nums):  # 优先改最小的
            if k == 0 or x >= 0:  # 修改次数用尽，或者负数已全部取反
                break
            nums[i] *= -1  # 负数取反
            k -= 1  # 消耗一次修改次数

        # 如果剩余的 k 是奇数，选最小的数取反
        return sum(nums) - (min(nums) * 2 if k % 2 else 0)
''',
    call='Solution().largestSumAfterKNegations([2,-3,-1,5], 3)',
    expect=9,
    views=[
        dict(type='array', var='nums', label='nums（排序后，负数在最左边）', pointers={'i': 'blue'}, h=230, cell=100,
             color=lambda S, i, v: 'green' if 'i' in S and i < S['i'] and False else None,
             dim=lambda S, i, v: False),
        dict(type='text', h=110, size=30,
             fn=lambda S: (f"剩余修改次数 `k = {S['k']}`，当前数组和 `{sum(S['nums'])}`" if 'k' in S else '')),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'pink'), ('k', 'k', 'orange')],
    captions={
        'nums.sort()': '从小到大排序：`{nums}`。越靠左的负数绝对值越大，取反收益越大',
        'for i, x in enumerate': lambda S, B, r: (f'看 `nums[{S.i}] = {S.x}`' if 'i' not in B or S.i != B.i else '遍历结束'),
        'if k == 0 or x >= 0': lambda S, B, r: ('`k = 0`：次数用完，停止' if S.k == 0
                                                else (f'`x = {S.x} >= 0`：负数已经全改完，停止' if S.x >= 0
                                                      else f'`x = {S.x} < 0` 且 `k = {S.k}`：取反能让和变大')),
        'break': '跳出循环，剩下的 `k` 是 `{k}`',
        'nums[i] *= -1': '`{x}` 取反 → `nums[{i}] = {nums[i]}`',
        'k -= 1': '用掉一次修改：`k = {k}`',
        'return sum': lambda S, B, r: (f'剩余 `k = {S.k}` 是奇数：必须再强行取反一次，改==最小的数== `{min(S.nums)}`，和减去 `2 × {min(S.nums)}` → `{r}`'
                                       if S.k % 2 else f'剩余 `k = {S.k}` 是偶数：同一个数取反偶数次不变 → `{r}`'),
    },
    cards=dict(
        one_liner='优先把最小的负数变正，剩下的次数看奇偶',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['恰好做 `k` 次：选一个下标，把 `nums[i]` 变成 `-nums[i]`（可重复选）',
                 '求操作后数组的最大和',
                 '本视频：`nums = [2,-3,-1,5], k = 3` → `9`'],
        quote='贪心地，优先改更小的负数（绝对值更大的负数），这样可以让元素和更大。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`k` 不超过负数个数：把最小的 `k` 个负数取反',
              '`k` 更大：负数全取反，剩余 `k` 为偶数则没有影响',
              '剩余 `k` 为奇数：必须强改一个数，改当前最小的，和减去 `2 × min`'],
        summary=['时间 `O(n log n)`，空间 `O(1)`（用快速选择可做到 `O(n)`）',
                 '循环结束后 `min(nums)` 要在取反之后再求',
                 '易错：剩余 `k` 为偶数时不用做任何事',
                 '写法二：一次遍历同时累加 `total` 和维护最小值 `mn`，思路相同'],
    ),
)
