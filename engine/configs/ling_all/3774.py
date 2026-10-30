CONFIG = dict(
    num=3774, title='最大和最小 K 个元素的绝对差', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='排序后前后各取 k 个',
    code='''
class Solution:
    def absDifference(self, nums: List[int], k: int) -> int:
        nums.sort()
        return sum(nums[-k:]) - sum(nums[:k])
''',
    call='Solution().absDifference([5,2,7,2,4,1,6,3], 3)',
    expect=13,
    views=[
        dict(type='text', size=34, fn=lambda S: ('排序后：最小 3 个 ==' + str(sum(S['nums'][:S['k']])) + '==，最大 3 个 ==' + str(sum(S['nums'][-S['k']:])) + '==，差 ==' + str(sum(S['nums'][-S['k']:]) - sum(S['nums'][:S['k']])) + '==') if S['nums'] == sorted(S['nums']) else '先排序，最小和最大的 k 个就会各自挤在两端'),
        dict(type='array', var='nums', h=300, label='nums（绿 = 最小的 k 个，粉 = 最大的 k 个）',
             color=lambda S, i, v: ('green' if i < S['k'] else 'pink' if i >= len(S['nums']) - S['k'] else None) if S['nums'] == sorted(S['nums']) else None),
    ],
    watch=['k', ('ans', 'ret', 'green')] if False else ['k'],
    captions={
        'nums.sort()': '从小到大排序：最小的 `k={k}` 个到了最左边，最大的 `k` 个到了最右边 → `{nums}`',
        'return sum': '`nums[-k:]` 是后 {k} 个，和为 =={sum(nums[-k:])}==；`nums[:k]` 是前 {k} 个，和为 =={sum(nums[:k])}==；两者相减 = =={ret}==',
    },
    cards=dict(
        after=[dict(heading='为什么不用写 abs', lines=['排序后，后 k 个每个都不小于前 k 个里的任何一个', '所以后 k 个之和 >= 前 k 个之和，直接相减不会为负', '原文还提到：用快速选择可以做到 `O(n)`'])],
        one_liner='排序后，后 k 个之和减前 k 个之和',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['给整数数组 `nums` 和整数 `k`，求 k 个最大元素之和与 k 个最小元素之和的绝对差',
                 '示例：`nums=[5,2,2,4], k=2` → `9 - 4 = 5`',
                 '演示用：`nums=[5,2,7,2,4,1,6,3], k=3` → `13`'],
        quote='把 nums 从小到大排序，后 k 个数之和减去前 k 个数之和，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后，最大的 k 个一定是末尾 k 个，最小的 k 个一定是开头 k 个',
              '后者之和一定不小于前者之和，所以不用写 `abs`',
              '切片 `nums[-k:]` 和 `nums[:k]` 直接取出两端'],
        summary=['时间 `O(n log n)`；用快速选择可降到 `O(n)`（原文 C++ 第二份代码）',
                 '排序后后 k 个之和 >= 前 k 个之和，所以无需绝对值',
                 '`k = n` 时两段重合，差为 0',
                 '易错点：`nums[-k:]` 取末尾 k 个，不要写成 `nums[-k]`'],
    ),
)
