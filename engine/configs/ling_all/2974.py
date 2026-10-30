CONFIG = dict(
    num=2974, title='最小数字游戏', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='排序 + 两两交换',
    tags=[],
    code='''
class Solution:
    def numberGame(self, nums: List[int]) -> List[int]:
        nums.sort()
        for i in range(1, len(nums), 2):
            nums[i - 1], nums[i] = nums[i], nums[i - 1]
        return nums
''',
    call='Solution().numberGame([5,4,2,3,9,7])',
    expect=[3,2,5,4,9,7],
    views=[
        dict(type='text', size=26, fn=lambda S: (f"交换这一对：`nums[{S['i']-1}]` 和 `nums[{S['i']}]`" if 'i' in S and S['_line'] in (5,) else '排好序后，每两个数一对，对内交换')),
        dict(type='array', var='nums', pointers={'i-1': 'blue', 'i': 'pink'}, pointer_labels={'i-1': 'i-1', 'i': 'i'}, cell=96, h=300,
             color=lambda S, k, v: ('green' if 'i' in S and k < S['i'] - 1 and False else None)),
    ],
    watch=[('i', 'i', 'pink')],
    captions={
        'nums.sort()': '先从小到大排序：每一轮取走的最小、次小，正好是相邻的两个数 → `{nums}`',
        'for i in range(1, len(nums), 2)': lambda S, B, r: (f'`i = {S.i}`：处理第 `{S.i//2+1}` 对 `(nums[{S.i-1}], nums[{S.i}])`' if 'i' in S and S.get('i') != B.get('i') else '所有的对都处理完了'),
        'nums[i - 1], nums[i] =': 'Alice 先拿小的、Bob 先放大的 → ==交换这一对==：`{nums[i-1]}` 在前，`{nums[i]}` 在后',
        'return nums': '题目的 `arr` 就是原地改好的 `nums` = `{nums}`',
    },
    cards=dict(
        one_liner='排序之后，两个两个一对交换',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['每轮：Alice 先取最小，Bob 再取次小；然后 Bob 先把他的数放进 `arr`，Alice 再放',
                 '返回最后的 `arr`',
                 '示例：`[5,4,2,3]` → `[3,2,5,4]`；本视频：`[5,4,2,3,9,7]`'],
        quote='该操作等价于，把 nums 从小到大排序，然后从左到右，两个两个一对交换。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每一轮取出的就是剩余数里的最小值和次小值',
              '放进 arr 时==次小值在前、最小值在后==',
              '所以排序后，下标 `(0,1)`、`(2,3)`... 各自交换即可'],
        summary=['时间 `O(n log n)`（瓶颈在排序），空间 `O(1)`',
                 '题目保证长度为偶数，所以 `i` 不会越界',
                 '`range(1, len(nums), 2)` 从 1 开始，每次交换 `i-1` 和 `i`',
                 '另一种写法：切片 `nums[::2], nums[1::2] = nums[1::2], nums[::2]`'],
    ),
)
