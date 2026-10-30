CONFIG = dict(
    num=2740, title='找出分区值', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='排序 + 相邻差', tags=['难度分 1302'],
    code='''
class Solution:
    def findValueOfPartition(self, nums: List[int]) -> int:
        nums.sort()
        return min(y - x for x, y in pairwise(nums))
''',
    call='Solution().findValueOfPartition([100,1,10,13,4])',
    expect=3,
    views=[
        dict(type='array', var='nums', h=260, label='nums',
             color=lambda S, i, v: None),
        dict(type='text', h=140, size=32, fn=lambda S: (
            '排序后，分区值的最小值一定出现在 ==相邻两数== 之间' if S['_line'] != 4 else
            '相邻差：' + '，'.join(f"`{S['nums'][k+1]}−{S['nums'][k]}={S['nums'][k+1]-S['nums'][k]}`" for k in range(len(S['nums'])-1)))),
    ],
    watch=[('nums', 'nums')],
    captions={
        'nums.sort': '排序后：任意两数的最小绝对差一定在相邻元素之间 → `nums = {nums}`',
        'return': '把 `<= nums[i-1]` 的放进 nums1，`>= nums[i]` 的放进 nums2，分区值就是相邻差；取最小 = =={ret}==',
    },
    cards=dict(
        one_liner='答案的理论最小值，就是任意两数的最小绝对差',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['把正整数数组分成两个非空数组 `nums1`、`nums2`',
                 '分区值 = `|max(nums1) - min(nums2)|`，求最小值',
                 '示例：`[100,1,10]` → `9`'],
        quote='答案的理论最小值，是 nums 任意两个元素绝对差的最小值。实际答案能否取到这个最小值呢？可以的，构造方案如下……',
        quote_src='—— 灵茶山艾府题解',
        idea=['分区值本身就是某两个数的差，所以不会比最小差更小',
              '排序后最小差在相邻元素 `nums[i-1]`、`nums[i]`',
              '小的一半给 nums1、大的一半给 nums2，刚好取到下界'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)`',
                 '易错：`pairwise` 要在排序后用；`nums.sort()` 会原地改数组',
                 '思路：先猜下界，再构造方案取到它'],
        before=[dict(heading='举例：[100,1,10]', lines=['排序得 `[1,10,100]`，相邻差是 `9` 和 `90`', '最小是 `9`：`nums1=[1]`，`nums2=[10,100]`', '分区值 `|1-10|=9`，与示例答案一致'])],
        after=[dict(heading='为什么能取到下界', lines=['排序后 `<= nums[i-1]` 的数都不大于它，放进 nums1，最大值就是它', '`>= nums[i]` 的数放进 nums2，最小值就是 `nums[i]`', '两边都非空（i 从 1 开始），所以构造合法'])],
    ),
)
