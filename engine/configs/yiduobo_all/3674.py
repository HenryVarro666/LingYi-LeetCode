CONFIG = dict(
    num=3674, title='数组元素相等的最小操作次数', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='判断是否已全相等',
    tags=['灵神题单', '难度分 1369'],
    code='''
class Solution(object):
    def minOperations(self, nums):
        
        for v in nums[1:]:
            if v != nums[0]:
                return 1
        
        return 0
''',
    call='Solution().minOperations([5,5,3,5,6])',
    expect=1,
    views=[
        dict(type='array', var='nums', h=240, label='nums（红 = 和 nums[0] 不同）',
             color=lambda S, i, v: 'red' if 'nums' in S and v != S['nums'][0] else None),
        dict(type='text', fn=lambda S: f"当前检查 `v = {S['v']}`，对比 `nums[0] = {S['nums'][0]}`" if 'v' in S else ''),
    ],
    watch=['v'],
    captions={
        'for v in': '从第二个元素开始，依次和 `nums[0]` 比较，当前 `v = {v}`',
        'if v != nums[0]': lambda S, B, r: (f'`{S.v} != {S.nums[0]}` 成立：数组一开始就不全相等' if S.v != S.nums[0] else f'`{S.v} == {S.nums[0]}`：相同，继续看下一个'),
        'return 1': '有不同的数 → 选取整个数组做一次按位与，最后只剩一个值，答案为 ==1==',
        'return 0': '都相等 → 不需要操作，答案为 ==0==',
    },
    cards=dict(
        one_liner='一开始就全相等是 0，否则一次整体按位与就够',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['一次操作可选任意子数组，替换为其所有元素的按位与',
                 '问让 `nums` 所有元素相等的最少操作次数',
                 '示例：`[5,5,3,5,6]`，有不同的数'],
        quote='如果nums中所有元素在一开始就相等，那么答案显然为0，反之，则只需选取整个子数组执行按位与操作，最后就只会剩下按位与结果这一个元素，也就是说答案为1。',
        quote_src='—— yiduobo 题解原文',
        idea=['先看是否已经全相等：是就 0',
              '不是则选整个数组，按位与的结果只有一个值，全部变为它',
              '所以只要扫一遍，遇到和第一个不同的就返回 1'],
        after=[dict(heading='为什么答案只有 0 或 1', lines=['选整个数组按位与，结果是一个数', '整个数组都被替换成它，一次就全相等', '所以不会有 2 次及以上的最优解', '例：`[1,2]` → `[0,0]`，一次完成'])],
        before=[dict(heading='先看两种情况', lines=['情况一：一开始就全相等 → 答案 `0`', '情况二：有不等的数 → 至少要 `1` 次', '按位与操作后，选中的子数组全部变成同一个数', '接下来只要确认 `1` 次够不够'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '答案只有 0 和 1 两种',
                 '遇到第一个不同的数就提前返回，不必扫完'],
    ),
)
