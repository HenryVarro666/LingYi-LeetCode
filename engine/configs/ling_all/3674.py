CONFIG = dict(
    num=3674, title='数组元素相等的最小操作次数', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='分类讨论 · 全相等或整体操作',
    tags=['灵神题单', '难度分 1369'],
    code='''
class Solution:
    def minOperations(self, nums: List[int]) -> int:
        return int(any(x != nums[0] for x in nums))
''',
    call='Solution().minOperations([5,5,3,5,6])',
    expect=1,
    views=[
        dict(type='array', var='nums', h=240, label='nums（和 nums[0] 不同的格子标红）',
             color=lambda S, i, v: 'red' if 'nums' in S and v != S['nums'][0] else 'green'),
        dict(type='text', fn=lambda S: f"`nums[0]` = =={S['nums'][0]}==，只要有一个数不等于它，答案就是 1" if 'nums' in S else ''),
    ],
    watch=['nums'],
    captions={
        'return int': lambda S, B, r: (f'`any(x != nums[0] ...)`：{"存在" if r else "不存在"}和 `nums[0] = {S.nums[0]}` 不同的数 → 返回 =={r}=='
                                       + ('，对整个数组做一次按位与，所有元素都变成同一个值' if r else '，本来就全相等，不用操作')),
    },
    cards=dict(
        one_liner='全相等答案 0，否则整体操作一次答案 1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['一次操作：选一个子数组，把它每个元素都替换成这段的按位与',
                 '求让整个数组元素全相等的最少操作次数',
                 '示例：`[1,2]` → `1`，`[5,5,5]` → `0`'],
        quote='如果 nums 所有元素都相等，无需操作，返回 0。否则，由于操作后，子数组所有元素都相等，所以直接操作整个数组，就能让所有元素相等，返回 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['已经全相等 → 0 次',
              '否则选整个数组一次操作，所有元素都变成整体按位与 → 1 次',
              '用 `any` 判断是否存在和 `nums[0]` 不同的数'],
        after=[dict(heading='为什么 1 次就够', lines=['整个数组按位与得到一个数 `t`，整段都被替换成 `t`', '所有元素立刻相等，所以最多 1 次', '按位与只会让数变小或不变，不用管 `t` 具体是多少', '例：`[1,2]` 与 = `0` → `[0,0]`'])],
        before=[dict(heading='先看两种情况', lines=['情况一：所有数本来就相等 → 什么都不用做', '情况二：存在不等的数 → 需要操作', '操作能把一段数变成同一个值', '所以问题变成：最少几次能覆盖整个数组'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '答案只可能是 0 或 1，不用真的算按位与',
                 '`int(True)` 为 1，布尔值直接转整数'],
    ),
)
