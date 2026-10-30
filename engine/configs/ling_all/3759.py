CONFIG = dict(
    num=3759, title='统计合格元素的数目', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='排序 + 二分（小于第 k 大的个数）',
    code='''
class Solution:
    def countElements(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if k == 0:
            return n
        nums.sort()
        return bisect_left(nums, nums[-k])  # 小于第 k 大的元素个数
''',
    call='Solution().countElements([5,7,5,2,9,4], 3)',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums', h=200, cell=90,
             pointers=dict(),
             color=lambda S, i, v: ('green' if S.get('_line') == 7 and v < S['nums'][-S['k']] else 'pink' if S.get('_line') == 7 and i == len(S['nums']) - S['k'] else None) if 'k' in S else None),
        dict(type='text', size=28, h=70, fn=lambda S: (f"第 `k = {S['k']}` 大是 `nums[-{S['k']}]` = =={S['nums'][-S['k']]}==；比它小的才合格" if S.get('_line') in (7,) and S['k'] > 0 else ('排序后：小于第 k 大的数全部合格' if S.get('_line') == 6 else ''))),
    ],
    watch=['n', 'k'],
    captions={
        'n = len': '`n = {n}`，`k = {k}`',
        'if k == 0': lambda S, B, r: ('`k = 0`：不需要有更大的数 → 所有元素都合格，返回 n' if S.k == 0 else '`k = {}`，不是 0，往下走'.format(S.k)),
        'nums.sort': '升序排序：`{nums}`。第 `k` 大的数就是 `nums[-{k}]`',
        'bisect_left': '第 {k} 大是 `nums[-{k}] = {nums[-k]}`；==严格小于它的元素有 {ret} 个==，最大的 {k} 个数都 ≥ 第 k 大 > 它们，所以它们都合格',
    },
    cards=dict(
        after=[dict(heading='lowerBound 速查表（灵神附表）', lines=['`< x` 的个数：`bisect_left(nums, x)`', '`<= x` 的个数：`bisect_left(nums, x + 1)`', '`>= x` 的个数：`n - bisect_left(nums, x)`', '`> x` 的个数：`n - bisect_left(nums, x + 1)`', '`< x` 与 `>= x` 互为补集，个数之和为 `n`'])],
        one_liner='小于“第 k 大”的数，都有至少 k 个数比它大',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['`nums` 里某个元素合格：至少有 `k` 个元素严格大于它',
                 '返回合格元素的总数',
                 '本视频：`nums = [5,7,5,2,9,4]`，`k = 3` → `2`'],
        quote='小于 nums 第 k 大的数都是满足要求的数。……特判 k=0，所有元素都满足要求，返回 n。',
        quote_src='—— 灵茶山艾府题解',
        idea=['升序排序后，第 `k` 大的数在 `nums[-k]`',
              '比它严格小的数，前面至少有 `k` 个元素更大 → 合格；等于或大于它的不合格',
              '“严格小于 x 的个数”正是 `bisect_left(nums, x)`'],
        summary=['时间 `O(n log n)`（排序），空间 `O(1)`',
                 '易错：`k = 0` 时 `nums[-0]` 是 `nums[0]`，必须特判，直接返回 n',
                 '用 `bisect_left` 而不是 `bisect_right`：相等的元素不算合格',
                 '也可用快速选择求第 k 大，再遍历统计，做到 `O(n)`'],
    ),
)
