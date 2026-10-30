CONFIG = dict(
    num=2009, title='使数组连续的最少操作数', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='数轴上的 n 长窗口 + 单调双指针',
    tags=['二、不定长滑动窗口', '难度分 2084'],
    code='''
class Solution(object):
    def minOperations(self, nums):

        n = len(nums)
        sorted_nums = sorted(set(nums))
        m = len(sorted_nums)

        res = n - 1
        now = 1
        left = 0

        while now < m:
            while sorted_nums[now] - sorted_nums[left] >= n:
                left += 1

            res = min(res, n - (now - left + 1))
            now += 1

        return res
''',
    call='Solution().minOperations([1,3,3,4,8,9,10])',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"右边界点 `{S['sorted_nums'][S['now']]}`，窗口内最左点 `{S['sorted_nums'][S['left']]}`，差 `{S['sorted_nums'][S['now']]-S['sorted_nums'][S['left']]}`，要求 ==< {S['n']}==" if 'now' in S and 'left' in S and S['now'] < S['m'] else '')),
        dict(type='array', var='sorted_nums', pointers={'left': 'blue', 'now': 'pink'}, window=('left', 'now'), h=300, label='sorted_nums（数轴上的点）',
             dim=lambda S, i, v: 'left' in S and 'now' in S and not (S['left'] <= i <= S['now'])),
    ],
    watch=['n', ('left', 'left', 'blue'), ('now', 'now', 'pink'), ('res', 'res', 'green')],
    captions={
        'sorted_nums = sorted': '改成数轴上的点：去重再排序 `{sorted_nums}`。题目变成：==长为 n 的窗口最多罩几个点 k==，答案 `n - k`',
        'res = n - 1': '初值 `n - 1`：至少保留 1 个点，最多改 n−1 个',
        'while sorted_nums[now]': '右边界点 `{sorted_nums[now]}` 减最左点 `{sorted_nums[left]}` = `{sorted_nums[now]-sorted_nums[left]}`，{"≥ n，最左点装不进长 n 的窗口" if sorted_nums[now]-sorted_nums[left] >= n else "< n，都在窗口里"}',
        'left += 1': '最左点放不下，`left` 右移到 {left}（右边界右移，最左点只会右移，单调）',
        'res = min': '窗口里有 `{now-left+1}` 个点，要改 `n - {now-left+1} = {n-(now-left+1)}` 个，`res = min({B.res}, ..) = {res}`',
        'now += 1': '右边界换到下一个点：`now` → {now}',
        'return res': '全部点枚举完，最少改 ==`{res}`== 次',
    },
    cards=dict(
        one_liner='把数组看成数轴上的点，找长为 n 的窗口最多罩多少点',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['一次操作可把任意元素改成任意整数',
                 '连续 = ==元素互不相同，最大 − 最小 = n − 1==',
                 '求最少操作次数。示例：`[1,3,3,4,8,9,10]` → `3`'],
        quote='可以证明的是，以数轴上某个点作为窗口右边界时必然能找到最优解。',
        quote_src='—— yiduobo 题解',
        idea=['窗口不是以点为右边界？整体左移到右边界碰到点，==窗口里的点不会变少==',
              '所以排序后枚举每个点当右边界 `now`，最左点 `left` 单调右移',
              '窗口内点数 `now - left + 1`，答案 `n - 最大点数`'],
        summary=['时间 `O(n log n)`，排序是瓶颈；双指针本身 `O(n)`',
                 '易错：==先 set 去重==，否则重复值被算成两个点',
                 '判断条件是 `差 >= n` 才移动 left，差等于 n−1 仍在窗口内'],
    ),
)
